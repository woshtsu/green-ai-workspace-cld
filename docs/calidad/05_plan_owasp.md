# Plan de Remediación OWASP Top 10 (2021) — Green AI Monorepo

**Documento:** `docs/calidad/05_plan_owasp.md`  
**Fecha:** 2026-11-07  
**Rol:** Arquitecto de Seguridad  
**Referencia de Entrada:** `docs/calidad/04_auditoria_owasp.md` (Hallazgos OW-01 a OW-12)  
**Alcance:** Servicios perimetrales, microservicios internos, frontend, canalizaciones de CI/CD y esquemas de persistencia.  
**Modo de operación:** Planificación arquitectónica no destructiva. Sin ejecución de comandos intrusivos.

---

## 1. Principios Rectores y Criterios de Aceptación

El presente plan de remediación establece la hoja de ruta técnica para subsanar los 12 hallazgos identificados en la auditoría de seguridad OWASP Top 10:2021. La ejecución está subordinada a las siguientes restricciones no negociables:

1. **NO romper funcionalidad existente:** Ningún cambio de seguridad debe alterar los contratos de API vigentes, las rutas perimetrales ni la estructura de datos consumida por los clientes web y microservicios.
2. **NO afectar procesos de negocio:** La ingesta de telemetría, el cálculo de métricas de eficiencia energética, las inferencias de consumo eléctrico y la emisión de recomendaciones operativas deben mantener su continuidad operativa.
3. **Mantener compatibilidad hacia atrás:** Las modificaciones en esquemas, cabeceras o filtros de seguridad deben soportar clientes actuales y flujos de despliegue en entornos locales y en la nube.
4. **Verificación obligatoria previa a integración:** Cada incremento debe superar su prueba de validación técnica, la suite de pruebas unitarias y de contrato asociada, y el smoke test del sistema.
5. **Reversibilidad garantizada:** Todo cambio debe contar con un procedimiento explícito de reversión (rollback) documentado y probado.

---

## 2. Roadmap de Remediación en Tres Olas

La remediación se organiza en tres olas de trabajo sucesivas, respetando la priorización del equipo técnico y la asignación formal de responsabilidades:

| Ola | Periodo | Alcance y Hallazgos | Responsable Principal |
|---|---|---|---|
| **Ola 1** | Semana 13 (07–09/11/2026) | Cabeceras HTTP Nginx (OW-06, OW-07), SRI en scripts externos (OW-08) y fijación de GitHub Actions por SHA (OW-10). CSP queda reservado para Ola 2. | Ricardo Porras Veli (con apoyo de Claude) |
| **Ola 2** | Sprint 7 (17–28/11/2026) | Revisión de RLS y retiro de columna password en Supabase (OW-01, OW-03), rate limiting en Gateway (OW-05), registro y métricas 401/403 (OW-12), CSP por meta etiqueta. | Administrador de Supabase (BD) / Ricardo Porras Veli (Gateway y Frontend) |
| **Ola 3** | Sprint 8 (01–12/12/2026) | Migración/mitigación de sesión en almacenamiento local (OW-09), digest SHA256 en Dockerfiles (OW-11), aislamiento de puertos locales (OW-02), retiro de contraseñas de dataset Excel (OW-04). | Ricardo Porras Veli / Equipo DevOps y Backend |

---

## 3. Plan Detallado de Remediación por Hallazgo

