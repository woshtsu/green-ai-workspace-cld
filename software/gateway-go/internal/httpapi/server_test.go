package httpapi

// Equivalencia con software/gateway/src/test/java/.../GatewayApplicationTests.java (11 casos, mismos nombres
// en comentarios) más casos inválidos adicionales.

import (
	"crypto"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/hmac"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"io"
	"math/big"
	"net/http"
	"net/http/httptest"
	"net/http/httputil"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"greenai/gateway/internal/auth"
	"greenai/gateway/internal/policy"
)

const issuer = "https://auth.test/auth/v1"
const allowedOrigin = "http://127.0.0.1:3001"

type env struct {
	t        *testing.T
	gw       *httptest.Server
	ecKey    *ecdsa.PrivateKey
	rsaKey   *rsa.PrivateKey
	jwksDown bool
	slow     time.Duration
}

func b64(b []byte) string { return base64.RawURLEncoding.EncodeToString(b) }

func newEnv(t *testing.T) *env {
	t.Helper()
	e := &env{t: t}
	e.ecKey, _ = ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	e.rsaKey, _ = rsa.GenerateKey(rand.Reader, 2048)
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if e.slow > 0 {
			time.Sleep(e.slow)
		}
		switch {
		case r.URL.Path == "/jwks":
			if e.jwksDown {
				w.WriteHeader(500)
				return
			}
			ecPub := e.ecKey.PublicKey
			x, y := make([]byte, 32), make([]byte, 32)
			ecPub.X.FillBytes(x)
			ecPub.Y.FillBytes(y)
			json.NewEncoder(w).Encode(map[string]any{"keys": []map[string]string{
				{"kty": "EC", "crv": "P-256", "kid": "test", "use": "sig", "x": b64(x), "y": b64(y)},
				{"kty": "RSA", "kid": "rsa", "n": b64(e.rsaKey.N.Bytes()), "e": b64(big.NewInt(int64(e.rsaKey.E)).Bytes())},
			}})
		case contains([]string{"/v1/predictions", "/v1/recommendations", "/v1/energy"}, r.URL.Path):
			w.Header().Set("Content-Type", "application/json")
			io.Copy(w, r.Body)
		case strings.HasPrefix(r.URL.Path, "/api/v1/prediction/dataset"):
			w.Header().Set("X-Request-Id", r.Header.Get("X-Request-Id"))
			w.Header().Set("Content-Type", "application/problem+json")
			w.WriteHeader(422)
			io.WriteString(w, `{"status":422,"detail":"invalid query"}`)
		case r.URL.Path == "/api/v1/metrics/catalog":
			io.WriteString(w, "xff="+r.Header.Get("X-Forwarded-For")+";host="+r.Header.Get("X-Forwarded-Host"))
		default:
			w.Header().Set("X-Request-Id", "upstream-must-not-win")
			io.WriteString(w, r.URL.RequestURI())
		}
	}))
	t.Cleanup(upstream.Close)
	u, _ := url.Parse(upstream.URL)
	dir := t.TempDir()
	os.WriteFile(filepath.Join(dir, "gateway-v0.1.yaml"), []byte("openapi: 3.1.0\n"), 0o644)
	verifier := auth.NewJWKSVerifier(issuer, "authenticated", upstream.URL+"/jwks")
	srv, err := New(Config{Upstreams: map[policy.Upstream]*url.URL{policy.Monitoring: u, policy.DataProcessing: u, policy.Prediction: u},
		AllowedOrigin: allowedOrigin, OpenAPIDir: dir}, verifier)
	if err != nil {
		t.Fatal(err)
	}
	e.gw = httptest.NewServer(srv)
	t.Cleanup(e.gw.Close)
	return e
}

type claims map[string]any

func (e *env) baseClaims(role string) claims {
	c := claims{"iss": issuer, "aud": "authenticated", "sub": "user-test", "iat": time.Now().Add(-time.Second).Unix(),
		"exp": time.Now().Add(5 * time.Minute).Unix(), "role": "authenticated", "is_anonymous": false}
	if role != "" {
		c["user_role"] = role
	}
	return c
}

