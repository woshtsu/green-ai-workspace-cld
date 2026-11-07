# Métricas Prometheus y significado de los datos

Una API técnicamente correcta puede comunicar conclusiones equivocadas si confunde unidades o ausencia con cero. Esta guía explica la teoría necesaria para interpretar las cinco métricas que Monitoring publica.

## 1 Qué es una serie temporal

Una métrica expresa una magnitud, como bytes utilizados. Una muestra añade un instante y un valor. Una serie temporal reúne muestras de la misma identidad: por ejemplo, memoria de node-01 dentro de una ejecución concreta.

Las etiquetas identifican dimensiones. CPU necesita saber a qué nodo pertenece; red necesita además identificar la interfaz; almacenamiento necesita device, mountpoint y fstype. Dos números con el mismo nombre de métrica no pertenecen necesariamente a la misma serie.

El exporter del simulador publica `cluster="sim-run-<uuid>"`, `node="node-01"` y `origin="simulated"`. Prometheus añade etiquetas del target, entre ellas `instance`, que normalmente describe la dirección consultada. Un exporter puede representar muchos nodos: por eso la dirección del exporter no basta como identidad del equipo modelado.

## 2 Counter y gauge

Un counter acumula una cantidad: bytes transmitidos o segundos de CPU. Durante una ejecución normal aumenta; un reinicio puede hacerlo volver a un valor menor. El contador de red no dice directamente cuántos bytes se transmiten por segundo.

Un gauge representa un estado que puede subir o bajar: memoria disponible o espacio libre. En este simulador el espacio libre solo disminuye porque su modelo únicamente escribe; sigue siendo un gauge por el significado de la magnitud.

| Familia del exporter | Tipo | Unidad antes de consultar |
| --- | --- | --- |
| `node_cpu_seconds_total` | Counter | Segundos acumulados por CPU y modo |
| `node_network_receive_bytes_total` | Counter | Bytes acumulados recibidos |
| `node_network_transmit_bytes_total` | Counter | Bytes acumulados enviados |
| `node_memory_MemTotal_bytes` | Gauge | Bytes totales |
| `node_memory_MemAvailable_bytes` | Gauge | Bytes disponibles |
| `node_filesystem_size_bytes` | Gauge | Bytes de capacidad |
| `node_filesystem_free_bytes` | Gauge | Bytes libres |
| `node_filesystem_device_error` | Gauge | Indicador 0 o 1 |

## 3 Cómo aparece una tasa

Si un contador pasa de 1 000 000 a 1 600 000 bytes en diez segundos, su incremento es 600 000 bytes y la tasa sencilla es 60 000 bytes/s. La operación cambia la unidad: cantidad dividida entre tiempo.

