# Reporte de evaluación de cumplimiento ICACIT 2025 — Informe final de la Unidad IV

**Auditoría de atributos del graduado: competencias transversales y específicas**

| Campo | Detalle |
|---|---|
| Proyecto | Green AI: sistema de monitoreo y predicción de demanda computacional para apoyar la gestión eficiente de recursos en entornos universitarios |
| Equipo | Ricardo Porras Veli; Leonid Kisley Orlando Huamán Collazos; Gina Diana Barrera Peña; Jhonny Cristhian Quintana Carhuaricra |
| Docente | Jorge Alfredo Guevara Jiménez |
| Curso / NRC | Taller de Proyectos 1 · NRC 30170 |
| Fecha del reporte | 26/11/2026 |
| Documento evaluado | `entregables/semana15/informe-unidad-IV.md` (versión corregida del 26/11/2026, commit `9e2d172`) |
| Reportes anteriores | 19/11/2026 (`entregables/semana14/reporte-icacit.md`, sobre el informe de la Unidad III) y reporte del equipo en Word |
| Naturaleza | **Autoevaluación asistida por IA (Claude, de Anthropic). No es un dictamen oficial de ICACIT ni del docente** |

## 0. Método, escala y límites

- **Criterio:** consigna «S14. Evaluación de evidencias de ICACIT» (siete competencias, hallazgos y mejoras por atributo y sección donde colocarlas) y competencias del sílabo. En `guias/` no se halló una rúbrica ICACIT con niveles por atributo; como apoyo se usaron la guía S6 de trazabilidad y la lista de cotejo de la Unidad IV.
- **Escala:** *Satisfactorio* (evidencia suficiente; las observaciones no alteran lo demostrado); *Parcial* (evidencia incompleta, no verificable o contradicha en puntos centrales); *No cumple* (sin evidencia).
- **Qué se hizo:** lectura documental del Markdown (las Tablas 3.a a 3.d y 8.1 a 8.47 solo de forma parcial), contraste puntual con el repositorio (configuración y dataset de Prediction, `pom.xml`, Compose, CSV de carga, ingeniería inversa), inspección de las Figuras VIII.12 a VIII.14 y del DOCX exportado el 25/11. «L123» es la línea del Markdown evaluado.
- **Qué no se hizo:** no se reejecutaron pruebas ni se verificaron Render, Supabase, Trello, el video ni los enlaces.
- **Aviso de versión:** el DOCX y el PDF de `exportados/semana15/` son anteriores a las correcciones del 26/11. Antes de evaluar el informe con otra herramienta hay que reexportarlo.

## 1. Matriz ejecutiva de cumplimiento

| # | Atributo | Tipo | 19/11 (Unidad III) | Reporte del equipo | **Ahora (26/11)** | Síntesis |
|---|---|---|---|---|---|---|
| 1 | Conocimientos de Ingeniería | Transversal | Satisfactorio | Satisfactorio | **Parcial** | Buena base matemática y de software, pero el dataset y las variables contradicen el repositorio. |
| 2 | Análisis de Problemas | Específica | Parcial | Satisfactorio | **Parcial** | Análisis estructurado; sin evidencia primaria, causas sin priorizar, sin PE4. |
| 3 | Diseño y Desarrollo de Soluciones | Específica | Parcial | Parcial | **Parcial** | 492 pruebas y despliegue; HU-07 parcial, sin usuarios y latencia bajo carga sobre RNF-02. |
| 4 | Uso de Herramientas Modernas | Específica | Satisfactorio | Satisfactorio | **Satisfactorio** | Selección y limitaciones medidas; versiones contradictorias y puntajes sin validar. |
| 5 | El Ingeniero y la Sociedad | Transversal | Parcial | Parcial | **Parcial** | Estado legal honesto; RLS abierto, `password` sin evidencia, sin usuarios. |
| 6 | Medioambiente y Sostenibilidad | Transversal | Parcial | Parcial | **Parcial** | Honestidad ambiental; sin balance neto, CO2e ni ahorro demostrado. |
| 7 | Gestión de Proyectos | Transversal | Satisfactorio | Parcial | **Parcial** | Gestión amplia; cronograma y estados desfasados e incoherencias. |