func (e *env) sign(alg, kid string, c claims, key any) string {
	head, _ := json.Marshal(map[string]string{"alg": alg, "kid": kid, "typ": "JWT"})
	body, _ := json.Marshal(c)
	input := b64(head) + "." + b64(body)
	digest := sha256.Sum256([]byte(input))
	var sig []byte
	switch k := key.(type) {
	case *ecdsa.PrivateKey:
		r, s, _ := ecdsa.Sign(rand.Reader, k, digest[:])
		sig = make([]byte, 64)
		r.FillBytes(sig[:32])
		s.FillBytes(sig[32:])
	case *rsa.PrivateKey:
		sig, _ = rsa.SignPKCS1v15(rand.Reader, k, crypto.SHA256, digest[:])
	case []byte:
		m := hmac.New(sha256.New, k)
		m.Write([]byte(input))
		sig = m.Sum(nil)
	case nil:
		sig = nil
	}
	return input + "." + b64(sig)
}

func (e *env) valid(role string) string { return e.sign("ES256", "test", e.baseClaims(role), e.ecKey) }

type req struct {
	method, path, token, body string
	headers                   map[string]string
}

func (e *env) do(r req) (*http.Response, string) {
	e.t.Helper()
	if r.method == "" {
		r.method = "GET"
	}
	hr, _ := http.NewRequest(r.method, e.gw.URL+r.path, strings.NewReader(r.body))
	if r.token != "" {
		hr.Header.Set("Authorization", "Bearer "+r.token)
	}
	for k, v := range r.headers {
		hr.Header.Set(k, v)
	}
	resp, err := http.DefaultClient.Do(hr)
	if err != nil {
		e.t.Fatal(err)
	}
	defer resp.Body.Close()
	b, _ := io.ReadAll(resp.Body)
	return resp, string(b)
}

func expect(t *testing.T, resp *http.Response, status int) {
	t.Helper()
	if resp.StatusCode != status {
		t.Fatalf("%s %s: estado %d, se esperaba %d", resp.Request.Method, resp.Request.URL.Path, resp.StatusCode, status)
	}
}

const path = "/api/monitoring/v1/metrics/current?metric=node.cpu.utilization&resourceType=node"

// requiresToken
func TestRequiresToken(t *testing.T) {
	e := newEnv(t)
	resp, body := e.do(req{path: path})
	expect(t, resp, 401)
	if resp.Header.Get("Content-Type") != "application/problem+json" || resp.Header.Get("X-Request-Id") == "" ||
		resp.Header.Get("WWW-Authenticate") != "Bearer" || !strings.Contains(body, `"status":401`) {
		t.Fatalf("respuesta 401 incompleta: %v %s", resp.Header, body)
	}
}

// operatorAndAdminReachOnlyConfirmedRoute
func TestOperatorAndAdminReachOnlyConfirmedRoute(t *testing.T) {
	e := newEnv(t)
	for _, role := range []string{"OPERATOR", "ADMIN"} {
		resp, body := e.do(req{path: path, token: e.valid(role), headers: map[string]string{"X-Request-Id": "browser-42"}})
		expect(t, resp, 200)
		if got := resp.Header.Values("X-Request-Id"); len(got) != 1 || got[0] != "browser-42" {
			t.Fatalf("X-Request-Id %v", got)
		}
		if body != "/api/v1/metrics/current?metric=node.cpu.utilization&resourceType=node" {
			t.Fatalf("ruta reenviada %q", body)
		}
	}
}

