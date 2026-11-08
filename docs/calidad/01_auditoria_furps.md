# 01_Auditoria_FURPS.md — Auditoría Integral de Calidad de Software (Modelo FURPS+)

**Proyecto:** Green AI (Optimización Energética y Capacidad en Data Centers con Machine Learning)  
**Institución:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol del Evaluador:** Auditor Senior de Calidad de Software  
**Fecha de Evaluación:** 2026-11-07  
**Rama Base de Trabajo:** `test` (commit sincronizado en monorepo, desarrollo activo)  
**Metodología y Marcos:** Modelo FURPS+ (Hewlett-Packard / Rational Software Corp.) y Directrices de Evaluación de Calidad UC (Guías Semana 12 y 13)

---

## 1. Resumen Ejecutivo

### 1.1. Propósito y Alcance de la Auditoría
El presente informe documenta la auditoría formal de calidad de software sobre el monorepo `green-ai`, aplicando el modelo **FURPS+** (Funcionalidad, Usabilidad, Confiabilidad, Rendimiento, Soporte y Restricciones de Diseño, Implementación, Interfaz, Despliegue y Licencias). La evaluación abarca el código fuente, la arquitectura hexagonal, contratos de API (OpenAPI), persistencia de datos (Supabase/PostgreSQL y perfil SQLite de desarrollo), infraestructura de observabilidad (Prometheus y reglas de alerta), microservicios de backend (Java Spring Boot, Python FastAPI, Go), frontend web estático, suites de pruebas automatizadas y documentación de despliegue.

El principio de evaluación es la **honestidad experimental** y la **evidencia verificable**: ninguna afirmación sobre funcionalidades, métricas o rendimientos se asume sin respaldo en el código, pruebas ejecutadas o mediciones documentadas (`AGENTS.md`, `docs/HANDOFF.md:L70-L75`).

### 1.2. Contexto Técnico del Monorepo
El sistema está compuesto por los siguientes subsistemas desacoplados dentro de `software/`:
1. **Simulator** (Python 3.12, `uv`): Generación sintética determinista de telemetría de 50 servidores en tiempo real (`/metrics`) y modo offline (`software/simulator/README.md`).
2. **Monitoring Service** (Java 21, Spring Boot 4.1.1): Consulta PromQL acotada hacia Prometheus, catálogo de métricas y fixtures deterministas (`software/monitoring/README.md`).
3. **Data Processing Service** (Python 3.14, FastAPI): Ingesta paginada de históricos con cursor, alineación temporal sin imputación y adaptador dual SQLite/Supabase (`software/data-processing/README.md`).
4. **Prediction Service** (Python 3.11/FastAPI): Inferencia de demanda futura de CPU a 15 minutos mediante Random Forest, recomendaciones con restricciones operacionales y cálculo trapezoidal de energía (`software/prediction/README.md`).
5. **API Gateway** (Java Spring Cloud Gateway WebFlux predeterminado; prototipo Go estándar alternativo): Control de acceso perimetral, verificación de JWT Supabase, RBAC, limitación de tasa y CORS (`software/gateway/README.md`, `software/gateway-go/README.md`).
6. **Frontend** (HTML5, Vanilla JS modular, CSS personalizado): Interfaz de observatorio con 5 pestañas, mapa de calor de Racks, red de flujos, ayuda contextual y manejo de errores humanos (`software/frontend/README.md`).
7. **Infraestructura & Observabilidad**: Orquestación local en `docker-compose.yml`, Prometheus v3.13.3, reglas de alerta validadas con `promtool` y verificación de humo end-to-end (`software/infraestructura/docker-compose.yml`).

### 1.3. Cuadro Resumen de Calificación FURPS+ (Alineado con Matriz)

| Categoría FURPS+ | Ponderación | Puntaje Obtenido (0–100) | Nivel de Calidad Inicial | Estado Técnico Cualitativo |
|---|:---:|:---:|:---:|---|
| **F — Funcionalidad (Functionality)** | 25 % | **78 / 100** | Aceptable | Cobertura amplia de PMV1 y PMV2. Brechas: aprobación humana no persistida (HU-07), energía modelada no medida (HU-09), MLflow sin UI en nube (HU-05), reportes sin PDF (HU-13) y riesgo RLS histórico (HU-15). |
| **U — Usabilidad (Usability)** | 15 % | **80 / 100** | Aceptable | Consola en 5 pestañas, modo claro/oscuro, Racks con mapa de calor y ayuda contextual. Brechas: falta guía rápida de usuario (M-U07), auditoría WCAG formal y flujos de energía en > 3 pasos. |
| **R — Confiabilidad (Reliability)** | 20 % | **93 / 100** | Bueno | 415+ pruebas automatizadas, smoke 14/14, RFC 7807 problem+json y timeouts defensivos. Brecha: persistencia Supabase remota requiere verificar RLS y control de carga. |
| **P — Rendimiento (Performance)** | 15 % | **87 / 100** | Bueno | Latencias locales < 30 ms (Go p50 = 3.5 ms), imagen Prediction adelgazada (510 MB, RAM 122 MiB). Brecha: arranque en frío en Render Free Tier (~60 s) incumple umbral de 7 s. |
| **S — Soporte / Mantenibilidad (Supportability)** | 15 % | **90 / 100** | Bueno | Monorepo limpio, CI en GitHub Actions y OpenAPI versionado. Brecha: acoplamiento de adaptadores en `software/simulator/.../application/runner.py:L5-L10`. |
| **+ — Restricciones Adicionales (PLUS)** | 10 % | **93 / 100** | Bueno | Arquitectura desacoplada, despliegue a costo cero documentado, licenciamiento Open Source y Ley N° 29733. Brecha: limitaciones físicas del hosting gratuito (750 h/mes, 512 MB). |
| **TOTAL PONDERADO** | **100 %** | **85.00 / 100** | **Satisfactorio** | **El sistema cumple las condiciones funcionales para revisión de calidad, sujeto a ejecución del plan de mejora.** |

---

## 2. Evaluación Detallada por Factores FURPS+

### 2.1. Funcionalidad (Functionality - F) — Puntaje: 78 / 100

#### 2.1.1. Análisis de Cobertura de Procesos de Negocio e Historias de Usuario
- **HU-01: Visualización de métricas de telemetría en tiempo real (PMV1).**  
  *Cumple.* El Simulator expone métricas sintéticas deterministas de 50 servidores cada 5 s (`software/simulator/README.md:L48-L66`). Prometheus realiza el raspado con etiquetas `cluster`, `node` y `origin="simulated"`. Monitoring expone `/api/v1/metrics/catalog`, `/current` y `/history` validando sintaxis sin PromQL arbitrario (`software/monitoring/src/main/resources/application.yaml:L1-L15`). El Frontend renderiza gráficos temporales y estadísticas agregadas (`software/frontend/dashboard.html:L63-L94`).
- **HU-02: Consulta de históricos de telemetría (PMV1).**  
  *Cumple.* Data Processing implementa el endpoint `GET /api/v1/historical-logs` con soporte de cursor keyset `(timestamp, log_id)` y ventana máxima de 31 días (`software/data-processing/infrastructure/adapters/input/api/routes.py:L33-L45`). Cuenta con desacoplamiento mediante puerto `HistoricalLogsSource` y adaptadores duales verificados: `SqliteHistoricalLogsAdapter` para desarrollo offline y `SupabaseHistoricalLogsAdapter` para nube, compartiendo una batería de 114 pruebas de contrato (`docs/DECISIONES.md:L32-L50`).
