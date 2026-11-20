

**UNIVERSIDAD CONTINENTAL**

**INGENIERÍA DE SISTEMAS E INFORMÁTICA**

	

**PROYECTO 20**

**Green AI para centros de datos universitarios**

**GUÍA 6**  
**CONOCIMIENTOS DE INGENIERÍA Y DISEÑO DE LA SOLUCIÓN**

| Estudiante | \[NOMBRE DEL ESTUDIANTE\] |
| :---- | :---- |
| **Docente** | \[NOMBRE DEL DOCENTE\] |
| **NRC** | \[NRC\] |
| **Ciclo académico** | \[CICLO\] |
| **Fecha** | Septiembre de 2026 |

**Huancayo, Perú**

# **CONTENIDO**

1\. Problema complejo de ingeniería

2\. Necesidades y requerimientos de ingeniería

3\. Fundamentos matemáticos y científicos

4\. Conocimientos de computación

5\. Conocimientos fundamentales de ingeniería

6\. Conocimientos especializados del dominio

7\. Selección y justificación de metodologías y tecnologías

8\. Aplicación de conocimientos al diseño de la solución

9\. Integración de conocimientos de ingeniería

10\. Validación de la aplicación de conocimientos

11\. Implementación, evidencias y trazabilidad de ingeniería

12\. Conclusiones de conocimientos de ingeniería

Referencias bibliográficas y fuentes de sustento

Nota documental: la numeración principal se organiza en doce apartados para conservar la estructura de conocimientos de ingeniería y, al mismo tiempo, incorporar dentro de ella la arquitectura, MLOps, optimización, seguridad, experimentación, riesgos, evidencias y antecedentes que ya habían sido desarrollados en el informe técnico anterior.

# **Presentación del documento**

El presente informe reorganiza y amplía el contenido técnico desarrollado para el Proyecto 20 bajo una estructura orientada a demostrar el atributo AG-I07, Conocimientos de Ingeniería. La organización toma como referencia el documento institucional de conocimientos de ingeniería proporcionado para el proyecto, cuya lógica exige evidenciar no solo conceptos, sino su selección, aplicación, integración y validación.

El documento base establece que la evidencia debe demostrar la relación entre problema complejo, necesidades y restricciones, conocimientos requeridos, selección, aplicación al diseño, integración, implementación, validación y conclusiones. En consecuencia, la presente versión no mantiene como capítulos independientes todos los componentes técnicos del informe anterior, sino que los integra dentro de los doce apartados principales para evitar repetición y mejorar la trazabilidad.

El proyecto aborda la predicción de demanda computacional y su utilización como insumo para optimizar la gestión energética de workloads en infraestructura universitaria. La solución propuesta combina adquisición de telemetría, análisis de series temporales, Machine Learning, optimización bajo restricciones, Policy/Safety Engine, MLOps, observabilidad y experimentación controlada.

La solución se plantea inicialmente en un entorno experimental controlado y bajo un modo Recommendation-Only. Esta decisión impide que el modelo predictivo tenga control irrestricto sobre la infraestructura y permite separar la calidad de la predicción de la seguridad de la decisión y del efecto energético finalmente observado.

El informe conserva la distinción entre consumo energético medido, energía estimada y métricas operativas utilizadas como proxy. En particular, la utilización de CPU no se considera equivalente al consumo energético. Asimismo, no se presupone un porcentaje de ahorro; cualquier mejora deberá demostrarse experimentalmente mediante comparación con una línea base y bajo condiciones equivalentes.

# **1\. Problema complejo de ingeniería**

El Proyecto 20 aborda la gestión eficiente de workloads computacionales ejecutados en una infraestructura universitaria cuya demanda de recursos varía en el tiempo. La dificultad de ingeniería no consiste únicamente en observar CPU, memoria, red o estado de los workloads, sino en determinar si la asignación actual responde adecuadamente a la demanda y si existe una oportunidad técnicamente demostrable para mejorar la eficiencia energética sin degradar el servicio.

El problema se formula como un problema de decisión bajo incertidumbre. La infraestructura dispone de información histórica y operacional, mientras que la demanda futura no se conoce con certeza. Por ello, el proyecto estudia si una predicción de corto plazo puede mejorar las decisiones de gestión de recursos y si esa mejora puede traducirse en una reducción medible de energía o de energía por unidad de trabajo.

La complejidad proviene de la interacción simultánea de variables y restricciones. Una decisión puede modificar utilización, latencia, throughput, disponibilidad, cantidad de réplicas, concentración de workloads y consumo energético. Por tanto, una solución técnicamente válida debe considerar objetivos energéticos y operativos de manera conjunta.

## **1.1 Contexto de aplicación**

El contexto corresponde a un entorno universitario donde se ejecutan servicios, aplicaciones, laboratorios, workloads académicos o cargas experimentales sobre infraestructura computacional local o administrada mediante una plataforma privada. La arquitectura definitiva deberá ajustarse al levantamiento real de nodos, CPU, memoria, almacenamiento, red, permisos de Kubernetes y mecanismos de medición energética.

La literatura sobre gestión energética en cloud demuestra que el problema de asignación de recursos puede abordarse mediante políticas de provisioning, consolidación y scheduling que deben mantener las condiciones de calidad del servicio. Beloglazov, Abawajy y Buyya plantearon principios de asignación energéticamente eficiente y consolidación dinámica con consideración explícita de QoS \[9\].

## **1.2 Causas principales**

* Variabilidad temporal de la demanda computacional.  
* Asociación conservadora o estática de recursos ante incertidumbre de demanda.  
* Ausencia de un mecanismo predictivo integrado con la gestión de workloads.  
* Falta de correlación sistemática entre telemetría operacional y variables energéticas.  
* Necesidad de mantener capacidad de reserva para cumplir disponibilidad y SLA.  
* Complejidad de decidir cuándo consolidar, redistribuir o escalar workloads sin deteriorar el servicio.  
* Necesidad de demostrar experimentalmente que una decisión de optimización produce un beneficio neto considerando también el overhead de la propia solución.

## **1.3 Consecuencias potenciales**

* Subutilización de recursos computacionales.  
* Consumo energético superior al necesario para una unidad funcional de trabajo.  
* Uso ineficiente de la capacidad instalada.  
* Incremento potencial de costos operativos.  
* Mayor impacto ambiental operacional cuando la energía consumida presenta una determinada intensidad de carbono.  
* Dificultad para justificar decisiones de optimización cuando no existe trazabilidad entre datos, predicción, decisión y resultado.

## **1.4 Restricciones de ingeniería**

* La infraestructura disponible condicionará la escala de los experimentos.  
* La calidad y frecuencia de las métricas determinarán la resolución del dataset.  
* La medición energética directa puede no estar disponible para todos los componentes.  
* Las acciones de infraestructura estarán limitadas por permisos, RBAC y políticas de seguridad.  
* El sistema no podrá sacrificar SLA, disponibilidad, latencia o throughput para producir una mejora energética no justificada.  
* El modelo predictivo no tendrá autorización para ejecutar acciones irrestrictas sobre Kubernetes.  
* Las conclusiones deberán distinguir resultados medidos, estimaciones y supuestos.

## **1.5 Oportunidad de ingeniería**

La oportunidad consiste en construir una cadena de decisión que transforme telemetría en información predictiva y posteriormente en recomendaciones de gestión de recursos. El aporte no se limita a entrenar un modelo de Machine Learning; la contribución de ingeniería se encuentra en integrar predicción, optimización, políticas de seguridad, operación controlada y validación experimental.

La literatura reciente sobre workload forecasting muestra que la predicción de recursos puede utilizarse conjuntamente con estimación del estado energético para apoyar la gestión de centros de datos. Khan et al. desarrollaron un enfoque centrado en Machine Learning para forecasting de workloads y estimación del estado energético utilizando trazas reales de centros de datos \[7\].

De manera complementaria, Ji et al. integraron predicción de workload con gestión de recursos, scheduling y migración dentro de un esquema de optimización energética y validaron el enfoque mediante trazas reales \[8\]. Estos antecedentes justifican estudiar una cadena integrada, pero sus resultados no se trasladan como resultados esperados del Proyecto 20\.

# **2\. Necesidades y requerimientos de ingeniería**

El documento de conocimientos de ingeniería establece que esta sección debe determinar qué necesita resolver la ingeniería. En el Proyecto 20, cada necesidad se traduce en una capacidad técnica, un requerimiento verificable y una evidencia. Esta relación permite que los conocimientos posteriores respondan a necesidades concretas.

*Tabla 1\. Necesidades, respuestas de ingeniería y evidencias*

| Necesidad | Respuesta de ingeniería | Requerimiento / condición | Evidencia |
| :---- | :---- | :---- | :---- |
| Conocer el estado de la infraestructura | Adquirir métricas de nodos, workloads y aplicaciones. | Telemetría disponible con frecuencia definida y procedencia identificable. | Series temporales, consultas y dashboards. |
| Caracterizar la demanda | Construir dataset temporal y variables predictoras. | Datos limpios, sincronizados y con calidad evaluada. | Reporte de calidad y dataset documentado. |
| Predecir demanda futura | Entrenar modelos de forecasting de corto plazo. | Modelo comparado contra baseline y horizonte definido. | MAE, RMSE, sMAPE y análisis de picos. |
| Convertir predicción en decisión | Evaluar alternativas mediante optimización bajo restricciones. | Variables de decisión, función objetivo y restricciones explícitas. | Ejecuciones reproducibles del optimizador. |
| Evitar decisiones inseguras | Aplicar Policy/Safety Engine antes de recomendar o ejecutar. | RBAC, restricciones de capacidad, SLA y seguridad. | Registros de políticas, aprobaciones y rechazos. |
| Demostrar impacto | Comparar baseline y tratamiento bajo condiciones equivalentes. | Escenarios controlados y repeticiones. | Resultados comparativos y análisis estadístico. |
| Medir sostenibilidad | Relacionar energía y unidad funcional. | Método de medición o estimación documentado. | kWh, Wh/unidad de trabajo y, cuando corresponda, gCO2e/unidad. |
| Asegurar reproducibilidad | Gestionar datasets, modelos, parámetros y artefactos. | Versionado y tracking de experimentos. | MLflow, identificadores de dataset y artefactos. |
| Controlar el riesgo operativo | Mantener la operación en Recommendation-Only. | Separación entre predicción y ejecución. | Auditoría y ausencia de acciones autónomas no autorizadas. |

## **2.1 Requerimientos funcionales**

1. Recolectar métricas de infraestructura, workloads y aplicaciones desde las fuentes disponibles.  
2. Normalizar y preparar series temporales para análisis y entrenamiento.  
3. Construir ventanas históricas y variables predictoras.  
4. Entrenar y evaluar modelos candidatos de predicción de demanda.  
5. Registrar modelos, parámetros, métricas y artefactos.  
6. Generar predicciones mediante una API controlada.  
7. Evaluar alternativas de asignación mediante el Optimization Engine.  
8. Validar las alternativas mediante el Policy/Safety Engine.  
9. Registrar y presentar recomendaciones trazables.  
10. Ejecutar experimentos comparables entre baseline y estrategia propuesta.

## **2.2 Requerimientos no funcionales**

* Seguridad: autenticación, autorización, RBAC, mínimo privilegio, gestión segura de secretos y auditoría.  
* Rendimiento: latencia de inferencia y de generación de recomendaciones dentro del presupuesto definido para el experimento.  
* Disponibilidad: recuperación controlada de componentes críticos del pipeline.  
* Reproducibilidad: identificación de datos, código, parámetros, modelo y configuración.  
* Mantenibilidad: separación de responsabilidades y modularidad.  
* Observabilidad: métricas, logs y evidencias suficientes para explicar el comportamiento.  
* Rollback: toda futura acción automatizada deberá poder revertirse.  
* Trazabilidad: cada recomendación deberá poder relacionarse con su predicción, contexto, restricciones y resultado.

# **2.4 Matriz de Épicas, Historias de Usuario y Criterios de Aceptación**

La tabla que tienes actualmente solamente desarrolla **Gestión de Datos**. Para el proyecto completo debemos ampliarla para cubrir los módulos reales de la arquitectura.

## **Matriz de Épicas, Historias de Usuario y Criterios de Aceptación**

| Épica (por módulo) | Historia de Usuario | Criterios de Aceptación (Given / When / Then) |
| ----- | ----- | ----- |
| **Gestión de Datos** | Como administrador necesito importar datos históricos de infraestructura y workloads para que el sistema pueda entrenar el modelo de predicción. | **Escenario 1: Importación exitosa.** Given que selecciono un archivo válido de datos históricos. When lo cargo al sistema. Then el sistema valida, procesa y almacena los datos correctamente. **Escenario 2: Formato inválido.** Given que selecciono un archivo con formato incorrecto. When intento cargarlo. Then el sistema muestra un mensaje indicando el formato esperado. |
| **Gestión de Datos** | Como responsable del sistema necesito validar y limpiar los datos recopilados para evitar que valores inválidos afecten el entrenamiento. | **Escenario 1: Datos válidos.** Given que existen datos recopilados. When se ejecuta el procesamiento. Then el sistema identifica registros válidos y los prepara para el modelo. **Escenario 2: Datos incompletos.** Given que existen registros con valores faltantes. When se ejecuta la limpieza. Then el sistema identifica y registra los valores faltantes según las reglas definidas. |
| **Observabilidad** | Como operador necesito visualizar métricas de infraestructura y workloads para conocer el estado actual del entorno Kubernetes. | **Escenario 1: Métricas disponibles.** Given que los componentes de observabilidad están activos. When el sistema consulta las métricas. Then se obtienen indicadores de CPU, memoria, workloads y recursos del clúster. **Escenario 2: Fuente no disponible.** Given que una fuente de métricas no responde. When se realiza la consulta. Then el sistema registra el incidente sin detener los demás componentes. |
| **Observabilidad** | Como operador necesito consultar las métricas históricas para analizar el comportamiento de la carga computacional. | **Escenario 1: Consulta histórica.** Given que existen métricas almacenadas. When selecciono un intervalo temporal. Then el sistema presenta los datos correspondientes al periodo solicitado. |
| **Predicción** | Como responsable de la plataforma necesito predecir la demanda computacional futura para anticipar incrementos de carga. | **Escenario 1: Predicción generada.** Given que existen datos suficientes y un modelo validado. When se solicita una predicción. Then el servicio genera una estimación de demanda para el horizonte configurado. **Escenario 2: Datos insuficientes.** Given que no existe información suficiente. When se solicita una predicción. Then el sistema informa que no puede generar una predicción confiable. |
| **Predicción** | Como investigador necesito comparar modelos de aprendizaje automático para seleccionar el que presente mejor desempeño predictivo. | **Escenario 1: Evaluación.** Given que existen conjuntos de entrenamiento, validación y prueba. When se ejecutan los modelos candidatos. Then el sistema registra MAE, RMSE, sMAPE y tiempo de inferencia. **Escenario 2: Selección.** Given que existen resultados de varios modelos. When se comparan sus métricas. Then el sistema identifica el modelo que cumple los criterios establecidos. |
| **Decisión** | Como operador necesito que el sistema interprete las predicciones junto con el estado actual de la infraestructura para determinar si existe una situación que requiere análisis. | **Escenario 1: Demanda normal.** Given que la demanda prevista se encuentra dentro de los límites establecidos. When el servicio analiza el contexto. Then no genera una alerta de incremento de demanda. **Escenario 2: Demanda elevada.** Given que la demanda prevista supera el umbral definido. When se analiza el contexto. Then se genera un evento de demanda elevada para el proceso de optimización. |
| **Optimización** | Como responsable de infraestructura necesito obtener alternativas de asignación de recursos que reduzcan el consumo energético sin incumplir las restricciones operativas. | **Escenario 1: Alternativas factibles.** Given que existe una predicción y un contexto operativo válido. When se ejecuta el motor de optimización. Then genera una o más alternativas factibles. **Escenario 2: Restricción incumplida.** Given que una alternativa supera la capacidad disponible o afecta un SLA. When se evalúa. Then la alternativa es descartada. |
| **Policy/Safety** | Como administrador necesito validar las recomendaciones antes de que puedan aplicarse sobre Kubernetes para evitar acciones inseguras. | **Escenario 1: Política aprobada.** Given que existe una recomendación técnicamente factible. When se evalúa mediante las políticas de seguridad y SLA. Then la recomendación es marcada como válida. **Escenario 2: Política rechazada.** Given que una recomendación incumple una política. When se valida. Then el sistema la rechaza y registra la causa. |
| **Recomendaciones** | Como operador necesito recibir recomendaciones trazables para conocer qué acción se propone, por qué se propone y qué impacto esperado tiene. | **Escenario 1: Recomendación válida.** Given que una alternativa fue validada. When finaliza el proceso de decisión. Then el sistema genera una recomendación con causa, recursos afectados, restricciones y métricas esperadas. |
| **Execution/Scheduler Adapter** | Como administrador necesito que las recomendaciones puedan ser preparadas para una ejecución controlada sobre Kubernetes. | **Escenario 1: Recommendation-Only.** Given que existe una recomendación validada. When se genera la salida del sistema. Then se presenta la acción propuesta sin modificar automáticamente el clúster. **Escenario 2: Acción no autorizada.** Given que una operación no posee autorización. When se intenta preparar su ejecución. Then el sistema bloquea la operación y registra el evento. |
| **Experimentación** | Como investigador necesito ejecutar experimentos controlados para comparar el comportamiento del sistema base frente a las recomendaciones de Green AI. | **Escenario 1: Experimento válido.** Given que existe una configuración experimental definida. When se ejecuta el escenario. Then el sistema registra las métricas de energía, rendimiento y SLA. **Escenario 2: Condiciones incomparables.** Given que las condiciones del experimento no cumplen los parámetros establecidos. When se inicia la evaluación. Then el sistema marca el experimento como no válido. |
| **Experimentación** | Como investigador necesito registrar los resultados de cada experimento para garantizar la reproducibilidad y trazabilidad. | **Escenario 1: Registro.** Given que un experimento ha finalizado. When se procesan sus resultados. Then se almacenan configuración, modelo, métricas y resultados asociados a una versión identificable. |
| **Visualización** | Como operador necesito visualizar el estado de la plataforma y los resultados de las recomendaciones mediante dashboards. | **Escenario 1: Dashboard disponible.** Given que existen métricas y resultados. When accedo al dashboard. Then puedo visualizar demanda, utilización, predicciones, recomendaciones y resultados experimentales. |
| **Seguridad y acceso** | Como administrador necesito controlar el acceso a las funciones de la plataforma según el rol del usuario. | **Escenario 1: Usuario autorizado.** Given que un usuario posee permisos suficientes. When accede a una función. Then el sistema permite la operación. **Escenario 2: Usuario no autorizado.** Given que el usuario no posee permisos. When intenta acceder. Then el sistema rechaza la solicitud y registra el intento. |

