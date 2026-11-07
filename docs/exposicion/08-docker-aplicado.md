# Docker aplicado a Green AI

Esta guía explica qué ejecuta Docker en el proyecto y cómo leer su configuración. Se basa en los Dockerfiles y el Compose revisados el 23 de septiembre de 2026. Describe configuración disponible, no una comprobación de que los contenedores estén ejecutándose ahora.

## 1 Imagen contenedor y máquina virtual

Una imagen es el paquete utilizado para crear un contenedor: incluye aplicación, dependencias y configuración de arranque. El contenedor es la ejecución aislada de ese paquete. Puedes crear varios contenedores desde una imagen, igual que puedes crear varios objetos de una clase, aunque la comparación no sea literal.

Los contenedores comparten el kernel del sistema donde se ejecutan; no son cada uno una máquina virtual completa. En un entorno Windows con contenedores Linux, debe existir un entorno Linux proporcionado por el motor correspondiente. No se inspeccionó aquí qué backend utiliza tu instalación. Véase [qué es un contenedor en Docker](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).

Docker resuelve principalmente el empaquetado y la ejecución. No convierte el programa Python en Java, no hace que un servicio conozca automáticamente la base de datos y no prueba que la aplicación sea correcta.

## 2 Los cuatro procesos del Compose

| Servicio | Qué ejecuta | Qué necesita |
| --- | --- | --- |
| simulator | CLI Python en modo realtime, exporter y registro local | Inventario y escenario incluidos en su imagen |
| prometheus | Servidor de recolección y consulta temporal | Configuración de scrape hacia simulator |
| monitoring | JAR Spring MVC | URL interna de Prometheus y etiquetas correctas |
| gateway | JAR Spring Cloud Gateway | URL interna de Monitoring y origen del frontend |

El Compose no incluye Supabase, Data Processing, Prediction, frontend ni un clúster Kubernetes. Los cuatro servicios tampoco son cuatro computadoras físicas: pueden compartir los recursos del mismo entorno Docker.

Hay tres medidas distintas de CPU: CPU real del contenedor Simulator, CPU sintética que ese proceso modela y CPU real del host que ejecuta los contenedores. El 85 % de high.json pertenece al modelo, no reserva ni consume por sí mismo el 85 % del host.

## 3 Cómo leer el Dockerfile de Monitoring

`FROM eclipse-temurin:21-jdk-jammy AS build` crea una etapa con herramientas de Java 21. `WORKDIR /workspace` establece el directorio de trabajo. `COPY` lleva wrapper, POM y fuentes del contexto de construcción a esa etapa. `RUN` ejecuta Maven para producir el JAR.

La segunda instrucción `FROM` inicia la etapa final con JRE. `COPY --from=build` toma únicamente el artefacto compilado. `USER 10001` selecciona un usuario sin privilegios y `ENTRYPOINT` ejecuta `java -jar /app/app.jar` cuando arranca el contenedor.

Esto separa herramientas de compilación y ejecución. Tu JDK local no es el que compila dentro de esa construcción. Gateway también tiene dos etapas, pero usa Maven de la imagen de construcción en vez del wrapper. En ambos casos `-DskipTests` omite ejecutar pruebas: una imagen construida correctamente no demuestra que los tests pasaron.

El contexto de construcción es la carpeta indicada por `build.context`; no es todo el disco del usuario. Los cambios de archivos copiados requieren construir una nueva imagen para incorporarse, salvo que haya montajes adicionales. Los fuentes Java no están montados en caliente en este Compose.

## 4 ENTRYPOINT CMD y command en Simulator

El Dockerfile define `ENTRYPOINT ["green-ai-simulator"]`. Su CMD aporta argumentos por defecto: ejecutar run, realtime, puerto 9090 y un tick de un segundo. Compose establece su propio `command` con puerto 8000, tick cinco y semilla 42.

En esta combinación, el comando efectivo es la entrada fija más los argumentos de Compose. Por eso el exporter del Compose escucha en 8000 aunque el Dockerfile documente `EXPOSE 9090`. EXPOSE no cambia el puerto elegido por el programa ni publica automáticamente una dirección en el host.

El programa debe escuchar en `0.0.0.0` dentro del contenedor para aceptar conexiones por sus interfaces de red. Escuchar únicamente en 127.0.0.1 lo limitaría al propio contenedor en esta configuración.

## 5 Direcciones puertos y DNS

