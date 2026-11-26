# Continuar en un chat nuevo (resumen al 2026-11-26)

## EMPEZAR AQUÍ (26/11/2026)
- Rama **`test`**, publicada en `origin/test` (push autorizado el 26/11). `main` sin tocar: no abrir PR ni fusionar sin autorización.
- Lista de trabajo con casillas: **[CHECKLIST-OBSERVACIONES-2026-11-26.md](CHECKLIST-OBSERVACIONES-2026-11-26.md)** (seguirla en orden; primero el dataset, y la imagen del MVP en el póster que pidió el docente).
- Hecho: informe U-IV `.md` corregido, wireframes, factores ponderados, póster según plantilla y sílabo, reporte ICACIT reevaluado (`entregables/semana15/reporte-icacit.md`). Sin reexportar Word/PDF del informe.
- Auditorías de apoyo: `docs/evidencias/auditoria-20261126/`. Póster: `bash herramientas_IA/exportacion/render_poster.sh`.
- Entrega aproximada: primera semana de diciembre; la revisión del póster era el 26/11.
- Trabajo: Claude coordina y delega en subagentes baratos (ahorro de tokens); preguntar antes de corregir si algo no está claro.

Lo que sigue más abajo es historial.

Lee primero `AGENTS.md`, `docs/HANDOFF.md` y este archivo. Rama de trabajo: **`test`** (publicada en `origin/test`). `main` no se tocó desde el retiro del workspace antiguo.

## Lo nuevo de la semana 13 (2026-11-07, tarde) — leer primero
| Qué | Dónde | Estado |
|---|---|---|
| Informe corregido (Word) | `entregables/informe-corregido/informe-unidad-III.md` → `exportados/semana13/…-informe-unidad-III-CORREGIDO.docx` | Listo para revisión del equipo; faltan 15 capturas, NRC y URL del video |
| Documento semana 13 (Word) | `entregables/semana13/semana13-calidad-furps-owasp.md` → `exportados/semana13/…-semana13-calidad-FURPS-OWASP.docx` + `MODELO-FURPSPLUS-Green-AI.xlsx` | Listo para revisión; faltan 11 capturas y NRC |
| Auditorías FURPS+/OWASP 01–07 | `docs/calidad/` | Ola 1 implementada (commit `d24d86f`); olas 2–3 planificadas (17/11–12/12) |
| Capturas por integrante | `entregables/CAPTURAS-PENDIENTES.md` | Por hacer (equipo) |
| Trello | `entregables/trello/GUIA-TRELLO-POR-INTEGRANTE.md` + `herramientas_IA/trello/validar_trello.py` | Días 1–4 (07/11–13/11) por hacer, cada uno con su cuenta; luego exportar JSON y validar |
| Video | `entregables/video/GUION-VIDEO-UNIDAD-III.md` + `herramientas_IA/video/grabar_episodios.py` | **Video completo sin voz** `exportados/video/green-ai-unidad-III.mp4` (24:28; carátula + 7 episodios + cierre; no versionado) + `descripcion-youtube.txt`. Falta: voces y cámaras de los 4 encima, subir no listado y poner la URL |
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

## 2026-11-11 (noche): carpetas del equipo
Solo `guias/` (docente), `entregables/` (fuentes .md) y `exportados/` (Word/Excel versionados). Informe: PMV3 = procesos de software (17/11–30/11); faltan capturas C100–C313, NRC y URL del video. Ver HANDOFF.

## 2026-11-12 (noche): semana 13 migrada a OWASP Top 10:2025
Entregable de semana 13 (.md, .docx y .xlsx) reclasificado a OWASP Top 10:2025; clasificación vigente y puntajes en `docs/calidad/08_reclasificacion_owasp_2025.md` (04–07 quedan como histórico 2021). Nuevo hallazgo OW-13 (A10:2025, ola 3). El informe corregido de la Unidad III no se tocó. Ver HANDOFF.
Roles del §4.3 alineados con el acta; responsables OWASP iguales en Word y Excel; reparto de revisión en `entregables/semana13/REVISION-POR-INTEGRANTE.md` (falta que cada integrante confirme). Los documentos `docs/calidad/01–08` se quedan en `docs/calidad/` (decisión del usuario).

