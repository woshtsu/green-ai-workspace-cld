# Endpoints detectados e inventario funcional — Prompt 7: Descubrimiento Funcional

> **Fase 4** · Fuentes: código de rutas (`MetricsController.java`, `routes.py`, `app.py`, `recommendations.py`, `policy/routes.go`, `application.yaml`), OpenAPI servidos en vivo (`/openapi.json` de Prediction y Data Processing), contratos estáticos, HTML/JS del frontend y ejecución E2E.

## 1. Módulos funcionales

| Módulo | Servicio | Capacidad de negocio | Historias de usuario referenciadas en el repo |
|---|---|---|---|
| Telemetría sintética | Simulator | Generar CPU, memoria, red y disco deterministas para 50 servidores (escenarios low/normal/high) y exponerlos en formato Prometheus | — |
| Observación de métricas | Monitoring (+ Prometheus) | Catálogo de 5 métricas de nodo; consulta actual e histórica (≤ 24 h, paso 15–3600 s) con calidad por muestra (`valid`/`missing`/`non_finite`) y procedencia | HU-01 |
| Procesamiento y preparación de datos | Data Processing | Normalizar series de Monitoring; construir el dataset v1 de CPU (%) para Prediction; ETL de `BD_GreenAi.xlsx` | HU-02, HU-03 |
| Históricos y reportes | Data Processing | Lectura paginada de `logs` (Supabase o SQLite) y reporte resumen JSON/CSV (CPU/RAM media y p95, % de carga alta, energía trapezoidal) | HU-02, HU-13 |
| Predicción de demanda | Prediction | Estimar CPU a 15 min con Random Forest; pipeline de entrenamiento con baselines y XGBoost | HU-03, HU-04, HU-05 |
| Recomendación con restricciones | Prediction | Evaluar política de demostración y proponer `maintain` / `review_capacity_reduction` / `review_capacity_increase` **sin ejecutar** | HU-06, HU-07 |
| Energía y CO₂e | Prediction | Integrar potencia (W) en kWh y, si se aporta factor con fuente, CO₂e | HU-09 |
| Seguridad de acceso | Gateway (Java/Go) + Supabase | Autenticación JWT, RBAC (ADMIN/OPERATOR/VIEWER), CORS, correlación | HU-14 |
| Alertas | Prometheus | 6 reglas (Prediction caído, política bloqueada, simulador caído, CPU > 85 %, memoria > 90 %, CPU predicha > 85 %) | HU-12 |
| Experiencia de usuario | Frontend | Observatorio, racks, red de flujos, reportes, energía, ayuda contextual, modo claro/oscuro | — |

## 2. Menús

| Contexto | Opciones |
|---|---|
| Página pública (`index.html`) | Inicio · Dashboard · Login · Registro; botones «Iniciar sesión» y «Registrarse» |
| Barra de la aplicación (dashboard, network, flows) | **Resumen** (`dashboard.html`) · **Racks** (`network.html`) · **Red de flujos** (`flows.html`) · Modo oscuro/claro · Cerrar sesión |
| Pestañas del observatorio (`dashboard.html`) | **Resumen** · **Detalle por servidor** · **Predicción y recomendación** · **Reportes y experimento** · **Energía y CO₂e** |
| Ayuda contextual | Iconos «?» (`data-help`) con textos de `help-content.js` en cada sección |

## 3. Formularios

