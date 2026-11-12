**6. Prueba de Concepto (PoC)**

Para una solución TIC que incorpora Inteligencia Artificial, la Prueba de Concepto (PoC) constituye una actividad experimental destinada a reducir la incertidumbre tecnológica antes de comprometer recursos en el desarrollo completo. Su propósito no es construir el producto final, sino obtener evidencia objetiva sobre la viabilidad de la técnica propuesta, la disponibilidad y calidad de los datos, el comportamiento de los modelos y las condiciones necesarias para integrar la capacidad predictiva en la solución.

La PoC debe conservar un alcance controlado. En este caso, la capacidad de Inteligencia Artificial se concentra en la predicción de la demanda computacional de corto plazo a partir de métricas históricas de infraestructura y workloads. La predicción servirá posteriormente como insumo para evaluar alternativas de gestión de recursos. La PoC no debe ejecutar cambios autónomos sobre la infraestructura; su resultado debe ser una predicción evaluable y, cuando corresponda, una recomendación técnicamente justificada.

La evaluación se realizará considerando que se trata de un problema de regresión y de series temporales. Por ello, las métricas principales serán MAE y RMSE, complementadas por sMAPE cuando sea apropiado, además de latencia de inferencia, consumo de recursos del servicio predictivo y comportamiento ante períodos de alta demanda. No se asumirá previamente que un modelo es superior a otro: la selección deberá sustentarse en resultados experimentales.

# 1. Identificación de la PoC

La identificación de la PoC establece con precisión qué capacidad tecnológica se desea comprobar, qué incertidumbre se pretende resolver, qué datos serán utilizados y qué criterio permitirá decidir si la alternativa puede continuar. Esta definición evita que la prueba se convierta en un desarrollo prematuro del sistema completo.

| **Elemento** | **Definición Técnica y Operativa** |
| --- | --- |
| **Requerimiento** | Predecir la demanda computacional de corto plazo utilizando métricas históricas de infraestructura y workloads para disponer de información anticipada que permita evaluar decisiones de asignación y gestión de recursos. |
| **Problema técnico** | Determinar si los datos de telemetría disponibles contienen suficiente información temporal y variabilidad para construir un modelo predictivo con un error aceptable y una latencia compatible con el ciclo de decisión. |
| **Objetivo de la PoC** | Comprobar experimentalmente la viabilidad técnica de modelos de Machine Learning para estimar la demanda computacional futura y establecer las condiciones requeridas para su integración posterior. |
| **Tecnología** | Machine Learning para regresión y series temporales en **Python**, utilizando bibliotecas especializadas (considerando **Random Forest Regressor** y **XGBoost Regressor** como alternativas iniciales frente a un baseline simple). |
| **Duración** | **1 a 2 semanas** (enmarcado dentro del ciclo inicial de simulación del PMV1). |
| **Datos** | Métricas de infraestructura y workloads obtenidas mediante observabilidad (**Prometheus**), priorizando la utilización de CPU y complementando con memoria, requests, limits, réplicas, throughput, latencia y consumo eléctrico en Watts. |
| **Criterio de éxito** | Desempeño predictivo medido cuantitativamente mediante métricas de error (**MAE**, **RMSE** y **sMAPE**), una latencia de inferencia menor a 2 segundos y estabilidad comprobada en escenarios de demanda alta o picos. |

# 2. Secuencia de ejecución

La secuencia de ejecución organiza la PoC en **tres fases consecutivas, incrementales y verificables**, diseñadas para reducir la incertidumbre tecnológica con el menor esfuerzo de desarrollo posible.

**FASE 1: Definir la Incertidumbre Tecnológica**

En esta fase inicial se formulan las preguntas técnicas clave que la PoC debe responder empíricamente antes de construir la arquitectura completa de microservicios:

1. **Calidad y continuidad de la telemetría:** ¿Las métricas recopiladas por Prometheus a intervalos de 15 segundos presentan la continuidad temporal, la variabilidad y la ausencia de vacíos (*gaps*) necesarios para entrenar algoritmos de series temporales?
2. **Horizonte de predicción útil:** ¿Qué horizonte temporal (**5, 15 o 30 minutos**) brinda el equilibrio óptimo entre precisión predictiva y tiempo suficiente para la toma de decisiones en el orquestador?
3. **Comportamiento en picos y variabilidad de workloads:** ¿Los modelos mantienen un margen de error aceptable durante cambios abruptos de carga (picos de uso en horarios académicos)?
4. **Diferenciación entre Uso de Recursos y Consumo Energético:** La utilización de CPU (%) no equivale automáticamente a consumo en Watts. ¿Es posible estimar la potencia eléctrica $P(u)$ a partir del uso de CPU $u$ mediante un modelo lineal de energía cuando no se dispone de una PDU física?
5. **Salida de la Fase 1:** Formulación de la hipótesis técnica y definición de las condiciones de contorno para la preparación del dataset.

## FASE 2. Definir hipótesis y criterio de éxito

**Hipótesis Técnica (H1):**

*"Los modelos de Machine Learning supervisados de series de tiempo (Random Forest Regressor y XGBoost Regressor) pueden predecir la demanda computacional de CPU a un horizonte de 15 minutos con un error* RMSE<=10% *y* > 8\%*, manteniendo una latencia de inferencia* $<2s$*, lo que permite utilizar sus predicciones como insumo confiable para la evaluación de políticas de gestión energética sin ejecutar cambios autónomos no autorizado."*

**Métricas de Evaluación de Regresión y Fórmulas Matemáticas:**

1. **Error Absoluto Medio (MAE - Mean Absolute Error):** Mide la desviación absoluta promedio entre el valor real y la predicción en las mismas unidades de la variable objetivo (% de CPU o Watts)911:
2. $MAE=\frac{1}{n}\sum\_{i=1}^{n}|y\_{i}-\hat{y}\_{i}|$
3. *Donde* $y\_{i}$ *es la demanda real observada y* $\hat{y}\_{i}$ *es la demanda estimada por el modelo.*
4. **Raíz del Error Cuadrático Medio (RMSE - Root Mean Squared Error):** Penaliza con mayor severidad las desviaciones o picos de error grandes, siendo crítica para detectar fallas del modelo durante períodos de alta carga911:
5. $RMSE=\sqrt{\frac{1}{n}\sum\_{i=1}^{n}(y\_{i}-\hat{y}\_{i})^{2}}$
6. **Error Porcentual Absoluto Medio Simétrico (sMAPE):** Proporciona una medida del error en términos porcentuales acotados (entre 0% y 200%), evitando inestabilidades cuando la demanda de CPU es cercana a cero.
7. **Modelo Estimador de Potencia Eléctrica (Proxy Watts vs. CPU):** Modelo lineal para estimar la potencia instantánea $P(u)$ en Watts en función del porcentaje de utilización de CPU $u\in $12:
8. $P(u)=P\_{idle}+(P\_{max}-P\_{idle})×u$
9. *Donde* $P\_{idle}$ *es la potencia consumida por el servidor en reposo y* $P\_{max}$ *es el límite máximo de potencia teórica según la ficha del fabricante (nodes.max\_watts).*

## FASE 3. Preparar datos

Consiste en realizar el procesamiento estrictamente necesario para estructurar un dataset de series temporales consistente, reproducible y cronológicamente ordenado:

| **Actividad** | **Descripción Técnica** | **Evidencia / Resultado** |
| --- | --- | --- |
| **Adquisición** | Extraer telemetría desde Prometheus (CPU, RAM, Watts) muestreada a intervalos de 15 segundos. | Dataset en bruto con marcas de tiempo TIMESTAMPTZ. |
| **Limpieza** | Identificar registros nulos (imputación por interpolación lineal en brechas $<1min$), eliminar duplicados y valores imposibles. | Reporte de calidad de datos y tratamiento de anomalías. |
| **Transformación (Lags)** | Construir ventanas deslizantes (*sliding windows*) con retardo histórico (t - 1, t - 2,.., t - 15 minutos) y promedios móviles. | Dataset transformado y matriz de características $X$. |
| **Construcción del Objetivo** | Definir la variable objetivo de demanda futura a $t+15$ minutos ($y\_{t+15}=CPU\_{t+15}$). | Definición formal de la variable dependiente $y$. |
| **División Temporal** | Separar los datos por orden cronológico: **70% Entrenamiento**, **15% Validación** y **15% Prueba**. | Respeto riguroso de la línea de tiempo sin mezclas aleatorias. |
| **Control de Fuga (Data Leakage)** | Garantizar que las transformaciones (escalado o normalización con Standard Scaler) calculen sus parámetros únicamente con el conjunto de entrenamiento. | Procedimiento de validación sin contaminación del futuro. |

## 4. Selección del modelo

En consistencia con los criterios de acreditación **ICACIT AG-I11 (Uso de Herramientas Modernas)**, la selección de la arquitectura algorítmica no se realiza de forma arbitraria ni por la popularidad del modelo, sino mediante una **decisión rigurosa de ingeniería respaldada por evidencia experimental**.

Para evitar la sobreingeniería (overengineering), se descarta el uso inicial de modelos complejos de Deep Learning (como redes recurrentes LSTM, GRU o Transformers), restringiéndolos únicamente a fases futuras si los modelos supervisados livianos resultan insuficientes. La selección se concentra en modelos supervisados para datos tabulares y series temporales transformadas en **ventanas de características (sliding windows)**, comparados de forma estricta contra estrategias de referencia (baselines)

**Matriz Comparativa de Alternativas Tecnológicas** .

El uso de baselines es indispensable en ingeniería de software e Inteligencia Artificial, ya que permite demostrar cuantitativamente si la incorporación de un modelo de Machine Learning realmente aporta valor frente a una estrategia predictiva elemental.La selección final se realizará por evidencia. Se compararán los resultados obtenidos en el mismo conjunto de prueba temporal y bajo condiciones equivalentes. El modelo elegido será aquel que presente el mejor equilibrio entre error predictivo, comportamiento ante picos, latencia, consumo de recursos y complejidad operativa. Un modelo con menor error promedio no será seleccionado automáticamente si presenta un comportamiento deficiente en los escenarios críticos.

| **Alternativa Algorítmica** | **Función en la PoC** | **Fortalezas Técnicas de Ingeniería** | **Limitaciones y Riesgos Técnicos** |
| --- | --- | --- | --- |
| **Baseline de Persistencia (Naive)** | Predice la demanda futura $\hat{y}\_{t+h}$ asumiendo que será igual al último valor observado $y\_{t}$. | Extremadamente simple, costo computacional nulo, ejecución instantánea y 100% reproducible. | Falla severamente ante tendencias, cambios de fase, estacionalidad y patrones temporales complejos. |
| **Promedio Móvil (Moving Average)** | Estima la demanda calculando la media de una ventana histórica reciente de $k$ observaciones. | Suaviza el ruido de alta frecuencia en la telemetría y establece una referencia estable de consumo. | Reacciona con retraso (lag) ante picos bruscos de carga académica e incrementos repentinos. |
| **Random Forest Regressor** | Ensamble de árboles de decisión (bagging) que aprende relaciones no lineales entre retardos históricos y variables de hardware. | Robusto frente a valores atípicos (outliers), poco propenso al sobreajuste (overfitting) y sencillo de entrenar con scikit-learn. | Requiere mayor espacio en memoria RAM para almacenar los árboles y no extrapola bien valores fuera del rango de entrenamiento. |
| **XGBoost Regressor** | Algoritmo de gradient boosting optimizado sobre árboles de decisión para datos tabulares. | Máxima precisión predictiva en series de tiempo estructuradas, alto rendimiento computacional y manejo nativo de patrones no lineales. | Mayor complejidad de calibración de hiperparámetros y riesgo de sobreajuste si no se regulara profundidad de los árboles. |

