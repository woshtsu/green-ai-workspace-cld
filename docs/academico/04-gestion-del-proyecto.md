# C4 · Gestión del proyecto (ICACIT + PMBOK 7 + Scrum)

Base: `guias/TrabajosDesarrollados/4. Gestión de Proyecto.md`, §VII del informe entregado
(`entregables/semana09-12/informe-unidad-III.md`) y las guías `4.Gestiòn de Proyecto.md`, `semana1.md`,
`PROJECT-CHARTER.md`, `S10.Evaluacion-formativa…`. **Correcciones exigidas por el docente:**
1. Presupuesto con componentes válidos.
2. EDT en diagrama con ramas de Ingeniería y Gestión.
3. Trello en el workspace UC con las listas de la S10.
4. Registro de cambios que incluya la reestructuración.

## 1. Inicio: Project Charter (resumen)
| Campo | Contenido |
|---|---|
| Proyecto | Green AI: monitoreo y predicción de demanda computacional para apoyar la gestión eficiente de recursos en entornos universitarios (Proyecto 20) |
| Necesidad | Decisiones de capacidad reactivas frente a demanda variable (C1) |
| Objetivo | Prototipo con monitoreo, predicción y recomendaciones explicables bajo supervisión humana |
| Entregables | PMV1 (observabilidad), PMV2 (predicción y recomendación), PMV3 (validación experimental); informe; video por PMV; repositorio |
| Excluye | Acciones automáticas sobre producción; medición energética física (salvo que la UC la provea); despliegue institucional |
| Equipo (4) | Jhonny Cristhian Quintana Carhuaricra — PO y gobierno · Gina Barrera Peña — Scrum Master y ML · Ricardo Porras Veli — Backend y MLOps · Leonid Huamán Collazos — Infraestructura y UI/UX |
| Asesor | Ing. Jorge Alfredo Guevara Jiménez |
| Hitos | PoC (S4) · cierre PMV1 (S6) · cierre PMV2 (S12) · revisión general (S13) · cierre PMV3 y sustentación (S15–S16) |
| Supuestos y restricciones | Costo monetario S/ 0; 10 h/semana por integrante; sin datos institucionales garantizados |
**Nombre oficial (confirmado por el usuario el 2026-11-06):** JHONNY CRISTHIAN QUINTANA CARHUARICRA. La carátula
del informe entregado («Cristhian Quintana Carhuaricra») omite el primer nombre: corregirla en la semana 13.
Nota: la rúbrica S8 asume 5 roles y el equipo tiene 4. Asignar QA/DevOps de forma compartida y declararlo.

## 2. Enfoque y metodología
Matriz enfoque: predictivo 2,50 · ágil 4,85 · híbrido 4,35, con pesos de cambio 25, incertidumbre 20, entrega
incremental 20, *feedback* 20 y restricciones 15 → **ágil**. Metodología: **Scrum con tablero Kanban**
(*Scrumban*). Sprints de 2 semanas (8 sprints en 16 semanas), dailies virtuales 3 veces por semana (*tailoring*
por horarios), *review* con el asesor al cierre de cada sprint y retrospectiva PDCA por PMV.

## 3. PMV, backlog y estado real (verificado en el repositorio el 2026-11-06)
| PMV (semanas) | Pregunta | HU | Estado verificable |
|---|---|---|---|
| PMV1 (1–6) | ¿Se observa la demanda multirrecurso de forma reproducible? | HU-01, HU-02, HU-15 | **Hecho:** Simulator → Prometheus → Monitoring → Gateway; registro e inicio de sesión con Supabase; pruebas de Monitoring 112/112 |
| PMV2 (7–12) | ¿La IA anticipa la demanda mejor que un baseline y recomienda con seguridad? | HU-03, HU-04, HU-06, HU-07, HU-08, HU-11 (+HU-05, HU-09, HU-12) | **Mayormente hecho:** predicción y recomendación por API (Prediction 96/96); comparación de 4 modelos. **Parcial:** HU-05 (MLflow no evidenciado), HU-07 (no hay flujo de aprobación; solo `executionAllowed=false`), HU-09 (energía calculada solo con potencia aportada), HU-12 (solo alerta de disponibilidad) |
| PMV3 (13–16) | ¿Mejora frente a la línea base en condiciones equivalentes? | HU-10, HU-13, HU-14, HU-16 | **Pendiente:** experimento baseline frente a Green AI; reportes PDF/CSV; carbono con factor y fuente. HU-14 (roles) ya existe en el Gateway (ADMIN/OPERATOR; «observador» no implementado) |

