# 04_Auditoria_OWASP.md — Auditoría de Seguridad OWASP Top 10

**Proyecto:** Green AI — Observabilidad y optimización energética predictiva  
**Institución:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol:** Auditor de Seguridad  
**Fecha:** 19/11/2026  
**Repositorio:** `woshtsu/green-ai-workspace-cld`  
**Rama inspeccionada:** `test`  
**Alcance:** Frontend, Gateway, APIs, autenticación, autorización, configuración, dependencias e infraestructura versionada.  
**Método:** revisión estática de archivos y evidencias disponibles en el repositorio. No se ejecutaron escáneres SAST/DAST/SCA, pruebas de penetración, consultas a Supabase ni validaciones de los servicios desplegados.

---

## 1. Resumen ejecutivo

La revisión identifica controles positivos en autenticación centralizada mediante Supabase JWT/JWKS, autorización por rutas y roles en el Gateway Go, validación de entradas, límites de tamaño/tiempo en el proxy, uso de HTTPS documentado para servicios desplegados, SRI en bibliotecas externas y acciones de GitHub fijadas por SHA.

Sin embargo, permanecen riesgos relevantes:
- Data Processing se describe como servicio interno y sus endpoints no implementan autenticación propia. La guía de despliegue documenta servicios Render comunicándose mediante URLs públicas, sin red privada.
- La guía de despliegue documenta que la clave legacy `anon` puede leer los registros `logs` debido a políticas RLS permisivas.
- El Gateway es el punto de control de acceso previsto, por lo que cualquier exposición directa de servicios internos o bypass del Gateway puede eludir la autorización.
- No se encontró evidencia de una política CSP efectiva en GitHub Pages, ni de un análisis completo de dependencias vulnerables.
- No se acreditó una evaluación dinámica de SSRF, inyección, control de acceso horizontal ni seguridad de sesión.

<badge color="warning">Riesgo global: ALTO</badge>

**Score global estimado: 42.5/100.** Es una estimación de postura basada en evidencia documental y estática; no es una puntuación oficial de OWASP ni sustituye un pentest.

---

## 2. Alcance y limitaciones

### 2.1 Componentes inspeccionados

- Frontend estático: `software/frontend/`.
- Gateway Go: `software/gateway-go/`.
- APIs Prediction: `software/prediction/`.
- APIs Data Processing: `software/data-processing/`.
- Configuración de Nginx: `software/frontend/nginx.conf`.
- Infraestructura Docker Compose: `software/infraestructura/docker-compose.yml`.
- CI/CD: `.github/workflows/ci.yml` y `.github/workflows/pages.yml`.
- Despliegue: `docs/GUIA-DESPLIEGUE-RENDER.md`.
- Evidencia de Ola 1: `docs/evidencias/semana13-ola1-verificacion.md`.

### 2.2 Limitaciones

1. La rama consultada puede no representar cambios locales o despliegues posteriores al snapshot recuperado.
2. No se inspeccionaron políticas RLS directamente desde el proyecto Supabase.
3. No se verificó el estado real de variables de entorno, reglas de firewall, configuración de Render, dominios ni secretos.
4. No se ejecutaron pruebas de explotación, fuzzing, escaneo de dependencias ni análisis de imágenes.
5. No se dispone de evidencia suficiente para afirmar ausencia de vulnerabilidades. «No observado» significa que no se encontró evidencia en el alcance inspeccionado.

---

## 3. Matriz de evaluación OWASP Top 10

| Categoría | Estado | Probabilidad | Impacto | Severidad |
|---|---|---|---|---|
| A01 Broken Access Control | Riesgo significativo | Alta | Alto | **Alto** |
| A02 Cryptographic Failures | Controles parciales; configuración no verificada | Media | Alto | **Medio** |
| A03 Injection | No se observa inyección directa en rutas revisadas; falta DAST | Baja/Media | Alto | **Medio** |
| A04 Insecure Design | Brechas de diseño en aislamiento y trazabilidad | Media | Alto | **Alto** |
| A05 Security Misconfiguration | Configuración de despliegue y cabeceras incompleta/no uniforme | Alta | Alto | **Alto** |
| A06 Vulnerable and Outdated Components | Riesgo no cuantificado; inventario/escaneo incompleto | Media | Alto | **Medio** |
| A07 Identification and Authentication Failures | Diseño con Supabase/JWKS; validación operativa incompleta | Media | Alto | **Medio** |
| A08 Software and Data Integrity Failures | Controles positivos en CI/SRI; cobertura parcial | Baja/Media | Alto | **Medio** |
| A09 Security Logging and Monitoring Failures | Correlación presente; auditoría/alertas de seguridad no demostradas | Media | Medio | **Medio** |
| A10 Server-Side Request Forgery (SSRF) | URLs upstream configurables; controles de destino incompletos/no probados | Media | Alto | **Medio** |

