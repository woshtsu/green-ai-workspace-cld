# 01\_Auditoria\_FURPS.md — Auditoría de Calidad de Software (FURPS+)

**Proyecto:** Green AI — Optimización energética y gestión de capacidad en centros de datos mediante Machine Learning  
**Asignatura:** Taller de Proyectos 1 — Universidad Continental  
**Rama de referencia:** `test`  
**Fecha de referencia documental:** noviembre de 2026  
**Tipo de evaluación:** Diagnóstico inicial FURPS+  
**Alcance de evidencia:** Monorepo Green AI y documentación técnica descrita en el informe de Semana 13.

> \*\*Criterio de auditoría:\*\* Este documento consolida el diagnóstico inicial descrito en el informe del proyecto. Los hallazgos se consideran respaldados por las rutas, líneas, pruebas y evidencias citadas. Cuando el informe indica que una validación está pendiente, no se considera como cumplimiento completo. Esta auditoría no modifica archivos ni ejecuta cambios en el proyecto.

\---

## 1\. Resumen ejecutivo

Green AI presenta una arquitectura distribuida compuesta por Simulator, Monitoring, Data Processing, Prediction, API Gateway, Frontend e infraestructura de observabilidad. La solución integra tecnologías Python/FastAPI, Java/Spring Boot, Go, Prometheus, Docker Compose, Supabase y GitHub Actions.

El diagnóstico inicial obtiene **85.00/100 de calidad FURPS+ ponderada**, con una base sólida en confiabilidad, mantenibilidad y restricciones técnicas. La cobertura funcional es amplia para los procesos principales de monitoreo, consulta histórica, predicción, recomendaciones y alertas. Sin embargo, existen brechas que impiden considerar completa la solución: aprobación humana de recomendaciones sin persistencia, potencia energética modelada y no medida por sensores físicos, MLflow sin interfaz desplegada, reportes sin PDF y validaciones pendientes del entorno Supabase.

Las principales debilidades adicionales se concentran en la falta de una guía rápida de usuario en el diagnóstico inicial, ausencia de validación formal WCAG 2.1 AA, arranque en frío del hosting gratuito y acoplamiento de adaptadores en el Simulator.

**Dictamen:** calidad inicial satisfactoria, con riesgos funcionales y operativos que deben mantenerse visibles. El porcentaje no representa certificación ni garantía de operación productiva; corresponde a la escala interna de evaluación definida para el proyecto.

## 2\. Puntaje por categoría

|Categoría|Puntaje|Ponderación|Aporte ponderado|Estado|
|-|-:|-:|-:|-|
|Functionality (F)|78/100|25 %|19.50|Aceptable|
|Usability (U)|80/100|15 %|12.00|Aceptable|
|Reliability (R)|93/100|20 %|18.60|Bueno|
|Performance (P)|87/100|15 %|13.05|Bueno|
|Supportability (S)|90/100|15 %|13.50|Bueno|
|Restricciones adicionales (+)|93/100|10 %|9.30|Bueno|
|**Total ponderado**||**100 %**|**85.95/100**|**Satisfactorio**|

**Nota de consistencia:** El informe consolidado del equipo registra el resultado global como **85.00/100**. La suma aritmética de los puntajes por categoría y ponderaciones mostrados en su tabla (78, 80, 93, 87, 90 y 93) produce **85.95/100**. Por tanto, existe una discrepancia de cálculo que debe resolverse en la matriz maestra antes de publicar un único valor oficial. Para mantener trazabilidad con el informe institucional, este documento conserva **85.00/100 como valor declarado por el equipo** y deja registrada la inconsistencia como hallazgo de auditoría documental.

## 3\. Evaluación por categoría

### 3.1 Functionality (F) — 78/100

**Estado general:** cobertura amplia de las funciones principales, con funcionalidades parciales y una función crítica ausente.

**Funcionalidades implementadas**

