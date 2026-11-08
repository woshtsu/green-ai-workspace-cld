# Política común de agentes — Green AI monorepo

Aplica a Claude Code, Antigravity CLI (`agy`, lee este archivo de forma nativa) y cualquier otro agente.
Contexto extenso y estado actual: [docs/HANDOFF.md](docs/HANDOFF.md). Léelo antes de trabajar.

## Repositorio
- Un único Git en esta carpeta. Prohibido crear Git anidados, submódulos o gitlinks (modo 160000).
- Ejecuta Git desde esta carpeta; comprueba `git rev-parse --show-toplevel`.
- El workspace antiguo se retiró; sus repos hijos se abandonaron y quedan solo en el zip del usuario.
- Ramas: `main` (producción) y `test` (desarrollo); ramas temporales → `test` → `main` con pruebas. Mismo código de adaptadores en todas; el entorno elige configuración.
- Sin push, publicación, cambios de producción, DNS o secretos remotos sin autorización explícita del usuario.

## Trabajo
- Incrementos pequeños y verificables. Traslados de carpetas y reescrituras en commits distintos.
- Arquitectura hexagonal real por servicio: dominio sin dependencias de adaptadores/infraestructura.
- Si cambia un contrato: migrar consumidores, pruebas, OpenAPI y documentación en el mismo incremento.
- Secretos solo por variables de entorno; versionar únicamente `.env.example` vacíos. Nada de secretos de servidor en el frontend.
- No convertir afirmaciones históricas sin evidencia en requisitos cumplidos (ver docs/HANDOFF.md, "Honestidad experimental").
- No declarar terminado lo que no se probó; registrar comandos, resultados y fallos en docs/HANDOFF.md.
- **Cierre de cada sesión (preferencia permanente del usuario, sin que lo pida):** antes de terminar, documentar lo hecho en `docs/HANDOFF.md` (cambios, pruebas con resultado, fallos) y actualizar `docs/CONTINUAR-EN-NUEVO-CHAT.md` (estado, URLs, pendientes en orden, cómo trabajar) para que otro chat pueda continuar sin contexto previo. Dejar evidencias (capturas, salidas) en `docs/evidencias/` y, si afectan al informe, en `entregables/informe-corregido/`. Commit local; el push solo con autorización.

## Graphify (índice de código)
- Grafo propio en `graphify-out/graph.json`. Antes de leer código, consulta: `graphify query "<pregunta>" --budget 1500`; usa `path` y `explain` para relaciones.
- Runtime local: ver [herramientas_IA/README.md](herramientas_IA/README.md). No instalar globalmente ni cambiar PATH.
- Tras modificar código: `graphify update .` (solo AST, sin coste de API). El grafo es un índice, no prueba de ejecución.

## Colaboración Claude ↔ Antigravity
- Claude coordina; delega con `herramientas_IA/agentes/agy_task.py` (ver su docstring). Cada encargo indica objetivo, archivos permitidos, restricciones, criterios de aceptación y formato de salida.
- Nunca dos agentes editando la misma rama/carpeta: usar `git worktree` por tarea con propiedad de archivos explícita.
- Prohibido `--dangerously-skip-permissions`, créditos de pago, pago por uso o proveedores API de respaldo. Ante cuota agotada: detenerse.
- Claude revisa diff, stdout/stderr, acciones denegadas y pruebas antes de integrar; `status: SUCCESS` no basta.

## Ahorro de tokens (preferencia permanente del usuario)
- Claude coordina y revisa; el trabajo pesado (lecturas amplias, redacción larga, refactors, pruebas repetitivas) se delega a Antigravity con `agy_task.py`, con Gemini Flash para encargos largos.
- Lo que no pueda hacer Antigravity va a subagentes con modelos baratos (`haiku` o `sonnet`); Claude Opus solo para decisiones, diseño y revisión final.
- Respuestas cortas; no releer archivos ya leídos; usar `graphify query` en vez de leer código.
