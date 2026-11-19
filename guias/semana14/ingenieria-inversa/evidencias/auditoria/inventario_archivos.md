# Inventario de archivos — Green AI (`woshtsu/green-ai-workspace-cld`)

> **Fase 1 · Auditoría del proyecto** · Evidencia base del Prompt 1
> Repositorio: `https://github.com/woshtsu/green-ai-workspace-cld.git` · rama `main` · commit `27ef69f` (Merge PR #5)
> Fecha de análisis: 2026-11-19 · Método: `git clone`, `git ls-files`, lectura directa del código fuente.

## 1. Resumen cuantitativo

| Indicador | Valor |
|---|---|
| Archivos versionados | **746** |
| Archivos de código y configuración bajo `software/` | 389 |
| Servicios ejecutables | 7 (`monitoring`, `gateway`, `gateway-go`, `data-processing`, `prediction`, `simulator`, `frontend`) + `infraestructura` |
| Líneas no vacías de código en `software/` | Python 9 577 · CSS 2 765 · JavaScript 2 406 (+600 de pruebas) · Java 2 126 · Go 1 639 · YAML 801 · HTML 743 · PowerShell 248 · SQL 176 |
| Documentación Markdown | 176 archivos |
| Binarios versionados | 105 PNG (21,1 MB), 18 JPG (2,5 MB), 2 DOCX (11,5 MB), 3 XLSX (7,5 MB) |
| Workflows CI/CD | 2 (`.github/workflows/ci.yml`, `pages.yml`) |
| Contratos OpenAPI / JSON Schema | 8 |

## 2. Árbol de directorios (nivel funcional)

```text
green-ai-workspace-cld/
├── .github/workflows/          CI por servicio (ci.yml) y despliegue del frontend a GitHub Pages (pages.yml)
├── .agents/, .claude/          Skills y perfiles de agentes de IA usados por el equipo (no ejecutables en runtime)
├── render.yaml                 Blueprint de Render (3 servicios web *-dev, plan gratuito)
├── software/
│   ├── monitoring/             Java 21 · Spring Boot 4.1.1 · API de métricas sobre Prometheus (hexagonal)
│   ├── gateway/                Java 21 · Spring Cloud Gateway 2025.1.3 · JWT Supabase + RBAC + CORS (predeterminado)
│   ├── gateway-go/             Go 1.25 · gateway equivalente sin dependencias externas (alternativa validada)
│   ├── data-processing/        Python 3.14 · FastAPI · ETL, históricos (Supabase/SQLite), dataset para Prediction
│   ├── prediction/             Python 3.11 · FastAPI + scikit-learn/XGBoost · predicción, recomendaciones, energía
│   ├── simulator/              Python 3.12 · CLI + exportador Prometheus de telemetría sintética (50 nodos)
│   ├── frontend/               HTML/CSS/JS estático + nginx · Supabase Auth (PKCE) · Chart.js
│   └── infraestructura/        docker-compose (+5 overlays), Prometheus, alertas, Grafana, smoke HTTP
├── docs/                       HANDOFF, DECISIONES (ADR D-01…D-07), guías de despliegue, calidad FURPS+/OWASP, evidencias
├── entregables/, guias/        Informes académicos, guías docentes, Word/Excel exportados
├── herramientas_IA/            Scripts de exportación DOCX, video, Trello, migración, diagramas PlantUML
└── graphify-out/               Grafo de conocimiento del código generado por la herramienta Graphify
```

## 3. Inventario por servicio

### 3.1 `software/monitoring` (60 archivos)
| Ruta | Rol |
|---|---|
| `pom.xml`, `mvnw`, `.mvn/` | Build Maven (Spring Boot 4.1.1, Java 21) |
| `src/main/java/.../domain/` | `MetricCatalog`, `MetricDefinition`, `MetricQuery`, `MetricData`, `MonitoringFailure` |
| `src/main/java/.../application/` | `MonitoringService` + puertos `port/in/QueryMetrics`, `port/out/MetricsSource` |
| `src/main/java/.../adapter/in/web/` | `MetricsController`, `ApiExceptionHandler` (RFC 7807), `RequestIdFilter`, `BoundedJson`, `QueryParameters` |
| `src/main/java/.../adapter/out/` | `prometheus/` (cliente, PromQL, mapper), `fixture/`, `support/` (límite de concurrencia/timeout) |
| `src/main/java/.../configuration/` | `MonitoringConfiguration`, `PrometheusProperties` |
| `src/main/resources/` | `application.yaml`, `static/openapi/monitoring-v0.1.json` |
| `src/test/` | 12 clases de prueba + 2 auxiliares (61 anotaciones `@Test`/`@ParameterizedTest`; 112 casos ejecutados según el HANDOFF del repo) |
| `Dockerfile` | Multi-etapa `eclipse-temurin:21` → JRE, usuario no root 10001 |

### 3.2 `software/gateway` (16 archivos)
| Ruta | Rol |
|---|---|
| `pom.xml` | Spring Boot 4.1.1 + Spring Cloud 2025.1.3 (`gateway-server-webflux`, `oauth2-resource-server`, actuator, micrometer-prometheus) |
| `SecurityConfiguration.java` | Decodificador JWT (RS256/ES256, JWKS), validadores de claims, RBAC por ruta, CORS, respuestas problem+json |
| `RequestIdFilter.java` | Correlación `X-Request-Id` validada por regex |
| `application.yaml` | 4 grupos de rutas (9 rutas), `StripPrefix`/`PrefixPath`, límites 2 MB, timeouts |
| `static/openapi/` | `gateway-v0.1.yaml`, `recommendations-v1.json` |
| `GatewayApplicationTests.java` | 12 pruebas de integración con upstream simulado |

### 3.3 `software/gateway-go` (14 archivos)
`cmd/gateway/main.go` (arranque, apagado ordenado, `-healthcheck`), `internal/policy/routes.go` (tabla de rutas = dominio), `internal/auth/jwks.go` (verificador JWKS con caché y backoff), `internal/httpapi/server.go` (CORS, autenticación, autorización, proxy inverso), pruebas `*_test.go` (32 pruebas de nivel superior), `tools/difftest/` (prueba diferencial contra el Gateway Java).

### 3.4 `software/data-processing` (74 archivos)
| Ruta | Rol |
|---|---|
| `main.py` | App FastAPI 1.1.0, middleware de correlación, manejadores RFC 7807 |
| `domain/` | `errors.py` (jerarquía `ServiceError`), `validation.py` (UTC, rangos), `monitoring_contract.py` (Pydantic), `ports/` (4 puertos) |
| `application/use_cases/` | `process_metrics`, `prepare_prediction_dataset`, `read_historical_logs`, `historical_report`, `process_greenai_dataset` |
| `infrastructure/adapters/input/` | API (`routes.py`, `models.py`), `monitoring_http_adapter`, `supabase_historical_logs_adapter`, `sqlite_historical_logs_adapter`, `greenai_excel_adapter` |
| `infrastructure/adapters/output/` | `csv_dataset_repository` |
| `infrastructure/persistence/` | `sqlite/schema.sql`, `postgres/contract-schema.sql`, `01-authenticator.sh` |
| `datasets/raw/synthetic_greenai/` | `BD_GreenAi.xlsx` (7,3 MB; 50 hardware, 100 000 logs, hoja Usuarios), muestra CSV |
| `scripts/` | ETL (`run_greenai_etl.py`), semilla SQLite, exportación OpenAPI, smoke Docker |
| `tests/` | 14 módulos + 1 fixture (129 casos: 121 OK + 8 omitidos por PostgREST no configurado) |

### 3.5 `software/prediction` (131 archivos)
| Ruta | Rol |
|---|---|
| `src/service/app.py` | API FastAPI: `/health*`, `/v1/predictions`, `/predict` |
| `src/service/recommendations.py` | `/v1/recommendations`, `/v1/energy`, `/metrics` (prometheus-client) |
| `src/recommendations/policy.py` | Motor de política (función pura) |
| `src/inference/`, `src/adapters/` | Inferencia, adaptadores de contrato de entrada/salida |
| `src/preprocessing/`, `src/data/` | Limpieza, remuestreo, variables temporales, lags, ventanas móviles, validación, generador sintético |
| `src/models/`, `src/training/`, `src/evaluation/` | Baselines (persistencia, media móvil), Random Forest, XGBoost; pipeline de entrenamiento y comparación |
| `src/drift/`, `src/mlflow/` | PSI/deriva de error; registro opcional en MLflow |
| `config/config.yaml` | Hiperparámetros, horizontes (5/15/30 min), splits 70/15/15 |
| `contracts/` | `prediction.openapi.json`, `recommendations-gateway.openapi.json`, `dataset-v1.schema.json`, `prediction-v1.schema.json` |
| `application/`, `domain/`, `infrastructure/` | **Carpetas hexagonales vacías** (solo `.gitkeep`) |
| `requirements*.txt` | 4 archivos: rangos, lock, servicio mínimo, desarrollo |
| `tests/` | 23 módulos de prueba (100 casos) |

### 3.6 `software/simulator` (33 archivos)
`domain/` (`engine.py`, `inventory.py`, `scenario.py`, `state.py`), `application/runner.py`, `adapters/` (CLI, parsers JSON, `prometheus/exporter.py`, `persistence/run_logger.py`), `configs/` (inventarios de 50 nodos, escenarios low/normal/high), `pyproject.toml` + `uv.lock`, 4 módulos de prueba (10 casos).

### 3.7 `software/frontend` (46 archivos)
6 páginas HTML (`index`, `login`, `register`, `dashboard`, `network`, `flows`), 17 módulos JS (`app.js` autenticación/fetch, `monitoring.js`, `prediction.js`, `recommendations.js`, `pmv2.js`, `racks.js`, `flows*.js`, `energy.js`, `aggregate.js`, `ui-kit.js`…), 6 hojas CSS (`styles2.css` no referenciada), `nginx.conf`, `supabase-auth-setup.sql`, `config.example.js`, 8 suites `node:test` (48 casos).

### 3.8 `software/infraestructura` (15 archivos)
`docker-compose.yml` (7 servicios, proyecto `green-ai-mono`), overlays `compose.swagger.yaml`, `compose.gateway-go.yml`, `compose.sqlite-dev.yml`, `compose.contract-postgres.yml`, `compose.observability.yml` (Grafana); `prometheus/` (`prometheus.yml`, `prometheus.render.yml`, `alerts.yml` con 6 reglas, `Dockerfile.render`); `grafana/` (datasource + dashboard `pmv2.json`); `smoke/smoke.py` (14 casos HTTP).

## 4. Archivos de dependencias detectados

| Archivo | Servicio | Gestor |
|---|---|---|
| `software/monitoring/pom.xml` | Monitoring | Maven |
| `software/gateway/pom.xml` | Gateway Java | Maven |
| `software/gateway-go/go.mod` | Gateway Go | Go modules (sin `require`) |
| `software/data-processing/requirements.txt` | Data Processing | pip (**codificado en UTF-16 LE con BOM y fin de línea CRLF**) |
| `software/prediction/requirements.txt`, `requirements.lock.txt`, `requirements.serve.txt`, `requirements-dev.txt` | Prediction | pip |
| `software/simulator/pyproject.toml`, `uv.lock` | Simulator | uv / hatchling |
| CDN en `software/frontend/*.html` | Frontend | Sin gestor (jsDelivr/cdnjs con SRI) |

## 5. Archivos de configuración detectados

`.env.example` (data-processing, prediction), `infrastructure/settings.py`, `src/config/settings.py`, `config/config.yaml`, `application.yaml` (×2), `config.example.js`, `nginx.conf`, `docker-compose.yml` + overlays, `prometheus*.yml`, `alerts.yml`, Grafana provisioning, `render.yaml`, workflows de GitHub Actions, `pytest.ini`, `.python-version`.

## 6. Observaciones del inventario

1. El repositorio mezcla **código ejecutable** (≈52 %) con **material académico** (informes, guías docentes, capturas, Word/Excel), lo que eleva el peso del clon (~43 MB de binarios).
2. `software/prediction/{application,domain,infrastructure}/` son esqueletos vacíos: la lógica real vive en `src/`.
3. `software/data-processing/requirements.txt` está codificado en UTF-16 LE, a diferencia del resto de archivos (UTF-8).
4. `software/frontend/styles2.css` no está referenciado por ninguna página.
5. No hay secretos versionados: la búsqueda de patrones (`sb_secret_`, `service_role`, JWT `eyJ…`, claves privadas, tokens de GitHub/AWS) no arrojó coincidencias. Sí aparece el *project ref* público de Supabase (`jpfugpsdhuucmilgysgg`) en 7 archivos y contraseñas sintéticas en texto plano en la hoja `Usuarios` de `BD_GreenAi.xlsx`.