### OW-01: Políticas RLS permisivas en Supabase («Permitir todo»)
* **Riesgo:** Pérdida de control de acceso si clientes directos acceden a PostgREST (`/rest/v1/`) con la clave pública eludiendo las políticas de autorización RBAC del Gateway.
* **Prioridad:** Alto.
* **Impacto:** Modificación no autorizada o borrado de registros de hardware, logs de telemetría y perfiles de usuario.
* **Componentes afectados:** Base de datos externa Supabase (tablas `hardware`, `logs`, `usuario`) y adaptador `software/data-processing/infrastructure/adapters/input/supabase_historical_logs_adapter.py`.
* **Estrategia de mitigación:** El administrador de Supabase revisará y eliminará las directivas generales `cmd: ALL` concedidas al rol `public`. Se implementarán políticas RLS específicas por comando: lectura permitida a roles autenticados (`authenticated`) y escrituras restringidas al rol de servicio (`service_role`) o con validación de pertenencia (`auth.uid() = usuario_id`).
* **Estrategia de validación:** Ejecutar en el editor SQL de Supabase la consulta a catálogo:
  ```sql
  SELECT schemaname, tablename, policyname, roles, cmd, qual 
  FROM pg_policies 
  WHERE tablename IN ('hardware', 'logs', 'usuario');
  ```
  Confirmar que ninguna directiva contenga `cmd = 'ALL'` combinado con `roles = '{public}'` y `qual = 'true'`.
* **Estrategia de rollback:** Reaplicar el script de políticas previo mediante sentencia DDL `ALTER POLICY` o restaurar el respaldo de políticas almacenado en el repositorio de scripts de administración.
* **Responsable:** Administrador / Dueño de base de datos Supabase.
* **Fecha:** Sprint 7 (17–28/11/2026) — Ola 2.

---

### OW-02: Exposición de puertos de microservicios internos en Docker Compose local
* **Riesgo:** Conexión directa no autorizada a microservicios internos (`monitoring:18080`, `simulator:18000`) desde la red local o interfaces compartidas sin pasar por la inspección JWT del Gateway.
* **Prioridad:** Medio.
* **Impacto:** Extracción de métricas internas o manipulación de la simulación omitiendo el control perimetral.
* **Componentes afectados:** `software/infraestructura/docker-compose.yml:L13-L44`.
* **Estrategia de mitigación:** Configurar el enlace de puertos de `monitoring` y `simulator` restringiéndolo expresamente a la dirección de bucle local `127.0.0.1` o eliminar el mapeo de puertos hacia el host para aquellos servicios que solo requieren comunicación inter-contenedor dentro de la red interna de Docker Compose.
* **Estrategia de validación:** Ejecutar `docker compose ps` y comprobar que las interfaces publicadas escuchen exclusivamente en `127.0.0.1:18080` y `127.0.0.1:18000`. Validar la denegación intentando una conexión HTTP desde una IP distinta a localhost.
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre `software/infraestructura/docker-compose.yml` para restablecer la configuración de puertos anterior.
* **Responsable:** Ricardo Porras Veli / Equipo de Infraestructura.
* **Fecha:** Sprint 8 (01–12/12/2026) — Ola 3.

---

### OW-03: Presencia de columna password en texto plano en esquema de base de datos
* **Riesgo:** Exposición involuntaria de contraseñas de usuarios en texto claro si la columna fue provisionada y poblada en la base de datos externa de Supabase.
* **Prioridad:** Alto.
* **Impacto:** Compromiso total de la confidencialidad de credenciales de usuario y riesgo de suplantación de identidad.
* **Componentes afectados:** Base de datos Supabase (tabla `usuario`) y referencia documental `software/simulator/docs/assets/esquema-verificado.json:L400-L412`.
* **Estrategia de mitigación:** El administrador de Supabase ejecutará un script de migración para eliminar definitivamente la columna `password` mediante `ALTER TABLE usuario DROP COLUMN IF EXISTS password;`, asegurando que toda autenticación utilice exclusivamente `password_hash` o el mecanismo gestionado de Supabase Auth.
* **Estrategia de validación:** Ejecutar en PostgreSQL la verificación de esquema:
  ```sql
  SELECT column_name, data_type 
  FROM information_schema.columns 
  WHERE table_name = 'usuario' AND column_name = 'password';
  ```
  Comprobar que retorne 0 registros. Posteriormente verificar que el inicio de sesión siga operando con normalidad.
