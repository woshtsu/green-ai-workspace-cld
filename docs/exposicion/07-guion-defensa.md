# Guion de exposición y defensa técnica

Esta guía ayuda a convertir la teoría en una explicación propia. Utiliza las respuestas como modelos de razonamiento, no como frases para memorizar sin entender. Una defensa sólida conecta problema, decisión, evidencia y límite.

## 1 Apertura de un minuto

«Esta parte de Green AI construye una cadena para generar, recolectar y consultar métricas de infraestructura. Simulator produce estados sintéticos reproducibles; Prometheus los recolecta; Monitoring los expone mediante un contrato con unidades y calidad; API Gateway ofrece las rutas para el frontend. La utilidad de esta separación es poder ensayar el flujo y cambiar fuentes sin mezclar generación, consulta y presentación. En este incremento se trabajan CPU, memoria, red y almacenamiento; todavía no se calcula energía ni se ejecutan predicciones».

## 2 Guion de quince minutos

| Tiempo | Contenido | Evidencia que puedes mostrar |
| --- | --- | --- |
| 0–1 min | Problema y alcance | Apertura y cinco métricas |
| 1–3 min | Arquitectura | Flujo de peticiones y de respuestas |
| 3–5 min | Simulator | Inventario, high.json y cálculo de un tick |
| 5–7 min | Prometheus | Counter frente a gauge, etiquetas y rate |
| 7–10 min | Monitoring | Controller, servicio, puerto y adaptador |
| 10–12 min | Gateway | Reescritura, origen CORS y límites |
| 12–14 min | Demostración | Catálogo, current e history |
| 14–15 min | Estado y siguientes pasos | Capacidades implementadas y pendientes |

Si no tienes conexión o los contenedores fallan, usa respuestas guardadas de una ejecución previa e indica su fecha y configuración. No presentes ejemplos didácticos como capturas en vivo.

## 3 Recorrido de código recomendado

Abre primero `MetricCatalog.java`: allí se ve exactamente qué se ofrece y en qué unidad. Después muestra `MetricsController.current`, donde se recibe la petición y se delega a `QueryMetrics`. Continúa con `MonitoringService.current` y `execute`, destacando reloj, fuente y calidad.

Muestra `MetricsSource` para explicar la interfaz y luego `MonitoringConfiguration` para revelar qué implementación se conecta. Termina con `PrometheusQueryBuilder`: la consulta la construye el servidor, no la envía libremente el usuario.

Para Simulator abre `high.json`, `compute_next_state` y `SimulatorCollector.collect`. Para Gateway basta comenzar por `application.yaml` y después revisar `RequestIdFilter`. No recorras todos los archivos: elige los que justifican cada decisión.

## 4 Preguntas sobre arquitectura

**¿Por qué tres componentes y no una sola aplicación?** Porque generación, consulta y entrada HTTP tienen responsabilidades diferentes. Separarlas permite evolucionarlas y probarlas de forma independiente. El coste es operar más procesos y manejar fallos de red. No debe justificarse solo diciendo que microservicios siempre es mejor.

**¿Por qué Monitoring no consulta directamente al simulador?** Porque el exporter expone el estado actual, mientras Prometheus recolecta y permite consultas temporales. Monitoring trabaja con una fuente de consultas estable que también podría recibir mediciones observadas compatibles.

**¿Qué aporta Monitoring si Prometheus ya tiene API?** Un catálogo cerrado del proyecto, filtros permitidos, unidades, identidad pública, tratamiento de huecos y errores y límites de consumo. El frontend no necesita conocer PromQL.

**¿Qué es un puerto hexagonal?** Una interfaz que expresa una capacidad ofrecida o requerida. `MetricsSource` representa lo que el caso de uso necesita de la fuente; no es el puerto de red 8080.

**¿Qué ocurriría si se cambia Prometheus por otra fuente?** Se necesitaría implementar un adaptador compatible con el puerto y el contrato semántico. El diseño reduce cambios en el núcleo, pero no hace automática la migración de unidades, etiquetas o consultas.

**¿Por qué Python en Simulator y Java en Monitoring?** El código mantiene el motor numérico sencillo en Python y aprovecha Spring para las APIs Java. La interoperabilidad se resuelve mediante HTTP y métricas, no compartiendo objetos en memoria. Esta es una explicación técnica de la separación observada, no una prueba de que esos lenguajes sean los únicos posibles.

## 5 Preguntas sobre datos y métricas

**¿Los datos son reales?** En la demo con Simulator son sintéticos y se declaran simulated. Prometheus es el mecanismo de recolección; no acredita que sean mediciones físicas.

