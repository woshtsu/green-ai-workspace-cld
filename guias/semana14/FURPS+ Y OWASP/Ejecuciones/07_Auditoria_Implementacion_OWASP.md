# 06_Auditoria_Implementacion_OWASP.md

**Proyecto:** Green AI — Universidad Continental, Taller de Proyectos 1 ISI  
**Rol:** Auditor Independiente de Seguridad  
**Fecha de auditoría:** 2026-11-19  
**Repositorio:** `woshtsu/green-ai-workspace-cld`  
**Rama principal de inspección:** `sprint7/7.2-proceso-pr`  
**Rama de contraste documental:** `test`  
**Marco de referencia:** OWASP Top 10:2021, conforme a los hallazgos y al plan 04–05.  
**Modalidad:** inspección estática de archivos del repositorio y revisión de evidencias documentadas. No se ejecutaron pruebas dinámicas, pentest, pruebas contra Supabase ni validaciones en los despliegues públicos.

---

## 1. Resumen ejecutivo

Se contrastaron los doce hallazgos OW-01 a OW-12 de `docs/calidad/04_auditoria_owasp.md` con las remediaciones definidas en `docs/calidad/05_plan_owasp.md` y con el código disponible en la rama `sprint7/7.2-proceso-pr`.

| Estado | Cantidad |
|---|---:|
| Corregida | 3 |
| Parcialmente corregida | 2 |
| No corregida / sin evidencia suficiente | 7 |
| **Total** | **12** |

**Score estimado actualizado: 86.0/100**, calculado con el mismo esquema aditivo de diez categorías (0–10 por categoría) empleado en el informe de implementación previo. Es una estimación documental y está condicionada a que las remediaciones observadas en la rama inspeccionada se integren en la rama de entrega. No es una certificación ni una métrica oficial de OWASP.

**Dictamen:** implementación parcial. Se verifican avances en aislamiento de puertos locales, cabeceras Nginx, SRI y fijación de GitHub Actions, pero permanecen riesgos relevantes en RLS, rate limiting, almacenamiento de sesión, autenticación directa de microservicios y auditoría de accesos. No procede declarar el sistema seguro para producción con la evidencia actual.

## 2. Alcance, fuentes y limitaciones

### 2.1 Fuentes inspeccionadas

- `docs/calidad/04_auditoria_owasp.md` — línea base y hallazgos OW-01 a OW-12.
- `docs/calidad/05_plan_owasp.md` — estrategia de remediación en tres olas.
- `docs/calidad/06_auditoria_implementacion_owasp.md` — informe anterior, utilizado únicamente como antecedente y no como prueba de corrección actual.
- `docs/evidencias/semana13-ola1-verificacion.md` — registro de las pruebas de Ola 1.
- `software/infraestructura/docker-compose.yml`
- `software/frontend/nginx.conf`, `software/frontend/app.js` y páginas HTML.
- `software/gateway/src/main/resources/application.yaml`
- `software/gateway-go/internal/httpapi/server.go` y `internal/policy/routes.go`
- `software/data-processing/main.py` y `infrastructure/adapters/input/api/routes.py`
- `software/infraestructura/prometheus/alerts.yml`
- Dockerfiles de Gateway, Monitoring, Data Processing, Prediction y Simulator.
- `.github/workflows/ci.yml` y `.github/workflows/pages.yml`.

La rama `sprint7/7.2-proceso-pr` fue utilizada como referencia del estado de desarrollo inspeccionado. No debe confundirse con una integración confirmada en `test` o `main`. La rama `test` conserva el conjunto documental de Ola 1 y sirve como contraste.

### 2.2 Limitaciones de verificación

1. No se dispuso de acceso administrativo verificable a Supabase; por tanto, no se certifican políticas RLS, columnas ni datos reales de la base remota.
2. No se ejecutaron los comandos de validación del plan ni las suites de pruebas durante esta auditoría.
3. No se verificaron respuestas HTTP reales de Nginx, GitHub Pages, Render ni los servicios desplegados.
4. La ausencia de un archivo en la rama inspeccionada no demuestra por sí sola que un dato sensible haya sido eliminado de todas las ramas, historial Git, despliegues o copias.
5. El informe 06 previo describe principalmente Ola 1; sus declaraciones no se aceptan como evidencia de remediaciones posteriores.

## 3. Matriz de estado de remediación

