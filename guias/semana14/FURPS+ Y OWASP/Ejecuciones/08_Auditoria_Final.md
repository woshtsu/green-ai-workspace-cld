# 07_Auditoria_Final.md

**Proyecto:** Green AI — Sistema de observabilidad y optimización energética predictiva para centros de datos  
**Institución:** Universidad Continental — Ingeniería de Sistemas e Informática  
**Curso:** Taller de Proyectos 1 ISI  
**Rol:** Auditor Principal de Calidad y Seguridad  
**Fecha:** 19 de noviembre de 2026  
**Repositorio:** `woshtsu/green-ai-workspace-cld`  
**Rama de referencia del estado de desarrollo:** `sprint7/7.2-proceso-pr`  
**Informes de entrada:**  
- `03_Auditoria_Implementacion_FURPS.md`
- `06_Auditoria_Implementacion_OWASP.md`

---

## 1. Resumen ejecutivo

Esta auditoría integra los resultados de calidad FURPS+ y seguridad OWASP, y determina si el estado observado del proyecto permite su puesta en producción.

El proyecto presenta una base técnica funcional y controles de ingeniería relevantes: arquitectura por servicios, pruebas automatizadas, autenticación perimetral, autorización por roles, validación de entradas, contenedores no privilegiados y controles de integridad en CI/CD. Sin embargo, los informes de implementación mantienen requisitos funcionales y de calidad pendientes, y documentan riesgos de seguridad que no han sido cerrados con evidencia suficiente.

### Dictamen consolidado

| Dimensión | Resultado | Dictamen |
|---|---|---|
| Calidad FURPS+ | 87.00 % bruto (174/200); 87.62 % ponderado, según informe 03 | **Cumple parcialmente** |
| Seguridad OWASP | 86.0/100 estimado en informe 06 | **Cumple parcialmente** |
| Funcionalidad | Sin regresiones observadas en la Ola 1; cambios posteriores sin regresión integral demostrada | **Preservación parcial demostrada; riesgo de regresión vigente** |
| Riesgo operativo | Alto | **No aceptable para producción** |

**Recomendación final: NO APTO PARA PRODUCCIÓN.**

La decisión no se basa únicamente en los puntajes. Se fundamenta en riesgos de control de acceso y exposición de servicios, ausencia de Rate Limiting y auditoría de rechazos, persistencia de sesión en navegador, remediaciones no verificadas en Supabase y falta de pruebas de regresión integrales sobre el commit que se pretende desplegar.

## 2. Alcance y criterio de decisión

Se integraron los resultados de los informes 03 y 06, junto con la inspección del estado de desarrollo documentado en la rama `sprint7/7.2-proceso-pr`.

Se aplicaron estos criterios:

1. Una mejora planificada no se considera implementada.
2. Una corrección estática no equivale a una prueba dinámica ni a una validación del entorno desplegado.
3. La falta de evidencia se trata como control no demostrado, no como prueba automática de vulnerabilidad explotable.
4. Los resultados de una rama de trabajo no se atribuyen a `test`, `main` o producción sin evidencia de integración y despliegue.
5. La recomendación de producción considera el impacto de los riesgos residuales, no solo el promedio de puntuaciones.

**Limitación:** esta auditoría es documental y estática. No se ejecutó un pentest, pruebas DAST/SAST/SCA completas, validación en Supabase, prueba de carga ni despliegue controlado. Tampoco se certifica que el commit inspeccionado sea el mismo que se encuentra desplegado.

## 3. Estado de calidad — FURPS+

<badge color="warning">Cumple parcialmente</badge>

### 3.1 Resultado cuantitativo

El informe `03_Auditoria_Implementacion_FURPS.md` registra:

- Puntaje bruto inicial: 170/200 (85.00 %).
- Puntaje bruto post Ola 1: 174/200 (87.00 %).
- Puntaje ponderado post Ola 1: 87.62 %.
- Mejora verificada: guía rápida de usuario (M-U07).
- Regresiones detectadas durante la Ola 1: cero; 48/48 pruebas de frontend satisfactorias según la evidencia de esa auditoría.

