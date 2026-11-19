# 03_Auditoria_Implementacion_FURPS.md — Auditoría Independiente de Implementación

**Proyecto:** Green AI — Optimización Energética y Capacidad en Data Centers con Machine Learning  
**Institución:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol:** Auditor Independiente  
**Fecha de auditoría:** 19/11/2026  
**Repositorio inspeccionado:** `woshtsu/green-ai-workspace-cld`  
**Rama inspeccionada:** `test`  
**Último commit observado en la consulta:** `27ef69f1def4f6846456f51c6a752c9be077cd10` — 10/11/2026  
**Entradas:** `01_Auditoria_FURPS.md` y `02_Plan_FURPS.md` generados en esta conversación.  
**Alcance de evidencia:** inspección de archivos versionados de la rama `test` y documentación/evidencias del repositorio. No se ejecutó el código, CI, suites automatizadas, smoke test ni pruebas contra Supabase/Render en esta auditoría.

---

## 1. Resumen ejecutivo

La auditoría verifica si las doce mejoras del plan `02_Plan_FURPS.md` están presentes en el estado observable del repositorio. Se aplicó un criterio conservador: la existencia de una propuesta, una tarea documentada o una ruta prevista no demuestra implementación; se exige evidencia concreta en código, configuración, documentación de ejecución o resultados de pruebas.

### 1.1 Resultado por estado

| Estado | Cantidad | Interpretación |
|---|---:|---|
| **Implementada** | **1** | Existe evidencia directa suficiente del entregable funcional/documental solicitado |
| **Parcialmente implementada** | **2** | Hay parte del resultado, pero falta cubrir todo el objetivo o demostrarlo |
| **No implementada** | **9** | No se encontró evidencia suficiente en la rama inspeccionada |
| **Total** | **12** | Mejoras evaluadas |

**Resultado global:** el plan no puede considerarse implementado. La guía rápida está presente; la validación del dashboard con sesión real y el etiquetado de energía cuentan con evidencia parcial; las demás mejoras no están demostradas en el snapshot inspeccionado.

### 1.2 Limitación temporal importante

El último commit que devolvió la consulta de historial de GitHub para el repositorio fue del **10/11/2026**. La fecha de esta auditoría es 19/11/2026. Por tanto, el resultado describe el estado versionado que fue posible inspeccionar, pero **no demuestra que no existan cambios locales, commits posteriores no visibles en la consulta o cambios en servicios externos**. Antes de cerrar formalmente el ciclo, el equipo debe proporcionar/confirmar el SHA vigente de `test` y repetir la inspección sobre ese commit.

---

## 2. Método y criterio de clasificación

Para cada mejora se contrastaron:
1. El objetivo y los criterios de aceptación del plan.
2. Los archivos y rutas relevantes de la rama `test`.
3. La evidencia documental de ejecución disponible.
4. La presencia o ausencia de pruebas específicas.

Estados:

- **Implementada:** el resultado requerido existe y hay evidencia suficiente de funcionamiento.
- **Parcialmente implementada:** existe una parte verificable, pero falta un componente del objetivo o una validación obligatoria.
- **No implementada:** no se encontró el cambio requerido o la evidencia disponible demuestra que la brecha permanece.

La ausencia de un archivo en GitHub se interpreta como «no encontrado en el snapshot inspeccionado», no como prueba absoluta de inexistencia fuera del repositorio.

---

## 3. Comparación antes / después

