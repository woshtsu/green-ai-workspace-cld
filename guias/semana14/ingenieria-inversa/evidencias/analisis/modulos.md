# Módulos del sistema

> **Fase 5** · Descomposición por servicio y por módulo interno, con tamaño (líneas no vacías), responsabilidad, dependencias y pruebas. Las líneas se midieron sobre el commit `27ef69f`.

## 1. Vista general

| Servicio | Código productivo (líneas) | Código de prueba (líneas) | Ratio prueba/código | Pruebas ejecutadas en la auditoría |
|---|---|---|---|---|
| Monitoring (Java) | 910 | 805 | 0,88 | No (Maven bloqueado); repo: 112 casos |
| Gateway Java | 141 | 165 | 1,17 | No; repo: 11–12 casos |
| Gateway Go | 956 | 683 | 0,71 | **32/32** |
| Data Processing | 1 733 | 1 845 | 1,06 | **121 OK + 8 omitidas** |
| Prediction (`src/` + `scripts/`) | 3 745 | 1 218 | 0,33 | **100/100** |
| Simulator | 725 | 197 | 0,27 | **10/10** |
| Frontend (JS) | 2 406 | 600 | 0,25 | **48/48** |
| **Total** | **10 616** | **5 513** | 0,52 | **311 ejecutadas, 0 fallos** |

## 2. Módulos por servicio

### 2.1 Monitoring
| Módulo | Responsabilidad | Depende de |
|---|---|---|
| `domain` | Catálogo de métricas, consulta con invariantes, tipos de respuesta, errores | `java.*` |
| `application` | `MonitoringService`: validar series, completar grilla, calidad/estado | `domain`, puertos |
| `application.port.{in,out}` | Contratos `QueryMetrics`, `MetricsSource` | `domain` |
| `adapter.in.web` | Controlador REST, validación de parámetros, JSON acotado (`BoundedJson`), errores RFC 7807, correlación | Spring WebMVC |
| `adapter.out.prometheus` | Cliente HTTP, constructor PromQL, *mapper* de respuesta | `java.net.http`, Jackson 3 |
| `adapter.out.support` | `BoundedMetricsSource` (16 hilos, 5 s, sin cola), `UnavailableMetricsSource` | `java.util.concurrent` |
| `adapter.out.fixture` | Fuente de datos de prueba (perfil `fixture`) | — |
| `configuration` | Ensamblaje por perfil y propiedades validadas | Spring Boot |

### 2.2 Gateway Java
| Módulo | Responsabilidad |
|---|---|
| `SecurityConfiguration` | Decodificador JWT (Nimbus) + validadores; convertidor `user_role → ROLE_*`; reglas por ruta; CORS; respuestas 401/403 problem+json |
| `RequestIdFilter` | Correlación `X-Request-Id` validada |
| `application.yaml` | Tabla de rutas, filtros `StripPrefix`/`PrefixPath`/`RequestSize`, timeouts |

### 2.3 Gateway Go
| Paquete | Responsabilidad |
|---|---|
| `internal/policy` | **Dominio**: rutas, roles, reescritura |
| `internal/auth` | Puerto `Verifier` + `JWKSVerifier` (caché, *backoff* 30 s, recarga sin bloquear, RSA ≥ 2048) |
| `internal/httpapi` | Adaptador HTTP: CORS, autenticación, autorización, proxy, límites (cabeceras 16 KB, cuerpo 2 MB/64 KB), errores |
| `cmd/gateway` | Configuración por entorno, apagado ordenado, `-healthcheck` |
| `tools/difftest` | Prueba diferencial Java vs Go (39 casos según el repo) |

### 2.4 Data Processing
| Módulo | Responsabilidad | Tamaño aprox. |
|---|---|---|
| `domain/` | Errores tipados, validación temporal, contrato Pydantic de Monitoring, 4 puertos | ~210 líneas |
| `application/use_cases/` | 5 casos de uso: procesar métricas, dataset para Prediction, leer históricos, reporte, ETL Excel | ~850 líneas |
| `infrastructure/adapters/input/api` | Rutas FastAPI y modelos de respuesta | ~250 líneas |
| `infrastructure/adapters/input/*` | Adaptadores Monitoring HTTP, Supabase, SQLite, Excel | ~220 líneas |
| `infrastructure/adapters/output` | Repositorio CSV | 27 líneas |
| `infrastructure/settings.py`, `historical_sources.py` | Configuración *fail-fast* y fábrica de fuente | ~100 líneas |
| `main.py` | App, middleware de correlación, manejadores de error | 62 líneas |
| `scripts/` | ETL, semilla SQLite, OpenAPI, smoke, inspección | — |