* **Estrategia de rollback:** En caso de contingencia con dependencias legadas no detectadas, restaurar temporalmente la columna con `ALTER TABLE usuario ADD COLUMN password varchar(255);`.
* **Responsable:** Administrador / Dueño de base de datos Supabase.
* **Fecha:** Sprint 7 (17–28/11/2026) — Ola 2.

---

### OW-04: Contraseñas sintéticas legibles en archivo Excel versionado
* **Riesgo:** Divulgación de contraseñas de referencia y eventual reutilización accidental en entornos reales de pruebas o staging.
* **Prioridad:** Bajo.
* **Impacto:** Riesgo bajo al tratarse de datos sintéticos, pero contrario a los estándares de higiene criptográfica en repositorios de código.
* **Componentes afectados:** `software/data-processing/datasets/BD_GreenAi.xlsx` (hoja `Usuarios`).
* **Estrategia de mitigación:** Abrir el dataset Excel y ofuscar o remover la columna de contraseñas en texto claro reemplazándola por valores no funcionales (`[REDACTED]`), actualizando los scripts de inicialización que consumen dicho archivo para no requerir ese campo.
* **Estrategia de validación:** Inspeccionar visualmente `BD_GreenAi.xlsx` para asegurar la ausencia de cadenas de texto plano de contraseñas y ejecutar la suite de pruebas de Data Processing (`pytest tests/`) para verificar que la carga de datos se complete sin fallos.
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre `software/data-processing/datasets/BD_GreenAi.xlsx`.
* **Responsable:** Ricardo Porras Veli / Equipo Data Processing.
* **Fecha:** Sprint 8 (01–12/12/2026) — Ola 3.

---

### OW-05: Ausencia de Rate Limiting en Gateway para endpoints de cómputo intensivo
* **Riesgo:** Saturación de recursos de CPU y memoria en los microservicios de predicción y recomendaciones ante ráfagas sostenidas de solicitudes maliciosas o accidentales.
* **Prioridad:** Medio.
* **Impacto:** Denegación de servicio (DoS) e indisponibilidad del subsistema de analítica para usuarios legítimos.
* **Componentes afectados:** `software/gateway/src/main/resources/application.yaml`, `software/gateway-go/internal/httpapi/server.go`.
* **Estrategia de mitigación:** Configurar filtros de limitación de tasa basados en Token Bucket por IP y por token autenticado en el Gateway Go y RequestRateLimiter en Spring Gateway. Se definirán cotas de 10 peticiones por segundo con ráfaga máxima de 20 peticiones para `/api/prediction/v1/predictions` y `/api/recommendations/v1/recommendations`.
* **Estrategia de validación:** Ejecutar una prueba automatizada con cliente HTTP concurrente enviando 30 peticiones consecutivas al endpoint de inferencia y validar que las solicitudes excedentes reciban respuesta HTTP `429 Too Many Requests`. Correr las pruebas de integración del Gateway para confirmar que peticiones bajo la cota operen sin retraso.
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre los archivos de configuración y middleware del Gateway.
* **Responsable:** Ricardo Porras Veli (con apoyo de Claude).
* **Fecha:** Sprint 7 (17–28/11/2026) — Ola 2.

---

### OW-06: Ausencia de cabeceras de seguridad HTTP en Nginx (X-Frame-Options, Permissions-Policy)
* **Riesgo:** Exposición a ataques de Clickjacking por incrustación en marcos (`iframe`) no autorizados y acceso sin restricción a capacidades del navegador (cámara, micrófono, geolocalización).
* **Prioridad:** Medio.
* **Impacto:** Secuestro de clics de usuarios autenticados e incremento de la superficie de explotación de vulnerabilidades en el cliente web.
* **Componentes afectados:** `software/frontend/nginx.conf:L1-L10`.
* **Estrategia de mitigación:** En Ola 1, agregar en el bloque `server` de `software/frontend/nginx.conf` las directivas:
  - `add_header X-Frame-Options "DENY" always;`
  - `add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;`
  - `add_header Cross-Origin-Opener-Policy "same-origin" always;`
  La política de Content-Security-Policy (CSP) queda reservada para Ola 2 para ser implementada homogéneamente mediante meta etiqueta HTML, dado que GitHub Pages opera como servidor estático sin capa Nginx.