---

## 4. Análisis por categoría

### A01 — Broken Access Control

**Estado:** Riesgo significativo.  
**Severidad:** **ALTO**.  
**Probabilidad:** Alta.  
**Impacto:** Alto.

**Evidencia:**
- `software/gateway-go/internal/policy/routes.go` define una tabla explícita de rutas y métodos. `ADMIN` y `OPERATOR` pueden acceder a las rutas publicadas; `VIEWER` solo puede utilizar rutas GET.
- El Gateway Go valida JWT mediante `auth.NewJWKSVerifier(issuer, "authenticated", jwks)` en `software/gateway-go/cmd/gateway/main.go`.
- `software/data-processing/infrastructure/adapters/input/api/routes.py` documenta en el endpoint `/historical-logs`: «hardwareId es un filtro, no autorización por usuario. Publicar únicamente detrás del Gateway autorizado».
- `software/data-processing/main.py` crea la aplicación FastAPI y registra las rutas, pero en el archivo inspeccionado no se observa middleware de autenticación/autorización propio.
- `docs/GUIA-DESPLIEGUE-RENDER.md` indica que los servicios se comunican mediante URLs públicas `https://….onrender.com` y que Render Free no dispone de red privada.

**Impacto:**
Si Data Processing o Prediction son accesibles directamente desde Internet sin una barrera equivalente, un atacante podría evitar el Gateway y sus controles de rol. En Data Processing, el filtro `hardwareId` no restringe por sí mismo los datos que un usuario está autorizado a consultar. La documentación de RLS permisiva aumenta la exposición potencial de históricos.

**Probabilidad:** Alta mientras no se demuestre que las URLs directas están protegidas por controles de red/autenticación y que las políticas RLS aíslan correctamente los datos.

**Observación:** La tabla de rutas del Gateway y el control VIEWER son controles positivos, pero no prueban que todos los caminos hacia los servicios pasen obligatoriamente por él.

### A02 — Cryptographic Failures

**Estado:** Controles parciales; configuración criptográfica completa no verificada.  
**Severidad:** **MEDIO**.  
**Probabilidad:** Media.  
**Impacto:** Alto.

**Evidencia:**
- `docs/GUIA-DESPLIEGUE-RENDER.md` define URLs HTTPS para frontend y servicios Render, y utiliza el emisor/JWKS de Supabase.
- `software/frontend/login.html` carga Supabase JS desde CDN con `integrity="sha384-..."` y `crossorigin="anonymous"`.
- `docs/evidencias/semana13-ola1-verificacion.md` registra hashes SRI estables para Supabase JS, Chart.js y Font Awesome.
- `software/infraestructura/docker-compose.yml` utiliza URLs HTTPS para issuer/JWKS de Supabase por defecto, aunque los servicios locales se comunican por HTTP dentro de la red Docker.
- No se encontró evidencia de una política completa de cifrado en reposo, gestión/rotación de secretos, política de TLS mínima o validación de certificados en todos los servicios.

**Impacto:**
Una configuración débil de TLS, exposición de secretos o almacenamiento sin cifrado de datos sensibles podría permitir interceptación o divulgación de credenciales/datos. La revisión estática no demuestra que estos escenarios estén ocurriendo.

**Probabilidad:** Media, debido a la presencia de HTTPS/SRI pero ausencia de evidencia de configuración criptográfica integral.

### A03 — Injection

**Estado:** No se observa evidencia directa de inyección en los fragmentos revisados; cobertura de pruebas insuficiente.  
**Severidad:** **MEDIO**.  
**Probabilidad:** Baja/Media.  
**Impacto:** Alto.

