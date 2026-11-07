# Etapa 1: entrenamiento (dependencias completas; no llegan a la imagen final).
FROM python:3.11.9-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 MPLBACKEND=Agg ML_ENV=experimental
WORKDIR /app

COPY requirements.txt requirements.lock.txt ./
RUN pip install --no-cache-dir -r requirements.lock.txt

COPY src ./src
COPY config ./config
COPY contracts ./contracts
COPY scripts ./scripts
COPY data/raw ./data/raw
COPY data/fixtures ./data/fixtures

RUN python scripts/run_pipeline.py --skip-mlflow

# Etapa 2: inferencia (solo dependencias de servicio, ver requirements.serve.txt).
FROM python:3.11.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLBACKEND=Agg \
    ML_ENV=experimental \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MALLOC_ARENA_MAX=2 \
    PYTHONOPTIMIZE=2

WORKDIR /app

RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser

COPY requirements.serve.txt ./
# --no-compile y sin carpetas de pruebas de las librerías: menos peso sin tocar el código en uso.
RUN pip install --no-cache-dir --no-compile -r requirements.serve.txt \
    && find /usr/local/lib/python3.11/site-packages -type d \( -name tests -o -name test \) -prune -exec rm -rf {} + \
    && find /usr/local/lib/python3.11/site-packages -name "*.pyc" -delete \
    && pip uninstall -y pip setuptools wheel

COPY --from=builder --chown=appuser:appuser /app /app

USER 10001:10001

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.service.app:app", "--host", "0.0.0.0", "--port", "8000"]