* **Estrategia de validación:** Levantar el servicio frontend o validar sintaxis con `nginx -t`, realizar petición HTTP mediante `curl -I http://127.0.0.1:13001/` y comprobar la presencia exacta de las tres cabeceras. Ejecutar `node --test tests/*.test.cjs` en `software/frontend` (48 pruebas pasando).
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre `software/frontend/nginx.conf`.
* **Responsable:** Ricardo Porras Veli (con apoyo de Claude).
* **Fecha:** Semana 13 (07–09/11/2026) — Ola 1.

---

### OW-07: Sobrescritura de cabeceras padre en bloque location de /config.local.js en Nginx
* **Riesgo:** Peticiones directas a `/config.local.js` se entregan sin cabeceras defensivas debido a que la directiva `add_header Cache-Control "no-store"` dentro de `location = /config.local.js` invalida las cabeceras declaradas en el nivel superior `server`.
* **Prioridad:** Bajo.
* **Impacto:** Falta de protección `X-Content-Type-Options: nosniff` y `X-Frame-Options` sobre el archivo de configuración en navegadores legados.
* **Componentes afectados:** `software/frontend/nginx.conf:L8-L10`.
* **Estrategia de mitigación:** Replicar explícitamente dentro del bloque `location = /config.local.js` todas las directivas `add_header` de seguridad heredadas (`X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy`, `Cross-Origin-Opener-Policy`), asegurando que convivan con `Cache-Control "no-store"`.
* **Estrategia de validación:** Ejecutar `curl -I http://127.0.0.1:13001/config.local.js` y confirmar en los encabezados devueltos la presencia simultánea de `Cache-Control: no-store` y de las 5 cabeceras de seguridad. Ejecutar la suite de pruebas del frontend (`node --test tests/*.test.cjs`).
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre `software/frontend/nginx.conf`.
* **Responsable:** Ricardo Porras Veli (con apoyo de Claude).
* **Fecha:** Semana 13 (07–09/11/2026) — Ola 1.

---

### OW-08: Inclusión de scripts externos desde CDN sin Subresource Integrity (SRI)
* **Riesgo:** Ejecución de código malicioso en el contexto del navegador de los usuarios en caso de alteración o compromiso de paquetes en los CDNs jsDelivr o cdnjs.
* **Prioridad:** Medio.
* **Impacto:** Vulnerabilidad de ejecución cruzada (XSS) y alteración de los flujos de autenticación e interfaz.
* **Componentes afectados:** `software/frontend/login.html:L10-L60`, `software/frontend/index.html:L10-L20`.
* **Estrategia de mitigación:** Incorporar los atributos `integrity="sha384-..."` y `crossorigin="anonymous"` en todas las etiquetas `<script>` y `<link>` externas, fijando estrictamente la versión inmutable de `@supabase/supabase-js@2.117.1` y de las hojas de estilo de FontAwesome.
* **Estrategia de validación:** Abrir `login.html` e `index.html` en navegador y verificar en la consola de herramientas de desarrollo que los recursos carguen sin advertencias de integridad. Ejecutar la suite completa de pruebas unitarias de frontend (`node --test tests/*.test.cjs`).
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre `software/frontend/login.html` y `software/frontend/index.html`.
* **Responsable:** Ricardo Porras Veli (con apoyo de Claude).
* **Fecha:** Semana 13 (07–09/11/2026) — Ola 1.

---

