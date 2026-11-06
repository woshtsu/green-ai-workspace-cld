SEMANA 2 (completar de semana 1\)

1. EVIDENCIAS DEL KICKOFF

![][image1]

1. SELECCIÓN DE LA IDEA DE PROYECTO POR FACTORES PONDERADOS.CONSIDERAR ENFOQUE DE SOSTENIBILIDAD

| Criterio de evaluación | Peso | Idea 1: Green AI para centros de datos universitarios | Idea 2: Gemelo Digital de la cuenca del Mantaro | Idea 3: Agentes autónomos para expedientes municipales |
| :---: | :---: | :---: | :---: | :---: |
| **Viabilidad técnica** (madurez tecnológica, conocimientos del equipo, disponibilidad de herramientas e integración) | 25 % | **4 (1.00)** | 3 (0.75) | 3 (0.75) |
| **Impacto de la solución** (capacidad para resolver un problema relevante y generar beneficios medibles) | 20 % | **4 (0.80)** | 4 (0.80) | 3 (0.60) |
| **Impacto social** (beneficio institucional, académico, ciudadano o social) | 15 % | 3 (0.45) | **4 (0.60)** | **4 (0.60)** |
| **Impacto ambiental** (eficiencia energética, uso sostenible de recursos y reducción potencial de impactos ambientales) | 15 % | **5 (0.75)** | **5 (0.75)** | 2 (0.30) |
| **Innovación y diferenciación** (integración tecnológica, originalidad y diferenciación frente a soluciones existentes) | 15 % | **4 (0.60)** | **4 (0.60)** | 4 (0.60) |
| **Factibilidad de implementación académica** (alcance, tiempo, acceso a datos, infraestructura y posibilidad de validación) | 10 % | **4 (0.40)** | 2 (0.20) | 3 (0.30) |
| **TOTAL** | **100 %** | **4.00** | **3.70** | **3.15** |

SEMANA 2

# **1\. Antecedentes del problema**

La gestión eficiente de recursos computacionales en centros de datos y plataformas cloud constituye un problema relevante debido a la variabilidad de los workloads, al sobreaprovisionamiento y a la necesidad de mantener niveles adecuados de calidad de servicio. En los últimos años se han desarrollado propuestas basadas en Machine Learning, Deep Learning, scheduling energético y técnicas de autoescalado predictivo para anticipar la demanda y ajustar la asignación de recursos.

Para el presente proyecto se priorizaron investigaciones publicadas entre 2022 y 2025, relacionadas directamente con predicción de workloads, eficiencia energética, gestión de recursos y Kubernetes. Se consideran además antecedentes nacionales y un antecedente relacionado con Universidad Continental para contextualizar la problemática peruana y local.

## **1.1 Antecedentes internacionales**

### **Antecedente 1\. Predicción de workloads y estados energéticos mediante Machine Learning**

Khan et al. desarrollaron un modelo basado en Machine Learning para predecir cargas de trabajo y estimar estados de consumo energético en centros de datos cloud. La arquitectura propuesta estuvo compuesta por un **Resource Management System** y un módulo predictivo encargado de procesar información histórica de máquinas virtuales. Los autores utilizaron trazas reales de Bitbrains que incluían CPU aprovisionada y utilizada, memoria, almacenamiento y tráfico de red. Compararon regresión lineal, Ridge Regression, ARD Regression, ElasticNet y GRU. Experimentalmente, GRU obtuvo los menores errores RMSE en las variables analizadas. Para la estimación del estado energético, el algoritmo TSSAP obtuvo una micro-precision de hasta **87,48 %** en una de las evaluaciones reportadas (1).

**Aporte al proyecto:** este trabajo sustenta que la predicción de demanda no debe depender exclusivamente del porcentaje de CPU. Para el sistema Green AI se deberán considerar variables multivariadas como CPU, memoria, disco, red y recursos aprovisionados. Además, respalda la comparación de varios modelos antes de seleccionar el algoritmo definitivo, evitando asumir anticipadamente que una red neuronal será necesariamente superior.

### **Antecedente 2\. Predicción multivariable de recursos cloud**