**¿CPU al 80 % equivale a cierta energía consumida?** No. Falta una fuente o modelo de potencia validado y su integración temporal. Tampoco es correcto reportar watts como energía.

**¿Qué es una tasa?** Una variación de cantidad por unidad de tiempo. Los bytes acumulados se convierten a bytes/s mediante rate sobre una ventana.

**¿Por qué no sumar todas las interfaces?** Porque pueden representar recorridos superpuestos o recursos con semánticas distintas. El contrato preserva cada interfaz para evitar agregaciones injustificadas.

**¿Qué significa que la respuesta sea complete?** Que las series retornadas cubren la rejilla sin huecos, datos no finitos ni advertencias que la vuelvan parcial. No garantiza que todos los equipos existan en la respuesta ni que nunca se perdió un scrape.

**¿Por qué null no se convierte en cero?** Porque no observar un valor no demuestra ausencia de uso. Rellenar con cero introduciría una afirmación falsa y sesgaría promedios o análisis posteriores.

**¿Qué distingue source y origin?** Source indica de qué mecanismo se obtuvo, como Prometheus. Origin indica naturaleza, como simulated. Ambas informaciones son necesarias y compatibles.

**¿Por qué no filtrar por sim-lab en esta demo?** Porque el exporter ya proporciona cluster sim-run-UUID. El default solo cubre etiquetas ausentes o vacías.

**¿Por qué usar node en vez de instance?** Porque instance identifica el endpoint compartido. node identifica cada equipo del inventario; así se evita mezclar o duplicar identidades.

## 6 Preguntas sobre Simulator

**¿La misma semilla da todo exactamente igual?** Da los mismos estados lógicos si se mantienen también entradas, paso, duración y versión. UUID, fechas y tiempos de scrape pueden cambiar.

**¿Por qué usar un hash?** Para derivar una perturbación estable de semilla, tiempo, nodo y recurso sin depender del orden global de llamadas. No se está usando como cifrado del experimento.

**¿Qué cambia entre offline y realtime?** Offline calcula sin esperar y guarda snapshots; realtime acompasa los pasos con tiempo real y expone métricas. Offline no carga automáticamente históricos en Prometheus.

**¿El simulador consume realmente 85 % de CPU?** No. Calcula números que representan una utilización sintética. El proceso Python tiene su propio consumo real, distinto de los recursos que modela.

**¿Qué simplificaciones tiene?** Carga de CPU uniforme entre núcleos, memoria como fracción instantánea, red por interfaz sin modelar paquetes y disco con escritura sin borrado. No simula latencia, energía ni comportamiento detallado de workloads.

**¿Qué guardo para repetir un experimento?** Configuraciones exactas, semilla, tick, duración, revisión de código y snapshots. El manifiesto actual guarda rutas, por lo que hay que conservar también los archivos de entrada.

## 7 Preguntas sobre Spring y Gateway

**¿Por qué el servicio no tiene @Service?** Porque se crea explícitamente desde un método @Bean y permanece independiente de Spring. La inyección existe aunque la clase de negocio no lleve esa anotación.

**¿Qué diferencia tiene MVC de WebFlux aquí?** Monitoring usa el modelo servlet y espera resultados limitados; Gateway encadena operaciones reactivas para el transporte. Un cliente HTTP asíncrono interno no vuelve reactiva toda la aplicación MVC.

**¿Qué es Mono<Void>?** Una representación reactiva de finalización o error sin un valor de respuesta propio del filtro. No es un hilo ni significa ejecutar el método inmediatamente en otro procesador.

**¿CORS protege la API de cualquier cliente?** No. Controla acceso desde JavaScript en navegadores. La API todavía necesita autenticación y autorización para controlar usuarios en un despliegue que lo requiera.

**¿Authorization en allowedHeaders significa JWT implementado?** No. Solo permite esa cabecera dentro de la política CORS. No hay validación de token ni roles implementados.

**¿Hay un mismo request ID en toda la cadena?** No de forma garantizada actualmente. Gateway conserva o genera uno y Monitoring genera otro. Debe acordarse una política común antes de afirmar trazabilidad unificada.

**¿Existe un circuit breaker?** No está configurado. Hay timeouts y límites de concurrencia en Monitoring; son mecanismos distintos.

## 8 Preguntas sobre pruebas y despliegue

**¿Qué demuestra construir Docker?** Que pudo construirse una imagen bajo esas condiciones. Los Dockerfiles Java omiten ejecución de tests; construir no demuestra que las pruebas pasaron ni que el flujo completo funcione.

**¿UP significa datos disponibles?** No. La salud del proceso y la disponibilidad funcional de la fuente son dimensiones diferentes. Consulta current para verificar el acceso a datos.

