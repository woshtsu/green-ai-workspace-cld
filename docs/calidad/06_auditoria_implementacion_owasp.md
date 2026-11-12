# 06_Auditoria_Implementacion_OWASP.md — Auditoria de Implementacion de Seguridad (OWASP Top 10)

**Proyecto:** Green AI (Optimizacion Energetica y Capacidad en Data Centers con Machine Learning)  
**Institucion:** Universidad Continental — Taller de Proyectos 1 (2026-20)  
**Rol:** Auditor Independiente de Seguridad de Software  
**Fecha de Auditoria:** 2026-11-07  
**Rama Base de Evaluacion:** `test` (commit `d24d86f` y arbol de trabajo)  
**Entradas Evaluadas:**  
- `docs/calidad/04_auditoria_owasp.md` (Linea base de seguridad inicial: 80.5 / 100)  
- `docs/calidad/05_plan_owasp.md` (Plan de remediacion en tres olas)  
- `docs/evidencias/semana13-ola1-verificacion.md` (Evidencia tecnica de ejecucion de Ola 1)  
- Archivos fuente: `software/frontend/nginx.conf`, `software/frontend/*.html`, `.github/workflows/*.yml`  
**Marco de Referencia:** OWASP Top 10:2021 y estandares de auditoria independiente de seguridad.

---

## 1. Resumen Ejecutivo y Alcance

La presente auditoria tecnica independiente verifica la aplicacion de las remediaciones de seguridad programadas para la **Ola 1 (Semana 13)** conforme a la hoja de ruta establecida en `docs/calidad/05_plan_owasp.md`.

### Criterios de Auditoria Aplicados:
1. **Comprobacion basada en evidencia:** No se asume ninguna correccion por declaracion documental; cada control fue inspeccionado directamente en el codigo fuente.
2. **Tratamiento de compromisos futuros:** Los hallazgos programados para las Olas 2 y 3 figuran formalmente como «No corregida (planificada para <fecha>)», distinguiendo el calendario de ejecucion de un fallo de seguridad.
3. **Control de regresiones:** Se constato que las modificaciones defensivas no introdujeran comportamientos anómalos en el frontend ni en los flujos de integracion continua.
4. **Recalculo metodologico:** Se recalculo el puntaje de seguridad global empleando el mismo modelo de ponderacion aditiva por categoria (0 a 10 puntos por cada riesgo OWASP) utilizado en `docs/calidad/04_auditoria_owasp.md:L292-L325`.

---

## 2. Estado de Remediacion de Hallazgos (OW-01 a OW-12)

A continuacion se dictamina el estado individual de cada una de las 12 vulnerabilidades registradas en la linea base:

| ID | Categoria OWASP | Descripcion del Hallazgo | Estado Post Ola 1 | Responsable y Plazo |
|---|---|---|:---:|---|
| **OW-01** | A01: Broken Access Control | Riesgo de politicas RLS permisivas («Permitir todo») en Supabase | **No corregida (planificada para Sprint 7, 17–23/11/2026 — Ola 2)** | Administrador de BD Supabase |
| **OW-02** | A01: Broken Access Control | Puertos de monitoring (18080) y simulator (18000) expuestos en local | **No corregida (planificada para Sprint 8, 24–30/11/2026 — Ola 3)** | Ricardo Porras / Infraestructura |
| **OW-03** | A02: Cryptographic Failures | Columna `password` en texto plano en la tabla `usuario` en Supabase | **No corregida (planificada para Sprint 7, 17–23/11/2026 — Ola 2)** | Administrador de BD Supabase |
| **OW-04** | A02: Cryptographic Failures | Contraseñas sinteticas legibles en archivo Excel `BD_GreenAi.xlsx` | **No corregida (planificada para Sprint 8, 24–30/11/2026 — Ola 3)** | Ricardo Porras / Data Processing |
| **OW-05** | A04: Insecure Design | Ausencia de Rate Limiting en Gateway para inferencia y recomendaciones | **No corregida (planificada para Sprint 7, 17–23/11/2026 — Ola 2)** | Ricardo Porras Veli |
| **OW-06** | A05: Security Misconfiguration | Ausencia de cabeceras HTTP de proteccion web en Nginx | **Parcialmente corregida** (Implementadas cabeceras base; CSP reservada para Ola 2) | Ricardo Porras Veli |
| **OW-07** | A05: Security Misconfiguration | Sobrescritura de cabeceras en bloque `location = /config.local.js` | **Corregida** (Cabeceras replicadas explicitamente con no-store) | Ricardo Porras Veli |
| **OW-08** | A06: Vulnerable Components | Inclusion de scripts JS y CSS de CDN en frontend sin hash SRI | **Corregida** (Atributos integrity y crossorigin en las 6 paginas HTML) | Ricardo Porras Veli |
| **OW-09** | A07: Identification Failures | Persistencia del token de sesion Supabase en `localStorage` | **No corregida (planificada para Sprint 8, 24–30/11/2026 — Ola 3)** | Ricardo Porras / Frontend |
| **OW-10** | A08: Integrity Failures | Acciones de GitHub CI referenciadas con tags mutables (`@v4`, `@v5`) | **Corregida** (100 % de acciones ancladas a commit SHA inmutable) | Ricardo Porras Veli |
| **OW-11** | A08: Integrity Failures | Imagenes base Docker de microservicios sin fijacion por digest SHA256 | **No corregida (planificada para Sprint 8, 24–30/11/2026 — Ola 3)** | Ricardo Porras / DevOps |
| **OW-12** | A09: Security Logging | Ausencia de registros y metricas de auditoria 401/403 en Gateway | **No corregida (planificada para Sprint 7, 17–23/11/2026 — Ola 2)** | Ricardo Porras / Backend |

