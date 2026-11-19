# Arquitectura detectada — Prompt 2: Detección Arquitectónica

> **Rol:** Arquitecto de Software · **Fase 1** · Base: estructura de carpetas, imports reales entre módulos, Dockerfiles, Compose y contratos.
> Escala de confianza: Alta (evidencia estructural + de código + ejecución), Media (estructural + código), Baja (indicios parciales), Nula (sin evidencia).

## 1. Matriz de estilos evaluados

| Estilo | ¿Presente? | Confianza | Alcance |
|---|---|---|---|
| Microservicios | **Sí** | **Alta** | Sistema completo |
| Arquitectura Hexagonal (Puertos y Adaptadores) | **Sí** | **Alta** en Monitoring, Data Processing y Gateway Go; **Media** en Simulator; **Baja** en Prediction | Interior de cada servicio |
| Clean Architecture | Parcial | Media | Data Processing, Monitoring |
| Arquitectura por Capas | Sí (local) | Media | Prediction (`src/`), Frontend |
| MVC | No | Nula | — |
| Modular Monolith | No | Nula | — |
| Event Driven Architecture | No | Nula (indicios de *pull* y alertas, no eventos) | — |

## 2. Microservicios — confianza Alta

**Evidencias**
- 6 procesos desplegables con runtime propio: `monitoring` (JVM), `gateway` (JVM) o `gateway-go` (binario estático), `data-processing` (CPython 3.14), `prediction` (CPython 3.11), `simulator` (CPython 3.12), `frontend` (nginx).
- Un `Dockerfile` por servicio y un servicio por bloque en `software/infraestructura/docker-compose.yml`.
- Comunicación exclusivamente por HTTP/JSON con contratos versionados: `monitoring-v0.1.json`, `data-processing-v1.openapi.json`, `prediction.openapi.json`, `gateway-v0.1.yaml`, `dataset-v1.schema.json`.
- **API Gateway** como único punto de entrada previsto (tabla de 9 rutas, `StripPrefix`/`PrefixPath`), con autenticación y RBAC centralizados.
- Despliegue y prueba independientes: 6 jobs de CI separados por servicio en `ci.yml`; 3 servicios separados en `render.yaml`.
- Propiedad de datos por servicio: solo Data Processing lee la base (`public.logs`); Prediction persiste solo su artefacto de modelo; Monitoring y Gateway no tienen base.

**Carpetas involucradas:** `software/*/`, `software/infraestructura/`, `render.yaml`, `.github/workflows/ci.yml`.

**Justificación técnica:** se cumplen los criterios de despliegue independiente, límites por capacidad de negocio (observar, procesar, predecir/recomendar, simular, exponer) y comunicación por red. Matices: (1) es un **monorepo** (un solo Git) y no hay *service discovery* (URLs por variables de entorno); (2) no hay comunicación asíncrona; (3) los servicios no se autentican entre sí (confianza en la red), lo que se vuelve crítico al desplegarlos con URL pública.

## 3. Arquitectura Hexagonal — confianza Alta (por servicio)

### 3.1 Monitoring (Java) — Alta
| Elemento hexagonal | Implementación |
|---|---|
| Dominio | `domain/MetricCatalog`, `MetricQuery` (invariantes: rango ≤ 24 h, paso 15–3600 s, regex de IDs), `MetricData` (records), `MonitoringFailure` |
| Puerto de entrada | `application/port/in/QueryMetrics` |
| Puerto de salida | `application/port/out/MetricsSource` (`@FunctionalInterface`) |
| Servicio de aplicación | `application/MonitoringService` (valida series, completa la grilla, marca `missing`/`non_finite`) |
| Adaptador de entrada | `adapter/in/web/MetricsController`, `ApiExceptionHandler` |
| Adaptadores de salida | `adapter/out/prometheus/*` (real), `adapter/out/fixture/*` (perfil `fixture`), `adapter/out/support/UnavailableMetricsSource` |
| Composición | `configuration/MonitoringConfiguration` (selección por perfil y por presencia de `MONITORING_PROMETHEUS_URL`) |

El dominio no importa Spring (solo `java.*`); `MonitoringService` es `final` y recibe `Clock` inyectado (testabilidad).

### 3.2 Data Processing (Python) — Alta
| Elemento | Implementación |
|---|---|
| Dominio | `domain/errors.py`, `validation.py`, `monitoring_contract.py` |
| Puertos | `domain/ports/metrics_source.py`, `historical_logs_source.py`, `dataset_source.py`, `dataset_repository.py` (ABC) |
| Casos de uso | `application/use_cases/*.py` (5) |
| Adaptadores | `infrastructure/adapters/input/` (API FastAPI, Monitoring HTTP, Supabase, SQLite, Excel) y `output/` (CSV) |
| Composición | `infrastructure/historical_sources.py` (fábrica por `HISTORICAL_SOURCE`) |