| Formulario | Página | Campos | Acción / API |
|---|---|---|---|
| Inicio de sesión (`#login-form`) | login | `email`, `password` | `supabase.auth.signInWithPassword` → redirige a `dashboard.html` |
| Registro (`#register-form`) | register | `nombre_completo`, `email`, `password`, `confirm_password` | `supabase.auth.signUp` (metadato `full_name`); el trigger crea perfil y rol OPERATOR |
| Filtro de métricas | dashboard | `metric`, `cluster`, `node`, `period` (15 min…); botón «Actualizar» | `GET /api/monitoring/v1/metrics/{catalog,current,history}` |
| Predicción | dashboard (pestaña Predicción) | Servidor seleccionado en el filtro; botón «Estimar CPU» (`#predict-button`) | `GET /api/processing/v1/prediction/dataset` → `POST /api/prediction/v1/predictions` |
| Recomendación (`#recommendation-form`) | dashboard | `policy-memory` (%), `policy-latency` (ms p95), `policy-errors` (%), `policy-time` (+ «ahora»), `policy-origin`; «Recomendar», «Ejemplo» | dataset → `POST /api/recommendations/v1/recommendations` |
| Reporte de históricos (`#historical-report-form`) | dashboard (Reportes) | `report-hardware-id` (HW045), `report-start`, `report-end` (fechas); «Ver resumen», «Descargar CSV» | `GET /api/processing/v1/reports/historical-summary?format=json\|csv` |
| Energía (`#energy-form`) | dashboard (Energía) | Archivo JSON de potencia (≤ 1,5 MB), `energy-factor` (kg CO₂e/kWh), `energy-factor-source`; botones «Calcular con el simulador», «Calcular con el ejemplo», «Descargar ejemplo» | `POST /api/recommendations/v1/energy` |
| Detalle de nodo | network | Clic en una celda de servidor; «Predecir 15 min» | `GET .../metrics/current`, dataset + predicción |

## 4. Procesos de negocio

1. **Alta de usuario y asignación de rol:** registro en Supabase → trigger `handle_new_auth_user` crea `user_profiles` y `user_roles` (OPERATOR por defecto) → el *hook* `custom_access_token_hook` añade `user_role` al JWT → un ADMIN promueve roles por SQL manual.
2. **Observación del parque:** Simulator genera ticks de 5 s → Prometheus *scrape* → Monitoring traduce la métrica de negocio a PromQL, valida identidad/grilla y marca calidad → panel (resumen, ranking, % > 80 %).
3. **Predicción de demanda:** el operador elige clúster y servidor → Data Processing pide a Monitoring la CPU (ratio) de las últimas 2 h, la convierte a %, excluye `missing`/`non_finite` sin imputar → Prediction remuestrea a 5 min, construye variables (calendario, lags 1–3, ventanas 3/6) y estima la CPU a +15 min (`origin=estimated`).
4. **Recomendación con revisión humana:** predicción + telemetría declarada por el operador → política (frescura ≤ 300 s, identidad, memoria ≤ 85 %, latencia p95 ≤ 500 ms, error ≤ 1 %) → `eligible_for_review` / `blocked` / `not_evaluable` → acción propuesta según CPU < 30 % o > 80 %; `executionAllowed` siempre `false`.
5. **Reporte de históricos:** rango ≤ 31 días por servidor → paginación interna (hasta 200 páginas × 500) → estadísticos, energía (Wh) por integración trapezoidal → JSON o CSV.
6. **Cálculo de energía y CO₂e:** muestras de potencia ordenadas (huecos ≤ 300 s) → kWh; CO₂e solo si el factor trae su fuente.
7. **Experimento baseline vs Green AI:** resultado precalculado (`experiment.json`, `docs/academico/10-plan-experimental.md`) mostrado con la advertencia «datos simulados · energía modelada».
8. **Entrenamiento y selección de modelo (offline):** dataset sintético (3 días, 5 min) → split temporal 70/15/15 → baselines (persistencia, media móvil), Random Forest y XGBoost → selección en validación por MAE, RMSE, sMAPE, MAE de alta demanda y latencia (si dos MAE difieren < 2 % gana el modelo más simple) → reentrenamiento en train+val → métricas en test → artefacto con SHA-256.

## 5. APIs consumidas

| Consumidor | API externa/interna | Operaciones |
|---|---|---|
| Frontend | Supabase Auth (supabase-js) | `signInWithPassword`, `signUp`, `getSession`, `refreshSession`, `signOut` (PKCE) |
| Frontend | Gateway Green AI | 9 rutas `/api/...` (§6.1) |
| Gateway | Supabase JWKS | `GET /auth/v1/.well-known/jwks.json` (con caché; observado: 1 descarga en toda la sesión E2E) |
| Gateway | Monitoring, Data Processing, Prediction | Proxy de las rutas publicadas |
| Data Processing | Monitoring | `GET /api/v1/metrics/history` |
| Data Processing | Supabase Data API (PostgREST) | `GET /rest/v1/logs?select=...&hardware_id=eq...&timestamp=gte/lte...&order=timestamp.asc,log_id.asc&limit=...` |
| Monitoring | Prometheus HTTP API | `GET /api/v1/query`, `GET /api/v1/query_range` |
| Prometheus | Simulator, Prediction | `GET /metrics` (*scrape*) |