| ID | Mejora del plan | Estado inicial según auditoría | Evidencia en `test` | Estado actual |
|---|---|---|---|---|
| F-01 | Verificar y endurecer Supabase Auth/RLS | Riesgo alto; RLS remota pendiente de verificación | Guía Render del 07/11 todavía documenta RLS permisiva y uso de JWT de lectura condicionado a su endurecimiento | **No implementada** |
| F-02 | Persistir aprobación/rechazo de recomendaciones | No existe persistencia de decisión humana | `recommendations.py` conserva recomendaciones y `executionAllowed=False`; no se encontró endpoint/tabla de decisiones | **No implementada** |
| F-03 | Validar dashboard con sesión real en `/dev/` | Arnés local; sesión real pendiente | Existe guía de acceso a `/dev/` y pipeline Pages, pero no evidencia reproducible de prueba de sesión real | **Parcialmente implementada** |
| F-04 | Completar visualización/acceso a MLflow | Runs locales; UI no demostrada | `software/prediction/README.md` documenta entrenamiento y ejecución, pero no evidencia de UI/servidor MLflow operativo | **No implementada** |
| F-05 | Añadir exportación PDF | JSON/CSV disponibles; PDF pendiente | `routes.py` ofrece JSON y CSV; no se encontró endpoint PDF ni prueba específica | **No implementada** |
| F-06 | Etiquetar energía como estimación cuando corresponda | Potencia modelada, no medida | `dashboard-ui.js` muestra «Potencia modelada, no medida» para origen simulado; `energy.js` declara el modelo lineal | **Parcialmente implementada** |
| U-01 | Publicar guía rápida de usuario | Guía ausente en línea base | Existe `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md` con tareas, roles y límites | **Implementada** |
| U-02 | Auditoría WCAG y alternativa textual al gráfico | Escaneo formal/tabla alternativa pendientes | `dashboard.html` contiene canvas para gráficos; no se encontró evidencia de escaneo WCAG ni prueba de tabla alternativa | **No implementada** |
| U-03 | Simplificar flujo de energía a tres pasos | Flujo de cuatro pasos | Los controles de carga/factor/cálculo siguen presentes; no se encontró evidencia de rediseño validado | **No implementada** |
| R-01 | Pruebas de carga controladas en staging | Carga remota/RLS no suficientemente verificadas | Hay evidencia de pruebas de carga de transacciones del sistema en commits, pero no evidencia suficiente de prueba de carga controlada de Data Processing/PostgREST y RLS en staging | **No implementada** |
| P-01 | Precalentamiento controlado de Render Free | Cold start aproximado de 60 s | Guía de Render sigue describiendo suspensión tras 15 min y despertar manual de servicios; no se encontró automatización de precalentamiento | **No implementada** |
| S-01 | Desacoplar adaptadores del Simulator | `runner.py` importa adaptadores directamente | `runner.py` todavía importa `parse_inventory_json`, `parse_scenario_json` y `RunLogger` desde `adapters` | **No implementada** |

---

## 4. Estado detallado de cada mejora

### F-01. Verificar y endurecer Supabase Auth/RLS

**Estado: NO IMPLEMENTADA**

**Antes:** la auditoría inicial identificó políticas RLS permisivas y falta de verificación completa del acceso remoto.

**Evidencia observada:**
- `docs/GUIA-DESPLIEGUE-RENDER.md` en la rama `test` indica que Data Processing usa `HISTORICAL_SOURCE=supabase` y documenta que la clave anon puede leer `logs` porque la RLS es permisiva; señala que, si se endurece RLS, será necesario un JWT de lectura dedicado.
- El documento no acredita que las políticas se hayan reemplazado ni que se hayan ejecutado pruebas negativas de aislamiento entre usuarios.

**Después:** no se encontró evidencia versionada de migración/políticas restrictivas, pruebas por rol/usuario ni resultado de verificación de RLS remota.

**Conclusión:** la brecha de seguridad permanece abierta en el estado documentado. No se debe modificar producción sin inspeccionar primero las políticas reales y contar con respaldo.

**Riesgo residual:** **Alto** — posible acceso excesivo a históricos.

### F-02. Persistir aprobación/rechazo de recomendaciones (HU-07)

**Estado: NO IMPLEMENTADA**

**Antes:** las recomendaciones no persistían la decisión del operador.

