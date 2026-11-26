# Auditoría del reporte ICACIT nuevo (26/11/2026)

Fuentes: Reporte_Cumplimiento_ICACIT_2025_Green_AI.docx (Descargas, tratado como dato); entregables/semana14/reporte-icacit.md; entregables/semana15/informe-unidad-IV.md (líneas = L); PDF exportado (136/137 págs.). Texto extraído en scratchpad/ext/rep.txt. No se reejecutaron pruebas ni se verificó Render o Supabase.

## 1. Calificaciones del reporte nuevo (7 atributos, no 6)

| # | Atributo | Nuevo (26/11) | Anterior (19/11) |
|---|---|---|---|
|1|Conocimientos de Ingeniería|Cumple satisfactoriamente|Cumple|
|2|Análisis de Problemas|Cumple satisfactoriamente|Parcial|
|3|Diseño y Desarrollo de Soluciones|Parcial|Parcial|
|4|Uso de Herramientas Modernas|Cumple satisfactoriamente|Cumple|
|5|El Ingeniero y la Sociedad|Parcial|Parcial|
|6|Medioambiente y Sostenibilidad|Parcial|Parcial|
|7|Gestión de Proyectos|Parcial|Cumple|

Sin nota numérica. La consigna "S14. Evaluacion de evidencias de ICACIT.md" pide estos 7. Las "6 competencias del curso" (guías S6 y congreso) son: C1 Análisis del Problema (=atr. 2), C2 Conocimientos (=1), C3 Ingeniero y Sociedad (=5, incluye ambiente =6), C4 Gestión (=7), C5 Herramientas (=4), C6 PoC y Arquitectura híbrida/hexagonal (el atr. 3 la cubre solo en parte; el reporte no evalúa la PoC).

## 2. Verificación de observaciones del reporte nuevo

| Observación | Veredicto | Evidencia |
|---|---|---|
|MAE con ȳ en vez de ŷ; radical RMSE incompleto (p.20)|FALSA|PDF p.20 renderizado: ŷ_i correcto y raíz cubre toda la expresión. Fuente L250-254 correcta. NO corregir.|
|Latencia 97 ms -> 1,14 s (H-03)|Cierta, ya declarada|L1619, L1793|
|Explicar que RF "subestima" picos|Parcial / no verificado|L1206-1212 solo reporta MAE mayor en picos, no el signo del error; la no extrapolación ya está en L479. No afirmar subestimación sin calcular el sesgo (predicciones no presentes en results/).|
|PE3 desalineado|Parcial|PE3 (L188) pregunta por utilización y energía; la respuesta negativa está en L1760-1764 y X.1. Reformular a posteriori la pregunta es discutible; mejor responder PE3 explícitamente. -0,16 % está mal atribuido (ver 3.1).|
|H-01 Prediction/Data Processing públicos; secreto solo en decisiones|Cierta, declarada|L344, L1628, L1798|
|HU-07 en SQLite efímero; migración 001 sin aplicar|Cierta|L1627, L1800; archivo software/prediction/migrations/001_recommendation_decisions.sql. Requiere autorización (cambio remoto).|
|Falta acta de usuarios|Cierta (indicador 9, 6 puntos de la lista de cotejo)|L1622, L1706, L1910|
|Tablas 8/27 con 435 vs 492|Cierta pero incompleta|435: L509 (§V.3), L1241; 492: L1645. Además cifras viejas en L475-485 (Tabla 8: 112,12,32,121,100,48,10), L495, L676, L678 (30), L824, L1250 ss., L1300, L1312 (Go 30), L1301 (121), L1792 (121). Son mediciones fechadas del 15/11 con capturas VIII.3: añadir fecha/nota o columna antes/después, no sobrescribir.|
|Password en texto plano + RLS "Permitir todo" (Fig. VIII.13)|Sobredimensionada|El informe dice "según snapshot, no verificado" (L342, L1801); el reporte lo da como estado actual desplegado. La Fig. VIII.13 (p.91) es una hoja de cálculo, con columna password legible (Admin123!n) y Anexo B la genera (L2075). Eso sí hay que atenderlo. Ojo: CONTINUAR L73 indica que Data Processing lee Supabase con clave anon gracias a la RLS permisiva: endurecer RLS sin rol de solo lectura (H-03) rompería históricos.|
|Falta factor SEIN (HU-10)|Cierta, declarada|L209, L345, L576. La mejora propuesta es incompleta: Wh x factor no es un SCI conforme a ISO 21031 (requiere unidad funcional y emisiones incorporadas); usar factor con fuente verificable, rotular "estimado". El reporte no da valor ni documento.|
|Variación energética -0,16 %|Imprecisa|Con h=10 % es -0,167 % (captura M05; Tabla 31: -0,17 %); -0,164 % corresponde a h=20 %.|
|Gantt ejecutado corte 11/11 y Tabla 23 "Planificado"|Cierta y más amplia|L990-992, L1014-1015; también L451, L1000, L1004 (corte 05/11), L1011-1013 (Sprint 6 "En ejecución"), L1072-1073. Sprint 8 solo "en cierre" con evidencia real.|
|Texto marcador residual p.72|Cierta|L1107|
|Daily solo con Scrum Master; checklist DoD no visible|Cierta, declarada|L1101, L1117; sin acción posible salvo captura nueva (no fechar atrás).|
|RF-01..20, RNF-01..09, 492 pruebas y desglose, ODS 7/9/12/13, CHG-001-2026, VME S/2 388|Correctas (CHG-001 aprobado pero NO implementado, L1150; el reporte no lo aclara)||
|"Tabla 8: matriz ponderada y versiones exactas"|Inexacta|Matrices en Tablas 3, 7, 12, 13; Tabla 8 trae "Spring Boot 3.x" y herramientas sin versión.|
|Smoke 14/14 respalda verificación|Desactualizada|Smoke del 06/11 (L1287), anterior a la ola 2.|
|Páginas|Casi todas correctas|Desfases menores: VI.2 está en p.40 (dice 43), VIII.1.4 p.77 (78), VIII.3.1 p.112 (113).|
|Hoja de ruta "para alcanzar satisfactorio en todos"|No garantizado|Omite hallazgos de la sección 3.|