**¿El Compose ya impide saltarse Gateway?** No. Publica otros puertos para la demo. La regla del frontend es arquitectónica y una política de despliegue más cerrada requeriría cambios de exposición de red.

**¿Dónde se guarda el histórico?** Prometheus almacena muestras recolectadas y Simulator escribe JSONL local por ejecución. Monitoring y Gateway no incorporan persistencia relacional. El Compose no define una política explícita de volúmenes de datos duraderos.

**¿Qué falta para declarar terminado el proyecto integrado?** Entre otros puntos, validar la fuente del laboratorio, métricas de workloads del Grupo B y los componentes de procesamiento/predicción que no forman parte de estos tres servicios. El catálogo actual no es todo el PMV1.

## 9 Ejercicios resueltos

**Ejercicio 1.** Un contador RX pasa de 2 000 a 8 000 bytes en tres segundos. ¿Qué representa 8 000 y cuál es la tasa sencilla? 8 000 son bytes acumulados. La tasa es `(8000-2000)/3 = 2000 bytes/s`.

**Ejercicio 2.** Dos CPU tienen idle 0.20 y 0.40. ¿Cuál es la utilización del nodo según la definición? Promedio idle 0.30; utilización 0.70 o 70 %.

**Ejercicio 3.** Histórico de una hora, paso quince, cuarenta y dos series. ¿Cabe? Cada serie tiene `3600/15 + 1 = 241` posiciones. Total `241 × 42 = 10 122`: excede diez mil aunque haya menos de cien series. Se espera rechazo por presupuesto.

**Ejercicio 4.** El gauge devuelve null con non_finite. ¿Puedes dibujarlo como cero? No. Debes mostrar o gestionar ausencia de valor utilizable, preservando su calidad.

**Ejercicio 5.** Cuatro CPU, dt=5 y utilización 0.75. ¿Cuánto aumenta user agregado? `4 × 5 × 0.75 = 15 segundos`. Idle aumenta cinco segundos. Cada núcleo suma 3.75 user y 1.25 idle.

**Ejercicio 6.** ¿Cuál es la ruta interna de `/api/monitoring/v1/metrics/history`? StripPrefix elimina tres segmentos y PrefixPath añade /api/v1: resulta `/api/v1/metrics/history`.

**Ejercicio 7.** El navegador está en localhost:3001 y se permite 127.0.0.1:3001. ¿Es el mismo origen? No. Hay que configurar el origen exacto utilizado.

**Ejercicio 8.** El exporter acaba de iniciar y la consulta de tasa está vacía. ¿Eso implica CPU cero? No. Puede faltar información suficiente para calcular rate o todavía no haberse recolectado la serie.

**Ejercicio 9.** Duración sesenta segundos, tick cinco y registro inicial. ¿Cuántos snapshots? Trece: el inicial y doce avances.

**Ejercicio 10.** Se repite la semilla pero cambia high.json. ¿Hay garantía de los mismos estados? No. El escenario también es entrada del modelo.

## 10 Frases que conviene corregir antes de exponer

| Afirmación imprecisa | Explicación defendible |
| --- | --- |
| «Simulator envía métricas a Monitoring» | Prometheus scrapea al exporter y Monitoring consulta Prometheus |
| «Prometheus siempre significa dato real» | La procedencia depende del origen declarado y acreditado |
| «Tenemos energía porque tenemos CPU» | Se miden o modelan recursos; energía requiere otra fuente o modelo |
| «El gateway autentica» | El gateway actual enruta y configura CORS y plazos |
| «La arquitectura hexagonal es idéntica en todos» | Monitoring tiene puertos explícitos; Simulator ensambla adaptadores en runner |
| «Con Docker ya está todo probado» | La imagen, las pruebas y la integración requieren evidencias diferentes |
| «El proyecto Green AI completo está terminado» | Este incremento cubre la cadena y el catálogo Grupo A descritos |

## 11 Ensayo final

Haz un primer ensayo de cinco minutos sin código: explica únicamente flujo, métricas y alcance. En el segundo añade el recorrido de cuatro clases y un ejemplo numérico. En el tercero usa el guion de quince minutos con la demostración preparada.

Si no puedes contestar algo, delimita el punto: «En el código revisado se implementa esta parte; esa otra requiere una decisión o prueba adicional». Es preferible una respuesta precisa sobre el alcance a inventar una capacidad.

Al finalizar, debes poder dibujar la cadena desde cero, calcular un incremento de contador, explicar un error funcional y señalar en qué archivo se decide una ruta o una fuente. Eso convierte tu exposición en una explicación técnica verificable.
