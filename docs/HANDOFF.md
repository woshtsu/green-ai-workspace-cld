# HANDOFF — migración a green-ai-monorepo

Actualizado por Claude Code el 2026-11-06. Encargo original: `../output/traspaso-claude/PROMPT_CLAUDE.md`.
Hechos históricos previos: `../output/semana10/HANDOFF.md` (el estado y las pruebas actuales prevalecen).

## Estado en una línea
Monorepo creado, fuentes copiadas sin Git anidados; las 6 suites de pruebas reproducen la línea base; el stack
`green-ai-mono` arranca en Docker y pasa el smoke 14/14 con datos simulados; perfil SQLite de desarrollo con
pruebas de contrato compartidas con PostgreSQL/PostgREST real; Gateway Go equivalente al Java (alternativa, no
predeterminada); Antigravity CLI validado con una revisión
de solo lectura y un cambio pequeño integrado. **Nada publicado, nada desplegado, workspace antiguo intacto.**

## Requisitos del encargo (resumen)
Monorepo con un solo Git; copiar (no mover) preservando cambios locales; recomendaciones dentro de Prediction;
ramas `main`/`test`; perfil SQLite de desarrollo con puertos/adaptadores sin simular Supabase; evaluar Go;
comparar hosting a costo cero; CI/CD revisable sin despliegue automático; DOCX desde Markdown; Claude coordina a
Antigravity sin IDE; honestidad experimental.

## Fuentes copiadas (SHA en `docs/migracion/manifiesto-copia.json`)
| Servicio | Origen | Rama / SHA | Archivos |
|---|---|---|---|
| monitoring | green-ai-monitoring | main d476c32 | 60 |
| simulator | green-ai-simulator | main 47536d7 | 32 |
| gateway | green-ai-gateway | main 9d043fa | 16 |
| data-processing | green-ai-data-processing/Green-IA/data-processing-service (+ datasets/) | main 9d24e3e | 60 + 4 |
| prediction | green-ai-prediction/green-ai-project-docs | Criss 8585d6b | 127 |
| frontend | green-ai-front-end/Frontend-GreenAi | main 2b34192 | 26 |
| infraestructura | raíz del workspace (compose, prometheus-demo, observability/) | b644980 | 10 |
Los 9 repos hijos estaban limpios (sin cambios locales) al copiar; coincide con `output/traspaso-claude/estado-final-repos.json`.
GreenAi_TPI no se migra (D-03). `project-docs` tiene sin versionar `Semana12/` y un PDF: se copiaron las guías y el entregable de Semana 12.

## Commits en `main` (monorepo)
Traslado verbatim → rutas de dataset → Compose aislado → adaptador agy → documentación base → cambio de Antigravity (merge).
Ver `git log --oneline`. Rama `test` creada desde `main`.

## Pruebas ejecutadas en el monorepo (2026-11-06)
| Servicio | Comando | Resultado | Comparación |
|---|---|---|---|
| monitoring | `mvnw.cmd -q -B verify` | 112 tests, 0 fallos | — |
| gateway | `mvnw.cmd -q -B verify` | 11 tests, 0 fallos | = handoff semana10 |
| simulator | `uv run --frozen python -m unittest discover -s tests` | Windows: 10 tests, 1 fallo | El fallo (`test_realtime_exporter_and_graceful_termination`) ocurre igual en el repo original en Windows (señales). |
| simulator (Docker) | `docker run ... green-ai-mono-simulator:local -m unittest discover -s /tests -v` | **10/10 OK** | Confirma que el fallo es solo de Windows. |
| data-processing | `pytest -q` | 88 passed | Antes del ajuste de rutas: 2 fallos por no encontrar `BD_GreenAi.xlsx` |
| prediction | `run_pipeline.py --skip-mlflow` + `pytest` | 96 passed | Sin el pipeline: 6 fallos con 503 MODEL_UNAVAILABLE (esperado: el modelo se genera en build) |
| frontend | `node --test tests/*.test.cjs` (lista explícita) | 13/13 | `node --test tests/` falla en Node actual: hay que pasar los archivos |
| infraestructura | `docker compose ... config --quiet` | OK (también overlay Grafana) | — |
| stack completo | `docker compose -f .../docker-compose.yml -f .../compose.swagger.yaml up -d --build` | 7 servicios Up; prediction y data-processing healthy | Proyecto `green-ai-mono`; workspace antiguo sin contenedores en marcha |
| smoke HTTP | `python software/infraestructura/smoke/smoke.py --out docs/evidencias/smoke-20261106.json` | **14/14** | Mismos casos que el smoke de semana 10 + monitoring vía Prometheus, JWT inválido, CORS y frontend |