---

# **2.5 Cuadro de Requerimientos por PMV con IA**

Aquí no debemos repetir simplemente las historias de usuario. Esta tabla debe mostrar **qué se construye en cada Producto Mínimo Viable**, cuál es el requerimiento y qué función cumple la IA.

La división debe mantener los **tres PMV definidos para las 16 semanas**.

## **Cuadro de Requerimientos por PMV con IA**

| PMV | Módulo | Requerimiento | Función de IA | Resultado esperado |
| ----- | ----- | ----- | ----- | ----- |
| **PMV 1** | Observabilidad | El sistema debe recopilar métricas de infraestructura, Kubernetes y workloads. | La IA todavía no toma decisiones; se prepara la información que utilizarán los modelos. | Datos de CPU, memoria, workloads, latencia, throughput y errores disponibles. |
| **PMV 1** | Gestión de Datos | El sistema debe almacenar y procesar datos históricos y métricas recopiladas. | Preparación de datos para aprendizaje automático. | Dataset versionado y preparado para entrenamiento. |
| **PMV 1** | Procesamiento de Datos | El sistema debe realizar limpieza, transformación y preparación de las variables. | Identificación y preparación de variables relevantes para predicción. | Dataset procesado y reproducible. |
| **PMV 1** | Línea Base | El sistema debe establecer modelos de referencia para comparar posteriormente el desempeño predictivo. | Predicción mediante baseline simple, como persistencia o promedio móvil cuando corresponda. | MAE, RMSE y demás métricas de referencia registradas. |
| **PMV 1** | Visualización | El sistema debe mostrar métricas históricas y actuales mediante dashboards. | Visualización del comportamiento que posteriormente será utilizado por los modelos. | Dashboard funcional de observabilidad. |
| **PMV 2** | Predicción | El sistema debe generar predicciones de demanda computacional a corto plazo. | Aplicación de modelos de aprendizaje automático como Random Forest y XGBoost. | Predicciones para horizontes de 5, 15 y/o 30 minutos. |
| **PMV 2** | Evaluación de modelos | El sistema debe comparar los modelos candidatos utilizando métricas objetivas. | Selección experimental del modelo con mejor desempeño. | Modelo seleccionado y registrado en MLflow. |
| **PMV 2** | Decision Service | El sistema debe interpretar las predicciones considerando el contexto operativo. | Identificación de condiciones como incrementos de demanda o riesgo operacional. | Eventos de decisión generados. |
| **PMV 2** | Optimization Service | El sistema debe generar alternativas de asignación de recursos bajo restricciones. | Uso de predicciones como entrada del proceso de optimización. | Alternativas factibles de gestión de workloads. |
| **PMV 2** | Policy/Safety | El sistema debe validar que las alternativas respeten restricciones de seguridad, disponibilidad y SLA. | La IA no puede saltarse las políticas; las recomendaciones quedan condicionadas por las reglas de seguridad. | Alternativas aprobadas o rechazadas con trazabilidad. |
| **PMV 2** | Recommendation Service | El sistema debe generar recomendaciones explicables y trazables. | IA utilizada para apoyar la generación y priorización de recomendaciones a partir de predicciones y optimización. | Recomendaciones con justificación e impacto esperado. |
| **PMV 2** | Event-Driven | Los microservicios deben comunicarse mediante eventos definidos. | La IA participa en los procesos que generan y consumen eventos de predicción y decisión. | Flujo de eventos mediante RabbitMQ. |
| **PMV 3** | Experimentación | El sistema debe ejecutar experimentos controlados para evaluar las recomendaciones. | Comparación entre comportamiento base y comportamiento utilizando las recomendaciones. | Resultados experimentales reproducibles. |
| **PMV 3** | Energía | El sistema debe medir o estimar el consumo energético bajo una metodología definida. | Evaluación del impacto de las decisiones asistidas por predicción. | Energía y energía por unidad de trabajo registradas. |
| **PMV 3** | Rendimiento | El sistema debe evaluar latencia, throughput y utilización durante los experimentos. | La IA debe demostrar que las recomendaciones no producen degradación inaceptable. | Métricas de rendimiento comparables con el baseline. |
| **PMV 3** | SLA | El sistema debe verificar el cumplimiento de las restricciones de servicio. | Las recomendaciones se consideran válidas únicamente si mantienen los límites definidos. | Evidencia de cumplimiento o incumplimiento del SLA. |
| **PMV 3** | Recommendation-Only | El sistema debe presentar recomendaciones sin realizar cambios autónomos sobre infraestructura. | La IA funciona como sistema de apoyo a la decisión, no como controlador autónomo. | Recomendaciones revisables por el operador. |
| **PMV 3** | MLOps | El sistema debe registrar modelos, experimentos, métricas y versiones. | Seguimiento del ciclo de vida de los modelos. | Trazabilidad mediante MLflow, Git y almacenamiento de artefactos. |
| **PMV 3** | Seguridad | El sistema debe controlar acceso, autorización, secretos y operaciones sensibles. | Las decisiones generadas por IA están subordinadas a las políticas de seguridad. | Operación controlada y auditable. |

---

# **2.6 Requerimientos relacionados con el uso de IA**

Este apartado es importante porque **no debemos presentar la IA como si fuera responsable de todo el sistema**.

La IA tiene una función específica dentro de la arquitectura:

### **Función de la IA**

La inteligencia artificial será empleada principalmente para **predecir la demanda computacional futura** a partir de datos históricos y observaciones actuales de infraestructura y workloads. Las predicciones servirán como entrada para los procesos de decisión y optimización.

El proceso se plantea de la siguiente manera:

**Datos de infraestructura y workloads**

**Procesamiento y preparación**

**Modelo predictivo**

**Predicción de demanda**

**Evaluación de contexto**

**Optimización**

**Validación de políticas y restricciones**

**Generación de recomendación**

La última etapa no implica ejecución autónoma durante el MVP. El sistema operará inicialmente bajo el enfoque **Recommendation-Only**, de manera que las recomendaciones generadas por los modelos puedan ser evaluadas antes de cualquier eventual modificación de infraestructura.

# **2.7 Trazabilidad entre necesidades, requerimientos, PMV y validación**

Esta parte conecta directamente el punto 2 con los puntos posteriores del informe.

| Necesidad | Requerimiento | PMV | Evidencia | Validación |
| ----- | ----- | ----- | ----- | ----- |
| Conocer el comportamiento de la infraestructura | Recopilar métricas de infraestructura y workloads | PMV 1 | Prometheus, Node Exporter, kube-state-metrics, dashboards | Verificación de disponibilidad y continuidad de métricas |
| Disponer de datos adecuados para ML | Procesar, limpiar y versionar datos | PMV 1 | Dataset procesado | Validación de calidad de datos |
| Anticipar la demanda | Generar predicciones de demanda computacional | PMV 2 | Modelos y predicciones | MAE, RMSE, sMAPE |
| Seleccionar el modelo adecuado | Comparar modelos candidatos | PMV 2 | Experimentos registrados en MLflow | Evaluación temporal del desempeño |
| Generar alternativas de gestión | Optimizar recursos bajo restricciones | PMV 2 | Resultados del Optimization Service | Factibilidad y cumplimiento de restricciones |
| Evitar decisiones inseguras | Validar recomendaciones mediante políticas | PMV 2 | Registros del Policy/Safety Service | Verificación de políticas y SLA |
| Proporcionar apoyo al operador | Generar recomendaciones trazables | PMV 2 | Recommendation Service | Criterios funcionales y trazabilidad |
| Evaluar impacto energético | Comparar baseline y tratamiento | PMV 3 | Resultados experimentales | Energía, energía por trabajo y métricas ambientales |
| Mantener el rendimiento | Evaluar SLA y rendimiento | PMV 3 | Métricas experimentales | Latencia, throughput y SLA |
| Garantizar reproducibilidad | Registrar modelos y experimentos | PMV 3 | MLflow, Git y artefactos | Reproducción de experimentos |
| Mantener control humano | Operar inicialmente en Recommendation-Only | PMV 3 | Recomendaciones sin ejecución automática | Verificación de ausencia de cambios autónomos |

# **3\. Fundamentos matemáticos y científicos**

Esta sección sustenta el análisis de datos, la predicción de demanda, la optimización y la evaluación energética. El proyecto no considera Machine Learning como una caja negra; se requieren conocimientos matemáticos y estadísticos para definir variables, evaluar incertidumbre, medir error, comparar estrategias y formular decisiones bajo restricciones.

## **3.1 Estadística descriptiva**

Se emplearán media, mediana, desviación estándar, percentiles, rango intercuartílico y distribución de las métricas para caracterizar el comportamiento de CPU, memoria, throughput, latencia, réplicas y otras variables disponibles. Los percentiles serán especialmente útiles para describir períodos de alta demanda sin reducir el comportamiento a un único promedio.

## **3.2 Series temporales**

La demanda computacional presenta dependencia temporal. Por ello se analizarán tendencias, estacionalidad, autocorrelación, frecuencia de muestreo, ventanas históricas y comportamiento en picos. La división de entrenamiento, validación y prueba será temporal para evitar fuga de información entre períodos.

## **3.3 Probabilidad e incertidumbre**

La predicción representa una estimación sujeta a error. El análisis de incertidumbre permitirá identificar condiciones donde el modelo es menos confiable, especialmente en cambios bruscos de demanda y períodos anómalos.

## **3.4 Correlación y selección de variables**

Se analizarán relaciones entre utilización, requests, límites, réplicas, throughput, latencia, frecuencia de CPU cuando esté disponible y variables energéticas. La correlación será utilizada como herramienta exploratoria y no como prueba automática de causalidad.

## **3.5 Regresión y aprendizaje supervisado**

La variable objetivo inicial será la demanda computacional futura. Se evaluarán modelos de regresión supervisada que permitan estimar el valor futuro a partir de variables históricas y del estado actual de la infraestructura.

## **3.6 Funciones de pérdida y métricas de predicción**

Durante el entrenamiento se utilizarán funciones de pérdida apropiadas al modelo seleccionado. Para la evaluación se emplearán MAE, RMSE y sMAPE. MAE permite interpretar el error absoluto medio; RMSE penaliza más los errores grandes; y sMAPE permite una comparación relativa que debe interpretarse cuidadosamente cuando existen valores próximos a cero.

## **3.7 Normalización y objetivos multiatributo**

Cuando se combinen energía y desempeño dentro de una función objetivo, las magnitudes deberán normalizarse antes de agregarse. Los pesos utilizados deberán justificarse y someterse a análisis de sensibilidad para evitar que una conclusión dependa de una selección arbitraria.

## **3.8 Optimización matemática**

El Optimization Engine se formulará mediante variables de decisión, función objetivo y restricciones. Las variables pueden incluir número de réplicas, asignación de CPU y memoria, consolidación y otras acciones seguras. Las restricciones considerarán capacidad, requests y limits, disponibilidad, latencia, throughput, SLA y seguridad.

## **3.9 Fundamentos energéticos**

La energía se obtiene integrando potencia respecto del tiempo. En una medición directa, la energía del escenario se expresará en kWh. Para comparar escenarios con cargas diferentes se utilizará una unidad funcional, por ejemplo request procesado, workload ejecutado o unidad de trabajo definida experimentalmente.

Cuando no exista medición eléctrica directa, se utilizará una estimación documentada y, si es posible, calibrada mediante mediciones parciales. La utilización de CPU se considerará únicamente un proxy de último recurso, no una medición de energía.

*Tabla 2\. Aplicación de fundamentos matemáticos y científicos*

| Conocimiento | Aplicación matemática/científica | Evidencia |
| :---- | :---- | :---- |
| Estadística descriptiva | Caracterización de distribución, variabilidad y percentiles. | Reporte exploratorio. |
| Series temporales | Tendencia, estacionalidad, autocorrelación y ventanas. | Análisis temporal. |
| Regresión | Predicción de demanda futura. | Modelo entrenado. |
| Error predictivo | MAE, RMSE y sMAPE. | Comparación de modelos. |
| Optimización | Variables, restricciones y función objetivo. | Ejecuciones reproducibles. |
| Energía | Potencia, energía y energía por unidad funcional. | Medición o estimación documentada. |
| Análisis experimental | Comparación de estrategias y variabilidad entre repeticiones. | Resultados estadísticos. |

# **4\. Conocimientos de computación**

Los conocimientos de computación permiten implementar el tratamiento de datos, los modelos, las interfaces, la infraestructura y los mecanismos de control. La selección se realiza de acuerdo con las necesidades del problema y no como una lista genérica de tecnologías.

*Tabla 3\. Conocimientos de computación aplicados*

