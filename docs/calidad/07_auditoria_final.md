# 07_Auditoria_Final.md — Dictamen Final Integral de Calidad y Seguridad de Software

> **Nota (2026-11-12):** tras la revisión del equipo, M-R01 pasó a Parcial (Prediction no usa problem+json); FURPS+ queda en 168 → 172 / 200 (84.0 % → 86.0 %; ponderado 84.78 → 86.28). Las cifras de este documento se conservan como registro histórico.

> **Nota (2026-11-12):** este documento usa OWASP Top 10:2021 y se conserva como registro histórico. Bajo OWASP Top 10:2025 el score de seguridad es 83.5/100; la clasificación vigente y los puntajes recalculados están en [08_reclasificacion_owasp_2025.md](08_reclasificacion_owasp_2025.md).

**Proyecto:** Green AI (Optimizacion Energetica y Capacidad en Data Centers con Machine Learning)  
**Institucion:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol:** Auditor Principal de Calidad y Seguridad (Auditor Final Integral)  
**Fecha de Emision:** 2026-11-07  
**Rama Base:** `test` (commit sincronizado `d24d86f` e inspeccion estatica integral)  
**Documentos de Entrada:**  
- `docs/calidad/03_auditoria_implementacion_furps.md` (Auditoria de Implementacion FURPS+)  
- `docs/calidad/06_auditoria_implementacion_owasp.md` (Auditoria de Implementacion OWASP)  
- `docs/evidencias/semana13-ola1-verificacion.md` (Evidencia tecnica consolidada)  
- Estado actual de repositorios, contratos OpenAPI, Dockerfiles y workflows  
**Marco Normativo y Referencial:** Metodologia FURPS+, OWASP Top 10:2021, Ley N° 29733 y Directrices de Evaluacion UC (Semanas 12 y 13).

---

## 1. Resumen Ejecutivo

El presente informe constituye el **dictamen final integral** emitido por el Auditor Principal sobre el estado técnico, funcional, operativo y de seguridad del monorepo `green-ai`. La evaluación sintetiza los hallazgos de las auditorías de implementación de calidad (FURPS+) y seguridad (OWASP Top 10), contrastándolos de manera independiente con el código fuente y las directrices docentes.

El proyecto Green AI exhibe una madurez de ingeniería destacable: arquitectura hexagonal desacoplada en todos sus servicios, perimetro de seguridad gobernado por un API Gateway con validacion JWT rigurosa y soporte RBAC para observadores (rol `VIEWER`), mas de 415 pruebas automatizadas pasando satisfactoriamente, un despliegue estático continuo en GitHub Pages con soporte multi-entorno (`main` en raiz y `test` en `/dev/`) y un backend contenerizado a costo cero sobre Render.