// rejectsInvalidTokens (+ casos adicionales)
func TestRejectsInvalidTokens(t *testing.T) {
	e := newEnv(t)
	other, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	mut := func(f func(claims)) string {
		c := e.baseClaims("ADMIN")
		f(c)
		return e.sign("ES256", "test", c, e.ecKey)
	}
	cases := map[string]string{
		"malformado":        "invalid",
		"emisor":            mut(func(c claims) { c["iss"] = "https://wrong.test" }),
		"audiencia":         mut(func(c claims) { c["aud"] = "wrong" }),
		"expirado 120 s":    mut(func(c claims) { c["exp"] = time.Now().Add(-120 * time.Second).Unix() }),
		"sin exp":           mut(func(c claims) { delete(c, "exp") }),
		"nbf futuro":        mut(func(c claims) { c["nbf"] = time.Now().Add(10 * time.Minute).Unix() }),
		"sub vacío":         mut(func(c claims) { c["sub"] = " " }),
		"role anon":         mut(func(c claims) { c["role"] = "anon" }),
		"is_anonymous":      mut(func(c claims) { c["is_anonymous"] = true }),
		"otra clave":        e.sign("ES256", "test", e.baseClaims("ADMIN"), other),
		"kid desconocido":   e.sign("ES256", "nope", e.baseClaims("ADMIN"), e.ecKey),
		"alg none":          e.sign("none", "test", e.baseClaims("ADMIN"), nil),
		"HS256 confusión":   e.sign("HS256", "test", e.baseClaims("ADMIN"), []byte("secret")),
		"ES256 con kid RSA": e.sign("ES256", "rsa", e.baseClaims("ADMIN"), e.ecKey),
	}
	for name, token := range cases {
		resp, _ := e.do(req{path: path, token: token})
		if resp.StatusCode != 401 {
			t.Errorf("%s: estado %d, se esperaba 401", name, resp.StatusCode)
		}
	}
	resp, _ := e.do(req{path: path, headers: map[string]string{"Authorization": "Basic Zm9vOmJhcg=="}})
	expect(t, resp, 401)
	// Sin holgura, como el Gateway Java medido en la prueba diferencial.
	resp, _ = e.do(req{path: path, token: mut(func(c claims) { c["exp"] = time.Now().Add(-5 * time.Second).Unix() })})
	expect(t, resp, 401)
	resp, _ = e.do(req{path: path, token: mut(func(c claims) { c["exp"] = time.Now().Add(-1 * time.Second).Unix() })})
	expect(t, resp, 401)
	// nbf dentro de la holgura de 60 s, como Java.
	resp, _ = e.do(req{path: path, token: mut(func(c claims) { c["nbf"] = time.Now().Add(20 * time.Second).Unix() })})
	expect(t, resp, 200)
	// Audiencia como lista.
	resp, _ = e.do(req{path: path, token: mut(func(c claims) { c["aud"] = []string{"x", "authenticated"} })})
	expect(t, resp, 200)
}

func TestRS256Accepted(t *testing.T) {
	e := newEnv(t)
	resp, _ := e.do(req{path: path, token: e.sign("RS256", "rsa", e.baseClaims("OPERATOR"), e.rsaKey)})
	expect(t, resp, 200)
}

// missingOrUnknownRoleIsForbidden
func TestMissingOrUnknownRoleIsForbidden(t *testing.T) {
	e := newEnv(t)
	for _, role := range []string{"", "ROOT", "admin"} {
		resp, _ := e.do(req{path: path, token: e.valid(role)})
		expect(t, resp, 403)
	}
}

// cannotPostOrProxyUnknownPaths
func TestCannotPostOrProxyUnknownPaths(t *testing.T) {
	e := newEnv(t)
	jwt := e.valid("ADMIN")
	resp, _ := e.do(req{method: "POST", path: "/api/monitoring/v1/metrics/current", token: jwt})
	expect(t, resp, 403)
	resp, _ = e.do(req{path: "/api/processing/v1/anything", token: jwt})
	expect(t, resp, 403)
	resp, _ = e.do(req{path: "/actuator/prometheus", token: jwt})
	expect(t, resp, 403)
	resp, _ = e.do(req{path: "/api/unknown"}) // sin token: 401 como Spring (denyAll exige autenticación)
	expect(t, resp, 401)
}

