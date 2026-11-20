# Documentación académica de trabajo (no se entrega ni se exporta)

Base de conocimiento corregida del proyecto Green AI (Taller de Proyectos 1, ISI, UC 2026-20). Sirve para que
las próximas entregas sean coherentes. Reglas:
- **Sin imágenes.** Los diagramas se describen o se dan en fuente textual (PlantUML).
- **Cada afirmación lleva su evidencia** (archivo del repo, prueba o fuente). Lo no verificado se marca así.
- **Lo único que se exportará** será el documento de la semana 13 (revisión general y levantamiento de
  correcciones), construido a partir de estos archivos.
- Las guías del docente están en `guias/exportados_docente/`; los trabajos previos del equipo, en
  `docs/historico/trabajos-desarrollados/` (usados como base, no como verdad); los artículos, en `guias/articulos/`.

| Archivo | Competencia / guía | Atributo ICACIT |
|---|---|---|
| [00-revision-docente-unidad-III.md](00-revision-docente-unidad-III.md) | Observaciones y puntajes de la Unidad III; plan de la semana 13 | — |
| [01-analisis-del-problema.md](01-analisis-del-problema.md) | C1 · Guía 1 | AG-T08 / AG-C08 |
| [02-conocimientos-de-ingenieria.md](02-conocimientos-de-ingenieria.md) | C2 · Guía 2 | AG-I07 |
| [03-ingeniero-y-sociedad.md](03-ingeniero-y-sociedad.md) | C3 · Guía 3 | AG-I01 / AG-I02 |
| [04-gestion-del-proyecto.md](04-gestion-del-proyecto.md) | C4 · Guía 4 + PMBOK 7 | AG-I12 |
| [05-herramientas-modernas.md](05-herramientas-modernas.md) | C5 · Guía 5 | AG-I11 |
| [06-prueba-de-concepto.md](06-prueba-de-concepto.md) | C6-A · Guía 6 (PoC) | AG-I11 / AG-I07 |
| [07-arquitectura-y-despliegue.md](07-arquitectura-y-despliegue.md) | C6-B · Arquitectura híbrida/hexagonal, Lab. 11 | AG-I09 |
| [08-pruebas-resultados-discusion.md](08-pruebas-resultados-discusion.md) | Pruebas por HU (PMV1/PMV2), resultados y discusión | — |
| [09-antecedentes-y-referencias.md](09-antecedentes-y-referencias.md) | Antecedentes (artículos) y referencias ISO 690-2 | — |

## Mapa de guías del docente
| Guía (archivo) | Qué exige | Dónde se desarrolla |
|---|---|---|
| `semana1.md` | Ideas (SCAMPER, Lean Startup, matriz de conveniencia), charter, alcance, recursos, cronograma | 04 §1–§3 |
| `0.Lineamientos al proyecto.md` (S2) | Kickoff, idea por factores ponderados con sostenibilidad, charter, 7 antecedentes Q1/Q2 (internacional, nacional y local), RF con 3 de predicción, HU por PMV, 3 arquitecturas por factores ponderados, UML de componentes y despliegue | 01, 02, 07, 09 |
| `1.Análisis del problema.md` | 10 secciones: contexto → conclusiones; AS-IS, Ishikawa/árbol/5 porqués, KPIs, restricciones | 01 |
| `2.Conocimientos de Ingenieria.md` | 11 secciones: problema → validación; matriz tecnológica ponderada | 02 |
| `3.El Ingeniero y la Sociedad.md` | 13–14 secciones: stakeholders, impactos, legal, ética de IA, accesibilidad, KPIs | 03 |
| `4.Gestiòn de Proyecto.md` | 14 secciones: enfoque, Scrum, tailoring, 3 PMV, backlog, riesgos, DoD, ejecución por PMV, cambios | 04 |
| `5.Uso de herramientas modernas.md` | 10 secciones: crear, seleccionar, aplicar y reconocer limitaciones | 05 |
| `6.Prueba de Concepto.md` | 1 requerimiento de IA → hipótesis → 3 alternativas → experimentos → Go/No-Go | 06 |
| `S6-TP1-CONSIGNA…UNIDAD-II.md`, `S6-TP1-TRAZABILIDAD…md`, `S7-TP1-LISTA-COTEJO…md` | Unidad II: C1–C6 (10 pts) + PMV1 con IA (capturas, GitHub hexagonal, video) | Todos |
| `S8-TP1-EX-PARCIAL-RUBRICA…md` | Exposición de 7+3 min, 5 roles, trazabilidad C1–C6, video PMV1 | 00 (roles) |
| `S9.LINEAMIENTOS…ARTICULO EN INGLES.md` | Artículo en inglés | Pendiente |
| `S10.Evaluacion-formativa…md` | Lista de cotejo de Trello, GitHub hexagonal, Python (precisión), procedimientos almacenados e informe | 04 §8, 07, 08 |
| `S11.GUÍA-DE-LABORATORIO11.md` | Despliegue en nube (no localhost), BD remota con seeding, pruebas G/W/T con URL pública | 07 §4, `docs/DECISIONES.md` D-07 |
| `semana12/consigna-taller1-icacit.md` + `lista-cotejo-unidad3.md` | Informe de la Unidad III (semanas 9–12) | 00 |
| `informeFinal.md` | Estructura del informe final (PMV3) | Esqueleto abajo |
| `Epicas_Historias_Criterios.md`, `PROJECT-CHARTER.md` | Formato G/W/T y plantilla de charter | 02 §2, 04 §1 |
| `S6.Arquitectura Híbrida.md` | **Archivo vacío (0 KB)**: pedir el original al docente | — |

