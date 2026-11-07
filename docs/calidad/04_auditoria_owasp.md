# Auditoría de Seguridad OWASP Top 10 (2021) — Green AI Monorepo

**Documento:** `docs/calidad/04_auditoria_owasp.md`  
**Fecha:** 2026-11-07  
**Rol:** Auditor de Seguridad Especializado en OWASP Top 10  
**Estándar de referencia:** OWASP Top 10:2021 (A01–A10) y Guía FURPS+ / OWASP (Semana 13)  
**Entorno evaluado:** Monorepo Green AI (`software/`: `gateway`, `gateway-go`, `monitoring`, `data-processing`, `prediction`, `simulator`, `frontend`, `infraestructura`)  
**Modo:** Solo lectura de código estático y configuraciones. Sin ejecución de comandos intrusivos ni modificación de código.

---

## 1. Resumen Ejecutivo y Línea Base de Pruebas

La presente auditoría evalúa la postura de seguridad del proyecto **Green AI** frente al estándar **OWASP Top 10:2021**. El análisis se basa estrictamente en evidencia verifiable extraída del código fuente, descriptores de despliegue, configuraciones de infraestructura y canalizaciones de CI/CD del monorepo.

### Línea Base de Pruebas Verificadas (según `docs/HANDOFF.md`)
El proyecto cuenta con un conjunto amplio de pruebas automatizadas que verifican los contratos de software y el comportamiento del perímetro:
- **Monitoring Service:** 112 tests unitarios y de integración (`0` fallos).
- **Gateway Service (Java):** 11/12 tests de contrato y seguridad superados (`0` fallos en línea base).
- **Data Processing Service:** 121 tests pasados (incluye 114 pruebas de contrato y perfil de desarrollo SQLite/PostgREST, y 7 tests de reportes históricos).
- **Prediction Service:** 100 tests pasados (`pytest` con modelo Random Forest seleccionado).
- **Frontend:** 48 tests unitarios (`node --test tests/*.test.cjs`).
- **Simulator:** 10/10 tests en contenedor Docker (`1` fallo específico de señales en Windows nativo documentado).
- **Smoke End-to-End local:** 14/14 comprobaciones superadas con datos simulados en stack Docker Compose (`smoke.py`).

---

## 2. Alcance y Metodología de Evaluación

Se examinaron las 10 categorías de riesgos de seguridad web definidas por OWASP (Top 10:2021):
1. **A01:2021 — Broken Access Control** (Pérdida de Control de Acceso)
2. **A02:2021 — Cryptographic Failures** (Fallos Criptográficos)
3. **A03:2021 — Injection** (Inyección)
4. **A04:2021 — Insecure Design** (Diseño Inseguro)
5. **A05:2021 — Security Misconfiguration** (Configuración de Seguridad Incorrecta)
6. **A06:2021 — Vulnerable and Outdated Components** (Componentes Vulnerables y Obsoletos)
7. **A07:2021 — Identification and Authentication Failures** (Fallos de Identificación y Autenticación)
8. **A08:2021 — Software and Data Integrity Failures** (Fallos en la Integridad del Software y de los Datos)
9. **A09:2021 — Security Logging and Monitoring Failures** (Fallos de Registro y Monitoreo de Seguridad)
10. **A10:2021 — Server-Side Request Forgery (SSRF)** (Falsificación de Peticiones del Lado del Servidor)

---

## 3. Evaluación Detallada por Categoría OWASP Top 10

*Tabla. Resumen de la evaluación OWASP Top 10 (2021).*

| ID | Categoría | Estado | Severidad máxima |
|---|---|---|---|
| A01 | Broken Access Control | Requiere Atención | Alto (no verificado) |
| A02 | Cryptographic Failures | Requiere Atención | Alto (no verificado) |
| A03 | Injection | Conforme / Mitigado | Bajo |
| A04 | Insecure Design | Requiere Atención | Medio |
| A05 | Security Misconfiguration | Requiere Atención | Medio |
| A06 | Vulnerable and Outdated Components | Requiere Atención | Medio |
| A07 | Identification and Authentication Failures | Conforme con Observación | Medio |
| A08 | Software and Data Integrity Failures | Requiere Atención | Bajo |
| A09 | Security Logging and Monitoring Failures | Requiere Atención | Medio |
| A10 | Server-Side Request Forgery (SSRF) | Conforme / Mitigado | Bajo |

---

### A01:2021 — Broken Access Control (Pérdida de Control de Acceso)

