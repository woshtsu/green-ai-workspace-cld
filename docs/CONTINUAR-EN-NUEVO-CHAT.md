# Continuar en un chat nuevo (resumen al 2026-11-07, tarde — semana 13)

Lee primero `AGENTS.md`, `docs/HANDOFF.md` y este archivo. Rama de trabajo: **`test`** (publicada en `origin/test`). `main` no se tocó desde el retiro del workspace antiguo.

## Lo nuevo de la semana 13 (2026-11-07, tarde) — leer primero
| Qué | Dónde | Estado |
|---|---|---|
| Informe corregido (Word) | `entregables/informe-corregido/informe-unidad-III.md` → `exportados/semana13/…-informe-unidad-III-CORREGIDO.docx` | Listo para revisión del equipo; faltan 15 capturas, NRC y URL del video |
| Documento semana 13 (Word) | `entregables/semana13/semana13-calidad-furps-owasp.md` → `exportados/semana13/…-semana13-calidad-FURPS-OWASP.docx` + `MODELO-FURPSPLUS-Green-AI.xlsx` | Listo para revisión; faltan 11 capturas y NRC |
| Auditorías FURPS+/OWASP 01–07 | `docs/calidad/` | Ola 1 implementada (commit `d24d86f`); olas 2–3 planificadas (17/11–12/12) |
| Capturas por integrante | `entregables/CAPTURAS-PENDIENTES.md` | Por hacer (equipo) |
| Trello | `guias/trello/GUIA-TRELLO-POR-INTEGRANTE.md` + `herramientas_IA/trello/validar_trello.py` | Días 1–4 (07/11–13/11) por hacer, cada uno con su cuenta; luego exportar JSON y validar |
| Video | `docs/exposicion/GUION-VIDEO-UNIDAD-III.md` + `herramientas_IA/video/carga_transacciones.py` | Guion listo; script sin ejecutar |
| Exportar a Word | `herramientas_IA/README.md` § Exportación DOCX | `md_a_docx.py` + `actualizar_word.ps1` |

