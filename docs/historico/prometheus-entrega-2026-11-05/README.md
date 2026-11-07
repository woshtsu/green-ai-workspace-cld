# Prometheus para Green AI

Paquete de configuración preparado el 5 de noviembre de 2026. Usa la imagen oficial prom/prometheus:v3.13.3; no requiere un repositorio de código propio ni un Dockerfile.
No incluye imágenes Docker, históricos, Grafana, credenciales ni los microservicios. La primera descarga requiere Internet. Es una base de despliegue: ajustar la conectividad al servidor de destino antes de utilizarla.

## 1. Si Green AI ya usa el Compose general
Ese Compose YA contiene Prometheus. Basta desplegar ese servicio con su configuración; no hace falta iniciar un segundo Prometheus. Este paquete sirve si se decidió administrarlo por separado.

## 2. Mismo servidor Docker, aplicación desplegada por separado
Desde esta carpeta, comprobar el nombre de la red de la aplicación:

    docker network ls

El override usa green-ai-workspace_default. Si la red real tiene otro nombre, cambiar el valor de `name` en compose.red-compartida.yaml o definir GREEN_AI_NETWORK en un archivo .env.
Prediction y Simulator deben pertenecer a esa red y resolver como prediction y simulator, respectivamente. No son direcciones públicas ni funcionan entre servidores distintos.

Validar configuración y arrancar:

    docker compose -f compose.yaml -f compose.red-compartida.yaml config --quiet
    docker compose -f compose.yaml -f compose.red-compartida.yaml run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml
    docker compose -f compose.yaml -f compose.red-compartida.yaml up -d

En Monitoring configurar MONITORING_PROMETHEUS_URL=http://green-ai-prometheus:9090 y recrear ese servicio desde su propio despliegue. Si se usa Grafana en la misma red, su datasource debe apuntar a esa misma URL.
No mantener dos instancias con el mismo puerto 9090 del host. Si ya existe una, decidir cuál conservar antes de iniciar esta; no borrar sus volúmenes.

## 3. Servidor diferente
Editar los targets de prometheus.yml: reemplazar prediction:8000 y simulator:8000 por DNS/IP privados y puertos accesibles DESDE el contenedor Prometheus. Mantener los job_name para que las reglas sigan funcionando. El endpoint predeterminado es /metrics. Para TLS/autenticación se requiere configurar scheme y las opciones de acceso correspondientes.
Los servicios deben permitir acceso desde ese servidor; los puertos publicados únicamente en 127.0.0.1 no son accesibles remotamente. localhost dentro del contenedor se refiere al propio contenedor.
Iniciar solo con compose.yaml:

    docker compose config --quiet
    docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml
    docker compose up -d

Para que Monitoring remoto consulte Prometheus, cambiar el enlace 127.0.0.1:9090:9090 por IP_PRIVADA_DEL_SERVIDOR:9090:9090, restringir el acceso en la red/firewall y configurar MONITORING_PROMETHEUS_URL con esa dirección privada. No publicar el puerto sin protección en Internet.

## 4. Verificar
Abrir http://127.0.0.1:9090/targets EN EL SERVIDOR: ambos targets deben aparecer UP. Consultar `up`. Revisar /alerts y:

    docker compose logs --tail 100 prometheus

Para acceder desde una laptop por SSH sin publicar la interfaz:

    ssh -L 19090:127.0.0.1:9090 usuario@servidor

Abrir http://127.0.0.1:19090/targets en la laptop.
La validación promtool comprueba sintaxis; targets UP comprueba la conectividad de recolección. Después verificar también que Monitoring devuelve métricas.

## Alcance y mantenimiento
Se copió la configuración local: scraping cada 5 segundos de Simulator y Prediction. No se añadieron Node Exporter ni cAdvisor; las métricas de nodos del simulador siguen siendo simuladas.
Las reglas incluidas evalúan indisponibilidad de Prediction y recomendaciones bloqueadas. Sin Alertmanager no envían notificaciones externas. Una regla sin series de entrada no demuestra que la función esté operativa.
El volumen conserva datos al recrear contenedores; la retención está fijada en 15 días. Dimensionar disco y respaldos según el volumen real. No usar down -v si se desean conservar históricos.
Después de editar prometheus.yml o alerts.yml, repetir promtool y reiniciar prometheus usando los mismos archivos Compose con los que se inició.
Este paquete no demuestra que el despliegue remoto ya funcione; las comprobaciones anteriores deben ejecutarse en destino.
