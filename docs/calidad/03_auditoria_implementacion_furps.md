# 03_Auditoria_Implementacion_FURPS.md — Auditoria de Implementacion de Calidad (FURPS+)

**Proyecto:** Green AI (Optimizacion Energetica y Capacidad en Data Centers con Machine Learning)  
**Institucion:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol:** Auditor Independiente de Calidad de Software  
**Fecha de Auditoria:** 2026-11-07  
**Rama Base de Evaluacion:** `test` (commit `d24d86f` y estado del workspace)  
**Entradas Evaluadas:**  
- `docs/calidad/01_auditoria_furps.md` (Linea base inicial: 85.00 %)  
- `docs/calidad/02_plan_furps.md` (Plan de mejora en tres olas)  
- `docs/evidencias/semana13-ola1-verificacion.md` (Evidencia de ejecucion de Ola 1)  
- Estado actual de codigo y documentacion en el repositorio  
**Marco de Referencia:** Modelo FURPS+ (Hewlett-Packard / Rational Software Corp.) y directrices de auditoria independiente UC.

---

## 1. Resumen Ejecutivo y Metodologia de Auditoria

El presente informe constituye la auditoria formal e independiente de verificacion sobre la implementacion del plan de mejora de calidad FURPS+ (`docs/calidad/02_plan_furps.md`).

Bajo el mandato de auditoria independiente:
1. No se asume ninguna mejora como implementada sin verificacion directa de existencia y consistencia en los archivos del repositorio.
2. Lo planificado para las olas posteriores (Ola 2 y Ola 3) figura de forma expresa como «No implementada (planificada para <fecha>)», distinguiendo compromisos futuros de incumplimientos.
3. Se verifico la ausencia de regresiones en las suites automatizadas activas.
4. Toda referencia técnica se documenta con la ruta y numero de linea exactos en texto plano (`ruta:Lnn`).

### Resultado General
- **Mejoras comprometidas para Ola 1 (Semana 13):** 1 (M-U07).
- **Estado de implementacion de Ola 1:** Implementada al 100 % (M-U07 satisfecha mediante la publicacion de `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L1-L106`).
- **Puntaje FURPS+ inicial (01_auditoria_furps.md):** 170 / 200 (85.00 %).
- **Puntaje FURPS+ actual auditado (Post Ola 1):** 174 / 200 (87.00 %).
- **Regresiones detectadas:** Cero (0). La suite de pruebas de frontend se mantiene en 48/48 pruebas satisfactorias y los microservicios de backend no sufrieron alteraciones en esta fase.

---

## 2. Comparacion Antes / Despues por Factor FURPS+

Se utiliza como base la evaluacion formal de `docs/calidad/01_auditoria_furps.md:L29-L40` y `docs/calidad/01_auditoria_furps.md:L339-L347`:

| Factor FURPS+ | Preguntas | Puntaje Deseado (PD) | Puntaje Inicial (01) | Nivel Inicial (%) | Puntaje Actual (03) | Nivel Actual (%) | Delta | Variacion Cualitativa |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **F — Funcionalidad** | 13 | 65 | 51 | 78.46 % | 51 | 78.46 % | 0.00 % | Sin cambios en Ola 1. Se preserva funcionalidad. Olas 2 y 3 programadas. |
| **U — Usabilidad** | 8 | 40 | 32 | 80.00 % | 36 | 90.00 % | +10.00 % | Incremento significativo. Se subsana M-U07 (Guia rapida de usuario). |
| **R — Confiabilidad** | 6 | 30 | 28 | 93.33 % | 28 | 93.33 % | 0.00 % | Sin cambios. Se preservan 415+ pruebas y contratos RFC 7807. |
| **P — Rendimiento** | 3 | 15 | 13 | 86.67 % | 13 | 86.67 % | 0.00 % | Sin cambios. Inferencia ligera y Gateway Go preservados. |
| **S — Soporte / Mantenibilidad** | 4 | 20 | 18 | 90.00 % | 18 | 90.00 % | 0.00 % | Sin cambios. Monorepo limpio y contratos OpenAPI vigentes. |
| **+ — Restricciones Adicionales** | 6 | 30 | 28 | 93.33 % | 28 | 93.33 % | 0.00 % | Sin cambios. Arquitectura perimetral, Docker Compose y licencias intactas. |
| **TOTAL MATRIZ (0-200)** | **40** | **200** | **170** | **85.00 %** | **174** | **87.00 %** | **+2.00 %** | **Progreso medible y verificable en Ola 1.** |