**Producción actualizada (PR #1 fusionado el 08/11):** https://woshtsu.github.io/green-ai-workspace-cld/ — `main` está protegida (ruleset: PR + 1 aprobación; el dueño tiene bypass). Trabajar en `test` y abrir PR.

URL real de Prediction en Render: `https://green-ai-prediction-dev-zxly.onrender.com` (las de Monitoring, Simulator y Prometheus: copiarlas del panel).

## Qué quedó hecho la noche anterior
| Área | Estado | Dónde |
|---|---|---|
| Carpeta `entregables/` | Reorganizada: `informe-corregido/` (lo que se entrega: `informe-unidad-III.md`, `evidencias/`, `evidencias-nube/`, `cambios-tecnicos-a-reflejar.md`) y `trabajos-previos/` | `entregables/README.md` |
| Prediction ligera | Imagen 2,85 GB → 510 MB; RAM 174 → 122 MiB (una medición); 100 pruebas y smoke 14/14 | `docs/evidencias/prediction-imagen-ligera-20261107.md` |
| CI/CD | `.github/workflows/ci.yml` (pruebas por servicio, imágenes Docker) y `pages.yml` (main = raíz, test = `/dev/`) | `docs/GUIA-GITHUB-PAGES-Y-CI.md` |
| Render (cuenta personal, workspace «My Workspace») | 6 servicios gratuitos `green-ai-*-dev` en rama `test`: prediction, data-processing, gateway (Go), simulator, prometheus, monitoring. Auto-deploy apagado. No tocar `SoftwareAnemia` (otro proyecto) | `docs/GUIA-DESPLIEGUE-RENDER.md`, `docs/evidencias/render-desarrollo-20261107.md`, `render.yaml` |
| Frontend nuevo (rama `test`) | Dashboard en pestañas, gráfico media/máx/mín + comparación de 5 servidores, tabla paginada, ayuda «?», avisos de espera sin códigos, energía (simulador modelado / ejemplo / archivo), vista `flows.html` «Red de flujos» (propuesta ilustrativa), navegación común | `software/frontend/` (48 pruebas) |
| Evidencias | Capturas en `entregables/informe-corregido/evidencias-nube/` | |
| Mejora del modelo | Solo investigación y plan | `docs/MEJORA-MODELO-PREDICCION.md` |

URLs (desarrollo): Gateway `https://green-ai-gateway-dev.onrender.com`; frontend `https://woshtsu.github.io/green-ai-workspace-cld/dev/` (producción: raíz del mismo sitio; desde el 08/11 `GATEWAY_URL_PROD` = Gateway de desarrollo, antes estaba vacía). Los servicios gratuitos se duermen a los 15 min y pierden el historial (Simulator/Prometheus): **despertarlos ≥ 25 min antes de grabar el video**.

## Pendiente (en orden)
1. **Supabase (lo hace el dueño del proyecto):** añadir a *Authentication → URL Configuration* las URLs `https://woshtsu.github.io/green-ai-workspace-cld/` y `.../dev/`; aplicar el enum `VIEWER`; revisar RLS «Permitir todo» y la columna `password` en texto plano (ver «Riesgos» en `docs/HANDOFF.md`).
2. Fijar el *Health Check Path* en cada servicio de Render (Prediction `/health/ready`, Data Processing `/api/v1/health`, Gateway/Monitoring `/actuator/health`, Simulator `/health`, Prometheus `/-/healthy`).
3. Verificar con sesión real el frontend nuevo en `/dev/` (cada pestaña, «Predecir 15 min», energía con el simulador, `flows.html`) y tomar capturas para el informe. Lo verificado hasta ahora fue con un arnés local (`herramientas_IA/arnes_frontend/`) que simula la sesión y usa datos reales de Render.
4. Video: seguir `docs/exposicion/GUION-VIDEO-UNIDAD-III.md`; ensayar y ejecutar `carga_transacciones.py` contra Render (verificar que funciona antes de grabar).
5. Informe y semana 13: insertar capturas (`entregables/CAPTURAS-PENDIENTES.md`), NRC y URL del video; reexportar si se edita el .md. Olas 2–3 del plan de calidad: `docs/calidad/02_plan_furps.md` y `05_plan_owasp.md` (HU-07 aprobación humana, PDF HU-13, rate limiting, registro de 401/403, RLS).
6. Mejora del modelo según `docs/MEJORA-MODELO-PREDICCION.md` (empezar por la evaluación walk-forward vs persistencia).
7. Producción real: crear servicios `*-prod` con rama `main`, y poner `GATEWAY_URL_PROD` distinto (hoy es igual a `GATEWAY_URL_DEV`). Cuidado con las 750 h/mes gratuitas compartidas (también las gasta `SoftwareAnemia`).
8. Pendientes técnicos viejos: Prometheus/Grafana con predicciones, reporte PDF, factor de emisión con fuente para CO₂e, refactor hexagonal de `application/runner.py` (ver HANDOFF).

## Cómo trabajar (política del repo)
- Claude coordina; Antigravity (`herramientas_IA/agentes/agy_task.py`) falló hoy dos veces en headless por permisos de `command` (denegado, sin cambios): por eso el frontend lo implementó Claude. Si se reintenta, lanzar con `cwd` en la carpeta del servicio y reglas `--allow-command` ancladas (ver `docs/TOOLS_EVALUATION.md`).
- Nada de push/producción sin autorización del usuario. El usuario autorizó el push a `test` la noche del 2026-11-07.
- Pruebas: `cd software/frontend && node --test tests/*.test.cjs` (48); Prediction `pytest` en `software/prediction` (100); smoke del stack local `python software/infraestructura/smoke/smoke.py`.
- Verificación visual del frontend sin login: `python herramientas_IA/arnes_frontend/harness.py software/frontend 18999`.
- Worktree auxiliar `../green-ai-wt-front` (rama `agy/frontend-redesign`, ya integrada en `test`): puede borrarse con `git worktree remove ../green-ai-wt-front`.

## Actualización (2026-11-07, mañana)
- El compañero (dueño de Supabase) ya configuró las URLs de redirección; los servicios de Render se suspendieron a mano; el login con Supabase funciona.
- Local: `docker compose -f software/infraestructura/docker-compose.yml -f software/infraestructura/compose.swagger.yaml up -d --build` (frontend en `http://127.0.0.1:13001`). Se corrigió el `Dockerfile` del frontend (copiaba los JS por nombre y omitía los módulos nuevos; commit `a760602`, **sin subir**). El stack local quedó detenido (`down`, sin borrar volúmenes).
- Para iterar el frontend sin reconstruir imagen: `docker compose ... stop frontend` y `python -m http.server 13001 --bind 127.0.0.1 --directory software/frontend` (el Gateway local solo acepta el origen `http://127.0.0.1:13001`). Refrescar con Ctrl+F5 por caché.
- Regla permanente nueva en `AGENTS.md`: documentar en HANDOFF y en este archivo al cierre de cada sesión.

- Graphify: instalado el extra `graphifyy[sql]==0.9.96` en `.tools/graphify` (indexa los .sql); grafo regenerado (4347 nodos).
