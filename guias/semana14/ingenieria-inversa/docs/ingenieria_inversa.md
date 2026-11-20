# Reporte de Ingeniería Inversa

| Campo | Valor |
|---|---|
| Sistema | Green AI — monitoreo y predicción de demanda computacional |
| Repositorio | `https://github.com/woshtsu/green-ai-workspace-cld.git` (rama `main`, commit `27ef69f`, Merge PR #5) |
| Fecha | 2026-11-19 |
| Rol | Auditor de Software Senior especializado en Ingeniería Inversa |
| Método | Plan de 7 fases y 12 prompts; análisis estático + ejecución real del sistema |
| Evidencias | `evidencias/auditoria/`, `evidencias/dependencias/`, `evidencias/configuracion/`, `evidencias/ejecucion/` (incluye `logs/`), `evidencias/analisis/` |

## 1. Resumen Ejecutivo

Green AI es un sistema de **microservicios políglota** (Python, Java y Go) que observa la carga de CPU de un parque de 50 servidores simulados, **predice la demanda a 15 minutos** con un modelo Random Forest y propone ajustes de capacidad que **nunca se ejecutan automáticamente** (`executionAllowed=false`). Lo componen un frontend web estático, un API Gateway con autenticación JWT de Supabase y control de acceso por roles (ADMIN, OPERATOR, VIEWER), y cinco servicios: Monitoring (Java/Spring), Data Processing (FastAPI), Prediction (FastAPI + scikit-learn), Simulator (Python) y un Gateway alternativo en Go. Se observa con Prometheus y se despliega en GitHub Pages y en la capa gratuita de Render.

**Resultado de la ejecución.** Se reconstruyó el entorno en Ubuntu 24.04 y se ejecutó el sistema de forma nativa: **311 pruebas automatizadas sin fallos** (Data Processing 121 + 8 omitidas, Prediction 100, Frontend 48, Gateway Go 32, Simulator 10), el pipeline de entrenamiento (Random Forest seleccionado; MAE de prueba 3,85 puntos porcentuales), el smoke del repositorio (**12/14**: los 2 fallos corresponden a Monitoring, que no pudo compilarse porque Maven Central está bloqueado en el entorno de auditoría), una batería E2E propia con tokens firmados (**38/38**), un recorrido del frontend real con roles OPERATOR y VIEWER y una carga de 600 peticiones (**600/600 HTTP 200**, ninguna respuesta 500).

**Valoración.** La arquitectura es **sólida en diseño** —contratos explícitos, núcleo hexagonal en los servicios principales, validación JWT exhaustiva, honestidad de datos como regla transversal— pero **frágil en su despliegue y operación**. Calificación global: **3,0/5** (Cohesión 4, Acoplamiento 3, Escalabilidad 2, Mantenibilidad 3, Testabilidad 4, Seguridad 2).

**Hallazgos clave (23 en total: 2 críticos, 4 altos, 10 medios, 7 bajos):**
1. **Crítico — elusión del Gateway en la nube:** Prediction y Data Processing se publican como servicios web en Render y no autentican; cualquiera puede invocar la inferencia o leer los históricos de Supabase sin pasar por el control de roles.
2. **Crítico — RLS permisiva en Supabase** registrada en el repositorio («Permitir todo» en `hardware`, `logs` y `usuario`, con columna de contraseña en texto plano); combinada con la clave pública del frontend, permitiría leer y modificar datos. Su estado actual debe verificarse en Supabase.
3. **Alto — Prediction no escala:** recarga y re-verifica el modelo dos veces por petición; con 8 usuarios concurrentes la latencia mediana pasa de 97 ms a 1,14 s y el throughput baja de 9,8 a 7,0 req/s.
4. **Alto — cadena síncrona de 6 componentes** sin caché ni *circuit breaker*, y **deriva entre `render.yaml` y el despliegue real** (3 de los 6 servicios en Render se crearon a mano; producción y desarrollo comparten backend).

Corregir los cuatro hallazgos P1 (H-01 a H-04) eleva la seguridad a 4/5 y elimina el cuello de botella principal con un esfuerzo bajo-medio.

## 2. Objetivos

1. Identificar, sin suposiciones previas, todas las tecnologías, lenguajes, frameworks, bases de datos y servicios externos del repositorio.
2. Determinar el estilo arquitectónico real y su grado de conformidad por servicio.
3. Auditar las dependencias: inventario, criticidad, obsolescencia y vulnerabilidades conocidas.
4. Reconstruir el entorno de ejecución y documentar variables, secretos y configuración.
5. Ejecutar el sistema, analizar sus logs y clasificar los problemas encontrados.
6. Descubrir la funcionalidad expuesta: módulos, menús, formularios, procesos y APIs.
7. Reconstruir el modelo de dominio (DDD) y la arquitectura real, contrastándolos con la documentación del proyecto.
8. Evaluar la calidad arquitectónica y emitir hallazgos, riesgos y recomendaciones priorizadas.

## 3. Alcance

**Incluido**
- Los 746 archivos versionados del commit `27ef69f`, con foco en `software/` (7 servicios + infraestructura), `.github/workflows/`, `render.yaml` y la documentación técnica (`docs/`).
- Ejecución local de todos los componentes Python, Go, frontend y Prometheus; validación de reglas de alerta con `promtool`; análisis SCA de dependencias Python.

**Excluido o limitado**
- **Servicios Java (Monitoring y Gateway Java):** análisis solo estático; Maven Central está bloqueado por la política de red del entorno de auditoría. Se usaron como referencia las ejecuciones documentadas por el repositorio (112 y 11–12 pruebas), sin reproducirlas.
- **Docker:** Docker Hub bloqueado; los Dockerfiles y el Compose se analizaron estáticamente y el stack se levantó de forma nativa con el Gateway Go en lugar del Java.
- **Supabase real y servicios desplegados en Render:** no se accedió a ellos (ni se sondearon), por tratarse de sistemas en producción de terceros; los riesgos se derivan de la configuración versionada y de la documentación del equipo, y se reprodujeron localmente cuando fue posible.
- **CDNs del frontend:** bloqueados; se sirvieron las mismas versiones desde sus paquetes npm para el recorrido E2E.
- Material académico (`entregables/`, `guias/`) y herramientas de IA (`herramientas_IA/`, `.agents/`): solo inventariados.

## 4. Metodología

Se ejecutaron en orden los 12 prompts del plan; cada uno produjo una evidencia que alimentó a los siguientes.

| Fase | Prompts | Evidencias |
|---|---|---|
| 1 Auditoría | 1 Descubrimiento tecnológico · 2 Detección arquitectónica | `inventario_archivos.md`, `stack_tecnologico.md`, `arquitectura_detectada.md` |
| 2 Dependencias | 3 Dependencias | `backend.md`, `frontend.md`, `infraestructura.md` |
| 3 Instalación y configuración | 4 Reconstrucción del entorno · 5 Variables de entorno | `instalacion.md`, `variables_entorno.md`, `servicios.md` |
| 4 Ejecución | 6 Análisis de logs · 7 Descubrimiento funcional | `backend_logs.md`, `frontend_logs.md`, `endpoints_detectados.md`, `logs/` |
| 5 Ingeniería inversa | 8 Dominio · 9 Arquitectura | `dominio.md`, `modulos.md`, `casos_uso.md`, `arquitectura_real.md` |
| 6 Evaluación | 10 Evaluación · 11 Hallazgos | `calidad_arquitectura.md`, `hallazgos.md` |
| 7 Reporte | 12 Generador final | `docs/ingenieria_inversa.md` |

### 4.1 Auditoría
Clonado del repositorio, inventario con `git ls-files`, conteo de líneas por lenguaje, búsqueda de secretos por patrones (claves `sb_secret_`, `service_role`, JWT, claves privadas, tokens de GitHub/AWS) y lectura de manifiestos, Dockerfiles, Compose, workflows y del código de cada servicio. La arquitectura se dedujo de la estructura de carpetas **y** de los *imports* reales entre módulos.

### 4.2 Instalación
Reconstrucción en Ubuntu 24.04.5 (2 vCPU, 7 GiB): entornos con `uv` para Python 3.11.9 (Prediction), 3.12+ (Simulator) y 3.14 (Data Processing); Go 1.24.7 sobre una copia con `go 1.24` en `go.mod` (sin red a `proxy.golang.org` para descargar 1.25); Node 22; Prometheus 3.13.3 desde GitHub Releases. El procedimiento completo, con comandos y desviaciones, está en `evidencias/configuracion/instalacion.md`.

### 4.3 Configuración
Extracción exhaustiva de variables (`os.getenv`, `${VAR}`, `@Value`, `os.Getenv`), clasificación de secretos y tokens, base SQLite de desarrollo sembrada con `seed_sqlite.py` (50 hardware, 100 000 logs) y un **emisor JWT local de pruebas** (clave ES256 + JWKS) con los mismos claims que exige el Gateway, para probar la autenticación de punta a punta sin tocar el Supabase real.

### 4.4 Ejecución
1. Suites de pruebas de cada servicio ejecutable.
2. Pipeline de entrenamiento de Prediction.
3. Stack nativo: Simulator (50 nodos, tick 5 s) → Prometheus → Prediction, Data Processing (SQLite), Gateway Go, frontend estático.
4. Smoke del repositorio, batería E2E propia (38 casos), recorrido del frontend real en Chrome *headless* (roles OPERATOR y VIEWER), carga de 600 peticiones y medición de memoria.
5. `pip-audit` sobre los requisitos y los árboles instalados.

### 4.5 Ingeniería Inversa
Reconstrucción del dominio con DDD (contextos, entidades, objetos de valor, agregados, repositorios, reglas, casos de uso y diagramas UML en texto), reconstrucción de la arquitectura en vistas C4 (contexto y contenedores), relaciones, integraciones, flujos de datos y despliegue; contraste sistemático entre lo documentado y lo implementado.

## 5. Inventario Tecnológico

| Categoría | Tecnología | Evidencia | Confianza |
|---|---|---|---|
| Lenguajes | Python 3.11/3.12/3.14, Java 21, Go 1.25, JavaScript, HTML/CSS, SQL | Dockerfiles, `pom.xml`, `go.mod`, `.python-version` | Alta (Java: Media) |
| Backend | FastAPI 0.141.1 + Uvicorn + Pydantic 2.13 | `requirements*.txt`; servicios levantados | Alta |
| Backend | Spring Boot 4.1.1, Spring Cloud Gateway 2025.1.3, Spring Security OAuth2 RS | `pom.xml` | Media |
| Backend | Biblioteca estándar de Go (proxy, JWKS) | `gateway-go/`; ejecutado | Alta |
| ML | scikit-learn 1.9.1 (RF), XGBoost 2.1.4, pandas, NumPy, joblib, MLflow 2.22.5 | `requirements.lock.txt`; pipeline ejecutado | Alta |
| Frontend | HTML/JS sin framework, supabase-js 2.117.1, Chart.js 4.4.8, Font Awesome 6.4.0 (CDN + SRI), nginx 1.28 | `*.html`, `Dockerfile` | Alta |
| Bases de datos | Supabase PostgreSQL + PostgREST (producción), SQLite (desarrollo), PostgreSQL 17 + PostgREST v13 (pruebas de contrato) | Adaptadores, `schema.sql`, Compose | Alta/Media |
| Observabilidad | Prometheus 3.13.3 (6 alertas), prometheus-client, Micrometer, Grafana 12.4 | Compose, `alerts.yml`; ejecutado | Alta |
| Autenticación | Supabase Auth (JWT ES256/RS256 vía JWKS, PKCE) + claim `user_role` por *hook* PL/pgSQL | `supabase-auth-setup.sql`, `SecurityConfiguration.java`, `jwks.go` | Alta |
| DevOps | Docker multi-etapa, Compose (7 servicios + 5 *overlays*), GitHub Actions (6 jobs, acciones por SHA), GitHub Pages | `software/infraestructura/`, `.github/workflows/` | Media |
| Despliegue | Render (Oregon, gratuito, `runtime: docker`) | `render.yaml`, guía | Media |
| Ausentes | Mensajería/eventos, Kubernetes | Búsqueda negativa | Alta |

Tamaño: 746 archivos; código productivo ≈ 10 600 líneas y de prueba ≈ 5 500 (Python 9 577, Java 2 126, Go 1 639, JS 2 406 + 600). Detalle: `evidencias/auditoria/stack_tecnologico.md` e `inventario_archivos.md`.

## 6. Arquitectura Detectada

| Estilo | Presente | Confianza |
|---|---|---|
| Microservicios con API Gateway | Sí | Alta |
| Hexagonal (puertos y adaptadores) | Sí, por servicio | Alta en Monitoring, Data Processing y Gateway Go; Media en Simulator; **Baja en Prediction** (carpetas hexagonales vacías) |
| Clean Architecture | Parcial | Media |
| Por capas | Local (Prediction `src/`, frontend) | Media |
| MVC, Monolito modular, Event Driven | No | Nula |

**Arquitectura predominante: microservicios síncronos HTTP/JSON detrás de un API Gateway, con núcleo hexagonal por servicio, en un monorepo.** Patrones complementarios: *Anti-Corruption Layer* (Data Processing valida todo payload de Monitoring), *Strategy* por configuración (fuente de históricos `none|supabase|sqlite`), *Bulkhead* con timeout (16 consultas concurrentes a Prometheus) y paginación *keyset* con cursor ligado al alcance. Detalle: `evidencias/auditoria/arquitectura_detectada.md`.

## 7. Dependencias

| Ámbito | Situación |
|---|---|
| Producción Python | Sin vulnerabilidades conocidas (`pip-audit`): imagen de inferencia de Prediction (8 paquetes), Data Processing (29 instalados), Simulator |
| Entrenamiento/CI | **MLflow 2.22.5: 29 avisos únicos** (corregidos desde 3.1.0 hasta 3.17.x), pytest 8.4.2: 1, pyarrow 19.0.1: 1 — no llegan a la imagen de servicio |
| Gateway Go | Sin dependencias externas; imagen distroless por digest |
| Java | Spring Boot 4.1.1 / Cloud 2025.1.3, versiones gestionadas por BOM; **SCA pendiente** (Maven Central inaccesible) |
| Frontend | 3 bibliotecas por CDN con SRI; sin `package.json`; sin CSP |
| Obsolescencia | Saltos de versión mayor pendientes: MLflow 2→3, XGBoost 2→3, pytest-cov 5→7, Font Awesome 6→7; pandas 2.3 (Prediction) vs 3.0 (Data Processing) |
| Reproducibilidad | Locks sin *hashes*; el lock de Prediction no fija transitivas (90 paquetes resueltos); imágenes Python con etiquetas flotantes; pytest dentro de la imagen de Data Processing; `requirements.txt` en UTF-16 |

Dependencias críticas: Spring Security/Nimbus o stdlib `crypto` (autenticación), FastAPI/Pydantic (contratos), scikit-learn + joblib (el artefacto solo es compatible con la misma versión), Supabase (identidad y JWKS), Prometheus (métricas en vivo), CDNs (frontend). Detalle: `evidencias/dependencias/`.

## 8. Configuración

- **Variables obligatorias:** `GATEWAY_AUTH_ISSUER_URI` y `GATEWAY_AUTH_JWK_SET_URI` (Gateway); `SUPABASE_URL`, `SUPABASE_API_KEY` y `SUPABASE_READ_TOKEN` si `HISTORICAL_SOURCE=supabase`; `SQLITE_PATH` si `sqlite`; `supabaseUrl`, `supabasePublishableKey` y `gatewayBaseUrl` en el frontend; `GRAFANA_ADMIN_PASSWORD` y `CONTRACT_*` en sus *overlays*.
- **Validación *fail-fast*** de buena calidad en Data Processing (URLs, timeouts, coherencia de la fuente, SQLite prohibido en producción, rechazo de claves `sb_*` como token de lectura) y en el Gateway Go. La política de recomendación (`DEMO_POLICY_JSON`) inválida impide arrancar Prediction.
- **Secretos:** ningún `.env` real versionado; secretos de Render como `sync: false`. Riesgos: el token de lectura en la nube es la clave legacy `anon`; contraseñas sintéticas en texto plano en `BD_GreenAi.xlsx`.
- **Configuraciones sin efecto:** `ML_PORT`, `HOST`/`PORT` del Simulator.
- **Seguridad por defecto en local:** todos los puertos publicados en `127.0.0.1`; Prediction y Data Processing no se publican salvo con el *overlay* de Swagger.

Detalle: `evidencias/configuracion/variables_entorno.md` y `servicios.md`.

## 9. Ejecución

| Ejecución | Resultado |
|---|---|
| Data Processing `pytest` (Python 3.14) | 121 passed, 8 skipped (contrato PostgREST no configurado) |
| Prediction pipeline + `pytest` (3.11.9) | RF seleccionado (MAE 3,847 · RMSE 5,446 · sMAPE 7,67 % en test); 100 passed |
| Simulator `unittest` | 10/10 |
| Gateway Go `vet` + `test -race` | 32/32 |
| Frontend `node --test tests/*.test.cjs` | 48/48 (la forma `node --test tests/` falla) |
| Monitoring / Gateway Java | No ejecutable (Maven Central bloqueado) |
| `promtool check rules` | 6 reglas válidas |
| Smoke del repositorio | 12/14 (fallan los 2 casos de Monitoring) |
| E2E de la auditoría | 38/38: autenticación, RBAC, CORS, correlación, históricos, predicción, recomendación, energía, degradación y superficie expuesta |
| Frontend real (Chrome *headless*) | OPERATOR: reporte 200, energía 200 (0,281 kWh), Monitoring 503 con mensaje amigable; VIEWER: reporte 200, energía 403 «Tu rol no permite esta acción»; 0 errores de JavaScript |
| Carga (vía Gateway Go) | Predicción c=1: p50 97 ms, 9,8 req/s; c=8: p50 1 143 ms, 7,0 req/s; históricos c=8: p50 94 ms, 75 req/s; 600/600 HTTP 200 |
| Memoria (RSS) | Prediction 293 MiB, Data Processing 250 MiB, Prometheus 97 MiB, Simulator 30 MiB, Gateway Go 15 MiB |

**Hallazgos de logs más relevantes:** servicios internos sin autenticación (Crítico), cadena caída sin Monitoring (Alto), Prediction no escala (Alto), Gateway Go sin *access log* y 503 sin causa registrada (Medio), `samples.jsonl` del Simulator ≈ 242 MB/día sin rotación (Medio), deprecaciones de Starlette/anyio silenciadas en Prediction (Bajo). **Ninguna excepción no controlada ni respuesta 500 en ~1 100 peticiones.** Detalle: `evidencias/ejecucion/backend_logs.md`, `frontend_logs.md` y `logs/`.

## 10. Reconstrucción Arquitectónica

```text
Navegador ──PKCE──► Supabase Auth                      Prometheus ◄──scrape── Simulator (50 nodos)
    │                                                       ▲   │ query_range        ▲
    └─Bearer─► Gateway (Java local / Go nube) ──► Monitoring ───┘   │                  │ scrape
                 │  JWKS·RBAC·CORS·límites      ◄────────────────────┘                  │
                 ├──► Data Processing ──► Monitoring (ACL)  ──► Supabase PostgREST / SQLite
                 └──► Prediction (RF + política + energía) ─────────────────────────────┘
```

- **Componentes:** frontend estático, Gateway, Monitoring, Data Processing, Prediction, Simulator, Prometheus (+ Grafana opcional) y Supabase como plataforma externa.
- **Relaciones:** todas síncronas por HTTP; el Gateway reenvía `Authorization` y `X-Request-Id` pero los servicios internos **confían en la red** (no autentican).
- **Flujo de datos en vivo:** Simulator (tick 5 s) → Prometheus → Monitoring (PromQL, calidad, procedencia) → Data Processing (ratio → %, sin imputación) → Prediction (remuestreo a 5 min, 20 variables, RF, +15 min) → política → métricas de negocio → alertas.
- **Históricos:** `BD_GreenAi.xlsx` → Supabase `public.logs` (carga externa) o SQLite (desarrollo) → paginación *keyset* → resumen JSON/CSV.
- **Entrenamiento:** dentro del `docker build` de Prediction, sobre un dataset sintético de un solo nodo (3 días, 864 registros).
- **Despliegue en la nube:** GitHub Pages (producción en la raíz y desarrollo en `/dev/`) → un único Gateway Go `-dev` en Render → Prediction y Data Processing con **URL pública**; Monitoring, Prometheus y Simulator creados a mano fuera de `render.yaml`.

**Documentado vs. real:** el «punto de entrada único» solo se cumple en local; el hexagonal es nominal en Prediction; RFC 7807 no se usa en Prediction; en la nube el Gateway desplegado es el de Go; producción y desarrollo comparten backend; Kubernetes y RabbitMQ no existen en el repositorio. Detalle: `evidencias/analisis/arquitectura_real.md` y `modulos.md`.

## 11. Modelo de Dominio

**Subdominio núcleo:** predicción de demanda y **política de capacidad con revisión humana**. Soporte: observación, preparación de datos y simulación. Genérico: identidad y acceso.

| Elemento DDD | Principales |
|---|---|
| Entidades | Node, Hardware, HistoricalLog, Series, Prediction, Recommendation, SelectedModel, SimulationRun, UserAccount |
| Objetos de valor | Resource, MetricQuery, MetricDefinition, Sample, Period, HistoricalCursor, PredictionDataset, Policy, Telemetry, Check, PowerSample, EnergyResult, Scenario, ValueWithOrigin, Route, AppRole |
| Agregados | Inventory, SimulationRun, MetricResponse (lectura), HistoricalLog, Hardware, **Recommendation**, SelectedModel, UserAccount |
| Servicios de dominio | `evaluate_policy` (puro), integración de energía, `select_model`, `build_supervised_frame` / anti-fuga, `compare_distributions` (PSI), `MonitoringService`, `PrometheusQueryBuilder`, `compute_next_state` (determinista), `Route.Allows` |
| Repositorios | `HistoricalLogsSource` (Supabase/SQLite), `MetricsSource` (Prometheus/fixture), `DatasetSource`/`DatasetRepository` (Excel/CSV), artefactos de modelo (implícito), `RunLogger` |

**Reglas de negocio clave:** toda predicción es `estimated`; `executionAllowed` siempre falso; recomendación `blocked` si algún umbral falla (memoria > 85 %, latencia p95 > 500 ms, error > 1 %), `not_evaluable` si falta información o frescura (≤ 300 s), `eligible_for_review` en otro caso, con acción según CPU < 30 % / > 80 %; energía por integración trapezoidal con huecos ≤ 300 s y CO₂e solo con factor y fuente; históricos ≤ 31 días y Monitoring ≤ 24 h; calidad por muestra y prohibición de imputar; VIEWER solo lectura; rol OPERATOR por defecto al registrarse.

**Observaciones:** el agregado `Recommendation` es anémico y vive en el adaptador HTTP; no hay persistencia del ciclo propuesta → aprobación (HU-07); el modelo se entrenó con un único recurso sintético y se aplica a 50. Detalle con diagramas UML: `evidencias/analisis/dominio.md` y `casos_uso.md` (21 casos de uso: 8 verificados en ejecución, 2 no implementados).

## 12. APIs e Integraciones

**API pública (Gateway):** 10 operaciones de negocio y 2 grupos públicos.

| Método | Ruta | Roles |
|---|---|---|
| GET | `/api/monitoring/v1/metrics/{catalog,current,history}` | ADMIN, OPERATOR, VIEWER |
| GET | `/api/processing/v1/{metrics/history, historical-logs, prediction/dataset, reports/historical-summary}` | ADMIN, OPERATOR, VIEWER |
| POST | `/api/prediction/v1/predictions` | ADMIN, OPERATOR |
| POST | `/api/recommendations/v1/{recommendations, energy}` | ADMIN, OPERATOR |
| GET | `/actuator/health/**`, `/openapi/**` | Público |

**APIs internas:** Monitoring 3 + actuator; Data Processing 6 (+ `/docs`); Prediction 8 (+ `/docs`, `/metrics`); Simulator `/metrics` (4 254 series).

| Integración | Mecanismo | Observación |
|---|---|---|
| Supabase Auth | supabase-js PKCE; JWKS en el Gateway; *hook* `custom_access_token_hook` añade `user_role` | Rol por defecto OPERATOR; promoción manual por SQL |
| Supabase Data API | PostgREST `/rest/v1/logs`, 7 columnas, orden `(timestamp, log_id)` | Token de lectura = clave `anon` en la nube |
| Prometheus | Exposición (*pull*) + PromQL desde Monitoring | Sin autenticación; en Render vía HTTPS público |
| GitHub Pages / Actions | `pages.yml` genera `config.local.js` por rama | Producción y desarrollo apuntan al mismo Gateway |
| Render | Blueprint parcial + servicios manuales | Sin red privada; suspensión a los 15 min |

Contratos versionados: `monitoring-v0.1.json`, `data-processing-v1.openapi.json`, `prediction.openapi.json`, `recommendations-gateway.openapi.json`, `gateway-v0.1.yaml`, `dataset-v1.schema.json`, `prediction-v1.schema.json`. Detalle: `evidencias/ejecucion/endpoints_detectados.md`.

## 13. Hallazgos

| ID | Hallazgo | Severidad | Prioridad |
|---|---|---|---|
| H-01 | El Gateway puede eludirse en la nube: Prediction y Data Processing públicos y sin autenticación | Crítica | P1 |
| H-02 | RLS «Permitir todo» y columna `password` en texto plano en Supabase (según snapshot) | Crítica | P1 |
| H-03 | Token de lectura de históricos = clave legacy `anon` (sin mínimo privilegio) | Alta | P1 |
| H-04 | Prediction recarga y re-hashea el modelo dos veces por petición; no escala | Alta | P1 |
| H-05 | Cadena síncrona de 6 componentes sin caché, reintentos ni *circuit breaker* | Alta | P2 |
| H-06 | Deriva entre `render.yaml` y el despliegue real; producción y desarrollo comparten backend | Alta | P2 |
| H-07 | `/metrics`, `/docs`, `/openapi.json` y la UI de Prometheus públicos | Media | P2 |
| H-08 | Sin *access log* en el Gateway Go, sin registro de 401/403/503, `X-Request-Id` sin validar en Prediction | Media | P2 |
| H-09 | MLflow 2.22.5 (29 avisos) y otras dependencias de CI; locks sin *hashes*; imágenes flotantes | Media | P2 |
| H-10 | Frontend sin CSP, sesión en `localStorage`, dependencia dura de CDNs | Media | P2 |
| H-11 | Sin *rate limiting*; reporte de históricos de hasta 100 000 filas en una sola petición | Media | P2 |
| H-12 | Prediction no usa RFC 7807 (contrato de errores inconsistente) | Media | P3 |
| H-13 | Pruebas PostgREST omitidas, sin E2E autenticado en CI, Java no verificable aquí | Media | P2 |
| H-14 | Modelo entrenado con 1 nodo sintético y 864 registros, aplicado a 50 nodos | Media | P3 |
| H-15 | Simulator sin rotación (≈ 242 MB/día), clúster variable, sin `restart`; Prometheus efímero | Media | P3 |
| H-16 | Recomendaciones sin persistencia ni flujo de aprobación (HU-07); sin PDF (HU-13) | Media | P3 |
| H-17 | Health checks superficiales; `depends_on` sin condición de salud | Baja | P3 |
| H-18 | Gateway duplicado Java/Go | Baja | P3 |
| H-19 | Hexagonal nominal en Prediction; dominio anémico; `runner.py` acoplado | Baja | P4 |
| H-20 | Contraseñas sintéticas en texto plano en `BD_GreenAi.xlsx` | Baja | P3 |
| H-21 | Repositorio mezclado con ~43 MB de material académico | Baja | P4 |
| H-22 | RBAC: VIEWER no puede usar `/energy`; la UI muestra acciones no permitidas | Baja | P4 |
| H-23 | Higiene: UTF-16, configuraciones muertas, CSS sin uso, artefactos versionados reescritos, deprecaciones silenciadas | Baja | P4 |

Matriz completa con evidencia, impacto y recomendación por hallazgo: `evidencias/analisis/hallazgos.md`.

**Fortalezas verificadas:** validación JWT y RBAC rigurosos con *deny-all*; honestidad de datos (procedencia, calidad, sin imputación, sin ejecución automática); 311 pruebas sin fallos y 0 respuestas 500; contenedores endurecidos y CI fijada por SHA; contratos con validación en el consumidor; integridad del modelo por SHA-256 y protección anti-fuga temporal; Gateway Go de 15 MiB; decisiones documentadas como ADR.

## 14. Riesgos

| ID | Riesgo | Hallazgos | Probabilidad | Impacto | Nivel |
|---|---|---|---|---|---|
| RG-01 | Acceso no autorizado a datos históricos y de usuarios (lectura y, con RLS permisiva, escritura) | H-01, H-02, H-03, H-07 | Alta (URLs publicadas en el repositorio) | Alto | **Crítico** |
| RG-02 | Incumplimiento de protección de datos personales (Ley N.º 29733) por contraseñas en texto plano y RLS abierta | H-02, H-20 | Media | Alto | **Alto** |
| RG-03 | Indisponibilidad de la demostración o del servicio (arranque en frío, 429/504, caída de un eslabón de la cadena) | H-05, H-06, H-15, H-17 | Alta | Medio | **Alto** |
| RG-04 | Degradación de rendimiento con pocos usuarios concurrentes o por abuso | H-04, H-11 | Alta | Medio | **Alto** |
| RG-05 | Decisiones de capacidad basadas en un modelo no validado para los nodos reales | H-14 | Media | Medio | **Medio** |
| RG-06 | Regresiones no detectadas en integraciones reales (Supabase, Gateway Java/Go) | H-13, H-18 | Media | Medio | **Medio** |
| RG-07 | Compromiso de la cadena de suministro (dependencias de CI, CDNs, imágenes flotantes) | H-09, H-10 | Baja | Alto | **Medio** |
| RG-08 | Imposibilidad de diagnosticar incidentes o auditar accesos | H-08 | Media | Medio | **Medio** |
| RG-09 | Afirmaciones documentales sin sustento técnico (auditoría interna optimista) | H-12 y §10 | Media | Medio | **Medio** |
| RG-10 | Costo de mantenimiento creciente por heterogeneidad y deuda estructural | H-18, H-19, H-21, H-23 | Alta | Bajo | **Medio** |

## 15. Recomendaciones

**Inmediatas (P1, antes de seguir usando el entorno en la nube)**
1. **Cerrar la elusión del Gateway (H-01):** servicios privados o red privada; si el plan no lo permite, validar el JWT de Supabase también en Prediction y Data Processing reutilizando la lógica del Gateway Go, o exigir una cabecera firmada por el Gateway. Retirar del repositorio las URLs públicas de los servicios internos.
2. **Endurecer Supabase (H-02, H-03):** eliminar las políticas «Permitir todo», borrar la columna `password`, crear un rol de solo `SELECT` sobre `logs` con JWT dedicado y rotable, y rotar cualquier credencial afectada.
3. **Cargar el modelo una sola vez (H-04):** caché en memoria verificada por SHA-256 al iniciar, `uvicorn --workers` según núcleos; volver a medir con la misma carga.

**Corto plazo (P2)**
4. Resiliencia de la cadena en vivo: caché de corta duración, reintentos con *backoff*, *circuit breaker* y «último valor conocido» en el panel (H-05).
5. Infraestructura como código completa y separación real de producción y desarrollo (H-06).
6. Reducir la superficie pública: sin `/docs` en producción, `/metrics` protegido, Prometheus con autenticación (H-07).
7. Observabilidad: *access log* estructurado, eventos de seguridad, validación de `X-Request-Id`, trazas distribuidas (H-08).
8. Dependencias: MLflow ≥ 3.17, pytest ≥ 9.0.3, locks con *hashes*, imágenes por digest, una sola versión de Python (H-09).
9. Frontend: CSP, *self-hosting* de bibliotecas, mensajes de error específicos (H-10).
10. *Rate limiting* en el Gateway y reporte de históricos acotado o asíncrono (H-11).
11. CI: pruebas de contrato PostgREST como *service container* y E2E autenticado con un emisor JWT de pruebas como el de esta auditoría (H-13).

**Mediano plazo (P3–P4)**
12. Unificar errores en RFC 7807 (H-12) y corregir la auditoría interna.
13. Validar el modelo con datos multi-nodo y evaluación *walk-forward* (H-14).
14. Operación sostenible del Simulator y Prometheus: rotación, clúster estable, `restart`, volumen (H-15).
15. Persistir el ciclo de vida de las recomendaciones con auditoría (H-16).
16. Adoptar un único Gateway (H-18), completar el hexágono de Prediction (H-19) y separar el material académico (H-21).

## 16. Conclusiones

1. **El sistema hace lo que promete en su núcleo funcional.** Se verificaron en ejecución la predicción de CPU a 15 minutos, la recomendación con restricciones y revisión humana, el cálculo de energía, los históricos paginados y los reportes, con control de acceso por rol de punta a punta y sin errores no controlados.
2. **El diseño es de buena calidad para un proyecto de su alcance:** contratos explícitos, validación estricta, puertos y adaptadores en los servicios principales, documentación de decisiones y una disciplina poco común de honestidad sobre el origen de los datos (`simulated`, `estimated`, «energía modelada, no medida»).
3. **La seguridad real depende del despliegue, no del diseño.** El Gateway valida los tokens de forma ejemplar, pero en la nube puede eludirse porque los servicios internos son públicos y no autentican, y la base de datos registra políticas de acceso abiertas. Son los dos riesgos que deben resolverse antes que cualquier otra mejora.
4. **El principal límite técnico es la operación**: una cadena de seis componentes síncronos sobre una capa gratuita sin red privada, un servicio de predicción que no escala con la concurrencia y una infraestructura como código que no refleja lo desplegado.
5. **La documentación del proyecto es valiosa pero optimista** en varios puntos (hexagonal en todos los servicios, RFC 7807 en todos, punto de entrada único); este reporte los contrasta con evidencia verificable.
6. Con las cuatro acciones P1 —cerrar la elusión del Gateway, endurecer Supabase, ajustar el token de lectura y cachear el modelo— la calificación arquitectónica pasaría de **3,0 a 3,5/5** (Seguridad 2 → 4, Escalabilidad 2 → 3), con un esfuerzo estimado bajo-medio.

**Limitaciones de esta auditoría:** los servicios Java no se compilaron ni ejecutaron, no se utilizaron Docker ni las imágenes oficiales, y no se accedió a Supabase ni a Render; los riesgos de la nube se fundamentan en la configuración versionada y la documentación del equipo, y la ausencia de autenticación interna se reprodujo localmente.