* **Estado:** Requiere Atención (Controles perimetrales sólidos; riesgo latente en base de datos externa no verificado).
* **Evidencia en Código:**
  1. **Control perimetral RBAC en Gateway Java:** En `software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java:L58-L80`, se extrae el claim `user_role` y se restringe el acceso:
     * Lectura (`GET /api/monitoring/v1/**`, `GET /api/processing/v1/**`): roles `OPERATOR`, `ADMIN` y `VIEWER` (observador de solo lectura, HU-14).
     * Modificación/Inferencia (`POST /api/prediction/v1/predictions`, `POST /api/recommendations/v1/**`): roles `OPERATOR` y `ADMIN` únicamente (`VIEWER` denegado).
     * Política restrictiva por defecto: `.anyExchange().denyAll()`.
  2. **Control perimetral RBAC en Gateway Go:** En `software/gateway-go/internal/policy/routes.go:L68-L78`, la función `Allows(role)` aplica la misma política idéntica: `VIEWER` solo ejecuta peticiones `GET`.
  3. **Riesgo en Políticas RLS Supabase (No verificado en vivo):** En el snapshot del esquema verificado `software/simulator/docs/assets/esquema-verificado.json:L458-L492`, se registran políticas RLS permisivas:
     * `"Permitir todo en hardware"`, `"Permitir todo en logs"`, `"Permitir todo en usuario"` con `cmd: "ALL"`, `roles: ["public"]`, `qual: "true"`.
     * Si estas políticas persisten en la instancia remota de Supabase, la clave pública (`publishable key` del frontend) permitiría a cualquier cliente eludir el Gateway y modificar datos directamente vía PostgREST (`/rest/v1/`). *Nota: Estado actual no verificado directamente en la nube por política de seguridad.*
  4. **Exposición de puertos en Docker Compose:** En `software/infraestructura/docker-compose.yml:L42-L43`, el servicio `monitoring` expone `127.0.0.1:18080:8080` y `simulator` expone `127.0.0.1:18000:8000` en la interfaz local sin requerir JWT.
* **Impacto:** Alto en caso de persistir RLS permisivas (pérdida de confidencialidad e integridad de telemetría y usuarios). Medio en red local por exposición de puertos directos.
* **Probabilidad:** Media (requiere interacción directa con Supabase conociendo la URL y clave pública, o acceso a la interfaz loopback).
* **Severidad:** **Alto** (por riesgo latente de RLS en base de datos externa).
* **Hallazgos:**
  * `OW-01`: Riesgo de elusión de Gateway mediante políticas RLS Supabase permisivas (`cmd: ALL`, `roles: public`) en `hardware`, `logs` y `usuario` (no verificado en vivo).
  * `OW-02`: Exposición de puertos de microservicios internos en `docker-compose.yml` (`18080`, `18000`) sin capa de autorización perimetral local.

---

### A02:2021 — Cryptographic Failures (Fallos Criptográficos)

* **Estado:** Requiere Atención (Criptografía de tokens robusta; riesgo latente de columna password en snapshot y contraseñas sintéticas en planilla).
* **Evidencia en Código:**
  1. **Validación criptográfica JWT/JWKS:**
     * En `software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java:L31-L32`, se aceptan exclusivamente firmas asimétricas seguras `RS256` y `ES256`.
     * En `software/gateway-go/internal/auth/jwks.go:L72-L73`, se rechaza explícitamente el algoritmo `none`, claves simétricas `HS256` y confusión de algoritmos. En `software/gateway-go/internal/auth/jwks.go:L304-L306`, se exige longitud de clave RSA $\ge 2048$ bits y exponente impar $\ge 3$.
  2. **Columna password en base de datos (No verificado en vivo):** En `software/simulator/docs/assets/esquema-verificado.json:L400-L426`, la tabla `usuario` contiene tanto `password` (varchar 255) como `password_hash` (varchar 255). Almacenar contraseñas en texto plano vulnera directamente las garantías de confidencialidad criptográfica (*no verificado en el estado actual de producción*).
  3. **Credenciales sintéticas en repositorio:** En `software/data-processing/datasets/BD_GreenAi.xlsx` (hoja `Usuarios`), se registran contraseñas sintéticas en texto plano (`Admin123!N`). Aunque no son credenciales reales de producción, representan un riesgo si fueron reutilizadas al provisionar cuentas.
  4. **Protección de datos en tránsito:** El despliegue de desarrollo en Render (`render.yaml:L6-L60`) y GitHub Pages opera forzadamente bajo HTTPS/TLS. En local (`software/infraestructura/docker-compose.yml`), la comunicación entre contenedores ocurre por HTTP en red aislada.
* **Impacto:** Alto si la columna `password` contiene credenciales reales en la base de datos externa. Bajo en el transporte debido a TLS en endpoints públicos.
* **Probabilidad:** Baja/Media (depende del estado de la base de datos en Supabase).
* **Severidad:** **Alto** (por riesgo latente de almacenamiento de contraseñas sin hash en base de datos externa).
* **Hallazgos:**
  * `OW-03`: Presencia de columna `password` junto a `password_hash` en el esquema de la tabla `usuario` de Supabase (no verificado en el estado actual).
  * `OW-04`: Inclusión de credenciales sintéticas en texto claro en dataset Excel versionado (`BD_GreenAi.xlsx`).

---

### A03:2021 — Injection (Inyección)