Ullah, Bilal y Yoon propusieron un framework de pronóstico multivariable para predecir simultáneamente diferentes recursos de infraestructura cloud. Su propuesta utilizó un modelo BiLSTM y fue validada sobre dos conjuntos de trazas cloud reales. Entre las variables consideradas se encontraban CPU aprovisionada, CPU utilizada, memoria, operaciones de disco, transmisión de red y número de núcleos. Los autores compararon BiLSTM con diferentes configuraciones LSTM y autoencoders, utilizando MAE, RMSE y MAPE como principales indicadores de rendimiento. El modelo multivariable BiLSTM presentó los menores errores en las variables evaluadas (2).

La revista *Computer Networks* se encontraba clasificada como **Q1 en Scopus/SJR durante 2023 y 2024**, lo que permite utilizar este artículo como antecedente de alta calidad científica.

**Aporte al proyecto:** aporta la justificación para formular la predicción como un problema de **series temporales multivariadas**. También proporciona métricas apropiadas para evaluar los modelos del proyecto: MAE, RMSE y MAPE o sMAPE. No obstante, debido al costo computacional de BiLSTM, el proyecto deberá comparar este tipo de arquitectura contra modelos más simples antes de adoptarla.

### **Antecedente 3\. Consolidación predictiva considerando múltiples recursos**

Awad, Leivadeas y Awad propusieron un enfoque de consolidación predictiva de workloads en ambientes virtualizados, considerando simultáneamente múltiples tipos de recursos. El trabajo analiza la relación entre predicción de utilización, consolidación de cargas y reducción potencial del consumo energético, manteniendo restricciones vinculadas con acuerdos de nivel de servicio. La propuesta reconoce que consolidar workloads en un número menor de servidores puede mejorar la utilización de infraestructura, pero que una consolidación excesiva puede incrementar el riesgo de degradación del servicio (3).

El artículo fue publicado en *Computer Networks*, revista clasificada Q1 en 2023 y 2024\.

**Aporte al proyecto:** este antecedente sustenta una de las acciones que podrá generar el motor de recomendaciones Green AI: **consolidar workloads o reducir capacidad cuando exista una predicción confiable de baja demanda**, siempre que las restricciones de rendimiento permitan hacerlo. También justifica que el objetivo no sea simplemente minimizar CPU o servidores activos, sino equilibrar energía y SLA/SLO.

### **Antecedente 4\. Scheduling energético mediante Deep Reinforcement Learning**

Un estudio publicado en *Computers and Electrical Engineering* propuso un mecanismo de scheduling de trabajos en centros de datos utilizando Deep Reinforcement Learning. El objetivo fue asignar trabajos en tiempo real a máquinas virtuales buscando reducir consumo energético sin degradar la calidad del servicio. Esta investigación evidencia que la asignación de recursos puede formularse como un problema de decisión multiobjetivo en el cual deben considerarse simultáneamente energía y QoS (4).

La revista estaba clasificada **Q2 en JCR y Q1 en SJR durante 2022**, y actualmente se mantiene dentro del primer cuartil.

**Aporte al proyecto:** demuestra que la optimización energética puede abordarse mediante aprendizaje por refuerzo, pero también evidencia una alternativa de mayor complejidad computacional. Para un proyecto académico de 16 semanas no resulta conveniente asumir DRL como primera opción. El antecedente será utilizado principalmente para sustentar la naturaleza multiobjetivo del problema y comparar posteriormente enfoques complejos frente a modelos más ligeros.

### **Antecedente 5\. Gestión energética de microservicios en Kubernetes**

Rao y Li desarrollaron un algoritmo de scheduling consciente de energía para microservicios desplegados en Kubernetes. El enfoque considera el consumo de recursos, comunicación entre pods y restricciones SLA. Para realizar la asignación utilizaron una versión mejorada del **Sparrow Search Algorithm**. Los autores reportaron que su propuesta redujo al menos **5 % del consumo energético** frente a algoritmos de comparación en el entorno experimental utilizado (5).

**Aporte al proyecto:** este estudio resulta especialmente importante porque utiliza Kubernetes y combina el componente energético con el cumplimiento de SLA. Sustenta que el motor de recomendaciones Green AI deberá incluir restricciones de calidad de servicio antes de sugerir escalamiento, consolidación o modificación de recursos.

## **1.2 Antecedente nacional**

### **Antecedente 6\. Eficiencia energética en un Data Center peruano**