| ID | Categoría | Hallazgo | Estado actual |
|---|---|---|---|
| OW-01 | A01 | Políticas RLS permisivas en Supabase | **No corregida / no demostrada** |
| OW-02 | A01 | Puertos internos publicados en Docker Compose | **Corregida en configuración inspeccionada** |
| OW-03 | A02 | Columna `password` en tabla `usuario` | **No corregida / no demostrada** |
| OW-04 | A02 | Contraseñas sintéticas en Excel versionado | **No demostrada** |
| OW-05 | A04 | Ausencia de Rate Limiting en Gateway | **No corregida** |
| OW-06 | A05 | Cabeceras de seguridad incompletas | **Parcialmente corregida** |
| OW-07 | A05 | Pérdida de cabeceras en `/config.local.js` | **Corregida en configuración inspeccionada** |
| OW-08 | A06 | Recursos CDN sin SRI | **Parcialmente corregida** |
| OW-09 | A07 | Sesión Supabase persistida en `localStorage` | **No corregida** |
| OW-10 | A08 | Acciones GitHub Actions con tags mutables | **Corregida en workflows inspeccionados** |
| OW-11 | A08 | Imágenes base Docker sin digest SHA256 | **No corregida** |
| OW-12 | A09 | Falta de logs/métricas de rechazos 401/403 | **No corregida** |

---

## 4. Evaluación detallada por hallazgo

### OW-01 — Políticas RLS permisivas en Supabase

**Estado: NO CORREGIDA / NO DEMOSTRADA**

**Evidencia:**
- El plan `05_plan_owasp.md` exige retirar políticas generales `cmd: ALL` para `public` y definir políticas específicas por operación y usuario.
- En `software/data-processing/infrastructure/adapters/input/api/routes.py`, los endpoints `/historical-logs` y `/reports/historical-summary` documentan expresamente que `hardwareId` es un filtro, no una autorización por usuario.
- No se encontró en las fuentes inspeccionadas una salida actual de `pg_policies` que demuestre la eliminación de las políticas permisivas en Supabase.

**Riesgo residual:** un cliente con la clave pública podría acceder directamente a PostgREST si las políticas permisivas continúan activas. La autorización del Gateway no sustituye las políticas de la base de datos.

**Validación necesaria:** ejecutar la consulta de `pg_policies` indicada en el plan, revisar cada tabla y operación, y probar con cuentas de roles distintos que las lecturas/escrituras no autorizadas sean denegadas. No registrar ni compartir secretos en el informe.

### OW-02 — Puertos de microservicios internos publicados en Docker Compose

**Estado: CORREGIDA EN CONFIGURACIÓN INSPECCIONADA**

**Evidencia:**
- `software/infraestructura/docker-compose.yml` publica Simulator como `127.0.0.1:${MONO_SIMULATOR_PORT:-18000}:8000`.
- Monitoring se publica como `127.0.0.1:${MONO_MONITORING_PORT:-18080}:8080`.
- Prometheus, Gateway y Frontend también se enlazan a `127.0.0.1`.
- Data Processing y Prediction utilizan `expose` y no publican puertos al host.

**Evaluación:** la configuración limita los puertos publicados a loopback y evita su exposición directa a interfaces de red externas en el escenario Docker local descrito.

**Riesgo residual:** la inspección estática no confirma el estado efectivo de los contenedores ni reglas de firewall del host. Tampoco demuestra que los servicios no estén expuestos por otros mecanismos.

**Validación necesaria:** ejecutar `docker compose config` y `docker compose ps`; comprobar sockets de escucha y realizar una prueba desde otro equipo de la red para confirmar que los puertos no son accesibles.

### OW-03 — Columna `password` en tabla `usuario`

**Estado: NO CORREGIDA / NO DEMOSTRADA**

**Evidencia:**
- El plan solicita ejecutar `ALTER TABLE usuario DROP COLUMN IF EXISTS password` y comprobar que la consulta a `information_schema.columns` devuelva cero filas.
- No se encontró evidencia de ejecución de la migración ni una captura/resultado actual del esquema remoto.
- La auditoría inicial identificó la columna en un snapshot, pero ese snapshot no demuestra el estado actual de Supabase.

**Riesgo residual:** si la columna existe y contiene valores reales, puede exponer credenciales en texto claro o inducir su uso por código legado.

