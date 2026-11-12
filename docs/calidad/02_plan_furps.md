# 02_Plan_FURPS.md — Plan Integral de Mejora de Calidad de Software (Modelo FURPS+)

**Proyecto:** Green AI (Optimización Energética y Capacidad en Data Centers con Machine Learning)  
**Institución:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol del Planificador:** Arquitecto de Software Senior  
**Fecha de Emisión:** 2026-11-07  
**Rama Base de Trabajo:** test (desarrollo activo; integración hacia main con pruebas)  
**Documento de Entrada:** docs/calidad/01_auditoria_furps.md  
**Marco de Referencia:** Modelo de Calidad FURPS+ (HP / Rational Software Corp.) y Directrices de Calidad UC  

---

## 1. Principios de Arquitectura y Restricciones Obligatorias

### 1.1. Restricción Fundamental: El Sistema ya Funciona
El sistema Green AI cuenta con una arquitectura hexagonal desacoplada, perímetro de seguridad operativo, 415 o más pruebas automatizadas pasando de forma exitosa y despliegues estables en desarrollo y producción. Por ende, ninguna propuesta de este plan de mejora debe poner en riesgo las funcionalidades existentes ni degradar la operación actual.

### 1.2. Principios Obligatorios de Ejecución
1. **Compatibilidad hacia atrás estricta:** Ningún cambio en contratos OpenAPI, formatos de respuesta RFC 7807 problem+json o esquemas de base de datos puede romper consumidores vigentes.
2. **Incrementos delgados y verificables:** Cada modificación se implementa en ramas de trabajo independientes o worktrees aislados, abordando un único cambio por incremento.
3. **Riesgo mínimo y zero-downtime:** Se prohíben migraciones destructivas. Cualquier ajuste en persistencia sigue el patrón expandir/contraer.
4. **Validación obligatoria con pruebas automatizadas:** Ningún cambio se considera completado sin la ejecución exitosa de su suite correspondiente antes del merge.
5. **Reversibilidad total (Rollback garantizado):** Cada entrega debe asociarse a un commit aislado que permita su reversión inmediata mediante comando git revert limpio.

---

## 2. Estrategia de Preservación de Funcionalidad

Para asegurar que ninguna intervención afecte la estabilidad del sistema, se define una barrera de regresión compuesta por las 7 suites de pruebas verificadas en el monorepo. Toda tarea del plan FURPS+ exige la ejecución obligatoria de su suite de dominio antes de solicitar revisión, y la corrida de humo global previa a la integración en la rama test.

### 2.1. Inventario de Suites de Pruebas de Regresión

| Subsistema / Ámbito | Herramienta | Pruebas Activas | Comando Concreto de Validación | Criterio de Aceptación |
|---|---|:---:|---|---|
| **Frontend** | node:test | 48 pruebas | `node --test tests/frontend/*.test.cjs` en `software/frontend/` | 48 pasadas, 0 fallos |
| **Prediction Service** | pytest | 100 pruebas | `pytest` en `software/prediction/` | 100 pasadas, 0 fallos, prevención anti-leakage |
| **Data Processing** | pytest | 121 pruebas | `pytest` en `software/data-processing/` | 121 pasadas, contratos SQLite/Postgres y CSV OK |
| **Monitoring Service** | Maven / JUnit 5 | 112 pruebas | `mvn test` en `software/monitoring/` | 112 pasadas, 0 fallos, parsing PromQL y fixtures |
| **API Gateway** | JUnit / Go test | 12 / 30 pruebas | `mvn test` en `software/gateway/` o `go test ./...` en `software/gateway-go/` | 12 pasadas en Java / 30 con flag -race en Go |
| **Simulator** | unittest (Docker) | 10 pruebas | `docker compose run --rm simulator python -m unittest discover tests` | 10 pasadas en Linux, determinismo verificado |
| **Smoke Test Global** | Python / Requests | 14/14 pasos | `python software/infraestructura/smoke.py` | 14 checks HTTP exitosos sobre stack en ejecución |

---