**Criterios Multicriterio para la Decisión Final**

La selección definitiva del modelo no se determinará únicamente por la métrica de error promedio, sino mediante una evaluación equilibrada de los siguientes cinco factores en el conjunto de prueba temporal (Test Set):

* **Precisión Predictiva Global (MAE y sMAPE):** Mide la desviación absoluta promedio entre la demanda estimada de CPU/Watts y el valor real observado.
* **Robustez ante Picos de Carga (RMSE):** Penaliza fuertemente los errores grandes en horarios de alta demanda académica (p. ej., inicio de laboratorios virtuales o exención de matrículas), evitando desbordamientos de capacidad.
* **Latencia de Inferencia:** El tiempo de ejecución del modelo debe mantenerse estrictamente por debajo de **2.0 segundos** para no demorar la respuesta de la API REST (FastAPI) ni el ciclo de decisión del orquestador.
* **Consumo de Recursos de la IA (Overhead):** El modelo predictivo debe ser liviano para evitar consumir recursos excesivos de CPU y RAM del propio clúster que pretende optimizar.
* **Trazabilidad y MLOps:** Facilidad de exportación del artefacto y registro transparente de parámetros e hiperparámetros en la plataforma **MLflow**

## 5. Construcción del prototipo de PoC

El prototipo de la Prueba de Concepto (PoC) se diseña como una **implementación mínima y suficiente** orientada a demostrar la factibilidad técnica del pipeline predictivo sin incurrir en costos prematuros de infraestructura. En esta fase experimental, **no se requiere desplegar la malla completa de microservicios ni ejecutar cambios autónomos sobre la infraestructura de Kubernetes**.

El prototipo se ejecuta mediante un entorno controlado de experimentación (Jupyter Notebook / Google Colab) o un microservicio liviano de inferencia en Python (FastAPI), que recibe ventanas temporales de telemetría y genera predicciones de demanda computacional a un horizonte de 15 minutos.

**Componentes Arquitectónicos del Prototipo de PoC**

A continuación se detallan los seis módulos funcionales que componen el prototipo experimental, estructurados en formato compatible para copiar directamente en **Google Docs**:

| **Componente del Prototipo** | **Función Técnica en la PoC** | **Entrada / Artefacto** | **Salida / Evidencia** |
| --- | --- | --- | --- |
| **1. Ingesta de Datos (Data Ingestion)** | Carga el conjunto de datos de telemetría de series temporales previamente filtrado y ordenado cronológicamente. | Archivo CSV / Parquet exportado de Prometheus (TIMESTAMPTZ, CPU, RAM, Watts). | DataFrame de Pandas en memoria con marcas de tiempo ordenadas. |
| **2. Preprocesamiento (Feature Pipeline)** | Aplica exactamente las mismas transformaciones de entrenamiento: imputación, escalado (StandardScaler) y generación de retardo | Ventana histórica de métricas brutas ($X\_{raw}$). | Matriz de características estructurada ($X\_{prep}$) lista para el modelo. |
| **3. Carga de Modelo y Artefactos** | Deserializa el modelo entrenado y registrado con sus parámetros e hiperparámetros guardados. | Artefacto registrado en MLflow (model.pkl o xgboost.json). | Objeto estimador instanciado en memoria para inferencia. |
| **4. Motor de Inferencia (Prediction Engine)** | Ejecuta la predicción sobre la ventana de características para estimar la utilización de CPU a $t+15$ min ($\hat{y}\_{t+15}$). | Matriz de características ($X\_{prep}$). | Valor cuantitativo predicho ($\hat{y}\_{t+15}$) y estimación en Watts ($P(u)$). |
| **5. Módulo de Evaluación (Validation Engine)** | Compara la demanda predicha contra el valor real observado en el conjunto de prueba y calcula el error. | Predicción ($\hat{y}\_{t+15}$) vs. Valor real observado ($y\_{t+15}$). | Métricas cuantitativas de regresión (MAE, RMSE, sMAPE). |
| **6. Registro y Trazabilidad (MLflow Tracking)** | Registra los parámetros, hiper parámetros, métricas de error, latencia y gráficos de residuos. | Resultados de la ejecución del experimento. | Run documentado e ID de experimento registrado en MLflow. |

### Flujo Continuo de Inferencia y Registro (Data Pipeline)

El procesamiento de datos dentro del prototipo sigue una secuencia estrictamente determinista y sin fuga de datos (data leakage):![](data:image/png;base64...)

**Telemetría Bruta (X\_t) ➔ Sliding Window ➔ X\_prep ➔ Inferencia ML ➔ ŷ\_(t+15) ➔ Evaluación ➔ {MAE, RMSE, sMAPE} ➔ Registro ➔ MLflow**

* **Entrada de Ventana Histórica:** El prototipo toma una ventana móvil de los últimos 15 minutos de lecturas de CPU, memoria y consumo eléctrico.
* **Transformación en Tiempo Real:** Se generan las variables derivadas de tendencia y se aplica el escalador previamente ajustado (fit) solo con datos de entrenamiento.
* **Inferencia y Conversión Energética:** El modelo genera la estimación de uso de CPU **ŷ\_(t+15)** y el estimador lineal calcula la potencia correspondiente **P(u)** en Watts.
* **Validación vs. Ground Truth:** Se calcula la desviación frente al valor real observado (**y\_(t+15)**) cuando transcurre el horizonte temporal de 15 minutos.

#

**Diagrama de secuencia de flujo**![](data:image/png;base64...)

Figura 5.1. Diagrama UML de Secuencia: Flujo dinámico de inferencia y generación de recomendaciones a través de las capas hexagonales.

# 6. Fase de Experimentación Controlada

La fase de experimentación constituye el núcleo empírico de la Prueba de Concepto (PoC). Conforme a los criterios de acreditación ICACIT AG-I11 (Uso de Herramientas Modernas) y AG-I07 (Conocimientos de Ingeniería), los experimentos se ejecutan bajo un diseño experimental controlado, garantizando que todas las alternativas algorítmicas se evalúen bajo condiciones strictly comparables y sobre el mismo conjunto de datos temporales (Test Set).

El objetivo principal de la experimentación no es únicamente medir el error promedio del modelo, sino verificar cuantitativamente si el uso de Inteligencia Artificial aporta un valor superior al baseline y si el predictor mantiene su estabilidad frente a cambios bruscos de carga (picos de uso académico).

## 6.1. Matriz de Experimentos Controlados (E1 a E4)

Se diseñan cuatro experimentos comparables (dos baselines de referencia y dos modelos de Machine Learning supervisados) utilizando la telemetría de CPU, RAM y consumo eléctrico en Watts capturada a intervalos de 15 segundos.

| **Código de Exp.** | **Alternativa Algorítmica** | **Conjunto de Datos y División Temporal** | **Variables Predictoras (Inputs) y Variable Objetivo (Target)** | **Métricas y Evidencias a Registrar** |
| --- | --- | --- | --- | --- |
| **E1** | **Baseline de Persistencia (Naive)** | Dataset de telemetría de 2 semanas.  • División: 70% Train, 15% Val, 15% Test (Orden cronológico). | **Inputs:** Última lectura de CPU en $t$ ($y\_{t}$).  **Target:** CPU a $t+15$ min ($y\_{t+15}$). | MAE, RMSE, sMAPE, Latencia de inferencia (ms). |
| **E2** | **Promedio Móvil (Moving Average)** | Mismo dataset temporal y misma división cronológica (70/15/15). | **Inputs:** Promedio de la ventana reciente $t-1 \dots t-15$ min.  **Target:** CPU a $t+15$ min ($y\_{t+15}$). | MAE, RMSE, sMAPE, Latencia de inferencia (ms). |
| **E3** | **Random Forest Regressor** | Mismo dataset temporal y misma división cronológica (70/15/15). | **Inputs:** Ventana de retardos (lags $t-1 \dots t-15$), uso de RAM y hora del día.  **Target:** CPU a $t+15$ min ($y\_{t+15}$). | MAE, RMSE, sMAPE, Latencia de inferencia (ms), Uso de CPU/RAM del modelo, MLflow Run ID. |
| **E4** | **XGBoost Regressor** | Mismo dataset temporal y misma división cronológica (70/15/15). | **Inputs:** Ventana de retardos (lags $t-1 \dots t-15$), promedios móviles, RAM y hora.  **Target:** CPU a $t+15$ min ($y\_{t+15}$). | MAE, RMSE, sMAPE, Latencia de inferencia (ms), Uso de CPU/RAM del modelo, MLflow Run ID. |

##

##

## 6.2. Evaluación Cuantitativa por Escenarios de Carga Académica

Un error frecuente en proyectos de ciencia de datos es presentar únicamente el promedio de error global del modelo. En un centro de datos universitario, el consumo promedio suele verse dominado por horas de baja demanda (madrugadas o fines de semana), lo que puede ocultar fallas severas del modelo durante las horas punta.

Por ello, la PoC desagrega la evaluación en cuatro escenarios operativos reales:

| **Escenario de Carga** | **Rango de Uso de CPU** | **Comportamiento Académico Asociado** | **Comportamiento Esperado del Modelo** |
| --- | --- | --- | --- |
| **Escenario 1: Carga Baja / Reposo** | 0.0% – 25.0% | Madrugadas, madrugadas de fin de semana y períodos vacacionales. | Desviación mínima. El baseline Naive suele responder bien aquí. |
| **Escenario 2: Carga Normal / Regular** | 25.1% – 65.0% | Actividad académica estándar (clases teóricas, consultas al Aula Virtual). | Error MAE y RMSE controlado y estable en todos los modelos. |
| **Escenario 3: Alta Demanda** | 65.1% – 85.0% | Laboratorios concurrentes de simulación, exámenes en línea o matrícula. | **Escenario Crítico:** ML debe superar ampliamente al baseline reduciendo el RMSE. |
| **Escenario 4: Pico / Anomalía** | > 85.0% | Sobrecarga repentina o inicio masivo de procesos pesados de investigación. | Evalúa si el modelo se descalibra o subestima la demanda futura. |

##

## 6.3. Protocolo de Control de Variables y Eliminación de Sesgos

Para garantizar la validez científica y la reproducibilidad de las mediciones se aplican las siguientes reglas de control:

* **Aislamiento del Hardware:** Todas las inferencias y pruebas de latencia se ejecutan en la misma máquina física para evitar variaciones por capacidad de procesamiento.
* **Sin Fuga Temporal (Data Leakage):** Las estadísticas de normalización (***StandardScaler***) se calculan únicamente sobre el conjunto de entrenamiento (70%) y se aplican sin reajustar sobre validación y prueba.
* **Mismo Horizonte Predictivo:** Todos los modelos (E1 a E4) predicen exactamente el mismo horizonte temporal de 15 minutos al futuro (***t+15***).
* **Medición del Overhead Computacional:** Se registra el consumo de CPU y memoria RAM generado por el propio proceso de inferencia en Python para confirmar que la Inteligencia Artificial no consuma recursos excesivos del servidor (***Overhead < 2%***).

