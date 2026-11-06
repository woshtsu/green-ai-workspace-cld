# Decisiones de arquitectura y migración

Formato breve: contexto → decisión → consecuencias. Estado: **Aceptada**, **Propuesta** (pendiente de validar) o **Pendiente**.

## D-01 Monorepo dentro del workspace, Git propio — Aceptada (2026-11-06)
- El usuario quiere abandonar los Git anidados sin perder la entrega vigente.
- `green-ai-monorepo/` con `git init` propio; el padre lo excluye en `.git/info/exclude` (local, sin commit) y en `.graphifyignore`. Worktrees de agentes en `../green-ai-monorepo-wt-*/`, también excluidos.
- Copia con `herramientas_IA/migracion/copiar_fuentes.py` (archivos versionados o no ignorados de cada repo; incluye cambios locales). SHA de origen en `docs/migracion/manifiesto-copia.json`.

## D-02 Exclusiones de la copia — Aceptada
- No se copian: `.git`, `.env`, `node_modules`, `.m2`, `target`, binarios (`*.exe`, `*.jar`), `runs/`, PDF/DOCX, ni los originales docentes de 2,7 MB y 1,5 MB que estaban duplicados dentro de Prediction.
- `datasets/processed/dataset_green_ai_v2_hexagonal.csv` (11 MB) no se copia: es salida regenerable de `scripts/run_greenai_etl.py`.
- `BD_GreenAi.xlsx` (7,3 MB) **sí** se versiona una vez: es la entrada original, y las pruebas del ETL lo necesitan.
- El modelo de Prediction no se versiona: lo genera `scripts/run_pipeline.py --skip-mlflow` (lo hace el Dockerfile; en local, antes de `pytest`).

## D-03 GreenAi_TPI no se migra como servicio — Aceptada
- Contiene un frontend alternativo, un backend Node con `node_modules` versionado (1192 archivos), un mock de monitoring, un exporter, manifiestos K8s y `kubectl.exe` (50 MB).
- **Riesgo detectado:** `Backend/.env` está versionado en el repositorio remoto LeonidKisley/GreenAi_TPI (contiene `SUPABASE_URL` y una clave de tipo *publishable*, no *secret*). No se copió. Rotarla o retirarla del historial es decisión del usuario/propietario.
- Los manifiestos K8s se revisarán al definir el despliegue (D-07). Hasta entonces quedan en el workspace antiguo.

## D-04 Compose del monorepo aislado — Aceptada
- Proyecto `green-ai-mono` y puertos 18000/18080/18081/19090/13001 (Swagger 18002/18003, Grafana 13002) configurables por `MONO_*`. Validado con `docker compose config`; **no arrancado todavía**.

## D-05 SQLite para desarrollo — Propuesta
- Requisito: persistencia ligera en desarrollo sin reemplazar Supabase/PostgreSQL.
- Restricción docente (lista de cotejo, criterio 11): "uso de procedimientos almacenados". SQLite no tiene procedimientos, RLS ni Auth; esa evidencia **solo** puede venir de Supabase/PostgreSQL.
- Propuesta: puerto de persistencia por servicio que realmente persista (pendiente inventario: Prediction/recomendaciones, Data Processing); adaptador SQLite (dev) y PostgreSQL (test/prod) con el mismo esquema en lo posible; pruebas de contrato comunes a ambos; integración contra un Supabase de pruebas antes de promover a `main`. Monitoring y Gateway sin BD.
- Autenticación local: pendiente de diseño. Cualquier emisor JWT de desarrollo será explícito, activado solo por perfil `dev` y rechazado en producción por configuración probada. No se desactiva la validación JWT del Gateway.

## D-06 Go — Pendiente
- Candidatos naturales por tamaño y forma: Gateway (proxy + JWT + CORS) y Monitoring (cliente de Prometheus). Simulator también es pequeño.
- Prediction (scikit-learn/XGBoost/pandas) permanece en Python salvo que se demuestre inferencia equivalente.
- Antes de reescribir: contrastar HU, contratos OpenAPI y pruebas actuales (Gateway 11, Monitoring 112), y medir memoria/arranque real. Go no elimina límites de hosting ni demuestra ahorro energético.

## D-07 Hosting a costo cero — Pendiente
- No se ha investigado todavía en esta sesión. Requiere comparar Render gratuito con alternativas vigentes (documentación oficial fechada) sobre suspensión, arranque en frío, RAM/CPU, cuotas, Docker, red interna, almacenamiento, tarjeta requerida y riesgo de cobro, incluida la viabilidad de Prometheus continuo e inferencia ML.
- El frontend es estático (HTML/JS + nginx), compatible en principio con GitHub Pages; falta base path, URL HTTPS del Gateway, CORS y redirects de Supabase Auth.
