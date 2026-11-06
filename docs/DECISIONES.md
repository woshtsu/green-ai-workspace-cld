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

## D-05 SQLite para desarrollo — Aceptada e implementada (2026-11-06)
- Requisito: persistencia ligera en desarrollo sin reemplazar Supabase/PostgreSQL.
- Restricción docente (lista de cotejo, criterio 11): "uso de procedimientos almacenados". SQLite no tiene procedimientos, RLS ni Auth; esa evidencia **solo** puede venir de Supabase/PostgreSQL.
- **Inventario de persistencia real** (Graphify + lectura): el único acceso a BD del backend es la lectura de
  históricos de `public.logs` en Data Processing (puerto `HistoricalLogsSource`, adaptador PostgREST de Supabase,
  solo lectura). Prediction no persiste (modelo como artefacto de archivo). Monitoring y Gateway sin BD (se mantienen
  así). El frontend usa Supabase Auth y las tablas `user_profiles`/`user_roles` con RLS y trigger
  (`supabase-auth-setup.sql`): eso no tiene equivalente SQLite y no se simula.
- **Implementación (Data Processing):**
  - `SqliteHistoricalLogsAdapter` (solo lectura, `mode=ro`), mismo puerto y mismas reglas: rango inclusivo,
    orden `(timestamp, log_id)`, cursor keyset, solo 7 columnas.
  - Esquema `infrastructure/persistence/sqlite/schema.sql` equivalente a `hardware`/`logs`, con divergencias
    documentadas en el propio archivo: sin `usuario`, timestamps TEXT UTC canónicos forzados por CHECK y REAL
    en lugar de numeric.
  - Semilla `scripts/seed_sqlite.py` con Hardware y Logs de `BD_GreenAi.xlsx` (sintéticos; **nunca** la hoja
    Usuarios). Tarda unos 13 s y ocupa 26 MB.
  - Selección por entorno: `HISTORICAL_SOURCE=none|supabase|sqlite`, compatible con `SUPABASE_ENABLED`.
    `sqlite` exige `APP_ENV=development|test`, y `APP_ENV` vale `production` por defecto.
  - **Contrato ampliado:** cada registro declara `source: "supabase" | "sqlite"` (antes fijo en `"supabase"`,
    lo que con SQLite habría mentido sobre la procedencia). Se regeneró el OpenAPI; el Gateway lo reenvía sin
    esquema y el frontend no lo consume.
- **Pruebas de contrato comunes** (`tests/test_historical_logs_contract.py`): la misma batería contra SQLite
  (siempre) y contra PostgreSQL 17 + PostgREST v13 reales (`compose.contract-postgres.yml`, secretos aleatorios
  por ejecución). Este segundo backend prueba la consulta del adaptador Supabase **sin modificarla**. También
  comprueba que la identidad de lectura no puede escribir. Limitación: no es Supabase (sin su Auth, RLS ni red)
  y **no** sustituye una prueba contra un proyecto Supabase de pruebas antes de promover a `main`.
- **Autenticación local:** no se añadió ningún proveedor JWT de desarrollo. El Gateway sigue validando JWT de
  Supabase en todos los perfiles. Para probar con usuario, usar el proyecto Supabase (idealmente uno de pruebas),
  añadiendo `http://127.0.0.1:13001` a sus redirects. Los servicios internos se pueden probar sin JWT por sus
  puertos loopback (18002/18003), que no se publican. Si en el futuro se añade un emisor de desarrollo, deberá
  activarse solo con `APP_ENV=development` y tener una prueba que demuestre su rechazo en `production`.

## D-06 Go — Pendiente
- Candidatos naturales por tamaño y forma: Gateway (proxy + JWT + CORS) y Monitoring (cliente de Prometheus). Simulator también es pequeño.
- Prediction (scikit-learn/XGBoost/pandas) permanece en Python salvo que se demuestre inferencia equivalente.
- Antes de reescribir: contrastar HU, contratos OpenAPI y pruebas actuales (Gateway 11, Monitoring 112), y medir memoria/arranque real. Go no elimina límites de hosting ni demuestra ahorro energético.

## D-07 Hosting a costo cero — Pendiente
- No se ha investigado todavía en esta sesión. Requiere comparar Render gratuito con alternativas vigentes (documentación oficial fechada) sobre suspensión, arranque en frío, RAM/CPU, cuotas, Docker, red interna, almacenamiento, tarjeta requerida y riesgo de cobro, incluida la viabilidad de Prometheus continuo e inferencia ML.
- El frontend es estático (HTML/JS + nginx), compatible en principio con GitHub Pages; falta base path, URL HTTPS del Gateway, CORS y redirects de Supabase Auth.