* **Estado:** Conforme / Mitigado (Consultas SQL, PostgREST y PromQL fuertemente parametrizadas).
* **Evidencia en Código:**
  1. **Inyección SQL en Data Processing (Perfil SQLite):** En `software/data-processing/infrastructure/adapters/input/sqlite_historical_logs_adapter.py:L38-L49`, todas las cláusulas `WHERE`, marcas de tiempo y límites emplean parámetros vinculados (`?` placeholders). No hay concatenación de cadenas en variables de entrada. Además, se conecta en modo estricto de solo lectura (`?mode=ro`, línea 32).
  2. **Inyección PostgREST (Supabase REST API):** En `software/data-processing/infrastructure/adapters/input/supabase_historical_logs_adapter.py:L12-L15`, se implementa la función `quoted(value)` para escapar barras invertidas y comillas dobles en los filtros PostgREST, y los parámetros de consulta se transmiten estructurados en tuplas a `httpx.Client.get` (líneas 31-45).
  3. **Inyección PromQL en Monitoring:** En `software/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/out/prometheus/PrometheusQueryBuilder.java:L27-L49`, la construcción de selectores PromQL escapa caracteres especiales (`quote(value)` en línea 47) y restringe las métricas permitidas a una lista blanca cerrada mediante `switch`, arrojando `MonitoringFailure.invalid("Métrica no permitida")` si no coincide.
  4. **Validación de entradas con Pydantic y FastAPI:** En `software/data-processing/infrastructure/adapters/input/api/routes.py:L23-L44`, los identificadores de clúster y recursos se validan con regex estricta `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$`, las fechas exigen zona horaria RFC3339 y los rangos numéricos imponen cotas (`stepSeconds` entre 15 y 3600, `limit` entre 1 y 500). En `software/data-processing/main.py:L45-L49`, el manejador de `RequestValidationError` no refleja datos arbitrarios inyectados en la respuesta.
* **Impacto:** Bajo (vectores de inyección SQL, PostgREST y PromQL neutralizados en código).
* **Probabilidad:** Muy Baja.
* **Severidad:** **Bajo**.
* **Hallazgos:**
  * No se detectaron vulnerabilidades de inyección críticas. Controles de parametrización verificados en un 100% del código analizado.

---

### A04:2021 — Insecure Design (Diseño Inseguro)

* **Estado:** Requiere Atención (Arquitectura hexagonal sólida y políticas seguras por defecto; falta rate limiting en Gateway).
* **Evidencia en Código:**
  1. **Principio Fail-Secure en Recomendaciones:** En `software/prediction/src/service/recommendations.py:L49-L50`, la configuración inválida impide el arranque en lugar de debilitar silenciosamente la política (`Policy.model_validate_json`). En la evaluación, las recomendaciones operan con `executionAllowed=false` de forma predeterminada para evitar acciones automatizadas no autorizadas sobre recursos.
  2. **Ausencia de limitación de tasa (Rate Limiting) en Gateway:** Ni en el Gateway Spring Cloud (`software/gateway/src/main/resources/application.yaml`) ni en el Gateway Go (`software/gateway-go/internal/httpapi/server.go`) se implementan filtros de limitación de tasa (Token Bucket / Redis Rate Limiter). Endpoints de alto costo computacional (`/api/prediction/v1/predictions` y `/api/recommendations/v1/recommendations`) pueden ser saturados por un cliente autenticado o scripting automatizado, ocasionando agotamiento de recursos.
  3. **Aislamiento de Entornos:** En `software/data-processing/infrastructure/settings.py:L64-L66`, el perfil SQLite se prohíbe explícitamente si `APP_ENV=production`, forzando el uso exclusivo de fuentes seguras en producción.
* **Impacto:** Medio (riesgo de denegación de servicio por agotamiento de CPU/memoria en el motor de inferencia).
* **Probabilidad:** Media (fácil de inducir mediante ráfagas de peticiones repetitivas).
* **Severidad:** **Medio**.
* **Hallazgos:**
  * `OW-05`: Ausencia de limitador de tasa de peticiones (Rate Limiter) en Gateway para endpoints de cómputo intensivo de inferencia y recomendaciones.

---

### A05:2021 — Security Misconfiguration (Configuración de Seguridad Incorrecta)

