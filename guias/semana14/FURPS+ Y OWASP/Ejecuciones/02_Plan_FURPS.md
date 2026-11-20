# 02_Plan_FURPS.md — Plan Integral de Mejora de Calidad

**Proyecto:** Green AI — Optimización Energética y Capacidad en Data Centers con Machine Learning  
**Institución:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol:** Arquitecto de Software Senior  
**Documento de entrada:** `01_Auditoria_FURPS.md`  
**Línea base:** 85.00 % (valor consignado en la auditoría)  
**Fecha de planificación:** 19/11/2026  
**Estado del sistema:** Sistema funcional; las mejoras se ejecutarán de forma incremental y controlada.

---

## 1. Objetivo y criterios de planificación

Este plan organiza las acciones necesarias para atender las brechas registradas en la auditoría FURPS+, sin reemplazar componentes que ya funcionan ni alterar contratos, flujos de negocio o integraciones existentes.

La auditoría identifica como principales brechas: persistencia de decisiones humanas (HU-07), validación de seguridad de Supabase/RLS (HU-15 y M-R05), validación del dashboard con sesión real en `/dev/`, trazabilidad/visualización de MLflow, reporte PDF, accesibilidad, guía rápida, simplificación del flujo de energía, cold start de Render Free y acoplamiento del Simulator.

### 1.1 Principios obligatorios

1. **Compatibilidad hacia atrás:** conservar rutas, métodos HTTP, esquemas de respuesta, nombres de variables y comportamiento actual. Los cambios de contrato, si fueran imprescindibles, se introducirán mediante versiones o campos opcionales.
2. **Cambios incrementales:** una mejora por unidad de cambio pequeña, revisable y reversible.
3. **Riesgo mínimo:** priorizar validaciones en local o staging; no experimentar directamente sobre datos o servicios de producción.
4. **Validación obligatoria:** cada cambio debe tener criterios de aceptación, pruebas automatizadas y smoke tests pertinentes.
5. **Rollback verificable:** mantener una versión estable identificable y documentar cómo volver a ella.
6. **No confundir simulación con medición:** la potencia y energía modeladas deben continuar identificadas como estimaciones mientras no existan sensores físicos.
7. **Restricciones de infraestructura:** las propuestas deben ser compatibles con el hosting gratuito documentado. No se presupone presupuesto para servicios pagados ni se propone mantener procesos de keep-alive permanentes que consuman la cuota gratuita.

### 1.2 Reglas de entrada a producción

Ninguna mejora se despliega si no cumple todas estas condiciones:

- Rama de trabajo separada y cambios revisados mediante Pull Request.
- Pruebas de la unidad afectada y pruebas de regresión del sistema aprobadas.
- Contratos API y migraciones revisados por compatibilidad.
- Copia de seguridad cuando se modifiquen datos, políticas o esquemas.
- Plan de rollback ensayado o técnicamente viable.
- Despliegue gradual y verificación posterior con health checks y smoke tests.
- Registro de versión, responsable, fecha y resultado de validación.

---

## 2. Roadmap de mejora

El roadmap se divide en tres olas. Las duraciones son estimaciones de planificación y deben ajustarse a la disponibilidad del equipo; no constituyen evidencia de implementación.

| Ola | Enfoque | Mejoras principales | Condición para avanzar |
|---|---|---|---|
| **Ola 0 — Protección y diagnóstico** | Reducir riesgo antes de modificar | Verificar RLS y esquema remoto; probar autenticación real; establecer baseline de regresión y respaldo | Acceso controlado a staging, inventario de políticas y pruebas reproducibles |
| **Ola 1 — Brechas funcionales prioritarias** | Completar flujos importantes sin romper los actuales | Persistencia de aprobación humana; validación dashboard `/dev/`; MLflow; reporte PDF | Pruebas de contrato, permisos y regresión aprobadas |
| **Ola 2 — Usabilidad y mantenibilidad** | Mejorar experiencia y estructura interna | Guía rápida; accesibilidad; flujo de energía; desacoplamiento Simulator | Evidencia de usabilidad y pruebas del módulo afectado |
| **Ola 3 — Operación y rendimiento** | Mitigar limitaciones operativas conocidas | Estrategia de pre calentamiento controlado; monitoreo de cold start y documentación de límites | Mediciones comparables y ausencia de impacto en cuotas o disponibilidad |

