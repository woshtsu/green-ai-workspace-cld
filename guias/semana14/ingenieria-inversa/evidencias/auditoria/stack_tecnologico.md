# Stack tecnológico — Prompt 1: Descubrimiento Tecnológico

> **Rol:** Auditor de Software Senior · **Fase 1** · Repositorio `woshtsu/green-ai-workspace-cld` @ `27ef69f`
> Criterio de confianza: **Alta** = verificado en código/configuración **y** ejecutado en esta auditoría; **Media** = verificado en código/configuración, no ejecutado; **Baja** = solo mencionado en documentación.

## 1. Lenguajes encontrados

| Lenguaje | Versión declarada | Dónde | Evidencia |
|---|---|---|---|
| Python | 3.11.9 (Prediction), 3.12 (Simulator), 3.14 (Data Processing) | 3 servicios + herramientas | `.python-version`, `pyproject.toml` (`requires-python >=3.12`), Dockerfiles `python:3.11.9-slim-bookworm`, `python:3.12-slim`, `python:3.14-slim`; CI `python-version: '3.11'` y `'3.14'` |
| Java | 21 | Monitoring, Gateway | `<java.version>21</java.version>` en ambos `pom.xml`; imágenes `eclipse-temurin:21` |
| Go | 1.25 | Gateway Go | `go.mod` (`go 1.25`), imagen `golang:1.25.14-alpine` fijada por digest |
| JavaScript (ES2020+) | — | Frontend | 17 módulos `.js`, pruebas `node:test` (`.cjs`), Node 22 en CI |
| HTML5 / CSS3 | — | Frontend | 6 páginas, 6 hojas de estilo |
| SQL (PL/pgSQL, SQLite) | PostgreSQL 17 / SQLite 3 | Supabase, perfil dev | `supabase-auth-setup.sql`, `contract-schema.sql`, `sqlite/schema.sql` |
| YAML / JSON | — | Configuración y contratos | Compose, Prometheus, Render, OpenAPI |
| PowerShell | — | Scripts de soporte (Windows) | `herramientas_IA/**/*.ps1`, `scripts/*.ps1` |

## 2. Tabla de tecnologías