* **Estado:** Requiere Atención (CORS estricto y sin secretos en repos; faltan cabeceras de seguridad web en frontend).
* **Evidencia en Código:**
  1. **Política CORS estricta:** En `software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java:L48-L55` y en `software/gateway-go/internal/httpapi/server.go:L136-L173`, CORS rechaza orígenes comodín (`*`). Se exige coincidencia exacta con la variable `GATEWAY_CORS_ALLOWED_ORIGIN` (`http://127.0.0.1:13001` en local o `https://woshtsu.github.io` en Render). Preflight `OPTIONS` restringe métodos a `GET, POST, OPTIONS` y cabeceras a una lista blanca cerrada.
  2. **Cabeceras HTTP en Frontend Nginx:** En `software/frontend/nginx.conf:L1-L10`:
     * Incluye: `X-Content-Type-Options: nosniff` y `Referrer-Policy: no-referrer`.
     * **Omite:** `Content-Security-Policy` (CSP), `X-Frame-Options: DENY` (o `frame-ancestors 'none'`), `Permissions-Policy` y `Strict-Transport-Security` (HSTS).
     * **Anulación en location:** En la línea 8, `location = /config.local.js { add_header Cache-Control "no-store" always; }` anula las directivas `add_header` del bloque `server` debido al comportamiento intrínseco de Nginx (los bloques hijos descartan las cabeceras padre si declaran su propio `add_header`).
  3. **Manejo de Secretos y Variables de Entorno:**
     * En `.gitignore:L4-L14`, se bloquean `.env`, `.env.*`, `*.pem`, `*.key`, `secrets/` y `software/frontend/config.local.js` (L69).
     * En `software/data-processing/.env.example` y `software/frontend/config.example.js`, no hay credenciales hardcodeadas (solo marcadores vacíos o instrucciones).
     * En `render.yaml:L56-L60`, todas las variables sensibles tienen `sync: false`, exigiéndose en el panel sin guardarse en el repositorio.
     * En `.github/workflows/pages.yml:L6-L7`, solo se inyecta la clave `SUPABASE_PUBLISHABLE_KEY` (pública para el cliente web); nunca `service_role` ni secretos de base de datos.
  4. **Exposición de Actuator:** En `software/gateway/src/main/resources/application.yaml:L61-L68`, solo se exponen `health,info,prometheus`. Los detalles de salud están ocultos (`show-details: never`) y no se exponen endpoints peligrosos como `env`, `heapdump` o `beans`.
  5. **Ejecución como Usuario No Root en Contenedores:**
     * Gateway Java (`software/gateway/Dockerfile:L8-L11`): usuario `10001` (`gateway`).
     * Gateway Go (`software/gateway-go/Dockerfile:L14`): usuario `nonroot:nonroot` en base Distroless.
     * Data Processing (`software/data-processing/Dockerfile:L15-L17`): usuario `app`.
     * Prediction (`software/prediction/Dockerfile:L34-L45`): usuario `10001:10001` (`appuser`).
     * Simulator (`software/simulator/Dockerfile:L8-L27`): usuario `simuser`.
     * Frontend (`software/frontend/Dockerfile:L1`): ejecuta en contenedor estándar `nginx:1.28.0-alpine` (proceso maestro root de Nginx, común en servidores estáticos).
* **Impacto:** Medio (ausencia de CSP y X-Frame-Options expone a Clickjacking e incrementa el radio de impacto de XSS).
* **Probabilidad:** Media.
* **Severidad:** **Medio**.
* **Hallazgos:**
  * `OW-06`: Falta de cabeceras HTTP de protección web en Nginx (`Content-Security-Policy`, `X-Frame-Options`, `Permissions-Policy`).
  * `OW-07`: Pérdida de cabeceras de seguridad en petición a `/config.local.js` por reemplazo de contexto en directiva `add_header` de Nginx.

---

### A06:2021 — Vulnerable and Outdated Components (Componentes Vulnerables y Obsoletos)

* **Estado:** Requiere Atención (Fijación rigurosa de dependencias de backend; bibliotecas frontend de CDN sin SRI).
* **Evidencia en Código:**
  1. **Fijación de dependencias de Backend:**
     * Python Data Processing: `software/data-processing/requirements.txt:L1-L27` fija todas las versiones con `==` (FastAPI 0.141.1, Pydantic 2.13.5, Pandas 3.0.5, Uvicorn 0.53.0).
     * Python Prediction: `software/prediction/requirements.lock.txt` y `software/prediction/requirements.serve.txt:L1-L10` fijan componentes de inferencia (scikit-learn 1.9.1, pandas 2.3.3, joblib 1.6.0).
     * Python Simulator: `software/simulator/pyproject.toml` y `uv.lock` bloquean el árbol completo con hashes mediante `uv sync --locked`.
     * Gateway Go: `software/gateway-go/go.mod:L1-L3` utiliza **cero dependencias externas**, basándose exclusivamente en la biblioteca estándar de Go 1.25.
     * Java Gateway & Monitoring: `software/gateway/pom.xml` y `software/monitoring/pom.xml` gestionan versiones declarativas mediante Spring Cloud BOM (`2025.1.3`).
  2. **Scripts frontend cargados desde CDN sin Subresource Integrity (SRI):**
     * En `software/frontend/login.html:L10-L60` e `software/frontend/index.html:L10`, se importan:
       * `https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.117.1`
       * `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`
     * Ninguno incluye los atributos `integrity="sha384-..."` ni `crossorigin="anonymous"`. Si un CDN externo o un proxy intermedio sufriese un compromiso o alteración de contenido, el cliente ejecutaría código malicioso en el navegador del usuario sin detección de integridad.
* **Impacto:** Medio (riesgo en la cadena de suministro en caso de envenenamiento de paquetes en CDNs públicos).
* **Probabilidad:** Baja (requiere compromiso de proveedores consolidados como jsDelivr o cdnjs).
* **Severidad:** **Medio**.
* **Hallazgos:**
  * `OW-08`: Carga de dependencias JavaScript/CSS de frontend desde CDN externos sin verificación de integridad de subrecursos (Subresource Integrity - SRI).