---

## 3. Evidencias Tecnicas Observadas en el Repositorio

Se documenta el analisis forense y la evidencia verificada para cada uno de los cambios aplicados en la Ola 1:

### 3.1. OW-06: Cabeceras Defensivas HTTP en Nginx
- **Archivo:** `software/frontend/nginx.conf:L8-L12`
- **Evidencia verificada:**
  ```nginx
  add_header X-Content-Type-Options nosniff always;
  add_header Referrer-Policy no-referrer always;
  add_header X-Frame-Options DENY always;
  add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()" always;
  add_header Cross-Origin-Opener-Policy same-origin always;
  ```
- **Analisis de efectividad:** Se bloquea el ataque de Clickjacking mediante `X-Frame-Options: DENY`, se desactivan APIs intrusivas del navegador mediante `Permissions-Policy` y se aísla el contexto de navegacion con `Cross-Origin-Opener-Policy: same-origin`.
- **Estado de completitud:** Parcialmente corregida. La cabecera `Content-Security-Policy` (CSP) no fue incluida en Nginx por diseño del plan, ya que su despliegue definitivo se hara en la Ola 2 mediante etiqueta `<meta>` para garantizar cobertura identica en el hosting estatico de GitHub Pages (`docs/calidad/05_plan_owasp.md:L124`).

### 3.2. OW-07: Preservacion de Cabeceras en Bloque `/config.local.js`
- **Archivo:** `software/frontend/nginx.conf:L13-L20`
- **Evidencia verificada:**
  ```nginx
  location = /config.local.js {
      add_header Cache-Control "no-store" always;
      add_header X-Content-Type-Options nosniff always;
      add_header Referrer-Policy no-referrer always;
      add_header X-Frame-Options DENY always;
      add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()" always;
      add_header Cross-Origin-Opener-Policy same-origin always;
  }
  ```
- **Analisis de efectividad:** Se neutraliza la caracteristica de Nginx donde un bloque hijo descarta todas las directivas `add_header` del bloque padre al declarar un `add_header` propio. Se confirma que peticiones directas a `/config.local.js` retornan tanto `Cache-Control: no-store` como las 5 cabeceras de proteccion (`docs/evidencias/semana13-ola1-verificacion.md:L21`).

