# Delegación del Sprint 7 (19/11 – 23/11/2026)

Ricardo ya implementó la ola 2 y abrió el PR #7. Estas tareas son para **Gina, Leonid y Jhonny**. Cada uno hace la suya **desde su propia cuenta** (Trello y GitHub), para que conste su autoría. Fechas reales: no se registra nada con fecha atrasada.

Lectura previa (5 min): [resumen de la ola 2](sprint7-ola2-implementacion.md) y [reporte ICACIT](reporte-icacit.md).

## Estado del gateway (Cloudflare)
El 19/11/2026 el gateway en Render respondía con normalidad: `/actuator/health` → 200, una ruta de API sin token → 401 (lo esperado) y CORS → 200. No hay bloqueo de Cloudflare activo; el de semana 13 fue temporal, durante las pruebas de carga. **No hay que crear un gateway nuevo.** Si al validar (tarea de Leonid) aparece una página de Cloudflare o un error 403/429, haz una captura y avisa a Ricardo.

---

## Jhonny — Product Owner (hasta el 20/11)
1. **Revisar y aprobar el PR #7** siguiendo [pasos-revision-pr-ola2.md](pasos-revision-pr-ola2.md). No fusionar.
2. Captura de la aprobación (evidencia C310 del informe).
3. En Trello, tarjeta «Sprint 7»: comentario de aceptación del incremento como Product Owner (qué historias se aceptan: HU-07 y HU-13, con el enlace al PR).

## Leonid — Infraestructura y Frontend (después del despliegue, avisará Ricardo)
Validación con sesión real en `/dev/` (F-03) y accesibilidad (U-02). Para cada punto, **captura de pantalla real**, sin que se vean contraseñas ni tokens.
1. Abre https://woshtsu.github.io/green-ai-workspace-cld/dev/ e inicia sesión con tu cuenta (rol OPERATOR).
2. Dashboard: recorre las 5 pestañas. En «Resumen», abre «Ver datos en tabla» bajo el gráfico → captura.
3. «Predicción y recomendación»: «Usar valores de ejemplo» → «Evaluar recomendación» → escribe un comentario → «Aprobar». Debe aparecer en la lista de decisiones → captura. Pulsa «Aprobar» otra vez: debe salir un aviso de que ya decidiste (409) → captura.
4. «Reportes y experimento»: HW045, 10/07/2026 a 11/07/2026 → «Descargar PDF». Abre el PDF y comprueba que dice «Datos simulados; energía modelada, no medida» → captura del PDF abierto.
5. Pestaña «Energía y CO₂e»: comprueba que dice «modelada/estimada» → captura.
6. Accesibilidad: en Chrome, F12 → pestaña **Lighthouse** → solo «Accessibility» → «Analyze page load» sobre el dashboard → captura del puntaje y de los avisos.
7. Si tienes una cuenta VIEWER (o Ricardo te la asigna): comprueba que no aparecen los botones Aprobar/Rechazar → captura.
8. Sube las capturas al grupo o a la tarjeta de Trello «PMV3 — Validación /dev/». Ricardo las inserta en el informe.

## Gina — Scrum Master (desde hoy hasta el 23/11)
1. **Trello, tarjetas del Sprint 7** (cada una con miembro único, fecha y DoD):
   - `PMV2-HU07: Aprobación humana persistente` → mover a QA-TESTING (miembro: Ricardo).
   - `PMV2-HU13: Reporte histórico en PDF` → QA-TESTING (miembro: Ricardo).
   - `PMV3 — Validación /dev/ y accesibilidad` → IN PROGRESS (miembro: Leonid).
   - `PMV3 — Revisión del PR #7` → IN PROGRESS (miembro: Jhonny).
   - Cuando Leonid y Jhonny terminen, mover a DONE con su comentario.
2. **Daily Scrum:** crear una tarjeta por día (20/11, 21/11, 23/11) en la lista 9. DAILY SCRUM; cada integrante comenta **ese mismo día** desde su cuenta (qué hice, qué haré, impedimentos).
3. **Sprint Review y Retrospectiva del Sprint 7** el 23/11: tarjetas en las listas 10 y 11 con lo entregado (ver [resumen de la ola 2](sprint7-ola2-implementacion.md)) y lo pendiente (RLS de Supabase, carga en staging).
4. Captura del tablero completo al cierre del 23/11 (evidencia para el informe final).

---

## Lo que hace Ricardo (no delegado)
- Configurar `GATEWAY_SHARED_SECRET` en Render, fusionar el PR #7 cuando Jhonny apruebe y avisar a Leonid del despliegue.
- Supabase: eliminar la contraseña en texto plano de la tabla `usuario` y revisar RLS.