**Orden de ejecución:** Ola 0 debe preceder a cualquier cambio de persistencia o autenticación. Las mejoras de cada ola pueden dividirse en entregas pequeñas, pero no deben adelantarse cambios dependientes de una validación de seguridad pendiente.

---

## 3. Mejoras priorizadas

### FURPS-F — Funcionalidad

#### F-01. Verificar y endurecer Supabase Auth/RLS (HU-15)

- **Objetivo:** confirmar las políticas RLS reales del proyecto remoto, retirar permisos excesivamente amplios si se confirman y verificar que la autenticación no dependa de una columna de contraseña propia.
- **Justificación:** la auditoría registra políticas descritas como «Permitir todo», ausencia de pruebas automatizadas con usuario real y una columna `password` pendiente de verificación en la base remota. También relaciona esta brecha con M-R05.
- **Prioridad:** **Crítica**.
- **Riesgo:** Alto. Una política mal modificada puede bloquear usuarios legítimos o exponer datos; una política permisiva puede permitir acceso no autorizado.
- **Dependencias:** acceso administrativo autorizado a Supabase; inventario de tablas, roles y políticas; entorno de staging; cuentas de prueba con roles representativos; respaldo del esquema y políticas actuales.
- **Estrategia de implementación:** primero auditar y exportar las políticas actuales, sin modificarlas. Reproducirlas en staging, definir reglas mínimas por tabla y operación, y probar aislamiento entre usuarios/roles. Aplicar cambios en producción solo tras aprobación y ventana controlada. No eliminar columnas ni alterar el mecanismo de Auth hasta confirmar referencias y dependencias.
- **Estrategia de validación:** pruebas positivas y negativas de SELECT/INSERT/UPDATE/DELETE; pruebas con sesión válida, sesión expirada y usuario sin permisos; verificación de aislamiento entre cuentas; pruebas de Gateway/RBAC; smoke test de login y navegación; confirmar que no se exponen secretos ni contraseñas.
- **Estrategia de rollback:** conservar exportación versionada de las políticas anteriores y respaldo de esquema. Revertir únicamente las políticas afectadas a la versión aprobada anterior si se detecta bloqueo o regresión. No restaurar políticas permisivas sin evaluación de seguridad; si el rollback reabre exposición, deshabilitar temporalmente la operación afectada y corregir en staging.

#### F-02. Persistir la aprobación/rechazo de recomendaciones (HU-07)

- **Objetivo:** incorporar trazabilidad persistente de la decisión humana sobre cada recomendación, manteniendo el bloqueo de ejecución automática.
- **Justificación:** la auditoría indica que el sistema devuelve `executionAllowed=false`, pero no existe flujo persistente de aprobar/rechazar.
- **Prioridad:** **Alta**.
- **Riesgo:** Alto. Una implementación incorrecta podría habilitar acciones no autorizadas, duplicar decisiones o asociar una decisión al usuario equivocado.
- **Dependencias:** F-01 validada; modelo de identidad Supabase; definición de roles autorizados; contrato actual de recomendaciones; diseño de auditoría y retención.
- **Estrategia de implementación:** añadir una entidad/tabla de decisiones separada, con identificador de recomendación, usuario, decisión, fecha y referencia/versionado de la recomendación. Añadir endpoints o acciones nuevas sin cambiar el contrato actual de `POST /v1/recommendations`. La aprobación será un registro de decisión, no una orden de ejecución. Mantener `executionAllowed=false` hasta que exista un proceso de ejecución explícitamente diseñado y autorizado.
- **Estrategia de validación:** pruebas de autorización por rol; persistencia y lectura de decisiones; rechazo de usuarios no autorizados; idempotencia o control de duplicados; integridad de referencia a la recomendación; pruebas de regresión de generación de recomendaciones; confirmar que ninguna decisión dispara ejecución automática.
- **Estrategia de rollback:** deshabilitar la nueva interfaz/ruta mediante feature flag o configuración; conservar la tabla y los registros ya creados; volver a mostrar el flujo anterior de recomendaciones de solo lectura. No borrar decisiones persistidas durante el rollback.

#### F-03. Validar dashboard con sesión real de Supabase en `/dev/` (HU-11)

