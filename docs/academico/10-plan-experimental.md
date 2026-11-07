# Plan experimental del PMV3 y ejecución del baseline (Sprint 7, HU-16)

## 1. Pregunta (PE3) e hipótesis
¿El aprovisionamiento **predictivo** (Green AI) reduce el riesgo de SLA o la capacidad reservada frente al
aprovisionamiento **reactivo** (baseline) en condiciones equivalentes?
- **H0:** no hay diferencia en el riesgo de SLA ni en la energía modelada.
- **H1:** con el mismo margen de seguridad, Green AI reduce el riesgo de SLA; o, con el mismo riesgo, reserva
  menos capacidad.

## 2. Diseño (condiciones equivalentes)
| Elemento | Definición |
|---|---|
| Datos | Split de **test** del pipeline (`results/predictions/test_predictions.csv`, 129 puntos cada 5 min, `dataset-sim-001`, **simulado**) |
| Baseline (reactivo) | Reserva para t+15 min la CPU observada en t, más un margen h |
| Tratamiento (Green AI) | Reserva para t+15 min la CPU **predicha** por el modelo seleccionado (Random Forest), más el mismo margen h |
| Variables | Riesgo de SLA = % de intervalos con CPU real > capacidad reservada; capacidad ociosa media (pp); energía **modelada** |
| Modelo de potencia | P = P_idle + (P_max − P_idle)·reservado/100, con P_max = 600 W (HW001) y P_idle = 50 % del pico; supuesto declarado, no medido |
| Factores | Margen h ∈ {10 %, 20 %, 30 %} |
| Reproducir | `cd software/prediction; .venv\Scripts\python.exe scripts\run_experiment.py --headroom 0.2` |
| Pruebas | `tests/unit/test_experiment.py` (4 casos) |

## 3. Resultados (2026-11-06; n = 126 intervalos evaluables)
| Margen | Riesgo SLA baseline | Riesgo SLA Green AI | Δ | Capacidad ociosa B / G (pp) | Energía modelada B / G (Wh) |
|---|---|---|---|---|---|
| 10 % | 15,9 % | **9,5 %** | **−6,3 pp** | 6,31 / 5,88 | 4 896 / 4 888 (−0,2 %) |
| 20 % | 4,0 % | 4,0 % | 0 | 10,89 / 10,60 | 5 055 / 5 046 (−0,2 %) |
| 30 % | 2,4 % | 2,4 % | 0 | 15,72 / 15,46 | 5 211 / 5 204 (−0,1 %) |
Evidencia: `docs/evidencias/experimento-baseline-vs-green-ai-20261106.json` (margen 20 %).

## 4. Interpretación honesta
- Con márgenes ajustados (10 %), la predicción **reduce a la mitad aproximadamente** el riesgo de
  subaprovisionamiento: se acepta H1 para el SLA, con datos simulados.
- La diferencia de energía modelada es **despreciable** (≤ 0,2 %): no hay evidencia de ahorro energético. El
  beneficio potencial está en **operar con menos margen al mismo riesgo** (p. ej., Green AI con 10 % tiene 9,5 %
  de riesgo; el baseline necesita algo más del 10 % para igualarlo). Esto debe cuantificarse con un barrido fino
  del margen.
- Validez externa baja: un nodo, datos simulados, 126 intervalos. La energía es un modelo, no una medición.

## 5. Pendiente para el Sprint 8
1. Barrido de márgenes (5–30 %) y curva riesgo frente a capacidad («iso-SLA»).
2. Repetir con más nodos o trazas públicas (Bitbrains).
3. Intervalos de confianza por *bootstrap*.
4. Si la UC da medición de potencia, sustituir el modelo lineal.