## 6. APIs expuestas

### 6.1 Gateway (fachada pública)
| Método | Ruta | Roles | Destino |
|---|---|---|---|
| GET | `/api/monitoring/v1/metrics/catalog` | ADMIN, OPERATOR, VIEWER | Monitoring `/api/v1/metrics/catalog` |
| GET | `/api/monitoring/v1/metrics/current` | ADMIN, OPERATOR, VIEWER | Monitoring `/api/v1/metrics/current` |
| GET | `/api/monitoring/v1/metrics/history` | ADMIN, OPERATOR, VIEWER | Monitoring `/api/v1/metrics/history` |
| GET | `/api/processing/v1/metrics/history` | ADMIN, OPERATOR, VIEWER | Data Processing `/api/v1/metrics/history` |
| GET | `/api/processing/v1/historical-logs` | ADMIN, OPERATOR, VIEWER | Data Processing `/api/v1/historical-logs` |
| GET | `/api/processing/v1/prediction/dataset` | ADMIN, OPERATOR, VIEWER | Data Processing `/api/v1/prediction/dataset` |
| GET | `/api/processing/v1/reports/historical-summary` | ADMIN, OPERATOR, VIEWER | Data Processing `/api/v1/reports/historical-summary` |
| POST | `/api/prediction/v1/predictions` | ADMIN, OPERATOR | Prediction `/v1/predictions` |
| POST | `/api/recommendations/v1/recommendations` | ADMIN, OPERATOR | Prediction `/v1/recommendations` |
| POST | `/api/recommendations/v1/energy` | ADMIN, OPERATOR | Prediction `/v1/energy` |
| GET | `/actuator/health/liveness` (y `/actuator/health/**` en Java) | público | Gateway |
| GET | `/openapi/gateway-v0.1.yaml`, `/openapi/recommendations-v1.json` | público | Gateway |

### 6.2 Monitoring (interno, puerto 8080)
| Método | Ruta | Parámetros | Respuestas |
|---|---|---|---|
| GET | `/api/v1/metrics/catalog` | ninguno (rechaza parámetros extra) | 200 lista de 5 métricas |
| GET | `/api/v1/metrics/current` | `metric`*, `resourceType`=node, `cluster`, `resourceId` | 200 / 400 / 422 / 502 / 503 / 504 (problem+json) |
| GET | `/api/v1/metrics/history` | + `start`*, `end`*, `stepSeconds` (15–3600) | ídem |
| GET | `/actuator/health/{liveness,readiness}`, `/actuator/prometheus` | — | — |

Métricas del catálogo: `node.cpu.utilization` (ratio), `node.memory.used` (bytes), `node.network.receive` / `node.network.transmit` (bytes/s por interfaz), `node.filesystem.used` (bytes por FS).

### 6.3 Data Processing (interno, puerto 8000; FastAPI 1.1.0)
| Método | Ruta | Parámetros clave | Respuestas |
|---|---|---|---|
| GET | `/` | — | Metadatos del servicio |
| GET | `/api/v1/health` | — | `{"status":"healthy"}` |
| GET | `/api/v1/metrics/history` | `metric`, `start`, `end` (con zona), `resourceType`, `cluster`, `resourceId`, `stepSeconds` | 200 `ProcessedHistory` / 422 / 502 / 503 / 504 |
| GET | `/api/v1/historical-logs` | `hardwareId` (1–20), `start`, `end` (≤ 31 d), `limit` (1–500), `cursor` | 200 `HistoricalPage` con `nextCursor` |
| GET | `/api/v1/prediction/dataset` | `cluster`*, `resourceId`*, `start`, `end` (≤ 24 h), `stepSeconds` | 200 `PredictionDataset` (contrato provisional v1) |
| GET | `/api/v1/reports/historical-summary` | `hardwareId`, `start`, `end`, `format=json\|csv` | 200 JSON o `text/csv` |
| GET | `/docs`, `/openapi.json` | — | Swagger |