* **HU-01 — Monitoreo:** telemetría sintética determinista de 50 servidores; Prometheus realiza el scraping y Monitoring expone catálogo, métricas actuales e históricos. Evidencia: `software/simulator/README.md:L48-L66`, `software/monitoring/src/main/resources/application.yaml:L1-L15`, `software/frontend/dashboard.html:L63-L94`.
* **HU-02 — Históricos:** endpoint `GET /api/v1/historical-logs`, paginación keyset y ventana máxima de 31 días; adaptadores SQLite y Supabase. Evidencia: `software/data-processing/infrastructure/adapters/input/api/routes.py:L33-L45`, `docs/DECISIONES.md:L32-L50`.
* **HU-03 — Predicción:** endpoint `POST /v1/predictions`, modelo Random Forest con horizonte de 15 minutos y metadatos `origin="estimated"`. Evidencia: `software/prediction/src/service/app.py:L132-L144`.
* **HU-04 — Comparación de modelos:** pipeline que compara Persistencia, Media Móvil, Random Forest y XGBoost; experimento Baseline vs. Green AI. Evidencia: `software/prediction/README.md:L11-L15`, `docs/academico/10-plan-experimental.md:L22-L28`.
* **HU-06 — Recomendaciones:** evaluación de CPU, memoria, latencia y tasa de errores; las recomendaciones retornan `executionAllowed: false` para evitar ejecución automática. Evidencia: `software/prediction/src/service/recommendations.py:L15-L80`.
* **HU-12 — Alertas:** cuatro reglas de alerta configuradas y validadas con `promtool`. Evidencia: `software/infraestructura/prometheus/alerts.yml`, `docs/HANDOFF.md:L111`.
* **HU-14 — RBAC:** Gateway valida roles `ADMIN`, `OPERATOR` y `VIEWER`. Evidencia: `software/gateway/src/main/resources/application.yaml:L70-L75`, `software/gateway-go/internal/policy/`.

**Funcionalidades parciales**

* **HU-05 — MLflow:** se registra un experimento local en `software/prediction/mlruns/`, pero no se acredita una UI de MLflow desplegada ni evidencia de acceso público. Evidencia: `docs/HANDOFF.md:L88-L91`.
* **HU-09 — Energía y CO₂e:** existe cálculo de kWh mediante integración trapezoidal, pero la potencia se obtiene de un modelo sintético y no de sensores físicos; el factor de emisión requiere entrada manual. Evidencia: `software/frontend/energy.js:L10-L50`.
* **HU-11 — Dashboard integrado:** interfaz implementada y probada en entorno local; queda pendiente la validación de sesión real de Supabase en el entorno publicado `/dev/`. Evidencia: `docs/CONTINUAR-EN-NUEVO-CHAT.md:L21-L22`.
* **HU-13 — Reportes:** se generan resúmenes JSON y exportación CSV; no se encuentra implementada la generación formal de PDF. Evidencia: `software/data-processing/infrastructure/adapters/input/api/routes.py:L8-L14`, `docs/HANDOFF.md:L113`.
* **HU-15 — Autenticación:** flujo PKCE y configuración de Supabase Auth presentes; faltan pruebas automatizadas con usuario real y verificación concluyente de las políticas RLS remotas. Evidencia: `software/frontend/supabase-auth-setup.sql`, `docs/HANDOFF.md:L150-L155`.

**Funcionalidad ausente**

* **HU-07 — Aprobación humana persistida:** no existe flujo completo de aprobar/rechazar recomendaciones con persistencia de la decisión. La bandera `executionAllowed: false` bloquea la ejecución automática, pero no reemplaza el registro de la decisión humana. Evidencia: `docs/academico/08-pruebas-resultados-discusion.md:L31`.

**Brechas y riesgos**

* Riesgo medio: ausencia de trazabilidad persistente de decisiones humanas sobre recomendaciones.
* Riesgo medio: el cálculo energético no representa medición física real; debe interpretarse como estimación basada en modelo.
* Riesgo bajo: MLflow y reportes PDF incompletos respecto del alcance previsto.
* Riesgo alto: políticas RLS remotas pendientes de verificación, con posible exposición de datos si la configuración es permisiva.

### 3.2 Usability (U) — 80/100

**Estado general:** interfaz estructurada y con mecanismos útiles de interacción; faltan validaciones formales de accesibilidad y documentación de primer uso en el diagnóstico inicial.

**Hallazgos favorables**

