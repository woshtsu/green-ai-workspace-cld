# HANDOFF — migración a green-ai-monorepo

Actualizado por Claude Code el 2026-11-06. Encargo original: `docs/historico/traspaso-claude/PROMPT_CLAUDE.md`.
Hechos históricos previos: `docs/historico/semana10/HANDOFF.md` (el estado y las pruebas actuales prevalecen).

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

## Avance del 2026-11-06 (tarde)
- **HU-05 MLflow:** `run_pipeline.py` sin `--skip-mlflow` registra el experimento `computational-demand-prediction`
  (id 394141087236111562), con 1 run `random_forest_15m` y MAE de test 3,85, en `software/prediction/mlruns/`
  (ignorado por Git). Falta una captura de la UI (`mlflow ui`).
- **CHG-07:** sin PDF; el reporte se entrega en JSON/CSV + Markdown; las pruebas, con capturas.
- **Frontend «Racks con calor»** (`software/frontend/network.html`, `racks.js`, `racks.css`, `racks.json`):
  50 nodos simulados en 5 racks, CPU en vivo cada 15 s y predicción por nodo. Lo hizo Antigravity (encargo 06,
  Gemini Flash) y lo revisó Claude: 20/20 pruebas. **Falta la verificación visual con sesión real**: el usuario
  inicia sesión en http://127.0.0.1:13001.
- Pendiente del frontend: reducir la verbosidad del resto de páginas y mostrar el PMV2 completo (reporte CSV,
  recomendación, experimento, alertas).
- Despliegue: el usuario evalúa Back4App (contenedores desde GitHub) y Deno Deploy (probablemente solo JS/TS:
  verificar). Idea: repartir servicios entre dos proveedores, con llamadas HTTPS públicas entre ellos.

## Sprint actual frente al plan (revisado el 2026-11-06)
Plan base: `guias/TrabajosDesarrollados/4. Gestión de Proyecto.md` §4.8 (8 sprints de 2 semanas desde el
25/08/2026).
- **Calendario:** el 06/11 corresponde al **Sprint 6** (03–14/11, semanas 11–12). La semana 13 empieza el **Sprint
  7** (17–28/11). El curso va una semana por delante del calendario del plan: el informe 9–12 ya se entregó el
  05/11. Ajustar las fechas del cronograma, línea base frente a ejecutado.

| Sprint | Comprometido | Estado real |
|---|---|---|
| 5 (S9–10) | Modelo seleccionado «≥ 90 %», Policy Engine, API | Hecho (RF, política, `/v1/predictions`, `/v1/recommendations`). El criterio «≥ 90 %» no aplica a una regresión: reformular como MAE frente al baseline. MLflow no evidenciado |
| 6 (S11–12) | Grafana con predicciones y eficiencia, alertas, indicadores de kWh y CO₂e | Alertas **hechas el 2026-11-06** (SimulatorTelemetryDown, NodeCpuSaturationRisk, NodeMemoryPressure, PredictedCpuHigh; promtool OK). Resto parcial: el dashboard `pmv2.json` existe; solo hay alerta de disponibilidad; `/v1/energy` calcula kWh, pero no hay datos de potencia reales y el CO₂e exige un factor con fuente |
| Lab. 11 (S11) | **Despliegue en la nube (no localhost)**, BD remota con *seeding*, pruebas G/W/T con URL pública | **Atrasado**: solo hay servicios antiguos en Render; el monorepo no está desplegado. Bloquea el video (ind. 9–10) |
| **7 (S13–14)** | **RBAC, reportes PDF/CSV, diseño del plan experimental y ejecución del baseline** | **Hecho el 2026-11-06 (salvo PDF):** rol VIEWER de solo lectura en Java y Go (Java 12/12; Go con pruebas nuevas; enum de Supabase ampliado, falta aplicarlo en Supabase); reporte JSON/CSV `GET /api/processing/v1/reports/historical-summary` (Data Processing 121 passed; encargo 05 de Antigravity con Gemini Flash, revisado); experimento baseline frente a Green AI (`docs/academico/10-plan-experimental.md`): con margen del 10 %, riesgo de SLA 15,9 % → 9,5 %; energía modelada −0,2 % (no hay ahorro demostrado). **PDF pendiente** |
| 8 (S15–16) | Experimento Green AI, análisis comparativo, informe y sustentación | Pendiente |

Criterio del PMV3 por corregir: «ahorro energético ≥ 15 %» no tiene sustento. Reformular como «medir la
diferencia de energía estimada, utilización y SLA frente al baseline, con su incertidumbre».
Orden recomendado: (1) desplegar a staging (D-07) → (2) cerrar los pendientes del Sprint 6 → (3) Sprint 7:
plan experimental + baseline, reportes CSV/PDF, rol observador → (4) documento de la semana 13.

## Documentación académica corregida (2026-11-06, segunda parte)
- El usuario aportó las guías del docente (`guias/exportados_docente/`, leídas íntegras), los trabajos previos
  (`guias/TrabajosDesarrollados/`) y 9 artículos (`guias/articulos/`).
- Se creó `docs/academico/` (**sin imágenes; no se entrega**), con el índice C1–C6, la revisión docente con
  puntajes (8,5/20 según la captura) y el plan de la semana 13, más un documento por competencia.
