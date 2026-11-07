# Workloads Kubernetes y qué medir en Green AI

Workload significa una aplicación o trabajo ejecutado en Kubernetes. En el diagrama de Green AI, la caja Workloads Kubernetes representa cargas que se desea observar en el entorno real o experimental. No es una tabla, una base de datos ni un microservicio llamado literalmente Workloads.

## 1 Las dos interpretaciones que debes separar

En Kubernetes, nuestros propios microservicios serían workloads si se desplegaran allí. Pero el diagrama utiliza esa caja para resumir las aplicaciones y cargas observadas, distintas del generador sintético. Puede tratarse, por ejemplo, de una API de laboratorio, un proceso de análisis por lotes o un servicio sometido a peticiones de prueba.

El nombre de la caja no identifica todavía qué aplicaciones, namespaces y métricas se han acordado. Esa definición sigue pendiente. La flecha discontinua desde Prometheus indica un flujo futuro de recolección, no una conexión ya validada en el Compose.

## 2 Tipos de workload y cuándo se usan

| Recurso | Para qué sirve | Ejemplo propuesto |
| --- | --- | --- |
| Deployment | Mantener réplicas de una aplicación que sigue atendiendo | Monitoring o Gateway |
| StatefulSet | Administrar Pods con identidad estable y almacenamiento asociado | Componente con estado si su diseño lo requiere |
| DaemonSet | Ejecutar una copia en cada nodo elegible | Exporter de métricas del nodo |
| Job | Ejecutar una tarea hasta que finalice | Una simulación de duración finita |
| CronJob | Programar Jobs periódicos | Procesamiento nocturno de datos autorizado |