* Frontend organizado en cinco pestañas: resumen, detalle por servidor, predicción/recomendación, reportes/experimento y energía/CO₂e. Evidencia: `software/frontend/dashboard.html:L54-L60`.
* Vistas complementarias para mapa de calor de racks y topología de red. Evidencia: `software/frontend/network.html`, `software/frontend/racks.js:L27-L48`, `software/frontend/flows.html`.
* Modo claro/oscuro con persistencia de preferencia. Evidencia: `software/frontend/appearance.js`.
* Ayuda contextual para explicar indicadores, cálculos y límites experimentales. Evidencia: `software/frontend/help-content.js:L1-L100`.
* Traducción de errores técnicos a mensajes comprensibles y acciones sugeridas. Evidencia: `software/frontend/friendly-errors.js:L21-L64`.

**Brechas**

* No se acredita una guía rápida de usuario en el diagnóstico inicial. Evidencia: revisión de `docs/` y `software/frontend/` consignada en la matriz.
* Los gráficos Chart.js no presentan una tabla alternativa accesible en la misma vista. Evidencia: `software/frontend/dashboard.html:L91`.
* No se acredita ejecución formal de auditoría WCAG 2.1 AA con Lighthouse o axe-core.
* El flujo de cálculo de energía con archivo y factor de emisión supera tres pasos. Evidencia: `software/frontend/dashboard.html:L275-L289`.

**Riesgos**

* Riesgo medio: curva de aprendizaje y dependencia de asistencia técnica por falta de guía rápida.
* Riesgo bajo: barreras parciales para usuarios de tecnologías de asistencia y fricción en el flujo de energía.

### 3.3 Reliability (R) — 93/100

**Estado general:** categoría de mayor fortaleza. El sistema documenta manejo estandarizado de errores, health checks, timeouts defensivos y pruebas automatizadas.

**Hallazgos favorables**

* Respuestas de error `application/problem+json` con identificador de solicitud en Data Processing y Prediction. Evidencia: `software/data-processing/main.py:L24-L37`, `software/prediction/src/service/app.py:L62-L82`.
* Manejo de errores de persistencia y traducción a códigos HTTP 422, 502, 503 y 504 sin exponer credenciales ni trazas internas. Evidencia: `software/data-processing/main.py:L40-L57`.
* Health checks y readiness/liveness en Prediction, Data Processing, Monitoring y Gateway. Evidencia: `software/prediction/src/service/app.py:L112-L130`, `software/data-processing/infrastructure/adapters/input/api/routes.py:L33-L35`, configuraciones Actuator y `software/gateway-go/README.md`.
* Timeouts por servicio para limitar bloqueos y fallos en cascada. Evidencia: `software/gateway/src/main/resources/application.yaml:L26-L53`, `software/data-processing/main.py:L79`.
* El informe registra más de 415 pruebas automatizadas y smoke test de 14/14 comprobaciones. Evidencia: `docs/HANDOFF.md:L36-L49`, `docs/evidencias/smoke-20261106.json`.

**Brechas**

* Resistencia ante carga elevada en PostgREST/Supabase no queda validada concluyentemente.
* Las políticas RLS remotas requieren revisión y prueba de acceso por rol. Evidencia: `docs/HANDOFF.md:L150-L155`.

**Riesgos**

* Riesgo medio-alto: una política RLS incorrecta o una saturación del servicio remoto podría comprometer disponibilidad o aislamiento de datos.
* La cantidad de pruebas reportada no sustituye pruebas de carga, resiliencia y recuperación sobre la infraestructura remota.

### 3.4 Performance (P) — 87/100

**Estado general:** buen rendimiento local y uso de memoria contenido; la disponibilidad del hosting gratuito introduce latencias de arranque en frío.

**Hallazgos favorables**

* Mediciones locales documentadas inferiores a 30 ms para Java y 4 ms para Gateway Go en las pruebas citadas. Evidencia: `docs/evidencias/gateway-go-difftest-20261106.txt:L46-L50`.
* Consumo de memoria documentado: Prediction 122–142 MiB, Gateway Go 2.3–9.8 MiB, Data Processing 76 MiB y Monitoring aproximadamente 211 MiB. Evidencia: `docs/evidencias/prediction-imagen-ligera-20261107.md:L8-L12` y mediciones referenciadas en la matriz.
* Imagen de Prediction reducida de 2.85 GB a 510 MB mediante Docker multi-stage. Evidencia: `docs/evidencias/prediction-imagen-ligera-20261107.md:L7-L12`.

**Brechas**

