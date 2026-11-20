# Instalación — Prompt 4: Reconstrucción del Entorno

> **Rol:** Ingeniero DevOps · **Fase 3** · Objetivo: reconstruir el entorno para ejecutar Green AI en **Linux Ubuntu** (probado en Ubuntu 24.04.5 LTS, 2 vCPU, 7 GiB RAM).
> Los procedimientos marcados **[EJECUTADO]** se corrieron en esta auditoría; los marcados **[NO EJECUTADO]** no pudieron correrse por restricciones de red del entorno (Docker Hub y Maven Central bloqueados) y se derivan de los Dockerfiles, el CI y el README.

## 1. Software requerido

| Software | Para qué | Obligatorio |
|---|---|---|
| Git | Clonar el monorepo | Sí |
| Docker Engine + Compose v2 (≥ 2.24) | Ruta recomendada: todo el stack con un comando | Sí (ruta Docker) |
| JDK 21 (Temurin/OpenJDK) | Monitoring y Gateway Java (ruta nativa) | Ruta nativa |
| Go 1.25.x | Gateway Go (ruta nativa) | Opcional |
| uv (gestor Python) | Crear entornos con la versión exacta de Python | Ruta nativa |
| Python 3.11.9 / 3.12 / 3.14 | Prediction / Simulator / Data Processing | Ruta nativa (uv los instala) |
| Node.js 22 | Pruebas del frontend | Solo pruebas |
| Prometheus 3.13.3 | Series temporales | Ruta nativa |
| Grafana 12.4.0 | Dashboard opcional | No |

## 2. Versiones recomendadas

| Componente | Versión recomendada | Fuente de la versión |
|---|---|---|
| Docker Compose | ≥ 2.24 (usa `env_file.required`, `bind.create_host_path`) | `docker-compose.yml` |
| Java | Temurin 21 | `pom.xml`, Dockerfiles |
| Maven | Wrapper del repo (`./mvnw`) / 3.9.11 | `.mvn/wrapper`, Dockerfile del Gateway |
| Go | 1.25.14 | Imagen de build del Gateway Go |
| Python | 3.11.9 (Prediction), 3.12 (Simulator), 3.14 (Data Processing) | `.python-version`, Dockerfiles, CI |
| Node.js | 22 | CI |
| Prometheus | v3.13.3 | Compose |
| PostgreSQL / PostgREST (contrato) | 17.6 / v13.0.7 | `compose.contract-postgres.yml` |

## 3. Servicios externos requeridos
1. **Proyecto Supabase** (Auth obligatorio para usar el panel; Data API opcional para históricos). Pasos: ejecutar `software/frontend/supabase-auth-setup.sql` en el SQL Editor, activar el *Custom Access Token Hook* con `public.custom_access_token_hook`, añadir la URL del frontend a *Redirect URLs*.
2. **Acceso a CDNs** (jsDelivr, cdnjs, Google Fonts) desde el navegador.
3. Para nube: cuenta de **Render** (Blueprint `render.yaml`) y **GitHub Pages** (workflow `pages.yml`).

## 4. Bases de datos requeridas
| Escenario | Base | Preparación |
|---|---|---|
| Producción/nube | Supabase PostgreSQL (`hardware`, `logs`, `user_profiles`, `user_roles`) | SQL de `supabase-auth-setup.sql`; carga de `logs` desde `BD_GreenAi.xlsx` (fuera del repo) |
| Desarrollo | SQLite de solo lectura | `scripts/seed_sqlite.py` (50 hardware, 100 000 logs, ~7 s, 26 MB) **[EJECUTADO]** |
| Pruebas de contrato | PostgreSQL 17 + PostgREST v13 | `compose.contract-postgres.yml` con secretos aleatorios |
| Métricas | Prometheus TSDB | Automática |

## 5. Variables de entorno
Detalle completo en [`variables_entorno.md`](variables_entorno.md). Mínimo para la ruta Docker: ninguna obligatoria (el Compose trae valores por defecto, incluido el *issuer* del proyecto Supabase del equipo). Para usar otro proyecto: `GATEWAY_AUTH_ISSUER_URI`, `GATEWAY_AUTH_JWK_SET_URI` y `software/frontend/config.local.js`.

## 6. Configuración necesaria
- `software/frontend/config.local.js` (copia de `config.example.js`, con `gatewayBaseUrl: 'http://127.0.0.1:18081'`). **Obligatorio**: el Compose monta el archivo con `create_host_path: false` y falla si no existe.
- Opcional: `software/data-processing/.env` (copia de `.env.example`).
- Opcional: `DEMO_POLICY_JSON` para cambiar los umbrales de recomendación.

