# Integración y demostración de Green AI

La demostración debe comprobar el recorrido completo y explicar qué significa cada resultado. Esta guía contiene un procedimiento propuesto para PowerShell. Se validó la combinación de archivos con `docker compose config`; no se ejecutaron el arranque ni las consultas funcionales. La demostración requiere Docker disponible, motor Linux y puertos libres.

## 1 Imagen contenedor y Compose

Una imagen empaqueta lo necesario para ejecutar una aplicación. Un contenedor es un proceso aislado creado desde esa imagen. Un Dockerfile describe su construcción. Compose reúne servicios, red, variables, puertos y montajes.

Los Dockerfiles Java usan una etapa de compilación y otra con JRE 21 para ejecutar el JAR. La etapa final utiliza un usuario sin privilegios. Simulator usa Python 3.12, instala su paquete y ejecuta la CLI con un usuario propio. Sus dependencias del Dockerfile no se instalan a partir de `uv.lock`, por lo que no debe afirmarse que esa imagen reproduce estrictamente el lock local.

`EXPOSE` documenta un puerto de la imagen; la publicación al host la determina Compose o la opción `-p`. La forma `8081:8081` significa puerto del host a puerto del contenedor.

## 2 Red interna y puertos

| Servicio | Desde el host en esta demo | Desde otro contenedor de Compose |
| --- | --- | --- |
| Simulator | `http://127.0.0.1:8000/metrics` | `http://simulator:8000/metrics` |
| Prometheus | `http://127.0.0.1:9090` | `http://prometheus:9090` |
| Monitoring | `http://127.0.0.1:8080` | `http://monitoring:8080` |
| Gateway | `http://127.0.0.1:8081` | `http://gateway:8081` |

Dentro del contenedor Monitoring, localhost apunta al propio Monitoring, no a Prometheus. Compose permite resolver nombres de servicios por su red. La dirección del navegador, en cambio, utiliza los puertos publicados en el host.

`depends_on` en este Compose ordena el arranque, pero no establece comprobaciones de disponibilidad funcional con healthchecks. Al inicio puede haber procesos arrancados y fuentes todavía no listas.

## 3 Corregir la identidad para la demostración

El exporter comparte un endpoint para varios nodos. Prometheus añade `instance=simulator:8000` a todos ellos. Monitoring usa por defecto `instance` como recurso, y el Compose actual no cambia esa propiedad.

La consecuencia inferida del código es relevante: CPU puede promediar núcleos de distintos nodos dentro de una misma identidad; memoria puede generar identidades duplicadas y terminar en 502. Cambiar el default-cluster a sim-lab no arregla la identidad del nodo.

El archivo adicional incluido junto a esta guía configura `MONITORING_PROMETHEUS_INSTANCE_LABEL=node`. Añade solo esa variable y deja intacto el Compose original. Comprueba la configuración combinada antes de iniciar:

```powershell
Set-Location 'C:\Practicas\202620\TallerProyectos\green-ai-workspace'
docker compose -f docker-compose.yml -f guia-exposicion/compose.exposicion.yaml config
```

La etiqueta cluster real seguirá siendo `sim-run-<uuid>`, porque el exporter la aporta y prevalece sobre el valor default. No filtres por sim-lab esperando encontrar esos datos.

## 4 Arrancar la demo

Si usas frontend, establece su origen exacto antes de ejecutar. Este ejemplo coincide con el valor habitual del Compose:

```powershell
$env:GATEWAY_CORS_ALLOWED_ORIGIN = 'http://127.0.0.1:3001'
docker compose -f docker-compose.yml -f guia-exposicion/compose.exposicion.yaml up --build -d
docker compose -f docker-compose.yml -f guia-exposicion/compose.exposicion.yaml ps
```

La construcción puede requerir acceso a registros de imágenes y repositorios de dependencias. El comando puede iniciar o recrear servicios del proyecto Compose; úsalo en tu entorno de demostración. No incluye el frontend ni lo arranca: el Compose revisado contiene cuatro servicios.

Comprueba logs cuando un servicio no permanezca activo:

```powershell
docker compose logs --tail 80 simulator prometheus monitoring gateway
```

No esperes exactamente 85 % de CPU desde el primer instante: hay ruido, estado inicial y ventana de cálculo. Para la presentación deja aproximadamente un minuto o algo más de recolección antes de mostrar tasas estabilizadas.

## 5 Comprobar cada salto

Primero consulta el exporter y observa familias y etiquetas:

```powershell
(Invoke-WebRequest 'http://127.0.0.1:8000/metrics').Content
```

Busca `node_cpu_seconds_total`, `node`, `cluster` y `origin`. El endpoint también puede contener instrumentación propia del proceso Python; no toda línea representa un recurso simulado.

Después revisa los targets de Prometheus:

```powershell
$targets = Invoke-RestMethod 'http://127.0.0.1:9090/api/v1/targets'
$targets.data.activeTargets | Select-Object health,lastError,scrapeUrl
```

Un target saludable indica que el scrape funciona. No prueba que el mapeo de Monitoring esté bien configurado. Comprueba una métrica de origen:

```powershell
$query = [uri]::EscapeDataString('node_memory_MemTotal_bytes')
$raw = Invoke-RestMethod "http://127.0.0.1:9090/api/v1/query?query=$query"
$raw.data.result | ConvertTo-Json -Depth 8
```

Estos accesos directos son comprobaciones administrativas de la demo. La aplicación frontend debe consumir Gateway.

## 6 Mostrar catálogo y datos actuales