* Render Free Tier puede suspender servicios tras inactividad y generar arranque en frío cercano a 60 segundos, superando el umbral de respuesta de 7 segundos definido en la matriz. Evidencia: `docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25`.
* Los resultados locales no representan necesariamente el rendimiento bajo concurrencia ni en la nube.

**Riesgos**

* Riesgo medio: experiencia degradada en la primera petición después de la suspensión del servicio.
* Riesgo medio: extrapolar resultados locales a producción sin pruebas de carga y mediciones distribuidas.

### 3.5 Supportability (S) — 90/100

**Estado general:** buena modularidad, contratos versionados y CI; se identifica un punto concreto de acoplamiento arquitectónico.

**Hallazgos favorables**

* Arquitectura hexagonal aplicada en Monitoring, Data Processing y Gateway Go, según el inventario del proyecto.
* Contratos OpenAPI versionados para Gateway y Data Processing; documentación Swagger en Prediction. Evidencia: `software/gateway/src/main/resources/static/openapi/gateway-v0.1.yaml`, `software/data-processing/contracts/data-processing-v1.openapi.json`.
* CI mediante GitHub Actions para ejecutar suites de pruebas. Evidencia: `.github/workflows/ci.yml`.
* Monorepo sin repositorios Git anidados ni gitlinks, según verificación consignada en `AGENTS.md` y `docs/DECISIONES.md:L5-L15`.

**Brecha**

* `software/simulator/src/green\_ai\_simulator/application/runner.py:L5-L10` importa adaptadores directamente desde la capa de aplicación, debilitando la inversión de dependencias y el aislamiento de infraestructura.

**Riesgo**

* Riesgo medio: el acoplamiento dificulta pruebas aisladas, sustitución de adaptadores y evolución del Simulator.

### 3.6 Restricciones adicionales (+) — 93/100

**Estado general:** restricciones de despliegue, licencias e integración externa están documentadas; persisten límites inherentes al hosting gratuito.

**Hallazgos favorables**

* Orquestación local mediante Docker Compose. Evidencia: `software/infraestructura/docker-compose.yml`.
* Guía de despliegue para Render y GitHub Pages. Evidencia: `docs/GUIA-DESPLIEGUE-RENDER.md`.
* Integración con Supabase Auth mediante verificación de JWKS y sin evidencia reportada de exposición de `service\_role` en frontend. Evidencia: `software/gateway/src/main/resources/application.yaml:L70-L75`, `software/frontend/README.md:L10-L13`.
* El informe declara uso de dependencias Open Source y referencia la Ley N.° 29733 de Protección de Datos Personales.

**Brecha**

* El hosting gratuito impone suspensión por inactividad, memoria y cuota mensual compartida, por lo que no garantiza disponibilidad continua. Evidencia: `docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25`, `render.yaml`.

**Riesgo**

* Riesgo medio: limitaciones de cuota y disponibilidad pueden afectar demostraciones o pruebas que requieran acceso continuo.

## 4\. Hallazgos transversales priorizados

|ID|Categoría|Hallazgo|Severidad|Evidencia principal|
|-|-|-|-|-|
|F-03|F|Aprobación humana de recomendaciones sin persistencia|Medio|`docs/academico/08-pruebas-resultados-discusion.md:L31`|
|F-01|F|Potencia/energía modeladas, no medidas físicamente|Medio|`software/frontend/energy.js:L10-L50`|
|F-05|F / R|RLS de Supabase pendiente de verificación concluyente|Alto|`docs/HANDOFF.md:L150-L155`|
|F-02|F|MLflow sin UI desplegada acreditada|Bajo|`docs/HANDOFF.md:L88-L91`|
|F-04|F|Reportes sin exportación PDF|Bajo|`docs/HANDOFF.md:L113`|
|U-01|U|Guía rápida ausente en el diagnóstico inicial|Medio|Revisión de `docs/` y `software/frontend/` consignada en matriz|
|U-02/U-03|U|Accesibilidad de gráficos y auditoría WCAG pendientes|Bajo|`software/frontend/dashboard.html:L91`|
|R-05|R|Resistencia a carga remota y aislamiento RLS no concluyentes|Medio|`docs/HANDOFF.md:L150-L155`|
|P-01|P|Cold start de Render Free Tier superior al umbral de 7 s|Medio|`docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25`|
|S-01|S|Dependencia directa de adaptadores en Simulator|Medio|`software/simulator/src/green\_ai\_simulator/application/runner.py:L5-L10`|
|DOC-01|Transversal|Diferencia entre total declarado (85.00) y recálculo ponderado (85.95)|Medio|Tabla de puntajes FURPS+ del informe Semana 13|

