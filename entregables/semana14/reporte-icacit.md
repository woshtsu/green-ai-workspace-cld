# Reporte de evaluación de evidencias ICACIT — Informe del proyecto Green AI

| Campo | Detalle |
|---|---|
| Proyecto | Green AI: sistema de monitoreo y predicción de demanda computacional para apoyar la gestión eficiente de recursos en entornos universitarios |
| Equipo | Ricardo Porras Veli; Leonid Kisley Orlando Huamán Collazos; Gina Diana Barrera Peña; Jhonny Cristhian Quintana Carhuaricra |
| Docente | Jorge Alfredo Guevara Jiménez |
| Curso / NRC | Taller de Proyectos 1 · NRC 30170 · Universidad Continental, EAP Ingeniería de Sistemas e Informática |
| Fecha del reporte | 19/11/2026 |
| Tarea | 7.6 (Sprint 7): evaluación de evidencias ICACIT, consigna de la Semana 14 |
| Documento evaluado | `entregables/informe-corregido/informe-unidad-III.md` (versión del 15/11/2026) |
| Evidencia adicional | `guias/semana14/ingenieria-inversa/docs/ingenieria_inversa.md` (19/11/2026) y `guias/semana14/FURPS+ Y OWASP/Ejecuciones/08_Auditoria_Final.md` (19/11/2026) |
| Referencia | Atributos del graduado ICACIT 2025 para las competencias indicadas en la consigna |

## 0. Método y criterios

- Rol: evaluador ICACIT. Se evalúa lo que el **informe** demuestra. Una afirmación sin captura, comando o tabla que la respalde se marca «sin evidencia en el informe».
- Niveles: **Cumple** (evidencia suficiente y consistente), **Cumple parcialmente** (evidencia incompleta, no verificable o contradicha por otra evidencia), **No cumple** (sin evidencia).
- Las citas «§» usan la numeración propia del informe (capítulos I–X; apartados 1.1, VI.1, VII.5.3, etc.). «Tabla N» y «Figura N» se citan tal como aparecen rotuladas.
- La ingeniería inversa y la auditoría final son **posteriores** al informe (19/11 frente a 15/11). Se usan para contrastar sus afirmaciones, no como parte del informe; sus hallazgos aún no están incorporados en él.
- Las guías de «Consolidado 4 PMV3/Articulo e Informe» evalúan el artículo científico y no aportan criterios por atributo ICACIT. Solo se aprovechó su regla de no ser benevolente: lo mencionado pero no demostrado cuenta como evidencia parcial.
- Limitación: evaluación documental. No se reejecutaron pruebas ni se verificaron los sistemas desplegados.

## 1. Tabla resumen por atributo

| # | Atributo ICACIT | Nivel | Evidencia principal en el informe | Hallazgo principal |
|---|---|---|---|---|
| 1 | Conocimientos de Ingeniería (transversal) | **Cumple** | Cap. II (a, b, c); Tablas 3, 7, 13; §VIII.1.2 (H1) | Fundamentos aplicados con trazabilidad al código. Falta justificar P_idle y P_max y unificar el cálculo del «−30 %». |
| 2 | Medioambiente y Sostenibilidad (transversal) | **Cumple parcialmente** | §1.2 (ODS 7, 9, 12, 13); §III.c; Tabla 31; §VIII.4.2; HU-10 (Tabla 11) | Honestidad ambiental, pero sin impacto demostrado: energía −0,17 % modelada y CO2e no implementada. |
| 3 | El Ingeniero y la Sociedad (transversal) | **Cumple parcialmente** | Cap. III (a–f); Tabla 4; Tabla 17 (R4); Anexo C | Estructura completa, pero el marco legal declara controles que la ingeniería inversa y la auditoría contradicen. Sin consulta a usuarios ni cuantificación. |
| 4 | Gestión de Proyectos (transversal) | **Cumple** | §VII.1–VII.7; Tablas 14–25; Figuras VII.2.4–VII.6.9 | Gestión integral y evidenciada. Observaciones: fechas desactualizadas, sin SPI/CPI, revisión por pares débil. |
| 5 | Diseño y Desarrollo de Soluciones (específica) | **Cumple parcialmente** | Cap. VI (Tablas 9–13; Figuras 2–13); Tablas 27–28; Figuras VIII.3.a–g; Tabla 31 | Buen diseño y 435 pruebas, pero los RNF de seguridad y rendimiento no están verificados y no se reflejan los riesgos críticos de la auditoría. |
| 6 | Análisis de Problemas (específica) | **Cumple parcialmente** | §1.1 (Tabla 1, Figura 1, Tabla 2, Figura 1.a); §1.2 | Análisis estructurado, pero la evidencia del problema es anecdótica o sintética (sin cita para «1 000 a 8 000»). |
| 7 | Uso de Herramientas Modernas (específica) | **Cumple** | Cap. V (Tabla 8; Figuras 1.b, 1.c); Tabla 30; Figuras VIII.36, VIII.37 | Uso integrado y limitaciones medidas. Sin herramientas de calidad (SonarQube, JMeter, ZAP) y Tabla 32 (multi-SO) sin capturas. |