---

### A07:2021 — Identification and Authentication Failures (Fallos de Identificación y Autenticación)

* **Estado:** Conforme con Observación (Validación de identidad JWT exhaustiva; almacenamiento de sesión en localStorage).
* **Evidencia en Código:**
  1. **Validación rigurosa de tokens Supabase en Gateway:**
     * En `software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java:L33-L42` y `software/gateway-go/internal/auth/jwks.go:L114-L148`, se exige:
       * Coincidencia exacta del emisor (`iss == GATEWAY_AUTH_ISSUER_URI`).
       * Coincidencia de audiencia (`aud` contiene `authenticated`).
       * Presencia de expiración (`exp`) y vigencia estricta en el tiempo.
       * Sujeto no vacío (`sub != ""`).
       * Claim de rol base `role == "authenticated"`.
       * Rechazo de usuarios anónimos (`is_anonymous != true`).
  2. **Protección contra ataques de DoS por claves JWKS:** En `software/gateway-go/internal/auth/jwks.go:L37-L46`, se define un intervalo mínimo de recarga (`MinRefresh: 30 * time.Second`) y sincronización por exclusión mutua, impidiendo que peticiones con `kid` inventados saturen la red o el servidor JWKS de Supabase.
  3. **Almacenamiento de tokens en Frontend:** En `software/frontend/app.js:L17-L19`, la inicialización de Supabase (`flowType: 'pkce'`, `persistSession: true`) persiste el token de acceso y el token de refresco en el `localStorage` del navegador. Si existiese una vulnerabilidad XSS, los tokens pueden ser extraídos mediante scripts del DOM.
  4. **Protección de transporte de credenciales:** En `software/frontend/app.js:L54-L57`, la función `authenticatedFetch` comprueba que el destino coincida estrictamente con el origen del Gateway antes de adjuntar la cabecera `Authorization: Bearer <token>`, previniendo fugas involuntarias a orígenes ajenos.
* **Impacto:** Medio (compromiso del token de sesión si ocurre una inyección script en el cliente).
* **Probabilidad:** Baja (mitigada por control estricto de orígenes y ausencia de inyecciones HTML en el frontend).
* **Severidad:** **Medio**.
* **Hallazgos:**
  * `OW-09`: Almacenamiento de tokens JWT de sesión en el almacenamiento local (`localStorage`) del navegador en lugar de cookies con atributos `HttpOnly`, `Secure` y `SameSite`.

---

### A08:2021 — Software and Data Integrity Failures (Fallos en la Integridad del Software y de los Datos)

* **Estado:** Requiere Atención (Verificación de hash en artefactos ML; falta digest en acciones de CI e imágenes Docker).
* **Evidencia en Código:**
  1. **Integridad de Artefactos de Machine Learning:** En `software/prediction/src/inference/predict.py:L34-L44`, antes de deserializar el modelo entrenado con `joblib.load(model_path)`, se calcula su hash SHA256 mediante `sha256_file(model_path)` y se contrasta contra el campo `modelSha256` registrado en `metadata.json`. Si difiere, arroja `ArtifactIntegrityError` (código HTTP 503).
  2. **Acciones de GitHub Actions no ancladas por Commit SHA:** En `.github/workflows/ci.yml:L23-L24` y `.github/workflows/pages.yml:L38-L42`, los pasos de CI utilizan etiquetas mutables de versión (`actions/checkout@v4`, `actions/setup-node@v4`, `actions/setup-python@v5`, `actions/setup-go@v5`, `actions/setup-java@v4`, `actions/deploy-pages@v4`) en vez del hash inmutable de confirmación (`@commit-sha`). Si un tag es reescrito en el repositorio upstream, el pipeline podría ejecutar código modificado.
  3. **Imágenes base Docker sin digest:**
     * Con excepción del Gateway Go (`software/gateway-go/Dockerfile:L3-L10`, que fija `golang:1.25.14-alpine@sha256:...` y `distroless/static-debian12@sha256:...`), los demás Dockerfiles usan etiquetas flotantes:
       * Gateway Java: `maven:3.9.11-eclipse-temurin-21`, `eclipse-temurin:21-jre-jammy` (`software/gateway/Dockerfile:L1-L7`).
       * Monitoring: `eclipse-temurin:21-jdk-jammy`, `eclipse-temurin:21-jre-jammy` (`software/monitoring/Dockerfile:L1-L8`).
       * Data Processing: `python:3.14-slim` (`software/data-processing/Dockerfile:L1`).
       * Prediction: `python:3.11.9-slim-bookworm` (`software/prediction/Dockerfile:L2-L20`).
       * Simulator: `python:3.12-slim` (`software/simulator/Dockerfile:L1`).
       * Frontend: `nginx:1.28.0-alpine` (`software/frontend/Dockerfile:L1`).
