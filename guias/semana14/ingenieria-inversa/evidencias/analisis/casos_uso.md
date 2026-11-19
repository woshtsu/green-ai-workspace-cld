# Casos de uso reconstruidos

> **Fase 5** · Reconstruidos desde el código (rutas, casos de uso de aplicación, formularios del frontend) y validados con la ejecución E2E cuando fue posible. Estado: **Verificado** (ejecutado en la auditoría), **Implementado** (código presente, no ejecutable aquí), **Parcial** o **No implementado**.

## 1. Actores

| Actor | Descripción | Rol técnico |
|---|---|---|
| Operador | Opera el observatorio, predice y solicita recomendaciones | `OPERATOR` |
| Observador | Consulta métricas, históricos y reportes sin modificar nada | `VIEWER` |
| Administrador | Igual que Operador; gestiona roles (por SQL) | `ADMIN` |
| Científico de datos / Desarrollador | Entrena y selecciona modelos, ejecuta ETL y simulaciones | CLI |
| Sistema de monitoreo | Prometheus: recolecta métricas y evalúa alertas | — |
| Supabase | Proveedor de identidad y base de históricos | — |

## 2. Diagrama de casos de uso (texto)

```text
                         ┌──────────────────────────── Green AI ─────────────────────────────┐
  Observador ───────────►│ CU-03 Consultar catálogo · CU-04 Métrica actual · CU-05 Histórico  │
   (VIEWER)  ───────────►│ CU-06 Históricos paginados · CU-07 Reporte JSON/CSV                │
             ───────────►│ CU-12 Racks · CU-13 Red de flujos · CU-14 Experimento               │
                         │                                                                     │
  Operador ──(hereda)───►│ CU-08 Preparar dataset ─«include»─► CU-09 Predecir CPU 15 min       │
  (OPERATOR) ───────────►│ CU-10 Recomendar ajuste ─«include»─► CU-09                          │
             ───────────►│ CU-11 Calcular energía y CO₂e                                       │
  Administrador ────────►│ CU-19 Asignar rol (SQL manual)                                      │
  Cualquiera ───────────►│ CU-01 Registrarse · CU-02 Iniciar sesión                            │
  Científico de datos ──►│ CU-15 Entrenar y seleccionar modelo · CU-16 ETL · CU-17 Simular     │
  Prometheus ───────────►│ CU-18 Evaluar alertas                                               │
                         └─────────────────────────────────────────────────────────────────────┘
```

## 3. Catálogo

| ID | Caso de uso | Actor | Disparador | Endpoint / componente | Estado |
|---|---|---|---|---|---|
| CU-01 | Registrarse | Visitante | `register.html` | Supabase `signUp` + trigger | Implementado |
| CU-02 | Iniciar sesión | Usuario | `login.html` | Supabase `signInWithPassword` (PKCE) | Implementado (verificado el ciclo de sesión con emisor local) |
| CU-03 | Consultar catálogo de métricas | Observador+ | Abrir panel | `GET /api/monitoring/v1/metrics/catalog` | Implementado (503 en la auditoría: Monitoring no construible) |
| CU-04 | Consultar métrica actual | Observador+ | Panel / Racks | `GET .../metrics/current` | Implementado |
| CU-05 | Consultar histórico de métricas | Observador+ | Filtro «Histórico» | `GET .../metrics/history`, `GET /api/processing/v1/metrics/history` | Implementado |
| CU-06 | Leer históricos paginados | Observador+ | API | `GET /api/processing/v1/historical-logs` | **Verificado** (E10–E14) |
| CU-07 | Generar reporte de históricos | Observador+ | Pestaña Reportes | `GET .../reports/historical-summary?format=json\|csv` | **Verificado** (E15–E16 y UI) |
| CU-08 | Preparar dataset de predicción | Operador | Elegir servidor | `GET .../prediction/dataset` | Implementado (503 sin Monitoring, E31) |
| CU-09 | Predecir CPU a 15 min | Operador | «Estimar CPU» / «Predecir 15 min» | `POST /api/prediction/v1/predictions` | **Verificado** (E20, carga 600/600) |
| CU-10 | Recomendar ajuste de capacidad | Operador | Formulario de recomendación | `POST /api/recommendations/v1/recommendations` | **Verificado** (E22–E23) |
| CU-11 | Calcular energía y CO₂e | Operador | Pestaña Energía | `POST /api/recommendations/v1/energy` | **Verificado** (E24–E26 y UI) |
| CU-12 | Visualizar racks con calor | Observador+ | `network.html` | `metrics/current` + `racks.json` | Implementado (inventario verificado; métricas 503) |
| CU-13 | Visualizar red de flujos | Observador+ | `flows.html` | Cálculo en el navegador (`flows-logic.js`), propuesta ilustrativa | Implementado (lógica verificada por pruebas) |
| CU-14 | Ver experimento baseline vs Green AI | Observador+ | Pestaña Reportes | `experiment.json` estático | Implementado (resultado precalculado) |
| CU-15 | Entrenar y seleccionar modelo | Científico de datos | CLI | `scripts/run_pipeline.py` | **Verificado** (RF; MAE test 3,85) |
| CU-16 | Ejecutar ETL del Excel | Desarrollador | CLI | `scripts/run_greenai_etl.py` | Implementado (cubierto por pruebas) |
| CU-17 | Simular telemetría | Desarrollador | CLI / contenedor | `green-ai-simulator run` | **Verificado** (50 nodos, 4 254 series) |
| CU-18 | Evaluar alertas | Prometheus | Cada 5–15 s | `alerts.yml` (6 reglas) | **Verificado** (reglas cargadas; ninguna activa con escenario normal) |
| CU-19 | Asignar rol | Administrador | SQL manual en Supabase | `update public.user_roles` | Parcial (sin interfaz ni API) |
| CU-20 | Aprobar/rechazar recomendación | Operador/Admin | — | — | **No implementado** (HU-07: sin persistencia) |
| CU-21 | Exportar reporte en PDF | Usuario | — | — | **No implementado** (solo JSON/CSV) |

