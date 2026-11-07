# Catálogo de herramientas para Codex y Claude Code

**Fecha de elaboración:** 2026-11-06  
**Objetivo:** evaluar herramientas, priorizar su adopción y servir como documento de entrada para una migración de un proyecto actualmente contextualizado en Codex hacia Claude Code.

> **Advertencia de evidencia:** este catálogo consolida la revisión y clasificación conversada. No constituye una auditoría técnica exhaustiva de todas las versiones de los repositorios. La compatibilidad y los comandos de instalación deben verificarse contra los README y documentación vigentes antes de ejecutar cambios.

## Resumen ejecutivo

- No instalar todas las herramientas. Elegir según arquitectura, pruebas, seguridad, presupuesto y restricciones del proyecto.
- **Prioridad inicial condicionada:** Spec Kit (si la migración implica cambios grandes), Playwright (si existe frontend web), Agent Skills (solo los pertinentes), Graphify/Archify (si el código es complejo), auditoría de seguridad (según superficie de ataque).
- OmniRoute/FreeLLMAPI/Free Claude Code son alternativas o complementos para modelos, no prerrequisitos de Claude Code. Verificar seguridad de claves, costos, términos de uso y compatibilidad.
- Los tres mods del video de TikTok son **ideas**, no implementaciones comprobadas: El Portero, El Vigilante y un panel de consumo.
- El número 20 original contenía cuatro plugins distintos; por eso este inventario tiene 30 entradas aunque la lista original tenía 25 números.

## Inventario

| ID | Herramienta | Categoría | Descripción | Prioridad | Compatibilidad / estado | Enlace |
|---|---|---|---|---|---|---|
| 1 | FreeLLMAPI | Modelos y APIs | Agregación de proveedores/cuotas de modelos | Alta | Por comprobar | https://github.com/tashfeenahmed/freellmapi |
| 2 | OmniRoute | Modelos y APIs | Gateway, routing y fallback multimodelo | Alta | Declarada; verificar versión | https://github.com/cheaper-inference/OmniRoute |
| 3 | Free Claude Code | Modelos y APIs | Conexión con modelos/proveedores alternativos | Media | Por comprobar | https://github.com/Alishahryar1/free-claude-code |
| 4 | Reverse API Engineer | Automatización y APIs | Observar tráfico y generar clientes de APIs | Media | Por comprobar | https://github.com/kalil0321/reverse-api-engineer |
| 5 | Artemis | Automatización móvil | Automatización Android por lenguaje natural | Específica | Por comprobar | https://github.com/google/artemis |
| 6 | UniFace | Visión artificial | Detección y reconocimiento facial | Específica | Independiente | https://github.com/yakhyo/uniface |
| 7 | Floci | Infraestructura | Emulación local de servicios AWS | Media | Independiente | https://github.com/floci-io/floci |
| 8 | Memanto | Memoria y contexto | Memoria persistente para agentes (verificar capacidades) | Media | Por comprobar | https://github.com/moorcheh-ai/memanto |
| 9 | Recordly | Documentación audiovisual | Grabación de demostraciones de software | Media | Por comprobar | https://github.com/webadderallorg/Recordly |
| 10 | FreeDomain | Dominios y despliegue | Recurso de dominios gratuitos | Media | Independiente | https://github.com/DigitalPlatDev/FreeDomain |
| 11 | Anatomy | Visualización | Ilustraciones isométricas interactivas de sistemas | Específica | Por comprobar | https://github.com/wheresryan22/anatomy |
| 12 | Graphify | Arquitectura y código | Grafo de conocimiento sobre código y documentación | Alta | Por comprobar | https://github.com/Graphify-Labs/graphify |
| 13 | Agent Skills | Skills y agentes | Colección de habilidades para agentes | Alta | Verificar skill por skill | https://github.com/addyosmani/agent-skills |
| 14 | Cloudflare Security Audit Skill | Seguridad | Auditoría de seguridad asistida por agente | Alta | Por comprobar | https://github.com/cloudflare/security-audit-skill |
| 15 | Awesome Opus 5.5 Videos | Inspiración y multimedia | Ejemplos y prompts de animaciones programadas | Media | Recurso de referencia | https://github.com/yihui-dev/awesome-opus5-5-videos |
| 16 | AI Job Search | Aplicación especializada | Búsqueda de empleo y adaptación de CV con IA | Específica | Por comprobar | https://github.com/ai-job-search-dev/ai-job-search |
| 17 | Claude.dev | Por verificar | Sitio pendiente de identificación inequívoca | Por verificar | No confirmado | https://claude.dev |
| 18 | Archify | Arquitectura y diagramas | Diagramas interactivos desde planes o código | Alta | Por comprobar | https://github.com/tt-a1i/archify |
| 19 | Shannon | Seguridad | Pentesting autónomo de web/APIs | Específica | Por comprobar | https://github.com/KeygraphHQ/shannon |
| 20 | Playwright | Testing y navegador | Pruebas E2E y automatización web | Alta | Verificar integración MCP/CLI | https://playwright.dev/ |
| 21 | Headroom | Optimización | Plugin sin enlace específico; función por verificar | Por verificar | No confirmado | Pendiente |
| 22 | MemPalace | Memoria y contexto | Plugin sin enlace específico; función por verificar | Por verificar | No confirmado | Pendiente |
| 23 | FrontDesign | Frontend y diseño | Plugin sin enlace específico; función por verificar | Por verificar | No confirmado | Pendiente |
| 24 | Agency Agents | Skills y agentes | Roles especializados para agentes | Media | Por comprobar | https://github.com/msitarzewski/agency-agents |
| 25 | Boneyard | Frontend y UX | Generación de skeleton loading | Media | Por comprobar | https://github.com/0xGF/boneyard |
| 26 | Caveman | Optimización de tokens | Compresión de respuestas/contexto | Media | Por comprobar | https://github.com/JuliusBrussee/caveman |
| 27 | GitHub Spec Kit | Especificaciones y procesos | Desarrollo guiado por especificaciones | Alta | Verificar integración | https://github.com/github/spec-kit |
| 28 | El Portero (mod conceptual) | Routing de modelos | Elegir modelo según complejidad de tarea | Concepto | No implementado | https://vt.tiktok.com/ZSp6yRWaE/ |
| 29 | El Vigilante (mod conceptual) | Optimización de tokens | Monitorizar caché y avisar sobre consumo | Concepto | No implementado | https://vt.tiktok.com/ZSp6yRWaE/ |
| 30 | Panel de consumo (mod conceptual) | Observabilidad | Dashboard de consumo por agente/modelo | Concepto | No implementado | https://vt.tiktok.com/ZSp6yRWaE/ |

