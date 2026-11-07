# Revisión docente del informe de la Unidad III (semanas 9–12) y plan de levantamiento

Informe evaluado: `exportados/semana12/Porras-Huaman-Barrera-Quintana-informe-unidad-III.pdf` (solo en el respaldo del workspace antiguo)
(texto en `entregables/informe-corregido/informe-unidad-III.md`). Guía seguida: `guias/semana12/consigna-taller1-icacit.md`.
Instrumento: `guias/semana12/lista-cotejo-unidad3.md`.

## 1. Primera revisión (comentarios del docente, literal resumido)
1. Incluir resultados de las pruebas del PMV1 y PMV2 y resaltar los resultados con la IA de cada PMV.
2. Incluir resultados de la ingeniería: arquitectura de software y despliegue.
3. Incluir resultados de la gestión: tablero Trello.
4. Gestión del proyecto: presupuesto con los componentes válidos (línea base y reservas).
5. EDT en forma de diagrama, con ramas de Ingeniería y de Gestión.
6. Actualizar el tablero Trello en el espacio oficial asignado (workspace UC).
7. Incluir la sección de Pruebas, resultados y discusión. En la discusión, comparar los resultados de cada PMV
   con los resultados de los antecedentes, citándolos.
8. Adecuar las referencias a la norma ISO 690-2 (versión UC).
9. No aparece el video.

## 2. Segunda revisión: puntajes obtenidos (captura del usuario)
| # | Indicador (resumen) | Máx. | Obtenido | Brecha |
|---|---|---|---|---|
| 1 | Entrega en plazo | 1 | 1 | — |
| 2 | Título, autores, resumen y abstract | 1 | 0,5 | 0,5 |
| 3 | Introducción, marco teórico y 3 antecedentes de integración con ML (IEEE, ACM, Springer, ScienceDirect, Scopus) | 1 | 0,5 | 0,5 |
| 4 | Metodología de gestión e ingeniería de producto | 1 | 0,5 | 0,5 |
| 5 | Pruebas y resultados detallados de PMV1 y PMV2 con ML (capturas con datos por HU; métricas ML, arquitectura, agilidad, calidad) | 3 | 1 | 2 |
| 6 | Discusión comparando con 3 estudios previos | 1 | **0** | 1 |
| 7 | Conclusiones por objetivos de PMV1 y PMV2 | 1 | 0,5 | 0,5 |
| 8 | Redacción, carátula (logo UC, asignatura, integrantes, NRC), ISO 690 numérico | 1 | 0,5 | 0,5 |
| 9 | Demostración en video con 500–1000 transacciones, PMV1 y PMV2, entorno de calidad | 4 | 2 | 2 |
| 10 | Demostración en video de 1.º y 2.º caso de uso de predicción desde la aplicación | 3 | 1 | 2 |
| 11 | Arquitectura hexagonal, procedimientos almacenados (GitHub) y Kanban completo | 3 | 1 | 2 |
| | **Total** | **20** | **8,5** | **11,5** |

La suma 8,5/20 es un cálculo propio a partir de las marcas de la captura; confirmar con la nota oficial.

## 3. Diagnóstico: por qué se perdieron puntos (verificado contra el texto entregado)
- **Ind. 6 (0 pts):** la sección VIII.5 compara con los antecedentes cifras propias **sin experimento que las
  respalde**: XGBoost con RMSE 7,1 %, MAE 5,4 %, sMAPE 8,6 %, RMSE 9,8 % en picos y F1 0,89. El pipeline real
  (`software/prediction`, semilla 42, dataset simulado) selecciona **Random Forest** con MAE 3,22 y RMSE 4,59
  puntos de CPU en validación a 15 minutos. Ver `06-prueba-de-concepto.md`.
- **Ind. 5 y 10:** faltan pruebas por HU con datos y la IA visible desde la aplicación (dos casos de uso:
  predicción de demanda y recomendación).
- **Ind. 9:** no había video; con 500–1000 transacciones deben mostrarse datos en un entorno de calidad (la Guía de
  laboratorio 11 exige nube, no localhost).
- **Ind. 11:** los procedimientos almacenados no se evidenciaron en GitHub. Además, el tablero Kanban no estaba en
  el workspace oficial UC ni seguía la lista de cotejo de la S10.
- **Ind. 2, 3, 7 y 8:** problemas de forma (resumen y abstract, marco teórico, conclusiones por objetivo de PMV,
  ISO 690-2 versión UC y carátula con NRC).

## 4. Plan de levantamiento para la semana 13 (único documento que se exportará)
| Pendiente | Acción | Responsable sugerido (rol S8) | Evidencia necesaria | Estado |
|---|---|---|---|---|
| Resultados reales de IA (ind. 5, 6, 10) | Reemplazar las cifras sin respaldo por las del pipeline reproducible; explicar el dataset simulado | AIE | `software/prediction/results/` + comando reproducible | Datos listos; redacción en `06-` y `08-` |
| Discusión con 3 antecedentes (ind. 6) | Tabla: resultado de cada PMV frente a 3 estudios, con su dataset y métrica, y diferencias de contexto | AIE + PM | Fichas de `09-antecedentes-y-referencias.md` | En curso |
| Pruebas por HU (ind. 5) | Matriz HU → criterio Given/When/Then → prueba automatizada o manual → resultado | QA | Suites del monorepo (Monitoring 112, Gateway 11, Data Processing 114, Prediction 96, Frontend 13, Simulator 10) + smoke 14/14 | Datos listos |
| Arquitectura y despliegue (comentario 2) | Diagramas de paquetes y despliegue actualizados; topología en la nube | ARQ | `docs/DECISIONES.md` D-04, D-06 y D-07 | D-07 (hosting) pendiente |
| Presupuesto (comentario 4) | Línea base + reserva de contingencia + reserva de gestión, con valor comercial y desembolso real S/ 0 | PM | §VII.4 del informe (revisar consistencia) | Por revisar |
| EDT en diagrama (comentario 5) | EDT con ramas de Gestión y de Ingeniería (PlantUML WBS) | PM | Fuente `.puml` en `herramientas_IA/` | Pendiente |
| Trello oficial (comentario 6, ind. 11) | Migrar el tablero al workspace UC con las listas de la lista de cotejo S10 | PM | Enlace público | Lo hace el usuario |
| Procedimientos almacenados (ind. 11) | Mostrar en GitHub el SQL de funciones/procedimientos de Supabase y su uso | AIE + QA | `software/frontend/supabase-auth-setup.sql` (trigger/función) + los que existan en Supabase | Verificar en Supabase |
| Video (comentario 9, ind. 9 y 10) | Video de ≤ 20 min con 500–1000 transacciones y los 2 casos de uso de IA en un entorno de calidad | Todos | URL + QR | Lo hace el equipo |
| ISO 690-2 UC y carátula (ind. 2 y 8) | Normalizar referencias; carátula con logo, asignatura, integrantes y NRC | PM | `09-antecedentes-y-referencias.md` | En curso |
| Seguridad Supabase | Revisar las políticas RLS «Permitir todo» y la columna `password` en texto plano | AIE | Consulta de políticas en Supabase | Lo verifica el usuario |
