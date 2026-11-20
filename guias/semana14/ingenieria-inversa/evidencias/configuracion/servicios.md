# Servicios — catálogo operativo

> **Fase 3** · Fuentes: `docker-compose.yml` y overlays, Dockerfiles, `render.yaml`, `prometheus*.yml`, guía de Render, y la ejecución nativa de esta auditoría (consumo de memoria medido con `ps -o rss`).

## 1. Catálogo

| Servicio | Tecnología | Puerto interno | Puerto local (Compose, `127.0.0.1`) | Health / readiness | Depende de | RSS medido (auditoría) |
|---|---|---|---|---|---|---|
| simulator | Python 3.12, prometheus-client | 8000 (Compose) / 9090 (Dockerfile) | 18000 | `/metrics` | — | 30 MiB |
| prometheus | Prometheus v3.13.3 | 9090 | 19090 | `/-/ready` | simulator, prediction | 97 MiB |
| monitoring | Java 21, Spring Boot 4.1.1 | 8080 | 18080 | `/actuator/health/{liveness,readiness}` | prometheus | No ejecutado (repo: 211 MiB) |
| data-processing | Python 3.14, FastAPI | 8000 | interno (`expose`); 18003 con `compose.swagger.yaml` | `/api/v1/health` (+ `HEALTHCHECK` en Dockerfile) | monitoring, Supabase o SQLite | 250 MiB |
| prediction | Python 3.11, FastAPI + RF | 8000 | interno; 18002 con `compose.swagger.yaml` | `/health/live`, `/health/ready` (verifica artefacto y SHA-256) | artefacto `model.joblib` | 293 MiB |
| gateway (Java) | Spring Cloud Gateway | 8081 | 18081 | `/actuator/health/liveness` | monitoring, data-processing, prediction, Supabase JWKS | No ejecutado (repo: 283 MiB) |
| gateway-go | Go 1.25 (stdlib) | 8081 | 18082 (overlay) — en la auditoría se usó como gateway principal en 18081 | `/actuator/health/liveness`; `HEALTHCHECK` con `-healthcheck` | ídem | **15 MiB** |
| frontend | nginx 1.28 + estáticos | 3001 | 13001 | `/` | gateway (desde el navegador), Supabase Auth, CDNs | — (servidor estático de Python en la auditoría) |
| grafana (opcional) | Grafana 12.4.0 | 3000 | 13002 | `/api/health` | prometheus | — |
| db / postgrest / gateway nginx (pruebas de contrato) | PostgreSQL 17.6, PostgREST v13, nginx | 5432/3000/80 | 13300 | `pg_isready` | — | — |

## 2. Orden de arranque (grafo de `depends_on`)

```text
simulator ──► prometheus ──► monitoring ──► data-processing ──┐
                    ▲                                          ├──► gateway ──► frontend
                    └────────── prediction ────────────────────┘
```
`depends_on` solo ordena el arranque (sin `condition: service_healthy`, salvo en el Compose de contrato); Prediction tiene `healthcheck` en Compose, pero nadie espera por él.

## 3. Rutas publicadas por el Gateway (9)

| Ruta pública | Método | Upstream | Reescritura | Roles | Timeout | Límite de cuerpo |
|---|---|---|---|---|---|---|
| `/api/monitoring/v1/metrics/{catalog,current,history}` | GET | monitoring | → `/api/v1/metrics/...` | ADMIN, OPERATOR, VIEWER | 6 s | — (Go: 64 KB en GET) |
| `/api/processing/v1/{metrics/history, historical-logs, prediction/dataset, reports/historical-summary}` | GET | data-processing | → `/api/v1/...` | ADMIN, OPERATOR, VIEWER | 15 s | — |
| `/api/prediction/v1/predictions` | POST | prediction | → `/v1/predictions` | ADMIN, OPERATOR | 30 s | 2 MB |
| `/api/recommendations/v1/{recommendations, energy}` | POST | prediction | → `/v1/...` | ADMIN, OPERATOR | 30 s | 2 MB |
| `/actuator/health/**`, `/openapi/**` | GET | (local) | — | público | — | — |

Todo lo demás: **denegado** (Java `anyExchange().denyAll()`; Go: tabla cerrada → 401 sin token, 403 con token).

## 4. Mapeo de despliegue

| Servicio | Local (Compose) | Nube (Render, plan gratuito) | Nube (GitHub Pages) |
|---|---|---|---|
| frontend | nginx :13001 | — | `https://woshtsu.github.io/green-ai-workspace-cld/` (prod) y `/dev/` |
| gateway | Java :18081 (Go opcional :18082) | **Go** `green-ai-gateway-dev` (puerto 10000) | — |
| prediction | interno | `green-ai-prediction-dev` (`type: web`, **URL pública**) | — |
| data-processing | interno | `green-ai-data-processing-dev` (`type: web`, **URL pública**), históricos desde Supabase | — |
| monitoring | :18080 | Servicio manual de la serie `green-ai-*-dev` según la documentación operativa (6 servicios); **`render.yaml` lo omite** y fija `GATEWAY_MONITORING_BASE_URL=https://example.invalid`, por lo que el panel de Render y el Blueprint divergen | — |
| prometheus | :19090 | Servicio manual con `Dockerfile.render` (scrape HTTPS público, 6 h en `/tmp`) | — |
| simulator | :18000 | Servicio manual (`green-ai-simulator-dev`) | — |

## 5. Comunicación entre servicios

| Origen → Destino | Protocolo | Autenticación | Observación |
|---|---|---|---|
| Navegador → Supabase Auth | HTTPS | Clave publishable + PKCE | — |
| Navegador → Gateway | HTTPS/HTTP + CORS | `Bearer` JWT | Origen único permitido |
| Gateway → servicios | HTTP | **Ninguna** (reenvía `Authorization` y `X-Request-Id`) | Confianza en la red |
| Data Processing → Monitoring | HTTP (httpx) | Ninguna | Valida estrictamente el contrato de respuesta |
| Data Processing → Supabase PostgREST | HTTPS | `apikey` + `Bearer` de lectura | Solo `SELECT` sobre 7 columnas |
| Monitoring → Prometheus | HTTP API (`/api/v1/query`, `/query_range`) | Ninguna | Máx. 16 consultas concurrentes, 5 s |
| Prometheus → Simulator / Prediction | HTTP *scrape* (`/metrics`) | Ninguna | Cada 5 s local; 15 s/60 s en Render por URL pública |

## 6. Consideraciones operativas
1. **Sin políticas `restart`** en Compose: un servicio caído no se recupera solo.
2. **Healthchecks superficiales**: Data Processing y Monitoring responden «sano» aunque su fuente (Monitoring/Prometheus/Supabase) esté caída; solo Prediction verifica su dependencia real (el artefacto).
3. **Prometheus sin volumen** en Compose y con `/tmp` en Render: el histórico se pierde al recrear el contenedor.
4. **Escalado**: todos los servicios Python corren con 1 *worker* de uvicorn; en la auditoría Prediction pasó de 9,8 a 7,0 peticiones/s al subir la concurrencia de 1 a 8 (ver `evidencias/ejecucion/backend_logs.md`).
