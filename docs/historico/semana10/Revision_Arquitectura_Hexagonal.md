# Revisión Arquitectónica: Arquitectura Hexagonal (Puntos 1 y 2)

**Estado:** APROBADO CON OBSERVACIONES MENORES (Cumple el criterio de evaluación formativa S10)
**Fecha:** 29 de octubre de 2026
**Objetivo:** Documentar para Codex la verificación del punto "Arquitectura hexagonal — 1 y 2", el recorrido de capas y las dependencias de los servicios.

---

## 1. Mapeo de Capas y Recorrido por Capas (Layer Traversal)

### A. Servicio de Predicción y Recomendaciones Integrado (`green-ai-prediction`)
La política de recomendaciones fue integrada satisfactoriamente en `green-ai-prediction`, separando la política de evaluación del protocolo HTTP.

- **Driving Adapter (Entrada HTTP):** `src/service/recommendations.py` (APIRouter) y `src/service/app.py`.
- **Capa de Aplicación / Inferencia:** `src/inference/predict.py` (`predict_from_payload()`, `load_selected_model()`).
- **Capa de Dominio Puro:** `src/recommendations/policy.py` (`evaluate_policy()`), `src/exceptions.py`.
- **Adaptadores Secundarios / Transformación:** `src/adapters/input_adapter.py`, `src/adapters/output_adapter.py`.

#### Recorrido de `POST /v1/recommendations`:
1. `service/recommendations.py` recibe `RecommendationRequest` (valida esquema JSON y formato ISO con zona horaria).
2. Llama internamente a `predict_from_payload()` en memoria (sin llamadas HTTP adicionales a sí mismo).
3. `adapters/input_adapter.py` valida ventana temporal; ejecuta preprocesamiento y modelo baseline; `adapters/output_adapter.py` formatea la salida normalizada.
4. Se invoca `evaluate_policy()` en `src/recommendations/policy.py`. Evalúa frescura de telemetría, umbrales de CPU, memoria, latencia P95 y tasa de error. Devuelve `(status, action, checks)`.
5. Se actualizan métricas Prometheus (`decisions`, `green_ai_last_prediction_cpu_percent`) y se retorna el DTO `Recommendation`.

#### Recorrido de `POST /v1/energy`:
1. `service/recommendations.py` recibe `EnergyRequest` con muestras de potencia.
2. Aplica integración trapezoidal continua ∫ P(t) dt sobre las muestras temporales (<= 300 s).
3. Registra métricas y retorna `EnergyResult`.

---

### B. Servicio de Monitoreo (`green-ai-monitoring`)
Implementación canónica en Java/Spring Boot con aislamiento hexagonal estricto.

- **Driving Adapter (In Web):** `pe.edu.continental.greenai.monitoring.adapter.in.web.MetricsController`.
- **Input Port:** `pe.edu.continental.greenai.monitoring.application.port.in.QueryMetrics`.
- **Application Service:** `pe.edu.continental.greenai.monitoring.application.MonitoringService`.
- **Domain Layer:** `MetricCatalog`, `MetricQuery`, `MetricData`, `MetricDefinition`, `MonitoringFailure` (Java puro, 0 dependencias de Spring).
- **Output Port:** `pe.edu.continental.greenai.monitoring.application.port.out.MetricsSource`.
- **Driven Adapters (Out):** `PrometheusMetricsSource`, `FixtureMetricsSource`.

#### Recorrido de `GET /api/v1/metrics/history`:
`MetricsController` -> Puerto `QueryMetrics` -> `MonitoringService` -> Puerto `MetricsSource` -> `PrometheusMetricsSource` (consulta PromQL) -> Normalización en `MonitoringService` -> DTO `MetricData.Response`.

---

### C. Servicio de Procesamiento de Datos (`green-ai-data-processing`)
- **Driving Adapter:** `infrastructure/adapters/input/api/routes.py` (FastAPI).
- **Application (Casos de Uso):** `ProcessMetricsUseCase`, `PreparePredictionDatasetUseCase`, `ReadHistoricalLogsUseCase`.
- **Domain (Puertos y Contratos):** `domain/ports/metrics_source.py`, `domain/ports/historical_logs_source.py`, `domain/monitoring_contract.py`.
- **Driven Adapters:** `MonitoringHttpAdapter` (consume Monitoring), `SupabaseHistoricalLogsAdapter` (consume Supabase).

---

### D. Enrutamiento en Gateway (`green-ai-gateway`)
En `application.yaml`:
- La ruta `recommendations` apunta a `GATEWAY_PREDICTION_BASE_URL:http://prediction:8000`.
- Con `StripPrefix=2`, `/api/recommendations/v1/recommendations` se reenvía a `http://prediction:8000/v1/recommendations`.
- **No se requiere contenedor separado para recommendations.**

---

## 2. Matriz de Dependencias y Deuda Técnica

