# Auditoría de observaciones del docente — informe Unidad IV (solo lectura)

Base: `entregables/semana15/informe-unidad-IV.md` (L = línea), rama test 514c8d0. El md es generado: editar `herramientas_IA/exportacion/construir_informe_iv.py`, `informe_iv_secciones.md` o la fuente `entregables/informe-corregido/informe-unidad-III.md`.
`graphify` no está en el PATH; para (j) se usó git ls-tree/grep.

## a) Referencias solo al final
- L355 `## ANTECEDENTES` (H2 tras el Cap. III, antes del Cap. IV en L417). L395-413 `### Referencias bibliográficas (Norma ISO 690-2)` lista [1]-[9].
- Lista final: L1925 `# REFERENCIAS BIBLIOGRÁFICAS`, [1]-[16].
- Falta: eliminar el subapartado L395-413 vía script. Antes, comparar el texto de [1]-[9] entre ambas listas (solo comprobé que la numeración existe al final).
- Duda: el docente dice "parte IV de antecedentes"; en el md los antecedentes no pertenecen al Cap. IV. Confirmar numeración en el Word/PDF.

## b) Factores ponderados
Tablas existentes: T3 L301 (Inferencia/ML, Observabilidad, API Gateway, Persistencia; solo puntaje total por alternativa, sin matriz criterio x peso, aunque L299 declara pesos 30/25/20/15/10); T6 L421 (ciclo de vida); T7 L434 (Scrum/Kanban/XP/Scrumban); T12 L613 (PostgreSQL/MySQL/MongoDB; 25 % cada criterio, total sobre 20); T13 L658 (estilo arquitectónico).
L465 declara otros pesos (25/20/15/10/10/10/10) sin ninguna tabla que los aplique.

| Herramienta (T8 L469-486, L1715, requirements/pom/HTML) | Tabla ponderada |
|---|---|
| Python / scikit-learn | Parcial (T3, solo total) |
| Prometheus | Parcial (T3) |
| Spring Cloud Gateway / Go | Parcial (T3) |
| Supabase / PostgreSQL | T12 (motor) y T3 parcial |
| SQLite | No (solo mencionado en T3) |
| Scrum | T7 |
| XGBoost (evaluado) | No como herramienta (comparación de métricas T26 L1184) |
| Simulator propio, Java 21 / Spring Boot | No |
| FastAPI, pandas, NumPy | No (pandas solo citado en T3) |
| MLflow, Grafana | No |
| Docker / Docker Compose | No |
| HTML/JS/CSS, Nginx, Chart.js 4.4.8, Font Awesome 6.4.0, supabase-js | No |
| OpenAPI / Swagger UI | No |
| Pytest, node --test, JUnit/Maven, go test, unittest, promtool | No |
| Git/GitHub, GitHub Actions, GitHub Pages, Render, Trello | No |
| Claude Code, Antigravity CLI, Graphify | No (evaluación sin pesos en docs/TOOLS_EVALUATION.md) |
| fpdf2, PostgREST | No |
| PlantUML, Pandoc/Word (documentación) | No; decidir si se listan |

Decisión: alcance; puntajes y pesos son juicio del equipo (no hay datos; si se puntúa a posteriori, decirlo).

