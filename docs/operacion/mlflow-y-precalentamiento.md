# Operación: consulta de MLflow (F-04) y precalentamiento controlado de Render (P-01)

Sprint 7, ola 2 — 19/11/2026.

## F-04 · Consultar los experimentos de MLflow en local

MLflow **no** es una dependencia de la inferencia: Prediction carga el modelo empaquetado (`models/selected`) y responde aunque MLflow esté detenido. MLflow solo registra los entrenamientos.

1. Reentrenar y registrar (semilla 42):
   ```bash
   cd software/prediction
   .venv/Scripts/python scripts/run_pipeline.py
   ```
   `--skip-mlflow` omite el registro (lo usa la reejecución capturada en la Figura VIII.1.a del informe).
2. Abrir la interfaz sobre el almacén local `mlruns/`:
   ```bash
   cd software/prediction
   .venv/Scripts/python -m mlflow ui --backend-store-uri ./mlruns --host 127.0.0.1 --port 5000
   ```
   y navegar a http://127.0.0.1:5000 → experimento `computational-demand-prediction` → run `random_forest_15m` (evidencia: captura C303 del informe).
3. No se despliega un servidor MLflow en Render: consumiría memoria y cupo del plan gratuito. Si se requiere en el futuro, debe ir aparte y sin bloquear la inferencia.

## P-01 · Precalentamiento controlado antes de una demostración

Render Free duerme cada servicio tras 15 min sin tráfico. Medición real del 19/11/2026 17:45 (captura `entregables/semana13/evidencias/captura-P01-arranque-frio-render.png`, script `herramientas_IA/operacion/medir_arranque_frio.ps1`):

| Servicio | 1.ª petición (s) | 2.ª petición (s) |
|---|---|---|
| gateway | 12,99 | 0,36 |
| monitoring | 69,50 | 0,37 |
| prediction | 46,57 | 0,78 |
| data-processing | 17,94 | 0,37 |
| simulator | 12,94 | 0,78 |
| prometheus | 12,62 | 0,47 |

Política (según el plan FURPS+ P-01):
- **No** se usa un ping permanente: consumiría las 750 h/mes compartidas del workspace y ocultaría la limitación real.
- Antes de una demo o sustentación, ~25 min antes: `python herramientas_IA/video/mantener_despierto.py --minutos 120` (solo GET a rutas de salud, se detiene solo).
- Para medir de nuevo el arranque en frío: `powershell -File herramientas_IA/operacion/medir_arranque_frio.ps1` tras ≥ 15 min sin tráfico.
- El cold start (12–70 s) queda documentado como limitación del hosting gratuito; con el servicio despierto la respuesta es < 1 s.
