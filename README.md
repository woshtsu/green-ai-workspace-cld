# Green AI — monorepo

Sistema de monitoreo y predicción de demanda computacional (Taller de Proyectos 1).
Migración en curso desde el workspace de repositorios anidados; **el workspace antiguo sigue siendo la entrega vigente**.
Estado y siguiente paso: [docs/HANDOFF.md](docs/HANDOFF.md). Decisiones: [docs/DECISIONES.md](docs/DECISIONES.md).

## Estructura
| Ruta | Contenido |
|---|---|
| `software/monitoring` | API Java/Spring que consulta Prometheus (sin BD propia) |
| `software/simulator` | CLI Python que genera métricas sintéticas y las expone a Prometheus |
| `software/gateway` | Spring Cloud Gateway: JWT de Supabase, RBAC, CORS, rutas |
| `software/data-processing` | FastAPI: ETL e históricos (incluye `datasets/`) |
| `software/prediction` | FastAPI + ML: predicción **y** recomendaciones |
| `software/frontend` | HTML/JS estático servido por nginx |
| `software/infraestructura` | Compose, Prometheus, Grafana |
| `guias/`, `entregables/`, `exportados/` | Guías docentes, informes Markdown (fuente de verdad), DOCX generados |
| `herramientas_IA/` | Adaptador Antigravity, scripts de migración/exportación, instalación de Graphify |

Flujo: frontend → gateway → monitoring → Prometheus; gateway → data-processing y prediction.

## Pruebas por servicio (Windows/PowerShell, desde la raíz)
```powershell
cd software\monitoring; .\mvnw.cmd -B verify; cd ..\..
cd software\gateway; .\mvnw.cmd -B verify; cd ..\..
cd software\simulator; uv run --frozen python -m unittest discover -s tests; cd ..\..
cd software\data-processing; uv venv .venv; uv pip install --python .venv\Scripts\python.exe -r requirements.txt; .venv\Scripts\python.exe -m pytest -q; cd ..\..
cd software\prediction; uv venv .venv --python 3.11.9; uv pip install --python .venv\Scripts\python.exe -r requirements-dev.txt; $env:MPLBACKEND='Agg'; .venv\Scripts\python.exe scripts\run_pipeline.py --skip-mlflow; .venv\Scripts\python.exe -m pytest -q; cd ..\..
cd software\frontend; node --test tests/frontend.test.cjs tests/prediction.test.cjs tests/recommendations.test.cjs; cd ..\..
```

## Ejecución local con Docker
```powershell
Copy-Item software\frontend\config.example.js software\frontend\config.local.js   # editar; gatewayBaseUrl http://127.0.0.1:18081
docker compose -f software/infraestructura/docker-compose.yml -f software/infraestructura/compose.swagger.yaml up -d --build
```
Frontend http://127.0.0.1:13001 · Gateway :18081 · Prometheus :19090 · Swagger Prediction :18002/docs.
Puertos distintos del workspace antiguo para que ambos puedan coexistir.
