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

## Semana 13 e informe corregido (2026-11-07, tarde) — Claude coordina, Antigravity (Gemini 3.8 Flash) redacta
**Entregables exportados** (en `exportados/semana13/`, no versionado): `…-informe-unidad-III-CORREGIDO.docx` (99 págs.,
15 capturas pendientes), `…-semana13-calidad-FURPS-OWASP.docx` (36 págs., 11 pendientes) y
`MODELO-FURPSPLUS-Green-AI.xlsx` (hojas Inicial / Actual / Esperado). Instructivo de capturas por integrante:
`entregables/CAPTURAS-PENDIENTES.md`. Faltan NRC (`NRC-PENDIENTE`) y URL del video (`VIDEO-URL-PENDIENTE`).

| Trabajo | Resultado | Revisión de Claude |
|---|---|---|
| Informe corregido (`entregables/informe-corregido/informe-unidad-III.md`) | 3 encargos en paralelo (partes I–VI, VII, VIII–anexos); cifras sin respaldo retiradas; RF real; discusión con 3 antecedentes; presupuesto PMBOK (S/ 24 872,40 cuadra); carátula con Claude declarado como asistente de IA | Verificado XGBoost 15 min MAE 3,457 vs RF 3,222 (`results/metrics/model_comparison.csv`) y energía 4 888/4 896 Wh; borrada imagen vieja del presupuesto (S/ 22 080 con K8s); enlace Trello corregido a PL8uQ4rF; URL de Prediction corregida (`-zxly`) |
| Diagramas | `componentes-green-ai.puml`, `despliegue-green-ai.puml` y EDT renderizados con PlantUML local | Sustituyen las capturas C102/C103 |
| Auditorías S13 (`docs/calidad/01..07`) | FURPS+ 85 % → 87 % tras ola 1 (esperado 98 %); OWASP 80,5 → 85,0/100; dictamen «Apto para producción con observaciones» | La 1.ª auditoría FURPS+ daba 96 % (sobrecalificada): se recalificó (HU-05/07/09/11/13/15, hexagonal del simulador, cold start). Rutas `file:///` sustituidas |
| Ola 1 de mejoras (commit `d24d86f`) | nginx: X-Frame-Options, Permissions-Policy, COOP y cabeceras repetidas en `config.local.js`; SRI SHA-384 en CDN; Actions fijadas por SHA; `docs/GUIA-RAPIDA-USUARIO.md` | `node --test` 48/48; `nginx -t` OK; cabeceras comprobadas con curl en contenedor; SRI cargado en navegador sin errores. Evidencia: `docs/evidencias/semana13-ola1-verificacion.md`. Workflows **no ejecutados** en GitHub |
| Documento S13 (`entregables/semana13/semana13-calidad-furps-owasp.md`) | Redactado por Antigravity | Salidas de comandos **inventadas** (puerto 8080, grep, node --test) sustituidas por salidas reales; nombres de alertas corregidos |
| Trello (`guias/trello/GUIA-TRELLO-POR-INTEGRANTE.md`) | Tarjeta por tarjeta y plan por integrante en 4 días; sin dailies retroactivos inventados | 16 rutas de evidencia inventadas corregidas; checklist HU-07 sin falso «hecho». Validador `herramientas_IA/trello/validar_trello.py` (el JSON actual: 57 errores) |
| Video (`docs/exposicion/GUION-VIDEO-UNIDAD-III.md`) | Guion de 25 min, 7 episodios, diálogos y planes B | Quitadas cifras anticipadas (600/600, p50 128 ms); marcadores `[leer …]`. Script `herramientas_IA/video/carga_transacciones.py` **no ejecutado** |
| Exportación | `md_a_docx.py` rediseñado (plantilla de estilos, carátula, encabezado/pie, tablas verdes, horizontal para ≥ 9 columnas), `actualizar_word.ps1` | Revisado en PDF por Word. El validador XSD de la skill docx falla en Windows por su instalación (falta un archivo de esquemas), no por el documento |
| Skills | `find-skills` (vercel-labs/skills) instalado en `.claude/skills/`; elegida la skill `docx` de Anthropic (214 k instalaciones) | Las demás opciones tenían < 1 k instalaciones |

Incidencias: Antigravity intentó ejecutar un comando en el encargo 17 (denegado; se reanudó la conversación).
Una exportación de Excel por COM se colgó (instancia oculta cerrada a mano). `exportados/` sigue sin versionar.

Push a `origin/test` (autorizado por el usuario, 2026-11-07): commits d24d86f..900d173. GitHub Actions run 42403467382 (CI): prediction, data-processing, gateway-go, frontend, monitoring e imágenes Docker **success**; Pages (run 42403467377) **success** con las acciones fijadas por SHA.

**PR #1 fusionado en `main`** (2026-11-08 00:15 UTC, commit e129b93, fusión con bypass del administrador a pedido del usuario; ruleset de `main` con 1 aprobación). CI de main (run 42428931873) y Pages (run 42428931843) **success**. Producción https://woshtsu.github.io/green-ai-workspace-cld/ ya sirve el frontend nuevo (`flows.html` 200, SRI presente); `/dev/` sigue en pie. Producción y desarrollo comparten el Gateway de Render.

