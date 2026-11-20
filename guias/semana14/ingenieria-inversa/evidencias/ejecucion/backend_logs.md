# Logs de backend — Prompt 6: Análisis de Logs

> **Rol:** Ingeniero de Soporte Nivel 3 · **Fase 4 · Ejecución** · 2026-11-19, 15:50–16:15 (UTC−5)
> Entorno: Ubuntu 24.04.5, 2 vCPU, 7 GiB, ejecución **nativa** (sin Docker). Proxy de salida con lista blanca: PyPI, npm y GitHub permitidos; **Docker Hub, Maven Central, proxy.golang.org y CDNs bloqueados**.
> Logs crudos: [`logs/`](logs/) (pruebas, servicios, smoke, E2E, carga, pip-audit). Script de arranque: [`logs/start_stack.sh`](logs/start_stack.sh).

## 1. Qué se ejecutó

| # | Ejecución | Comando | Resultado | Log |
|---|---|---|---|---|
| 1 | Pruebas Data Processing (Python 3.14) | `pytest -q` | **121 passed, 8 skipped**, 2 warnings, 59 s | `logs/dp_tests.log` |
| 2 | Pipeline de entrenamiento Prediction (Python 3.11.9) | `scripts/run_pipeline.py --skip-mlflow` | **OK** — seleccionado `random_forest` 15 min; test: MAE 3,847 · RMSE 5,446 · sMAPE 7,67 % | `logs/pred_tests.log` |
| 3 | Pruebas Prediction | `pytest` | **100 passed**, 1 warning, 14 s | `logs/pred_tests.log` |
| 4 | Pruebas Simulator | `uv run --frozen python -m unittest discover -s tests -v` | **10/10 OK**, 1,5 s | `logs/sim_tests.log` |
| 5 | Gateway Go | `go vet ./...` + `go test -race -count=1 ./...` | **vet limpio; 32/32 pruebas OK** (auth 3,4 s, httpapi 18,1 s, policy 1,0 s) | `logs/gateway_go_tests.log` |
| 6 | Frontend | `node --test tests/*.test.cjs` | **48/48 OK**, 0,56 s | `logs/frontend_tests.log` |
| 7 | Frontend (forma alternativa) | `node --test tests/` | **Falla (exit 1)** | `logs/frontend_tests_dir.log` |
| 8 | Monitoring / Gateway Java | `./mvnw -B verify` | **No ejecutable**: Maven Central bloqueado por el proxy (`connect_rejected`) | — |
| 9 | Semilla SQLite | `scripts/seed_sqlite.py` | 50 hardware, 100 000 logs, 7,3 s | `logs/servicios/seed_sqlite.log` |
| 10 | Validación Prometheus | `promtool check rules alerts.yml` | **SUCCESS: 6 rules found**; `check config` falla solo por la ruta absoluta `/etc/prometheus/alerts.yml` (esperado fuera del contenedor) | — |
| 11 | Stack nativo | `start_stack.sh` (Simulator, Prometheus, Prediction, Data Processing con SQLite, Gateway Go, frontend estático, emisor JWT local) | 7 procesos arriba en < 15 s | `logs/servicios/*.log` |
| 12 | Smoke del repo | `software/infraestructura/smoke/smoke.py` | **12/14**: fallan «monitoring catálogo» y «monitoring CPU actual» (servicio no construible) | `logs/smoke-auditoria.json` |
| 13 | E2E de la auditoría (Gateway + JWT ES256 locales) | `logs/e2e_auditoria.py` | **38/38 conformes** | `logs/e2e.json` |
| 14 | Carga ligera | 600 peticiones vía Gateway | 600/600 HTTP 200 (ver §4) | `logs/carga.json` |
| 15 | SCA Python | `pip-audit` (OSV/PyPA) | Imágenes de servicio limpias; MLflow 2.22.5 con 29 avisos (solo *builder*/CI) | `logs/pip_audit.log` |

## 2. Extractos relevantes de logs