### 3.3. OW-08: Subresource Integrity (SRI) en Recursos Externos de CDN
- **Archivos verificados:** Las 6 paginas HTML del directorio `software/frontend/`.
- **Evidencias verificadas:**
  1. `software/frontend/index.html:L10`: Font Awesome 6.4.0 CSS con `integrity="sha384-iw3OoTErCYJJB9mCa8LNS2hbsQ7M3C0EpIsO/H5+EGAkPGc6rk+V8i04oW/K5xq0"` y `crossorigin="anonymous"`.
  2. `software/frontend/login.html:L10`: Font Awesome con el mismo hash SRI.
  3. `software/frontend/login.html:L60`: Supabase JS 2.117.1 con `integrity="sha384-q36VSR1ktH2hgqgm+0LDeyqPW8CyZHSxfDSttSPm5ReOJzB+sYThmh7D4fE+jWTs"` y `crossorigin="anonymous"`.
  4. `software/frontend/register.html:L11` y `software/frontend/register.html:L73`: Font Awesome y Supabase JS con sus respectivos hashes SRI y `crossorigin="anonymous"`.
  5. `software/frontend/dashboard.html:L298-L299`: Supabase JS y Chart.js 4.4.8 con `integrity="sha384-T/4KgSWuZEPozpPz7rnnp/5lDSnpY1VPJCojf1S81uTHS1E38qgLfMgVsAeRCWc4"` y `crossorigin="anonymous"`.
  6. `software/frontend/network.html:L133`: Supabase JS con hash SRI y `crossorigin="anonymous"`.
  7. `software/frontend/flows.html:L97`: Supabase JS con hash SRI y `crossorigin="anonymous"`.
- **Analisis de efectividad:** Todos los scripts ejecutables cargados desde redes CDN públicas (`cdn.jsdelivr.net`) y las hojas de estilo de terceros (`cdnjs.cloudflare.com`) se encuentran estrictamente protegidos contra alteraciones no autorizadas o envenenamiento de paquetes.

### 3.4. OW-10: Anclaje de Acciones de CI por Commit SHA Inmutable
- **Archivos verificados:** `.github/workflows/ci.yml` y `.github/workflows/pages.yml`.
- **Evidencias verificadas:**
  - En `.github/workflows/ci.yml`:
    - `actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4` (`ci.yml:L23,L32,L43,L53,L63,L72`)
    - `actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4` (`ci.yml:L24`)
    - `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5` (`ci.yml:L33,L44`)
    - `actions/setup-go@40f1582b2485089dde7abd97c1529aa768e1baff # v5` (`ci.yml:L54`)
    - `actions/setup-java@cf277c60eb25467037889841efdb72551f06f6c3 # v4` (`ci.yml:L64`)
  - En `.github/workflows/pages.yml`:
    - `actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4` (`pages.yml:L38,L40`)
    - `actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4` (`pages.yml:L42`)
    - `actions/configure-pages@983d7736d9b0ae728b81ab479565c72886d7745b # v5` (`pages.yml:L79`)
    - `actions/upload-pages-artifact@7b1f4a764d45c48632c6b24a0339c27f5614fb0b # v4` (`pages.yml:L80`)
    - `actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e # v4` (`pages.yml:L83`)
- **Analisis de efectividad:** Se comprobo que no subsiste ninguna etiqueta de version flotante (`@v4`, `@v5`). Las 16 referencias `uses:` en las canalizaciones de GitHub Actions estan ancladas a hashes SHA-1 exactos de 40 caracteres con su version semantica original preservada como comentario inline.

---

## 4. Evaluacion de Nuevas Vulnerabilidades o Controles Incompletos

Durante la auditoria independiente se identificaron las siguientes observaciones tecnicas sobre los controles implementados:

1. **Excepcion de SRI en Hojas de Estilo de Google Fonts:**
   - En `software/frontend/index.html:L9`, `login.html:L9` y `register.html:L10`, se incluye la hoja de estilos de Google Fonts:
     `<link href="https://fonts.googleapis.com/css2?family=Inter:...&family=Fira+Code:...&display=swap" rel="stylesheet">` sin atributo `integrity`.
   - *Dictamen del auditor:* No se clasifica como vulnerabilidad introducida ni como control fallido. Google Fonts genera el archivo CSS de forma dinamica variando el contenido segun la cabecera `User-Agent` del cliente, lo que hace inviable el uso de un hash estatico sin romper la carga en navegadores heterogéneos. Como buena practica para entornos de alta seguridad (air-gap), se recomienda en futuras fases alojar las fuentes tipograficas WOFF2 directamente en el repositorio local.
2. **Postergacion controlada de Content-Security-Policy (CSP):**
   - La cabecera CSP no fue incorporada en `software/frontend/nginx.conf`.
   - *Dictamen del auditor:* Conforme con la estrategia no destructiva de `docs/calidad/05_plan_owasp.md:L124`. Dado que GitHub Pages sirve el frontend sin pasar por Nginx, implementar CSP en el servidor web habria dejado desprotegido el entorno desplegado en nube. La implementacion homogenea mediante `<meta http-equiv="Content-Security-Policy">` en Ola 2 asegura cobertura en ambos entornos.