**Validación necesaria:** consultar el esquema remoto, revisar dependencias y vistas, verificar que la autenticación use Supabase Auth o hashes adecuados, y ejecutar pruebas de login antes y después de la migración.

### OW-04 — Contraseñas sintéticas legibles en `BD_GreenAi.xlsx`

**Estado: NO DEMOSTRADA**

**Evidencia:**
- El plan exige retirar/ofuscar la columna de contraseñas y adaptar los consumidores del Excel.
- El archivo `software/data-processing/datasets/BD_GreenAi.xlsx` no pudo recuperarse en la rama `sprint7/7.2-proceso-pr` mediante la ruta indicada por la auditoría inicial.
- No se obtuvo evidencia verificable del archivo actualizado, de su eliminación del historial ni de pruebas de los scripts que lo consumían.

**Evaluación:** la falta del archivo en la ruta consultada no permite declarar corregido el hallazgo. Puede tratarse de eliminación, cambio de ruta o diferencia entre ramas.

**Riesgo residual:** los valores podrían persistir en otra rama, en el historial Git, en artefactos descargables o en copias del dataset.

**Validación necesaria:** buscar el dataset en todas las ramas y en el historial, inspeccionar sus hojas/celdas, revisar scripts consumidores y ejecutar las pruebas de Data Processing.

### OW-05 — Ausencia de Rate Limiting en Gateway

**Estado: NO CORREGIDA**

**Evidencia:**
- `software/gateway/src/main/resources/application.yaml` define rutas de inferencia y recomendaciones, tamaños máximos de petición y timeouts, pero no muestra filtros de limitación de tasa.
- `software/gateway-go/internal/httpapi/server.go` implementa CORS, autenticación, autorización, proxy, límites de tamaño y timeouts; no se observa un limitador por IP/token ni respuesta `429` por exceso de cuota.
- `software/gateway-go/internal/policy/routes.go` define rutas, métodos, tamaños y timeouts, sin política de tasa.

**Evaluación:** límites de tamaño y timeout no equivalen a Rate Limiting. No se encontró la implementación prevista por el plan (Token Bucket/RequestRateLimiter).

**Riesgo residual:** un usuario autenticado puede enviar solicitudes repetitivas a inferencia/recomendaciones y consumir recursos de los servicios de Prediction.

**Validación necesaria:** implementar límites coordinados en el Gateway efectivo y probar concurrencia, ráfagas, aislamiento por identidad y respuesta HTTP `429`, verificando que las peticiones legítimas bajo el umbral continúen funcionando.

### OW-06 — Cabeceras HTTP de seguridad incompletas

**Estado: PARCIALMENTE CORREGIDA**

**Evidencia:**
- `software/frontend/nginx.conf` contiene `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY`, `Permissions-Policy` y `Cross-Origin-Opener-Policy: same-origin`.
- La configuración inspeccionada no incluye `Content-Security-Policy` ni `Strict-Transport-Security`.
- El plan contempla CSP mediante meta etiqueta para cubrir GitHub Pages, que no pasa por Nginx.

**Evaluación:** las cabeceras defensivas base están presentes en Nginx. El control sigue incompleto porque no se encontró CSP en las páginas HTML ni evidencia de una política equivalente desplegada. HSTS debe evaluarse en el servidor HTTPS que termina TLS; no se puede resolver ni certificar únicamente desde este archivo Nginx si TLS termina en el proveedor de hosting.

**Riesgo residual:** mayor impacto potencial de XSS por ausencia de CSP y falta de evidencia de política homogénea entre Nginx y GitHub Pages.

**Validación necesaria:** definir CSP compatible con scripts/estilos usados, desplegarla en todos los entornos y probarla primero en modo Report-Only; verificar HSTS en el endpoint HTTPS público.

### OW-07 — Pérdida de cabeceras en `/config.local.js`

**Estado: CORREGIDA EN CONFIGURACIÓN INSPECCIONADA**

**Evidencia:**
- En `software/frontend/nginx.conf`, el bloque `location = /config.local.js` declara `Cache-Control: no-store` y replica explícitamente `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy` y `Cross-Origin-Opener-Policy`.
- Esto aborda el problema de herencia de `add_header` de Nginx identificado en la auditoría inicial.

**Riesgo residual:** no se repitió una petición HTTP real para confirmar las cabeceras entregadas por el servidor desplegado.

