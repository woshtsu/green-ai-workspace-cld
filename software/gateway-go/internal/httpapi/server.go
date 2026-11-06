// Package httpapi es el adaptador de entrada HTTP: correlación, CORS, autenticación, autorización
// y reenvío a los servicios internos según la tabla de policy.
package httpapi

import (
	"context"
	"crypto/rand"
	"errors"
	"fmt"
	"net"
	"net/http"
	"net/http/httputil"
	"net/url"
	"regexp"
	"strings"
	"time"

	"greenai/gateway/internal/auth"
	"greenai/gateway/internal/policy"
)

const requestIDHeader = "X-Request-Id"

// MaxHeaderBytes: Go añade ~4 KB de holgura; 12 KB efectivos ≈ max-http-request-header-size 16KB de Spring.
const MaxHeaderBytes = 12 << 10

// defaultMaxBody acota el cuerpo de rutas sin límite propio (las GET).
const defaultMaxBody = 64 << 10

var safeRequestID = regexp.MustCompile(`^[A-Za-z0-9._:-]{1,128}$`)

var (
	corsMethods = []string{"GET", "POST", "OPTIONS"}
	corsHeaders = map[string]bool{"accept": true, "content-type": true, "authorization": true, "x-request-id": true}
)

// Config reúne lo que aporta el entorno.
type Config struct {
	Upstreams     map[policy.Upstream]*url.URL
	AllowedOrigin string
	OpenAPIDir    string // vacío = /openapi no se sirve
	ConnectTimout time.Duration
}

type Server struct {
	cfg      Config
	verifier auth.Verifier
	proxies  map[policy.Upstream]*httputil.ReverseProxy
	openapi  http.Handler
}

type ctxKey struct{}

func New(cfg Config, verifier auth.Verifier) (*Server, error) {
	if cfg.ConnectTimout == 0 {
		cfg.ConnectTimout = time.Second
	}
	transport := &http.Transport{
		DialContext:         (&net.Dialer{Timeout: cfg.ConnectTimout}).DialContext,
		MaxIdleConnsPerHost: 16,
		IdleConnTimeout:     90 * time.Second,
	}
	s := &Server{cfg: cfg, verifier: verifier, proxies: map[policy.Upstream]*httputil.ReverseProxy{}}
	for _, r := range policy.Routes() {
		target, ok := cfg.Upstreams[r.Upstream]
		if !ok || target == nil {
			return nil, fmt.Errorf("falta la URL del servicio %s", r.Upstream)
		}
		if _, done := s.proxies[r.Upstream]; done {
			continue
		}
		s.proxies[r.Upstream] = &httputil.ReverseProxy{
			Transport: transport,
			Rewrite: func(pr *httputil.ProxyRequest) {
				route := pr.In.Context().Value(ctxKey{}).(policy.Route)
				pr.SetURL(target)
				pr.Out.URL.Path = strings.TrimSuffix(target.Path, "/") + route.UpstreamPath()
				pr.Out.URL.RawPath = ""
				pr.Out.URL.RawQuery = pr.In.URL.RawQuery // la query se reenvía sin recodificar
				pr.SetXForwarded()
			},
			ModifyResponse: func(resp *http.Response) error {
				resp.Header.Del(requestIDHeader) // la correlación la fija el Gateway
				for k := range resp.Header {
					if strings.HasPrefix(strings.ToLower(k), "access-control-") {
						resp.Header.Del(k)
					}
				}
				return nil
			},
			ErrorHandler: proxyError,
		}
	}
	if cfg.OpenAPIDir != "" {
		s.openapi = http.StripPrefix("/openapi/", http.FileServer(http.Dir(cfg.OpenAPIDir)))
	}
	return s, nil
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	id := r.Header.Get(requestIDHeader)
	if !safeRequestID.MatchString(id) {
		id = newUUID()
	}
	r.Header.Set(requestIDHeader, id)
	h := w.Header()
	h.Set(requestIDHeader, id)
	h.Add("Vary", "Origin")
	h.Add("Vary", "Access-Control-Request-Method")
	h.Add("Vary", "Access-Control-Request-Headers")

	if !s.cors(w, r) {
		return
	}
	if s.public(w, r) {
		return
	}
	principal, err := s.authenticate(r)
	if err != nil {
		if errors.Is(err, auth.ErrUnavailable) {
			problem(w, http.StatusServiceUnavailable, "Service Unavailable", "No fue posible validar la sesión en este momento.")
			return
		}
		unauthorized(w)
		return
	}
	route, ok := policy.Match(r.Method, r.URL.Path)
	if !ok || !policy.RoleAllowed(principal.Role) {
		problem(w, http.StatusForbidden, "Forbidden", "Tu cuenta no tiene permiso para esta operación.")
		return
	}
	s.forward(w, r, route)
}