**Resumen:** 1 satisfactorio, 6 parciales, ninguno en «No cumple». Las bajas no significan que el informe haya empeorado: esta revisión contrastó más afirmaciones con el repositorio.

## 2. Evaluación detallada por atributo

### 2.1 Conocimientos de Ingeniería (transversal) — Parcial

**Evidencias verificadas**

- Regresión supervisada, codificación cíclica, partición cronológica 70/15/15, MAE, RMSE y sMAPE y descarte justificado de F1 (§II.a, L217–258).
- Integración trapezoidal de la potencia y CO2e = E·FE (§II.b, L260–280); modelo proxy P(u) (Figura VIII.2).
- Arquitectura hexagonal, contratos y seguridad (§II.c, L282–295); selección ponderada (Tablas 3 y 3.a a 3.d).
- H1 y criterios (§VIII.1.2), cuatro alternativas (Tabla 26), reejecución con semilla 42 (Figura VIII.1.a).

**Brechas**

1. **Crítica, dataset:** §VIII.1.3 (L2293) declara 80 640 muestras cada 15 s en `sample_dataset.json`; el archivo contiene **864 registros cada 5 minutos, del 01 al 03/09/2026, de un nodo**, coherente con n = 125 y 129 y con la limitación H-14 declarada (L3132). Se repite en la Tabla 34 (L2990); la Tabla 29 (L2497–2506) presenta 80 640 y 78 059 como la serie del benchmark, y no se hallaron en el código ni en los datos de `software/`.
2. **Variables:** L230–231 declara retardos de CPU y memoria y ventanas de 15, 30 y 60 min; `config/config.yaml` usa retardos 1–3 de CPU, ventanas de 15 y 30 min y `use_additional: false`. L2962 y L2991 dicen «t−1 … t−15», frente a t−1 a t−3 (L2295).
3. P_idle = 300 W y P_max = 600 W sin fuente ni análisis de sensibilidad (§VIII.3.1, L2894).
4. No hay matriz «conocimiento → decisión de diseño → evidencia» (guía S6).
5. El error en picos se cuantifica (L2334) pero no su signo; no afirmar que el modelo «subestima» sin calcular el sesgo.

**Acción:** corregir §II.a, §VIII.1.3 y las Tablas 29 y 34 según el repositorio (o adjuntar el dataset de 14 días si existe); dar fuente a P_idle y P_max o rotularlos como supuesto; agregar la matriz al final del Capítulo II. Con los puntos 1 y 2 corregidos el atributo puede volver a satisfactorio.

**Cambio:** atendidos la base del −30 % y la declaración de H-14. La observación del reporte del equipo sobre las fórmulas de MAE y RMSE era **incorrecta** (L250–252 son correctas): se retira. Baja a parcial por las contradicciones 1 y 2, no detectadas antes.

### 2.2 Análisis de Problemas (específica) — Parcial

**Evidencias verificadas**

- SIPOC y AS-IS/TO-BE, Ishikawa 6M (Tabla 1), causa raíz, árbol de problemas (Figura 1), análisis del dataset (Tabla 2, Figura 1.a), restricciones y formulación (§1.1, L95–188).
- El dato de 1 000 a 8 000 usuarios está rotulado «referencial no verificado» (L99).
- Antecedentes y corrección sobre el 87,48 % de Khan et al. (Tabla 5; L424–427); discusión comparativa (§VIII.5, Tabla 34).
- Cuatro conclusiones, una por objetivo específico (§X.1).

**Brechas**

1. Sin evidencia primaria del problema real: la Tabla 2 describe datos sintéticos y la Figura A.1 es una fotografía de consulta, no usada en §1.1.
2. Causas sin priorización ni enlace con RF o HU; sin KPI de línea base ni diagrama BPMN.
3. Hay OE4 sin **PE4** (L186–201). La conclusión del OE3 no responde PE3 en sus términos. OE3 dice «consumo energético físico/trapezoidal» (L200), pero la energía es modelada.
4. Referencias [4], [5], [8] y [9] sin citar; [14] solo en el Anexo C; la numeración no sigue el orden de aparición.

**Acción:** añadir PE4; responder PE3 en §X.1; quitar «físico»; tabla causa → prioridad → RF/HU; citar o retirar las referencias sobrantes. La evidencia primaria requiere trabajo del equipo.