## 7. Procedimiento completo de instalación (Ubuntu)

### 7.1 Ruta A — Docker Compose (recomendada) **[NO EJECUTADO: Docker Hub bloqueado en el entorno de auditoría]**
```bash
# 1. Docker Engine + Compose (repositorio oficial de Docker)
sudo apt-get update && sudo apt-get install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER" && newgrp docker

# 2. Código y configuración del frontend
git clone https://github.com/woshtsu/green-ai-workspace-cld.git && cd green-ai-workspace-cld
cp software/frontend/config.example.js software/frontend/config.local.js
sed -i "s#http://127.0.0.1:8081#http://127.0.0.1:18081#" software/frontend/config.local.js
# Editar supabaseUrl y supabasePublishableKey con los datos del proyecto Supabase

# 3. Validar y levantar (7 servicios; el build de Prediction entrena el modelo)
docker compose -f software/infraestructura/docker-compose.yml config --quiet
docker compose -f software/infraestructura/docker-compose.yml -f software/infraestructura/compose.swagger.yaml up -d --build

# 4. Verificación
python3 software/infraestructura/smoke/smoke.py --out /tmp/smoke.json   # 14 casos
# Frontend http://127.0.0.1:13001 · Gateway :18081 · Prometheus :19090 · Swagger Prediction :18002/docs

# Opcionales
docker compose -f software/infraestructura/docker-compose.yml -f software/infraestructura/compose.gateway-go.yml up -d --build gateway-go   # :18082
GRAFANA_ADMIN_PASSWORD='<elegir>' docker compose -f software/infraestructura/docker-compose.yml -f software/infraestructura/compose.observability.yml up -d grafana   # :13002
```

### 7.2 Ruta B — Nativa (sin Docker) **[EJECUTADO, salvo los servicios Java]**
```bash
# 0. Herramientas
sudo apt-get update && sudo apt-get install -y git curl openjdk-21-jdk
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.local/bin/env
curl -fsSL https://go.dev/dl/go1.25.14.linux-amd64.tar.gz | sudo tar -C /usr/local -xz && export PATH=$PATH:/usr/local/go/bin
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs
curl -sSL https://github.com/prometheus/prometheus/releases/download/v3.13.3/prometheus-3.13.3.linux-amd64.tar.gz | tar xz -C ~/

git clone https://github.com/woshtsu/green-ai-workspace-cld.git && cd green-ai-workspace-cld/software
export R=$PWD

# 1. Simulator (Python 3.12+, uv.lock)            [EJECUTADO: 10/10 pruebas]
cd $R/simulator && uv run --frozen python -m unittest discover -s tests
nohup uv run --frozen green-ai-simulator run --inventory configs/inventory.hardware.json \
  --scenario configs/scenarios/normal.json --seed 42 --duration-seconds 86400 --tick-seconds 5 \
  --mode realtime --output-dir /tmp/simruns --host 127.0.0.1 --port 18000 > /tmp/simulator.log 2>&1 &

# 2. Prediction (Python 3.11.9): entrenar el modelo ANTES de pruebas y arranque   [EJECUTADO: 100/100]
cd $R/prediction && uv venv .venv --python 3.11.9 && uv pip install --python .venv/bin/python -r requirements-dev.txt
MPLBACKEND=Agg .venv/bin/python scripts/run_pipeline.py --skip-mlflow     # genera models/selected/model.joblib
.venv/bin/python -m pytest -q
nohup .venv/bin/python -m uvicorn src.service.app:app --host 127.0.0.1 --port 18002 > /tmp/prediction.log 2>&1 &
git -C $R/.. checkout -- software/prediction/results/manifest.json        # el pipeline reescribe un archivo versionado

# 3. Data Processing (Python 3.14) con históricos SQLite   [EJECUTADO: 121 OK + 8 omitidas]
cd $R/data-processing && uv venv .venv --python 3.14 && uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/seed_sqlite.py --db .local/greenai-dev.sqlite
APP_ENV=development HISTORICAL_SOURCE=sqlite SQLITE_PATH=$PWD/.local/greenai-dev.sqlite SUPABASE_ENABLED=false \
MONITORING_BASE_URL=http://127.0.0.1:18080 nohup .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 18003 > /tmp/dp.log 2>&1 &

# 4. Prometheus con la configuración del repo apuntando a localhost   [EJECUTADO]
sed -e "s#prediction:8000#127.0.0.1:18002#; s#simulator:8000#127.0.0.1:18000#; s#/etc/prometheus/alerts.yml#$R/infraestructura/prometheus/alerts.yml#" \
  $R/infraestructura/prometheus/prometheus.yml > /tmp/prometheus.local.yml
~/prometheus-3.13.3.linux-amd64/promtool check rules $R/infraestructura/prometheus/alerts.yml
nohup ~/prometheus-3.13.3.linux-amd64/prometheus --config.file=/tmp/prometheus.local.yml \
  --web.listen-address=127.0.0.1:19090 --storage.tsdb.path=/tmp/prom > /tmp/prometheus.log 2>&1 &

# 5. Monitoring (Java 21)   [NO EJECUTADO: Maven Central inaccesible en el entorno de auditoría]
cd $R/monitoring && ./mvnw -B verify
MONITORING_PROMETHEUS_URL=http://127.0.0.1:19090 MONITORING_PROMETHEUS_DEFAULT_CLUSTER=sim-lab \
MONITORING_PROMETHEUS_INSTANCE_LABEL=node SERVER_PORT=18080 \
nohup java -jar target/monitoring-service-0.0.1-SNAPSHOT.jar > /tmp/monitoring.log 2>&1 &

# 6a. Gateway Java (predeterminado)   [NO EJECUTADO]
cd $R/gateway && ./mvnw -B verify
GATEWAY_PORT=18081 GATEWAY_MONITORING_BASE_URL=http://127.0.0.1:18080 GATEWAY_DATA_PROCESSING_BASE_URL=http://127.0.0.1:18003 \
GATEWAY_PREDICTION_BASE_URL=http://127.0.0.1:18002 GATEWAY_CORS_ALLOWED_ORIGIN=http://127.0.0.1:13001 \
GATEWAY_AUTH_ISSUER_URI=https://<ref>.supabase.co/auth/v1 GATEWAY_AUTH_JWK_SET_URI=https://<ref>.supabase.co/auth/v1/.well-known/jwks.json \
nohup java -jar target/gateway-service-0.1.0-SNAPSHOT.jar > /tmp/gateway.log 2>&1 &

# 6b. Gateway Go (alternativa)   [EJECUTADO: 32/32 pruebas con -race; binario de 6,9 MB]
cd $R/gateway-go && go vet ./... && go test -race ./... && CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /tmp/gateway ./cmd/gateway
GATEWAY_PORT=18081 GATEWAY_OPENAPI_DIR=$R/gateway/src/main/resources/static/openapi (... mismas variables que 6a ...) nohup /tmp/gateway > /tmp/gateway-go.log 2>&1 &

# 7. Frontend   [EJECUTADO: 48/48 pruebas; servido con servidor estático]
cd $R/frontend && node --test tests/*.test.cjs        # OJO: «node --test tests/» falla en Node 22
cp config.example.js config.local.js   # editar supabaseUrl, supabasePublishableKey, gatewayBaseUrl=http://127.0.0.1:18081
python3 -m http.server 13001 --bind 127.0.0.1         # o nginx con nginx.conf

# 8. Verificación
cd $R/.. && python3 software/infraestructura/smoke/smoke.py   # [EJECUTADO: 12/14; fallan los 2 casos de Monitoring]
```