- Es la referencia para las próximas entregas. Lo único que se exportará será el documento de la semana 13.
- **Hallazgos clave:**
  1. Las cifras de la PoC (XGBoost MAE 5,4 %, RMSE 7,1 %, 45 ms, menos de 35 MB) no tienen experimento. El
     pipeline real elige Random Forest (MAE 3,22, RMSE 4,59 pp en validación).
  2. Khan et al. está mal citado (el 87,48 % es la mejora de un clustering).
  3. El presupuesto omitía recursos en la línea base y fijaba la contingencia sin vínculo con los riesgos.
  4. Las listas de Trello no coinciden con la lista de cotejo S10.
  5. Nombre inconsistente del integrante Quintana.
  6. `S6.Arquitectura Híbrida.md` está vacío.
- EDT en `herramientas_IA/diagramas/edt-green-ai.puml` (sin renderizar).

## Documentación académica (2026-11-06)
- Índice por semana: `entregables/README.md`; guías: `guias/README.md`; cambios técnicos que deben reflejarse en
  las semanas 13–16: `entregables/informe-corregido/cambios-tecnicos-a-reflejar.md`.
- Semanas 9–12: el **informe entregado** (PDF del usuario en `exportados/semana12/`, no versionado) se convirtió a
  `entregables/informe-corregido/informe-unidad-III.md` con 54 imágenes y 41 tablas, mediante
  `herramientas_IA/exportacion/pdf_a_markdown.py`. Se revisaron a mano la portada y varias páginas (22, 47); el
  código del anexo perdió la sangría.
- Semanas 1–2, 4 (por confirmar) y 6 importadas desde `project-docs` (solo en el respaldo del workspace antiguo) con las imágenes separadas.
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
- `GreenAi_TPI/Backend/.env` (solo en el respaldo del workspace antiguo) versionado en GitHub (clave Supabase *publishable* + URL). Decide el propietario.
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
   usuario/equipo (afecta a `docs/exposicion` y a `software/gateway/AGENTS.md`). Monitoring en Go: solo si D-07 lo
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

## Verificación visual de Racks (2026-11-06, con sesión real del usuario en el panel)
- OK: 50 nodos en 5 racks con CPU real del stack, resumen (CPU media 49,9 %), rol OPERATOR visible, panel de detalle de HW001.
- Fallo: «Predecir 15 min» → 422 INSUFFICIENT_DATA (2 registros). Causa: el simulador se reiniciaba cada hora y perdía el historial. Corregido: duración por defecto 86400 s en docker-compose.yml.
- Errores de la UI para el próximo encargo de frontend: el panel no muestra los errores de la API y el refresco de 15 s borra el resultado de la predicción. Con la escena «normal» todos los nodos quedan en ~50 %; para la demo usar SIMULATOR_SCENARIO=configs/scenarios/high.json o variar la carga.

## Frontend PMV2 (2026-11-06, encargo 07 de Antigravity + correcciones de Claude)
- Dashboard con menos texto y sección «Capacidades PMV2»: recomendación con restricciones, reporte de históricos (resumen + CSV) y experimento baseline vs Green AI (riesgo SLA 3,97 % / 3,97 %; energía modelada −0,16 %; etiqueta «datos simulados, energía modelada»). Verificado en el panel con sesión real.
- Racks: muestra errores de la API (INSUFFICIENT_DATA, 403) y conserva la selección entre refrescos.
- Corrección de Claude: las fechas del reporte se envían con zona horaria (UTC). Etiqueta «Diferencia de energía». Frontend 31/31 pruebas.
- Pendiente: verificar en el panel «Ver resumen» y «Descargar CSV» tras la corrección; capturas para la semana 13; panel de Grafana con predicciones.

## Prediction ligera (2026-11-07)
- Dockerfile multi-etapa + `requirements.serve.txt` + importación diferida de xgboost: imagen 2,85 GB → 510 MB; RAM en reposo 174 → 133–142 MiB; con `PYTHONOPTIMIZE=2` y sin pip, 122 MiB (una medición). Suite 100 pruebas OK; stack reconstruido, smoke 14/14. Detalle: `docs/evidencias/prediction-imagen-ligera-20261107.md`. Sin commitear. Pendiente: desplegar en Render (`docs/GUIA-DESPLIEGUE-RENDER.md`). Los contenedores `green-ai-mono` siguen en marcha.
- `entregables/` reorganizado: `informe-corregido/` (lo que se entrega) y `trabajos-previos/`.

## CI/CD (2026-11-07)
- Añadidos `.github/workflows/ci.yml` y `pages.yml` (main = producción en la raíz de Pages, test = desarrollo en `/dev/`). Guía: `docs/GUIA-GITHUB-PAGES-Y-CI.md`. Solo validados como YAML; sin ejecutar en GitHub. Retirado `software/frontend/.github/workflows/deploy.yml`.

## Estado al 2026-11-07 (noche)
Resumen para continuar en un chat nuevo: `docs/CONTINUAR-EN-NUEVO-CHAT.md`. Frontend nuevo (pestañas, ayuda, avisos de espera, energía, red de flujos) en `test` con 48 pruebas; mejora del modelo: solo plan (`docs/MEJORA-MODELO-PREDICCION.md`); Antigravity falló en headless por permisos de `command` (sin cambios), el frontend lo implementó Claude.
