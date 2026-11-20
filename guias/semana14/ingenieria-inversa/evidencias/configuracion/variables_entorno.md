# Variables de entorno — Prompt 5

> **Fase 3** · Archivos analizados: `software/data-processing/.env.example`, `infrastructure/settings.py`, `software/prediction/.env.example`, `src/config/settings.py`, `config/config.yaml`, `src/service/recommendations.py`, `software/gateway/src/main/resources/application.yaml`, `SecurityConfiguration.java`, `software/monitoring/src/main/resources/application.yaml`, `PrometheusProperties.java`, `software/gateway-go/cmd/gateway/main.go`, `software/infraestructura/*.yml`, `render.yaml`, `.github/workflows/pages.yml`, `software/frontend/config.example.js`.
> Búsqueda exhaustiva de `os.getenv`, `os.environ`, `${VAR}`, `@Value`, `os.Getenv`, `env(...)`.
> **Ningún archivo `.env` real está versionado** (solo `.env.example`; `.gitignore` excluye `.env` y `.env.*`).

## 1. Tabla de variables

### 1.1 Gateway (Java y Go comparten nombres)
| Variable | Obligatoria | Descripción | Valor de Ejemplo |
|---|---|---|---|
| `GATEWAY_AUTH_ISSUER_URI` | **Sí** (Go aborta el arranque; Java falla al resolver `${...}`) | Emisor exacto (`iss`) del JWT de Supabase | `https://<ref>.supabase.co/auth/v1` |
| `GATEWAY_AUTH_JWK_SET_URI` | **Sí** | URL del JWKS público | `https://<ref>.supabase.co/auth/v1/.well-known/jwks.json` |
| `GATEWAY_CORS_ALLOWED_ORIGIN` | No (def. `http://127.0.0.1:3001`) | Único origen CORS permitido; debe coincidir exactamente con la URL del frontend | `https://woshtsu.github.io` |
| `GATEWAY_MONITORING_BASE_URL` | No (def. `http://127.0.0.1:8080`) | Upstream de Monitoring | `http://monitoring:8080` |
| `GATEWAY_DATA_PROCESSING_BASE_URL` | No (def. `http://data-processing:8000`) | Upstream de Data Processing | `http://data-processing:8000` |
| `GATEWAY_PREDICTION_BASE_URL` | No (def. `http://prediction:8000`) | Upstream de Prediction (incluye recomendaciones y energía) | `http://prediction:8000` |
| `GATEWAY_PORT` | No (def. `8081`) | Puerto de escucha | `8081` (local), `10000` (Render) |
| `GATEWAY_OPENAPI_DIR` | No (solo Go) | Carpeta con los OpenAPI servidos en `/openapi/` | `/openapi` |
| `PORT` | Solo Render | Puerto que Render enruta; el código no lo lee (se iguala a `GATEWAY_PORT`) | `10000` |

### 1.2 Monitoring (propiedades `monitoring.prometheus.*` por *relaxed binding*)
| Variable | Obligatoria | Descripción | Valor de Ejemplo |
|---|---|---|---|
| `MONITORING_PROMETHEUS_URL` | No, pero sin ella el servicio responde **503 METRICS_SOURCE_UNAVAILABLE** | URL HTTP(S) de Prometheus sin credenciales ni query | `http://prometheus:9090` |
| `MONITORING_PROMETHEUS_DEFAULT_CLUSTER` | No (def. `lab-01`) | Clúster asumido cuando la serie no trae etiqueta `cluster` | `sim-lab` |
| `MONITORING_PROMETHEUS_INSTANCE_LABEL` | No (def. `instance`) | Etiqueta que identifica el nodo | `node` |
| `MONITORING_PROMETHEUS_CLUSTER_LABEL` / `_ORIGIN_LABEL` / `_DEFAULT_ORIGIN` | No | Nombres de etiquetas de identidad y procedencia | `cluster` / `origin` / `unknown` |
| `SPRING_PROFILES_ACTIVE` | No | `fixture` activa la fuente de datos de prueba | `fixture` |