## Pendiente (en orden)
- **Semana 13:** entregada el 12/11 (Word, PDF y Excel en `exportados/semana13/`, etiqueta `semana13-entrega`). Solo si el docente lo pide: capturas S44 (rol VIEWER) y S50a–S50d (pruebas de backend).
0. **OW-13 (A10:2025, ola 3, hasta 30/11):** recover con problem+json en gateway-go, manejador global en el Gateway Spring, pruebas de cuerpos 500 genéricos y timeouts uniformes en el frontend (`docs/calidad/08_reclasificacion_owasp_2025.md` §4.3).
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
- Subtítulos: `python herramientas_IA/video/guion_a_srt.py entregables/video/GUION-VIDEO-UNIDAD-III.md exportados/video/green-ai-unidad-III.srt --fin 24:26`, luego `python herramientas_IA/video/srt_a_ass_apilado.py exportados/video/green-ai-unidad-III.srt exportados/video/sub.ass` (cada subtítulo dura al menos su tiempo de lectura, hasta 3 apilados con el más reciente abajo, caja semitransparente) e incrustado con ffmpeg `subtitles=sub.ass` sobre el cortado → `green-ai-unidad-III-subtitulado.mp4`. Si se cambia el guion, repetir ambos pasos.
- Pendiente: la diapositiva de cierre muestra minutos de indicadores con 2 s de más (no regrabada); filas antiguas 00:17, 00:54 y 01:00 tienen más texto que tiempo (subtítulos rápidos).

### Estado 12/11/2026 (madrugada)
- PR #6 abierto (Sprint 7, tarea 7.2, rama `sprint7/7.2-proceso-pr` → `test`) para la captura C310: falta CI verde y aprobación de otro integrante.
- Logo C100/S00: confirmar con el usuario dónde lo dejó antes de reexportar (no reexportar con el Word abierto).
- Marcadores pendientes: informe C100, C203, C204, C310, C312, C313; semana 13 S00, S04, S07, S08.

### Estado 15/11/2026
- Evidencias: solo capturas reales. Usar `herramientas_IA/capturas/captura_ventana.ps1` (consola real), nunca `terminal_a_png.py` para entregables.
- Informe corregido: 123 páginas, cifras verificadas con capturas del 15/11 (435 pruebas). Pendiente de visto bueno del equipo y push.
- Pendientes de captura: consola DevTools (S08), latencias locales y cold start de semana 13.

### Estado 19/11/2026 (Sprint 7)
- Ola 2 implementada e integrada en `test` (HU-07 decisiones, HU-13 PDF, U-02, F-06, S-01; F-04 y P-01 documentados). 492 pruebas aprobadas con capturas reales.
- Resumen para el equipo: `entregables/semana14/sprint7-ola2-implementacion.md`; reporte ICACIT: `entregables/semana14/reporte-icacit.md`.
- Siguiente: autorización para desplegar (test → main, `GATEWAY_SHARED_SECRET` en Render), F-01 RLS, F-03 sesión real, informe final (Sprint 8, aplicar mejoras del reporte ICACIT).

### Estado 26/11/2026 — levantamiento de observaciones (entrega en ~1 semana)
Decisiones del usuario:
- Informe: por ahora solo cambios en `entregables/` (.md), sin reexportar. El póster nuevo se revisa el 26/11: guía en `guias/semana15-16/plantillas-poster/`.
- Referencias solo al final. Factores ponderados para **todas** las herramientas (Claude redacta, equipo valida).
- Cap. VI (ingeniería): wireframes explicados en vez de capturas de la app; prototipos por PMV (wireframes) tras cada flujo; capturas reales solo en pruebas.
- 4 conclusiones, una por objetivo específico (sin conclusión aparte del general).
- Discusión de pruebas y resultados respecto a los entregables, **en párrafos** (no tablas).
- FURPS+/OWASP oficial: semana 13 (86 %, OWASP 83,5, apto) más correcciones posteriores. El equipo informa que la columna `password` ya se corrigió (falta evidencia).
- ICACIT: el docente lo evalúa con NotebookLM (prompt no revelado); mejorar el informe/reporte y volver a ejecutarlo.