| Área de conocimiento | Aplicación en el proyecto | Contribución a la solución |
| :---- | :---- | :---- |
| 4.1 Algoritmos y estructuras de datos | Procesamiento de métricas, ventanas, reglas y alternativas. | Procesamiento eficiente y determinista. |
| 4.2 Bases de datos | Persistencia de experimentos, predicciones, recomendaciones y resultados. | Integridad, consulta y trazabilidad. |
| 4.3 Ingeniería de software | Modularidad, abstracción, pruebas, integración y mantenimiento. | Solución verificable y mantenible. |
| 4.4 Arquitectura de software | Separación de observación, datos, ML, optimización y políticas. | Desacoplamiento controlado. |
| 4.5 Inteligencia Artificial / Machine Learning | Preparación, entrenamiento, evaluación e inferencia. | Predicción de demanda. |
| 4.6 Redes y comunicaciones | REST/HTTP, eventos y comunicación entre componentes. | Integración controlada. |
| 4.7 Seguridad informática | Autenticación, autorización, RBAC, secretos y auditoría. | Protección de infraestructura. |
| 4.8 Sistemas distribuidos / Cloud | Contenedores, Kubernetes, scheduling y escalamiento. | Entorno experimental reproducible. |
| 4.9 Visualización y observabilidad | Dashboards, métricas y análisis de series temporales. | Supervisión y evidencia. |

## **4.1 Procesamiento y arquitectura de datos**

Prometheus se utilizará para las métricas de series temporales de infraestructura y workloads. PostgreSQL se utilizará para información estructurada que requiere integridad y relaciones. MinIO se utilizará para artefactos y datasets procesados, mientras que MLflow conservará el tracking y el ciclo de vida de modelos.

## **4.2 Sistemas distribuidos y Kubernetes**

Kubernetes constituye el entorno experimental para workloads y para los componentes contenedorizados de la plataforma. La interacción con el clúster se realizará mediante su API y cuentas de servicio con permisos mínimos. La solución no implementará un scheduler alternativo para reemplazar Kubernetes; añadirá una capa de decisión orientada al problema energético.

## **4.3 Observabilidad**

Prometheus, Node Exporter y kube-state-metrics permiten construir la base de telemetría. Grafana permitirá representar comportamiento de infraestructura, Machine Learning, energía y SLA. La observabilidad también se aplicará a la propia solución para medir el overhead que introduce.

# **5\. Conocimientos fundamentales de ingeniería**

El Proyecto 20 aplica conocimientos propios de Ingeniería de Sistemas e Ingeniería de Software para transformar requisitos y restricciones en una solución verificable. Esta sección constituye la base para justificar decisiones de arquitectura, calidad, seguridad, integración, configuración y validación.

* Ingeniería de requisitos.  
* Modelamiento y especificación del sistema.  
* Arquitectura y diseño de software.  
* Modularidad y separación de responsabilidades.  
* Patrones de integración y contratos.  
* Calidad de software.  
* Gestión de configuración y versiones.  
* Pruebas unitarias, integración, rendimiento y resiliencia.  
* Integración continua y trazabilidad.  
* Observabilidad y mantenibilidad.  
* Gestión de riesgos.  
* Seguridad y operación controlada.

## **5.1 Decisión arquitectónica**

Se adopta una arquitectura de microservicios orientada a eventos, desplegada sobre Kubernetes, con separación explícita entre observabilidad, procesamiento de datos, predicción, decisión, optimización, seguridad y ejecución. La decisión se justifica por la necesidad de escalar y aislar independientemente componentes con cargas y ciclos de procesamiento diferentes. RabbitMQ se utilizará como bus de eventos para procesos asíncronos, mientras Prometheus conservará las series temporales de alta frecuencia. El sistema operará inicialmente en Recommendation-Only, manteniendo separadas la predicción, la decisión, la validación de políticas y la futura ejecución.

## **5.2 Seguridad como condición de diseño**

La seguridad no se incorpora como una actividad posterior. El Policy/Safety Engine constituye una frontera obligatoria entre una alternativa calculada y cualquier acción sobre infraestructura. El diseño incorpora autenticación, autorización, RBAC, mínimo privilegio, secretos fuera del código, auditoría y rollback.

## **5.3 Calidad y mantenibilidad**

Los microservicios tendrán responsabilidades explícitas. La predicción no ejecutará acciones de infraestructura, la optimización no reemplazará la capa de políticas y la persistencia de series temporales no se confundirá con la base transaccional. Esta separación permite realizar pruebas y análisis de fallos por componente.

## **5.4 Gestión de riesgos**

*Tabla 4\. Riesgos técnicos y controles de ingeniería*

| ID | Riesgo | Probabilidad | Impacto | Control de ingeniería |
| :---- | :---- | :---- | :---- | :---- |
| R01 | Datos históricos insuficientes | Media | Alta | Instrumentar el entorno y generar workloads controlados. |
| R02 | Ausencia de medición energética directa | Media | Alta | Definir jerarquía de medición y documentar estimaciones. |
| R03 | Predicciones inexactas | Media | Alta | Comparar contra baseline y modelos candidatos. |
| R04 | Degradación de SLA | Baja/Media | Muy alta | Policy Engine y Recommendation-Only. |
| R05 | Drift del modelo | Media | Media/Alta | Monitorear distribución y error. |
| R06 | Overhead de la solución | Media | Media | Medir recursos consumidos por la plataforma. |
| R07 | Complejidad excesiva | Media | Media | Revisar la necesidad de cada componente. |
| R08 | Permisos excesivos en Kubernetes | Baja/Media | Muy alta | RBAC, ServiceAccounts y mínimo privilegio. |
| R09 | Fallas del entorno experimental | Media | Alta | Health checks, backups y aislamiento. |
| R10 | Resultados no reproducibles | Media | Alta | MLflow, configuración y datasets identificables. |

# **6\. Conocimientos especializados del dominio**

Los conocimientos especializados se seleccionan específicamente para el dominio de optimización energética de infraestructura computacional. Constituyen el conjunto que diferencia el proyecto de una aplicación genérica de Machine Learning.

## **6.1 Green Computing y eficiencia energética**

* Gestión energética de centros de datos e infraestructura computacional.  
* Medición de potencia y energía.  
* Energía por unidad de trabajo.  
* Estimación energética cuando no existe medición directa.  
* Cálculo de emisiones operacionales a partir de energía e intensidad de carbono.  
* Evaluación del overhead energético de la propia solución.  
* Uso de una unidad funcional para comparación entre escenarios.

## **6.2 Workload forecasting y series temporales**

* Predicción de demanda computacional a corto plazo.  
* Ventanas históricas y frecuencia de muestreo.  
* Análisis de picos y comportamiento anómalo.  
* Validación temporal y prevención de fuga de información.  
* Detección de degradación del modelo.

## **6.3 Machine Learning aplicado a gestión de recursos**

* Modelos de regresión para demanda futura.  
* Baselines de persistencia y promedio móvil cuando sean pertinentes.  
* Random Forest Regressor y XGBoost como candidatos iniciales.  
* Evaluación mediante MAE, RMSE y sMAPE.  
* Análisis específico de períodos de alta demanda.

## **6.4 Optimización de workloads**

* Consolidación de cargas.  
* Redistribución de workloads.  
* Scaling de réplicas.  
* Asignación de CPU y memoria.  
* Evaluación de alternativas bajo restricciones.  
* Análisis de compromiso entre energía y desempeño.

## **6.5 Autoscaling y resource management**

El sistema considerará mecanismos nativos de Kubernetes como referencia operacional, pero la propuesta no se limitará al autoscaling reactivo. El componente predictivo buscará anticipar demanda y alimentar una evaluación de alternativas. La comparación experimental determinará si la información predictiva aporta valor frente a la estrategia convencional.

## **6.6 SLA, QoS y restricciones de servicio**

* Latencia.  
* Throughput.  
* Disponibilidad.  
* Errores.  
* Capacidad.  
* Requests y limits.  
* Restricciones de SLA.  
* Condiciones de seguridad para cualquier acción.

## **6.7 MLOps**

* Versionado de datos y modelos.  
* Tracking de experimentos.  
* Registro de parámetros y métricas.  
* Monitoreo de inferencia.  
* Detección de drift.  
* Retraining controlado.  
* Gestión de artefactos y reproducibilidad.

## **6.8 Policy Engine y safety layer**

La capa de políticas evalúa si una alternativa técnicamente eficiente también es admisible desde la perspectiva de capacidad, disponibilidad, rendimiento y seguridad. La recomendación solo podrá pasar a una futura ejecución cuando todas las políticas requeridas sean satisfechas.

## **6.9 Sistemas cloud-native y Kubernetes**

* Contenedorización.  
* Namespaces.  
* ServiceAccounts.  
* RBAC.  
* Scheduling.  
* Observabilidad.  
* Integración mediante API.  
* Aislamiento del entorno experimental.

## **6.10 Sostenibilidad de sistemas computacionales**

La sostenibilidad se abordará mediante la medición de energía total y energía por unidad funcional. Como referencia técnica se considerará Software Carbon Intensity, normalizado como ISO/IEC 21031:2024, para organizar la relación entre energía, intensidad de carbono, emisiones incorporadas y unidad funcional \[13\]. El proyecto no declarará conformidad formal con la norma salvo que se realice una evaluación de conformidad.

# **7\. Selección y justificación de metodologías y tecnologías**

La selección de metodologías y tecnologías se realiza como una decisión de ingeniería. El criterio no es la popularidad de una herramienta, sino su adecuación al problema, la capacidad de generar evidencia, la reproducibilidad, la integración con el entorno universitario y la complejidad operacional que introduce.

## **7.1 Escala de evaluación**

*Tabla 5\. Escala multicriterio*

| Puntuación | Interpretación |
| :---- | :---- |
| 1 | Muy baja |
| 2 | Baja |
| 3 | Media |
| 4 | Alta |
| 5 | Muy alta |

Las puntuaciones representan juicio de ingeniería aplicado al Proyecto 20 y no una medida absoluta de calidad de las metodologías o tecnologías.

## **7.2 Selección de metodología de desarrollo**

### **Scrum**

**Scrum** es un marco de trabajo ágil orientado al desarrollo incremental e iterativo de productos complejos. El trabajo se organiza en períodos de duración definida denominados **Sprints**, dentro de los cuales el equipo planifica, desarrolla, verifica y presenta un incremento del producto.

Scrum utiliza elementos como el **Product Backlog**, que contiene las necesidades y funcionalidades pendientes; el **Sprint Backlog**, que representa el trabajo seleccionado para el Sprint; y el **Increment**, correspondiente al resultado potencialmente utilizable producido durante el Sprint.

Para el presente proyecto, Scrum resulta relevante porque permite organizar el desarrollo tecnológico en incrementos verificables. Por ejemplo, un Sprint puede concentrarse en la implementación de la observabilidad, otro en el pipeline de datos, otro en los modelos predictivos y posteriormente en el motor de optimización.

Una característica importante de Scrum es la incorporación de ciclos de **inspección y adaptación**. Al finalizar cada Sprint se puede revisar el resultado obtenido, identificar problemas técnicos y modificar las actividades siguientes. Esto es especialmente importante en un proyecto de investigación aplicada, debido a que los resultados obtenidos durante el análisis de datos o la evaluación de Machine Learning pueden modificar decisiones posteriores.

En este proyecto, Scrum también permite relacionar los **Sprints con los PMV**, los resultados verificables y las evidencias de ingeniería.

### **Kanban**

**Kanban** es un método de gestión del trabajo basado en la visualización del flujo de actividades y en la limitación del trabajo en progreso (**WIP, Work in Progress**). Su objetivo principal es controlar y mejorar continuamente el flujo de trabajo.

En Kanban, las actividades se representan normalmente mediante un tablero compuesto por estados como:

* Pendiente.  
* En análisis.  
* En desarrollo.  
* En validación.  
* Completado.

A diferencia de Scrum, Kanban no requiere necesariamente trabajar mediante iteraciones de duración fija. Las actividades pueden incorporarse y completarse de acuerdo con la capacidad disponible del equipo y las prioridades establecidas.

Para este proyecto, Kanban podría utilizarse para gestionar actividades de investigación y desarrollo que presenten un flujo variable, por ejemplo, correcciones, análisis de datos, documentación, experimentos adicionales o actividades derivadas de resultados inesperados.

Su principal ventaja para este contexto es la flexibilidad para incorporar nuevas actividades sin esperar necesariamente al inicio de un nuevo Sprint. Sin embargo, presenta una menor estructura formal para relacionar períodos de desarrollo, revisiones y entregables incrementales cuando se compara con Scrum.

### **Waterfall**

**Waterfall**, o modelo en cascada, es un enfoque secuencial de desarrollo en el que el proyecto se divide en etapas que se ejecutan siguiendo una planificación previamente definida. Las etapas normalmente incluyen actividades como análisis de requisitos, diseño, implementación, pruebas, despliegue y mantenimiento.

La característica principal de este modelo es que cada fase se completa antes de avanzar a la siguiente. Por ello, los requisitos y especificaciones suelen definirse con mayor detalle al inicio del proyecto.

Para el presente proyecto, Waterfall ofrece ventajas en situaciones donde los requisitos son estables y se necesita mantener un control estricto sobre el alcance y la documentación. También puede facilitar la planificación anticipada de entregables y actividades.

Sin embargo, el proyecto incorpora componentes experimentales, especialmente en el desarrollo de Machine Learning, optimización y medición energética. Los resultados de estas actividades no pueden conocerse completamente antes de ejecutar los experimentos. Por ejemplo, el modelo que finalmente presente mejor desempeño no puede determinarse de manera válida únicamente mediante una decisión inicial, sino que debe establecerse mediante evaluación experimental.

Por esta razón, un enfoque completamente secuencial puede presentar dificultades para responder a resultados inesperados o modificar decisiones técnicas durante el desarrollo.

*Tabla 6\. Evaluación de metodologías de desarrollo*

| Criterio | Scrum | Kanban | Waterfall |
| :---- | :---- | :---- | :---- |
| Desarrollo incremental | 5 | 5 | 2 |
| Adaptación ante cambios | 5 | 5 | 2 |
| Entregables verificables | 5 | 4 | 4 |
| Adecuación experimental | 5 | 4 | 2 |
| Control del alcance | 4 | 4 | 5 |
| Integración con investigación | 5 | 4 | 3 |
| TOTAL | 29 | 26 | 18 |

Se selecciona Scrum con 29 puntos. El proyecto presenta incertidumbres que se resolverán progresivamente: disponibilidad y calidad de datos, variable objetivo, horizonte de predicción, modelo final, formulación del optimizador y condiciones de medición energética. Scrum proporciona iteraciones, inspección y adaptación, por lo que se utilizará como marco de gestión del desarrollo \[1\].

## **7.3 Selección de metodología para Machine Learning**

### **CRISP-DM**

**CRISP-DM (Cross-Industry Standard Process for Data Mining)** es una metodología estructurada para proyectos de minería de datos y Machine Learning. Organiza el trabajo en seis fases principales:

1. Comprensión del negocio.  
2. Comprensión de los datos.  
3. Preparación de los datos.  
4. Modelado.  
5. Evaluación.  
6. Despliegue.

Una característica importante de CRISP-DM es que el proceso no necesariamente es estrictamente secuencial. Los resultados obtenidos durante una fase pueden generar la necesidad de regresar a una fase anterior. Por ejemplo, si durante el modelado se identifica que las variables disponibles no permiten obtener predicciones adecuadas, puede ser necesario regresar a la preparación o comprensión de los datos.

Para el presente proyecto, CRISP-DM resulta adecuado porque permite relacionar directamente el problema de ingeniería con el desarrollo del modelo predictivo. La metodología permite partir de la necesidad de predecir la demanda computacional, analizar las métricas disponibles, preparar las series temporales, entrenar modelos, evaluar su desempeño y posteriormente incorporar el modelo seleccionado al sistema.

Además, su carácter iterativo resulta apropiado para la investigación experimental, debido a que el desempeño de los modelos puede conducir a modificaciones en las variables, ventanas temporales, algoritmos o parámetros utilizados.

### **TDSP**

**TDSP (Team Data Science Process)** es un proceso estructurado para proyectos de ciencia de datos que proporciona una organización sistemática de las actividades, roles, artefactos y prácticas necesarias para desarrollar soluciones basadas en datos.

TDSP contempla actividades relacionadas con:

* Comprensión del negocio.  
* Adquisición y comprensión de los datos.  
* Modelado.  
* Despliegue.  
* Aceptación de la solución.