Morales Romero desarrolló en Perú una investigación cuantitativa sobre eficiencia energética en un Data Center de una refinería ubicada en Lima Metropolitana. Para caracterizar la infraestructura utilizó métricas **PUE y DCiE**, además de validar los cálculos mediante el software DC PRO. La situación inicial presentó un DCiE de **48,54 %**. Luego de diseñar mejoras relacionadas con UPS y sistemas de aire acondicionado, la potencia activa estimada disminuyó de **24,47 kW a 19,67 kW**. La investigación también estimó una reducción de aproximadamente **8380 kg de CO₂** bajo los factores de conversión empleados (6).

**Aporte al proyecto:** proporciona evidencia nacional de que la eficiencia energética de un centro de datos puede evaluarse utilizando indicadores cuantitativos. Sin embargo, su alcance se concentra principalmente en infraestructura eléctrica y climatización, mientras que Green AI actuará sobre la **gestión del workload y los recursos computacionales**. Esta diferencia permite sustentar la complementariedad de nuestra propuesta.

> **Importante:** este antecedente pertenece a ALICIA y es una tesis de grado, no un artículo Q1/Q2. Debe utilizarse como antecedente nacional contextual, no presentarse falsamente como publicación Q1.

## **1.3 Antecedente local / vinculado con Universidad Continental**

### **Antecedente 7\. Eficiencia energética de centros de datos y sostenibilidad**

Arellanos-Tafur et al., con participación de un investigador afiliado a **Universidad Continental**, analizaron la eficiencia energética de centros de datos mediante indicadores como Power Usage Effectiveness y el uso de Power Purchase Agreements. El estudio fue publicado en las actas de LACCEI 2025 y se encuentra indexado en Scopus. El trabajo resalta el uso de monitoreo en tiempo real, distribución inteligente de workloads y tecnologías de optimización energética como mecanismos relevantes para mejorar sostenibilidad. Además, vincula explícitamente el estudio con los ODS 7 y 13 (7).

**Aporte al proyecto:** proporciona un antecedente institucional cercano al contexto académico de Universidad Continental y respalda la pertinencia del problema de eficiencia energética desde una perspectiva de sostenibilidad. Sin embargo, el caso analizado utiliza información de centros de datos de Google y no constituye una validación experimental de infraestructura universitaria de Huancayo. Por ello, su función principal será contextual y no se utilizará como prueba de que la universidad presenta actualmente determinado nivel de ineficiencia.

**1.4 Matriz comparativa de antecedentes** 

| Fuente | Arquitectura/enfoque | IA o técnica | Datos/entorno | Métricas | Resultado relevante | Aporte al Green AI |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Khan et al. (2022) | RMS \+ módulo predictivo | LR, Ridge, ARD, ElasticNet, GRU, clustering | Bitbrains | RMSE, micro-precision | TSSAP hasta 87,48 % | Variables multivariadas y comparación de modelos |
| Ullah et al. (2023) | Forecasting multivariable | BiLSTM | Trazas cloud reales | MAE, RMSE, MAPE | BiLSTM obtuvo menores errores | Sustento de series temporales multivariadas |
| Awad et al. (2023) | Predicción \+ consolidación | Predicción multi-recurso | Infraestructura virtualizada | Energía, SLA, utilización | Mejora de consolidación | Sustenta consolidación predictiva |
| DRL scheduling (2022) | Scheduler inteligente | Deep Reinforcement Learning | Cloud/VM | Energía y QoS | Optimización multiobjetivo | Justifica restricciones de QoS |
| Rao y Li (2025) | Kubernetes Scheduler | ISSA | Kubernetes | Energía, SLA | ≥5 % menor energía en sus experimentos | Referencia directa para recomendaciones Kubernetes |
| Morales Romero (2024) | Auditoría energética | Modelado PUE/DCiE | Data Center peruano | PUE, DCiE, kW, CO₂ | 24,47 → 19,67 kW | Referencia nacional de medición energética |
| Arellanos-Tafur et al. (2025) | Análisis energético | Analítica/IA reportada | Centros de datos Google | PUE | Variaciones geográficas de PUE | Sostenibilidad y referencia UC |

# **1.5 Brecha identificada**

Los antecedentes muestran que existen soluciones para predecir workloads, realizar consolidación, autoescalamiento y scheduling consciente de energía. Sin embargo, las propuestas analizadas suelen resolver solo una parte del problema: algunas se concentran en predicción, otras en scheduling, otras en consolidación y otras en infraestructura eléctrica.

