# Pasos para revisar y aprobar el PR del Sprint 7 (ola 2)

**PR:** https://github.com/woshtsu/green-ai-workspace-cld/pull/7 (`test` → `main`)
**Revisor asignado:** Jhonny (Product Owner). Si no puede, otro integrante distinto de Ricardo.
**Por qué:** la Definición de Terminado exige que otro integrante apruebe el PR antes de fusionar (criterio 3). El PR anterior (#6) se fusionó sin aprobación y el docente lo vería como incumplimiento.

## 0. Acceso (una sola vez)
- Necesitas una cuenta de GitHub con acceso al repositorio. Hoy solo tienen acceso `woshtsu` (Ricardo) y `reit-art`.
- Si tu cuenta no es una de esas, pásale tu usuario de GitHub a Ricardo para que te invite (Settings → Collaborators → Add people) y acepta la invitación desde el correo o desde https://github.com/notifications.

## 1. Abrir el PR
1. Entra a https://github.com/woshtsu/green-ai-workspace-cld/pull/7.
2. En la pestaña **Conversation** lee la descripción: qué cambia y cómo se probó.
3. Baja hasta el final y comprueba que los checks de **CI** están en verde (✔). Si alguno está en rojo, no apruebes y avisa a Ricardo.

## 2. Revisar los cambios
1. Abre la pestaña **Files changed**.
2. Revisa al menos estas partes (no hace falta entender cada línea; busca que lo descrito exista):
   - `docs/contratos/sprint7-ola2.md`: qué se prometió.
   - `software/frontend/dashboard.html` y `recommendations.js`: botones «Aprobar» y «Rechazar» y el texto «Registrar una decisión no ejecuta ningún cambio».
   - `software/prediction/src/decisions/`: el registro de decisiones.
   - `entregables/semana14/sprint7-ola2-implementacion.md`: resumen y capturas de las pruebas (492 aprobadas).
3. Si algo no te queda claro, deja un comentario en la línea (icono **+** al pasar el ratón) o en la pestaña Conversation.

## 3. Aprobar
1. Arriba a la derecha de **Files changed**, pulsa **Review changes** (o «Revisar cambios»).
2. Escribe un comentario breve, por ejemplo: «Revisado como Product Owner: los incrementos HU-07 y HU-13 coinciden con el contrato y las pruebas están en verde.»
3. Marca **Approve** y pulsa **Submit review**.
4. **No pulses «Merge»**: Ricardo fusiona después de configurar el secreto en Render.

## 4. Captura para el informe (la usaremos como evidencia C310)
- Cuando hayas aprobado, haz una captura de la pestaña **Conversation** donde se vea tu aprobación («approved these changes») y los checks en verde. Súbela al grupo o a la tarjeta de Trello del Sprint 7.