## Trazabilidad integradora C1 → C6 (cadena exigida en S6/S8)
| Eslabón | Contenido Green AI | Evidencia verificable |
|---|---|---|
| C1 Problema | Dificultad para adaptar la asignación de recursos a la variabilidad de los workloads sin degradar el servicio; energía como efecto por medir | 01 |
| C2 Conocimiento | Series temporales, regresión supervisada (MAE/RMSE/sMAPE), división temporal sin fuga, hexagonal, sistemas distribuidos, P = dE/dt | 02; `software/prediction/src/` |
| C3 Sociedad | Stakeholders UC, impacto ambiental medible solo con energía válida (ISO/IEC 21031), Recommendation-Only, sin datos personales en telemetría | 03 |
| C4 Gestión | Scrum adaptado, 3 PMV, backlog HU-01..HU-16, presupuesto con línea base y reservas | 04 |
| C5 Herramientas | Prometheus, FastAPI, scikit-learn/XGBoost, Spring Boot, Go, Docker, Supabase, Trello, GitHub, agentes de IA con sus limitaciones | 05 |
| C6 PoC + Arquitectura | PoC reproducible (Random Forest elegido; XGBoost **no** ganó); microservicios con hexágono por servicio | 06, 07; suites de prueba |

## Esqueleto del informe final (`informeFinal.md`) ← fuentes
Resumen (≤ 250 palabras, ODS, ≥ 3 palabras clave) · 1 Introducción: 1.1 antecedentes (2 en español y 1 en inglés,
ISO 690-2) ← 09; 1.2 problema con estadísticas, ODS, Ishikawa, problema general y 3 específicos ← 01; 1.3 marco
teórico ← 02; 1.4 objetivos (máx. 3, por PMV) ← 01 §8 · 2 Conocimientos ← 02 · 3 Ingeniero y sociedad ← 03 ·
4 Metodología y aportes (≥ 3 por PMV) ← 04 · 5 Herramientas ← 05 · 6 Diseño: RF por PMV (entrega S7-S8, S12,
S15-S16), BD, arquitectura de componentes/despliegue, código por capas ← 02, 07 · 7 Gestión: inicio (charter),
planificación (alcance, EDT de gestión e ingeniería, comunicaciones, riesgos, presupuesto, Gantt base), monitoreo
(Gantt ejecutado, reporte de estado, tablero), cierre (acta, lecciones) ← 04 · 8 Pruebas (PoC + por PMV +
discusión) ← 06, 08 · 9 Lecciones (≥ 3 por PMV) · 10 Conclusiones (una por objetivo) · Referencias · Anexos
(experto, PDF de presentación, video por PMV con QR, GitHub, enlace ML).