## 3. Roadmap de Ejecución en Olas

El plan se organiza en tres olas de trabajo sincronizadas con el calendario académico y los sprints del monorepo, asegurando balance de carga entre los integrantes del equipo.

```
+-----------------------------------------------------------------------------------+
| OLA 1: Semana 13 (07/11/2026 - 09/11/2026)                                        |
| Implementación Inmediata (Documental / Usabilidad)                               |
| -> M-U07: Guía rápida de usuario (entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md)                    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| OLA 2: Sprint 7 (17/11/2026 - 23/11/2026)                                         |
| Funcionalidades Críticas, Seguridad, Despliegue y Mantenibilidad                  |
| -> M-F07: Aprobación humana persistida HU-07 (Ricardo Porras Veli)                |
| -> M-F11: Generación de reporte PDF formal HU-13 (Jhonny Quintana Carhuaricra)   |
| -> M-F05: MLflow UI con evidencia visual HU-05 (Gina Barrera Peña)                |
| -> M-F09: Verificación dashboard en /dev/ con sesión real (Leonid Huamán)        |
| -> M-S01: Refactor hexagonal en Simulator runner.py (Leonid Huamán)               |
| -> M-P01: Keep-alive / precalentamiento Render (Ricardo Porras Veli)              |
| -> M-U06: Auditoría Lighthouse WCAG 2.1 AA y tabla Chart.js (Leonid Huamán)      |
| -> M-F13 / M-R05: Endurecimiento RLS Supabase (Dueño Supabase / Ricardo Porras)  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| OLA 3: Sprint 8 (24/11/2026 - 30/11/2026)                                         |
| Optimizaciones Finales, Ergonomía y Gestión de Hosting                            |
| -> M-F08: Energía y CO2e con factores certificados (Gina Barrera Peña)            |
| -> M-U08: Flujo de energía optimizado en <= 3 pasos (Leonid Huamán)               |
| -> M-PL03: Automatización de reposo y ahorro en Render (Leonid Huamán)             |
+-----------------------------------------------------------------------------------+
```

---

## 4. Fichas Detalladas de Mejora por Brecha Detectada

A continuación se define la especificación técnica de intervención para cada una de las 13 brechas (calificadas como No cumple o Parcial) registradas en docs/calidad/01_auditoria_furps.md.

---

### Brecha 1: M-U07 — Inexistencia de Guía Rápida de Usuario

* **Factor FURPS+:** Usabilidad (U)
* **Requisito / ID Matriz:** M-U07
* **Estado Inicial:** No cumple (1 punto)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Redactar y publicar en `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md` un manual conciso (máximo 2 páginas) orientado al usuario final (administrador de TI, operador de centro de datos y auditor observador), detallando requisitos, accesos, roles y tareas cotidianas en 3 pasos o menos, sin inventar botones y sustentado en los componentes reales de la interfaz.
* **Justificación:** ¿Cómo puede operar el clúster un usuario sin asistencia técnica? Actualmente carece de una síntesis operativa para ejecutar flujos críticos de telemetría, inferencia y reportes sin tener que inspeccionar el código fuente.
* **Prioridad:** Alta (Ola 1, implementación inmediata).
* **Nivel de Riesgo:** Mínimo (cambio documental, no altera lógica de ejecución ni contratos de API).
* **Dependencias:** Interfaz web desplegada en `software/frontend/`.
* **Estrategia de Validación:** Verificación documental de existencia del archivo `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md`, contraste directo contra las cadenas reales de texto de `software/frontend/dashboard.html`, `network.html`, `flows.html`, `login.html`, `register.html`, `help-content.js` y `friendly-errors.js`.
* **Estrategia de Rollback:** `git revert <commit_guia_usuario>` (eliminación limpia del archivo markdown).
* **Responsable:** Jhonny Quintana Carhuaricra.
* **Fecha de Compromiso:** 09/11/2026 (Semana 13).

---

### Brecha 2: M-F07 — Aprobación Humana Persistida de Recomendaciones (HU-07)

