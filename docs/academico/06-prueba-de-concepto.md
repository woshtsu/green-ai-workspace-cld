# C6-A · Prueba de concepto (PoC) de IA

Base: `docs/historico/trabajos-desarrollados/Guia_6_Prueba_de_Concepto_Completa_Revisada.md` y la guía `6.Prueba de Concepto.md`.
**Corrección crítica.** La tabla de resultados del trabajo previo (§7.1) no proviene de ningún experimento
encontrado en el repositorio:
- MAE: Naive 12,4 % · MA 10,1 % · RF 6,2 % · **XGBoost 5,4 %**.
- RMSE **7,1 %** y picos **9,8 %**.
- Latencia **45 ms**, RAM < **35 MB** y varianza **0,2 %** «en MLflow».

Esas cifras se copiaron al informe entregado y explican el 0 en la discusión (ind. 6). Se sustituyen por la
ejecución **reproducible** del pipeline del repositorio.

## 1. Identificación
| Elemento | Definición |
|---|---|
| Requerimiento con IA | RF-09 / HU-03: predecir la utilización de CPU por nodo a 15 min |
| Incertidumbre | ¿Un modelo de ML mejora a referencias triviales (persistencia y media móvil) en el mismo split temporal, con latencia aceptable? |
| Hipótesis H1 | Un modelo de árboles (Random Forest o XGBoost) obtiene un **MAE menor que el baseline de persistencia** a 15 min en validación, con **latencia p95 < 2 s** |
| Criterios de éxito | MAE(ML) < MAE(persistencia) y < MAE(media móvil); RMSE en picos menor que el baseline; latencia p95 < 2 000 ms |
| Datos | `dataset-sim-001` (telemetría **simulada**, cadencia de 5 min; `software/prediction/data/raw/sample_dataset.json`); SHA-256 en `results/manifest.json` |
| Alternativas (≤ 3 de ML + baselines) | Persistencia, media móvil, Random Forest Regressor, XGBoost Regressor |
| Horizontes | 5, 15 y 30 min |
Se retiró el umbral «RMSE ≤ 10 %» del trabajo previo: la métrica está en **puntos porcentuales de CPU**, no en
porcentaje relativo. Mezclar ambas cosas fue el origen de la confusión.

## 2. Método
Variables: CPU actual, retardos 1–3, estadísticos móviles (media, desv., mín., máx.), hora, minuto y día
codificados con seno/coseno. División cronológica 70/15/15 sin *shuffle* (`config/config.yaml`), prueba de
anti-fuga (`tests/unit/test_anti_leakage.py`) y semilla 42. El modelo se selecciona por el error de
**validación**; el test se reporta una sola vez.
Reproducir:
```powershell
cd software\prediction
$env:MPLBACKEND='Agg'; .venv\Scripts\python.exe scripts\run_pipeline.py --skip-mlflow
```
Resultados en `results/metrics/model_comparison.csv`, `results/reports/model_report.md` y
`results/manifest.json`. La ejecución del 2026-11-06 coincide con el manifiesto versionado (determinista).

## 3. Resultados (validación, horizonte de 15 min, n = 125; unidades: puntos de CPU)
| Modelo | MAE | RMSE | sMAPE (%) | MAE en alta demanda (n=32) | MAE en picos (n=13) | Latencia media (ms) |
|---|---|---|---|---|---|---|
| Persistencia (baseline) | 4,61 | 6,39 | 11,16 | 5,43 | 8,99 | 0,09 |
| Media móvil (baseline) | 3,74 | 5,19 | 9,17 | 4,44 | 7,25 | 4,71 |
| **Random Forest (seleccionado)** | **3,22** | **4,59** | **7,85** | **3,58** | **6,12** | 26,6 |
| XGBoost | 3,46 | 4,79 | 8,46 | 3,86 | 6,21 | 18,7 |
**Test** del modelo seleccionado (n = 129): MAE 3,85 · RMSE 5,45 · sMAPE 7,67 · MAE en picos 8,45.
Latencias de una sola ejecución en el equipo de desarrollo; son por lote del split, no por petición HTTP.

## 4. Validación de H1
| Criterio | Meta | Resultado | Cumple |
|---|---|---|---|
| MAE frente a persistencia | menor | 3,22 frente a 4,61 (−30 %) | Sí |
| MAE frente a media móvil | menor | 3,22 frente a 3,74 (−14 %) | Sí |
| MAE en picos frente a persistencia | menor | 6,12 frente a 8,99 | Sí |
| Latencia | p95 < 2 000 ms | decenas de ms | Sí |
| Generalización a datos reales | probada | **No probada** (datos simulados) | No |

## 5. Limitaciones
1. **Datos simulados y pocos:** unas 125 muestras de validación. Con datos de la UC el error puede cambiar.
2. **En picos el error se duplica** (MAE 6,1 frente a 3,2 global, y 8,45 en test): riesgo de subestimar la
   demanda en matrícula y exámenes.
3. **Los árboles no extrapolan** por encima del máximo visto en entrenamiento.
4. **XGBoost no superó a Random Forest** a 15 min (sí a 30 min: 3,41 frente a 3,41, prácticamente un empate).
   «XGBoost como modelo final» es **falso**.
5. **MLflow** no se ejecutó (`--skip-mlflow`); la trazabilidad se apoya en el manifiesto con SHA del dataset y
   de la configuración.
6. Error en el archivo `results/metrics/selected_model_metrics.json`: dice `"split": "validation"` pero
   contiene las métricas de test. Corregir en el código antes de citarlo.

## 6. Decisión: **GO CON CONDICIONES**
El ML supera a los baselines con latencia holgada, así que se integra en el PMV2 (hecho: `/v1/predictions`).
Condiciones para el PMV3:
- Validar con datos reales o con trazas públicas (p. ej. Bitbrains, usadas por [1]–[3]).
- Reportar el error en picos.
- Mantener la persistencia como respaldo.
- Activar el registro de experimentos.

## 7. Trazabilidad ICACIT
Análisis (incertidumbre) → conocimiento (selección de modelos por error de validación) → herramientas (Python,
scikit-learn, XGBoost) → experimentación (4 alternativas × 3 horizontes) → limitaciones (§5) → decisión (§6).