Compose crea una red donde los servicios pueden resolverse por nombre. Al recrear un contenedor puede cambiar su dirección IP, por lo que los consumidores deben utilizar el nombre de servicio. La comunicación interna utiliza el puerto del contenedor, no el puerto publicado en el host. Véase [redes de Compose](https://docs.docker.com/compose/how-tos/networking/).

```text
Navegador en el host → 127.0.0.1:8081 → gateway:8081
gateway             → monitoring:8080
monitoring          → prometheus:9090
prometheus          → simulator:8000/metrics
```

`8081:8081` se lee host:contenedor. Si se cambiara a `18081:8081`, el navegador usaría 18081 y el proceso seguiría escuchando en 8081 dentro del contenedor. Ese cambio no obliga a modificar el puerto interno de otros servicios.

Localhost siempre debe interpretarse desde quien realiza la llamada. Desde Monitoring, localhost es su propio contenedor; desde el navegador es la máquina del navegador. El nombre `gateway` de la red de Compose no es necesariamente resoluble por el navegador del host.

## 6 Configuración externa y la identidad de nodos

El Compose suministra `MONITORING_PROMETHEUS_URL=http://prometheus:9090`. Spring la vincula con la propiedad de configuración correspondiente. Esto separa la dirección del servicio de la lógica del controlador.

El exporter representa varios nodos bajo un solo target. Es necesario configurar `MONITORING_PROMETHEUS_INSTANCE_LABEL=node` para que Monitoring distinga esos recursos. El archivo [compose.exposicion.yaml](compose.exposicion.yaml) complementa el Compose original con ese ajuste.

`MONITORING_PROMETHEUS_DEFAULT_CLUSTER=sim-lab` no reemplaza la etiqueta real `sim-run-<uuid>`. Default significa respaldo cuando falta el valor. Tampoco existe relación automática entre esa etiqueta y un clúster Kubernetes físico.

## 7 Archivos y persistencia

El montaje `./prometheus-demo.yml:/etc/prometheus/prometheus.yml` conecta un archivo del host con una ruta del contenedor. Es configuración de scrape, no almacenamiento del histórico.

Simulator escribe `runs` en su sistema de archivos; el Compose no monta esa salida en una carpeta del host. Prometheus tampoco tiene aquí un volumen de datos explícito administrado por el proyecto. No debes garantizar conservación de históricos al eliminar o recrear contenedores basándote solamente en este Compose.

Una evolución propuesta sería declarar almacenamiento persistente para el directorio de datos de Prometheus y para las ejecuciones del Simulator. Antes debe acordarse qué conservar, capacidad, permisos, retención y copias de seguridad. Un volumen no crea automáticamente backup y no resuelve la identidad de las ejecuciones.

## 8 Arranque y fallos

`depends_on` expresa dependencia de arranque, pero el archivo actual no define healthchecks con condiciones de servicio saludable. Prometheus puede estar iniciándose cuando Monitoring ya acepta peticiones. Además, las tasas necesitan muestras antes de producir resultados útiles.

El Compose no declara una política de reinicio para Simulator. Su CLI termina al completar la duración; esa salida es normal en un experimento finito. Cambiarlo a reinicio permanente alteraría el comportamiento al crear nuevas ejecuciones, algo que debe ser una decisión explícita.

La disponibilidad se comprueba en niveles: proceso activo, target recolectable, consulta válida y respuesta semánticamente correcta. Un contenedor visible en `ps` no acredita todos esos niveles.

## 9 Ejercicios con comandos

Desde la raíz del workspace, este comando solo interpreta y muestra configuración; no arranca servicios:

```powershell
docker compose -f docker-compose.yml -f guia-exposicion/compose.exposicion.yaml config
```

Para practicar el arranque usa el procedimiento de la [guía 06](06-integracion-demostracion.md), ya actualizado a la ubicación actual de esta carpeta. Comandos de inspección, si ya existe una ejecución:

```powershell
docker compose ps
docker compose logs --tail 60 monitoring
docker compose logs --tail 60 simulator
```

**Caso A:** Prometheus consulta `localhost:8000`. ¿A quién intenta llegar? A sí mismo. Debe usar simulator:8000 en esta red.

**Caso B:** Cambias high.json en el host y reinicias una imagen antigua. ¿Se incorpora necesariamente? No: el Dockerfile copia configs al construir. Reiniciar no reconstruye esos archivos.

**Caso C:** El exporter publica dos nodos, pero la API los mezcla. ¿Más memoria al contenedor lo arregla? No. Primero hay que revisar el mapeo de identidad node frente a instance.

## 10 Explicación para la exposición

«Docker empaqueta cada componente con su runtime y Compose conecta cuatro procesos mediante nombres internos. Los puertos publicados permiten acceder desde mi máquina. El despliegue actual es una demostración local: tiene configuración de scrape, pero no despliega Kubernetes ni Supabase y no define una política completa de persistencia. La reproducibilidad requiere también conservar las entradas y las versiones de las imágenes».

Fuentes del proyecto: `docker-compose.yml`, `prometheus-demo.yml` y los Dockerfiles de Monitoring, Gateway y Simulator.
