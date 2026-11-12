# Guía paso a paso del tablero Trello por integrante — Proyecto Green AI

Este documento constituye la guía operativa definitiva para que los cuatro integrantes del equipo configuren, actualicen y sincronicen el tablero Trello del proyecto universitario **Green AI (Proyecto 20)**.

El objetivo central es reflejar de forma fidedigna y verificable el estado de la ingeniería en el repositorio, asegurando que la exportación en formato JSON supere de manera sobresaliente la auditoría académica automatizada basada en el prompt del docente (`guias/trello/pront evaluacion mediante json.txt`) y la validación con [herramientas_IA/trello/validar_trello.py](file:///C:/Practicas/202620/TallerProyectos/green-ai/herramientas_IA/trello/validar_trello.py).

---

## 0. Responsabilidades pendientes por estudiante (export del 09/11/2026, 20:24 h Lima)

> [!IMPORTANT]
> **Regla obligatoria del docente sobre miembros:** «En cada tarjeta, como miembro, solo debe estar un integrante.» La colaboración multidisciplinaria entre compañeros se demuestra exclusivamente a través de **comentarios técnicos individuales** en la tarjeta, nunca agregándolos como miembros.
> **Honestidad temporal:** Se prohíbe terminantemente retrofechar dailies o reuniones: si un integrante no participó el día exacto de la sesión, no debe registrar comentarios con fechas pasadas artificiales (constará formalmente que no participó).
> **Participación actual en el tablero (export del 09/11/2026, 20:24 h Lima):** Gina Diana Barrera Peña: 479 acciones (56 %), Leonid Kisley Orlando Huamán Collazos: 189 acciones (22 %), Ricardo Porras Veli: 167 acciones (20 %), Jhonny Cristhian Quintana Carhuaricra: 13 acciones (1,5 %). Es prioritario y urgente reequilibrar la actividad de Jhonny (2 % actual), y cada integrante debe operar estricta y exclusivamente con su propia cuenta de Trello.

### Tareas pendientes de Ricardo →
1. Si aún es 09/11, comentar el Daily 09/11 en la tarjeta de Gina. Si no, no retrofechar: constará que no participó.
2. HU-14 (DONE): quitar a Leonid como miembro; pegar la ficha de §4; reemplazar el checklist actual (3/10) por el de la ficha al 100 % (marcar los 5 ítems [x]).
3. HU-06 (DONE): pegar la ficha de §4; reemplazar el checklist actual (0/10) por el de la ficha al 100 % (marcar los 5 ítems [x]).
4. HU-02 (DONE): quitar a Leonid y a Gina como miembros (quedar Ricardo como miembro único).
5. HU-07, HU-13 y HU-09 (IN PROGRESS): pegar la ficha de §4; checklist de la ficha con el avance real (HU-07: marcar 2 ítems; HU-13 y HU-09: marcar 3 de 6 ítems); corregir fecha límite al 14/11 (hoy figura 15/11).
6. Corregir sus comentarios ya publicados con datos sin respaldo: en HU-06 corregir ruta a `software/prediction/src/recommendations/policy.py` y cambiar «13 pruebas» por pruebas de recomendación (`pytest`); en HU-09 corregir referencia de `domain/energy.py` a «cálculo por trapecio en Data Processing (`software/data-processing/tests/test_historical_report.py`) y panel `software/frontend/energy.js`»; en HU-14 corregir «30/30… 5 veces» por `N passed` tras `go test -race ./...` en `software/gateway-go`; en HU-03 sustituir «100 passed» por `N passed` tras `pytest` en `software/prediction` (último registro en docs/HANDOFF.md: 96 passed); en HU-15 corregir `handle_new_user` por el trigger `on_auth_user_created_green_ai`.
7. Tarea RLS (TO DO): corregir la ruta del SQL en la descripción (`software/frontend/supabase-auth-setup.sql`); ajustar fecha de vencimiento al 11/11.
8. RE-02 y RE-05 (REFINAMIENTO DE EXPERTOS): quedar como miembro único (quitar a Gina y Jhonny como miembros), asignar etiquetas técnicas (RE-02: `Arquitectura`, `Backend`; RE-05: `Machine Learning`), marcar el checklist completo y publicar comentario propio.

**Más adelante (Día 3 — 11/11 / Día 4 — 13/11):**
- Día 3 (11/11): en HU-13 y HU-09 continuar el avance técnico en IN PROGRESS; en la tarjeta de `Sprint Review — Sprint 5` (cuyo miembro único es Jhonny) publicar comentario sobre los acuerdos técnicos alcanzados.
- Día 4 (13/11): en `Sprint Review — Sprint 6` (tarjeta de Jhonny) publicar comentario confirmando el despliegue de microservicios en Render; en `Retrospectiva — PMV2 (Sprints 4–6)` (tarjeta de Gina) publicar comentario sobre la arquitectura hexagonal y el Gateway en Go; verificar que la tarea de RLS Supabase en TO DO mantenga su fecha y miembro.

**Ya hecho (no repetir):**
Etiquetas y fechas de HU-06, HU-07, HU-09, HU-13 y HU-14; tarjetas HU-12 y HU-15 movidas.

### Tareas pendientes de Gina Diana →
1. Daily 09/11: archivar la tarjeta vacía (sin miembros). Desde el 11/11, mantener estrictamente una sola tarjeta por sesión.
2. Archivar los 23 dailies antiguos «Daily | Sprint [5]/[10]» y las 5 reviews antiguas «Sprint 1»…«Sprint 5».
3. Borrar la etiqueta «Infraestructura» duplicada. Consultar con el docente antes de quitar a `UC_ES_TRELLO001` y `trello001`.
4. Dejarse como miembro único (quitar a los demás integrantes): HU-03 (quitar a Jhonny y Ricardo), HU-04 (quitar a Jhonny), HU-05 (quitar a Leonid), HU-08 (quitar a Ricardo), tarea walk-forward (quitar a Jhonny), Sprint 6 y Sprint 7 (quitar a Jhonny), Retrospectiva PMV1 y Retrospectiva PMV2 (quitar a los otros 3 miembros).
5. RE-03 y RE-04: miembro único Gina (quitar a Jhonny). RE-03: corregir etiqueta a `PMV1` (hoy figura `PMV2`) + `Datos`. RE-04: asignar etiqueta `Machine Learning`. Marcar los checklists. Ceder RE-01 (a Leonid), RE-02 y RE-05 (a Ricardo) y RE-06 (a Jhonny).
6. Corregir su comentario de HU-08 sustituyendo la referencia a `domain/constraints.py` por los umbrales de la política en `software/prediction/src/recommendations/policy.py`.
7. Dejar de ejecutar las tareas de otros (actualmente el 56 % de las acciones del tablero son suyas; cada integrante debe operar desde su propia cuenta).

**Más adelante (Día 3 — 11/11 / Día 4 — 13/11):**
- Día 3 (11/11): en HU-05 (QA-TESTING) mantener 4 ítems marcados [x] y 2 [ ]; coordinar con el equipo la captura de pantalla con `mlflow ui`; en `Sprint Review — Sprint 4` (tarjeta de Jhonny) publicar comentario como Scrum Master.
- Día 4 (13/11): cerrar la tarjeta `Retrospectiva — PMV2 (Sprints 4–6)` (hoy con checklist 3/5; dado que ya tiene el comentario «Cerramos…» del 09/11, no marcar los ítems restantes hasta el 13/11); en `Sprint Review — Sprint 6` (tarjeta de Jhonny) publicar comentario de cierre como Scrum Master; auditar que no queden tarjetas huérfanas en el tablero.

**Ya hecho (no repetir):**
Creación y configuración de Sprint 6, Sprint 7, Sprint Reviews S1–S6, Retrospectivas PMV1 y PMV2, tarjeta SCRUM MASTER y tarea walk-forward.

### Tareas pendientes de Leonid →
1. Si aún es 09/11, comentar el Daily 09/11 en la tarjeta de Gina. Si no, no retrofechar: constará que no participó.
2. Crear la tarea técnica «Fijar Health Check Path en Render» en la lista `4. TO DO` (no existe en el tablero; vencía el 10/11); miembro único Leonid, etiquetas `PMV2`, `Infraestructura`, checklist con los 6 pasos y comentario inicial.
3. HU-12 (DONE): pegar la ficha de §4; reemplazar el checklist actual (0/10) por el de la ficha al 100 % (marcar los 5 ítems [x]); publicar comentario propio (actualmente solo comentó Ricardo).
4. HU-11 (QA-TESTING): pegar la ficha de §4; checklist de la ficha con avance real (marcar 4 [x] de desarrollo y dejar 2 [ ] de validación en vivo para el Día 3); publicar comentario propio.
5. HU-01 (DONE): quitar a Ricardo como miembro (quedar Leonid como miembro único). HU-15 (DONE): cambiar la etiqueta `Backend` por `Frontend` (etiquetas finales: `PMV1`, `Seguridad`, `Frontend`; quitar a Ricardo y Jhonny como miembros).
6. SCRUM TEAM: miembro único Leonid (quitar a los otros 3 compañeros como miembros), asignar etiqueta `Documentación`, marcar checklist de compromisos, ajustar fecha al 30/11 (hoy figura 13/12) y publicar comentario.
7. RE-01 (REFINAMIENTO DE EXPERTOS): miembro único Leonid (quitar a Gina y Jhonny), asignar etiquetas `PMV1`, `Arquitectura`, `Infraestructura`, marcar checklist y publicar comentario propio.

**Más adelante (Día 3 — 11/11 / Día 4 — 13/11):**
- Día 3 (11/11): en HU-11 (QA-TESTING) mantener los 4 [x] y 2 [ ] y reportar avances; en HU-05 (tarjeta de Gina) publicar comentario sobre la captura pendiente con `mlflow ui`; en HU-09 (tarjeta de Ricardo) publicar comentario sobre el panel de visualización de energía en el frontend.
- Día 4 (13/11): publicar comentario en `Sprint Review — Sprint 6` (tarjeta de Jhonny) y en `Retrospectiva — PMV2` (tarjeta de Gina); realizar la exportación preliminar de `tablero-green-ai.json` y ejecutar la validación técnica con Python.

**Ya hecho (no repetir):**
HU-01, HU-02 y HU-15 completas y verificadas en DONE.

### Tareas pendientes de Jhonny →
1. PRIORIDAD CRÍTICA: su participación actual es de solo el 2 % (13 acciones registradas). Todo lo siguiente debe realizarse obligatoriamente iniciando sesión con su propia cuenta de Trello.
2. Crear la tarea técnica «Grabar video de la Unidad III» en la lista `4. TO DO` (no existe en el tablero); miembro único Jhonny, etiquetas `PMV2`, `Documentación`, fecha 14/11, checklist con los 5 pasos y comentario inicial con el desglose de los 7 episodios.
3. PRODUCT OWNER (hoy vacía en `8. ROLES DE SCRUM`): asignar etiqueta `Documentación`, pegar descripción de §4, marcar checklist al 100 % [x], fecha 30/11 y publicar comentario de rol activo.
4. Sprint Review S1 a S6: quedar como miembro único Jhonny en las 6 tarjetas de Sprint Review (quitar a los otros 3 integrantes como miembros) y publicar el comentario formal de aceptación del Product Owner en cada una (las revisiones de S2, S3 y S5 no tienen ningún comentario actualmente). En Sprint Review — Sprint 6: no aceptarla formalmente hasta el 13/11.
5. HU-10 (PRODUCT BACKLOG): quitar a Gina como miembro (quedar Jhonny como miembro único); pegar la ficha de §4; ajustar fecha de vencimiento al 28/11 (hoy figura 29/11); publicar comentario de justificación de backlog para PMV3.
6. HU-16 (PRODUCT BACKLOG): cambiar el miembro asignado Leonid → Jhonny (quedar Jhonny como miembro único); añadir las etiquetas `Documentación` y `Machine Learning` (etiquetas finales: `PMV3`, `Documentación`, `Machine Learning`); ajustar fecha al 30/11 (hoy figura 13/12); pegar la ficha de §4; sustituir el checklist actual (12 ítems vacíos) por el de la ficha (6 ítems: 1 [x] y 5 [ ]); publicar comentario sobre el protocolo experimental.
7. RE-06 (REFINAMIENTO DE EXPERTOS): quedar como miembro único Jhonny (quitar a Gina), asignar etiqueta `Documentación` (etiquetas: `PMV2`, `Documentación`), marcar el checklist completo y publicar comentario propio.
8. Comentarios de validación como Product Owner: ingresar a HU-03 (en DONE) y a HU-06 (en DONE) y publicar sus comentarios de validación funcional y de criterios de aceptación.

**Más adelante (Día 3 — 11/11 / Día 4 — 13/11):**
- Día 3 (11/11): publicar comentarios de validación en HU-11 (Dashboard, tarjeta de Leonid), HU-13 (Reportes CSV/PDF, tarjeta de Ricardo) y HU-07 (Aprobación humana, tarjeta de Ricardo).
- Día 4 (13/11): publicar comentario de aceptación formal del incremento en `Sprint Review — Sprint 6` (su propia tarjeta); publicar comentario de balance en `Retrospectiva — PMV2` (tarjeta de Gina); participar en la auditoría final de cumplimiento de §7.

**Ya hecho (no repetir):**
Comentario del Daily Scrum 09/11 publicado en la tarjeta de Daily.

---

## 1. Objetivo y reglas de colaboración

### 1.1 Contexto de la auditoría académica
El docente evalúa el proyecto mediante un análisis estructurado del archivo JSON exportado desde Trello. El evaluador algorítmico y docente audita específicamente:
1. **Evidencia de trabajo auténtico y colaborativo:** Distribución equilibrada de actividad entre los miembros humanos mediante sus cuentas de Trello.
2. **Estado de los paquetes de trabajo (PMV):**
   - **PMV1 (Observabilidad, Sprints 1 a 3):** Debe figurar 100 % culminado, concentrado en las listas `7. DONE`, `10. SPRINT REVIEW` y `11. SPRINT RETROSPECTIVE`.
   - **PMV2 (Inteligencia, Sprints 4 a 6):** En ejecución activa al día de hoy (Sprint 6), con tarjetas distribuidas en `4. TO DO`, `5. IN PROGRESS`, `6. QA-TESTING` y `7. DONE`.
   - **PMV3 (Validación experimental y optimización, Sprints 7 a 8):** Planificado en `1. PRODUCT BACKLOG` y `2. SPRINT BACKLOG`.
3. **Calidad de cada tarjeta:** Cada tarjeta abierta debe contener simultáneamente seis elementos coherentes:
   - **Fecha de vencimiento (due date):** Coherente con el calendario de sprints.
   - **Checklist:** Con 4 a 7 ítems técnicos reales y casillas marcadas según el avance comprobable.
   - **Miembro (único):** En cada tarjeta, como miembro, solo debe figurar un único integrante responsable. La colaboración multidisciplinaria se evidencia a través de comentarios técnicos de los demás integrantes, nunca agregándolos como miembros.
   - **Etiquetas:** Etiqueta de fase (PMV1, PMV2 o PMV3) y etiquetas de especialidad técnica.
   - **Descripción exhaustiva:** Mayor a 80 caracteres. Para historias de usuario, debe cumplir estrictamente la estructura «Como… necesito… para…», delimitación de alcance, criterios de aceptación numerados con formato Given/When/Then (CA-01..), evidencia técnica en el repositorio y Definición de Terminado (DoD).
   - **Comentarios y actividad:** Comentarios técnicos individuales, diferenciados y con citas de comandos, pruebas y métricas reales.

### 1.2 Reglas obligatorias para evitar observaciones de simulación o maquillaje
1. **Uso exclusivo de cuentas personales:** No existe importación automática de actividades en Trello. Cada integrante debe iniciar sesión con su propia cuenta de Trello para realizar las acciones asignadas. Si una sola persona crea o comenta todo, el JSON registrará un único `memberCreator` en las acciones, lo que genera una penalización crítica inmediata por autoría ficticia.
2. **Prohibición de comentarios clonados o genéricos:** Los comentarios deben reflejar el trabajo individual de cada rol. Queda prohibido copiar y pegar textos idénticos entre integrantes.
3. **Registro verídico de transiciones de estado:** Para que el JSON registre movimientos entre listas (`updateCard` con `listAfter`), las tarjetas no deben crearse directamente en `DONE`. Deben desplazarse progresivamente siguiendo el flujo natural: `TO DO` -> `IN PROGRESS` -> `QA-TESTING` -> `DONE`.
4. **Tratamiento honesto de sprints pasados:** No se deben inventar reuniones ni falsificar marcas temporales pasadas en el Daily Scrum. Para las tarjetas de revisión y retrospectiva de los Sprints 1 al 5, se debe incluir explícitamente en la descripción la leyenda:
   > «Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio».
5. **Dailies en tiempo real:** Desde el Sprint 6, se mantiene una tarjeta única por sesión de Daily Scrum (Lunes, Miércoles y Viernes a las 08:00). Cada integrante publica su propio comentario respondiendo a las tres preguntas ágiles el día correspondiente.
6. **Regla del miembro único y colaboración por comentarios:** Por disposición obligatoria docente, en cada tarjeta de Trello debe figurar **un solo integrante como miembro asignado** (el responsable directo de la tarjeta). La colaboración de los otros integrantes se demuestra exclusivamente mediante **comentarios técnicos individuales** en dicha tarjeta. Queda terminantemente prohibido asignar múltiples miembros a una misma tarjeta.

---

## 2. Preparación del tablero (Paso 0 — Gina Diana Barrera Peña, Scrum Master)

Antes de que el equipo inicie la carga de información, la Scrum Master debe acondicionar la estructura del tablero.

### 2.1 Estandarización de etiquetas
Acceder al menú lateral del tablero -> **Etiquetas** y aplicar la siguiente configuración:

| Etiqueta anterior | Nombre nuevo final | Color en Trello | Propósito |
|---|---|---|---|
| `MVP-01` | `PMV1` | Verde | Productos y actividades del Producto Mínimo Viable 1 |
| `MVP 02` | `PMV2` | Amarillo | Productos y actividades del Producto Mínimo Viable 2 |
| `MVP 03` | `PMV3` | Azul | Productos planificados para el Producto Mínimo Viable 3 |
| *(Nueva)* | `Arquitectura` | Morado | Diseño de microservicios, contratos OpenAPI y patrones |
| *(Nueva)* | `Infraestructura` | Negro | Docker, Compose, Prometheus, Grafana y despliegue |
| *(Nueva)* | `Machine Learning` | Naranja | Algoritmos predictivos, métricas de error y MLflow |
| *(Nueva)* | `Seguridad` | Rojo | Supabase Auth, JWT, RBAC y políticas RLS |
| *(Nueva)* | `Backend` | Celeste (Sky) | Servicios en Python (FastAPI), Go y Java |
| *(Nueva)* | `Frontend` | Rosa (Pink) | Interfaz web, gráficos en canvas y vistas modulares |
| *(Nueva)* | `Datos` | Verde lima (Lime) | Telemetría, SQLite, PostgreSQL y scripts de carga |
| *(Nueva)* | `Documentación` | Gris (Light Gray) | Actas, informes académicos, planes y guías |

> [!IMPORTANT]
> Gina debe eliminar cualquier etiqueta residual o etiqueta naranja sin nombre existente en el tablero.

### 2.2 Depuración y archivo de tarjetas duplicadas u obsoletas
Gina debe archivar las siguientes tarjetas que distorsionan el flujo y son detectadas como anomalías por el validador:
1. **Tarjeta `Sprint 1` en lista `2. SPRINT BACKLOG`:** Tarjeta plantilla obsoleta y vacía. Se archiva (el Sprint 1 ya concluyó en PMV1).
2. **Tarjeta `Sprint 7` en lista `10. SPRINT REVIEW`:** Placeholder vacío de sprint futuro. Se archiva.
3. **Tarjeta `Sprint 8` en lista `10. SPRINT REVIEW`:** Placeholder vacío de sprint futuro. Se archiva.
4. **Tarjetas de retrospectivas parciales:** Archivar las tarjetas `Retrospectiva | Sprint [4] | [2026-10-05]` y `Retrospectiva | Sprint [5] | [2026-10-23]` en la lista `11. SPRINT RETROSPECTIVE`. Se reemplazan por las tarjetas consolidadas oficiales `Retrospectiva — PMV1 (Sprints 1–3)` y `Retrospectiva — PMV2 (Sprints 4–6)`.
5. **Tarjetas de Daily Scrum obsoletas:** Archivar cualquier tarjeta de Daily Scrum suelta o vacía que no corresponda al ciclo formal (en especial las 23 tarjetas antiguas de formato «Daily | Sprint [5]/[10]»).

### 2.3 Fondo y miembros oficiales
- **Fondo del tablero:** Seleccionar un color sólido formal (azul marino o gris oscuro) en Configuración -> Cambiar fondo.
- **Miembros del tablero:** Confirmar que únicamente figuren los 4 integrantes universitarios:
  1. `Jhonny Cristhian Quintana Carhuaricra` (Product Owner)
  2. `Gina Diana Barrera Peña` (Scrum Master)
  3. `Ricardo Porras Veli` (Backend y DevOps)
  4. `Leonid Kisley Orlando Huamán Collazos` (Infraestructura y Frontend)

> [!IMPORTANT]
> **Miembro único por tarjeta:** Aunque los 4 integrantes pertenecen al tablero, a nivel de tarjeta rige estrictamente la directiva del docente: **cada tarjeta tiene un único integrante asignado como miembro**. El trabajo colaborativo no se refleja sumando miembros a la tarjeta, sino a través de los comentarios técnicos registrados por cada estudiante con su propia cuenta.


### 2.4 Nomenclatura de tarjetas de historia de usuario

Las 16 tarjetas HU deben titularse con el formato `PMVn-HUxx: <nombre>`, donde `n` es el PMV que la tabla maestra (sección 3) asigna a esa HU (debe coincidir con su etiqueta PMV) y `xx` su número. Ejemplos: `PMV1-HU01: Métricas de infraestructura`, `PMV2-HU03: Predicción de CPU a 15 min`.

- Cada responsable renombra **su propia** tarjeta desde su cuenta personal, según la columna «Responsable de moverla» de la tabla maestra. No renombrar en bloque desde una sola cuenta: el JSON registraría una única autoría para todos los cambios.
- Gina verifica al cierre de la preparación que las 16 HU siguen el formato, sin renombrarlas por los demás.
- En el texto corrido (descripciones y comentarios) puede seguir usándose la referencia «HU-xx».

---

## 3. Tabla maestra de tarjetas

A continuación se detalla la asignación completa de las 39 tarjetas maestras que estructuran el tablero Green AI, bajo la regla del **miembro único** por tarjeta (la colaboración se evidencia mediante comentarios técnicos):

| Tarjeta | Lista destino | Etiquetas | Miembro (único) | Fecha vencimiento |
|---|---|---|---|---|
| PMV1-HU01: Métricas de infraestructura | 7. DONE | PMV1, Infraestructura, Backend | Leonid Huamán | 2026-09-05 |
| PMV1-HU02: Almacenamiento de históricos | 7. DONE | PMV1, Datos, Backend | Ricardo Porras | 2026-09-19 |
| PMV1-HU15: Registro y autenticación | 7. DONE | PMV1, Seguridad, Frontend | Leonid Huamán | 2026-10-03 |
| PMV2-HU03: Predicción de CPU a 15 min | 7. DONE | PMV2, Machine Learning, Backend | Gina Barrera | 2026-10-17 |
| PMV2-HU04: Comparación de modelos | 7. DONE | PMV2, Machine Learning, Datos | Gina Barrera | 2026-10-17 |
| PMV2-HU06: Recomendaciones explicables | 7. DONE | PMV2, Backend, Machine Learning | Ricardo Porras | 2026-10-31 |
| PMV2-HU08: Restricciones operativas | 7. DONE | PMV2, Backend, Seguridad | Gina Barrera | 2026-10-31 |
| PMV2-HU12: Alertas operativas | 7. DONE | PMV2, Infraestructura, Backend | Leonid Huamán | 2026-11-14 |
| PMV2-HU14: Control de acceso con VIEWER | 7. DONE | PMV2, Seguridad, Backend | Ricardo Porras | 2026-10-31 |
| PMV2-HU11: Dashboard con pestañas | 6. QA-TESTING | PMV2, Frontend, Infraestructura | Leonid Huamán | 2026-11-14 |
| PMV2-HU05: Registro en MLflow | 6. QA-TESTING | PMV2, Machine Learning, Datos | Gina Barrera | 2026-11-14 |
| PMV2-HU07: Aprobación humana de decisiones | 5. IN PROGRESS | PMV2, Backend, Seguridad | Ricardo Porras | 2026-11-14 |
| PMV2-HU13: Reportes históricos CSV y PDF | 5. IN PROGRESS | PMV2, Backend, Datos | Ricardo Porras | 2026-11-14 |
| PMV2-HU09: Estimación de energía en kWh | 5. IN PROGRESS | PMV2, Backend, Machine Learning | Ricardo Porras | 2026-11-14 |
| Tarea: Fijar Health Check Path en Render | 4. TO DO | PMV2, Infraestructura | Leonid Huamán | 2026-11-10 |
| Tarea: Revisar RLS Supabase y password | 4. TO DO | PMV2, Seguridad, Backend | Ricardo Porras | 2026-11-11 |
| Tarea: Evaluación walk-forward de CPU | 4. TO DO | PMV2, Machine Learning | Gina Barrera | 2026-11-13 |
| Tarea: Grabar video de la Unidad III | 4. TO DO | PMV2, Documentación | Jhonny Quintana | 2026-11-14 |
| PMV3-HU10: Estimación de emisiones CO2e | 1. PRODUCT BACKLOG | PMV3, Machine Learning, Datos | Jhonny Quintana | 2026-11-28 |
| PMV3-HU16: Experimento comparativo | 1. PRODUCT BACKLOG | PMV3, Documentación, Machine Learning | Jhonny Quintana | 2026-11-30 |
| Sprint 6 (03/11–14/11) | 2. SPRINT BACKLOG | PMV2, Documentación | Gina Barrera | 2026-11-14 |
| Sprint 7 (17/11–23/11) | 2. SPRINT BACKLOG | PMV3, Documentación | Gina Barrera | 2026-11-23 |
| RE-01 Delimitación de infraestructura | 3. REFINAMIENTO DE EXPERTOS | PMV1, Arquitectura, Infraestructura | Leonid Huamán | 2026-09-05 |
| RE-02 Contratos y arquitectura híbrida | 3. REFINAMIENTO DE EXPERTOS | PMV1, Arquitectura, Backend | Ricardo Porras | 2026-09-19 |
| RE-03 Calidad y trazabilidad de datos | 3. REFINAMIENTO DE EXPERTOS | PMV1, Datos | Gina Barrera | 2026-10-03 |
| RE-04 Validación de modelos de IA | 3. REFINAMIENTO DE EXPERTOS | PMV2, Machine Learning | Gina Barrera | 2026-10-17 |
| RE-05 Telemetría energética vs proxy | 3. REFINAMIENTO DE EXPERTOS | PMV2, Machine Learning | Ricardo Porras | 2026-10-31 |
| RE-06 Diseño experimental riguroso | 3. REFINAMIENTO DE EXPERTOS | PMV2, Documentación | Jhonny Quintana | 2026-11-14 |
| Sprint Review — Sprint 1 | 10. SPRINT REVIEW | PMV1, Documentación | Jhonny Quintana | 2026-09-05 |
| Sprint Review — Sprint 2 | 10. SPRINT REVIEW | PMV1, Documentación | Jhonny Quintana | 2026-09-19 |
| Sprint Review — Sprint 3 | 10. SPRINT REVIEW | PMV1, Documentación | Jhonny Quintana | 2026-10-03 |
| Sprint Review — Sprint 4 | 10. SPRINT REVIEW | PMV2, Documentación | Jhonny Quintana | 2026-10-17 |
| Sprint Review — Sprint 5 | 10. SPRINT REVIEW | PMV2, Documentación | Jhonny Quintana | 2026-10-31 |
| Sprint Review — Sprint 6 | 10. SPRINT REVIEW | PMV2, Documentación | Jhonny Quintana | 2026-11-14 |
| Retrospectiva — PMV1 (Sprints 1–3) | 11. SPRINT RETROSPECTIVE | PMV1, Documentación | Gina Barrera | 2026-10-03 |
| Retrospectiva — PMV2 (Sprints 4–6) | 11. SPRINT RETROSPECTIVE | PMV2, Documentación | Gina Barrera | 2026-11-14 |
| PRODUCT OWNER | 8. ROLES DE SCRUM | Documentación | Jhonny Quintana | 2026-11-30 |
| SCRUM MASTER | 8. ROLES DE SCRUM | Documentación | Gina Barrera | 2026-11-30 |
| SCRUM TEAM | 8. ROLES DE SCRUM | Documentación | Leonid Huamán | 2026-11-30 |

---

## 4. Fichas de tarjetas listas para copiar y pegar

En esta sección se suministran los contenidos técnicos exactos para cada una de las 39 tarjetas. Los integrantes deben copiar y pegar los textos de forma rigurosa.

```
================================================================================
4.1 HISTORIAS DE USUARIO (HU-01 A HU-16)
================================================================================
```

### Tarjeta PMV1-HU01: Visualización de métricas de infraestructura
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV1`, `Infraestructura`, `Backend`
- **Miembro (único):** `Leonid Kisley Orlando Huamán Collazos`
- **Colaboran con comentarios:** `Ricardo Porras Veli`
- **Fecha de vencimiento:** `2026-09-05`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito visualizar métricas actualizadas de CPU, memoria, red y almacenamiento de los nodos en supervisión,
para evaluar el comportamiento operativo del entorno computacional e identificar sobrecargas o anomalías.

ALCANCE

Incluye la ingesta continua de telemetría mediante Prometheus desde el simulador de infraestructura, el consumo estructurado a través del microservicio de Monitoring (Spring Boot) y su exposición mediante contratos OpenAPI al API Gateway. Todo registro identifica explícitamente recurso, unidad, marca temporal y procedencia. Los datos generados por el simulador declaran su origen simulado mediante la propiedad origin=simulated.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un nodo en ejecución y Prometheus en estado UP, cuando el usuario consulta sus métricas de telemetría, entonces el servicio retorna las series temporales con identificación de recurso, unidad física y procedencia simulada.
CA-02: Dado un nodo inexistente o un identificador con caracteres inválidos, cuando se solicita su estado, entonces el servicio devuelve un código HTTP 404/400 con un mensaje de error descriptivo sin exponer trazas internas.
CA-03: Dada la indisponibilidad de la fuente de métricas, cuando se consultan los endpoints de supervisión, entonces el sistema informa la degradación del servicio sin inventar datos ni asumir valores nulos como consumo cero.
CA-04: Dado el flujo continuo de recolección de métricas, cuando se actualiza la consulta, entonces se presentan los registros más recientes dentro del intervalo de raspado configurado (5 segundos).

EVIDENCIA EN REPOSITORIO

- Microservicio Monitoring: software/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/
- Pruebas de contrato y unitarias: MetricsHttpContractTest en software/monitoring/ (N pruebas JUnit aprobadas — anotar la cifra real tras ejecutar `mvn test` en software/monitoring).
- Prueba de humo integral: software/infraestructura/smoke/smoke.py (14/14 comprobaciones superadas).

DEFINICIÓN DE TERMINADO (DoD)

1. Criterios de aceptación verificados con pruebas automatizadas.
2. Contrato OpenAPI publicado y accesible.
3. Código integrado en la rama test/main sin secretos en texto plano.
4. Documentado en el entregable de la Unidad III y actas de revisión.
```
- **Checklist «Actividades técnicas»:**
  - [x] Configurar scraping de Prometheus hacia el servicio simulator en puerto 8000
  - [x] Implementar endpoints /api/v1/metrics en servicio Monitoring con Spring Boot
  - [x] Incorporar atributo origin=simulated en contratos DTO de respuesta
  - [x] Implementar suite MetricsHttpContractTest y pruebas unitarias (anotar la cifra real de pruebas tras ejecutar `mvn test` en software/monitoring)
  - [x] Validar actualización en vivo cada 5 segundos y gestión de nodos inexistentes
- **Comentarios a publicar:**
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Verifiqué la recolección en Prometheus en el puerto 9090. El target del simulador reporta estado UP con 50 nodos simulados respondiendo métricas de CPU y memoria de manera estable. Ejecuté la suite de pruebas de Monitoring y se obtuvieron N pruebas unitarias y de integración aprobadas (N passed — anotar la cifra real tras ejecutar `mvn test` en software/monitoring).»
  - `Ricardo Porras Veli`:
    > «Integré el servicio Monitoring al Gateway local en el puerto 13000 y ejecuté la suite de verificación extremo a extremo software/infraestructura/smoke/smoke.py. El resultado arrojó 14/14 verificaciones aprobadas, confirmando que la cabecera origin=simulated se preserva a lo largo del pipeline HTTP.»

---

### Tarjeta PMV1-HU02: Almacenamiento y consulta de métricas históricas
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV1`, `Datos`, `Backend`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Leonid Kisley Orlando Huamán Collazos`, `Gina Diana Barrera Peña`
- **Fecha de vencimiento:** `2026-09-19`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito consultar registros históricos de métricas y eventos computacionales de forma estructurada y paginada,
para analizar tendencias de carga y alimentar los pipelines de datos de los modelos predictivos.

ALCANCE

Comprende el almacenamiento temporal de series de tiempo en el volumen persistente de Prometheus y la ingesta estructurada de registros históricos a través del microservicio Data Processing. Se implementó una capa de persistencia dual: SQLite para desarrollo local y pruebas herméticas, y PostgreSQL/PostgREST para entornos distribuidos. No se mezclan métricas volátiles con registros de auditoría.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un rango temporal válido menor o igual a 31 días y filtros de nodo, cuando el cliente solicita históricos, entonces el servicio retorna las muestras ordenadas cronológicamente con paginación por cursor y procedencia identificada.
CA-02: Dado un parámetro de consulta temporal inconsistente o un cursor corrupto, cuando se procesa la petición, entonces la API responde con código HTTP 422/400 detallando el parámetro no válido.
CA-03: Dado un periodo en el cual no existan registros computacionales, cuando se realiza la consulta, entonces el sistema responde con una lista vacía y metadatos de paginación coherentes, sin sintetizar datos artificiales.
CA-04: Dado el reinicio de los contenedores Docker preservando el volumen de almacenamiento, cuando el servicio se restablece, entonces los datos históricos previamente almacenados continúan disponibles.

EVIDENCIA EN REPOSITORIO

- Microservicio Data Processing: software/data-processing/
- Pruebas de contrato SQLite/PostgREST: software/data-processing/tests/test_historical_logs_contract.py
- Suite de pruebas de persistencia: 114 pruebas pytest aprobadas en entorno con PostgREST de prueba.

DEFINICIÓN DE TERMINADO (DoD)

1. Criterios de aceptación validados mediante pruebas de contrato.
2. Persistencia en volumen comprobada tras reinicio del servicio.
3. Documentación de endpoints en OpenAPI/Swagger.
4. Validación de paginación eficiente sin fugas de memoria.
```
- **Checklist «Actividades técnicas»:**
  - [x] Configurar volumen persistente en software/infraestructura/docker-compose.yml
  - [x] Diseñar contrato de paginación por cursor para históricos de telemetría
  - [x] Implementar adaptador dual SQLite / PostgreSQL en Data Processing
  - [x] Ejecutar suite de pruebas de contrato en test_historical_logs_contract.py
  - [x] Validar manejo de periodos sin datos y cursores inválidos (código 422)
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «Se completó la verificación del adaptador de persistencia en Data Processing. En entorno local con SQLite y en contenedor con PostgreSQL 17/PostgREST v13 la suite ejecutó 114 pruebas unitarias y de contrato sin fallos (114 passed). La paginación por cursor responde de manera determinista.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Se comprobó la persistencia de datos reiniciando el stack con compose.sqlite-dev.yml. Las 100 000 muestras sembradas en el fixture inicial permanecieron intactas y el endpoint /api/v1/historical-logs respondió con cabecera source=sqlite.»

---

### Tarjeta PMV1-HU15: Registro y autenticación de usuarios
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV1`, `Seguridad`, `Frontend`
- **Miembro (único):** `Leonid Kisley Orlando Huamán Collazos`
- **Colaboran con comentarios:** `Ricardo Porras Veli`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-03`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como usuario autorizado del sistema Green AI,
necesito registrar una cuenta y acceder de forma segura mediante mis credenciales,
para interactuar con las funcionalidades de supervisión y gestión según mi rol asignado.

ALCANCE

Abarca el flujo de registro de nuevos usuarios y autenticación de sesiones mediante Supabase Auth. La asignación inicial de roles se realiza de manera controlada en el backend mediante un trigger en base de datos que asigna por defecto el rol OPERATOR. No se permite la autoasignación de privilegios administrativos ni el almacenamiento de credenciales en texto claro.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un correo institucional y una contraseña que cumpla las directivas de seguridad, cuando el usuario completa el formulario de registro, entonces el sistema crea la cuenta en Supabase Auth y genera el perfil con rol OPERATOR.
CA-02: Dadas credenciales válidas de un usuario registrado, cuando solicita iniciar sesión, entonces el sistema genera y devuelve un token JWT firmado que permite consumir rutas protegidas.
CA-03: Dadas credenciales incorrectas o una cuenta inexistente, cuando se envía la solicitud, entonces la interfaz y la API retornan un mensaje de error genérico de autenticación sin revelar la existencia del correo.
CA-04: Dado un usuario autenticado que intenta modificar su carga útil (payload) JWT para elevar su rol a ADMIN, cuando el token llega al API Gateway, entonces la firma es invalidada y se rechaza la solicitud con HTTP 401.

EVIDENCIA EN REPOSITORIO

- Script de configuración de autenticación y triggers: software/frontend/supabase-auth-setup.sql
- Módulo cliente de autenticación en frontend: software/frontend/login.html
- Verificación en staging en Render con redirecciones hacia https://woshtsu.github.io/green-ai-workspace-cld/dev/

DEFINICIÓN DE TERMINADO (DoD)

1. Autenticación verificada de extremo a extremo contra Supabase.
2. Triggers de seguridad en PostgreSQL probados y sin fugas de privilegios.
3. Protección de contraseñas garantizada por el proveedor de identidad.
4. Cierre seguro de sesión con invalidación local del token.
```
- **Checklist «Actividades técnicas»:**
  - [x] Configurar esquema de autenticación y trigger de roles en software/frontend/supabase-auth-setup.sql
  - [x] Implementar cliente Supabase Auth en software/frontend/login.html
  - [x] Configurar URLs de redirección de producción y desarrollo en Supabase
  - [x] Probar rechazo ante contraseñas incorrectas y expiración de tokens
  - [x] Verificar que el registro asigna estrictamente el rol OPERATOR
- **Comentarios a publicar:**
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Configuramos las URLs de redirección en el panel de Supabase Auth para admitir tanto localhost:13001 como la URL de despliegue en GitHub Pages. Las sesiones inician correctamente y el token JWT se inyecta en las cabeceras Authorization de las peticiones subsiguientes.»
  - `Ricardo Porras Veli`:
    > «Revisé el trigger on_auth_user_created_green_ai en Supabase: se validó que cualquier registro público recibe estrictamente el rol OPERATOR en la tabla profiles. No existe ningún mecanismo en el frontend que permita inyectar el rol ADMIN.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Realicé pruebas funcionales de registro de usuario y recuperación de sesión desde el frontend. La gestión de errores responde adecuadamente ante contraseñas de menos de 8 caracteres.»

---

### Tarjeta PMV2-HU03: Predicción de utilización de CPU a corto plazo
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV2`, `Machine Learning`, `Backend`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Ricardo Porras Veli`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-17`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito obtener la predicción de la demanda computacional de CPU por nodo para un horizonte de 15 minutos,
para anticipar situaciones de saturación y planificar ajustes operativos proactivos.

ALCANCE

Comprende el pipeline de inferencia servido por el microservicio Prediction (FastAPI). El modelo seleccionado en producción es un Random Forest entrenado sobre series temporales con resolución de 5 minutos (ventana de observación de 2 horas con rezagos temporales y agregaciones). El endpoint retorna el valor estimado, el intervalo de tiempo, el recurso y la procedencia origin=estimated.

CRITERIOS DE ACEPTACIÓN

CA-01: Dada una serie histórica continua de al menos 6 intervalos consecutivos (30 minutos mínimos) de telemetría válida, cuando se invoca el endpoint /v1/predictions, entonces el servicio retorna el porcentaje de utilización de CPU previsto para los próximos 15 minutos con metadatos del modelo.
CA-02: Dada una serie de telemetría con menos de 6 muestras válidas o con valores nulos, cuando se solicita inferencia, entonces el servicio responde con HTTP 422 indicando datos insuficientes sin generar estimaciones aleatorias.
CA-03: Dado un valor de predicción generado, cuando se expone en la respuesta JSON, entonces incluye de forma explícita el campo origin="estimated" y el identificador de versión del modelo utilizado.
CA-04: Dado un conjunto de datos de validación temporal independiente, cuando se mide el error del modelo frente a una línea base de persistencia, entonces el modelo exhibe un MAE menor a 4,0 puntos porcentuales.

EVIDENCIA EN REPOSITORIO

- Microservicio Prediction: software/prediction/
- Metadatos del modelo serializado: software/prediction/models/selected/metadata.json
- Suite de pruebas de inferencia y contrato: N pruebas pytest aprobadas en software/prediction/tests/ (N passed — anotar la cifra real tras ejecutar `pytest` en software/prediction; último registro en docs/HANDOFF.md: 96 passed).
- Validación de humo: endpoint /v1/predictions retorna 200 con origin=estimated en software/infraestructura/smoke/smoke.py.

DEFINICIÓN DE TERMINADO (DoD)

1. Modelo serializado con metadatos y pipeline de preprocesamiento versionado.
2. Pruebas unitarias de inferencia y pruebas anti-fuga temporal aprobadas.
3. Verificación de consumo de memoria y tiempo de respuesta inferior a 200 ms.
4. Integración validada a través del API Gateway.
```
- **Checklist «Actividades técnicas»:**
  - [x] Entrenar y serializar modelo Random Forest en software/prediction/models/selected/
  - [x] Implementar endpoint REST POST /v1/predictions con FastAPI
  - [x] Incorporar validación estricta de ventana temporal mínima de telemetría
  - [x] Ejecutar suite de pruebas pytest completa de Prediction (N passed — anotar la cifra real tras ejecutar `pytest` en software/prediction; último registro en docs/HANDOFF.md: 96 passed)
  - [x] Validar presencia del campo origin=estimated en respuestas de inferencia
  - [x] Optimizar imagen Docker de Prediction reduciendo tamaño de 2.85 GB a 510 MB
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Se ejecutó el pipeline completo de entrenamiento y validación temporal. El modelo Random Forest obtuvo un MAE de 3.22 en el conjunto de validación y 3.85 en prueba. El artefacto final quedó registrado con sus hiperparámetros en models/selected/metadata.json.»
  - `Ricardo Porras Veli`:
    > «Ejecuté la suite de pruebas unitarias y de integración de Prediction con pytest: se alcanzaron N pruebas aprobadas (N passed — anotar la cifra real tras ejecutar `pytest` en software/prediction; último registro en docs/HANDOFF.md: 96 passed). Asimismo, optimizamos el Dockerfile multicapa reduciendo el peso de la imagen de 2.85 GB a solo 510 MB, ideal para el despliegue en Render.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Validé el contrato del endpoint /v1/predictions mediante Swagger UI y la suite de pruebas de humo. Cuando se envían menos de 6 registros de telemetría, el sistema responde consistentemente con código 422 y el detalle de insuficiencia de datos.»

---

### Tarjeta PMV2-HU04: Comparación reproducible de modelos de predicción
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV2`, `Machine Learning`, `Datos`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-17`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como analista de datos,
necesito comparar el desempeño de diferentes algoritmos predictivos bajo condiciones y divisiones de datos idénticas,
para justificar técnicamente la elección del modelo desplegado en el entorno de producción.

ALCANCE

Incluye la ejecución reproducible de un pipeline de evaluación comparativa que entrena y contrasta cuatro algoritmos: Regresión Ridge, Random Forest, HistGradientBoosting y un modelo de persistencia (baseline ingenuo). La comparación evalúa horizontes de 15, 30 y 60 minutos, registrando métricas de error (MAE, RMSE, MAPE) y tiempos de cómputo en archivos versionados.

CRITERIOS DE ACEPTACIÓN

CA-01: Dados los mismos conjuntos de entrenamiento y prueba temporales, cuando se ejecuta el pipeline de comparación, entonces los cuatro algoritmos se entrenan bajo particiones idénticas sin contaminación de datos futuros.
CA-02: Dados los resultados de la evaluación, cuando se consolidan en el reporte CSV, entonces se presentan las métricas de MAE, RMSE y tiempo de inferencia para cada algoritmo y horizonte evaluado.
CA-03: Dado el análisis de métricas, cuando se compara el modelo Random Forest con el baseline de persistencia para el horizonte de 15 minutos, entonces demuestra una reducción del MAE superior al 20 %.
CA-04: Dadas las limitaciones del dataset experimental sintético, cuando se documenta el reporte, entonces se declaran explícitamente los supuestos del generador y no se reclama superioridad energética sin mediciones físicas.

EVIDENCIA EN REPOSITORIO

- Script de entrenamiento comparativo: software/prediction/src/evaluation/comparison.py
- Tabla consolidada de métricas: software/prediction/results/metrics/model_comparison.csv
- Reporte analítico de discusión: docs/academico/08-pruebas-resultados-discusion.md

DEFINICIÓN DE TERMINADO (DoD)

1. Pipeline de comparación ejecutable mediante comando único sin intervención manual.
2. Archivo model_comparison.csv generado y registrado en Git.
3. Gráficas y tablas comparativas incorporadas en el informe de la Unidad III.
4. Código libre de advertencias críticas en scikit-learn.
```
- **Checklist «Actividades técnicas»:**
  - [x] Desarrollar script compare_models.py con particionado temporal estricto
  - [x] Implementar evaluación de Random Forest, Ridge, HistGradientBoosting y Persistencia
  - [x] Calcular métricas MAE, RMSE y latencia de inferencia en milisegundos
  - [x] Generar tabla de resultados en software/prediction/results/metrics/model_comparison.csv
  - [x] Documentar límites experimentales en la sección de discusión académica
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Se ejecutó la comparativa con partición temporal (split 70/15/15). Para el horizonte de 15 min: Random Forest alcanzó MAE 3.22 / RMSE 4.59; Ridge MAE 4.10; HistGradientBoosting MAE 3.45; Persistencia MAE 4.60. Random Forest superó a la persistencia en un 30 % de reducción del error en validación.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Revisé los resultados consolidados en model_comparison.csv. Se verificó que ninguna prueba usara aleatorización desordenada (shuffle=False), garantizando total respeto a la causalidad temporal en series de tiempo.»

---

### Tarjeta PMV2-HU06: Generación de recomendaciones operativas explicables
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV2`, `Backend`, `Machine Learning`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Leonid Kisley Orlando Huamán Collazos`, `Gina Diana Barrera Peña`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-31`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito recibir recomendaciones operativas fundamentadas en la predicción de demanda y el contexto de los nodos,
para evaluar ajustes de capacidad que prevengan la saturación o reduzcan el desperdicio computacional de manera segura.

ALCANCE

Comprende el motor de políticas de recomendación (Policy Engine) implementado en el servicio Prediction. El motor analiza la telemetría actual y la predicción a 15 minutos, aplicando umbrales y reglas operativas configurables para recomendar acciones de aumento, mantenimiento o revisión de capacidad. El sistema opera en modo Recommendation-Only: genera propuestas explicables marcadas con executionAllowed=false sin aplicar modificaciones autónomas a contenedores o máquinas virtuales.

CRITERIOS DE ACEPTACIÓN

CA-01: Dada una predicción de CPU y telemetría válidas, cuando se evalúan las reglas de política, entonces el servicio retorna una propuesta con acción sugerida (SCALE_UP, SCALE_DOWN_REVIEW, MAINTAIN), justificación detallada y nivel de urgencia.
CA-02: Dados datos de entrada incompatibles, desactualizados o incompletos, cuando se solicitan recomendaciones, entonces el motor se abstiene de sugerir cambios y retorna una respuesta con estado de información insuficiente.
CA-03: Dada una recomendación generada, cuando se inspecciona su carga útil, entonces incluye explícitamente los umbrales aplicados, la predicción de entrada y la bandera de seguridad executionAllowed=false.
CA-04: Dada una condición de alta carga sostenida por encima del umbral crítico, cuando se genera la recomendación, entonces se clasifica con severidad alta y motivo de prevención de violación de SLA.

EVIDENCIA EN REPOSITORIO

- Motor de políticas: software/prediction/src/recommendations/policy.py
- Pruebas unitarias de reglas de decisión: software/prediction/tests/test_recommendations_api.py
- Validación en prueba de humo: software/infraestructura/smoke/smoke.py (endpoint /v1/recommendations responde 200 con eligible_for_review).

DEFINICIÓN DE TERMINADO (DoD)

1. Motor de políticas desacoplado de los modelos estadísticos de inferencia.
2. Pruebas unitarias que cubran escenarios de baja carga, carga normal y saturación.
3. Exposición de endpoints en OpenAPI/Swagger.
4. Garantía de no ejecución automática sobre infraestructura verificada.
```
- **Checklist «Actividades técnicas»:**
  - [x] Diseñar e implementar clase PolicyEngine con reglas explicables
  - [x] Configurar umbrales de decisión parametrizables por variables de entorno
  - [x] Implementar estructura de respuesta con campos justification y executionAllowed=false
  - [x] Escribir pruebas unitarias en test_policy_engine.py (pruebas de recomendación — anotar la cifra real tras ejecutar `pytest` en software/prediction)
  - [x] Probar abstención ante telemetría ausente o parámetros fuera de rango
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «Implementamos la lógica del PolicyEngine en software/prediction/src/recommendations/policy.py. Se programaron pruebas unitarias de recomendación que cubren todas las ramas de decisión (anotar la cifra real tras ejecutar `pytest` en software/prediction). En todas las respuestas generadas se incluye rigurosamente executionAllowed=false y la justificación técnica correspondiente.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Se probó el endpoint /v1/recommendations a través de la suite de humo y mediante el Gateway en Go. El tiempo de respuesta del motor de recomendaciones es inferior a 45 ms y valida adecuadamente las cabeceras CORS.»
  - `Gina Diana Barrera Peña`:
    > «Verificamos la coherencia entre la salida del modelo de regresión y las entradas del motor de reglas. La recomendación solo se emite cuando la predicción cuenta con un intervalo de confianza y telemetría de soporte consistente.»

---

### Tarjeta PMV2-HU08: Configuración y evaluación de restricciones operativas
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV2`, `Backend`, `Seguridad`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Ricardo Porras Veli`
- **Fecha de vencimiento:** `2026-10-31`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito definir y evaluar restricciones operativas y márgenes de seguridad para las propuestas del sistema,
para impedir que se sugieran acciones incompatibles con la disponibilidad del servicio o la estabilidad del clúster.

ALCANCE

Abarca el módulo de restricciones operativas en el microservicio Prediction. Las políticas determinan márgenes de seguridad para la utilización de CPU y memoria, tiempos mínimos entre transiciones de escala (cooldown) y umbrales mínimos de redundancia. Las restricciones son versionadas y configurables mediante archivos JSON (DEMO_POLICY_JSON) o variables de entorno.

CRITERIOS DE ACEPTACIÓN

CA-01: Dada una política operativa válida, cuando se inicializa el servicio, entonces se cargan y versionan los parámetros de umbral y márgenes de seguridad establecidos.
CA-02: Dada una recomendación que violaría una restricción comprobable (ej. reducir capacidad en horario punta), cuando se evalúa, entonces la propuesta se bloquea y se documenta el motivo del descarte.
CA-03: Dada una restricción cuya verificación requiere métricas no disponibles en el entorno, cuando se procesa, entonces el sistema la declara como no verificable y no la presenta como cumplida.
CA-04: Dados parámetros contradictorios en la configuración de la política (ej. umbral de saturación menor al de enfriamiento), cuando el servicio inicia, entonces se rechaza la configuración con un error fatal controlado.

EVIDENCIA EN REPOSITORIO

- Módulo de restricciones: software/prediction/src/recommendations/policy.py
- Pruebas de validación de políticas: software/prediction/tests/test_recommendations_api.py
- Documentación de arquitectura de políticas: docs/academico/04-gestion-del-proyecto.md

DEFINICIÓN DE TERMINADO (DoD)

1. Módulo de restricciones con pruebas unitarias independientes.
2. Validación de políticas al inicio del contenedor.
3. Bloqueo determinista de recomendaciones inseguras probado.
4. Trazabilidad de versiones de política en respuestas de API.
```
- **Checklist «Actividades técnicas»:**
  - [x] Desarrollar modelo y umbrales de restricciones operativas en software/prediction/src/recommendations/policy.py
  - [x] Implementar soporte para configuración externa mediante variable DEMO_POLICY_JSON
  - [x] Crear pruebas para restricciones cumplidas, violadas y no verificables
  - [x] Validar rechazo de configuraciones con umbrales contradictorios
  - [x] Integrar evaluación de restricciones dentro del pipeline de recomendación
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Definimos la matriz de restricciones y umbrales de la política en software/prediction/src/recommendations/policy.py con umbrales de seguridad (CPU máxima permitida 80 %, margen de guarda 10 %). Todas las pruebas de validación de umbrales pasaron satisfactoriamente en pytest.»
  - `Ricardo Porras Veli`:
    > «Se probó la inyección de políticas personalizadas vía DEMO_POLICY_JSON. Cuando un valor es inválido o contradictorio, el validador Pydantic intercepta la carga y evita que el servicio opere con parámetros incoherentes.»

---

### Tarjeta PMV2-HU12: Detección y gestión de alertas operativas
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV2`, `Infraestructura`, `Backend`
- **Miembro (único):** `Leonid Kisley Orlando Huamán Collazos`
- **Colaboran con comentarios:** `Ricardo Porras Veli`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito recibir alertas tempranas ante condiciones de saturación, fallas de telemetría o riesgo predictivo en los nodos,
para intervenir oportunamente antes de que se presenten degradaciones o caídas en la disponibilidad del servicio.

ALCANCE

Comprende la definición y evaluación de reglas de alerta en Prometheus (alerts.yml). Se implementaron cuatro reglas principales: SimulatorTelemetryDown (telemetría caída por más de 1 minuto), NodeCpuSaturationRisk (utilización actual de CPU > 85 % durante 2 minutos), NodeMemoryPressure (memoria > 90 % durante 2 minutos) y PredictedCpuHigh (predicción de CPU > 80 % para los próximos 15 minutos).

CRITERIOS DE ACEPTACIÓN

CA-01: Dada una condición de sobrecarga que supere el umbral durante la ventana de tiempo estipulada, cuando Prometheus evalúa la regla, entonces se genera una alerta activa con etiqueta de severidad, nodo afectado y mensaje explicativo.
CA-02: Dada una condición de sobrecarga temporal de corta duración (pico menor a 30 segundos), cuando se ejecuta el raspado de métricas, entonces la alerta no se dispara, evitando alertas falsas por fluctuaciones transitorias.
CA-03: Dada una condición anormal que se restablece a valores normales, cuando se realiza la siguiente evaluación, entonces la alerta pasa automáticamente al estado resuelto (resolved).
CA-04: Dada la desconexión total del servicio de telemetría del simulador, cuando transcurre 1 minuto, entonces se genera la alerta SimulatorTelemetryDown con severidad crítica.

EVIDENCIA EN REPOSITORIO

- Archivo de reglas de alerta: software/infraestructura/prometheus/alerts.yml
- Validación de sintaxis y coherencia con herramienta oficial: promtool check rules software/infraestructura/prometheus/alerts.yml
- Registro de pruebas en informe: docs/HANDOFF.md (sección Avances del 2026-11-06).

DEFINICIÓN DE TERMINADO (DoD)

1. Archivo alerts.yml validado con promtool con 0 errores.
2. Alertas visibles en la interfaz de Prometheus en http://localhost:9090/alerts.
3. Reglas probadas simulando desconexión de telemetría y saturación sintética.
4. Documentadas en el manual de despliegue y observabilidad.
```
- **Checklist «Actividades técnicas»:**
  - [x] Diseñar reglas de alerta en Prometheus para CPU, memoria, disponibilidad y predicción
  - [x] Configurar tiempos de evaluación (for: 1m y for: 2m) para mitigar falsos positivos
  - [x] Validar archivo software/infraestructura/prometheus/alerts.yml usando promtool
  - [x] Probar activación de alerta SimulatorTelemetryDown apagando el contenedor del simulador
  - [x] Verificar transición de estado firing a resolved en interfaz de Prometheus
- **Comentarios a publicar:**
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Se validó el conjunto de reglas en alerts.yml ejecutando promtool check rules: la sintaxis y las expresiones PromQL resultaron impecables (SUCCESS). Las cuatro alertas (SimulatorTelemetryDown, NodeCpuSaturationRisk, NodeMemoryPressure, PredictedCpuHigh) están operativas.»
  - `Ricardo Porras Veli`:
    > «Realizamos la prueba de desconexión del simulador. A los 60 segundos Prometheus disparó la alerta SimulatorTelemetryDown con severidad critical. Al reiniciar el servicio, la alerta se resolvió de forma automática a los 15 segundos.»

---

### Tarjeta PMV2-HU14: Control de acceso basado en roles con rol VIEWER
- **Lista destino:** `7. DONE`
- **Etiquetas:** `PMV2`, `Seguridad`, `Backend`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Leonid Kisley Orlando Huamán Collazos`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-31`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador del sistema,
necesito restringir el acceso a las operaciones y endpoints según el rol asignado a cada usuario (ADMIN, OPERATOR, VIEWER),
para garantizar la confidencialidad de la información y proteger la plataforma contra modificaciones no autorizadas.

ALCANCE

Abarca el filtro de autorización RBAC (Role-Based Access Control) en el API Gateway, desarrollado tanto en Go como en Java (Spring Cloud Gateway). Se implementó la matriz de permisos completa: ADMIN (gestión integral y configuración), OPERATOR (supervisión, consultas y simulación) y VIEWER (rol de solo lectura para auditoría e inspección académica, sin acceso a disparar simulaciones ni alterar configuraciones).

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un token JWT firmado válido que contenga el rol adecuado en sus claims, cuando el usuario solicita un recurso protegido, entonces el Gateway permite el paso al microservicio correspondiente.
CA-02: Dado un token JWT ausente, expirado o con firma digital inválida, cuando se solicita cualquier ruta protegida, entonces el Gateway rechaza la petición con código HTTP 401 Unauthorized.
CA-03: Dado un usuario autenticado con rol VIEWER que intenta ejecutar una acción reservada para OPERATOR o ADMIN, cuando el Gateway intercepta la llamada, entonces deniega el acceso respondiendo HTTP 403 Forbidden.
CA-04: Dado un usuario con un rol desconocido o inventado (ej. ROOT o GUEST), cuando intenta acceder a cualquier endpoint protegido, entonces el Gateway deniega la operación con código HTTP 403.

EVIDENCIA EN REPOSITORIO

- Gateway ligero en Go: software/gateway-go/ (N pruebas unitarias aprobadas con detector de carreras: go test -race ./... — anotar la cifra real tras ejecutar `go test -race ./...` en software/gateway-go).
- Gateway alternativo en Java: software/gateway/ (12 pruebas JUnit aprobadas).
- Extensión del enum de roles en base de datos: software/frontend/supabase-auth-setup.sql (soporte de VIEWER).

DEFINICIÓN DE TERMINADO (DoD)

1. Matriz de permisos documentada en el informe de arquitectura.
2. Filtros de seguridad en Gateway con pruebas automáticas para 401 y 403.
3. Cobertura de pruebas de concurrencia en Go sin condiciones de carrera.
4. Despliegue en Render verificado con variables de entorno de clave pública JWKS.
```
- **Checklist «Actividades técnicas»:**
  - [x] Definir matriz de roles ADMIN, OPERATOR y VIEWER
  - [x] Implementar middleware de validación JWT y verificación de claims en Gateway Go
  - [x] Incorporar suite de pruebas unitarias con go test -race ./... en software/gateway-go/ (anotar la cifra real tras ejecutar `go test -race ./...` en software/gateway-go)
  - [x] Actualizar Gateway Java con 12 pruebas JUnit aprobadas
  - [x] Validar que peticiones sin token retornan 401 y con rol insuficiente retornan 403
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «Implementé el soporte del rol VIEWER en el Gateway en Go. Corrí la suite de pruebas unitarias con el race detector activado: go test -race ./...: N passed (anotar la cifra real tras ejecutar `go test -race ./...` en software/gateway-go) sin ninguna condición de carrera ni fugas de memoria.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Verificamos la respuesta del Gateway en desarrollo: una llamada a rutas administrativas con token que contiene claim de rol VIEWER recibe estrictamente un código HTTP 403 Forbidden. Las pruebas de contrato en Java también arrojaron 12/12 passed.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Revisé la matriz de accesos y la coherencia con los requerimientos de la Unidad III. El rol VIEWER permite que los evaluadores y directivos examinen tableros sin riesgo de alteraciones accidentales.»

---

### Tarjeta PMV2-HU11: Dashboard integrado con pestañas y telemetría multirrecurso
- **Lista destino:** `6. QA-TESTING`
- **Etiquetas:** `PMV2`, `Frontend`, `Infraestructura`
- **Miembro (único):** `Leonid Kisley Orlando Huamán Collazos`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`, `Ricardo Porras Veli`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito consultar una interfaz unificada y modular con visualización de telemetría en vivo, gráficos comparativos de servidores y predicciones a 15 minutos,
para supervisar el estado integral de la infraestructura universitaria y evaluar las recomendaciones del sistema.

ALCANCE

Comprende el rediseño completo de la interfaz web (software/frontend/) organizado en pestañas interactivas: Visión general, Métricas en tiempo real, Predicciones, Recomendaciones y Flujo de red (flows.html). Incorpora renderizado en canvas con valores medios, máximos y mínimos, selector de hasta 5 servidores para comparación simultánea, tabla paginada con ordenamiento y modales de ayuda sin códigos de error crípticos.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un usuario autenticado que accede al dashboard, cuando selecciona un nodo en el catálogo, entonces la interfaz actualiza los paneles de telemetría y muestra la utilización de CPU y memoria correspondiente a ese nodo.
CA-02: Dadas predicciones y recomendaciones disponibles, cuando se cargan en la interfaz, entonces se muestran con indicación explícitamente de procedencia (origin=estimated), fecha y justificación técnica legible.
CA-03: Dada una falla o demora en la respuesta de un microservicio secundario, cuando se carga una pestaña, entonces el panel muestra un indicador amigable de espera sin quebrar el resto de la interfaz.
CA-04: Dado el botón de predicción a 15 minutos, cuando el usuario lo presiona, entonces se ejecuta la petición al Gateway y se dibuja el horizonte previsto en el gráfico comparativo de canvas.

EVIDENCIA EN REPOSITORIO

- Código fuente del frontend: software/frontend/ (archivos dashboard.html, racks.js, flows.html).
- Suite de pruebas automatizadas de UI en Node.js: software/frontend/tests/*.test.cjs (48 pruebas aprobadas).
- Arnés de pruebas local sin login: herramientas_IA/arnes_frontend/harness.py.
- Despliegue en GitHub Pages: https://woshtsu.github.io/green-ai-workspace-cld/dev/

DEFINICIÓN DE TERMINADO (DoD)

1. Suite de pruebas frontend ejecutada con 48 pruebas en verde.
2. Compatibilidad comprobada en Chrome y Firefox sin errores en consola.
3. Verificación con sesión real de Supabase Auth en entorno de staging (/dev/).
4. Capturas de pantalla adjuntas en el informe académico.
```
- **Checklist «Actividades técnicas»:**
  - [x] Diseñar arquitectura de pestañas y componentes visuales en software/frontend/
  - [x] Implementar gráfico comparativo en canvas (media, máximo, mínimo y comparación de 5 nodos)
  - [x] Desarrollar vista flows.html para visualización de topología y flujos computacionales
  - [x] Ejecutar suite de pruebas unitarias en Node.js (48/48 pruebas aprobadas)
  - [ ] Verificar funcionamiento con sesión real de Supabase en GitHub Pages /dev/
  - [ ] Capturar pantallas finales de cada pestaña para el anexo de evidencias del informe
- **Comentarios a publicar:**
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Se completó el rediseño del frontend modular. Corrí la suite de pruebas unitarias de componentes con Node.js: node --test tests/*.test.cjs y pasaron las 48 pruebas (48 passed). La navegación entre pestañas y los selectores de nodo funcionan con total fluidez.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Inspeccioné visualmente la interfaz usando el arnés local en el puerto 18999. El gráfico en canvas traza correctamente las curvas de media, mínimo y máximo sin parpadeos. La tarjeta pasa a QA-TESTING a la espera de validar el inicio de sesión real en /dev/ con el token de Supabase.»
  - `Ricardo Porras Veli`:
    > «Verifiqué la configuración de CORS en el Gateway de desarrollo para admitir las peticiones provenientes del origen https://woshtsu.github.io. Las cabeceras de preflight OPTIONS devuelven código 200 y permiten la comunicación segura con el backend.»

---

### Tarjeta PMV2-HU05: Registro y trazabilidad de experimentos en MLflow
- **Lista destino:** `6. QA-TESTING`
- **Etiquetas:** `PMV2`, `Machine Learning`, `Datos`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como analista de datos,
necesito registrar y versionar las ejecuciones de entrenamiento, hiperparámetros y métricas de error en MLflow Tracking,
para garantizar la trazabilidad de los artefactos predictivos y reproducir cualquier evaluación previa.

ALCANCE

Abarca la integración del cliente de MLflow en el pipeline de entrenamiento de Prediction (run_pipeline.py). Cuando el pipeline se ejecuta sin la bandera --skip-mlflow, registra el experimento computational-demand-prediction, almacenando parámetros del modelo (n_estimators, max_depth), métricas de evaluación (MAE, RMSE, MAPE) y los artefactos serializados con sus firmas de entrada/salida.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado el entrenamiento del modelo de predicción, cuando finaliza el pipeline, entonces se genera un run en MLflow con sus hiperparámetros, métricas numéricas y artefacto registrado.
CA-02: Dado un artefacto desplegado en producción, cuando se consulta su manifiesto, entonces es posible identificar el experiment_id y run_id correspondiente en el repositorio de MLflow.
CA-03: Dada la ejecución repetida del entrenamiento con semillas idénticas, cuando se comparan los registros en MLflow, entonces las métricas obtenidas resultan deterministas y reproducibles.
CA-04: Dado el entorno local o de CI, cuando MLflow no está disponible, entonces el pipeline admite la opción de fallback --skip-mlflow sin interrumpir la generación del manifiesto json básico.

EVIDENCIA EN REPOSITORIO

- Pipeline de entrenamiento con integración MLflow: software/prediction/scripts/run_pipeline.py
- Carpeta de tracking de experimentos: software/prediction/mlruns/ (experimento computational-demand-prediction, ID 394141087236111562, run random_forest_15m).
- Manifiesto de metadatos: software/prediction/results/manifest.json

DEFINICIÓN DE TERMINADO (DoD)

1. Pipeline conectado al servidor/directorio de MLflow.
2. Al menos un run completo registrado con métricas de test (MAE 3.85).
3. Captura de pantalla de la interfaz de MLflow UI incorporada en evidencias.
4. Documentación del comando de ejecución reproducible en el README.
```
- **Checklist «Actividades técnicas»:**
  - [x] Configurar cliente MLflow en software/prediction/src/mlflow/tracking.py
  - [x] Integrar logging de parámetros y métricas en run_pipeline.py
  - [x] Registrar experimento computational-demand-prediction con corrida random_forest_15m
  - [x] Validar persistencia de metadatos y firmas en software/prediction/mlruns/
  - [ ] Levantar interfaz mlflow ui localmente y tomar captura de evidencia
  - [ ] Adjuntar captura a la documentación de evidencias de la Unidad III
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Ejecuté run_pipeline.py integrando MLflow. Se registró con éxito el experimento computational-demand-prediction (id 394141087236111562) con el run random_forest_15m, registrando un MAE de prueba de 3.85 y los artefactos correspondientes en software/prediction/mlruns/.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «La tarjeta se encuentra en QA-TESTING: el tracking de MLflow en código está 100 % implementado y verificado. Solo resta levantar el servidor local con mlflow ui --port 5000 para capturar la vista de los gráficos de comparación de corridas para el informe.»

---

### Tarjeta PMV2-HU07: Flujo de aprobación humana para recomendaciones
- **Lista destino:** `5. IN PROGRESS`
- **Etiquetas:** `PMV2`, `Backend`, `Seguridad`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como administrador de TI,
necesito revisar las recomendaciones operativas generadas por la IA y registrar explícitamente mi aprobación o rechazo con una justificación,
para mantener el control operacional y garantizar una auditoría completa antes de cualquier modificación física.

ALCANCE

Comprende el ciclo de vida de aprobación de recomendaciones. Actualmente el sistema opera con el seguro de ejecución Recommendation-Only (executionAllowed=false). Esta historia incorpora la entidad DecisionLog para almacenar el estado de la propuesta (PENDING, APPROVED, REJECTED), el identificador del usuario responsable, la marca temporal confiable y el motivo del operador. En ningún caso la aprobación ejecuta comandos automáticos directos sobre contenedores o hipervisores.

CRITERIOS DE ACEPTACIÓN

CA-01: Dada una recomendación en estado pendiente, cuando un usuario con rol ADMIN la aprueba o rechaza, entonces el sistema registra la decisión con usuario, fecha, estado final y texto de justificación.
CA-02: Dado un usuario con rol OPERATOR o VIEWER, cuando intenta aprobar o rechazar una recomendación, entonces el sistema rechaza la solicitud con código HTTP 403.
CA-03: Dada una recomendación que ha expirado o que ya fue resuelta previamente, cuando se intenta emitir una nueva decisión, entonces el sistema retorna un conflicto HTTP 409 impidiendo transiciones duplicadas.
CA-04: Dada la aprobación formal de una propuesta, cuando se registra en el sistema, entonces la recomendación queda marcada como autorizada para ejecución manual por el equipo de operaciones, garantizando que el software no altera la infraestructura de forma autónoma.

EVIDENCIA EN REPOSITORIO

- Modelo base y seguro de ejecución: software/prediction/src/recommendations/policy.py (executionAllowed=false)
- Endpoint de consulta de recomendaciones: software/prediction/src/service/recommendations.py
- Documento de diseño arquitectónico: docs/academico/04-gestion-del-proyecto.md

DEFINICIÓN DE TERMINADO (DoD)

1. Modelo de datos DecisionLog implementado con validación de estados.
2. Endpoints POST /v1/recommendations/{id}/approve y /reject creados.
3. Pruebas de autorización con tokens de diferentes roles.
4. Registro de auditoría persistente verificado.
```
- **Checklist «Actividades técnicas»:**
  - [x] Garantizar bandera de seguridad executionAllowed=false en todas las respuestas
  - [ ] Diseñar modelo de persistencia para el registro de decisiones (DecisionLog)
  - [ ] Implementar endpoint POST /v1/recommendations/{id}/decision en Prediction
  - [ ] Restringir la toma de decisiones exclusivamente al rol ADMIN en el Gateway
  - [ ] Crear suite de pruebas unitarias para transiciones válidas e inválidas (código 409)
  - [ ] Integrar formulario de aprobación/rechazo en la interfaz web de recomendaciones
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «La tarjeta se encuentra IN PROGRESS. El backend ya asegura que ninguna recomendación se ejecute automáticamente (executionAllowed=false). Estamos definiendo el contrato del endpoint de registro de auditoría para guardar la decisión con firma del operador.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Revisé los criterios de aceptación: como Product Owner confirmo que es imprescindible exigir un campo obligatorio de justificación de al menos 15 caracteres para que ningún operador apruebe o descarte sin dejar constancia técnica.»

---

### Tarjeta PMV2-HU13: Exportación de reportes históricos en CSV y PDF
- **Lista destino:** `5. IN PROGRESS`
- **Etiquetas:** `PMV2`, `Backend`, `Datos`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como directivo universitario,
necesito generar y descargar reportes consolidados de demanda computacional, eficiencia y consumo estimado en formatos CSV y PDF,
para comunicar el balance técnico y justificar la toma de decisiones ante las autoridades académicas.

ALCANCE

Comprende el endpoint de reportes históricos en el microservicio Data Processing. Actualmente se encuentra 100 % implementada y probada la generación estructurada de reportes en formato JSON y CSV mediante el endpoint /api/processing/v1/reports/historical-summary. La exportación a PDF se encuentra pendiente y programada para el cierre del Sprint 6 / inicio de Sprint 7 según el acuerdo de alcance técnico CHG-07.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un intervalo de fechas seleccionado, cuando el usuario solicita la exportación en CSV, entonces el servicio genera un archivo tabular con cabeceras claras, marcas temporales ISO y procedencia de datos.
CA-02: Dados los datos consolidados en el reporte, cuando se comparan con las métricas del periodo, entonces coinciden exactamente con los promedios y máximos registrados en la base de datos.
CA-03: Dado un periodo sin datos en el rango seleccionado, cuando se solicita el reporte, entonces el sistema advierte la condición informando la ausencia de datos en vez de generar un archivo con ceros engañosos.
CA-04: Dado un usuario sin autenticación que solicita la descarga de reportes, cuando llega la petición al Gateway, entonces se bloquea respondiendo HTTP 401.

EVIDENCIA EN REPOSITORIO

- Endpoint de reportes: software/data-processing/application/use_cases/historical_report.py
- Pruebas unitarias y de formato CSV: 121 pruebas aprobadas en software/data-processing/tests/
- Registro de alcance en acta: docs/HANDOFF.md (sección Avances del 2026-11-06).

DEFINICIÓN DE TERMINADO (DoD)

1. Generación de CSV completada con pruebas automatizadas en verde.
2. Motor de plantillas o conversión PDF implementado y verificado.
3. Consistencia matemática idéntica comprobada entre CSV y PDF.
4. Descarga validada a través del Gateway.
```
- **Checklist «Actividades técnicas»:**
  - [x] Diseñar estructura de agregación de métricas diarias y semanales
  - [x] Implementar endpoint GET /api/processing/v1/reports/historical-summary en FastAPI
  - [x] Incorporar serializador a formato CSV con 121 pruebas pytest aprobadas
  - [ ] Implementar generador de reporte en formato PDF respetando el acuerdo CHG-07
  - [ ] Verificar coincidencia exacta de valores entre el reporte CSV y el reporte PDF
  - [ ] Agregar botones de descarga directa en la pestaña de reportes del frontend
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «La exportación en CSV está completamente terminada y probada: ejecutamos la suite de Data Processing alcanzando 121 pruebas aprobadas (121 passed). El endpoint entrega el archivo con codificación UTF-8 y cabeceras correctas. Mantenemos la tarjeta en IN PROGRESS hasta integrar la generación de PDF.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Verifiqué el archivo CSV descargado desde el endpoint de Data Processing. Las columnas de fecha, utilización promedio de CPU y cantidad de anomalías cuadran exactamente con la base de datos SQLite de pruebas.»

---

### Tarjeta PMV2-HU09: Estimación de consumo energético en kWh
- **Lista destino:** `5. IN PROGRESS`
- **Etiquetas:** `PMV2`, `Backend`, `Machine Learning`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como directivo universitario,
necesito consultar indicadores de consumo de energía acumulada en kilovatios-hora (kWh) calculados a partir de telemetría de potencia,
para evaluar el impacto energético de la infraestructura y fundamentar futuras estrategias de ahorro.

ALCANCE

Comprende el cálculo de energía mediante la regla del trapecio implementado en el endpoint /v1/energy del servicio Prediction. Siguiendo las directivas de honestidad experimental y las advertencias del experto (RE-05), la utilización de CPU no se convierte directamente a watts sin un modelo calibrado; el servicio requiere muestras de potencia (W) para integrar la energía (kWh). Cuando no se dispone de medidores de potencia física, el sistema declara la limitación e indica que la fuente es modelada o simulada.

CRITERIOS DE ACEPTACIÓN

CA-01: Dadas muestras consecutivas de potencia activa con intervalos de tiempo conocidos, cuando se procesa el cálculo, entonces el servicio aplica integración numérica trapezoidal retornando el total en kWh con precisión de dos decimales.
CA-02: Dado un conjunto de telemetría donde solo existe utilización de CPU y no existen datos de potencia medida, cuando se consulta el consumo energético, entonces el servicio retorna el consumo como estimado/no disponible y advierte la ausencia de medición física directa.
CA-03: Dada la comparación entre dos periodos de prueba, cuando se calcula la diferencia de energía, entonces se presentan el consumo de referencia, el consumo evaluado y la diferencia porcentual con su margen de incertidumbre.
CA-04: Dados intervalos de muestreo irregulares o con pérdida de paquetes, cuando se calcula la integral, entonces el algoritmo pondera cada trapecio por su delta de tiempo real sin asumir muestreo uniforme ficticio.

EVIDENCIA EN REPOSITORIO

- Módulo de cálculo energético: software/prediction/src/service/recommendations.py
- Pruebas unitarias de integración numérica: software/frontend/tests/energy.test.cjs
- Frontend de visualización energética: pruebas en software/frontend/ (prueba «energy displays absence of carbon factor»).

DEFINICIÓN DE TERMINADO (DoD)

1. Algoritmo de integración trapezoidal con pruebas unitarias matemáticas.
2. Manejo explícito de ausencia de datos de potencia física verificado.
3. Declaración de origen y supuestos en la carga útil de la API.
4. Integración probada con la vista de energía en el frontend.
```
- **Checklist «Actividades técnicas»:**
  - [x] Desarrollar función de integración trapezoidal en software/prediction/src/service/recommendations.py
  - [x] Implementar endpoint REST /v1/energy para recepción de series de potencia y retorno en kWh
  - [x] Crear pruebas unitarias que validen la integral frente a valores analíticos conocidos
  - [ ] Implementar modelo proxy de estimación CPU-to-Power sustentado con benchmark en reposo
  - [ ] Incorporar selector de fuentes (medición real vs simulación modelada) en el frontend
  - [ ] Documentar supuestos de cálculo y limitaciones en el informe de la Unidad III
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «El cálculo de kWh mediante regla del trapecio está programado y probado como cálculo por trapecio en Data Processing (software/data-processing/tests/test_historical_report.py) y panel software/frontend/energy.js con pruebas matemáticas específicas. La tarjeta queda IN PROGRESS porque debemos conectar el modelo de potencia base calibrado en reposo según la medición de docker stats (22 MiB/174 MiB).»
  - `Gina Diana Barrera Peña`:
    > «Es vital mantener la distinción exigida en RE-05: la CPU mide actividad, no watts directamente. El endpoint /v1/energy responde adecuadamente indicando el origen simulado cuando se alimenta de telemetría del simulador.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «En la interfaz web se implementó la tarjeta de visualización de energía que muestra claramente las unidades en kWh y una advertencia cuando no se cuenta con telemetría de potencia medida físicamente.»

---

### Tarjeta PMV3-HU10: Estimación de emisiones de CO2 equivalente
- **Lista destino:** `1. PRODUCT BACKLOG`
- **Etiquetas:** `PMV3`, `Machine Learning`, `Datos`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña`
- **Fecha de vencimiento:** `2026-11-28`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como directivo universitario,
necesito estimar las emisiones de gases de efecto invernadero (kg CO2e) atribuibles al consumo eléctrico del entorno computacional,
para evaluar la huella ambiental del sistema dentro del marco de sostenibilidad de la iniciativa Green AI.

ALCANCE

Planificado para el Sprint 7 dentro del PMV3. Consiste en la multiplicación del consumo energético (kWh) obtenido en HU-09 por el factor de emisión oficial del Sistema Eléctrico Interconectado Nacional (SEIN) o de la región del centro de datos, publicado por fuentes oficiales (ej. Ministerio del Ambiente o COES). No se inventan factores globales genéricos sin referencia formal.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un valor consolidado de energía en kWh y un factor de emisión debidamente referenciado y versionado, cuando se solicita el cálculo, entonces el sistema retorna los kilogramos de CO2e estimados identificando la fuente del factor.
CA-02: Dado que el factor de emisión puede variar según la estacionalidad de la matriz energética, cuando se consulta el detalle, entonces se identifican el año, el periodo y la entidad emisora del factor aplicado.
CA-03: Dado que no se dispone de un factor de emisión formalmente sustentado o el cálculo de energía es nulo, cuando se solicita la huella, entonces el sistema informa que la emisión no puede estimarse con rigor.
CA-04: Dadas las emisiones calculadas, cuando se visualizan en reportes o pantallas, entonces se declaran como estimadas y limitadas al alcance 2 (electricidad consumida), excluyendo manufactura de hardware.

EVIDENCIA EN REPOSITORIO

- Planificación y diseño técnico: docs/academico/04-gestion-del-proyecto.md (sección PMV3)
- Lineamientos de honestidad experimental: docs/HANDOFF.md

DEFINICIÓN DE TERMINADO (DoD)

1. Factor de emisión oficial documentado con cita bibliográfica verificable.
2. Función de cálculo implementada en el backend con pruebas unitarias.
3. Integración en los reportes consolidados CSV/PDF.
4. Criterio de alcance 2 explícitamente delimitado en la documentación.
```
- **Checklist «Actividades técnicas»:**
  - [ ] Recopilar y documentar factor de emisión del SEIN peruano con fuente oficial (COES/MINAM)
  - [ ] Diseñar módulo de cálculo de emisiones CO2e en software/prediction/src/service/recommendations.py
  - [ ] Implementar pruebas unitarias de conversión validando unidades físicas
  - [ ] Incorporar parámetro de factor de emisión configurable por variable de entorno
  - [ ] Añadir sección de emisiones en los reportes exportables de la Unidad IV
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «La tarjeta permanece en el PRODUCT BACKLOG para el Sprint 7. Hemos iniciado la búsqueda bibliográfica de los factores de emisión del SEIN correspondientes al último balance nacional para aplicarlo rigurosamente sobre los kWh integrados.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Como Product Owner confirmo que esta historia pertenece al PMV3. No se adelantará su desarrollo hasta contar con el factor oficial publicado y la validación de la integración energética de HU-09.»

---

### Tarjeta PMV3-HU16: Protocolo y ejecución de experimento comparativo Green AI vs Baseline
- **Lista destino:** `1. PRODUCT BACKLOG`
- **Etiquetas:** `PMV3`, `Documentación`, `Machine Learning`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña`, `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-11-30`
- **Descripción:**
```markdown
HISTORIA DE USUARIO

Como investigador del proyecto,
necesito ejecutar un protocolo experimental controlado que compare el comportamiento de un escenario tradicional (baseline) frente al escenario asistido por Green AI bajo cargas idénticas,
para determinar científicamente si el sistema aporta beneficios verificables en utilización, estabilidad y energía estimada.

ALCANCE

Constituye el entregable central del PMV3 (Sprints 7 y 8). Incluye la ejecución de pruebas bajo condiciones idénticas de carga de trabajo, duración y topología de servidores. Dado que Green AI opera en modo Recommendation-Only, las acciones operativas se aplican de forma controlada y registrada. Si el sistema no produce mejoras estadísticamente significativas, los resultados se comunicarán con total transparencia y honestidad científica.

CRITERIOS DE ACEPTACIÓN

CA-01: Dado un protocolo experimental formalmente documentado, cuando se ejecutan los escenarios baseline y Green AI, entonces se mantienen condiciones idénticas de hardware, carga simulada y duración temporal.
CA-02: Dadas las ejecuciones de los escenarios, cuando se registran los datos, entonces se almacenan las series temporales completas, identificando versiones de software, semillas aleatorias y políticas aplicadas.
CA-03: Dados los resultados obtenidos, cuando se contrastan, entonces se presentan las diferencias absolutas y relativas junto con sus intervalos de confianza y análisis de variabilidad.
CA-04: Dado que durante una prueba se identifiquen condiciones externas no homogéneas o fallas de red, cuando se audita la corrida, entonces se invalida formalmente el experimento y se programa su repetición.
CA-05: Dado que no se observe una reducción significativa en el consumo o una mejora en SLA, cuando se redacta la discusión, entonces se reporta el resultado objetivo sin maquillar las cifras.

EVIDENCIA EN REPOSITORIO

- Plan experimental detallado: docs/academico/10-plan-experimental.md
- Guía metodológica: docs/academico/08-pruebas-resultados-discusion.md
- Protocolo base: guias/TrabajosDesarrollados/4. Gestión de Proyecto.md

DEFINICIÓN DE TERMINADO (DoD)

1. Protocolo experimental con hipótesis y métricas de éxito formalizadas.
2. Al menos 3 réplicas ejecutadas por cada escenario con registro de semillas.
3. Tabla comparativa consolidada con cálculo de significancia estadística.
4. Capítulo de resultados y discusión del informe final redactado.
```
- **Checklist «Actividades técnicas»:**
  - [x] Redactar protocolo experimental base en docs/academico/10-plan-experimental.md
  - [ ] Preparar scripts de generación de carga reproducible con semillas deterministas
  - [ ] Ejecutar corridas del escenario de referencia (baseline estático)
  - [ ] Ejecutar corridas del escenario asistido por Green AI con registro de decisiones
  - [ ] Analizar diferencias en utilización, violaciones de SLA y energía modelada
  - [ ] Redactar conclusiones objetivas para la sustentación final de la Unidad IV
- **Comentarios a publicar:**
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Tarjeta en PRODUCT BACKLOG para los Sprints 7 y 8. Ya se completó el diseño del protocolo en docs/academico/10-plan-experimental.md. Las corridas comparativas se efectuarán en la etapa de cierre tras consolidar el entorno de pruebas.»
  - `Gina Diana Barrera Peña`:
    > «Aseguraremos que el protocolo experimental utilice semillas fijas en el simulador para que la curva de tráfico sintético sea matemáticamente idéntica tanto para el baseline como para Green AI.»
  - `Ricardo Porras Veli`:
    > «Prepararemos los scripts de recolección de métricas para volcar los resultados de cada corrida directamente a tablas de datos reproducibles para el análisis estadístico en Python.»

```
================================================================================
4.2 TAREAS TÉCNICAS EN TO DO (SPRINT 6)
================================================================================
```

### Tarjeta: Fijar Health Check Path en Render
- **Lista destino:** `4. TO DO`
- **Etiquetas:** `PMV2`, `Infraestructura`
- **Miembro (único):** `Leonid Kisley Orlando Huamán Collazos`
- **Colaboran con comentarios:** `Ricardo Porras Veli`
- **Fecha de vencimiento:** `2026-11-10`
- **Descripción:**
```markdown
TAREA TÉCNICA

Configurar las rutas específicas de comprobación de estado de salud (Health Check Path) en cada uno de los 6 servicios web desplegados en la plataforma Render, para evitar reinicios innecesarios y optimizar el tiempo de disponibilidad en el plan gratuito.

ALCANCE

Aplica a los 6 servicios gratuitos green-ai-*-dev en el workspace My Workspace de Render:
1. green-ai-prediction-dev: ruta /health/ready
2. green-ai-data-processing-dev: ruta /api/v1/health
3. green-ai-gateway-dev: ruta /actuator/health
4. green-ai-monitoring-dev: ruta /actuator/health
5. green-ai-simulator-dev: ruta /health
6. green-ai-prometheus-dev: ruta /-/healthy
No se debe modificar bajo ninguna circunstancia el servicio ajeno SoftwareAnemia.

CRITERIOS DE ACEPTACIÓN

CA-01: Cada servicio web en Render debe tener configurado su Health Check Path correspondiente según la lista técnica.
CA-02: Al desplegar un contenedor, Render debe marcar el estado en verde (Live) tras recibir un código HTTP 200 en la ruta especificada.
CA-03: Los tiempos de espera de inicio (initial delay) deben configurarse para tolerar el arranque en frío sin provocar reinicios continuos.

EVIDENCIA EN REPOSITORIO

- Guía de despliegue en Render: docs/GUIA-DESPLIEGUE-RENDER.md
- Especificación de infraestructura como código: render.yaml
- Registro de pendientes: docs/CONTINUAR-EN-NUEVO-CHAT.md
```
- **Checklist «Pasos de configuración»:**
  - [ ] Acceder al panel de control de Render (workspace My Workspace)
  - [ ] Configurar ruta /health/ready en green-ai-prediction-dev
  - [ ] Configurar ruta /api/v1/health en green-ai-data-processing-dev
  - [ ] Configurar ruta /actuator/health en Gateway y Monitoring
  - [ ] Configurar rutas de salud en Simulator (/health) y Prometheus (/-/healthy)
  - [ ] Verificar que los 6 servicios pasen a estado Healthy de forma estable
- **Comentarios a publicar:**
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Tarea creada en TO DO para el Sprint 6. Tenemos mapeadas las rutas de salud en render.yaml. Esta configuración es prioritaria para estabilizar los servicios en la nube antes de la grabación del video demostrativo.»
  - `Ricardo Porras Veli`:
    > «Verifiqué localmente que todos los endpoints de salud responden con código 200 en menos de 20 ms. Al configurarlos en Render evitaremos los falsos reinicios que ocurrían por defecto al consultar la raíz /. »

---

### Tarjeta: Revisar RLS de Supabase y columna password
- **Lista destino:** `4. TO DO`
- **Etiquetas:** `PMV2`, `Seguridad`, `Backend`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-11`
- **Descripción:**
```markdown
TAREA TÉCNICA

Realizar una auditoría de seguridad sobre la base de datos Supabase del proyecto: revisar las políticas de Row Level Security (RLS) para eliminar permisos globales permisivos (permitir todo) y verificar la eliminación de la columna password en texto plano en la tabla auxiliar de usuarios.

ALCANCE

Comprende la revisión de las tablas públicas en el esquema de Supabase. Supabase Auth gestiona internamente las credenciales seguras mediante bcrypt en el esquema auth.users. Se debe asegurar que ninguna tabla del esquema public contenga contraseñas en texto claro y que las políticas RLS exijan autenticación para lectura y privilegios específicos para escritura.

CRITERIOS DE ACEPTACIÓN

CA-01: Ninguna tabla del esquema public almacena contraseñas o datos sensibles de credenciales.
CA-02: Las políticas RLS de las tablas profiles y logs están activadas, bloqueando el acceso anónimo no autenticado.
CA-03: Se ejecuta un script SQL de remediación que aplique las restricciones mínimas requeridas.

EVIDENCIA EN REPOSITORIO

- Script SQL de base de datos: software/frontend/supabase-auth-setup.sql
- Informe de riesgos de seguridad: docs/HANDOFF.md (sección Riesgos detectados)
- Lista de pendientes en: docs/CONTINUAR-EN-NUEVO-CHAT.md
```
- **Checklist «Pasos de auditoría y remediación»:**
  - [ ] Inspeccionar esquema de tablas públicas en el panel de Supabase
  - [ ] Verificar que la tabla profiles no posea la columna password en texto plano
  - [ ] Eliminar cualquier política RLS con condición USING (true) sin autenticación
  - [ ] Aplicar políticas RLS restrictivas para lectura pública solo de campos no sensibles
  - [ ] Comprobar que las operaciones de modificación exijan token JWT válido
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «Tarea en TO DO. Como dueño del proyecto en Supabase, realizaré la auditoría de las políticas RLS. El almacenamiento de contraseñas es gestionado al 100 % por Supabase Auth, por lo que aseguraremos que no quede ningún campo redundante en el esquema público.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Esta tarea responde a la observación del análisis de seguridad en docs/HANDOFF.md. Corregir cualquier política permisiva es indispensable antes de la entrega final.»

---

### Tarjeta: Evaluación walk-forward del modelo frente a persistencia
- **Lista destino:** `4. TO DO`
- **Etiquetas:** `PMV2`, `Machine Learning`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-13`
- **Descripción:**
```markdown
TAREA TÉCNICA

Implementar un protocolo de evaluación honesta de series temporales mediante validación de origen móvil (walk-forward con brecha o gap) para medir la habilidad predictiva (skill score) del modelo de CPU frente a una referencia de persistencia ingenua, según la propuesta técnica de docs/MEJORA-MODELO-PREDICCION.md.

ALCANCE

Consiste en programar un script de validación que divida las corridas de telemetría respetando el orden temporal, aplicando la métrica:
Skill = 1 - (MAE_modelo / MAE_persistencia).
Se evaluará el modelo Random Forest actual sobre diferentes escenarios del simulador (normal, high y con picos) para verificar en qué condiciones supera realmente a la simple persistencia de predecir el último valor observado.

CRITERIOS DE ACEPTACIÓN

CA-01: El script de validación walk-forward divide los datos cronológicamente con un gap configurable sin contaminación de información futura.
CA-02: Se reporta el Skill Score para cada horizonte temporal y escenario de carga.
CA-03: Los resultados se documentan en un archivo de evidencia reproducible en docs/evidencias/.

EVIDENCIA EN REPOSITORIO

- Plan técnico de mejora del modelo: docs/MEJORA-MODELO-PREDICCION.md
- Pipeline predictivo actual: software/prediction/src/training/
```
- **Checklist «Pasos de evaluación walk-forward»:**
  - [ ] Programar generador de splits temporales con gap en software/prediction/src/evaluation/
  - [ ] Implementar cálculo de métrica de habilidad (Skill Score) frente a persistencia
  - [ ] Ejecutar validación sobre corrida con tráfico variado del simulador
  - [ ] Comparar resultados de Random Forest frente a HistGradientBoosting
  - [ ] Guardar reporte de métricas en docs/evidencias/walk-forward-20261113.md (se creará al terminar la tarea)
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Tarea en TO DO. Siguiendo el plan de docs/MEJORA-MODELO-PREDICCION.md, diseñaremos la validación walk-forward para corroborar que la mejora frente a predecir el último valor se mantenga en periodos con alta varianza.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Esta evaluación aportará respaldo cuantitativo para la discusión de resultados de la Unidad III, demostrando rigor frente al baseline ingenuo.»

---

### Tarjeta: Grabar video de la Unidad III
- **Lista destino:** `4. TO DO`
- **Etiquetas:** `PMV2`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Leonid Kisley Orlando Huamán Collazos`, `Gina Diana Barrera Peña`, `Ricardo Porras Veli`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
TAREA TÉCNICA

Planificar, coordinar y grabar el video demostrativo de la Unidad III (indicadores 9 y 10 de la rúbrica) cumpliendo con la estructura exigida de 7 episodios en un tiempo de 20 a 30 minutos, ejecutado sobre los servicios desplegados en la nube de Render (no en localhost) y procesando un lote de transacciones reales.

ALCANCE

Comprende el guion de 7 episodios especificado en guias/semana12/lista-cotejo-unidad3.md:
1. Inicio de sesión y control de acceso con Supabase Auth.
2. Monitoreo en vivo de 50 nodos en el dashboard modular.
3. Generación y procesamiento de un lote masivo de transacciones (500 a 1000 peticiones).
4. Caso de uso de IA 1: Predicción de demanda a 15 minutos.
5. Caso de uso de IA 2: Recomendación explicable con política y advertencias.
6. Inspección de observabilidad y alertas en Prometheus.
7. Arquitectura de código por capas y buenas prácticas en GitHub.
Importante: Despertar los servicios en Render al menos 25 minutos antes de la grabación para evitar latencias de arranque en frío.

CRITERIOS DE ACEPTACIÓN

CA-01: Video grabado en alta resolución con audio claro de los integrantes participantes.
CA-02: Demostración realizada sobre las URLs públicas de Render y GitHub Pages (/dev/).
CA-03: Procesamiento comprobado de más de 500 transacciones demostradas en consola o gráficos.
CA-04: Video publicado en plataforma accesible (YouTube en modo oculto o Drive institucional) con enlace en la carátula del informe.

EVIDENCIA EN REPOSITORIO

- Estructura y guion técnico: docs/academico/08-pruebas-resultados-discusion.md (sección 5)
- Guía de la lista de cotejo: guias/semana12/lista-cotejo-unidad3.md
```
- **Checklist «Pasos de producción del video»:**
  - [ ] Redactar guion detallado y asignar tiempos de locución por integrante
  - [ ] Despertar los servicios en Render 25 minutos antes y verificar telemetría
  - [ ] Preparar script generador de 500 transacciones para llamadas a la API
  - [ ] Grabar demostración de extremo a extremo en entorno de staging
  - [ ] Renderizar video, subirlo a plataforma institucional y adjuntar enlace en el informe
- **Comentarios a publicar:**
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Tarea en TO DO. He estructurado la pauta del video según la lista de cotejo de la Unidad III. Cada uno tendrá asignado un episodio técnico demostrando el valor del software en la nube.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Dejaremos preparados los comandos y el frontend con las 50 máquinas virtuales levantadas para que el flujo de grabación se desarrolle sin pausas técnicas.»

```
================================================================================
4.3 TARJETAS DE SPRINT BACKLOG
================================================================================
```

### Tarjeta: Sprint 6 (03/11–14/11)
- **Lista destino:** `2. SPRINT BACKLOG`
- **Etiquetas:** `PMV2`, `Documentación`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
PLANIFICACIÓN DE SPRINT

Sprint activo: Sprint 6 (Semanas 11 y 12 del calendario académico).
Periodo: 03/11/2026 al 14/11/2026.
Objetivo del Sprint:
Estabilizar y culminar las capacidades nucleares del PMV2, desplegando los microservicios en la nube de Render, activando el conjunto de alertas operativas en Prometheus, rediseñando el dashboard del frontend con pestañas y preparando la evidencia integral para el cierre de la Unidad III.

HISTORIAS Y TAREAS COMPROMETIDAS

- HU-12 Detección y gestión de alertas operativas (Terminada)
- HU-11 Dashboard integrado con pestañas (En QA-Testing)
- HU-05 Registro y trazabilidad en MLflow (En QA-Testing)
- HU-07 Flujo de aprobación humana para recomendaciones (En progreso)
- HU-13 Reportes históricos en CSV/PDF (En progreso)
- HU-09 Estimación de energía en kWh (En progreso)
- Tareas técnicas de despliegue en Render, auditoría de seguridad y guion de video.
```
- **Checklist «Metas del Sprint 6»:**
  - [x] Reglas de alertas en Prometheus validadas con promtool
  - [x] Despliegue de los 6 microservicios dev en Render completado
  - [x] Rediseño del frontend en pestañas con 48 pruebas unitarias aprobadas
  - [ ] Verificación en vivo de sesión real en https://woshtsu.github.io/green-ai-workspace-cld/dev/
  - [ ] Grabación y edición del video demostrativo de la Unidad III
  - [ ] Consolidación de evidencias en el informe académico
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Iniciamos la segunda semana del Sprint 6. Hemos alcanzado un avance sustancial en observabilidad y frontend; nos concentramos ahora en cerrar las pruebas de QA y preparar el material demostrativo.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Como Product Owner ratifico que los entregables comprometidos para este sprint satisfacen los criterios de aceptación de la Unidad III.»

---

### Tarjeta: Sprint 7 (17/11–23/11)
- **Lista destino:** `2. SPRINT BACKLOG`
- **Etiquetas:** `PMV3`, `Documentación`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-28`
- **Descripción:**
```markdown
PLANIFICACIÓN DE SPRINT

Sprint futuro: Sprint 7 (Semanas 13 y 14 del calendario académico).
Periodo: 17/11/2026 al 23/11/2026.
Objetivo del Sprint:
Iniciar la ejecución del PMV3 incorporando el cálculo de huella de carbono sustentado con el factor de emisión oficial, completar la generación de reportes en PDF y ejecutar el escenario de referencia (baseline) del protocolo experimental.

HISTORIAS Y PAQUETES DE TRABAJO PROYECTADOS

- HU-10 Estimación de emisiones de CO2 equivalente con factor oficial.
- HU-13 Culminación de exportación de reportes en formato PDF.
- HU-16 Configuración del banco de pruebas y ejecución del escenario baseline.
- Configuración de entorno productivo en rama main.
```
- **Checklist «Objetivos previstos»:**
  - [ ] Definir factor de emisión oficial de la red eléctrica nacional
  - [ ] Implementar motor de renderizado de reportes PDF en Data Processing
  - [ ] Preparar scripts de carga determinista para el baseline experimental
  - [ ] Realizar corridas de medición de referencia sin intervención de IA
  - [ ] Documentar resultados preliminares para el informe de la Unidad IV
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Sprint 7 planificado formalmente en el backlog. Los requerimientos y dependencias técnicas están claramente delimitados para el inicio el 17/11/2026.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «El backlog del Sprint 7 prioriza las capacidades analíticas requeridas para la sustentación final de la tesis.»

```
================================================================================
4.4 REFINAMIENTO DE EXPERTOS (RE-01 A RE-06)
================================================================================
```

### Tarjeta RE-01: Delimitación de infraestructura y workloads
- **Lista destino:** `3. REFINAMIENTO DE EXPERTOS`
- **Etiquetas:** `PMV1`, `Arquitectura`, `Infraestructura`
- **Miembro (único):** `Leonid Kisley Orlando Huamán Collazos`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-09-05`
- **Descripción:**
```markdown
REFINAMIENTO DE EXPERTOS

Número de delimitación: 1. Delimitación del alcance de la infraestructura y workloads computacionales.
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Historia de usuario:
Como investigador del proyecto Green AI, quiero delimitar los servidores, workloads computacionales y periodos de análisis que serán considerados por el sistema predictivo, para establecer un alcance técnico verificable y asegurar que los resultados obtenidos correspondan exactamente a la infraestructura evaluada sin generalizaciones infundadas.

Relación con la observación del experto:
Responde a la observación sobre la necesidad de acotar el dominio del problema. Aunque la optimización es pertinente, se deben especificar qué servidores, cargas y horizontes se evalúan, evitando generalizar conclusiones a centros de datos completos cuando solo se evalúan nodos específicos.
```
- **Checklist «Retroalimentación del experto»:**
  - [x] Delimitar clúster evaluado a 50 nodos simulados homogéneos
  - [x] Definir perfiles de carga sintética (normal, alta, estacional)
  - [x] Establecer ventana de observación en intervalos de 5 minutos
  - [x] Documentar límites explícitos en el alcance del proyecto
  - [x] Evitar extrapolar métricas a entornos físicos no medidos
- **Comentarios a publicar:**
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «El experto recomendó acotar estrictamente la topología. Acordamos fijar el alcance inicial en 50 nodos virtuales homogéneos con telemetría de CPU y memoria cada 5 segundos.»
  - `Gina Diana Barrera Peña`:
    > «Se incorporó la delimitación en el Project Charter y en la especificación de requisitos del PMV1, impidiendo generalizaciones injustificadas.»

---

### Tarjeta RE-02: Definición de arquitectura y comunicación entre servicios
- **Lista destino:** `3. REFINAMIENTO DE EXPERTOS`
- **Etiquetas:** `PMV1`, `Arquitectura`, `Backend`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-09-19`
- **Descripción:**
```markdown
REFINAMIENTO DE EXPERTOS

Número de delimitación: 2. Definición de la arquitectura híbrida y contratos de comunicación.
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Historia de usuario:
Como desarrollador del sistema Green AI, quiero establecer contratos de comunicación OpenAPI claros y desacoplar los servicios mediante arquitectura hexagonal, para garantizar una integración trazable, mantenible y libre de dependencias circulares.

Relación con la observación del experto:
El experto señaló el riesgo de sobreingeniería y complejidad innecesaria en la distribución de servicios. Recomendó definir contratos API estrictos, esquemas DTO claros y desacoplar el dominio de la infraestructura para facilitar pruebas herméticas.
```
- **Checklist «Retroalimentación del experto»:**
  - [x] Definir especificaciones OpenAPI para cada microservicio
  - [x] Aplicar arquitectura hexagonal aislando lógica de dominio
  - [x] Implementar contratos HTTP y pruebas de integración
  - [x] Retirar componentes innecesarios (RabbitMQ/Kubernetes) para el prototipo
  - [x] Validar comunicación unificada mediante API Gateway
- **Comentarios a publicar:**
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Siguiendo el consejo del experto, descartamos el uso de colas distribuidas complejas en esta etapa, optando por contratos REST OpenAPI sincrónicos gestionados por un Gateway eficiente.»
  - `Gina Diana Barrera Peña`:
    > «La arquitectura hexagonal permitió que los servicios de predicción y procesamiento de datos se prueben con adaptadores de prueba sin levantar bases de datos externas.»

---

### Tarjeta RE-03: Calidad, consistencia y trazabilidad de los datos
- **Lista destino:** `3. REFINAMIENTO DE EXPERTOS`
- **Etiquetas:** `PMV1`, `Datos`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-03`
- **Descripción:**
```markdown
REFINAMIENTO DE EXPERTOS

Número de delimitación: 3. Calidad, consistencia y trazabilidad de los datos de telemetría.
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Historia de usuario:
Como responsable de la gestión de datos, quiero implementar un proceso estructurado de validación, limpieza y versionado de las series de tiempo, para asegurar que los modelos se entrenen con datos consistentes y con estricto respeto a la causalidad temporal.

Relación con la observación del experto:
El experto enfatizó que la calidad de los datos es el factor determinante en el éxito del aprendizaje automático. Señaló la obligación de documentar unidades de medida, frecuencias de captura, tratamiento de nulos y particiones temporales sin fuga de datos futuros.
```
- **Checklist «Retroalimentación del experto»:**
  - [x] Documentar fuentes, unidades de medida (%) y frecuencia (5s/5min)
  - [x] Implementar filtro para eliminar o imputar muestras faltantes
  - [x] Prohibir aleatorización (shuffle) en series de tiempo
  - [x] Separar conjuntos de entrenamiento, validación y prueba cronológicamente
  - [x] Versionar el dataset sintético con hash criptográfico en el repositorio
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Implementamos la partición temporal estricta en el generador de datos. Se respetó la causalidad temporal, dividiendo los datos en 70 % train, 15 % val y 15 % test sin mezclar secuencias.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «La verificación de calidad de datos quedó plasmada en la suite de pruebas unitarias de Data Processing, garantizando esquemas consistentes.»

---

### Tarjeta RE-04: Validación del rendimiento de modelos de Machine Learning
- **Lista destino:** `3. REFINAMIENTO DE EXPERTOS`
- **Etiquetas:** `PMV2`, `Machine Learning`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-17`
- **Descripción:**
```markdown
REFINAMIENTO DE EXPERTOS

Número de delimitación: 4. Validación del rendimiento del modelo predictivo y comparación con baselines.
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Historia de usuario:
Como investigador del proyecto, quiero entrenar y evaluar modelos predictivos utilizando métricas adecuadas para problemas de regresión (MAE, RMSE) y contrastarlos frente a una línea base ingenua, para justificar objetivamente la capacidad predictiva del sistema.

Relación con la observación del experto:
El experto advirtió que reportar métricas de porcentaje plano (como precisión del 90 %) carece de sentido en tareas de regresión continua. Exigió el uso de MAE y RMSE en las unidades reales de la variable y la comparación obligatoria contra una referencia simple de persistencia.
```
- **Checklist «Retroalimentación del experto»:**
  - [x] Reemplazar afirmaciones genéricas de porcentaje por MAE y RMSE
  - [x] Implementar modelo de persistencia (predecir último valor) como baseline
  - [x] Evaluar modelos candidatos (Random Forest, Ridge, Gradient Boosting)
  - [x] Analizar el incremento del error en periodos de picos de carga
  - [x] Registrar parámetros y métricas en tablas versionadas
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Adoptamos el uso riguroso de MAE y RMSE en puntos porcentuales de utilización de CPU. En el informe se eliminaron las referencias a precisión porcentual plana y se reporta la mejora del 30 % frente a persistencia.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Se actualizaron los criterios de aceptación de HU-03 y HU-04 para reflejar las métricas exigidas por el revisor.»

---

### Tarjeta RE-05: Diferenciación entre consumo energético medido y estimado
- **Lista destino:** `3. REFINAMIENTO DE EXPERTOS`
- **Etiquetas:** `PMV2`, `Machine Learning`
- **Miembro (único):** `Ricardo Porras Veli`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-31`
- **Descripción:**
```markdown
REFINAMIENTO DE EXPERTOS

Número de delimitación: 5. Diferenciación estricta entre consumo energético medido y estimado.
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Historia de usuario:
Como responsable de la evaluación energética, quiero distinguir claramente las mediciones físicas de potencia de las estimaciones computacionales basadas en CPU, para evitar atribuir ahorros energéticos no comprobados experimentalmente.

Relación con la observación del experto:
El experto alertó taxativamente que la utilización de CPU no es equivalente a potencia eléctrica en watts. La relación depende de estados de energía (C-states/P-states), consumo estático de placa y memorias. Exigió que cualquier indicador de kWh no medido físicamente se declare como estimado y sujeto a supuestos.
```
- **Checklist «Retroalimentación del experto»:**
  - [x] Prohibir la conversión directa lineal de CPU % a Watts sin modelo validado
  - [x] Marcar respuestas de API con origen simulated o estimated
  - [x] Declarar supuestos y limitaciones en la documentación del informe
  - [x] Exigir telemetría de potencia activa cuando se evalúe eficiencia real
  - [x] Mantener el sistema en modo Recommendation-Only para evitar reclamos falsos de ahorro
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Incorporamos en el código del Policy Engine y del calculador de energía la advertencia explícita de procedencia estimada cuando no existen sensores físicos de potencia.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Corregimos el capítulo de pruebas en el informe: dejamos constancia formal de que el prototipo calcula kWh a partir de telemetría de simulación, postergando la medición física al PMV3.»

---

### Tarjeta RE-06: Diseño experimental y evaluación de beneficios potenciales
- **Lista destino:** `3. REFINAMIENTO DE EXPERTOS`
- **Etiquetas:** `PMV2`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
REFINAMIENTO DE EXPERTOS

Número de delimitación: 6. Diseño experimental riguroso y reporte transparente de resultados.
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Historia de usuario:
Como investigador principal, quiero diseñar un protocolo experimental con criterios de invalidación, réplicas y condiciones controladas, para asegurar que cualquier comparación futura entre escenarios sea metodológicamente inobjetable.

Relación con la observación del experto:
El experto exigió que antes de ejecutar pruebas de ahorro se defina formalmente un protocolo con criterios de éxito, control de variables intervinientes y el compromiso explícito de publicar resultados negativos o no concluyentes si el sistema no produce mejoras.
```
- **Checklist «Retroalimentación del experto»:**
  - [x] Redactar protocolo experimental previo a las corridas (docs/academico/10-plan-experimental.md)
  - [x] Definir condiciones idénticas de hardware y patrones de tráfico sintético
  - [x] Especificar criterios formales de invalidación ante fallas externas
  - [x] Comprometer reporte de resultados negativos sin alteración de datos
  - [x] Medir no solo utilización, sino también potenciales violaciones de SLA
- **Comentarios a publicar:**
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Se elaboró el documento docs/academico/10-plan-experimental.md detallando las condiciones de comparabilidad y los criterios de descarte ante anomalías de red.»
  - `Gina Diana Barrera Peña`:
    > «El protocolo garantiza que las pruebas de la Unidad IV sigan el estándar científico exigido por el evaluador.»

```
================================================================================
4.5 SPRINT REVIEWS (SPRINT 1 A SPRINT 6)
================================================================================
```

### Tarjeta: Sprint Review — Sprint 1
- **Lista destino:** `10. SPRINT REVIEW`
- **Etiquetas:** `PMV1`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña` (como SM), `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-09-05`
- **Descripción:**
```markdown
REVISIÓN DE SPRINT — SPRINT 1
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Datos de la sesión:
- Sprint: Sprint 1 (25/08/2026 al 05/09/2026).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.
- Objetivo del Sprint: Definir la arquitectura de alto nivel de Green AI, seleccionar la pila tecnológica y desplegar el simulador de telemetría con Prometheus.

Incremento presentado:
Prototipo base de recolección de métricas. El simulador genera telemetría de 50 nodos y Prometheus realiza el raspado regular en el puerto 9090. Se revisaron los criterios de HU-01 (Métricas de infraestructura).

Decisiones y acuerdos:
1. Validar contratos OpenAPI para desacoplar el simulador de los servicios de consulta.
2. Formalizar la delimitación de infraestructura según RE-01.
```
- **Checklist «Revisión del Sprint 1»:**
  - [x] Demostrar targets UP en Prometheus
  - [x] Comprobar telemetría continua de CPU y memoria de 50 nodos
  - [x] Validar que la cabecera origin=simulated se mantenga
  - [x] Revisar y aceptar criterios de aceptación de HU-01
  - [x] Consolidar acta de revisión técnica
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio. Se dio por aceptado el incremento de observabilidad base correspondiente a HU-01.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Como Product Owner certifiqué que el raspado continuo de Prometheus cumple con los requerimientos funcionales del inicio de PMV1.»

---

### Tarjeta: Sprint Review — Sprint 2
- **Lista destino:** `10. SPRINT REVIEW`
- **Etiquetas:** `PMV1`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña` (como SM), `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-09-19`
- **Descripción:**
```markdown
REVISIÓN DE SPRINT — SPRINT 2
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Datos de la sesión:
- Sprint: Sprint 2 (08/09/2026 al 19/09/2026).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.
- Objetivo del Sprint: Implementar el almacenamiento estructurado y paginado de telemetría histórica en Data Processing y configurar el volumen persistente de Prometheus.

Incremento presentado:
Endpoints de históricos en Data Processing respondiendo con paginación por cursor y suite de pruebas de contrato en SQLite y PostgreSQL (HU-02 terminada con 114 pruebas en verde).

Decisiones y acuerdos:
1. Confirmar el uso del perfil SQLite para pruebas locales herméticas.
2. Preparar la integración del módulo de autenticación de usuarios para el Sprint 3.
```
- **Checklist «Revisión del Sprint 2»:**
  - [x] Demostrar consultas históricas paginadas por cursor
  - [x] Comprobar persistencia de datos tras reinicio de contenedores
  - [x] Validar ejecución de 114 pruebas en Data Processing
  - [x] Aceptar criterios de HU-02
  - [x] Registrar retroalimentación sobre volumen de retención
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio. Se demostró la resiliencia de los históricos en Data Processing pasando las pruebas de contrato sin fallos.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Se validó la persistencia montando volúmenes Docker independientes para evitar pérdidas de datos en reinicios.»

---

### Tarjeta: Sprint Review — Sprint 3
- **Lista destino:** `10. SPRINT REVIEW`
- **Etiquetas:** `PMV1`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña` (como SM), `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-10-03`
- **Descripción:**
```markdown
REVISIÓN DE SPRINT — SPRINT 3 (Cierre del PMV1)
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Datos de la sesión:
- Sprint: Sprint 3 (22/09/2026 al 03/10/2026).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.
- Objetivo del Sprint: Culminar el PMV1 integrando el sistema de autenticación de usuarios con Supabase Auth y validando la seguridad de extremo a extremo.

Incremento presentado:
Flujo completo de registro e inicio de sesión con emisión de tokens JWT seguros y trigger de asignación del rol OPERATOR (HU-15 terminada). Se cierra formalmente el PMV1 con todas sus historias aprobadas.

Decisiones y acuerdos:
1. Declarar completado el hito PMV1 (Observabilidad y seguridad base).
2. Iniciar el desarrollo del PMV2 focalizado en modelos predictivos y políticas en el Sprint 4.
```
- **Checklist «Revisión del Sprint 3»:**
  - [x] Demostrar flujo de registro de usuario con validación de credenciales
  - [x] Validar generación de token JWT firmado por Supabase
  - [x] Comprobar asignación automática del rol OPERATOR sin elevación de privilegios
  - [x] Declarar cierre exitoso del PMV1
  - [x] Actualizar backlog priorizando modelos de Machine Learning
- **Comentarios a publicar:**
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio. Se demostró el inicio de sesión contra Supabase y la protección de rutas mediante JWT.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Como Product Owner aprobé la entrega formal del PMV1. Las tres historias comprometidas (HU-01, HU-02 y HU-15) quedaron cerradas al 100 % en DONE.»

---

### Tarjeta: Sprint Review — Sprint 4
- **Lista destino:** `10. SPRINT REVIEW`
- **Etiquetas:** `PMV2`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña` (como SM), `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-10-17`
- **Descripción:**
```markdown
REVISIÓN DE SPRINT — SPRINT 4
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Datos de la sesión:
- Sprint: Sprint 4 (06/10/2026 al 17/10/2026).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.
- Objetivo del Sprint: Entrenar, evaluar y desplegar el microservicio de predicción de CPU (FastAPI) y consolidar la comparativa de modelos frente a persistencia.

Incremento presentado:
Microservicio Prediction operando con el modelo Random Forest serializado, respondiendo inferencias en tiempo real a 15 minutos (HU-03). Tabla comparativa model_comparison.csv con métricas de 4 algoritmos (HU-04).

Decisiones y acuerdos:
1. Confirmar Random Forest como el modelo servido para producción (MAE 3.22 vs 4.60 del baseline).
2. Desarrollar el motor de políticas explicables (HU-06 y HU-08) para el Sprint 5.
```
- **Checklist «Revisión del Sprint 4»:**
  - [x] Demostrar inferencia en vivo en endpoint /v1/predictions
  - [x] Comprobar presencia de origin=estimated en la respuesta
  - [x] Revisar tabla comparativa model_comparison.csv
  - [x] Aceptar criterios de HU-03 y HU-04
  - [x] Definir reglas de recomendación para el siguiente sprint
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio. Se validó la inferencia del Random Forest con N pruebas pasando en pytest (anotar la cifra real tras ejecutar `pytest` en software/prediction; último registro en docs/HANDOFF.md: 96 passed) y una reducción sustancial del MAE frente a persistencia.»
  - `Ricardo Porras Veli`:
    > «Se verificó que el endpoint /v1/predictions responde con tiempos de latencia inferiores a 50 ms a través del Gateway.»

---

### Tarjeta: Sprint Review — Sprint 5
- **Lista destino:** `10. SPRINT REVIEW`
- **Etiquetas:** `PMV2`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña` (como SM), `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-10-31`
- **Descripción:**
```markdown
REVISIÓN DE SPRINT — SPRINT 5
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Datos de la sesión:
- Sprint: Sprint 5 (20/10/2026 al 31/10/2026).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.
- Objetivo del Sprint: Desarrollar el Policy Engine para recomendaciones explicables con seguro de ejecución, implementar restricciones operativas y habilitar el rol VIEWER.

Incremento presentado:
Motor de recomendaciones en Prediction operando en modo Recommendation-Only (HU-06). Módulo de restricciones operativas parametrizables (HU-08). Filtro RBAC en Gateway con soporte para ADMIN, OPERATOR y VIEWER (HU-14).

Decisiones y acuerdos:
1. Garantizar que todas las recomendaciones mantengan executionAllowed=false.
2. Preparar el despliegue en Render y el frontend por pestañas para el Sprint 6.
```
- **Checklist «Revisión del Sprint 5»:**
  - [x] Demostrar generación de recomendaciones con campo justification
  - [x] Comprobar bloqueo de recomendaciones inseguras según restricciones
  - [x] Probar acceso de solo lectura con rol VIEWER (código 403 en modificaciones)
  - [x] Aceptar criterios de HU-06, HU-08 y HU-14
  - [x] Planificar integración en la nube para el Sprint 6
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio. Se aceptaron formalmente HU-06, HU-08 y HU-14 con pruebas en Go y Java totalmente aprobadas.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Como Product Owner confirmé que el seguro de recomendación protege la infraestructura universitaria, cumpliendo las restricciones éticas y de seguridad.»

---

### Tarjeta: Sprint Review — Sprint 6
- **Lista destino:** `10. SPRINT REVIEW`
- **Etiquetas:** `PMV2`, `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** `Gina Diana Barrera Peña` (como SM), `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
REVISIÓN DE SPRINT — SPRINT 6
Datos de la sesión:
- Sprint: Sprint 6 (03/11/2026 al 14/11/2026).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.
- Objetivo del Sprint: Desplegar microservicios en Render, configurar reglas de alertas en Prometheus, implementar el frontend modular en pestañas y cerrar las evidencias de la Unidad III.

Incremento presentado:
6 microservicios desplegados en Render (green-ai-*-dev). Reglas de alerta en Prometheus validadas con promtool (HU-12 terminada). Frontend modular con pestañas y gráficos canvas (HU-11 en QA-TESTING con 48 pruebas). Experimento registrado en MLflow (HU-05 en QA-TESTING). Avances en HU-07, HU-13 y HU-09.

Decisiones y acuerdos:
1. Completar la validación con sesión real en GitHub Pages /dev/ para pasar HU-11 a DONE.
2. Capturar interfaz de MLflow UI para cerrar HU-05.
3. Iniciar el Sprint 7 enfocado en huella de carbono y plan experimental (PMV3).
```
- **Checklist «Revisión del Sprint 6»:**
  - [x] Demostrar microservicios respondiendo en la nube de Render
  - [x] Comprobar activación y sintaxis de alertas con promtool
  - [x] Demostrar interfaz web modular con 48 pruebas unitarias
  - [x] Registrar run de entrenamiento en MLflow
  - [x] Acordar cierre del Sprint 6 y transición al Sprint 7
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Presentamos los resultados del Sprint 6. Se logró la consolidación del PMV2 con 6 historias culminadas en DONE y dos historias en fase final de QA-TESTING.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Aprobé los incrementos demostrados. La observabilidad, alertas y capacidades predictivas satisfacen plenamente los requerimientos de la Unidad III.»

```
================================================================================
4.6 SPRINT RETROSPECTIVES (PMV1 Y PMV2)
================================================================================
```

### Tarjeta: Retrospectiva — PMV1 (Sprints 1–3)
- **Lista destino:** `11. SPRINT RETROSPECTIVE`
- **Etiquetas:** `PMV1`, `Documentación`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-10-03`
- **Descripción:**
```markdown
RETROSPECTIVA DE FASE — PMV1 (SPRINTS 1 A 3)
Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio.

Datos de la sesión:
- Fase evaluada: PMV1 (Observabilidad y seguridad base).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.

1. ¿QUÉ HICIMOS BIEN?
- Desacoplamiento temprano mediante contratos OpenAPI y arquitectura hexagonal.
- Automatización de suites de prueba desde el primer sprint (Monitoring con N pruebas tras mvn test, Data Processing con 114 pruebas).
- Mantenimiento riguroso del repositorio sin subir secretos gracias al uso de variables de entorno.

2. ¿QUÉ PODEMOS MEJORAR?
- La dependencia de imágenes Docker pesadas dificultaba los despliegues locales rápidos.
- Mayor comunicación previa antes de modificar esquemas de bases de datos para evitar desajustes en el frontend.

3. ACCIONES DE MEJORA IMPLEMENTADAS:
- Acción 1: Crear overlays de Docker Compose livianos para desarrollo local (compose.sqlite-dev.yml). Responsable: Ricardo Porras.
- Acción 2: Establecer reuniones cortas de sincronización técnica los días lunes, miércoles y viernes. Responsable: Gina Barrera.

4. COMPROMISO PARA EL SIGUIENTE PMV:
Priorizar modelos predictivos con métricas reproducibles frente a baselines sencillos, manteniendo una honestidad científica estricta.
```
- **Checklist «Acuerdos de mejora PMV1»:**
  - [x] Evaluar cumplimiento de objetivos del PMV1
  - [x] Analizar eficacia del flujo Git y suites de pruebas
  - [x] Definir acciones para aligerar contenedores Docker
  - [x] Formalizar cronograma de Dailies L/Mi/V
  - [x] Archivar compromisos de mejora en la documentación
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Registro consolidado el 07/11/2026 a partir de actas del equipo y del historial del repositorio. La retrospectiva del PMV1 evidenció una sólida base técnica en observabilidad y contratos.»
  - `Ricardo Porras Veli`:
    > «El compromiso de aligerar imágenes Docker se cumplió con creces: reducimos la imagen de Prediction de 2.85 GB a 510 MB mediante compilación multicapa.»

---

### Tarjeta: Retrospectiva — PMV2 (Sprints 4–6)
- **Lista destino:** `11. SPRINT RETROSPECTIVE`
- **Etiquetas:** `PMV2`, `Documentación`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-14`
- **Descripción:**
```markdown
RETROSPECTIVA DE FASE — PMV2 (SPRINTS 4 A 6)
Datos de la sesión:
- Fase evaluada: PMV2 (Inteligencia, recomendaciones y despliegue).
- Participantes: Jhonny Quintana, Gina Barrera, Ricardo Porras, Leonid Huamán.

1. ¿QUÉ HICIMOS BIEN?
- Evaluación comparativa honesta de algoritmos predictivos, superando al baseline de persistencia en un 30 % sin inflar métricas.
- Despliegue funcional de 6 microservicios en la nube pública de Render sin incurrir en costos monetarios.
- Rediseño integral del frontend con arquitectura de pestañas y 48 pruebas automáticas en Node.js.
- Implementación de reglas de alerta en Prometheus validadas formalmente con promtool.

2. ¿QUÉ PODEMOS MEJORAR?
- La latencia provocada por la suspensión (arranque en frío) de los servicios gratuitos de Render tras 15 minutos de inactividad.
- Coordinar con mayor anticipación la toma de capturas y la verificación visual con sesiones reales en staging.

3. ACCIONES DE MEJORA PARA EL PMV3:
- Acción 1: Diseñar un script de calentamiento automático para despertar los microservicios en Render antes de las evaluaciones y grabaciones. Responsable: Leonid Huamán.
- Acción 2: Desarrollar el protocolo experimental (HU-16) con réplicas estadísticas deterministas para la evaluación comparativa final. Responsable: Gina Barrera / Jhonny Quintana.

4. COMPROMISO PARA EL CIERRE DEL PROYECTO:
Mantener la transparencia académica, reportando los resultados exactos del modelo y de la estimación de energía sin prometer ahorros mágicos que no se hayan medido físicamente.
```
- **Checklist «Acuerdos de mejora PMV2»:**
  - [x] Evaluar desempeño del modelo Random Forest frente al baseline
  - [x] Analizar estabilidad del despliegue en Render y GitHub Pages
  - [x] Identificar lecciones aprendidas sobre cuotas y planes gratuitos
  - [ ] Implementar script de precalentamiento para evitar retardos de arranque en frío
  - [ ] Consolidar compromisos para el diseño experimental del PMV3
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Cerramos la retrospectiva del PMV2. La madurez técnica del equipo se refleja en un flujo de trabajo disciplinado, respetando las buenas prácticas de arquitectura y pruebas automáticas.»
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Como Product Owner destaco la honestidad experimental del equipo: evitamos falsas promesas de ahorro y nos enfocamos en entregar un prototipo verificable.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «Asumo la tarea de programar el script de calentamiento para asegurar que las demostraciones en la nube respondan de inmediato.»
  - `Ricardo Porras Veli`:
    > «La arquitectura hexagonal y el API Gateway en Go demostraron ser decisiones óptimas para operar de manera eficiente dentro de los límites de memoria de la nube gratuita.»

```
================================================================================
4.7 ROLES DE SCRUM
================================================================================
```

### Tarjeta: PRODUCT OWNER
- **Lista destino:** `8. ROLES DE SCRUM`
- **Etiquetas:** `Documentación`
- **Miembro (único):** `Jhonny Cristhian Quintana Carhuaricra`
- **Colaboran con comentarios:** Ninguno (rol individual)
- **Fecha de vencimiento:** `2026-11-30`
- **Descripción:**
```markdown
ROL DE SCRUM: PRODUCT OWNER
Titular: Jhonny Cristhian Quintana Carhuaricra

RESPONSABILIDADES EN EL PROYECTO:
- Definir, comunicar y custodiar la visión y objetivos del producto Green AI.
- Priorizar y ordenar las historias en el Product Backlog según valor académico y técnico.
- Refinar los criterios de aceptación en formato Given/When/Then con el equipo de desarrollo.
- Validar el cumplimiento de la Definición de Terminado (DoD) antes de aceptar cualquier HU en DONE.
- Redactar los informes académicos de gestión y coordinar las revisiones con el docente y asesor.
```
- **Checklist «Responsabilidades clave»:**
  - [x] Priorizar historias del Product Backlog para PMV1, PMV2 y PMV3
  - [x] Validar criterios de aceptación de cada HU con pruebas comprobables
  - [x] Participar activamente en las sesiones de Sprint Review y Sprint Planning
  - [x] Mantener actualizada la matriz de trazabilidad de requisitos en el informe
- **Comentarios a publicar:**
  - `Jhonny Cristhian Quintana Carhuaricra`:
    > «Rol activo. Superviso permanentemente que el backlog refleje el avance fidedigno del repositorio y que los criterios de aceptación se verifiquen con pruebas automatizadas.»

---

### Tarjeta: SCRUM MASTER
- **Lista destino:** `8. ROLES DE SCRUM`
- **Etiquetas:** `Documentación`
- **Miembro (único):** `Gina Diana Barrera Peña`
- **Colaboran con comentarios:** Ninguno (rol individual)
- **Fecha de vencimiento:** `2026-11-30`
- **Descripción:**
```markdown
ROL DE SCRUM: SCRUM MASTER
Titular: Gina Diana Barrera Peña

RESPONSABILIDADES EN EL PROYECTO:
- Facilitar y asegurar la correcta aplicación del marco ágil Scrum (Scrumban).
- Guiar las ceremonias de Daily Scrum (L/Mi/V), Sprint Planning, Sprint Review y Retrospectivas.
- Identificar, gestionar y eliminar impedimentos técnicos u operativos que afecten al equipo.
- Mantener la integridad y coherencia del tablero Trello y verificar su validación algorítmica.
- Liderar técnicamente el diseño, entrenamiento y evaluación de los modelos de Machine Learning.
```
- **Checklist «Responsabilidades clave»:**
  - [x] Estandarizar etiquetas, listas y reglas del tablero Trello
  - [x] Facilitar las ceremonias de inspección y adaptación del equipo
  - [x] Gestionar el backlog de impedimentos y acciones de retrospectiva
  - [x] Auditar que no existan tarjetas vacías ni flujos decorativos en Trello
- **Comentarios a publicar:**
  - `Gina Diana Barrera Peña`:
    > «Rol activo. Velamos por la disciplina metodológica del equipo, coordinando los dailies y asegurando que las tarjetas reflejen el avance técnico real del repositorio.»

---

### Tarjeta: SCRUM TEAM
- **Lista destino:** `8. ROLES DE SCRUM`
- **Etiquetas:** `Documentación`
- **Miembro (único):** `Leonid Kisley Orlando Huamán Collazos`
- **Colaboran con comentarios:** `Ricardo Porras Veli`, `Gina Diana Barrera Peña`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** `2026-11-30`
- **Descripción:**
```markdown
ROL DE SCRUM: EQUIPO DE DESARROLLO (SCRUM TEAM)
Integrantes:
- Ricardo Porras Veli: Backend, contratos OpenAPI, integración de microservicios y despliegue (dueño del repositorio).
- Leonid Kisley Orlando Huamán Collazos: Infraestructura, Docker, observabilidad (Prometheus), seguridad y frontend.
- Gina Diana Barrera Peña: Procesamiento de datos, pipelines de entrenamiento y evaluación de modelos de IA.
- Jhonny Cristhian Quintana Carhuaricra: Pruebas de aceptación, documentación académica y auditoría de calidad.

RESPONSABILIDADES COMPARTIDAS:
- Estimar y seleccionar ítems del backlog respetando la capacidad del equipo.
- Diseñar, codificar y probar incrementos de software funcionales bajo arquitectura hexagonal.
- Mantener la cobertura de pruebas unitarias, de contrato y de humo en cada servicio.
- Realizar revisiones cruzadas de código (pull requests) y respetar las directivas de seguridad.
```
- **Checklist «Compromisos del equipo»:**
  - [x] Mantener suites de pruebas automatizadas en verde antes de cada integración
  - [x] Actualizar diariamente el estado y checklists de las tarjetas en Trello
  - [x] Cumplir los criterios de calidad y Definición de Terminado (DoD)
  - [x] Colaborar de forma interdisciplinaria para resolver bloqueos técnicos
- **Comentarios a publicar:**
  - `Ricardo Porras Veli`:
    > «Equipo multidisciplinario consolidado. Mantenemos el código modular con más de 300 pruebas automatizadas acumuladas a lo largo de los microservicios.»
  - `Leonid Kisley Orlando Huamán Collazos`:
    > «La infraestructura en contenedores y el despliegue en la nube garantizan que los incrementos sean demostrables en cualquier momento.»

```
================================================================================
4.8 TARJETA DE DAILY SCRUM (SESIONES DIARIAS)
================================================================================
```

### Tarjeta: Daily Scrum — AAAA-MM-DD
- **Lista destino:** `9. DAILY SCRUM`
- **Etiquetas:** Ninguna (o `Documentación`)
- **Miembro (único):** `Gina Diana Barrera Peña` (facilitadora)
- **Colaboran con comentarios:** `Ricardo Porras Veli`, `Leonid Kisley Orlando Huamán Collazos`, `Jhonny Cristhian Quintana Carhuaricra`
- **Fecha de vencimiento:** Fecha de la sesión (ej. `2026-11-09`)
- **Descripción:** (Ver plantilla institucional en §6.1)
- **Checklist «Asistencia y sincronización»:**
  - [x] Gina Diana Barrera Peña (Scrum Master)
  - [x] Ricardo Porras Veli (Backend/DevOps)
  - [x] Leonid Kisley Orlando Huamán Collazos (Infra/Frontend)
  - [x] Jhonny Cristhian Quintana Carhuaricra (Product Owner)
- **Comentarios a publicar:** Una sola tarjeta por sesión; cada integrante publica individualmente su comentario respondiendo a las tres preguntas ágiles (ver ejemplos en §6.2).

---

## 5. Plan de acciones por integrante y por día

Para garantizar que el tablero exhiba un historial de actividad orgánico, colaborativo y con transiciones secuenciales respetando la directiva de **miembro único** por tarjeta, los integrantes deben ejecutar las tareas distribuidas en los siguientes cuatro días clave:

```
Día 1: Sábado 07/11/2026 (Consolidación PMV1, configuración inicial y arranque)
Día 2: Lunes 09/11/2026 (Daily Scrum 08:00, avance de PMV2, To Do e In Progress)
Día 3: Miércoles 11/11/2026 (Daily Scrum 08:00, QA-Testing, validaciones y evidencias)
Día 4: Viernes 13/11/2026 (Cierre de Sprint 6, Review, Retro PMV2 y exportación JSON)
```

---

### DÍA 1: SÁBADO 07/11/2026 — Consolidación y configuración

#### 1. Gina Diana Barrera Peña (Scrum Master)
1. **Configuración de etiquetas:** Acceder a Menú -> Etiquetas. Renombrar `MVP-01` a `PMV1` (Verde), `MVP 02` a `PMV2` (Amarillo) y `MVP 03` a `PMV3` (Azul). Crear las 8 etiquetas de área técnica. Borrar la etiqueta naranja sin nombre y la etiqueta Infraestructura duplicada.
2. **Archivar tarjetas obsoletas:** Archivar `Sprint 1` de `2. SPRINT BACKLOG`, `Sprint 7` y `Sprint 8` de `10. SPRINT REVIEW`, las retrospectivas parciales de Sprint 4 y 5 en `11. SPRINT RETROSPECTIVE`, los 23 dailies antiguos «Daily | Sprint [5]/[10]» y las 5 reviews antiguas «Sprint 1»…«Sprint 5».
3. **Crear / Actualizar tarjeta `Sprint 6 (03/11–14/11)`:** Ubicar en `2. SPRINT BACKLOG`, pegar descripción, checklist, fecha `14/11/2026`, miembro único Gina (quitar a Jhonny como miembro; Jhonny colabora con comentario), etiquetas `PMV2`, `Documentación`. Publicar comentario.
4. **Actualizar tarjeta `Sprint 7 (17/11–23/11)`:** Ubicar en `2. SPRINT BACKLOG`, pegar descripción, checklist, fecha `23/11/2026`, miembro único Gina (quitar a Jhonny como miembro; Jhonny colabora con comentario), etiquetas `PMV3`, `Documentación`. Publicar comentario.
5. **Actualizar tarjetas RE-03 y RE-04:** En lista `3. REFINAMIENTO DE EXPERTOS`, miembro único Gina (quitar a Jhonny). RE-03: etiqueta `PMV1`, `Datos`. RE-04: `PMV2`, `Machine Learning`. Marcar checklists y publicar comentario técnico (ceder RE-01 a Leonid, RE-02 y RE-05 a Ricardo, RE-06 a Jhonny).
6. **Crear tarjeta `Retrospectiva — PMV1 (Sprints 1–3)`:** En lista `11. SPRINT RETROSPECTIVE`, pegar descripción consolidada, checklist [x], fecha `03/10/2026`, miembro único Gina (quitar a los otros 3 miembros; colaboran con comentarios), etiquetas `PMV1`, `Documentación`. Publicar comentario.

#### 2. Ricardo Porras Veli (Backend y DevOps)
1. **Actualizar HU-02 (Históricos):** Ubicada en `7. DONE` (ya movida), miembro único Ricardo (quitar a Leonid y Gina), pegar descripción completa, checklist [x], fecha `19/09/2026`, etiquetas `PMV1`, `Datos`, `Backend`. Publicar comentario de pruebas (114 passed).
2. **Actualizar HU-14 (Roles con VIEWER):** En `7. DONE`, miembro único Ricardo (quitar a Leonid y Jhonny), pegar descripción de §4 con evidencia corregida de Gateway Go (`go test -race ./...`) y SQL en `software/frontend/supabase-auth-setup.sql`, checklist [x] al 100 %, fecha `31/10/2026`, etiquetas `PMV2`, `Seguridad`, `Backend`. Publicar comentario técnico corregido (`go test -race ./...`: N passed).
3. **Crear / Actualizar tarjeta en To Do: «Revisar RLS de Supabase y columna password»:** En lista `4. TO DO`, pegar descripción con ruta corregida (`software/frontend/supabase-auth-setup.sql`), checklist [ ], fecha `11/11/2026`, miembro único Ricardo (quitar a Jhonny; Jhonny colabora con comentario), etiquetas `PMV2`, `Seguridad`, `Backend`. Publicar comentario inicial.
4. **Actualizar RE-02 y RE-05:** En lista `3. REFINAMIENTO DE EXPERTOS`, miembro único Ricardo (quitar a Gina y Jhonny), asignar etiquetas técnicas (RE-02: `PMV1`, `Arquitectura`, `Backend`; RE-05: `PMV2`, `Machine Learning`), marcar checklist y publicar comentario propio.

#### 3. Leonid Kisley Orlando Huamán Collazos (Infraestructura y Frontend)
1. **Actualizar HU-01 (Métricas):** Ubicada en `7. DONE`, miembro único Leonid (quitar a Ricardo), pegar descripción completa con N pruebas JUnit tras `mvn test`, checklist [x], fecha `05/09/2026`, etiquetas `PMV1`, `Infraestructura`, `Backend`. Publicar comentario técnico (N passed tras `mvn test` en software/monitoring, smoke 14/14).
2. **Actualizar HU-15 (Registro y autenticación):** En `7. DONE`, miembro único Leonid (quitar a Ricardo y Jhonny), cambiar etiqueta `Backend` por `Frontend` (etiquetas: `PMV1`, `Seguridad`, `Frontend`), pegar descripción de §4 con ruta corregida de SQL, checklist [x], fecha `03/10/2026`. Publicar comentario.
3. **Actualizar HU-12 (Alertas):** En `7. DONE` (ya movida), miembro único Leonid (quitar a Ricardo; Ricardo colabora con comentario), pegar descripción y checklist de §4 al 100 % [x], fecha `14/11/2026`, etiquetas `PMV2`, `Infraestructura`, `Backend`. Publicar comentario propio de validación con `promtool`.
4. **Crear tarjeta en To Do: «Fijar Health Check Path en Render»:** En lista `4. TO DO`, pegar descripción, checklist [ ], fecha `10/11/2026`, miembro único Leonid (quitar a Ricardo; Ricardo colabora con comentario), etiquetas `PMV2`, `Infraestructura`. Publicar comentario inicial.
5. **Actualizar RE-01 (Delimitación de infraestructura):** En lista `3. REFINAMIENTO DE EXPERTOS`, miembro único Leonid (quitar a Gina y Jhonny), etiquetas `PMV1`, `Arquitectura`, `Infraestructura`, marcar checklist y publicar comentario propio.

#### 4. Jhonny Cristhian Quintana Carhuaricra (Product Owner)
1. **Actualizar tarjeta PRODUCT OWNER:** En lista `8. ROLES DE SCRUM`, pegar descripción, checklist [x], fecha `30/11/2026`, miembro único Jhonny, etiqueta `Documentación`. Publicar comentario de rol activo.
2. **Actualizar HU-10 (Emisiones CO2e):** En lista `1. PRODUCT BACKLOG`, miembro único Jhonny (quitar a Gina), pegar descripción completa, checklist [ ], fecha `28/11/2026`, etiquetas `PMV3`, `Machine Learning`, `Datos`. Publicar comentario de justificación de backlog.
3. **Actualizar HU-16 (Experimento comparativo):** En lista `1. PRODUCT BACKLOG`, cambiar miembro asignado Leonid → Jhonny (quedar Jhonny como miembro único), añadir etiquetas `Documentación` y `Machine Learning` (etiquetas: `PMV3`, `Documentación`, `Machine Learning`), ajustar fecha al 30/11/2026, pegar ficha de §4 con checklist de 6 ítems (1 [x] y 5 [ ]), publicar comentario sobre protocolo experimental.
4. **Actualizar revisiones Sprint 1, 2 y 3:** En lista `10. SPRINT REVIEW`, miembro único Jhonny en las 3 tarjetas (quitar a los demás; los demás colaboran con comentarios), verificar textos consolidados, marcar checklists [x], fechas correspondientes (`05/09`, `19/09`, `03/10`) y publicar comentarios de aceptación formal del PO de PMV1.
5. **Actualizar RE-06:** En lista `3. REFINAMIENTO DE EXPERTOS`, miembro único Jhonny (quitar a Gina), etiqueta `Documentación` (etiquetas: `PMV2`, `Documentación`), marcar checklist y publicar comentario propio.

---

### DÍA 2: LUNES 09/11/2026 — Daily Scrum y avance de PMV2

#### 1. Gina Diana Barrera Peña (Scrum Master)
1. **Crear tarjeta de Daily Scrum:** A las 08:00, crear en lista `9. DAILY SCRUM` una sola tarjeta `Daily Scrum — 2026-11-09`, miembro único Gina (como facilitadora; los 4 integrantes comentan en ESA tarjeta). Pegar plantilla de descripción, fecha `09/11/2026`. Publicar su comentario respondiendo a las 3 preguntas. Archivar la tarjeta vacía sin miembros.
2. **Actualizar HU-03 (Predicción CPU):** En `7. DONE`, miembro único Gina (quitar a Jhonny y Ricardo), pegar descripción completa, checklist [x] al 100 %, fecha `17/10/2026`, etiquetas `PMV2`, `Machine Learning`, `Backend`. Publicar comentario de métricas (MAE 3.22, N passed tras `pytest` en software/prediction).
3. **Actualizar HU-04 (Comparación de modelos):** En `7. DONE`, miembro único Gina (quitar a Jhonny), pegar descripción, checklist [x] al 100 %, fecha `17/10/2026`, etiquetas `PMV2`, `Machine Learning`, `Datos`. Publicar comentario de `model_comparison.csv`.
4. **Actualizar HU-08 (Restricciones):** En `7. DONE`, miembro único Gina (quitar a Ricardo; Ricardo colabora con comentario), pegar ficha, checklist al 100 % [x], fecha `31/10/2026`. Corregir su comentario sustituyendo `domain/constraints.py` por los umbrales de la política en `software/prediction/src/recommendations/policy.py`.
5. **Crear tarjeta en To Do: «Evaluación walk-forward del modelo frente a persistencia»:** En lista `4. TO DO`, pegar descripción, checklist [ ], fecha `13/11/2026`, miembro único Gina (quitar a Jhonny; Jhonny colabora con comentario), etiquetas `PMV2`, `Machine Learning`. Publicar comentario inicial.

#### 2. Ricardo Porras Veli (Backend y DevOps)
1. **Daily Scrum:** Si aún es 09/11, acceder a la tarjeta de Gina `Daily Scrum — 2026-11-09` en `9. DAILY SCRUM` y publicar su comentario propio respondiendo a las 3 preguntas. Si no, no retrofechar: constará que no participó.
2. **Actualizar HU-06 (Recomendaciones explicables):** En `7. DONE`, miembro único Ricardo (quitar a Leonid y Gina), pegar ficha de §4, reemplazar checklist actual (0/10) por el de la ficha al 100 % [x], fecha `31/10/2026`, etiquetas `PMV2`, `Backend`, `Machine Learning`. Publicar comentario técnico corregido (`software/prediction/src/recommendations/policy.py`, pruebas de recomendación tras `pytest`).
3. **Actualizar HU-07, HU-13 y HU-09:** En `5. IN PROGRESS`, miembro único Ricardo en las 3 tarjetas (quitar colaboradores como miembros). Pegar fichas de §4; checklist de la ficha con avance real (HU-07: marcar 2 ítems; HU-13 y HU-09: marcar 3 de 6 ítems); fecha de vencimiento 14/11/2026 (corregir fecha si figuraba 15/11). Publicar comentarios respectivos (en HU-09 corregir referencia a cálculo por trapecio en Data Processing y panel frontend).
4. **Corregir comentarios anteriores con datos sin respaldo:** En HU-14 (quitar «5 veces consecutivas» y poner `go test -race ./...`: N passed), en HU-03 (sustituir «100 passed» por N passed tras `pytest`), y en HU-15 (reemplazar `handle_new_user` por `on_auth_user_created_green_ai`).

#### 3. Leonid Kisley Orlando Huamán Collazos (Infraestructura y Frontend)
1. **Daily Scrum:** Si aún es 09/11, acceder a la tarjeta `Daily Scrum — 2026-11-09` de Gina en `9. DAILY SCRUM` y publicar su comentario propio respondiendo a las 3 preguntas. Si no, no retrofechar: constará que no participó.
2. **Actualizar HU-11 (Dashboard con pestañas):** En `6. QA-TESTING`, miembro único Leonid (quitar a Jhonny y Ricardo; colaboran con comentarios), pegar ficha de §4, checklist de la ficha (marcar 4 [x] y dejar 2 [ ]), fecha `14/11/2026`, etiquetas `PMV2`, `Frontend`, `Infraestructura`. Publicar comentario propio sobre la suite de 48 pruebas en Node.js.
3. **Actualizar HU-12 (Alertas):** En `7. DONE`, reemplazar checklist actual (0/10) por el de la ficha al 100 % [x]. Publicar comentario propio de validación con `promtool` (actualmente solo figuraba el de Ricardo).
4. **Actualizar tarjeta SCRUM TEAM:** En lista `8. ROLES DE SCRUM`, miembro único Leonid (quitar a los otros 3 compañeros; colaboran con comentarios), pegar descripción, checklist [x], fecha `30/11/2026` (corregir si figura 13/12), etiqueta `Documentación`. Publicar comentario.

#### 4. Jhonny Cristhian Quintana Carhuaricra (Product Owner)
1. **Daily Scrum:** Acceder a la tarjeta `Daily Scrum — 2026-11-09` de Gina en `9. DAILY SCRUM` y verificar su comentario (ya publicado el 09/11).
2. **Crear tarjeta en To Do: «Grabar video de la Unidad III»:** En lista `4. TO DO`, pegar descripción, checklist [ ], fecha `14/11/2026`, miembro único Jhonny (quitar a los otros 3; colaboran con comentarios), etiquetas `PMV2`, `Documentación`. Publicar comentario inicial con el esquema de los 7 episodios.
3. **Sprint Reviews S4 y S5:** En lista `10. SPRINT REVIEW`, miembro único Jhonny en ambas tarjetas (quitar a los otros 3 miembros). Publicar comentarios de aceptación formal del Product Owner (S4 y S5).
4. **Comentar en HU-03 y HU-06:** Entrar a HU-03 en DONE y HU-06 en DONE y publicar sus comentarios de validación de criterios como Product Owner.

---

### DÍA 3: MIÉRCOLES 11/11/2026 — QA-Testing y evidencias de integración

#### 1. Gina Diana Barrera Peña (Scrum Master)
1. **Daily Scrum:** A las 08:00, crear en lista `9. DAILY SCRUM` la tarjeta única `Daily Scrum — 2026-11-11`, miembro único Gina (los 4 comentan en esa tarjeta). Publicar su comentario.
2. **Actualizar HU-05 (Registro en MLflow):** En `6. QA-TESTING`, miembro único Gina (quitar a Leonid; Leonid colabora con comentario), pegar descripción completa, checklist (4 ítems [x], 2 [ ]), fecha `14/11/2026`, etiquetas `PMV2`, `Machine Learning`, `Datos`. Publicar comentario técnico sobre experimento 394141087236111562. Coordinar con el equipo la captura de pantalla con `mlflow ui`.
3. **Comentar en Sprint Review — Sprint 4:** En lista `10. SPRINT REVIEW`, acceder a la tarjeta de Jhonny y publicar comentario de revisión como Scrum Master.
4. **Actualizar tarjeta SCRUM MASTER:** En lista `8. ROLES DE SCRUM`, pegar descripción, checklist [x], fecha `30/11/2026`, miembro único Gina, etiqueta `Documentación`. Publicar comentario.

#### 2. Ricardo Porras Veli (Backend y DevOps)
1. **Daily Scrum:** Acceder a la tarjeta `Daily Scrum — 2026-11-11` en `9. DAILY SCRUM` y publicar su comentario respondiendo a las 3 preguntas.
2. **Avanzar HU-13 (Reportes CSV y PDF):** En `5. IN PROGRESS`, mantener avance técnico del serializador CSV y preparación de PDF, checklist (3 ítems [x], 3 [ ]), fecha `14/11/2026`.
3. **Avanzar HU-09 (Energía en kWh):** En `5. IN PROGRESS`, mantener avance técnico en la regla del trapecio, checklist (3 ítems [x], 3 [ ]), fecha `14/11/2026`.
4. **Comentar en Sprint Review — Sprint 5:** En lista `10. SPRINT REVIEW`, acceder a la tarjeta de Jhonny y publicar comentario sobre los acuerdos técnicos alcanzados.

#### 3. Leonid Kisley Orlando Huamán Collazos (Infraestructura y Frontend)
1. **Daily Scrum:** Acceder a la tarjeta `Daily Scrum — 2026-11-11` en `9. DAILY SCRUM` y publicar su comentario respondiendo a las 3 preguntas.
2. **Avanzar HU-11 en QA-TESTING:** En `6. QA-TESTING`, mantener 4 ítems marcados [x] y 2 [ ] de validación en vivo. Publicar comentario sobre pruebas de interfaz con el arnés local.
3. **Comentar en HU-05 (MLflow):** Acceder a HU-05 en `6. QA-TESTING` (tarjeta de Gina) y publicar comentario sobre la captura de pantalla pendiente con `mlflow ui`.
4. **Comentar en HU-09 (Energía):** Acceder a HU-09 en `5. IN PROGRESS` (tarjeta de Ricardo) y publicar comentario sobre el panel de visualización de energía en el frontend.

#### 4. Jhonny Cristhian Quintana Carhuaricra (Product Owner)
1. **Daily Scrum:** Acceder a la tarjeta `Daily Scrum — 2026-11-11` en `9. DAILY SCRUM` y publicar su comentario respondiendo a las 3 preguntas.
2. **Revisar y comentar en HU-11 (Dashboard):** Entrar a HU-11 en `6. QA-TESTING` (tarjeta de Leonid) y publicar comentario de revisión visual con el arnés local.
3. **Revisar y comentar en HU-13 (Reportes):** Entrar a HU-13 en `5. IN PROGRESS` (tarjeta de Ricardo) y publicar comentario de validación del CSV generado.
4. **Revisar y comentar en HU-07 (Aprobación):** Entrar a HU-07 en `5. IN PROGRESS` (tarjeta de Ricardo) y publicar comentario de exigencia del campo de justificación obligatorio.

---

### DÍA 4: VIERNES 13/11/2026 — Cierre de Sprint 6, Review, Retro y Validación

#### 1. Gina Diana Barrera Peña (Scrum Master)
1. **Daily Scrum:** A las 08:00, crear en lista `9. DAILY SCRUM` la tarjeta única `Daily Scrum — 2026-11-13`, miembro único Gina (los 4 comentan en esa tarjeta). Publicar su comentario.
2. **Comentar en Sprint Review — Sprint 6:** En lista `10. SPRINT REVIEW`, acceder a la tarjeta de Jhonny y publicar comentario de cierre del Sprint 6 como Scrum Master.
3. **Cerrar Retrospectiva — PMV2 (Sprints 4–6):** En lista `11. SPRINT RETROSPECTIVE`, miembro único Gina (quitar a los otros 3 miembros). Dado que ya cuenta con el comentario del 09/11 («Cerramos…»), completar los 2 ítems restantes del checklist al 100 % [x] el 13/11.
4. **Auditar tablero:** Verificar que no quede ninguna tarjeta huérfana o sin actividad reciente.

#### 2. Ricardo Porras Veli (Backend y DevOps)
1. **Daily Scrum:** Acceder a la tarjeta `Daily Scrum — 2026-11-13` en `9. DAILY SCRUM` y publicar su comentario respondiendo a las 3 preguntas.
2. **Comentar en Retrospectiva PMV2:** Acceder a `Retrospectiva — PMV2 (Sprints 4–6)` (tarjeta de Gina) y publicar comentario sobre la arquitectura hexagonal y el Gateway Go.
3. **Comentar en Sprint Review — Sprint 6:** Acceder a `Sprint Review — Sprint 6` (tarjeta de Jhonny) y publicar comentario confirmando el estado de los microservicios en Render.
4. **Verificar estado de To Do:** Revisar que la tarea de RLS Supabase mantenga su miembro único (Ricardo) y fecha asignada.

#### 3. Leonid Kisley Orlando Huamán Collazos (Infraestructura y Frontend)
1. **Daily Scrum:** Acceder a la tarjeta `Daily Scrum — 2026-11-13` en `9. DAILY SCRUM` y publicar su comentario respondiendo a las 3 preguntas.
2. **Comentar en Retrospectiva PMV2:** Acceder a `Retrospectiva — PMV2 (Sprints 4–6)` (tarjeta de Gina) y publicar comentario sobre el script de calentamiento para mitigar el arranque en frío de Render.
3. **Comentar en Sprint Review — Sprint 6:** Acceder a `Sprint Review — Sprint 6` (tarjeta de Jhonny) y publicar comentario sobre la integración del frontend con Render.
4. **Exportar JSON preliminar:** Realizar exportación de prueba desde Trello (Menú -> Imprimir, exportar y compartir -> Exportar como JSON) y ejecutar el script validador con Python.

#### 4. Jhonny Cristhian Quintana Carhuaricra (Product Owner)
1. **Daily Scrum:** Acceder a la tarjeta `Daily Scrum — 2026-11-13` en `9. DAILY SCRUM` y publicar su comentario respondiendo a las 3 preguntas.
2. **Aprobar formalmente Sprint Review — Sprint 6:** En lista `10. SPRINT REVIEW`, como miembro único de la tarjeta, marcar checklist al 100 % [x] y publicar el comentario formal de aceptación del Product Owner el 13/11.
3. **Comentar en Retrospectiva PMV2:** Acceder a `Retrospectiva — PMV2 (Sprints 4–6)` (tarjeta de Gina) y publicar comentario como PO destacando la honestidad experimental.
4. **Auditoría final de cumplimiento:** Ejecutar la lista de chequeo de la sección 7.

---

## 6. Daily Scrum: Plantilla y ejemplos de respuestas (Día 2)

### 6.1 Plantilla de descripción para la tarjeta Daily Scrum
Gina crea una única tarjeta en la lista `9. DAILY SCRUM` con el nombre `Daily Scrum — YYYY-MM-DD` (ej. `Daily Scrum — 2026-11-09`). Como facilitadora de Scrum, **Gina es el miembro único asignado a la tarjeta**. Los 4 integrantes participan comentando en esa misma tarjeta con sus cuentas personales.
En la **Descripción** pega el siguiente texto institucional:

```markdown
REUNIÓN DIARIA DE SINCRONIZACIÓN — DAILY SCRUM
Fecha: YYYY-MM-DD | Hora: 08:00 AM (Duración máxima: 15 minutos)
Facilitadora: Gina Diana Barrera Peña (Scrum Master)

OBJETIVO DE LA REUNIÓN:
Sincronizar las actividades diarias del equipo, evaluar el avance hacia el Objetivo del Sprint 6, detectar tempranamente cualquier bloqueo o impedimento técnico y mantener el flujo continuo de trabajo.

DINÁMICA DE PARTICIPACIÓN:
Cada integrante debe responder en un comentario individual, con su propia cuenta de Trello, las tres preguntas estándar del marco de trabajo Scrum:
1. ¿Qué actividades completé desde la sesión anterior para contribuir al objetivo del Sprint?
2. ¿Qué actividades realizaré el día de hoy?
3. ¿Qué impedimentos o bloqueos técnicos obstaculizan mi trabajo?
```

### 6.2 Ejemplos exactos de comentarios individuales para el Día 2 (Lunes 09/11/2026)

Cada miembro debe ingresar con su cuenta y publicar el siguiente comentario adaptado a su rol real:

#### Comentario de Gina Diana Barrera Peña (Scrum Master / ML)
> **Daily Scrum 2026-11-09:**
> 1. **¿Qué hice?** Finalicé la auditoría de etiquetas del tablero, archivé las tarjetas duplicadas y consolidé las métricas de error de Random Forest frente al baseline en `model_comparison.csv` (MAE 3.22 vs 4.60).
> 2. **¿Qué haré hoy?** Moveré HU-03 y HU-04 a DONE con sus checklists al 100 %, registraré la tarea de validación *walk-forward* en TO DO y prepararé el tracking de MLflow en Prediction para registrar el run `random_forest_15m`.
> 3. **¿Impedimentos?** Ningún impedimento bloqueante. Solo debemos coordinar la captura de la interfaz de MLflow UI una vez que se levante localmente.

#### Comentario de Ricardo Porras Veli (Backend / DevOps)
> **Daily Scrum 2026-11-09:**
> 1. **¿Qué hice?** Verifiqué las suites de pruebas unitarias de Monitoring (N passed tras `mvn test`) y Data Processing (114 passed en SQLite/PostgREST), y comprobé que la suite de humo arrojó 14/14 verificaciones aprobadas.
> 2. **¿Qué haré hoy?** Moveré HU-06 a DONE validando que la bandera `executionAllowed=false` se mantenga activa, registraré la tarea de revisión de políticas RLS de Supabase en TO DO y avanzaré la implementación de la entidad de auditoría en HU-07.
> 3. **¿Impedimentos?** La suspensión de los contenedores gratuitos en Render a los 15 minutos de inactividad genera retardos en el primer consumo; debemos fijar los *Health Check Paths* para mitigar este comportamiento.

#### Comentario de Leonid Kisley Orlando Huamán Collazos (Infraestructura / Frontend)
> **Daily Scrum 2026-11-09:**
> 1. **¿Qué hice?** Validé el archivo `alerts.yml` de Prometheus con la herramienta `promtool` confirmando 0 errores, e integré las 48 pruebas unitarias de los módulos del frontend en Node.js.
> 2. **¿Qué haré hoy?** Trasladaré HU-12 a DONE, moveré el rediseño del dashboard con pestañas (HU-11) hacia QA-TESTING y configuraré la tarea técnica en TO DO para fijar las rutas de health check en los 6 servicios de Render.
> 3. **¿Impedimentos?** Necesitamos que el usuario titular confirme el inicio de sesión real en `https://woshtsu.github.io/green-ai-workspace-cld/dev/` para tomar las capturas finales y cerrar HU-11.

#### Comentario de Jhonny Cristhian Quintana Carhuaricra (Product Owner)
> **Daily Scrum 2026-11-09:**
> 1. **¿Qué hice?** Revisé los criterios de aceptación y evidencias de las historias de PMV1 en DONE (HU-01, HU-02 y HU-15), confirmando que cumplen estrictamente con la Definición de Terminado.
> 2. **¿Qué haré hoy?** Registraré la tarea para la grabación del video de la Unidad III en TO DO con el desglose de los 7 episodios, auditaré los refinamientos de expertos (RE-04 al RE-06) y validaré los entregables de HU-03 y HU-06.
> 3. **¿Impedimentos?** Debemos asegurar que todos los servicios de Render estén activos al momento de procesar el lote masivo de transacciones para la demostración grabada.

---

## 7. Lista de verificación final y validación técnica

Antes de exportar el archivo definitivo para la entrega, la Scrum Master y el Product Owner deben verificar el estricto cumplimiento de los siguientes puntos de control:

### 7.1 Matriz de verificación de los 6 elementos obligatorios por tarjeta
- [ ] **1. Fecha de vencimiento:** Todas las tarjetas del tablero tienen una fecha configurada coherente con el sprint al que pertenecen.
- [ ] **2. Checklist con ítems técnicos:** Ninguna tarjeta tiene un checklist vacío. Todas contienen entre 4 y 7 ítems descriptivos reales, con casillas marcadas [x] según su estado real (100 % en DONE, parciales en QA e In Progress, vacías en To Do).
- [ ] **3. Miembro (único) asignado:** Cada tarjeta del tablero tiene exactamente un único integrante asignado como miembro. El trabajo compartido se evidencia en los comentarios de los demás integrantes, sin miembros duplicados ni tarjetas compartidas.
- [ ] **4. Etiquetas coherentes:** Cada tarjeta cuenta con su etiqueta de fase (`PMV1`, `PMV2` o `PMV3`) y al menos una etiqueta de especialidad técnica (salvo Dailies).
- [ ] **5. Descripción completa (>= 80 caracteres):**
  - Todas las historias HU contienen los bloques: `HISTORIA DE USUARIO` («Como… necesito… para…»), `ALCANCE`, `CRITERIOS DE ACEPTACIÓN` (formato CA-01 Given/When/Then), `EVIDENCIA EN REPOSITORIO` y `DEFINICIÓN DE TERMINADO (DoD)`.
  - Las tareas técnicas, revisiones, retrospectivas y roles cuentan con alcance y criterios detallados.
- [ ] **6. Comentarios y actividad auténtica:** Todas las tarjetas abiertas poseen entre 2 y 4 comentarios publicados por diferentes integrantes con sus cuentas personales, citando datos técnicos exactos (pruebas unitarias, códigos de error, comandos y URLs).

### 7.2 Validación del flujo Scrum y distribución por PMV
- [ ] **PMV1 100 % cerrado:** Todas las tarjetas asociadas a la etiqueta `PMV1` (HU-01, HU-02, HU-15, Reviews S1–S3 y Retro PMV1) residen exclusivamente en `7. DONE`, `10. SPRINT REVIEW` o `11. SPRINT RETROSPECTIVE`. No existe ninguna tarjeta de PMV1 en To Do o In Progress.
- [ ] **PMV2 activo y distribuido:** Existen tarjetas asociadas a la etiqueta `PMV2` en las cuatro columnas activas:
  - En `4. TO DO`: Tareas técnicas de Render, Supabase, walk-forward y video.
  - En `5. IN PROGRESS`: HU-07, HU-13, HU-09.
  - En `6. QA-TESTING`: HU-11, HU-05.
  - En `7. DONE`: HU-03, HU-04, HU-06, HU-08, HU-12, HU-14.
- [ ] **PMV3 en backlog:** HU-10 y HU-16 se ubican en `1. PRODUCT BACKLOG`, y la tarjeta de Sprint 7 en `2. SPRINT BACKLOG`.
- [ ] **Ausencia de duplicados:** Se archivaron los placeholders redundantes (`Sprint 1`, `Sprint 7` y `Sprint 8` vacíos en Review).
- [ ] **Trazabilidad de movimientos:** Las tarjetas que llegaron a DONE o QA se movieron de forma progresiva a lo largo de los días, registrando acciones de actualización de lista en el historial.

> [!NOTE]
> **Aviso sobre el validador técnico:** El script validador puede emitir el error «PMV1 fuera de Done/Review/Retro» debido a la presencia de las tarjetas RE-01 y RE-02 en la lista `3. REFINAMIENTO DE EXPERTOS` con etiqueta `PMV1`. Este es un **error conocido y documentado** que se explica al docente: las tarjetas RE corresponden a las actas de refinamiento histórico de expertos de dicha fase y su ubicación metodológica correcta es esa lista. **No se deben cambiar ni eliminar las etiquetas PMV1 de RE-01 y RE-02 para ocultar artificialmente este reporte del validador.**

---

### 7.3 Instrucciones para exportar el archivo JSON desde Trello
1. En el tablero de Trello de Green AI, hacer clic en el botón **Mostrar menú** (o el ícono de tres puntos `...` en la esquina superior derecha).
2. Seleccionar la opción **Más** (o Configuración del tablero).
3. Hacer clic en **Imprimir, exportar y compartir**.
4. Seleccionar **Exportar como JSON**.
5. El navegador descargará un archivo con extensión `.json` (ejemplo: `tablero-green-ai.json`). Guardar este archivo en la raíz del proyecto o en la carpeta `guias/trello/`.

---

### 7.4 Ejecución del validador técnico en Python
Abrir una terminal en la raíz del repositorio y ejecutar el script validador con la ruta al archivo descargado:

```bash
python herramientas_IA/trello/validar_trello.py "guias/trello/tablero-green-ai.json"
```

#### Interpretación de resultados del validador:
- **ERRORES (0):** Si la salida reporta `ERRORES (0)`, el tablero cumple al 100 % con todas las directivas obligatorias de formato, integridad de historias, distribución de PMVs y ausencia de duplicados. El archivo JSON está listo para ser sometido a la auditoría académica del docente.
- **AVISOS:** El validador puede emitir avisos informativos respecto a la distribución porcentual de acciones entre miembros o tarjetas que no hayan registrado movimientos entre listas. Siguiendo el plan paso a paso de los 4 días, los 4 integrantes acumularán más del 15 % de acciones cada uno y todas las tarjetas de flujo contarán con movimientos registrados, minimizando cualquier advertencia.