Resumen: 3 Cumple, 4 Cumple parcialmente, 0 No cumple.

## 2. Evaluación por atributo

### 2.1 Conocimientos de Ingeniería — Cumple

**Hallazgos**
1. Fortaleza: el Cap. II cubre (a) matemáticas y computación (series temporales, regresión, división temporal sin fuga, MAE y RMSE), (b) ciencias naturales (E = ∫P(t)dt con regla del trapecio en `software/prediction/src/service/recommendations.py`; CO2e = E·FE con ISO/IEC 21031:2024) y (c) ingeniería de software (hexagonal, OpenAPI, JWT/RBAC).
2. Fortaleza: selección ponderada y comparativa (Tablas 3, 6, 7, 12 y 13).
3. Fortaleza: aplicación real, con H1 cuantitativa (§VIII.1.2), prueba de no fuga (§IX.1) y reejecución con semilla 42 (Figura VIII.1.a).
4. Observación: §V.3 y la Tabla 34 mezclan bases. El «−30,15 % vs persistencia» sale de 3,22 frente a 4,61 (validación), pero se presenta junto a «MAE 3,85 en test».
5. Observación: P_idle = 300 W y P_max = 600 W (§VIII.3.1) no tienen fuente (ficha técnica o SPECpower).
6. Observación: el Cap. II no conecta cada conocimiento con la decisión de diseño que sustenta.
7. Evidencia adicional (ingeniería inversa, H-14): el modelo se entrenó con 1 nodo sintético y 864 registros y se aplica a 50 nodos. El informe no declara esa limitación.

| Prioridad | Mejora | Sección destino |
|---|---|---|
| Media | Tabla «Conocimiento → decisión de diseño → evidencia» | Final del Cap. II (nueva tabla) |
| Media | Indicar el conjunto de datos (validación o test) en cada porcentaje de mejora y unificar cifras | §V.3; Tabla 34; §VIII.4.1 |
| Media | Citar la fuente de P_idle y P_max o declararlos como supuesto con análisis de sensibilidad | §II.b y §VIII.3.1 |
| Baja | Declarar la limitación de 1 nodo y 864 registros | §VIII.1.3 y §X.2 |

### 2.2 Medioambiente y Sostenibilidad — Cumple parcialmente

