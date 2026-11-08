# Lista de aceptación para retirar el workspace antiguo

El borrado es **irreversible**. Lo ejecuta el usuario, o Claude con confirmación explícita, solo con todas las
casillas marcadas.

## A. Respaldo (antes de nada)
- [x] **Zip completo** (hecho por el usuario) de `green-ai-workspace` fuera de esa carpeta. Incluye los `.git` de los 9 repos hijos,
  `output/` (docx, pdf, `git-backup/*.bundle`, `green-ai-portable` de 3,3 GB), `GreenAi_TPI`,
  `Consigna-Taller1-Actualizado-Icacit-English.docx` y `project-docs/*.pdf`.
- [x] Repos hijos abandonados por decisión del usuario (2026-11-06): sus commits quedan solo en el zip.

## B. El monorepo es autosuficiente
- [x] Código de los 6 servicios + infraestructura (`software/`), con pruebas en verde (ver HANDOFF).
- [x] Material importado: `docs/exposicion` (guía de exposición), `docs/historico/` (project-docs, semana10,
  traspaso, entrega Prometheus), `entregables/trabajos-previos/evidencias-del-sistema/` (capturas y Supabase), guías,
  trabajos y artículos.
- [ ] Rutas a `../` actualizadas en la documentación vigente (encargo 08 de Antigravity, en revisión).
- [ ] Graphify instalado en el propio monorepo: `.\herramientas_IA\instalar-graphify.ps1` (hoy usa `..\.tools`).
- [ ] `config.local.js` del frontend y los `.env` locales recreados desde los ejemplos tras mover la carpeta
  (están ignorados por Git).

## C. Copia remota del monorepo
- [x] Repositorio **público** (requisito del docente): https://github.com/woshtsu/green-ai-workspace-cld. Antes del primer push se eliminaron del historial `guias/articulos/` (solo queda el índice) y los grafos antiguos; respaldo previo en `../green-ai-monorepo-antes-de-limpiar.bundle`.
- [x] `git push` de `main` y `test` (2026-11-06).

## D. Mover y limpiar
Script: `herramientas_IA/retirar-workspace.ps1` (mueve a `..green-ai`, instala Graphify y pide escribir BORRAR) (ejecutarlo con esta app cerrada). Al mover la carpeta se conservan
`config.local.js` y los `.env` ignorados, así que no hay que recrearlos.
- [ ] Mover `green-ai-monorepo` fuera, p. ej. a `C:\Practicas\202620\TallerProyectos\green-ai` (no hay rutas
  absolutas en el código; Docker Compose usa rutas relativas).
- [ ] Detener los contenedores del stack antiguo si los hubiera (`docker compose -p green-ai-workspace down`, sin `-v`).
- [ ] Borrar las carpetas sobrantes de worktrees: `green-ai-monorepo-wt-agy`, `-wt-agy2`, `-wt-rutas`.
- [ ] Solo entonces, borrar `green-ai-workspace`.