## 4. EDT (diagrama; fuente PlantUML en `herramientas_IA/diagramas/edt-green-ai.puml`)
Ramas de **Gestión** e **Ingeniería** (pedido del docente). Se retiran los paquetes que no se ejecutaron:
clúster K3s/Minikube, Locust, MLflow Registry, JMeter, SonarQube y OWASP ZAP. Quedan como «propuesto PMV3» solo
si se hacen.
```
@startwbs
* Green AI
** 1 Gestión del proyecto
*** 1.1 Inicio: charter, stakeholders
*** 1.2 Planificación: backlog, EDT, cronograma, presupuesto, riesgos, comunicaciones
*** 1.3 Monitoreo y control: sprints, Trello, reporte de estado, Gantt ejecutado, registro de cambios
*** 1.4 Calidad: DoD, matriz de pruebas por HU
*** 1.5 Cierre: acta, lecciones aprendidas, informe final, sustentación
** 2 Ingeniería
*** 2.1 Requisitos: RF/RNF, HU con criterios Given/When/Then
*** 2.2 Arquitectura: componentes, despliegue, contratos OpenAPI
*** 2.3 PMV1 Observabilidad: Simulator, Prometheus, Monitoring, Gateway, Frontend, Auth
*** 2.4 PMV2 Inteligencia: Data Processing, PoC, Prediction, política de recomendación, energía
*** 2.5 PMV3 Validación: experimento baseline frente a Green AI, reportes, carbono
*** 2.6 Infraestructura y despliegue: Docker Compose, nube de staging, CI
*** 2.7 Pruebas: unitarias, contrato, integración, smoke, carga
@endwbs
```

## 5. Riesgos (cuantificados; alimentan la reserva de contingencia)
| ID | Riesgo | PMV | Prob. | Impacto (S/) | VME (S/) | Respuesta |
|---|---|---|---|---|---|---|
| R1 | Datos institucionales no disponibles | 1–3 | 0,6 | 1 200 (40 h) | 720 | Dataset sintético y simulador; declarar el origen |
| R2 | Límites del hosting gratuito (suspensión, RAM) | 2–3 | 0,5 | 900 (30 h) | 450 | Gateway Go ligero; D-07; demo local de respaldo |
| R3 | Bajo desempeño del modelo con datos reales o deriva | 3 | 0,4 | 1 200 (40 h) | 480 | Baselines siempre disponibles; error por régimen de carga |
| R4 | Incidente de seguridad en Supabase (RLS permisiva) | 2–3 | 0,3 | 1 500 (50 h) | 450 | Corregir políticas; rotar claves |
| R5 | Indisponibilidad de un integrante | 1–3 | 0,3 | 960 (32 h) | 288 | Roles compartidos; documentación en el repo |
| | **Total VME** | | | | **2 388** | |