**Hallazgos**
1. Fortaleza: ODS 7 (meta 7.3), 9, 12 y 13 (§1.2). Se distinguen W, kWh y CO2e (§III.c; §II.b).
2. Fortaleza: honestidad. Con h = 10 % la energía modelada baja −0,17 % (4 896 → 4 888 Wh) y el informe concluye que «no existe evidencia empírica de ahorro energético significativo» (§VIII.3.1, Tabla 31). Descarta el −18,4 % previo (CHG-05).
3. Fortaleza: *Green-in-AI*. Imagen de Prediction de 2,85 GB a 510 MB y RAM en reposo de 122–142 MiB (§V.2; §VIII.4.2; Figuras 1.b, 1.c).
4. Hallazgo: no hay impacto ambiental demostrado. HU-10 (CO2e) es trabajo futuro (§X.2). El ODS 13 promete «cuantificación… con factores de emisión certificados» y nada en el informe cuantifica CO2e.
5. Hallazgo: *Green-in-AI* mide imagen y RAM, no energía. §III.c promete un «balance energético neto» que la Tabla 30 y §X.2 no incluyen.
6. Hallazgo: no hay análisis de ciclo de vida ni indicador de sostenibilidad con meta y método. La reducción se evalúa con un modelo lineal proxy sobre 126 intervalos de un nodo (HW001).
7. Contexto: la validación con trazas reales (condición C1 del dictamen GO CON CONDICIONES, §VIII.1.5) sigue pendiente.

| Prioridad | Mejora | Sección destino |
|---|---|---|
| Alta | Reformular ODS 13 («método de estimación, no reducción medida») y añadir tabla ODS → meta → indicador → evidencia | §1.2 |
| Alta | Cálculo ilustrativo de CO2e con factor oficial del SEIN (con fuente) marcado «estimado», o declarar que HU-10 no tiene resultado | §III.c y §VIII.3.1 |
| Media | Balance energético neto: energía evitada frente a la del propio stack (P(u) y `docker stats`) | §VIII.4.2 |
| Media | Sensibilidad de P_idle, P_max y número de nodos para explicar la diferencia < 0,2 % | §VIII.3.1 |
| Baja | Tabla de decisiones de diseño con efecto ambiental (Gateway Go, imagen multi-etapa, SQLite) | §V.2 o §IX.3 |

### 2.3 El Ingeniero y la Sociedad — Cumple parcialmente

**Hallazgos**
1. Fortaleza: el Cap. III cubre los seis aspectos (III.a a III.f) e incluye la Tabla 4 (Ley 29733 y D.S. 016-2024-JUS, D. Leg. 1412, Ley 30096, ISO/IEC 21031:2024).
2. Fortaleza: ética aplicada con *Recommendation-Only* (`executionAllowed=false`) y política de no declarar ahorros sin medición.
3. Hallazgo crítico: la Tabla 4 declara «eliminación de endpoints expuestos sin autorización» (Ley 30096) y minimización «bajo políticas RLS» (Ley 29733). La ingeniería inversa contradice ambas: H-01 (crítica: Prediction y Data Processing públicos en Render sin autenticación, con elusión del Gateway), H-02 (crítica: RLS «Permitir todo» y columna `password` en el snapshot) y RG-02 (riesgo de incumplimiento de la Ley 29733). La auditoría 08 concluye «NO APTO PARA PRODUCCIÓN» y deja OW-01, OW-03 y el bypass de Data Processing como P0/P1 abiertos. El informe reconoce el riesgo de RLS (§III.e; R4 en la Tabla 17), pero lo presenta como medida ya implementada.
4. Hallazgo: sin evidencia de consulta a usuarios. La Figura A.1 es solo el formulario de entrevista y las pruebas con usuarios están «Planificadas» (Tabla 30).
5. Hallazgo: las justificaciones social y económica no tienen indicadores (§III.b declara que no hay cifras).
6. Hallazgo: §III.f cubre solo riesgos técnicos. No hay seguridad de la información ni accesibilidad (la auditoría FURPS+ registra que falta auditoría WCAG 2.1 AA).
7. Hallazgo: no se distingue qué obligaciones legales se activarían con datos reales (consentimiento, retención, anonimización).
8. Observación: la Tabla 35 marca «Atendida» esta competencia, lo que no se sostiene por el punto 3.