El porcentaje bruto y el ponderado son métricas distintas; no deben intercambiarse. Para este dictamen se reportan ambos valores.

### 3.2 Brechas que impiden declarar cumplimiento completo

El informe 03 identifica mejoras que permanecen pendientes o parcialmente satisfechas:

- Aprobación humana persistida de recomendaciones (HU-07).
- Exportación PDF de reportes históricos.
- Interfaz gráfica de MLflow desplegada.
- Verificación interactiva del observatorio `/dev/` con sesión real.
- Desacoplamiento de adaptadores del Simulator.
- Mitigación del impacto de cold start en Render Free.
- Auditoría WCAG 2.1 AA y alternativa accesible para gráficos.
- Endurecimiento de RLS en Supabase.
- Validación de factores de emisión para el cálculo de energía/CO₂e.
- Simplificación de operaciones principales en la interfaz.
- Gestión de cuota del hosting gratuito.

La existencia de estas tareas no implica que todo el producto sea inoperable; sí demuestra que el plan FURPS+ no está cerrado.

### 3.3 Dictamen de calidad

**Green AI cumple parcialmente FURPS+.**

El resultado de 87.00 % bruto y 87.62 % ponderado refleja avances, especialmente en usabilidad. No permite declarar cumplimiento total porque varias mejoras funcionales, de accesibilidad, mantenibilidad y operación continúan pendientes. La aprobación de Ola 1 no equivale a aprobación integral del producto.

## 4. Estado de seguridad — OWASP Top 10

<badge color="warning">Cumple parcialmente</badge>

### 4.1 Resultado cuantitativo

El informe `06_Auditoria_Implementacion_OWASP.md` estima un score de seguridad de **86.0/100**. La puntuación es una estimación de auditoría y no una certificación oficial OWASP.

El informe registra:

- 3 hallazgos corregidos.
- 2 hallazgos parcialmente corregidos.
- 7 hallazgos no corregidos o no demostrados.

Controles con corrección observada:
- OW-02: puertos de servicios publicados en loopback en la configuración Docker Compose inspeccionada.
- OW-07: cabeceras defensivas replicadas en la ruta `/config.local.js`.
- OW-10: acciones de GitHub Actions fijadas mediante SHA en los workflows inspeccionados.

Controles parcialmente corregidos:
- OW-06: cabeceras HTTP defensivas presentes en Nginx, pero CSP/HSTS no están acreditadas de forma homogénea en todos los entornos.
- OW-08: SRI aplicado a recursos externos principales, pero el inventario y la validación completa de recursos no se consideran cerrados.

### 4.2 Riesgos de seguridad pendientes

Permanecen abiertos o sin evidencia concluyente:

1. **OW-01 — RLS de Supabase:** no se aportó evidencia actual de políticas por tabla/operación ni pruebas negativas con usuarios de distintos roles.
2. **OW-03 — Columna `password`:** no se demostró el estado actual del esquema remoto ni la eliminación segura de la columna.
3. **OW-04 — Dataset Excel:** no se verificó de forma concluyente la eliminación/ofuscación de datos sensibles en todas las ramas, historial y artefactos.
4. **OW-05 — Rate Limiting:** los límites de tamaño y timeout no sustituyen la limitación de tasa por identidad/IP.
5. **OW-09 — Sesión:** el frontend conserva `persistSession: true`; la sesión sigue bajo almacenamiento persistente administrado por Supabase en el navegador.
6. **OW-11 — Imágenes Docker:** varios Dockerfiles utilizan etiquetas de imágenes base sin fijar digest SHA256.
7. **OW-12 — Auditoría 401/403:** no se demostró la existencia de logs estructurados, métricas y alertas específicas para rechazos de autenticación/autorización.