### 1.3 Data Processing
| Variable | Obligatoria | Descripción | Valor de Ejemplo |
|---|---|---|---|
| `MONITORING_BASE_URL` | No (def. `http://localhost:8080`) | URL de Monitoring (validada: http/https, sin credenciales) | `http://monitoring:8080` |
| `REQUEST_TIMEOUT_SECONDS` | No (def. `10`, rango 0–120) | Timeout de llamadas salientes | `10` |
| `APP_ENV` | No (def. `production`) | `development` \| `test` \| `production`; `sqlite` prohibido en producción | `development` |
| `HISTORICAL_SOURCE` | No (vacío = deduce de `SUPABASE_ENABLED`) | `none` \| `supabase` \| `sqlite` | `supabase` |
| `SUPABASE_ENABLED` | No (def. `false`); debe ser coherente con `HISTORICAL_SOURCE` | Activa el adaptador PostgREST | `true` |
| `SUPABASE_URL` | Sí si Supabase activo (solo `https`) | URL del proyecto | `https://<ref>.supabase.co` |
| `SUPABASE_API_KEY` | Sí si Supabase activo | Clave de API (cabecera `apikey`) | `sb_publishable_…` |
| `SUPABASE_READ_TOKEN` | Sí si Supabase activo; rechaza `sb_publishable_`/`sb_secret_` | **JWT de lectura** dedicado (cabecera `Authorization`) | `eyJhbGciOi…` (JWT de rol con solo `SELECT` en `logs`) |
| `HISTORICAL_MAX_PAGE_SIZE` | No (def. `500`, rango 1–500) | Tamaño máximo de página | `500` |
| `SQLITE_PATH` | Sí si `HISTORICAL_SOURCE=sqlite` (archivo existente) | Ruta de la base de desarrollo | `/data/greenai-dev.sqlite` |
| `PORT` | Solo Render | Informativo para Render (el CMD fija 8000) | `8000` |
| `PROCESSING_BASE_URL` | Solo script `check_monitoring_integration.py` | URL de Data Processing para la verificación | `http://data-processing:8000` |
| `CONTRACT_POSTGREST_URL`, `CONTRACT_JWT_SECRET` | Solo pruebas de contrato | Activan 8 pruebas omitidas por defecto | `http://127.0.0.1:13300/rest/v1`, 32+ caracteres aleatorios |

### 1.4 Prediction
| Variable | Obligatoria | Descripción | Valor de Ejemplo |
|---|---|---|---|
| `ML_ENV` | No | Sobrescribe `environment` del `config.yaml` | `experimental` |
| `ML_MODEL_DIR` | No (def. `models/selected`) | Carpeta de `model.joblib` + `metadata.json` | `models/selected` |
| `ML_PORT` | No | Escribe `service.port` en la configuración, **pero el CMD de uvicorn fija `--port 8000`**: sin efecto real | `8000` |
| `MLFLOW_TRACKING_URI` | No (def. `./mlruns`) | Tracking de MLflow en el pipeline | `./mlruns` |
| `DEMO_POLICY_JSON` | No (def. `{}`); **JSON inválido impide el arranque** | Umbrales de la política de recomendación (CPU baja/alta, memoria, latencia p95, error, frescura) | `{"cpuLowPercent":30,"cpuHighPercent":80,"memoryMaxPercent":85}` |
| `MPLBACKEND`, `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MALLOC_ARENA_MAX`, `PYTHONOPTIMIZE` | Fijadas en Dockerfile | Ajustes de runtime y memoria | `Agg`, `1`, `1`, `2`, `2` |

### 1.5 Simulator
No lee variables de entorno: se configura por argumentos CLI obligatorios (`--inventory`, `--scenario`, `--seed`, `--duration-seconds`, `--tick-seconds`, `--mode`, `--output-dir`; `--host` def. `127.0.0.1`, `--port` def. `9090`). El `Dockerfile` define `HOST`/`PORT` que **el código no usa**. En Compose se parametriza con:

| Variable | Obligatoria | Descripción | Valor de Ejemplo |
|---|---|---|---|
| `SIMULATOR_INVENTORY` | No | Inventario JSON | `configs/inventory.hardware.json` (50 nodos) |
| `SIMULATOR_SCENARIO` | No | Escenario de carga | `configs/scenarios/high.json` |
| `SIMULATOR_DURATION_SECONDS` | No (def. `86400`) | Duración total (múltiplo del tick) | `86400` |

### 1.6 Frontend (`config.local.js`, generado en el despliegue)
| Clave / Variable de Actions | Obligatoria | Descripción | Valor de Ejemplo |
|---|---|---|---|
| `supabaseUrl` ← `SUPABASE_URL` | **Sí** | Proyecto Supabase | `https://<ref>.supabase.co` |
| `supabasePublishableKey` ← `SUPABASE_PUBLISHABLE_KEY` | **Sí** | Clave pública del navegador (nunca `service_role`) | `sb_publishable_…` |
| `gatewayBaseUrl` ← `GATEWAY_URL_PROD` / `GATEWAY_URL_DEV` | **Sí** | URL https del Gateway sin `/` final | `https://green-ai-gateway-dev.onrender.com` |