* **Impacto:** Bajo en CI/desarrollo; medio en entornos de producción con auditoría estricta de procedencia de imágenes.
* **Probabilidad:** Baja.
* **Severidad:** **Bajo**.
* **Hallazgos:**
  * `OW-10`: Pasos de GitHub Actions referenciados por etiquetas de versión mutables en lugar de hashes de confirmación SHA inmutables.
  * `OW-11`: Imágenes base de Docker en la mayoría de servicios construidas a partir de tags flotantes sin fijación de digest criptográfico SHA256.

---

### A09:2021 — Security Logging and Monitoring Failures (Fallos de Registro y Monitoreo de Seguridad)

* **Estado:** Requiere Atención (Trazabilidad end-to-end con X-Request-Id y alertas de Prometheus; faltan registros de eventos de seguridad).
* **Evidencia en Código:**
  1. **Correlación distribuida con `X-Request-Id`:**
     * En Gateway (`software/gateway-go/internal/httpapi/server.go:L30-L107`), se valida la cabecera `X-Request-Id` contra regex segura `^[A-Za-z0-9._:-]{1,128}$` o se genera un UUIDv4 nuevo, propagándolo aguas abajo y hacia el cliente.
     * En Monitoring (`software/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/in/web/RequestIdFilter.java`), se captura el atributo y se incluye en respuestas estructuradas RFC 7807 `software/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/in/web/ApiExceptionHandler.java:L45`.
     * En Data Processing (`software/data-processing/main.py:L31-L37`) y Prediction (`software/prediction/src/service/app.py:L49-L55`), se conserva y propaga el identificador en cada solicitud.
  2. **Reglas de Alerta en Prometheus:** En `software/infraestructura/prometheus/alerts.yml:L1-L46`, se definen 6 alertas operativas validadas con `promtool`: `RecommendationsUnavailable`, `DemoPolicyBlocked`, `SimulatorTelemetryDown`, `NodeCpuSaturationRisk`, `NodeMemoryPressure` y `PredictedCpuHigh`.
  3. **Ausencia de Registro de Auditoría de Seguridad:**
     * Las respuestas de error 401 (`UNAUTHORIZED`) y 403 (`FORBIDDEN`) en el Gateway (`software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java:L81-L87` y `software/gateway-go/internal/httpapi/server.go:L118-L131`) no emiten un log estructurado de auditoría con dirección IP de origen, ruta solicitada e identificador de sujeto/token rechazado.
     * Prometheus no expone contadores ni alertas específicas sobre intentos de autenticación fallidos o picos de accesos denegados (detección de escaneo o ataques de fuerza bruta).
* **Impacto:** Medio (dificulta la detección temprana de intrusiones y el análisis forense post-incidente).
* **Probabilidad:** Media.
* **Severidad:** **Medio**.
* **Hallazgos:**
  * `OW-12`: Ausencia de eventos estructurados de auditoría de seguridad y métricas en Prometheus para intentos de acceso no autorizados (401/403) en la capa de Gateway.

---

### A10:2021 — Server-Side Request Forgery (SSRF) (Falsificación de Peticiones del Lado del Servidor)

* **Estado:** Conforme / Mitigado (URLs de servicios fijos por configuración; validación estricta de esquemas y sin redirecciones).
* **Evidencia en Código:**
  1. **Validación de URLs de servicio en Data Processing:** En `software/data-processing/infrastructure/settings.py:L7-L14`, la función `validate_url(value, *, secure=False)` descompone la URL con `urlsplit` y valida estrictamente:
     * El esquema debe ser `http` o `https` (para Supabase exige obligatoriamente `https`).
     * Exige presencia obligatoria de `hostname`.
     * Rechaza expresamente credenciales embebidas (`username`, `password`), parámetros de consulta (`query`) o fragmentos (`fragment`).
  2. **Prevención de SSRF por Redirección en Monitoring:** En `software/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/out/prometheus/PrometheusClient.java:L35-L37`, el cliente HTTP se configura con `HttpClient.Redirect.NEVER`, impidiendo que un servidor Prometheus comprometido o falsificado redirija las peticiones a interfaces de metadatos de nube (`http://169.254.169.254/`) o a servicios internos no previstos.
  3. **Rutas upstream estáticas en Gateway:** En `software/gateway-go/internal/policy/routes.go:L40-L53` y `software/gateway/src/main/resources/application.yaml:L8-L50`, todas las rutas de reenvío son inmutables y asignadas a servicios previamente configurados. No existe ningún parámetro ni cabecera de entrada que permita a un cliente especificar la dirección IP o destino de reenvío.
* **Impacto:** Bajo.
* **Probabilidad:** Muy Baja.
* **Severidad:** **Bajo**.
* **Hallazgos:**
  * No se identificaron vulnerabilidades de SSRF. La arquitectura no expone endpoints que reciban o resuelvan URLs controladas por el usuario.

---

## 4. Matriz Consolidada de Hallazgos de Seguridad