**Evidencia observada:**
- `software/prediction/src/service/recommendations.py` contiene el modelo de recomendación y el endpoint `POST /v1/recommendations`.
- El contrato conserva `executionAllowed: Literal[False] = False`, lo cual mantiene la barrera contra ejecución automática.
- No se encontró en el archivo inspeccionado un endpoint para registrar decisiones, ni evidencia de la tabla `recommendation_decisions` o equivalente.
- `software/prediction/src/service/app.py` incluye el router de recomendaciones, pero no aporta evidencia de un flujo persistente de aprobación.

**Después:** no hay evidencia de almacenamiento de usuario, decisión, justificación y fecha.

**Conclusión:** la salvaguarda de no autoejecución está preservada, pero HU-07 continúa sin trazabilidad persistente.

**Riesgo residual:** **Medio** — no queda historial auditable de las decisiones humanas.

### F-03. Validar dashboard con sesión real de Supabase en `/dev/`

**Estado: PARCIALMENTE IMPLEMENTADA**

**Antes:** la auditoría inicial describía validación local, pendiente de sesión real en el entorno desplegado.

**Evidencia observada:**
- La guía rápida incluye la URL de staging `/dev/` y describe inicio de sesión y roles.
- `docs/evidencias/semana13-ola1-verificacion.md` documenta pruebas del frontend 48/48 y pruebas de navegador para recursos SRI y carga de librerías.
- Esa evidencia declara expresamente que GitHub Pages no usa Nginx y que las suites backend/smoke no se reejecutaron.
- No se encontró en la evidencia inspeccionada un registro reproducible de login real en `/dev/`, expiración/renovación de sesión y recorrido autenticado de las cinco pestañas.

**Después:** el entorno y las instrucciones de acceso están documentados; la prueba integral de sesión real no está demostrada.

**Conclusión:** existe avance documental y validación parcial de frontend, pero el criterio de aceptación de sesión real no puede marcarse como cumplido.

**Riesgo residual:** **Medio** — integración remota de Auth y permisos no confirmada de extremo a extremo.

### F-04. Completar visualización/acceso a MLflow

**Estado: NO IMPLEMENTADA**

**Antes:** el pipeline registraba experimentos localmente, sin UI desplegada demostrada.

**Evidencia observada:**
- `software/prediction/README.md` documenta ejecución del pipeline y entrenamiento de modelos.
- No se encontró evidencia de un servicio MLflow UI desplegado, URL operativa, captura verificable ni procedimiento de acceso para el equipo.
- No se encontró evidencia de que la inferencia dependa de MLflow; esto es positivo para preservar la operación actual.

**Después:** no se demuestra la visualización centralizada de experimentos solicitada.

**Conclusión:** el registro local de experimentos no equivale a disponer de una UI accesible.

**Riesgo residual:** **Bajo/Medio** — trazabilidad experimental menos accesible; evitar convertir MLflow en dependencia crítica.

### F-05. Añadir exportación PDF de reportes históricos

**Estado: NO IMPLEMENTADA**

**Antes:** la API proporcionaba resumen JSON y CSV.

**Evidencia observada:**
- `software/data-processing/infrastructure/adapters/input/api/routes.py` define `GET /reports/historical-summary`.
- El parámetro `format` está limitado a `json` y `csv`.
- No se encontró ruta `historical-pdf`, media type `application/pdf` ni prueba `test_pdf_report.py`.

**Después:** JSON/CSV permanecen disponibles; no hay evidencia del PDF.

**Conclusión:** la mejora no está implementada. La compatibilidad de los formatos existentes parece preservada en el código inspeccionado.

**Riesgo residual:** **Bajo** — falta el formato formal, sin evidencia de regresión en JSON/CSV.

### F-06. Mantener explícita la naturaleza estimada de energía y CO₂e

**Estado: PARCIALMENTE IMPLEMENTADA**

**Antes:** la auditoría advertía que la potencia se calcula mediante un modelo lineal y no procede de sensores físicos.

