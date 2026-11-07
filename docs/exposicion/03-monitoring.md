# Monitoring explicado desde el código

Monitoring ofrece un contrato controlado para consultar métricas. Su trabajo es seleccionar definiciones permitidas, validar consultas, obtener series de una fuente y comunicar unidades, identidad, calidad y errores. Prometheus resuelve las consultas sobre sus datos; Monitoring añade una interfaz propia del proyecto.

## 1 Organización de las capas

Dentro de `src/main/java/pe/edu/continental/greenai/monitoring`, el paquete `domain` contiene datos y reglas. `application` contiene el caso de uso y sus interfaces. `adapter/in/web` recibe HTTP. `adapter/out/prometheus` conecta con Prometheus; `adapter/out/fixture` produce datos de prueba; `adapter/out/support` añade límites y representa la falta de fuente. `configuration` construye y conecta todo.

El núcleo no importa Spring, HTTP o Jackson. Así sus reglas pueden probarse sin servidor web. Esta independencia no significa ausencia de framework en el proceso completo: los adaptadores sí necesitan Spring y la serialización necesita Jackson.

## 2 Cómo arranca y elige la fuente

`MonitoringConfiguration` registra un reloj UTC y una fuente limitada a cinco segundos y dieciséis consultas simultáneas. Si está activo el perfil `fixture`, construye `FixtureMetricsSource`. Si no está activo y existe URL Prometheus, conecta `PrometheusClient`, `PrometheusQueryBuilder` y `PrometheusResponseMapper`. Si falta URL, usa `UnavailableMetricsSource`.

El perfil fixture tiene prioridad aunque exista una URL. No se activa automáticamente si Prometheus falla. Esta regla evita mostrar una gráfica ficticia como si fuera continuidad de datos observados.

El catálogo no necesita consultar la fuente: vive en código. Por ello puede responder correctamente aunque `current` e `history` respondan 503 por falta de fuente. Esto también explica por qué un endpoint de salud puede estar UP y las consultas de datos fallar.

## 3 Recorrido de una consulta actual

Considera la petición interna:

```http
GET /api/v1/metrics/current?metric=node.memory.used&resourceType=node&resourceId=node-01
```

1. `RequestIdFilter` genera un identificador local y lo coloca en atributo de petición y cabecera de respuesta.
2. `MetricsController.current` recibe todos los parámetros mediante `MultiValueMap`. Una clave puede tener varias entradas, por eso este tipo permite detectar repeticiones.
3. `QueryParameters` comprueba claves permitidas, una entrada por clave, contenido no vacío y longitud máxima. Extrae `metric` y aplica `resourceType=node` por defecto.
4. `MonitoringService.current` captura el reloj una vez y lo reduce a segundos enteros. Busca la definición en `MetricCatalog` y construye un `MetricQuery` con inicio igual a fin.
5. `MetricQuery` valida el tipo de recurso y la sintaxis de los filtros. Su constructor impide representar determinadas consultas inválidas.
6. `BoundedMetricsSource` admite la operación si hay capacidad y ejecuta la fuente con un presupuesto de tiempo.
7. `PrometheusQueryBuilder` genera la resta entre memoria total y disponible con filtros controlados.
8. `PrometheusClient` envía GET a la API de Prometheus y limita plazo, tamaño y estructura básica de la respuesta.
9. `PrometheusResponseMapper` transforma el vector en series del dominio, con recurso, etiquetas, source y origin.
10. `MonitoringService.execute` verifica coherencia y normaliza muestras. `BoundedJson` serializa la respuesta, y el controlador devuelve HTTP 200 si todo termina correctamente.

El ejemplo supone `instance-label=node`. Con el valor predeterminado `instance`, el filtro `resourceId=node-01` se dirigiría a la etiqueta incorrecta para este exporter.

## 4 Recorrido de un histórico

`history` añade `start`, `end` y `stepSeconds`. La web exige timestamps con zona conocida y segundos enteros. Acepta formatos con Z o desplazamiento válido y los convierte a `Instant`, una posición en la línea temporal.