// cors aplica la política de un único origen. Devuelve false si ya respondió.
func (s *Server) cors(w http.ResponseWriter, r *http.Request) bool {
	origin := r.Header.Get("Origin")
	if origin == "" || origin == "http://"+r.Host || origin == "https://"+r.Host {
		return true // no es una petición CORS
	}
	if origin != s.cfg.AllowedOrigin {
		w.WriteHeader(http.StatusForbidden)
		return false
	}
	h := w.Header()
	preflight := r.Method == http.MethodOptions && r.Header.Get("Access-Control-Request-Method") != ""
	if !preflight {
		h.Set("Access-Control-Allow-Origin", origin)
		h.Set("Access-Control-Expose-Headers", requestIDHeader)
		return true
	}
	method := r.Header.Get("Access-Control-Request-Method")
	if !contains(corsMethods, method) {
		w.WriteHeader(http.StatusForbidden)
		return false
	}
	requested := r.Header.Get("Access-Control-Request-Headers")
	for _, name := range strings.Split(requested, ",") {
		if n := strings.ToLower(strings.TrimSpace(name)); n != "" && !corsHeaders[n] {
			w.WriteHeader(http.StatusForbidden)
			return false
		}
	}
	h.Set("Access-Control-Allow-Origin", origin)
	h.Set("Access-Control-Allow-Methods", strings.Join(corsMethods, ","))
	if requested != "" {
		h.Set("Access-Control-Allow-Headers", requested)
	}
	h.Set("Access-Control-Expose-Headers", requestIDHeader)
	h.Set("Access-Control-Max-Age", "3600")
	w.WriteHeader(http.StatusOK)
	return false
}

func (s *Server) public(w http.ResponseWriter, r *http.Request) bool {
	switch p := r.URL.Path; {
	case p == "/actuator/health":
		writeJSON(w, http.StatusOK, `{"groups":["liveness","readiness"],"status":"UP"}`)
	case p == "/actuator/health/liveness" || p == "/actuator/health/readiness":
		writeJSON(w, http.StatusOK, `{"status":"UP"}`)
	case strings.HasPrefix(p, "/openapi/") && s.openapi != nil && (r.Method == http.MethodGet || r.Method == http.MethodHead):
		if strings.HasSuffix(p, "/") {
			http.NotFound(w, r) // sin listado de directorio (revisión 03)
		} else {
			s.openapi.ServeHTTP(w, r)
		}
	default:
		return false
	}
	return true
}

func (s *Server) authenticate(r *http.Request) (auth.Principal, error) {
	value := r.Header.Get("Authorization")
	scheme, token, found := strings.Cut(value, " ")
	if !found || !strings.EqualFold(scheme, "Bearer") || strings.TrimSpace(token) == "" {
		return auth.Principal{}, auth.ErrInvalidToken
	}
	return s.verifier.Verify(r.Context(), strings.TrimSpace(token))
}

func (s *Server) forward(w http.ResponseWriter, r *http.Request, route policy.Route) {
	limit := route.MaxBody
	if limit == 0 {
		limit = defaultMaxBody // rutas GET: Java no limita; aquí se acota (endurecimiento, revisión 03)
	}
	if r.ContentLength > limit {
		problem(w, http.StatusRequestEntityTooLarge, "Payload Too Large", "El cuerpo supera el tamaño permitido.")
		return
	}
	r.Body = http.MaxBytesReader(w, r.Body, limit)
	ctx, cancel := context.WithTimeout(context.WithValue(r.Context(), ctxKey{}, route), route.Timeout)
	defer cancel()
	s.proxies[route.Upstream].ServeHTTP(w, r.WithContext(ctx))
}

func proxyError(w http.ResponseWriter, r *http.Request, err error) {
	var tooLarge *http.MaxBytesError
	switch {
	case errors.As(err, &tooLarge):
		problem(w, http.StatusRequestEntityTooLarge, "Payload Too Large", "El cuerpo supera el tamaño permitido.")
	case errors.Is(err, context.DeadlineExceeded):
		problem(w, http.StatusGatewayTimeout, "Gateway Timeout", "El servicio no respondió a tiempo.")
	case errors.Is(err, context.Canceled):
		// el cliente cerró la conexión; no hay a quién responder
	default:
		// Sin detalles internos (DNS, direcciones) en la respuesta.
		problem(w, http.StatusServiceUnavailable, "Service Unavailable", "El servicio no está disponible.")
	}
}

func unauthorized(w http.ResponseWriter) {
	w.Header().Set("WWW-Authenticate", "Bearer")
	problem(w, http.StatusUnauthorized, "Unauthorized", "Inicia sesión con un token válido.")
}

func problem(w http.ResponseWriter, status int, title, detail string) {
	w.Header().Set("Content-Type", "application/problem+json")
	w.WriteHeader(status)
	fmt.Fprintf(w, `{"type":"about:blank","title":%q,"status":%d,"detail":%q}`, title, status, detail)
}

func writeJSON(w http.ResponseWriter, status int, body string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_, _ = w.Write([]byte(body))
}

func contains(list []string, v string) bool {
	for _, x := range list {
		if x == v {
			return true
		}
	}
	return false
}

func newUUID() string {
	var b [16]byte
	_, _ = rand.Read(b[:])
	b[6] = (b[6] & 0x0f) | 0x40
	b[8] = (b[8] & 0x3f) | 0x80
	return fmt.Sprintf("%x-%x-%x-%x-%x", b[0:4], b[4:6], b[6:8], b[8:10], b[10:16])
}
