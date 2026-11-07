# Lista de revisión final del informe Green AI

**Para:** integrantes del equipo.  
**Fecha de preparación:** 29 de octubre de 2026.  
**Propósito:** comprobar el informe actualizado contra las listas de cotejo del docente e identificar contenido, pruebas y capturas pendientes.

Esta lista no certifica que el informe actualizado esté completo: todavía debe contrastarse con esa versión y sus evidencias. Aunque el software haya avanzado, el documento debe demostrar cada requisito. Marcar una casilla únicamente después de revisar el contenido y su respaldo.

Fuentes de requisitos:

- `S10.Evaluacion-formativa-Tablero-Github-Python.docx`.
- `TallerProy1-ListaCotejo-Unidad-3-202610.docx`.
- Informe original: `Consigna-Taller1-Actualizado-Icacit.docx (1).pdf`.

**Trello:** lo completan los compañeros responsables. Su evaluación detallada queda fuera de esta guía, pero deben coordinar su inclusión en la entrega grupal y el video cuando corresponda.

## Cómo usar esta lista

1. Trabajar sobre una única versión del informe y anotar su fecha.
2. Revisar los doce apartados en orden.
3. Marcar lo comprobado y registrar página, figura o enlace de evidencia.
4. Asignar responsable a cada pendiente.
5. Repetir el control final antes de entregar.

Una captura ya existente puede reutilizarse si es legible y demuestra el requisito. No hace falta generar capturas nuevas por cantidad: deben aportar evidencia concreta.

## 1. Portada, resumen y abstract

### Ubicación

Portada y páginas iniciales del informe.

### Comprobar

- [ ] Logo de la Universidad Continental, asignatura y NRC.
- [ ] Título del proyecto y nombres completos de los integrantes.
- [ ] Datos adicionales exigidos por la plantilla.
- [ ] Retirar textos de instrucciones como “Consigna de trabajo”, si no pertenecen al informe final.
- [ ] Resumen en español y abstract en inglés con el mismo contenido: problema, objetivo, método, resultado demostrado y limitaciones.

### Correcciones que deben mantenerse en todo el documento

- [ ] Retirar el ahorro del **18,4 %** y los resultados atribuidos a **XGBoost** que no tienen experimentos de respaldo. El usuario confirmó que esos archivos no existen.
- [ ] Si presentan el manifiesto de Random Forest, identificarlo como un experimento con **datos simulados**.
- [ ] Describir recomendaciones como responsabilidad de **Prediction**, con revisión humana y sin ejecución automática.
- [ ] Diferenciar funcionalidades implementadas, probadas y pendientes.

**Capturas:** no se necesitan capturas del software en este apartado.

## 2. Introducción, marco teórico y antecedentes

### Ubicación

Secciones Introducción, Marco teórico y Antecedentes, según la estructura del informe.

### Comprobar

- [ ] Desarrollar los **tres antecedentes iniciales** exigidos.
- [ ] Desarrollar los **tres antecedentes sobre integración con Machine Learning**.
- [ ] Explicar los conceptos necesarios para entender arquitectura, monitoreo, predicción y recomendaciones.
- [ ] En cada antecedente, explicar problema, método, datos, resultados y relación con Green AI.
- [ ] Respaldar cada antecedente con una referencia académica verificable.

Una lista de referencias al final no sustituye el análisis de antecedentes. Las referencias a Scrum, ISO o IEA tampoco sustituyen automáticamente los estudios académicos solicitados.

**Capturas:** no son necesarias para demostrar los antecedentes. Utilizar citas y análisis; incorporar figuras conceptuales solo si ayudan a explicar el marco teórico.

## 3. Metodología y cronograma

### Ubicación

Gestión del proyecto y Metodología de ingeniería.

### Comprobar

- [ ] Explicar cómo aplicaron Scrum y organizaron el trabajo por sprint.
- [ ] Describir cómo desarrollaron requisitos, diseño, implementación y pruebas.
- [ ] Identificar qué HU corresponden a PMV1 y PMV2.
- [ ] Presentar el cronograma actualizado y coherente con la fecha de entrega.
- [ ] Separar planificación futura de avance ejecutado.
- [ ] Sustentar porcentajes y métricas de avance con registros.

**Dónde colocar evidencia:** el Gantt debe aparecer junto a la explicación del cronograma, con leyenda y fecha de actualización.

No presentar fechas futuras o entregas previstas como trabajo ya ejecutado. Los responsables de Trello deben completar las evidencias de Kanban y ceremonias requeridas para la entrega grupal.

## 4. Arquitectura implementada

### Ubicación

Diseño y Arquitectura del sistema.

### Comprobar

