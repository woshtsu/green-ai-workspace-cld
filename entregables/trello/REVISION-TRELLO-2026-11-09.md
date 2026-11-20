# Revisión del tablero Trello — 09/11/2026

- **Fuente:** export JSON del tablero `PL8uQ4rF` (descargado el 09/11; última acción `2026-11-10T00:26Z` = 09/11 19:26 hora de Lima). La copia anterior en `guias/trello/` es del 07/11 y está desactualizada.
- **Referencias:** `entregables/trello/GUIA-TRELLO-POR-INTEGRANTE.md` (en adelante «la guía»), prompt del docente, lista de cotejo U3 (ind. 4 y 11).
- **Regla:** solo cuenta lo que está en el JSON. Lo que no está, está pendiente. Hoy es el **Día 2**: los Días 3 (11/11) y 4 (13/11) todavía no tocan; se listan solo para planificar.

## 1. Validador (`herramientas_IA/trello/validar_trello.py`)

Resultado: **51 errores, 29 avisos**. Tarjetas completas: 15 de 65 (el validador cuenta 65; hay 68 abiertas).

| Tipo | Nº | Tarjetas |
|---|---|---|
| Falta fecha de vencimiento | 16 | HU-06, 07, 09, 10, 11, 12, 13, 14, 15, 16; RE-01…RE-06 |
| Dailies antiguos sin checklist y/o sin comentarios | 20 | «Daily \| Sprint [5]/[10] \| [12/10…23/10]» (5 fechas × 4 copias) |
| Daily 09/11 incompleto | 3 | 3 tarjetas «Daily Scrum — 2026-11-09»: sin checklist; una sin miembros ni comentarios |
| Reviews antiguas «Sprint 1…5» | 5 | sin fecha, sin miembros, sin comentarios; «Sprint 2» y «Sprint 5» con descripción de 11 caracteres |
| Reviews nuevas sin comentarios | 3 | Sprint Review — Sprint 2, 3 y 5 |
| PMV1 fuera de Done/Review/Retro | 1 | RE-01 y RE-02 en `3. REFINAMIENTO` (ver §4: la guía y el validador se contradicen) |

Avisos: 26 dailies con menos de 4 comentaristas; HU-01 y la tarea RLS sin movimientos entre listas; **participación baja**: Gina 479 acciones (66 %), Leonid 189 (26 %), Ricardo 41 (6 %), Jhonny 13 (2 %).

Lo que el validador **no** detecta y el docente sí verá: dailies duplicados por persona, reviews duplicadas («Sprint 1» vs «Sprint Review — Sprint 1»), etiquetas de PMV equivocadas, checklists sin marcar en DONE, saltos de lista (1→7) y fechas de cierre adelantadas.

## 2. Tablero frente a la guía, tarjeta por tarjeta

Leyenda: ✅ coincide con la guía · ❌ falta o está mal. «Desc. antigua» = no se pegó la ficha de la guía (no tiene DoD y casi siempre le faltan los Given/When/Then o la evidencia).

### Historias de usuario