## 5\. Brechas identificadas

1. Completar el flujo de aprobación/rechazo de recomendaciones y su trazabilidad persistente.
2. Mantener claramente diferenciadas la telemetría simulada, las estimaciones matemáticas y las mediciones físicas reales.
3. Acreditar despliegue y acceso a MLflow si forma parte del alcance funcional comprometido.
4. Completar la generación de reportes PDF si se mantiene como requisito.
5. Verificar autenticación real y políticas RLS en Supabase con pruebas por rol.
6. Incorporar documentación operativa de primer uso y evidencia formal de accesibilidad.
7. Medir rendimiento en entorno remoto y bajo concurrencia, separándolo de las mediciones locales.
8. Corregir la dependencia arquitectónica de adaptadores en la capa de aplicación del Simulator.
9. Unificar el cálculo del puntaje global y los porcentajes en todos los artefactos de calidad.

## 6\. Riesgos detectados

|Riesgo|Probabilidad / impacto cualitativo|Consecuencia potencial|
|-|-|-|
|RLS permisiva o incorrecta en Supabase|Media / Alta|Acceso no autorizado o exposición de registros|
|Recomendaciones sin aprobación persistida|Media / Media|Ausencia de trazabilidad y auditoría de decisiones|
|Interpretar potencia modelada como medición real|Media / Alta|Conclusiones energéticas engañosas|
|Cold start en hosting gratuito|Alta / Media|Demoras de acceso y fallas en demostraciones|
|Falta de PDF y MLflow UI|Media / Baja|Incumplimiento parcial de requisitos del producto|
|Accesibilidad no validada formalmente|Media / Baja|Barreras para usuarios con tecnologías de asistencia|
|Acoplamiento en Simulator|Media / Media|Mayor costo de mantenimiento y pruebas|
|Inconsistencia aritmética del score|Alta / Media|Dictamen de calidad no reproducible|

## 7\. Recomendaciones de alto nivel

* Priorizar la verificación de seguridad de Supabase y las políticas RLS antes de considerar validado el acceso a datos remotos.
* Completar la trazabilidad de decisiones humanas para las recomendaciones operativas.
* Comunicar en interfaz y documentación que la potencia y energía son estimaciones basadas en telemetría sintética mientras no existan sensores físicos integrados.
* Cerrar las brechas de entregables funcionales comprometidos (MLflow UI y PDF) o documentar formalmente su exclusión del alcance.
* Ejecutar pruebas de accesibilidad automatizadas y revisión manual con tecnologías de asistencia.
* Separar y documentar resultados de rendimiento local, pruebas de carga y mediciones del entorno desplegado.
* Mantener las pruebas automatizadas y smoke tests como barrera de regresión.
* Revisar el límite arquitectónico del Simulator para preservar la inversión de dependencias.
* Corregir y recalcular el puntaje global de forma reproducible antes de emitir la versión final del informe.

## 8\. Limitaciones de la auditoría

* El diagnóstico se elaboró a partir de las evidencias y rutas técnicas consignadas en el informe de Semana 13 y en `01\_auditoria\_furps.md`; no se ejecutó una nueva compilación, análisis estático ni prueba dinámica del repositorio durante esta elaboración.
* Las mediciones de rendimiento citadas son las que el equipo documentó; no se deben interpretar como SLA ni como garantía de rendimiento continuo.
* Los resultados no equivalen a certificación ISO, auditoría externa independiente ni validación de producción.
* La puntuación corresponde a la escala interna de la matriz FURPS+ del curso.

## 9\. Dictamen

**Resultado declarado por el equipo: 85.00/100 — Satisfactorio**, sujeto a las brechas funcionales, de seguridad, rendimiento y mantenibilidad descritas. Se identifica una discrepancia aritmética que debe resolverse: con los puntajes por categoría y ponderaciones consignados, el total calculado es 85.95/100. Hasta que se corrija la matriz maestra, ambos valores deben permanecer diferenciados y no presentarse como equivalentes.