- [ ] Diagrama general actualizado, con recomendaciones dentro de Prediction.
- [ ] Responsabilidades de cada servicio.
- [ ] Tabla que relacione capas con archivos o clases reales.
- [ ] Recorrido de una solicitud por las capas, según la implementación del servicio.
- [ ] Dependencias revisadas: las carpetas por sí solas no prueban aislamiento.

Ejemplo de recorrido que debe explicarse con clases reales:

> Entrada HTTP → caso de uso → puerto → adaptador → fuente externa.

### Capturas y ubicación

| Evidencia | Dónde colocarla | Qué debe mostrar |
| --- | --- | --- |
| Estructura de carpetas | Después del diagrama | Organización real del código, legible. |
| Caso de uso y puerto | Después de explicar las capas | Cómo la aplicación depende de una abstracción. |
| Adaptador concreto | Junto al recorrido de la solicitud | Implementación de la comunicación externa. |
| Resultado de pruebas de reglas | En pruebas de arquitectura | Que las reglas pueden probarse sin HTTP o servicios externos. |

- [ ] Cada captura se vincula con una afirmación del texto.
- [ ] Los archivos mostrados pertenecen a la versión entregada.

No basta con tener carpetas vacías. Si algún servicio conserva acoplamientos, corregirlos o documentarlos y justificar su alcance. No afirmar “100 % hexagonal” ignorando esas brechas.

## 5. Pruebas organizadas por historia de usuario

### Ubicación

Sección **Pruebas, resultados y discusión**, separando:

- Pruebas del PMV1.
- Pruebas del PMV2.

Dentro de cada apartado, crear una subsección por cada HU comprometida. Usar los identificadores definitivos del backlog.

### Ficha que debe completarse por HU

| Campo | Contenido |
| --- | --- |
| HU y PMV | Identificador, título y mínimo viable. |
| Criterio de aceptación | Qué debe cumplir la funcionalidad. |
| Entorno y versión | Fecha, commit y configuración relevante. |
| Datos de entrada | Valores utilizados y procedencia: observados o simulados; si se desconoce, declararlo. |
| Procedimiento | Pasos realmente ejecutados. |
| Resultado esperado | Comportamiento definido antes de la prueba. |
| Resultado obtenido | Respuesta o comportamiento observado. |
| Evidencia | Número de figura y archivo o reporte relacionado. |
| Veredicto | Aprobada, fallida o pendiente, con explicación. |

- [ ] Todas las HU comprometidas en PMV1 y PMV2 tienen ficha.
- [ ] La ficha permite comprobar los criterios de aceptación, no solo la existencia de una pantalla.
- [ ] No se aprobaron funcionalidades pendientes solo mediante redacción.
- [ ] Los resultados corresponden a ejecuciones reales documentadas.

**Dónde colocar las capturas:** inmediatamente después de la ficha correspondiente, no todas juntas al final. Los reportes extensos pueden ir en anexos, con referencia desde la ficha.

Cada figura debe tener número, título, explicación y una referencia desde el texto. Evitar capturas de toda la pantalla si los datos quedan ilegibles.

## 6. Capturas funcionales que deben comprobarse

| Funcionalidad | Evidencia necesaria | Ubicación recomendada |
| --- | --- | --- |
| Monitoreo actual | Interfaz con recurso, métrica, valor y momento de consulta identificables. | Prueba de la HU de monitoreo, PMV1. |
| Históricos | Consulta con rango temporal y recurso; resultado mostrado en tabla o gráfica. | Prueba de la HU de históricos. |
| Prometheus y Grafana | Targets disponibles y panel con métricas, rango temporal y fuente reconocible. | Pruebas de observabilidad, vinculadas a la HU correspondiente. |
| Predicción | Entrada o dataset identificado, respuesta y visualización de la estimación en la aplicación. | Prueba de la HU de predicción, PMV2. |
| Recomendación | Entrada, respuesta, estado, comprobaciones y propuesta mostrada al usuario. | Prueba de la HU de recomendaciones. |
| Restricciones | Caso que incumple un límite y resultado bloqueado; caso con datos insuficientes, si corresponde al criterio. | Prueba de la HU de restricciones. |
| Autenticación | Acceso anónimo rechazado y operación permitida con sesión válida. | Pruebas de seguridad. |
| Aprobación humana | Acción explícita de aprobar/rechazar y efecto o registro correspondiente, si esa HU está comprometida. | Prueba individual de HU-07, si ese es su identificador definitivo. |

### Evitar conclusiones incorrectas

