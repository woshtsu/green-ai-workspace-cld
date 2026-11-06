# Gateway Green AI — prototipo Go (evaluación, no predeterminado)

Reimplementación del Gateway Java (`software/gateway`) con la biblioteca estándar de Go 1.25. Mismas rutas, reglas
JWT/RBAC, CORS, límites, variables de entorno y OpenAPI. Decisión y mediciones: `docs/DECISIONES.md` (D-06).

## Estructura (puertos y adaptadores)
| Paquete | Rol |
|---|---|
| `internal/policy` | Dominio: 9 rutas explícitas (método + path exacto), reescritura de prefijos, límites, roles ADMIN/OPERATOR |
| `internal/auth` | Puerto `Verifier` + adaptador JWKS (ES256/RS256; iss, aud, exp sin holgura, nbf ±60 s, sub, role, is_anonymous) |
| `internal/httpapi` | Adaptador HTTP: X-Request-Id, CORS de un origen, 401/403 `problem+json`, proxy con timeouts, 413/504/503 |
| `cmd/gateway` | Configuración por entorno y arranque; `-healthcheck` para la imagen distroless |
| `tools/difftest` | Prueba diferencial Java vs Go y medición de carga |

## Pruebas (sin instalar Go: imagen oficial)
```powershell
docker run --rm -v "${PWD}/software/gateway-go:/src" -w /src -e CGO_ENABLED=0 golang:1.25.14-alpine go test ./...
docker build -f software/gateway-go/Dockerfile -t green-ai-mono-gateway-go:local software   # ejecuta vet + test
.\software\gateway-go\tools\difftest\run.ps1        # requiere el stack green-ai-mono en marcha
```

## Variables
`GATEWAY_PORT` (8081), `GATEWAY_MONITORING_BASE_URL`, `GATEWAY_DATA_PROCESSING_BASE_URL`, `GATEWAY_PREDICTION_BASE_URL`,
`GATEWAY_AUTH_ISSUER_URI` y `GATEWAY_AUTH_JWK_SET_URI` (obligatorias), `GATEWAY_CORS_ALLOWED_ORIGIN`,
`GATEWAY_OPENAPI_DIR` (la imagen la fija en `/openapi`).