### 1.7 Infraestructura local (Compose)
| Variable | Obligatoria | Descripción | Valor de Ejemplo |
|---|---|---|---|
| `MONO_SIMULATOR_PORT`, `MONO_PROMETHEUS_PORT`, `MONO_MONITORING_PORT`, `MONO_GATEWAY_PORT`, `MONO_FRONTEND_PORT`, `MONO_PREDICTION_SWAGGER_PORT`, `MONO_DATAPROC_SWAGGER_PORT`, `MONO_GATEWAY_GO_PORT`, `MONO_GRAFANA_PORT` | No | Puertos publicados en `127.0.0.1` | 18000, 19090, 18080, 18081, 13001, 18002, 18003, 18082, 13002 |
| `GRAFANA_ADMIN_PASSWORD` | **Sí** con el overlay de Grafana (`${VAR:?}`) | Contraseña del administrador | (secreto local) |
| `CONTRACT_DB_PASSWORD`, `CONTRACT_AUTH_PASSWORD`, `CONTRACT_JWT_SECRET` | **Sí** con `compose.contract-postgres.yml` | Credenciales efímeras de pruebas | aleatorias por ejecución |
| `GREENAI_NETWORK`, `DATA_PROCESSING_LOCAL_PORT` | No | Compose propio de Data Processing (heredado) | `greenai-net` |

## 2. Secretos
| Secreto | Dónde se usa | Manejo observado |
|---|---|---|
| `SUPABASE_READ_TOKEN` | Data Processing → PostgREST | `sync: false` en Render; `repr=False` en `Settings`; validación que rechaza claves `sb_*`. **El HANDOFF registra que en Render se configuró la clave legacy `anon`** (un JWT válido pero sin privilegios mínimos dedicados), aceptada por la validación |
| `SUPABASE_API_KEY` | Data Processing | `sync: false` |
| `GRAFANA_ADMIN_PASSWORD` | Grafana | Obligatoria por `${VAR:?}`; nunca con valor por defecto |
| `CONTRACT_*` | PostgreSQL/PostgREST de pruebas | Aleatorios en memoria, `down -v` tras cada ejecución |
| Contraseñas sintéticas | `BD_GreenAi.xlsx` (hoja `Usuarios`, p. ej. `Admin123!N`) | **Versionadas en texto plano**; la semilla SQLite no carga esa hoja |

## 3. Tokens
- **JWT de usuario (Supabase Auth):** emitido en el navegador (PKCE) y enviado como `Authorization: Bearer` al Gateway. Claims exigidos: `iss` exacto, `aud=authenticated`, `exp` (sin holgura), `nbf` (60 s), `sub` no vacío, `role=authenticated`, `is_anonymous≠true`, `user_role ∈ {ADMIN, OPERATOR, VIEWER}`.
- **JWT de servicio (lectura de históricos):** `SUPABASE_READ_TOKEN`, de larga duración y no rotado automáticamente.
- **Clave publishable:** pública por diseño; inyectada en `config.local.js` desde variables (no secretos) de Actions.

## 4. Configuración de base de datos
- **Supabase/PostgreSQL:** tablas `public.hardware`, `public.logs` (leídas por PostgREST `/rest/v1/logs` con 7 columnas, orden `timestamp.asc,log_id.asc`, cursor *keyset*), `public.usuario` (legado, con columnas `password` y `password_hash`), `public.user_profiles`, `public.user_roles` (enum `app_role`), trigger `on_auth_user_created_green_ai`, función `custom_access_token_hook`.
- **SQLite (dev):** `SQLITE_PATH`, apertura `mode=ro`, esquema `STRICT` con `CHECK` de timestamps UTC canónicos, índices `(hardware_id, timestamp DESC)`.
- **PostgreSQL 17 + PostgREST v13 (contrato):** rol `web_anon`, usuario `authenticator`, esquema `contract-schema.sql`.

## 5. Configuración de APIs externas
| API | Variables |
|---|---|
| Supabase Auth (JWKS) | `GATEWAY_AUTH_ISSUER_URI`, `GATEWAY_AUTH_JWK_SET_URI`; frontend: `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY` |
| Supabase Data API | `SUPABASE_URL`, `SUPABASE_API_KEY`, `SUPABASE_READ_TOKEN`, `REQUEST_TIMEOUT_SECONDS` |
| Prometheus HTTP API | `MONITORING_PROMETHEUS_URL` (+ etiquetas) |
| Servicios internos | `GATEWAY_*_BASE_URL`, `MONITORING_BASE_URL` |

## 6. Observaciones
1. La validación de configuración es **fail-fast** y de buena calidad en Data Processing (URL, timeouts, coherencia de fuente, prohibición de SQLite en producción) y en el Gateway Go.
2. `ML_PORT` y `HOST`/`PORT` del Simulator son configuraciones **sin efecto** (deuda menor).
3. Monitoring arranca «sano» aunque falte `MONITORING_PROMETHEUS_URL` y solo falla en las consultas (503): el *health* no refleja la dependencia.
4. El valor por defecto del *issuer* en `docker-compose.yml` apunta al proyecto Supabase real (`jpfugpsdhuucmilgysgg`): datos públicos, pero acopla el entorno local al proyecto de la nube.