```powershell
$base = 'http://127.0.0.1:8081/api/monitoring/v1/metrics'
Invoke-RestMethod "$base/catalog" | Format-Table id,unit,aggregation,windowSeconds
$current = Invoke-RestMethod "$base/current?metric=node.memory.used"
$current | ConvertTo-Json -Depth 12
```

Comprueba que los recursos devueltos incluyen node-01 y node-02, con `source=prometheus` y `origin=simulated`. Si no hay series, no continúes usando un índice de lista vacío: resuelve antes el scrape, la disponibilidad o el etiquetado.

Obtén la identidad real desde la respuesta. No escribas un UUID supuesto en la consulta:

```powershell
if ($current.series.Count -eq 0) { throw 'La consulta no devolvió series; revisar la fuente.' }
$cluster = $current.series[0].resource.cluster
$node = $current.series[0].resource.id
$clusterParam = [uri]::EscapeDataString($cluster)
$nodeParam = [uri]::EscapeDataString($node)
Invoke-RestMethod "$base/current?metric=node.cpu.utilization&cluster=$clusterParam&resourceId=$nodeParam" |
    ConvertTo-Json -Depth 12
```

Explica que la unidad ratio obliga a multiplicar por cien únicamente al presentar un porcentaje.

## 7 Mostrar un histórico reciente

El formato siguiente genera timestamps UTC de segundos enteros y un final en el pasado. Un intervalo corto evita superar el presupuesto:

```powershell
$endTime = [DateTimeOffset]::UtcNow.AddSeconds(-5)
$end = $endTime.ToString("yyyy-MM-dd'T'HH:mm:ss'Z'")
$start = $endTime.AddMinutes(-2).ToString("yyyy-MM-dd'T'HH:mm:ss'Z'")
$historyUrl = "$base/history?metric=node.memory.used&cluster=$clusterParam&resourceId=$nodeParam&start=$start&end=$end&stepSeconds=15"
Invoke-RestMethod $historyUrl | ConvertTo-Json -Depth 12
```

Si la simulación empezó hace menos de dos minutos, parte del intervalo precede sus datos. Eso puede generar huecos y `partial`. No es motivo para rellenar con cero.

## 8 Mostrar una validación controlada

Solicita un identificador no registrado para explicar la lista permitida:

```powershell
try {
    Invoke-RestMethod "$base/current?metric=node.energy"
} catch {
    $_.ErrorDetails.Message
}
```

Se espera un 400 de Monitoring porque esa métrica no pertenece al catálogo. No la presentes como una caída del sistema. La operación fue rechazada según el contrato.

Para comprobar salud del proceso:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8081/actuator/health/readiness'
Invoke-RestMethod 'http://127.0.0.1:8080/actuator/health/readiness'
```

Una respuesta UP no sustituye las verificaciones funcionales anteriores.

## 9 Alternativa de estudio sin Prometheus

Puedes estudiar el contrato de Monitoring usando fixture. No ejecutes esta alternativa simultáneamente con un contenedor ocupando 8080.

```powershell
Set-Location 'C:\Practicas\202620\TallerProyectos\green-ai-workspace\green-ai-monitoring'
.\mvnw.cmd spring-boot:run '-Dspring-boot.run.profiles=fixture' '-Dspring-boot.run.arguments=--server.address=127.0.0.1'
```

En otra terminal consulta el catálogo o current por la API interna. Aquí se esperan `source=fixture`, `origin=simulated` y cluster fixture-lab. Esta alternativa demuestra el contrato y las reglas; no la presentes como integración con Simulator y Prometheus.

## 10 Diagnóstico por síntomas

| Síntoma | Qué revisar primero |
| --- | --- |
| Conexión rechazada en 8081 | Gateway activo y puerto publicado |
| 404 en Gateway | Ruta exacta y método GET |
| 400 | Métrica, parámetros repetidos, fechas, recurso y paso |
| 422 | Rango, número de series, puntos y tamaño |
| 502 en memoria con dos nodos | `instance-label=node` y ausencia de identidades duplicadas |
| 503 | URL de Prometheus, disponibilidad y saturación |
| 504 | Tiempo de respuesta de la fuente y carga |
| `no_data` | Target, etiquetas, filtro cluster, calentamiento o fin de simulación |
| PowerShell funciona y navegador falla | Origen CORS exacto y preflight |
| Aparece fixture en vez de prometheus | Perfil fixture activo |

El código HTTP local del Gateway puede diferir del de un problema generado por Monitoring. Inspecciona cuerpo y logs antes de atribuir todos los fallos a Prometheus.

## 11 Conservar evidencia y detener

El Compose no declara un volumen de datos de Prometheus ni un montaje de salida para runs del Simulator. No hay una política explícita de persistencia histórica que debas dar por garantizada al recrear contenedores. Exporta la evidencia relevante antes de cambiar el entorno.

Para finalizar los procesos sin pedir eliminación de volúmenes:

```powershell
Set-Location 'C:\Practicas\202620\TallerProyectos\green-ai-workspace'
docker compose -f docker-compose.yml -f guia-exposicion/compose.exposicion.yaml stop
```

Anota fecha, configuración, semilla, revisión de código y consultas usadas. Distingue pruebas ejecutadas de procedimientos preparados. Tener un guion no equivale a tener un resultado de ejecución.

## Referencias locales

- `docker-compose.yml` y `prometheus-demo.yml` de la raíz.
- Los tres archivos `Dockerfile` de los servicios.
- `green-ai-monitoring/docs/integracion-simulator.md`
- [Configuración adicional para la exposición](compose.exposicion.yaml)
