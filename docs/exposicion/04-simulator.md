# Simulator y su modelo matemático

Simulator genera el estado de equipos ficticios mediante reglas explícitas. Sirve para ensayar la cadena de métricas sin depender de equipos reales. No genera carga de CPU equivalente en el host, no crea máquinas virtuales y no ejecuta un modelo de inteligencia artificial.

## 1 Python mínimo para leer el proyecto

En Python la indentación delimita bloques. `def` define funciones; `class` define clases. Un diccionario asocia claves con valores y se parece al uso de `Map` en Java. Las anotaciones como `seed: int` describen tipos esperados, pero no validan automáticamente todos los valores en runtime.

`@dataclass(frozen=True)` genera métodos habituales para clases de datos e impide reasignar sus atributos normalmente. No congela recursivamente los diccionarios y listas contenidos. En el motor se construyen nuevos estados en cada paso; el uso de frozen por sí solo no sería suficiente para garantizar esa disciplina. Consulta la [documentación de dataclasses](https://docs.python.org/3/library/dataclasses.html).

Los modelos principales son `Inventory`, `Node`, `Scenario` y `EngineState`. Cada estado de nodo agrupa CPU, memoria, red y filesystems. `ValueWithOrigin` acompaña una capacidad con unidad y procedencia.

## 2 Inventario escenario y estado

El inventario responde «qué recursos existen». El escenario responde «cómo se comportan». El estado responde «cómo están en este momento». Separarlos permite ejecutar distintos escenarios sobre el mismo inventario sin reescribir la lógica.

El inventario incluido tiene node-01 con cuatro CPU lógicas, 16 GiB, una interfaz y un filesystem de 50 GiB. Node-02 tiene ocho CPU lógicas, 32 GiB, dos interfaces y un filesystem de 100 GiB. Son capacidades sintéticas, no equipos descubiertos automáticamente.

El archivo `high.json` configura CPU base 0.85, memoria base 0.70, transmisión base 50 000 000 bytes/s, recepción base 45 000 000 bytes/s, escritura 1 048 576 bytes/s y factor de ruido 0.10.

Los valores de capacidad distinguen `synthetic_fixture`, `observed` y `modeling_assumption` como vocabulario de procedencia de entradas. Esto no es el mismo enum de salida de Monitoring. El exporter declara siempre `origin=simulated` para sus resultados.

## 3 Flujo de ejecución

```text
CLI → parseo JSON → validación → RunLogger → estado inicial
                                             ↓
                              compute_next_state en cada tick
                                             ↓
                                  JSONL y exporter realtime
```

La CLI define `validate` y `run` con `argparse`. `validate` lee inventario y escenario y ejecuta comprobaciones. `run` llama a `run_simulation`, que coordina archivos, reloj, señales y exposición.

El dominio importa herramientas de la biblioteca estándar como dataclasses y hashlib. El exporter importa prometheus-client; el registro de ejecuciones usa archivos. `runner.py` ensambla adaptadores concretos. Esta implementación conserva un dominio independiente, aunque la capa de aplicación sí conoce adaptadores.

## 4 Determinismo semilla y ruido

Determinismo significa que entradas iguales producen los mismos estados lógicos. `derive_noise` construye una clave con versión v1, semilla, tiempo lógico, nodo y recurso. Calcula SHA-256, toma los primeros cuatro bytes como entero y lo transforma al intervalo de −1 a 1:

```text
ruido = 2 × entero / (2^32 − 1) − 1
```

Aquí el hash se usa para obtener una perturbación reproducible, no para cifrar datos. La clave incluye el recurso para que CPU, memoria y cada interfaz tengan perturbaciones diferenciadas. La función no depende de una secuencia global de llamadas a random.

La misma semilla por sí sola no basta: inventario, escenario, tick, duración y versión del algoritmo deben coincidir. El tamaño del paso afecta la integración, por lo que cambiar de un tick de uno a cinco segundos puede cambiar la trayectoria aunque se conserve la semilla.

Dos ejecuciones repetidas tienen UUID y fechas de manifiesto distintos. También los timestamps de scrape pueden variar. La garantía que se puede defender corresponde a los estados lógicos con las mismas entradas, no a que todos los archivos y consultas Prometheus sean idénticos byte por byte.

## 5 CPU paso a paso

El motor calcula `u = clamp(base_cpu + ruido × noise_factor, 0, 1)`. Clamp recorta el resultado para que permanezca entre cero y uno.

Después distribuye el tiempo acumulado entre user e idle:

```text
segundos totales de CPU = dt × número de CPU lógicas
incremento user = segundos totales × u
incremento idle = segundos totales × (1 − u)
```

Ejemplo didáctico: cuatro CPU, paso cinco segundos, base 0.85, ruido 0.20 y factor 0.10 dan u=0.87. Hay veinte segundos de CPU disponibles; user aumenta 17.4 e idle 2.6. El tiempo de pared avanzó cinco segundos, pero hay cuatro CPU trabajando en paralelo.

El exporter divide los acumulados entre el número de núcleos y publica una serie por CPU y modo. Cada núcleo aumenta 4.35 segundos user y 0.65 idle en ese paso. El modelo distribuye carga uniformemente; no representa afinidad, procesos, instrucciones o núcleos heterogéneos.

## 6 Memoria red y disco

Memoria usa `u = clamp(base_memory + ruido × factor, 0, 1)`, calcula `used = int(total × u)` y `available = total - used`. Es un estado absoluto en cada tick, no una suma de todas las asignaciones anteriores.

En red la perturbación es relativa a la tasa base:

```text
tasa = base + ruido × base × factor
tasa acotada = clamp(tasa, 0, capacidad de la interfaz)
nuevo contador = contador anterior + int(tasa acotada × dt)
```

Con base TX de 50 000 000, ruido 0.20 y factor 0.10, la tasa es 51 000 000 bytes/s. Un paso de cinco segundos suma 255 000 000 bytes. Cada interfaz usa la tasa base; no se reparte un presupuesto total del nodo entre interfaces. RX y TX se limitan por separado.

Disco calcula una tasa de escritura no negativa, obtiene bytes escritos y reduce el espacio libre sin bajar de cero. Comienza completamente libre. No modela borrados, lecturas, latencia, IOPS, caché o desgaste. El indicador de error generado por esta evolución es falso. La tasa de escritura se convierte en ocupación; no se exporta como una métrica pública adicional de Monitoring.

Observa que CPU y memoria reciben una perturbación absoluta de la fracción, mientras que red y disco reciben una perturbación proporcional a su tasa. Con factor 0.10, CPU base 0.85 puede variar entre 0.75 y 0.95; no solo un diez por ciento relativo de 0.85.

## 7 Tiempo lógico offline y realtime

El estado inicial tiene tiempo lógico cero, contadores cero, memoria completamente disponible y discos libres. Se registra antes del primer avance. Con duración sesenta y paso cinco, hay doce avances y trece snapshots contando el inicial.

Offline calcula esos pasos sin esperar su duración real. Produce archivos locales y no arranca el exporter. No es un mecanismo para cargar automáticamente ese histórico en Prometheus.

Realtime utiliza `time.monotonic()` para programar el siguiente instante y espera aproximadamente `tick_seconds` entre avances. Un reloj monotónico es apropiado para duraciones porque no depende de reajustes del reloj civil. El objetivo es avanzar a ritmo 1x; si el proceso se retrasa, el bucle continúa intentando recuperar la programación. No es un sistema de tiempo real con garantías estrictas.

Prometheus asigna timestamps de recolección al estado publicado. Exportar contadores acelerados y calcular rate contra segundos reales alteraría la interpretación. Por eso offline y realtime tienen propósitos diferentes.

## 8 Exporter y acceso concurrente

`SimulatorCollector` recibe el inventario y UUID, guarda el último estado y produce familias compatibles con los nombres usados por Monitoring. Cada ejecución utiliza `cluster=sim-run-<uuid>`; no utiliza directamente el nombre de clúster del inventario como identidad externa.

El bucle puede actualizar el estado mientras un hilo HTTP atiende un scrape. Un lock protege la referencia al snapshot. `collect` toma esa referencia bajo bloqueo y luego construye las métricas. El motor crea nuevos snapshots, en vez de modificar progresivamente el mismo mientras otro hilo lo lee.

Al llegar a la duración programada se desregistra el collector y el proceso finaliza. El histórico ya recolectado puede seguir disponible en Prometheus, pero deja de haber una fuente viva de datos actuales.

## 9 Persistencia local

Cada ejecución crea `runs/run-<uuid>/manifest.json` y `samples.jsonl`. JSONL contiene un objeto JSON por línea, de modo que se pueden escribir snapshots sucesivos sin reconstruir una gran lista completa.

El manifiesto guarda UUID, modo, semilla, duración, tick, rutas de entradas, estado, tiempos UTC, causa de parada y bytes escritos. Se escribe primero un archivo temporal y después se reemplaza el manifiesto. Esto reduce la posibilidad de dejar un manifiesto parcialmente escrito; no debe presentarse como una transacción de base de datos ni una garantía absoluta frente a todo fallo.

Las entradas se registran por ruta. El código actual no copia automáticamente sus contenidos ni guarda sus hashes; conservar solo el manifiesto no basta para reproducir si esos JSON se modifican después. Para un experimento defendible conserva también inventario, escenario y revisión de código.

El guardado controla un umbral aproximado de 100 MiB. Comprueba el acumulado antes de escribir y utiliza `>`; una línea puede rebasar el umbral antes de que la siguiente escritura sea rechazada. No es un techo exacto de bytes.

## 10 Validaciones y límites actuales

El inventario valida versión, nombres de nodos, duplicados, capacidades positivas y unidades; limita cien nodos, mil CPU totales, diez interfaces y veinte filesystems por nodo. El escenario comprueba rangos de utilización y ruido y tasas no negativas. El runner exige tick positivo y que duración sea múltiplo del tick.

No todas las restricciones imaginables están implementadas: el runner no rechaza expresamente una duración cero o negativa, y una anotación `Literal` no garantiza que el parser valide sus valores de origen. Esto no invalida los ejemplos válidos suministrados, pero impide afirmar que la validación cubre cualquier entrada arbitraria.

El árbol revisado no presenta una suite de tests del simulador equivalente a la de Monitoring. Para defender reproducibilidad conviene demostrarla comparando snapshots, no atribuirle una cobertura que no se ha evidenciado.

## 11 Explicación oral breve

«El simulador combina inventario, escenario, semilla y reloj lógico para generar snapshots reproducibles. Calcula contadores consistentes de CPU y red, y estados de memoria y disco. Guarda la ejecución en archivos y, en modo realtime, expone el estado para que Prometheus lo recolecte. Todos los resultados se identifican como simulados y no representan carga física aplicada al laboratorio».

## Archivos de referencia

- `green-ai-simulator/src/green_ai_simulator/domain/engine.py`
- `green-ai-simulator/src/green_ai_simulator/domain/inventory.py`
- `green-ai-simulator/src/green_ai_simulator/domain/scenario.py`
- `green-ai-simulator/src/green_ai_simulator/application/runner.py`
- `green-ai-simulator/src/green_ai_simulator/adapters/prometheus/exporter.py`
- `green-ai-simulator/src/green_ai_simulator/adapters/persistence/run_logger.py`
- `green-ai-simulator/configs/inventory.synthetic.json` y `configs/scenarios/high.json`