El servicio rechaza un final posterior al reloj actual. `MetricQuery` requiere inicio anterior a fin, paso entre 15 y 3600 segundos y rango no mayor a 24 horas. El cliente usa `/api/v1/query_range`, y el mapper espera `resultType=matrix` en vez de vector.

La aplicación construye la rejilla esperada. Para cada serie coloca sus muestras por timestamp en un mapa y recorre las posiciones. Cuando no encuentra una muestra, añade null con `missing`; cuando encuentra NaN o infinito, añade null con `non_finite`. No interpola.

Una serie que no aparece nunca no puede reconstruirse a partir del resultado vacío. El servicio no inventa que node-03 existe para entregarle una línea llena de huecos.

## 5 Qué comprueba cada clase

| Clase | Responsabilidad concreta |
| --- | --- |
| `MetricCatalog` | Lista cerrada de cinco métricas y sus definiciones |
| `MetricQuery` | Reglas de fechas, resolución, recurso e identidad de filtros |
| `QueryParameters` | Sintaxis y estructura de parámetros HTTP |
| `MonitoringService` | Tiempo actual, presupuesto, coherencia y normalización |
| `PrometheusQueryBuilder` | Expresiones permitidas a partir de filtros tipados |
| `PrometheusClient` | Red, plazos, tamaño y sobre de respuesta upstream |
| `PrometheusResponseMapper` | Conversión de vector o matrix a tipos del dominio |
| `BoundedMetricsSource` | Capacidad simultánea y espera acotada |
| `BoundedJson` | Tamaño del JSON antes de comprometer la respuesta |
| `ApiExceptionHandler` | Conversión de fallos Java a errores HTTP |

La repetición de algunas comprobaciones es deliberada: validar lo recibido por HTTP no permite confiar automáticamente en una respuesta externa. Una fuente puede devolver series duplicadas, timestamps fuera de rango o campos inesperados.

## 6 Por qué no recibe PromQL del cliente

El cliente selecciona un identificador como `node.cpu.utilization`. El servidor decide cómo se traduce. No se admiten parámetros `query`, `url` u otros filtros libres.

Esto reduce la superficie de consultas, estabiliza definiciones y ayuda a controlar coste y acceso. No equivale a autenticación. Un cliente que llega a estas rutas todavía puede solicitar operaciones permitidas porque no hay JWT o roles implementados.

El constructor de propiedades valida que la URL de Prometheus sea HTTP(S), tenga host y no incluya credenciales, query ni fragmento. La URL viene de configuración administrativa, no del usuario de la API. El cliente no sigue redirecciones ni hace reintentos automáticos.

## 7 Concurrencia timeout y saturación

Concurrencia significa cuántas consultas pueden estar activas a la vez. `BoundedMetricsSource` utiliza un `ThreadPoolExecutor` de dieciséis hilos de plataforma y una `SynchronousQueue`, que no almacena una cola de trabajos pendientes. Si todos los ejecutores están ocupados, se rechaza la nueva tarea y se comunica 503.

Un `Future` representa el resultado pendiente. `task.get` espera hasta el límite. Si vence, se intenta cancelar con interrupción y se devuelve 504. La interrupción es una solicitud cooperativa: no garantiza que todo código externo se detenga instantáneamente. El límite de hilos evita crecimiento ilimitado incluso ante una fuente que no coopera.

El cliente HTTP tiene un segundo de conexión y un plazo de tres segundos que abarca recepción del cuerpo. También solicita a Prometheus un timeout de evaluación de tres segundos. El envoltorio externo dispone de cinco segundos. Son límites en distintos niveles, no esperas que deban sumarse siempre.

`sendAsync` devuelve un futuro, pero luego se espera su resultado. Por tanto, Monitoring no se convierte en una aplicación enteramente reactiva por usar ese método. Su adaptador de entrada es MVC.

## 8 Límites y errores