## 8. Desviaciones encontradas al reconstruir el entorno
| # | Situación | Impacto | Solución aplicada / recomendada |
|---|---|---|---|
| 1 | `go.mod` exige Go 1.25 y el *toolchain* se descarga de `proxy.golang.org` | Sin red al proxy, `go` no compila | Instalar Go 1.25 localmente (en la auditoría se usó 1.24.7 sobre una copia con `go 1.24`: compila y pasa) |
| 2 | El pipeline de Prediction reescribe `results/manifest.json` (versionado) | Árbol Git «sucio» tras cada entrenamiento | `git checkout` posterior o dejar de versionar el archivo |
| 3 | `node --test tests/` falla; hay que pasar los archivos | CI y README ya lo contemplan | Usar `tests/*.test.cjs` |
| 4 | `config.local.js` inexistente bloquea `docker compose up` | Error de montaje | Crear el archivo antes de levantar |
| 5 | Monitoring y Gateway Java requieren Maven Central | Sin acceso, no se construyen | Caché `~/.m2` o *mirror* corporativo |
| 6 | Docker Hub requerido por todas las imágenes | Sin acceso, no hay ruta A | *Mirror* de registro o ruta nativa |
| 7 | El Simulator termina al cumplir `--duration-seconds` (3600 s en el `Dockerfile`, 86400 s en Compose) y ningún servicio del Compose define política `restart` | Tras 1 h/24 h deja de haber telemetría; si se relanza, la etiqueta `cluster=sim-run-<uuid>` cambia y se pierde la continuidad del historial (el repo documenta un 422 INSUFFICIENT_DATA por esta causa) | Usar 86400 s y añadir `restart: unless-stopped`; fijar un nombre de clúster estable |
