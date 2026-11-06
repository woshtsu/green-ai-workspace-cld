# C2 · Conocimientos de ingeniería (AG-I07)

Base: `guias/TrabajosDesarrollados/2. Conocimiento de Ingenieria.md` (fundamentos matemáticos correctos y
extensos) y la guía `2.Conocimientos de Ingenieria.md` (11 secciones). **Corrección principal:** cada
conocimiento se enlaza con el **módulo real del repositorio** donde se aplica, y se retiran los resultados no
obtenidos (XGBoost como modelo final, RMSE 7,1 %).

## 1. Problema de ingeniería (de C1)
Predecir a corto plazo (horizonte de 15 min) la utilización de CPU por nodo a partir de series temporales
multivariables. Convertir la predicción en una recomendación segura que respete restricciones de servicio y
estimar la energía solo con datos de potencia válidos.

## 2. Requerimientos (RF-01..RF-20 del informe; los de IA en negrita)
| Necesidad | Requerimiento | Implementación actual |
|---|---|---|
| Observar recursos | RF-01..RF-04 | Simulator → Prometheus → Monitoring (`software/monitoring`) |
| Preparar series | **RF-05, RF-06** | `software/data-processing` (ETL, dataset de predicción) y `software/prediction/src/preprocessing` |
| Entrenar/evaluar | **RF-07** | `software/prediction/src/training`, `src/evaluation`, `scripts/run_pipeline.py` |
| Versionar modelos | RF-08 | Manifiesto con SHA del dataset y de la configuración (`results/manifest.json`). MLflow existe en `src/mlflow`, pero el pipeline se ejecuta con `--skip-mlflow`: **no evidenciado** |
| Servir predicción | **RF-09** | `POST /v1/predictions` (FastAPI) detrás del Gateway con JWT |
| Recomendar con seguridad | **RF-11, RF-12** | `src/recommendations/policy.py` + `POST /v1/recommendations` (`executionAllowed=false`) |
| Energía | RF-14 | `POST /v1/energy` (integración trapezoidal; CO₂e solo con factor y fuente) |
| Seguridad | RF-18, RF-19 | Gateway: JWT de Supabase (ES256/RS256) + RBAC ADMIN/OPERATOR |
| No funcionales | RNF-01..RNF-09 | Pruebas, contratos OpenAPI, Docker, timeouts, límites de tamaño |

## 3. Fundamentos matemáticos y estadísticos (y dónde se usan)
| Conocimiento | Aplicación concreta | Módulo |
|---|---|---|
| Serie temporal y regresión supervisada: ŷ(t+h) = f(x(t), x(t−1), …) | Objetivo: CPU a t+15 min (h = 3 pasos de 5 min) | `src/preprocessing`, `config/config.yaml` |
| Ingeniería de variables | Retardos (lags 1–3), media/desv./mín./máx. móviles, hora y día codificados con seno/coseno (variables cíclicas) | `results/metrics/selected_model_metrics.json` (lista de *features*) |
| División temporal sin mezcla | 70 / 15 / 15 en orden cronológico; sin *shuffle* para evitar fuga de información | `config/config.yaml` (split), `tests/unit/test_anti_leakage.py` |
| Métricas de error: MAE = (1/n)Σ\|y−ŷ\|; RMSE = √((1/n)Σ(y−ŷ)²); sMAPE = (100/n)Σ 2\|y−ŷ\|/(\|y\|+\|ŷ\|) | Selección de modelo y comparación con baselines; RMSE penaliza los errores en picos | `src/evaluation` |
| Estratificación por régimen de carga | Error por carga baja, normal y alta y en picos (umbrales por cuantiles) | `model_comparison.csv` (`high_demand_*`, `peak_*`) |
| Estadística descriptiva | Caracterización del dataset (media, p95, % del tiempo bajo o sobre umbrales) | `01-analisis-del-problema.md` §7 |
| Latencia de inferencia (p50/p95) | Criterio de la PoC: < 2 s | `model_comparison.csv` (`latency_*`) |