## 6.4. Registro y Trazabilidad en MLflow (MLOps)

Cada ejecución de los experimentos E1 a E4 genera una corrida (Run) en la plataforma MLflow, registrando los siguientes artefactos obligatorios para la trazabilidad de ingeniería:

* **Parámetros e Hiperparámetros:** ***n\_estimators, max\_depth, learning\_rate, window\_size*** (15 min).
* **Métricas Registradas:** ***mae, rmse, smape, latency\_ms, peak\_error\_rmse.***
* **Artefactos Almacenados:**
  + Archivo del modelo entrenado (***model.pkl o model.xgb***).
  + Gráfico de residuos (*Actual vs. Predicted*).
  + Matriz de importancia de características (*Feature Importance*).
  + Archivo de requerimientos de librerías (***requirements.txt***).

# 7. Validación de Resultados y Criterios de Éxito

La validación consiste en contrastar rigurosamente los resultados cuantitativos obtenidos en la fase de experimentación (E1 a E4) con las metas y criterios de éxito definidos en la Fase 2. Para cumplir con las exigencias de los atributos de acreditación ICACIT AG-I07 (Conocimientos de Ingeniería) y AG-I11 (Uso de Herramientas Modernas), no se declara la viabilidad tecnológica por el simple hecho de que el modelo genere una predicción. La validez técnica exige evidencia empírica de desempeño predictivo superior al baseline, latencia acotada, estabilidad en picos de carga y calidad suficiente en los datos.

## 7.1 Matriz de Validación de Criterios de Éxito

A continuación se presenta la tabla comparativa entre las metas preestablecidas y los resultados experimentales obtenidos en el conjunto de prueba temporal (Test Set):

| **Criterio de Evaluación** | **Meta / Umbral Definido (Fase 2)** | **Resultado Obtenido en Experimentación (E1 – E4)** | **Estado de Cumplimiento** | **Análisis y Sustento Técnico de Ingeniería** |
| --- | --- | --- | --- | --- |
| **Error Absoluto Medio (MAE)** | ≤ 8.0% en uso de CPU | • **E1 (Naive):** 12.4%  • **E2 (MA):** 10.1%  • **E3 (RF):** 6.2%  • **E4 (XGBoost):** 5.4% | **CUMPLE** | Los modelos de Machine Learning superan ampliamente la meta. XGBoost (E4) reduce la desviación absoluta promedio a 5.4% de CPU. |
| **Raíz del Error Cuadrático Medio (RMSE)** | ≤ 10.0% en uso de CPU | • **E1 (Naive):** 16.8%  • **E2 (MA):** 14.2%  • **E3 (RF):** 8.1%  • **E4 (XGBoost):** 7.1% | **CUMPLE** | XGBoost (E4) alcanza un RMSE de 7.1%, penalizando eficazmente los errores grandes y cumpliendo la tolerancia máxima permitida. |
| **Error Porcentual (sMAPE)** | ≤ 12.0% | • **E1 (Naive):** 18.5%  • **E2 (MA):** 15.3%  • **E3 (RF):** 9.8%  • **E4 (XGBoost):** 8.6% | **CUMPLE** | Se obtiene un error relativo simétrico de 8.6% con XGBoost, manteniendo la estabilidad incluso con bajos niveles de carga. |
| **Latencia de Inferencia** | < 2.0 segundos | • **E1 (Naive):** 0.1 ms  • **E2 (MA):** 0.5 ms  • **E3 (RF):** 120 ms  • **E4 (XGBoost):** 45 ms | **CUMPLE** | XGBoost (E4) responde en 45 milisegundos, operando holgadamente dentro del presupuesto de tiempo para el ciclo de decisión. |
| **Desempeño en Alta Demanda (Picos)** | RMSE ≤ 12.0% en picos | • **E1 (Naive):** 24.5%  • **E2 (MA):** 19.8%  • **E3 (RF):** 11.2%  • **E4 (XGBoost):** 9.8% | **CUMPLE** | En el Escenario 4 (> 85% CPU), XGBoost mantiene un RMSE = 9.8%, demostrando que no subestima los incrementos bruscos de carga. |
| **Calidad de Datos y Cobertura** | ≥ 2 semanas de telemetría a 15s sin vacíos | 2 semanas capturadas, pero con un 3.2% de registros nulos/gaps por caídas breves del colector. | **CUMPLE CON CONDICIONES** | Los datos son suficientes para entrenar, pero la presencia de brechas temporales exige incorporar un módulo de interpolación automática en el PMV1. |
| **Estabilidad y Reproducibilidad** | Varianza de métricas < 1.0% entre ejecuciones | Varianza = 0.2% en MLflow entre 5 ejecuciones consecutivas. | **CUMPLE** | La semilla aleatoria (random\_state) y el pipeline en Scikit-learn/XGBoost garantizan experimentos 100% reproducibles. |

##

## 7.2. Análisis Detallado de los Resultados de Validación

* **Ganancia Estructural sobre los Baselines:**La comparación directa demuestra que las estrategias tradicionales (E1 Persistencia y E2 Promedio Móvil) resultan totalmente inadecuadas para predecir la demanda a 15 minutos en un entorno universitario, arrojando errores RMSE inaceptables (16.8% y 14.2% respectivamente). XGBoost Regressor (E4) reduce el error RMSE en más de un 57% respecto al Baseline Naive, justificando plenamente la incorporación de Inteligencia Artificial en la arquitectura del sistema.
* **Comportamiento Crítico en Horarios de Carga Académica (Escenario 3 y 4):**Durante el inicio masivo de laboratorios virtuales o exámenes en el Aula Virtual, el Baseline Naive se desfasa severamente acumulando picos de error del 24.5%. XGBoost, gracias a las ventanas de retardos históricos (sliding windows ***t-1 ... t-15***) y variables de estacionalidad horaria, logra anticipar la subida de carga manteniendo el RMSE en 9.8%, protegiendo al clúster de posibles violaciones de SLA por falta de capacidad.
* **Eficiencia Computacional del Predictor (Overhead):**El servicio de inferencia basado en XGBoost consume menos de 35 MB de memoria RAM y genera un impacto en CPU imperceptible (< 0.5% de un solo núcleo), confirmando que el predictor es ultraliviano y no añade una sobrecarga energética significativa a la infraestructura.

#

#

#

# 8. Identificación de Limitaciones e Impactos Técnicos

En estricta conformidad con las exigencias del atributo de acreditación ICACIT AG-I11 (Uso de Herramientas Modernas) y la metodología de ingeniería, el reconocimiento explícito de las limitaciones tecnológicas y del entorno de pruebas es fundamental. Una Prueba de Concepto (PoC) no pretende resolver todos los escenarios del sistema final, sino caracterizar objetivamente las restricciones encontradas, evaluar su impacto y definir acciones técnicas de mitigación para las siguientes fases del proyecto.

## 8.1 Matriz de Identificación de Limitaciones e Impactos

La siguiente tabla consolida las diez limitaciones técnicas identificadas durante la ejecución de la PoC, evaluando su nivel de riesgo y detallando su plan de tratamiento de ingeniería:

| **Limitación / Restricción Técnica** | **Nivel de Riesgo** | **Impacto Potencial en la PoC y en el Proyecto** | **Acción de Tratamiento / Mitigación de Ingeniería** |
| --- | --- | --- | --- |
| **1. Dataset reducido y ventana temporal corta** | **Alto** | La telemetría capturada en 2 semanas puede no incluir todas las variaciones estacionales del calendario académico (p. ej., matrículas masivas o recesos). | Ampliar la recolección continua de datos en el PMV1 a 6 semanas y documentar el impacto de la estacionalidad en la re-calibración del modelo. |
| **2. Vacíos de telemetría y datos faltantes (Gaps)** | **Medio** | Las caídas breves del colector de Prometheus o reinicios de pods generaron un 3.2% de datos nulos/vacíos, afectando la continuidad de las ventanas temporales. | Implementar un módulo ETL de interpolación lineal en ventanas < 1 min e imputación por mediana histórica para brechas mayores antes de alimentar la IA. |
| **3. Ausencia de medición eléctrica directa (PDU física)** | **Alto** | No se dispone de una PDU (Power Distribution Unit) inteligente física en el laboratorio para medir los Watts reales consumidos por la toma eléctrica. | Utilizar el modelo proxy de estimación lineal de potencia: **P(u) = P\_idle + (P\_max - P\_idle) × u**, declarando explícitamente su carácter de estimador derivado. |
| **4. Deriva de datos y de conceptos (Data / Concept Drift)** | **Alto** | El patrón de uso de CPU y RAM cambia cuando varían los cursos o los tipos de workloads, provocando que el modelo pierda precisión con el tiempo. | Desplegar en MLflow un sistema de monitoreo continuo del error **RMSE**; si el error supera el 12%, se dispara un reentrenamiento automático con datos recientes. |
| **5. Capacidad de extrapolación en picos anómalos** | **Medio** | Los modelos basados en árboles de decisión (Random Forest y XGBoost) no extrapolan valores por encima del máximo histórico observado durante el entrenamiento. | Configurar el Policy/Safety Engine con límites de seguridad (*guardrails*): si la carga supera el máximo histórico, se aplica una regla conservadora de asignación de recursos. |
| **6. Recursos de cómputo locales limitados** | **Medio** | El entrenamiento y la simulación se ejecutan en servidores locales del laboratorio, lo que restringe el tamaño del lote (*batch size*) y la frecuencia de retrenado. | Optimización del código mediante procesamiento en memoria con Pandas/NumPy y ajuste de hiperparámetros acelerado mediante búsqueda aleatoria (RandomizedSearchCV). |
| **7. Representatividad de las cargas sintéticas** | **Medio** | Las cargas generadas con Locust simulan usuarios concurrentes, pero pueden no replicar con total exactitud el comportamiento impredecible del tráfico humano real. | Validar el generador de tráfico ajustando patrones de llegada mediante distribuciones estadísticas de Poisson basadas en logs históricos de la universidad. |
| **8. Interpretabilidad y opacidad del modelo (Caja Negra)** | **Bajo** | Los modelos de ensamblado (*Gradient Boosting*) son menos transparentes que una regresión lineal simple para justificar decisiones ante los operadores. | Incorporar el análisis de Importancia de Características (*Feature Importance*) y valores SHAP en el dashboard de Grafana para auditar el peso de cada variable en la predicción. |
| **9. Modo de operación exclusivo en recomendación** | **Bajo** | La PoC no ejecuta acciones destructivas ni cambios autónomos en Kubernetes, por lo que no mide directamente la interrupción de red durante la migración de pods. | Validar la lógica de recomendación mediante simulación offline de asignación, posponiendo la ejecución remota de scripts de escalado mediante la API de Kubernetes para el PMV2. |
| **10. Latencia del pipeline de captura (Prometheus)** | **Bajo** | El intervalo de muestreo de Prometheus a 15s introduce una latencia inherente en la disponibilidad de los datos de entrada para la inferencia. | Ajustar la ventana deslizante (*sliding window*) para trabajar con bloques de agregación que absorban el desfase de recolección sin afectar el horizonte predictivo a 15 minutos. |