Desviación menor: los adaptadores **de salida** hacia Monitoring/Supabase/SQLite están ubicados en `adapters/input/` (nombre por dirección del dato, no del control).

### 3.3 Gateway Go — Alta
`internal/policy` es el dominio puro (tabla de rutas, roles, reescritura de prefijos; no importa `net/http`), `internal/auth.Verifier` es el puerto y `JWKSVerifier` su adaptador; `internal/httpapi` es el adaptador de entrada.

### 3.4 Simulator — Media
`domain/` (motor determinista basado en SHA-256, inventario, escenario, estado), `application/runner.py`, `adapters/` (CLI, JSON, Prometheus, logger). **Violación:** `application/runner.py` importa directamente adaptadores (`json_parser`, `scenario_parser`, `RunLogger`, `prometheus_client`) y gestiona señales del sistema operativo; la propia documentación del repo lo registra como refactor pendiente.

### 3.5 Prediction — Baja
Existen `application/ports/{inbound,outbound}`, `domain/{entities,services,value_objects}` e `infrastructure/adapters/...` **vacíos** (solo `.gitkeep`). La lógica real está en `src/` organizada por etapas técnicas del pipeline de ML. Hay adaptadores de contrato (`src/adapters/input_adapter.py`, `output_adapter.py`) y la política de recomendación es una función pura (`src/recommendations/policy.py`), pero no hay puertos explícitos.

## 4. Clean Architecture — confianza Media
Hay casos de uso explícitos y dependencias apuntando hacia el dominio en Data Processing y Monitoring, pero no existen capas de *entities* independientes de los DTO ni *presenters*: los modelos Pydantic/records cumplen a la vez el rol de entidad y DTO. Se considera una **variante hexagonal**, no una Clean Architecture completa.

## 5. Arquitectura por Capas — confianza Media
- **Prediction (`src/`):** `service` (HTTP) → `inference` → `preprocessing`/`adapters` → `models`/`data` → `config`. Dependencias descendentes, sin puertos.
- **Frontend:** capa de presentación (HTML) → módulos de interacción (`dashboard-ui.js`, `racks.js`) → lógica pura testeable (`aggregate.js`, `energy.js`, `flows-logic.js`) → acceso a API (`app.js: authenticatedFetch`).

## 6. MVC — confianza Nula
No hay controladores que rendericen vistas en servidor ni modelos de vista: los controladores Spring/FastAPI devuelven JSON y son adaptadores de entrada. El frontend no usa un framework MVC.

## 7. Modular Monolith — confianza Nula
Los módulos no comparten proceso ni base de datos; cada uno se compila y despliega por separado.

## 8. Event Driven Architecture — confianza Nula
No existen brokers ni colas (Kafka, RabbitMQ, NATS) en dependencias, código ni Compose. Las interacciones asíncronas observadas son: (a) *scraping* periódico de Prometheus (modelo *pull*), (b) reglas de alerta evaluadas por Prometheus sin Alertmanager configurado y (c) refresco periódico del frontend (30 s). Ninguna constituye arquitectura orientada a eventos. La documentación académica histórica menciona RabbitMQ, pero el propio `HANDOFF.md` lo marca como afirmación sin respaldo.

## 9. Conclusión — arquitectura predominante

**Microservicios con API Gateway y núcleo hexagonal por servicio, organizados en un monorepo.**

- Nivel de sistema: microservicios síncronos HTTP/JSON detrás de un Gateway con JWT + RBAC, más un pipeline de observabilidad *pull* (Simulator → Prometheus → Monitoring).
- Nivel de servicio: puertos y adaptadores en Monitoring, Data Processing y Gateway Go (alta conformidad), parcial en Simulator y nominal en Prediction.
- Patrones complementarios detectados: *API Gateway*, *Anti-Corruption Layer* (validación estricta de contratos entre Monitoring → Data Processing → Prediction), *Strategy* por configuración (fuente de históricos `none|supabase|sqlite`; `MetricsSource` real/fixture/no disponible), *Bulkhead/Timeout* (`BoundedMetricsSource` con 16 permisos y 5 s), *Keyset Pagination* con cursor ligado al alcance (hardware y periodo; codificado en Base64, no firmado).