## c) Capturas en la parte de ingeniería (Cap. VI, L514-707)
| # | Línea md | Figura | Título | Archivo |
|---|---|---|---|---|
| 7 | 590 | Figura 2 | Pantalla de registro de usuario en el frontend web. | `entregables/informe-corregido/evidencias/p026-img002.png` |
| 8 | 593 | Figura 3 | Confirmación del registro de usuario mediante Supabase Auth. | `entregables/informe-corregido/evidencias/p027-img003.png` |
| 9 | 596 | Figura 4 | Pantalla de inicio de sesión y autenticación con validación de credenciales. | `entregables/informe-corregido/evidencias/p027-img004.png` |
| 10 | 599 | Figura 5 | Dashboard principal con visualización histórica de telemetría de CPU y memoria. | `entregables/informe-corregido/evidencias/p028-img005.png` |
| 11 | 602 | Figura 6 | Dashboard de visualización en tiempo real de nodos de cómputo. | `entregables/informe-corregido/evidencias/p028-img006.png` |
| 13 | 636 | Figura 8 | Modelo físico implementado en Supabase / PostgreSQL (captura del visualizador de esquema de Supabase | `entregables/informe-corregido/evidencias-nube/captura-supabase-esquema-fisico.png` |
| 14 | 647 | Figura 9 | Procedimiento almacenado y disparador de sincronización de usuarios en Supabase (GitHub). | `entregables/informe-corregido/evidencias-nube/captura-C101-github-sql.png` |

#8 es un correo de Supabase en Gmail, #13 el visualizador de Supabase, #14 GitHub: no son pantallas propias. #7 y #9-#11 son la app (flujo L584-605). El resto del Cap. VI son diagramas.
Si "ingeniería" incluye pruebas (Cap. VIII), pantallas de la app:

| # | Línea md | Figura | Título | Archivo |
|---|---|---|---|---|
| 62 | 1502 | Figura VIII.16 | Esquema conceptual del caso de uso de inferencia de demanda de CPU a 15 minutos. | `entregables/informe-corregido/evidencias/p068-img035.png` |
| 67 | 1532 | Figura VIII.21 | Dashboard de métricas de infraestructura en la interfaz web de usuario. | `entregables/informe-corregido/evidencias/p072-img039.png` |
| 68 | 1536 | Figura VIII.22 | Interfaz web de inferencia predictiva de CPU e integración HTTP End-to-End. | `entregables/informe-corregido/evidencias/p072-img040.png` |
| 69 | 1542 | Figura VIII.23 | Interfaz web del Policy/Safety Engine y evaluación de recomendaciones con guardrails de SLA. | `entregables/informe-corregido/evidencias/p073-img041.png` |
| 70 | 1548 | Figura VIII.24 | Vista de infraestructura "Racks con calor" en la nube con sesión activa de usuario bajo rol OPERATOR | `entregables/informe-corregido/evidencias-nube/racks-nube-sesion-real-operator.png` |
| 71 | 1552 | Figura VIII.25 | Inspección de red con DevTools ante respuesta HTTP 422 Unprocessable Content por historial insuficie | `entregables/informe-corregido/evidencias-nube/racks-nube-devtools-422-datos-insuficientes.png` |
| 72 | 1556 | Figura VIII.26 | Tablero de evolución temporal multi-servidor mostrando la media del conjunto (85,4 %), área de dispe | `entregables/informe-corregido/evidencias-nube/grafico-media-max-min-comparacion.jpg` |
| 73 | 1560 | Figura VIII.27 | Tabla paginada de telemetría por servidor (HW001 a HW010) con filtros y atributos de calidad. Prueba | `entregables/informe-corregido/evidencias-nube/tabla-paginada-detalle.jpg` |
| 74 | 1564 | Figura VIII.28 | Vista analítica "Red de flujos" en topología circular para evaluación de balanceo de cargas entre ra | `entregables/informe-corregido/evidencias-nube/red-de-flujos-tela-de-arana.jpg` |
| 75 | 1570 | Figura VIII.29 | Primer caso de uso de IA: predicción de demanda de CPU a 15 minutos visualizada desde la aplicación  | `entregables/informe-corregido/evidencias-nube/captura-C306-prediccion.png` |
| 76 | 1574 | Figura VIII.30 | Segundo caso de uso de IA: recomendación asistiva con restricciones de seguridad visualizada desde l | `entregables/informe-corregido/evidencias-nube/captura-C307-recomendacion.png` |
| 77 | 1578 | Figura VIII.31 | Reporte histórico consolidado de HW045 y descarga en CSV desde la aplicación (Data Processing Servic | `entregables/informe-corregido/evidencias-nube/captura-C308-csv.png` |
| 79 | 1594 | Figura VIII.33 | Interfaz web para estimación experimental de demanda de CPU sobre el nodo HW001. | `entregables/informe-corregido/evidencias/p075-img042.png` |
| 80 | 1598 | Figura VIII.34 | Manejo de error contractual HTTP 422 Unprocessable Entity en la interfaz web ante telemetría tempora | `entregables/informe-corregido/evidencias/p075-img043.png` |
| 94 | 1727 | Figura VIII.38 | Evidencia de consulta y graficación de métricas de telemetría (HU-01). | `entregables/informe-corregido/evidencias/p078-img045.png` |
| 95 | 1731 | Figura VIII.39 | Evidencia de consulta de predicción de utilización de CPU a 15 minutos (HU-03). | `entregables/informe-corregido/evidencias/p079-img046.png` |

No hallé wireframes en el informe. Decisión: alcance; conflicto posible con (f) si se sustituyen capturas que deberían mostrar URL.

## d) Flujos y prototipos por PMV
- Flujos: L584-588 navegación (con capturas L590-605); L690-694 procesamiento (fórmulas, sin imágenes). AS-IS/TO-BE L101 (proceso). No hay flujo por PMV ni de predicción, recomendación, decisión HU-07 o PDF.
- PMV: definiciones L446-451; alcance L998-1000; hitos T24 L1027; HU por PMV T11 L561; pruebas PMV1 L1317, PMV2 L1491, PMV3 L1606.
- Candidatos: PMV1 #7, #9-#11; PMV2 #75-#77; PMV3: no hay en el informe captura de la UI aprobar/rechazar (HU-07), del PDF (HU-13) ni de la tabla accesible; habrá que dibujar wireframe o capturar.
- Decisión: "prototipo" = wireframe o captura real; qué flujos.

## e) Gantt y % de avance
- Informe: planificado L984; ejecutado L990 (`entregables/informe-corregido/evidencias/gantt-ejecutado-2026-11.png`, corte 11/11); resumen L1019.
- Fuente editable: `entregables/informe-corregido/fuentes/gantt_render.py` (usa PIL, ausente en C:/Python314); `cronograma-planificado.puml`. Estados fijos en `status()`: todo Completado salvo 6.x En ejecución y 6.5/PMV3 Planificado.
- Conteo del script: 40 actividades (13/13/14). Al 11/11: PMV1 13/13, PMV2 8/13, PMV3 0/14; global 21/40 = 52,5 % (derivado por mí).
- Alerta: marca Completado 1.3 "Cluster Kubernetes desplegado" (L704 dice que no se implementó). Revisar con evidencia 2.2 (Grafana), 5.1 ("precisión >= 90 %") y 6.1.
- Datos: T23 L1008-1015 (S7/S8 "Planificado"); L1069 22/41 = 53,6 % (29/10); L1071-1073 PMV3 "Planificado" (obsoleto); T30 L1610-1623 estado PMV3 al 25/11 (10 filas: 7 Ejecutada, 2 Pendiente, 1 Parcial); entregables/trello/REVISION-TRELLO-2026-11-09.md; entregables/semana14/. El JSON de guias/trello es antiguo (última actividad 05/11).
- Falta: estado de las 14 tareas 7.x/8.x, método de cálculo del %, fecha de corte, export Trello actual.

## f) Figuras sin URL
Revisadas las 107 imágenes del md (hojas de contacto y recortes de la franja superior). No audité imágenes fuera del informe.

### Con URL visible (11)
| # | Línea md | Figura | Título | Archivo |
|---|---|---|---|---|
| 10 | 599 | Figura 5 | Dashboard principal con visualización histórica de telemetría de CPU y memoria. | `entregables/informe-corregido/evidencias/p028-img005.png` |
| 27 | 1055 | Figura VII.6.1 | Tablero oficial de Trello con las listas del flujo de trabajo (vista parcial; el tablero completo ti | `entregables/informe-corregido/evidencias-nube/captura-C201-trello-tablero.png` |
| 28 | 1059 | Figura VII.6.2 | Detalle de tarjeta de Historia de Usuario en Trello con criterios BDD, checklist, etiquetas y coment | `entregables/informe-corregido/evidencias-nube/captura-C202-trello-hu03.png` |
| 49 | 1287 | Figura VIII.4 | Verificación de integración de extremo a extremo: smoke test de 14 comprobaciones sobre el stack loc | `entregables/informe-corregido/evidencias-nube/captura-C302-smoke.png` |
| 63 | 1506 | Figura VIII.17 | Especificación y contratos OpenAPI (Swagger UI) del Data Processing Service (`/docs`). | `entregables/informe-corregido/evidencias/p069-img036.png` |
| 64 | 1514 | Figura VIII.18 | Especificación interactiva OpenAPI (Swagger UI) del microservicio Prediction Service (`/docs`). | `entregables/informe-corregido/evidencias/p070-img037.png` |
| 71 | 1552 | Figura VIII.25 | Inspección de red con DevTools ante respuesta HTTP 422 Unprocessable Content por historial insuficie | `entregables/informe-corregido/evidencias-nube/racks-nube-devtools-422-datos-insuficientes.png` |
| 75 | 1570 | Figura VIII.29 | Primer caso de uso de IA: predicción de demanda de CPU a 15 minutos visualizada desde la aplicación  | `entregables/informe-corregido/evidencias-nube/captura-C306-prediccion.png` |
| 76 | 1574 | Figura VIII.30 | Segundo caso de uso de IA: recomendación asistiva con restricciones de seguridad visualizada desde l | `entregables/informe-corregido/evidencias-nube/captura-C307-recomendacion.png` |
| 77 | 1578 | Figura VIII.31 | Reporte histórico consolidado de HW045 y descarga en CSV desde la aplicación (Data Processing Servic | `entregables/informe-corregido/evidencias-nube/captura-C308-csv.png` |
| 89 | 1681 | Figura VIII.46 | Ola 2 desplegada en Render: Prediction rechaza con 401 la identidad falsificada sin el secreto del G | `entregables/semana15/evidencias/captura-S15-ola2-render-401.png` |

(#10 es local 127.0.0.1:3001; #89 muestra la URL dentro del comando.)

### Web, Trello, GitHub o app SIN barra de direcciones (52)
| # | Línea md | Figura | Título | Archivo |
|---|---|---|---|---|
| 7 | 590 | Figura 2 | Pantalla de registro de usuario en el frontend web. | `entregables/informe-corregido/evidencias/p026-img002.png` |
| 8 | 593 | Figura 3 | Confirmación del registro de usuario mediante Supabase Auth. | `entregables/informe-corregido/evidencias/p027-img003.png` |
| 9 | 596 | Figura 4 | Pantalla de inicio de sesión y autenticación con validación de credenciales. | `entregables/informe-corregido/evidencias/p027-img004.png` |
| 11 | 602 | Figura 6 | Dashboard de visualización en tiempo real de nodos de cómputo. | `entregables/informe-corregido/evidencias/p028-img006.png` |
| 13 | 636 | Figura 8 | Modelo físico implementado en Supabase / PostgreSQL (captura del visualizador de esquema de Supabase | `entregables/informe-corregido/evidencias-nube/captura-supabase-esquema-fisico.png` |
| 14 | 647 | Figura 9 | Procedimiento almacenado y disparador de sincronización de usuarios en Supabase (GitHub). | `entregables/informe-corregido/evidencias-nube/captura-C101-github-sql.png` |
| 29 | 1063 | Figura VII.6.3 | Registro histórico del tablero de trabajo Kanban en Trello. | `entregables/informe-corregido/evidencias/p051-img019.png` |
| 30 | 1075 | (sin pie propio) | (sin título) | `entregables/informe-corregido/evidencias/p052-img020.png` |
| 31 | 1077 | Figura VII.6.4 | Trazabilidad de avance cuantitativo y estado de tarjetas de Historias de Usuario. | `entregables/informe-corregido/evidencias/p053-img021.png` |
| 32 | 1089 | Figura VII.6.5 | Tarjeta del Daily Scrum del 09/11/2026 con la estructura de tres preguntas; solo registró su comenta | `entregables/informe-corregido/evidencias-nube/captura-C203-trello-daily.png` |
| 33 | 1093 | Figura VII.6.6 | Tarjeta de Sprint Review del Sprint 3 (cierre del PMV1) con el acta y la aceptación formal del Produ | `entregables/informe-corregido/evidencias-nube/captura-C204-trello-review-s3.png` |
| 34 | 1097 | (sin pie propio) | (sin título) | `entregables/informe-corregido/evidencias/p054-img022.png` |
| 35 | 1099 | (sin pie propio) | (sin título) | `entregables/informe-corregido/evidencias/p054-img023.png` |
| 36 | 1101 | Figura VII.6.7 | Registro de evidencias y ceremonias ágiles en el tablero Trello. | `entregables/informe-corregido/evidencias/p054-img024.png` |
| 37 | 1109 | (sin pie propio) | Tablero de Trello, listas 1 a 6, con tarjetas tituladas PMVn-HU-xx | `entregables/informe-corregido/evidencias-nube/captura-C312-trello-tablero-1.png` |
| 38 | 1111 | Figura VII.6.8 | Tablero de Trello (dos vistas) con tarjetas tituladas PMVn-HU-xx y distribuidas por estado. | `entregables/informe-corregido/evidencias-nube/captura-C312-trello-tablero-2.png` |
| 39 | 1115 | Figura VII.6.9 | Tarjeta PMV2-HU-04 en Done con responsable, vencimiento cumplido y comentarios de verificación (el c | `entregables/informe-corregido/evidencias-nube/captura-C313-trello-pmv2-hu04.png` |
| 40 | 1210 | Figura VIII.1 | Registro y trazabilidad del experimento de entrenamiento de Machine Learning en MLflow Tracking UI. | `entregables/informe-corregido/evidencias-nube/captura-C303-mlflow-run.png` |
| 52 | 1335 | Figura VIII.7 | Despliegue operativo de los 6 microservicios del sistema Green AI en Render (región Oregon) utilizan | `entregables/informe-corregido/evidencias-nube/render-6-servicios-desplegados.png` |
| 53 | 1343 | Figura VIII.8 | Panel de objetivos de recolección en Prometheus Server (`Status > Target health`). | `entregables/informe-corregido/evidencias/p060-img028.png` |
| 55 | 1356 | Figura VIII.9 | Panel de reglas de alerta configuradas en Prometheus Server. | `entregables/informe-corregido/evidencias-nube/captura-C304-prometheus-alerts.png` |
| 56 | 1364 | Figura VIII.10 | Tablero de observabilidad operativa en tiempo real en Grafana (`Dashboards > Green AI / Prometheus e | `entregables/informe-corregido/evidencias/p061-img029.png` |
| 58 | 1473 | Figura VIII.12 | Registros de servidores en la tabla `hardware` en PostgreSQL / Supabase. | `entregables/informe-corregido/evidencias/p066-img031.png` |
| 59 | 1477 | Figura VIII.13 | Registros de cuentas de acceso en la tabla `usuario` en PostgreSQL / Supabase. | `entregables/informe-corregido/evidencias/p066-img032.png` |
| 60 | 1481 | Figura VIII.14 | Registros de series temporales en la tabla `logs` en PostgreSQL / Supabase. | `entregables/informe-corregido/evidencias/p067-img033.png` |
| 61 | 1485 | Figura VIII.15 | Diagrama Entidad-Relación (ERD) del modelo de persistencia relacional en PostgreSQL / Supabase. | `entregables/informe-corregido/evidencias/p067-img034.png` |
| 62 | 1502 | Figura VIII.16 | Esquema conceptual del caso de uso de inferencia de demanda de CPU a 15 minutos. | `entregables/informe-corregido/evidencias/p068-img035.png` |
| 65 | 1518 | Figura VIII.19 | Esquemas Pydantic y estructuras DTO de validación de datos del Prediction Service. | `entregables/informe-corregido/evidencias/p071-img038.png` |
| 66 | 1524 | Figura VIII.20 | Documentación interactiva OpenAPI (Swagger UI) del microservicio Prediction Service en el entorno de | `entregables/informe-corregido/evidencias-nube/captura-C305-swagger-prediction.png` |
| 67 | 1532 | Figura VIII.21 | Dashboard de métricas de infraestructura en la interfaz web de usuario. | `entregables/informe-corregido/evidencias/p072-img039.png` |
| 68 | 1536 | Figura VIII.22 | Interfaz web de inferencia predictiva de CPU e integración HTTP End-to-End. | `entregables/informe-corregido/evidencias/p072-img040.png` |
| 69 | 1542 | Figura VIII.23 | Interfaz web del Policy/Safety Engine y evaluación de recomendaciones con guardrails de SLA. | `entregables/informe-corregido/evidencias/p073-img041.png` |
| 70 | 1548 | Figura VIII.24 | Vista de infraestructura "Racks con calor" en la nube con sesión activa de usuario bajo rol OPERATOR | `entregables/informe-corregido/evidencias-nube/racks-nube-sesion-real-operator.png` |
| 72 | 1556 | Figura VIII.26 | Tablero de evolución temporal multi-servidor mostrando la media del conjunto (85,4 %), área de dispe | `entregables/informe-corregido/evidencias-nube/grafico-media-max-min-comparacion.jpg` |
| 73 | 1560 | Figura VIII.27 | Tabla paginada de telemetría por servidor (HW001 a HW010) con filtros y atributos de calidad. Prueba | `entregables/informe-corregido/evidencias-nube/tabla-paginada-detalle.jpg` |
| 74 | 1564 | Figura VIII.28 | Vista analítica "Red de flujos" en topología circular para evaluación de balanceo de cargas entre ra | `entregables/informe-corregido/evidencias-nube/red-de-flujos-tela-de-arana.jpg` |
| 79 | 1594 | Figura VIII.33 | Interfaz web para estimación experimental de demanda de CPU sobre el nodo HW001. | `entregables/informe-corregido/evidencias/p075-img042.png` |
| 80 | 1598 | Figura VIII.34 | Manejo de error contractual HTTP 422 Unprocessable Entity en la interfaz web ante telemetría tempora | `entregables/informe-corregido/evidencias/p075-img043.png` |
| 90 | 1685 | Figura VIII.47 | Servicios del proyecto desplegados en Render. | `entregables/informe-corregido/evidencias-nube/render-6-servicios-desplegados.png` |
| 91 | 1691 | Figura VIII.36 | Pull Request #7 del Sprint 7 (ola 2) aprobado por otro integrante antes de fusionar, con los 12 chec | `entregables/informe-corregido/evidencias-nube/captura-C310-pr7-aprobado.png` |
| 92 | 1695 | Figura VIII.36.a | Fusión del Pull Request #7 en main después de la aprobación. | `entregables/informe-corregido/evidencias-nube/captura-C310b-pr7-fusionado.png` |
| 93 | 1699 | Figura VIII.37 | Historial de ejecuciones de GitHub Actions (workflow ci.yml). | `entregables/informe-corregido/evidencias-nube/captura-C311-actions.png` |
| 94 | 1727 | Figura VIII.38 | Evidencia de consulta y graficación de métricas de telemetría (HU-01). | `entregables/informe-corregido/evidencias/p078-img045.png` |
| 95 | 1731 | Figura VIII.39 | Evidencia de consulta de predicción de utilización de CPU a 15 minutos (HU-03). | `entregables/informe-corregido/evidencias/p079-img046.png` |
| 98 | 1984 | Figura A.2 | Repositorio de código fuente del microservicio Prediction Service. | `entregables/informe-corregido/evidencias/p095-img048.png` |
| 99 | 1991 | Figura A.3 | Repositorio de código fuente del microservicio Data Processing Service. | `entregables/informe-corregido/evidencias/p095-img049.png` |
| 100 | 1998 | Figura A.4 | Repositorio de código fuente del microservicio Monitoring Service. | `entregables/informe-corregido/evidencias/p096-img050.png` |
| 101 | 2005 | Figura A.5 | Repositorio de código fuente del microservicio API Gateway. | `entregables/informe-corregido/evidencias/p096-img051.png` |
| 102 | 2012 | Figura A.6 | Repositorio de código fuente de la aplicación frontend web. | `entregables/informe-corregido/evidencias/p097-img052.png` |
| 103 | 2019 | Figura A.7 | Repositorio de código fuente del simulador de infraestructura. | `entregables/informe-corregido/evidencias/p097-img053.png` |
| 104 | 2030 | Figura A.8 | Panel de servicios activos en la plataforma en la nube Render. | `entregables/informe-corregido/evidencias/p098-img054.png` |
| 105 | 2037 | Figura A.9 | Tablero Kanban de seguimiento ágil del proyecto en el espacio de trabajo oficial. | `entregables/informe-corregido/evidencias/p051-img019.png` |

Notas: #62, #68, #69, #80 solo muestran "Request URL" en DevTools. #29 y #105 son la misma imagen; #52 y #90 también. #98-#103 muestran repositorios antiguos (no el monorepo); #104 un Render antiguo con un deploy fallido. #59 expone contraseñas sintéticas en claro; #7-#9 muestran correo institucional de un integrante.

### Consola o escritorio, sin URL de página (24): decidir si se les exige
| # | Línea md | Figura | Título | Archivo |
|---|---|---|---|---|
| 4 | 165 | Figura 1.a | Cálculo de los indicadores de la Tabla 2 con pandas sobre el dataset sintético (herramienta: Python  | `entregables/informe-corregido/evidencias-nube/captura-M02-dataset-estadisticos.png` |
| 5 | 496 | Figura 1.b | Tamaños de imagen Docker medidos con `docker images`. | `entregables/informe-corregido/evidencias-nube/captura-M03-imagenes-docker.png` |
| 6 | 499 | Figura 1.c | Memoria en reposo de cada contenedor medida con `docker stats` (stack local, 15/11/2026). | `entregables/informe-corregido/evidencias-nube/captura-M04-docker-stats.png` |
| 41 | 1214 | Figura VIII.1.a | Reejecución del pipeline de entrenamiento (`scripts/run_pipeline.py`, semilla 42): métricas de la Ta | `entregables/informe-corregido/evidencias-nube/captura-M01-metricas-modelos.png` |
| 42 | 1258 | Figura VIII.3.a | Monitoring: `mvnw verify`, Tests run: 112, Failures: 0, BUILD SUCCESS. | `entregables/informe-corregido/evidencias-nube/captura-C301c-monitoring-mvn.png` |
| 43 | 1262 | Figura VIII.3.b | Gateway Java: `mvnw verify`, Tests run: 12, Failures: 0, BUILD SUCCESS. | `entregables/informe-corregido/evidencias-nube/captura-C301d-gateway-java.png` |
| 44 | 1266 | Figura VIII.3.c | Gateway Go: `go test -race` en Docker golang:1.25, paquetes ok y 32 pruebas PASS. | `entregables/informe-corregido/evidencias-nube/captura-C301e-gateway-go.png` |
| 45 | 1270 | Figura VIII.3.d | Data Processing: pytest, 121 passed y 8 skipped. | `entregables/informe-corregido/evidencias-nube/captura-C301b-data-processing-pytest.png` |
| 46 | 1274 | Figura VIII.3.e | Prediction: pytest, 100 passed. | `entregables/informe-corregido/evidencias-nube/captura-C301a-prediction-pytest.png` |
| 47 | 1278 | Figura VIII.3.f | Frontend: node --test, 48 pass y 0 fail. | `entregables/informe-corregido/evidencias-nube/captura-S10-frontend-tests.png` |
| 48 | 1282 | Figura VIII.3.g | Simulator: unittest en Docker python:3.12, Ran 10 tests, OK. | `entregables/informe-corregido/evidencias-nube/captura-C301f-simulator-unittest.png` |
| 50 | 1323 | Figura VIII.5 | Estado operativo de los contenedores locales en Docker Desktop Dashboard. | `entregables/informe-corregido/evidencias/p059-img026.png` |
| 51 | 1329 | Figura VIII.6 | Construcción y arranque de servicios mediante Docker Compose CLI (`docker compose up -d --build`). | `entregables/informe-corregido/evidencias/p060-img027.png` |
| 54 | 1353 | Figura VIII.8.a | Validación de las reglas de alerta con `promtool check rules`. | `entregables/informe-corregido/evidencias-nube/captura-M06-promtool.png` |
| 78 | 1582 | (sin pie propio) | Figura VIII.32. Prueba de carga masiva sobre el API Gateway en Render (10/11/2026, 01:49–01:56): 601 | `entregables/informe-corregido/evidencias-nube/carga-601-transacciones-render.png` |
| 81 | 1647 | Figura VIII.38 | Prediction Service: 116 pruebas aprobadas, incluidas las 16 de decisiones HU-07. | `entregables/informe-corregido/evidencias-nube/captura-S7-prediction-pytest.png` |
| 82 | 1651 | Figura VIII.39 | Data Processing: 128 aprobadas y 8 omitidas, incluidas las 7 del reporte PDF. | `entregables/informe-corregido/evidencias-nube/captura-S7-data-processing-pytest.png` |
| 83 | 1655 | Figura VIII.40 | Gateway Java: 19 pruebas, BUILD SUCCESS. | `entregables/informe-corregido/evidencias-nube/captura-S7-gateway-java-mvn.png` |
| 84 | 1659 | Figura VIII.41 | Gateway Go: 40 pruebas con detector de carreras, 0 fallos. | `entregables/informe-corregido/evidencias-nube/captura-S7-gateway-go.png` |
| 85 | 1663 | Figura VIII.42 | Simulator: 14 pruebas, incluida la que verifica que la aplicación no importa adaptadores. | `entregables/informe-corregido/evidencias-nube/captura-S7-simulator-unittest.png` |
| 86 | 1667 | Figura VIII.43 | Frontend: 63 pruebas (tabla accesible, URL del PDF, decisiones y etiquetas modeladas). | `entregables/informe-corregido/evidencias-nube/captura-S7-frontend-tests.png` |
| 87 | 1671 | Figura VIII.44 | Monitoring sin regresiones: 112 pruebas. | `entregables/informe-corregido/evidencias-nube/captura-S7-monitoring-mvn.png` |
| 88 | 1677 | Figura VIII.45 | Arranque en frío medido en Render Free: primera petición tras inactividad (12,6–69,5 s) y segunda (< | `entregables/semana13/evidencias/captura-P01-arranque-frio-render.png` |
| 96 | 1757 | Figura VIII.39.a | Reejecución del experimento comparativo (`scripts/run_experiment.py`, P_max 600 W, P_idle 300 W). | `entregables/informe-corregido/evidencias-nube/captura-M05-experimento-sla.png` |

### No son capturas (20: diagramas, logos, fórmulas, fotos)
Ids [1, 2, 3, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 57, 97, 106, 107]. #19 (`p037-img011.png`, L776, leyenda RACI) es un rectángulo negro: imagen defectuosa. Las fotos del congreso no tienen URL.
Además: numeración duplicada "Figura VIII.36-39" (L1649-1701 frente a L1729-1733) y varias imágenes sin pie.

## g) Sección de pruebas y resultados: discusión respecto a los entregables
- Cap. VIII L1152; la única discusión es VIII.5 L1833-1852, contra antecedentes (T34).
- Insumos: T18 L865, T24 L1027, T28 L1295, T30 L1610, T33 L1785, EDT L835.
- Falta: por entregable, criterio, prueba, resultado, discusión y pendiente. Cifras desfasadas: V.3 L506-511 y T27 L1243-1252 usan 435 pruebas (15/11) frente a 492 (19/11, L1632); L670-678 igual.
- Decisión: qué son "los entregables" (PMV/EDT o entregables del curso: informe, artículo, póster, video).

## h) Conclusiones
Objetivos L192-201: general, OE1 (PMV1 observabilidad), OE2 (PMV2 predicción y recomendación), OE3 (PMV3 experimentación y eficiencia), OE4 (PMV3 procesos, calidad, entregables).

| Conclusión actual | Línea | Objetivo real |
|---|---|---|
| General | 1872 | General |
| "OE1 Monitoreo" | 1875 | OE1 |
| "OE2 Datos" | 1878 | OE1 (no corresponde a OE2) |
| "OE3 Predicción" | 1881 | OE2 |
| "OE4 Recomendaciones" | 1884 | OE2 |
| "OE5 Experimentación" | 1887 | OE3 (no existe OE5) |
| "OE4 de proceso" | 1890 | OE4 |

Propuesta: OE1 = 1875+1878; OE2 = 1881+1884; OE3 = 1887; OE4 = 1890. L451 y L1000 aún dicen PMV3 "planificado". OE3 promete utilización y energía; el resultado de energía es solo modelado.
Decisión: confirmar que "4" son los 4 OE y si se mantiene la del objetivo general.

## i) FURPS+ y OWASP
- En el informe solo: T30 L1615, indicador 8 L1705, H-01/H-02 (T4 y alrededores del marco legal), L1619-1630, T33 L1785, L1890-1912. Sin tabla por factor FURPS+, sin categorías OWASP, sin tabla hallazgo-corrección y sin anexo de calidad (anexos actuales A, B, C, D, E desde L1961).

| Fuente | FURPS+ | OWASP | Dictamen |
|---|---|---|---|
| docs/calidad/07_auditoria_final.md (07/11) | 87,00 % (nota 12/11: 86,0 / 86,28) | 85,0 (2021) | Apto con observaciones |
| docs/calidad/08 y entregables/semana13/semana13-calidad-furps-owasp.md L335-470 (entregado) | 84,0 a 86,0 | 79,0 a 83,5 (2025); matriz 56 a 68 % | Apto con observaciones |
| guias/semana14/FURPS+ Y OWASP/Ejecuciones/08_Auditoria_Final.md (19/11), el que cita el informe | 87,00 / 87,62 | 86,0 estimado | NO APTO |

- Además el global difiere: docs/calidad/08 da 79,2 a 83,2 %; semana13 da 78,4 a 82,4 %.
- En Ejecuciones solo hay 01, 02, 04, 05, 07, 08; no están los 03 y 06 que cita el 08.
- Contradicción: semana13 §8 (hacia L360-370) afirma que RLS y columnas password se verificaron en consola Supabase el 12/11 (S11, S12); el informe L1619 y T33 dicen "no verificado".
- Respaldo: docs/calidad/01..08; docs/evidencias/semana13-mapa-evidencias.md, semana13-ola1-verificacion.md, semana13-salidas/; entregables/semana13/evidencias/; exportados/semana13/MODELO-FURPSPLUS-Green-AI.xlsx; guias/semana14/FURPS+ Y OWASP/; guias/semana14/ingenieria-inversa/docs/ingenieria_inversa.md (hallazgos L223-245).
- Correcciones: ola 1 OW-06, 07, 08, 10 corregidos; OW-01..05, 09, 11, 12 pendientes y OW-13 nuevo (docs/calidad/08 L31-47). Ola 2: HU-07, HU-13, U-02, F-06, S-01 y H-01 parcial (L1625-1630). No hallé re-medición de la matriz posterior a la ola 2.
- Decisión: versión oficial y estado real de RLS.

## j) Adaptadores (woshtsu/green-ai-workspace-cld)
git ls-remote: main 51234b4, test 514c8d0 (igual que local). Los tres archivos existen en ambas ramas; el diff main..test en software solo toca 2 archivos de frontend.

| Clase | Línea | Enlace (test; cambiar por main) |
|---|---|---|
| SupabaseHistoricalLogsAdapter (PostgREST, solo lectura) | 17 | https://github.com/woshtsu/green-ai-workspace-cld/blob/test/software/data-processing/infrastructure/adapters/input/supabase_historical_logs_adapter.py#L17 |
| SqliteHistoricalLogsAdapter | 22 | https://github.com/woshtsu/green-ai-workspace-cld/blob/test/software/data-processing/infrastructure/adapters/input/sqlite_historical_logs_adapter.py#L22 |
| SqliteDecisionRepository | 30 | https://github.com/woshtsu/green-ai-workspace-cld/blob/test/software/prediction/src/decisions/adapters/sqlite_repository.py#L30 |

- Puertos: software/data-processing/domain/ports/historical_logs_source.py; DecisionRepository en software/prediction/src/decisions/domain/decision.py L46. Selección: software/data-processing/infrastructure/historical_sources.py.
- NO existe adaptador Supabase para decisiones HU-07 (solo software/prediction/migrations/001_recommendation_decisions.sql, que el informe declara no aplicado). No vi adaptadores Supabase/SQLite en Monitoring ni Simulator.
- Supabase Auth (no son repositorios): software/frontend/app.js L17; software/gateway-go/internal/auth/jwks.go; software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java.

## k) Póster
- No está insertado; solo menciones L1623 y L1970. Imagen: exportados/semana15/poster-green-ai.png (2384x3370); fuente entregables/semana15/poster/poster-green-ai.html.
- Diseño: vertical, cabecera verde-azul con logo, título largo, autores y docente; 3 columnas. 1 Problema, 2 Objetivo, 3 Metodología (Fig. 1 despliegue), 4 Resultados predicción (KPI y barras), 5 Resultados calidad (barras y captura pytest), 6 Resultados despliegue (dashboard y pendientes), 7 Conclusiones (3), 8 Referencias [1], [6], [12]; pie con URLs y nota de IA. Sin Introducción, Discusión ni QR; sin cifras FURPS+/OWASP; capturas ilegibles a escala.
- Plantillas halladas (guias/semana15-16): Cartel científico.md (título, autores, introducción, metodología, resultados, discusión, conclusiones, bibliografía); Poster-ejemplo-1 y 2 (organizados por PMV). Ninguna transcripción mostró QR ni exactamente la plantilla numerada descrita: pedir el archivo/imagen oficial.
- QR: pendiente (docs/CONTINUAR-EN-NUEVO-CHAT.md: falta paquete qrcode); definir destino.