### Smoke 2026-11-06 (datos SIMULADOS)
Prediction ready/OpenAPI 200; predicción 200 `origin=estimated`; recomendación 200 `eligible_for_review`,
`executionAllowed=false`; recomendación inválida 422; data-processing health 200; monitoring catálogo y CPU actual 200
con series `origin=simulated` del simulador vía Prometheus; Gateway 401 sin JWT (predicción y recomendación) y con JWT
inválido; preflight CORS desde `http://127.0.0.1:13001` aceptado; frontend 200; Prometheus con jobs prediction y
simulator UP. **No** autentica un usuario real de Supabase ni prueba precisión o ahorro.

### Consumo observado en reposo (docker stats, Windows/WSL2)
gateway 283 MiB · monitoring 211 MiB · prediction 174 MiB · data-processing 76 MiB · prometheus 41 MiB ·
simulator 22 MiB · frontend 9 MiB. Imágenes: prediction 2,85 GB (el lock incluye jupyter/mlflow), gateway 520 MB,
monitoring 457 MB. Relevante para D-06 (Go) y D-07 (hosting con 512 MB típicos en planes gratuitos); medición única, sin carga.
Avisos de deprecación en pytest/Maven no se ocultaron ni se cambiaron umbrales.
El pipeline de Prediction reescribe `software/prediction/results/manifest.json` (versionado); se restauró con `git checkout`.

## Antigravity
Detalle y registro de la prueba inicial: [TOOLS_EVALUATION.md](TOOLS_EVALUATION.md). Resumen:
- `agy` 1.5.2 autenticado; headless `-p --output-format json`; continuidad con `--conversation <id>`.
- Lecciones: (1) `SUCCESS` + exit 0 puede venir vacío o con "Wait for subagent response."; (2) las acciones denegadas solo aparecen en `denied_actions`; (3) las reglas `command` se comparan con la línea completa → lanzar con `cwd` del servicio y regex anclada; (4) concesión global heredada `command(powershell)` → denegada siempre por el adaptador.
- Plan Google AI Pro: no verificado en la cuenta (lo confirma el usuario). Créditos de pago desactivados por sesión.

## Honestidad experimental
Sin respaldo verificado (no convertir en resultados): XGBoost como modelo final, RMSE 7,1 %, mejora 57,7 %, 45 ms,
RAM < 35 MB, ahorro 18,4 %, 50 propuestas rechazadas, afirmaciones de Kubernetes/RabbitMQ. El informe copiado en
`entregables/semana12/` contiene 66 menciones de estos términos; revisarlo antes de reutilizarlo. Capturas prueban
solo el caso mostrado; Swagger no prueba precisión; CPU simulada no es energía física.

## Perfil SQLite (2026-11-06) — ver D-05
| Prueba | Resultado |
|---|---|
| Data Processing completo, sin PostgREST | 106 passed, 8 skipped (PostgREST de pruebas no configurado → NO verificado en esa ejecución) |
| Data Processing completo + PostgreSQL 17/PostgREST v13 de pruebas | **114 passed** (contrato idéntico en ambos backends + lector sin escritura) |
| Stack con `compose.sqlite-dev.yml`, semilla completa (50 hardware, 100 000 logs) | `/api/v1/historical-logs` 200 `source=sqlite`; página 2 por cursor coherente; cursor inválido 422; Gateway sin JWT 401 |
| Smoke del stack con el overlay | 14/14 |
Comandos: ver `software/infraestructura/compose.sqlite-dev.yml` y `compose.contract-postgres.yml` (cabeceras).
La BD de contrato se levantó y destruyó (`down -v`) en cada ejecución; sus contraseñas y el secreto JWT fueron
aleatorios en memoria y no se guardaron.

## Documentación académica (2026-11-06)
- Índice por semana: `entregables/README.md`; guías: `guias/README.md`; cambios técnicos que deben reflejarse en
  las semanas 13–16: `entregables/notas/reestructuracion-monorepo.md`.
- Semanas 9–12: el **informe entregado** (PDF del usuario en `exportados/semana12/`, no versionado) se convirtió a
  `entregables/semana09-12/informe-unidad-III.md` con 54 imágenes y 41 tablas, mediante
  `herramientas_IA/exportacion/pdf_a_markdown.py`. Se revisaron a mano la portada y varias páginas (22, 47); el
  código del anexo perdió la sangría.
