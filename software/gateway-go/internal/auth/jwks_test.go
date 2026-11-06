package auth

// Pruebas del adaptador JWKS centradas en la recarga (revisión 03, hallazgos 1, 2, 3 y 7).

import (
	"context"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"math/big"
	"net/http"
	"net/http/httptest"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

type fakeIssuer struct {
	key   *ecdsa.PrivateKey
	extra []map[string]string
	hits  atomic.Int32
	fail  atomic.Bool
	delay atomic.Int64
	srv   *httptest.Server
}

func b64(b []byte) string { return base64.RawURLEncoding.EncodeToString(b) }

func newIssuer(t *testing.T) *fakeIssuer {
	f := &fakeIssuer{}
	f.key, _ = ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	f.srv = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		f.hits.Add(1)
		time.Sleep(time.Duration(f.delay.Load()))
		if f.fail.Load() {
			w.WriteHeader(500)
			return
		}
		x, y := make([]byte, 32), make([]byte, 32)
		f.key.PublicKey.X.FillBytes(x)
		f.key.PublicKey.Y.FillBytes(y)
		keys := append([]map[string]string{{"kty": "EC", "crv": "P-256", "kid": "k1", "x": b64(x), "y": b64(y)}}, f.extra...)
		json.NewEncoder(w).Encode(map[string]any{"keys": keys})
	}))
	t.Cleanup(f.srv.Close)
	return f
}

func (f *fakeIssuer) token(kid string) string {
	head, _ := json.Marshal(map[string]string{"alg": "ES256", "kid": kid})
	body, _ := json.Marshal(map[string]any{"iss": "iss", "aud": "authenticated", "sub": "u", "role": "authenticated",
		"exp": time.Now().Add(time.Hour).Unix(), "user_role": "ADMIN"})
	in := b64(head) + "." + b64(body)
	d := sha256.Sum256([]byte(in))
	r, s, _ := ecdsa.Sign(rand.Reader, f.key, d[:])
	sig := make([]byte, 64)
	r.FillBytes(sig[:32])
	s.FillBytes(sig[32:])
	return in + "." + b64(sig)
}

type clock struct {
	mu sync.Mutex
	t  time.Time
}

func (c *clock) now() time.Time {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.t
}

func (c *clock) add(d time.Duration) {
	c.mu.Lock()
	c.t = c.t.Add(d)
	c.mu.Unlock()
}

func verifier(f *fakeIssuer, c *clock) *JWKSVerifier {
	v := NewJWKSVerifier("iss", "authenticated", f.srv.URL)
	v.Now = c.now
	return v
}

func TestFailedRefreshBacksOffAndKeepsServingCachedKeys(t *testing.T) {
	f, c := newIssuer(t), &clock{t: time.Now()}
	v := verifier(f, c)
	tok := f.token("k1")
	if _, err := v.Verify(context.Background(), tok); err != nil {
		t.Fatal(err)
	}
	f.fail.Store(true)
	c.add(6 * time.Minute) // TTL caducado
	for i := 0; i < 50; i++ {
		if _, err := v.Verify(context.Background(), tok); err != nil {
			t.Fatalf("con claves en caché no debe fallar: %v", err)
		}
	}
	time.Sleep(200 * time.Millisecond) // deja terminar la recarga en segundo plano
	if h := f.hits.Load(); h > 2 {
		t.Fatalf("recargas tras fallo sin backoff: %d descargas", h)
	}
}

func TestSlowJWKSDoesNotBlockCachedVerification(t *testing.T) {
	f, c := newIssuer(t), &clock{t: time.Now()}
	v := verifier(f, c)
	tok := f.token("k1")
	v.Verify(context.Background(), tok)
	f.delay.Store(int64(2 * time.Second))
	c.add(6 * time.Minute)
	start := time.Now()
	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func() { defer wg.Done(); v.Verify(context.Background(), tok) }()
	}
	wg.Wait()
	if d := time.Since(start); d > time.Second {
		t.Fatalf("verificaciones bloqueadas por la recarga: %v", d)
	}
}

func TestUnknownKidRefreshIsRateLimited(t *testing.T) {
	f, c := newIssuer(t), &clock{t: time.Now()}
	v := verifier(f, c)
	v.Verify(context.Background(), f.token("k1"))
	for i := 0; i < 100; i++ {
		if _, err := v.Verify(context.Background(), f.token("nope")); err != ErrInvalidToken {
			t.Fatalf("kid desconocido: %v", err)
		}
	}
	if h := f.hits.Load(); h > 1 {
		t.Fatalf("kid desconocido provocó %d descargas dentro de MinRefresh", h)
	}
}

func TestCanceledClientContextDoesNotAbortFetch(t *testing.T) {
	f, c := newIssuer(t), &clock{t: time.Now()}
	v := verifier(f, c)
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if _, err := v.Verify(ctx, f.token("k1")); err != nil {
		t.Fatalf("la descarga usa su propio contexto: %v", err)
	}
}

func TestFirstFetchFailureIsUnavailableAndBackedOff(t *testing.T) {
	f, c := newIssuer(t), &clock{t: time.Now()}
	f.fail.Store(true)
	v := verifier(f, c)
	for i := 0; i < 10; i++ {
		if _, err := v.Verify(context.Background(), f.token("k1")); err != ErrUnavailable {
			t.Fatalf("se esperaba ErrUnavailable: %v", err)
		}
	}
	if h := f.hits.Load(); h != 1 {
		t.Fatalf("%d descargas sin backoff", h)
	}
}

func TestWeakRSAKeysAreIgnored(t *testing.T) {
	f, c := newIssuer(t), &clock{t: time.Now()}
	weak, _ := rsa.GenerateKey(rand.Reader, 1024)
	e := b64(big.NewInt(65537).Bytes())
	f.extra = []map[string]string{
		{"kty": "RSA", "kid": "weak", "n": b64(weak.N.Bytes()), "e": e},
		{"kty": "RSA", "kid": "padded", "n": b64(append(make([]byte, 160), weak.N.Bytes()...)), "e": e},
	}
	v := verifier(f, c)
	v.Verify(context.Background(), f.token("k1"))
	keys, _, _ := v.snapshot()
	if len(keys) != 1 {
		t.Fatalf("claves RSA débiles aceptadas: %d claves", len(keys))
	}
}