### OW-09: Persistencia del token de sesión Supabase en localStorage
* **Riesgo:** Si ocurre una inyección de script (XSS) en la aplicación cliente, el token de acceso JWT almacenado en `localStorage` puede ser exfiltrado mediante JavaScript accesible por el DOM.
* **Prioridad:** Medio.
* **Impacto:** Secuestro de sesión autenticada hasta la expiración del token.
* **Componentes afectados:** `software/frontend/app.js:L17-L25`.
* **Estrategia de mitigación:** Evaluar la transición hacia almacenamiento de tokens en memoria de aplicación con rotación automática mediante PKCE y refresco silencioso, o intermediación a través de cookies seguras con directivas `HttpOnly`, `Secure` y `SameSite=Strict`. Como fase previa, reducir la vigencia del token de acceso y forzar expiración estricta.
* **Estrategia de validación:** Validar los flujos de inicio de sesión, navegación protegida, expiración forzada y cierre de sesión en `app.js`. Ejecutar `node --test tests/*.test.cjs` para verificar que el comportamiento del cliente web no presente regresiones.
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre `software/frontend/app.js`.
* **Responsable:** Ricardo Porras Veli / Equipo Frontend.
* **Fecha:** Sprint 8 (01–12/12/2026) — Ola 3.

---

### OW-10: Acciones de GitHub Actions referenciadas con tags mutables
* **Riesgo:** Modificación inadvertida o maliciosa del código de una acción de GitHub de terceros si su etiqueta flotante (`@v4`, `@v5`) es actualizada upstream en el repositorio público.
* **Prioridad:** Bajo.
* **Impacto:** Ejecución de código no confiable dentro del entorno de compilación, empaquetado y despliegue del proyecto.
* **Componentes afectados:** `.github/workflows/ci.yml:L23-L65`, `.github/workflows/pages.yml:L38-L45`.
* **Estrategia de mitigación:** Sustituir los tags de versión mutables por los hashes SHA de confirmación inmutables de 40 caracteres para cada acción utilizada (`actions/checkout`, `actions/setup-node`, `actions/setup-python`, `actions/setup-go`, `actions/setup-java`, `actions/deploy-pages`), manteniendo el nombre semántico original en un comentario inline (ejemplo: `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2`).
* **Estrategia de validación:** Revisar el diff de workflows y comprobar que la canalización automatizada de CI ejecute todos sus pasos con éxito en la siguiente ejecución sin errores de referencia de acciones.
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre los archivos de flujo en `.github/workflows/`.
* **Responsable:** Ricardo Porras Veli (con apoyo de Claude).
* **Fecha:** Semana 13 (07–09/11/2026) — Ola 1.

---

### OW-11: Imágenes base de Docker en microservicios sin fijación por digest SHA256
* **Riesgo:** Compilaciones no deterministas al descargar imágenes base de Docker que pueden incorporar cambios o vulnerabilidades imprevistas entre compilaciones locales y remotas.
* **Prioridad:** Bajo.
* **Impacto:** Discrepancia en el entorno de ejecución y falta de reproducibilidad estricta de las imágenes empaquetadas.
* **Componentes afectados:** Dockerfiles en `software/gateway/Dockerfile`, `software/monitoring/Dockerfile`, `software/data-processing/Dockerfile`, `software/prediction/Dockerfile`, `software/simulator/Dockerfile` y `software/frontend/Dockerfile`.
* **Estrategia de mitigación:** Anclar la cláusula `FROM` de cada Dockerfile con el hash inmutable `@sha256:...` correspondiente a su versión estable verificada, homologando el patrón ya implementado en `software/gateway-go/Dockerfile`.
* **Estrategia de validación:** Ejecutar `docker compose build --no-cache` y validar que todos los contenedores construyan exitosamente sin fallos de capas. Ejecutar la prueba de integración `python software/infraestructura/smoke.py` (14/14 comprobaciones).
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre los Dockerfiles modificados.
* **Responsable:** Ricardo Porras Veli / Equipo DevOps.
* **Fecha:** Sprint 8 (01–12/12/2026) — Ola 3.

