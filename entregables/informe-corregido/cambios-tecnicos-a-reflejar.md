# Reestructuración técnica (nov. 2026) y dónde reflejarla en las próximas entregas

El informe de las semanas 9–12 describe el sistema **antes** de esta reestructuración. Este archivo sirve para
redactar las semanas 13–16 (PMV3) sin inventar resultados. Para cada cambio se indica la sección de la consigna
(`guias/semana12/consigna-taller1-icacit.md`) donde es pertinente, la evidencia disponible y lo que falta.

| Cambio | ¿Relevante para la consigna? | Sección | Evidencia en el repo | Falta antes de declararlo |
|---|---|---|---|---|
| Repos Git anidados → **monorepo** con un solo Git, ramas `main` (prod) y `test` (desarrollo) | Sí: «gestión de cambios con acciones preventivas o correctivas» y «registro de decisiones y cambios» | VII Gestión del proyecto | `docs/DECISIONES.md` D-01..D-04, `docs/migracion/manifiesto-copia.json`, historial Git | Publicar el repositorio (destino por decidir) y retirar el workspace antiguo tras la lista de aceptación |
| Perfil **SQLite** de desarrollo con pruebas de contrato comunes con PostgreSQL/PostgREST | Sí | VI.2 Diseño de base de datos; VIII Pruebas | D-05; `software/data-processing/tests/test_historical_logs_contract.py` (114 pruebas con PostgREST) | Prueba contra un Supabase de pruebas. SQLite **no** aporta la evidencia de procedimientos almacenados del criterio 11 (eso sigue en Supabase) |
| **Gateway en Go** equivalente al Java (alternativa, no predeterminado) | Sí, si se adopta | V Herramientas modernas; VI.3 Arquitectura (vista de despliegue); VIII Pruebas | D-06; `docs/evidencias/gateway-go-difftest-20261106.txt` (0 diferencias en 39 casos; 16 MB frente a 520 MB; ~10 frente a ~290 MiB) | Decisión del equipo; actualizar `docs/exposicion` (defiende Spring Cloud Gateway); prueba con usuario real |
| Riesgo de **RLS permisiva** en Supabase (snapshot 2026-09-22) | Sí | III f. Salud, seguridad y riesgos; VII Registro de riesgos | `docs/HANDOFF.md` «Riesgos detectados» | Verificar el estado actual en Supabase y corregir las políticas |
| Smoke reproducible del stack (14/14) y pruebas por servicio en el monorepo | Sí | VIII Pruebas por PMV | `docs/evidencias/smoke-20261106.json`, `docs/HANDOFF.md` | Datos simulados: no prueban precisión ni ahorro |
| Claude Code + Antigravity CLI, Graphify | Opcional (proceso del equipo, no del producto) | V Herramientas modernas (uso de IA en el desarrollo) | `docs/TOOLS_EVALUATION.md` | Explicar sus límites: la revisión del agente se verificó a mano (7 de 8 hallazgos ciertos) |
| Despliegue de staging en Render desde la rama `test` (Gateway Go, Prediction, Data Processing) | Sí (Lab. 11, VI.3 vista de despliegue) | VI.3; VIII Pruebas con URL pública | D-07 (comparativa de proveedores con fuentes del 2026-11-06); `docs/GUIA-DESPLIEGUE-RENDER.md` | **No desplegado aún**: faltan URL pública, resultados de los `curl` de verificación y capturas. Registrar fallos de arranque en frío y memoria si ocurren |
| Adelgazar la imagen de Prediction (2,85 GB → solo dependencias de servicio, multi-etapa) | Sí (herramientas y consumo de recursos) | V; VIII | Análisis en `docs/academico/07-arquitectura-y-despliegue.md` §4 | **Implementado y medido el 2026-11-07**: 2,85 GB → 510 MB; 174 → 122 MiB en reposo (133–142 sin `PYTHONOPTIMIZE=2`) (una medición, sin carga); 100 pruebas y smoke 14/14. Evidencia: `docs/evidencias/prediction-imagen-ligera-20261107.md`. Falta probarlo en Render. Portar a Go descartado por ahora |

Cifras del informe 9–12 que **no** deben repetirse sin experimento: ver la advertencia en `entregables/README.md`.