**Evidencia observada:**
- `software/frontend/energy.js` incluye comentario explícito: la potencia derivada de CPU es un modelo lineal, no una medición.
- `software/frontend/dashboard-ui.js` muestra la procedencia y, para `origin === 'simulated'`, presenta el texto «Potencia modelada, no medida».
- La salida distingue procedencia y el factor de emisión requiere valor y fuente; no se aplica automáticamente un factor por defecto.

**Después:** existe comunicación explícita para el origen simulado y la lógica mantiene la distinción de procedencia. Sin embargo, la evidencia inspeccionada no demuestra que todas las vistas, reportes y exportaciones representen de forma uniforme la condición modelada para todos los orígenes estimados.

**Conclusión:** mejora parcial; no debe elevarse el cumplimiento a total hasta verificar UI, reportes y pruebas para `simulated` y `estimated`.

**Riesgo residual:** **Medio** — interpretación incorrecta si una vista secundaria omite la procedencia.

### U-01. Publicar guía rápida de usuario

**Estado: IMPLEMENTADA**

**Antes:** la auditoría inicial registraba ausencia de guía breve de primer uso.

**Evidencia observada:**
- Existe `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md`.
- El documento explica requisitos, URLs de desarrollo/producción y roles ADMIN, OPERATOR y VIEWER.
- Incluye procedimientos para login, consulta de métricas, racks, predicción, recomendaciones y descarga CSV.
- Explica la naturaleza simulada/modelada de los datos y los límites de la demostración.
- `docs/evidencias/semana13-ola1-verificacion.md` registra revisión de textos de la guía contra la interfaz (10/10 textos) y la regla VIEWER.

**Después:** el entregable documental existe y está alineado con componentes de interfaz citados.

**Conclusión:** implementada como mejora documental. No se afirma que exista una prueba formal de usabilidad con usuarios finales.

**Riesgo residual:** **Bajo** — mantener la guía sincronizada con cambios de interfaz y endpoints.

### U-02. Auditoría WCAG y alternativa textual al gráfico

**Estado: NO IMPLEMENTADA**

**Antes:** la auditoría identificó semántica/ARIA parcial, pero no escaneo formal ni tabla alternativa asociada al gráfico.

**Evidencia observada:**
- `software/frontend/dashboard.html` contiene el dashboard y sus paneles; el gráfico de resumen se representa con canvas.
- No se encontró evidencia de un informe Lighthouse/axe con resultados WCAG 2.1 AA.
- No se encontró la prueba o implementación identificable de la tabla textual alternativa solicitada.

**Después:** no se demuestra la ejecución de la auditoría de accesibilidad ni la alternativa textual.

**Conclusión:** la brecha permanece.

**Riesgo residual:** **Medio** — usuarios de lector de pantalla pueden no disponer de una alternativa equivalente al gráfico.

### U-03. Simplificar flujo de energía a tres pasos

**Estado: NO IMPLEMENTADA**

**Antes:** el flujo de energía con archivo, factor, fuente y cálculo se describía como una secuencia de cuatro acciones.

**Evidencia observada:**
- `software/frontend/dashboard-ui.js` conserva listeners separados para ejemplo, descarga, carga y envío de energía.
- `software/frontend/energy.js` valida factor y fuente como datos asociados, sin evidencia de que el flujo de interfaz haya sido reducido a tres pasos.
- No se encontró evidencia de prueba de usabilidad o comparación antes/después que demuestre el nuevo flujo.

**Después:** la lógica de cálculo y sus validaciones permanecen presentes; la simplificación solicitada no está acreditada.

**Conclusión:** no implementada.

**Riesgo residual:** **Bajo** — fricción operativa del flujo actual.

### R-01. Pruebas de carga controladas en staging

**Estado: NO IMPLEMENTADA**

**Antes:** la auditoría solicitaba validar resistencia ante carga remota y comportamiento de PostgREST/Supabase.