Los controladores administran Pods; no sustituyen la lógica de la aplicación. La elección depende de su ciclo de vida, no del lenguaje utilizado. Véase [workloads de Kubernetes](https://kubernetes.io/docs/concepts/workloads/).

Ejemplo de decisión: Monitoring debería seguir atendiendo consultas después de una hora, pero Simulator está diseñado para terminar tras su duración. Usar un Deployment para ese Simulator puede reiniciar el contenedor al terminar y crear un run distinto. Un Job representa mejor una ejecución finita.

Un Job también puede repetir trabajo por fallos. La aplicación debe identificar ejecuciones e intentos y evitar tratar una repetición como un resultado nuevo indistinguible. `backoffLimit` controla reintentos del Job; no transforma automáticamente el trabajo en una operación de exactamente una ejecución. Véase [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/).

## 3 Ejemplo de Job para estudiar

El siguiente YAML es un ejemplo parcial sin aplicar. Presupone una imagen publicada y un namespace existente. No proporciona persistencia de runs ni recolección automática de Prometheus; esas piezas se diseñan aparte.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: simulacion-clase-01
  namespace: green-ai
spec:
  backoffLimit: 0
  template:
    metadata:
      labels:
        app: simulator
        experiment: clase-01
    spec:
      restartPolicy: Never
      containers:
        - name: simulator
          image: registry.example.com/green-ai-simulator:ejemplo
          args:
            - run
            - --inventory
            - configs/inventory.synthetic.json
            - --scenario
            - configs/scenarios/high.json
            - --seed
            - "42"
            - --duration-seconds
            - "3600"
            - --tick-seconds
            - "5"
            - --mode
            - realtime
            - --output-dir
            - /app/runs
            - --host
            - 0.0.0.0
            - --port
            - "8000"
          ports:
            - name: metrics
              containerPort: 8000
```

`args` reemplaza los argumentos predeterminados manteniendo la entrada de la imagen. `restartPolicy: Never` y `backoffLimit: 0` evitan reintentos automáticos en este ejemplo de estudio. El directorio de salida permanece local al contenedor sin un volumen añadido.

No se incluyó un Service porque exponer un puerto declarado no resuelve por sí solo cómo Prometheus descubrirá el Pod del Job. En una instalación real se acordaría descubrimiento de Pods/endpoints o recursos del operador de Prometheus, si ese operador existe. Un ServiceMonitor no es un recurso disponible por defecto en cualquier Kubernetes.

## 4 Una aplicación puede existir sin ser observable

Kubernetes puede ejecutar una API sin saber cuántas operaciones de negocio termina o cuánto tardan. Para medirlo, la aplicación debe instrumentarse y exponer métricas, o debe existir un mecanismo de observación apropiado.

Ejemplo didáctico: una API recibe peticiones de clasificación de documentos. El generador de carga envía cien solicitudes por segundo. La API registra solicitudes, errores y tiempos de respuesta. Un exporter de nodo registra recursos del sistema. Prometheus recolecta ambas fuentes. Son mediciones relacionadas, pero ninguna reemplaza a la otra.

Generar números sintéticos en Simulator no es lo mismo que enviar esas cien solicitudes a la API. Un generador de tráfico real sería otro componente o adaptador, actualmente no implementado en Simulator.

## 5 Las fuentes responden preguntas diferentes

| Pregunta | Fuente que habría que disponer |
| --- | --- |
| ¿Qué CPU y memoria utiliza un nodo? | Exporter del nodo con identidad validada |
| ¿Cuánto consume un contenedor? | Métricas del kubelet/runtime, según configuración del clúster |
| ¿Cuántas réplicas desea y tiene listas un Deployment? | Estado de Kubernetes, por ejemplo kube-state-metrics |
| ¿Cuál es la latencia o tasa de errores de una API? | Instrumentación de la aplicación |
| ¿Qué mide el proceso Java Monitoring? | Su Actuator/Micrometer |
| ¿Cuánta potencia consume físicamente el equipo? | Sensor o método de potencia validado |

Kube-state-metrics genera métricas sobre el estado de objetos consultando la API de Kubernetes. No es un medidor directo de CPU consumida ni produce latencia HTTP de negocio. Véase su [repositorio oficial](https://github.com/kubernetes/kube-state-metrics).

No atribuyas a `/actuator/prometheus` de Monitoring el consumo de todos los workloads. Es instrumentación de ese proceso. Además, el archivo `prometheus-demo.yml` actual solo recoge el exporter del Simulator.

## 6 Grupo A y Grupo B

El catálogo actual de Monitoring es Grupo A: CPU del nodo, memoria, recepción y transmisión de red y ocupación de filesystem. Aun desplegado en Kubernetes, seguiría ofreciendo esas cinco definiciones hasta que cambie su contrato.

El Grupo B documentado como pendiente incorpora métricas de workloads: solicitudes, throughput, concurrencia, latencia, errores y estados de Pods o réplicas. No basta con añadir un target a Prometheus: también deben definirse identificadores, fuentes, dimensiones, unidades y reglas de consulta en Monitoring.

Una secuencia de integración sería: elegir workload → instrumentarlo → comprobar scrape → acordar semántica → extender catálogo y OpenAPI → probar adaptador → integrar consumidores. No debe invertirse exponiendo un nombre de métrica sin saber qué significa.

## 7 Ejemplos de métricas de workload

**Solicitudes:** si el contador aumenta 6 000 durante sesenta segundos, la tasa sencilla es cien solicitudes/s. Cuenta llegadas HTTP; no necesariamente operaciones de negocio completadas.

**Throughput:** si se completan 4 800 tareas durante ese minuto, hay ochenta tareas/s. Una petición puede iniciar varias tareas, ninguna o una tarea diferida. Por eso hay que definir la relación con solicitudes.

**Concurrencia:** un gauge puede mostrar veinte operaciones en curso ahora. No son veinte operaciones por segundo: concurrencia es una cantidad simultánea.

**Errores:** si 120 de 6 000 solicitudes fallan con una definición acordada de error, el ratio es 0.02, es decir 2 %. El período, denominador y códigos incluidos deben coincidir.

**Latencia p95:** representa un umbral bajo el cual se sitúa aproximadamente el 95 % de las observaciones según la medición o estimación utilizada. No es el promedio. En el contrato propuesto se habla de histogramas y ventana de cinco minutos. No se deben promediar percentiles individuales de Pods como si fueran el percentil global; hay que acordar la agregación de distribuciones.

Estos cálculos son ejemplos didácticos del contrato futuro, no endpoints disponibles hoy.

## 8 Identidad y escalado

Para workloads, cluster y node no bastan. Harán falta dimensiones como namespace, workload y posiblemente Pod o servicio. Una petición pasa por un Pod, pero el usuario puede querer ver la aplicación completa.

Cuando se crean réplicas nuevas, cambia el conjunto de Pods. Por eso las agregaciones deben conservar identidad del workload y decidir cómo manejar reinicios, series nuevas y ausencias. Un request ID individual como etiqueta de métrica provocaría muchas series; la correlación de peticiones no debe confundirse con dimensiones de agregación.

Ejemplo: dos réplicas atienden 40 y 60 solicitudes/s. La tasa de aplicación puede ser 100 si las series cuentan operaciones disjuntas con la misma definición. Eso no autoriza a sumar porcentajes de CPU del nodo ni latencias p95.

## 9 Medir predecir y actuar son pasos separados

Un posible flujo futuro sería: obtener observaciones → prepararlas en Data Processing → solicitar predicción → evaluar una política → aplicar una acción autorizada. Hoy la cadena revisada no configura un controlador que escale réplicas o apague nodos basándose en predicciones.

Horizontal Pod Autoscaler, cuando se configura con sus fuentes y reglas, administra réplicas; no es sinónimo de Prediction ni aparece implementado en este proyecto. Tampoco reducir réplicas demuestra automáticamente ahorro energético: debe medirse el efecto y comprobar latencia, errores y demás criterios de servicio.

## 10 Ejercicio de exposición

Te preguntan: «Si Monitoring se ejecuta en Kubernetes, ¿ya monitorea Kubernetes?». Respuesta: «No necesariamente. Ejecutarse allí lo convierte en un workload. Observar otros workloads exige fuentes, instrumentación y contratos que aún faltan. El catálogo actual sigue centrado en nodos».

Te preguntan: «¿Workloads se conecta a Supabase?». Respuesta: «La caja no representa un cliente de BD definido. En el diagrama su relación es la recolección de Prometheus. Un workload de negocio podría necesitar una BD por su propio diseño, pero no se ha establecido ese acceso como parte de esta integración».

Referencias del proyecto: [diagrama general](../project-docs/diagrama.png), [contrato Monitoring](../green-ai-monitoring/docs/contrato-monitoring-v0.1.md) y [ensamblaje](../project-docs/ENSAMBLAJE-MICROSERVICIOS.md).
