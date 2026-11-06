# Pruebas, resultados y discusión (PMV1 y PMV2)

Responde a los indicadores 5, 6, 9, 10 y 11 de la lista de cotejo y a la observación «incluir resultados de
pruebas del PMV1 y PMV2 y resaltar los resultados con la IA». Todas las cifras salen de ejecuciones del
2026-11-06 en el monorepo (`docs/HANDOFF.md`); los datos son **simulados**.

## 1. Pruebas automatizadas por servicio
| Servicio | Suite | Resultado | Tipo |
|---|---|---|---|
| Monitoring | Maven/JUnit | 112/112 | Unitarias, contrato HTTP, integración con Prometheus |
| Gateway (Java) | Maven/JUnit | 11/11 | JWT, RBAC, CORS, reenvío |
| Gateway (Go) | `go test -race` ×5 | 30/30 | Lo anterior más casos inválidos de JWT, límites y JWKS |
| Data Processing | pytest | 114/114 con PostgREST de pruebas (106 + 8 omitidas sin él) | Unitarias, contrato SQLite/PostgreSQL, API |
| Prediction | pytest (tras el pipeline) | 96/96 | Unitarias, anti-fuga, contrato, API |
| Frontend | `node --test` | 13/13 | Lógica de la UI |
| Simulator | unittest en Docker | 10/10 | Ciclo de vida, inventario, regresiones |
| Stack | `software/infraestructura/smoke/smoke.py` | 14/14 | Extremo a extremo vía HTTP |

## 2. Matriz por historia de usuario (criterio → prueba → resultado)
| HU | PMV | Criterio (Given/When/Then, resumido) | Prueba / evidencia | Resultado |
|---|---|---|---|---|
| HU-01 Visualizar métricas | 1 | Dado un usuario OPERATOR, cuando consulta la CPU actual, entonces recibe series por nodo con `origin=simulated` | Smoke «monitoring CPU actual» (200, 50 nodos); `MetricsHttpContractTest` | Aprobado |
| HU-01 (seguridad) | 1 | Dado un usuario sin token, cuando consulta, entonces recibe 401 | Smoke y Gateway (Java 11, Go 30) | Aprobado |
| HU-02 Históricos | 1 | Dado un rango ≤ 31 días, cuando pide históricos, entonces obtiene registros ordenados y paginados sin duplicados | `test_historical_logs_contract.py` (SQLite y PostgreSQL/PostgREST, 15 casos) | Aprobado |
| HU-15 Registro | 1 | Dado un correo válido, cuando se registra, entonces se crea un perfil con rol OPERATOR (trigger) | `supabase-auth-setup.sql`; **sin prueba con usuario real en el monorepo** | Pendiente de evidencia |
| HU-03 Predicción | 2 | Dada una ventana válida reciente, cuando solicita predecir a 15 min, entonces obtiene un valor con `origin=estimated` | Smoke «predicción con fixture simulado» (200); 96 pruebas | Aprobado |
| HU-03 (inválido) | 2 | Dado un dataset vacío o un esquema inválido, cuando predice, entonces recibe 400/422 sin inferir | `tests/api/test_health_and_predict.py` | Aprobado |
| HU-04 Comparar alternativas | 2 | Dados los mismos datos y split, cuando se entrenan, entonces se reportan métricas comparables | `results/metrics/model_comparison.csv` (4 modelos × 3 horizontes) | Aprobado |
| HU-05 Registro en MLflow | 2 | — | MLflow no ejecutado | **No cumplido** (sustituido por el manifiesto) |
| HU-06/HU-08 Recomendación con restricciones | 2 | Dada una predicción y telemetría frescas, cuando se pide recomendación, entonces se evalúan los umbrales y se devuelve una acción con `executionAllowed=false` | Smoke «recomendación con telemetría simulada» (200, `eligible_for_review`); 13 pruebas de recomendación | Aprobado (umbrales de demostración, configurables por `DEMO_POLICY_JSON`) |
| HU-07 Aprobación humana | 2 | Dada una recomendación, cuando el administrador la aprueba, entonces se registra | No existe flujo de aprobación; solo bloqueo de ejecución | **Parcial** |
| HU-09 Energía | 2 | Dadas muestras de potencia, cuando se calcula la energía, entonces se obtiene kWh por trapecio; sin factor no hay CO₂e | `/v1/energy`; prueba del frontend «energy displays absence of carbon factor» | Aprobado (estimación; no medición) |
| HU-11 Dashboard | 2 | — | `software/frontend/dashboard.html`; Grafana opcional | Funcional (falta captura con datos) |
| HU-12 Alertas | 2 | — | `prometheus/alerts.yml` (solo disponibilidad de Prediction) | Parcial |
| HU-14 Roles | 3 | Dado un token con un rol desconocido, cuando accede, entonces recibe 403 | Gateway (rol ROOT → 403) | Aprobado (ADMIN/OPERATOR; sin «observador») |

## 3. Resultado de la IA por PMV (para resaltar, como pidió el docente)
- **PMV1:** sin IA, por diseño. La observabilidad provee la serie que la IA necesita. 50 nodos simulados a 5 s.
- **PMV2:** Random Forest a 15 min con MAE 3,22 y RMSE 4,59 puntos de CPU (validación). Mejora del 30 % sobre la
  persistencia y del 14 % sobre la media móvil. Test: MAE 3,85. Latencia: decenas de ms. En picos el error sube
  a 6,1–8,4: es la principal limitación.

## 4. Discusión con antecedentes (ind. 6)
Tabla completa con Khan 2022 [1], Ji 2021 [2] y Sharma 2020 [3] en `09-antecedentes-y-referencias.md` §3.
Conclusión: coincidimos en la **tendencia**, porque el ML supera a las referencias simples, pero **no en
magnitud**: los datos (simulados frente a trazas reales), los modelos (árboles frente a RNN) y las métricas
(MAE en pp frente a RMSE por variable) son distintos. Los ahorros energéticos de [3]–[5] son simulados y el rango
de la literatura es 13–115 % [6], por eso Green AI no reclama ahorro hasta medirlo en el PMV3.
Regla: comparar **método, datos y orden de magnitud**, nunca afirmar «superamos a X» con datos distintos.

## 5. Video y transacciones (ind. 9 y 10)
El video aún no existe. Guion mínimo (≤ 20 min):
1. Login.
2. Monitoreo de 50 nodos.
3. Lote de ≥ 500 transacciones: llamadas a predicción y recomendación (se pueden generar con un script
   contra staging).
4. Caso de uso de IA 1: predicción de demanda.
5. Caso de uso de IA 2: recomendación con su política y advertencias.
6. Arquitectura y código por capas en GitHub.
El Lab. 11 exige **entorno en la nube** (no localhost), lo que depende de D-07.