| Tarjeta | Lista | Problemas |
|---|---|---|
| HU-01 | DONE ✅ | Sin movimientos (se creó directamente en DONE el 05/11). El resto ✅. |
| HU-02 | DONE ✅ | Completa ✅. |
| HU-15 | DONE ✅ | Etiqueta **PMV3** (debe ser PMV1 + Seguridad + Frontend); miembros solo Leonid (faltan Ricardo, Jhonny); sin fecha (03/10); movida 1→7→1→7 por Ricardo (la guía pide que Leonid la mueva paso a paso). |
| HU-03 | DONE ✅ | Nombre «**PMV1-HU-03**» (es PMV2; renombrar a «HU-03 …»). Falta el comentario de Jhonny como PO. |
| HU-04 | DONE ✅ | Salta QA (5→7). Solo comenta Gina. |
| HU-06 | DONE ✅ | Etiquetas: solo PMV2 (faltan Backend y ML); sin fecha (31/10); checklist **0/10** en DONE; desc. antigua; salta 4→7; falta el comentario de Jhonny como PO. |
| HU-08 | DONE ✅ | Salta 1→7 en una sola acción (la guía pide 1→2→4→5 el Día 1 y 5→6→7 el Día 2). |
| HU-12 | DONE ✅ | Etiqueta **PMV3** (debe ser PMV2 + Infraestructura + Backend); faltan miembros (Ricardo); sin fecha (14/11); checklist **0/10**; desc. antigua sin Given/When/Then; 1→7 directo, movida por Ricardo y no por Leonid. |
| HU-14 | DONE ✅ | Etiqueta **PMV1** (debe ser PMV2 + Seguridad + Backend); falta Jhonny; sin fecha (31/10); checklist **3/10**; desc. antigua; salta QA. |
| HU-11 | QA ✅ | Etiquetas PMV2 + **PMV3** (quitar PMV3; faltan Frontend e Infraestructura); faltan Jhonny y Ricardo; sin fecha; checklist 0/10; desc. antigua; 1→6 directo, movida por Ricardo. Leonid no ha comentado. |
| HU-05 | QA ✅ | Bien (4/6). Movimientos erráticos el mismo día (4→6→4→5→6). Solo comenta Gina. |
| HU-07 | IN PROGRESS ✅ | Etiquetas: solo PMV2 (faltan Backend y Seguridad); falta Jhonny; sin fecha (14/11); checklist 0/9 (la guía pide 2 ítems marcados); desc. antigua; salta TO DO (2→5). |
| HU-13 | IN PROGRESS ✅ | Etiqueta **PMV3** (debe ser PMV2 + Backend + Datos); falta Jhonny; sin fecha; checklist 0/10 (la guía pide 3 de 6 marcados); desc. antigua; 1→5 directo. |
| HU-09 | IN PROGRESS ✅ | Etiqueta **PMV3** (debe ser PMV2 + Backend + ML); faltan Gina y Leonid; sin fecha; checklist 0/10; desc. antigua; 1→5 directo. |
| HU-10 | **SPRINT BACKLOG** ❌ (va en PRODUCT BACKLOG) | Etiqueta PMV2 (debe ser PMV3 + ML + Datos); sin fecha (28/11); desc. antigua; el comentario de Gina dice «permanece en el PRODUCT BACKLOG», lo que contradice la lista donde está. Era tarea de Jhonny. |
| HU-16 | PRODUCT BACKLOG ✅ | Etiquetas: solo PMV3 (faltan Documentación y ML); miembros solo Leonid (deben ser los 4); sin fecha (12/12); checklist de 12 ítems (la guía pide 4–7); desc. antigua; Jhonny no ha comentado. |

### Tareas, sprints, refinamiento, reviews, retros, roles y dailies

| Tarjeta | Estado |
|---|---|
| Tarea «Fijar Health Check Path en Render» | ❌ **No existe** (Leonid, Día 1). |
| Tarea «Revisar RLS Supabase y password» | TO DO ✅; falta Jhonny; fecha 12/11 (la guía dice 11/11); la ruta `database/supabase-auth-setup.sql` no existe (ver §4). |
| Tarea «Evaluación walk-forward…» | TO DO ✅ completa. |
| Tarea «Grabar video de la Unidad III» | ❌ **No existe** (Jhonny, Día 2). |
| Sprint 6 / Sprint 7 | SPRINT BACKLOG ✅ completas. |
| RE-01 … RE-06 | Sin fecha; solo etiqueta de fase (faltan Arquitectura/Backend/Datos/ML/Documentación); **RE-03 con PMV2** (la guía dice PMV1); checklists 0/N sin marcar; RE-03, RE-04 y RE-06 con más de 7 ítems; solo comenta Gina; faltan los comentarios de Jhonny como PO en RE-04, RE-05 y RE-06. |
| «Sprint 1»…«Sprint 5» (Review antiguas) | ❌ **Duplicadas** de las «Sprint Review — Sprint N»: archivarlas. |
| Sprint Review — S1…S5 | Completas, con la leyenda de consolidación ✅. S2, S3 y S5 sin comentarios; faltan los comentarios de aceptación de Jhonny en S1–S3 (Día 1). S4 y S5 ya están hechas (eran del Día 3). |
| Sprint Review — Sprint 6 | Ya creada con checklist **5/5** y comentario de «resultados del Sprint 6» el 09/11, **antes de que termine el sprint** (14/11). |
| Retrospectiva — PMV1 | Completa ✅; solo comenta Gina. |
| Retrospectiva — PMV2 | Ya tiene el comentario «Cerramos la retrospectiva del PMV2» del 09/11, **antes del cierre** (era del Día 4). |
| PRODUCT OWNER | ❌ Sin etiqueta, sin fecha, sin checklist y sin comentarios (Jhonny, Día 1). |
| SCRUM MASTER | Completa ✅ (era del Día 3). |
| SCRUM TEAM | ❌ Sin etiqueta, sin checklist y sin comentarios; fecha 13/12 (la guía dice 12/12) (Leonid, Día 2). |
| 20 dailies «Daily \| Sprint [5]/[10] \| …» | ❌ Creados el 04–05/11 con fechas de octubre, 4 copias por fecha (una por persona), sin comentarios, «Sprint [10]» no existe, y fechas de vencimiento que no coinciden con el título (p. ej. vence 12/09 y el título dice 12/10). Es **el indicio de simulación más fuerte**. La guía (§1.2.4 y §2.2.5) pide archivarlos. |
| Daily Scrum — 2026-11-09 | ❌ **3 tarjetas** (con miembro Gina, con miembro Jhonny y sin miembros) en lugar de una. Han comentado Gina y Jhonny, cada uno en su tarjeta. **Ricardo y Leonid no han comentado.** |