| Prioridad | Mejora | Sección destino |
|---|---|---|
| Alta | Reescribir «Medidas técnicas» de la Tabla 4 con el estado real (implementado y verificado frente a pendiente: H-01, H-02, OW-01, OW-03) | Tabla 4 (§III.e); Tabla 17 (R4) |
| Alta | Párrafo con los hallazgos de la ingeniería inversa y la auditoría final (veredicto, riesgos P0/P1) | §III.f y §VIII.2.4 |
| Media | Matriz parte interesada → impacto → mitigación, con ética de IA (explicabilidad, supervisión humana, sesgo de datos sintéticos) | §III.a (nueva tabla) |
| Media | Resultados y acta de pruebas con usuarios (cuando existan), con satisfacción y accesibilidad | §VIII.2.3 |
| Baja | Escenario económico hipotético (S/ por kWh evitado) marcado como no medido | §III.b |
| Baja | Tabla 35: pasar a «Atendida parcialmente» | Anexo C |

### 2.4 Gestión de Proyectos — Cumple

**Hallazgos**
1. Fortaleza: acta (Tabla 14), selección metodológica (Tablas 6 y 7), ceremonias (Tabla 15), RACI (Tabla 16), stakeholders (Figuras VII.2.4 y VII.2.5), riesgos con VME y reserva de S/ 2 388,00 (Tabla 17), DoD (§VII.3), EDT (Figura VII.3.1; Tabla 18), horas-hombre y costos (Tablas 19–21), comunicaciones (Tabla 22) y cronogramas (Figuras VII.5.1, VII.5.2).
2. Fortaleza: control con línea base frente a ejecución (Tabla 23), hitos (Tabla 24), cambios CHG-01 a CHG-09 (Tabla 25) y evidencias de Trello (Figuras VII.6.1 a VII.6.9).
3. Fortaleza: honestidad. El PMV3 es «planificado»; el PR #6 no tiene aprobación de otro integrante (Figura VIII.36); el Daily del 09/11 solo tiene comentario de la Scrum Master (Figura VII.6.5).
4. Observación (fechas): §VII.5.3 habla de «corte al 05/11/2026» y del Sprint 6; la Tabla 23 dice Sprint 7 «Planificado», pero la Figura VIII.36 muestra un PR del Sprint 7 fusionado el 12/11. Hay tres fechas de corte (05/11, 11/11, 15/11).
5. Observación (control): presupuesto de S/ 24 872,40, línea base de S/ 23 688,00 y gasto real S/ 0,00 (§VII.4.6), sin SPI/CPI, burn-down ni velocidad; la Tabla 23 es cualitativa.
6. Observación (calidad del proceso): un PR sin revisión aprobada contradice el criterio 3 del DoD (§VII.3).
7. Evidencia adicional: la deriva entre `render.yaml` y el despliegue real (H-06) es un hallazgo de gestión de configuración que debería registrarse en el control de cambios.

| Prioridad | Mejora | Sección destino |
|---|---|---|
| Alta | Unificar fecha de corte y estado de los sprints | §VII.5.3; Tablas 23 y 24 |
| Alta | Registrar la aprobación de PR por otro integrante y documentar la política (CODEOWNERS o reglas de rama) | §VII.3 (criterio 3); Tabla 30; Figura VIII.36 |
| Media | Indicadores de control (SPI/CPI o burn-down) y presupuesto frente a gasto real | §VII.5.3 y §VII.4.5 |
| Media | Mostrar las 11 listas de Trello y completar las vistas pendientes | §VII.6.4 y Tabla 35 |
| Media | Registrar el trabajo del Sprint 7 y la deriva de `render.yaml` | §VII.7 (CHG-10 y CHG-11) |
| Baja | Añadir a la Tabla 17 los riesgos nuevos de la auditoría con probabilidad, impacto y VME | §VII.2.5 |

### 2.5 Diseño y Desarrollo de Soluciones — Cumple parcialmente