| Categoría | Tecnología | Evidencia | Confianza |
|---|---|---|---|
| Lenguaje | Python 3.11 / 3.12 / 3.14 | Dockerfiles, `.python-version`, `pyproject.toml`, `ci.yml`; suites ejecutadas con 3.11.9, 3.13 (uv) y 3.14 | Alta |
| Lenguaje | Java 21 | `pom.xml` (×2), Dockerfiles `eclipse-temurin:21` | Media (no compilado: Maven Central bloqueado en el entorno de auditoría) |
| Lenguaje | Go 1.25 | `go.mod`; `go vet` + `go test -race` ejecutados (toolchain 1.24.7, ver nota) | Alta |
| Lenguaje | JavaScript | `software/frontend/*.js`; `node --test` ejecutado (48/48) | Alta |
| Framework backend | FastAPI 0.141.1 + Uvicorn 0.53.0 + Pydantic 2.13 | `requirements.txt`, `requirements.serve.txt`; Data Processing y Prediction levantados | Alta |
| Framework backend | Spring Boot 4.1.1 (WebMVC, Validation, Actuator) | `software/monitoring/pom.xml` | Media |
| Framework backend | Spring Cloud Gateway 2025.1.3 (WebFlux) + Spring Security OAuth2 Resource Server | `software/gateway/pom.xml`, `SecurityConfiguration.java` | Media |
| Framework backend | Biblioteca estándar de Go (`net/http`, `httputil.ReverseProxy`, `crypto/ecdsa`, `crypto/rsa`) | `gateway-go/internal/**`; binario construido y ejecutado | Alta |
| Machine Learning | scikit-learn 1.9.1 (Random Forest), XGBoost 2.1.4, pandas 2.3.3, NumPy 2.4.6, joblib 1.6.0 | `requirements.lock.txt`, `src/models/*.py`; pipeline ejecutado: RF seleccionado (MAE test 3,85) | Alta |
| Machine Learning | statsmodels 0.15.0, matplotlib 3.11.2, seaborn 0.13.2 | `requirements.lock.txt`, `src/evaluation/plots.py` | Alta |
| MLOps | MLflow 2.22.5 (tracking local `./mlruns`) | `src/mlflow/tracking.py`, `config.yaml` (`mlflow:`) | Media (pipeline ejecutado con `--skip-mlflow`) |
| Datos / ETL | pandas 3.0.5 + openpyxl 3.1.5 (lectura de `BD_GreenAi.xlsx`) | `data-processing/requirements.txt`, `greenai_excel_adapter.py`; semilla SQLite ejecutada (50 hw, 100 000 logs, 7,3 s) | Alta |
| Cliente HTTP | httpx 0.28.1 | Adaptadores Monitoring/Supabase en Data Processing | Alta |
| Frontend | HTML/CSS/JS sin framework (vanilla), patrón de módulos globales | `software/frontend/` | Alta |
| Frontend | Chart.js 4.4.8 (CDN jsDelivr + SRI) | `dashboard.html:299` | Alta |
| Frontend | supabase-js 2.117.1 (CDN + SRI) | `login.html:60`, `dashboard.html:298` | Alta |
| Frontend | Font Awesome 6.4.0 (cdnjs + SRI), Google Fonts (Inter, Fira Code) | `<link>` en las páginas | Alta |
| Servidor web | nginx 1.28.0-alpine (puerto 3001, cabeceras de seguridad) | `frontend/Dockerfile`, `nginx.conf` | Media (sustituido por servidor estático en la ejecución) |
| Base de datos | Supabase (PostgreSQL gestionado + PostgREST/Data API) — tablas `hardware`, `logs`, `usuario`, `user_profiles`, `user_roles` | `supabase_historical_logs_adapter.py`, `supabase-auth-setup.sql`, `esquema-verificado.json`, `render.yaml` | Media |
| Base de datos | SQLite (perfil de desarrollo, solo lectura `mode=ro`) | `sqlite_historical_logs_adapter.py`, `schema.sql`, `seed_sqlite.py`; ejecutado | Alta |
| Base de datos | PostgreSQL 17.6 + PostgREST v13.0.7 (solo pruebas de contrato) | `compose.contract-postgres.yml` | Media (8 pruebas omitidas sin PostgREST) |
| Series temporales | Prometheus v3.13.3 (scrape, PromQL, reglas de alerta) | `docker-compose.yml`, `prometheus.yml`, `alerts.yml`; ejecutado: 2 targets UP, 6 reglas | Alta |
| Observabilidad | prometheus-client 0.26.0 (Python), Micrometer Prometheus (Java), Spring Actuator | `recommendations.py`, `exporter.py`, `pom.xml` | Alta |
| Observabilidad | Grafana 12.4.0 (dashboard `pmv2.json`, 5 paneles) | `compose.observability.yml` | Media |
| Autenticación | Supabase Auth (JWT ES256/RS256 vía JWKS, flujo PKCE en navegador) | `app.js` (`flowType: 'pkce'`), `SecurityConfiguration.java`, `jwks.go` | Alta (validado con emisor JWKS local) |
| Autorización | RBAC por claim `user_role` (`ADMIN`, `OPERATOR`, `VIEWER`) inyectado por `custom_access_token_hook` (PL/pgSQL) | `supabase-auth-setup.sql`, `policy/routes.go` | Alta |
| Seguridad de datos | Row Level Security de Supabase | `supabase-auth-setup.sql` (tablas de perfil) / `esquema-verificado.json` (políticas «Permitir todo») | Media |
| Contenedores | Docker (Dockerfiles multi-etapa, usuarios no root, distroless para Go) | 7 Dockerfiles | Media (Docker Hub bloqueado en el entorno) |
| Orquestación local | Docker Compose (proyecto `green-ai-mono`, 7 servicios, 5 overlays) | `software/infraestructura/*.yml` | Media |
| Gestor de paquetes | uv (Simulator, entornos locales), pip, Maven Wrapper | `uv.lock`, `mvnw` | Alta |
| CI | GitHub Actions: 6 jobs (frontend, prediction, data-processing, gateway-go, monitoring, imágenes Docker) con acciones fijadas por SHA | `.github/workflows/ci.yml` | Media (runs documentados en `docs/HANDOFF.md`; no consultados vía API) |
| CD frontend | GitHub Pages (main → raíz, test → `/dev/`), configuración inyectada desde variables de Actions | `.github/workflows/pages.yml` | Media |
| Despliegue backend | Render (plan gratuito, región Oregon, `runtime: docker`, `autoDeployTrigger: off`) | `render.yaml`, `Dockerfile.render`, `docs/GUIA-DESPLIEGUE-RENDER.md` | Media |
| Servicios externos | Supabase (Auth + Data API), CDN jsDelivr/cdnjs/Google Fonts, Render, GitHub Pages | Configuración y HTML | Alta |
| Herramientas de IA (desarrollo) | Claude Code, Antigravity (`agy`), Graphify | `CLAUDE.md`, `AGENTS.md`, `herramientas_IA/agentes/agy_task.py`, `graphify-out/` | Alta (solo tiempo de desarrollo) |
| Documentación | PlantUML, Markdown → DOCX (script propio) | `herramientas_IA/diagramas/*.puml`, `md_a_docx.py` | Media |
| Mensajería / eventos | **No encontrada** (no hay Kafka, RabbitMQ ni colas) | Búsqueda en dependencias y código | Alta (ausencia verificada) |
| Kubernetes | **No usado en este repo** (los manifiestos K8s quedaron en el workspace antiguo, D-03) | `docs/DECISIONES.md` | Alta (ausencia verificada) |

