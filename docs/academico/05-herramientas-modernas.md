# C5 · Uso de herramientas modernas (AG-I11: crear, seleccionar, aplicar, reconocer limitaciones)

Base: `docs/historico/trabajos-desarrollados/5.Uso de herramientas modernas.md` y la guía `5.Uso de herramientas modernas.md`.
**Correcciones:**
- Solo figuran herramientas **usadas con evidencia**. Se retiran SonarQube, JMeter y OWASP ZAP como «usadas»:
  no hay reportes; se pueden incorporar en el PMV3.
- Se añaden las herramientas de IA empleadas en el desarrollo, con sus límites.

## 1. Necesidad → herramienta → evidencia
| Necesidad | Herramienta (versión) | Evidencia en el repo | Limitación reconocida |
|---|---|---|---|
| Generar telemetría reproducible | Simulator propio en Python (**creado**) | `software/simulator`, 10 pruebas | Datos sintéticos; no representa la carga de la UC |
| Recolectar y consultar métricas | Prometheus 3.13 | `software/infraestructura/prometheus` | Retención local corta; no es almacén histórico de largo plazo |
| API de métricas | Java 21 + Spring Boot | `software/monitoring` (112 pruebas) | JVM pesada (~210 MiB) |
| Gateway, JWT, RBAC, CORS | Spring Cloud Gateway; Go 1.25 (alternativa **creada**) | `software/gateway`, `software/gateway-go` (30 pruebas; 0 diferencias en 39 casos) | Java: 520 MB de imagen; Go: aún sin prueba con usuario real |
| ETL e históricos | Python, FastAPI, pandas, openpyxl | `software/data-processing` (114 pruebas) | Pandas carga todo en memoria |
| ML y predicción | scikit-learn, XGBoost, pandas, NumPy | `software/prediction` (96 pruebas; pipeline reproducible) | Datos simulados; los árboles no extrapolan |
| Persistencia y autenticación | Supabase (PostgreSQL + Auth); SQLite en desarrollo | `supabase-auth-setup.sql`; D-05 | Plan gratuito; SQLite no tiene RLS ni procedimientos |
| Contenedores | Docker, Docker Compose | `software/infraestructura/docker-compose.yml` | No es orquestación de producción |
| Pruebas | JUnit, pytest, `node --test`, Go `testing`, smoke HTTP propio | Suites y `smoke.py` | Sin pruebas de carga ni de seguridad dinámicas |
| Contratos | OpenAPI 3.1 | `contracts/*.json`, `static/openapi/*` | Hay que regenerarlos al cambiar el código |
| Gestión ágil | Trello | Tablero (mover al workspace UC) | Métricas limitadas (sin burndown nativo) |
| Código y versiones | Git, GitHub; monorepo | Historial del monorepo | — |
| Modelado | PlantUML | `herramientas_IA/diagramas/edt-green-ai.puml` | Requiere un renderizador |
| Paneles | Grafana 12.4 (opcional) | `software/infraestructura/grafana` | No hay medición de kWh real |
| Asistentes de IA en el desarrollo | Claude Code, Antigravity CLI 1.5.2, Graphify 0.9.96 | `docs/TOOLS_EVALUATION.md` | En la revisión 03, 1 de 8 hallazgos del agente era falso; un `SUCCESS` puede venir vacío. **Todo resultado se verificó a mano** |

## 2. Selección ponderada (ejemplos; criterios: adecuación 25, funcionalidad 20, integración 15, costo 10, seguridad 10, escalabilidad 10, usabilidad 10)
| Necesidad | Alternativas | Elegida |
|---|---|---|
| Gestión | Trello · Jira · GitHub Projects | Trello (requisito del curso, lista de cotejo S10) |
| BD | PostgreSQL/Supabase · MySQL · MongoDB | Supabase (Auth + SQL + RLS) |
| Observabilidad | Prometheus · InfluxDB · Zabbix | Prometheus |
| Gateway | Spring Cloud Gateway · Go stdlib · Nginx | Spring (vigente); Go por consumo (D-06) |

## 3. Herramientas por PMV
| Herramienta | PMV1 | PMV2 | PMV3 |
|---|---|---|---|
| Simulator, Prometheus, Monitoring | ✓ | ✓ | ✓ |
| Gateway (Java; Go opcional) | ✓ | ✓ | ✓ |
| Supabase Auth/SQL | ✓ | ✓ | ✓ |
| Data Processing, Prediction (scikit-learn/XGBoost) | — | ✓ | ✓ |
| Pruebas de contrato con PostgreSQL/PostgREST | — | ✓ | ✓ |
| Prueba de carga (k6 o JMeter) y análisis estático (SonarCloud) | — | — | propuesto |

## 4. Resultados medidos con las herramientas (no estimados)
- Pipeline ML: RF con MAE 3,22 frente a persistencia 4,61 (−30 %), a 15 min, en validación.
- Gateway Go frente a Java: imagen 16,2 MB frente a 520 MB; RAM ~10 frente a ~290 MiB; arranque 0,5 frente a
  6–8 s; p50 del proxy 3,5 frente a 26 ms (`docs/evidencias/gateway-go-difftest-20261106.txt`).
- Smoke del stack: 14/14.

## 5. Decisiones de sustitución
| Hallazgo | Decisión |
|---|---|
| Recomendaciones como microservicio aparte | Integradas en Prediction (CHG-01) |
| Kubernetes en el plan | Sustituido por Docker Compose; K8s opcional en el PMV3 |
| MLflow sin ejecución | Manifiesto con SHA del dataset y de la configuración; MLflow opcional |
| Gateway Java pesado | Go validado como alternativa |