Prometheus usa `rate(contador[1m])` para estimar la tasa media por segundo en una ventana de un minuto. La función contempla reinicios y extrapolación hacia los bordes; por eso no siempre coincide con una resta manual de dos muestras. Necesita muestras suficientes y se aplica a contadores. Véase la [referencia oficial de rate](https://prometheus.io/docs/prometheus/latest/querying/functions/#rate).

Si el contador vuelve de 1 600 000 a cero al reiniciar, eso no representa tráfico negativo. La interpretación de counter permite reconocer el reinicio. En el proyecto, cada nueva ejecución del simulador también recibe un cluster diferente para separar su identidad.

## 4 CPU y denominador

Monitoring utiliza esta idea:

```text
utilización = 1 − promedio de la tasa idle de las CPU lógicas
```

Si cuatro CPU tienen fracciones idle 0.10, 0.20, 0.30 y 0.40, su promedio idle es 0.25 y la utilización es 0.75. La API devuelve ratio 0.75; el frontend puede presentarlo como 75 % multiplicando por cien.

El denominador es la capacidad de todas las CPU lógicas del nodo. No es el límite de CPU de un pod ni el porcentaje asignado a un usuario. Si no aclaras el denominador, el porcentaje puede resultar ambiguo.

La fórmula cuenta como utilizado todo lo que no sea idle. Eso incluye iowait bajo esta definición. Además, promedia las CPU lógicas por igual. En el simulador todos los núcleos reciben la misma fracción de utilización, porque el estado agregado se distribuye uniformemente al exportar.

## 5 Memoria utilizada

La definición implementada es `MemTotal - MemAvailable`, expresada en bytes. La memoria disponible no es simplemente la completamente libre; en un sistema real puede contemplar memoria recuperable. La API conserva la definición del catálogo y no la cambia por `MemTotal - MemFree`.

Ejemplo: total 16 GiB y disponible 6 GiB implican 10 GiB utilizados. Un GiB son 1 073 741 824 bytes; un GB decimal son 1 000 000 000 bytes. El frontend puede elegir una presentación, pero debe indicar la unidad y no alterar el dato original.

El inventario sintético contiene 17 179 869 184 bytes para node-01, equivalentes a 16 GiB. Es una capacidad modelada; no certifica la memoria del computador donde corre Docker.

## 6 Red y almacenamiento

Las métricas de red devuelven bytes/s por interfaz. TX es transmisión; RX es recepción. La API conserva `device`, como eth0 o eth1. Sumar interfaces sin analizar la topología puede contar el mismo tráfico varias veces, por ejemplo en interfaces físicas y virtuales.

Almacenamiento devuelve `size - free` en bytes por filesystem. La API conserva `device`, `mountpoint` y `fstype`. No calcula porcentaje ocupado ni tasa de escritura. El simulador sí usa una tasa de escritura para actualizar el estado, pero la métrica pública de Monitoring es ocupación resultante.

Se permiten ext2, ext3, ext4, xfs, btrfs y zfs. Se excluyen los montajes /proc, /sys, /dev y /run y sus descendientes. Además se exige `device_error=0`. Un filesystem descartado no se convierte en un cero de ocupación.

## 7 Quién consulta a quién

Un exporter publica el estado en un endpoint HTTP de métricas. Prometheus actúa como cliente, consulta ese endpoint periódicamente y almacena las muestras. Esta recolección se denomina scrape y utiliza un modelo pull.

Monitoring no scrapea al Simulator: usa la API de consultas de Prometheus. Para `current`, el adaptador llama `/api/v1/query`; para `history`, llama `/api/v1/query_range`. Prometheus evalúa la expresión y devuelve un vector o una matriz, respectivamente. Monitoring traduce ese resultado a su contrato.

El archivo `prometheus-demo.yml` configura un scrape cada cinco segundos de `simulator:8000`. No contiene un target para `/actuator/prometheus` de Monitoring o Gateway. Que esos endpoints existan no significa que el Prometheus de esta demo ya los esté recolectando.

## 8 Los cuatro tiempos que debes diferenciar

| Concepto | Ejemplo de la demo | Significado |
| --- | --- | --- |
| Tick lógico | 5 s | Cuánto avanza el estado del simulador |
| Intervalo de scrape | 5 s | Cada cuánto Prometheus intenta leer el exporter |
| Ventana de rate | 60 s | Tramo observado para calcular cada tasa |
| Paso de history | 15 s por defecto | Separación entre instantes de evaluación solicitados |

Cambiar `stepSeconds` a 30 no cambia la ventana de rate a treinta segundos. Devuelve evaluaciones más separadas, cada una basada en la ventana configurada de sesenta segundos.

Un histórico desde 12:00:00 hasta 12:01:00 con paso 15 tiene cinco posiciones: 00, 15, 30, 45 y 60. La fórmula es `floor((end-start)/step)+1`. Si el extremo final no cae en la rejilla, no se inventa un punto extra para alcanzarlo.

Los timestamps de la API son instantes de evaluación. Para gauges, Prometheus puede reutilizar una muestra reciente; el cliente configura `lookback_delta=30s`. Por tanto, una rejilla completa no prueba que todos los scrapes hayan sido exitosos.

## 9 Procedencia y calidad

`source` describe el mecanismo que entregó los datos: `fixture` o `prometheus`. `origin` expresa su naturaleza: `observed`, `simulated`, `estimated` o `unknown`.

La combinación `source=prometheus` y `origin=simulated` es correcta: Prometheus almacena datos producidos por el simulador. Utilizar Prometheus no transforma datos ficticios en mediciones reales. Un inventario observado tampoco convierte una salida modelada en observada.

| Resultado | Interpretación correcta |
| --- | --- |
| `value=0`, `quality=valid` | El valor numérico es cero |
| `value=null`, `quality=missing` | Falta una muestra en una serie identificada |
| `value=null`, `quality=non_finite` | La fuente produjo NaN o infinito |
| `dataStatus=no_data`, `series=[]` | La consulta tuvo éxito pero no devolvió series |
| HTTP 503 | No se pudo disponer de la fuente o está saturada |

`partial` indica huecos, datos no finitos o advertencias. `complete` indica cobertura de la rejilla retornada sin esos problemas. Ninguno certifica verdad física ni presencia de todos los equipos: Monitoring no posee un inventario autoritativo para construir series de recursos totalmente ausentes.

## 10 Cardinalidad y presupuesto

Cardinalidad es el número de series distintas. Si cada nodo tiene dos interfaces, una consulta de recepción sobre cincuenta nodos puede producir cien series. Cada etiqueta que varía puede aumentar ese número.

Monitoring permite como máximo cien series y diez mil puntos totales. Un día con paso quince produce 5 761 posiciones por serie; dos series producirían 11 522 y superarían el límite aunque el rango de un día sea válido. La solución es filtrar, aumentar el paso o dividir el período según el caso.

No se recortan silenciosamente los resultados. Rechazar una consulta excesiva permite al consumidor saber que no recibió una vista completa. Al dividir rangos recuerda que los extremos son inclusivos para evitar duplicar muestras al unir resultados.

## 11 Qué significa Green AI en este alcance

CPU mide utilización; potencia se mide en watts; energía puede expresarse en joules o kWh. Con potencia constante, energía = potencia × tiempo. Con potencia variable habría que integrar en el tiempo. El proyecto actual no dispone de una medición o modelo de potencia validado para hacer esa conversión.

Estas métricas preparan una base de observación para análisis posteriores. No demuestran ahorro energético ni entrenan un modelo predictivo. Una defensa rigurosa presenta esa separación como parte del método experimental.

## Referencias del código

- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/domain/MetricCatalog.java`
- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/domain/MetricData.java`
- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/out/prometheus/PrometheusQueryBuilder.java`
- `green-ai-monitoring/docs/contrato-monitoring-v0.1.md`
- `prometheus-demo.yml`