Hallazgos adicionales del informe 06:
- Data Processing no muestra autenticación propia en `main.py` y sus rutas dependen de que el Gateway sea el único perímetro. Si el servicio es accesible directamente, existe riesgo de elusión del control del Gateway.
- La documentación OpenAPI/Swagger y la ruta raíz de FastAPI requieren revisar su exposición en producción.
- Los cambios observados en una rama de trabajo no se consideran integrados en `test` o `main` hasta comprobar el PR, el SHA y el despliegue.

### 4.3 Dictamen de seguridad

**Green AI cumple parcialmente OWASP Top 10.**

Se observan controles relevantes, pero no existe evidencia suficiente para cerrar los riesgos de autorización en Supabase, exposición directa de servicios, Rate Limiting, gestión de sesión y trazabilidad de eventos de seguridad. El score 86.0/100 no elimina estos riesgos ni sustituye la validación dinámica.

## 5. Funcionalidad y regresiones

### 5.1 Funcionalidad preservada

El informe FURPS+ registra que durante la Ola 1:

- La suite frontend obtuvo 48/48 pruebas satisfactorias.
- No se modificaron microservicios backend durante esa fase.
- Se verificó correspondencia de textos y elementos de interfaz incluidos en la guía rápida.
- No se detectaron regresiones atribuibles a los cambios de esa ola.

El informe OWASP también registra pruebas de frontend y validaciones de configuración de Nginx para el alcance de Ola 1.

Por tanto, **la funcionalidad existente se preservó en el alcance y momento de la Ola 1, según las evidencias documentadas**.

### 5.2 Regresiones actuales

No se dispone de evidencia suficiente para afirmar que existan regresiones funcionales confirmadas en el estado actual. Tampoco se dispone de una ejecución integral posterior a los cambios de la rama `sprint7/7.2-proceso-pr` que permita afirmar que no existen.

**Resultado:** no se acreditan regresiones actuales confirmadas, pero tampoco se certifica su ausencia.

### 5.3 Riesgos de regresión

Los cambios de seguridad pendientes o propuestos pueden afectar:

- Login, registro, PKCE, refresh token, expiración y logout al modificar el almacenamiento de sesión.
- Consultas y reportes al endurecer RLS o retirar columnas de la base de datos.
- Inferencias y recomendaciones legítimas al aplicar Rate Limiting.
- Carga de scripts, estilos y gráficos al aplicar CSP.
- Compatibilidad de despliegue al fijar imágenes Docker por digest.
- Acceso y funcionamiento de Data Processing al restringir su exposición o exigir autenticación de servicio.

Se requieren pruebas de regresión específicas antes de aprobar cada remediación.

## 6. Riesgo operativo

<badge color="danger">Alto</badge>

El riesgo operativo se clasifica como **ALTO** por la combinación de:

- Riesgo de acceso directo a Data Processing si el servicio tiene exposición pública.
- RLS de Supabase sin verificación concluyente.
- Ausencia de Rate Limiting demostrado en el Gateway.
- Ausencia de auditoría específica para respuestas 401/403.
- Gestión de sesión persistente en el navegador.
- Falta de evidencia integral de pruebas de seguridad y regresión en el commit final.
- Dependencia de servicios gratuitos con posibles cold starts y restricciones de disponibilidad.
- Funcionalidades FURPS+ aún pendientes.

La clasificación no significa que se haya demostrado explotación activa. Indica que el impacto potencial y la falta de evidencia de controles críticos no permiten aceptar el riesgo para un entorno productivo.

## 7. Riesgos pendientes y condiciones de cierre