// processingRoutesRequireRoleAndForwardContractPathsAndQueries
func TestProcessingRoutesForwardContractPathsAndQueries(t *testing.T) {
	e := newEnv(t)
	logs := "/api/processing/v1/historical-logs?start=2026-09-01T00:00:00Z&end=2026-09-02T00:00:00Z&hardwareId=HW-42&limit=25&cursor=next%2Bpage"
	resp, _ := e.do(req{path: logs})
	expect(t, resp, 401)
	for _, role := range []string{"OPERATOR", "ADMIN"} {
		resp, body := e.do(req{path: logs, token: e.valid(role), headers: map[string]string{"X-Request-Id": "processing-42"}})
		expect(t, resp, 200)
		if resp.Header.Get("X-Request-Id") != "processing-42" ||
			body != "/api/v1/historical-logs?start=2026-09-01T00:00:00Z&end=2026-09-02T00:00:00Z&hardwareId=HW-42&limit=25&cursor=next%2Bpage" {
			t.Fatalf("reenvío %q", body)
		}
	}
	resp, _ = e.do(req{path: logs, token: e.valid("ROOT")})
	expect(t, resp, 403)
	q := "metric=node.cpu.utilization&start=2026-09-01T00:00:00Z&end=2026-09-02T00:00:00Z&stepSeconds=30&cluster=lab&resourceId=node-1"
	resp, body := e.do(req{path: "/api/processing/v1/metrics/history?" + q, token: e.valid("OPERATOR")})
	expect(t, resp, 200)
	if body != "/api/v1/metrics/history?"+q {
		t.Fatalf("reenvío %q", body)
	}
	resp, body = e.do(req{path: "/api/processing/v1/prediction/dataset?start=2026-09-01T00:00:00Z&end=2026-09-02T00:00:00Z&cluster=lab&resourceId=node-1&stepSeconds=60",
		token: e.valid("ADMIN"), headers: map[string]string{"X-Request-Id": "error-99"}})
	expect(t, resp, 422)
	if resp.Header.Get("X-Request-Id") != "error-99" || body != `{"status":422,"detail":"invalid query"}` {
		t.Fatalf("problema upstream alterado: %q", body)
	}
}

// corsPreflightNeedsNoToken
func TestCorsPreflightNeedsNoToken(t *testing.T) {
	e := newEnv(t)
	resp, _ := e.do(req{method: "OPTIONS", path: "/api/monitoring/v1/metrics/current", headers: map[string]string{
		"Origin": allowedOrigin, "Access-Control-Request-Method": "GET", "Access-Control-Request-Headers": "authorization"}})
	expect(t, resp, 200)
	if resp.Header.Get("Access-Control-Allow-Origin") != allowedOrigin || resp.Header.Get("Access-Control-Max-Age") != "3600" {
		t.Fatalf("cabeceras CORS %v", resp.Header)
	}
}

// deniesForeignOrigin (+ método y cabecera no permitidos, petición simple de otro origen)
func TestDeniesForeignOrigin(t *testing.T) {
	e := newEnv(t)
	for _, h := range []map[string]string{
		{"Origin": "https://wrong.test", "Access-Control-Request-Method": "GET"},
		{"Origin": allowedOrigin, "Access-Control-Request-Method": "DELETE"},
		{"Origin": allowedOrigin, "Access-Control-Request-Method": "GET", "Access-Control-Request-Headers": "x-evil"},
	} {
		resp, _ := e.do(req{method: "OPTIONS", path: "/api/monitoring/v1/metrics/current", headers: h})
		expect(t, resp, 403)
	}
	resp, _ := e.do(req{path: path, token: e.valid("ADMIN"), headers: map[string]string{"Origin": "https://wrong.test"}})
	expect(t, resp, 403)
	resp, _ = e.do(req{path: path, token: e.valid("ADMIN"), headers: map[string]string{"Origin": allowedOrigin}})
	expect(t, resp, 200)
	if resp.Header.Get("Access-Control-Allow-Origin") != allowedOrigin || resp.Header.Get("Access-Control-Expose-Headers") != "X-Request-Id" {
		t.Fatalf("CORS en respuesta real %v", resp.Header)
	}
}

// healthIsPublic
func TestHealthAndOpenAPIArePublic(t *testing.T) {
	e := newEnv(t)
	for _, p := range []string{"/actuator/health", "/actuator/health/liveness", "/actuator/health/readiness", "/openapi/gateway-v0.1.yaml"} {
		resp, _ := e.do(req{path: p})
		expect(t, resp, 200)
	}
}