**Cambio:** atendidos el rótulo del dato institucional, las cuatro conclusiones, las referencias al final y la discusión por entregable. Sin evidencia primaria nueva: **no se acepta la subida** del reporte del equipo.

### 2.3 Diseño y Desarrollo de Soluciones (específica) — Parcial

**Evidencias verificadas**

- RF-01 a RF-20 y RNF-01 a RNF-09 (Tablas 9 y 10); historias con criterios Dado/Cuando/Entonces (Tabla 11).
- Wireframes y prototipos por PMV (Figuras 2 a 12); modelo lógico y SQL (Figura 13; Listados 1 y 2); arquitectura (Tabla 13; Figuras 15 y 17).
- 492 pruebas al 19/11 (Tabla 30.a; Figuras VIII.38 a VIII.44), smoke 14/14 (Figura VIII.4), rechazo 401 en Render (Figura VIII.46), experimento de 126 intervalos (Tabla 31; Figura VIII.51.a).
- Límites declarados (Tablas 28, 30 y 33; §VIII.6); adaptadores enlazados (Anexo G).

**Brechas**

1. **RNF-02 e HU-03 (p95 < 2 s):** la carga de 601 transacciones con concurrencia 3 (Figura VIII.32, L2731) dio p95 de 3,5 s en predicción y recomendación. HU-03 figura «Aprobado» (Tabla 28, L2419) y H1 se acepta con la latencia por lote de 9,46 ms (L2319). El informe no contrasta el incumplimiento.
2. No hay tabla de verificación de cada RNF.
3. L2768 y L2942 atribuyen la latencia a H-03; en la ingeniería inversa es **H-04** (H-03 es la clave `anon`).
4. §III.f (L403) afirma límites `deploy.resources.limits` y cadencia de 5 min: no se hallaron límites en los Compose revisados y la recolección es cada 15 s.
5. La Tabla 27 (L2366) atribuye al Gateway Go «límites de tasa», pero OW-05 declara que no hay *rate limiting*.
6. Las Figuras VIII.12 a VIII.14 se rotulan como tablas en PostgreSQL / Supabase, pero son hojas de cálculo (L2592–2602).
7. Pendientes reales: HU-07 sin adaptador Supabase y con SQLite efímero; H-01 mitigado solo en decisiones; sin sesión real (F-03); sin usuarios ni acta; sin trazas reales; CHG-001-2026 no implementado.

**Acción:** subsección «Verificación de requisitos no funcionales» en §VIII.2.3; HU-03 «Parcial» en rendimiento en la nube; corregir 3 a 6. El equipo debe resolver H-04, el adaptador HU-07 y las pruebas con usuarios.

**Cambio:** se incorporaron resultados del Sprint 7, H-01, PDF HU-13, wireframes y adaptadores. El incumplimiento de RNF-02 no estaba en reportes previos.

### 2.4 Uso de Herramientas Modernas (específica) — Satisfactorio

**Evidencias verificadas**

- Inventario con rol y limitación (Tabla 8) y selección ponderada (Tablas 8.0 a 8.47), declarada como juicio posterior, apoyado por IA y sin validar (L525).
- Imágenes y memoria (Figuras 1.b y 1.c); evaluación de asistentes de IA con 1 falso positivo de 8 hallazgos (§V.2).
- MLflow local (Figura VIII.1), OpenAPI (Figuras VIII.17 a VIII.20), `promtool` (Figura VIII.8.a), PR e integración continua (Figuras VIII.48 y VIII.49), limitaciones (§VIII.2.4).

**Brechas**

1. Tablas 8 y 20 dicen Spring Boot 3.x/3.3 y Go 1.22; los `pom.xml` indican Spring Boot 4.1.1 y `go.mod` Go 1.25.
2. La Tabla 8 llama «alternativa» al Gateway Go, que según CHG-08 es el configurado en Render.
3. §V.1 y §V.3 conservan cifras del 15/11 (435), fechadas y remitidas a la Tabla 30.a: aceptable.
4. Sin SonarQube, JMeter ni OWASP ZAP (declarado); MLflow sin servidor.
5. Puntajes de factores sin validar por el equipo.