- **Objetivo:** completar la verificación del dashboard desplegado con autenticación real y servicios integrados.
- **Justificación:** la auditoría indica que el dashboard fue probado en arnés local, pero falta validar sesión real de Supabase en `/dev/`.
- **Prioridad:** **Alta**.
- **Riesgo:** Medio. Cambios de configuración pueden provocar errores de login, CORS o acceso a APIs.
- **Dependencias:** F-01; cuenta de prueba; variables de entorno y redirect URLs revisadas; disponibilidad de Gateway y servicios upstream.
- **Estrategia de implementación:** realizar primero pruebas de diagnóstico sin cambios de código. Si se identifica un defecto, modificar solo la configuración o módulo responsable, conservando las URLs y rutas actuales. Validar primero en `/dev/`.
- **Estrategia de validación:** login/logout; renovación y expiración de sesión; carga de las cinco pestañas; consultas de métricas e históricos; predicción; permisos ADMIN/OPERATOR/VIEWER; errores 401/403; CORS y redirecciones. Registrar evidencias sin incluir tokens ni datos personales.
- **Estrategia de rollback:** restaurar la configuración previa de `/dev/` y retirar el cambio puntual. Mantener intacta la versión estable del frontend y Gateway.

#### F-04. Completar visualización y acceso a experimentos MLflow (HU-05)

- **Objetivo:** permitir consultar de forma reproducible los experimentos que actualmente se registran localmente.
- **Justificación:** existe registro local en `software/prediction/mlruns`, pero la auditoría no encontró UI desplegada ni evidencia de visualización.
- **Prioridad:** **Media**.
- **Riesgo:** Medio. La persistencia de artefactos y el consumo de memoria/almacenamiento pueden afectar el entorno gratuito.
- **Dependencias:** pipeline actual de entrenamiento; ubicación de artefactos; política de almacenamiento; recursos disponibles.
- **Estrategia de implementación:** primero documentar cómo consultar los runs localmente y adjuntar evidencia. Evaluar una UI temporal/local antes de desplegar un servidor persistente. No convertir MLflow en dependencia obligatoria del servicio de inferencia ni bloquear predicciones si MLflow no está disponible.
- **Estrategia de validación:** ejecutar pipeline controlado; comprobar parámetros, métricas y artefactos; comparar resultados con el manifiesto existente; verificar que la inferencia funciona con MLflow detenido.
- **Estrategia de rollback:** desactivar la UI o integración nueva y volver al registro local actual. Preservar `mlruns` y manifiestos; no eliminar artefactos durante el rollback.

#### F-05. Añadir exportación PDF de reportes históricos (HU-13)

- **Objetivo:** complementar las salidas JSON y CSV con un reporte PDF descargable.
- **Justificación:** la auditoría confirma JSON y CSV, pero señala que el PDF formal está pendiente.
- **Prioridad:** **Media**.
- **Riesgo:** Medio. La generación de documentos puede aumentar uso de memoria y tiempo de respuesta.
- **Dependencias:** endpoint actual `historical-summary`; definición del contenido del reporte; límites de rango temporal y tamaño; librería compatible con el entorno.
- **Estrategia de implementación:** añadir una ruta o formato de exportación nuevo, sin modificar ni retirar JSON/CSV. Generar el PDF a partir del mismo modelo de datos validado y aplicar límites de tamaño/tiempo. Si el reporte es grande, evaluar generación bajo demanda y no bloquear consultas existentes.
- **Estrategia de validación:** comparar totales y rangos del PDF con JSON/CSV para el mismo filtro; probar fechas inválidas, dataset vacío y volumen máximo admitido; validar descarga, nombre de archivo y caracteres; comprobar memoria y latencia.
- **Estrategia de rollback:** ocultar/deshabilitar únicamente la opción PDF y conservar las rutas JSON/CSV. Retirar la dependencia nueva solo después de confirmar que ningún otro módulo la utiliza.

#### F-06. Mantener explícita la naturaleza estimada de energía y CO₂e (HU-09)