Además del ciclo de desarrollo, TDSP enfatiza la organización del proyecto, la documentación, la estructura de los artefactos y la reproducibilidad. Esto resulta útil cuando participan diferentes integrantes o cuando se requiere mantener una estructura consistente para datos, modelos, experimentos y resultados.

En el presente proyecto, TDSP puede contribuir especialmente en la organización de los datasets, experimentos, modelos y artefactos de Machine Learning. También resulta compatible con herramientas como **MLflow**, utilizadas para registrar experimentos, métricas, parámetros y versiones de modelos.

Sin embargo, para este proyecto se considera menos adecuado que CRISP-DM debido a que el foco principal está en la investigación experimental del forecasting y no solamente en la organización integral de un proceso de ciencia de datos.

### **SEMMA**

**SEMMA (Sample, Explore, Modify, Model, Assess)** es una metodología desarrollada para organizar proyectos de minería de datos mediante cinco actividades principales:

1. **Sample:** selección de una muestra representativa de los datos.  
2. **Explore:** exploración y análisis de los datos.  
3. **Modify:** transformación y preparación de variables.  
4. **Model:** construcción de modelos.  
5. **Assess:** evaluación de los resultados.

SEMMA proporciona una estructura clara para el tratamiento de datos y la construcción de modelos. Su fortaleza se encuentra principalmente en las actividades de exploración, transformación, modelado y evaluación.

Para el presente proyecto, SEMMA puede utilizarse como referencia para las actividades de preparación y modelado. Sin embargo, presenta una cobertura menor respecto a la comprensión del problema de ingeniería, la integración de los resultados con el sistema completo y la gestión del ciclo de vida del modelo.

Por esta razón, aunque resulta útil para estructurar las actividades analíticas, presenta una menor adecuación como metodología principal para el proyecto.

*Tabla 7\. Evaluación de metodologías de Machine Learning*

| Criterio | CRISP-DM | TDSP | SEMMA |
| :---- | :---- | :---- | :---- |
| Comprensión del problema | 5 | 4 | 3 |
| Comprensión y preparación de datos | 5 | 5 | 5 |
| Modelado y evaluación | 5 | 5 | 5 |
| Adecuación a series temporales | 5 | 4 | 4 |
| Integración con experimentación | 5 | 4 | 3 |
| Adaptación al entorno universitario | 5 | 4 | 4 |
| Reproducibilidad | 5 | 5 | 4 |
| TOTAL | 35 | 31 | 28 |

Se selecciona CRISP-DM con 35 puntos como estructura principal del ciclo de datos y Machine Learning. Se adaptará a series temporales, manteniendo separación temporal entre entrenamiento, validación y prueba. TDSP se utilizará como referencia complementaria para prácticas de proyecto, estructura de artefactos y despliegue de soluciones predictivas; Microsoft describe TDSP como un ciclo iterativo con comprensión del problema, adquisición y comprensión de datos, modelado, despliegue y aceptación \[14\].

La selección no implica que CRISP-DM resuelva por sí sola el ciclo operativo del modelo. Por ello se complementará con MLOps.

## **7.4 Selección del enfoque de validación**

#### **Experimento controlado**

El **experimento controlado** consiste en comparar una condición de referencia con una condición de tratamiento bajo condiciones previamente definidas y controladas. En el presente proyecto, la condición de referencia corresponde al **baseline**, mientras que el tratamiento corresponde a la estrategia predictiva propuesta.

El baseline representa la forma convencional de gestión de los workloads definida para el experimento, mientras que el tratamiento incorpora el componente predictivo y el motor de optimización.

El experimento deberá controlar, en la medida de lo posible, variables como:

* Hardware utilizado.  
* Configuración del clúster Kubernetes.  
* Workloads ejecutados.  
* Cantidad y características de las cargas.  
* Duración de cada prueba.  
* Condiciones iniciales.  
* Recursos asignados.  
* Patrones de demanda.  
* Condiciones de ejecución.

La comparación permitirá analizar variables dependientes como:

* Energía consumida.  
* Energía por unidad de trabajo.  
* Utilización de recursos.  
* Latencia.  
* Throughput.  
* Disponibilidad.  
* Cumplimiento del SLA.  
* Overhead introducido por la solución.

Este enfoque permite establecer una relación más clara entre la estrategia aplicada y los resultados observados, siempre que las condiciones experimentales sean suficientemente controladas.

Para este proyecto, el experimento controlado resulta especialmente apropiado porque permite comparar directamente el comportamiento del baseline frente a la estrategia predictiva bajo escenarios equivalentes.

---

#### **Enfoque cuasi-experimental**

El **enfoque cuasi-experimental** busca evaluar los efectos de una intervención mediante la comparación de condiciones antes y después, entre grupos o entre escenarios, pero sin disponer necesariamente de un control experimental completo o de una asignación aleatoria.

En el contexto del proyecto, podría utilizarse, por ejemplo, para comparar el comportamiento de una infraestructura antes y después de incorporar el mecanismo predictivo, o para comparar diferentes grupos de workloads cuando no sea posible controlar completamente las condiciones de ejecución.

Su principal ventaja es que puede aplicarse en entornos donde el control absoluto de las variables resulta difícil. Esto puede ser relevante en una infraestructura universitaria compartida, donde pueden existir variaciones de carga, disponibilidad de recursos u otras condiciones externas.

Sin embargo, esta característica también dificulta la atribución directa de los resultados. Si se observa una reducción de consumo energético después de introducir la estrategia predictiva, podría existir incertidumbre respecto a si la mejora fue causada exclusivamente por la solución o por otros cambios ocurridos durante el período de observación.

Por esta razón, el enfoque cuasi-experimental obtiene una puntuación inferior en control de variables y atribución de resultados.

---

#### **Simulación**

La **simulación** consiste en representar mediante un modelo computacional el comportamiento de una infraestructura, workload o estrategia de gestión, sin ejecutar necesariamente todas las condiciones directamente sobre la infraestructura física.

La simulación puede ser útil para explorar diferentes configuraciones, escenarios de demanda y políticas de asignación de recursos antes de realizar experimentos sobre el entorno real.

En este proyecto, una simulación podría utilizarse como mecanismo complementario para explorar escenarios que sean difíciles, costosos o riesgosos de ejecutar directamente sobre Kubernetes.

Sin embargo, la simulación presenta una limitación importante para el objetivo principal del proyecto: **la medición directa del consumo energético**. Un modelo simulado puede representar el comportamiento energético, pero la validez de dicha representación dependerá de la calidad del modelo y de los parámetros utilizados.

Por esta razón, la simulación no se considera como mecanismo principal para determinar el impacto energético real de la solución. Puede utilizarse como apoyo para explorar escenarios, probar restricciones o analizar comportamientos antes de la ejecución experimental.

*Tabla 8\. Evaluación del enfoque de validación*

| Criterio | Experimento controlado | Cuasi-experimental | Simulación |
| :---- | :---- | :---- | :---- |
| Comparación con baseline | 5 | 5 | 4 |
| Control de variables | 5 | 3 | 5 |
| Reproducibilidad | 5 | 4 | 5 |
| Aplicabilidad universitaria | 5 | 4 | 5 |
| Medición de energía | 5 | 4 | 2 |
| Evaluación de SLA y rendimiento | 5 | 4 | 3 |
| Atribución de resultados | 5 | 3 | 3 |
| TOTAL | 35 | 27 | 27 |

Se selecciona el experimento controlado con 35 puntos. La hipótesis requiere comparar una estrategia convencional con una estrategia predictiva bajo condiciones equivalentes. Por ello se controlarán hardware, workload, duración, aplicación, configuración y condiciones de prueba.

## **7.5 Selección del enfoque MLOps**

### **MLOps estructurado**

El **MLOps estructurado** corresponde a un enfoque sistemático para gestionar el ciclo de vida de los modelos de Machine Learning, integrando las actividades de desarrollo, experimentación, despliegue, monitoreo y mantenimiento.

En este enfoque, los modelos no se consideran artefactos aislados. Cada modelo se relaciona con los datos, código, parámetros, métricas y resultados utilizados durante su construcción.

Para el presente proyecto, el enfoque MLOps estructurado permitirá gestionar:

* Versiones de datasets.  
* Versiones de modelos.  
* Parámetros de entrenamiento.  
* Métricas de evaluación.  
* Experimentos.  
* Artefactos generados.  
* Resultados de inferencia.  
* Historial de modelos.  
* Cambios en el desempeño.  
* Detección de posibles fenómenos de drift.

La implementación utilizará **MLflow** para el seguimiento de experimentos y modelos, mientras que **MinIO** podrá utilizarse para conservar datasets y artefactos. El código permanecerá versionado mediante Git.

Este enfoque también facilita la reproducibilidad de los experimentos. Por ejemplo, si XGBoost obtiene mejores resultados que Random Forest, deberá ser posible identificar qué dataset, características, parámetros y configuración produjeron dicho resultado.

Por estas características, MLOps estructurado presenta la mayor adecuación para un proyecto experimental de Machine Learning.

---

### **Gestión manual**

La **gestión manual** consiste en administrar los modelos, datasets, experimentos y resultados mediante procedimientos realizados directamente por los integrantes del equipo, utilizando archivos, carpetas, hojas de cálculo, scripts y registros independientes.

Este enfoque puede resultar suficiente para experimentos pequeños o pruebas exploratorias iniciales. Sin embargo, conforme aumenta la cantidad de modelos y experimentos, puede producir problemas de trazabilidad y reproducibilidad.

En el contexto del proyecto, una gestión completamente manual podría dificultar la identificación de:

* Qué versión del dataset fue utilizada.  
* Qué parámetros produjo determinado resultado.  
* Qué versión del código generó un modelo.  
* Qué modelo se encontraba desplegado.  
* Qué experimento produjo una determinada métrica.  
* Cuándo se produjo una degradación del desempeño.

También presenta dificultades para implementar mecanismos sistemáticos de detección de drift y monitoreo continuo.

Por estas razones, se considera una alternativa de menor adecuación para el proyecto.

---

### **Despliegue tradicional**

El **despliegue tradicional** se centra principalmente en entrenar un modelo y posteriormente incorporarlo a una aplicación o servicio mediante un proceso de despliegue definido.

Su principal objetivo es llevar el modelo desde el entorno de desarrollo hacia un entorno de ejecución. Sin embargo, el seguimiento integral del ciclo de vida del modelo puede ser limitado en comparación con un enfoque MLOps estructurado.

En este proyecto, el despliegue tradicional permitiría poner en funcionamiento el modelo seleccionado dentro del **Prediction Service**, pero no necesariamente proporcionaría por sí mismo mecanismos suficientes para administrar de manera sistemática todos los experimentos, versiones, métricas y cambios de distribución de los datos.

Por esta razón, puede resultar útil como mecanismo técnico de despliegue, pero no constituye el enfoque principal recomendado para administrar el ciclo de vida completo del Machine Learning.

*Tabla 9\. Evaluación del enfoque MLOps*

| Criterio | MLOps estructurado | Gestión manual | Despliegue tradicional |
| :---- | :---- | :---- | :---- |
| Reproducibilidad | 5 | 2 | 3 |
| Registro de modelos | 5 | 2 | 3 |
| Seguimiento de métricas | 5 | 3 | 3 |
| Versionado | 5 | 2 | 3 |
| Monitoreo | 5 | 2 | 3 |
| Detección de drift | 5 | 1 | 2 |
| Adecuación experimental | 5 | 3 | 4 |
| TOTAL | 35 | 15 | 21 |

Se selecciona MLOps estructurado con 35 puntos. La literatura señala que operacionalizar Machine Learning requiere gestionar datos, modelos, infraestructura, monitoreo, versionado y mantenimiento como partes de un mismo sistema \[2\]. Una revisión arquitectónica reciente de 93 estudios identifica componentes, procesos, herramientas y roles recurrentes en sistemas MLOps \[3\].

## **7.6 Selección de arquitectura**

### **Microservicios orientados a eventos \+ eventos**

La arquitectura de **microservicios orientados a eventos** organiza el sistema como un conjunto de servicios independientes, cada uno responsable de una capacidad funcional específica, complementando la comunicación mediante APIs con mecanismos de comunicación asíncrona basados en eventos.

En el presente proyecto, esta arquitectura permite separar las principales responsabilidades del sistema en componentes independientes, tales como:

* Monitoring Service.  
* Data Processing Service.  
* Prediction Service.  
* Decision Service.  
* Optimization Service.  
* Policy/Safety Service.  
* Recommendation Service.  
* Execution/Scheduler Adapter.  
* Experiment Service.

Cada microservicio posee una responsabilidad delimitada y puede desarrollarse, probarse y desplegarse independientemente de los demás.

La comunicación síncrona se realizará mediante APIs REST cuando una operación requiera una respuesta inmediata. Para procesos asíncronos se utilizará RabbitMQ como mecanismo de mensajería.

Entre los eventos considerados se encuentran:

* `METRICS_AVAILABLE`.  
* `PREDICTION_READY`.  
* `DEMAND_SPIKE`.  
* `SLA_RISK`.  
* `OPTIMIZATION_REQUESTED`.  
* `POLICY_VALIDATED`.  
* `RECOMMENDATION_READY`.

Kubernetes será utilizado como plataforma de despliegue y administración de los microservicios.

Esta arquitectura permite separar claramente el proceso de observación, procesamiento, predicción, decisión, optimización, validación de políticas y generación de recomendaciones. Además, permite mantener el modelo predictivo aislado de la infraestructura, evitando que el Prediction Service tenga acceso directo al clúster Kubernetes.

Para el proyecto, la interacción con Kubernetes se concentrará en el **Execution/Scheduler Adapter**, manteniendo inicialmente el sistema bajo el modelo **Recommendation-Only**.

---

### **Microservicios**

La arquitectura de **microservicios** divide la aplicación en servicios independientes que representan capacidades funcionales específicas. Cada servicio posee una responsabilidad definida y puede desplegarse y escalarse de manera independiente.

En esta alternativa, los servicios pueden comunicarse mediante APIs REST u otros mecanismos de comunicación entre servicios. Sin embargo, la arquitectura no requiere necesariamente que la comunicación principal se base en eventos.

Su principal ventaja es la separación de responsabilidades y la posibilidad de escalar individualmente los componentes que presenten mayores necesidades de procesamiento.

Para este proyecto, por ejemplo, el Prediction Service podría escalar independientemente del Recommendation Service o del Experiment Service.

Sin embargo, una implementación basada únicamente en microservicios puede requerir una mayor cantidad de comunicación síncrona. Esto puede incrementar el acoplamiento operacional, la cantidad de dependencias entre servicios y la dificultad para diagnosticar problemas distribuidos.

Por esta razón, aunque constituye una alternativa adecuada para la solución, obtiene una valoración inferior respecto a la arquitectura que combina microservicios con comunicación orientada a eventos.

---

### **Event-Driven distribuida**

La arquitectura **Event-Driven distribuida** organiza el funcionamiento del sistema alrededor de eventos que representan cambios de estado o acontecimientos relevantes.

En este enfoque, los componentes productores generan eventos y los consumidores reaccionan ante ellos sin requerir necesariamente una comunicación directa entre ambos.

Para el proyecto, un evento como `PREDICTION_READY` podría indicar que una nueva predicción se encuentra disponible para que el Decision Service evalúe la situación. De manera similar, `POLICY_VALIDATED` podría indicar que una alternativa de optimización ha superado las restricciones definidas.

Este enfoque proporciona un alto nivel de desacoplamiento y facilita la incorporación de nuevos consumidores de eventos. También resulta adecuado para procesos asíncronos y sistemas que necesitan reaccionar ante cambios de estado.

Sin embargo, una arquitectura predominantemente Event-Driven puede incrementar la dificultad para rastrear una operación completa cuando participan múltiples productores y consumidores. La depuración y observabilidad requieren mecanismos adicionales de trazabilidad distribuida, correlación de eventos y registro de estados.

Por ello, en el presente proyecto se considera más apropiado utilizar eventos como **mecanismo complementario dentro de una arquitectura de microservicios**, en lugar de convertir todo el sistema en un flujo exclusivamente orientado a eventos.

