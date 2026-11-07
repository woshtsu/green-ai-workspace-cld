# Ruta de estudio para exponer Green AI

Este material explica Simulator, Monitoring y API Gateway desde una base inicial de Java y Spring. El objetivo es que puedas describir qué hace cada componente, seguir una petición por el código, interpretar las métricas y defender las decisiones sin atribuir al proyecto capacidades que todavía no tiene.

Ampliación del 23 de septiembre de 2026: las guías 08 a 11 explican Docker, el despliegue previsto en Kubernetes, workloads y la relación directa de Supabase con los servicios. Incluyen ejemplos conceptuales y YAML ilustrativo; no constituyen un despliegue Kubernetes realizado. Toda la colección está en `guia-exposicion` en la raíz del workspace.

Fecha de revisión del código: 22 de septiembre de 2026. Los ejemplos numéricos son didácticos, salvo cuando se indica que proceden de la configuración del repositorio. Esta entrega es documental: no certifica una nueva ejecución de las aplicaciones ni de sus pruebas.

## Orden de lectura

| Documento | Qué aprenderás | Tiempo orientativo |
| --- | --- | --- |
| [01 Fundamentos de Java Spring y arquitectura](01-fundamentos-java-spring.md) | Interfaces, inyección, beans, MVC, arquitectura hexagonal y contratos | 45–60 min |
| [02 Métricas y Prometheus](02-metricas-prometheus.md) | Contadores, gauges, tasas, etiquetas, tiempo y calidad | 45–60 min |
| [03 Monitoring explicado desde el código](03-monitoring.md) | Capas, consultas, validaciones, errores y límites | 50–65 min |
| [04 Simulator y su modelo matemático](04-simulator.md) | Python mínimo, determinismo, fórmulas y exportación | 45–60 min |
| [05 API Gateway y programación reactiva](05-apigateway.md) | Rutas, filtros, WebFlux, CORS y correlación | 35–50 min |
| [06 Integración y demostración](06-integracion-demostracion.md) | Docker, configuración correcta, comprobaciones y diagnóstico | 45–60 min más práctica |
| [07 Guion y defensa del proyecto](07-guion-defensa.md) | Exposición de 15 minutos, preguntas y ejercicios resueltos | 45–60 min más ensayo |
| [08 Docker aplicado](08-docker-aplicado.md) | Imágenes, contenedores, Dockerfiles, red, configuración y persistencia reales | 35–45 min |
| [09 Kubernetes aplicado](09-kubernetes-aplicado.md) | Clúster, Pods, Deployment, Service, probes y ejemplo de Monitoring | 45–60 min |
| [10 Workloads Kubernetes](10-workloads-kubernetes.md) | Tipos de cargas, Job de simulación, instrumentación y Grupo B | 40–55 min |
| [11 Supabase y el diagrama](11-supabase-y-diagrama.md) | Accesos directos, tablas, consultas, permisos y flujos pendientes | 45–60 min |

Los tiempos son una propuesta de estudio, no una medición. Distribuye el contenido en varias sesiones. Al finalizar cada guía, intenta explicarla en voz alta sin leer; vuelve al código cuando no puedas justificar una afirmación.

## La idea central

Simulator produce estados sintéticos de equipos. Prometheus consulta periódicamente su exporter y almacena muestras. Monitoring consulta ese histórico mediante expresiones controladas y entrega un contrato JSON. API Gateway ofrece al frontend las rutas autorizadas para acceder a Monitoring.

```text
Datos:       Simulator → Prometheus → Monitoring → Gateway → Frontend
Peticiones:  Prometheus → Simulator
             Frontend → Gateway → Monitoring → Prometheus
```

Las dos líneas representan cosas diferentes: los datos viajan en las respuestas; la petición HTTP la inicia quien necesita leerlos. No hay una cadena de envíos automáticos desde Simulator hasta el navegador.

## Qué debes dominar antes de exponer

1. Explicar una interfaz y mostrar por qué `MonitoringService` depende de `MetricsSource`.
2. Diferenciar el contador de bytes de la tasa en bytes por segundo.
3. Identificar `cluster`, `node`, `instance`, `origin` y `source`.
4. Recorrer una consulta desde la URL pública hasta la respuesta de Prometheus.
5. Explicar `0`, `null`, `no_data` y un error 503 sin confundirlos.
6. Describir qué hace el simulador con la semilla y el tiempo lógico.
7. Mostrar cómo se reescribe una ruta del Gateway.
8. Reconocer que CPU no equivale a energía y que el PMV1 integrado sigue incompleto.
9. Diferenciar el contenedor que ejecuta Simulator de los nodos que el motor modela.
10. Explicar por qué una API continua y una simulación finita necesitan ciclos de vida distintos en Kubernetes.
11. Identificar qué métricas de workloads siguen pendientes y qué fuentes necesitarían.
12. Justificar por qué Monitoring no consulta Supabase y quién tendría acceso a hardware y logs.

## Observaciones importantes de la revisión

- El Compose del workspace necesita configurar `MONITORING_PROMETHEUS_INSTANCE_LABEL=node` para distinguir los equipos que comparte el exporter. La guía 06 proporciona un archivo de configuración adicional sin alterar el Compose original.
- Gateway y Monitoring tienen políticas distintas para `X-Request-Id`. Actualmente no puede prometerse un mismo identificador de extremo a extremo. La guía 05 explica la diferencia concreta.
- La implementación del simulador espera `tick_seconds` segundos entre pasos en modo realtime. No un segundo fijo por cada tick, como podría interpretarse de una frase del README.
- El escenario incluido es `high`. Los escenarios adicionales mencionados en planes no deben presentarse como archivos ya implementados.
- La documentación de base de datos describe un contexto de integración. No demuestra que estos tres componentes estén conectados a Supabase.

## Cómo comprobar las afirmaciones

Cada guía termina con archivos de referencia. Las rutas de código se indican desde la raíz del workspace; puedes encontrarlas con la búsqueda de archivos del editor. Las fuentes oficiales complementan la teoría. Las versiones que se describen como propias del proyecto proceden de sus POM y archivos de configuración, no de la versión más reciente de una página web.

Estudia con esta secuencia: concepto → ejemplo → código → explicación oral. Memorizar nombres de anotaciones sin entender el recorrido de los datos no basta para defender la arquitectura.