- **Objetivo:** asegurar que toda visualización y exportación identifique la potencia como modelada/sintética cuando no provenga de sensores físicos.
- **Justificación:** la auditoría registra cálculo trapezoidal de kWh basado en potencia lineal modelada y factor de emisión manual; no hay evidencia de medición física.
- **Prioridad:** **Alta** para claridad de resultados; no se plantea como incorporación de sensores.
- **Riesgo:** Bajo. El principal riesgo es presentar una estimación como medición real.
- **Dependencias:** módulo `software/frontend/energy.js`; etiquetas y documentación de la interfaz; esquema de reportes.
- **Estrategia de implementación:** conservar la fórmula y los resultados actuales; mejorar etiquetas, metadatos y textos para indicar `estimated`/modelado y registrar la fuente del factor CO₂e. No modificar la fórmula sin validación experimental.
- **Estrategia de validación:** casos deterministas conocidos; consistencia entre UI y CSV/PDF; comprobar que ninguna pantalla etiqueta la potencia modelada como lectura de hardware.
- **Estrategia de rollback:** revertir únicamente textos o metadatos nuevos si generan incompatibilidad; no retirar el cálculo actual ni alterar datos históricos.

### FURPS-U — Usabilidad

#### U-01. Publicar una guía rápida de usuario

- **Objetivo:** facilitar el primer uso de la consola y explicar las funciones, límites y significado de los indicadores.
- **Justificación:** la auditoría inicial no encontró una guía rápida en `docs/` ni integrada en el frontend.
- **Prioridad:** **Media**.
- **Riesgo:** Bajo.
- **Dependencias:** flujos actuales del dashboard; revisión del responsable funcional; capturas actualizadas.
- **Estrategia de implementación:** crear una guía breve versionada y enlazarla desde un punto visible de ayuda, sin modificar la navegación principal.
- **Estrategia de validación:** revisión por un usuario que no haya desarrollado el sistema; comprobar que puede iniciar sesión, navegar, consultar métricas y reconocer los límites de los datos.
- **Estrategia de rollback:** retirar o corregir el enlace sin modificar las vistas existentes; conservar la guía versionada.

#### U-02. Completar validación de accesibilidad (M-U06)

- **Objetivo:** verificar accesibilidad con herramientas automatizadas y ofrecer alternativa textual accesible para el gráfico Chart.js.
- **Justificación:** la auditoría identifica semántica y ARIA existentes, pero no una auditoría WCAG 2.1 AA formal ni una tabla alternativa directa al gráfico.
- **Prioridad:** **Media**.
- **Riesgo:** Medio. Cambios de DOM/ARIA pueden afectar selectores, estilos o interacción.
- **Dependencias:** frontend actual; herramienta de auditoría (Lighthouse/axe-core); criterios WCAG 2.1 AA acordados.
- **Estrategia de implementación:** ejecutar primero el escaneo sin modificar la interfaz. Corregir hallazgos individualmente. Añadir una tabla textual asociada al conjunto de datos del gráfico sin retirar el canvas ni cambiar su fuente de datos.
- **Estrategia de validación:** escaneo automatizado antes/después; navegación por teclado; lector de pantalla; contraste; zoom; verificar equivalencia entre gráfico y tabla.
- **Estrategia de rollback:** revertir el componente accesible puntual si introduce regresión visual o funcional, manteniendo el gráfico original. Registrar la brecha pendiente para una corrección posterior.

#### U-03. Reducir a tres pasos el flujo de energía (M-U08)

- **Objetivo:** simplificar la secuencia de cálculo de energía sin eliminar opciones ni cambiar los resultados.
- **Justificación:** la auditoría describe cuatro acciones para carga de archivo, factor/fuente y cálculo.
- **Prioridad:** **Baja**.
- **Riesgo:** Medio. La simplificación puede ocultar parámetros o inducir entradas incorrectas.
- **Dependencias:** flujo actual de `software/frontend/energy.js`; reglas de validación de archivo y factor de emisión.
- **Estrategia de implementación:** probar primero una propuesta de interfaz; conservar campos avanzados y valores explícitos; no asignar factores de emisión implícitos ni cambiar defaults científicos sin aprobación.
- **Estrategia de validación:** pruebas de cálculo con datasets conocidos; entradas inválidas; comparación numérica antes/después; prueba de usabilidad con operador.
- **Estrategia de rollback:** restaurar el formulario anterior mediante reversión del componente UI; mantener intacta la lógica de cálculo.

### FURPS-R — Confiabilidad

#### R-01. Ejecutar pruebas de carga controladas contra staging (M-R05)