- **HU-03: Predicción de demanda computacional (PMV2).**  
  *Cumple.* Prediction expone `POST /v1/predictions` y `POST /predict` (`software/prediction/src/service/app.py:L132-L144`). Recibe un dataset procesado de 2 horas (muestreado a 15 s) y devuelve la predicción de CPU a un horizonte de 15 minutos mediante un modelo Random Forest serializado en `models/selected/`. Devuelve metadatos explícitos con `origin="estimated"`.
- **HU-04: Comparación de alternativas de modelos y estrategias (PMV2/PMV3).**  
  *Cumple.* En entrenamiento, el pipeline compara 4 modelos (Persistencia, Media Móvil, Random Forest y XGBoost) a través de 3 horizontes (`software/prediction/README.md:L11-L15`). En tiempo de ejecución, el experimento comparativo entre heurística reactiva (baseline) y Green AI predictivo está documentado y visible en la UI (`docs/academico/10-plan-experimental.md:L22-L28`, `software/frontend/dashboard.html:L225-L250`).
- **HU-05: Registro de experimentos en MLflow (PMV2).**  
  *Parcial.* `run_pipeline.py` genera el experimento local en `software/prediction/mlruns/`, pero no hay interfaz de MLflow expuesta ni capturas de la UI registradas (`docs/HANDOFF.md:L88-L91`).
- **HU-06: Recomendaciones de optimización con restricciones de política (PMV2).**  
  *Cumple.* Prediction integra `POST /v1/recommendations` evaluando restricciones operacionales (CPU 30–80 %, memoria ≤ 85 %, latencia p95 ≤ 500 ms, tasa de error ≤ 1 %). Toda recomendación retorna `executionAllowed: false` garantizando supervisión humana (`software/prediction/src/service/recommendations.py:L15-L80`, `software/frontend/dashboard.html:L156-L186`).
- **HU-07: Aprobación humana de recomendaciones (PMV2).**  
  *No cumple.* No existe flujo de aprobar/rechazar ni persistencia de la decisión humana en base de datos; el sistema se limita a bloquear la auto-ejecución (`docs/academico/08-pruebas-resultados-discusion.md:L31`).
- **HU-09: Cálculo de energía y CO₂e (PMV2).**  
  *Parcial.* El cálculo de energía en kWh mediante regla trapezoidal asume potencia lineal simulada $P = P_{idle} + (P_{max} - P_{idle}) \times CPU$ (`software/frontend/energy.js:L10-L50`). No es potencia medida por sensores físicos. El cálculo de CO₂e queda «no evaluable» sin un factor manual.
- **HU-11: Dashboard integrado de observabilidad (PMV2).**  
  *Parcial.* Implementado con 5 pestañas y arnés local verificado, pero falta validación con sesión real de Supabase en el entorno desplegado en GitHub Pages (`/dev/`) (`docs/CONTINUAR-EN-NUEVO-CHAT.md:L21-L22`).
- **HU-12: Alertas de infraestructura (PMV2).**  
  *Cumple.* 4 reglas de alerta configuradas en `software/infraestructura/prometheus/alerts.yml`, validadas técnicamente con `promtool` (`docs/HANDOFF.md:L111`).
- **HU-13: Reportes históricos y exportación (PMV2/PMV3).**  
  *Parcial.* Data Processing implementa `GET /api/processing/v1/reports/historical-summary` devolviendo JSON agregado y descarga en formato CSV plano (`software/data-processing/infrastructure/adapters/input/api/routes.py:L8-L14`). La generación formal de reporte PDF sigue pendiente (`docs/HANDOFF.md:L113`).
- **HU-14: Control de acceso basado en roles RBAC (PMV2/PMV3).**  
  *Cumple.* Gateway valida claims en JWT de Supabase para roles `ADMIN`, `OPERATOR` y `VIEWER`. El rol `VIEWER` tiene acceso restringido de solo lectura sin permisos de inferencia (`software/gateway/src/main/resources/application.yaml:L70-L75`, `docs/HANDOFF.md:L113`).
- **HU-15: Registro e inicio de sesión seguro (PMV1).**  
  *Parcial.* Flujo PKCE configurado con Supabase Auth y trigger SQL de auto-asignación (`software/frontend/supabase-auth-setup.sql`), pero sin pruebas automatizadas con usuario real y persistiendo riesgo de RLS permisiva en el esquema histórico (`docs/HANDOFF.md:L150-L155`).

#### 2.1.2. Tabla de Hallazgos de Funcionalidad

| ID | Evidencia (Archivo y Línea) | Brecha Identificada | Nivel de Riesgo |
|:---:|---|---|:---:|
| **F-01** | `software/prediction/README.md:L18`, `software/frontend/dashboard.html:L260` | **Potencia y energía modeladas, no medidas físicamente:** El cálculo de kWh mediante regla trapezoidal asume potencia lineal simulada. No proviene de sensores PDU o IPMI físicos. | **Medio** (Declarado con honestidad experimental; no invalida la lógica algorítmica). |
| **F-02** | `docs/HANDOFF.md:L88-L91`, `software/prediction/README.md:L67-L69` | **Registro en MLflow sin interfaz gráfica desplegada:** Aunque `run_pipeline.py` genera el run en `mlruns/`, no se cuenta con captura de la UI ni servidor MLflow desplegado. | **Bajo** (Mitigado por el manifiesto versionado en `results/manifest.json`). |
| **F-03** | `docs/academico/08-pruebas-resultados-discusion.md:L31` | **Aprobación de recomendaciones sin persistencia (HU-07):** La recomendación bloquea la auto-ejecución (`executionAllowed=false`), pero no almacena la decisión de aceptación/rechazo en una tabla de auditoría. | **Medio** (Falta trazabilidad de decisiones humanas operativas). |
| **F-04** | `docs/HANDOFF.md:L113`, `software/data-processing/infrastructure/adapters/input/api/routes.py:L8-L14` | **Ausencia de exportación PDF en reportes (HU-13):** Solo se entregan resúmenes JSON y CSV plano; el PDF acordado no está implementado. | **Bajo** (CSV es utilizable para análisis, pero el entregable universitario requiere reporte formal). |
| **F-05** | `docs/HANDOFF.md:L150-L155` | **Falta de verificación de RLS y contraseñas en Supabase (HU-15):** Políticas `Permitir todo` y columna `password` sin verificar en la BD remota de Supabase. | **Alto** (Riesgo de seguridad para datos de usuario). |

---

### 2.2. Usabilidad (Usability - U) — Puntaje: 80 / 100

#### 2.2.1. Consistencia Visual, Navegación y Accesibilidad
- **Estructura y Navegación:** El frontend presenta una arquitectura limpia basada en 5 vistas/pestañas principales (`software/frontend/dashboard.html:L54-L60`):
  1. *Resumen:* Tarjetas KPI (media, nodo más/menos cargado, saturados >80 %) y gráfico temporal dinámico.
  2. *Detalle por servidor:* Tabla paginada (10 filas/pág.) con buscador por ID (ej. `HW045`), ordenación por columnas y estado de calidad (`software/frontend/dashboard.html:L97-L132`).
  3. *Predicción y recomendación:* Formulario guiado con valores por defecto y horizonte de 15 min.
  4. *Reportes y experimento:* Consulta histórica con descarga CSV y comparativa interactiva Baseline vs Green AI.
  5. *Energía y CO₂e:* 3 vías de evaluación (simulador, ejemplo determinista o subida de archivo JSON).
- **Vistas Especializadas Complementarias:**
  - `network.html`: Visualización matricial de Racks (5 racks con 10 servidores cada uno) con mapa de calor por colores semafóricos: verde (<40 %), ámbar (40–80 %) y rojo (>80 %) (`software/frontend/racks.js:L27-L48`).
  - `flows.html`: Representación ilustrativa de la topología de red y flujos de tráfico.