---

### OW-12: Ausencia de registros de auditoría y métricas para peticiones 401/403 en Gateway
* **Riesgo:** Dificultad para detectar ataques de fuerza bruta, escaneo no autorizado de endpoints o anomalías de autorización en tiempo de ejecución.
* **Prioridad:** Medio.
* **Impacto:** Falta de visibilidad forense y retraso en la detección de incidentes de seguridad perimetral.
* **Componentes afectados:** `software/gateway/src/main/java/pe/edu/continental/greenai/gateway/SecurityConfiguration.java:L81-L87`, `software/gateway-go/internal/httpapi/server.go:L118-L131`, `software/infraestructura/prometheus/alerts.yml`.
* **Estrategia de mitigación:** Incorporar en los interceptores de seguridad del Gateway Java y Gateway Go la emisión de registros estructurados (nivel WARN) con campos normalizados: IP origen, timestamp RFC3339, ruta solicitada, método HTTP y motivo del rechazo. Exponer un contador de métrica Prometheus `gateway_security_rejected_requests_total` con etiquetas de ruta y código de respuesta (401 y 403), agregando una alerta preventiva en Prometheus ante picos anormales de rechazos.
* **Estrategia de validación:** Emitir peticiones sin token hacia `/api/monitoring/v1/metrics/cluster-summary` esperando código 401 y con token de rol `VIEWER` hacia `POST /api/prediction/v1/predictions` esperando código 403. Constatar que se emita la traza estructurada en los logs del Gateway y que la métrica incremente en el endpoint `/actuator/prometheus` o `/metrics`. Ejecutar las suites de prueba de contrato del Gateway.
* **Estrategia de rollback:** Ejecutar `git revert <commit>` sobre las clases y módulos de seguridad del Gateway.
* **Responsable:** Ricardo Porras Veli / Equipo Backend.
* **Fecha:** Sprint 7 (17–28/11/2026) — Ola 2.

---

## 4. Orden Recomendado de Ejecución

Para minimizar riesgos de regresión y respetar las dependencias entre componentes, se define la siguiente secuencia de ejecución:

```
[Ola 1: Semana 13 (07–09/11/2026)]
  1. OW-10: Fijar GitHub Actions por SHA en .github/workflows/*.yml
  2. OW-08: Añadir SRI y crossorigin en scripts CDN de frontend (login.html, index.html)
  3. OW-06 y OW-07: Configurar cabeceras en software/frontend/nginx.conf y replicar en /config.local.js
  --> Validar: node --test tests/*.test.cjs (48 tests) y CI en verde

[Ola 2: Sprint 7 (17–28/11/2026)]
  4. OW-01: Administrador revisa y restringe políticas RLS en Supabase
  5. OW-03: Administrador elimina columna password en tabla usuario de Supabase
  6. OW-06 (Fase CSP): Incorporar CSP restrictivo por meta etiqueta en index.html y login.html
  7. OW-12: Implementar registro de auditoría y métricas de seguridad 401/403 en Gateway
  8. OW-05: Implementar rate limiting en endpoints de inferencia del Gateway
  --> Validar: pg_policies, pruebas de contrato de Gateway Java y Go, smoke test 14/14

[Ola 3: Sprint 8 (01–12/12/2026)]
  9. OW-04: Remover contraseñas en claro de BD_GreenAi.xlsx
  10. OW-02: Restringir exposición de puertos en docker-compose.yml a 127.0.0.1
  11. OW-11: Fijar digests SHA256 en Dockerfiles de microservicios
  12. OW-09: Evaluar y migrar almacenamiento de sesión de localStorage a esquema seguro
  --> Validar: docker compose build --no-cache, smoke test 14/14, pruebas unitarias globales
```

---

## 5. Riesgos de Implementación y Medidas Preventivas