```text
# Prediction — pipeline (pred_tests.log)
INFO src.training.train: Retraining selected random_forest on TRAIN+VALIDATION
INFO src.training.train: Selected random_forest for horizon 15m
INFO run_pipeline: Pipeline complete. selected=random_forest horizon=15m MAE=3.847020 RMSE=5.446480 sMAPE=7.666788

# Data Processing — pruebas omitidas (pytest -rs)
SKIPPED [1] tests/test_historical_logs_contract.py:117: PostgREST de pruebas no configurado (CONTRACT_POSTGREST_URL, CONTRACT_JWT_SECRET): NO verificado
... (8 en total)

# Advertencias comunes en Data Processing y Prediction
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.   (solo Data Processing)

# Go — toolchain
go: downloading go1.25.0 (linux/amd64)
go: download go1.25.0: ... dial tcp: lookup proxy.golang.org ...: no such host

# Simulator (simulator.log)
Run ID: 711fc934-3002-4545-aa23-5d19035fe68d
Starting Prometheus exporter on 127.0.0.1:18000/metrics

# Gateway Go (gateway-go.log) — única línea en toda la sesión (≈ 700 peticiones atendidas)
2026/11/19 15:57:43 INFO gateway escuchando port=18081

# Data Processing (access log de uvicorn, agregado)
212 "GET /api/v1/historical-logs" 200 · 6 "GET /api/v1/historical-logs" 422 · 4 "GET /api/v1/reports/historical-summary" 200
  2 "GET /api/v1/prediction/dataset" 503   ← sin línea de error asociada (causa: Monitoring caído)

# Prediction (access log agregado, sin /metrics)
405 "POST /v1/predictions" 200 · 2 "POST /v1/predictions" 422 · 5 "POST /v1/recommendations" 200 · 1 ... 422
  2 "POST /v1/energy" 200 · 4 "POST /v1/energy" 422 · 2 "GET /docs" 200
+ 1 línea "GET /metrics" 200 cada 5 s (scrape de Prometheus)

# Smoke (smoke-auditoria.json)
FAIL   0 (esperado 200) monitoring catálogo
FAIL   0 (esperado 200) monitoring CPU actual (vía Prometheus, datos simulados)
12/14 casos correctos
```

## 3. Resultado de la batería E2E (38 casos, todos conformes)

| Grupo | Casos | Comportamiento verificado |
|---|---|---|
| Autenticación | E01–E08 | Health y OpenAPI públicos; sin token → 401 + `WWW-Authenticate: Bearer`; token expirado → 401; `is_anonymous` → 401; sin `user_role` → 403; rutas o métodos no publicados → 403 (*deny-all*) |
| Históricos (SQLite) | E10–E16 | Paginación *keyset* con `nextCursor`; cursor manipulado → 422; rango > 31 días → 422; fecha sin zona → 422; reporte JSON y CSV con rol VIEWER |
| Predicción / recomendación / energía | E20–E27 | Predicción 200 (`origin=estimated`, ~97 ms); VIEWER → 403; recomendación con telemetría → `executionAllowed=false`; sin telemetría → `not_evaluable`; energía trapezoidal exacta (0,06875 kWh); hueco > 300 s → 422; factor CO₂e sin fuente → 422; ventana insuficiente → 422 `INSUFFICIENT_DATA` |
| Degradación | E30–E31 | Monitoring caído → Gateway 503 sin detalles internos; Data Processing → 503 `SOURCE_UNAVAILABLE` en problem+json con `requestId` |
| CORS y correlación | E40–E43 | Preflight de origen permitido 200; origen ajeno 403; `X-Request-Id` válido se conserva; malicioso (`<script>`) se reemplaza por UUID |
| Superficie expuesta | E50–E54 | **Data Processing y Prediction responden sin token si se accede directo**; `/metrics` y `/docs` de Prediction públicos; Prediction **refleja `X-Request-Id` sin validar** (`<b>x</b>`, 6 000 caracteres) |
| Observabilidad | E60–E63 | Prometheus: 2 targets UP, 6 reglas cargadas; Simulator expone 4 254 series `node_*` (50 nodos); frontend sirve `dashboard.html` |

## 4. Prueba de carga ligera (Gateway Go → servicios, rol OPERATOR)

| Escenario | n | Concurrencia | HTTP 200 | p50 | p95 | máx | Throughput |
|---|---|---|---|---|---|---|---|
| Predicción (960 muestras de 15 s) | 200 | 1 | 200 | 97,5 ms | 134,7 ms | 171,9 ms | 9,8 req/s |
| Predicción | 200 | 8 | 200 | **1 142,8 ms** | 1 374,8 ms | 1 483,8 ms | **7,0 req/s** |
| Históricos (página de 500, 30 días) | 200 | 8 | 200 | 94,4 ms | 217,7 ms | 261,3 ms | 75,2 req/s |

**Diagnóstico:** Prediction no escala con la concurrencia: el throughput **baja** de 9,8 a 7,0 req/s. Causas verificadas en el código: (1) `predict_from_window()` y `predict()` llaman cada una a `load_selected_model()`, que **deserializa `model.joblib` (1,2 MB) y recalcula su SHA-256 en cada petición** — medido: 14,8 ms por carga en caliente, ×2 por predicción; (2) endpoints síncronos CPU-bound (pandas + scikit-learn) en un único *worker* uvicorn, compitiendo por el GIL.

Consumo de memoria (RSS) en reposo tras la carga: Prediction 293 MiB · Data Processing 250 MiB · Prometheus 97 MiB · Simulator 30 MiB · **Gateway Go 15 MiB**.

## 5. Matriz de hallazgos de logs

Clasificación: **Crítico** (riesgo de seguridad explotable o caída total), **Alto** (función principal degradada o riesgo serio), **Medio** (degradación parcial, deuda con impacto), **Bajo** (higiene, cosmético).

