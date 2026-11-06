// difftest compara el Gateway Java y el Go con la misma matriz de peticiones y mide latencia.
// Actúa como emisor JWT de PRUEBAS (clave EC efímera en memoria, JWKS en -listen). Los gateways
// deben configurarse con GATEWAY_AUTH_ISSUER_URI=-issuer y GATEWAY_AUTH_JWK_SET_URI=<este>/jwks.
//
//	go run ./tools/difftest -java http://gw-java:8081 -go http://gw-go:8081 -listen :9999
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"sort"
	"strings"
	"sync"
	"time"
)

var key, otherKey *ecdsa.PrivateKey

func b64(b []byte) string { return base64.RawURLEncoding.EncodeToString(b) }

func sign(alg string, c map[string]any, k *ecdsa.PrivateKey) string {
	head, _ := json.Marshal(map[string]string{"alg": alg, "kid": "diff", "typ": "JWT"})
	body, _ := json.Marshal(c)
	input := b64(head) + "." + b64(body)
	d := sha256.Sum256([]byte(input))
	switch alg {
	case "ES256":
		r, s, _ := ecdsa.Sign(rand.Reader, k, d[:])
		sig := make([]byte, 64)
		r.FillBytes(sig[:32])
		s.FillBytes(sig[32:])
		return input + "." + b64(sig)
	case "HS256":
		m := hmac.New(sha256.New, []byte("secret"))
		m.Write([]byte(input))
		return input + "." + b64(m.Sum(nil))
	}
	return input + "."
}

func claims(issuer, role string, mutate func(map[string]any)) map[string]any {
	c := map[string]any{"iss": issuer, "aud": "authenticated", "sub": "diff-user", "role": "authenticated",
		"is_anonymous": false, "iat": time.Now().Unix(), "exp": time.Now().Add(10 * time.Minute).Unix()}
	if role != "" {
		c["user_role"] = role
	}
	if mutate != nil {
		mutate(c)
	}
	return c
}

type tc struct {
	name, method, path, body, token string
	headers                         map[string]string
}

type result struct {
	status                      int
	ctype, acao, reqID, wwwAuth string
}

func call(base string, t tc) (result, error) {
	req, _ := http.NewRequest(t.method, base+t.path, strings.NewReader(t.body))
	if t.token != "" {
		req.Header.Set("Authorization", "Bearer "+t.token)
	}
	for k, v := range t.headers {
		req.Header.Set(k, v)
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return result{}, err
	}
	io.Copy(io.Discard, resp.Body)
	resp.Body.Close()
	ct := strings.SplitN(resp.Header.Get("Content-Type"), ";", 2)[0]
	return result{resp.StatusCode, ct, resp.Header.Get("Access-Control-Allow-Origin"),
		resp.Header.Get("X-Request-Id"), resp.Header.Get("WWW-Authenticate")}, nil
}

func waitHealthy(base string) error {
	for i := 0; i < 180; i++ {
		if r, err := http.Get(base + "/actuator/health/liveness"); err == nil && r.StatusCode == 200 {
			r.Body.Close()
			return nil
		}
		time.Sleep(time.Second)
	}
	return fmt.Errorf("%s no respondió", base)
}

func load(base, path, token string, want, n, conc int) (p50, p95 time.Duration, rps float64, errs int) {
	lat := make([]time.Duration, n)
	var mu sync.Mutex
	var wg sync.WaitGroup
	jobs := make(chan int)
	start := time.Now()
	for w := 0; w < conc; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := range jobs {
				t0 := time.Now()
				r, err := call(base, tc{method: "GET", path: path, token: token})
				lat[i] = time.Since(t0)
				if err != nil || r.status != want {
					mu.Lock()
					errs++
					mu.Unlock()
				}
			}
		}()
	}
	for i := 0; i < n; i++ {
		jobs <- i
	}
	close(jobs)
	wg.Wait()
	total := time.Since(start)
	sort.Slice(lat, func(a, b int) bool { return lat[a] < lat[b] })
	return lat[n/2], lat[n*95/100], float64(n) / total.Seconds(), errs
}