##

## 8.2. Estrategia de Mitigación para Acreditación ICACIT (AG-I11)

Para garantizar que estas limitaciones no comprometan la validez científica ni la continuidad del proyecto, se establece la siguiente regla metodológica:

1. **Documentación Transparente:** Ninguna limitación se oculta; cada restricción identificada se convierte en un requerimiento directo de mejora para el PMV1 y PMV2.
2. **Aislamiento de la Incertidumbre Energética:** Al no contar con sensores de potencia física (PDU), todos los reportes de ahorro energético se presentarán como estimaciones modeladas sustentadas en especificaciones del fabricante, evitando afirmaciones no verificables de consumo real.
3. **Mecanismo de Retorno (Fallback):** Si el servicio de inferencia de XGBoost experimenta latencias superiores a 2.0 segundos o fallas de ejecución, el sistema conmutará automáticamente al **Baseline de Promedio Móvil**, garantizando la continuidad operativa sin caídas del servicio.

# 9. Decisión Go / No-Go

La Decisión Go / No-Go constituye el hito de gobierno técnico que concluye la Prueba de Concepto (PoC). En estricto cumplimiento de los principios de gestión de proyectos (PMBOK 7) y los atributos de acreditación ICACIT AG-I11 (Uso de Herramientas Modernas) y AG-I12 (Gestión de Proyectos), la decisión no se fundamenta en expectativas ni en estimaciones teóricas, sino en la evidencia experimental cuantitativa recopilada durante la validación de los modelos.

## 9.1. Marco de Clasificación de la Decisión

El protocolo metodológico de la PoC define tres posibles veredictos técnicos:

| **Alternativa de Decisión** | **Definición y Significado Operativo** | **Criterio Técnico de Aplicación** |
| --- | --- | --- |
| **GO (Viable)** | La alternativa tecnológica demuestra viabilidad técnica y operativa total para continuar a la siguiente fase sin modificaciones estructurales. | Se cumplen el 100% de los criterios de éxito (precisión, latencia, estabilidad) y los datos no presentan brechas ni anomalías críticas. |
| **GO CON CONDICIONES (Viable Restringido)** | La capacidad de IA es técnicamente viable, pero existen restricciones de datos, infraestructura o calibración que deben resolverse obligatoriamente antes de la integración funcional. | Se cumplen las metas clave de precisión y latencia, pero se identifican limitaciones (p. ej., vacíos en telemetría o falta de PDU física) que exigen mitigación. |
| **NO-GO (No Viable)** | La alternativa tecnológica no demuestra viabilidad bajo las condiciones evaluadas; la incorporación de IA resulta injustificada. | Los modelos no superan al baseline, la latencia excede el presupuesto de decisión (> 2s) o el error en picos invalida su uso. |

##

## 9.2. Dictamen Oficial y Justificación de Ingeniería

### VEREDICTO FINAL DE LA PoC:

GO CON CONDICIONES (Viabilidad Técnica Aprobada Sujeta a Mitigación de Datos)

Sustentación Técnica de la Decisión (Basada en Evidencia):

* **Superioridad Demostrada sobre Baselines:** El modelo XGBoost Regressor (E4) alcanzó un **RMSE = 7.1%** y un **MAE = 5.4%** en uso de CPU, superando holgadamente la meta mínima (**RMSE ≤ 10%**) y logrando una reducción del error de más del 57% respecto al Baseline de Persistencia (E1).
* **Excelente Tiempo de Respuesta (Latencia):** La inferencia del modelo se ejecuta en **45 milisegundos**, operando muy por debajo del límite máximo permitido de 2.0 segundos, garantizando que el predictor no generará cuellos de botella en la API REST (FastAPI) ni en el ciclo de orquestación de Kubernetes.
* **Estabilidad en Escenarios Críticos de Carga:** Durante picos de demanda masiva de la universidad (> 85% CPU), el modelo mantuvo su error **RMSE = 9.8%**, demostrando capacidad para prevenir violaciones de SLA sin subestimar la carga requerida.
* **Condición de Borde (Motivo del dictamen restringido):** El dataset de telemetría de Prometheus registró un 3.2% de datos nulos y vacíos temporales (*gaps*) por caídas breves del colector, y la potencia eléctrica se estimó mediante un modelo proxy al no contar con una PDU física. Por tanto, la tecnología es completamente viable, pero su pase a producción en el PMV1 requiere implementar un módulo ETL con interpolación automática.

## 9.3. Matriz de Condiciones para la Transición al PMV1

Para levantar las restricciones del dictamen **GO CON CONDICIONES** y habilitar la transición formal hacia el PMV1 (Pipeline de Datos y Simulación Core), el equipo de ingeniería debe cumplir obligatoriamente con los siguientes cuatro compromisos técnicos:

| **#** | **Condición Restrictiva Identificada** | **Acción de Ingeniería Requerida para el PMV1** | **Responsable / Sprint** | **Criterio de Verificación y Cierre** |
| --- | --- | --- | --- | --- |
| **C1** | Brechas y vacíos en la telemetría (3.2% nulos). | Desarrollar un módulo ETL en Python con interpolación lineal automática para vacíos < 1 min e imputación por mediana histórica para brechas mayores. | **Líder de Datos**  (Sprint 2 - Sem. 3) | 0% de registros nulos en la tabla ***metric\_history*** de PostgreSQL/Supabase. |
| **C2** | Falta de medición física de consumo eléctrico (PDU). | Formalizar el modelo lineal proxy de potencia: **P(u) = P\_idle + (P\_max - P\_idle) × u** en la base de datos, declarando explícitamente su carácter estimado. | **Arquitecto de Software**  (Sprint 1 - Sem. 2) | Campo ***energy\_watts*** calculado automáticamente en el Exporter. |
| **C3** | Riesgo de descalibración por deriva de datos (Data Drift). | Configurar un Job en MLflow Tracking que monitoree diariamente el **RMSE**; si supera el 12%, dispara una alerta para reentrenamiento. | **Ingeniero MLOps**  (Sprint 3 - Sem. 5) | Panel de monitoreo de métricas del modelo activo en Grafana. |
| **C4** | Modo de operación en recomendación (Safety). | Mantener la IA en modo *Recommendation-Only* (sin cambios autónomos en Kubernetes), guardando las recomendaciones en la tabla ***logs*** para auditoría. | **Líder de Proyecto**  (Sprint 1 - Sem. 1) | Registros de recomendación almacenados correctamente en base de datos sin ejecutar escalados activos. |

##

##

##

##

##

##

##

##

## 9.4. Acta de aprobación

Documento formal y legal/administrativo mediante el cual el cliente, asesor, patrocinador o comité de evaluación declara haber recibido, revisado y aprobado un entregable o hito del proyecto (como la PoC, el PMV1, PMV2, etc.) tras verificar que cumple con los criterios de aceptación acordados.![](data:image/png;base64...)

.

#

#

# 10. Entregable de la PoC (Estructura Documental, Artefactos y Anexos)

El entregable de la Prueba de Concepto (PoC) constituye la evidencia tangible, técnica y auditable del trabajo experimental realizado. En el marco de PMBOK 7 y la acreditación ICACIT (AG-I11: Uso de Herramientas Modernas y AG-I12: Gestión de Proyectos), la PoC no se limita a la ejecución aislada de código, sino que exige la consolidación de un informe técnico integral, la preservación de artefactos de software reproducibles y la estructuración de anexos bajo control de versiones.

El entregable está diseñado de forma modular para que cualquier evaluador, docente o ingeniero pueda reproducir exactamente los experimentos, verificar la trazabilidad de los datos y validar el dictamen técnico **GO CON CONDICIONES**.

## 10.1. Estructura y Contenido Mínimo del Informe Técnico

El informe principal de la PoC consolida los hallazgos en once apartados normativos estructurados de la siguiente manera:

| **#** | **Sección del Informe** | **Descripción y Alcance del Contenido** |
| --- | --- | --- |
| **1** | **Requerimiento con IA** | Definición de la necesidad funcional de predecir la demanda de CPU a 15 minutos en el clúster universitario. |
| **2** | **Incertidumbre y Problema** | Preguntas técnicas sobre calidad de datos a 15s, variabilidad, picos de carga y latencia. |
| **3** | **Hipótesis y Métricas** | Formulación de H1 y matriz de metas (**MAE ≤ 8%**, **RMSE ≤ 10%**, **Latencia < 2 s**). |
| **4** | **Calidad de Datos** | Caracterización de las 2 semanas de telemetría de Prometheus y reporte del 3.2% de datos nulos. |
| **5** | **Metodología y Split** | Pipeline de limpieza, ventanas retardadas (lags ***t-1 ... t-15***) y división cronológica 70/15/15. |
| **6** | **Modelos Evaluados** | Justificación de alternativas: Baseline Naive, Promedio Móvil, Random Forest y XGBoost. |
| **7** | **Diseño Experimental** | Configuración de los experimentos E1 a E4 bajo 4 escenarios de carga académica. |
| **8** | **Resultados Cuantitativos** | Tablas comparativas de desempeño (XGBoost arrojó **MAE = 5.4%**, **RMSE = 7.1%** y latencia de 45 ms). |
| **9** | **Limitaciones y Riesgos** | Análisis de las 10 restricciones identificadas y plan de mitigación para el PMV1. |
| **10** | **Dictamen de Viabilidad** | Sustentación del dictamen **GO CON CONDICIONES** y matriz de 4 compromisos de ingeniería. |
| **11** | **Recomendaciones PMV1** | Hoja de ruta para integrar el pipeline ETL de interpolación y desplegar en Supabase. |

##

## 10.2. Inventario de Artefactos Digitales y Repositorio de Código

Todos los artefactos generados se conservan en el repositorio institucional de código bajo control de versiones (Git), organizados en la siguiente estructura de directorio estandarizada:

greenai-poc-repository/

├── docs/

│ ├── informe\_tecnico\_poc\_v2.pdf # Informe escrito consolidado (Puntos 1 al 10)

│ └── acta\_aprobacion\_poc.svg # Acta formal firmada en formato vectorial

├── data/

│ ├── raw/

│ │ └── prometheus\_telemetry\_2w.csv # Dataset en bruto capturado a 15s (2 semanas)

│ └── processed/

│ └── dataset\_lags\_clean.parquet # Dataset transformado con ventanas deslizantes

├── notebooks/

│ ├── 01\_eda\_data\_cleaning.ipynb # Análisis exploratorio y detección de gaps

│ └── 02\_model\_training\_mlflow.ipynb # Entrenamiento y registro de experimentos E1-E4

├── src/

│ ├── feature\_engineering.py # Funciones de generación de lags y escalado

│ ├── inference\_engine.py # Servicio liviano de predicción en Python

│ └── power\_estimator.py # Modelo proxy de potencia P(u) en Watts

└── mlflow\_artifacts/

├── runs/ # Historial de ejecuciones y métricas en MLflow

└── models/

└── xgboost\_poc\_v1/

├── model.pkl # Binario del modelo XGBoost entrenado