### Tablero (configuración)

- Miembros de más: `UC_ES_TRELLO001` y `trello001`. La guía pide solo los 4 integrantes; **antes de quitarlos, confirmar que no sea la cuenta del docente**.
- La etiqueta «Infraestructura» está **duplicada**: dejar una.
- Las etiquetas de fase están mal en 9 HU (ver arriba), y por eso el validador cuenta PMV3 en IN PROGRESS y en DONE.

## 3. Pendientes por integrante (orden de prioridad, listo para enviar)

> Lo de los Días 1 y 2 está **vencido o es para hoy**. Lo de los Días 3 y 4 (11/11 y 13/11) se hace en su fecha. No crear ni retrofechar dailies pasados.

| Integrante | Pendientes concretos |
|---|---|
| **Gina Barrera (SM)** | 1. Daily 09/11: dejar **una sola** tarjeta con los 4 miembros y la fecha; archivar las otras 2 (Jhonny debe volver a publicar su comentario en la que quede). 2. Archivar los 20 dailies «Daily \| Sprint [5]/[10]» y las 5 reviews «Sprint 1…5» duplicadas. 3. Borrar la etiqueta «Infraestructura» duplicada; decidir con el docente sobre `UC_ES_TRELLO001`/`trello001`. 4. RE-01…RE-03: fecha, etiqueta técnica, RE-03 → PMV1, marcar checklist. 5. Corregir su comentario en HU-08 (`domain/constraints.py` no existe; ver §4). 6. Revisar «Sprint Review — Sprint 6» y «Retro PMV2»: desmarcar el checklist o dejar la tarjeta como «en curso» hasta el 13/11; el comentario de cierre se publica el Día 4. 7. Dejar de hacer las tareas de otros: el docente mide la autoría (66 % de las acciones son suyas). Día 3: HU-05 → comentario de Leonid. |
| **Ricardo Porras (Backend/DevOps)** | 1. **Hoy:** comentar el Daily 09/11 en la tarjeta única. 2. HU-06, HU-14 y HU-07: pegar la ficha de la guía, poner fechas y etiquetas correctas (HU-14 → PMV2), completar miembros y marcar el checklist (100 % en DONE; 2 ítems en HU-07). 3. HU-13 y HU-09: etiqueta PMV2 (no PMV3), miembros, fecha, ficha y checklist parcial. 4. Corregir sus comentarios con rutas o cifras inexistentes: HU-06 (`domain/policy_engine.py`), HU-09 (`domain/energy.py`), HU-14 («30/30 … 5 veces»), HU-03 («100 passed»), HU-15 (`handle_new_user`) (ver §4). 5. Tarea RLS: añadir a Jhonny, fecha 11/11 y corregir la ruta del SQL. 6. Subir su participación (6 %): moverse por su cuenta y dejar las tarjetas de Leonid (HU-11, HU-12, HU-15) para que las mueva Leonid. Día 3: Sprint Review S5 (ya creada por Gina: solo comentario de acuerdos). |
| **Leonid Huamán (Infra/Frontend)** | 1. **Hoy:** comentar el Daily 09/11. 2. Crear la tarea **«Fijar Health Check Path en Render»** en TO DO (vence 10/11; es del Día 1). 3. HU-15: etiquetas PMV1 + Seguridad + Frontend, miembros Ricardo y Jhonny, fecha 03/10. 4. HU-12: etiquetas PMV2 + Infraestructura + Backend, añadir a Ricardo, fecha, ficha, checklist al 100 % y comentario de promtool. 5. HU-11: quitar PMV3, poner Frontend e Infraestructura, miembros, fecha, ficha y comentario (48 pruebas en Node.js). 6. SCRUM TEAM: etiqueta, checklist, fecha 12/12 y comentario. Día 3: dejar 4 ítems marcados en HU-11 y comentar HU-05 y HU-09. |
| **Jhonny Quintana (PO)** | 1. **Hoy:** volver a publicar su comentario del Daily en la tarjeta única. 2. Crear la tarea **«Grabar video de la Unidad III»** en TO DO (Día 2). 3. PRODUCT OWNER: etiqueta, checklist, fecha 12/12 y comentario. 4. HU-10: moverla a PRODUCT BACKLOG, etiqueta PMV3 + ML + Datos, fecha 28/11, ficha y comentario. 5. HU-16: etiquetas, 4 miembros, fecha 12/12, ficha y comentario. 6. Comentarios de aceptación como PO en Sprint Review S1–S3, HU-03 y HU-06, y de seguimiento en RE-04…RE-06. 7. Su participación es del **2 %**: es el riesgo más alto de «trabajo no colaborativo». Día 3: comentar HU-11, HU-13 y HU-07. |