## 6. Presupuesto corregido (componentes válidos: línea base + reservas)
Supuestos del informe: 4 integrantes × 10 h/semana × 16 semanas = 640 h; tarifa de referencia S/ 30/h.
| Componente | Cálculo | S/ |
|---|---|---|
| Mano de obra (valor comercial) | 640 h × 30 | 19 200,00 |
| Recursos valorados (no desembolsados) | Docker/Compose 350 · Prometheus+Grafana 250 · Python/FastAPI/scikit-learn 200 · Spring Boot/Go 200 · PostgreSQL/Supabase (free tier) 300 · 4 laptops (depreciación) 800 | 2 100,00 |
| **Costo directo** | 19 200 + 2 100 | **21 300,00** |
| Reserva de contingencia | VME de los riesgos identificados (§5) | 2 388,00 |
| **Línea base de costos (LBC)** | 21 300 + 2 388 | **23 688,00** |
| Reserva de gestión | 5 % de la LBC (riesgos no identificados; fuera de la LBC) | 1 184,40 |
| **Presupuesto total** | LBC + reserva de gestión | **24 872,40** |
| Desembolso real | Software libre, planes gratuitos y equipos propios | **0,00** |
Errores corregidos del informe entregado:
- El costo directo omitía los S/ 2 100 de recursos.
- La contingencia era un 10 % plano, sin vínculo con los riesgos.
- Se valoraban Kubernetes y MLflow, que no se usan.
- Declaraba «80 640 registros», cuando el dataset tiene 100 000.

## 7. Calidad: Definition of Done
Una HU está *Done* si cumple estos puntos:
1. Cumple su criterio Given/When/Then.
2. Tiene una prueba automatizada que lo verifica.
3. Pasa la revisión del diff.
4. Está integrada en `main` sin romper las suites.
5. Su contrato OpenAPI está actualizado.
6. No expone secretos.
7. Tiene evidencia en el informe (comando o captura).

## 8. Tablero Trello (lista de cotejo S10; mover al workspace UC)
Listas obligatorias:
- Product Backlog: HU del PMV3.
- Sprint Backlog: HU del PMV2 o PMV1.
- HU-Pendientes.
- HU-En proceso, con una tarjeta de **WIP** (p. ej. 3) que no se supere.
- HU-Terminadas: PMV1.
- CE-Daily Scrum: semanas 9 y 10, con las 3 preguntas y respuestas de cada integrante.
- CE-Sprint Review: tarjeta del PMV1 con su registro de cambios.
- CE-Retrospective: tarjeta del PMV1 con sus lecciones.
- Roles Scrum.

El tablero actual usa otras listas (To Do, In Progress, QA, Done), lo que no coincide con la lista de cotejo.
Esto lo hace el usuario en Trello.

## 9. Registro de cambios (formato CHG)
| ID | Fecha | Cambio | Motivo | Impacto |
|---|---|---|---|---|
| CHG-01 | 2026-10 | Recomendaciones integradas en Prediction (sin microservicio aparte) | Decisión del equipo; menos despliegues | Contrato `/api/recommendations/v1/*` conservado |
| CHG-02 | 2026-11-06 | Migración a monorepo con un Git; ramas `main`/`test` | Repos anidados desordenados | `docs/DECISIONES.md` D-01..D-04 |
| CHG-03 | 2026-11-06 | Perfil SQLite de desarrollo con pruebas de contrato contra PostgreSQL | Desarrollo sin depender de Supabase | D-05; el contrato añade `source` |
| CHG-04 | 2026-11-06 | Gateway en Go validado como alternativa (no predeterminado) | Consumo (16 MB frente a 520 MB) para el hosting | D-06 |
| CHG-05 | 2026-11-06 | Corrección de cifras de IA: Random Forest en lugar de «XGBoost final» | Las cifras previas no tenían experimento | `06-`, `08-` |
| CHG-07 | 2026-11-06 | HU-13: el reporte se entrega en JSON/CSV (API) y Markdown; **se descarta el PDF** | Decisión del usuario: todo el texto en Markdown; evidencias con capturas | Backlog y criterio de HU-13 |
| CHG-06 | Pendiente | Alcance: Kubernetes, MLflow Registry y JMeter pasan a «opcional PMV3» | No ejecutados | EDT §4 |

## 10. Medición del desempeño
El informe entregado reporta un avance de 22 de 41 actividades (53,6 %) y un SPI al 29/10/2026, sin el cálculo de
EV ni de PV. Para la semana 13, recalcular con el tablero real: `SPI = EV/PV`, historias terminadas por sprint y
*lead time*.