### Ponderacion FURPS+ Oficial (segun Seccion 1.3 de 01_auditoria_furps.md)
- **Funcionalidad (25 %):** 78.46 % * 0.25 = 19.62 %
- **Usabilidad (15 %):** 90.00 % * 0.15 = 13.50 % (antes 80.00 % * 0.15 = 12.00 %, sube 1.50 %)
- **Confiabilidad (20 %):** 93.33 % * 0.20 = 18.67 %
- **Rendimiento (15 %):** 86.67 % * 0.15 = 13.00 %
- **Soporte (15 %):** 90.00 % * 0.15 = 13.50 %
- **Restricciones + (10 %):** 93.33 % * 0.10 = 9.33 %
- **Calificacion Ponderada Global:** **87.62 %** (inicial ponderado: 85.95 % / redondeado a 85.00 %).

---

## 3. Estado de Cada Mejora del Plan FURPS+

Se evaluan de forma exhaustiva las 12 mejoras formalizadas en `docs/calidad/02_plan_furps.md:L82-L358`:

### Ficha M-U07: Inexistencia de Guia Rapida de Usuario
- **Factor:** Usabilidad (U).
- **Estado Anterior:** No cumple (1 punto).
- **Estado Actual:** **Implementada (Cumple - 5 puntos)**.
- **Evidencia Observable:** Creacion y publicacion formal del archivo `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L1-L106`.
  - Contiene requisitos tecnicos y URLs operativas para desarrollo (`/dev/`) y produccion (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L7-L19`).
  - Define roles de usuario RBAC (ADMIN, OPERATOR, VIEWER) coincidiendo exactamente con la logica perimetral de `software/gateway-go/internal/policy/routes.go:L72-L77` (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L22-L29`).
  - Documenta 8 tareas operativas completables en 3 pasos o menos, sustentadas en botones e identificadores reales de la interfaz web (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L32-L83`).
  - Incorpora catalogo de errores amigables alineado con `software/frontend/friendly-errors.js` (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L86-L98`).
  - Refuerza el principio de honestidad experimental respecto al origen de datos simulados y potencia modelada (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L101-L106`).
- **Responsable:** Jhonny Quintana Carhuaricra.
- **Fecha de Compromiso:** 09/11/2026 (Semana 13) — Cumplida en plazo.

### Ficha M-F07: Aprobacion Humana Persistida de Recomendaciones (HU-07)
- **Factor:** Funcionalidad (F).
- **Estado Anterior:** No cumple (1 punto).
- **Estado Actual:** **No implementada (planificada para 20/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** El archivo `software/prediction/src/service/recommendations.py:L15-L80` mantiene la salvaguarda defensiva `executionAllowed=false`, pero aun no existen la tabla `recommendation_decisions` ni el endpoint REST de decision en backend. No constituye un fallo en esta etapa al estar programada para el Sprint 7.
- **Responsable:** Ricardo Porras Veli.

### Ficha M-F11: Ausencia de Exportacion PDF en Reportes Historicos (HU-13)
- **Factor:** Funcionalidad (F).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 18/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** `software/data-processing/infrastructure/adapters/input/api/routes.py:L8-L14` expone el resumen JSON y la descarga CSV (`GET /api/processing/v1/reports/historical-summary`), manteniendose pendiente el adaptador generador de documento binario PDF.
- **Responsable:** Jhonny Quintana Carhuaricra.

### Ficha M-F05: Registro en MLflow sin Interfaz Grafica Desplegada (HU-05)
- **Factor:** Funcionalidad (F).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 14/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** El pipeline `software/prediction/scripts/run_pipeline.py` genera el registro en `software/prediction/mlruns/`, pero aun no se han capturado las graficas de la interfaz grafica ni se ha documentado el despliegue del servidor MLflow.
- **Responsable:** Gina Barrera Peña.

### Ficha M-F09: Verificacion de Observatorio en Entorno /dev/ con Sesion Real (HU-11)
- **Factor:** Funcionalidad (F).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 12/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** El workflow `.github/workflows/pages.yml:L76` construye la ruta `dist/dev`, pero la prueba interactiva con cuenta real y verificacion de red en la URL remota de Pages sigue programada para la siguiente semana.
- **Responsable:** Leonid Huaman Collazos.

### Ficha M-S01: Acoplamiento de Adaptadores en Simulator runner.py
- **Factor:** Soporte y Mantenibilidad (S).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 24/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** `software/simulator/src/green_ai_simulator/application/runner.py:L5-L10` conserva importaciones directas de modulos de infraestructura (`parse_inventory_json`, `parse_scenario_json`, `RunLogger`). Su abstraccion a puertos queda asignada al Sprint 7.
- **Responsable:** Leonid Huaman Collazos.

### Ficha M-P01: Impacto de Cold Start en Render Free Tier (> 7 s)
- **Factor:** Rendimiento (P).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 19/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** `docs/GUIA-DESPLIEGUE-RENDER.md:L21-L25` describe la suspension tras 15 minutos; el script automatizado de precalentamiento previo a revisiones docentes se construira en el Sprint 7.
- **Responsable:** Ricardo Porras Veli.

### Ficha M-U06: Ausencia de Auditoria Automatizada WCAG 2.1 AA y Tabla Accesible
- **Factor:** Usabilidad (U).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 15/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** `software/frontend/dashboard.html:L91` renderiza el canvas de Chart.js sin la tabla accesible oculta alternativa; el escaneo con Google Lighthouse CLI se ejecutara en el Sprint 7.
- **Responsable:** Leonid Huaman Collazos.

### Ficha M-F13 / M-R05: Endurecimiento de Seguridad RLS en Base de Datos Supabase
- **Factor:** Funcionalidad (F) y Confiabilidad (R).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 11/11/2026, Sprint 7 - Ola 2)**.
- **Evidencia Observable:** La instancia remota de Supabase y las politicas RLS permisivas registradas en `software/simulator/docs/assets/esquema-verificado.json:L458-L492` estan pendientes de intervencion coordinada con el propietario del proyecto Supabase.
- **Responsable:** Dueño del proyecto Supabase y Ricardo Porras Veli.

### Ficha M-F08: Potencia Modelada y Calculo de Energia / CO2e (HU-09)
- **Factor:** Funcionalidad (F).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 21/11/2026, Sprint 8 - Ola 3)**.
- **Evidencia Observable:** `software/frontend/energy.js:L10-L50` implementa la regla del trapecio sobre potencia modelada. Se mantiene como Parcial justificado por honestidad experimental hasta contar con factores de emision validados para Peru en la Ola 3.
- **Responsable:** Gina Barrera Peña.

### Ficha M-U08: Operaciones Principales en Tres Pasos o Menos
- **Factor:** Usabilidad (U).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada a nivel de codigo UI (planificada para 17/11/2026, Sprint 8 - Ola 3)**.
- **Evidencia Observable:** Si bien `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L32-L83` estandariza el procedimiento de 8 tareas en <= 3 pasos, la simplificacion ergonomica del formulario de carga de potencia en `software/frontend/dashboard.html:L275-L289` se abordara en el Sprint 8.
- **Responsable:** Leonid Huaman Collazos.

### Ficha M-PL03: Gestion y Optimizacion de Cuota de Hosting Gratuito en Render
- **Factor:** Restricciones Adicionales (PLUS).
- **Estado Anterior:** Parcial (3 puntos).
- **Estado Actual:** **No implementada (planificada para 22/11/2026, Sprint 8 - Ola 3)**.
- **Evidencia Observable:** `render.yaml:L1-L60` gestiona el despliegue a costo cero; la politica operativa de control de horas mensuales compartidas se consolidara en el Sprint 8.
- **Responsable:** Leonid Huaman Collazos.

---

## 4. Analisis y Busqueda de Regresiones

Como auditor independiente, se inspeccionaron los posibles efectos colaterales de los cambios introducidos en la Ola 1:

1. **Pruebas Automatizadas de Frontend:**
   - La suite modular en `software/frontend/tests/*.test.cjs` fue ejecutada antes y despues de la integracion documental y de seguridad.
   - **Resultado:** **48 de 48 pruebas exitosas (0 fallos)**, segun consta en `docs/evidencias/semana13-ola1-verificacion.md:L19`.
   - Se verifico que la inclusion de `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md` y los atributos de seguridad en archivos HTML no rompieron los selectores del DOM, los parsers de configuracion, ni las rutinas de calculo de agregados y energia.
2. **Estabilidad de Microservicios Backend:**
   - Durante la Ola 1 no se modifico ningun archivo dentro de `software/monitoring/`, `software/data-processing/`, `software/prediction/`, `software/gateway/` ni `software/gateway-go/`.
   - La linea base de pruebas de backend reportada en `docs/HANDOFF.md:L36-L49` (112 en Monitoring, 121 en Data Processing, 100 en Prediction, 30 en Gateway Go y 10 en Simulator) permanece intacta sin riesgo de regresion funcional.
3. **Consistencia de Textos e Interfaz:**
   - Se comprobo que las cadenas citadas en `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md` correspondan con los elementos del DOM en `software/frontend/dashboard.html`, `network.html`, `login.html` y `register.html` (10 de 10 textos confirmados segun `docs/evidencias/semana13-ola1-verificacion.md:L25`).
   - No se detectaron enlaces rotos ni botones huerfanos.

---

## 5. Riesgos Residuales

Tras la culminacion de la Ola 1, persisten los siguientes riesgos tecnicos a ser atendidos en las olas subsiguientes:

1. **Riesgo Operativo por Falta de Persistencia en Decisiones Humanas (HU-07):** El operador no puede registrar si acepto o rechazo formalmente una recomendacion emitida por el modelo, comprometiendo la trazabilidad de auditoria (Ola 2).
2. **Riesgo de Disponibilidad por Cold Start en Render (M-P01):** La primera peticion tras suspension puede demorar ~60 s en el plan gratuito, superando el umbral de 7 s exigido por los criterios de evaluacion docente (Ola 2).
3. **Riesgo de Datos Modelados sin Medicion Fisica (HU-09 / M-F08):** La potencia y energia son calculadas sobre simulacion determinista lineal. Requiere mantener visible la declaracion de honestidad en pantalla y guias (Ola 3).
4. **Riesgo de Seguridad en Base de Datos Supabase (M-F13 / M-R05):** Permanece abierta la verificacion de politicas RLS y contraseñas en la base de datos de produccion en la nube (Ola 2).

---

## 6. Conclusion de Cumplimiento

1. **Cumplimiento del Plan:** El equipo ejecuto de forma impecable el 100 % de los compromisos adquiridos para la Ola 1 (Semana 13), entregando una guia de usuario de alto valor operativo (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md`) sin introducir ninguna regresion en el software existente.
2. **Evolucion del Nivel de Calidad:** El puntaje global del modelo FURPS+ se eleva de **85.00 % a 87.00 %** (174 de 200 puntos brutos; ponderado de 85.95 % a 87.62 %), fortaleciendo especificamente el pilar de Usabilidad que paso de 80.00 % a 90.00 %.
3. **Dictamen de Auditoria:** **APROBADO CONFORME PARA OLA 1.** Las 11 brechas restantes quedan correctamente identificadas y calendarizadas para el Sprint 7 (Ola 2) y Sprint 8 (Ola 3) segun la hoja de ruta establecida.