> **Nota de ejecución (Go):** `go.mod` exige `go 1.25`; el entorno de auditoría tiene Go 1.24.7 y no puede descargar el *toolchain* (proxy.golang.org inaccesible). Se ejecutó sobre una copia con `go 1.24` en `go.mod`; el código no usa APIs exclusivas de 1.25 (32/32 pruebas OK con `-race`).

## 3. Respuesta por dimensión solicitada

1. **Lenguajes:** Python, Java, Go, JavaScript, HTML/CSS, SQL, YAML, PowerShell.
2. **Frameworks:** FastAPI, Spring Boot 4, Spring Cloud Gateway (WebFlux), Spring Security, scikit-learn, XGBoost, MLflow; frontend sin framework.
3. **Backend:** 5 servicios HTTP (Monitoring, Gateway Java/Go, Data Processing, Prediction) + 1 CLI/exportador (Simulator).
4. **Frontend:** SPA multipágina estática servida por nginx (contenedor) o GitHub Pages (nube).
5. **Bases de datos:** Supabase/PostgreSQL (producción), SQLite (desarrollo), PostgreSQL+PostgREST (pruebas de contrato), Prometheus TSDB (métricas), artefacto `model.joblib` en disco (modelo).
6. **DevOps:** Docker, Docker Compose, GitHub Actions, GitHub Pages, Render Blueprint, Prometheus, Grafana, promtool, uv, Maven Wrapper.
7. **Servicios externos:** Supabase Auth/Data API, Render, GitHub Pages, CDNs (jsDelivr, cdnjs, Google Fonts).
8. **Autenticación:** Supabase Auth (OIDC-like, JWT firmados asimétricamente, JWKS público) + PKCE en el navegador + RBAC por claim personalizado.
9. **Despliegue:** Frontend en GitHub Pages; Gateway Go, Prediction y Data Processing declarados en `render.yaml`; Prometheus, Simulator y Monitoring creados **a mano** en Render (`Dockerfile.render`, guía de despliegue; `docs/CONTINUAR-EN-NUEVO-CHAT.md` registra 6 servicios `green-ai-*-dev`). El Blueprint no refleja el despliegue real: declara Monitoring con la URL de relleno `https://example.invalid`.

## 4. Conclusión técnica

Green AI es un **sistema políglota de microservicios** (Python, Java y Go) orientado a la **observación y predicción de la demanda de CPU** de un parque de servidores simulado, con un motor de recomendaciones que **nunca ejecuta acciones** (`executionAllowed=false`). El stack es moderno y de versiones muy recientes (Spring Boot 4.1.1, Python 3.14, Go 1.25, Prometheus 3.13), con disciplina de ingeniería visible: contratos OpenAPI versionados, errores RFC 7807 en la mayoría de los servicios, imágenes multi-etapa con usuarios no root y CI con acciones fijadas por SHA.

Las tensiones principales del stack son: (a) **heterogeneidad de runtimes** (tres versiones de Python y dos gateways equivalentes en lenguajes distintos) que multiplica el costo de mantenimiento; (b) una **dependencia fuerte de Supabase** para identidad, roles y datos históricos, cuya configuración RLS real no es verificable desde el repositorio; y (c) un **despliegue en capa gratuita de Render sin red privada**, que obliga a exponer públicamente servicios diseñados como internos. La confianza global del inventario es **alta** para Python, Go, frontend y Prometheus (ejecutados en esta auditoría) y **media** para los servicios Java (verificados solo estáticamente por restricciones de red del entorno).