## Evaluación práctica por bloques

### Modelos y APIs
**FreeLLMAPI, OmniRoute, Free Claude Code:** considerar únicamente si se necesitan proveedores alternativos, límites de presupuesto o fallback. Probar primero un único gateway en un entorno de prueba; no mezclar múltiples proxies sin necesidad.

### Skills, agentes y especificaciones
**Agent Skills, Agency Agents, GitHub Spec Kit:** priorizar especificaciones claras y pocos roles útiles. Los archivos de instrucciones deben estar versionados y no duplicar reglas contradictorias.

### Memoria, contexto y optimización
**Memanto, MemPalace, Caveman, Headroom, El Vigilante:** no asumir que más memoria o compresión mejora el resultado. Medir fidelidad de recuperación, latencia y consumo de tokens. Evitar transmitir código privado a servicios no autorizados.

### Arquitectura y visualización
**Graphify, Archify, Anatomy:** Graphify se orienta a conocimiento sobre repositorios; Archify a diagramas; Anatomy a visualizaciones especializadas. No son equivalentes.

### Pruebas y seguridad
**Playwright, Reverse API Engineer, Cloudflare Security Audit Skill, Shannon, Artemis:** elegir según web, APIs o Android. Cualquier prueba ofensiva debe estar expresamente autorizada; ejecutar con credenciales de prueba y alcance limitado.

### Infraestructura, frontend y contenido
**Floci, FreeDomain, Boneyard, FrontDesign, Recordly, UniFace, Awesome Opus 5.5 Videos:** herramientas situacionales, no dependencias básicas de un agente de programación.

### Pendientes de identificación
**Claude.dev, Headroom, MemPalace, FrontDesign:** solicitar enlace exacto y comprobar procedencia, licencias, mantenimiento y seguridad antes de recomendar instalación.

## APARTADO ESPECIAL: INSTRUCCIONES PARA CODEX ANTES DE MIGRAR EL PROYECTO A CLAUDE CODE

### Contexto para el agente que lea este documento
El usuario tiene un **proyecto abierto en Codex**, y Codex **ya dispone del contexto del proyecto**. Codex está preparando un prompt o paquete de transferencia a Claude Code. Este catálogo es un **anexo de evaluación de herramientas**, no la especificación del proyecto ni una autorización para cambiar su arquitectura. La información del proyecto real debe extraerse del repositorio, documentación, historial relevante y contexto disponible en la sesión de Codex; **no inventarla a partir de este catálogo**.