*Tabla 10\. Evaluación de alternativas arquitectónicas*

| Criterio | Microservicios orientados a eventos \+ eventos | Microservicios | Event-Driven distribuida |
| :---- | :---- | :---- | :---- |
| Complejidad operacional | 5 | 2 | 3 |
| Adecuación a prototipo universitario | 5 | 3 | 4 |
| Separación de responsabilidades | 5 | 5 | 5 |
| Escalabilidad independiente | 4 | 5 | 5 |
| Facilidad de depuración | 5 | 3 | 3 |
| Experimentación | 5 | 4 | 4 |
| Mantenibilidad inicial | 5 | 3 | 3 |
| TOTAL | 34 | 25 | 27 |

Se selecciona la arquitectura de microservicios orientada a eventos con 29 puntos. La decisión responde a la necesidad de desacoplar responsabilidades con diferentes cargas de trabajo y permitir escalamiento y evolución independiente de observabilidad, predicción, decisión, optimización y experimentación. Kubernetes proporciona el plano de despliegue y aislamiento mediante namespaces, mientras RabbitMQ proporciona el mecanismo de comunicación asíncrona. La complejidad adicional se controla mediante límites de servicio explícitos, contratos de API y eventos versionados, observabilidad, RBAC y un alcance inicial Recommendation-Only.

## **7.6.1 Principios de la arquitectura seleccionada**

## La arquitectura seleccionada se rige por cinco principios: (1) responsabilidad única por microservicio; (2) comunicación síncrona solo cuando se requiere respuesta inmediata; (3) eventos para desacoplar procesos asíncronos; (4) observabilidad transversal de servicios, eventos, infraestructura y modelo; y (5) seguridad y autorización como frontera obligatoria antes de cualquier interacción con Kubernetes. El diseño evita que el Prediction Service ejecute acciones de infraestructura y concentra la interacción con el clúster en el Execution/Scheduler Adapter.

## **7.7 Selección tecnológica**

*Tabla 11\. Matriz tecnológica seleccionada*

| Componente | Tecnología seleccionada | Justificación |
| :---- | :---- | :---- |
| Backend y API | Python \+ FastAPI | Integración directa con ML, procesamiento científico y optimización. |
| Procesamiento | Pandas \+ NumPy | Preparación de datos y operaciones numéricas del volumen experimental previsto. |
| ML | scikit-learn \+ XGBoost | Comparación de modelos de regresión sin introducir complejidad de Deep Learning no justificada. |
| Observabilidad | Prometheus \+ Node Exporter \+ kube-state-metrics | Adecuados para métricas de infraestructura y Kubernetes. |
| Visualización | Grafana | Dashboards operativos, energéticos y de ML. |
| Persistencia | PostgreSQL | Relaciones, integridad y trazabilidad transaccional. |
| Artefactos | MinIO | Almacenamiento de objetos en entorno privado. |
| MLOps | MLflow | Tracking, registro de modelos y artefactos. |
| Mensajería | RabbitMQ | Procesamiento asíncrono selectivo y desacoplamiento controlado. |
| Orquestación | Kubernetes | Entorno realista para workloads y experimentación cloud-native. |
| Contenedores | Docker | Reproducibilidad del entorno de ejecución. |
| Optimización | Python \+ solver | Formulación de variables, restricciones y función objetivo. |
| Seguridad | Kubernetes RBAC \+ JWT \+ Secrets | Control de acceso y mínimo privilegio. |

# **8\. Aplicación de conocimientos al diseño de la solución**

Esta sección constituye la evidencia principal de AG-I07 porque muestra cómo los conocimientos seleccionados se convierten en decisiones concretas de diseño. El contenido técnico desarrollado anteriormente se integra aquí para demostrar la relación entre conocimiento, aplicación, componente y evidencia.

*Tabla 12\. Aplicación de conocimientos al diseño*

| Conocimiento | Aplicación en el proyecto | Componente / artefacto | Evidencia |
| :---- | :---- | :---- | :---- |
| Estadística y series temporales | Análisis de patrones, estacionalidad, ventanas históricas y preparación del dataset. | Data Processor / Feature Engineering | Dataset y análisis exploratorio. |
| Machine Learning | Modelo predictivo de demanda futura. | ML Engine | MAE, RMSE, sMAPE. |
| Optimización | Generación de decisiones de consolidación, redistribución o scaling bajo restricciones. | Optimization Engine | Función objetivo y escenarios. |
| Ingeniería de software | Requisitos, modularidad, pruebas, integración y mantenibilidad. | Microservicios y contratos | Pruebas y revisión estructural. |
| Arquitectura | Separación de adquisición, datos, ML, optimización, políticas y presentación. | Arquitectura distribuida por microservicios | Diagramas y despliegue. |
| Bases de datos | Persistencia de métricas procesadas, predicciones, recomendaciones y resultados. | PostgreSQL | Modelo lógico, relacional y físico. |
| Seguridad | RBAC, autenticación, autorización, secretos, auditoría y mínimo privilegio. | Policy/Safety Engine | Pruebas de seguridad y logs. |
| Sistemas distribuidos / Cloud | Despliegue y experimentación sobre Kubernetes y contenedores. | Kubernetes | Estado del clúster y workloads. |
| Green Computing | Medición de energía por unidad funcional. | Energy Evaluation | kWh y Wh/unidad. |
| MLOps | Tracking, registro, monitoreo y drift. | MLflow \+ monitoreo | Runs, modelos y reportes. |

## **8.1 Arquitectura general**

La arquitectura general se implementa como un conjunto de microservicios con responsabilidades explícitas: Monitoring Service, Data Processing Service, Prediction Service, Decision Service, Optimization Service, Policy/Safety Service, Recommendation Service, Execution/Scheduler Adapter y Experiment Service. Los servicios se despliegan en Kubernetes y se comunican mediante APIs REST para operaciones síncronas y RabbitMQ para eventos asíncronos. La interacción con Kubernetes se concentra en el Execution/Scheduler Adapter y nunca se concede al modelo predictivo acceso directo al clúster. Prometheus permanece como fuente de series temporales; el bus de eventos complementa la telemetría con señales operacionales como METRICS\_AVAILABLE, PREDICTION\_READY, DEMAND\_SPIKE, SLA\_RISK y RECOMMENDATION\_READY.

## **![][image1]**

Figura 1\. Diagrama de la Arquitectura general

## **8.2 Arquitectura lógica**

La arquitectura lógica se organiza alrededor del flujo de información desde la observación hasta la recomendación. Data Collector obtiene métricas; Data Processor las limpia; Feature Engineering genera variables; ML Engine produce predicciones; Optimization Engine evalúa alternativas; Policy/Safety Engine verifica restricciones; Recommendation Manager registra y presenta el resultado; Experiment Manager conserva el contexto de evaluación.

## **![][image2]**

Figura 2\. Arquitectura de componentes

## **8.3 Estructura interna**

*Tabla 13\. Estructura interna de la solución*

| Módulo | Responsabilidad | Entrada | Salida |
| :---- | :---- | :---- | :---- |
| Data Collector | Obtención de métricas. | Prometheus, Kubernetes y APIs. | Datos observados. |
| Data Processor | Limpieza, transformación y resampling. | Datos observados. | Dataset analítico. |
| Feature Engineering | Construcción de ventanas y variables. | Dataset temporal. | Features. |
| ML Engine | Entrenamiento, evaluación e inferencia. | Features. | Predicciones. |
| Optimization Engine | Evaluación de alternativas. | Predicción y estado. | Alternativas candidatas. |
| Policy/Safety Engine | Validación de restricciones. | Alternativas y políticas. | Alternativas permitidas o rechazadas. |
| Recommendation Manager | Registro y presentación. | Alternativa validada. | Recomendación trazable. |
| Scheduler Adapter | Interacción controlada con Kubernetes. | Recomendación aprobada. | Solicitud autorizada. |
| Experiment Manager | Gestión de escenarios y resultados. | Configuración experimental. | Resultados comparables. |

## **8.4 Arquitectura de datos**

*Tabla 14\. Arquitectura de datos*

| Dato | Fuente | Almacenamiento | Uso |
| :---- | :---- | :---- | :---- |
| CPU, memoria, red, estado de nodos | Node Exporter / Kubernetes | Prometheus | Observabilidad y forecasting. |
| Pods, réplicas, requests y limits | kube-state-metrics / Kubernetes | Prometheus | Contexto de workloads. |
| Requests, throughput, latencia y errores | Métricas de aplicación | Prometheus | Demanda y SLA. |
| Predicciones | ML Engine | PostgreSQL | Trazabilidad y evaluación. |
| Recomendaciones | Recommendation Manager | PostgreSQL | Auditoría y comparación. |
| Experimentos | Experiment Manager | PostgreSQL \+ MLflow | Reproducibilidad. |
| Modelos y datasets procesados | ML Engine / MLflow | MinIO | Conservación y despliegue. |

**![][image3]**

Figura 3\. Arquitectura de datos de flujo end-to-end

## **8.5 Modelo de datos**

*Tabla 15\. Entidades principales del modelo de datos*

| Entidad | Propósito |
| :---- | :---- |
| projects | Identificación del entorno experimental. |
| clusters | Configuración y metadatos del clúster. |
| nodes | Características de los nodos. |
| workloads | Identificación y configuración de workloads. |
| experiments | Condiciones y configuración del experimento. |
| models | Versión y metadatos del modelo. |
| predictions | Predicciones generadas. |
| optimization\_runs | Ejecuciones del optimizador. |
| recommendations | Recomendaciones producidas. |
| policy\_evaluations | Resultados de validación de restricciones. |
| energy\_measurements | Mediciones o estimaciones energéticas. |
| experiment\_results | Resultados consolidados. |
| audit\_events | Trazabilidad de decisiones y acciones. |

**![][image4]**

*Figura 14: Diseño del diagrama lógico*

## **8.6 Machine Learning aplicado**

*Tabla 16\. Diseño preliminar del componente predictivo*

| Elemento | Definición preliminar |
| :---- | :---- |
| Variable objetivo | Demanda computacional futura, priorizando CPU y complementando con memoria y requests según disponibilidad. |
| Horizontes | 5, 15 y 30 minutos; se seleccionará el horizonte útil para el ciclo de decisión. |
| Ventana histórica | Definida mediante análisis temporal, autocorrelación y pruebas comparativas. |
| Baseline | Persistencia o naive y promedio móvil cuando corresponda. |
| Modelos candidatos | Random Forest Regressor y XGBoost Regressor. |
| Métricas | MAE, RMSE, sMAPE y latencia de inferencia. |
| Validación | División temporal train, validation y test. |
| Drift | Monitoreo de cambios en distribución y degradación del error. |

No se incorporará Deep Learning inicialmente. LSTM, GRU o Transformers solo serán considerados si la estructura y cantidad de datos, la estacionalidad, el horizonte y la evidencia experimental muestran que los modelos iniciales son insuficientes. Esto evita introducir complejidad algorítmica sin justificación.

![][image5]

Figura 6\. Pipeline de Machine learning

## **8.7 MLOps aplicado**

*Tabla 17\. Aplicación de MLOps*

| Etapa | Implementación | Evidencia |
| :---- | :---- | :---- |
| Dataset | Identificación, metadatos y checksum cuando corresponda. | ID, período, variables y procedencia. |
| Entrenamiento | Scripts reproducibles en Python. | Parámetros y métricas. |
| Tracking | MLflow Tracking. | Run ID y artefactos. |
| Registro | MLflow Model Registry. | Versión y estado. |
| Inferencia | Servicio mediante FastAPI. | Endpoint, logs y latencia. |
| Monitoreo | Error, latencia, distribución y disponibilidad. | Dashboard y alertas. |
| Drift | Comparación de distribución y degradación del error. | Reporte. |
| Retraining | Proceso controlado bajo condición definida. | Nueva versión registrada. |

## **8.8 Motor de optimización**

*Tabla 18\. Formulación preliminar del Optimization Engine*

| Elemento | Definición |
| :---- | :---- |
| Variables de decisión | Número de réplicas, CPU/memoria, consolidación y otras acciones seguras. |
| Objetivo energético | Minimizar energía medida o estimada asociada al escenario. |
| Objetivos operativos | Minimizar penalizaciones de latencia, costo computacional y violaciones de SLA. |
| Restricciones | Capacidad, requests/limits, disponibilidad, latencia, throughput, SLA y seguridad. |
| Salida | Alternativas candidatas ordenadas según función objetivo. |
| Ejecución inicial | Recommendation-Only. |

## **![][image6]**

Figura 7\. Flujo de motores de optimización

## **8.9 Policy/Safety Engine y seguridad**

*Tabla 19\. Controles de seguridad y safety*

| Control | Implementación prevista |
| :---- | :---- |
| Autenticación | JWT para acceso a la API. |
| Autorización | RBAC por rol y operación. |
| Kubernetes RBAC | ServiceAccount con permisos mínimos. |
| Secrets | Kubernetes Secrets; credenciales fuera del código. |
| Comunicación segura | TLS y NetworkPolicies cuando correspondan. |
| Auditoría | Registro de predicción, recomendación, política y aprobación. |
| Rollback | Reversión obligatoria para futuras acciones automatizadas. |
| Modo inicial | Recommendation-Only. |

# **9\. Integración de conocimientos de ingeniería**

Esta sección demuestra que los conocimientos no se utilizan de forma aislada. El problema requiere integrar estadística, computación, ingeniería de software, arquitectura, Machine Learning, optimización, seguridad, sistemas distribuidos y Green Computing para producir una solución única.

La integración se materializa en una cadena funcional en la que cada conocimiento cumple una función específica. La estadística caracteriza la demanda; la computación permite capturar y procesar datos; Machine Learning estima la demanda futura; la optimización evalúa alternativas; la ingeniería de software estructura los componentes; la arquitectura define responsabilidades e interfaces; la seguridad controla las acciones; Kubernetes proporciona el entorno de ejecución; y Green Computing define la forma de medir el impacto.

*Tabla 20\. Integración de conocimientos*

| Etapa | Conocimiento integrado | Resultado | Evidencia |
| :---- | :---- | :---- | :---- |
| Observación | Computación \+ observabilidad | Estado medido de infraestructura y workloads. | Métricas y dashboards. |
| Caracterización | Estadística \+ series temporales | Dataset y patrones de demanda. | EDA y análisis temporal. |
| Predicción | ML \+ estadística | Demanda futura estimada. | Métricas predictivas. |
| Decisión | Optimización \+ restricciones | Alternativas factibles. | Ejecución del optimizador. |
| Control | Seguridad \+ ingeniería | Alternativa admisible. | Policy/Safety Engine. |
| Operación | Arquitectura \+ Kubernetes | Recomendación o acción controlada. | Logs y estado del clúster. |
| Evaluación | Experimentación \+ Green Computing | Impacto energético y operativo. | Baseline versus tratamiento. |
| Ciclo de vida | MLOps \+ software | Reproducibilidad y mantenimiento. | MLflow y versiones. |

**![][image7]**

**Figura 8\. Integración de conocimiento de ingenieria**

## **9.1 Relación con la arquitectura**

La integración de conocimientos se refleja en la arquitectura. No existe un componente de Machine Learning aislado; el modelo recibe datos preparados, produce predicciones registradas, alimenta un optimizador y queda sujeto a políticas. La arquitectura, por tanto, materializa los conocimientos aplicados y permite observar sus interacciones.

## **9.2 Relación con la experimentación**

La integración también se demuestra mediante el diseño experimental. La calidad de una predicción no constituye por sí misma evidencia de mejora energética. El proyecto debe demostrar la cadena completa: calidad predictiva, calidad de la decisión, cumplimiento de restricciones y efecto observado en energía por unidad funcional, SLA y desempeño.

## **9.3 Cómo se trabajaron problemas similares**

