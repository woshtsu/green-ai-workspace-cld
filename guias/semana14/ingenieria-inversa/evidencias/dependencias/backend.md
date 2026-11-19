# Dependencias de backend — Prompt 3: Auditoría de Dependencias

> **Rol:** Especialista en Auditoría de Dependencias · **Fase 2**
> Archivos analizados: `software/monitoring/pom.xml`, `software/gateway/pom.xml`, `software/gateway-go/go.mod`, `software/data-processing/requirements.txt`, `software/prediction/requirements{,.lock,.serve,-dev}.txt`, `software/simulator/pyproject.toml` + `uv.lock`.
> Herramientas: lectura de manifiestos, instalación real con `uv` (Python), `pip-audit 2.x` contra la base OSV/PyPA (2026-11-19), consulta de últimas versiones en PyPI. Los árboles Maven **no** pudieron resolverse (Maven Central bloqueado por el proxy del entorno de auditoría).

## 1. Inventario completo

### 1.1 Monitoring — Java 21 / Maven (`pom.xml`)
| Dependencia | Versión | Alcance | Propósito |
|---|---|---|---|
| `spring-boot-starter-parent` | 4.1.1 | parent/BOM | Gestión de versiones |
| `spring-boot-starter-webmvc` | (BOM) | compile | API REST servlet |
| `spring-boot-starter-validation` | (BOM) | compile | Bean Validation |
| `spring-boot-starter-actuator` | (BOM) | compile | `/actuator/health`, probes |
| `micrometer-registry-prometheus` | (BOM) | runtime | `/actuator/prometheus` |
| `json-schema-validator` (com.networknt) | 3.0.7 | test | Pruebas de contrato OpenAPI/JSON Schema |
| `spring-boot-starter-{actuator,validation,webmvc}-test` | (BOM) | test | Pruebas |

### 1.2 Gateway — Java 21 / Maven (`pom.xml`)
| Dependencia | Versión | Alcance | Propósito |
|---|---|---|---|
| `spring-boot-starter-parent` | 4.1.1 | parent | — |
| `spring-cloud-dependencies` | 2025.1.3 | BOM | — |
| `spring-cloud-starter-gateway-server-webflux` | (BOM) | compile | Enrutamiento reactivo |
| `spring-boot-starter-security-oauth2-resource-server` | (BOM) | compile | Validación JWT/JWKS (Nimbus) |
| `spring-boot-starter-actuator` | (BOM) | compile | Health/probes |
| `micrometer-registry-prometheus` | (BOM) | runtime | Métricas |
| `spring-boot-starter-webflux-test` | (BOM) | test | `WebTestClient` |

### 1.3 Gateway Go (`go.mod`)
`module greenai/gateway`, `go 1.25`, **sin `require`**: solo biblioteca estándar. Superficie de cadena de suministro mínima. Imagen final `gcr.io/distroless/static-debian12:nonroot` fijada por digest.

### 1.4 Data Processing — Python 3.14 (`requirements.txt`, 27 líneas, UTF-16 LE)
| Paquete | Versión fijada | Tipo real | Última publicada (PyPI) |
|---|---|---|---|
| fastapi | 0.141.1 | producción | 0.165.0 |
| starlette | 1.6.0 | producción (transitiva fijada) | 1.10.0 |
| uvicorn | 0.53.0 | producción | 0.54.0 |
| pydantic / pydantic_core | 2.13.5 / 2.46.5 | producción | 2.14.4 |
| httpx | 0.28.1 | producción | 0.28.1 |
| pandas | 3.0.5 | producción | 3.1.1 |
| numpy | 2.5.3 | producción | 2.5.5 |
| openpyxl / et_xmlfile | 3.1.5 / 2.0.0 | producción (ETL Excel) | 3.1.5 |
| python-dateutil, six, tzdata, idna, anyio, h11, click, annotated-*, typing-* | — | transitivas | — |
| **pytest 9.1.1, pluggy, iniconfig, Pygments, packaging** | — | **desarrollo, mezcladas con producción** | pytest 9.2.0 |
| **colorama 0.4.6** | — | solo Windows (dependencia de click/pytest en Windows) | — |

Instalado en esta auditoría: **29 paquetes** (faltan fijar `httpcore` y `certifi`, que se resuelven de forma transitiva).