| ID Hallazgo | Categoría OWASP | Descripción del Hallazgo | Ubicación Principal | Severidad | Estado |
|---|---|---|---|---|---|
| **OW-01** | A01: Broken Access Control | Riesgo de RLS permisivas («Permitir todo») en Supabase que eluden el Gateway si la base externa no fue corregida | `software/simulator/docs/assets/esquema-verificado.json:L458-L492` | **Alto** | No verificado en BD remota |
| **OW-02** | A01: Broken Access Control | Puertos de `monitoring` (18080) y `simulator` (18000) expuestos directamente en el host Docker local sin autenticación | `software/infraestructura/docker-compose.yml:L13-L44` | **Medio** | Presente en local |
| **OW-03** | A02: Cryptographic Failures | Columna `password` en texto plano en la tabla `usuario` del snapshot de Supabase | `software/simulator/docs/assets/esquema-verificado.json:L400-L412` | **Alto** | No verificado en BD remota |
| **OW-04** | A02: Cryptographic Failures | Contraseñas sintéticas legibles en archivo Excel versionado en datasets | `software/data-processing/datasets/BD_GreenAi.xlsx` | **Bajo** | Presente |
| **OW-05** | A04: Insecure Design | Ausencia de Rate Limiting en el Gateway ante peticiones continuas a `/predictions` y `/recommendations` | `software/gateway-go/internal/httpapi/server.go` / `software/gateway/src/main/resources/application.yaml` | **Medio** | Presente |
| **OW-06** | A05: Security Misconfiguration | Ausencia de cabeceras de seguridad CSP, X-Frame-Options y Permissions-Policy en el frontend | `software/frontend/nginx.conf:L6-L9` | **Medio** | Presente |
| **OW-07** | A05: Security Misconfiguration | Sobrescritura de cabeceras padre en bloque `location = /config.local.js` de Nginx | `software/frontend/nginx.conf:L8` | **Bajo** | Presente |
| **OW-08** | A06: Vulnerable Components | Inclusión de scripts JS y CSS de CDN en frontend sin hash de integridad (SRI) | `software/frontend/login.html:L10-L60` | **Medio** | Presente |
| **OW-09** | A07: Authentication Failures | Persistencia del token de sesión Supabase en `localStorage` del navegador | `software/frontend/app.js:L18` | **Medio** | Presente |
| **OW-10** | A08: Integrity Failures | Acciones de GitHub CI referenciadas con tags mutables (`@v4`, `@v5`) en lugar de SHA inmutables | `.github/workflows/ci.yml:L23-L65` | **Bajo** | Presente |
| **OW-11** | A08: Integrity Failures | Imágenes base de Docker en la mayoría de servicios sin fijación por digest SHA256 | `software/*/Dockerfile` | **Bajo** | Presente |
| **OW-12** | A09: Logging & Monitoring | Ausencia de registro de auditoría de seguridad para peticiones 401/403 en el Gateway | `software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java:L81-L86` | **Medio** | Presente |

---

## 5. Cálculo y Justificación del Score Global de Seguridad

El puntaje global de seguridad se determina sobre una escala de **0 a 100**, asignando un peso equilibrado de 10 puntos a cada una de las 10 categorías de OWASP Top 10:2021, con deducciones proporcionales basadas en la severidad y verificación de los hallazgos identificados:

$$\text{Score Global} = \sum_{i=1}^{10} \text{Puntaje}(\text{A}_i)$$

### Desglose por Categoría:

1. **A01: Broken Access Control (Puntuación: 7.0 / 10)**  
   *Deducción (-3.0):* Controles de Gateway RBAC (ADMIN, OPERATOR, VIEWER) impecables (+9.0), pero penalizado por el riesgo latente de RLS permisivo en Supabase (`OW-01`, -2.0 por falta de verificación remota) y exposición de puertos directos en compose local (`OW-02`, -1.0).
2. **A02: Cryptographic Failures (Puntuación: 7.5 / 10)**  
   *Deducción (-2.5):* Criptografía asimétrica RS256/ES256 estricta en JWKS y TLS forzado (+9.0), pero penalizado por la presencia de columna `password` en el esquema verificado (`OW-03`, -2.0) y contraseñas sintéticas en el Excel (`OW-04`, -0.5).
3. **A03: Injection (Puntuación: 9.5 / 10)**  
   *Deducción (-0.5):* Parametrización exhaustiva en SQLite (`?`, `mode=ro`), escape en PostgREST (`quoted`), PromQL controlado por lista blanca y modelos Pydantic (`extra='forbid'`). Se descuenta 0.5 únicamente por el riesgo teórico inherente al ensamblado dinámico de filtros en PostgREST.
4. **A04: Insecure Design (Puntuación: 8.0 / 10)**  
   *Deducción (-2.0):* Arquitectura hexagonal y principio fail-secure en políticas de recomendaciones (+9.5), pero penalizado por ausencia de Rate Limiting perimetral para endpoints de inferencia (`OW-05`, -1.5) y falta de mitigación ante DoS algorítmico (-0.5).