| Restricción | Valor actual |
| --- | --- |
| Rango histórico | 24 horas |
| Series | 100 |
| Puntos totales de rejilla | 10 000 |
| Cuerpo de respuesta funcional | 5 MiB |
| Cuerpo leído de Prometheus | 5 MiB |
| Consultas simultáneas a la fuente | 16 sin cola |
| Presupuesto externo de fuente | 5 segundos |

El cliente pide `limit=101` a Prometheus para detectar que se superó el máximo de cien. El servicio vuelve a comprobar cardinalidad y puntos. No entrega las primeras cien series como si fueran todas.

Los fallos de negocio no conocen HTTP. `MonitoringFailure` contiene un código, y `ApiExceptionHandler` decide el estado de respuesta:

| HTTP | Código | Ejemplo |
| --- | --- | --- |
| 400 | `INVALID_QUERY` | Métrica inexistente o timestamp inválido |
| 422 | `QUERY_LIMIT_EXCEEDED` | Demasiados puntos o cuerpo demasiado grande |
| 502 | `UPSTREAM_INVALID_RESPONSE` | Identidades duplicadas o JSON incompatible |
| 503 | `METRICS_SOURCE_UNAVAILABLE` | Sin fuente, conexión fallida o saturación |
| 504 | `METRICS_SOURCE_TIMEOUT` | Espera agotada |

Los problemas usan `application/problem+json` con type, title, status, detail, instance, code y requestId. Los mensajes expuestos son controlados y no copian arbitrariamente trazas, PromQL o texto interno del upstream.

## 9 Cómo leer una respuesta

Este fragmento es didáctico y omite campos del sobre:

```json
{
  "metric": "node.cpu.utilization",
  "unit": "ratio",
  "dataStatus": "complete",
  "series": [{
    "resource": {"type": "node", "cluster": "sim-run-ejemplo", "id": "node-01"},
    "labels": {},
    "source": "prometheus",
    "origin": "simulated",
    "samples": [{"timestamp": "2026-09-22T15:00:00Z", "value": 0.85, "quality": "valid"}]
  }]
}
```

La lectura oral sería: «La utilización del nodo modelado node-01 es 85 % en el instante de evaluación. Es un dato sintético consultado desde Prometheus y su muestra es válida dentro del contrato». Evita decir que el equipo físico está al 85 %.

## 10 Pruebas y alcance de la evidencia

El repositorio contiene pruebas del servicio, consultas PromQL, mapeo, cliente HTTP, límites, configuración y contratos web. Los tests con fixture comprueban reglas de negocio; los tests de cliente utilizan respuestas controladas para provocar fallos de red o formato.

También existen scripts `Test-Java21.ps1` y `Test-Prometheus.ps1`. Su propósito es verificar en contenedores y probar integración con Prometheus y Node Exporter. Los resultados históricos se describen en `docs/validacion-incremento-1.md`; para afirmar que pasan en una presentación concreta debes disponer de evidencia de esa ejecución. Esta guía no los ha vuelto a ejecutar.

Tener tests de unidades no prueba el etiquetado del Compose del workspace. Tener Prometheus real en un test tampoco prueba que las muestras pertenezcan al laboratorio universitario. El contexto de la medición forma parte de la evidencia.

## 11 Explicación oral breve

«Monitoring separa el contrato web de la lógica de consultas. El controlador valida la petición, el servicio aplica las reglas y el adaptador consulta Prometheus con expresiones cerradas. La respuesta conserva identidad, unidad y procedencia, y distingue datos ausentes de fallos. Los límites de tiempo, tamaño y concurrencia evitan consultas sin control. No utiliza una base relacional ni reemplaza errores por datos ficticios».

## Referencias del código

Todos los nombres de clase de esta guía están bajo `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring` en los paquetes descritos. Revisa también:

- `green-ai-monitoring/src/main/resources/static/openapi/monitoring-v0.1.json`
- `green-ai-monitoring/src/test/java/pe/edu/continental/greenai/monitoring`
- `green-ai-monitoring/docs/validacion-incremento-1.md`