| Riesgo de Implementación | Probabilidad | Impacto | Medida Preventiva y Mitigación |
|---|---|---|---|
| **Bloqueo de scripts externos por hash SRI incorrecto** | Baja | Alto | Calcular el hash SHA-384 directamente del archivo descargado con `openssl dgst -sha384 -binary <file> \| openssl base64 -A` y verificar en consola de navegador antes de commit. |
| **Pérdida de cabeceras en Nginx por directivas hijas** | Media | Medio | Replicar todas las cabeceras de seguridad dentro de bloques `location` que declaren `add_header` propio (`/config.local.js`). |
| **Bloqueo de recursos legítimos por Content Security Policy** | Media | Alto | Implementar CSP en Ola 2 utilizando `<meta http-equiv="Content-Security-Policy">` tras auditar todos los orígenes de scripts, fuentes y conexiones utilizados en producción y GitHub Pages. |
| **Denegación de servicio a clientes legítimos por Rate Limiting restrictivo** | Media | Medio | Calibrar cotas de Rate Limiting con margen suficiente (10 req/s con burst de 20) y probar bajo carga con las suites de contrato existentes. |
| **Interrupción de ingesta por ajuste de RLS en Supabase** | Media | Crítico | Validar previamente que el adaptador `supabase_historical_logs_adapter.py` autentique con credenciales que posean el rol autorizado antes de revocar políticas abiertas. |
| **Fallo en scripts de migración o seeding por ausencia de columna password** | Baja | Medio | Comprobar que ningún código activo consuma el campo `password` antes de ejecutar la sentencia `DROP COLUMN` en la base de datos. |
| **Incompatibilidad de imágenes Docker al anclar digests** | Baja | Medio | Verificar previamente que los digests correspondan a la arquitectura multi-plataforma requerida (`linux/amd64` y `linux/arm64`). |

---

## 6. Estrategia para Preservar la Funcionalidad y Pruebas Requeridas

Ningún cambio del plan de remediación será promovido a la rama de integración sin superar la batería de pruebas automatizadas del proyecto:

### 1. Suite de Pruebas de Frontend (48 pruebas)
* **Comando:**
  ```powershell
  node --test tests/*.test.cjs
  ```
* **Ubicación:** `software/frontend/`
* **Criterio de éxito:** 48 tests pasados, 0 fallos. Verifica el parser de configuración dinámica, renderizado de gráficos, formateo de métricas y validación de formularios sin regresiones.

### 2. Prueba End-to-End Smoke Test (14/14 comprobaciones)
* **Comando:**
  ```powershell
  python software/infraestructura/smoke.py
  ```
* **Ubicación:** `software/infraestructura/`
* **Criterio de éxito:** 14/14 comprobaciones superadas. Valida la disponibilidad de la interfaz frontend (puerto 13001), los endpoints del Gateway (puerto 18080/8080), la salud de los microservicios de monitoreo, procesamiento y predicción, y el flujo completo de telemetría e inferencia.

### 3. Suites de Contrato y Seguridad del Gateway
* **Gateway Java (Spring Cloud Gateway):**
  ```powershell
  ./mvnw test
  ```
  *Ubicación:* `software/gateway/`  
  *Criterio de éxito:* 11/12 tests superados (línea base verificada). Valida reglas de autorización RBAC (`OPERATOR`, `ADMIN`, `VIEWER`), validación de firmas JWT y rechazo de peticiones anónimas.
* **Gateway Go:**
  ```powershell
  go test ./...
  ```
  *Ubicación:* `software/gateway-go/`  
  *Criterio de éxito:* Cobertura completa de rutas, validación de JWKS, rechazo de algoritmos inseguros y verificación de cabeceras `X-Request-Id`.

### 4. Suites de Soporte de Microservicios
* **Data Processing Service:** `pytest tests/` en `software/data-processing/` (121 tests pasados).
* **Prediction Service:** `pytest` en `software/prediction/` (100 tests pasados).
* **Monitoring Service:** `./mvnw test` en `software/monitoring/` (112 tests pasados).