Durante la fase de verificación de la Ola 1 (Semana 13), el equipo subsanó con éxito las brechas de usabilidad documental mediante la publicación de la Guía Rápida de Usuario (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md`), blindó el frontend ante ataques de Clickjacking y alteración de CDNs (cabeceras Nginx y Subresource Integrity), e inmunizó la cadena de suministro en GitHub Actions mediante anclaje por commit SHA inmutable. No obstante, persisten condicionantes estructurales derivadas del alojamiento en capas gratuitas y de la superficie de persistencia externa que delimitan el alcance del dictamen.

---

## 2. Estado de Calidad (Modelo FURPS+)

### Dictamen: **Cumple parcialmente FURPS+**

### Justificación Técnica:
- **Nivel de Calidad Inicial (01_auditoria_furps.md):** 85.00 % (170 / 200 puntos brutos; 85.95 % ponderado).
- **Nivel de Calidad Post Ola 1 (03_auditoria_implementacion_furps.md):** **87.00 %** (174 / 200 puntos brutos; **87.62 %** ponderado).
- **Evolución por factores:**
  - *Funcionalidad (F - 78.46 %):* Cobertura completa de casos de uso centrales (HU-01 telemetría en tiempo real, HU-02 histórico con paginación keyset, HU-03 predicción de CPU a 15 min, HU-04 comparación de modelos, HU-06 recomendaciones y HU-14 RBAC). Brechas pendientes planificadas para Ola 2 y Ola 3: falta de persistencia en aprobación humana (HU-07), reporte PDF formal (HU-13), UI desplegada de MLflow (HU-05) y potencia modelada sin sensores físicos (HU-09).
  - *Usabilidad (U - 90.00 %):* Subió del 80.00 % inicial al 90.00 % gracias a la implementación de `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md` (M-U07), que documenta 8 flujos esenciales en <= 3 pasos basándose en la interfaz real. Pendiente: auditoría formal con Lighthouse y tabla accesible oculta para Chart.js (M-U06).
  - *Confiabilidad (R - 93.33 %):* Estándar RFC 7807 (problem+json) estricto en todos los servicios, sondas de salud (liveness/readiness), timeouts en cascada y 415+ pruebas automatizadas.
  - *Rendimiento (P - 86.67 %):* Latencias locales sobresalientes (Gateway Go con p50 = 3.5 ms e imagen liviana de inferencia reducida en un 82 % a 510 MB). Brecha: arranque en frío (cold start de ~60 s) en Render Free Tier (M-P01).
  - *Soporte y Mantenibilidad (S - 90.00 %):* Monorepo limpio, CI en GitHub Actions y OpenAPI versionado. Brecha: acoplamiento en `runner.py` del Simulator (M-S01).
  - *Restricciones Adicionales (+ - 93.33 %):* Punto de entrada único perimetral, Docker Compose unificado, compatibilidad de licencias Open Source y apego estricto a la Ley N° 29733.
- **Conclusión de Calidad:** Cumple con la base requerida para operación de demostración, manteniendo el compromiso de alcanzar el **98.00 %** con la ejecución de las Olas 2 y 3.

---

## 3. Estado de Seguridad (OWASP Top 10:2021)

### Dictamen: **Cumple parcialmente OWASP Top 10**

### Justificación Técnica:
- **Score Inicial de Seguridad (04_auditoria_owasp.md):** 80.5 / 100.
- **Score Actualizado Auditado (06_auditoria_implementacion_owasp.md):** **85.0 / 100**.
- **Evolución y Controles Implementados en Ola 1:**
  - *A05: Security Misconfiguration (9.0 / 10, +2.0 puntos):* Implementación de cabeceras HTTP defensivas en Nginx (`X-Frame-Options: DENY`, `Permissions-Policy`, `Cross-Origin-Opener-Policy`, `nosniff`, `no-referrer`) en `software/frontend/nginx.conf:L8-L12` (OW-06 parcial) y corrección de anulación de cabeceras en `location = /config.local.js` (OW-07 total).
  - *A06: Vulnerable and Outdated Components (9.5 / 10, +1.5 puntos):* Incorporación de atributos `integrity="sha384-..."` y `crossorigin="anonymous"` en scripts y hojas de estilo de CDN en las 6 páginas HTML del frontend (OW-08 total).
  - *A08: Software and Data Integrity Failures (8.5 / 10, +1.0 punto):* Fijación inmutable del 100 % de las acciones de GitHub Actions mediante SHA de commit de 40 caracteres en `.github/workflows/ci.yml` y `pages.yml` (OW-10 total).
- **Vulnerabilidades Críticas Pendientes (Planificadas para Olas 2 y 3):**
  - Riesgo de políticas RLS permisivas en la base de datos externa de Supabase (OW-01).
  - Presencia latente de columna `password` en el esquema de la tabla `usuario` en Supabase (OW-03).
  - Ausencia de Rate Limiting perimetral para endpoints de inferencia computacionalmente intensivos en el Gateway (OW-05).
  - Persistencia de sesión JWT en `localStorage` en lugar de cookies seguras con atributo HttpOnly (OW-09).
  - Ausencia de registros y métricas de seguridad para eventos de rechazo 401/403 en el Gateway (OW-12).
- **Conclusión de Seguridad:** El perímetro y el cliente web presentan un blindaje robusto; las brechas remanentes recaen sobre la capa de persistencia administrada en la nube y la resiliencia ante saturación del Gateway.

---

## 4. Estado de Funcionalidad y Análisis de Regresiones

### Dictamen: **Se preservó la funcionalidad existente**

### Justificación Técnica:
1. **Regresiones funcionales:** Cero (0) regresiones detectadas.
2. **Resultados de Suites de Prueba:**
   - La suite modular de pruebas del frontend (`node --test tests/*.test.cjs`) se ejecutó tras las modificaciones de seguridad y documentación, confirmando **48 de 48 pruebas exitosas** (`docs/evidencias/semana13-ola1-verificacion.md:L19`).
   - Los contratos de API, el parser de configuración dinámica (`config.local.js`), el renderizado de gráficos y el formateo de métricas conservan total integridad.
3. **Aislamiento de Cambios:** Las modificaciones de la Ola 1 se limitaron a configuración web Nginx, marcado HTML de seguridad, workflows de CI/CD y documentación markdown. El código de backend de los microservicios (`monitoring`, `data-processing`, `prediction`, `gateway` y `simulator`) no fue alterado, preservando intacta la suite consolidada de **415+ pruebas automatizadas** y el smoke test end-to-end de 14/14 pasos.
4. **Riesgo de regresión:** Mínimo. Los cambios aplicados fueron incrementales, desacoplados y reversibles mediante control de versiones.

---

## 5. Clasificación de Riesgo Operativo

### Dictamen: **Riesgo Operativo Medio**

### Justificación de Factores Determinantes:
El sistema presenta una arquitectura técnicamente muy sólida, pero opera bajo condicionantes físicas y de despliegue que imponen un nivel de riesgo operativo **Medio**:

1. **Datos de telemetría y potencia simulados/modelados:**  
   Todos los registros del observatorio provienen de un generador sintético determinista (`software/simulator/`) y la potencia eléctrica en vatios (así como la energía acumulada en kWh) es modelada mediante relación lineal P = P_idle + (P_max - P_idle) * CPU (`software/frontend/energy.js:L10-L50`). No proviene de mediciones directas de hardware, sensores IPMI o medidores PDU reales. Aunque se declara con total honestidad experimental (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L101-L106`), operar sobre un clúster físico real requerirá adaptadores de ingesta por telemetría SNMP/Redfish aún no implementados.
2. **Políticas RLS en Supabase no verificadas en vivo:**  
   El snapshot histórico de la base de datos (`esquema-verificado.json:L458-L492`) registra directivas `Permitir todo` para roles públicos. Si estas políticas siguen activas en la nube de Supabase, un atacante que obtenga la clave pública del cliente (`publishable key`) podría interactuar directamente con PostgREST (`/rest/v1/`) evadiendo el Gateway. Dicha verificación remota sigue pendiente de validación directa en la consola por el administrador (programada para el Sprint 7).
3. **Recomendaciones de optimización sin flujo de aprobación persistido (HU-07):**  
   Prediction Service evalúa restricciones operativas y retorna `executionAllowed=false` por seguridad (`software/prediction/src/service/recommendations.py:L15-L80`). No obstante, el sistema no provee la interfaz para que el operador acepte o rechace la propuesta ni almacena dicha decisión humana en una tabla de auditoría, impidiendo la trazabilidad de negocio.
4. **Entorno de producción comparte Gateway con desarrollo en hosting gratuito:**  
   En la infraestructura desplegada en Render (`render.yaml`), las rutas de producción y desarrollo apuntan al mismo API Gateway en la nube compartida. El plan gratuito suspende los contenedores tras 15 minutos de inactividad, provocando retardos de arranque en frío (cold starts de 45 a 70 segundos) y riesgo de 504 Gateway Timeout durante exposiciones. Asimismo, la cuota mensual de 750 horas se comparte con otros proyectos de la cuenta del usuario, con riesgo de suspensión imprevista si no se mantiene disciplina de apagado.

---

## 6. Inventario de Riesgos Pendientes

Se consolidan los riesgos pendientes a gestionar durante las Olas 2 y 3:

| ID Riesgo | Categoria | Descripcion del Riesgo | Impacto | Mitigacion Programada |
|:---:|---|---|:---:|---|
| **RP-01** | Seguridad / BD | Políticas RLS permisivas y columna `password` en Supabase remota | Alto | Endurecimiento SQL en Sprint 7 (Ola 2, 11/11/2026). |
| **RP-02** | Disponibilidad | Cold starts de ~60 s en Render Free Tier exceden umbral de 7 s | Medio | Script de keep-alive previo a sustentaciones (Ola 2, 19/11/2026). |
| **RP-03** | Funcionalidad | Ausencia de tabla de auditoría y flujo de aprobación para HU-07 | Medio | Tabla `recommendation_decisions` y endpoint POST (Ola 2, 20/11/2026). |
| **RP-04** | Seguridad / Red | Ausencia de Rate Limiting perimetral ante saturación de inferencia | Medio | Token Bucket en Gateway Go / Spring Gateway (Ola 2, 17–28/11/2026). |
| **RP-05** | Operacion Cloud | Compartición de cuota horaria (750 h/mes) y Gateway único Prod/Dev | Medio | Rutina de apagado y separación de Blueprints (Ola 3, 22/11/2026). |
| **RP-06** | Usabilidad / Accesibilidad | Canvas de Chart.js sin tabla accesible oculta para lectores de pantalla | Bajo | Marcador HTML semántico y auditoría Lighthouse (Ola 2, 15/11/2026). |
| **RP-07** | Funcionalidad | Reportes históricos limitados a formato plano CSV sin PDF formal | Bajo | Módulo generador de PDF institucional (Ola 2, 18/11/2026). |

---

## 7. Observaciones del Auditor Independiente

1. **Rigor en la Cadena de Suministro:** Se destaca positivamente la rigurosidad aplicada en la sustitución de etiquetas flotantes por hashes SHA de 40 caracteres en GitHub Actions y la inclusión de SRI en scripts de terceros, resolviendo de forma limpia dos vectores frecuentes de ataque a la cadena de suministro.
2. **Honestidad Experimental Verificada:** Tanto el frontend (`software/frontend/dashboard.html:L260`, `network.html:L17`, `flows.html:L38`) como la nueva documentación (`entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md:L101-L106`) declaran explícitamente la naturaleza sintética de los datos y el carácter modelado de la potencia eléctrica, cumpliendo a cabalidad con las pautas éticas universitarias.
3. **Calidad de Pruebas y Arquitectura:** El desacoplamiento en adaptadores intercambiables (perfil de desarrollo SQLite y perfil de nube Supabase compartiendo 114 pruebas de contrato idénticas) evidencia un diseño de software mantenible, profesional y robusto.

---

## 8. Recomendacion Final

### Dictamen Oficial:
**APTO PARA PRODUCCION CON OBSERVACIONES**

### Justificación del Dictamen:
El sistema Green AI demuestra solvencia arquitectónica, estabilidad funcional (415+ pruebas pasando y 0 regresiones) y un nivel de apego sobresaliente en calidad (**87.00 % FURPS+**) y seguridad (**85.0 / 100 OWASP**), superando los requisitos para un entorno de demostración académica, evaluación docente y validación de Producto Mínimo Viable (PMV2).

Se otorga la condición de **«Con Observaciones»** debido a los condicionantes descritos que deben resolverse antes de considerar su explotación corporativa irrestricta:
1. **Verificación mandatoria en Supabase:** El propietario de la base de datos debe constatar en la consola SQL que las tablas históricas tengan RLS habilitado y carezcan de la columna `password` en texto claro.
2. **Precalentamiento en demostraciones:** En exposiciones docentes, debe ejecutarse el precalentamiento de Render con 25 minutos de anticipación para evitar que el jurado experimente cold starts de 60 segundos.
3. **Transparencia continua:** Mantener en toda presentación que las métricas corresponden a un entorno de data center simulado con fines de optimización algorítmica.
4. **Cumplimiento del Roadmap:** Continuar con la ejecución de las Olas 2 y 3 para alcanzar la calificación meta del 98.00 % FURPS+.