**Acción:** corregir versiones; validar puntajes; si hay tiempo, adjuntar un análisis estático o de carga.

**Cambio:** evidencia nueva (matrices ponderadas, pruebas del Sprint 7, PR aprobado). Las cifras 435/492 son mediciones con su captura y no deben sobrescribirse.

### 2.5 El Ingeniero y la Sociedad (transversal) — Parcial

**Evidencias verificadas**

- Seis aspectos (§III.a a §III.f) y marco legal con estado (Tabla 4).
- H-01 y H-02 reconocidos (L399); supervisión humana (`executionAllowed=false`).
- Partes interesadas (§VII.2.4); hallazgos OWASP con estado (Tablas 34.a y 34.b).

**Brechas**

1. Políticas RLS «Permitir todo» pendientes (estado del 12/11). La columna `password` está «corregida según el equipo», **sin evidencia adjunta**.
2. La Figura VIII.13 y el script del Anexo B (L3305) muestran contraseñas sintéticas legibles; revisar correos en VIII.15.c a VIII.15.e.
3. Sin matriz de impactos por parte interesada, análisis ético de IA (sesgo, falsos positivos y negativos, responsabilidad) ni accesibilidad WCAG; §III.f no trata seguridad de la información.
4. Justificaciones social y económica sin indicadores.
5. Sin usuarios finales; la Figura A.1 no es validación (así se declara).
6. La portada incluye al asistente de IA bajo «Integrantes» (L45): confirmar si debe pasar a una declaración de uso de IA.

**Acción:** matriz de impactos y ética de IA; ocultar contraseñas; evidencia de Supabase, RLS con rol de solo lectura y sesión con usuarios.

**Cambio:** la Tabla 4 ya no declara controles inexistentes. «Atendida» en la Tabla 35 se refiere a cubrir apartados, no a cerrar riesgos.

### 2.6 Medioambiente y Sostenibilidad (transversal) — Parcial

**Evidencias verificadas**

- ODS 7, 9, 12 y 13 (ODS 13 solo como método de estimación) (§1.2, L203–209).
- Balance neto declarado pendiente (§III.c, L382).
- Energía modelada −0,17 %, −0,16 % y −0,13 % sin ahorro demostrado (Tabla 31; §X.1).
- *Green-in-AI*: imagen y memoria (§VIII.4.2; Figuras 1.b y 1.c); PUE y refrigeración (§VII.8; Tabla VII.8).

**Brechas**

1. Sin CO2e calculado (HU-10); el factor del SEIN está por validar.
2. Sin balance energético neto ni tabla ODS → meta → indicador → evidencia.
3. No se mide la energía del propio sistema; §IX.3 (L3096) afirma que se evitó contrarrestar beneficios sin medirlo.
4. Mantener lenguaje potencial sobre el ODS 7.
5. CHG-001-2026 sin implementar.

**Acción:** redactar L3096 como beneficio no medido; añadir tabla ODS y sensibilidad a P_idle y P_max. Un CO2e opcional debe rotularse «estimado»: Wh × factor no equivale a un SCI de ISO/IEC 21031.

**Cambio:** atendidos ODS 13, balance neto prometido y coherencia de la variación energética. Sin medición nueva.

### 2.7 Gestión de Proyectos (transversal) — Parcial

**Evidencias verificadas**

- Selección y adaptación (Tablas 6, 7, 14 y 15), RACI (Tabla 16), riesgos y presupuesto (Tablas 17 y 19 a 21), DoD y EDT (§VII.3; Tabla 18), comunicaciones (Tabla 22).
- Control y cambios (Tablas 23 a 25 y VII.8); Trello (Figuras VII.6.1 a VII.6.9); PR #7 aprobado (Figuras VIII.48 y VIII.48.a).

**Brechas**