**Validación necesaria:** ejecutar `curl -sSI` sobre `/config.local.js` y confirmar simultáneamente `Cache-Control: no-store` y todas las cabeceras defensivas.

### OW-08 — Recursos CDN sin Subresource Integrity (SRI)

**Estado: PARCIALMENTE CORREGIDA**

**Evidencia:**
- `software/frontend/login.html` incluye Supabase JS `2.117.1` con `integrity` y `crossorigin="anonymous"`.
- `software/frontend/index.html` y `login.html` incluyen Font Awesome 6.4.0 con SRI.
- En las páginas inspeccionadas, Google Fonts continúa cargándose desde `fonts.googleapis.com` sin SRI.
- El informe anterior registra hashes SRI para Supabase JS, Font Awesome y Chart.js en las seis páginas HTML y pruebas de carga en navegador durante Ola 1. Esa evidencia corresponde al estado y ejecución documentados entonces; no se reejecutó en esta auditoría.

**Evaluación:** los recursos estáticos versionados de Supabase/Font Awesome muestran SRI. El hallazgo se mantiene parcial porque no todos los recursos externos están fijados por SRI y la verificación de navegador no se repitió sobre la rama inspeccionada.

**Riesgo residual:** dependencia externa de Google Fonts sin integridad criptográfica verificable mediante hash estático.

**Validación necesaria:** inventariar todas las referencias externas en todas las páginas, validar hashes contra los bytes servidos y decidir si Google Fonts se mantiene como excepción documentada o se autohospeda.

### OW-09 — Persistencia de sesión Supabase en `localStorage`

**Estado: NO CORREGIDA**

**Evidencia:**
- `software/frontend/app.js` crea el cliente Supabase con `persistSession: true`.
- La configuración no define un almacén de sesión alternativo en memoria ni una intermediación mediante cookie `HttpOnly`.
- La aplicación consulta la sesión mediante `auth.getSession()` y mantiene `activeAuthSession` en memoria, pero ello no elimina la persistencia administrada por Supabase.

**Riesgo residual:** un XSS que consiga ejecutarse en el origen puede acceder a datos de sesión almacenados por JavaScript en el navegador.

**Validación necesaria:** diseñar una migración compatible (BFF/cookie `HttpOnly`, `Secure`, `SameSite` o sesión en memoria con renovación controlada), probar login, PKCE, refresh, expiración, navegación protegida y logout. No desactivar `persistSession` sin probar el flujo completo.

### OW-10 — Acciones GitHub Actions referenciadas con tags mutables

**Estado: CORREGIDA EN WORKFLOWS INSPECCIONADOS**

**Evidencia:**
- `.github/workflows/ci.yml` fija `actions/checkout`, `setup-node`, `setup-python`, `setup-go` y `setup-java` mediante SHA de 40 caracteres.
- `.github/workflows/pages.yml` fija `checkout`, `setup-node`, `configure-pages`, `upload-pages-artifact` y `deploy-pages` mediante SHA.
- En los archivos inspeccionados no se observaron referencias `uses:` con tags flotantes para las acciones mencionadas.

**Riesgo residual:** fijar SHA no sustituye la revisión de permisos, dependencias transitivas, scripts ejecutados ni resultados de CI. La inspección no confirma que los workflows hayan concluido exitosamente en GitHub Actions.

**Validación necesaria:** ejecutar ambos workflows en la rama objetivo, revisar resultados y mantener un proceso controlado de actualización de SHA.

### OW-11 — Imágenes base Docker sin digest SHA256

**Estado: NO CORREGIDA**

**Evidencia:**
- `software/gateway/Dockerfile` usa `maven:3.9.11-eclipse-temurin-21` y `eclipse-temurin:21-jre-jammy` sin digest.
- `software/monitoring/Dockerfile` usa `eclipse-temurin:21-jdk-jammy` y `eclipse-temurin:21-jre-jammy` sin digest.
- `software/data-processing/Dockerfile` usa `python:3.14-slim` sin digest.
- `software/prediction/Dockerfile` usa `python:3.11.9-slim-bookworm` en ambas etapas sin digest.
- `software/simulator/Dockerfile` usa `python:3.12-slim` sin digest.
- La fijación por digest que el plan toma como patrón no se ha extendido a todos los Dockerfiles inspeccionados.

**Riesgo residual:** una etiqueta de imagen puede apuntar a contenido diferente con el tiempo, reduciendo la reproducibilidad de builds y la trazabilidad de la cadena de suministro.