### 1.5 Prediction — Python 3.11.9
| Paquete | `requirements.txt` (rango) | `requirements.lock.txt` | `requirements.serve.txt` (imagen) | Última |
|---|---|---|---|---|
| pandas | ≥2.1,<3 | 2.3.3 | 2.3.3 | 3.1.1 |
| numpy | ≥1.26,<3 | 2.4.6 | 2.4.6 | 2.5.5 |
| scikit-learn | ≥1.4,<2 | 1.9.1 | 1.9.1 | 1.9.1 |
| xgboost | ≥2.0,<3 | 2.1.4 | — (import diferido) | 3.4.1 |
| joblib | ≥1.3,<2 | 1.6.0 | 1.6.0 | 1.6.0 |
| pyyaml | ≥6.0.1,<7 | 6.0.3 | 6.0.3 | 6.0.3 |
| fastapi | ≥0.115,<1 | 0.141.1 | 0.141.1 | 0.165.0 |
| uvicorn | ≥0.30,<1 | 0.53.0 | 0.53.0 | 0.54.0 |
| prometheus-client | ≥0.26,<0.27 | 0.26.0 | 0.26.0 | 0.26.0 |
| httpx | ≥0.28.1,<0.29 | 0.28.1 | — | 0.28.1 |
| mlflow | ≥2.14,<3 | 2.22.5 | — | **3.18.0** |
| statsmodels | ≥0.14,<1 | 0.15.0 | — | 0.15.0 |
| matplotlib / seaborn | — | 3.11.2 / 0.13.2 | — | 3.11.2 / 0.13.2 |
| pytest / pytest-cov | ≥8,<9 / ≥5,<6 | 8.4.2 / 5.0.0 | — | 9.2.0 / 7.1.0 |
| jupyter | ≥1,<2 | **no incluido en el lock** | — | — |

El lock fija solo dependencias de primer nivel: el entorno instalado tiene **90 paquetes** (p. ej. `starlette 1.10.0`, `pyarrow 19.0.1`, `flask 3.1.3`, `sqlalchemy 2.1.9`, `gunicorn 23.0.0` arrastrados por MLflow) sin versión fijada.

### 1.6 Simulator — Python ≥3.12 (`pyproject.toml` + `uv.lock`)
| Paquete | Restricción | Bloqueado (`uv.lock`) |
|---|---|---|
| prometheus-client | ≥0.20.0 | 0.26.0 |
| hatchling | build-system | — |

## 2. Dependencias de producción vs. desarrollo

| Servicio | Producción (imagen final) | Desarrollo / CI |
|---|---|---|
| Monitoring | webmvc, validation, actuator, micrometer | json-schema-validator, starters `*-test` |
| Gateway | gateway-server-webflux, oauth2-resource-server, actuator, micrometer | webflux-test |
| Gateway Go | stdlib | stdlib (`testing`, `-race`) |
| Data Processing | **Todo `requirements.txt` (incluye pytest)** — no existe separación | — |
| Prediction | `requirements.serve.txt` (8 paquetes; imagen 510 MB según el repo) | `requirements.lock.txt` + `requirements-dev.txt` (MLflow, XGBoost, statsmodels, matplotlib, seaborn, pytest) — usados en la etapa *builder* y en CI |
| Simulator | prometheus-client (`uv sync --no-dev`) | — (pruebas con `unittest`) |

## 3. Dependencias críticas (si fallan, el sistema cae)

| Dependencia | Servicio | Motivo de criticidad |
|---|---|---|
| Spring Security OAuth2 Resource Server / Nimbus JOSE | Gateway Java | Toda la autenticación del sistema depende de la validación JWT/JWKS |
| `crypto/ecdsa`, `crypto/rsa`, `net/http/httputil` (stdlib Go) | Gateway Go | Equivalente al anterior en la alternativa Go |
| Spring Cloud Gateway (WebFlux/Netty) | Gateway Java | Único punto de entrada |
| FastAPI + Starlette + Pydantic | Data Processing, Prediction | Validación de contratos y servidor HTTP |
| scikit-learn + joblib | Prediction | Deserialización del modelo; **el artefacto `model.joblib` solo es compatible con la misma versión de scikit-learn** |
| pandas + numpy | Data Processing, Prediction | Ingeniería de características y procesamiento de series |
| prometheus-client | Simulator, Prediction | Exposición de métricas que alimentan Prometheus → Monitoring |
| httpx | Data Processing | Comunicación con Monitoring y Supabase |

## 4. Dependencias obsoletas o con versión rezagada

| Paquete | Usada | Última | Brecha | Observación |
|---|---|---|---|---|
| mlflow | 2.22.5 | 3.18.0 | **mayor (2 → 3)** | Rango `<3` en `requirements.txt` bloquea la actualización |
| xgboost | 2.1.4 | 3.4.1 | **mayor (2 → 3)** | Rango `<3`; solo candidato del pipeline (no se sirve) |
| pytest-cov | 5.0.0 | 7.1.0 | mayor | Rango `<6` |
| pytest (Prediction) | 8.4.2 | 9.2.0 | mayor | Rango `<9` |
| pandas (Prediction) | 2.3.3 | 3.1.1 | mayor | **Divergencia interna**: Data Processing ya usa pandas 3.0.5 |
| fastapi | 0.141.1 | 0.165.0 | 24 versiones menores | Ambos servicios |
| numpy | 2.4.6 / 2.5.3 | 2.5.5 | menor | Versiones distintas entre servicios |
| pyarrow (transitiva) | 19.0.1 | 26.0.1 | mayor | Arrastrada por MLflow |
| starlette (transitiva) | 1.6.0 / 1.10.0 | 1.10.0 | — | Divergencia entre servicios; aviso `StarletteDeprecationWarning` (usar `httpx2` en `TestClient`) observado en ambas suites |

