# Recommendations · PMV2 de demostración

Responsabilidad: componente Policy Engine de Green AI, mantenido por el equipo backend del proyecto. Consulta Prediction, evalúa restricciones y devuelve propuestas para revisión humana. No modifica infraestructura ni aprueba acciones. La telemetría de SLA se ingresa manualmente y su procedencia es declarada, no certificada.

## Contrato

OpenAPI reproducible: `openapi.json`, generado desde `app.py`; también disponible en `/openapi.json` al ejecutar el servicio.

| Método/ruta interna | Entrada y resultado |
| --- | --- |
| GET `/health` | Disponibilidad del motor y modo demo; no comprueba Prediction |
| POST `/v1/recommendations` | `{dataset, telemetry?}`. El dataset completo proviene de Data Processing; el servicio invoca Prediction y comprueba identidad, unidad, valor y vigencia. |
| POST `/v1/energy` | `{origin, samples:[{timestamp,watts}], emissionFactorKgPerKwh?, emissionFactorSource?}`. Integración trapezoidal W·s/3 600 000 → kWh; CO₂e opcional en kg. |
| GET `/metrics` | Métricas internas Prometheus; no publicado por Gateway |

`telemetry`: `{resource:{type:"node",cluster,id}, observedAt, origin:"observed"|"simulated", memoryPercent?, latencyP95Ms?, errorRatePercent?}`. Fechas con zona horaria. Campos ausentes permanecen desconocidos. Errores se expresan en porcentaje, de 0 a 100.

Resultados: `not_evaluable` si falta evidencia, `blocked` cuando alguna restricción conocida falla, `eligible_for_review` cuando las comprobaciones actuales pasan. Nunca significa SLA futuro garantizado. Todas las respuestas incluyen `executionAllowed:false`, política, comprobaciones, recurso, dataset, predicción y referencia de recomendación. No hay persistencia de decisiones ni aprobación/rechazo en esta entrega.

Gateway expone exclusivamente POST `/api/recommendations/v1/recommendations` y `/api/recommendations/v1/energy`, con JWT y rol ADMIN/OPERATOR, límite de 2 MB y timeout de 30 s. Servicio interno sin puerto publicado: debe mantenerse detrás del Gateway y en red de confianza. HTTP 422: entrada inválida; 502: Prediction no disponible/incompatible; 504: timeout. No reintentos.

## Configuración autorizada: demostración

`PREDICTION_BASE_URL`: dirección administrada por despliegue, nunca aportada por el cliente; default `http://prediction:8000`. Timeout interno 25 s.

`DEMO_POLICY_JSON`: objeto JSON opcional; claves y defaults:

```json
{"cpuLowPercent":30,"cpuHighPercent":80,"memoryMaxPercent":85,"latencyP95MaxMs":500,"errorRateMaxPercent":1,"freshnessSeconds":300}
```

La configuración inválida impide el arranque. La evaluación exige telemetría reciente del mismo nodo y predicción vigente; CPU por debajo/encima de umbrales propone **revisar** reducción/aumento, sin dimensionar ni ejecutar réplicas. Valores iguales a límites pasan. No se deduce potencia a partir de CPU. Energía requiere 2–10 000 muestras ordenadas, sin duplicados ni huecos mayores a 300 s. Factor de emisiones exige fuente; sin él CO₂e es `null`.

## Ejecutar y comprobar

Desde la raíz del workspace, con Docker Desktop iniciado:

```powershell
docker compose up --build -d
# Grafana opcional: definir antes GRAFANA_ADMIN_PASSWORD con una contraseña propia.
docker compose -f docker-compose.yml -f compose.observability.yml up --build -d
```

Frontend: `http://127.0.0.1:3001`; Grafana: `http://127.0.0.1:3002`, usuario `admin`. Dashboard provisionado **Green AI · PMV2 demo**. Alertas visibles en Prometheus, sin notificaciones externas configuradas. Los contadores se reinician al reiniciar el servicio; energía muestra el último periodo importado por procedencia, nunca consumo acumulado o ahorro. La CPU mostrada es la última consulta, no un promedio de la flota.

Desarrollo local, Python 3.13, desde este directorio:

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m unittest discover -s tests
& .\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8002
```

Smoke visual aislado: `python tests/browser_preview.py`, abrir `http://127.0.0.1:8766`. Usa handlers reales y fixtures de Prediction/Data Processing; no prueba autenticación ni integración completa. Nunca desplegar este harness. API y dependencias verificadas localmente con las versiones de `requirements.txt`.

Provisionamiento Grafana basado en [documentación oficial](https://grafana.com/docs/grafana/latest/administration/provisioning/).