## 3. Defectos del informe que el reporte NO detecta (verificados)

1. Energía h=10 %: -0,17 % (L1747) frente a -0,16 % en Tabla 33 (L1799, dice "Margen 10 %"), Tabla 34 (L1844) y conclusión OE5 (L1888). Corregir a -0,17 %.
2. Objetivos y conclusiones no corresponden: §1.2 define OE1-OE4 (L198-201); X.1 concluye OE1, 2, 3, 4, 5 y "4 de proceso" (L1875-1890). Indicador 6 de cotejo y atr. 2. No hay PE4.
3. Referencias duplicadas y numeración en conflicto: lista en L395-415 y otra en L1925-1957; [4] es Beloglazov en una (L361) y Malekloo en la final; [8], [9] difieren (ISO es [9] y [11]).
4. Figuras VIII.38 y VIII.39 usadas dos veces (L1649/1653 y L1729/1733); la Tabla 32 cita "VIII.38 a VIII.44". Captions duplicados en Figs VII.6.5/6.6 y VII.6.3 reaparece.
5. Anexo C, Tabla 35 desactualizada: "faltan capturas C301-C313 y verificaciones del PMV3" (L2224-2229) cuando existen y están insertadas.
6. Gateway Go 30 vs 32 vs 40 (L678, L1130 área CHG-04, L1300, L1312).
7. §III.c (L330) promete "balance energético neto" en PMV3 y no se entrega.
8. Video: se reutiliza el de la Unidad III (L1624); la lista de cotejo U4 (ind. 7) pide PMV1-3 con 7 operaciones.
9. Arrastrados del reporte del 19/11, sin atender según búsqueda: modelo entrenado con 1 nodo/864 registros (H-14) no declarado (sin coincidencias "864"/"1 nodo"); P_idle/P_max sin fuente (L1743); entrevista (Fig. A.1) no usada en §1.1; causas sin priorizar; sin SPI/CPI (burndown se menciona en L973 sin gráfico hallado); sin matriz de partes interesadas-impacto ni accesibilidad WCAG (guía S6, C3, puntos 9 y 12); "-30 %" de validación junto a test (L508).
10. Sí atendidos desde el 19/11: Tabla 4, Tabla 33, ODS 13, Tabla 32, dato 8 000 rotulado, concurrencia, estado HU-07/13.
11. Portada lista a "Claudio (Claude...)" bajo INTEGRANTES (verificar con el usuario/docente).

## 4. Mejoras al propio reporte

- Quitar la observación falsa de ecuaciones; corregir -0,16 %, Tabla 8, páginas.
- Declarar fecha, versión evaluada, método, escala de niveles y limitaciones (el anterior lo hacía; el nuevo no tiene ni fecha ni equipo en el texto).
- Cita verificable (línea/página) por evidencia; distinguir "verificado" de "declarado".
- Añadir hallazgos de la sección 3 y tabla de mapeo a las 6 competencias; tabla de seguimiento frente al 19/11 (atendido/pendiente).
- Priorizar: separar correcciones documentales (hoy) de las que dependen de terceros (usuarios, Supabase).
- Justificar por qué Herramientas es "satisfactorio" con inconsistencia propia, y por qué Análisis sube a satisfactorio sin que cambie la evidencia primaria.

## 5. Plan priorizado

P1 documental: items 1, 2, 3, 4, 5, 6; Gantt/Tabla 23/estados; marcador p.72; cifras de pruebas con fecha; ocultar contraseñas en Fig. VIII.13 y Anexo B (sin afirmar corrección en Supabase).
P1 dependiente del equipo: acta de usuarios; video; F-01 en Supabase + migración 001.
P2: PE3 respondido explícitamente; limitación H-14; fuente o sensibilidad de P_idle/P_max; CO2e estimado; matriz stakeholders/accesibilidad.
P3: balance energético neto, priorización de causas, SPI/CPI.

## 6. Dudas para el usuario

1. ¿"6 competencias" = C1-C6 del curso o las 7 de la consigna ICACIT?
2. ¿El docente señaló correcciones concretas? ¿El .docx es la nueva ejecución o la que él objetó? ¿Quién la generó?
3. ¿Hay (o habrá) sesión con usuarios y acta? Nunca fabricarla.
4. ¿Se autoriza cambiar Supabase (password, RLS, migración) y quién es el dueño?
5. ¿Se puede reexportar el informe (venció el 25/11 23:59) y subir video nuevo?