**Validación necesaria:** resolver y fijar digests verificados para cada plataforma/imagen, reconstruir sin caché y ejecutar las pruebas de integración/smoke.

### OW-12 — Falta de registros y métricas para rechazos 401/403

**Estado: NO CORREGIDA**

**Evidencia:**
- `software/gateway-go/internal/httpapi/server.go` responde con `401` y `403` en los flujos de autenticación/autorización, pero no se observa registro estructurado de esos eventos ni incremento de métricas dedicadas.
- `software/infraestructura/prometheus/alerts.yml` contiene alertas operativas de telemetría, CPU, memoria y recomendaciones; no se observan reglas para tasas de rechazo `401/403`.
- `software/gateway/src/main/resources/application.yaml` expone `health,info,prometheus`, pero la configuración por sí sola no acredita métricas de denegación.

**Riesgo residual:** menor capacidad para detectar fuerza bruta, enumeración, abuso de permisos e incidentes; trazabilidad forense incompleta.

**Validación necesaria:** registrar eventos sin tokens ni datos sensibles, añadir contadores por resultado/ruta/rol, exponer métricas y crear alertas con umbrales. Probar que no se filtren credenciales ni datos personales en logs.

---

## 5. Nuevos hallazgos y controles incompletos

### NEW-01 — Data Processing depende de que el Gateway sea el único perímetro

**Categoría relacionada:** A01 Broken Access Control  
**Severidad preliminar:** Alta si el servicio es accesible directamente desde Internet.

**Evidencia:**
- `software/data-processing/main.py` registra middleware de correlación y manejadores de errores, pero no muestra middleware de autenticación/autorización.
- `software/data-processing/infrastructure/adapters/input/api/routes.py` expone `/historical-logs`, `/reports/historical-summary`, `/metrics/history` y `/prediction/dataset` sin validación de identidad local.
- Los comentarios del propio código indican que `hardwareId` es filtro y que el servicio debe publicarse únicamente detrás del Gateway autorizado.

**Riesgo:** si el servicio se despliega con URL pública accesible, un usuario podría invocar las rutas directamente y eludir JWT/RBAC del Gateway. La auditoría estática no confirma si la configuración real de Render restringe el acceso.

**Acción requerida:** confirmar el tipo de servicio y exposición de red en Render. Si la URL es pública, implementar autenticación de servicio o restringir el acceso por red/identidad; después probar acceso directo sin token y a través del Gateway.

### NEW-02 — Endpoints de documentación y raíz de Data Processing

**Categoría relacionada:** A05 Security Misconfiguration  
**Severidad preliminar:** Media, sujeta a exposición real.

**Evidencia:**
- `software/data-processing/main.py` crea `FastAPI(...)` sin deshabilitar explícitamente la documentación OpenAPI/Swagger.
- El endpoint `/` devuelve una referencia a `/docs`.

**Riesgo:** si el servicio está publicado directamente, la documentación interactiva facilita enumerar contratos y endpoints. No constituye por sí sola una vulnerabilidad crítica, pero amplía la superficie de reconocimiento.

**Acción requerida:** deshabilitar `/docs`, `/redoc` y `/openapi.json` en producción o protegerlos con autenticación; conservarlos en desarrollo si son necesarios.

### NEW-03 — Diferencia entre el alcance de las ramas

**Categoría relacionada:** A08 Software and Data Integrity Failures (gobernanza de release)  
**Severidad preliminar:** Media.

**Evidencia:**
- La rama inspeccionada `sprint7/7.2-proceso-pr` contiene cambios y no es equivalente por definición a `test` o `main`.
- Los workflows de CI y Pages declaran disparadores para `main` y `test`; no incluyen la rama `sprint7/7.2-proceso-pr` en sus filtros `push` de la configuración inspeccionada.
- El workflow Pages obtiene explícitamente `main` y `test` para construir los dos entornos.

**Riesgo:** las remediaciones de una rama de trabajo pueden no recibir la misma validación automática ni llegar al entorno de entrega. No debe atribuirse a `test` o `main` una corrección observada únicamente en la rama de trabajo.

**Acción requerida:** integrar mediante PR revisado, ejecutar CI en la rama objetivo y verificar el commit desplegado.

## 6. Regresiones funcionales y controles de compatibilidad

No se ejecutaron pruebas en esta auditoría; por tanto, **no se certifica ausencia de regresiones**.