// predictionPostIsAuthenticatedAndPreservesBody
func TestPredictionPostIsAuthenticatedAndPreservesBody(t *testing.T) {
	e := newEnv(t)
	p, payload := "/api/prediction/v1/predictions", `{"datasetId":"test-dataset","features":[]}`
	resp, _ := e.do(req{method: "POST", path: p})
	expect(t, resp, 401)
	resp, _ = e.do(req{method: "POST", path: p, token: e.valid("ROOT")})
	expect(t, resp, 403)
	for _, role := range []string{"OPERATOR", "ADMIN"} {
		jwt := e.valid(role)
		resp, body := e.do(req{method: "POST", path: p, token: jwt, body: payload,
			headers: map[string]string{"Content-Type": "application/json", "X-Request-Id": "prediction-test"}})
		expect(t, resp, 200)
		if body != payload || resp.Header.Get("X-Request-Id") != "prediction-test" {
			t.Fatalf("cuerpo %q", body)
		}
		resp, _ = e.do(req{path: p, token: jwt})
		expect(t, resp, 403)
	}
	resp, _ = e.do(req{method: "OPTIONS", path: p, headers: map[string]string{"Origin": allowedOrigin,
		"Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "authorization,content-type"}})
	expect(t, resp, 200)
}

// recommendationRoutesRequireRoleAndPreserveBody
func TestRecommendationRoutesRequireRoleAndPreserveBody(t *testing.T) {
	e := newEnv(t)
	for _, endpoint := range []string{"recommendations", "energy"} {
		p := "/api/recommendations/v1/" + endpoint
		resp, _ := e.do(req{method: "POST", path: p})
		expect(t, resp, 401)
		resp, _ = e.do(req{method: "POST", path: p, token: e.valid("ROOT")})
		expect(t, resp, 403)
		for _, role := range []string{"OPERATOR", "ADMIN"} {
			resp, body := e.do(req{method: "POST", path: p, token: e.valid(role), body: `{"demo":true}`,
				headers: map[string]string{"Content-Type": "application/json"}})
			expect(t, resp, 200)
			if body != `{"demo":true}` {
				t.Fatalf("cuerpo %q", body)
			}
		}
	}
}

// ---------- adicionales (sin equivalente en la suite Java) ----------

func TestBodyOver2MBIsRejected(t *testing.T) {
	e := newEnv(t)
	big := strings.Repeat("a", 2<<20+1)
	resp, _ := e.do(req{method: "POST", path: "/api/prediction/v1/predictions", token: e.valid("ADMIN"), body: big})
	expect(t, resp, 413)
	exact := `"` + strings.Repeat("a", 2<<20-2) + `"`
	resp, _ = e.do(req{method: "POST", path: "/api/prediction/v1/predictions", token: e.valid("ADMIN"), body: exact})
	expect(t, resp, 200)
}

func TestInvalidRequestIDIsReplaced(t *testing.T) {
	e := newEnv(t)
	resp, _ := e.do(req{path: path, token: e.valid("ADMIN"), headers: map[string]string{"X-Request-Id": "bad id!"}})
	expect(t, resp, 200)
	if id := resp.Header.Get("X-Request-Id"); len(id) != 36 || id == "bad id!" {
		t.Fatalf("X-Request-Id %q", id)
	}
}

func TestUpstreamTimeoutIs504(t *testing.T) {
	e := newEnv(t)
	jwt := e.valid("ADMIN") // obtiene el JWKS antes de ralentizar
	e.do(req{path: path, token: jwt})
	e.slow = 7 * time.Second // > 6 s de las rutas de Monitoring
	resp, body := e.do(req{path: path, token: jwt})
	expect(t, resp, 504)
	if strings.Contains(body, "127.0.0.1") {
		t.Fatal("filtra dirección interna")
	}
}

func TestUpstreamDownIs503WithoutInternalDetails(t *testing.T) {
	e := newEnv(t)
	jwt := e.valid("ADMIN")
	e.do(req{path: path, token: jwt})
	dead, _ := url.Parse("http://127.0.0.1:1")
	srv := e.gw.Config.Handler.(*Server)
	srv.proxies[policy.Monitoring].Rewrite = func(pr *httputil.ProxyRequest) { pr.SetURL(dead) }
	resp, body := e.do(req{path: path, token: jwt})
	expect(t, resp, 503)
	if strings.Contains(body, "127.0.0.1") || strings.Contains(body, "refused") {
		t.Fatalf("filtra detalles: %s", body)
	}
}

func TestJWKSUnavailableIs503AndNeverAccepts(t *testing.T) {
	e := newEnv(t)
	e.jwksDown = true
	resp, _ := e.do(req{path: path, token: e.valid("ADMIN")})
	expect(t, resp, 503)
}

func TestHeaderLimitMatchesSpring16KB(t *testing.T) {
	e := newEnv(t)
	srv := httptest.NewUnstartedServer(e.gw.Config.Handler)
	srv.Config.MaxHeaderBytes = MaxHeaderBytes
	srv.Start()
	defer srv.Close()
	for size, want := range map[int]int{15000: 401, 17000: 431} {
		r, _ := http.NewRequest("GET", srv.URL+"/api/unknown", nil)
		r.Header.Set("X-Big", strings.Repeat("a", size))
		resp, err := http.DefaultClient.Do(r)
		if err != nil {
			t.Fatal(err)
		}
		resp.Body.Close()
		if resp.StatusCode != want {
			t.Errorf("cabecera de %d bytes: %d, se esperaba %d", size, resp.StatusCode, want)
		}
	}
}

// Revisión 03, hallazgo 4 (refutado): ReverseProxy en modo Rewrite elimina X-Forwarded-* del cliente.
func TestClientForwardedHeadersAreNotTrusted(t *testing.T) {
	e := newEnv(t)
	resp, body := e.do(req{path: "/api/monitoring/v1/metrics/catalog", token: e.valid("ADMIN"),
		headers: map[string]string{"X-Forwarded-For": "10.9.9.9", "X-Forwarded-Host": "evil.test"}})
	expect(t, resp, 200)
	if strings.Contains(body, "10.9.9.9") || strings.Contains(body, "evil.test") || !strings.Contains(body, "xff=127.0.0.1") {
		t.Fatalf("cabeceras de reenvío incorrectas: %s", body)
	}
}

// Revisión 03, hallazgo 5.
func TestGetRoutesBodyIsBounded(t *testing.T) {
	e := newEnv(t)
	resp, _ := e.do(req{path: "/api/monitoring/v1/metrics/catalog", token: e.valid("ADMIN"), body: strings.Repeat("a", 65<<10)})
	expect(t, resp, 413)
}

// Revisión 03, hallazgo 6.
func TestOpenAPIDirectoryIsNotListed(t *testing.T) {
	e := newEnv(t)
	for _, p := range []string{"/openapi/", "/openapi/../../etc/passwd"} {
		resp, body := e.do(req{path: p})
		if resp.StatusCode == 200 || strings.Contains(body, "gateway-v0.1.yaml") {
			t.Errorf("%s: %d %q", p, resp.StatusCode, body)
		}
	}
}

// HU-14: rol observador (VIEWER) de solo lectura.
func TestViewerRoleIsReadOnly(t *testing.T) {
	e := newEnv(t)
	resp, _ := e.do(req{path: path, token: e.valid("VIEWER")})
	expect(t, resp, 200)
	resp, _ = e.do(req{path: "/api/processing/v1/historical-logs?hardwareId=HW1&start=2026-09-01T00:00:00Z&end=2026-09-02T00:00:00Z", token: e.valid("VIEWER")})
	expect(t, resp, 200)
	for _, p := range []string{"/api/prediction/v1/predictions", "/api/recommendations/v1/recommendations", "/api/recommendations/v1/energy"} {
		resp, _ = e.do(req{method: "POST", path: p, token: e.valid("VIEWER"), body: "{}"})
		expect(t, resp, 403)
	}
}
