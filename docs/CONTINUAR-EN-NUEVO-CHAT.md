# Continuar en un chat nuevo (resumen al 2026-11-07, noche)

Lee primero `AGENTS.md`, `docs/HANDOFF.md` y este archivo. Rama de trabajo: **`test`** (publicada en `origin/test`). `main` no se tocó desde el retiro del workspace antiguo.

## Qué quedó hecho hoy
| Área | Estado | Dónde |
|---|---|---|
| Carpeta `entregables/` | Reorganizada: `informe-corregido/` (lo que se entrega: `informe-unidad-III.md`, `evidencias/`, `evidencias-nube/`, `cambios-tecnicos-a-reflejar.md`) y `trabajos-previos/` | `entregables/README.md` |
| Prediction ligera | Imagen 2,85 GB → 510 MB; RAM 174 → 122 MiB (una medición); 100 pruebas y smoke 14/14 | `docs/evidencias/prediction-imagen-ligera-20261107.md` |
| CI/CD | `.github/workflows/ci.yml` (pruebas por servicio, imágenes Docker) y `pages.yml` (main = raíz, test = `/dev/`) | `docs/GUIA-GITHUB-PAGES-Y-CI.md` |
| Render (cuenta personal, workspace «My Workspace») | 6 servicios gratuitos `green-ai-*-dev` en rama `test`: prediction, data-processing, gateway (Go), simulator, prometheus, monitoring. Auto-deploy apagado. No tocar `SoftwareAnemia` (otro proyecto) | `docs/GUIA-DESPLIEGUE-RENDER.md`, `docs/evidencias/render-desarrollo-20261107.md`, `render.yaml` |
| Frontend nuevo (rama `test`) | Dashboard en pestañas, gráfico media/máx/mín + comparación de 5 servidores, tabla paginada, ayuda «?», avisos de espera sin códigos, energía (simulador modelado / ejemplo / archivo), vista `flows.html` «Red de flujos» (propuesta ilustrativa), navegación común | `software/frontend/` (48 pruebas) |
| Evidencias | Capturas en `entregables/informe-corregido/evidencias-nube/` | |
| Mejora del modelo | Solo investigación y plan | `docs/MEJORA-MODELO-PREDICCION.md` |

URLs (desarrollo): Gateway `https://green-ai-gateway-dev.onrender.com`; frontend `https://woshtsu.github.io/green-ai-workspace-cld/dev/` (producción: raíz del mismo sitio, hoy usa el mismo Gateway). Los servicios gratuitos se duermen a los 15 min y pierden el historial (Simulator/Prometheus): **despertarlos ≥ 25 min antes de grabar el video**.

## Pendiente (en orden)
1. **Supabase (lo hace el dueño del proyecto):** añadir a *Authentication → URL Configuration* las URLs `https://woshtsu.github.io/green-ai-workspace-cld/` y `.../dev/`; aplicar el enum `VIEWER`; revisar RLS «Permitir todo» y la columna `password` en texto plano (ver «Riesgos» en `docs/HANDOFF.md`).
2. Fijar el *Health Check Path* en cada servicio de Render (Prediction `/health/ready`, Data Processing `/api/v1/health`, Gateway/Monitoring `/actuator/health`, Simulator `/health`, Prometheus `/-/healthy`).
3. Verificar con sesión real el frontend nuevo en `/dev/` (cada pestaña, «Predecir 15 min», energía con el simulador, `flows.html`) y tomar capturas para el informe. Lo verificado hasta ahora fue con un arnés local (`herramientas_IA/arnes_frontend/`) que simula la sesión y usa datos reales de Render.
4. Video (guion en `guias/semana12/lista-cotejo-unidad3.md`, líneas 41–61: 7 episodios, 20–30 min, con 500–1000 transacciones y entorno de calidad): preparar datos masivos y el episodio de métricas.
5. Informe `entregables/informe-corregido/informe-unidad-III.md`: corregir las cifras sin respaldo (XGBoost RMSE 7,1 %, 57,7 %, 45 ms, 18,4 %…; ver `docs/HANDOFF.md`) y reflejar los cambios técnicos de `cambios-tecnicos-a-reflejar.md`.
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