3. **Validacion de Acciones de CI sin SHA:**
   - Se reviso la totalidad de archivos en `.github/workflows/`. No existe ninguna accion de terceros referenciada sin commit SHA. Cumplimiento estricto al 100 %.

---

## 5. Analisis de Regresiones

Se inspecciono si las remediaciones de seguridad introdujeron fallos funcionales:
- **Suite de Pruebas de Frontend:** La ejecucion de `node --test tests/*.test.cjs` arrojó **48 pruebas pasadas de 48 (0 fallos)** (`docs/evidencias/semana13-ola1-verificacion.md:L19`).
- **Carga de Recursos en Navegador:** Se verifico que la inclusion de hashes SRI no bloquee la descarga de scripts por discrepancia criptografica (`docs/evidencias/semana13-ola1-verificacion.md:L22`). Tanto `window.supabase` como `window.Chart` se inicializan correctamente.
- **Sintaxis de Configuracion Nginx:** Validada mediante `docker run ... nginx -t` con resultado satisfactorio (`syntax is ok`, `test is successful`) (`docs/evidencias/semana13-ola1-verificacion.md:L20`).
- **Microservicios de Backend:** Intactos. No hubo modificaciones en ningun microservicio de backend.

---

## 6. Recalculo Metodologico del Score de Seguridad

Se recalcula el Score Global de Seguridad aplicando la metodologia formal de `docs/calidad/04_auditoria_owasp.md:L292-L325`, sobre un total de 100 puntos (10 puntos maximos por categoria OWASP Top 10):

### Desglose por Categoria Post Ola 1:

1. **A01: Broken Access Control (Puntuacion: 7.0 / 10)**  
   *Sin cambio.* Gateway RBAC excelente (+9.0), pero persisten el riesgo latente de RLS permisivo en Supabase (`OW-01`, -2.0) y la exposicion de puertos locales (`OW-02`, -1.0).
2. **A02: Cryptographic Failures (Puntuacion: 7.5 / 10)**  
   *Sin cambio.* Criptografia JWT/TLS robusta (+9.0), pero persisten el riesgo de columna `password` en el snapshot (`OW-03`, -2.0) y contraseñas sinteticas en Excel (`OW-04`, -0.5).
3. **A03: Injection (Puntuacion: 9.5 / 10)**  
   *Sin cambio.* Parametrizacion plena en SQLite (`?`), escape en PostgREST (`quoted`), PromQL protegido por lista blanca. Descuento residual de 0.5 por filtros dinamicos.
4. **A04: Insecure Design (Puntuacion: 8.0 / 10)**  
   *Sin cambio.* Politicas fail-secure en recomendaciones (+9.5), pero pendiente Rate Limiting perimetral (`OW-05`, -1.5) y mitigacion de DoS algoritmico (-0.5).
5. **A05: Security Misconfiguration (Puntuacion: 9.0 / 10)**  
   *Evolucion: Pasa de 7.0 a 9.0 (+2.0 puntos).* Se subsano totalmente la perdida de cabeceras en `/config.local.js` (`OW-07`, +1.0) y se implementaron `X-Frame-Options: DENY`, `Permissions-Policy` y `COOP` en Nginx (`OW-06`, +1.0). Se mantiene una deduccion de -1.0 pendiente por CSP y HSTS para Ola 2.
6. **A06: Vulnerable and Outdated Components (Puntuacion: 9.5 / 10)**  
   *Evolucion: Pasa de 8.0 a 9.5 (+1.5 puntos).* Se subsano la carga de scripts de CDN sin comprobacion criptografica incorporando hashes SRI y `crossorigin="anonymous"` en las 6 paginas HTML (`OW-08`, +1.5). Descuento residual menor de -0.5 por fuentes de Google no autohospedadas.
7. **A07: Identification and Authentication Failures (Puntuacion: 8.5 / 10)**  
   *Sin cambio.* Validacion exhaustiva de claims JWT en Gateway (+9.5), con deduccion de -1.0 por persistencia de sesion en `localStorage` (`OW-09`) y -0.5 residual.