Avance 26/11 (tarde): informe `.md` corregido (ahora es la fuente de verdad; el script exige `--forzar`), póster ajustado al sílabo. Siguiente: revisión del equipo (póster hoy), validar factores ponderados, mejorar y volver a ejecutar el ICACIT, y solo entonces reexportar Word/PDF. Dudas abiertas al final de `docs/HANDOFF.md`.

**Anotado para hacer después (desde otra PC):**
1. Recapturar las evidencias mostrando el link (lista: auditoría del 26/11; Cap. VI Fig. 2–4, 6, 8, 9; Trello VII.6.3–6.9; Cap. VIII; Anexo A.2–A.9) y tapar las contraseñas de la Fig. VIII.13 y Anexo B.
2. Actualizar % de avance del PMV y Gantt ejecutado (corte actual 11/11: PMV1 13/13, PMV2 8/13, PMV3 0/14); confirmar tareas de Sprints 7–8 y Trello. Corregir la tarea «Cluster Kubernetes desplegado» marcada como completada.
3. Programar el adaptador Supabase para las decisiones HU-07 (hoy solo `software/prediction/src/decisions/adapters/sqlite_repository.py` y la migración `001_recommendation_decisions.sql` sin aplicar), con pruebas. Mientras tanto, en anexos enlazar los adaptadores existentes (Supabase y SQLite de históricos en `software/data-processing/infrastructure/adapters/input/`, SQLite de decisiones) y declarar este pendiente.
4. Validación con usuarios finales: **sigue declarada como pendiente** en el informe (decisión del usuario, 26/11). La consulta con el experto (Fig. A.1) no se presenta como acta; revisar su pie, porque la imagen es una foto y no un formulario.

### Estado 25/11/2026 (noche) — entrega S15 generada
- Informe final: `exportados/semana15/Porras-Huaman-Barrera-Quintana-informe-unidad-IV.pdf` (129 págs.), fuente `entregables/semana15/informe-unidad-IV.md`, regenerable con `herramientas_IA/exportacion/construir_informe_iv.py` + `md_a_docx.py` + `actualizar_word.ps1` + Word COM.
- Póster: `exportados/semana15/poster-green-ai.pdf` / `.png`, fuente `entregables/semana15/poster/poster-green-ai.html`.
- Congreso: informe `exportados/semana15/Porras-Huaman-Barrera-Quintana-informe-congreso.pdf`, resumen para el equipo `exportados/semana15/resumen-hallazgo-congreso-equipo.pdf`; CHG-001-2026 aprobado, no implementado (§VII.8 del informe final, ahora 136 págs.).
- Pendientes en orden: 1) acta de usuarios finales (§VIII.2.3 dice que no hay); 2) F-01 RLS y columna `password` en Supabase; 3) F-03 sesión real; 4) migración de decisiones HU-07 a Supabase; 5) QR en el póster (falta paquete qrcode).

### Estado 25/11/2026 (tarde) — para el chat del entregable S15
- Ola 2 desplegada en Render (gateway Go, prediction y data-processing en `c807af9`, servicios en rama `test` con autoDeploy OFF → desplegar manualmente). `GATEWAY_SHARED_SECRET` configurado por el usuario. PDF y decisiones verificados (curl y logs de Render).
- PR #7 aprobado por CristhianQuintana (Jhonny) y fusionado en main (51234b4). Evidencia C310 actualizada en el informe corregido (124 páginas).
- Pruebas al 19/11: 492 aprobadas (capturas `entregables/informe-corregido/evidencias-nube/captura-S7-*.png`).
- Entrega S15 (cierre 25/11/2026 23:59): informe final PDF `Porras-Huaman-Barrera-Quintana-informe-unidad-IV.pdf`, video en anexo (enlace Drive, no se sube), póster. Ver prompt del usuario.