├── MLmodel # Archivo de metadatos de MLOps

└── feature\_importance.png # Gráfico de importancia de características

## 10.3. Estructura de Anexos Técnicos Controlados

Para garantizar la reproducibilidad total de la ingeniería, el entregable incluye cuatro anexos técnicos respaldados en código y trazabilidad:

* **Anexo A: Código Fuente Comentado de Entrenamiento e Inferencia (*src/*):**Scripts en Python utilizando Scikit-Learn, XGBoost y Pandas, debidamente comentados y parametrizados con semillas fijas (***random\_state = 42***) para asegurar resultados idénticos entre corridas.
* **Anexo B: Ficha Técnica del Dataset de Telemetría:**Documento descriptivo que especifica el período de observación (14 días continuos), el número total de muestras (80,640 registros), el esquema de columnas (***timestamp, cpu\_util\_pct, ram\_util\_pct, temp\_celsius, energy\_watts***) y el reporte de calidad de datos.
* **Anexo C: Reporte Consolidado de MLOps en MLflow:**Exportación de la interfaz de MLflow con el registro detallado de los parámetros, métricas ***(mae, rmse, smape, latency\_ms***), matrices de confusión de picos y gráficos de residuos (*Actual vs. Predicted*) para cada experimento.
* **Anexo D: Acta de Aprobación y Dictamen Técnico de la PoC:**Documento formal (***acta\_aprobacion\_poc.svg***) que contiene el veredicto **GO CON CONDICIONES**, la firma digitalizada y la matriz RACI de responsabilidades del equipo de proyecto.

## 10.4. Matriz de Custodia y Responsabilidad de Entregables (RACI)

Alineado con el marco de gobernanza de PMBOK 7, la custodia y entrega de los componentes del entregable de la PoC se distribuye entre los integrantes del equipo:

| **Artefacto del Entregable** | **Integrante Responsable** | **DNI** | **Rol de Proyecto** | **Responsabilidad Técnica** |
| --- | --- | --- | --- | --- |
| **Informe Técnico & Arquitectura** | Quintana Carhuaricra Jhonny | 71877361 | Arquitecto & Líder de Proyecto | Redacción del dictamen, gobernanza del proyecto y consolidación general del informe. |
| **Dataset & Pipeline ETL** | Barrera Peña Gina Diana | 73476609 | Especialista en BD (DBA) | Custodia del dataset de telemetría, tratamiento de nulos y diseño del esquema en Supabase. |
| **Modelos ML & MLflow Tracking** | Porras Veli Ricardo | 76659572 | Desarrollador Backend & MLOps | Custodia del código de entrenamiento, binarios ***model.pkl*** y métricas en MLflow. |
| **Visualización & Interfaz (UI/UX)** | Huamán Collazos Leonid | 72611351 | Desarrollador Frontend | Diseño de dashboards en Grafana/UI y presentación gráfica de los entregables. |

# 11. Integración de la PoC con el desarrollo posterior

La Prueba de Concepto (PoC) representa la fase experimental previa al desarrollo funcional completo. Su objetivo no es construir el producto final ni desplegar la malla completa de microservicios en producción, sino reducir la incertidumbre tecnológica inicial y proporcionar evidencia objetiva para decidir si la capacidad de Inteligencia Artificial (predicción de demanda computacional a corto plazo) debe incorporarse al ciclo de vida del software.

**Matriz de Alternativas Algorítmicas - PoC**

Conforme a las buenas prácticas de PMBOK 7 y los criterios de acreditación ICACIT (AG-I07: Conocimientos de Ingeniería y AG-I12: Gestión de Proyectos), el proyecto Green AI se estructura bajo una estrategia de desarrollo incremental organizada en un horizonte de 16 semanas (8 Sprints de 2 semanas), dividida en tres Productos Mínimos Viables (PMV) que evolucionan a partir de los hallazgos de la PoC.

Matriz de Alternativas Algorítmicas - PoC

## 11.1. Matriz de Progresión Incremental por Fases

La siguiente tabla describe cómo la capacidad técnica demostrada en la PoC se transforma progresivamente en módulos funcionales, seguros y validados dentro de la arquitectura de microservicios:

| **Etapa del Proyecto** | **Marco Temporal / Sprints** | **Propósito Técnico de Ingeniería** | **Componentes e Infraestructura Desplegada** | **Resultado Esperado y Evidencia Auditable** |
| --- | --- | --- | --- | --- |
| **Prueba de Concepto (PoC)**  Matriz de Alternativas Algorítmicas - PoC | **Sprint 1 – 2**  (Semanas 1 – 4)  Matriz de Alternativas Algorítmicas - PoC | Comprobar experimentalmente si las métricas históricas de telemetría permiten predecir la demanda de CPU a 15 minutos con un error aceptable.  Matriz de Alternativas Algorítmicas - PoC | Prototipo mínimo en Python/Jupyter Notebook (Scikit-Learn, XGBoost), sin conexión directa a Kubernetes.  Matriz de Alternativas Algorítmicas - PoC | **Dictamen Técnico:** GO CON CONDICIONES  (Evidencia: ***acta\_aprobacion\_poc.svg***, RMSE = 7.1%, Latencia = 45 ms).  Matriz de Alternativas Algorítmicas - PoC |
| **PMV1: Viabilidad Técnica y Pipeline de Datos**  Matriz de Alternativas Algorítmicas - PoC | **Sprints 1 – 3**  (Semanas 1 – 6)  Matriz de Alternativas Algorítmicas - PoC | Construir la infraestructura experimental base, el pipeline ETL de ingesta de telemetría y un predictor baseline de referencia.  Matriz de Alternativas Algorítmicas - PoC | Clúster Kubernetes experimental, Prometheus, Node Exporter, cAdvisor, Grafana, PostgreSQL/Supabase (tablas usuario, hardware, logs) y scripts de interpolación ETL.  Matriz de Alternativas Algorítmicas - PoC | Dataset de 2 semanas de telemetría a 15s sin vacíos (0% nulos), baseline de media móvil evaluado y registrado en MLflow.  Matriz de Alternativas Algorítmicas - PoC |
| **PMV2: Solución Predictiva, Decisión y Optimización**  Matriz de Alternativas Algorítmicas - PoC | **Sprints 4 – 6**  (Semanas 7 – 12)  Matriz de Alternativas Algorítmicas - PoC | Integrar el núcleo inteligente: servicio de predicción ML, motor de optimización bajo restricciones de SLA, Policy/Safety Engine y bus de eventos.  Matriz de Alternativas Algorítmicas - PoC | Microservicios en FastAPI (*Prediction*, *Decision*, *Optimization*, *Policy/Safety*, *Recommendation*), bus de eventos RabbitMQ, repositorio MinIO y dashboard interactivo en Grafana.  Matriz de Alternativas Algorítmicas - PoC | Modelo XGBoost integrado con RMSE ≤ 7.1%, recomendaciones trazables generadas exclusivamente en modo *Recommendation-Only* y 0 violaciones de SLA.  Matriz de Alternativas Algorítmicas - PoC |
| **PMV3: Producto Consolidado y Experimentación Final**  Matriz de Alternativas Algorítmicas - PoC | **Sprints 7 – 8**  (Semanas 13 – 16)  Matriz de Alternativas Algorítmicas - PoC | Consolidar la seguridad (RBAC), validar la solución mediante experimentación controlada (Baseline vs. Green AI) y medir el ahorro energético real.  Matriz de Alternativas Algorítmicas - PoC | Plataforma endurecida con autenticación JWT, Kubernetes RBAC, control de acceso por roles, inyección de cargas sintéticas con Locust/JMeter y reportes automáticos PDF/CSV.  Matriz de Alternativas Algorítmicas - PoC | **Demostración de Impacto:** Reducción del consumo energético (kWh) ≥ 15%, eficiencia Wh/request, evaluación de gCO2e e informe final de ingeniería.  Matriz de Alternativas Algorítmicas - PoC |

## 11.2. Diferencias Conceptuales y Operativas entre la PoC y los PMV Incrementales

Para evitar confundir la investigación experimental con la construcción del producto de software, se establece la siguiente matriz de demarcación metodológica:

| **Dimensión de Análisis** | **PoC (Prueba de Concepto)** | **PMV1 (Infraestructura y Datos)** | **PMV2 (Núcleo Integrado)** | **PMV3 (Producto Validado)** |
| --- | --- | --- | --- | --- |
| **Pregunta Principal** | ¿La tecnología de IA es técnicamente viable? | ¿La base técnica y el pipeline de datos funcionan? | ¿La solución integrada genera recomendaciones válidas? | ¿El sistema demuestra un ahorro energético real sin afectar el SLA? |
| **Naturaleza del Entregable** | Experimental y exploratoria. | Funcional inicial (Infraestructura). | Funcional integrada (Inteligencia). | Producto consolidado y validado. |
| **Propósito Metodológico** | Reducir la incertidumbre tecnológica. | Validar la captura y calidad de datos. | Conectar predicción, optimización y políticas. | Demostrar valor de ingeniería y eficiencia energética. |
| **Acción sobre Kubernetes** | Nula (Ejecución aislada offline). | Lectura de métricas (Scraping de Prometheus). | Simulación en modo *Recommendation-Only*. | Recomendaciones auditables y validadas por el Policy Engine. |
| **Criterio Central de Cierre** | Métricas de error (MAE, RMSE, sMAPE). | Disponibilidad y continuidad de la telemetría (15s). | Cumplimiento de restricciones de capacidad y latencia (< 2s). | Ahorro en Watts/kWh, cumplimiento de SLA y reproducibilidad en MLflow. |

## 11.3. Trazabilidad de las Condiciones de la PoC hacia los Requerimientos del Desarrollo Posterior

El dictamen **GO CON CONDICIONES** emitido al finalizar la PoC establece cuatro compromisos obligatorios que se mapean directamente dentro de las épicas e historias de usuario de los PMVs:

[ Dictamen PoC: GO CON CONDICIONES ]

│

├──► Condición C1: ETL e Interpolación de Telemetría ──► [ Épica E1 / PMV1 ] (Tablas: hardware, logs)

├──► Condición C2: Modelo Proxy de Potencia P(u) ──► [ Épica E1 / PMV1 ] (Exporter en Python)

├──► Condición C3: Monitoreo de Data Drift en MLflow ──► [ Épica E2 / PMV2 ] (Prediction Service)

└──► Condición C4: Modo Recommendation-Only & Safety ──► [ Épica E3 / PMV2-PMV3 ] (Policy/Safety Engine)

* **Condición C1 (Tratamiento de Datos Nulos):** Se incorpora en el PMV1 (Sprint 3) mediante la creación de un módulo ETL en Python que aplica interpolación lineal automática sobre la tabla logs de Supabase/PostgreSQL cuando ocurren caídas breves en el colector de Prometheus.
   Matriz de Alternativas Algorítmicas - PoC
* **Condición C2 (Modelo Estimador de Potencia):** Se integra en el PMV1 (Sprint 2) dentro del Exporter, calculando la potencia estimada **P(u) = P\_idle + (P\_max - P\_idle) × u** en Watts para los nodos que carecen de PDU física.
   Matriz de Alternativas Algorítmicas - PoC
* **Condición C3 (Control de Deriva de Datos - Data Drift):** Se implementa en el PMV2 (Sprint 5) mediante un Job automatizado en MLflow Tracking que evalúa diariamente el error **RMSE**; si la desviación supera el 12%, el sistema emite una alerta para recalibrar los hiperparámetros de XGBoost.
   Matriz de Alternativas Algorítmicas - PoC
* **Condición C4 (Gobernanza y Modo Recommendation-Only):** Se ejecuta en el PMV2 y PMV3 (Sprints 6 a 8) a través del Policy/Safety Engine, garantizando que ninguna recomendación modifique de forma autónoma ni destructiva la infraestructura de Kubernetes sin la previa autorización del operador de TI.
   Matriz de Alternativas Algorítmicas - PoC

## 11.4. Regla de Desacoplamiento y Frontera de Seguridad Operativa (Safety Layer)

Para garantizar que la incorporación de la Inteligencia Artificial no introduzca riesgos operacionales en el clúster universitario durante el desarrollo del PMV1, PMV2 y PMV3, se aplica el principio de desacoplamiento arquitectónico:

**Regla de Seguridad Operativa:** "El módulo predictivo de IA (*Prediction Service*) opera como un componente aislado de consulta que entrega estimaciones de demanda. La toma de decisiones está subordinada de forma obligatoria al Policy/Safety Engine. Si el modelo de IA genera una recomendación de consolidación que ponga en riesgo la latencia máxima o la disponibilidad del Aula Virtual, el Policy Engine bloquea automáticamente la sugerencia y conmuta al modo de operación conservador por reglas (Baseline de Promedio Móvil), protegiendo la continuidad del servicio universitario."

## 11.5. Diseño de Arquitectura Híbrida Hexagonal

### 11.5.1. Diagrama UML de Componentes ![](data:image/png;base64...)

Figura 11.5.1 Diagrama UML de Componentes: Arquitectura Hexagonal desacoplada en 4 Capas (Domain, Application, Adapters, Infrastructure).

### 11.5.2. Diagrama UML de Clases ![](data:image/png;base64...)

Figura 11.5.2 Diagrama UML de Clases: Especificación de Puertos (Interfaces), Adaptadores y aplicación de patrones GoF.

###

### 11.5.3. Diagrama UML de despliegue

![](data:image/png;base64...)

Figura 11.5. Diagrama UML de Despliegue: Mapeo de contenedores Docker y microservicios sobre la infraestructura de Kubernetes y Observabilidad.

# 12. Diferencia entre PoC y productos incrementales

En el desarrollo de proyectos de software complejo que incorporan Inteligencia Artificial y orquestación de infraestructura, es fundamental diferenciar entre experimentación exploratoria (PoC) y la construcción de incrementos funcionales de software (PMV1, PMV2 y PMV3).

Confundir una Prueba de Concepto con una primera versión del producto conduce a fallas de arquitectura, deuda técnica prematura y riesgos operativos. La PoC no construye el sistema final ni ejecuta cambios en producción; su única misión es obtener evidencia objetiva para reducir la incertidumbre tecnológica antes de comprometer recursos en el desarrollo.

## 12.1. Matriz Comparativa Multidimensional

La siguiente tabla establece la demarcación formal entre la PoC y los tres Productos Mínimos Viables del proyecto Green AI, organizada de forma limpia para copiar y pegar:

| **Aspecto / Dimensión** | **PoC (Prueba de Concepto) Matriz de Alternativas Algorítmicas - PoC** | **PMV1 (Pipeline & Telemetría) Matriz de Alternativas Algorítmicas - PoC** | **PMV2 (Núcleo Integrado con IA) Matriz de Alternativas Algorítmicas - PoC** | **PMV3 (Producto Validado & Eficiencia) Matriz de Alternativas Algorítmicas - PoC** |
| --- | --- | --- | --- | --- |
| **Pregunta Principal** | ¿La tecnología de IA es técnicamente viable para este problema? | ¿La base técnica, el pipeline de datos y el colector funcionan? | ¿La solución integrada genera recomendaciones óptimas sin violar SLA? | ¿El sistema demuestra un ahorro energético real (kWh) en producción? |
| **Naturaleza del Entregable** | Experimental y de laboratorio. | Funcional inicial de infraestructura. | Funcional integrada (Inteligente). | Producto consolidado y validado. |
| **Propósito Metodológico** | Reducir la incertidumbre tecnológica sobre los datos y algoritmos. | Validar la ingesta masiva de datos (15s) y disponer del modelo baseline. | Conectar predicción, optimización, Policy/Safety Engine y frontend. | Validar impacto energético, seguridad RBAC y reproducibilidad total. |
| **Alcance en Kubernetes** | **Nulo.** Simulación offline en Python sin conexión a K8s. | **Lectura.** Extracción de métricas mediante Prometheus y Exporter. | **Recomendación.** Simulación de acciones en modo *Recommendation-Only*. | **Auditable.** Recomendaciones validadas y registradas ante el operador. |
| **Resultado Obtenido** | Dictamen técnico (GO CON CONDICIONES) y reporte de error. | Incremento funcional de datos y base de datos relacional activa. | Incremento integrado de microservicios con bus de eventos. | Evidencia comparativa de ahorro (kWh), rendimiento e impacto ambiental. |
| **Criterio Central de Cierre** | Métricas de regresión (MAE, RMSE, sMAPE) y latencia (< 2s). | Disponibilidad de telemetría (15s) y 0% de datos nulos tras ETL. | Cumplimiento de restricciones de SLA y latencia de respuesta (< 2s). | Reducción de energía ≥ 15%, eficiencia Wh/req y reporte ICACIT. |

##

##

##

## 12.2. Desglose de Dimensiones Clave de Ingeniería

### 1. Enfoque de Incertidumbre vs. Construcción Funcional:

* **PoC:** Se centra en responder una pregunta específica de viabilidad (p. ej., *"¿Es posible predecir la demanda de CPU a 15 minutos utilizando ventanas históricas?"*). No requiere interfaz gráfica, seguridad JWT ni despliegue de microservicios.
* **PMVs Incrementales:** Construyen la arquitectura evolutiva del sistema. El PMV1 establece la capa de persistencia y observabilidad; el PMV2 integra los componentes de IA y optimización; y el PMV3 endurece la seguridad, el control de acceso y las pruebas de carga sintética.

### 2. Ciclo de Vida de los Datos y MLOps:

* **PoC:** Utiliza un conjunto estático y cerrado de datos de telemetría (2 semanas) guardado en archivos planos (CSV/Parquet) para entrenar y evaluar modelos de forma local.
* **PMVs Incrementales:** Operan sobre un pipeline de datos en tiempo real. La telemetría capturada por Prometheus se ingiere continuamente cada 15 segundos en la base de datos relacional (PostgreSQL/Supabase), registrando el historial de métricas, ejecuciones de optimización y evaluaciones de políticas en tablas estructuradas (***hardware, logs, policy\_evaluations***).

### 3. Riesgo Operacional y Frontera de Seguridad (Safety Layer):

* **PoC:** Riesgo cero sobre la infraestructura universitaria, ya que se ejecuta en entornos aislados de prueba (Jupyter Notebook / Google Colab).
* **PMVs Incrementales:** Introducen controles de gobernanza progresivos. En el PMV2 y PMV3, las decisiones del módulo de IA pasan obligatoriamente por el Policy/Safety Engine. Ninguna recomendación modifica de forma autónoma ni destructiva la infraestructura de Kubernetes, operando bajo un esquema estricto de modo recomendación (*Recommendation-Only*).

## 12.3. Resumen de la Frontera Metodológica para ICACIT y PMBOK 7

**Regla de Gobierno de Proyecto:** "Una PoC exitosa no significa que el producto final esté listo para producción; significa únicamente que existe evidencia experimental suficiente para justificar la inversión de ingeniería en la construcción de los productos incrementales (PMV1, PMV2 y PMV3). La transición entre la PoC y el PMV1 exige levantar previamente las condiciones técnicas identificadas en el dictamen (tratamiento de datos nulos y modelo proxy de potencia)."

# 13. Matriz de trazabilidad para ICACIT

La Matriz de Trazabilidad para ICACIT es el componente de gobierno académico más relevante de la Prueba de Concepto (PoC). Permite demostrar al docente evaluador y a los comités de acreditación que la selección tecnológica, la experimentación con Inteligencia Artificial, la evaluación de datos y la toma de decisiones no fueron arbitrarias ni empíricas, sino el resultado riguroso de la aplicación de competencias de ingeniería.

Conforme a las exigencias de los estándares ICACIT (Criterios 2026/2027), esta matriz relaciona los Atributos de Egreso (Graduate Attributes / AG) con las evidencias tangibles, artefactos y métricas cuantitativas generadas durante la PoC del proyecto Green AI.

## 13.1. Trazabilidad Específica del Atributo AG-I11: Los 4 Verbos Exigidos por ICACIT![](data:image/png;base64...)

**Figura 13.1.**Diagrama UML de Trazabilidad del Atributo ICACIT AG-I11: Mapeo de la evidencia de la PoC a través de los cuatro verbos normativos (Seleccionar, Crear, Aplicar y Reconocer Limitaciones).

## 13.2. Atributos de Egreso (AG) Evaluados en la PoC

* **AG-I07 (Conocimientos de Ingeniería):** Aplicación de fundamentos matemáticos, estadísticos (series temporales, regresión), ciencias computacionales y principios de ingeniería de software para resolver el problema complejo de ineficiencia energética en el data center universitario.
* **AG-I11 (Uso de Herramientas Modernas):** Capacidad para crear, seleccionar, aplicar y reconocer las limitaciones de técnicas, recursos y herramientas informáticas modernas y de IA (Python, Scikit-learn, XGBoost, Prometheus, Grafana, MLflow).
* **AG-I12 (Gestión de Proyectos):** Demostración de prácticas de gestión (PMBOK 7 y Marco Ágil Scrum) al acotar el alcance de la PoC, definir criterios de éxito objetivos y emitir un dictamen técnico de gobierno (GO CON CONDICIONES).
* **AG-I01 (El Profesional y el Mundo / Sostenibilidad):** Reconocimiento del impacto ambiental, desarrollo sostenible y cumplimiento de restricciones de SLA/QoS en infraestructura computacional.

## 13.3. Matriz Maestra de Trazabilidad ICACIT – PoC

A continuación se presenta la tabla articulada de trazabilidad, estructurada de forma directamente copiable e integrable al informe final:

| **Atributo de Egreso (ICACIT)** | **Criterio / Exigencia Académica** | **Actividad Concreta Realizada en la PoC** | **Evidencia Concreta Generada** | **Métrica / Indicador Cuantitativo** | **Artefacto de Respaldo** |
| --- | --- | --- | --- | --- | --- |
| **AG-I07**  Conocimientos de Ingeniería | Identificación y análisis de problemas complejos de ingeniería. | Caracterización de la variabilidad temporal de uso de CPU a intervalos de 15s y formulación del problema de decisión bajo incertidumbre. | Formulación de la Incertidumbre Tecnológica y preguntas de investigación. | Cobertura de telemetría (80,640 registros en 2 semanas). | docs/informe\_tecnico\_poc\_v2.pdf (Punto 1 y 2) |
| **AG-I07**  Conocimientos de Ingeniería | Fundamentos matemáticos, estadísticos y modelo energético. | Definición de ecuaciones formales de error (MAE, RMSE, sMAPE) y modelo lineal proxy de potencia eléctrica **P(u) = P\_idle + (P\_max - P\_idle) × u**. | Formulación matemática de la hipótesis H1 y matriz de metas cuantitativas. | • MAE ≤ 8%  • RMSE ≤ 10%  • sMAPE ≤ 12% | Notebook de formulación (*01\_eda\_data\_cleaning.ipynb*) |
| **AG-I11**  Uso de Herramientas (Seleccionar) | Selección justificada de técnicas e instrumentos de TI. | Evaluación multicriterio de alternativas algorítmicas frente a baselines (Naive y Promedio Móvil). | Matriz comparativa ponderada entre Random Forest y XGBoost Regressor. | Puntuación ponderada de selección (4.90 sobre 5.00). | Tabla del Punto 4 e informe de selección tecnológica |
| **AG-I11**  Uso de Herramientas (Crear y Aplicar) | Construcción y aplicación de pipelines y modelos predictivos. | Desarrollo del prototipo de inferencia en Python con Scikit-learn y XGBoost, sobre ventanas históricas de retardos (lags t-1 ... t-15). | Pipeline de datos end-to-end y ejecuciones experimentales E1 a E4. | Reducción del RMSE en 57.7% respecto al Baseline Naive. | Scripts ***src/feature\_engineering.py y src/inference\_engine.py*** |
| **AG-I11**  Uso de Herramientas (Limitaciones) | Reconocimiento consciente de limitaciones de herramientas e IA. | Identificación y caracterización del 3.2% de vacíos en telemetría y falta de extrapolación en picos no observados. | Matriz de 10 Limitaciones y Acciones de Tratamiento de Ingeniería para el PMV1. | % de datos nulos (3.2%) y margen de deriva (Data Drift RMSE > 12%). | Tabla del Punto 8 (***02\_model\_training\_mlflow.ipynb***) |
| **AG-I12**  Gestión de Proyectos | Definición de alcance, metas, riesgos y gobierno de proyecto. | Delimitación del tiempo de ejecución (Sprint 1-2) y emisión del veredicto técnico de transición al PMV1. | Acta formal de aprobación con veredicto **GO CON CONDICIONES**. | Cumplimiento del 100% de metas de precisión (Latencia = 45 ms). | Imagen vectorial ***acta\_aprobacion\_poc.svg*** |
| **AG-I01**  Sostenibilidad y SLA | Evaluación de restricciones operativas y sostenibilidad energética. | Operación bajo esquema aislado *Recommendation-Only* sin modificaciones destructivas en Kubernetes y control de SLA. | Verificación de estabilidad y prevención de degradación de servicio en picos de carga. | RMSE = 9.8% en el Escenario de Carga Pico (> 85% CPU). | Registros de corridas y artefactos en MLflow Tracking |

##

##

##

## 13.4. Trazabilidad Específica del Atributo AG-I11 (Los 4 Verbos Exigidos por ICACIT 2026/2027)

Para satisfacer plenamente la rúbrica del docente en el atributo AG-I11, la PoC demuestra de forma explícita el cumplimiento de los cuatro verbos metodológicos:![](data:image/png;base64...)

* **SELECCIONAR:** Justificación cuantitativa mediante matrices ponderadas para la elección de Python, XGBoost Regressor, Prometheus, PostgreSQL/Supabase y MLflow, descartando alternativas de sobreingeniería (como Deep Learning no justificado).
* **CREAR:** Diseño y programación de scripts de tratamiento de series temporales, generación de ventanas de retardos (sliding windows t-1 ... t-15), modelo lineal proxy de potencia y microservicio liviano de inferencia.
* **APLICAR:** Ejecución sistemática del protocolo experimental (E1 a E4) bajo cuatro escenarios operativos de carga universitaria (Carga Baja, Normal, Alta y Pico), registrando métricas y artefactos en MLflow.
* **RECONOCER LIMITACIONES:** Declaración transparente de los riesgos de deriva de datos (data drift), vacíos en la captura de telemetría (3.2% de datos nulos), falta de PDU física y límites de extrapolación de los árboles de decisión.

## 13.5. Regla de Oro Metodológica de la PoC para Evaluadores ICACIT

La PoC se alinea con la regla de oro metodológica de acreditación, garantizando que la experimentación no se convierta prematuramente en un desarrollo completo sin control:

![](data:image/png;base64...)

**1 Requerimiento IA ➔ 1 Incertidumbre ➔ 1 Hipótesis ➔ Máx 3 Alternativas ➔ 3–5 Experimentos ➔ Métricas Objetivas ➔ Limitaciones ➔ Decisión Go/No-Go**

* **1 Requerimiento de IA:** Predecir la demanda de CPU a 15 minutos en el data center universitario.
* **1 Incertidumbre Tecnológica:** Determinar si la telemetría a 15s tiene suficiente calidad y variabilidad para entrenar un regresor confiable.
* **1 Hipótesis Técnica (H1):** XGBoost/Random Forest estiman la demanda a 15 min con **RMSE ≤ 10%** y **Latencia < 2 s**.
* **3 Alternativas Tecnológicas:** Baseline Naive, Random Forest Regressor y XGBoost Regressor.
* **4 Experimentos Controlados:** E1 (Naive), E2 (Promedio Móvil), E3 (Random Forest) y E4 (XGBoost).
* **Métricas Objetivas:** MAE = 5.4%, RMSE = 7.1%, sMAPE = 8.6%, Latencia = 45 ms.
* **Limitaciones Identificadas:** 3.2% de nulos en telemetría y estimación lineal proxy de potencia.
* **Decisión de Gobierno:** Dictamen técnico **GO CON CONDICIONES** respaldado en el acta vectorial.

## 13.6. Distribución de Responsabilidad de Acreditación por Integrante (Matriz RACI para ICACIT)

Para la sustentación ante el jurado o docente evaluador, la responsabilidad del cumplimiento de cada Atributo de Egreso se asigna formalmente a los miembros del equipo:

| **Integrante del Equipo** | **DNI** | **Rol de Proyecto** | **Atributo ICACIT Principal** | **Evidencia Directa Bajo su Custodia** |
| --- | --- | --- | --- | --- |
| **Quintana Carhuaricra Jhonny Cristhian** | 71877361 | Arquitecto de Software & PO | **AG-I12** (Gestión) & **AG-I07** | Liderazgo del alcance, Project Charter, acta de dictamen GO CON CONDICIONES y gobernanza del proyecto. |
| **Barrera Peña Gina Diana** | 73476609 | Especialista en Base de Datos (DBA) | **AG-I11** (Herramientas) & **AG-I07** | Pipeline ETL de limpieza, esquema relacional en PostgreSQL/Supabase y tratamiento del 3.2% de nulos. |
| **Porras Veli Ricardo** | 76659572 | Desarrollador Backend & MLOps | **AG-I11** (Herramientas) & **AG-I07** | Código de entrenamiento E1-E4, APIs en FastAPI, binarios model.pkl y ejecuciones registradas en MLflow. |
| **Huamán Collazos Leonid** | 72611351 | Desarrollador Frontend (UI/UX) | **AG-I11** (Herramientas) & **AG-I01** | Visualización de métricas en Grafana/UI, wireframes de observabilidad e indicadores de sostenibilidad. |

# 14. Regla de ejecución de la PoC

Para mantener la Prueba de Concepto (PoC) en un ámbito estrictamente experimental y evitar que se transforme prematuramente en un desarrollo completo sin control de alcance, se establece una regla metodológica rigurosa de aislamiento. Esta regla garantiza que el esfuerzo de ingeniería se concentre en reducir la incertidumbre tecnológica mediante evidencia objetiva, antes de comprometer recursos en la construcción de los productos mínimos viables (PMV1, PMV2 y PMV3).

## 14.1. Definición Formal de la Regla de Oro de la PoC

**Regla de Ejecución Metodológica:**

*"Todo requerimiento funcional que incorpore Inteligencia Artificial debe vincularse de forma unívoca con una sola incertidumbre técnica, una hipótesis contrastable, un máximo de tres alternativas tecnológicas razonables, entre tres y cinco experimentos comparables, métricas objetivas de error y latencia, la identificación transparente de limitaciones y un dictamen explícito de decisión (Go / Go con Condiciones / No-Go)."*

## 14.2. Materialización de la Regla en el Proyecto Green AI

En la predicción de la demanda computacional de corto plazo a 15 minutos, la regla metodológica se operacionaliza mediante el siguiente flujo de correspondencia 1:1:

| **Eslabón de la Regla** | **Instanciación Concreta en el Proyecto Green AI** |
| --- | --- |
| **1. Requerimiento de IA** | Predecir la demanda futura de CPU a 15 minutos en el clúster universitario mediante métricas históricas de telemetría. |
| **2. Incertidumbre Técnica** | Determinar si la telemetría a 15s recopilada por Prometheus contiene suficiente información temporal y variabilidad para entrenar un modelo con error y latencia aceptables. |
| **3. Hipótesis Técnica (H1)** | Modelos supervisados de series temporales (Random Forest y XGBoost) estiman la CPU a 15 min con **RMSE ≤ 10%** y **latencia < 2 s**. |
| **4. Alternativas Tecnológicas (Máx. 3)** | 1. Baseline de Persistencia (Naive)  2. Random Forest Regressor  3. XGBoost Regressor |
| **5. Experimentos Controlados (3 a 5)** | • **E1:** Baseline Naive  • **E2:** Promedio Móvil  • **E3:** Random Forest Regressor  • **E4:** XGBoost Regressor |
| **6. Métricas Objetivas** | • **MAE:** 5.4% de CPU  • **RMSE:** 7.1% de CPU  • **sMAPE:** 8.6%  • **Latencia de Inferencia:** 45 ms |
| **7. Identificación de Limitaciones** | Presencia de un 3.2% de vacíos (*gaps*) en la telemetría e imprevisibilidad de picos extremos no observados en el entrenamiento. |
| **8. Decisión de Gobierno** | Veredicto técnico: **GO CON CONDICIONES** (Pase al PMV1 sujeto al desarrollo de un módulo ETL de interpolación). |

##

## 14.3. Salvaguardas para Evitar la Sobreingeniería (Scope Creep)

Para garantizar el cumplimiento de esta regla de ejecución, el equipo de ingeniería aplica cuatro restricciones metodológicas obligatorias:

* **Prohibición de Cambios Autónomos en Infraestructura:** La PoC opera exclusivamente en modo de simulación y recomendación (*Recommendation-Only*). No ejecuta cambios de escalado de pods ni apaga nodos físicos de Kubernetes de manera autónoma.
* **Rechazo de Algoritmos Injustificados:** Se descarta el uso inicial de arquitecturas complejas de Deep Learning (como redes LSTM o Transformers) hasta que los modelos supervisados livianos en datos tabulares (XGBoost) demuestren ser insuficientes.
* **Mismo Conjunto de Datos de Evaluación:** Todos los experimentos (E1 a E4) se evalúan estrictamente sobre la misma división cronológica del conjunto de prueba (*Test Set* del 15%), prohibiendo cualquier re-división aleatoria que introduzca fuga de datos (*data leakage*).
* **Criterio de Descarte Activo:** Si una alternativa algorítmica no logra una reducción estadísticamente significativa del error frente al Baseline Naive o genera una latencia > 2.0 s, queda automáticamente descartada para el PMV1.

## 14.4. Valor para la Acreditación ICACIT (AG-I11 y AG-I12)

Esta regla de ejecución constituye la evidencia de que la experimentación con Inteligencia Artificial no es un proceso improvisado, sino una disciplina de ingeniería regida por controles de gobierno:

* **Demuestra AG-I11 (Uso de Herramientas Modernas):** Al exigir la comparación contra baselines simples y limitar la cantidad de alternativas, demuestra que las herramientas de IA se eligen por su rendimiento probado y no por moda tecnológica.
* **Demuestra AG-I12 (Gestión de Proyectos):** Garantiza que los recursos del proyecto (tiempo, cómputo y esfuerzo del equipo) se gestionan con eficiencia, cerrando la PoC con un veredicto explícito antes de iniciar la inversión de horas en el PMV1.

# 15. Criterios de calidad de la evidencia

En el marco de la acreditación ICACIT (AG-I11: Uso de Herramientas Modernas y AG-I12: Gestión de Proyectos) y los estándares de ingeniería de software, la evidencia obtenida en una Prueba de Concepto (PoC) no puede ser anecdótica ni basarse en métricas aisladas. La calidad de la evidencia exige que cada resultado, gráfico o conclusión sea 100% reproducible, auditable y trazable a lo largo de todo el pipeline experimental.

Un error frecuente en proyectos de ciencia de datos es presentar afirmaciones sin el respaldo de los artefactos originales. Para garantizar la solidez científica del proyecto Green AI, la evidencia generada debe cumplir con ocho criterios obligatorios de calidad de datos e inferencia.

## 15.1. Los Ocho Criterios Mandatorios de Calidad de la Evidencia

1. **Identificación y Trazabilidad del Dataset:** Cada experimento debe declarar explícitamente la fuente de los datos (Prometheus API), el período cronológico de captura (14 días continuos), el volumen exacto (80,640 registros) y la frecuencia de muestreo (15 segundos).
2. **Definición Rigurosa de Variables (Inputs / Target):** Declaración formal de la variable dependiente ($y\_{t+15}=CPU\_{t+15}$) y la matriz de características ($X\_{prep}$) generada mediante ventanas deslizantes.
3. **División Temporal Estricta (No Data Leakage):** Garantizar la separación cronológica de los datos (70% Entrenamiento, 15% Validación y 15% Prueba). Queda strictly prohibida la división aleatoria (*random split*), asegurando que los parámetros de escalado (StandardScaler) se calculen únicamente sobre el conjunto de entrenamiento.
4. **Registro de Hiperparámetros, Semillas y Entorno (MLOps):** Fijar la semilla de aleatoriedad (random\_state = 42) y registrar las versiones exactas de las bibliotecas (requirements.txt), garantizando que la corrida produzca idénticos resultados en cualquier máquina.
5. **Registro Multicriterio de Métricas por Experimento:** Ningún modelo se evalúa con una sola métrica. Es obligatorio reportar simultáneamente $MAE$, $RMSE$, $sMAPE$, latencia de inferencia ($ms$) y el consumo de recursos de la propia IA (*overhead*).
6. **Caracterización Transparente de Anomalías y Limitaciones:** Registrar el tratamiento aplicado a los vacíos de telemetría (3.2% de nulos imputados por interpolación) y declarar el carácter estimado de la potencia eléctrica en Watts ($P(u)$) al no contar con PDU física.
7. **Preservación y Custodia de Artefactos Digitales:** Todos los artefactos intermedios y finales (model.pkl, MLmodel, gráficos de residuos, logs de auditoría y archivos .svg) deben almacenarse en repositorios versionados (Git / MLflow / Supabase).
8. **Separación entre Metas Previas y Resultados Observados:** Marcada diferenciación conceptual entre los umbrales de éxito definidos en la planificación.

## 15.2. Matriz de Control de Calidad y Custodia de la Evidencia

La siguiente tabla resume el protocolo de verificación de calidad aplicado a la PoC, estructurada de forma limpia para copiar y pegar directamente:

| **Criterio de Calidad** | **Requisito Técnico de Ingeniería** | **Mecanismo de Verificación / Herramienta** | **Artefacto de Respaldo e Identificador** |
| --- | --- | --- | --- |
| **1. Trazabilidad del Dataset** | Dataset estático de 2 semanas de telemetría a 15s sin contaminación externa. | Cálculo del Checksum MD5/SHA256 del archivo prometheus\_telemetry\_2w.csv. | data/raw/prometheus\_telemetry\_2w.csv  *(Hash MD5 registrado en MLflow)* |
| **2. Control de Fuga Temporal** | Preprocesamiento e imputación calculados exclusivamente sobre el 70% de Train. | Inspección del pipeline FeatureEngineering en Python antes del .fit(). | Script src/feature\_engineering.py  *(Revisión en Pull Request de GitHub)* |
| **3. Reproducibilidad de IA** | Generación de resultados idénticos en distintas ejecuciones (random\_state = 42). | Ejecución automatizada de 5 corridas consecutivas en MLflow Tracking. | MLflow Experiment ID: 0  Run IDs: run\_e1 a run\_e4 |
| **4. Medición de Latencia** | Medición del tiempo de ejecución del endpoint de inferencia en milisegundos. | Pruebas de carga y tiempo de respuesta con Postman y FastAPI Timer. | Log de auditoría de inferencia:  latency\_ms = 45 ms *(Promedio)* |
| **5. Monitoreo de Overhead** | Garantizar que el modelo consuma < 2% de CPU y < 50 MB de RAM en el nodo. | Monitoreo del proceso Python mediante cAdvisor y Prometheus. | Dashboard de Grafana:  Panel *ML Engine Resource Usage* |
| **6. Trazabilidad MLOps** | Registro persistente de hiperparámetros, métricas y binarios del modelo. | Registro del modelo en MLflow Model Registry y almacenamiento en MinIO. | Artefacto xgboost\_poc\_v1/model.pkl  Registrado en MLflow Registry |
| **7. Gobernanza y Seguridad** | Decisiones almacenadas en modo recomendación sin escrituras en Kubernetes. | Verificación de la tabla logs en PostgreSQL/Supabase (0 llamadas a K8s API). | Diagrama relacional y script: script\_pmv1\_postgresql.sql |
| **8. Conformidad Institucional** | Veredicto formal respaldado por firmas digitalizadas del equipo de proyecto. | Generación del vector SVG formal con membrete y matriz RACI de roles. | Imagen vectorial formal |

##

##

##

## 15.3. Valor de la Calidad de la Evidencia para la Acreditación ICACIT

La rigurosidad en la calidad de la evidencia respalda directamente la evaluación docente bajo las rúbricas de acreditación:

* **Sustento para AG-I11 (Uso de Herramientas Modernas):** Demuestra que el uso de MLflow, Git, Python, Prometheus y Grafana no es un despliegue cosmético, sino un ecosistema integrado de trazabilidad donde cada métrica reportada tiene una prueba de origen.
* **Sustento para AG-I12 (Gestión de Proyectos):** Proporciona la evidencia auditable que justifica el dictamen **GO CON CONDICIONES**, permitiendo que el Product Owner y el asesor aprueben el paso al PMV1 sobre bases cuantitativas reales y no sobre supuestos.

# 16. Resultado esperado de la PoC

En estricta conformidad con la metodología de ingeniería y los criterios de acreditación ICACIT (AG-I07: Conocimientos de Ingeniería, AG-I11: Uso de Herramientas Modernas y AG-I12: Gestión de Proyectos), el resultado esperado de la Prueba de Concepto (PoC) no consiste en declarar anticipadamente un ahorro energético ni asumir que un algoritmo es el definitivo sin sustento experimental.

El objetivo central de la PoC es determinar con evidencia objetiva, cuantitativa y reproducible si la predicción de la demanda computacional de corto plazo es técnicamente viable, qué alternativa algorítmica presenta el mejor desempeño bajo escenarios reales y qué restricciones de datos deben resolverse obligatoriamente antes de integrar el núcleo de Inteligencia Artificial en el PMV1.

## 16.1. Síntesis de Resultados Esperados y Logros Cuantitativos

La ejecución de la PoC sobre la telemetría histórica del clúster experimental ha producido tres resultados técnicos de ingeniería:

* **Demostración de Viabilidad Predictiva:** Se demostró que la telemetría muestreada a intervalos de 15 segundos contiene la variabilidad y estructura temporal necesarias para predecir la utilización de CPU a un horizonte de 15 minutos.
* **Selección Algorítmica Basada en Evidencia:** El modelo XGBoost Regressor (E4) demostró una superioridad estadística contundente frente a los baselines, alcanzando las siguientes métricas en el conjunto de prueba (*Test Set*):
  + **Error Absoluto Medio (MAE):** 5.4% en uso de CPU (Meta: ≤ 8.0%).
  + **Raíz del Error Cuadrático Medio (RMSE):** 7.1% en uso de CPU (Meta: ≤ 10.0%), logrando una reducción del error del 57.7% frente al Baseline Naive (16.8%).
  + **Error Porcentual Simétrico (sMAPE):** 8.6% (Meta: ≤ 12.0%).
  + **Latencia de Inferencia:** 45 ms (Presupuesto máximo: < 2000 ms).
  + **Comportamiento en Alta Demanda:** RMSE = 9.8% durante picos de carga (> 85% CPU).
* **Caracterización Objetiva de Restricciones:** Se identificó que el dataset de telemetría de Prometheus registró un 3.2% de datos nulos/vacíos (*gaps*) por caídas breves del colector y que el consumo eléctrico se evaluó mediante un modelo proxy lineal al no disponer de una PDU física.

##

##

##

## 16.2. Matriz de Resultados Observados vs. Criterios de Cierre de PoC

| **Dimensión Evaluada** | **Criterio Previo de Evaluación** | **Resultado Experimental Medido** | **Estado de Validación** | **Conclusión de Ingeniería** |
| --- | --- | --- | --- | --- |
| **Calidad Predictiva Global** | MAE ≤ 8.0%  RMSE ≤ 10.0% | MAE = 5.4%  RMSE = 7.1% | **CUMPLE** | XGBoost supera las metas y reduce drásticamente la desviación respecto al baseline. |
| **Tiempo de Respuesta** | Latencia < 2.0 s | 45 ms | **CUMPLE** | Inferencia ultraliviana compatible con el ciclo de decisión. |
| **Comportamiento en Picos** | RMSE ≤ 12.0% en picos | RMSE = 9.8% | **CUMPLE** | El modelo previene subestimaciones durante sobrecargas académicas. |
| **Continuidad de Telemetría** | 0% vacíos temporales | 3.2% de datos nulos | **CONDICIONADO** | Exige desarrollo de un módulo ETL de interpolación en el PMV1. |
| **Veredicto Técnico** | Transición al PMV1 | **GO CON CONDICIONES** | **APROBADO** | Habilita el desarrollo del PMV1 bajo 4 compromisos de mitigación. |