Los antecedentes revisados muestran patrones metodológicos similares al problema del Proyecto 20\. Khan et al. abordaron forecasting de workload y estimación del estado energético utilizando trazas reales, mostrando la pertinencia de vincular predicción y gestión energética \[7\]. Ji et al. integraron predicción de workload con scheduling, gestión de recursos y migración, y validaron la propuesta mediante experimentos con trazas reales \[8\].

Sharma y Garg desarrollaron un enfoque basado en redes neuronales para scheduling energético de tareas en centros de datos cloud, evaluando conjuntamente makespan, consumo energético, cantidad de racks activos y overhead \[10\]. Este antecedente es relevante porque muestra que la evaluación debe considerar energía y desempeño, no únicamente la exactitud del algoritmo.

Beloglazov, Abawajy y Buyya establecieron principios de asignación y consolidación energéticamente eficiente considerando QoS \[9\]. Este antecedente es especialmente importante para el Proyecto 20 porque demuestra que la reducción energética no se obtiene simplemente moviendo cargas: la consolidación debe estar vinculada a cambios reales en la utilización de recursos y, cuando corresponda, a estados de menor consumo.

En MLOps, Kreuzberger, Kühl y Hirschl sistematizaron componentes, principios, roles y arquitectura del ciclo de vida de Machine Learning \[2\]. Najafabadi et al. ampliaron esta perspectiva mediante un mapeo sistemático de 93 estudios y la identificación de componentes arquitectónicos y pasos de proceso \[3\]. Estos antecedentes justifican que el modelo predictivo, sus datos, monitoreo, versiones y operación sean tratados como un sistema de ingeniería completo.

A partir de estos antecedentes, el Proyecto 20 adopta una adaptación específica para una infraestructura universitaria: entorno controlado, Recommendation-Only, predicción de corto plazo, optimización bajo restricciones, medición energética documentada y comparación experimental frente a baseline. No se copian resultados ni configuraciones de los antecedentes; se reutilizan patrones de ingeniería y se someten a validación en el entorno propio.

# **10\. Validación de la aplicación de conocimientos**

La validación debe responder a la pregunta: ¿cómo se determinará que los conocimientos aplicados fueron adecuados para producir una solución técnicamente válida? Para el Proyecto 20, la validación se realizará en cuatro dimensiones principales: software, Machine Learning, arquitectura e infraestructura y Green Computing.

## **10.1 Validación de software**

* Pruebas unitarias de componentes.  
* Pruebas de integración del pipeline y APIs.  
* Pruebas de rendimiento y latencia.  
* Verificación de observabilidad.  
* Pruebas de autenticación y autorización.  
* Verificación de trazabilidad y auditoría.  
* Pruebas de resiliencia y recuperación controlada.

## **10.2 Validación de Machine Learning**

* MAE.  
* RMSE.  
* sMAPE.  
* Comparación contra baseline de persistencia y promedio móvil cuando corresponda.  
* Análisis del error en períodos de alta demanda.  
* Estabilidad y robustez frente a variaciones del workload.  
* Detección y seguimiento de drift.  
* Latencia de inferencia.

## **10.3 Validación de arquitectura e infraestructura**

* Acoplamiento y cohesión.  
* Complejidad operacional.  
* Disponibilidad de componentes críticos.  
* Rendimiento y overhead.  
* Seguridad y mínimo privilegio.  
* Capacidad de rollback.  
* Observabilidad de la infraestructura y de la propia solución.

## **10.4 Validación Green Computing**

* Consumo energético total en kWh o estimación energética documentada.  
* Energía por unidad de trabajo.  
* Potencia media.  
* Utilización de recursos.  
* Número de nodos activos cuando sea una variable relevante.  
* Cumplimiento de SLA.  
* Latencia.  
* Throughput.  
* Disponibilidad.  
* Overhead energético y computacional de la propia solución.  
* Carbono operacional cuando se disponga de un factor de intensidad de carbono válido.

## **10.5 Diseño experimental**

*Tabla 21\. Diseño experimental de validación*

| Elemento | Definición |
| :---- | :---- |
| Baseline | Gestión convencional del workload sin predicción ni optimización propuesta. |
| Tratamiento | Predicción de demanda, optimización, Policy/Safety Engine y recomendación. |
| Escenarios | Baja carga, carga normal, alta carga, pico y comportamiento anómalo. |
| Variable independiente | Estrategia de gestión y configuración experimental. |
| Variables dependientes | Energía, energía por trabajo, carbono, SLA, latencia, throughput y utilización. |
| Variables de control | Hardware, workload, duración, aplicación, configuración y condiciones de prueba. |
| Repeticiones | Múltiples ejecuciones por escenario. |
| Resultado | Comparación técnica y estadística. |

## **10.6 Criterios de aceptación**

*Tabla 22\. Criterios de aceptación de la solución*

| Criterio | Condición de aceptación |
| :---- | :---- |
| Datos | Dataset documentado, procedencia conocida y calidad evaluada. |
| Modelo | Comparación contra baseline y métricas reportadas. |
| Optimización | Alternativas factibles bajo restricciones explícitas. |
| Seguridad | Políticas, permisos y controles verificados. |
| Recomendación | Trazable hasta predicción, restricciones y contexto. |
| Experimentación | Baseline y tratamiento ejecutados bajo condiciones comparables. |
| Energía | Método de medición o estimación documentado. |
| Servicio | SLA, latencia, throughput y disponibilidad evaluados. |
| Reproducibilidad | Experimentos, versiones y artefactos identificables. |

## **10.7 Principio de validez**

La eficacia energética no será declarada únicamente porque el prototipo funcione o porque el modelo alcance una determinada métrica predictiva. Solo podrá afirmarse una mejora cuando los resultados experimentales muestren una diferencia favorable en las métricas energéticas definidas y, simultáneamente, no exista una degradación inaceptable de SLA, latencia, throughput o disponibilidad.

La cadena de validación se establece como conocimiento aplicado, resultado observado y evidencia experimental. Esta trazabilidad permite determinar si la ingeniería aplicada fue adecuada y evita confundir funcionamiento técnico con eficacia científica.

# **11\. Implementación, evidencias y trazabilidad de ingeniería**

Este apartado integra los elementos del informe técnico anterior que no deben desaparecer, pero que no constituyen conocimientos independientes. Arquitectura física, despliegue, APIs, observabilidad, plan de pruebas, infraestructura, roadmap, entregables y evidencias se incorporan como material de implementación y demostración de que los conocimientos seleccionados se convierten en una solución ejecutable.

## **11.1 Arquitectura física y despliegue**

El despliegue se realizará en un entorno universitario controlado. Los componentes se empaquetarán como contenedores y se gestionarán mediante Kubernetes. La distribución física definitiva dependerá de la capacidad real del clúster y no deberá asumirse hasta completar el levantamiento de infraestructura.

*Tabla 23\. Despliegue previsto*

| Componente | Despliegue previsto |
| :---- | :---- |
| Kubernetes | Clúster experimental para todos los servicios y workloads. |
| Monitoring Service | Deployment en namespace de observabilidad. |
| Data Processing Service | Deployment escalable según volumen de telemetría. |
| Prediction Service | Deployment independiente para inferencia y API ML. |
| Decision / Optimization Services | Deployments independientes para decisión y optimización. |
| Policy/Safety Service | Deployment con controles de acceso reforzados. |
| Recommendation / Experiment Services | Deployments de gestión, trazabilidad y experimentación. |
| Prometheus / Grafana | Namespace de observabilidad. |

**![][image8]**

Figura 9\. Despliegue kubernetes por namespace

## **11.2 Arquitectura de comunicación y APIs**

La comunicación síncrona se realizará mediante REST/HTTP para consultas, administración y operaciones que requieran respuesta inmediata. La comunicación asíncrona se realizará mediante RabbitMQ como bus de eventos entre microservicios. Los eventos deberán contar con contratos versionados, identificador, timestamp, origen, tipo y payload documentado. Se evitarán dependencias directas innecesarias entre servicios y se establecerán políticas de reintento, idempotencia y manejo de fallos para los consumidores.

*Tabla 24\. Contratos de integración previstos*

| API o evento | Propósito | Tipo |
| :---- | :---- | :---- |
| /metrics | Consultar métricas procesadas. | REST / GET |
| /predictions | Generar o consultar predicciones. | REST / POST, GET |
| /models | Consultar versiones y estado de modelos. | REST / GET |
| /optimizations | Solicitar evaluación de alternativas. | REST / POST |
| /recommendations | Consultar y registrar recomendaciones. | REST / GET, POST |
| /policies/validate | Validar una acción contra políticas. | REST / POST |
| /experiments | Crear y consultar experimentos. | REST / POST, GET |
| METRICS\_AVAILABLE | Notificar disponibilidad de nuevas métricas. | Evento |
| PREDICTION\_READY | Notificar nueva predicción. | Evento |
| RECOMMENDATION\_READY | Notificar recomendación validada. | Evento |

La comunicación event-driven se utilizará para desacoplar procesos que no requieren una respuesta síncrona inmediata. Los eventos representan cambios de estado o disponibilidad de información; no sustituyen el almacenamiento de series temporales.

## **11.3 Observabilidad y SRE**

*Tabla 25\. Indicadores de observabilidad*

| Área | Indicadores |
| :---- | :---- |
| Disponibilidad | API, pipeline y componentes críticos. |
| Latencia | Consulta, predicción y generación de recomendación. |
| Rendimiento | Throughput de procesamiento y experimentos. |
| Machine Learning | MAE, RMSE, sMAPE, drift y latencia de inferencia. |
| Infraestructura | CPU, memoria, red, pods, nodos y eventos Kubernetes. |
| Energía | Potencia, kWh y energía por unidad de trabajo. |
| SLA | Latencia, errores, disponibilidad y violaciones. |
| Seguridad | Eventos de autenticación, autorización y operaciones sensibles. |
| Overhead | Recursos consumidos por la propia plataforma. |

## **11.4 Plan de pruebas**

*Tabla 26\. Plan de pruebas*

| Nivel | Qué se verifica | Evidencia |
| :---- | :---- | :---- |
| Unitarias | Procesamiento, features, reglas y cálculos. | Reporte de pruebas. |
| Integración | Prometheus, pipeline, ML, optimización y Policy Engine. | Ejecución integrada. |
| API | Contratos, autenticación, autorización y validaciones. | Pruebas de endpoints. |
| Rendimiento | Latencia y throughput. | Métricas bajo carga. |
| Seguridad | RBAC, secrets, permisos y exposición. | Resultados de pruebas. |
| Resiliencia | Fallas controladas y recuperación. | Logs y tiempos de recuperación. |
| Machine Learning | Calidad predictiva y comportamiento en picos. | MAE, RMSE, sMAPE y análisis. |
| Experimental | Repetibilidad y comparación. | Dataset y resultados. |

## **11.5 Requerimientos de información e infraestructura**

*Tabla 27\. Levantamiento previo de infraestructura*

| Recurso | Información a verificar | Decisión asociada |
| :---- | :---- | :---- |
| Nodos | Cantidad, CPU, memoria, almacenamiento y modelo de hardware. | Capacidad experimental. |
| Kubernetes | Versión, permisos y namespaces disponibles. | Alcance de integración. |
| Métricas | Retención, frecuencia y cobertura. | Horizonte y dataset. |
| Energía | Smart PDU, medidor, IPMI/Redfish u otra fuente. | Método de medición. |
| Workloads | Tipo, demanda y criticidad. | Escenarios experimentales. |
| Red | Latencia y capacidad. | Arquitectura de comunicación. |
| Almacenamiento | Capacidad y persistencia. | Retención de datos y artefactos. |
| Seguridad | RBAC, cuentas de servicio y políticas disponibles. | Nivel de automatización permitido. |

## **11.6 Entregables técnicos**

11. Especificación de requisitos del sistema.  
12. Matriz de selección metodológica.  
13. Matriz de selección tecnológica.  
14. Arquitectura lógica, física y de despliegue.  
15. Modelo lógico, relacional y físico de datos.  
16. Pipeline de adquisición y procesamiento de métricas.  
17. Dataset documentado para experimentación.  
18. Baselines predictivos.  
19. Modelos Random Forest y XGBoost evaluados.  
20. Modelo seleccionado y registrado en MLflow.  
21. API de inferencia.  
22. Motor de optimización bajo restricciones.  
23. Policy/Safety Engine.  
24. Módulo de recomendaciones.  
25. Integración controlada con Kubernetes.  
26. Dashboards de observabilidad, Machine Learning y energía.  
27. Plan y evidencias de pruebas.  
28. Diseño y ejecución experimental.  
29. Informe de comparación baseline versus propuesta.  
30. Informe de resultados, limitaciones y validez.

## **11.7 MVP**

*Tabla 28\. Alcance del MVP*

| Incluido en el MVP | Fuera del MVP |
| :---- | :---- |
| Un clúster o entorno Kubernetes experimental. | Gestión de múltiples centros de datos. |
| Monitoreo de infraestructura y workloads. | Optimización global de nubes comerciales. |
| Predicción de demanda a corto plazo. | Deep Learning complejo sin justificación. |
| Optimización bajo restricciones. | Automatización autónoma irrestricta. |
| Recommendation-Only. | Migración de workloads críticos de producción. |
| Medición o estimación energética documentada. | Certificación energética del centro de datos. |
| MLflow para trazabilidad. | Plataforma MLOps distribuida de gran escala sin necesidad demostrada. |
| Comparación experimental. | Declaraciones de ahorro previas a la experimentación. |

## **11.8 Roadmap**

El proyecto se organiza en un horizonte de **16 semanas**, distribuido en **8 sprints de dos semanas** y agrupado en **3 Productos Mínimos Viables (PMV)**. La planificación integra el desarrollo de la arquitectura de microservicios orientada a eventos, la infraestructura Kubernetes, la observabilidad, el procesamiento de datos, los modelos de Machine Learning, el motor de decisión y optimización, el Policy/Safety Service, la seguridad y la experimentación de Green Computing.

El roadmap se establece con base en resultados verificables. Cada fase debe producir un incremento funcional, una evidencia técnica o un resultado experimental que permita evaluar el avance del proyecto y realizar los ajustes necesarios.

### **11.8.1 Roadmap general de desarrollo**

*Tabla 29\. Roadmap general del proyecto*

| Fase | Semanas | Actividad principal | Resultado verificable | Evidencia principal |
| ----- | ----- | ----- | ----- | ----- |
| 0 | 1 | Investigación y definición | Problema, requisitos, alcance, restricciones, criterios de éxito y riesgos definidos | Project Charter, requisitos, alcance y matriz de riesgos |
| 1 | 1–2 | Diseño arquitectónico | Arquitectura de microservicios, Event-Driven y Kubernetes definida | Diagramas arquitectónicos, contratos API y eventos |
| 2 | 1–2 | Infraestructura experimental | Clúster Kubernetes y componentes base operativos | Clúster, namespaces, Docker y configuraciones |
| 3 | 3–4 | Observabilidad | Telemetría de infraestructura y workloads disponible | Prometheus, Node Exporter, kube-state-metrics y Grafana |
| 4 | 5–6 | Pipeline de datos | Dataset temporal preparado, documentado y versionado | Pipeline ETL, dataset y metadatos |
| 5 | 5–6 | Baseline predictivo | Línea base predictiva cuantificada | Métricas MAE, RMSE y sMAPE registradas |
| 6 | 7–8 | Machine Learning | Modelos candidatos entrenados y evaluados | Experimentos MLflow y comparación de modelos |
| 7 | 7–8 | Prediction Service | Servicio independiente de predicción operativo | API FastAPI, modelo versionado y registros de inferencia |
| 8 | 9–10 | Decision Service | Alternativas de decisión generadas y trazables | Reglas, contexto de decisión y eventos |
| 9 | 9–10 | Optimization Service | Motor de optimización funcionando bajo restricciones | Función objetivo, restricciones y resultados |
| 10 | 9–10 | Policy/Safety Service | Alternativas evaluadas según seguridad, capacidad y SLA | Evaluaciones de políticas y auditoría |
| 11 | 11–12 | Recommendation Service | Recomendaciones trazables disponibles | API, dashboard y registros |
| 12 | 11–12 | Integración Event-Driven | Comunicación asíncrona entre servicios operativa | RabbitMQ, contratos y pruebas de eventos |
| 13 | 11–12 | Observabilidad integral | Métricas de servicios, infraestructura, ML y overhead disponibles | Dashboards y registros |
| 14 | 13–14 | Seguridad y hardening | Plataforma protegida y controlada | RBAC, JWT, Secrets, auditoría y pruebas |
| 15 | 13–16 | Experimentación controlada | Escenarios baseline y estrategia predictiva ejecutados | Resultados experimentales reproducibles |
| 16 | 15–16 | Evaluación y consolidación | Comparación energética, desempeño, SLA y conclusiones | Informe experimental y evidencias finales |