- **Modo Claro / Oscuro:** Implementado mediante variables CSS y conmutador accesible que persiste la preferencia en `localStorage('greenai-theme')` (`software/frontend/appearance.js`, `software/frontend/index.html:L12`).
- **Ayuda Contextual y Errores Amigables:**
  - El archivo `software/frontend/help-content.js:L1-L100` define ventanas modales emergentes («?») para cada métrica, explicando: *Qué es*, *Para qué sirve*, *Cómo se calcula*, *Qué ingresar* y *Límites experimentales*.
  - El componente `software/frontend/friendly-errors.js:L21-L64` intercepta respuestas técnicas (401, 403, 413, 422, 500, `INSUFFICIENT_DATA`, `INVALID_DATASET`) y las traduce a lenguaje humano natural, indicando la acción requerida (*"Tu sesión venció"*, *"El simulador necesita unos 20 minutos de historial"*, *"El archivo es demasiado grande (máx 1.5 MB)"*).
- **Flujos de Operación en Tres Pasos:** Las operaciones primarias (consultar métrica, cambiar tema, login) toman de 1 a 3 pasos. Sin embargo, la carga de telemetría de potencia con archivo propio y factor de emisión requiere 4 pasos (pestaña → examinar archivo → factor y fuente → calcular), y la predicción requiere seleccionar previamente nodo en otra pestaña.
- **Accesibilidad y Guía de Usuario:** Uso intensivo de etiquetas semánticas (`<main>`, `<nav>`, `<header>`, `<article>`), atributos ARIA (`role="tablist"`, `aria-selected`, `aria-live="polite"`, `aria-sort`) y etiquetas ocultas para lectores de pantalla (`<label class="sr-only">`). No existe una guía rápida de usuario documentada en `docs/` ni integrada en la interfaz.

#### 2.2.2. Tabla de Hallazgos de Usabilidad

| ID | Evidencia (Archivo y Línea) | Brecha Identificada | Nivel de Riesgo |
|:---:|---|---|:---:|
| **U-01** | `docs/` y `software/frontend/` | **Inexistencia de guía rápida de usuario:** No existe un manual breve o tutorial de primer uso para que el operador comprenda la consola sin asistencia técnica. | **Medio** (Afecta la adopción inicial del sistema). |
| **U-02** | `software/frontend/dashboard.html:L91` | **Gráfico en elemento `<canvas>` sin tabla directa alternativa en la misma pestaña:** El gráfico de Chart.js no incluye fallback en tabla accesible inmediatamente debajo (aunque los datos están tabulados en la pestaña contigua «Detalle por servidor»). | **Bajo** (Afecta parcialmente a lectores de pantalla que naveguen únicamente en la pestaña Resumen). |
| **U-03** | `software/frontend/styles.css` | **Ausencia de auditoría automatizada WCAG 2.1 AA:** Aunque el contraste de colores y la tipografía cumplen visualmente, no se ha corrido un escáner formal con herramientas como Lighthouse o `axe-core`. | **Bajo** (Oportunidad de validación formal en laboratorio de usabilidad). |
| **U-04** | `software/frontend/dashboard.html:L275-L289` | **Operaciones de energía superan los 3 pasos:** Subir archivo de potencia, asociar factor de emisión, registrar fuente y computar energía toma 4 acciones secuenciales. | **Bajo** (Fricción operativa menor en usuarios avanzados). |

---

### 2.3. Confiabilidad (Reliability - R) — Puntaje: 93 / 100

#### 2.3.1. Robustez, Manejo de Errores y Recuperación ante Fallos
- **Manejo Estandarizado de Errores (RFC 7807):**
  - **Data Processing:** Implementa `problem(status, code, detail)` generando respuestas estrictas `application/problem+json` e inyectando siempre la cabecera `X-Request-Id` (`software/data-processing/main.py:L24-L37`).
  - **Monitoring:** Captura excepciones del dominio (consultas inválidas, ausencia de fuente) y las traduce a `application/problem+json` (`software/monitoring/README.md:L72-L73`).
  - **Prediction:** Emplea jerarquía de excepciones tipadas (`MLError`, `DatasetError`, `ModelNotFoundError`) asignando códigos de estado HTTP 400, 422, 503 y 500 (`software/prediction/src/service/app.py:L62-L82`).
  - **Gateway (Java & Go):** Normaliza rechazos de seguridad (401 sin token, 403 rol insuficiente, 413 payload excesivo) en formato problem+json coherente (`software/gateway-go/README.md:L11`).
- **Control de Retorno Exitoso y No Exitoso desde la Base de Datos:**
  - Data Processing captura y mapea fallos de conexión, respuestas vacías o datos corruptos provenientes de PostgREST o SQLite a través de `ServiceError` (`InvalidQuery`, `UpstreamContractError`, `SourceNotConfigured`, `SourceTimeout`), garantizando que la API retorne códigos 422, 502, 503 o 504 sin exponer credenciales ni stack traces (`software/data-processing/main.py:L40-L57`, `software/data-processing/infrastructure/adapters/output/sqlite_historical_logs_adapter.py`).
- **Sondas de Salud (Health Checks):**
  - Prediction: Implementa `/health/live` y `/health/ready` con verificación de integridad del artefacto y hash SHA-256 (`software/prediction/src/service/app.py:L112-L130`). Integrado en Compose con `urllib.request` (`software/infraestructura/docker-compose.yml:L71-L76`).
  - Data Processing: Endpoint `/api/v1/health` que valida el estado del servicio (`software/data-processing/infrastructure/adapters/input/api/routes.py:L33-L35`).
  - Monitoring & Gateway: Probes de Spring Boot Actuator en `/actuator/health/liveness` y `/actuator/health/readiness` (`software/monitoring/src/main/resources/application.yaml:L17-L21`, `software/gateway/src/main/resources/application.yaml:L65-L68`).
  - Gateway Go: Binario con flag `-healthcheck` para contenedores distroless sin shell (`software/gateway-go/README.md:L12`).
- **Aislamiento y Timeouts en Cascada:**
  - Gateway a Monitoring: Timeout estricto de 6 s (`software/gateway/src/main/resources/application.yaml:L53`).
  - Gateway a Data Processing: Timeout de 15 s (superior al timeout interno de Data Processing de 10 s para evitar cancelaciones anticipadas) (`software/gateway/src/main/resources/application.yaml:L26`).
  - Gateway a Prediction: Timeout de 30 s para inferencia y recomendaciones (`software/gateway/src/main/resources/application.yaml:L38`).
  - Monitoring: Presupuesto contractual que limita consultas simultáneas a 16 hilos hacia Prometheus; saturación responde 503 `METRICS_SOURCE_UNAVAILABLE` sin colapsar el proceso Java (`software/monitoring/README.md:L60`).
- **Alertas de Infraestructura:** Configuración de alertas Prometheus en `software/infraestructura/prometheus/alerts.yml` (`SimulatorTelemetryDown`, `NodeCpuSaturationRisk`, `NodeMemoryPressure`, `PredictedCpuHigh`), validadas con `promtool` (`docs/HANDOFF.md:L111`).

#### 2.3.2. Tabla de Hallazgos de Confiabilidad