**Hallazgos**
1. Fortaleza: requisitos (Tablas 9 y 10), HU con criterios Dado/Cuando/Entonces (Tabla 11), pantallas (Figuras 2–6), BD y arquitectura evaluadas (Tablas 12 y 13), modelos lógico y físico (Figuras 7 y 8) y procedimiento almacenado (Figura 9).
2. Fortaleza: arquitectura inicial y actualizada (Figuras 10–13), con el cambio gestionado (RabbitMQ y Kubernetes descartados; Tabla 25).
3. Fortaleza: 435 pruebas, 0 fallos (Tabla 27; Figuras VIII.3.a–g), smoke 14/14 (Figura VIII.4), OpenAPI (Figuras VIII.17–VIII.20), `promtool` (Figura VIII.8.a) y experimento reproducible (Tabla 31; Figura VIII.39.a). La Tabla 33 distingue lo «Demostrado».
4. Hallazgo: los RNF (Tabla 10) no tienen resultados de seguridad ni de rendimiento bajo carga. §V.1 declara que JMeter y ZAP no se usaron y la Tabla 33 no tiene filas de rendimiento ni seguridad. La ingeniería inversa midió que Prediction pasa de 97 ms a 1,14 s con 8 usuarios concurrentes (H-04).
5. Hallazgo: H-01, H-02 y H-03 y el veredicto «NO APTO PARA PRODUCCIÓN» no están reflejados. La Tabla 33 declara «Control perimetral (RBAC): Demostrado» sin advertir que Prediction y Data Processing pueden invocarse sin Gateway.
6. Hallazgo: «hexagonal real» (§II.c) frente a «hexagonal nominal» en Prediction (H-19).
7. Hallazgo: la auditoría FURPS+ indica pendientes HU-07 (aprobación persistida) y HU-13 PDF.
8. Inconsistencia: Gateway Go con 32 pruebas (Tabla 27; Figura VIII.3.c) y 30 (Tabla 33; CHG-04; §V.2).

| Prioridad | Mejora | Sección destino |
|---|---|---|
| Alta | Subsección de verificación de RNF (seguridad y rendimiento) con resultados de ingeniería inversa, FURPS+ y OWASP, vinculando cada RNF de la Tabla 10 | §VIII.2.3 y nueva fila en la Tabla 33 |
| Alta | Ajustar «Control perimetral (RBAC)» a «Demostrado en el Gateway; elusible en la nube (H-01)» y documentar la remediación | Tabla 33 (§VIII.3.3); §VI.3 |
| Media | Matizar «hexagonal» por servicio | §II.c; §VI.3 |
| Media | Unificar 32 frente a 30 pruebas del Gateway Go | Tabla 33; CHG-04; §V.2 |
| Media | Declarar la validez del modelo (1 nodo, 864 registros) y el plan walk-forward | §VIII.1.3; §VIII.4.1 |
| Baja | Indicar el estado de HU-07 y HU-13 tras el Sprint 7 | Tablas 28 y 33 |

### 2.6 Análisis de Problemas — Cumple parcialmente

**Hallazgos**
1. Fortaleza: §1.1 con SIPOC, AS-IS/TO-BE, Ishikawa 6M (Tabla 1), árbol de problemas (Figura 1; Anexo C, punto 1), restricciones explícitas, problema general y tres específicos alineados a PMV1–PMV3, y objetivos medibles (§1.2).
2. Fortaleza: el informe declara lo que no afirma (restricciones 2 a 4). La Tabla 2 tiene captura reproducible (Figura 1.a).
3. Hallazgo: «de ~1 000 a picos de 8 000 concurrentes» (§1.1) es la única evidencia institucional y no lleva cita ni captura. El informe reconoce que no hay auditoría energética ni telemetría física.
4. Hallazgo: la Tabla 2 describe el dataset sintético (CPU media 50,1 %; 6,13 % fuera de SLA), no el problema real.
5. Hallazgo: Ishikawa y árbol no tienen criterio de priorización (Pareto, causa raíz validada) ni se enlazan con RF/HU.
6. Hallazgo: no hay costo actual del problema ni caracterización cuantitativa de afectados. La entrevista (Figura A.1) no se cita en §1.1.
7. Hallazgo: PE3 (reducción de consumo) no tuvo resultado favorable (§VIII.3.1) y el análisis del problema no lo refleja.