| ID | Tipo | Hallazgo | Evidencia en logs | Severidad |
|---|---|---|---|---|
| L-01 | Problema de autenticación | Los servicios internos (Data Processing, Prediction) **no autentican**: aceptan peticiones directas sin JWT. En Render son `type: web` con URL pública, por lo que el Gateway puede ser **eludido** | E50/E51: `GET /api/v1/historical-logs` 200 y `POST /v1/predictions` 200 sin `Authorization`; `render.yaml`; `prometheus.render.yml` hace *scrape* a `https://green-ai-prediction-dev-zxly.onrender.com` | **Crítico** |
| L-02 | Dependencia faltante (entorno) | Monitoring y Gateway Java no se pudieron construir: Maven Central inaccesible | `connect_rejected repo.maven.apache.org:443`; smoke 12/14 | **Alto** (para esta ejecución; no es defecto del producto) |
| L-03 | Error / problema de red | Sin Monitoring, la cadena de datos en vivo cae: catálogo y CPU actual 503; dataset de predicción 503 `SOURCE_UNAVAILABLE`; el panel y Racks quedan sin métricas | E30/E31; `frontend/e2e_operator.json` (`GET .../metrics/catalog 503`, `.../metrics/current 503`) | **Alto** |
| L-04 | Advertencia (rendimiento) | Prediction recarga y re-hashea el modelo dos veces por petición; throughput cae con concurrencia (p50 ×11,7) | `carga.json`; medición `load_selected_model` 14,8 ms | **Alto** |
| L-05 | Problema de configuración | `/metrics` y `/docs`/`/openapi.json` de Prediction (y `/docs` de Data Processing) públicos sin autenticación; en la nube exponen métricas y contrato completo | E52/E53 | **Medio** |
| L-06 | Problema de configuración | Gateway Go **sin access log**: una sola línea en ~700 peticiones; tampoco registra 401/403/503. Data Processing devuelve 503 sin registrar la causa | `gateway-go.log`; `data-processing.log` | **Medio** |
| L-07 | Advertencia | 8 pruebas de contrato PostgREST **omitidas** por defecto: la consulta real a Supabase no se verifica en CI | `dp_tests.log` (SKIPPED ×8) | **Medio** |
| L-08 | Problema de configuración | El Simulator escribe `samples.jsonl` a ~2,8 KB/s (**≈ 242 MB/día**) sin rotación; en contenedores sin volumen consume disco efímero | `run_data/simruns/.../samples.jsonl` 2,18 MB en 779 s | **Medio** |
| L-09 | Problema de configuración | La identidad `cluster=sim-run-<uuid>` cambia en cada arranque del Simulator; el Compose configura Monitoring con `DEFAULT_CLUSTER=sim-lab`. Reinicios rompen la continuidad de series para predicción | Consulta PromQL: `cluster="sim-run-711fc934-…"` | **Medio** |
| L-10 | Dependencia vulnerable | MLflow 2.22.5 (29 avisos), pytest 8.4.2 (1), pyarrow 19.0.1 (1) en el entorno de entrenamiento/CI | `pip_audit.log` | **Medio** |
| L-11 | Advertencia de entorno | `go.mod` exige `go 1.25`: sin acceso a `proxy.golang.org` el build falla aunque el código compila con 1.24 | Mensaje `go: download go1.25.0 ... no such host` | **Medio** |
| L-12 | Advertencia de seguridad | Prediction refleja `X-Request-Id` arbitrario (sin regex ni límite de longitud), a diferencia del Gateway y Data Processing | E54; `curl` con 6 000 caracteres reflejados | **Bajo** |
| L-13 | Advertencia | Deprecaciones de Starlette (`httpx` en `TestClient`) y anyio (`BlockingPortal`) | `dp_tests.log`, `pred_tests.log` | **Bajo** |
| L-14 | Problema de configuración | `pytest.ini` de Prediction ignora globalmente `DeprecationWarning` y `FutureWarning` (oculta futuras roturas) | `software/prediction/pytest.ini` | **Bajo** |
| L-15 | Error | `node --test tests/` falla en Node 22; solo funciona la lista explícita | `frontend_tests_dir.log` | **Bajo** |
| L-16 | Advertencia | El pipeline reescribe `results/manifest.json` (archivo versionado) → árbol Git modificado tras entrenar | `git status`: ` M software/prediction/results/manifest.json` | **Bajo** |
| L-17 | Advertencia | Scrape de Prediction cada 5 s → 12 líneas `GET /metrics` por minuto en el access log (ruido) | `prediction.log` | **Bajo** |
| L-18 | Excepción controlada | Ventanas con pocos datos tras remuestrear a 5 min → 422 `INSUFFICIENT_DATA` (comportamiento correcto; el repo documenta que el panel da 422 si el simulador lleva < 20 min) | E27 | **Bajo** |
| L-19 | Verificación positiva | Tokens expirados, anónimos, sin rol, CORS ajeno y cursores manipulados se rechazan correctamente; ninguna excepción no controlada (0 respuestas 500) en todas las ejecuciones | `e2e.json` | — |

**Excepciones no controladas:** ninguna. No se observó ningún `Traceback`, `500` ni `INTERNAL_ERROR` en ~1 100 peticiones de negocio; todas las fallas se mapearon a 401/403/422/503 con cuerpo estructurado.
