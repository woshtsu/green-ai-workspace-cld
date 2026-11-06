package auth

import (
	"bytes"
	"context"
	"crypto"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"math/big"
	"net/http"
	"strings"
	"sync"
	"time"
)

// JWKSVerifier valida JWT firmados con ES256 o RS256 contra un JWKS remoto (adaptador de salida).
// Reglas equivalentes al Gateway Java (NimbusReactiveJwtDecoder + validadores):
// iss exacto, aud contiene la audiencia, exp obligatorio, nbf opcional,
// sub no vacío, role == "authenticated" e is_anonymous != true.
// Holguras medidas con la prueba diferencial contra el Gateway Java (Spring Security 7):
// exp sin holgura (rechaza un token expirado hace 1 s); nbf con 60 s (acepta +20 s, rechaza +2 min).
type JWKSVerifier struct {
	Issuer   string
	Audience string
	JWKSURL  string
	Client   *http.Client
	Now      func() time.Time
	Skew     time.Duration // holgura para exp
	NbfSkew  time.Duration // holgura para nbf
	CacheTTL time.Duration
	// MinRefresh limita la recarga del JWKS ante un kid desconocido.
	MinRefresh time.Duration

	// mu protege el almacén; refreshMu serializa las descargas (nunca se mantiene mu durante la red).
	mu          sync.RWMutex
	keys        []jwk
	fetched     time.Time
	nextAttempt time.Time // tras un fallo o una recarga, no reintentar antes (evita DoS por recarga)
	refreshMu   sync.Mutex
}

type jwk struct {
	kid string
	key crypto.PublicKey
}

func NewJWKSVerifier(issuer, audience, jwksURL string) *JWKSVerifier {
	return &JWKSVerifier{Issuer: issuer, Audience: audience, JWKSURL: jwksURL,
		Client: &http.Client{Timeout: 5 * time.Second}, Now: time.Now, Skew: 0, NbfSkew: 60 * time.Second,
		CacheTTL: 5 * time.Minute, MinRefresh: 30 * time.Second}
}

func (v *JWKSVerifier) Verify(ctx context.Context, token string) (Principal, error) {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return Principal{}, ErrInvalidToken
	}
	var header struct {
		Alg string `json:"alg"`
		Kid string `json:"kid"`
		Typ string `json:"typ"`
	}
	if err := decodeJSON(parts[0], &header); err != nil {
		return Principal{}, ErrInvalidToken
	}
	if header.Alg != "ES256" && header.Alg != "RS256" {
		return Principal{}, ErrInvalidToken // rechaza none, HS256 y cualquier otro
	}
	if header.Typ != "" && !strings.EqualFold(header.Typ, "JWT") {
		return Principal{}, ErrInvalidToken
	}
	sig, err := base64.RawURLEncoding.DecodeString(parts[2])
	if err != nil {
		return Principal{}, ErrInvalidToken
	}
	keys, err := v.candidates(header.Kid)
	if err != nil {
		return Principal{}, err
	}
	digest := sha256.Sum256([]byte(parts[0] + "." + parts[1]))
	verified := false
	for _, k := range keys {
		if verifySignature(header.Alg, k.key, digest[:], sig) {
			verified = true
			break
		}
	}
	if !verified {
		return Principal{}, ErrInvalidToken
	}
	return v.validateClaims(parts[1])
}

func verifySignature(alg string, key crypto.PublicKey, digest, sig []byte) bool {
	switch k := key.(type) {
	case *ecdsa.PublicKey:
		if alg != "ES256" || k.Curve != elliptic.P256() || len(sig) != 64 {
			return false
		}
		r, s := new(big.Int).SetBytes(sig[:32]), new(big.Int).SetBytes(sig[32:])
		return ecdsa.Verify(k, digest, r, s)
	case *rsa.PublicKey:
		return alg == "RS256" && rsa.VerifyPKCS1v15(k, crypto.SHA256, digest, sig) == nil
	}
	return false
}

func (v *JWKSVerifier) validateClaims(payload string) (Principal, error) {
	var c map[string]any
	if err := decodeJSON(payload, &c); err != nil {
		return Principal{}, ErrInvalidToken
	}
	now := v.Now()
	if iss, _ := c["iss"].(string); iss != v.Issuer {
		return Principal{}, ErrInvalidToken
	}
	if !audienceContains(c["aud"], v.Audience) {
		return Principal{}, ErrInvalidToken
	}
	exp, ok := numericDate(c["exp"])
	if !ok || now.After(exp.Add(v.Skew)) {
		return Principal{}, ErrInvalidToken
	}
	if raw, present := c["nbf"]; present {
		nbf, ok := numericDate(raw)
		if !ok || now.Before(nbf.Add(-v.NbfSkew)) {
			return Principal{}, ErrInvalidToken
		}
	}
	sub, _ := c["sub"].(string)
	if strings.TrimSpace(sub) == "" {
		return Principal{}, ErrInvalidToken
	}
	if role, _ := c["role"].(string); role != "authenticated" {
		return Principal{}, ErrInvalidToken
	}
	if anon, _ := c["is_anonymous"].(bool); anon {
		return Principal{}, ErrInvalidToken
	}
	userRole, _ := c["user_role"].(string)
	return Principal{Subject: sub, Role: userRole}, nil
}