- **Objetivo:** medir el comportamiento de Data Processing/PostgREST ante carga y verificar que el aislamiento de datos se mantiene.
- **Justificación:** la auditoría señala que la resistencia ante carga remota y RLS no está suficientemente verificada.
- **Prioridad:** **Alta**.
- **Riesgo:** Alto si se ejecuta contra producción; Medio en staging con límites controlados.
- **Dependencias:** F-01; entorno de staging; dataset sintético; límites de tasa y volumen; métricas de observabilidad.
- **Estrategia de implementación:** no realizar pruebas de estrés sobre producción. Definir carga gradual con umbrales de parada, comenzando por una carga baja y aumentando solo si no aparecen errores o degradación. No usar datos personales.
- **Estrategia de validación:** latencia p50/p95/p99, tasa de errores, timeouts, uso de memoria, conexiones y consistencia de paginación; pruebas de acceso cruzado entre usuarios; confirmar recuperación tras detener la carga.
- **Estrategia de rollback:** detener inmediatamente el generador de carga; revocar credenciales de prueba; limpiar solo los datos sintéticos identificados; restaurar el entorno de staging si fuera necesario. No tocar datos de producción.

### FURPS-P — Rendimiento

#### P-01. Mitigar el cold start de Render Free con operación controlada

- **Objetivo:** reducir el impacto operativo del arranque en frío en sesiones de demostración y pruebas.
- **Justificación:** la auditoría registra latencias locales bajas, pero un cold start aproximado de 60 segundos en Render Free tras inactividad, superior al umbral de 7 segundos.
- **Prioridad:** **Media**.
- **Riesgo:** Medio. Un keep-alive permanente puede consumir cuota gratuita compartida y ocultar la limitación real del hosting.
- **Dependencias:** disponibilidad de Render Free; health endpoints; calendario de demostraciones; cuota mensual restante.
- **Estrategia de implementación:** priorizar una rutina manual o programada únicamente antes de una ventana de demostración, si la política y cuota del servicio lo permiten. No introducir un ping continuo ni afirmar que elimina el cold start. Mantener documentado el comportamiento real del plan gratuito.
- **Estrategia de validación:** medir tiempo de primera petición tras inactividad y peticiones posteriores; comparar con baseline; verificar cuota y disponibilidad; confirmar que la operación normal no depende del precalentamiento.
- **Estrategia de rollback:** retirar la tarea de precalentamiento o configuración añadida; mantener health checks existentes y aceptar el cold start documentado cuando no haya ventana de demostración.

### FURPS-S — Soportabilidad

#### S-01. Desacoplar adaptadores del caso de uso del Simulator (M-S01)

- **Objetivo:** corregir la dependencia directa de adaptadores desde `application/runner.py`, manteniendo el comportamiento del simulador.
- **Justificación:** la auditoría identifica imports directos de adaptadores en `software/simulator/src/green_ai_simulator/application/runner.py:L5-L10`, contrarios a la inversión de dependencias aplicada en otros servicios.
- **Prioridad:** **Media**.
- **Riesgo:** Medio/Alto. El Simulator alimenta la telemetría; una refactorización incorrecta puede detener la generación de métricas.
- **Dependencias:** pruebas actuales del Simulator; identificación de puertos, adaptadores y puntos de composición; contrato `/metrics`; configuración Docker Compose.
- **Estrategia de implementación:** crear la abstracción mínima necesaria y mover el ensamblaje de dependencias al punto de composición. No reescribir el servicio ni cambiar formato, nombres o frecuencia de métricas. Mantener el comportamiento determinista.
- **Estrategia de validación:** pruebas unitarias del caso de uso; pruebas de contrato del formato Prometheus; comparación de salida determinista antes/después; smoke test de Prometheus y Monitoring; ejecución del Compose completo.
- **Estrategia de rollback:** revertir el commit de refactorización si cambia la salida o falla el arranque; conservar la versión anterior del paquete y la configuración de Compose.

---

## 4. Orden recomendado de ejecución