### **11.8.2 Plan de releases y Productos Mínimos Viables**

El roadmap se divide en tres ciclos de entrega. Cada PMV representa un incremento de valor verificable y constituye un punto formal de inspección del proyecto.

#### **PMV1. Viabilidad técnica y pipeline de datos**

**Sprints 1, 2 y 3\. Semanas 1 a 6**

**Objetivo:** demostrar la viabilidad de la infraestructura experimental y garantizar la disponibilidad de datos confiables para el desarrollo de los modelos predictivos.

**Actividades principales:**

1. Definición del problema y requisitos.  
2. Definición del alcance y restricciones.  
3. Elaboración del WBS/EDT.  
4. Diseño de la arquitectura de microservicios.  
5. Diseño de la comunicación orientada a eventos.  
6. Despliegue del clúster Kubernetes.  
7. Configuración de Prometheus y Grafana.  
8. Configuración de Node Exporter y kube-state-metrics.  
9. Implementación de workloads sintéticos.  
10. Construcción del pipeline ETL.  
11. Preparación y versionado del dataset.  
12. Implementación del baseline predictivo.  
13. Registro inicial de experimentos mediante MLflow.

**Resultado esperado:** infraestructura experimental operativa, telemetría disponible, dataset preparado y baseline predictivo evaluado.

**Criterio de cierre:** el dataset debe presentar suficiente calidad, trazabilidad y consistencia temporal para continuar con el entrenamiento de los modelos de Machine Learning.

---

#### **PMV2. Solución predictiva, decisión y optimización**

**Sprints 4, 5 y 6\. Semanas 7 a 12**

**Objetivo:** implementar y validar el núcleo inteligente de la solución, compuesto por los servicios de predicción, decisión, optimización, seguridad de políticas y generación de recomendaciones.

**Actividades principales:**

1. Análisis exploratorio del dataset.  
2. Selección y transformación de variables.  
3. Construcción de características predictoras.  
4. Evaluación del baseline.  
5. Entrenamiento de Random Forest.  
6. Entrenamiento de XGBoost.  
7. Comparación de modelos mediante MAE, RMSE y sMAPE.  
8. Selección experimental del modelo.  
9. Implementación del Prediction Service.  
10. Implementación del Decision Service.  
11. Implementación del Optimization Service.  
12. Implementación del Policy/Safety Service.  
13. Implementación del Recommendation Service.  
14. Integración de los microservicios mediante APIs.  
15. Integración de comunicación asíncrona mediante RabbitMQ.  
16. Implementación del dashboard de predicciones y recomendaciones.  
17. Registro de modelos, experimentos y resultados mediante MLflow.

**Resultado esperado:** sistema capaz de procesar telemetría, generar predicciones, evaluar alternativas, aplicar restricciones y producir recomendaciones trazables.

**Criterio de cierre:** las recomendaciones deben respetar las restricciones establecidas de capacidad, latencia, disponibilidad y SLA.

La precisión del modelo será determinada experimentalmente. El valor de 90 % corresponde a una **meta de referencia**, no a un resultado asumido previamente.

---

#### **PMV3. Producto consolidado y experimentación final**

**Sprints 7 y 8\. Semanas 13 a 16**

**Objetivo:** consolidar la plataforma, implementar los controles de seguridad y determinar experimentalmente el impacto de la estrategia predictiva sobre la eficiencia energética.

**Actividades principales:**

1. Implementación de Kubernetes RBAC.  
2. Implementación de autenticación y autorización.  
3. Configuración de Secrets.  
4. Aplicación del principio de mínimo privilegio.  
5. Implementación de auditoría.  
6. Pruebas de seguridad.  
7. Pruebas de resiliencia.  
8. Validación de mecanismos de rollback.  
9. Consolidación de dashboards.  
10. Ejecución del escenario baseline.  
11. Ejecución de la estrategia Green AI.  
12. Medición o estimación documentada del consumo energético.  
13. Cálculo de energía por unidad de trabajo.  
14. Evaluación de latencia, throughput, disponibilidad y SLA.  
15. Medición del overhead introducido por la solución.  
16. Evaluación de emisiones operacionales cuando exista información válida sobre intensidad de carbono.  
17. Análisis estadístico de resultados.  
18. Elaboración del informe técnico y científico.

**Resultado esperado:** producto experimental consolidado y resultados comparativos entre la estrategia convencional y la estrategia basada en predicción y optimización.

**Criterio de cierre:** disponer de evidencia suficiente para determinar si la estrategia propuesta mejora la eficiencia energética sin producir una degradación inaceptable del servicio.

El objetivo de reducción energética del **15 %** se considera una meta experimental. El resultado final deberá determinarse a partir de las mediciones obtenidas y no deberá asumirse antes de ejecutar los experimentos.

---

### **11.8.3 Planificación detallada de los sprints**

*Tabla 30\. Planificación detallada de sprints*

| Sprint | PMV | Semanas | Actividades principales | Entregable principal |
| ----- | ----- | ----- | ----- | ----- |
| Sprint 1 | PMV1 | 1–2 | Investigación, requisitos, alcance, riesgos, WBS/EDT, arquitectura de microservicios y planificación | Project Charter, WBS/EDT, Product Backlog y arquitectura inicial |
| Sprint 2 | PMV1 | 3–4 | Kubernetes, Docker, namespaces, Prometheus, Node Exporter, kube-state-metrics, Grafana y workloads sintéticos | Clúster experimental y sistema de observabilidad operativo |
| Sprint 3 | PMV1 | 5–6 | Pipeline ETL, limpieza, transformación, resampling, dataset, versionado y baseline | Dataset documentado, baseline y experimentos iniciales en MLflow |
| Sprint 4 | PMV2 | 7–8 | Análisis exploratorio, feature engineering, Random Forest y XGBoost | Modelos candidatos evaluados |
| Sprint 5 | PMV2 | 9–10 | Prediction Service, Decision Service, Optimization Service y Policy/Safety Service | Núcleo predictivo y de decisión operativo |
| Sprint 6 | PMV2 | 11–12 | Recommendation Service, RabbitMQ, contratos de eventos, APIs, dashboards y observabilidad | Flujo completo de predicción y recomendación |
| Sprint 7 | PMV3 | 13–14 | RBAC, JWT, Secrets, auditoría, resiliencia, pruebas y diseño experimental | Plataforma endurecida y escenario baseline ejecutado |
| Sprint 8 | PMV3 | 15–16 | Experimentación Green AI, análisis energético, comparación, documentación y resultados | Resultados experimentales e informe final |

Cada sprint tendrá un resultado verificable y finalizará con revisión del incremento, validación de los criterios definidos, registro de retroalimentación y actualización de las decisiones técnicas.

---

### **11.8.4 Componentes técnicos incorporados progresivamente**

La arquitectura de microservicios se implementará de forma progresiva para evitar introducir complejidad distribuida antes de disponer de una necesidad funcional u operacional que la justifique.

*Tabla 31\. Incorporación progresiva de componentes*

| Componente | Sprint | Propósito |
| ----- | ----- | ----- |
| Kubernetes | 1–2 | Entorno de ejecución y aislamiento |
| Prometheus | 2 | Recolección y almacenamiento de métricas temporales |
| Grafana | 2–3 | Visualización y monitoreo |
| Node Exporter | 2 | Telemetría de infraestructura |
| kube-state-metrics | 2 | Estado de recursos Kubernetes |
| Pipeline ETL | 3 | Preparación de datos |
| MLflow | 3–4 | Seguimiento y versionado de experimentos |
| Prediction Service | 4–5 | Inferencia del modelo |
| Decision Service | 5 | Evaluación del contexto |
| Optimization Service | 5 | Optimización bajo restricciones |
| Policy/Safety Service | 5 | Validación de políticas y seguridad |
| Recommendation Service | 6 | Gestión de recomendaciones |
| RabbitMQ | 6 | Comunicación asíncrona mediante eventos |
| PostgreSQL | 3–6 | Metadatos, resultados y trazabilidad |
| MinIO | 3–6 | Artefactos y datasets |
| RBAC | 7 | Control de acceso Kubernetes |
| Sistema experimental | 7–8 | Comparación baseline y Green AI |

---

### **11.8.5 Eventos principales de la arquitectura**

La comunicación orientada a eventos se utilizará para desacoplar procesos que no requieren una respuesta síncrona inmediata.

*Tabla 32\. Catálogo inicial de eventos*

| Evento | Servicio emisor | Servicio consumidor | Propósito |
| ----- | ----- | ----- | ----- |
| `METRICS_AVAILABLE` | Monitoring Service | Data Processing Service | Informar disponibilidad de nuevas métricas |
| `DEMAND_SPIKE` | Monitoring Service / Prediction Service | Decision Service | Informar incremento relevante de demanda |
| `PREDICTION_READY` | Prediction Service | Decision Service | Informar disponibilidad de una predicción |
| `OPTIMIZATION_REQUESTED` | Decision Service | Optimization Service | Solicitar generación de alternativas |
| `SLA_RISK` | Monitoring Service / Decision Service | Policy/Safety Service | Informar riesgo de incumplimiento |
| `POLICY_VALIDATED` | Policy/Safety Service | Recommendation Service | Informar validación de una alternativa |
| `RECOMMENDATION_READY` | Recommendation Service | Experiment Service / interfaz | Informar disponibilidad de una recomendación |

Los eventos deberán disponer de contratos versionados y registrar información mínima de identificación, origen, tipo, timestamp y contenido del mensaje.

Prometheus continuará siendo el mecanismo principal para almacenar y consultar series temporales. RabbitMQ cumplirá una función complementaria como mecanismo de comunicación asíncrona entre servicios.

---

### **11.8.6 Hitos de control del roadmap**

*Tabla 33\. Hitos y criterios de decisión*

| Hito | Semana | Pregunta de control | Criterio de decisión |
| ----- | ----- | ----- | ----- |
| H1 | 2 | ¿La arquitectura y el entorno experimental son técnicamente viables? | Continuar o realizar ajustes arquitectónicos |
| H2 | 6 | ¿Los datos disponibles son suficientes para desarrollar los modelos? | Continuar, ampliar observación o modificar variables |
| H3 | 8 | ¿Existe un modelo que supere al baseline? | Seleccionar modelo o revisar estrategia predictiva |
| H4 | 10 | ¿El motor genera alternativas técnicamente factibles? | Ajustar función objetivo o restricciones |
| H5 | 12 | ¿El sistema genera recomendaciones trazables? | Autorizar inicio de experimentación |
| H6 | 14 | ¿La plataforma dispone de controles de seguridad adecuados? | Corregir vulnerabilidades antes de experimentar |
| H7 | 16 | ¿Existe evidencia de mejora energética sin degradación inaceptable del servicio? | Consolidar resultados y conclusiones |

---

### **11.8.7 Adaptación del roadmap**

Debido a la incertidumbre inherente al desarrollo de modelos predictivos y a la medición del consumo energético, el roadmap podrá adaptarse en función de los resultados obtenidos durante los PMV.

Las principales condiciones de adaptación serán las siguientes:

| Situación identificada | Acción de adaptación |
| ----- | ----- |
| Datos insuficientes | Ampliar el período de observación o generar workloads sintéticos adicionales |
| Variables poco representativas | Incorporar nuevas variables justificadas mediante análisis exploratorio |
| Baseline con buen desempeño | Evaluar si la complejidad adicional del modelo ML está justificada |
| Random Forest con mejor desempeño | Seleccionar Random Forest como modelo definitivo |
| XGBoost con mejor desempeño | Seleccionar XGBoost como modelo definitivo |
| Error elevado durante períodos de alta demanda | Ajustar variables, ventanas temporales o modelo |
| Recomendaciones cercanas a límites de SLA | Incrementar márgenes de seguridad en el Policy/Safety Service |
| Overhead elevado | Reducir frecuencia de inferencia u optimizar los servicios |
| Medición energética insuficiente | Utilizar una estimación documentada y limitar el alcance de las conclusiones |
| Ausencia de ahorro energético | Analizar las causas y reportar el resultado experimental sin alterar artificialmente los resultados |
| Complejidad excesiva de los microservicios | Revisar límites de servicio y eliminar componentes que no demuestren valor |

---

### **11.8.8 Criterios de cierre de los PMV**

*Tabla 34\. Evidencias obligatorias por PMV*

| PMV | Evidencias de cierre |
| ----- | ----- |
| PMV1 | Incremento funcional, pruebas del pipeline, métricas de observabilidad, dataset versionado, baseline predictivo, retroalimentación del asesor, riesgos y decisiones registradas |
| PMV2 | Incremento funcional, pruebas de integración, evaluación de modelos, motor de decisión y optimización, Policy/Safety Service, recomendaciones trazables, feedback del asesor y decisiones de adaptación |
| PMV3 | Producto integrado, pruebas de seguridad, experimentación baseline, experimentación Green AI, resultados cuantitativos, análisis energético, evaluación de SLA y documentación final |

---

### **11.8.9 Relación del roadmap con los conocimientos de ingeniería**

*Tabla 35\. Trazabilidad entre conocimientos y actividades del roadmap*

| Conocimiento de ingeniería | Fases relacionadas | Evidencia |
| ----- | ----- | ----- |
| Estadística y series temporales | 4, 5 y 6 | Análisis exploratorio, ventanas temporales y métricas |
| Machine Learning | 5, 6 y 7 | Baseline, Random Forest, XGBoost y evaluación |
| Ingeniería de software | Todas | Código, pruebas, APIs y documentación |
| Microservicios | 1, 7, 8, 9, 10 y 11 | Servicios independientes y contratos |
| Event-Driven Architecture | 12 | RabbitMQ y catálogo de eventos |
| Kubernetes | 2, 3 y 14 | Clúster, namespaces, workloads y RBAC |
| Optimización | 9 | Función objetivo y restricciones |
| Seguridad | 10 y 14 | Policy/Safety, RBAC, JWT, Secrets y auditoría |
| MLOps | 5, 6 y 7 | MLflow, modelos versionados y experimentos |
| Green Computing | 15 y 16 | Energía, energía por unidad de trabajo y emisiones |
| Experimentación | 15 y 16 | Comparación baseline frente a Green AI |
| Gestión de proyectos | Todas | Backlog, sprints, PMV, riesgos, decisiones y evidencias |

---

### **11.8.10 Resultado esperado del roadmap**

Al finalizar las 16 semanas, el proyecto deberá disponer de un prototipo experimental integrado compuesto por:

* Arquitectura de microservicios desplegada sobre Kubernetes.  
* Comunicación síncrona mediante APIs.  
* Comunicación asíncrona mediante RabbitMQ.  
* Sistema de observabilidad basado en Prometheus y Grafana.  
* Pipeline de procesamiento y preparación de datos.  
* Baseline predictivo.  
* Modelos de Machine Learning evaluados experimentalmente.  
* Prediction Service.  
* Decision Service.  
* Optimization Service.  
* Policy/Safety Service.  
* Recommendation Service.  
* Registro y trazabilidad de modelos mediante MLflow.  
* Seguridad mediante RBAC y mínimo privilegio.  
* Sistema de experimentación controlada.  
* Comparación entre estrategia baseline y estrategia predictiva.  
* Métricas de energía, eficiencia, SLA, latencia, throughput, disponibilidad y overhead.  
* Documentación técnica y resultados experimentales.