En consecuencia, se identifica una oportunidad para evaluar una arquitectura que integre:

**Monitoreo histórico → predicción de demanda → estimación del estado futuro → generación de recomendaciones → validación de restricciones SLA/SLO → evaluación energética experimental.**

Además, existe poca evidencia localizada en **entornos universitarios peruanos con recursos de infraestructura limitados**, por lo cual no se conoce si los enfoques propuestos internacionalmente mantienen sus beneficios bajo estas condiciones.

La contribución del proyecto no será inventar un nuevo algoritmo de Machine Learning, sino **integrar y evaluar experimentalmente un mecanismo predictivo y de recomendación energética adaptado a infraestructura universitaria**, comparándolo contra una estrategia convencional.

# **1.6 Sustento técnico del modelo de IA**

No recomiendo que el informe diga desde ahora:

> “Se utilizará LSTM porque es el mejor modelo”.

Eso sería metodológicamente débil.

La propuesta debería evaluar como mínimo tres familias de modelos:

| Modelo | Función | Ventaja | Riesgo |
| :---: | :---: | :---: | :---: |
| **ARIMA / Exponential Smoothing** | Baseline temporal | Interpretabilidad y bajo costo | Dificultad ante patrones altamente no lineales |
| **Random Forest / XGBoost** | Predicción supervisada con features temporales | Buen rendimiento y bajo costo operativo | Requiere ingeniería de características |
| **LSTM o GRU** | Captura dependencias temporales | Adecuado para comportamiento no lineal | Mayor costo de entrenamiento e inferencia |

El modelo seleccionado será aquel que alcance el mejor equilibrio entre:

**MAE \+ RMSE \+ sMAPE \+ tiempo de inferencia \+ consumo computacional \+ estabilidad.**

Esto además concuerda con la literatura: modelos GRU/BiLSTM muestran buenos resultados, pero investigaciones recientes también señalan que modelos híbridos o tradicionales pueden ser más eficientes dependiendo del patrón de carga.

# **1.7 Validación experimental propuesta**

La solución deberá compararse mediante dos escenarios:

| Escenario | Descripción |
| :---- | :---- |
| **Baseline** | Kubernetes con asignación convencional / HPA o reglas estáticas |
| **Tratamiento** | Sistema Green AI con predicción y recomendaciones |

Las condiciones deberán mantenerse equivalentes:

* mismo hardware;  
* mismo workload;  
* misma duración;  
* misma intensidad de carga;  
* mismas métricas;  
* mismas condiciones de red;  
* mismos límites SLA/SLO.

Las métricas principales serán:

| Dimensión | Métrica |
| :---- | :---- |
| Predicción | MAE, RMSE, sMAPE |
| Rendimiento | throughput, p95/p99 de latencia |
| Disponibilidad | % uptime |
| SLA/SLO | número y % de violaciones |
| Infraestructura | CPU, RAM, réplicas |
| Energía | Wh, kWh |
| Eficiencia | Wh/request o Wh/workload |
| Ambiental | gCO₂e, solo con factor de emisión sustentado |

No se establecerá inicialmente un “15 % de ahorro” ni “90 % de precisión” como resultado garantizado.

# **2\. Obtención y especificación de requisitos de software**

El lineamiento solicita expresamente requisitos funcionales, **tres requisitos de predicción de datos**, requisitos no funcionales y posteriormente la especificación mediante tema, épica, historia de usuario y criterios Given/When/Then.

## **2.1 Requerimientos funcionales**

