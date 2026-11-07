# Cómo mejorar la precisión del modelo de predicción de CPU (propuesta, 2026-11-07)

**Estado: investigación y plan. No se implementó ni se midió ninguna mejora.** Cualquier cifra futura debe salir de un experimento reproducible (ver `docs/HANDOFF.md`, «Honestidad experimental»).

## Punto de partida (verificado en el repo)
- Modelo servido: Random Forest, horizonte 15 min, remuestreo a 5 min, ventana de 2 h (`software/prediction`, `models/selected/metadata.json`).
- Entrenado con un **fixture sintético** y evaluado con MAE ≈ 3,2–3,9 pp en validación (el valor depende del run; ver `reports/` y MLflow local). No hay evidencia de precisión con telemetría real.
- Limitación operativa observada en la nube: necesita ~20 min de historial (6 intervalos de 5 min consecutivos); con menos devuelve «datos insuficientes».
- El escenario «high» del simulador deja todos los nodos ≈ 85 %, lo que hace trivial predecir «se mantiene»: **un modelo puede parecer bueno solo por no moverse**. La métrica correcta es la mejora frente a la persistencia (predecir el último valor), no el MAE absoluto.

## Qué dice la literatura consultada (búsqueda del 2026-11-07, fuentes secundarias)
- Comparativas de carga en VM/nube: LSTM tiende a ser el más preciso en secuencias, pero con más costo de entrenamiento; Random Forest y gradient boosting son una línea base competitiva y barata ([Experimental Analysis of Random Forest and LSTM Models for Optimizing CPU Efficiency in Cloud Computing](https://wjps.uowasit.edu.iq/index.php/wjps/article/view/893); [estudio en Research Square](https://www.researchsquare.com/article/rs-3419624/v1), preprint). Las cifras de estos trabajos no son comparables entre sí ni con las nuestras (datasets y métricas distintos) y no aíslan el efecto de cada técnica: no las usamos como objetivo.
- Intervalos de predicción para series: la predicción conforme necesita adaptarse porque las series no son intercambiables; se recomienda calibrar con validación de origen móvil y dejar un hueco (*gap*) entre entrenamiento y calibración ([conformalForecast](https://cran.r-project.org/web/packages/conformalForecast/refman/conformalForecast.html); [Xu et al., arXiv 2309.07435](https://arxiv.org/abs/2309.07435); [Nixtla StatsForecast](https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/conformalprediction.html)).

## Plan propuesto (en orden de costo/beneficio)
1. **Evaluación honesta primero.** Validación *walk-forward* (origen móvil, con *gap*) y métrica «skill» = 1 − MAE_modelo / MAE_persistencia, por escenario del simulador (normal, high y al menos uno con picos). Sin esto, ninguna mejora es demostrable. Datos: generar corridas más largas y variadas con el Simulator (semillas distintas), separando entrenamiento/validación por corrida, no por filas mezcladas.
2. **Más señal en las variables.** Además de los lags actuales: medias y desviaciones móviles (15/30/60 min), tendencia (diferencia y pendiente), hora del día en forma cíclica, y valores de memoria/red del mismo nodo. Predecir el **cambio** respecto del último valor (delta) en vez del nivel absoluto.
3. **Modelos candidatos con el mismo protocolo:** `HistGradientBoostingRegressor` (ya en scikit-learn: no añade dependencias pesadas), XGBoost (ya existe en el código; importación diferida), y Random Forest actual como referencia. Un LSTM solo si los anteriores no superan la persistencia con margen, por su costo y por el límite de 512 MB del hosting.
4. **Hiperparámetros** con búsqueda acotada dentro del *walk-forward* (no sobre el conjunto de prueba).
5. **Incertidumbre:** intervalos con predicción conforme sobre errores de validación (p. ej. MAPIE con `TimeSeriesSplit(gap=…)`); mostrar «15 min: 62 % (rango 55–70 %)» en vez de un solo número. Es más útil para decidir que bajar el MAE unas décimas.
6. **Reducir el historial mínimo** (hoy ~20 min): evaluar si 3–4 intervalos bastan sin perder skill; si sí, mejora la demo en la nube tras un arranque en frío.
7. **Registro:** cada experimento en MLflow (`software/prediction/mlruns/`, ya soportado con `run_pipeline.py` sin `--skip-mlflow`) y resultados en `docs/evidencias/`.

## Criterio de aceptación sugerido
Una mejora se declara solo si, en validación *walk-forward* sobre ≥ 3 corridas/escenarios no vistos, el modelo nuevo reduce el MAE frente a la persistencia y frente al Random Forest actual con intervalo de confianza que no incluya cero, y las 100 pruebas de Prediction y el smoke siguen en verde. Reportar también el costo (RAM/latencia en imagen de 512 MB).
