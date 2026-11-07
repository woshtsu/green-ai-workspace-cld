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
