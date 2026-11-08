# Despliegue de desarrollo en Render (2026-11-07)

Servicios creados en el workspace «My Workspace» (plan gratuito, región Oregón, rama `test`, commit `886b034`, Auto-Deploy apagado):

| Servicio | URL pública | Estado del despliegue |
|---|---|---|
| green-ai-prediction-dev | https://green-ai-prediction-dev-zxly.onrender.com | live (build ~2 min 50 s) |
| green-ai-data-processing-dev | https://green-ai-data-processing-dev.onrender.com | live (~1 min) |
| green-ai-gateway-dev | https://green-ai-gateway-dev.onrender.com | live (~1 min) |

Comprobaciones con `curl` desde fuera (mismo día):
| Prueba | Resultado |
|---|---|
| `GET /health/ready` de Prediction | 200 |
| `GET /api/v1/health` de Data Processing | 200 |
| `GET` y `POST` al Gateway `/api/prediction/v1/predictions` sin JWT | 401 (correcto) |
| Preflight CORS desde `https://woshtsu.github.io` | 200, `access-control-allow-origin` correcto |

Límites: no se probó con sesión real de Supabase ni una predicción autenticada; Monitoring, Simulator y Prometheus no están desplegados (Monitoring apunta a una URL de relleno); los servicios gratuitos se suspenden tras 15 min sin tráfico. Falta fijar el *Health Check Path* en el panel y capturas de pantalla para el informe.

## Entorno completo en la nube (2026-11-07, tarde)
Añadidos en Render: `green-ai-simulator-dev`, `green-ai-prometheus-dev` (imagen con `Dockerfile.render`, scrape HTTPS) y `green-ai-monitoring-dev`; Gateway y Data Processing apuntan a Monitoring. Seis servicios en plan gratuito, rama `test`.

| Prueba | Resultado |
|---|---|
| Prometheus `/api/v1/targets` | prediction y simulator `up` |
| Monitoring `/api/v1/metrics/current?metric=node.cpu.utilization` | datos del Simulator (1.ª llamada en frío: 504; siguientes: 200) |
| Frontend en `https://woshtsu.github.io/green-ai-workspace-cld/dev/` con sesión real de Supabase (rol OPERATOR) | «Racks con calor»: 50 nodos con CPU en vivo (media 84,9 %), origen «Simulado» |
| «Predecir 15 min» a los ~14 min de arrancar el Simulator | 422 `INSUFFICIENT_DATA` («necesita ~20 min de historial»): esperado, no es un fallo |

Capturas: `entregables/informe-corregido/evidencias-nube/`. Pendiente: repetir la predicción con ≥ 20 min de historial; las URLs de redirección de Supabase (las añade el propietario del proyecto). Todos los nodos están ~85 % porque el escenario es `high`; para el video conviene variar la carga.