func main() {
	javaURL := flag.String("java", "", "")
	goURL := flag.String("go", "", "")
	listen := flag.String("listen", ":9999", "")
	issuer := flag.String("issuer", "https://difftest.local/auth/v1", "")
	origin := flag.String("origin", "http://127.0.0.1:13001", "")
	n := flag.Int("n", 2000, "peticiones de carga por gateway")
	flag.Parse()
	key, _ = ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	otherKey, _ = ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	http.HandleFunc("/jwks", func(w http.ResponseWriter, _ *http.Request) {
		x, y := make([]byte, 32), make([]byte, 32)
		key.PublicKey.X.FillBytes(x)
		key.PublicKey.Y.FillBytes(y)
		json.NewEncoder(w).Encode(map[string]any{"keys": []map[string]string{
			{"kty": "EC", "crv": "P-256", "kid": "diff", "use": "sig", "alg": "ES256", "x": b64(x), "y": b64(y)}}})
	})
	go http.ListenAndServe(*listen, nil)
	for _, b := range []string{*javaURL, *goURL} {
		if err := waitHealthy(b); err != nil {
			fmt.Println("ERROR", err)
			os.Exit(2)
		}
	}
	ok := func(role string) string { return sign("ES256", claims(*issuer, role, nil), key) }
	mut := func(f func(map[string]any)) string { return sign("ES256", claims(*issuer, "ADMIN", f), key) }
	now := time.Now().UTC()
	window := "start=" + now.Add(-10*time.Minute).Format(time.RFC3339) + "&end=" + now.Add(-time.Minute).Format(time.RFC3339)
	cases := []tc{
		{name: "sin token", method: "GET", path: "/api/monitoring/v1/metrics/catalog"},
		{name: "catálogo ADMIN", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: ok("ADMIN")},
		{name: "current OPERATOR + request id", method: "GET", path: "/api/monitoring/v1/metrics/current?metric=node.cpu.utilization", token: ok("OPERATOR"), headers: map[string]string{"X-Request-Id": "diff-1"}},
		{name: "monitoring métrica inválida (422 upstream)", method: "GET", path: "/api/monitoring/v1/metrics/current?metric=nope", token: ok("ADMIN")},
		{name: "processing history", method: "GET", path: "/api/processing/v1/metrics/history?metric=node.cpu.utilization&stepSeconds=60&" + window, token: ok("ADMIN")},
		{name: "historical-logs", method: "GET", path: "/api/processing/v1/historical-logs?hardwareId=HW045&start=2026-07-10T00:00:00Z&end=2026-07-11T00:00:00Z&limit=2", token: ok("ADMIN")},
		{name: "predicción cuerpo inválido (422 upstream)", method: "POST", path: "/api/prediction/v1/predictions", body: `{}`, token: ok("ADMIN"), headers: map[string]string{"Content-Type": "application/json"}},
		{name: "recomendación inválida", method: "POST", path: "/api/recommendations/v1/recommendations", body: `{"dataset":{}}`, token: ok("OPERATOR"), headers: map[string]string{"Content-Type": "application/json"}},
		{name: "rol ROOT", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: ok("ROOT")},
		{name: "sin rol", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: ok("")},
		{name: "método no publicado", method: "POST", path: "/api/monitoring/v1/metrics/catalog", token: ok("ADMIN")},
		{name: "ruta no publicada", method: "GET", path: "/api/processing/v1/anything", token: ok("ADMIN")},
		{name: "ruta no publicada sin token", method: "GET", path: "/api/unknown"},
		{name: "actuator prometheus con token", method: "GET", path: "/actuator/prometheus", token: ok("ADMIN")},
		{name: "emisor erróneo", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["iss"] = "https://x" })},
		{name: "audiencia errónea", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["aud"] = "x" })},
		{name: "expirado 2 min", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["exp"] = time.Now().Add(-2 * time.Minute).Unix() })},
		{name: "expirado 30 s", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["exp"] = time.Now().Add(-30 * time.Second).Unix() })},
		{name: "expirado 5 s", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["exp"] = time.Now().Add(-5 * time.Second).Unix() })},
		{name: "expirado 1 s", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["exp"] = time.Now().Add(-1 * time.Second).Unix() })},
		{name: "nbf futuro 2 min", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["nbf"] = time.Now().Add(2 * time.Minute).Unix() })},
		{name: "nbf futuro 20 s", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["nbf"] = time.Now().Add(20 * time.Second).Unix() })},
		{name: "sub vacío", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["sub"] = " " })},
		{name: "aud en lista", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["aud"] = []string{"x", "authenticated"} })},
		{name: "role anon", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["role"] = "anon" })},
		{name: "is_anonymous", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: mut(func(c map[string]any) { c["is_anonymous"] = true })},
		{name: "otra clave", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: sign("ES256", claims(*issuer, "ADMIN", nil), otherKey)},
		{name: "alg none", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: sign("none", claims(*issuer, "ADMIN", nil), nil)},
		{name: "HS256", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: sign("HS256", claims(*issuer, "ADMIN", nil), nil)},
		{name: "Basic", method: "GET", path: "/api/monitoring/v1/metrics/catalog", headers: map[string]string{"Authorization": "Basic Zm9vOmJhcg=="}},
		{name: "preflight ok", method: "OPTIONS", path: "/api/prediction/v1/predictions", headers: map[string]string{"Origin": *origin, "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "authorization,content-type"}},
		{name: "preflight otro origen", method: "OPTIONS", path: "/api/monitoring/v1/metrics/catalog", headers: map[string]string{"Origin": "https://evil.test", "Access-Control-Request-Method": "GET"}},
		{name: "preflight método DELETE", method: "OPTIONS", path: "/api/monitoring/v1/metrics/catalog", headers: map[string]string{"Origin": *origin, "Access-Control-Request-Method": "DELETE"}},
		{name: "simple con origen permitido", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: ok("ADMIN"), headers: map[string]string{"Origin": *origin}},
		{name: "simple con otro origen", method: "GET", path: "/api/monitoring/v1/metrics/catalog", token: ok("ADMIN"), headers: map[string]string{"Origin": "https://evil.test"}},
		{name: "cuerpo > 2 MB", method: "POST", path: "/api/prediction/v1/predictions", body: strings.Repeat("a", 2<<20+10), token: ok("ADMIN"), headers: map[string]string{"Content-Type": "application/json"}},
		{name: "cabecera 17 KB", method: "GET", path: "/api/unknown", headers: map[string]string{"X-Big": strings.Repeat("a", 17000)}},
		{name: "health liveness", method: "GET", path: "/actuator/health/liveness"},
		{name: "openapi", method: "GET", path: "/openapi/gateway-v0.1.yaml"},
	}
	mismatches := 0
	fmt.Printf("%-44s %-26s %-26s %s\n", "caso", "java (estado ctype acao)", "go", "")
	for _, c := range cases {
		j, ej := call(*javaURL, c)
		g, eg := call(*goURL, c)
		same := ej == nil && eg == nil && j.status == g.status && (j.acao != "") == (g.acao != "") &&
			(j.wwwAuth != "") == (g.wwwAuth != "") &&
			(c.headers["X-Request-Id"] == "" || (j.reqID == c.headers["X-Request-Id"] && g.reqID == c.headers["X-Request-Id"]))
		mark := "="
		if !same {
			mark = "DIFERENTE"
			mismatches++
		}
		fmt.Printf("%-44s %-26s %-26s %s\n", c.name, fmt.Sprintf("%d %s %t", j.status, short(j.ctype), j.acao != ""),
			fmt.Sprintf("%d %s %t", g.status, short(g.ctype), g.acao != ""), mark)
	}
	fmt.Printf("\nDiferencias: %d de %d casos\n\n", mismatches, len(cases))
	for _, target := range []struct{ name, base string }{{"java", *javaURL}, {"go", *goURL}} {
		for _, p := range []struct {
			name, path, token string
			want              int
		}{
			{"proxy catálogo (ADMIN)", "/api/monitoring/v1/metrics/catalog", ok("ADMIN"), 200},
			{"rechazo 401 (sin token)", "/api/monitoring/v1/metrics/catalog", "", 401},
		} {
			load(target.base, p.path, p.token, p.want, 200, 8) // calentamiento
			p50, p95, rps, errs := load(target.base, p.path, p.token, p.want, *n, 16)
			fmt.Printf("CARGA %-5s %-24s n=%d conc=16 p50=%v p95=%v rps=%.0f inesperados=%d\n", target.name, p.name, *n,
				p50.Round(10*time.Microsecond), p95.Round(10*time.Microsecond), rps, errs)
		}
	}
	if mismatches > 0 {
		os.Exit(1)
	}
}

func short(ct string) string {
	if ct == "" {
		return "-"
	}
	return strings.TrimPrefix(strings.TrimPrefix(ct, "application/"), "vnd.spring-boot.actuator.v3+")
}