### 6.4 Prediction (interno, puerto 8000; FastAPI 1.0.0)
| Método | Ruta | Cuerpo / respuesta | Errores |
|---|---|---|---|
| GET | `/health` | `ok`/`degraded`, versión del modelo | — |
| GET | `/health/live` | `{"status":"live"}` | — |
| GET | `/health/ready` | Artefacto presente y SHA-256 válido (`precise: false`) | 503 `MODEL_UNAVAILABLE` |
| POST | `/v1/predictions` y alias `/predict` | Dataset v1 → `{predictionId, resource, target, unit:"%", value, origin:"estimated", predictedFor, generatedAt, modelVersion, ...}` | 400 `INVALID_INPUT`, 422 `INVALID_DATASET`, 503 |
| POST | `/v1/recommendations` | `{dataset, telemetry?}` → `Recommendation` (`status`, `action`, `checks`, `policy`, `executionAllowed:false`) | 422 / 502 / 503 |
| POST | `/v1/energy` | `{origin, samples[2..10000], emissionFactorKgPerKwh?, emissionFactorSource?}` → `{energyKwh, co2eKg, method:"trapezoidal_power_integration"}` | 422 |
| GET | `/metrics` (oculto en OpenAPI) | Contadores `green_ai_recommendations_total{status}` y *gauges* de última CPU/energía | — |
| GET | `/docs`, `/openapi.json` | Swagger | — |

### 6.5 Simulator
| Método | Ruta | Contenido |
|---|---|---|
| GET | `/metrics` | `node_cpu_seconds_total{cluster,node,origin,cpu,mode}`, `node_memory_MemTotal_bytes`, `node_memory_MemAvailable_bytes`, `node_network_{receive,transmit}_bytes_total{device}`, `node_filesystem_{size,free}_bytes`, `node_filesystem_device_error` (4 254 series para 50 nodos) |

## 7. Flujos principales (secuencia)

### 7.1 Inicio de sesión y llamada autenticada
```text
Usuario ─► login.html ─► Supabase Auth (PKCE) ─► JWT{user_role} en localStorage
Panel ─► authenticatedFetch(GW/api/...) [Bearer] ─► Gateway: JWKS → iss/aud/exp/nbf/sub/role/is_anonymous → RBAC por ruta
      ◄─ 401 → refreshSession() una vez → reintento GET ─► si persiste: signOut y login.html
```

### 7.2 Predicción en vivo
```text
Panel ─► GW GET /api/processing/v1/prediction/dataset?cluster&resourceId&start&end
   Gateway ─► Data Processing ─► Monitoring /api/v1/metrics/history (node.cpu.utilization, ratio)
      Monitoring ─► Prometheus query_range (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m])))
   Data Processing: ratio→%, excluye missing/non_finite, conserva origin ─► dataset v1
Panel ─► GW POST /api/prediction/v1/predictions (dataset) ─► Prediction: remuestreo 5 min → features → RF → +15 min
```

### 7.3 Recomendación
```text
Panel ─► dataset (7.2) + telemetría declarada ─► GW POST /api/recommendations/v1/recommendations
Prediction: predicción interna → valida identidad (resource, datasetId) → evaluate_policy() → Counter{status}
◄─ {status: eligible_for_review|blocked|not_evaluable, action, checks[], executionAllowed:false}
```

### 7.4 Reporte de históricos
```text
Panel ─► GW GET /api/processing/v1/reports/historical-summary?hardwareId&start&end&format
Data Processing ─► HistoricalLogsSource (Supabase PostgREST | SQLite ro) páginas de 500 por cursor keyset
◄─ JSON {cpu/ram mean·p95·max, highLoadPct, energyWh, recordCount, gaps} | CSV
```

## 8. Inventario funcional resumido

| Indicador | Valor |
|---|---|
| Páginas de UI | 6 |
| Pestañas del observatorio | 5 |
| Formularios | 8 |
| Endpoints de negocio expuestos por el Gateway | 10 (3 Monitoring, 4 Data Processing, 3 Prediction) |
| Endpoints internos totales | Monitoring 3 (+ actuator), Data Processing 6, Prediction 8, Simulator 1 |
| Roles | 3 (ADMIN, OPERATOR, VIEWER) + `PENDING` mostrado si falta el claim |
| Procesos de negocio | 8 |
| Reglas de alerta | 6 |