## 4. Contradicciones entre el tablero, la guía y el repo

1. **Rutas citadas que no existen en el repo** (vienen de la guía y se copiaron en Trello):
   - `domain/policy_engine.py` (comentario de Ricardo en HU-06) → lo real es `software/prediction/src/recommendations/policy.py` (+ `src/service/recommendations.py`).
   - `domain/constraints.py` (comentario de Gina en HU-08) → no existe; la política está en el mismo `policy.py`.
   - `domain/energy.py` (comentario de Ricardo en HU-09) → no existe; el trapecio está en Data Processing (`tests/test_historical_report.py`) y el panel en `software/frontend/energy.js`.
   - `database/supabase-auth-setup.sql` (HU-15 y tarea RLS) → lo real es `software/frontend/supabase-auth-setup.sql`.
   - `handle_new_user` (comentario en HU-15) → el trigger del repo se llama `on_auth_user_created_green_ai`.
2. **Cifras sin evidencia** en `docs/HANDOFF.md` ni en el repo: «112 passed» (Monitoring), «100 passed» (Prediction, HU-03), «30 passed / 30/30 con -race 5 veces» (HU-14; el gateway Go tiene 32 funciones `Test`). Sí constan: 114 y 121 passed (Data Processing), 2.85 GB → 510 MB, MAE 3.85 y 3.22, `SimulatorTelemetryDown` y el experimento MLflow `394141087236111562`. Hay que volver a ejecutar las pruebas y publicar la cifra real, o quitar la cifra.
3. **La guía contra el validador:** la guía pone RE-01…RE-03 como PMV1 en `3. REFINAMIENTO`, y el validador lo marca como error («PMV1 fuera de Done/Review/Retro»). Hay que decidir: o el validador acepta Refinamiento en PMV1 (es una lista sin flujo), o se acepta el error como conocido. No he cambiado el validador.
4. **La guía se contradice:** en la tabla maestra HU-12 va en DONE con fecha 14/11, pero el Día 1 la deja en IN PROGRESS. HU-08 aparece en PRODUCT BACKLOG el Día 1 pese a que su fecha es 31/10.
5. **Cierres adelantados:** el 09/11 ya hay Review S6 al 5/5 y la retro PMV2 «cerrada», con el sprint abierto hasta el 14/11. El prompt del docente busca justo esto («flujo artificial o decorativo»).
6. Los comentarios de Ricardo del 09/11 en hora de Lima figuran el 10/11 en UTC: es normal, no es un error.
7. Las fichas de la guía tienen checklists de 4–7 ítems, pero las tarjetas conservan los antiguos de 9–12: hay que reemplazarlos, no solo marcarlos.

## 5. Cómo se generó

```bash
python herramientas_IA/trello/validar_trello.py "<export>.json"   # exit 1: 51 errores, 29 avisos
```
El volcado por tarjeta (lista, etiquetas, miembros, fecha, checklist, movimientos y comentarios) se hizo con un script de solo lectura sobre el JSON. Las rutas se comprobaron con `git ls-files` y `git grep`. No se conectó con Trello.
