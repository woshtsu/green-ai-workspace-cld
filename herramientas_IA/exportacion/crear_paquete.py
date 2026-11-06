from pathlib import Path
import json, shutil
root=Path(__file__).resolve().parents[1]
out=root/'output/green-ai-portable'
out.mkdir(parents=True,exist_ok=True)
def write(name,text):
 p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
services=['simulator','monitoring','data-processing','prediction','gateway','frontend']
compose='''name: green-ai-portable
services:
  simulator:
    image: green-ai-portable/simulator:2026-10-21
    platform: linux/amd64
    command: [run, --inventory, configs/inventory.hardware.json, --scenario, configs/scenarios/normal.json, --seed, '42', --duration-seconds, '86400', --tick-seconds, '5', --mode, realtime, --output-dir, /app/runs, --host, 0.0.0.0, --port, '8000']
    volumes: [simulator-runs:/app/runs]
    restart: unless-stopped
  prometheus:
    image: prom/prometheus:v3.13.3
    platform: linux/amd64
    ports: ['127.0.0.1:${PROMETHEUS_PORT:-9090}:9090']
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    depends_on: [simulator]
    restart: unless-stopped
  monitoring:
    image: green-ai-portable/monitoring:2026-10-21
    platform: linux/amd64
    environment:
      MONITORING_PROMETHEUS_URL: http://prometheus:9090
      MONITORING_PROMETHEUS_DEFAULT_CLUSTER: sim-lab
      MONITORING_PROMETHEUS_INSTANCE_LABEL: node
    depends_on: [prometheus]
    restart: unless-stopped
  data-processing:
    image: green-ai-portable/data-processing:2026-10-21
    platform: linux/amd64
    environment:
      MONITORING_BASE_URL: http://monitoring:8080
      REQUEST_TIMEOUT_SECONDS: '10'
      SUPABASE_ENABLED: ${SUPABASE_ENABLED:-false}
      SUPABASE_URL: ${SUPABASE_URL:-}
      SUPABASE_API_KEY: ${SUPABASE_API_KEY:-}
      SUPABASE_READ_TOKEN: ${SUPABASE_READ_TOKEN:-}
    depends_on: [monitoring]
    restart: unless-stopped
  prediction:
    image: green-ai-portable/prediction:2026-10-21
    platform: linux/amd64
    restart: unless-stopped
  gateway:
    image: green-ai-portable/gateway:2026-10-21
    platform: linux/amd64
    ports: ['127.0.0.1:${GATEWAY_PORT:-8081}:8081']
    environment:
      GATEWAY_MONITORING_BASE_URL: http://monitoring:8080
      GATEWAY_DATA_PROCESSING_BASE_URL: http://data-processing:8000
      GATEWAY_PREDICTION_BASE_URL: http://prediction:8000
      GATEWAY_AUTH_ISSUER_URI: ${SUPABASE_AUTH_URL:-https://jpfugpsdhuucmilgysgg.supabase.co}/auth/v1
      GATEWAY_AUTH_JWK_SET_URI: ${SUPABASE_AUTH_URL:-https://jpfugpsdhuucmilgysgg.supabase.co}/auth/v1/.well-known/jwks.json
      GATEWAY_CORS_ALLOWED_ORIGIN: http://127.0.0.1:${FRONTEND_PORT:-3001}
    depends_on: [monitoring, data-processing, prediction]
    restart: unless-stopped
  frontend:
    image: green-ai-portable/frontend:2026-10-21
    platform: linux/amd64
    ports: ['127.0.0.1:${FRONTEND_PORT:-3001}:3001']
    volumes: ['${FRONTEND_CONFIG:-./config.local.js}:/usr/share/nginx/html/config.local.js:ro']
    depends_on: [gateway]
    restart: unless-stopped
  grafana:
    image: grafana/grafana:12.4.11
    platform: linux/amd64
    ports: ['127.0.0.1:3000:3000']
    environment:
      GF_AUTH_ANONYMOUS_ENABLED: 'true'
      GF_AUTH_ANONYMOUS_ORG_ROLE: Viewer
      GF_USERS_ALLOW_SIGN_UP: 'false'
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD:-green-ai-local-demo}
      GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH: /var/lib/grafana/dashboards/green-ai.json
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
      - grafana-data:/var/lib/grafana
    depends_on: [prometheus]
    restart: unless-stopped
volumes:
  simulator-runs:
  prometheus-data:
  grafana-data:
'''
write('compose.yaml',compose)
write('prometheus.yml','''global:
  scrape_interval: 5s
scrape_configs:
  - job_name: green-ai-simulator
    static_configs:
      - targets: ['simulator:8000']
  - job_name: green-ai-monitoring
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ['monitoring:8080']
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']
''')
write('grafana/provisioning/datasources/prometheus.yaml','''apiVersion: 1
datasources:
  - name: Prometheus
    uid: prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: 5s
''')
write('grafana/provisioning/dashboards/default.yaml','''apiVersion: 1
providers:
  - name: Green AI
    type: file
    options:
      path: /var/lib/grafana/dashboards
''')
panels=[]
def panel(title,expr,unit,x,y,w=12,h=8,legend='{{node}}',kind='timeseries'):
 panels.append({'id':len(panels)+1,'title':title,'type':kind,'gridPos':{'x':x,'y':y,'w':w,'h':h},'datasource':{'type':'prometheus','uid':'prometheus'},'targets':[{'refId':'A','expr':expr,'legendFormat':legend}],'fieldConfig':{'defaults':{'unit':unit},'overrides':[]},'options':{'legend':{'displayMode':'list','placement':'bottom'}}})