| ID | Evidencia (Archivo y Línea) | Brecha Identificada | Nivel de Riesgo |
|:---:|---|---|:---:|
| **R-01** | `docs/HANDOFF.md:L150-L155` | **Políticas RLS permisivas en snapshot histórico de Supabase:** En el esquema inicial (`esquema-verificado.json`, 2026-09-22) existían políticas «Permitir todo» y columna `password` en texto plano en `usuario`. | **Alto** (Pendiente de endurecimiento en el panel de Supabase por el dueño del proyecto). |
| **R-02** | `docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25` | **Fallo transitorio por suspensión de backend en Render:** El primer request tras inactividad puede provocar un 504 Gateway Timeout antes de que el microservicio complete su cold start. | **Medio** (Requiere precalentamiento antes de demostraciones). |
| **R-03** | `software/simulator/README.md:L86-L89`, `docs/HANDOFF.md:L41` | **Manejo de señales POSIX del Simulator en Windows nativo:** 1 prueba de 10 falla al correr localmente en PowerShell por manejo de `SIGTERM`; en Docker Linux corre 10/10 OK. | **Bajo** (Se mitiga ejecutando en contenedor Docker como está definido en Compose). |

---

### 2.4. Rendimiento (Performance - P) — Puntaje: 87 / 100

#### 2.4.1. Tiempo de Respuesta, Escalabilidad y Uso de Recursos
- **Latencia y Capacidad de Respuesta:**
  - El umbral de calidad docente exige que las transacciones y consultas respondan en promedio en **menos de 7 segundos**.
  - Evidencia empírica bajo carga (2 000 peticiones concurrentes con $c=16$, `docs/evidencias/gateway-go-difftest-20261106.txt:L46-L50`):
    - **Gateway Go:** Proxy hacia Monitoring con $p_{50} = 3.54\text{ ms}$, $p_{95} = 7.45\text{ ms}$, throughput de 4 139 rps. Rechazo 401 sin token con $p_{50} = 510\ \mu\text{s}$ (0.51 ms) y 16 648 rps.
    - **Gateway Java:** Proxy hacia Monitoring con $p_{50} = 26.24\text{ ms}$, $p_{95} = 57.29\text{ ms}$, throughput de 542 rps. Rechazo 401 con $p_{50} = 6.89\text{ ms}$ y 2 001 rps.
  - **Brecha identificada:** Estas mediciones fueron obtenidas en un host de desarrollo local. En Render (Free Tier), los contenedores se duermen tras 15 min; el arranque en frío (cold start) tarda entre 45 y 70 segundos (`docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25`), violando temporalmente el umbral de 7 s en la primera invocación.
- **Optimización de Memoria y Tamaño de Artefactos:**
  - **Prediction Ligera (2026-11-07):** Reestructuración multi-etapa del Dockerfile separando entrenamiento de inferencia (`requirements.serve.txt`), eliminando paquetes pesados (`jupyter`, `matplotlib`, `mlflow`, `seaborn`, `statsmodels`) e importando `xgboost` de forma diferida (`docs/evidencias/prediction-imagen-ligera-20261107.md:L1-L21`):
    - Tamaño de imagen: Reducido de **2.85 GB** a **510 MB** (reducción del 82 %).
    - Memoria RAM en reposo: Reducida de **174 MiB** a **133 MiB** aislado, y hasta **122 MiB** dentro del stack aplicando `PYTHONOPTIMIZE=2` y eliminando herramientas de instalación (`pip`, `wheel`, `setuptools`).
  - **Gateway Go vs Java:**
    - Tamaño de imagen: **16.2 MB** (Go distroless) frente a **520 MB** (Java Spring Boot JRE).
    - Memoria RAM en reposo: **2.3 MiB** (Go) frente a **224 MiB** (Java). Tras carga intensiva: **9.8 MiB** (Go) frente a **287 MiB** (Java).
    - Tiempo de arranque hasta `/actuator/health` 200: **0.45 s** (Go) frente a **6.49 s** (Java).
- **Eficiencia en el Almacenamiento y Consultas:**
  - Data Processing aplica paginación estricta basada en cursor keyset `(timestamp, log_id)` con límites configurables (máximo 500 filas por llamada) y proyección de 7 columnas indispensables (`log_id, hardware_id, timestamp, cpu_utilization_pct, ram_utilization_pct, temperatura_celsius, energia_watts`) (`software/data-processing/README.md:L33-L36`). Se previene el desbordamiento de memoria por consultas masivas de tablas enteras.
  - En el Frontend, la agregación estadística (media, máx, mín, percentil 95) se procesa en el navegador en un único recorrido por muestra ($O(N)$), evitando peticiones repetitivas al servidor (`software/frontend/aggregate.js:L11-L20`).

#### 2.4.2. Tabla de Hallazgos de Rendimiento

| ID | Evidencia (Archivo y Línea) | Brecha Identificada | Nivel de Riesgo |
|:---:|---|---|:---:|
| **P-01** | `docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25` | **Cold Start en Render Free Tier excede los 7 s:** La primera petición a un servicio dormido toma ~60 s en responder. | **Medio** (Requiere script de keep-alive previo a sustentación). |
| **P-02** | `docs/HANDOFF.md:L57-L61` | **Huella de memoria del Gateway Java:** 283 MiB de consumo en reposo excede el 55 % del límite del plan gratuito de Render (512 MB). | **Medio** (Mitigado por la alternativa de Gateway Go que consume ~10 MiB). |
| **P-03** | `docs/evidencias/prediction-imagen-ligera-20261107.md:L8-L12` | **Build time inicial de Prediction en la nube:** Construir el contenedor desde cero toma entre 8 y 10 minutos debido a la fase de preparación de datos y entrenamiento del modelo. | **Bajo** (Se realiza una sola vez por despliegue). |

---

### 2.5. Soporte y Mantenibilidad (Supportability - S) — Puntaje: 90 / 100

#### 2.5.1. Modularidad, Arquitectura Hexagonal y Trazabilidad de Pruebas
- **Arquitectura Hexagonal:**
  - **Monitoring:** Separación rigurosa de capas: `domain` (reglas de cálculo PromQL, entidades de series y calidad sin frameworks), `application` (puertos de entrada y salida `MetricsSource`), `adapter/in/web` (controladores MVC y traducción problem+json) y `adapter/out` (Prometheus HTTP y Fixture determinista) (`software/monitoring/README.md:L62-L73`).
  - **Data Processing:** Separación en `domain` (errores de negocio y contratos de monitoreo), `application/use_cases` e `infrastructure` (adaptadores SQLite, Supabase y FastAPI) (`software/data-processing/main.py`).
  - **Prediction:** Aislamiento del núcleo de inferencia ML (`src/inference/`, `src/models/`, `src/features/`) respecto al adaptador HTTP (`src/service/app.py`).
  - **Gateway Go:** Desacoplamiento en paquetes internos `internal/policy`, `internal/auth` e `internal/httpapi` (`software/gateway-go/README.md:L6-L14`).
  - **Brecha identificada:** En el Simulator, el archivo `software/simulator/src/green_ai_simulator/application/runner.py:L5-L10` importa adaptadores directamente (`parse_inventory_json`, `parse_scenario_json`, `RunLogger`), violando la inversión de dependencias pura de la arquitectura hexagonal.
- **Estructura Monorepo y Control de Versiones:**
  - Repositorio Git unificado en la raíz (`AGENTS.md`). Eliminación total de Git anidados, submódulos y gitlinks defectuosos (modo 160000). Ramas de trabajo estandarizadas: `main` (producción) y `test` (desarrollo/staging).
- **Especificaciones OpenAPI Formales y Versionadas:**
  - Gateway: `software/gateway/src/main/resources/static/openapi/gateway-v0.1.yaml`.
  - Monitoring: `software/monitoring/src/main/resources/static/openapi/monitoring-v0.1.json`.
  - Data Processing: `software/data-processing/contracts/data-processing-v1.openapi.json`.
  - Prediction: Esquemas OpenAPI autogenerados disponibles interactivamente en `/docs`.