**Evidencia:**
- `software/data-processing/infrastructure/adapters/input/api/routes.py` utiliza parámetros tipados, enumeraciones, límites y expresiones regulares para filtros como `cluster`, `resourceId`, `hardwareId`, `limit` y `stepSeconds`.
- `software/data-processing/main.py` evita devolver los valores brutos de entrada en errores de validación.
- `software/prediction/src/service/recommendations.py` utiliza modelos Pydantic con `extra='forbid'`, límites numéricos y validación de campos.
- No se encontró en los archivos inspeccionados una prueba DAST/fuzzing que cubra sistemáticamente SQL/NoSQL injection, command injection, template injection o inyección en consultas a servicios externos.
- No se revisó exhaustivamente cada consulta SQL ni cada adaptador de persistencia.

**Impacto:**
Una inyección exitosa podría alterar consultas, acceder a datos no autorizados o comprometer el proceso que ejecuta el servicio.

**Probabilidad:** Baja/Media por la validación observada, pero no puede reducirse a baja con certeza sin revisar adaptadores y ejecutar pruebas.

**Conclusión:** no se confirma una vulnerabilidad de inyección; la categoría permanece en observación por falta de cobertura dinámica.

### A04 — Insecure Design

**Estado:** Brechas de diseño relevantes.  
**Severidad:** **ALTO**.  
**Probabilidad:** Media.  
**Impacto:** Alto.

**Evidencia:**
- Data Processing declara expresamente que `hardwareId` es filtro, no autorización por usuario, y que el servicio debe publicarse detrás del Gateway.
- La guía de Render documenta comunicación entre servicios por URLs públicas y ausencia de red privada.
- La misma guía declara que el token anon puede leer `logs` debido a RLS permisiva.
- `software/prediction/src/service/recommendations.py` fija `executionAllowed=False`, lo que reduce el riesgo de ejecución automática de cambios de infraestructura.
- No se encontró un flujo persistente de aprobación humana con identidad, decisión, motivo y marca temporal.

**Impacto:**
El diseño depende de que el Gateway sea un punto de control obligatorio y de que Supabase aplique aislamiento correcto. Una configuración incorrecta puede convertir una ruta de solo lectura en acceso horizontal a datos. La ausencia de persistencia de aprobación limita la trazabilidad de decisiones operativas.

**Probabilidad:** Media, elevada por la arquitectura de servicios públicos sin red privada y la política RLS permisiva documentada.

### A05 — Security Misconfiguration

**Estado:** Configuración parcialmente endurecida; existen brechas verificables.  
**Severidad:** **ALTO**.  
**Probabilidad:** Alta.  
**Impacto:** Alto.

**Evidencia:**
- `software/frontend/nginx.conf` establece `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY`, `Permissions-Policy` y `Cross-Origin-Opener-Policy`.
- El bloque `/config.local.js` repite las cabeceras y añade `Cache-Control: no-store`.
- `docs/evidencias/semana13-ola1-verificacion.md` documenta validación de sintaxis Nginx y comprobación de cabeceras en `/login.html` y `/config.local.js`.
- La misma evidencia indica que GitHub Pages no usa Nginx y que la CSP por `<meta>` quedó pendiente para una ola posterior.
- `docs/GUIA-DESPLIEGUE-RENDER.md` reconoce que los servicios Render se comunican por URLs públicas y que no hay red privada.
- La guía documenta RLS permisiva para `logs`.
- `software/infraestructura/docker-compose.yml` publica puertos de Simulator, Prometheus, Monitoring, Gateway y Frontend ligados a `127.0.0.1`, lo cual limita la exposición en el entorno local; no representa por sí solo la configuración de Render.

**Impacto:**
La falta de CSP efectiva en el frontend público aumenta la superficie frente a ciertos ataques de inyección de scripts. La exposición directa de APIs y políticas RLS permisivas pueden permitir eludir controles de acceso.

**Probabilidad:** Alta debido a brechas documentadas y a diferencias entre el Nginx local y GitHub Pages.

### A06 — Vulnerable and Outdated Components

**Estado:** Riesgo no cuantificado.  
**Severidad:** **MEDIO**.  
**Probabilidad:** Media.  
**Impacto:** Alto.

