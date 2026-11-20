#!/bin/bash
# Arranque NATIVO del stack Green AI (equivalente a docker-compose.yml, sin Docker: Docker Hub y Maven Central
# están bloqueados en el entorno de auditoría). Puertos iguales a los MONO_* del monorepo.
R=<repo>/software
L=~/run_logs/services
mkdir -p $L ~/run_data/prom ~/run_data/simruns
# 0) Emisor JWT local (JWKS)
cd ~/idp && nohup python3 -m http.server 18999 --bind 127.0.0.1 > $L/idp.log 2>&1 &
# 1) Simulator (tick 5 s, 24 h, inventario de 50 nodos, escenario normal, semilla 42)
cd $R/simulator && nohup uv run --frozen green-ai-simulator run --inventory configs/inventory.hardware.json \
  --scenario configs/scenarios/normal.json --seed 42 --duration-seconds 86400 --tick-seconds 5 --mode realtime \
  --output-dir ~/run_data/simruns --host 127.0.0.1 --port 18000 > $L/simulator.log 2>&1 &
# 2) Prediction (FastAPI + modelo RF generado por run_pipeline.py)
cd $R/prediction && ML_ENV=experimental nohup ~/venvs/pred/bin/python -m uvicorn src.service.app:app \
  --host 127.0.0.1 --port 18002 > $L/prediction.log 2>&1 &
# 3) Data Processing (perfil SQLite de desarrollo; Monitoring en :18080 NO disponible)
cd $R/data-processing && APP_ENV=development HISTORICAL_SOURCE=sqlite SQLITE_PATH=~/run_data/greenai-dev.sqlite \
  SUPABASE_ENABLED=false MONITORING_BASE_URL=http://127.0.0.1:18080 REQUEST_TIMEOUT_SECONDS=10 \
  nohup ~/venvs/dp/bin/python -m uvicorn main:app --host 127.0.0.1 --port 18003 > $L/data-processing.log 2>&1 &
# 4) Prometheus (config del repo con targets locales)
sed -e "s#prediction:8000#127.0.0.1:18002#; s#simulator:8000#127.0.0.1:18000#; s#/etc/prometheus/alerts.yml#$R/infraestructura/prometheus/alerts.yml#" \
  $R/infraestructura/prometheus/prometheus.yml > ~/run_data/prometheus.local.yml
nohup ~/tools/prometheus-3.13.3.linux-amd64/prometheus --config.file=~/run_data/prometheus.local.yml \
  --web.listen-address=127.0.0.1:19090 --storage.tsdb.path=~/run_data/prom > $L/prometheus.log 2>&1 &
# 5) Gateway Go (alternativa validada del Gateway Java; mismas variables)
GATEWAY_PORT=18081 GATEWAY_MONITORING_BASE_URL=http://127.0.0.1:18080 GATEWAY_DATA_PROCESSING_BASE_URL=http://127.0.0.1:18003 \
  GATEWAY_PREDICTION_BASE_URL=http://127.0.0.1:18002 GATEWAY_AUTH_ISSUER_URI=http://127.0.0.1:18999/auth/v1 \
  GATEWAY_AUTH_JWK_SET_URI=http://127.0.0.1:18999/auth/v1/.well-known/jwks.json GATEWAY_CORS_ALLOWED_ORIGIN=http://127.0.0.1:13001 \
  GATEWAY_OPENAPI_DIR=$R/gateway/src/main/resources/static/openapi nohup ~/bin/gateway > $L/gateway-go.log 2>&1 &
# 6) Frontend estático (nginx no disponible: servidor estático de Python)
mkdir -p ~/run_data/front && cp $R/frontend/*.html $R/frontend/*.css $R/frontend/*.js $R/frontend/*.json $R/frontend/favicon.svg ~/run_data/front/
cat > ~/run_data/front/config.local.js <<'CFG'
window.GREEN_AI_CONFIG = Object.freeze({ supabaseUrl: 'https://audit-placeholder.supabase.co', supabasePublishableKey: 'sb_publishable_placeholder', gatewayBaseUrl: 'http://127.0.0.1:18081' });
CFG
cd ~/run_data/front && nohup python3 -m http.server 13001 --bind 127.0.0.1 > $L/frontend.log 2>&1 &
echo "stack lanzado"