| ID | Requerimiento funcional |
| :---- | :---- |
| RF-01 | El sistema deberá recopilar métricas de CPU, memoria, red y almacenamiento de los nodos monitoreados. |
| RF-02 | El sistema deberá recopilar métricas de workload como solicitudes, concurrencia, throughput y latencia. |
| RF-03 | El sistema deberá almacenar las métricas históricas con marca temporal. |
| RF-04 | El sistema deberá permitir consultar series históricas por nodo, servicio y período. |
| **RF-IA-01** | **El sistema deberá predecir la demanda futura de workloads para un horizonte configurable.** |
| **RF-IA-02** | **El sistema deberá predecir la utilización futura de CPU y memoria a partir de métricas históricas.** |
| **RF-IA-03** | **El sistema deberá estimar el consumo energético o riesgo energético futuro cuando exista información válida para entrenar el modelo.** |
| RF-08 | El sistema deberá comparar al menos tres modelos de predicción utilizando métricas de error. |
| RF-09 | El sistema deberá registrar versiones de modelos, parámetros y experimentos. |
| RF-10 | El sistema deberá generar recomendaciones de escalamiento, consolidación o modificación de recursos. |
| RF-11 | El sistema deberá verificar restricciones SLA/SLO antes de emitir una recomendación. |
| RF-12 | El sistema deberá clasificar las recomendaciones según nivel de riesgo. |
| RF-13 | El administrador deberá poder aprobar o rechazar una recomendación. |
| RF-14 | El sistema deberá registrar la decisión del administrador en una bitácora de auditoría. |
| RF-15 | El sistema deberá presentar indicadores de consumo energético y eficiencia. |
| RF-16 | El sistema deberá presentar predicción y valores reales en una misma visualización. |
| RF-17 | El sistema deberá mostrar alertas de saturación, subutilización o riesgo de SLA/SLO. |
| RF-18 | El sistema deberá generar reportes comparativos entre baseline y estrategia Green AI. |
| RF-19 | El sistema deberá autenticar usuarios técnicos autorizados. |
| RF-20 | El sistema deberá administrar roles y permisos. |

# **2.2 Requerimientos no funcionales**

| ID | Requisito | Criterio |
| :---- | :---- | :---- |
| RNF-01 | Seguridad | Acceso mediante autenticación y RBAC |
| RNF-02 | Confidencialidad | No almacenar datos personales innecesarios |
| RNF-03 | Auditabilidad | Registrar usuario, acción, fecha y resultado |
| RNF-04 | Rendimiento | El dashboard deberá responder a consultas ordinarias en ≤3 s bajo el entorno experimental |
| RNF-05 | Disponibilidad | Los componentes experimentales deberán registrar disponibilidad durante las pruebas |
| RNF-06 | Mantenibilidad | La lógica de dominio deberá desacoplarse de infraestructura y frameworks |
| RNF-07 | Escalabilidad | El módulo de adquisición deberá soportar incorporación de nuevos nodos |
| RNF-08 | Interoperabilidad | Comunicación mediante APIs REST y/o eventos normalizados |
| RNF-09 | Portabilidad | Los componentes deberán desplegarse mediante contenedores |
| RNF-10 | Observabilidad | Servicios con logs, métricas y trazabilidad |
| RNF-11 | Reproducibilidad IA | Experimentos, hiperparámetros y métricas deberán versionarse |
| RNF-12 | Seguridad operacional | Las acciones serán Recommendation-Only durante el MVP |
| RNF-13 | Sostenibilidad | Se deberá registrar el costo computacional del modelo seleccionado |
| RNF-14 | Usabilidad | El dashboard deberá presentar información interpretable para personal TI |
| RNF-15 | Fiabilidad | Una falla del módulo IA no deberá detener el monitoreo |
| RNF-16 | Trazabilidad | Cada recomendación deberá vincularse a datos y predicción que la originaron |

# **2.3 Épicas, historias de usuario y criterios de aceptación**