- **Integración Continua (CI/CD):**
  - Flujo automatizado en `.github/workflows/ci.yml` que compila y ejecuta pruebas de todos los servicios ante eventos `push` y `pull_request` en `main` y `test`.
  - Despliegue continuo estático en `.github/workflows/pages.yml` sirviendo la raíz en producción y `/dev/` para desarrollo en GitHub Pages (`docs/GUIA-GITHUB-PAGES-Y-CI.md`).
- **Inventario Exhaustivo de Pruebas Automatizadas Verificadas:**
  Conforme a las cifras consolidadas en `docs/HANDOFF.md:L36-L49` y `docs/HANDOFF.md:L201-L208`:
  1. **Monitoring:** 112 pruebas unitarias y de integración (Maven / JUnit 5), 0 fallos.
  2. **Gateway:** 11/12 pruebas de contrato y seguridad en Java; 30 pruebas unitarias con `-race` en Go.
  3. **Data Processing:** 121 pruebas (pytest), incluyendo 114 pruebas de contrato sobre PostgreSQL y SQLite, y pruebas de reportes CSV.
  4. **Prediction:** 100 pruebas (pytest) tras optimización multi-etapa, validando prevención de fugas de datos (anti-leakage) y consistencia del modelo.
  5. **Frontend:** 48 pruebas de unidad e integración de UI ejecutadas mediante `node:test` (`frontend.test.cjs`, `racks.test.cjs`, `pmv2.test.cjs`, `energy.test.cjs`, `aggregate.test.cjs`).
  6. **Simulator:** 10 pruebas unitarias en Docker Linux (`unittest`), 0 fallos.
  7. **Smoke Test de Integración:** 14 pruebas de 14 exitosas sobre el stack HTTP en contenedores (`smoke.py`).
  *Total acumulado:* **415+ pruebas automatizadas**.

#### 2.5.2. Tabla de Hallazgos de Soporte y Mantenibilidad

| ID | Evidencia (Archivo y Línea) | Brecha Identificada | Nivel de Riesgo |
|:---:|---|---|:---:|
| **S-01** | `software/simulator/src/green_ai_simulator/application/runner.py:L5-L10` | **Acoplamiento de adaptadores en capa de aplicación:** El archivo `runner.py` importa adaptadores de parseo y logger, rompiendo la inversión de dependencias hexagonal. | **Bajo** (Deuda técnica interna del simulador; no afecta contratos externos). |
| **S-02** | `docs/HANDOFF.md:L62-L63` | **Reescritura de artefacto versionado por el pipeline de ML:** Al ejecutar `run_pipeline.py`, el script sobrescribe `software/prediction/results/manifest.json`, requiriendo descarte manual con Git para mantener el workspace limpio. | **Bajo** (Procedimiento de desarrollo; mitigado en CI al correr en contenedor efímero). |
| **S-03** | `software/data-processing/requirements.txt` | **Fijación de dependencias sin lock estricto en Data Processing:** A diferencia de Prediction (`requirements.lock.txt`) y Simulator (`uv.lock`), Data Processing usa un `requirements.txt` con rangos de versiones. | **Bajo** (Se recomienda congelar con `pip freeze` o migrar a `uv`). |

---

### 2.6. Factores «+» (Restricciones Adicionales) — Puntaje: 93 / 100

#### 2.6.1. Restricciones de Diseño, Implementación, Interfaces, Hosting y Licencias
1. **Restricciones de Diseño (Design Constraints):**
   - El sistema impone **punto de entrada único perimetral**: el Frontend tiene prohibido comunicarse directamente con los microservicios internos o con las tablas de base de datos; todo tráfico operacional fluye por el Gateway (`software/frontend/README.md:L24-L26`).
   - Cada microservicio encapsula estrictamente su persistencia: Monitoring no almacena estado relacional; Prediction no persiste en BD (maneja artefactos de archivo serializados); Data Processing es el único consumidor de históricos.
2. **Restricciones de Implementación (Implementation Constraints):**
   - Políticas corporativas de desarrollo monorepo: prohibidos repositorios Git anidados, credenciales quemadas en código fuente (solo `.env.example` vacíos o con valores sintéticos de prueba) y permisos globales `--dangerously-skip-permissions` (`AGENTS.md`).
   - Perfil de desarrollo SQLite implementado bajo el principio de no mentir sobre el origen de los datos: cada registro histórico declara explícitamente `source: "sqlite"` o `source: "supabase"` en su contrato JSON (`docs/DECISIONES.md:L42-L44`).
3. **Restricciones de Interfaces (Interface Constraints):**
   - Protocolo universal REST sobre HTTP/1.1 y HTTP/2 con codificación UTF-8.
   - Seguridad e Identidad: Validación de tokens JWT estándar generados por Supabase Auth, firmados mediante algoritmos asimétricos ES256 o RS256, verificados contra el endpoint público JWKS (`.well-known/jwks.json`) sin almacenamiento de claves privadas en el backend (`software/gateway/README.md:L58-L64`).
   - Métricas: Formato de exposición compatible con el estándar Prometheus OpenMetrics.
4. **Restricciones de Despliegue y Hosting a Costo Cero (Deployment Constraints):**
   - Infraestructura en la nube basada exclusivamente en capas gratuitas (Free Tier) sin costos de tarjeta (`docs/DECISIONES.md:L121-L140`, `docs/GUIA-DESPLIEGUE-RENDER.md`):
     - Frontend alojado en **GitHub Pages** (HTTPS automático, alta disponibilidad).
     - Backend alojado en **Render** mediante Blueprint declarativo `render.yaml:L1-L60`: 3 servicios web gratuitos (Gateway Go, Prediction y Data Processing).
     - Restricción de diseño: La cuota mensual de 750 horas en Render y el límite de 512 MB de RAM impiden desplegar Prometheus y Simulator de forma continua en la nube; se diseñó una arquitectura híbrida donde el simulador opera en local para la demo o se alimenta con datasets precargados.
5. **Licenciamiento y Cumplimiento Legal (Licensing & Governance):**
   - Proyecto desarrollado bajo marco académico de la Universidad Continental (Taller de Proyectos 1).
   - Uso exclusivo de bibliotecas con licencias Open Source compatibles (Apache 2.0, MIT, BSD).
   - Cumplimiento normativo con la legislación peruana sobre protección de datos personales (**Ley N° 29733**), explícitamente referenciada en la landing page (`software/frontend/index.html:L85`). No se persisten contraseñas en texto plano ni información sensible de operadores.

#### 2.6.2. Tabla de Hallazgos de Factores «+»

| ID | Evidencia (Archivo y Línea) | Brecha Identificada | Nivel de Riesgo |
|:---:|---|---|:---:|
| **PLUS-01** | `render.yaml:L37-L39`, `docs/GUIA-DESPLIEGUE-RENDER.md:L16-L18` | **Monitoring no desplegado en el Blueprint gratuito de Render:** En `render.yaml`, Data Processing apunta a `MONITORING_BASE_URL: https://example.invalid` para evitar exceder las cuotas de RAM y CPU de Render Free Tier. | **Medio** (Limita la visualización de métricas en vivo en la nube a datos precargados o enlaces locales). |
| **PLUS-02** | `docs/CONTINUAR-EN-NUEVO-CHAT.md:L25` | **Consumo de cuota compartida en Render:** Las 750 horas mensuales del plan gratuito se comparten con otros proyectos de la cuenta del usuario (ej. `SoftwareAnemia`), con riesgo de agotamiento si no se apagan los servicios tras pruebas. | **Medio** (Se recomienda suspender servicios manualmente tras las sesiones de prueba). |
| **PLUS-03** | `software/infraestructura/docker-compose.yml` | **Inexistencia de un instalador ejecutable «en un clic» para Windows nativo sin Docker:** La instalación local requiere Docker Desktop instalado y configurado previamente. | **Bajo** (Práctica estándar en microservicios contenerizados para centros de datos). |