El roadmap establece como criterio fundamental que **la implementación tecnológica no constituye por sí misma evidencia de mejora energética**. La validez de la propuesta deberá determinarse mediante la experimentación controlada y la comparación cuantitativa de los resultados obtenidos.

La planificación queda alineada con la gestión del proyecto definida para **16 semanas, 8 sprints y 3 PMV**, incorporando la arquitectura actual de **microservicios orientada a eventos sobre Kubernetes** y manteniendo la separación entre observabilidad, predicción, decisión, optimización, validación de políticas, recomendación y ejecución controlada

## **11.9 Matriz de trazabilidad de ingeniería**

*Tabla 36\. Matriz de trazabilidad problema, conocimiento, decisión, solución y evidencia*

| Problema / necesidad | Conocimiento | Decisión | Componente | Evidencia |
| :---- | :---- | :---- | :---- | :---- |
| Demanda variable | Series temporales \+ ML | Predecir demanda | ML Engine | MAE, RMSE, sMAPE |
| Subutilización | Optimización | Evaluar consolidación / scaling | Optimization Engine | Escenarios y función objetivo |
| Riesgo de degradación | Seguridad \+ SRE | Validar antes de actuar | Policy Engine | SLA y auditoría |
| Falta de visibilidad | Observabilidad | Monitoreo centralizado | Prometheus / Grafana | Dashboards |
| Necesidad de demostrar mejora | Experimentación | Baseline controlado | Experiment Manager | Resultados comparativos |
| Sostenibilidad | Green Computing | Medir energía por trabajo | Energy Evaluation | kWh y Wh/unidad |
| Necesidad de reproducibilidad | MLOps | Registrar ciclo de vida | MLflow | Runs, modelos y artefactos |

## **11.10 Evidencias gráficas requeridas**

31. Infraestructura Kubernetes utilizada en el experimento.  
32. Dashboard de Prometheus/Grafana.  
33. Ejemplo de métricas históricas.  
34. Pipeline de datos ejecutado.  
35. Experimento registrado en MLflow.  
36. Comparación de modelos predictivos.  
37. Predicción frente a valor observado.  
38. Recomendación generada.  
39. Validación de políticas.  
40. Estado del workload en Kubernetes.  
41. Resultado baseline frente a propuesta.  
42. Métricas energéticas del experimento.

# **12\. Conclusiones de conocimientos de ingeniería**

El Proyecto 20 evidencia conocimientos de ingeniería mediante su aplicación coordinada a un problema complejo de gestión energética de workloads computacionales. La solución no se reduce a la incorporación de Machine Learning, sino que integra fundamentos matemáticos, computación, ingeniería de software, arquitectura, infraestructura cloud-native, optimización, seguridad, MLOps y Green Computing.

Los conocimientos de estadística y series temporales permiten caracterizar la demanda y construir el dataset; Machine Learning permite anticipar la demanda futura; optimización permite transformar la predicción en alternativas de decisión; ingeniería de software y arquitectura permiten separar responsabilidades; Kubernetes proporciona el entorno experimental; seguridad y Policy/Safety Engine controlan las acciones; MLOps permite reproducibilidad y operación del modelo; y Green Computing proporciona criterios para medir energía e impacto ambiental.

La selección metodológica adopta Scrum para el desarrollo incremental, CRISP-DM adaptado para el ciclo de datos y Machine Learning, MLOps para la gestión del ciclo de vida del modelo, optimización matemática para la toma de decisiones y experimento controlado para la validación de la hipótesis. La combinación es deliberada: cada enfoque cubre una dimensión diferente del problema.

La arquitectura de microservicios orientada a eventos se justifica por la necesidad de separar responsabilidades con diferentes cargas de trabajo y permitir escalamiento, aislamiento y evolución independiente de los componentes de observabilidad, predicción, decisión, optimización y experimentación. Kubernetes proporciona el entorno de despliegue y RabbitMQ el mecanismo de comunicación asíncrona. La complejidad adicional se controla mediante límites de servicio explícitos, contratos de API/eventos, observabilidad, RBAC y un alcance inicial Recommendation-Only.

La validación constituye el mecanismo que determinará si los conocimientos aplicados fueron adecuados. El criterio final no será únicamente que el sistema funcione, que el modelo tenga bajo error o que una recomendación sea factible. La validez requerirá evidencia conjunta de calidad predictiva, factibilidad de la decisión, seguridad, desempeño y comportamiento energético por unidad funcional.

Finalmente, el diseño mantiene tres condiciones abiertas que deben verificarse antes de cerrar la implementación: disponibilidad y calidad de datos históricos, disponibilidad de medición energética suficientemente confiable y capacidad real del entorno Kubernetes para ejecutar escenarios controlados. Estas verificaciones son puntos de control de ingeniería y no supuestos que deban darse por cumplidos.

## **12.1 Conclusión de trazabilidad AG-I07**

*Tabla 37\. Evidencia final de AG-I07*

| Dimensión | Evidencia esperada en el Proyecto 20 |
| :---- | :---- |
| Matemáticas y ciencias | Estadística, series temporales, regresión, métricas de error, optimización y cálculo energético. |
| Computación | Algoritmos, datos, BD, ML, APIs, Kubernetes, observabilidad y seguridad. |
| Ingeniería fundamental | Requisitos, arquitectura, diseño, calidad, pruebas, configuración y gestión de riesgos. |
| Ingeniería especializada | Green Computing, forecasting, resource management, MLOps y optimización energética. |
| Problema complejo | Demanda variable y múltiples restricciones de energía, SLA, rendimiento, seguridad y disponibilidad. |
| Desarrollo de solución | Arquitectura, componentes, pipeline, modelos, optimizador, Policy Engine y despliegue. |
| Validación | Pruebas, métricas predictivas, energía, SLA, rendimiento y comparación baseline versus tratamiento. |
| Trazabilidad | Relación entre necesidad, conocimiento, decisión, componente y evidencia. |

# **REFERENCIAS BIBLIOGRÁFICAS Y FUENTES DE SUSTENTO**

Las referencias se presentan mediante numeración consecutiva y se organizan de acuerdo con la orientación de citación para ingeniería de la Universidad Continental. El manual institucional de Dennis Arias Chávez establece directrices para referencias de documentos impresos y digitales y está dirigido específicamente a estudiantes y profesionales de ingeniería \[15\].

\[1\] SCHWABER, Ken; SUTHERLAND, Jeff. The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game \[en línea\]. November 2020\. Disponible en: https://scrumguides.org/scrum-guide.html. Documento oficial de Scrum.

\[2\] KREUZBERGER, Dominik; KÜHL, Niklas; HIRSCHL, Sebastian. Machine Learning Operations (MLOps): Overview, Definition, and Architecture. IEEE Access \[en línea\]. 2023, vol. 11, pp. 31866-31879. DOI: 10.1109/ACCESS.2023.3262138. Disponible en: https://doi.org/10.1109/ACCESS.2023.3262138.

\[3\] NAJAFABADI, Faezeh Amou; BOGNER, Justus; GEROSTATHOPOULOS, Ilias; LAGO, Patricia. An architectural perspective on MLOps: Structures, processes, tools, and stakeholders. Information and Software Technology \[en línea\]. 2026, vol. 193, art. 108029, pp. 1-31. DOI: 10.1016/j.infsof.2026.108029. Disponible en: https://doi.org/10.1016/j.infsof.2026.108029.

\[4\] WOŹNIAK, Adrian P.; MILCZAREK, Mateusz; WOŹNIAK, Joanna. MLOps Components, Tools, Process, and Metrics: A Systematic Literature Review. IEEE Access \[en línea\]. 2025, vol. 13, pp. 22166-22175. DOI: 10.1109/ACCESS.2025.3534990. Disponible en: https://doi.org/10.1109/ACCESS.2025.3534990.

\[5\] VERMA, Prateek; MAURYA, Ashish Kumar; YADAV, R. S. A survey on energy-efficient workflow scheduling algorithms in cloud computing. Software: Practice and Experience \[en línea\]. 2024, vol. 54, n. 5, pp. 637-682. DOI: 10.1002/spe.3292. Disponible en: https://doi.org/10.1002/spe.3292.

\[6\] LIOW, Kai Wen; SUBRAMANIAM, Hema; WANG, Ruizhuo; ZHENG, Runna; AKTER, Hossain; HUANG, Bangning. CARA: Adaptive scheduling for carbon-efficient workload orchestration in distributed cloud systems. Sustainable Computing: Informatics and Systems \[en línea\]. 2026, vol. 51, art. 101407\. DOI: 10.1016/j.suscom.2026.101407. Disponible en: https://doi.org/10.1016/j.suscom.2026.101407.

\[7\] KHAN, Tahseen; TIAN, Wenhong; ILAGER, Shashikant; BUYYA, Rajkumar. Workload forecasting and energy state estimation in cloud data centres: ML-centric approach. Future Generation Computer Systems \[en línea\]. 2022, vol. 128, pp. 320-332. DOI: 10.1016/j.future.2021.10.019. Disponible en: https://doi.org/10.1016/j.future.2021.10.019.

\[8\] JI, Kai; ZHANG, Fa; CHI, Ce; SONG, Penglei, et al. A joint energy efficiency optimization scheme based on marginal cost and workload prediction in data centers. Sustainable Computing: Informatics and Systems \[en línea\]. 2021, vol. 32, art. 100596\. DOI: 10.1016/j.suscom.2021.100596. Disponible en: https://doi.org/10.1016/j.suscom.2021.100596.

\[9\] BELOGLAZOV, Anton; ABAWAJY, Jemal; BUYYA, Rajkumar. Energy-aware resource allocation heuristics for efficient management of data centers for Cloud computing. Future Generation Computer Systems \[en línea\]. 2012, vol. 28, n. 5, pp. 755-768. DOI: 10.1016/j.future.2011.04.017. Disponible en: https://doi.org/10.1016/j.future.2011.04.017.

\[10\] SHARMA, Mohan; GARG, Ritu. An artificial neural network based approach for energy efficient task scheduling in cloud data centers. Sustainable Computing: Informatics and Systems \[en línea\]. 2020, vol. 26, art. 100373\. DOI: 10.1016/j.suscom.2020.100373. Disponible en: https://doi.org/10.1016/j.suscom.2020.100373.

\[11\] GREEN SOFTWARE FOUNDATION. Software Carbon Intensity (SCI) \[en línea\]. 2026\. Disponible en: https://greensoftware.foundation/standards/sci/. Referencia técnica alineada con ISO/IEC 21031:2024.

\[12\] MICROSOFT. Team Data Science Process: Lifecycle Detail \[en línea\]. Microsoft Azure / Microsoft-TDSP. Disponible en: https://github.com/Azure/Microsoft-TDSP/blob/master/Docs/lifecycle-detail.md.

\[13\] ISO. ISO/IEC 21031:2024. Software Carbon Intensity (SCI). Norma internacional para la medición de la intensidad de carbono del software.

\[14\] MICROSOFT. Team Data Science Process: An Overview \[en línea\]. Microsoft-TDSP. Disponible en: https://github.com/Azure/Microsoft-TDSP/blob/master/Docs/README.md.

\[15\] ARIAS CHÁVEZ, Dennis. Manual para citar y referenciar fuentes en textos de ingeniería según la norma ISO 690-2. 1.ª ed. Huancayo: Universidad Continental. Fondo Editorial, 2019\. 83 p. ISBN 978-612-4443-04-6. Disponible en: https://fondoeditorial.continental.edu.pe/product/manual-para-citar-y-referenciar-fuentes-en-textos-de-ingenieria-segun-la-norma-iso-690-2/.

## **Nota sobre cuartiles y calidad de las fuentes**

Los cuartiles Q1/Q2 dependen de la base bibliométrica, categoría temática y año de consulta. Por ello, este documento utiliza los artículos para justificar decisiones técnicas y metodológicas y no presenta el cuartil como una propiedad absoluta del artículo. Para una entrega de tesis o artículo científico se recomienda conservar el registro bibliométrico de la fecha de consulta y verificar la categoría específica utilizada por la institución.

Las referencias \[7\], \[8\], \[9\] y \[10\] sustentan directamente el problema de workload forecasting, scheduling, asignación de recursos y eficiencia energética. Las referencias \[2\], \[3\] y \[4\] sustentan la incorporación de MLOps. Las referencias \[1\], \[12\] y \[14\] sustentan los enfoques metodológicos de desarrollo y ciencia de datos. La referencia \[15\] sustenta el criterio documental de citación utilizado para el informe.

# **ANEXO A. Control de correspondencia con el formato de Conocimientos de Ingeniería**

La siguiente matriz permite verificar que los doce apartados principales conservan la lógica del documento institucional proporcionado y, simultáneamente, incorporan el contenido técnico desarrollado previamente.

*Tabla 38\. Correspondencia entre la estructura solicitada y el contenido técnico*

| Apartado principal | Contenido integrado del informe técnico anterior |
| :---- | :---- |
| 1\. Problema complejo de ingeniería | Problema, contexto, causas, consecuencias, oportunidad y restricciones. |
| 2\. Necesidades y requerimientos de ingeniería | Necesidades, requisitos funcionales y no funcionales. |
| 3\. Fundamentos matemáticos y científicos | Estadística, series temporales, ML, error, optimización y energía. |
| 4\. Conocimientos de computación | Algoritmos, BD, software, arquitectura, ML, redes, seguridad, cloud y observabilidad. |
| 5\. Conocimientos fundamentales de ingeniería | Requisitos, arquitectura, calidad, pruebas, seguridad, riesgos y mantenibilidad. |
| 6\. Conocimientos especializados | Green Computing, forecasting, scheduling, autoscaling, MLOps, SLA, Policy Engine y Kubernetes. |
| 7\. Selección y justificación | Scrum, CRISP-DM, experimento controlado, MLOps, arquitectura y tecnologías. |
| 8\. Aplicación al diseño | Arquitectura, microservicios, datos, BD, ML, MLOps, optimización y seguridad. |
| 9\. Integración | Interacción de conocimientos y antecedentes de proyectos similares. |
| 10\. Validación | Software, ML, arquitectura, infraestructura, energía, experimento y aceptación. |
| 11\. Implementación, evidencias y trazabilidad | Despliegue, APIs, observabilidad, pruebas, infraestructura, entregables, MVP, roadmap, riesgos y evidencias. |
| 12\. Conclusiones | Conclusiones AG-I07 y evidencia final de conocimientos. |

Esta estructura evita mantener como capítulos independientes elementos que son evidencias de aplicación. Por ejemplo, Machine Learning, MLOps, arquitectura, base de datos, optimización y seguridad aparecen dentro de los apartados donde demuestran conocimiento aplicado, en lugar de presentarse como una colección separada de tecnologías.

El documento conserva los diagramas e imágenes como espacios reservados para que las evidencias reales del proyecto sean incorporadas posteriormente. No se incorporan resultados experimentales no obtenidos ni porcentajes de ahorro no demostrados.

| Evento | Emisor | Consumidor principal |
| :---- | :---- | :---- |
| METRICS\_AVAILABLE | Monitoring Service | Data Processing Service |
| DEMAND\_SPIKE | Monitoring / Prediction Service | Decision Service |
| PREDICTION\_READY | Prediction Service | Decision Service |
| OPTIMIZATION\_REQUESTED | Decision Service | Optimization Service |
| POLICY\_VALIDATED | Policy/Safety Service | Recommendation Service |
| SLA\_RISK | Monitoring / Decision Service | Policy/Safety Service |
| RECOMMENDATION\_READY | Recommendation Service | Experiment Service / UI |

[image1]: <evidencias/img-5fdb4a6410e8.png>

[image2]: <evidencias/img-d9ab4d2703f4.png>

[image3]: <evidencias/img-7079b609c342.png>

[image4]: <evidencias/img-ab06522e9da6.png>

[image5]: <evidencias/img-7dc9618e09bf.png>

[image6]: <evidencias/img-7fa5fe22ca83.png>

[image7]: <evidencias/img-1dc4bd457d04.png>

[image8]: <evidencias/img-d802c038406f.png>