| Prioridad | Mejora | Sección destino |
|---|---|---|
| Alta | Citar la fuente de «1 000 a 8 000» (ISO 690) o marcarlo «referencial no verificado» | §1.1, primer apartado |
| Alta | Usar los resultados de la entrevista (Figura A.1) como evidencia primaria y ligarlos a cada causa de la Tabla 1 | §1.1, tras la Tabla 1 |
| Media | Priorizar causas y vincularlas con RF/HU | §1.1, tras la Figura 1 |
| Media | Aclarar que la Tabla 2 es del simulador, con columna «uso en el proyecto» | §1.1 «Análisis cuantitativo del dataset» |
| Baja | Contraste problema planteado frente a evidencia obtenida (PE3 solo en parte) | §X.1 y cierre de §1.1 |

### 2.7 Uso de Herramientas Modernas — Cumple

**Hallazgos**
1. Fortaleza: la Tabla 8 inventaría 13 categorías con versión, rol y limitación, y la selección se pondera con 7 criterios (§V).
2. Fortaleza: limitaciones medidas, no solo declaradas (Figuras 1.b y 1.c; Gateway Java 285,7 MiB frente a Go 8,0 MiB; 0 diferencias en 39 pruebas diferenciales).
3. Fortaleza: limitaciones de los asistentes de IA documentadas (1 de 8 falsos positivos; respuestas vacías con `SUCCESS`) y verificación humana obligatoria (§V.2); la IA se declara en la carátula.
4. Fortaleza: CI/CD y Git (Figuras VIII.36, VIII.37), MLflow (Figura VIII.1). La ingeniería inversa corrobora 311 pruebas sin fallos en Ubuntu 24.04.
5. Observación: SonarQube, JMeter, ZAP y Kubernetes figuran como no usados (§V.1). El informe no contiene SAST, SCA ni carga propios, aunque la ingeniería inversa sí hizo SCA (MLflow 2.22.5, 29 avisos, H-09) y medición de concurrencia.
6. Observación: la Tabla 32 afirma portabilidad «verificada en las tres plataformas» (Ubuntu 22.04, Windows 11/WSL2, macOS Sonoma) sin capturas ni comandos de Ubuntu ni macOS. Sin evidencia en el informe.
7. Observación: las figuras 1.a, 1.b y 1.c rompen la numeración de las figuras 1 a 13.
8. Observación: faltan comandos de instalación y matriz de versiones (Python 3.12, Java 21, Go 1.25).

| Prioridad | Mejora | Sección destino |
|---|---|---|
| Alta | Respaldar la Tabla 32 con capturas o comandos, o reducirla a lo verificado (Windows 11/Docker; Ubuntu 24.04 nativo) | §VIII.3.2 |
| Media | Incorporar a la Tabla 8 las herramientas realmente usadas en calidad (SCA, `promtool`, concurrencia, FURPS+/OWASP) con resultados | §V.1 y §V.3 |
| Media | Incluir la prueba de concurrencia (97 ms → 1,14 s; 9,8 → 7,0 req/s) y su remediación | §V.2 y §VIII.4.2 |
| Baja | Renumerar las figuras 1.a, 1.b y 1.c | Cap. I, Cap. V |
| Baja | Tabla de versiones y comandos de reproducción | §V.1, tras la Tabla 8 |

## 3. Mejoras priorizadas (consolidado)