### 2.5 Prediction
| Módulo (`src/`) | Responsabilidad | Líneas (`wc -l`) |
|---|---|---|
| `service/app.py` | Endpoints de salud y predicción; mapeo de errores | 144 |
| `service/recommendations.py` | Endpoints de recomendación, energía y `/metrics`; modelos Pydantic; métricas Prometheus | 199 |
| `recommendations/policy.py` | Motor de política (puro) | 29 |
| `inference/predict.py` | Carga y verificación del artefacto, inferencia desde ventana | 212 |
| `adapters/input_adapter.py`, `output_adapter.py` | Traducción del contrato de dataset ↔ DataFrame; contrato de salida | 400 |
| `preprocessing/` | Limpieza, remuestreo, variables temporales, lags/ventanas, anti-fuga | 743 |
| `data/` | Esquema, carga, validación, generador sintético | 767 |
| `models/` | Persistencia, media móvil, Random Forest, XGBoost | 217 |
| `training/train.py` | Pipeline completo de entrenamiento/selección | 504 |
| `evaluation/` | Métricas, comparación, selección, gráficos, informe | 438 |
| `drift/`, `mlflow/`, `reproducibility.py`, `exceptions.py`, `config/` | Deriva, tracking, semillas/SHA, errores, configuración | 378 |
| `application/`, `domain/`, `infrastructure/` (raíz del servicio) | **Vacíos** | 0 |

### 2.6 Simulator (líneas `wc -l`)
`domain/engine.py` (133), `inventory.py` (118), `scenario.py` (41), `state.py` (37); `application/runner.py` (139, mezcla orquestación + adaptadores + señales); `adapters/cli` (78), `configuration` (131), `persistence/run_logger.py` (75), `prometheus/exporter.py` (112).

### 2.7 Frontend
| Capa | Módulos |
|---|---|
| Acceso a API y sesión | `app.js` (Supabase, `authenticatedFetch`, login/registro, logout) |
| Lógica pura (testeada) | `aggregate.js`, `energy.js`, `flows-logic.js`, `metrics.js`, `friendly-errors.js` |
| Funcionalidad por vista | `monitoring.js`, `prediction.js`, `recommendations.js`, `pmv2.js`, `racks.js`, `flows.js`, `dashboard-ui.js` |
| UI transversal | `ui-kit.js`, `help-content.js`, `appearance.js` |
| Datos estáticos | `racks.json`, `experiment.json` |

## 3. Dependencias entre módulos (acoplamiento)

```text
frontend ──HTTP──► gateway ──HTTP──► monitoring ──HTTP──► prometheus ◄──scrape── simulator
                      │                   ▲                     ▲
                      ├──HTTP──► data-processing ──HTTP─────────┘ (vía monitoring)
                      │                   └──HTTPS──► supabase (logs)
                      └──HTTP──► prediction ◄──scrape── prometheus
frontend ──HTTPS──► supabase (auth)        gateway ──HTTPS──► supabase (JWKS)
```
- **Acoplamiento de contrato más fuerte:** Data Processing ↔ Monitoring (valida todo el sobre de respuesta) y Data Processing ↔ Prediction (dataset v1 «provisional»).
- **Acoplamiento temporal:** la predicción en vivo exige que Simulator, Prometheus, Monitoring y Data Processing estén arriba simultáneamente (cadena de 4 saltos síncronos).
- **Duplicación:** dos gateways con la misma política (Java y Go) que deben mantenerse equivalentes; el OpenAPI del Gateway se comparte copiándolo en el build de Go.

## 4. Observaciones
1. Los módulos con lógica de dominio pura (política, energía, flujos, agregados) están bien aislados y probados.
2. Prediction concentra el 35 % del código productivo y tiene la menor relación de pruebas por línea entre los servicios Python, aunque sus pruebas cubren los riesgos clave (anti-fuga temporal, contrato, integridad del artefacto).
3. El Simulator tiene la menor cobertura relativa (0,27) y el acoplamiento `application → adapters` ya identificado por el equipo.