5. **A05: Security Misconfiguration (Puntuación: 7.0 / 10)**  
   *Deducción (-3.0):* CORS estricto sin comodines, variables con `sync: false` y contenedores non-root (+9.0), pero penalizado por falta de cabeceras CSP, X-Frame-Options y Permissions-Policy (`OW-06`, -2.0) y pérdida de cabeceras en Nginx (`OW-07`, -1.0).
6. **A06: Vulnerable Components (Puntuación: 8.0 / 10)**  
   *Deducción (-2.0):* Dependencias de backend perfectamente bloqueadas con lockfiles y Go con 0 dependencias externas (+9.5), pero penalizado por scripts CDN en frontend sin hashes Subresource Integrity (`OW-08`, -1.5).
7. **A07: Identification and Authentication Failures (Puntuación: 8.5 / 10)**  
   *Deducción (-1.5):* Verificación minuciosa de claims JWT (iss, aud, exp, sub, no-anónimo) y backoff en JWKS (+9.5), pero penalizado por almacenamiento del token de sesión en `localStorage` del navegador (`OW-09`, -1.0).
8. **A08: Software and Data Integrity Failures (Puntuación: 7.5 / 10)**  
   *Deducción (-2.5):* Verificación SHA256 de artefactos de Machine Learning antes de carga (+9.0), pero penalizado por tags mutables en GitHub Actions (`OW-10`, -1.0) e imágenes Docker sin digest SHA256 (`OW-11`, -1.5).
9. **A09: Security Logging and Monitoring Failures (Puntuación: 8.0 / 10)**  
   *Deducción (-2.0):* Correlación mediante `X-Request-Id` y 6 alertas en Prometheus con Promtool (+9.5), pero penalizado por falta de registros de auditoría y métricas de seguridad para eventos 401/403 en el Gateway (`OW-12`, -1.5).
10. **A10: Server-Side Request Forgery (SSRF) (Puntuación: 9.5 / 10)**  
    *Deducción (-0.5):* Rutas estáticas, `validate_url` con rechazo de esquemas no permitidos, y `Redirect.NEVER` en HTTP client. Sin rutas controladas por usuarios. Se descuenta 0.5 por configuración externa de endpoints upstream sin resolución restrictiva de rangos IP privados.

---

### Resultado Final:

$$\mathbf{Score\ Global\ de\ Seguridad:\ 80.5\ /\ 100\quad (\approx 81\ /\ 100)}$$

**Dictamen:** **NIVEL DE SEGURIDAD BUENO / ROBUSTO A NIVEL PERIMETRAL Y DE CÓDIGO INTERNO.**  
El proyecto demuestra una madurez técnica notable en diseño seguro (arquitectura hexagonal, Gateway con validación JWT rigurosa, RBAC con soporte para `VIEWER`, prevención de inyecciones y control de orígenes CORS). Los puntos que reducen el puntaje se concentran principalmente en la superficie externa de la base de datos (riesgos latentes de RLS y columna `password` en Supabase pendientes de validación por el administrador), falta de cabeceras defensivas web (CSP/X-Frame-Options/SRI) en el frontend y ausencia de rate limiting y registros de auditoría en el Gateway.

---

## 6. Recomendaciones para el Plan de Remediación (Paso 6)

1. **Prioridad 1 (Remota / Administrador de Base de Datos):**
   * Validar en la consola web de Supabase que las tablas `hardware`, `logs` y `usuario` tengan habilitadas políticas RLS restrictivas basadas en la identidad del usuario (`auth.uid() = usuario_id`), eliminando las políticas `"Permitir todo"`.
   * Verificar la eliminación o vaciado definitivo de la columna `password` en la tabla `usuario`, garantizando el uso exclusivo de `password_hash` o de Supabase Auth nativo.
2. **Prioridad 2 (Configuración Web Frontend):**
   * Incorporar en `software/frontend/nginx.conf` las cabeceras `Content-Security-Policy`, `X-Frame-Options: DENY`, `Permissions-Policy` y asegurar que `add_header` en `location` preserve las directivas heredadas.
   * Agregar atributos `integrity="sha384-..."` y `crossorigin="anonymous"` a las etiquetas `<script>` y `<link>` que importan dependencias externas desde CDN en `index.html` y `login.html`.
3. **Prioridad 3 (Endurecimiento del Gateway):**
   * Configurar un filtro de Rate Limiting (ej. RequestRateLimiter en Spring Gateway o algoritmo Token Bucket en Gateway Go) para los endpoints de inferencia `/api/prediction/v1/predictions` y `/api/recommendations/v1/**`.
   * Agregar logs de auditoría estructurados (WARN) ante eventos 401 (`UNAUTHORIZED`) y 403 (`FORBIDDEN`), registrando IP de origen, timestamp y motivo de rechazo.
4. **Prioridad 4 (Cadena de Suministro y CI/CD):**
   * Anclar las imágenes base de los Dockerfiles a sus respectivos hashes SHA256 (siguiendo el ejemplo implementado en `software/gateway-go/Dockerfile`).
   * Fijar las acciones de GitHub Workflows (`ci.yml`, `pages.yml`) mediante SHA inmutables de confirmación.