Observaciones de riesgo funcional que requieren pruebas:

1. **OW-09 (sesión):** cambiar el almacenamiento de sesión puede afectar PKCE, renovación automática, navegación protegida y persistencia tras recargar la página.
2. **OW-01/OW-03 (Supabase):** endurecer RLS o eliminar una columna puede romper consultas, reportes, perfiles o procesos legados si no se revisan dependencias y permisos por operación.
3. **OW-05 (Rate Limiting):** umbrales demasiado bajos pueden bloquear inferencias legítimas o ejecuciones concurrentes de demostración.
4. **OW-06 (CSP):** una política estricta puede bloquear Supabase JS, Chart.js, Font Awesome, Google Fonts o scripts inline existentes.
5. **OW-02 (puertos):** el enlace a loopback es adecuado para acceso local, pero debe verificarse que el frontend y los procesos de desarrollo sigan utilizando los puertos esperados.
6. **OW-11 (digests):** fijar imágenes debe conservar arquitectura/plataforma compatible y permitir actualizaciones de seguridad controladas.

**Pruebas de regresión mínimas antes de aprobar el cierre:**
- Login, registro, refresh, expiración y logout.
- Acceso de ADMIN, OPERATOR y VIEWER por cada ruta/método.
- Acceso directo a Data Processing sin pasar por Gateway.
- Histórico, reportes JSON/CSV y consultas de telemetría.
- Inferencia y recomendaciones bajo carga normal y por encima del límite.
- Carga de todos los recursos frontend bajo CSP/SRI.
- `docker compose config`, build de imágenes y smoke test integral.
- Verificación de RLS con usuarios y roles reales de prueba.
- Ejecución completa de CI y comprobación del despliegue desde el commit aprobado.

## 7. Score de seguridad actualizado

### 7.1 Criterio

Se conserva el modelo aditivo del informe anterior: diez categorías OWASP con un máximo de 10 puntos cada una. El score no sustituye un análisis de riesgo formal ni una prueba de penetración.

El informe anterior registró **85.0/100 post Ola 1**. En esta revisión se reconoce el cumplimiento de OW-02 en `docker-compose.yml` porque Simulator y Monitoring están publicados exclusivamente en loopback y Data Processing/Prediction no publican puertos al host. Se incrementa A01 en un punto respecto del desglose anterior. No se concede crédito por OW-01, OW-03 u OW-04 al no existir evidencia actual de la base remota o del dataset.

### 7.2 Desglose

| Categoría | Score anterior post Ola 1 | Score revisado | Motivo |
|---|---:|---:|---|
| A01 Broken Access Control | 7.0 | 8.0 | OW-02 cumple el enlace loopback; OW-01 sigue sin demostración y NEW-01 requiere verificar exposición de Data Processing. |
| A02 Cryptographic Failures | 7.5 | 7.5 | OW-03 y OW-04 sin evidencia suficiente de cierre. |
| A03 Injection | 9.5 | 9.5 | No se encontró evidencia nueva que invalide los controles de parametrización previamente documentados; no se reejecutaron pruebas. |
| A04 Insecure Design | 8.0 | 8.0 | OW-05 sigue sin Rate Limiting. |
| A05 Security Misconfiguration | 9.0 | 9.0 | OW-07 corregida; OW-06 parcial por CSP/HSTS y NEW-02 requiere endurecimiento si hay exposición pública. |
| A06 Vulnerable Components | 9.5 | 9.0 | SRI presente para recursos principales, pero OW-08 sigue parcial por recursos externos no cubiertos y falta de repetición de pruebas. |
| A07 Identification and Authentication Failures | 8.5 | 8.5 | OW-09 sigue usando persistencia de sesión Supabase. |
| A08 Software and Data Integrity Failures | 8.5 | 8.5 | OW-10 corregida; OW-11 continúa sin digest en varios Dockerfiles. |
| A09 Logging and Monitoring Failures | 8.0 | 8.0 | OW-12 continúa sin evidencia de auditoría 401/403. |
| A10 Server-Side Request Forgery | 9.5 | 9.5 | No se verificó un cambio que justifique modificar la valoración anterior; no se ejecutaron pruebas SSRF. |
| **TOTAL** | **85.0** | **86.0** | **Variación neta: +1.0** |

**Score actualizado estimado: 86.0/100.**