| Orden | ID | Mejora | Prioridad | Motivo del orden |
|---:|---|---|---|---|
| 1 | F-01 | Verificar y endurecer Supabase Auth/RLS | **Crítica** | Reduce el riesgo de exposición y habilita de forma segura los cambios dependientes de identidad |
| 2 | R-01 | Pruebas de carga controladas en staging | **Alta** | Aporta evidencia de confiabilidad sin afectar producción |
| 3 | F-03 | Validar dashboard con sesión real en `/dev/` | **Alta** | Confirma la integración real de autenticación y servicios |
| 4 | F-02 | Persistir aprobación/rechazo humano | **Alta** | Completa trazabilidad después de validar identidad y permisos |
| 5 | F-06 | Etiquetado explícito de energía estimada | **Alta** | Evita interpretaciones incorrectas de resultados |
| 6 | F-04 | Visualización/consulta de MLflow | **Media** | Completa trazabilidad experimental sin convertir MLflow en dependencia operativa |
| 7 | F-05 | Exportación PDF | **Media** | Añade formato nuevo conservando JSON y CSV |
| 8 | U-02 | Accesibilidad WCAG y alternativa textual | **Media** | Mejora acceso sin reemplazar visualizaciones existentes |
| 9 | U-01 | Guía rápida de usuario | **Media** | Mejora adopción con riesgo técnico mínimo |
| 10 | S-01 | Desacoplamiento del Simulator | **Media** | Refactorización aislada después de establecer regresiones |
| 11 | P-01 | Precalentamiento controlado | **Media** | Mitiga el impacto en demostraciones sin consumir cuota permanentemente |
| 12 | U-03 | Simplificación del flujo de energía | **Baja** | Mejora incremental de experiencia, no bloquea operación actual |

El orden es deliberado: primero se protege la identidad y los datos; después se validan integraciones y confiabilidad; luego se completan funcionalidades; finalmente se abordan mejoras de experiencia, estructura y operación. Las mejoras de baja prioridad no deben retrasar correcciones de seguridad.

---

## 5. Riesgos de ejecución y controles

| Riesgo | Impacto potencial | Control preventivo | Respuesta / rollback |
|---|---|---|---|
| Modificar RLS sin inventario completo | Bloqueo de usuarios o exposición de datos | Exportar políticas, staging y pruebas por rol | Restaurar política aprobada anterior; suspender operación afectada si el rollback reduce seguridad |
| Migración de esquema para aprobaciones | Pérdida/inconsistencia de datos | Migración aditiva, backup y tabla nueva | Revertir aplicación; conservar registros; migración inversa solo si es segura |
| Cambiar contratos de API existentes | Ruptura del frontend o integraciones | Añadir endpoints/campos opcionales; pruebas de contrato | Revertir endpoint nuevo; mantener rutas previas |
| Generar PDF dentro de solicitudes pesadas | Timeouts o consumo de RAM | Límites de rango/tamaño y pruebas de carga | Deshabilitar PDF; mantener JSON/CSV |
| Desplegar MLflow persistente en hosting gratuito | Agotamiento de recursos/cuota | Preferir consulta local o ejecución temporal | Apagar UI/servicio adicional; preservar runs locales |
| Cambiar DOM/ARIA para accesibilidad | Regresiones visuales o de interacción | Cambios pequeños y pruebas de teclado/lector | Revertir componente puntual |
| Refactorizar Simulator | Pérdida de métricas o inestabilidad de Prometheus | Pruebas deterministas y de contrato | Volver al commit estable |
| Keep-alive permanente | Consumo de horas gratuitas y falsa expectativa de disponibilidad | Precalentamiento limitado a ventanas controladas | Retirar tarea; documentar cold start |
| Interpretar energía estimada como medición real | Conclusiones experimentales incorrectas | Etiquetas y metadatos de procedencia | Revertir presentación confusa y corregir reportes |

### 5.1 Riesgos transversales

- **Cambios simultáneos:** no agrupar varias mejoras de alto riesgo en un único despliegue.
- **Credenciales:** nunca registrar JWT, claves Supabase, contraseñas o secretos en evidencias, logs o commits.
- **Datos:** las pruebas deben utilizar cuentas y datasets sintéticos; cualquier prueba sobre datos reales requiere autorización expresa.
- **Dependencias:** revisar tamaño, licencia, mantenimiento y compatibilidad antes de incorporar librerías nuevas.
- **Cuota gratuita:** medir consumo y apagar servicios temporales tras las pruebas.
- **Evidencia:** conservar resultados de CI, smoke tests, pruebas de contrato, mediciones y capturas sin datos sensibles.

---

## 6. Estrategia de preservación de funcionalidad

### 6.1 Línea base que no debe degradarse

Las mejoras deben preservar como mínimo los comportamientos ya documentados en la auditoría:

