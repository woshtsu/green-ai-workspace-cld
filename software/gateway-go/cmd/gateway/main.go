// Gateway Green AI (prototipo Go). Mismas variables de entorno que el Gateway Java.
package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"log/slog"
	"net/http"
	"net/url"
	"os"
	"os/signal"
	"syscall"
	"time"

	"greenai/gateway/internal/auth"
	"greenai/gateway/internal/httpapi"
	"greenai/gateway/internal/policy"
)

func main() {
	healthcheck := flag.Bool("healthcheck", false, "consulta /actuator/health/liveness y termina (para Docker)")
	flag.Parse()
	port := env("GATEWAY_PORT", "8081")
	if *healthcheck {
		os.Exit(probe(port))
	}
	if err := run(port); err != nil {
		slog.Error("arranque fallido", "error", err)
		os.Exit(1)
	}
}

func run(port string) error {
	issuer, jwks := os.Getenv("GATEWAY_AUTH_ISSUER_URI"), os.Getenv("GATEWAY_AUTH_JWK_SET_URI")
	if issuer == "" || jwks == "" {
		return errors.New("GATEWAY_AUTH_ISSUER_URI y GATEWAY_AUTH_JWK_SET_URI son obligatorios")
	}
	upstreams := map[policy.Upstream]*url.URL{}
	for name, spec := range map[policy.Upstream][2]string{
		policy.Monitoring:     {"GATEWAY_MONITORING_BASE_URL", "http://127.0.0.1:8080"},
		policy.DataProcessing: {"GATEWAY_DATA_PROCESSING_BASE_URL", "http://data-processing:8000"},
		policy.Prediction:     {"GATEWAY_PREDICTION_BASE_URL", "http://prediction:8000"},
	} {
		u, err := url.Parse(env(spec[0], spec[1]))
		if err != nil || (u.Scheme != "http" && u.Scheme != "https") || u.Host == "" || u.User != nil || u.RawQuery != "" {
			return fmt.Errorf("%s inválida", spec[0])
		}
		upstreams[name] = u
	}
	handler, err := httpapi.New(httpapi.Config{
		Upstreams:     upstreams,
		AllowedOrigin: env("GATEWAY_CORS_ALLOWED_ORIGIN", "http://127.0.0.1:3001"),
		OpenAPIDir:    os.Getenv("GATEWAY_OPENAPI_DIR"),
	}, auth.NewJWKSVerifier(issuer, "authenticated", jwks))
	if err != nil {
		return err
	}
	srv := &http.Server{Addr: ":" + port, Handler: handler, MaxHeaderBytes: httpapi.MaxHeaderBytes,
		ReadHeaderTimeout: 10 * time.Second, ReadTimeout: 60 * time.Second, IdleTimeout: 120 * time.Second}
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	errc := make(chan error, 1)
	go func() { errc <- srv.ListenAndServe() }()
	slog.Info("gateway escuchando", "port", port)
	select {
	case err := <-errc:
		return err
	case <-ctx.Done():
		shutdown, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		return srv.Shutdown(shutdown)
	}
}

func probe(port string) int {
	c := http.Client{Timeout: 3 * time.Second}
	resp, err := c.Get("http://127.0.0.1:" + port + "/actuator/health/liveness")
	if err != nil {
		return 1
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return 1
	}
	return 0
}

func env(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