---

## 3. Recomendaciones de Alto Nivel

1. **Funcionalidad (F):**
   - Implementar la persistencia de aprobaciones de recomendaciones (HU-07) mediante una tabla `recommendation_approvals` en Supabase o perfil local.
   - Completar el script de reporte para exportar PDF formal con encabezados académicos y gráficos incrustados (HU-13).
   - Asegurar las políticas RLS en Supabase eliminando `Permitir todo` y verificando la columna `password` (HU-15).
2. **Usabilidad (U):**
   - Redactar una guía rápida de usuario (1 página) en `docs/manuales/guia_rapida_usuario.md` y enlazarla desde la barra superior del frontend.
   - Optimizar el flujo de energía para admitir cálculo en 3 pasos con valores por defecto contextuales.
   - Proveer una tabla HTML oculta accesible conectada a `history-chart` para lectores de pantalla.
3. **Confiabilidad (R):**
   - Implementar un cronjob o endpoint de keep-alive para precalentar los contenedores en Render 25 minutos antes de la sustentación o grabación de video.
   - Correr pruebas de contrato de Data Processing contra un proyecto Supabase de staging con credenciales seguras.
4. **Rendimiento (P):**
   - Adoptar oficialmente el Gateway en Go como predeterminado en Render, liberando 270 MiB de RAM por instancia frente a Java.
5. **Soporte y Restricciones (S / +):**
   - Refactorizar `software/simulator/src/green_ai_simulator/application/runner.py:L5-L10` abstrayendo los parsers y logger detrás de interfaces/puertos en `domain/` o `application/ports/`.
   - Fijar dependencias con hashes en `software/data-processing/requirements.lock.txt`.

---

## 4. Matriz FURPS+ del Docente (Evaluación Estricta)

*Escala de Calificación:*
- **Cumple (5 puntos):** Requisito totalmente implementado, documentado y probado con evidencia en el repositorio.
- **Parcial (3 puntos):** Requisito implementado de forma parcial, con limitaciones operacionales, datos modelados o pendiente de verificación en la nube.
- **No cumple (1 punto):** Requisito ausente o sin evidencia en el código.
- **PO:** Puntaje Obtenido.
- **PD:** Puntaje Deseado (5 puntos).

*Asignación de Responsabilidades para Brechas (Parcial / No cumple):*
- **Ricardo Porras Veli:** Backend y Seguridad
- **Leonid Huamán Collazos:** Infraestructura y Frontend
- **Gina Barrera Peña:** Datos y Machine Learning
- **Jhonny Quintana Carhuaricra:** Documentación y Pruebas
- *Fechas de compromiso establecidas entre el 09/11/2026 y el 28/11/2026.*

