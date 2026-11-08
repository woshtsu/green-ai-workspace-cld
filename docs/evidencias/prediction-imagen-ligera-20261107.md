# Prediction: imagen de inferencia ligera (2026-11-07)

Cambio: `software/prediction/Dockerfile` multi-etapa (entrena con `requirements.lock.txt`; la imagen final instala solo
`requirements.serve.txt`), importación diferida de `xgboost` en `src/models/xgboost_model.py`, `--no-compile`,
sin carpetas `tests` de librerías y variables `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MALLOC_ARENA_MAX=2`.

| Medida | Antes | Después | Condiciones |
|---|---|---|---|
| Tamaño de imagen | 2,85 GB | **510 MB** | `docker images`, Docker Desktop/WSL2 |
| Memoria en reposo | 174 MiB | **133 MiB** (contenedor aislado) | `docker stats --no-stream`, una sola medición, sin carga |
| Memoria en reposo dentro del stack | 174 MiB | **142 MiB**; con `PYTHONOPTIMIZE=2`: **122 MiB** | `docker stats --no-stream` con el stack levantado |

Pruebas: suite completa de Prediction con el cambio, 100 pruebas sin fallos (entorno completo, Windows). Imagen: `/health/ready` 200
y servicio sin `xgboost`, `matplotlib`, `mlflow`, `seaborn` ni `statsmodels`. Stack completo reconstruido con la imagen nueva:
smoke 14/14 (`smoke-20261107-prediction-slim.json`).

Límites: una medición por caso, sin carga; el "antes" proviene de la medición del 2026-11-06 en el HANDOFF. No mide latencia
ni precisión. Los resultados del smoke usan datos simulados.

## Segunda optimización: PYTHONOPTIMIZE=2 y sin pip
Quita docstrings y `assert` en tiempo de ejecución (`src/` no usa `assert`) y desinstala pip/setuptools/wheel de la imagen final. RAM en reposo en el stack: 142 → **122 MiB** (una medición, sin carga). Tamaño sin cambio apreciable (510 MB). Smoke 14/14 (`smoke-20261107-prediction-slim2.json`); `sys.flags.optimize` = 2 en el contenedor. Riesgo: librerías que dependan de docstrings; el smoke no lo detectó. Las 100 pruebas se ejecutaron sin la opción, en el entorno completo.