### Instrucciones concretas para Codex
1. **Reconstruye el estado real del proyecto:** propósito, stack y versiones, estructura de carpetas, arquitectura, decisiones tomadas, funcionalidades terminadas y pendientes, comandos de desarrollo/pruebas, variables de entorno (solo nombres; nunca secretos), despliegue, incidencias abiertas y restricciones.
2. **Distingue hechos de hipótesis:** indica qué has comprobado en archivos o comandos, qué proviene de la conversación y qué falta verificar. Incluye rutas de archivos relevantes.
3. **Prepara un handoff autónomo para Claude Code:** objetivo, estado actual, pasos reproducibles para arrancar, decisiones técnicas, reglas de estilo, tareas prioritarias, criterios de aceptación, riesgos y preguntas pendientes.
4. **Revisa este catálogo contra necesidades reales:** selecciona un máximo de 3–5 herramientas iniciales; para cada una documenta beneficio concreto, alternativa ya disponible, compatibilidad confirmada, instalación oficial, riesgos, costo y cómo revertirla. No instales nada sin aprobación del usuario.
5. **Prioriza herramientas nativas:** antes de añadir proxies, memoria externa o agentes, revisa las funciones que Claude Code ya ofrezca en la versión disponible y las herramientas existentes en el repositorio.
6. **Diseña una migración incremental:** conserva el repositorio y su historial, evita cambios masivos de prompts/configuración, propone una primera tarea pequeña y verificable para comprobar que Claude entiende el proyecto.
7. **Seguridad y privacidad:** nunca incluyas tokens, API keys, cookies, contraseñas, archivos .env con valores, ni datos privados en el handoff. Señala cualquier MCP/plugin con acceso al filesystem, navegador, terminal, red o credenciales.
8. **Valida la transferencia:** solicita a Claude Code que resuma la arquitectura, enumere las tareas pendientes y proponga el primer cambio sin ejecutarlo. Compara con el estado registrado por Codex antes de autorizar cambios.
9. **Genera entregables sugeridos:** `CLAUDE.md` breve con reglas persistentes verificadas, `docs/HANDOFF_CODEX_TO_CLAUDE.md` con contexto completo y `docs/TOOLS_EVALUATION.md` con la selección de herramientas. Ajusta nombres/rutas a convenciones existentes.
10. **No confundas la migración de agente con una migración de aplicación:** el objetivo es transferir contexto y flujo de trabajo; modificar el stack, proveedor de IA o infraestructura requiere una decisión separada.

### Prompt listo para pegar en Codex

```text
Lee el archivo de catálogo de herramientas adjunto, especialmente el apartado «INSTRUCCIONES PARA CODEX ANTES DE MIGRAR EL PROYECTO A CLAUDE CODE».

Ya tienes contexto de este proyecto. Usa ese contexto y compruébalo contra el repositorio para preparar un paquete de transferencia fiel hacia Claude Code. No asumas que las herramientas del catálogo ya están instaladas ni que todas son necesarias.

Entrega: (1) resumen verificable del proyecto y su estado actual, (2) arquitectura, rutas y comandos, (3) decisiones y restricciones, (4) pendientes y siguiente tarea segura, (5) prompt de inicio para Claude Code, (6) propuesta justificada de hasta cinco herramientas del catálogo con riesgos y compatibilidad por verificar, (7) checklist de validación del handoff.

No reveles secretos. No modifiques código, dependencias, configuración ni instales herramientas sin mi aprobación. Distingue información verificada, contexto conversacional y supuestos. Si el repositorio ya tiene documentación para agentes, respétala y propón cambios mínimos.
```

## Checklist de adopción

- [ ] Verificar README, licencia, mantenimiento y última versión
- [ ] Confirmar compatibilidad con la versión concreta de Claude Code/Codex
- [ ] Evaluar permisos y tratamiento de código privado
- [ ] Probar en rama o entorno aislado
- [ ] Medir mejora real (tiempo, tokens, fallos, cobertura de pruebas)
- [ ] Documentar instalación y rollback
- [ ] Evitar duplicación con herramientas nativas

## Nota sobre el video de TikTok
Origen: https://vt.tiktok.com/ZSp6yRWaE/ . Los tres mods se clasifican como **conceptos por implementar**, no como repositorios o extensiones verificadas. «El Portero» propone selección de modelos; «El Vigilante», alertas de caché/consumo; «Tu propio panel», observabilidad del gasto por agente/modelo. Requieren comprobar APIs y telemetría disponibles antes de prometer automatización.