| Épica | ID | Historia de Usuario | Criterios de Aceptación (Given / When / Then) |
| ----- | ----- | ----- | ----- |
| **Observabilidad y gestión de datos** | **HU-01** | Como administrador de infraestructura, quiero visualizar las métricas de CPU, memoria, red y almacenamiento para conocer el estado actual del entorno computacional. | **Given:** que existe un nodo registrado y accesible. **When:** el sistema recibe nuevas métricas. **Then:** deberá almacenarlas y mostrarlas en el dashboard indicando el nodo, valor, fecha y hora de registro. |
| **Observabilidad y gestión de datos** | **HU-02** | Como administrador de infraestructura, quiero consultar las métricas históricas para identificar patrones de utilización y comportamiento de los workloads. | **Given:** que existen registros históricos almacenados. **When:** selecciono un nodo, una métrica y un período. **Then:** el sistema deberá mostrar la serie temporal correspondiente y permitir analizar su evolución. |
| **Inteligencia predictiva** | **HU-03** | Como administrador TI, quiero conocer la demanda futura de los workloads para anticipar períodos de alta o baja utilización. | **Given:** que existe una cantidad suficiente de datos históricos válidos. **When:** solicito una predicción para un horizonte determinado. **Then:** el sistema deberá mostrar la demanda estimada, el horizonte de predicción y el modelo utilizado. |
| **Inteligencia predictiva** | **HU-04** | Como administrador TI, quiero predecir la utilización futura de CPU y memoria para planificar la capacidad computacional requerida. | **Given:** que existe un modelo entrenado y validado. **When:** el sistema procesa las métricas más recientes. **Then:** deberá generar la predicción futura de CPU y memoria para el horizonte configurado. |
| **Inteligencia predictiva** | **HU-05** | Como administrador TI, quiero estimar el consumo energético futuro para analizar escenarios de gestión energéticamente eficientes. | **Given:** que existen datos energéticos medidos o un modelo energético previamente validado. **When:** el sistema procesa la demanda prevista y las características de utilización. **Then:** deberá mostrar el consumo energético estimado en Wh o kWh e indicar si el valor corresponde a una medición o estimación. |
| **Optimización de recursos** | **HU-06** | Como administrador TI, quiero recibir recomendaciones de escalamiento, consolidación o ajuste de recursos para utilizar eficientemente la infraestructura disponible. | **Given:** que existe una predicción válida de demanda o utilización. **When:** el sistema identifica una diferencia entre la capacidad asignada y la demanda prevista. **Then:** deberá generar una recomendación indicando la acción propuesta, los recursos involucrados y la justificación. |
| **Optimización de recursos** | **HU-07** | Como administrador TI, quiero que las recomendaciones consideren restricciones de SLA/SLO para evitar degradaciones en la calidad del servicio. | **Given:** que existe una recomendación candidata. **When:** el motor evalúa las restricciones de latencia, throughput, disponibilidad y SLA/SLO. **Then:** deberá aceptar, modificar o descartar la recomendación según el cumplimiento de los límites establecidos. |
| **Control y seguridad operacional** | **HU-08** | Como administrador TI, quiero aprobar o rechazar las recomendaciones generadas para mantener control humano sobre las decisiones aplicadas a la infraestructura. | **Given:** que existe una recomendación pendiente. **When:** selecciono aprobar o rechazar. **Then:** el sistema deberá registrar la decisión, usuario responsable, fecha, justificación y estado final en la bitácora de auditoría. |
| **Evaluación y sostenibilidad** | **HU-09** | Como investigador, quiero comparar la gestión convencional con la estrategia Green AI para determinar experimentalmente su impacto energético y operacional. | **Given:** que existen experimentos equivalentes de baseline y tratamiento. **When:** finaliza la ejecución de ambos escenarios. **Then:** el sistema deberá comparar consumo energético, Wh/request o Wh/workload, utilización, latencia, throughput, disponibilidad y cumplimiento de SLA/SLO. |
| **Evaluación y sostenibilidad** | **HU-10** | Como investigador, quiero generar un reporte de los resultados experimentales para sustentar las conclusiones del proyecto mediante indicadores cuantitativos. | **Given:** que existen resultados válidos de los experimentos. **When:** solicito generar el informe. **Then:** el sistema deberá presentar las métricas del baseline y Green AI, sus diferencias absolutas y relativas y los indicadores de desempeño del modelo predictivo. |

# **2.4 Cuadro de requerimientos por PMV con IA**