- Telemetría sintética determinista de 50 servidores y exposición de métricas Prometheus.
- Consulta de métricas y catálogo mediante Monitoring.
- Consulta histórica paginada mediante `/api/v1/historical-logs`.
- Predicción de CPU a 15 minutos mediante Random Forest.
- Recomendaciones con `executionAllowed=false`.
- Cálculo actual de energía mediante regla trapezoidal, manteniendo su condición de estimación.
- Cuatro reglas de alerta Prometheus.
- Roles `ADMIN`, `OPERATOR` y `VIEWER`.
- Respuestas de error `application/problem+json` y cabecera `X-Request-Id` donde ya estén implementadas.
- Health checks, readiness/liveness y timeouts existentes.
- Exportación histórica JSON/CSV.
- Dashboard actual, sus cinco pestañas y el modo claro/oscuro.
- Suites automatizadas y smoke test documentados en la auditoría.

### 6.2 Barreras de regresión por cambio

| Nivel | Validación mínima antes de integrar |
|---|---|
| Código de dominio o aplicación | Pruebas unitarias del módulo y análisis estático |
| API o persistencia | Pruebas de contrato, validación de esquema y pruebas de compatibilidad |
| Autenticación/RBAC/RLS | Pruebas positivas y negativas por rol, sesión y usuario |
| Frontend | Pruebas de interacción, navegación, accesibilidad y regresión visual cuando corresponda |
| Simulator/Prometheus | Pruebas deterministas, formato de métricas y smoke end-to-end |
| Infraestructura/despliegue | Health checks, readiness, smoke test y revisión de variables/configuración |

### 6.3 Procedimiento de despliegue seguro

1. Crear rama `feature/<id-mejora>` desde la rama estable acordada.
2. Registrar el comportamiento actual mediante pruebas y resultados baseline.
3. Implementar una sola mejora o un conjunto estrictamente acoplado.
4. Ejecutar pruebas específicas y suite de regresión.
5. Revisar el diff y los contratos; aprobar mediante Pull Request.
6. Desplegar primero en entorno de desarrollo/staging.
7. Ejecutar smoke tests y observar logs, métricas y health checks.
8. Promover a producción solo con aprobación del responsable.
9. Verificar la versión desplegada y conservar evidencia.
10. Si falla un criterio, detener promoción y ejecutar rollback.

### 6.4 Condiciones para considerar una mejora terminada

Una mejora solo se marca como implementada cuando:

- Existe evidencia reproducible del cambio.
- Las pruebas específicas y de regresión pasan.
- No se han eliminado ni alterado involuntariamente rutas o funcionalidades existentes.
- Se verificó el comportamiento de los roles y permisos aplicables.
- El procedimiento de rollback está documentado.
- La auditoría de implementación independiente puede comprobar el resultado.

---

## 7. Metas y tratamiento del puntaje

La auditoría de entrada consigna un nivel inicial de **85.00 %** y una meta global esperada de **98.00 %**, con 11 de 13 brechas previstas para subsanación y restricciones aceptadas para potencia modelada y hosting gratuito. Este plan conserva esas cifras como metas declaradas por la auditoría; no las presenta como resultados ya alcanzados.

La mejora del puntaje solo podrá confirmarse en `03_Auditoria_Implementacion_FURPS.md`, después de verificar cada acción contra el estado real del repositorio y sus pruebas. No se debe aumentar una calificación por el solo hecho de que una tarea figure en este plan.

**Nota de consistencia:** la auditoría contiene también una discrepancia entre el total ponderado declarado y el recálculo de sus categorías. Este plan no recalcula ni modifica la línea base; la discrepancia debe resolverse contra la matriz maestra antes de usar el puntaje como indicador comparativo oficial.

---

## 8. Dictamen del plan

El proyecto Green AI debe evolucionar mediante cambios aditivos, aislados y reversibles. La primera prioridad es verificar la seguridad efectiva de Supabase/RLS y establecer un entorno de validación seguro. A continuación, se deben completar los flujos funcionales que dependen de identidad y trazabilidad. Las mejoras de presentación, accesibilidad, mantenibilidad y operación se ejecutarán después de asegurar la línea base.

**No se recomienda una reescritura, migración masiva ni sustitución de microservicios.** La arquitectura y las funcionalidades que ya operan deben conservarse; toda mejora que no supere sus pruebas de aceptación debe revertirse sin afectar el servicio estable.