**Evidencia:**
- `software/frontend/login.html` referencia Supabase JS `2.117.1` y Font Awesome `6.4.0` desde CDN con SRI.
- `docs/evidencias/semana13-ola1-verificacion.md` documenta SRI para Supabase JS 2.117.1, Chart.js 4.4.8 y Font Awesome 6.4.0.
- `software/prediction/Dockerfile` utiliza `python:3.11.9-slim-bookworm` como imagen base.
- `software/data-processing/Dockerfile` utiliza `python:3.14-slim`.
- `software/gateway-go/Dockerfile` fija imágenes base por digest SHA256 y ejecuta `go vet`/`go test` durante build.
- `.github/workflows/ci.yml` fija las acciones de GitHub por SHA de commit.
- No se encontró en la evidencia inspeccionada un informe vigente de Dependabot, OSV, Trivy, Grype, pip-audit, npm audit u otro SCA que enumere CVE, versiones afectadas y remediación.

**Impacto:**
Una dependencia vulnerable podría permitir ejecución remota, escalamiento, divulgación de información o compromiso de la cadena de suministro.

**Probabilidad:** Media, ya que hay fijación de versiones y digests, pero no evidencia de evaluación continua de vulnerabilidades.

**Conclusión:** no se declara que las versiones citadas sean vulnerables; se declara que el riesgo no está cuantificado con un informe SCA actual.

### A07 — Identification and Authentication Failures

**Estado:** Diseño de autenticación presente; validación de seguridad operativa incompleta.  
**Severidad:** **MEDIO**.  
**Probabilidad:** Media.  
**Impacto:** Alto.

**Evidencia:**
- `software/frontend/app.js` configura Supabase Auth con `flowType: 'pkce'`, `autoRefreshToken: true`, `persistSession: true` y `detectSessionInUrl: true`.
- `authenticatedFetch` obtiene la sesión, adjunta el token Bearer y, ante 401 en solicitudes GET, intenta renovar la sesión.
- `software/gateway-go/cmd/gateway/main.go` exige `GATEWAY_AUTH_ISSUER_URI` y `GATEWAY_AUTH_JWK_SET_URI`, y construye un verificador JWKS.
- `software/gateway-go/internal/policy/routes.go` limita rutas por rol.
- `software/frontend/app.js` decodifica el payload JWT en el navegador para mostrar el rol; la autorización efectiva debe residir en el Gateway, no en ese valor de interfaz.
- No se encontró evidencia de pruebas completas de expiración, revocación, rotación de claves, sesiones concurrentes, recuperación de contraseña, rate limiting de login o bloqueo de intentos.
- No se inspeccionó el código interno del verificador JWT, por lo que no se certifican validaciones de `iss`, `aud`, `exp`, `nbf`, algoritmo y `kid`.

**Impacto:**
Una validación incorrecta del JWT o una gestión débil de sesión podría permitir suplantación, acceso no autorizado o persistencia de sesiones comprometidas.

**Probabilidad:** Media, por la integración Supabase/JWKS existente y las pruebas de autenticación no demostradas.

### A08 — Software and Data Integrity Failures

**Estado:** Controles positivos en frontend y CI; cobertura parcial de cadena de suministro.  
**Severidad:** **MEDIO**.  
**Probabilidad:** Baja/Media.  
**Impacto:** Alto.

**Evidencia:**
- `software/frontend/login.html` utiliza SRI para recursos CDN.
- `docs/evidencias/semana13-ola1-verificacion.md` registra verificación de hashes SRI estables y acciones GitHub fijadas por SHA.
- `.github/workflows/ci.yml` declara `permissions: contents: read`, ejecuta pruebas por servicio y construye imágenes sin publicarlas.
- `software/gateway-go/Dockerfile` fija imágenes base por digest SHA256.
- No se encontró evidencia de firma de imágenes, attestations, SBOM obligatoria, verificación de procedencia de artefactos o protección de ramas obligatoria.
- La evidencia de Ola 1 indica que los workflows no se ejecutaron en ese momento porque no hubo push.

**Impacto:**
Un artefacto o dependencia manipulados podrían introducir código malicioso en frontend, servicios o pipeline.