**Evidencia observada:**
- El historial de commits menciona una carga de transacciones contra Render (601/601 HTTP 200 en una prueba del flujo de video y 16/16 en otro ensayo).
- Esa evidencia no acredita una prueba controlada de carga de Data Processing/PostgREST en staging, ni medición de latencia p95/p99, errores, conexiones y recuperación bajo carga.
- La guía de Render confirma el uso de Supabase en Data Processing, pero no sustituye una prueba de carga.

**Después:** hay evidencia de pruebas de transacciones en el sistema, pero no de la prueba específica requerida por el plan.

**Conclusión:** no implementada conforme al criterio definido en R-01. No se afirma que el servicio falle; se afirma que el ensayo requerido no está demostrado.

**Riesgo residual:** **Medio/Alto** — capacidad y estabilidad bajo carga remota siguen sin caracterización suficiente.

### P-01. Precalentamiento controlado de Render Free

**Estado: NO IMPLEMENTADA**

**Antes:** la auditoría registraba cold start aproximado de 60 segundos después de inactividad en Render Free.

**Evidencia observada:**
- `docs/GUIA-DESPLIEGUE-RENDER.md` describe suspensión tras 15 minutos sin tráfico y recomienda despertar los servicios antes de una demostración.
- No se encontró un script/job versionado de precalentamiento programado ni evidencia de mediciones comparativas antes/después.
- La documentación sigue reconociendo el cold start como limitación del plan gratuito.

**Después:** existe procedimiento operativo manual, no automatización de precalentamiento.

**Conclusión:** no implementada respecto al objetivo automatizado/controlado. La documentación de la limitación sí está presente.

**Riesgo residual:** **Medio** — primera petición de una sesión puede exceder el umbral esperado; un keep-alive continuo podría consumir cuota gratuita.

### S-01. Desacoplar adaptadores del Simulator

**Estado: NO IMPLEMENTADA**

**Antes:** `runner.py` importaba directamente componentes de infraestructura/adaptadores desde la capa de aplicación.

**Evidencia observada:**
- `software/simulator/src/green_ai_simulator/application/runner.py` sigue importando:
  - `parse_inventory_json` desde `adapters.configuration.json_parser`.
  - `parse_scenario_json` desde `adapters.configuration.scenario_parser`.
  - `RunLogger` desde `adapters.persistence.run_logger`.
- No se encontró evidencia en el archivo inspeccionado de puertos o interfaces que sustituyan esas dependencias directas.

**Después:** el acoplamiento señalado persiste en la rama inspeccionada.

**Conclusión:** no implementada. No se recomienda realizar la refactorización sin pruebas deterministas y de contrato del exportador Prometheus.

**Riesgo residual:** **Medio** — mantenibilidad y testabilidad del caso de uso.

---

## 5. Regresiones, errores nuevos e incompatibilidades

### 5.1 Hallazgos de regresión

En el alcance de archivos y evidencias inspeccionados **no se identificó una regresión funcional demostrada atribuible a las mejoras del plan FURPS**. Esta conclusión es limitada: no se ejecutó una batería completa en esta auditoría y el historial consultado no demuestra por sí solo el estado desplegado actual.

### 5.2 Evidencia de pruebas disponible

`docs/evidencias/semana13-ola1-verificacion.md` registra:
- Frontend: **48/48** pruebas aprobadas.
- Nginx: `nginx -t` correcto.
- Cabeceras de seguridad servidas en rutas probadas.
- Verificación de SRI y carga de librerías en navegador.
- YAML de workflows validado.
- **No ejecutado:** GitHub Actions por ausencia de push.
- **No reejecutado:** suites backend y smoke 14/14 durante esa ola.

Estos resultados pertenecen a la evidencia documentada de Ola 1; **no son una ejecución nueva realizada el 19/11/2026** y no prueban las doce mejoras del plan generado en esta conversación.

### 5.3 Incompatibilidades

- **No se observó** evidencia de cambios en los contratos JSON/CSV del endpoint de reportes; el código inspeccionado conserva `format: json | csv`.
- **No se observó** que las recomendaciones permitan autoejecución; `executionAllowed` permanece fijado en `False`.
- **No se puede certificar** compatibilidad de las mejoras no implementadas o no verificadas.
- El historial/documentación tiene una discrepancia temporal: el estado observable de GitHub llega al 10/11/2026, mientras que la fecha de auditoría es 19/11/2026.