La variación es limitada y no debe interpretarse como cierre de los riesgos de mayor impacto. El score permanece condicionado por hallazgos no verificados en servicios externos y por pruebas dinámicas pendientes.

## 8. Plan de cierre priorizado

| Prioridad | Hallazgo | Acción de cierre | Evidencia obligatoria |
|---|---|---|---|
| P0 | OW-01 / NEW-01 | Verificar RLS y cerrar acceso directo a Data Processing | Salida `pg_policies`; pruebas negativas PostgREST; prueba directa sin JWT |
| P1 | OW-03 | Confirmar/eliminar columna `password` y dependencias | Consulta de esquema antes/después; pruebas de autenticación |
| P1 | OW-05 | Implementar Rate Limiting en Gateway efectivo | Prueba concurrente con respuestas 429 y tráfico legítimo |
| P1 | OW-12 | Añadir auditoría y métricas 401/403 | Logs estructurados sin secretos; métricas y alertas verificadas |
| P1 | OW-09 | Resolver persistencia de sesión con diseño compatible | Pruebas completas PKCE, refresh, expiración y logout |
| P2 | OW-06 | Aplicar CSP en todos los entornos y verificar HSTS | Cabeceras reales; CSP Report-Only y posterior enforcement |
| P2 | OW-11 | Fijar imágenes base por digest | Dockerfiles revisados, build reproducible y smoke test |
| P2 | OW-04 | Localizar y sanear dataset en ramas/historial | Archivo inspeccionado, diff, búsqueda histórica y tests |
| P2 | OW-08 | Completar inventario SRI/recursos externos | Inventario de URLs, hashes comprobados y prueba de navegador |
| P2 | NEW-02 | Proteger documentación OpenAPI en producción | Pruebas de acceso anónimo a `/docs` y `/openapi.json` |
| P2 | NEW-03 | Integrar cambios y ejecutar CI en rama de entrega | PR, SHA integrado, checks exitosos y commit desplegado |

## 9. Conclusión y dictamen

La revisión confirma tres correcciones en los archivos inspeccionados: OW-02 (publicación local restringida a loopback), OW-07 (cabeceras replicadas en `/config.local.js`) y OW-10 (acciones GitHub Actions fijadas por SHA). OW-06 y OW-08 muestran implementación parcial. Los hallazgos OW-01, OW-03, OW-05, OW-09, OW-11 y OW-12 permanecen abiertos; OW-04 no puede darse por corregido porque no se obtuvo evidencia verificable del dataset actualizado.

Además, se identificó un riesgo relevante: Data Processing declara depender del Gateway como perímetro, pero sus rutas no muestran autenticación propia. Si la URL del servicio es pública, se podría eludir el control de acceso del Gateway. También debe revisarse la exposición de la documentación FastAPI y la integración de la rama de trabajo con los flujos CI/CD.

**Dictamen: NO APROBADO PARA CIERRE DE SEGURIDAD.** El score estimado de 86.0/100 no compensa la falta de verificación de controles de acceso en Supabase, autenticación entre servicios, Rate Limiting y auditoría de accesos. La aprobación requiere evidencia técnica reproducible, pruebas negativas de seguridad, pruebas de regresión y validación sobre el commit realmente integrado y desplegado.

---

## 10. Referencias de código

Las rutas y revisiones citadas corresponden a la rama `sprint7/7.2-proceso-pr`, salvo que se indique otra:

- [docker-compose.yml](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/infraestructura/docker-compose.yml)
- [nginx.conf](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/frontend/nginx.conf)
- [app.js](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/frontend/app.js)
- [Gateway Spring application.yaml](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/gateway/src/main/resources/application.yaml)
- [Gateway Go server.go](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/gateway-go/internal/httpapi/server.go)
- [Gateway Go routes.go](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/gateway-go/internal/policy/routes.go)
- [Data Processing main.py](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/data-processing/main.py)
- [Data Processing routes.py](https://github.com/woshtsu/green-ai-workspace-cld/blob/test/software/data-processing/infrastructure/adapters/input/api/routes.py)
- [Prometheus alerts.yml](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/software/infraestructura/prometheus/alerts.yml)
- [CI workflow](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/.github/workflows/ci.yml)
- [Pages workflow](https://github.com/woshtsu/green-ai-workspace-cld/blob/sprint7/7.2-proceso-pr/.github/workflows/pages.yml)