1. **Cronograma desfasado:** corte 11/11 (Figura VII.5.2) y 05/11 (L2119), Sprints 7 y 8 «Planificados» (Tabla 23), PMV2 «En proceso» (Tabla 24), frente a verificaciones al 25/11 (Tabla 30).
2. La Tabla 7 elige Scrum (4,85) sobre Scrumban (4,15), pero L1856 declara *Scrumban*; se dicen sprints de dos semanas aunque el 7 y el 8 duran una (Tabla 15).
3. L2156 indica HU-01 a HU-20; la Tabla 11 tiene HU-01 a HU-16 y el CHG llama nuevas a HU-17 y HU-18. Nombres de HU-02 y HU-11 (L2186–2187) distintos a la Tabla 11.
4. Sin SPI/CPI, *burndown* (mencionado sin gráfico) ni velocidad.
5. Un solo comentario en el Daily (Figura VII.6.5); DoD no visible (Figura VII.6.9).
6. La Tabla 30 marca «Video y póster: Ejecutada», pero el video es el de la Unidad III. Falta el artículo en inglés de OE4.

**Acción:** corregir 2, 3 y 6 en texto; actualizar avance, Gantt y Trello con datos reales antes de tocar las Tablas 23 y 24.

**Cambio:** mejoran la revisión por pares y el registro de cambios; el desfase de fechas se agravó. Pasa de satisfactorio a parcial.

## 3. Correspondencia con las siete competencias del sílabo

| Competencia del sílabo | Tipo | Secciones | Evidencia clave | Brecha principal | Nivel |
|---|---|---|---|---|---|
| Conocimientos de Ingeniería | Transversal | Cap. II; §VIII.1 | Tablas 3 y 26; Figura VIII.1.a | Dataset y variables | Parcial |
| Medioambiente y Sostenibilidad | Transversal | §1.2; §III.c; §VIII.4.2 | Tablas 31 y VII.8 | Sin balance neto ni CO2e | Parcial |
| El Ingeniero y la Sociedad | Transversal | Cap. III; §VII.2.4; §VIII.7 | Tablas 4 y 34.b | RLS, `password`, usuarios | Parcial |
| Gestión de Proyectos | Transversal | Cap. IV y VII | Tablas 17, 21 y 25; Figura VII.6.8 | Gantt, avance, incoherencias | Parcial |
| Diseño y Desarrollo de Soluciones | Específica | Cap. VI; §VIII.2–3; Anexo G | Tablas 30.a y 33; Figura VIII.46 | RNF-02, HU-07, usuarios | Parcial |
| Análisis de Problemas | Específica | §1.1; §1.2; §VIII.5 | Tablas 1 y 2; Figura 1 | Evidencia primaria, PE4 | Parcial |
| Uso de Herramientas Modernas | Específica | Cap. V; §VIII.2.4 | Tablas 8 y 8.0; Figuras 1.b y 1.c | Versiones; puntajes | Satisfactorio |

La guía S6 trabaja además con una sexta competencia del curso (prueba de concepto y arquitectura híbrida o hexagonal), que no figura entre las siete del sílabo. Su evidencia está en §VIII.1 (dictamen «GO con condiciones»), §VI.3 y el Anexo G; hereda las brechas del dataset y de HU-07.

## 4. Seguimiento de las observaciones del reporte del equipo

| Observación | Estado al 26/11 |
|---|---|
| Errata en MAE y RMSE | No procede: las fórmulas son correctas |
| Latencia de 97 ms a 1,14 s | Vigente y declarada; el identificador correcto es H-04 |
| PE3 desalineado | Parcial: falta respuesta explícita; no reescribir la pregunta tras el experimento |
| H-01 y persistencia efímera de HU-07 | Vigentes y declaradas |
| Acta de usuarios | Pendiente |
| 435 frente a 492 pruebas | Atendida con fechas |
| `password` y RLS | `password` corregida según el equipo, sin evidencia; RLS pendiente |
| Factor de emisión del SEIN | Pendiente, por validar |
| Variación energética «−0,16 %» | Precisada: −0,17 % (margen 10 %) y −0,16 % (20 %) |
| Gantt y Tabla 23 | Pendientes |
| Texto marcador residual | Atendido |

## 5. Correcciones de texto posibles en el informe (sin trabajo técnico nuevo)

Las marcadas con (*) requieren que el equipo confirme el dato.

