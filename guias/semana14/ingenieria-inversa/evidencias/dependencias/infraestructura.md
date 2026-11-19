# Dependencias de infraestructura — Prompt 3: Auditoría de Dependencias

> **Fase 2** · Imágenes base, herramientas DevOps, acciones de CI y servicios externos.
> Fuentes: 7 Dockerfiles, `software/infraestructura/*.yml`, `render.yaml`, `.github/workflows/{ci,pages}.yml`, `docs/GUIA-DESPLIEGUE-RENDER.md`.

## 1. Inventario de imágenes de contenedor

| Imagen | Uso | Fijación | Usuario | Observación |
|---|---|---|---|---|
| `golang:1.25.14-alpine@sha256:1ae0735f…` | Build Gateway Go | **Digest** | — | Ejecuta `go vet` + `go test` en el build |
| `gcr.io/distroless/static-debian12:nonroot@sha256:afa5c872…` | Runtime Gateway Go | **Digest** | `nonroot` | Sin shell; healthcheck por el propio binario |
| `maven:3.9.11-eclipse-temurin-21` | Build Gateway Java | Etiqueta | — | Ejecuta `mvn verify` (pruebas en el build) |
| `eclipse-temurin:21-jdk-jammy` / `21-jre-jammy` | Build/Runtime Monitoring y Gateway | Etiqueta | uid 10001 | — |
| `python:3.11.9-slim-bookworm` | Prediction (builder + runtime) | Etiqueta exacta | uid 10001 | Entrena el modelo **dentro del build**; elimina pip en runtime |
| `python:3.14-slim` | Data Processing | **Etiqueta flotante** | `app` | Instala pytest en la imagen |
| `python:3.12-slim` | Simulator | **Etiqueta flotante** | `simuser` | Instala `uv` sin versión (`pip install uv`) |
| `nginx:1.28.0-alpine` | Frontend; proxy de pruebas de contrato | Etiqueta | root (por defecto) | No copia `favicon.svg` |
| `prom/prometheus:v3.13.3` | Prometheus (local y Render) | Etiqueta | por defecto | `Dockerfile.render` hornea la configuración |
| `grafana/grafana:12.4.0` | Overlay de observabilidad | Etiqueta | por defecto | Exige `GRAFANA_ADMIN_PASSWORD` |
| `postgres:17.6-alpine` | Pruebas de contrato | Etiqueta | — | Solo loopback |
| `postgrest/postgrest:v13.0.7` | Pruebas de contrato | Etiqueta | — | Secretos aleatorios por ejecución |

## 2. Herramientas DevOps

| Herramienta | Versión | Evidencia |
|---|---|---|
| Docker Engine / Compose v2 | — | `docker-compose.yml` (`name: green-ai-mono`, `env_file.required: false`, `bind.create_host_path: false` exigen Compose ≥ 2.24) |
| GitHub Actions | `actions/checkout` v4, `setup-node` v4, `setup-python` v5, `setup-go` v5, `setup-java` v4, `configure-pages` v5, `upload-pages-artifact` v4, `deploy-pages` v4 | **Todas fijadas por SHA de commit** |
| Maven Wrapper | `.mvn/wrapper/maven-wrapper.properties` | Monitoring y Gateway |
| uv | sin versión fija (`pip install uv` en Docker) | Simulator |
| promtool | incluida en Prometheus 3.13.3 | Validación ejecutada en esta auditoría: `alerts.yml` → **SUCCESS: 6 rules** |
| Render Blueprint | `render.yaml` | 3 servicios `type: web`, `plan: free`, `autoDeployTrigger: "off"` |
| PlantUML, Pandoc/`md_a_docx.py`, Playwright, ffmpeg | Herramientas académicas | `herramientas_IA/` (no forman parte del runtime) |

## 3. Servicios externos requeridos

| Servicio | Obligatorio | Para qué | Credenciales |
|---|---|---|---|
| Supabase Auth | **Sí** (cualquier llamada autenticada) | Emisión de JWT y JWKS público | `SUPABASE_URL`, clave *publishable* (navegador) |
| Supabase Data API (PostgREST) | Opcional (`HISTORICAL_SOURCE=supabase`) | Históricos `public.logs` | `SUPABASE_API_KEY` + `SUPABASE_READ_TOKEN` (JWT de lectura) |
| Render | Solo nube | Hosting de Gateway Go, Prediction, Data Processing (Blueprint) + Prometheus, Simulator y Monitoring (creados manualmente) | Variables `sync: false` en el panel |
| GitHub Pages | Solo nube | Frontend (prod en raíz, dev en `/dev/`) | Variables de repositorio `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, `GATEWAY_URL_PROD`, `GATEWAY_URL_DEV` |
| jsDelivr, cdnjs, Google Fonts | Sí (navegador) | Bibliotecas y tipografías | — |

## 4. Dependencias críticas de infraestructura
1. **Supabase JWKS** (`/auth/v1/.well-known/jwks.json`): si no responde, el Gateway Go devuelve 503 y el Java no puede validar tokens nuevos.
2. **Prometheus**: sin él, Monitoring responde `METRICS_SOURCE_UNAVAILABLE` y la cadena Monitoring → Data Processing → Prediction (dataset en vivo) se interrumpe.
3. **Simulator**: única fuente de telemetría; sin él, las alertas `SimulatorTelemetryDown` se disparan y no hay datos frescos.
4. **Render (capa gratuita)**: suspensión tras 15 min de inactividad, ~1 min de arranque en frío, sin red privada (documentado en `docs/DECISIONES.md` D-07 y HANDOFF: 429/504 intermitentes entre servicios).

## 5. Obsolescencia y riesgos
| Elemento | Riesgo | Severidad |
|---|---|---|
| Etiquetas flotantes `python:3.14-slim`, `python:3.12-slim` | Builds no reproducibles; cambio silencioso de la base | Media |
| `pip install uv` sin versión | Cambio de comportamiento del instalador | Baja |
| Imágenes sin digest (salvo Gateway Go) | Cadena de suministro | Baja |
| Prometheus en Render con datos en `/tmp` y retención 6 h | Pérdida de histórico en cada reinicio | Media |
| Prometheus y Grafana sin autenticación propia; Prometheus en Render con URL pública | Exposición de métricas y topología | Media |
| Monitoring, Prometheus y Simulator creados a mano en Render, fuera de `render.yaml` (que declara Monitoring como `https://example.invalid`) | Deriva entre infraestructura como código y despliegue real; reconstrucción del entorno no reproducible | Media |

## 6. Dependencias por categoría solicitada
- **Seguridad:** Supabase Auth/JWKS, imágenes no root, distroless, acciones fijadas por SHA, cabeceras nginx, secretos solo por variables (`sync: false`, `${VAR:?}` en Compose).
- **Persistencia:** Supabase/PostgreSQL, SQLite (montaje `read_only`), volumen `grafana-data`, TSDB de Prometheus (sin volumen en Compose: se pierde con `down`).
- **APIs:** Gateway (Java/Go) como fachada; Swagger/OpenAPI expuestos vía overlay `compose.swagger.yaml` solo en loopback.

## 7. Conclusión
La infraestructura está bien endurecida a nivel de contenedor (usuarios no root, multi-etapa, distroless, *pinning* por SHA en CI) y la configuración local es segura por defecto (todos los puertos publicados en `127.0.0.1`). Las debilidades se concentran en el **entorno de nube gratuito**: sin red privada, con servicios internos publicados como `type: web`, Prometheus efímero y la mitad de los servicios creados a mano fuera del Blueprint.