### 5.4 Incidencias que requieren seguimiento

1. RLS permisiva documentada en la guía de despliegue.
2. Ausencia de persistencia de decisiones humanas.
3. PDF no implementado.
4. Accesibilidad WCAG sin evidencia formal.
5. Pruebas de carga específicas de PostgREST/RLS no demostradas.
6. Cold start mitigado solo mediante procedimiento manual documentado.
7. Dependencias directas de adaptadores en Simulator.

---

## 6. Riesgos residuales consolidados

| Riesgo | Severidad | Estado | Acción requerida |
|---|---|---|---|
| Políticas RLS permisivas / aislamiento no demostrado | **Alto** | Abierto | Verificación remota autorizada y pruebas negativas en staging |
| Decisiones humanas sin persistencia | **Medio** | Abierto | Implementar tabla/endpoint con control de rol e idempotencia |
| Sesión real en `/dev/` no acreditada | **Medio** | Parcial | Evidencia de login, renovación, logout y acceso por rol |
| Energía estimada no etiquetada uniformemente en todas las salidas | **Medio** | Parcial | Verificar todas las vistas y reportes por origen |
| Capacidad PostgREST bajo carga no caracterizada | **Medio/Alto** | Abierto | Prueba controlada de carga en staging |
| Accesibilidad de gráficos | **Medio** | Abierto | Auditoría WCAG y alternativa textual |
| Cold start de Render Free | **Medio** | Abierto | Procedimiento de demostración medido y control de cuota |
| Acoplamiento de Simulator | **Medio** | Abierto | Refactorización aislada con pruebas deterministas |
| Ausencia de PDF | **Bajo** | Abierto | Añadir formato sin retirar JSON/CSV |
| MLflow sin UI accesible | **Bajo/Medio** | Abierto | Evidencia de consulta de experimentos sin dependencia operativa |

---

## 7. Conclusión de cumplimiento

**Dictamen: CUMPLIMIENTO PARCIAL DEL PLAN; NO APTO PARA CIERRE DE LA FASE FURPS+.**

La evidencia inspeccionada permite confirmar una mejora implementada (U-01), dos parcialmente implementadas (F-03 y F-06) y nueve no implementadas o no demostradas. La guía rápida constituye un avance verificable. La distinción entre potencia modelada y medida también está reflejada en el frontend, pero falta verificar su consistencia en todas las salidas. La validación de sesión real en `/dev/` no cuenta con evidencia suficiente para cerrar el criterio.

Las brechas críticas y de mayor riesgo —especialmente RLS/Supabase— deben resolverse antes de declarar la calidad y seguridad operativa completas. La persistencia de aprobaciones, pruebas de carga específicas, PDF, accesibilidad y desacoplamiento del Simulator continúan pendientes en el snapshot revisado.

### 7.1 Condiciones para una nueva auditoría

1. Confirmar el SHA más reciente de la rama `test` y la fecha del último commit.
2. Entregar evidencia de las políticas RLS remotas y pruebas de aislamiento, sin compartir secretos.
3. Ejecutar las suites de regresión actuales y adjuntar logs completos.
4. Probar login real en `/dev/` con cuentas de cada rol.
5. Aportar resultados de pruebas de carga específicas de Data Processing/PostgREST en staging.
6. Adjuntar evidencias de PDF, MLflow UI, accesibilidad y aprobación persistida cuando estén implementadas.
7. Repetir la revisión del Simulator y comparar métricas Prometheus antes/después.

**No se asigna un nuevo puntaje FURPS+ en este documento.** La auditoría de implementación clasifica el cumplimiento de las mejoras; la recalificación requiere aplicar la matriz oficial sobre evidencia actualizada y resolver previamente la discrepancia aritmética documentada en la línea base.