1. **green-ai-monitoring:** Conforme 100%. Inversión de dependencias perfecta. El dominio no tiene dependencias externas.
2. **green-ai-prediction:** Conforme. `src/recommendations/policy.py` es dominio puro (solo `datetime`, sin FastAPI ni HTTP).
3. **green-ai-data-processing:** Conforme con deuda en nomenclatura. `monitoring_http_adapter.py` y `supabase_historical_logs_adapter.py` son adaptadores guiados (Driven/Output) pero están ubicados en la carpeta `adapters/input/`.
4. **green-ai-simulator:** Acoplamiento directo. `runner.py` importa directamente de `adapters/*`; el directorio `application/ports/` está vacío.

---

## 3. Conclusión para la Entrega S10
El criterio **Arquitectura hexagonal — 1 y 2** está **CONFIRMADO Y COMPLETO**:
- La política de recomendaciones está desacoplada del protocolo HTTP.
- Está integrada en Prediction y probada en verde (13 tests aprobados).
- El recorrido entre capas y la dirección de dependencias están auditados y documentados.

---

## 5. Criterio 3: Integración REST — CONFIRMADO Y EVIDENCIADO
- **Estado:** 100% CUMPLIDO.
- **Evidencias en disco:**
  - `output/semana10/evidencias/Login_supabase.jpg`: Login real con correo `76659572@continental.edu.pe` (HTTP 200 de Supabase Auth token grant).
  - `output/semana10/evidencias/prediction_demanda.jpg`: Inferencia autenticada vía Gateway `POST :8081/api/prediction/v1/predictions` (HTTP 200 OK, CPU 54.23%, recurso HW001).
  - `output/semana10/evidencias/prediction_recomendacion.jpg`: Orquestación completa vía Gateway a Data Processing (`dataset`) y Prediction (`recommendations`), evaluando políticas y checks de SLA (HTTP 200 OK).
- **Conclusión:** Se comprobó el recorrido integral extremo a extremo con usuario real de Supabase, Gateway con JWT y renderizado en UI.

---

## 6. Criterio 4: Predicción, Precisión y Resultados — CORREGIDO Y SUSTENTADO
- **Estado:** CORREGIDO con datos reales del manifiesto.
- **Acciones aplicadas:**
  1. Se eliminaron del informe las referencias a XGBoost (MAE 5.4) y el ahorro energético del 18.4% por carecer de respaldo experimental.
  2. Se adoptaron las métricas oficiales de `results/manifest.json`:
     - Modelo: **Random Forest** (horizonte 15 min).
     - Test ($n=129$): **MAE = 3.85 pp**, **RMSE = 5.45 pp**, **sMAPE = 7.67 %**.
     - Picos ($n=13$): **RMSE = 10.87 pp**, **MAE = 8.45 pp**.
     - Latencia interna: media **5.78 ms**, P95 **7.03 ms**.
     - Procedencia: **simulated** (`dataset-sim-001`, semilla 42).
  3. El cálculo energético se delimitó formalmente como integración trapezoidal teórica de muestras de potencia sin afirmación de ahorro físico en producción.

---

## 7. Criterio 6: Pruebas por HU y Discusión Académica — COMPLETADO
- **Estado:** Fichas de prueba formuladas y discusión comparativa desarrollada.
- **Fichas documentadas:**
  - `HU-01`: Observabilidad actual en tiempo real (Aprobada, HTTP 200).
  - `HU-02`: Consulta histórica estructurada sin imputaciones artificiales (Aprobada, HTTP 200).
  - `HU-03`: Demanda futura de CPU en 15m con Random Forest (Aprobada, HTTP 200, 54.23% estimado).
  - `HU-06/07/08`: Recomendación con restricciones de SLA y Recommendation-Only (Aprobada, HTTP 200, checks validados, executionAllowed=false).
  - `HU-Seguridad`: Autenticación perimetral JWT en Gateway (Aprobada, rechazo anónimo 401, sesión válida 200).
- **Discusión Académica:** Comparación metodológica estructurada frente a Khan et al. (2022), Ullah et al. (2023) y Rao & Li (2025), sustentando el uso de Random Forest liviano frente a redes recurrentes pesadas y la arquitectura defensiva Recommendation-Only.

---

## 8. Criterio 7: Enlaces y Publicación — CONFIRMADO
- **Estado:** Commits publicados en los repositorios de origen de cada microservicio.
- **Ramas actualizadas:**
  - `Data Processing`: `main` actualizado en GitHub.
  - `Frontend`: `main` actualizado en GitHub.
  - `Prediction`: rama `Criss` actualizada en GitHub (incluye endpoints y OpenAPI de recomendaciones).
  - `Gateway`: `main` actualizado en GitHub.
  - `Monitoring`: `main` actualizado en GitHub.
  - `Workspace Raíz`: `main` sincronizado.
- **Acceso:** Enlaces de GitHub y Google Drive verificados para acceso sin credenciales.