**Probabilidad:** Baja/Media por los controles de fijación/SRI, pero no se acredita una cadena de suministro firmada y verificable de extremo a extremo.

### A09 — Security Logging and Monitoring Failures

**Estado:** Correlación y métricas técnicas presentes; monitoreo de seguridad no demostrado.  
**Severidad:** **MEDIO**.  
**Probabilidad:** Media.  
**Impacto:** Medio.

**Evidencia:**
- `software/data-processing/main.py` asigna `X-Request-Id`, limita el formato de identificadores recibidos y devuelve el identificador en respuestas.
- `software/prediction/src/service/app.py` añade `X-Request-Id` y registra excepciones no controladas.
- `software/prediction/src/service/recommendations.py` expone métricas Prometheus de recomendaciones, energía y predicciones.
- No se encontró evidencia de alertas específicas para intentos de autenticación fallidos, cambios de privilegios, accesos denegados repetidos, anomalías de acceso a históricos o cambios de políticas RLS.
- No se encontró evidencia de centralización, retención protegida e inmutable de logs de auditoría ni de un procedimiento de respuesta a incidentes.

**Impacto:**
Un incidente podría no detectarse oportunamente o carecer de evidencia suficiente para reconstruir el acceso, identificar el usuario y determinar el alcance.

**Probabilidad:** Media debido a la ausencia de evidencia de monitoreo de seguridad y auditoría de acceso.

### A10 — Server-Side Request Forgery (SSRF)

**Estado:** Riesgo potencial por configuración de destinos upstream; explotación no demostrada.  
**Severidad:** **MEDIO**.  
**Probabilidad:** Media.  
**Impacto:** Alto.

**Evidencia:**
- `software/gateway-go/cmd/gateway/main.go` obtiene las URLs upstream de variables de entorno (`GATEWAY_MONITORING_BASE_URL`, `GATEWAY_DATA_PROCESSING_BASE_URL`, `GATEWAY_PREDICTION_BASE_URL`) y valida que tengan esquema HTTP/HTTPS, host y ausencia de credenciales/query.
- La validación no demuestra por sí sola una lista permitida de hosts/IP, bloqueo de loopback, redes privadas, link-local, metadata endpoints o redirecciones a destinos no confiables.
- `software/data-processing/infrastructure/adapters/input/api/routes.py` utiliza `MonitoringHttpAdapter` con URL tomada de configuración.
- `docs/GUIA-DESPLIEGUE-RENDER.md` indica que los upstreams se configuran mediante URLs públicas.
- No se encontró una prueba SSRF específica ni evidencia de filtrado de destinos/resolución DNS/revalidación de redirecciones.

**Impacto:**
Si un atacante puede influir en una URL de destino o modificar configuración, podría inducir solicitudes del servidor hacia servicios internos o endpoints de metadatos. No se encontró evidencia de que un usuario remoto controle directamente esas variables; por ello se trata como riesgo de configuración y no como SSRF explotable confirmada.

**Probabilidad:** Media, condicionada al control sobre configuración o a una ruta indirecta que permita influir en el destino.

---

## 5. Controles de seguridad positivos identificados

1. Gateway Go con tabla de rutas explícita y control de métodos/roles.
2. Validación JWT configurada mediante issuer y JWKS de Supabase.
3. Supabase Auth en frontend con flujo PKCE y renovación automática.
4. Validación tipada y límites de parámetros en Data Processing y Prediction.
5. `extra='forbid'` y restricciones numéricas en modelos Pydantic de recomendaciones.
6. Límites de tamaño de cuerpo y timeout definidos en el Gateway.
7. Nginx con cabeceras de seguridad verificadas en las rutas probadas.
8. SRI para dependencias CDN del frontend.
9. Acciones de GitHub fijadas por SHA y permisos CI `contents: read`.
10. Imágenes base fijadas por digest en Gateway Go.
11. Usuario no root en imágenes de Prediction, Data Processing y Gateway Go.
12. `executionAllowed=False` en recomendaciones, evitando que la API autorice ejecución automática.

Estos controles reducen riesgos concretos, pero no neutralizan los hallazgos de exposición de servicios, RLS o falta de evidencia de pruebas dinámicas.

---

## 6. Score global de seguridad

### 6.1 Método de cálculo