Precisión conceptual: las clases binarias (Precision, Recall, F1) del trabajo previo solo aplican si se define
una tarea de clasificación de «evento de alta demanda». El sistema actual hace **regresión**; F1 no se calcula.
No citar F1 = 0,89, que no tiene experimento.

## 4. Ciencias naturales
- **Potencia y energía:** E = ∫P dt ≈ Σ ½(Pᵢ + Pᵢ₊₁)Δt (regla del trapecio); 1 kWh = 3,6·10⁶ J. Implementado en
  `src/service/recommendations.py` (`energy`), que rechaza intervalos inválidos.
- **Emisiones:** CO₂e = E · FE. El factor debe venir con su fuente; si falta, no se calcula (evita una huella
  inventada). Referencia metodológica: ISO/IEC 21031:2024 (SCI) [9].
- **Termodinámica:** la energía eléctrica de un servidor se disipa como calor (refrigeración, PUE). Es contexto:
  no se mide en el proyecto.

## 5. Computación
Estructuras temporales (ventanas deslizantes), API REST/JSON con contratos OpenAPI, autenticación con JWT y
firma ECDSA/RSA, paginación por cursor *keyset* (timestamp, id), series en Prometheus (PromQL), contenedores.

## 6. Ingeniería de software
Arquitectura hexagonal por servicio (dominio sin dependencias de infraestructura), puertos y adaptadores (p. ej.
`HistoricalLogsSource` con adaptadores Supabase y SQLite), pruebas unitarias, de contrato e integración, gestión
de configuración por entorno, *fail-fast* en configuración inválida.

## 7. Conocimiento especializado del dominio
Observabilidad (Prometheus, *scraping*, *exporters*), gestión de capacidad, SLA/SLO, Green AI (el costo
computacional del propio modelo [Verdecchia 2023]).

## 8. Selección tecnológica ponderada (pesos: adecuación 30, ecosistema 25, integración 20, rendimiento 15, curva 10)
| Componente | Alternativas (puntaje 1–5 ponderado) | Elegida | Motivo |
|---|---|---|---|
| ML / predicción | Python 4,8 · Java 3,1 · Go 2,6 | Python (scikit-learn, XGBoost, pandas) | Ecosistema ML |
| Observabilidad | Prometheus 4,7 · InfluxDB 3,9 · Zabbix 3,4 | Prometheus | Modelo *pull*, PromQL, estándar de facto |
| Gateway | Spring Cloud Gateway 4,0 · Go stdlib 4,3 · Nginx 3,2 | Spring (vigente); Go validado como alternativa | D-06: Go equivalente con 16 MB frente a 520 MB |
| Persistencia | PostgreSQL/Supabase 4,6 · MySQL 3,8 · MongoDB 3,3 | Supabase (Auth + PostgreSQL); SQLite solo en desarrollo | D-05 |
Los puntajes son una propuesta del equipo para documentar el criterio; ajustarlos en consenso.

## 9. Integración de conocimientos
Matemáticas (series y error) + computación (API, JWT, contenedores) + ingeniería de software (hexagonal y
pruebas) + ciencias naturales (energía) → flujo: simulador → Prometheus → Monitoring → Data Processing →
Prediction (modelo + política + energía) → Gateway → Frontend.

## 10. Validación (evidencia del 2026-11-06, ver `08-`)
Pipeline reproducible (semilla 42): Random Forest con MAE 3,22 y RMSE 4,59 frente a persistencia 4,61 / 6,39
(validación, 15 min). Suites: Monitoring 112, Gateway 11 (+30 en Go), Data Processing 114 con PostgREST,
Prediction 96, Frontend 13, Simulator 10. Smoke del stack: 14/14.

## 11. Conclusión
Las decisiones técnicas se sustentan en conocimientos aplicados y verificables. El aporte de la IA está acotado
a datos simulados: mejora del error frente a los baselines y cumplimiento de la latencia. La relación con la
energía queda formulada y codificada (E = ∫P dt), pero su efecto real requiere medición (PMV3).
