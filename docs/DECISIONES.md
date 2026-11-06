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

## D-06 Go — Gateway: prototipo validado, **sin reemplazar** (2026-11-06); Monitoring: pendiente
**Problema.** El Gateway Java ocupa 220–300 MiB de RAM, tarda 6–8 s en arrancar y su imagen pesa 520 MB. En los
planes gratuitos típicos (unos 512 MB por servicio, con suspensión y arranque en frío) eso pesa en D-07. La consigna
no exige ningún lenguaje.

**Opciones.**
1. Mantener Java.
2. Ajustar la JVM (heap, CDS o nativo con GraalVM): no medido.
3. Reescribir en Go con la biblioteca estándar.

**Arquitectura del prototipo (`software/gateway-go`).**
- `policy` (dominio): tabla de 9 rutas, roles y reescritura de prefijos.
- `auth`: puerto `Verifier` y adaptador JWKS (ES256/RS256).
- `httpapi` (adaptador de entrada): correlación, CORS, autenticación, autorización y proxy.
- Mismas variables de entorno que Java y el mismo OpenAPI servido. Sin dependencias externas.

**Pruebas de aceptación y resultados.**
| Prueba | Resultado |
|---|---|
| Los 11 casos de `GatewayApplicationTests.java`, portados uno a uno + 19 adicionales (alg none, HS256, RS256, sub vacío, anónimo, nbf, 413, 504, 503 sin fugas, 431, recarga de JWKS, cabeceras X-Forwarded, listado de directorio, claves RSA débiles) | 30/30, 5 repeticiones con `-race` |
| Revisión de seguridad de solo lectura por Antigravity (encargo 03) | 8 hallazgos: 7 confirmados y corregidos con prueba; 1 refutado con prueba (X-Forwarded-For: `ReverseProxy.Rewrite` ya elimina las cabeceras del cliente) |
| **Diferencial** contra el Gateway Java real con los servicios reales del stack (`tools/difftest/run.ps1`) | **0 diferencias en 39 casos** (estado, CORS, WWW-Authenticate, X-Request-Id) |
| Smoke del stack a través del Gateway Go (puerto 18082) | 14/14 (y Java 14/14) |
| Token inválido contra el JWKS real de Supabase | 401 |

**Medición** (una ejecución local, Docker Desktop/WSL2, 2 000 peticiones, concurrencia 16; evidencia en
`docs/evidencias/gateway-go-difftest-20261106.txt`):
| | Java | Go |
|---|---|---|
| Imagen | 520 MB | 16,2 MB |
| Arranque hasta health 200 | 5,8–8,4 s | 0,5–0,6 s |
| RAM en reposo / tras carga | 220–237 / 290–313 MiB | 2,2–2,4 / 9–10 MiB |
| Proxy a Monitoring p50 / p95 | 24–31 / 52–73 ms | 3,7–5,6 / 7–16 ms |
| Rechazo 401 p50 | 6,5–8 ms | 0,5–0,75 ms |
Estas cifras son de un equipo de desarrollo, no de producción. Indican menor consumo de recursos de cómputo;
**no** demuestran ahorro energético.

**Hallazgo de la prueba diferencial.** Spring Security 7 no da holgura a `exp` (rechaza un token expirado hace 1 s)
y sí la da a `nbf` (60 s). La suposición inicial era de 60 s para ambos. Se corrigió en Go y queda cubierto por pruebas.

**Endurecimiento tras la revisión 03:**
- La recarga del JWKS no retiene el candado durante la red y responde con las claves en caché.
- Backoff de 30 s tras un fallo o ante un `kid` desconocido; contexto de descarga propio.
- RSA ≥ 2048 bits medidos en bits y exponente válido.
- `ReadTimeout` de 60 s y sin listado en `/openapi/`.
- Cuerpo de las rutas GET limitado a 64 KB (Java no lo limita).

**Divergencias aceptadas** (no afectan a clientes):
- Cuerpos de más de 64 KB en GET devuelven 413.
- Content-Type de 413 y 431 y del OpenAPI.
- JWKS caído: Go responde 503 sin aceptar el token; en Java no se probó.
- Upstream caído: Go responde 503 sin detalles; en Java no se probó.

**Decisión.** Java sigue siendo el Gateway por defecto. El Go queda como alternativa validada, activable con
`compose.gateway-go.yml`. Motivos para no cambiar todavía:
1. La guía de exposición del equipo (`guia-exposicion/01`, `05`) defiende Spring Cloud Gateway.
2. `software/gateway/AGENTS.md` fija Java 21/Spring.
3. El beneficio depende del hosting (D-07).

Activarlo como predeterminado requiere decisión del usuario/equipo, actualizar la guía de exposición, el
`AGENTS.md` del Gateway y los workflows, y una prueba con usuario real de Supabase.

**Monitoring y Simulator.** No se reescribieron. Monitoring (112 pruebas, constructor PromQL) es el siguiente
candidato solo si D-07 lo justifica. Prediction sigue en Python.

## D-07 Hosting a costo cero — Pendiente
- No se ha investigado todavía en esta sesión. Requiere comparar Render gratuito con alternativas vigentes (documentación oficial fechada) sobre suspensión, arranque en frío, RAM/CPU, cuotas, Docker, red interna, almacenamiento, tarjeta requerida y riesgo de cobro, incluida la viabilidad de Prometheus continuo e inferencia ML.
- El frontend es estático (HTML/JS + nginx), compatible en principio con GitHub Pages; falta base path, URL HTTPS del Gateway, CORS y redirects de Supabase Auth.