- [ ] Swagger no se presenta como prueba funcional solo por mostrar endpoints plegados: debe verse una operación ejecutada cuando se use como evidencia de ejecución.
- [ ] `executionAllowed=false` no se usa como única evidencia de aprobación humana. Solo demuestra que no se ejecutan acciones automáticamente.
- [ ] HTTP 200 no se usa como prueba automática de que se cumplen todos los criterios de una HU.
- [ ] Un target UP no se presenta como disponibilidad del 100 % durante un periodo sin medición temporal.
- [ ] Contraseñas, tokens y claves están ocultos en las evidencias.

Las capturas de login, predicción y recomendación mencionadas por Gemini pueden reutilizarse si son legibles y muestran el criterio que se está evaluando. Su presencia debe comprobarse en el informe actualizado.

## 7. Supabase y rutinas almacenadas

### Ubicación

- **Diseño de base de datos:** diagrama y explicación de tablas.
- **Pruebas de base de datos:** definición, activación y resultado de las rutinas.

### Capturas necesarias

| Captura | Qué debe demostrar |
| --- | --- |
| Definición de las funciones instaladas | Nombre, firma y lógica relevante. |
| Definición del trigger | Tabla, evento y función que ejecuta. |
| Registro desde la aplicación | Evento que activa el flujo para una cuenta de prueba. |
| Resultado en perfiles y roles | Efecto sobre el mismo usuario, sin inserción manual. |
| Configuración del hook | Función seleccionada para incorporar el rol al token. |
| Operación autorizada | Uso del rol en el acceso a la aplicación, sin exponer el token. |

- [ ] Relacionar las capturas mediante la misma cuenta de prueba, identificada de forma anonimizada.
- [ ] Mostrar las rutinas instaladas, no solo el archivo SQL local.
- [ ] Demostrar ejecución y efecto; el esquema de tablas no basta.
- [ ] Resolver la interpretación docente de “procedimientos almacenados”: documentar correctamente las funciones y triggers existentes, sin cambiarles el nombre para aparentar cumplimiento.
- [ ] No atribuir al trigger una fila antigua que pudo crearse mediante una inserción manual o regularización.

La guía detallada para Gemini está en [Contexto del criterio 5 de Supabase](Contexto_Gemini_Criterio5_Supabase.md). Incluye funciones existentes, consultas de inspección y condiciones para cerrar el criterio.

## 8. Experimento de Machine Learning

### Ubicación

Resultados del PMV2 y Evaluación predictiva.

### Comprobar

- [ ] Modelo y horizonte.
- [ ] Dataset, procedencia, cantidad de muestras y periodo.
- [ ] Separación de entrenamiento, validación y prueba.
- [ ] Modelo de referencia utilizado para comparar.
- [ ] Métricas y unidades.
- [ ] Versión del código y archivo de resultados.
- [ ] Criterio de aceptación y comparación del resultado contra él.

### Figuras y tablas que deben aparecer aquí

1. Tabla comparativa de resultados del experimento identificado.
2. Gráfica de valores reales del dataset frente a predicciones sobre el conjunto de prueba. Si el dataset es simulado, aclarar que esos valores de referencia también proceden de la simulación.
3. Resultados específicos de picos, si los evalúan.
4. Referencia al manifiesto o reporte reproducible.

Si usan el manifiesto revisado anteriormente, indicar **Random Forest, horizonte de 15 minutos y datos simulados**. No mezclarlo con cifras de otra corrida. Si ejecutaron un experimento nuevo, identificarlo y presentar sus propios resultados.

- [ ] Separar latencia de inferencia de latencia HTTP completa.
- [ ] No usar un endpoint de salud como evidencia de precisión.
- [ ] Expresar MAE/RMSE en puntos porcentuales cuando CPU esté en escala de 0 a 100; distinguirlos de métricas porcentuales como sMAPE.
- [ ] No atribuir validación con datos observados a una prueba simulada.

## 9. Pruebas de carga y métricas de calidad

### Ubicación

Pruebas de calidad y Rendimiento.

### Comprobar

- [ ] Demostración de **500 a 1000 transacciones**, según la rúbrica.
- [ ] Operación evaluada y entorno.
- [ ] Número de solicitudes, éxitos y errores.
- [ ] Duración y concurrencia.
- [ ] Latencias relevantes.
- [ ] Resultado frente al criterio de aceptación.

**Capturas necesarias:** configuración de la prueba y reporte final. Colocarlas junto a la tabla de resultados y vincular el reporte completo si va en anexos.

Las filas de un dataset, las muestras de Prometheus y el número de pruebas unitarias no equivalen automáticamente a transacciones de una prueba de carga.