| Factor | ID | Pregunta de Auditoría de Calidad | Artefacto | Cumplimiento | Evidencia Técnica / Brecha Identificada | Responsable | Fecha Compromiso | PO | PD |
|:---:|:---:|---|:---:|:---:|---|:---:|:---:|:---:|:---:|
| **F** | M-F01 | ¿Se ha implementado el caso de uso de visualización de métricas en tiempo real (HU-01)? | SOFTWARE | **Cumple (5)** | Catálogo y telemetría de 50 servidores vía Prometheus y Monitoring. Evidencia: `software/monitoring/src/main/resources/application.yaml:L1-L15`, `software/frontend/dashboard.html:L37-L49`, smoke 14/14. | — | — | 5 | 5 |
| **F** | M-F02 | ¿Se ha implementado el caso de uso de consulta y paginación de históricos (HU-02)? | SOFTWARE | **Cumple (5)** | Endpoint `/api/v1/historical-logs` con paginación keyset y adaptador dual SQLite/Supabase. Evidencia: `software/data-processing/infrastructure/adapters/input/api/routes.py:L33-L45`, 114 tests de contrato. | — | — | 5 | 5 |
| **F** | M-F03 | ¿Se ha implementado el caso de uso de predicción de demanda de CPU a 15 min (HU-03)? | SOFTWARE | **Cumple (5)** | Inferencia con Random Forest vía `POST /v1/predictions` con metadatos y `origin=estimated`. Evidencia: `software/prediction/src/service/app.py:L132-L144`, 100 pruebas pytest. | — | — | 5 | 5 |
| **F** | M-F04 | ¿Se ha implementado la comparación de alternativas de modelos y estrategias (HU-04)? | SOFTWARE / HERRAMIENTA | **Cumple (5)** | Comparación de 4 modelos en pipeline y experimento Baseline reactivo vs Green AI predictivo en UI. Evidencia: `docs/academico/10-plan-experimental.md:L22-L28`, `software/frontend/dashboard.html:L225-L250`. | — | — | 5 | 5 |
| **F** | M-F05 | ¿Se ha implementado el registro y visualización de experimentos en MLflow (HU-05)? | SOFTWARE / HERRAMIENTA | **Parcial (3)** | Run registrado localmente en `software/prediction/mlruns` (ignorado por Git); falta captura de UI de MLflow y servidor desplegado en la nube. | Gina Barrera Peña | 14/11/2026 | 3 | 5 |
| **F** | M-F06 | ¿Se ha implementado el caso de uso de recomendación con restricciones de política (HU-06)? | SOFTWARE | **Cumple (5)** | Evaluación de CPU, memoria, latencia y errores con `executionAllowed=false` para control humano. Evidencia: `software/prediction/src/service/recommendations.py:L15-L80`, `software/frontend/dashboard.html:L156-L186`. | — | — | 5 | 5 |
| **F** | M-F07 | ¿Se ha implementado la aprobación humana persistida de recomendaciones (HU-07)? | SOFTWARE | **No cumple (1)** | No existe flujo interactivo de aprobar/rechazar ni persistencia de decisiones en base de datos; solo bandera defensiva `executionAllowed=false`. | Ricardo Porras Veli | 20/11/2026 | 1 | 5 |
| **F** | M-F08 | ¿Se ha implementado el cálculo de energía y CO₂e a partir de potencia (HU-09)? | SOFTWARE | **Parcial (3)** | Cálculo de kWh por regla del trapecio implementado; sin embargo, la potencia es aportada o modelada sintéticamente, no medida en hardware real. CO₂e requiere factor manual. Evidencia: `software/frontend/energy.js:L10-L50`. | Gina Barrera Peña | 21/11/2026 | 3 | 5 |
| **F** | M-F09 | ¿Se ha implementado el dashboard integrado de observabilidad (HU-11)? | SOFTWARE | **Parcial (3)** | Implementado en `software/frontend/dashboard.html:L31-L295` y probado en arnés local; pendiente verificación con sesión real de Supabase en `/dev/`. | Leonid Huamán Collazos | 12/11/2026 | 3 | 5 |
| **F** | M-F10 | ¿Se ha implementado el sistema de reglas de alerta de infraestructura (HU-12)? | SOFTWARE | **Cumple (5)** | 4 reglas configuradas en `software/infraestructura/prometheus/alerts.yml`, validadas con `promtool`. Evidencia: `docs/HANDOFF.md:L111`. | — | — | 5 | 5 |
| **F** | M-F11 | ¿Se ha implementado la generación y descarga de reportes históricos (HU-13)? | SOFTWARE | **Parcial (3)** | Endpoint `/api/processing/v1/reports/historical-summary` genera resumen JSON y exportación CSV plano; exportación en formato PDF sigue pendiente. Evidencia: `docs/HANDOFF.md:L113`. | Ricardo Porras Veli | 18/11/2026 | 3 | 5 |
| **F** | M-F12 | ¿Se ha implementado el control de acceso y autorización RBAC (HU-14)? | SOFTWARE | **Cumple (5)** | Gateway valida claims `user_role` para roles ADMIN, OPERATOR y VIEWER. Evidencia: `software/gateway/src/main/resources/application.yaml:L70-L75`, `software/gateway-go/internal/policy/`. | — | — | 5 | 5 |
| **F** | M-F13 | ¿Se ha implementado el registro e inicio de sesión seguro (HU-15)? | SOFTWARE / HOSTING | **Parcial (3)** | Flujo PKCE y trigger SQL en `software/frontend/supabase-auth-setup.sql`; sin pruebas automatizadas con usuario real y persistiendo riesgo de RLS permisiva en histórico (`docs/HANDOFF.md:L150-L155`). | Ricardo Porras Veli | 11/11/2026 | 3 | 5 |
| **U** | M-U01 | ¿La interfaz cuenta con navegación organizada en pestañas y consistencia visual? | SOFTWARE | **Cumple (5)** | Consola organizada en 5 pestañas temáticas, layout responsive y navegación común. Evidencia: `software/frontend/dashboard.html:L54-L60`, `software/frontend/styles.css`. | — | — | 5 | 5 |
| **U** | M-U02 | ¿El sistema dispone de soporte para temas visuales (modo oscuro y claro)? | SOFTWARE | **Cumple (5)** | Conmutador accesible con persistencia en localStorage y variables CSS. Evidencia: `software/frontend/appearance.js`, `software/frontend/dashboard.html:L26`. | — | — | 5 | 5 |
| **U** | M-U03 | ¿Se cuenta con visualizaciones avanzadas de infraestructura (Racks con mapa de calor)? | SOFTWARE | **Cumple (5)** | Matriz interactiva de 50 servidores en 5 racks con umbrales verde/ámbar/rojo. Evidencia: `software/frontend/network.html`, `software/frontend/racks.js:L27-L48`, 20 pruebas unitarias. | — | — | 5 | 5 |
| **U** | M-U04 | ¿El sistema provee ayuda contextual comprensible y textos explicativos (botones «?»)? | SOFTWARE | **Cumple (5)** | Módulo de ayuda contextual detallando qué es, uso, cálculo y límites experimentales. Evidencia: `software/frontend/help-content.js:L1-L100`. | — | — | 5 | 5 |
| **U** | M-U05 | ¿Se traducen los errores técnicos de la API a mensajes amigables para el usuario? | SOFTWARE | **Cumple (5)** | Clasificación de errores en lenguaje humano con botones de acción sin códigos crípticos. Evidencia: `software/frontend/friendly-errors.js:L21-L64`. | — | — | 5 | 5 |
| **U** | M-U06 | ¿La interfaz respeta estándares de accesibilidad (semántica HTML, ARIA y contraste)? | SOFTWARE | **Parcial (3)** | Código semántico y atributos ARIA completos; pendiente escaneo formal WCAG 2.1 AA con Lighthouse y tabla accesible para Chart.js. Evidencia: `software/frontend/dashboard.html:L54-L63`. | Leonid Huamán Collazos | 15/11/2026 | 3 | 5 |
| **U** | M-U07 | ¿Se cuenta con una guía rápida de usuario para la operación del sistema? | GUÍA INST. / DOC | **No cumple (1)** | No existe manual breve de usuario ni guía de primer uso en `docs/` ni integrada en el frontend (verificado). | Jhonny Quintana Carhuaricra | 16/11/2026 | 1 | 5 |
| **U** | M-U08 | ¿Se completa cualquier operación principal en tres pasos o menos? | SOFTWARE | **Parcial (3)** | Consultas básicas y cambios de tema toman ≤ 3 pasos; sin embargo, calcular energía con archivo y factor toma 4 pasos, e inferir CPU requiere pasos en pestañas separadas. | Leonid Huamán Collazos | 17/11/2026 | 3 | 5 |
| **R** | M-R01 | ¿Se manejan los errores de las APIs mediante el estándar RFC 7807 (problem+json)? | SOFTWARE | **Cumple (5)** | Respuestas `application/problem+json` uniformes con requestId en todos los microservicios. Evidencia: `software/data-processing/main.py:L24-L28`, `software/prediction/src/service/app.py:L58-L82`. | — | — | 5 | 5 |
| **R** | M-R02 | ¿Todos los microservicios exponen sondas de salud (health checks / liveness / readiness)? | SOFTWARE | **Cumple (5)** | Probes `/health/ready`, `/api/v1/health`, Actuator y binario `-healthcheck` en Go. Evidencia: `software/prediction/src/service/app.py:L112-L130`, `software/gateway/src/main/resources/application.yaml:L65-L68`. | — | — | 5 | 5 |
| **R** | M-R03 | ¿El sistema implementa timeouts defensivos para mitigar caídas de servicios upstream? | SOFTWARE | **Cumple (5)** | Timeouts escalonados en Gateway (6 s, 15 s, 30 s) y Data Processing (10 s) para evitar bloqueos. Evidencia: `software/gateway/src/main/resources/application.yaml:L26-L53`, `software/data-processing/main.py:L79`. | — | — | 5 | 5 |
| **R** | M-R04 | ¿Se cuenta con una batería de pruebas automatizadas y smoke test end-to-end? | SOFTWARE / HERRAMIENTA | **Cumple (5)** | 415+ pruebas automatizadas en 6 suites y smoke test de 14/14 pasos pasando satisfactoriamente. Evidencia: `docs/HANDOFF.md:L36-L49`, `docs/evidencias/smoke-20261106.json`. | — | — | 5 | 5 |
| **R** | M-R05 | ¿La plataforma resiste caídas y saturación sin comprometer la base de datos de producción? | SOFTWARE / HOSTING | **Parcial (3)** | SQLite aísla desarrollo local; falta verificar resistencia ante carga masiva en PostgREST remoto y corregir RLS permisiva en Supabase (`docs/HANDOFF.md:L150-L155`). | Ricardo Porras Veli | 13/11/2026 | 3 | 5 |
| **R** | M-R06 | ¿Se controla el retorno exitoso y no exitoso desde la base de datos? | SOFTWARE | **Cumple (5)** | Data Processing intercepta respuestas/errores de PostgREST y SQLite traduciéndolos a problem+json (422, 502, 503, 504) sin filtrar datos sensibles. Evidencia: `software/data-processing/main.py:L40-L57`. | — | — | 5 | 5 |
| **P** | M-P01 | ¿La operación y consulta responde en promedio en menos de 7 segundos? | SOFTWARE | **Parcial (3)** | En pruebas locales responde en < 30 ms (Java) y < 4 ms (Go) (`docs/evidencias/gateway-go-difftest-20261106.txt:L46-L50`), pero en Render Free Tier el cold start toma ~60 s tras 15 min de inactividad (`docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25`). | Leonid Huamán Collazos | 19/11/2026 | 3 | 5 |
| **P** | M-P02 | ¿El sistema hace un uso razonable de memoria RAM (< 512 MB por contenedor)? | SOFTWARE / SISTEMA OPERATIVO | **Cumple (5)** | Prediction optimizada consume 122–142 MiB (`docs/evidencias/prediction-imagen-ligera-20261107.md:L8-L12`); Gateway Go 2.3–9.8 MiB; Data Processing 76 MiB; Monitoring ~211 MiB. | — | — | 5 | 5 |
| **P** | M-P03 | ¿Se cuenta con imágenes de contenedor optimizadas y ligeras para inferencia? | SOFTWARE / HERRAMIENTA | **Cumple (5)** | Dockerfile multi-etapa en Prediction redujo imagen de 2.85 GB a 510 MB (`docs/evidencias/prediction-imagen-ligera-20261107.md:L7-L12`); Gateway Go distroless de 16.2 MB. | — | — | 5 | 5 |
| **S** | M-S01 | ¿El código fuente sigue los principios de arquitectura hexagonal (puertos y adaptadores)? | SOFTWARE | **Parcial (3)** | Hexagonal pura en Monitoring, Data Processing y Gateway Go; sin embargo, en Simulator `software/simulator/src/green_ai_simulator/application/runner.py:L5-L10` importa adaptadores directamente, rompiendo la inversión de dependencias. | Ricardo Porras Veli | 24/11/2026 | 3 | 5 |
| **S** | M-S02 | ¿Se cuenta con especificaciones de contratos de interfaz OpenAPI versionadas? | SOFTWARE / HERRAMIENTA | **Cumple (5)** | Archivos OpenAPI versionados en Gateway, Monitoring, Data Processing y Swagger en Prediction. Evidencia: `software/gateway/src/main/resources/static/openapi/gateway-v0.1.yaml`, `software/data-processing/contracts/data-processing-v1.openapi.json`. | — | — | 5 | 5 |
| **S** | M-S03 | ¿Se dispone de un flujo de integración continua (CI) que valide pruebas en cada cambio? | HERRAMIENTA | **Cumple (5)** | Workflow de GitHub Actions que ejecuta suites completas de pruebas en `main` y `test`. Evidencia: `.github/workflows/ci.yml`, `docs/GUIA-GITHUB-PAGES-Y-CI.md`. | — | — | 5 | 5 |
| **S** | M-S04 | ¿El monorepo cuenta con estructura limpia sin repositorios Git anidados ni gitlinks? | HERRAMIENTA | **Cumple (5)** | Repositorio unificado en la raíz; verificación `git ls-files -s` sin modo 160000; ramas `main` y `test`. Evidencia: `AGENTS.md`, `docs/DECISIONES.md:L5-L15`. | — | — | 5 | 5 |
| **PLUS** | M-PL01 | ¿Se cuenta con guía de instalación y despliegue paso a paso para la nube? | GUÍA INST. | **Cumple (5)** | Guía detallada paso a paso para desplegar en Render y GitHub Pages sin secretos versionados. Evidencia: `docs/GUIA-DESPLIEGUE-RENDER.md:L1-L111`. | — | — | 5 | 5 |
| **PLUS** | M-PL02 | ¿Existe un instalador o mecanismo automático de arranque local (docker-compose)? | HERRAMIENTA / SOFTWARE | **Cumple (5)** | Archivo Docker Compose multi-servicio que arranca el stack completo con un comando `docker compose up`. Evidencia: `software/infraestructura/docker-compose.yml:L1-L111`. | — | — | 5 | 5 |
| **PLUS** | M-PL03 | ¿Existe viabilidad y espacio para alojar el sistema en entorno de hosting a costo cero? | HOSTING | **Parcial (3)** | Frontend en Pages y backend en Render Free Tier con `render.yaml:L1-L60`; limitaciones de suspensión (15 min) y cuota de 750 h/mes compartida con otros proyectos. | Leonid Huamán Collazos | 22/11/2026 | 3 | 5 |
| **PLUS** | M-PL04 | ¿El sistema invoca servicios externos de manera segura desacoplada? | SOFTWARE / HOSTING | **Cumple (5)** | Conexión segura a Supabase Auth por JWKS público; sin llaves `service_role` en frontend ni backend. Evidencia: `software/gateway/src/main/resources/application.yaml:L70-L75`, `software/frontend/README.md:L10-L13`. | — | — | 5 | 5 |
| **PLUS** | M-PL05 | ¿El proyecto cumple con las restricciones de licencias de software y normativa legal? | SOFTWARE / GUÍA INST. | **Cumple (5)** | Dependencias Open Source compatibles (Apache 2.0/MIT); apego explícito a la Ley N° 29733 en el frontend. Evidencia: `software/frontend/index.html:L85`, `docs/academico/README.md`. | — | — | 5 | 5 |
| **PLUS** | M-PL06 | ¿Se cuenta con una guía de inicio/arranque del sistema? | GUÍA INST. / DOC | **Cumple (5)** | El archivo `README.md:L22-L38` provee la guía de arranque paso a paso para Docker Compose, configuración de puertos y pruebas, complementado por `docs/CONTINUAR-EN-NUEVO-CHAT.md:L30-L38`. | — | — | 5 | 5 |