| ID | PMV | META (Objetivo específico) | VALOR | REQUERIMIENTOS | ENTREGA |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **1** | **Predicción inteligente de demanda y utilización de recursos** | Recopilar métricas históricas y **predecir la demanda de workloads y la utilización futura de CPU y memoria**, con el propósito de anticipar las necesidades de capacidad de la infraestructura computacional. | Obtener visibilidad anticipada del comportamiento de los workloads y reducir la incertidumbre en la asignación de recursos frente a períodos de alta o baja demanda. | **HU-01:** Como administrador de infraestructura, necesito visualizar las métricas de CPU, memoria, red y almacenamiento para conocer el estado actual del entorno y disponer de datos para el análisis predictivo. **HU-02:** Como administrador de infraestructura, necesito consultar métricas históricas por nodo, variable y período para identificar patrones de utilización de los recursos. **HU-03:** Como administrador TI, necesito que el sistema prediga la demanda futura de workloads para un horizonte configurable, con el fin de anticipar períodos de alta o baja utilización. **HU-04:** Como administrador TI, necesito que el sistema prediga la utilización futura de CPU y memoria para planificar la capacidad computacional requerida. **HU-05:** Como administrador TI, necesito que el sistema compare los modelos predictivos mediante MAE, RMSE y sMAPE para seleccionar el modelo con mejor desempeño bajo las condiciones evaluadas. | **S4 – S10**Pipeline de recopilación de métricas.Repositorio histórico de series temporales.Dashboard de utilización.Servicio de predicción desplegado.Modelos entrenados, comparados y validados.Predicciones disponibles en el dashboard. |
| **2** | **Estimación y monitoreo del consumo energético** | Relacionar la demanda, utilización de recursos y ejecución de workloads con el **consumo energético medido o estimado** para establecer una línea base energética del entorno experimental. | Cuantificar el comportamiento energético de la infraestructura y disponer de indicadores objetivos que permitan evaluar posteriormente la eficiencia de las estrategias de gestión. | **HU-06:** Como administrador de infraestructura, necesito visualizar el consumo energético del entorno en Wh o kWh para conocer su comportamiento durante la ejecución de los workloads. **HU-07:** Como administrador TI, necesito que el sistema estime el consumo energético futuro a partir de la demanda y utilización previstas para evaluar posibles escenarios de gestión. **HU-08:** Como administrador TI, necesito consultar indicadores como Wh/request o Wh/workload para evaluar la eficiencia energética de la infraestructura.El sistema deberá diferenciar explícitamente los valores energéticos **medidos** de aquellos obtenidos mediante **estimación**. | **S8 – S11**Mecanismo de medición o estimación energética.Línea base energética experimental.Indicadores Wh y kWh.Indicadores Wh/request o Wh/workload.Visualización energética integrada al dashboard. |
| **3** | **Generación inteligente de recomendaciones de gestión de recursos** | Utilizar las predicciones de demanda y el estado de la infraestructura para proponer acciones de **escalamiento, consolidación o ajuste de recursos**, considerando restricciones de rendimiento. | Transformar las predicciones en información accionable que permita mejorar la utilización de los recursos computacionales sin limitar el sistema únicamente al monitoreo o pronóstico. | **HU-09:** Como administrador TI, necesito que el sistema genere recomendaciones de escalamiento, consolidación o ajuste de recursos cuando exista una diferencia relevante entre la capacidad asignada y la demanda prevista. **HU-10:** Como administrador TI, necesito conocer la justificación de cada recomendación, incluyendo demanda prevista, utilización actual, recursos involucrados y acción propuesta. **HU-11:** Como administrador TI, necesito que el sistema evalúe las restricciones de latencia, throughput, disponibilidad y SLA/SLO antes de emitir una recomendación, para reducir el riesgo de degradación del servicio. | **S10 – S13**Motor de recomendaciones operativo.Integración del modelo predictivo con el motor de decisión.Reglas de escalamiento y consolidación.Validación de SLA/SLO implementada.Recomendaciones disponibles en el dashboard. |
| **4** | **Control, seguridad operacional y trazabilidad** | Garantizar que las recomendaciones sean supervisadas, auditables y sujetas a **control humano** antes de cualquier posible aplicación sobre la infraestructura. | Reducir riesgos operacionales, mantener control sobre las decisiones propuestas por la IA y garantizar la trazabilidad de las acciones realizadas durante el experimento. | **HU-12:** Como administrador TI, necesito aprobar o rechazar las recomendaciones generadas por el sistema para mantener control humano sobre las decisiones relacionadas con la infraestructura. **HU-13:** Como administrador TI, necesito que el sistema registre cada recomendación, su justificación, fecha, usuario responsable, decisión adoptada y resultado para garantizar trazabilidad y auditoría. **HU-14:** Como administrador TI, necesito que las recomendaciones sean clasificadas según su nivel de riesgo para identificar aquellas que podrían afectar la calidad del servicio.Durante el MVP, el sistema funcionará bajo el enfoque **Recommendation-Only**, sin ejecutar automáticamente cambios irrestrictos sobre infraestructura crítica. | **S11 – S14**Módulo de aprobación y rechazo.Motor de políticas de seguridad operacional.Clasificación de recomendaciones.Bitácora de auditoría.Trazabilidad de decisiones disponible. |
| **5** | **Evaluación experimental y sostenibilidad** | Comparar experimentalmente una estrategia convencional de gestión de recursos con la estrategia **Green AI**, utilizando condiciones equivalentes de infraestructura y workload. | Obtener evidencia cuantitativa para determinar si la estrategia propuesta mejora la eficiencia energética sin producir una degradación inaceptable del rendimiento o de la calidad del servicio. | **HU-15:** Como investigador, necesito comparar el escenario baseline con Green AI mediante métricas de energía, utilización, rendimiento y SLA/SLO para determinar el impacto real de la estrategia propuesta. **HU-16:** Como investigador, necesito visualizar las diferencias de consumo energético, Wh/request, latencia p95/p99, throughput, utilización, disponibilidad y violaciones de SLA/SLO entre ambos escenarios. **HU-17:** Como investigador, necesito generar un reporte de los resultados experimentales y métricas de los modelos predictivos para sustentar cuantitativamente las conclusiones del proyecto. | **S14 – S16**Experimentos baseline vs. Green AI ejecutados.Resultados comparativos obtenidos.Métricas energéticas y de rendimiento consolidadas.Análisis cuantitativo de resultados.Reporte experimental y documentación final. |