- Semanas 1–2, 4 (por confirmar) y 6 importadas desde `project-docs` con las imágenes separadas.
- **Faltan las guías del docente de las semanas 1–7 (y 10–11, si existen)**: el usuario ofreció enviarlas.
- No exportar DOCX/PDF salvo pedido expreso del usuario (instrucción del 2026-11-06).
- El informe entregado contiene cifras sin respaldo (XGBoost RMSE 7,1 %, 57,7 %, 45 ms, menos de 35 MB, 18,4 %):
  no reutilizarlas en las próximas entregas.

## Riesgos detectados
- **Supabase con RLS permisiva (según el snapshot `software/simulator/docs/assets/esquema-verificado.json`, 2026-09-22):**
  políticas `"Permitir todo"` (`ALL`, `true`, rol `public`) en `hardware`, `logs` y `usuario`. Además `usuario`
  tiene una columna `password` junto a `password_hash`. Si sigue vigente, la clave *publishable* (pública en el
  frontend) permitiría leer y modificar esas tablas. **No se comprobó el estado actual ni se tocó la BD**. Revisar
  con prioridad en Supabase: restringir las políticas y eliminar `password` en texto plano.
- `BD_GreenAi.xlsx` (versionado aquí y en el repo original) contiene en la hoja `Usuarios` contraseñas en texto
  plano de usuarios sintéticos (`Admin123!N`). No son credenciales reales conocidas, pero no deben reutilizarse; si
  se usaron para crear usuarios reales en Supabase, cambiarlas. La semilla SQLite no carga esa hoja.
- `GreenAi_TPI/Backend/.env` versionado en GitHub (clave Supabase *publishable* + URL). Decide el propietario.
- `.gitignore` del workspace antiguo está envuelto literalmente en un here-string de PowerShell (`@' ... '@ | Set-Content`): sus reglas pueden no aplicarse como se espera. No se modificó.

## Pendientes (en orden propuesto)
1. ~~Simulator en Docker~~ — hecho (10/10) tras arrancar Docker Desktop con autorización del usuario.
2. ~~Arrancar `green-ai-mono` y smoke~~ — hecho (14/14). Falta: recorrido desde el navegador con sesión real de
   Supabase (añadir `http://127.0.0.1:13001` a los redirects de Supabase Auth si se usa login) y capturas sin tokens.
   El stack queda en marcha; detener con `docker compose -f software/infraestructura/docker-compose.yml down` (sin `-v`).
   Separar dependencias de entrenamiento/notebooks de la imagen de inferencia de Prediction (2,85 GB).
3. Graphify del monorepo: generado con `graphify update .` (ver abajo); revisar `.graphifyignore`.
4. Hosting (D-07): investigación con fuentes oficiales fechadas y recomendación; workflows `.github/workflows` con activación manual (`workflow_dispatch`) y GitHub Environments. Adaptar `software/frontend/.github/workflows/deploy.yml` (no se ejecuta desde una subcarpeta).
5. ~~SQLite (D-05)~~ — hecho. Pendiente: ejecutar `tests/test_historical_logs_contract.py` contra un proyecto
   **Supabase de pruebas** (requiere su URL, API key y JWT de lectura, aportados por el usuario) antes de promover a `main`.6. ~~Evaluación Go (D-06)~~ — Gateway Go validado (30 pruebas, 0 diferencias en 39 casos frente a Java, smoke 14/14,
   16 MB / ~10 MiB / 0,5 s frente a 520 MB / ~290 MiB / 6–8 s). **No es el predeterminado**; activarlo es decisión del
   usuario/equipo (afecta a `guia-exposicion` y a `software/gateway/AGENTS.md`). Monitoring en Go: solo si D-07 lo
   justifica. Comandos: `software/gateway-go/README.md`. El contenedor `gateway-go` (puerto 18082) queda en marcha.
7. DOCX: instalar Pandoc de forma reproducible (o `pypandoc-binary` en `.tools/`) y exportar `entregables/semana12/`; revisar tablas e imágenes visualmente.
8. Perfiles de Agency Agents (máx. 3) tras verificar nombres en el repositorio oficial.
9. Comprobación final: sin gitlinks/secretos/Git anidados, arranque desde clon limpio, lista de aceptación.
10. Refactor sugerido por la revisión 01: `application/runner.py` importa adaptadores y maneja señales (hexagonal).

## Comandos útiles
```powershell
git -C C:\Practicas\202620\TallerProyectos\green-ai-workspace\green-ai-monorepo status
git ls-files -s | Select-String '^160000'        # debe estar vacío
git worktree list                                  # worktrees de agentes
```

No borrar el workspace antiguo ni cambiar producción: requiere autorización expresa tras la lista de aceptación.