| Prioridad | Línea(s) | Corrección | Atributo |
|---|---|---|---|
| 1 | L2293, L2497–2506, L2990 (*) | Dataset real: 864 registros de 5 min, 3 días, un nodo; retirar o respaldar 80 640 y 78 059 (revisar Figura VIII.11 y L2489–2495) | 2.1 |
| 2 | L230–231, L2962, L2991 | Retardos 1–3 solo de CPU; ventanas de 15 y 30 min | 2.1 |
| 3 | L2319, L2419, L2731; §VIII.2.3 | Declarar p95 de 3,5 s frente a RNF-02; HU-03 parcial en la nube; tabla de RNF | 2.3 |
| 4 | L2178, L2216, L2663, L2697–2713 | Quitar la numeración antigua del texto alternativo (Word la imprime como leyenda); revisar L1900, L1954, L2099, L2105 y L2134 | Presentación |
| 5 | L2592–2602 | Rotular VIII.12 a VIII.14 como hojas de cálculo sintéticas | 2.3 |
| 6 | L2596, L3305 | Tapar contraseñas en la imagen y el script | 2.5 |
| 7 | L403, L2366 | Retirar límites de memoria no hallados y «límites de tasa»; cadencia de 15 s | 2.3 |
| 8 | L2768, L2942 | H-03 → H-04 | 2.3 |
| 9 | L464, L1856, L2156, L2186–2187 (*) | Unificar Scrum/Scrumban, duración de sprints, total y nombres de HU | 2.7 |
| 10 | L2772 | «Video y póster»: Parcial | 2.7 |
| 11 | L509–511, L2039 | Spring Boot 4.1.1 y Go 1.25 | 2.4 |
| 12 | L186–200; §X.1 | Añadir PE4, responder PE3, quitar «físico» | 2.2 |
| 13 | L3153–3185 | Citar o retirar [4], [5], [8], [9]; citar [14]; ordenar; fecha de consulta en [15] y [16] | 2.2 |
| 14 | L2894 (*) | P_idle y P_max como supuestos con fuente o sensibilidad | 2.1, 2.6 |
| 15 | §III.a/e; §1.2; Cap. II (*) | Matrices de impactos y ética de IA, ODS → indicador, conocimiento → diseño, causa → RF/HU | Varios |
| 16 | L2991 (*) | Verificar contra [3] la expansión de la sigla AGEN | 2.2 |
| 17 | L3096 | Redactar como beneficio no medido | 2.6 |
| 18 | L45 (*) | Ubicación de la declaración de uso de IA | 2.5 |
| 19 | Cap. VIII | Cerrar el salto de Figuras VIII.35–37 (la 32 solo tiene leyenda en el texto alternativo) | Presentación |
| 20 | Tablas 35, D.1, D.2 | Reflejar estas brechas; D.1 menciona «Anexos A a E» y ya hay F a H | Presentación |

## 6. Pendientes que requieren trabajo del equipo (en orden)

1. **Validación con usuarios finales y acta** (indicador 9 de la lista de cotejo). No fabricarla ni presentar la consulta con el experto como acta.
2. **Supabase:** evidencia de la corrección de `password` y RLS con rol de solo lectura.
3. **Avance del PMV y Gantt ejecutado**, Sprints 7 y 8 y Trello (incluida la tarea de Kubernetes marcada como completada).
4. **Recapturas con el enlace visible**, ocultando correos y contraseñas.
5. **Adaptador Supabase para HU-07**, migración 001 y pruebas; sesión real (F-03); cierre de H-01.
6. **Rendimiento:** corregir H-04 y volver a medir frente a RNF-02.
7. **Validar los puntajes de factores.**
8. **Supuestos por validar:** factor de emisión del SEIN, P_idle y P_max.
9. Video de la Unidad IV, artículo en inglés y re-medición FURPS+/OWASP.
10. Reexportar Word y PDF, revisar índices y volver a ejecutar la evaluación ICACIT.

## 7. Declaración de honestidad

No se subió ninguna calificación. «Corregido según el equipo» no equivale a verificado. FURPS+ 86 % y OWASP 83,5/100 son las cifras de la semana 13, anteriores a la ola 2. Las contradicciones se basan en el repositorio local al 26/11/2026; si existe otra fuente (por ejemplo, un dataset de 14 días), el equipo debe adjuntarla. El resultado de la evaluación del docente puede diferir, porque no se conoce el prompt que utiliza.