| # | Prioridad | Atributo | Mejora | Sección destino |
|---|---|---|---|---|
| 1 | Alta | Sociedad / Diseño | Corregir Tabla 4 y Tabla 33 con el estado real de seguridad y su plan de remediación | Tabla 4; Tabla 33; nueva subsección en §VIII.2 |
| 2 | Alta | Medioambiente | Reformular ODS 13 y CO2e (sin reducción medida) | §1.2; §III.c; §VIII.3.1 |
| 3 | Alta | Herramientas | Respaldar o reducir la Tabla 32 | §VIII.3.2 |
| 4 | Alta | Gestión | Unificar fechas y estados; cerrar la revisión por pares de PR | §VII.5.3; Tabla 23; §VII.3; Figura VIII.36 |
| 5 | Alta | Análisis de Problemas | Citar el dato «1 000 a 8 000» y usar la entrevista como evidencia primaria | §1.1; Figura A.1 |
| 6 | Media | Diseño / Herramientas | Verificar RNF de seguridad y rendimiento con resultados reales | §VIII.2.3; Tabla 33; §V.2 |
| 7 | Media | Ingeniería | Unificar el −30 %, justificar P_idle y P_max, declarar 1 nodo y 864 registros | §V.3; Tabla 34; §II.b; §VIII.1.3 |
| 8 | Media | Medioambiente | Balance energético neto y sensibilidad de la Tabla 31 | §VIII.4.2; §VIII.3.1 |
| 9 | Media | Gestión | SPI/CPI o burn-down y vistas de Trello pendientes | §VII.5.3; §VII.6.4; Tabla 35 |
| 10 | Media | Sociedad | Pruebas con usuarios y matriz de partes interesadas con ética de IA | §VIII.2.3; §III.a |
| 11 | Media | Diseño | Matizar «hexagonal» por servicio; unificar 32 frente a 30 pruebas | §II.c; §VI.3; Tabla 33; CHG-04 |
| 12 | Baja | Análisis | Priorizar causas (Pareto) y vincular a RF/HU | §1.1, tras la Figura 1 |
| 13 | Baja | Herramientas | Renumerar figuras; tabla de versiones y comandos | Cap. I, Cap. V |
| 14 | Baja | Sociedad | Escenario económico y actualizar Tabla 35 | §III.b; Anexo C |

## 4. Plan corto para el informe final (Sprint 8, 24/11 a 30/11/2026)

1. **24–25/11, honestidad (mejoras 1, 2, 3):** reescribir Tabla 4, Tabla 33 y ODS 13; reducir o evidenciar la Tabla 32.
2. **25–26/11, integración de evidencias (mejoras 6, 7, 10):** resumen de la ingeniería inversa (23 hallazgos, 2 críticos) y de la auditoría final (FURPS+ 87,00 % bruto; OWASP 86,0/100 estimado; «NO APTO PARA PRODUCCIÓN»). Resultados de pruebas con usuarios solo si existen; si no, mantenerlas como planificadas.
3. **26–27/11, gestión (mejoras 4, 9):** actualizar fechas y estados, SPI/CPI o burn-down, una aprobación de PR por otro integrante y vistas de Trello.
4. **27–28/11, análisis y sostenibilidad (mejoras 5, 8, 12):** citar el dato «1 000 a 8 000», priorizar causas y calcular el balance energético neto con datos medidos.
5. **28–29/11, cierre formal (mejoras 11, 13, 14):** unificar cifras, renumerar figuras, actualizar Tabla 35 y reexportar.
6. **29–30/11, verificación y sustentación:** comprobar que cada número del informe tenga su captura o comando.

Criterio de cierre: los cuatro atributos en «Cumple parcialmente» pasan a «Cumple» solo si las mejoras de prioridad Alta tienen evidencia (captura, comando o tabla) en el informe final.

## 5. Declaración de honestidad

- No se asigna «Cumple» por afirmaciones sin evidencia en el informe. La portabilidad multi-SO (Tabla 32), el cumplimiento legal (Tabla 4), el balance energético neto (§III.c) y las pruebas con usuarios (Tabla 30) no tienen evidencia en el informe del 15/11.
- Los hallazgos de seguridad provienen de documentos del 19/11/2026 (análisis estático y documental). La auditoría advierte que no incluyó pentest, DAST ni validación en Supabase, y que Supabase y Render deben verificarse. Lo que se afirma aquí es que el informe no los reconoce, no que las vulnerabilidades estén confirmadas en producción.
- Esta evaluación no sustituye la valoración del docente ni de ICACIT.