panel('Recoleccion activa (1 = UP)', 'up', 'short',0,0,8,5,'{{job}}','stat')
panel('Muestras ingeridas por segundo - Prometheus real','rate(prometheus_tsdb_head_samples_appended_total[1m])','ops',8,0,8,5,kind='stat')
panel('Memoria JVM Monitoring - proceso real','sum(jvm_memory_used_bytes{job="green-ai-monitoring"})','bytes',16,0,8,5,kind='stat')
panel('CPU por nodo - SIMULADA','100 * (1 - avg by (cluster,node) (rate(node_cpu_seconds_total{job="green-ai-simulator",mode="idle"}[1m])))','percent',0,5)
panel('Memoria por nodo - SIMULADA','100 * (1 - node_memory_MemAvailable_bytes{job="green-ai-simulator"} / node_memory_MemTotal_bytes{job="green-ai-simulator"})','percent',12,5)
panel('Red recibida por nodo - SIMULADA','sum by (cluster,node) (rate(node_network_receive_bytes_total{job="green-ai-simulator"}[1m]))','Bps',0,13)
panel('Filesystem usado - SIMULADO','100 * (1 - node_filesystem_free_bytes{job="green-ai-simulator"} / node_filesystem_size_bytes{job="green-ai-simulator"})','percent',12,13)
write('grafana/dashboards/green-ai.json',json.dumps({'uid':'green-ai-live','title':'Green AI | Prometheus en vivo | Nodos SIMULADOS','schemaVersion':39,'version':1,'editable':False,'refresh':'5s','time':{'from':'now-15m','to':'now'},'timezone':'browser','tags':['green-ai','simulated'],'panels':panels},ensure_ascii=False,indent=2))
shutil.copyfile(root/'green-ai-front-end/Frontend-GreenAi/config.local.js',out/'config.local.js')
write('.env.example','''# Solo completar para habilitar lectura de historicos. Nunca compartir tokens.
SUPABASE_ENABLED=false
SUPABASE_URL=
SUPABASE_API_KEY=
SUPABASE_READ_TOKEN=
SUPABASE_AUTH_URL=https://jpfugpsdhuucmilgysgg.supabase.co
GRAFANA_ADMIN_PASSWORD=green-ai-local-demo
''')
write('README.md','''# Green AI portable

## Iniciar en otro equipo
1. Instalar Docker Engine + Compose v2 o Docker Desktop con contenedores Linux.
2. Copiar TODA esta carpeta, incluido imagenes.tar, sin cambiar su estructura.
3. Abrir una terminal dentro de esta carpeta y ejecutar:

```sh
docker load -i imagenes.tar
docker compose up -d --pull never
docker compose ps
```

Abrir http://127.0.0.1:3001 (aplicacion) y http://127.0.0.1:3000/d/green-ai-live (Grafana).
Prometheus: http://127.0.0.1:9090/targets . Esperar 1-2 minutos para las tasas de CPU/red.
El dashboard se instala automaticamente y refresca cada 5 segundos. No necesita login para visualizarse.
Administracion local de Grafana: admin / green-ai-local-demo (cambiar con .env antes del primer arranque).
Los puertos estan ligados a loopback: abrir en el mismo equipo que ejecuta Docker.

## Que se esta demostrando
Simulator -> /metrics -> Prometheus -> Grafana.
Prometheus tambien recolecta /actuator/prometheus de Monitoring y sus propias metricas.
Las curvas CPU/memoria/red/disco de nodos son SIMULADAS, aunque se recolectan en vivo.
La JVM de Monitoring y la ingestion de Prometheus son mediciones de procesos ejecutados.
No afirmar que son mediciones de servidores universitarios ni energia medida.
La aplicacion conserva su flujo Frontend -> Gateway -> Monitoring/Data Processing/Prediction.
Grafana consulta Prometheus directamente; no reemplaza el frontend ni necesita Supabase.

## Captura solicitada
Abrir el dashboard, esperar a ver curvas y targets UP; seleccionar ultimos 15 minutos.
Tomar captura de pantalla con el titulo (SIMULADOS), paneles, rango de tiempo y actualizacion 5s visibles.
Complementarla con captura de http://127.0.0.1:9090/targets, donde deben aparecer los tres targets UP.
Si exigen metricas de hardware real, las curvas del simulador NO satisfacen esa condicion:
se necesita un exporter sobre el host o cluster real y mantener separada su procedencia.

## Dependencias externas y limites
Las imagenes no incluyen usuarios, contrasenas, base de datos ni historicos de Supabase.
El frontend utiliza Supabase Auth y su SDK desde un CDN: login/registro requieren Internet
y una cuenta autorizada en el proyecto configurado en config.local.js. La clave publishable
incluida es publica; nunca poner service_role o tokens privados en ese archivo.
Para otro Supabase, ajustar config.local.js y SUPABASE_AUTH_URL en .env, usuarios y permisos.
Historicos: deshabilitados por defecto. Copiar .env.example a .env y completar SUPABASE_*
con un token de servidor dedicado con SELECT minimo sobre logs, segun el servicio de datos.
No se exportaron datos ni secretos. Sin esas credenciales, NO se replica el historico remoto.
Prediction contiene el modelo generado por su Dockerfile; no demuestra reentrenamiento continuo.
Este paquete ejecuta los servicios Compose actuales; no despliega Kubernetes ni sus workloads.
Imagenes linux/amd64: nativo en PC Intel/AMD; ARM requiere emulacion compatible, no validada aqui.
Reservar espacio para el TAR y las imagenes importadas; el predictor es la imagen mas grande.
El simulador genera ejecuciones de 24 horas; restart inicia otra al finalizar, con otro cluster/run.

## Operacion
```sh
docker compose logs --tail 100
docker compose stop
docker compose start
docker compose down
```
Los volumenes preservan Prometheus, Grafana y runs. No usar down -v si desea conservarlos.
Una replica nueva inicia con historicos locales vacios; el TAR solo transporta imagenes.

Provisioning basado en https://grafana.com/docs/grafana/latest/administration/provisioning/
''')
print(out)