## 4. Especificaciones detalladas de los casos núcleo

### CU-09 Predecir CPU a 15 minutos
- **Precondiciones:** sesión válida con rol OPERATOR/ADMIN; artefacto `model.joblib` íntegro; ventana con datos suficientes tras remuestrear a 5 min.
- **Flujo principal:** 1) el operador elige clúster y servidor; 2) el frontend obtiene el dataset v1 de las últimas 2 h (CU-08); 3) envía el dataset a `POST /api/prediction/v1/predictions`; 4) Prediction adapta el contrato, remuestrea, limpia, construye 20 variables, verifica ausencia de variables futuras y predice; 5) responde `value` (%), `predictedFor` (+15 min), `origin=estimated`, `modelVersion`; 6) el panel muestra el valor con su procedencia.
- **Flujos alternativos:** A1 sin sesión → 401 → renovación única → login; A2 rol VIEWER → 403 «Tu rol no permite esta acción»; A3 datos insuficientes → 422 `INVALID_DATASET`/`INSUFFICIENT_DATA` (el frontend no reintenta el POST); A4 artefacto ausente/alterado → 503 `MODEL_UNAVAILABLE`; A5 Monitoring caído → 503 en el paso 2.
- **Postcondición:** se actualiza el *gauge* `green_ai_last_prediction_cpu_percent` solo si la predicción proviene de una recomendación (CU-10); la predicción no se persiste.

### CU-10 Recomendar ajuste de capacidad
- **Precondiciones:** las de CU-09; telemetría opcional declarada por el operador (memoria %, latencia p95, error %, instante, origen).
- **Flujo principal:** 1) dataset (CU-08) + telemetría; 2) Prediction valida la identidad del recurso y `datasetId`; 3) predice (CU-09 interno); 4) verifica que la predicción devuelta corresponde al mismo recurso y dataset (si no, 502); 5) `evaluate_policy` produce 5 comprobaciones; 6) calcula `status`/`action`; 7) incrementa `green_ai_recommendations_total{status}`; 8) devuelve la recomendación con `executionAllowed=false` y 3 advertencias fijas.
- **Alternativos:** sin telemetría ⇒ `not_evaluable`; algún umbral excedido ⇒ `blocked` (alerta `DemoPolicyBlocked`); dataset sin identidad ⇒ 422.
- **Postcondición:** ninguna acción sobre la infraestructura; no queda registro persistente de la recomendación.

### CU-07 Generar reporte de históricos
- **Precondiciones:** rol VIEWER+; fuente de históricos configurada (`supabase` o `sqlite`; con `none` → 503 `SOURCE_NOT_CONFIGURED`).
- **Flujo:** valida periodo (≤ 31 días, con zona) → recorre páginas de 500 por cursor *keyset* (máx. 200 páginas) → calcula media/p95/máx de CPU y RAM, % de carga alta, energía trapezoidal en Wh y huecos ignorados → JSON o CSV.
- **Observación:** el recorrido es síncrono dentro de la petición: un rango amplio puede leer hasta 100 000 filas antes de responder (timeout del Gateway: 15 s).

### CU-11 Calcular energía y CO₂e
- **Flujo:** muestras (archivo, ejemplo o CPU del simulador convertida a potencia modelada en el navegador) → validación (orden, huecos ≤ 300 s, 2–10 000) → kWh trapezoidal → CO₂e solo con factor y fuente → *gauges* de energía.
- **Verificado:** 3 muestras (400/420/410 W cada 5 min) ⇒ 0,06875 kWh exactos; ejemplo del frontend ⇒ 0,281 kWh.

## 5. Trazabilidad caso de uso ↔ código ↔ prueba

| CU | Código | Pruebas automatizadas del repo | Prueba de la auditoría |
|---|---|---|---|
| CU-06/07 | `read_historical_logs.py`, `historical_report.py`, adaptadores | `test_historical_logs*.py`, `test_historical_report.py`, `test_sqlite_profile.py` | E10–E16, UI |
| CU-08 | `prepare_prediction_dataset.py` | `test_prepare_prediction_dataset.py`, `test_monitoring_to_prediction_pipeline.py` | E31 |
| CU-09 | `inference/predict.py`, `service/app.py` | `tests/api`, `tests/integration`, `tests/temporal` | E20, E21, E27, carga |
| CU-10 | `recommendations/policy.py`, `service/recommendations.py` | `test_recommendations_api.py` | E22, E23 |
| CU-11 | `service/recommendations.py`, `frontend/energy.js` | `test_recommendations_api.py`, `energy.test.cjs` | E24–E26, UI |
| CU-03/04/05 | `MetricsController`, `MonitoringService`, `PrometheusQueryBuilder` | 12 clases JUnit | No ejecutable (Maven) |
| CU-02 + RBAC | `SecurityConfiguration.java`, `internal/auth`, `internal/policy` | `GatewayApplicationTests` (Java), 32 pruebas Go | E01–E08, E21, UI VIEWER |
| CU-15 | `training/train.py`, `evaluation/comparison.py` | `test_training_pipeline.py`, `test_comparison.py`, `test_anti_leakage.py` | Pipeline ejecutado |
| CU-17 | `simulator/domain`, `exporter.py` | 4 módulos `unittest` | Stack nativo |