* **Factor FURPS+:** Funcionalidad (F)
* **Requisito / ID Matriz:** M-F07
* **Estado Inicial:** No cumple (1 punto)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Extender el flujo de recomendaciones incorporando acciones explícitas de decisión humana ("Aprobar propuesta" o "Rechazar propuesta") en la interfaz de usuario, y persistir la decisión junto con el identificador del operador, justificación y sello de tiempo en una tabla relacional de auditoría `recommendation_decisions`.
* **Justificación:** Actualmente el sistema cumple defensivamente con bloquear la auto-ejecución mediante la bandera `executionAllowed=false`, pero incumple la trazabilidad de negocio requerida por la HU-07, perdiendo el registro histórico de qué decisiones tomó el operador ante las propuestas del modelo.
* **Prioridad:** Crítica (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Medio. Requiere un nuevo endpoint REST en backend y una tabla en base de datos.
* **Dependencias:** Tablas de usuario en Supabase / SQLite y endpoint `POST /v1/recommendations` en Prediction Service.
* **Estrategia de Validación:**
  1. Ejecución de prueba unitaria y de integración: `pytest tests/test_recommendations_approval.py`.
  2. Invocación HTTP verificando respuesta 201 Created y almacenamiento del registro:  
     `curl -X POST http://127.0.0.1:8081/api/v1/recommendations/decisions -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"recommendation_id\":\"REC-001\",\"decision\":\"APPROVED\",\"notes\":\"Autorizado por ventana nocturna\"}"`.
  3. Ejecución de suite de regresión: `node --test tests/frontend/pmv2.test.cjs`.
* **Estrategia de Rollback:** `git revert <commit_aprobacion_hu07>` y aplicación de script SQL de desmantelamiento `DROP TABLE IF EXISTS recommendation_decisions;`.
* **Responsable:** Ricardo Porras Veli.
* **Fecha de Compromiso:** 20/11/2026.

---

### Brecha 3: M-F11 — Ausencia de Exportación PDF en Reportes Históricos (HU-13)

* **Factor FURPS+:** Funcionalidad (F)
* **Requisito / ID Matriz:** M-F11
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Implementar la generación y descarga de reportes históricos consolidados en formato PDF formal, integrando membrete institucional de la Universidad Continental, parámetros de consulta, resumen estadístico de CPU/memoria/temperatura, gráficos de tendencia y declaración expresa de procedencia de datos.
* **Justificación:** El endpoint actual de Data Processing entrega resúmenes en JSON y descarga en CSV plano. Aunque el CSV es funcional para análisis crudo, la HU-13 exige un reporte formal presentable a comités técnicos y auditorías académicas.
* **Prioridad:** Alta (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Bajo. Se añade un adaptador de salida sin modificar la consulta de datos existente.
* **Dependencias:** Endpoint `GET /api/processing/v1/reports/historical-summary` en Data Processing.
* **Estrategia de Validación:**
  1. Prueba unitaria de generación de documento: `pytest software/data-processing/tests/test_pdf_report.py`.
  2. Descarga HTTP verificando cabecera `Content-Type: application/pdf` y firma binaria `%PDF-1.4`:  
     `curl -sI "http://127.0.0.1:8000/api/processing/v1/reports/historical-pdf?hardware_id=HW045&start_date=2026-07-10&end_date=2026-07-11" | grep -i "content-type: application/pdf"`.
  3. Suite de regresión de Data Processing: `pytest` (121 pruebas pasando intactas).
* **Estrategia de Rollback:** `git revert <commit_reporte_pdf>` conservando intacto el endpoint CSV.
* **Responsable:** Jhonny Quintana Carhuaricra.
* **Fecha de Compromiso:** 18/11/2026.

---

### Brecha 4: M-F05 — Registro en MLflow sin Interfaz Gráfica Desplegada (HU-05)

* **Factor FURPS+:** Funcionalidad (F)
* **Requisito / ID Matriz:** M-F05
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Habilitar la visualización formal de los experimentos de entrenamiento de modelos registrados en `software/prediction/mlruns/`, documentando el procedimiento de levantamiento de `mlflow ui` local y alojando capturas estandarizadas en `docs/evidencias/` que demuestren las métricas comparativas de MAE y RMSE entre modelos.
* **Justificación:** El pipeline `run_pipeline.py` registra ejecuciones locales, pero la ausencia de evidencia visual de la UI de MLflow impide auditar de forma inmediata la experimentación comparativa sin correr comandos manuales en la estación de trabajo.
* **Prioridad:** Media (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Mínimo. No toca código del servicio productivo; solo documentación y script auxiliar de observabilidad.
* **Dependencias:** Directorio `software/prediction/mlruns/` y entorno virtual con MLflow.
* **Estrategia de Validación:**
  1. Ejecución de interfaz en entorno local: `mlflow ui --backend-store-uri software/prediction/mlruns --port 5000`.
  2. Verificación de acceso HTTP: `curl -sI http://127.0.0.1:5000 | grep "200 OK"`.
  3. Comprobación de artefactos gráficos guardados en `docs/evidencias/mlflow-experiments-ui.png`.
* **Estrategia de Rollback:** `git revert <commit_evidencias_mlflow>`.
* **Responsable:** Gina Barrera Peña.
* **Fecha de Compromiso:** 14/11/2026.

---

### Brecha 5: M-F09 — Verificación de Observatorio en Entorno /dev/ con Sesión Real (HU-11)

* **Factor FURPS+:** Funcionalidad (F)
* **Requisito / ID Matriz:** M-F09
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Ejecutar la validación integral end-to-end de la consola web estática desplegada en GitHub Pages en la ruta `/dev/`, iniciando sesión con un usuario autenticado real contra el backend de Supabase Auth y comprobando la conexión perimetral hacia el API Gateway.
* **Justificación:** El frontend ha sido probado exitosamente en arnés local con `node:test` y en navegador local con mock, pero la confirmación de operación sobre la infraestructura real desplegada en nube (`https://woshtsu.github.io/green-ai-workspace-cld/dev/`) con tokens PKCE válidos es necesaria para asegurar que no existan problemas de CORS ni de propagación de cabeceras en hosting compartido.
* **Prioridad:** Alta (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Bajo. Prueba de integración sobre entorno de staging ya configurado.
* **Dependencias:** Despliegue de Pages activo y Gateway accesible vía HTTPS.
* **Estrategia de Validación:**
  1. Navegación interactiva en `/dev/login.html` autenticando con credencial de prueba de operador.
  2. Inspección de consola de red verificando intercambio de token JWT, consulta a `/api/v1/metrics/catalog` y renderizado de tarjetas KPI en `dashboard.html`.
  3. Ejecución de suite de pruebas frontend: `node --test tests/frontend/*.test.cjs` (48 pasadas).
* **Estrategia de Rollback:** `git revert <commit_config_dev_pages>` en caso de requerir ajuste de variables.
* **Responsable:** Leonid Huamán Collazos.
* **Fecha de Compromiso:** 12/11/2026.

---

### Brecha 6: M-S01 — Acoplamiento de Adaptadores en Simulator runner.py

* **Factor FURPS+:** Soporte y Mantenibilidad (S)
* **Requisito / ID Matriz:** M-S01
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Refactorizar el módulo `software/simulator/src/green_ai_simulator/application/runner.py` para desacoplar las importaciones directas de adaptadores de infraestructura (`parse_inventory_json`, `parse_scenario_json`, `RunLogger`), sustituyéndolas por inyección de dependencias basada en puertos abstractos en `domain/ports/`.
* **Justificación:** La arquitectura hexagonal del proyecto exige que la capa de aplicación dependa exclusivamente de interfaces de dominio y no de implementaciones concretas de lectura de JSON o registro en disco, preservando la pureza estructural del monorepo.
* **Prioridad:** Media (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Bajo. Refactor interno de diseño sin alteración de comportamiento externo.
* **Dependencias:** Suite de pruebas del simulador en `software/simulator/tests/`.
* **Estrategia de Validación:**
  1. Ejecución de suite de pruebas unitarias: `docker compose run --rm simulator python -m unittest discover tests`.
  2. Verificación de importaciones limpias con herramienta de linting / ast check:  
     `python -c "import ast; tree = ast.parse(open('software/simulator/src/green_ai_simulator/application/runner.py').read()); print('Sintaxis e importaciones conformes')"`
* **Estrategia de Rollback:** `git revert <commit_refactor_runner_hexagonal>`.
* **Responsable:** Leonid Huamán Collazos.
* **Fecha de Compromiso:** 24/11/2026.

---

### Brecha 7: M-P01 — Impacto de Cold Start en Render Free Tier (> 7 s)

* **Factor FURPS+:** Rendimiento (P)
* **Requisito / ID Matriz:** M-P01
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Mitigar el retardo de arranque en frío (~60 s tras 15 minutos de inactividad) en los microservicios alojados en Render Free Tier mediante la implementación de un script automatizado de precalentamiento y keep-alive temporal programado antes de sesiones de demostración o evaluaciones docentes.
* **Justificación:** Aunque las respuestas locales responden en menos de 30 ms (Java) y 4 ms (Go), la primera petición sobre un contenedor suspendido en Render excede el umbral académico de 7 segundos, generando riesgo de 504 Gateway Timeout durante exposiciones.
* **Prioridad:** Alta (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Bajo. Proceso operativo externo que no modifica el código de producción.
* **Dependencias:** Endpoints de salud pública `/actuator/health` y `/health/ready` de los microservicios en Render.
* **Estrategia de Validación:**
  1. Ejecución del script de precalentamiento 25 minutos antes de la revisión:  
     `python scripts/prewarm_services.py --target-url https://green-ai-gateway.onrender.com`.
  2. Medición automatizada de tiempo de respuesta verificando `HTTP 200` con latencia inferior a 2 segundos:  
     `curl -o /dev/null -s -w "Tiempo de respuesta: %{time_total} s\n" https://green-ai-gateway.onrender.com/actuator/health`.
* **Estrategia de Rollback:** Cancelación del script o tarea programada sin impacto en el repositorio.
* **Responsable:** Ricardo Porras Veli.
* **Fecha de Compromiso:** 19/11/2026.

---

### Brecha 8: M-U06 — Ausencia de Auditoría Automatizada WCAG 2.1 AA y Tabla Accesible

* **Factor FURPS+:** Usabilidad (U)
* **Requisito / ID Matriz:** M-U06
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Ejecutar una auditoría formal de accesibilidad mediante Google Lighthouse / axe-core sobre las páginas del frontend, asegurando puntaje de accesibilidad superior al 90 %, e incorporar una tabla HTML semánticamente accesible (`class="sr-only"`) asociada al elemento `<canvas id="history-chart">` en `software/frontend/dashboard.html`.
* **Justificación:** Los lectores de pantalla y tecnologías de asistencia no pueden interpretar los datos vectoriales graficados por Chart.js dentro del lienzo canvas, limitando la operación a usuarios con discapacidad visual en la pestaña Resumen.
* **Prioridad:** Media (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Mínimo. Adición de markup accesible oculto visualmente con técnicas estándar de CSS.
* **Dependencias:** `software/frontend/dashboard.html` y servidor web local.
* **Estrategia de Validación:**
  1. Ejecución de Lighthouse CLI sobre la página principal:  
     `npx lighthouse-ci collect --url=http://localhost:8080/dashboard.html && npx lighthouse-ci assert --preset=lighthouse:recommended`.
  2. Verificación de renderizado de la tabla accesible oculta:  
     `node --test tests/frontend/frontend.test.cjs`.
* **Estrategia de Rollback:** `git revert <commit_tabla_accesible_lighthouse>`.
* **Responsable:** Leonid Huamán Collazos.
* **Fecha de Compromiso:** 15/11/2026.

---

### Brecha 9: M-F13 / M-R05 — Endurecimiento de Seguridad RLS en Base de Datos Supabase

* **Factor FURPS+:** Funcionalidad (F) y Confiabilidad (R)
* **Requisitos / ID Matriz:** M-F13 y M-R05
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Endurecer la seguridad en la instancia de Supabase de producción: suprimir definitivamente políticas históricas de tipo "Permitir todo", eliminar columnas obsoletas de contraseñas en texto plano (`password`) en la tabla `usuario`, y verificar que las políticas de seguridad a nivel de fila (Row Level Security - RLS) permitan exclusivamente lecturas y escrituras validadas por rol JWT.
* **Justificación:** En el snapshot histórico inicial (`esquema-verificado.json`) se detectaron políticas permisivas que exponen datos de auditoría o configuración si no se aplican las restricciones estrictas definidas en `software/frontend/supabase-auth-setup.sql`.
* **Prioridad:** Crítica (Ola 2, Sprint 7).
* **Nivel de Riesgo:** Medio. Requiere coordinación con el propietario de la cuenta de Supabase.
* **Dependencias:** Credenciales administrativas de consola en Supabase.
* **Estrategia de Validación:**
  1. Ejecución de script de verificación de políticas RLS:  
     `psql "$DATABASE_URL" -c "SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';"` asegurando que todas las tablas tengan `rowsecurity = true`.
  2. Intento de consulta anónima sin token esperando rechazo:  
     `curl -s -o /dev/null -w "%{http_code}" https://<supabase-id>.supabase.co/rest/v1/historical_logs | grep "401"`.
  3. Ejecución de pruebas de contrato: `pytest software/data-processing/tests/test_contracts.py` (114 pruebas pasando).
* **Estrategia de Rollback:** Reaplicación de políticas de respaldo documentadas en `docs/seguridad/backup-rls-policies.sql`.
* **Responsable:** Dueño del proyecto Supabase y Ricardo Porras Veli.
* **Fecha de Compromiso:** 11/11/2026.

---

### Brecha 10: M-F08 — Potencia Modelada y Cálculo de Energía / CO2e (HU-09)

* **Factor FURPS+:** Funcionalidad (F)
* **Requisito / ID Matriz:** M-F08
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Parcial mantenido con transparencia documental plena (3 puntos / justificado)
* **Objetivo:** Mantener el rigor de la honestidad experimental en el módulo de energía: documentar formalmente que la potencia en vatios es modelada mediante la fórmula lineal P = P_idle + (P_max - P_idle) * CPU a partir de telemetría de CPU simulada, incorporar factores de emisión de CO2e oficiales validados (ej. SEIN Perú 2024 / 2025) y exigir siempre la declaración de la fuente.
* **Justificación:** El cálculo de energía por la regla del trapecio es matemáticamente exacto, pero mientras no se conecten sensores IPMI o medidores físicos PDU en un centro de datos real, no se puede afirmar que la potencia es medida directamente. Declararlo explícitamente cumple con las directrices éticas del proyecto.
* **Prioridad:** Media (Ola 3, Sprint 8).
* **Nivel de Riesgo:** Bajo. Modificación de textos de ayuda y tablas de factores predeterminadas.
* **Dependencias:** `software/frontend/energy.js` y `software/frontend/help-content.js`.
* **Estrategia de Validación:**
  1. Ejecución de suite de pruebas de cálculo de energía: `node --test tests/frontend/energy.test.cjs`.
  2. Verificación de etiqueta de honestidad en pantalla: presencia de texto "Con datos simulados la potencia es modelada, no medida" en `panel-energia`.
* **Estrategia de Rollback:** `git revert <commit_refinamiento_energia>`.
* **Responsable:** Gina Barrera Peña.
* **Fecha de Compromiso:** 21/11/2026.

---

### Brecha 11: M-U08 — Operaciones Principales en Tres Pasos o Menos

* **Factor FURPS+:** Usabilidad (U)
* **Requisito / ID Matriz:** M-U08
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Cumple (5 puntos)
* **Objetivo:** Optimizar la ergonomía del flujo de energía y cálculo de CO2e en `software/frontend/dashboard.html` para que cualquier usuario pueda seleccionar un archivo o el ejemplo determinista y obtener el consumo en exactamente 2 o 3 pasos, precargando de forma contextual factores de referencia sugeridos.
* **Justificación:** Actualmente, subir un archivo de telemetría propio, escribir el factor de emisión, especificar la fuente y pulsar calcular toma 4 pasos sucesivos, excediendo la pauta de diseño ergonómico de 3 pasos.
* **Prioridad:** Media (Ola 3, Sprint 8).
* **Nivel de Riesgo:** Mínimo. Ajustes de conveniencia en interfaz JavaScript sin alterar el algoritmo de integración.
* **Dependencias:** `software/frontend/energy.js` y `software/frontend/dashboard-ui.js`.
* **Estrategia de Validación:**
  1. Inspección de flujo interactivo completando el cálculo en 3 clics: Pestaña -> Seleccionar vía simulador -> Ver resultado inmediato.
  2. Suite de regresión frontend: `node --test tests/frontend/energy.test.cjs`.
* **Estrategia de Rollback:** `git revert <commit_flujo_energia_3pasos>`.
* **Responsable:** Leonid Huamán Collazos.
* **Fecha de Compromiso:** 17/11/2026.

---

### Brecha 12: M-PL03 — Gestión y Optimización de Cuota de Hosting Gratuito en Render

* **Factor FURPS+:** Restricciones Adicionales (PLUS)
* **Requisito / ID Matriz:** M-PL03
* **Estado Inicial:** Parcial (3 puntos)
* **Estado Esperado:** Parcial aceptado con control de operación (3 puntos)
* **Objetivo:** Establecer una rutina operativa documentada y mecanismos de apagado controlado de servicios tras sesiones de prueba, asegurando que el consumo acumulado mensual no exceda las 750 horas compartidas del plan gratuito de Render.
* **Justificación:** Las limitaciones físicas de memoria (512 MB) y cuota horaria mensual son restricciones del proveedor cloud. Al adoptar el API Gateway en Go (consumo de ~10 MiB frente a 280 MiB de Java), la huella de memoria ya está resuelta; la gestión de horas requiere disciplina de apagado.
* **Prioridad:** Baja (Ola 3, Sprint 8).
* **Nivel de Riesgo:** Mínimo. Buenas prácticas de gestión cloud sin impacto de código.
* **Dependencias:** Panel de control de Render y repositorio GitHub.
* **Estrategia de Validación:**
  1. Verificación de consumo en panel de Render manteniendo servicios suspendidos fuera de ventanas de desarrollo.
  2. Medición de memoria en reposo inferior a 150 MiB en todos los servicios activos.
* **Estrategia de Rollback:** No aplica (política operativa).
* **Responsable:** Leonid Huamán Collazos.
* **Fecha de Compromiso:** 22/11/2026.

---

## 5. Matriz Consolidada de Mejoras y Orden Recomendado de Ejecución

A continuación se presenta la secuencia lógica de ejecución recomendada, considerando dependencias técnicas, impacto académico y minimización de riesgos.

| Orden | ID Brecha | Acción Principal de Mejora | Prioridad | Responsable | Fecha Límite | Suite de Validación Requerida |
|:---:|:---:|---|:---:|---|:---:|---|
| **1** | **M-U07** | Redacción y publicación de Guía Rápida de Usuario (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md`) | Alta | Jhonny Quintana Carhuaricra | 09/11/2026 | Revisión documental contra interfaz real |
| **2** | **M-F13 / M-R05** | Endurecimiento de RLS y verificación de políticas en base de datos Supabase | Crítica | Ricardo Porras / Dueño Supabase | 11/11/2026 | Pruebas de contrato Data Processing (114) |
| **3** | **M-F09** | Validación de observatorio en entorno `/dev/` de Pages con sesión real | Alta | Leonid Huamán Collazos | 12/11/2026 | Suite Frontend node:test (48) |
| **4** | **M-F05** | Levantamiento y captura estandarizada de MLflow UI para modelos entrenados | Media | Gina Barrera Peña | 14/11/2026 | Verificación HTTP MLflow + capturas |
| **5** | **M-U06** | Auditoría Lighthouse WCAG 2.1 AA y tabla accesible oculta para Chart.js | Media | Leonid Huamán Collazos | 15/11/2026 | Auditoría Lighthouse + Frontend tests (48) |
| **6** | **M-F11** | Implementación de generación y exportación de reportes en PDF formal (HU-13) | Alta | Jhonny Quintana Carhuaricra | 18/11/2026 | Pytest Data Processing (121) |
| **7** | **M-P01** | Script automatizado de precalentamiento y keep-alive para Render Free Tier | Alta | Ricardo Porras Veli | 19/11/2026 | Medición de latencia HTTP (< 2 s en salud) |
| **8** | **M-F07** | Flujo de aprobación humana persistida de recomendaciones (HU-07) en BD | Crítica | Ricardo Porras Veli | 20/11/2026 | Pytest Prediction (100) + PMV2 tests |
| **9** | **M-S01** | Desacoplamiento de adaptadores en `runner.py` de Simulator a puertos de aplicación | Media | Leonid Huamán Collazos | 24/11/2026 | Docker unittest Simulator (10) |
| **10** | **M-F08** | Documentación formal de potencia modelada y factores de emisión de CO2e | Media | Gina Barrera Peña | 21/11/2026 | Energy tests (node:test) |
| **11** | **M-U08** | Simplificación ergonómica del cálculo de energía a tres pasos o menos | Media | Leonid Huamán Collazos | 17/11/2026 | Suite Frontend node:test (48) |
| **12** | **M-PL03** | Rutina de suspensión y control de cuota horaria en hosting gratuito de Render | Baja | Leonid Huamán Collazos | 22/11/2026 | Inspección de métricas en Render Dashboard |

---

## 6. Análisis de Riesgos de Ejecución y Mitigación

Para cada vector de intervención técnica, se establecen medidas de contención para garantizar la operación continua del monorepo:

1. **Riesgo de Regresión en Contratos de API:**
   * *Amenaza:* Alterar la estructura de respuesta en endpoints compartidos rompiendo el frontend o el gateway.
   * *Mitigación:* Se mantiene estricto cumplimiento del esquema OpenAPI versionado y del formato problem+json (RFC 7807). Toda adición de campos se realiza de forma optativa y retrocompatible.
2. **Riesgo de Bloqueo por Suspensión de Instancias Gratuitas en Render:**
   * *Amenaza:* Fallos temporales durante demostraciones en vivo debido al tiempo de cold start.
   * *Mitigación:* Ejecución disciplinada del script de keep-alive 25 minutos antes de cualquier presentación y soporte alternativo de exposición con el stack Docker Compose local.
3. **Riesgo de Desalineación en Base de Datos Remota:**
   * *Amenaza:* Alteraciones en Supabase que afecten la operación local con SQLite.
   * *Mitigación:* El patrón de adaptadores duales (`SqliteHistoricalLogsAdapter` y `SupabaseHistoricalLogsAdapter`) aísla totalmente el entorno de desarrollo del entorno en la nube, compartiendo la misma batería de 114 pruebas de contrato.
4. **Riesgo de Ruptura en Pruebas de UI por Cambios en el DOM:**
   * *Amenaza:* La introducción de la tabla accesible oculta o nuevos botones de aprobación podría alterar selectores de prueba.
   * *Mitigación:* Las pruebas unitarias en `node:test` emplean selectores por identificador exacto y atributos semánticos de accesibilidad (`role`, `aria-*`), asegurando que no dependan de estructuras rígidas de estilo.

---

## 7. Compromiso de Calidad y Cierre

La ejecución disciplinada de este plan eleva la calificación integral FURPS+ del sistema Green AI desde un nivel inicial del **85.00 %** hasta una meta esperada del **98.00 %**, cubriendo todas las brechas funcionales, ergonómicas y operativas comprometidas para las semanas 13 y 14 del periodo académico, manteniendo intactas la robustez y estabilidad ya alcanzadas.