Corrección 2026-11-08 00:45 UTC: la variable de repositorio `GATEWAY_URL_PROD` valía `https://` (incompleta desde el 07/11), por lo que producción servía `gatewayBaseUrl: "https:"`. Se fijó a `https://green-ai-gateway-dev.onrender.com` (autorizado por el usuario) y se relanzó Pages (run 42431158995, success). Verificado: config de producción correcta, `/dev/` 200 y preflight CORS desde github.io 200.

Diagnóstico 2026-11-08: 429 intermitente de Render/Cloudflare entre servicios por URL pública (Prometheus→Prediction /metrics marcado down; desde fuera, 200) y 504 por arranque en frío. No es rendimiento del código (Monitoring 0,5 s). Red privada no disponible: los servicios gratuitos no reciben tráfico privado (https://render.com/docs/free). Añadido `herramientas_IA/video/mantener_despierto.py` (probado: 6/6 en 200). Pendiente opcional: Prometheus→Prediction cada 60 s y refresco del frontend a 30 s.

Ajuste 2026-11-08 (pedido del usuario, opción B: grabar con la URL de producción y backend *-dev): refresco del frontend 15 → 30 s (monitoring.js, racks.js, flows.js, textos de ayuda e index) y Prometheus→Prediction 60 s (`prometheus.render.yml`, timeout 20 s; alertas con ventanas ≥ 2 min). Frontend 48/48; YAML válido (promtool no ejecutado: Docker apagado). Guion: sección 0 con los cambios y las herramientas.

**PR #2 fusionado en `main`** (2026-11-08, commit b5975b0, bypass del administrador a pedido del usuario). Pages y CI de main **success**; producción sirve el refresco de 30 s y `gatewayBaseUrl` correcto. Prometheus-dev redesplegado en Render (deploy dep-dbnupobl550s73890k7g, commit af903e4): Prediction 1m **up**, Simulator 15s **up**.

Guion del video adaptado a grabación por partes (2026-11-08): sección 0.5 (quién graba qué, franja común con `mantener_despierto.py` a cargo de Ricardo, ajustes OBS, entrega de clips; edita Jhonny Cristhian), episodio 4 solo con navegador (GitHub Actions y archivos de resultados; métricas base corregidas según `model_comparison.csv`: persistencia 4,61/6,39, media móvil 3,74/5,19, XGBoost 3,46/4,79), carátula y cierre con clips individuales y URLs de producción en lugar de `/dev/`.

2026-11-09: PR #4 fusionado: `entregables/word/` con los .docx y el .xlsx (excepción en .gitignore). Reexportar y volver a subir si cambian los .md.

## Video Unidad III: grabador y prueba de carga (2026-11-09, chat del video; sigue en curso)
- `carga_transacciones.py` **probado contra Render por primera vez**: `--iteraciones 5` → 16/16 HTTP 200; p95 2,8–3,5 s; recomendaciones `eligible_for_review` 5/5 (`docs/evidencias/carga-ensayo-5.csv`). Un intento previo dio 504 al descubrir nodos (pasajero entre Gateway y Monitoring): ahora el descubrimiento reintenta hasta 3 veces y registra cada intento en el CSV. Si Supabase rechaza el login, el script muestra el motivo. Estimación para 200 iteraciones: ~8–9 min.
- Nuevo `herramientas_IA/video/grabar_episodios.py` (Playwright + Edge + ffmpeg gdigrab; un MP4 por episodio en `exportados/video/` con rótulos y `-pasos.md` con minutos para la locución; verifica el HTTP de cada llamada y marca FALLO sin ocultarlo) y `ep3_terminal.ps1` (carga real en Windows Terminal). Runtime en `.tools/video` (venv con playwright 1.48.0; perfil de Edge en `.tools/video/perfil-edge`). Ensayos sin grabar: Ep. 1, 2, 4, 5 y 7 OK; Ep. 6 se omite sin sesión de Trello (tablero privado). Prueba de 5 s de ffmpeg: escritorio 1920×1080 correcto.
- Históricos en la nube: `green-ai-data-processing-dev` tenía `HISTORICAL_SOURCE=none` (el reporte del Ep. 2 daba 503). El usuario configuró en Render `HISTORICAL_SOURCE=supabase`, `SUPABASE_ENABLED=true`, URL, `sb_publishable` y la clave legacy `anon` como `SUPABASE_READ_TOKEN`; verificado: `/api/v1/reports/historical-summary` HW045 10–11/07 → 200, `source=supabase`, 40 registros. Riesgo: funciona porque la RLS es permisiva; al endurecerla hará falta un JWT de lectura dedicado. `render.yaml` y la guía actualizados.
- Guion: tabla 6.1 corregida con `model_comparison.csv` (antes tenía MAE/RMSE inexistentes) y retiradas de 6.3 las cifras sin medición (arranque en frío 140→45 s, inferencia 85→28 ms).
- Riesgos de rúbrica: el video automático no lleva cámara (cada integrante graba cara y voz encima); Ind. 9 solo tiene 1 llamada del PMV1 en la carga (opción: añadir métricas por iteración → 801); Ind. 11 usa funciones PL/pgSQL y trigger, no `CREATE PROCEDURE`.
- Pendiente: grabar Ep. 1, 2, 5, 3, 4 y 7 (el usuario decide cuándo); Ep. 6 cuando el tablero esté completo (otro chat revisa Trello).

## Video Unidad III: grabación de pantalla (2026-11-10, 00:50–02:00)
- **Grabados los 7 episodios** con `grabar_episodios.py --ritmo 1.6` (sin voz, 1920×1080, tema oscuro): Ep1 1:48, Ep2 2:23, Ep3 7:58, Ep4 2:49, Ep5 1:48, Ep6 2:11, Ep7 3:54 → `exportados/video/` (no versionado). Revisados con mosaicos de 12 fotogramas por clip: datos visibles, sin pantallas vacías ni errores. El 1.er Ep. 3 se descartó (letra ilegible y Prometheus tapado por la terminal) y se regrabó.
- **Ep. 3 / Ind. 9:** dos corridas reales, ambas 601/601 HTTP 200. La del video (01:49–01:56, 414 s): p50/p95 dataset 892/1511 ms, predicción 2700/3471 ms, recomendación 2704/3475 ms; 200 `eligible_for_review`. CSV `docs/evidencias/carga-video.csv`; 1.ª corrida en `carga-video-20261110-0127.csv`. Captura C309 insertada en el informe (`evidencias-nube/carga-601-transacciones-render.png`); falta reexportar el Word.
- Cambios del grabador: Edge normal + CDP (`launch_persistent_context` salía con código 0 en Edge 157 con el perfil; además así Google/Trello permiten iniciar sesión); tema oscuro forzado (`--force-dark-mode` + `prefers-color-scheme: dark`); sin banda verde sobre GitHub; detección de 404 de GitHub (el Ep. 4 enlazaba `model_comparison.csv`, que está en `.gitignore` → ahora muestra `docs/academico/06-prueba-de-concepto.md` §3; guion corregido); Trello: selector `card-name`, cookies «Solo necesarias», espera de inicio de sesión; Ep. 3: letra ×2 en Windows Terminal (SendKeys `^{ADD}`), la terminal se cierra sola y Edge pasa al frente.
- Ensayos previos: el Ep. 5 da 422 si el simulador lleva < 20 min despierto (esperado); un 504 aislado al refrescar racks durante el despertar.
- Pendiente: locución y cámara de cada integrante, carátula/intro/cierre, montaje (Jhonny), subir y reemplazar `VIDEO-URL-PENDIENTE`; reexportar el informe Word.

## Video Unidad III: carátula, cierre y montaje (2026-11-10, 02:00–02:25)
- Nuevo `herramientas_IA/video/portada_cierre.py`: carátula (proyecto, docente, 4 integrantes con rol, 7 episodios; 0:46) y cierre (indicadores → minuto real de cada episodio calculado con ffprobe, QR del repo y de la app, créditos y declaración del asistente de IA; 0:47) como diapositivas HTML a pantalla completa; `unir` recorta el blanco inicial de cada clip (Ep. 3: 2 s) y recodifica (con `-c copy` quedaban DTS repetidos).
- **Video completo:** `exportados/video/green-ai-unidad-III.mp4` (24:28, 1920×1080, 30 fps, sin audio, 24,7 MB; decodificado sin errores) + `descripcion-youtube.txt` (marcas de tiempo). Se tapó con fondo oscuro un `about:blank` de 5 s en 12:29–12:33 (Ep. 3, al cerrarse la terminal); quedan 3 s de carga de página (Prometheus y Trello).
- Sin logo de la UC (no está en el repo; C100 sigue pendiente) ni NRC (pendiente). Sin voz ni cámaras: la rúbrica pide cámara y nombre completo de los 4 → grabar encima en la edición.
- Fallos corregidos por el camino: Edge restauraba la pestaña anterior al matarlo y las diapositivas se grabaron en una pestaña de fondo (ahora cierre limpio por CDP `Browser.close` y pestaña nueva); `--start-fullscreen` no se aplica al conectar por CDP (ahora `Browser.setWindowBounds` fullscreen); `about:blank` blanco al iniciar cada clip (ahora página oscura).

**PR #5 fusionado en `main`** (2026-11-10 07:36 UTC, commit 27ef69f, bypass del administrador a pedido del usuario). CI del PR 12/12 en verde. El video (`exportados/video/green-ai-unidad-III.mp4`) queda solo en local y en el Drive del equipo, no en GitHub.

**Guion sincronizado con el video (2026-11-10):** `GUION-VIDEO-UNIDAD-III.md` §0.5 (voz y cámara encima del video, tramos por integrante según su rol), §2.2, §5 (locución por minuto real, con las cifras que se ven), §8 y marcas de YouTube con los minutos de 24:28. Detectado: la tabla del doc 08 que sale en el Ep. 4 no coincide con §6.2 (433/447): pendiente actualizar el doc 08.
