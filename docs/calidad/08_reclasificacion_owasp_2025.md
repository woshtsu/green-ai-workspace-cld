# Reclasificación a OWASP Top 10:2025 — Green AI Monorepo

**Proyecto:** Green AI (Optimización Energética y Capacidad en Data Centers con Machine Learning)  
**Documento:** `docs/calidad/08_reclasificacion_owasp_2025.md`  
**Fecha:** 2026-11-12  
**Rama:** `test`  
**Referencia oficial:** https://top10.owasp.org/2025/  
**Documentos de entrada:** `04_auditoria_owasp.md`, `05_plan_owasp.md`, `06_auditoria_implementacion_owasp.md`, `07_auditoria_final.md`

---

## 1. Motivo

Las auditorías 04–07 se redactaron con OWASP Top 10:2021. El entregable de la semana 13 debe usar la edición vigente (2025). Los documentos 04–07 se conservan sin cambios de fondo como registro histórico (solo llevan una nota al inicio que remite a este archivo). **Este documento es la clasificación autoritativa OWASP Top 10:2025** para el entregable de la semana 13.

## 2. Cambios 2021 → 2025 (lista oficial)

| 2025 | Nombre oficial | Procedencia (2021) |
|---|---|---|
| A01:2025 | Broken Access Control (Pérdida de Control de Acceso) | A01:2021 + A10:2021 SSRF (absorbida, CWE-918) |
| A02:2025 | Security Misconfiguration (Configuración de Seguridad Incorrecta) | A05:2021 (sube de #5 a #2) |
| A03:2025 | Software Supply Chain Failures (Fallos en la Cadena de Suministro de Software) | A06:2021 Vulnerable and Outdated Components (ampliada) |
| A04:2025 | Cryptographic Failures (Fallos Criptográficos) | A02:2021 (baja a #4) |
| A05:2025 | Injection (Inyección) | A03:2021 (baja a #5) |
| A06:2025 | Insecure Design (Diseño Inseguro) | A04:2021 (baja a #6) |
| A07:2025 | Authentication Failures (Fallos de Autenticación) | A07:2021 (renombrada; antes «Identification and Authentication Failures») |
| A08:2025 | Software or Data Integrity Failures (Fallos de Integridad del Software o de los Datos) | A08:2021 (renombre aclaratorio) |
| A09:2025 | Security Logging and Alerting Failures (Fallos de Registro y Alertas de Seguridad) | A09:2021 (renombrada: «Monitoring» pasa a «Alerting») |
| A10:2025 | Mishandling of Exceptional Conditions (Manejo Inadecuado de Condiciones Excepcionales) | **Nueva** |

## 3. Reclasificación de hallazgos OW-01…OW-13

| Hallazgo | Descripción breve | Categoría 2021 | Categoría 2025 | Estado |
|---|---|---|---|---|
| OW-01 | RLS permisivas en Supabase | A01 | A01:2025 | Pendiente (no verificado en BD remota) |
| OW-02 | Puertos de compose expuestos (18080, 18000) | A01 | A01:2025 | Pendiente (presente en local) |
| OW-03 | Columna `password` en tabla `usuario` | A02 | A04:2025 | Pendiente (no verificado en BD remota) |
| OW-04 | Contraseñas sintéticas en Excel versionado | A02 | A04:2025 | Pendiente |
| OW-05 | Sin rate limiting en gateway | A04 | A06:2025 | Pendiente |
| OW-06 | Faltan cabeceras CSP, X-Frame-Options, Permissions-Policy | A05 | A02:2025 | Corregido (Ola 1) |
| OW-07 | Pérdida de cabeceras en `/config.local.js` | A05 | A02:2025 | Corregido (Ola 1) |
| OW-08 | CDN sin SRI | A06 | A03:2025 | Corregido (Ola 1) |
| OW-09 | Token en `localStorage` | A07 | A07:2025 | Pendiente |
| OW-10 | Acciones de GitHub sin fijar por SHA | A08 | A08:2025 | Corregido (Ola 1) |
| OW-11 | Imágenes Docker sin digest | A08 | A08:2025 | Pendiente (bajo) |
| OW-12 | Sin auditoría de 401/403 | A09 | A09:2025 | Pendiente |
| OW-13 | Manejo de condiciones excepcionales en gateways y frontend | (no existía) | A10:2025 | Nuevo (Ola 3) |

Notas:
- SSRF (A10:2021) queda absorbida por A01:2025. Sin hallazgo abierto: está mitigada (rutas upstream fijas, rechazo de redirecciones, validación de esquemas URL).
- A05:2025 Injection no tiene hallazgos (mitigado).
- OW-10 y OW-11 se mantienen en A08 según el mapeo oficial, aunque A03:2025 también abarca la seguridad de CI/CD.

## 4. Evaluación de la nueva A10:2025

Evaluación por inspección estática de código (rama `test`). Calificación: **Parcial (3)**, puntaje **8.0/10**, severidad Media, estado Requiere Atención.

### 4.1 Fortalezas (fail-closed y respuestas genéricas)

- `software/prediction/src/service/app.py:74-92`: manejadores `MLError` y catch-all `Exception`; registra con `LOGGER.exception` y responde 500 genérico `{"code":"INFERENCE_ERROR","message":"Inference failed"}` con `X-Request-Id`, sin traza. Modelo ausente devuelve 503 `MODEL_UNAVAILABLE` (probado en `tests/api/test_health_and_predict.py` y `tests/test_recommendations_api.py`).
- `software/data-processing/main.py:40-57`: catch-all RFC 7807 genérico con `requestId`; los errores de validación devuelven solo nombres de campo.
- `software/monitoring/.../ApiExceptionHandler.java`: `@RestControllerAdvice`; fallos mapeados a 400/422/502/503/504; catch-all genérico sin traza. `PrometheusClient` con timeouts y concurrencia acotada (`BoundedMetricsSource`).
- `software/gateway-go/internal/httpapi/server.go`: JWKS no disponible devuelve 503 y nunca acepta el token (`TestJWKSUnavailableIs503AndNeverAccepts`); upstream caído devuelve 503 sin detalles internos (`TestUpstreamDownIs503WithoutInternalDetails`); timeout devuelve 504 (`TestUpstreamTimeoutIs504`); timeouts por ruta (6 s por defecto), sin reintentos, límites de cuerpo.
- Frontend: `friendly-errors.js` clasifica errores de red/401/403 en mensajes comprensibles; `AbortSignal.timeout` en `app.js` y `prediction.js`.
- Sin `debug=True` ni `--reload` en los Dockerfiles.

### 4.2 Brechas

1. Los gateways no manejan explícitamente sus propios fallos: `gateway-go` no tiene middleware de recuperación de pánicos (`recover`) que devuelva problem+json; Spring Cloud Gateway (`software/gateway`) no tiene manejador global ni `server.error.include-*` en `never`.
2. Faltan pruebas que aseguren que los catch-all 500 no filtran detalles internos; los timeouts de fetch del frontend no son uniformes (`monitoring.js`, `pmv2.js`, `racks.js`) y el login muestra `error.message` de Supabase sin filtrar (`app.js:107`).

### 4.3 Hallazgo OW-13 — Manejo inadecuado de condiciones excepcionales

| Campo | Valor |
|---|---|
| Categoría | A10:2025 Mishandling of Exceptional Conditions |
| Severidad | Media |
| Ola | 3 |
| Responsable | Ricardo Porras Veli |
| Fecha objetivo | 30/11/2026 |

**Acciones de remediación**
1. `gateway-go`: añadir middleware de recuperación de pánicos que responda problem+json genérico, con prueba que provoque un pánico y verifique el cuerpo.
2. `software/gateway` (Spring): configurar `server.error.include-message/-stacktrace/-exception/-binding-errors = never` o añadir un manejador global de excepciones, con prueba asociada.
3. Pruebas que afirmen cuerpos 500 genéricos (sin traza ni detalles internos) en `prediction`, `data-processing` y `monitoring`.
4. Frontend: timeouts de fetch uniformes (`AbortSignal.timeout`) en `monitoring.js`, `pmv2.js` y `racks.js`; no mostrar `error.message` crudo de Supabase en el login (`app.js:107`), sino un mensaje amigable.

**Criterios de aceptación**
- Un pánico en `gateway-go` produce una respuesta problem+json genérica y el servicio sigue atendiendo peticiones.
- Una excepción no controlada en el gateway Spring no expone mensaje, traza ni clase de excepción.
- Las pruebas de 500 genérico de los tres servicios pasan en CI.
- Todas las llamadas fetch del frontend tienen timeout y el login no muestra texto crudo de Supabase.

## 5. Puntajes recalculados

### 5.1 Score de seguridad 0–100 (10 puntos por categoría)

| Categoría 2025 | Inicial | Post Ola 1 |
|---|---|---|
| A01 | 7.0 | 7.0 |
| A02 | 7.0 | 9.0 |
| A03 | 8.0 | 9.5 |
| A04 | 7.5 | 7.5 |
| A05 | 9.5 | 9.5 |
| A06 | 8.0 | 8.0 |
| A07 | 8.5 | 8.5 |
| A08 | 7.5 | 8.5 |
| A09 | 8.0 | 8.0 |
| A10 | 8.0 | 8.0 |
| **Global** | **79.0 / 100** | **83.5 / 100 (+4.5)** |

Con 2021 el resultado era 80.5 → 85.0. La diferencia proviene de retirar SSRF como categoría propia (9.5, absorbida en A01, que conserva 7.0 por OW-01/OW-02) e incorporar A10:2025 con 8.0.

### 5.2 Matriz docente (Cumple 5 / Parcial 3 / No cumple 1)

| Categoría 2025 | Inicial | Actual (post Ola 1) | Esperado |
|---|---|---|---|
| A01 | 1 | 1 | 5 |
| A02 | 3 | 5 | 5 |
| A03 | 3 | 5 | 5 |
| A04 | 1 | 1 | 5 |
| A05 | 5 | 5 | 5 |
| A06 | 3 | 3 | 5 |
| A07 | 3 | 3 | 3 |
| A08 | 3 | 5 | 5 |
| A09 | 3 | 3 | 5 |
| A10 | 3 | 3 | 5 |
| **OWASP** | 28/50 = 56.0 % | 34/50 = 68.0 % | 48/50 = 96.0 % |

Variación Ola 1 en OWASP: +12.0 %.

| Bloque | Inicial | Actual | Esperado |
|---|---|---|---|
| FURPS+ (sin cambios) | 170 / 200 | 174 / 200 | 196 / 200 |
| OWASP | 28 / 50 | 34 / 50 | 48 / 50 |
| **Global (250)** | **198 = 79.2 %** | **208 = 83.2 %** | **244 = 97.6 %** |

Variación global: +4.0 %. Con 2021 el global era 200/250 = 80.0 % y 210/250 = 84.0 %.

Nota: A01 y A04:2025 (antes A01 y A02:2021) valen **No cumple (1)** en Inicial y Actual, tal como figuran en el Excel oficial y en los totales previos (30 y 36). La versión anterior del `.md` los mostraba como «Parcial (3)», incoherente con sus propios totales; se corrige.

## 6. Impacto en entregables

- `entregables/semana13/semana13-calidad-furps-owasp.md`: actualizar a la clasificación 2025 y a los puntajes de este documento.
- `exportados/semana13/…-semana13-calidad-FURPS-OWASP.docx`: regenerar a partir del `.md` actualizado.
- `MODELO-FURPSPLUS-Green-AI.xlsx`: regenerado con `herramientas_IA/calidad/llenar_modelo_furps.py`.
- Fuera de alcance: el informe corregido de la Unidad III (`informe-corregido`).

## Nota de honestidad

La evaluación de A10:2025 es de inspección estática de código. No se ejecutó ninguna prueba en tiempo de ejecución para esta reclasificación.