- [ ] Incluir reportes de pruebas de software.
- [ ] Incluir las métricas de arquitectura, calidad y agilidad exigidas; coordinar las de agilidad con los responsables del tablero.
- [ ] Toda cifra de cobertura tiene su reporte. El número de pruebas aprobadas no permite deducir cobertura.
- [ ] Los resultados muestran fecha y versión, y no presentan ejecuciones anteriores como si fueran la última entrega.

## 10. Discusión con tres estudios

### Ubicación

Después de presentar los resultados, en un apartado explícito de **Discusión**.

- [ ] Comparar Green AI con **tres estudios recientes y pertinentes** de los antecedentes.
- [ ] Verificar título, autores, año y DOI o enlace de cada estudio.
- [ ] Comprobar que las fuentes realmente apoyan las afirmaciones redactadas.

| Aspecto | Qué explicar |
| --- | --- |
| Problema y contexto | En qué se parecen o diferencian. |
| Datos | Procedencia, tamaño y condiciones. |
| Método | Modelo, estrategia y restricciones. |
| Resultados | Qué métricas pueden compararse y cuáles no. |
| Limitaciones | Qué no demuestra el experimento de Green AI. |

No afirmar que Green AI supera otro trabajo si los datos, horizontes y métricas no permiten esa comparación. Una mención autor–año no sustituye una referencia verificable ni una discusión argumentada.

**Figuras:** suelen ser más útiles una tabla comparativa y argumentos con citas que capturas del software.

## 11. Conclusiones y referencias

### Conclusiones

- [ ] Responder a cada objetivo de PMV1 y PMV2.
- [ ] Seguir la estructura: qué se logró → con qué evidencia → bajo qué condiciones → qué limitación permanece.
- [ ] No introducir resultados que no aparezcan antes en las pruebas.
- [ ] Evitar “garantiza el SLA”, “ahorro real” o “precisión validada en producción” si no se demostraron.
- [ ] Mantener coherencia con el resumen, las tablas de resultados y la discusión.

### Referencias

- [ ] Mantener el formato ISO 690 numérico solicitado.
- [ ] Revisar que cada número de cita corresponda a la fuente correcta.
- [ ] Incluir todas las fuentes citadas.
- [ ] Comprobar especialmente las citas que cambiaron al reescribir antecedentes y discusión.

## 12. Video, enlaces y anexos

### Ubicación

Anexos y Evidencias de entrega, con referencias desde el cuerpo del informe.

- [ ] Enlace al informe final.
- [ ] Enlace al video.
- [ ] Enlaces a repositorios y ramas de la entrega.
- [ ] Enlaces a reportes y evidencias complementarias.
- [ ] Acceso comprobado desde una sesión sin privilegios del equipo.
- [ ] Los enlaces apuntan a la versión correcta y se indica fecha de verificación.

### Contenido del video solicitado

- [ ] Demostración del PMV1.
- [ ] Demostración del PMV2.
- [ ] Pruebas con datos masivos y métricas.
- [ ] **Dos casos de uso predictivos** desde la aplicación.
- [ ] Demostración de arquitectura y rutinas de base de datos.
- [ ] Segmento Trello coordinado con sus responsables.
- [ ] Duración de **20–30 minutos**, según la guía.
- [ ] Participación de todos los integrantes con cámara y nombre completo.

Dos nombres de endpoint para la misma operación no demuestran dos casos de uso distintos. Una captura tampoco sustituye el video cuando la rúbrica exige una demostración grabada.

Comprobar adicionalmente el plazo y la constancia de entrega: ese requisito no se acredita con el contenido del informe.

## Control final antes de enviar

- [ ] Cada HU comprometida tiene criterio, prueba, resultado y evidencia.
- [ ] Cada cifra importante tiene una fuente experimental identificable.
- [ ] Las capturas están junto a lo que demuestran y son legibles.
- [ ] Resumen, resultados, discusión y conclusiones describen el mismo estado del proyecto.
- [ ] Se distinguen datos simulados, observados y estimaciones.
- [ ] El video demuestra lo que pide la rúbrica.
- [ ] Los enlaces permiten acceder a la versión correcta.
- [ ] Se revisaron ortografía, numeración de figuras/tablas, referencias cruzadas y presentación.

Si alguna respuesta es **no**, ese es un pendiente concreto del documento, aunque la funcionalidad ya esté implementada. La calificación final corresponde al docente.

## Registro de pendientes del equipo

Completar una fila por hallazgo. No sustituye las fichas de prueba: sirve para organizar la revisión final.

| Apartado o criterio | Qué falta o debe corregirse | Evidencia que se agregará | Página o sección de destino | Responsable | Estado |
| --- | --- | --- | --- | --- | --- |
| Por completar | Por completar | Por completar | Por completar | Por asignar | Pendiente |

