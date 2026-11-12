**Guía para la Evaluación, Mejora y Validación de la Calidad y Seguridad de Software mediante FURPS+ y OWASP Top 10 utilizando Agentes de IA**

1. Introducción

La presente guía establece un procedimiento estandarizado para evaluar, mejorar y validar proyectos de software utilizando agentes de inteligencia artificial y dos marcos ampliamente reconocidos en la industria:

* FURPS+, para la evaluación de la calidad del software.
* OWASP Top 10, para la evaluación de la seguridad de aplicaciones.

La metodología está orientada a proyectos académicos y profesionales que ya se encuentran funcionales, independientemente de la tecnología utilizada.

Esta guía puede aplicarse mediante agentes como:

* Claude Code
* OpenAI Codex
* Cursor Agent
* Gemini Code Assist
* GitHub Copilot Agent
* Windsurf Agent
* Devin
* Otros agentes equivalentes

2. Objetivos

Objetivo General

Evaluar, mejorar y validar la calidad y seguridad de un proyecto de software utilizando agentes de inteligencia artificial, preservando la funcionalidad existente.

Objetivos Específicos

* Evaluar la calidad del software mediante FURPS+.
* Identificar oportunidades de mejora.
* Implementar mejoras de forma controlada.
* Evaluar la seguridad mediante OWASP Top 10.
* Remediar vulnerabilidades identificadas.
* Verificar que las mejoras implementadas no generen regresiones.
* Emitir una validación final del estado del proyecto.

3. Alcance

La guía puede aplicarse a:

* Aplicaciones web.
* Aplicaciones móviles.
* APIs.
* Sistemas empresariales.
* Sistemas académicos.
* Sistemas desplegados en producción.
* Proyectos universitarios.

4. Principios Fundamentales

Preservación de Funcionalidad

Toda modificación realizada por un agente debe mantener el correcto funcionamiento del sistema.

No se deben introducir cambios que:

* Rompan funcionalidades existentes.
* Afecten procesos de negocio.
* Generen regresiones.

Compatibilidad

Las mejoras implementadas deben mantener compatibilidad con:

* Usuarios actuales.
* APIs existentes.
* Integraciones existentes.
* Bases de datos existentes.

Evidencia

Toda conclusión emitida por un agente debe basarse en evidencia verificable obtenida del proyecto.

No se deben asumir funcionalidades ni vulnerabilidades sin evidencia.

Implementación Incremental

Las mejoras deben aplicarse de manera progresiva y controlada.

Se debe evitar:

* Reescrituras completas.
* Migraciones masivas.
* Cambios arquitectónicos innecesarios.

5. Organización de Entregables

Todos los documentos generados durante el proceso deberán almacenarse en la carpeta:

./docs

La estructura mínima esperada es:

docs/

│

├── 01\_auditoria\_furps.md

├── 02\_plan\_furps.md

├── 03\_auditoria\_implementacion\_furps.md

│

├── 04\_auditoria\_owasp.md

├── 05\_plan\_owasp.md

├── 06\_auditoria\_implementacion\_owasp.md

│

└── 07\_auditoria\_final.md

6. Flujo General del Proceso

FASE 1 - CALIDAD

1. Auditor FURPS+

↓

2. Planificador FURPS+

↓

3. El agente aplica el plan

↓

4. Auditor de Implementación FURPS+

FASE 2 - SEGURIDAD

5. Auditor OWASP Top 10

↓

6. Planificador OWASP Top 10

↓

7. El agente aplica el plan

↓

8. Auditor de Implementación OWASP

FASE 3 - VALIDACIÓN GLOBAL

9. Auditor Final Integral

7. Fase 1 – Evaluación y Mejora de Calidad

Paso 1. Auditoría FURPS+

Objetivo

Evaluar el estado actual del proyecto respecto a:

* Functionality
* Usability
* Reliability
* Performance
* Supportability

Ejecución

[Aquí va el prompt Auditor FURPS+]

Entregable

./docs/01\_auditoria\_furps.md

Paso 2. Planificación de Mejoras FURPS+

Objetivo

Definir un plan de mejora basado en los hallazgos de la auditoría.

Ejecución

[Aquí va el prompt Planificador FURPS+]

Entregable

./docs/02\_plan\_furps.md

Paso 3. Aplicación del Plan

Objetivo

Implementar las mejoras propuestas.

Actividades mínimas

* Analizar impacto.
* Implementar mejoras.
* Ejecutar pruebas.
* Validar funcionamiento.

Resultado

Proyecto actualizado.

Paso 4. Auditoría de Implementación FURPS+

Objetivo

Verificar que las mejoras hayan sido implementadas correctamente.

Ejecución

[Aquí va el prompt Auditor de Implementación FURPS+]

Entregable

./docs/03\_auditoria\_implementacion\_furps.md

8. Fase 2 – Evaluación y Mejora de Seguridad

Paso 5. Auditoría OWASP Top 10

Objetivo

Evaluar el nivel de seguridad del proyecto.

Categorías mínimas

* Broken Access Control
* Cryptographic Failures
* Injection
* Insecure Design
* Security Misconfiguration
* Vulnerable Components
* Authentication Failures
* Software and Data Integrity Failures
* Logging and Monitoring Failures
* SSRF

Ejecución

[Aquí va el prompt Auditor OWASP Top 10]

Entregable

./docs/04\_auditoria\_owasp.md

Paso 6. Planificación de Remediación

Objetivo

Definir acciones para corregir vulnerabilidades detectadas.

Ejecución

[Aquí va el prompt Planificador OWASP Top 10]

Entregable

./docs/05\_plan\_owasp.md

Paso 7. Aplicación del Plan

Objetivo

Implementar las remediaciones definidas.

Validaciones mínimas

* Inicio de sesión.
* Gestión de sesiones.
* APIs.
* Roles y permisos.
* Formularios.
* Integraciones.

Resultado

Proyecto reforzado en seguridad.

Paso 8. Auditoría de Implementación OWASP

Objetivo

Verificar que las vulnerabilidades hayan sido corregidas.

Ejecución

[Aquí va el prompt Auditor de Implementación OWASP]

Entregable

./docs/06\_auditoria\_implementacion\_owasp.md

9. Fase 3 – Validación Integral

Paso 9. Auditoría Final Integral

Objetivo

Emitir un dictamen final del estado del proyecto.

Ejecución

[Aquí va el prompt Auditor Final Integral]

Entregable

./docs/07\_auditoria\_final.md

10. Criterios de Aprobación

Calidad

* Las mejoras críticas fueron implementadas.
* No existen hallazgos críticos pendientes.

Seguridad

* Las vulnerabilidades críticas fueron mitigadas.
* Los riesgos residuales están documentados.

Funcionalidad

* No existen regresiones funcionales.
* Los procesos de negocio funcionan correctamente.

Estabilidad

* El sistema compila correctamente.
* El sistema despliega correctamente.
* Las pruebas críticas son satisfactorias.

11. Resultados Esperados

Al finalizar el proceso se deberá contar con:

* Diagnóstico de calidad mediante FURPS+.
* Plan de mejora de calidad.
* Validación de mejoras implementadas.
* Diagnóstico de seguridad mediante OWASP Top 10.
* Plan de remediación de vulnerabilidades.
* Validación de remediaciones implementadas.
* Informe final de calidad y seguridad.

Todo ello preservando la funcionalidad existente y garantizando una mejora controlada del proyecto.