func audienceContains(raw any, want string) bool {
	switch a := raw.(type) {
	case string:
		return a == want
	case []any:
		for _, x := range a {
			if s, _ := x.(string); s == want {
				return true
			}
		}
	}
	return false
}

func numericDate(raw any) (time.Time, bool) {
	n, ok := raw.(json.Number)
	if !ok {
		return time.Time{}, false
	}
	f, err := n.Float64()
	if err != nil {
		return time.Time{}, false
	}
	return time.Unix(int64(f), 0), true
}

func decodeJSON(segment string, out any) error {
	raw, err := base64.RawURLEncoding.DecodeString(segment)
	if err != nil {
		return err
	}
	dec := json.NewDecoder(bytes.NewReader(raw))
	dec.UseNumber()
	return dec.Decode(out)
}

// candidates devuelve las claves aplicables. Con claves en caché válidas no toca la red. Si caducó el TTL y
// hay claves utilizables, recarga en segundo plano y responde con las actuales. Solo espera la red cuando no hay
// ninguna clave aplicable (primer arranque o kid nuevo), y como máximo una descarga por MinRefresh.
func (v *JWKSVerifier) candidates(kid string) ([]jwk, error) {
	keys, fetched, next := v.snapshot()
	now := v.Now()
	match := filter(keys, kid)
	stale := keys == nil || now.Sub(fetched) > v.CacheTTL
	if (stale || len(match) == 0) && !now.Before(next) {
		if len(match) > 0 {
			go func() {
				if v.refreshMu.TryLock() {
					defer v.refreshMu.Unlock()
					if _, _, n := v.snapshot(); !v.Now().Before(n) { // otra recarga pudo terminar antes
						v.refresh()
					}
				}
			}()
		} else {
			v.refreshMu.Lock()
			if _, _, n := v.snapshot(); !v.Now().Before(n) { // otro pudo recargar mientras esperábamos
				v.refresh()
			}
			v.refreshMu.Unlock()
			keys, _, _ = v.snapshot()
			match = filter(keys, kid)
		}
	}
	if keys == nil {
		return nil, ErrUnavailable
	}
	if len(match) == 0 {
		return nil, ErrInvalidToken
	}
	return match, nil
}

func (v *JWKSVerifier) snapshot() ([]jwk, time.Time, time.Time) {
	v.mu.RLock()
	defer v.mu.RUnlock()
	return v.keys, v.fetched, v.nextAttempt
}

func filter(keys []jwk, kid string) []jwk {
	if kid == "" {
		return keys
	}
	var out []jwk
	for _, k := range keys {
		if k.kid == kid {
			out = append(out, k)
		}
	}
	return out
}

// refresh descarga el JWKS con un contexto propio (no el del cliente, que puede cancelarse) y fija el backoff.
func (v *JWKSVerifier) refresh() {
	keys, err := v.fetch()
	now := v.Now()
	v.mu.Lock()
	defer v.mu.Unlock()
	v.nextAttempt = now.Add(v.MinRefresh)
	if err == nil {
		v.keys, v.fetched = keys, now
	}
}

func (v *JWKSVerifier) fetch() ([]jwk, error) {
	ctx, cancel := context.WithTimeout(context.Background(), v.Client.Timeout)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, v.JWKSURL, nil)
	if err != nil {
		return nil, err
	}
	resp, err := v.Client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("jwks: estado %d", resp.StatusCode)
	}
	var set struct {
		Keys []struct {
			Kty, Kid, Use, Crv, X, Y, N, E string
		} `json:"keys"`
	}
	if err := json.NewDecoder(io.LimitReader(resp.Body, 1<<20)).Decode(&set); err != nil {
		return nil, err
	}
	var keys []jwk
	for _, k := range set.Keys {
		if k.Use != "" && k.Use != "sig" {
			continue
		}
		switch k.Kty {
		case "EC":
			if k.Crv != "P-256" {
				continue
			}
			x, ex := base64.RawURLEncoding.DecodeString(k.X)
			y, ey := base64.RawURLEncoding.DecodeString(k.Y)
			if ex != nil || ey != nil {
				continue
			}
			pub := &ecdsa.PublicKey{Curve: elliptic.P256(), X: new(big.Int).SetBytes(x), Y: new(big.Int).SetBytes(y)}
			if !pub.Curve.IsOnCurve(pub.X, pub.Y) {
				continue
			}
			keys = append(keys, jwk{k.Kid, pub})
		case "RSA":
			n, en := base64.RawURLEncoding.DecodeString(k.N)
			e, ee := base64.RawURLEncoding.DecodeString(k.E)
			if en != nil || ee != nil || len(e) > 4 {
				continue
			}
			pub := &rsa.PublicKey{N: new(big.Int).SetBytes(n), E: int(new(big.Int).SetBytes(e).Int64())}
			if pub.N.BitLen() < 2048 || pub.E < 3 || pub.E%2 == 0 {
				continue // exige RSA >= 2048 bits y exponente impar >= 3
			}
			keys = append(keys, jwk{k.Kid, pub})
		}
	}
	if keys == nil {
		keys = []jwk{} // JWKS vacío válido: se distingue de "nunca descargado"
	}
	return keys, nil
}