Spring Boot 4.1.1 y Spring Cloud 2025.1.3 son líneas actuales (no verificable el último parche por el bloqueo de Maven Central).

## 5. Vulnerabilidades potenciales (pip-audit, OSV/PyPA, 2026-11-19)

| Alcance auditado | Resultado |
|---|---|
| `prediction/requirements.serve.txt` (imagen de inferencia) | **Sin vulnerabilidades conocidas** |
| `data-processing/requirements.txt` (29 paquetes instalados) | **Sin vulnerabilidades conocidas** |
| `simulator` (`uv.lock` exportado) | **Sin vulnerabilidades conocidas** |
| `prediction/requirements.lock.txt` + árbol instalado (90 paquetes) | **`mlflow 2.22.5`: 29 avisos únicos** (53 entradas con duplicados entre bases PYSEC/OSV), entre ellos PYSEC-2025-52, PYSEC-2026-93/94/195/419/421/423/424/425/1639/1656/1660/2219–2222/2654–2661/3686/3687, GHSA-gqvg-gmmx-x4hm, CVE-2026-53995 y CVE-2026-116691; versiones corregidas desde 3.1.0 hasta 3.17.x. **`pytest 8.4.2`: 1 aviso** (PYSEC-2026-1845, corregido en 9.0.3). **`pyarrow 19.0.1`** (transitiva de MLflow): **1 aviso** (PYSEC-2026-113, corregido en 23.0.1) |

**Valoración del riesgo:** MLflow, pytest y pyarrow **no llegan a la imagen de inferencia** (etapa *builder* y CI). El riesgo real se concentra en (a) la estación de desarrollo y el *runner* de CI, y (b) un eventual `mlflow ui`/`mlflow server` expuesto (la guía sugiere levantar la UI para capturas). Severidad: **Media**.

Riesgos de cadena de suministro adicionales:
- Ningún manifiesto Python usa *hashes* (`--require-hashes`); `pip-audit` lo advierte.
- El lock de Prediction no fija transitivas → builds no reproducibles en el tiempo.
- `model.joblib` se deserializa con `joblib.load` (pickle); se mitiga con verificación SHA-256 contra `metadata.json` antes de cargar.
- Java: no fue posible ejecutar OWASP Dependency-Check/OSV sobre el árbol Maven en este entorno → **pendiente**.

## 6. Dependencias relacionadas con seguridad

| Dependencia | Uso |
|---|---|
| `spring-boot-starter-security-oauth2-resource-server` | Validación JWT (RS256/ES256), emisor, audiencia, claims personalizados |
| Go stdlib `crypto/*` | Verificación JWS ES256/RS256, RSA ≥ 2048 bits |
| `cryptography` (transitiva de MLflow) | No usada por el código del servicio |
| supabase-js (frontend, CDN) | Sesión PKCE y renovación de tokens |
| `hashlib` (stdlib) | Integridad del modelo (`sha256_file`) y ruido determinista del simulador |

## 7. Dependencias relacionadas con persistencia

| Dependencia | Servicio | Persistencia |
|---|---|---|
| httpx → Supabase PostgREST (`/rest/v1/logs`) | Data Processing | Lectura de históricos (solo lectura) |
| `sqlite3` (stdlib) | Data Processing | Perfil de desarrollo `mode=ro` |
| openpyxl + pandas | Data Processing | Fuente ETL `BD_GreenAi.xlsx`; salida CSV |
| joblib | Prediction | Artefacto de modelo en disco |
| MLflow (`./mlruns`, SQLAlchemy/alembic transitivas) | Prediction | Tracking de experimentos local |
| Prometheus TSDB (imagen) | Infraestructura | Series temporales (efímero en Render: `/tmp`, 6 h) |

## 8. Dependencias relacionadas con APIs

| Dependencia | Rol |
|---|---|
| FastAPI / Starlette / Uvicorn / Pydantic | Servidores y validación de API (Data Processing, Prediction) |
| Spring WebMVC | API de Monitoring |
| Spring Cloud Gateway / `httputil.ReverseProxy` | Proxy inverso del Gateway |
| httpx | Cliente HTTP saliente (Monitoring, Supabase) |
| prometheus-client / Micrometer | API de métricas en formato de exposición Prometheus |
| json-schema-validator | Pruebas de contrato OpenAPI |

## 9. Conclusiones de la fase

1. El backend tiene una **huella de dependencias pequeña en producción** (Gateway Go sin dependencias; Prediction reducido a 8 paquetes de servicio) y **sin vulnerabilidades conocidas en las imágenes de ejecución Python**.
2. La deuda está en **desarrollo/CI**: MLflow 2.x con 29 avisos únicos, pytest en la imagen de Data Processing y locks parciales sin hashes.
3. **Inconsistencias entre servicios** (pandas 2.3 vs 3.0, numpy 2.4 vs 2.5, starlette 1.6 vs 1.10, tres versiones de Python) aumentan el costo de mantenimiento y el riesgo de incompatibilidad del contrato de dataset.
4. Falta un análisis SCA del árbol Maven (Spring Boot 4.1.1 / Spring Cloud 2025.1.3) en un entorno con acceso a Maven Central.