8. **A08: Software and Data Integrity Failures (Puntuacion: 8.5 / 10)**  
   *Evolucion: Pasa de 7.5 a 8.5 (+1.0 punto).* Se sustituyeron el 100 % de las etiquetas flotantes de GitHub Actions por hashes SHA inmutables de 40 caracteres (`OW-10`, +1.0). Se conserva una deduccion de -1.5 por imagenes base de Docker sin fijacion por digest (`OW-11`).
9. **A09: Security Logging and Monitoring Failures (Puntuacion: 8.0 / 10)**  
   *Sin cambio.* Correlacion distribuida con `X-Request-Id` y 6 alertas Prometheus (+9.5), con deduccion de -1.5 por ausencia de logs/metricas para rechazos 401/403 en Gateway (`OW-12`) y -0.5 residual.
10. **A10: Server-Side Request Forgery (SSRF) (Puntuacion: 9.5 / 10)**  
    *Sin cambio.* Rutas estaticas, `validate_url` restrictivo y `Redirect.NEVER` en cliente HTTP (+9.5). Descuento de 0.5 residual.

### Cuadro Comparativo de Score OWASP:

| Categoria OWASP Top 10 | Puntaje Inicial (04) | Puntaje Post Ola 1 (06) | Variacion | Justificacion de Mejora |
|---|:---:|:---:|:---:|---|
| A01: Broken Access Control | 7.0 / 10 | 7.0 / 10 | 0.0 | RLS Supabase y puertos locales programados para Olas 2 y 3. |
| A02: Cryptographic Failures | 7.5 / 10 | 7.5 / 10 | 0.0 | Columna password y Excel programados para Olas 2 y 3. |
| A03: Injection | 9.5 / 10 | 9.5 / 10 | 0.0 | Mitigado y conforme desde la linea base inicial. |
| A04: Insecure Design | 8.0 / 10 | 8.0 / 10 | 0.0 | Rate Limiting programado para Ola 2. |
| **A05: Security Misconfiguration** | **7.0 / 10** | **9.0 / 10** | **+2.0** | **Cabeceras defensivas Nginx (OW-06) y correccion en /config.local.js (OW-07).** |
| **A06: Vulnerable Components** | **8.0 / 10** | **9.5 / 10** | **+1.5** | **Subresource Integrity (SRI) en scripts y CSS de CDN en 6 paginas HTML (OW-08).** |
| A07: Identification Failures | 8.5 / 10 | 8.5 / 10 | 0.0 | Almacenamiento en localStorage programado para Ola 3. |
| **A08: Integrity Failures** | **7.5 / 10** | **8.5 / 10** | **+1.0** | **Anclaje de 100 % de acciones de GitHub Actions por commit SHA inmutable (OW-10).** |
| A09: Logging and Monitoring | 8.0 / 10 | 8.0 / 10 | 0.0 | Logs de auditoria y metricas 401/403 programados para Ola 2. |
| A10: SSRF | 9.5 / 10 | 9.5 / 10 | 0.0 | Mitigado y conforme desde la linea base inicial. |
| **TOTAL SCORE DE SEGURIDAD** | **80.5 / 100** | **85.0 / 100** | **+4.5** | **Incremento sustancial en robustez perimetral y cadena de suministro.** |

**Score de Seguridad Actualizado: 85.0 / 100**

---

## 7. Conclusion y Dictamen de Seguridad

1. **Efectividad de la Ola 1:** Las cuatro tareas de seguridad asignadas a la Semana 13 fueron implementadas con rigor tecnico, verificandose la presencia efectiva de cabeceras de proteccion contra Clickjacking y aislamiento de politicas (OW-06, OW-07), la salvaguarda de integridad criptografica ante manipulacion de CDNs (OW-08) y la eliminacion del vector de compromiso en la canalizacion de CI/CD (OW-10).
2. **Evaluacion de Regresiones:** Ningun cambio altero la compatibilidad ni quebro las suites de prueba existentes. El frontend conservo su tasa de éxito de 48/48 pruebas unitarias.
3. **Dictamen de Auditoria:** **APROBADO CON SCORE DE 85.0 / 100.** El sistema alcanza un nivel de seguridad robusto a nivel de codigo e integracion continua, restando ejecutar las remediaciones de persistencia externa (RLS y columna password en Supabase) y resiliencia en Gateway (Rate Limiting y auditoria de accesos) programadas para el Sprint 7.
