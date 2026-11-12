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
| Video | `docs/exposicion/GUION-VIDEO-UNIDAD-III.md` + `herramientas_IA/video/grabar_episodios.py` | **Video completo sin voz** `exportados/video/green-ai-unidad-III.mp4` (24:28; carátula + 7 episodios + cierre; no versionado) + `descripcion-youtube.txt`. Falta: voces y cámaras de los 4 encima, subir no listado y poner la URL |
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

## 2026-11-11: revisión de Dina aplicada al informe (ver HANDOFF). Pendiente integrar la rama `worktree-agent-a8e294441df89aac0` (guía Trello PMVn-HUxx) tras confirmar los cambios sin commit de la guía.

## Pendiente (en orden)
1. **Supabase (lo hace el dueño del proyecto):** añadir a *Authentication → URL Configuration* las URLs `https://woshtsu.github.io/green-ai-workspace-cld/` y `.../dev/`; aplicar el enum `VIEWER`; revisar RLS «Permitir todo» y la columna `password` en texto plano (ver «Riesgos» en `docs/HANDOFF.md`).
2. Fijar el *Health Check Path* en cada servicio de Render (Prediction `/health/ready`, Data Processing `/api/v1/health`, Gateway/Monitoring `/actuator/health`, Simulator `/health`, Prometheus `/-/healthy`).
3. Verificar con sesión real el frontend nuevo en `/dev/` (cada pestaña, «Predecir 15 min», energía con el simulador, `flows.html`) y tomar capturas para el informe. Lo verificado hasta ahora fue con un arnés local (`herramientas_IA/arnes_frontend/`) que simula la sesión y usa datos reales de Render.
4. Video: versión vigente `green-ai-unidad-III-subtitulado.mp4` (24:26, chat de 0:45 cortado, subtítulos del guion incrustados; `.srt` aparte); el original `green-ai-unidad-III.mp4` (24:28) queda intacto; la pantalla ya está grabada (ver «Video Unidad III» al final de este archivo). Pendiente del equipo: locución y cámara encima de cada clip con su `-pasos.md`, montaje (Jhonny), subir no listado y reemplazar `VIDEO-URL-PENDIENTE` en el informe; reexportar el Word (C309 ya insertada).
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

## Video Unidad III (2026-11-10) — estado para continuar
- **Clips grabados** (pantalla completa 1920×1080, sin voz, tema oscuro, rótulos): `exportados/video/ep1…ep7-20261110-*.mp4` + `-pasos.md` (minuto de cada paso para la locución). Duraciones: Ep1 1:48, Ep2 2:23, Ep3 7:58, Ep4 2:49, Ep5 1:48, Ep6 2:11, Ep7 3:54 (≈ 22,5 min; con carátula, intro y cierre ≈ 25 min). `DESCARTADO-ep3-…0127.mp4`: letra ilegible. `exportados/` no se versiona: **compartir los MP4 con el equipo por la carpeta del grupo**.
- **Ep. 3 (Ind. 9):** 601/601 HTTP 200 (01:49–01:56); p95 dataset 1,5 s, predicción/recomendación 3,5 s; 200 `eligible_for_review`. CSV `docs/evidencias/carga-video.csv` (y la 1.ª corrida, también 601/601, en `carga-video-20261110-0127.csv`).
- **Regrabar un episodio:** `python herramientas_IA/video/mantener_despierto.py` ≥ 25 min antes (el Ep. 5 necesita historial del simulador; antes da 422), luego `.tools/video/Scripts/python herramientas_IA/video/grabar_episodios.py --ritmo 1.6 <N>`; ensayar antes con `--ensayo`. El perfil de Edge (`.tools/video/perfil-edge`) guarda las sesiones de la app y de Trello (Google). Edge se lanza normal y se controla por CDP (puerto 9333): cerrar cualquier Edge abierto con ese perfil antes.
- **Históricos en la nube:** Data Processing en Render lee Supabase (`HISTORICAL_SOURCE=supabase`; clave `anon` como token de lectura, funciona por la RLS permisiva).
- **Carátula y cierre:** `herramientas_IA/video/portada_cierre.py caratula|cierre|unir` (el cierre calcula los minutos reales; `unir` recorta blancos iniciales y recodifica). Logo UC y NRC no incluidos (pendientes).

### Edición 10/11 noche (subtítulos)
- Corte 0:44,5–0:46,5 (se veía el chat) → `green-ai-unidad-III-cortado.mp4`; todos los minutos del guion −2 s desde 00:46.
- Guion §5 ampliado (colores de racks, suites, nueva respuesta de Ep. 5, tarjetas HU-03/HU-06, Ep. 7).
- Subtítulos: `python herramientas_IA/video/guion_a_srt.py docs/exposicion/GUION-VIDEO-UNIDAD-III.md exportados/video/green-ai-unidad-III.srt --fin 24:26`, luego `python herramientas_IA/video/srt_a_ass_apilado.py exportados/video/green-ai-unidad-III.srt exportados/video/sub.ass` (cada subtítulo dura al menos su tiempo de lectura, hasta 3 apilados con el más reciente abajo, caja semitransparente) e incrustado con ffmpeg `subtitles=sub.ass` sobre el cortado → `green-ai-unidad-III-subtitulado.mp4`. Si se cambia el guion, repetir ambos pasos.
- Pendiente: la diapositiva de cierre muestra minutos de indicadores con 2 s de más (no regrabada); filas antiguas 00:17, 00:54 y 01:00 tienen más texto que tiempo (subtítulos rápidos).