El score se calcula como una estimación de riesgo residual para las diez categorías, con igual ponderación por categoría. Se asigna un valor de riesgo:

| Severidad | Valor de riesgo |
|---|---:|
| Crítico | 4 |
| Alto | 3 |
| Medio | 2 |
| Bajo | 1 |
| Sin hallazgo evidenciado | 0 |

La puntuación de postura se calcula así:

\[
Score = 100 - \left(\frac{\sum Riesgo_i}{10 \times 4}\times100\right)
\]

Para esta evaluación se asignaron los siguientes valores: A01=3, A02=2, A03=2, A04=3, A05=3, A06=2, A07=2, A08=2, A09=2, A10=2. La suma es 23.

\[
Score = 100 - \left(\frac{23}{40}\times100\right) = 42.5
\]

**Score calculado: 42.5/100.**

**Interpretación:** postura de seguridad insuficiente, con riesgos altos en control de acceso, diseño y configuración.

> El score de 55/100 mencionado en el resumen preliminar queda reemplazado por el cálculo explícito de esta sección. El valor final del informe es **42.5/100**. No es una métrica oficial OWASP; sirve únicamente para comparar auditorías del mismo proyecto usando la misma escala.

### 6.2 Distribución de severidad

| Severidad | Categorías |
|---|---:|
| Crítico | 0 |
| Alto | 3 |
| Medio | 7 |
| Bajo | 0 |

---

## 7. Dictamen de seguridad

**Dictamen: NO SE RECOMIENDA DECLARAR EL PROYECTO SEGURO PARA EXPOSICIÓN OPERATIVA SIN VALIDACIONES ADICIONALES.**

El repositorio contiene controles importantes de autenticación, autorización en Gateway, validación de datos, integridad de dependencias frontend y endurecimiento parcial de infraestructura. No obstante, la documentación reconoce que Data Processing depende de estar detrás del Gateway, que los servicios desplegados usan URLs públicas y que la clave anon puede leer históricos debido a RLS permisiva. Esos hechos impiden considerar cerrado el riesgo de control de acceso.

La evaluación tampoco acredita pruebas de penetración, SCA, DAST, validación exhaustiva del JWT, política CSP efectiva en GitHub Pages ni monitoreo de eventos de seguridad. El score estimado de 42.5/100 refleja esta evidencia incompleta y los riesgos observados; no significa que se haya confirmado explotación.

### 7.1 Evidencia requerida para una reevaluación

- Exportación/revisión de políticas RLS de Supabase y pruebas negativas de acceso entre usuarios.
- Confirmación de que Data Processing y Prediction no son accesibles sin pasar por el Gateway o evidencia de controles equivalentes.
- Pruebas de autorización por rol y por recurso (incluyendo acceso a `hardwareId` ajeno).
- Evidencia de validación de claims JWT (`iss`, `aud`, `exp`, `nbf`, algoritmo y `kid`) y manejo de rotación JWKS.
- Informe SCA actualizado para dependencias Python, Go, JavaScript y contenedores.
- Informe DAST/penetración que cubra inyección, SSRF, autenticación, autorización y exposición de información.
- Cabeceras efectivas del sitio GitHub Pages y del Gateway desplegado.
- Evidencia de alertas y retención de logs de seguridad.

---

## 8. Fuentes técnicas inspeccionadas

- `software/gateway-go/internal/policy/routes.go`
- `software/gateway-go/cmd/gateway/main.go`
- `software/frontend/app.js`
- `software/frontend/login.html`
- `software/frontend/register.html`
- `software/frontend/nginx.conf`
- `software/data-processing/main.py`
- `software/data-processing/infrastructure/adapters/input/api/routes.py`
- `software/data-processing/infrastructure/historical_sources.py`
- `software/prediction/src/service/app.py`
- `software/prediction/src/service/recommendations.py`
- `software/infraestructura/docker-compose.yml`
- `software/prediction/Dockerfile`
- `software/data-processing/Dockerfile`
- `software/gateway-go/Dockerfile`
- `.github/workflows/ci.yml`
- `.github/workflows/pages.yml`
- `docs/GUIA-DESPLIEGUE-RENDER.md`
- `docs/evidencias/semana13-ola1-verificacion.md`

**Fin del informe.**