| Prioridad | Riesgo / brecha | Condición mínima para cierre |
|---|---|---|
| P0 | RLS Supabase (OW-01) | Políticas por tabla/operación verificadas y pruebas negativas con usuarios/roles distintos. |
| P0 | Exposición de Data Processing (NEW-01) | Confirmar topología real; impedir acceso directo no autenticado y probar el bypass. |
| P1 | Rate Limiting (OW-05) | Implementar límites por identidad y/o IP; demostrar respuesta 429 y ausencia de bloqueo indebido. |
| P1 | Auditoría 401/403 (OW-12) | Logs y métricas sin secretos, alertas y pruebas de generación/consulta. |
| P1 | Sesiones (OW-09) | Definir el diseño de sesión y probar login, PKCE, refresh, expiración, logout y navegación. |
| P1 | Columna `password` (OW-03) | Inspección del esquema remoto, migración segura y pruebas de dependencias. |
| P1 | Datos del Excel (OW-04) | Inspección del archivo, ramas, historial y consumidores; evidenciar saneamiento. |
| P2 | CSP/HSTS (OW-06) | Política compatible desplegada en todos los entornos y cabeceras HTTPS verificadas. |
| P2 | Imágenes Docker (OW-11) | Digests verificados en todos los Dockerfiles, build reproducible y smoke test. |
| P2 | SRI (OW-08) | Inventario de recursos externos y validación de integridad en navegador. |
| P2 | OpenAPI/Swagger (NEW-02) | Documentación protegida o deshabilitada en producción. |
| P2 | Integración de rama (NEW-03) | PR aprobado, SHA integrado, CI satisfactorio y verificación del commit desplegado. |
| P2 | Brechas FURPS+ | Cerrar y verificar mejoras funcionales, accesibilidad, mantenibilidad y operación pendientes. |

## 8. Observaciones del auditor

1. **Los puntajes no son un certificado de producción.** FURPS+ mide atributos de calidad y OWASP resume el estado de controles de seguridad; ninguno reemplaza pruebas operativas ni aceptación de riesgos.
2. **No mezclar ramas ni versiones.** Los resultados de `sprint7/7.2-proceso-pr` no deben atribuirse automáticamente a `test`, `main` o al servicio desplegado.
3. **No confundir pruebas de Ola 1 con pruebas actuales.** El resultado 48/48 corresponde al alcance documentado en esa fase y no acredita todos los cambios posteriores.
4. **La arquitectura debe validarse en despliegue.** Que un servicio se describa como interno no demuestra que su URL pública esté restringida.
5. **Mantener honestidad experimental.** La telemetría del proyecto es simulada y las estimaciones de energía/CO₂e son modeladas; no deben presentarse como mediciones físicas ni ahorros reales sin instrumentación y evidencia.
6. **La disponibilidad del hosting gratuito es una restricción operativa.** El cold start y las cuotas pueden ser aceptables para demostración académica, pero deben declararse y no confundirse con un SLA productivo.

## 9. Recomendación final

<badge color="danger">NO APTO PARA PRODUCCIÓN</badge>

El proyecto **no debe aprobarse para producción en su estado auditado**. Puede continuar utilizándose en desarrollo, pruebas controladas o demostraciones académicas con datos sintéticos y exposición limitada, siempre que se mantengan las advertencias sobre el origen simulado de la telemetría y se restrinja el acceso a los servicios.

Para reconsiderar la aprobación se requiere, como mínimo:

1. Cerrar y demostrar OW-01 y NEW-01 mediante pruebas de acceso no autorizado.
2. Implementar y probar Rate Limiting y auditoría de eventos 401/403.
3. Verificar el estado de credenciales y datos sensibles en Supabase y datasets.
4. Resolver el diseño de sesión y comprobar los flujos de autenticación completos.
5. Integrar las remediaciones en la rama de entrega y ejecutar CI.
6. Ejecutar pruebas de regresión, seguridad y despliegue sobre el mismo SHA candidato a producción.
7. Registrar formalmente los riesgos residuales aceptados por el responsable del proyecto.

**Conclusión:** Green AI muestra avances verificables en calidad y seguridad, pero mantiene brechas relevantes y controles críticos no demostrados. La recomendación técnica es **NO APTO PARA PRODUCCIÓN** hasta completar las condiciones de cierre y realizar una nueva auditoría sobre el artefacto efectivamente desplegable.