---

## 5. Recálculo y Comparativa: Nivel de Calidad Inicial vs. Nivel de Calidad Esperado

### 5.1. Tabla de Nivel de Apego por Factor (Inicial y Esperado)

| Factor FURPS+ | Total Preguntas | Puntaje Deseado (PD) | Puntaje Obtenido Inicial (PO) | Nivel de Calidad Inicial (%) | Puntaje Obtenido Esperado (Meta) | Nivel de Calidad Esperado (%) | Filas que Pasan a Cumple en el Plan |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **F — Funcionalidad** | 13 | 65 | 51 | **78.46 %** | 63 | **96.92 %** | M-F05 (MLflow UI), M-F07 (Aprobación persistida), M-F09 (Dashboard en /dev/), M-F11 (Reporte PDF) y M-F13 (Seguridad Supabase/RLS). *M-F08 se mantiene en 3 por ser potencia modelada.* |
| **U — Usabilidad** | 8 | 40 | 32 | **80.00 %** | 40 | **100.00 %** | M-U06 (Accesibilidad Lighthouse + tabla Chart.js), M-U07 (Guía rápida de usuario en `docs/`) y M-U08 (Flujo de energía optimizado a ≤ 3 pasos). |
| **R — Confiabilidad** | 6 | 30 | 28 | **93.33 %** | 30 | **100.00 %** | M-R05 (Endurecimiento de RLS y prueba de carga en PostgREST). |
| **P — Rendimiento** | 3 | 15 | 13 | **86.67 %** | 15 | **100.00 %** | M-P01 (Precalentamiento automatizado / script keep-alive para mitigar cold start en Render). |
| **S — Soporte / Mantenibilidad** | 4 | 20 | 18 | **90.00 %** | 20 | **100.00 %** | M-S01 (Refactorización de `software/simulator/.../application/runner.py:L5-L10` para desacoplar adaptadores). |
| **+ — Restricciones Adicionales** | 6 | 30 | 28 | **93.33 %** | 28 | **93.33 %** | M-PL03 se mantiene en Parcial (3) debido a las restricciones intrínsecas del plan gratuito de Render (512 MB y 750 h/mes compartidas). |
| **TOTAL GLOBAL** | **40** | **200** | **170** | **85.00 %** | **196** | **98.00 %** | **11 de 13 brechas subsanadas en el plan de mejora.** |

### 5.2. Conclusiones del Diagnóstico
1. **Nivel de Calidad Inicial (85.00 %):** El proyecto cuenta con una base arquitectónica sólida y una batería de 415+ pruebas automatizadas verificadas. Sus principales debilidades radican en funcionalidades pendientes de soporte documental y operativo (HU-07 aprobación humana, HU-13 reporte PDF, M-U07 guía rápida de usuario), la naturaleza sintética de la potencia (HU-09) y el impacto del cold start en Render Free Tier (M-P01).
2. **Nivel de Calidad Esperado (98.00 %):** La ejecución del plan de trabajo asignado a los cuatro integrantes del equipo entre el 09/11/2026 y el 28/11/2026 permitirá alcanzar un apego del 98 %, manteniendo únicamente como restricciones aceptadas la naturaleza modelada de la potencia (hasta disponer de sensores físicos) y las limitaciones de cuota del hosting gratuito.