3.Arquitectura de la solución.

Describir tres arquitecturas de software y seleccionar una por factores ponderados entre: Arquitectura hexagonal, de microservicios, event-driven o una combinación de ellas

• arquitectura hexagonal,

• separación de capas,

• puertos y adaptadores,

• desacoplamiento entre dominio e infraestructura,

• escalabilidad del sistema,

• mantenibilidad.

3.1 Diagrama de arquitectura de componentes de software UML (de la arquitectura seleccionada)

![][image2]

3.2 Diagrama de arquitectura de despliegue UML (de la arquitectura seleccionada)

![][image3]

# **6\. Referencias ISO 690 numéricas preliminares**

**1\.** KHAN, Tahseen, et al. *Workload forecasting and energy state estimation in cloud data centres: ML-centric approach*. Future Generation Computer Systems. 2022, vol. 128, pp. 320–332. DOI 10.1016/j.future.2021.10.019.

**2\.** ULLAH, Farman; BILAL, Muhammad y YOON, Su-Kyung. *Intelligent time-series forecasting framework for non-linear dynamic workload and resource prediction in cloud*. Computer Networks. 2023\. DOI 10.1016/j.comnet.2023.109653.

**3\.** AWAD, Mirna; LEIVADEAS, Aris y AWAD, Abir. *Multi-resource predictive workload consolidation approach in virtualized environments*. Computer Networks. 2023, vol. 237, art. 110088\. DOI 10.1016/j.comnet.2023.110088.

**4\.** *Energy-aware systems for real-time job scheduling in cloud data centers: A deep reinforcement learning approach*. Computers and Electrical Engineering. 2022, vol. 99, art. 107688\. DOI 10.1016/j.compeleceng.2022.107688.

**5\.** RAO, Wei y LI, Hongjian. *Energy-aware Scheduling Algorithm for Microservices in Kubernetes Clouds*. Journal of Grid Computing. 2025, vol. 23\. DOI 10.1007/s10723-024-09788-w.

**6\.** MORALES ROMERO, Boris Mijael. *Elaboración del Plan de Mejora de la eficiencia energética para optimizar el consumo de energía eléctrica en el Data Center de refinería de petróleo en la ciudad Lima Metropolitana para el 2024*. Lima: Universidad Tecnológica del Perú, 2024\. Tesis de grado. Disponible en ALICIA-CONCYTEC.

**7\.** ARELLANOS-TAFUR, Elmer; GUTIERREZ RUPAY, Hugo; ROJAS-ARQUIÑEGO, Felix y DAMAS-NIÑO, Marcelo. *Impact of energy efficiency on reducing consumption in data centers with power purchase agreements – PPAs*. Proceedings of the LACCEI International Multi-Conference for Engineering, Education and Technology. 2025\. DOI 10.18687/LACCEI2025.1.1.2072.

[image1]: <evidencias/img-44325653a810.png>

[image2]: <evidencias/img-5d0ed2a5c3c5.png>

[image3]: <evidencias/img-60faa3f79481.png>