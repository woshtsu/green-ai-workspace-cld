# Semana 13 — Mapa de evidencias de la matriz de calidad (FURPS+ / OWASP 2025)

Generado el 2026-11-12. Imágenes en `entregables/semana13/evidencias/`; salidas crudas en `docs/evidencias/semana13-salidas/`. Cada imagen se generó con `herramientas_IA/capturas/terminal_a_png.py` a partir de la salida real de un comando (el .txt correspondiente). No se editó el entregable ni `exportados/`.

Prefijos: `S` = `entregables/semana13/evidencias/captura-S..-*.png`; `txt` = `docs/evidencias/semana13-salidas/`.

## Matriz (50 filas)

| ID | Estado actual | Evidencia | Qué demuestra | Pendiente |
|---|---|---|---|---|
| M-F01 | Cumple | — | — | Sin imagen. Sin pytest/venv/mvn offline no se pudo ejecutar la prueba de Monitoring. Captura sugerida: dashboard con datos reales (ver S01 solo como apoyo de M-F09). |
| M-F02 | Cumple | — | — | Sin imagen: pytest de data-processing no ejecutable (sin pytest ni venv; prohibido instalar). |
| M-F03 | Cumple | — | — | Sin imagen: pytest de prediction no ejecutable (ídem). |
| M-F04 | Cumple | — | — | Sin imagen (experimento en UI: captura manual del equipo). |
| M-F05 | Parcial | C303-mlflow-run.png (existente) | Corridas MLflow locales | Falta servidor MLflow público (no es evidencia nueva). |
| M-F06 | Cumple | — | — | Sin imagen. Se ve la bandera `executionAllowed` en S15, pero no la evaluación completa de políticas. |
| M-F07 | No cumple | S15-f07-aprobacion-sin-persistencia.png; txt/s15-f07.txt | Cero coincidencias de aprobar/rechazar/approv en frontend y prediction; solo existe la bandera `executionAllowed: Literal[False]`; sin tabla/endpoint de decisiones | Implementar flujo y persistencia (Ricardo, 20/11). |
| M-F08 | Parcial | S16-f08-potencia-modelada.png; txt/s16-f08.txt | `energy.js` modela P = P_idle + (P_max−P_idle)×CPU con IDLE_FRACTION=0.4; sin lectura de sensores | Medición real de potencia (fuera de alcance). |
| M-F09 | Parcial | S01-dashboard.png (existente) | Dashboard implementado y probado en local | Verificar con sesión Supabase real en /dev/. |
| M-F10 | Cumple | C304-prometheus-alerts.png (existente) | Reglas de alerta cargadas en Prometheus | — |
| M-F11 | Parcial | S17-f11-reporte-sin-pdf.png; txt/s17-f11.txt | `/reports/historical-summary` solo acepta `json`/`csv`; ninguna librería/MIME PDF en `software/` | Implementar PDF (Ricardo, 18/11). |
| M-F12 | Cumple | S13-login-sesion.png (apoyo: rol OPERATOR) | Sesión con rol OPERATOR | Sin imagen de la prueba 403 por rol; `go test` no ejecutable (Go no instalado). |
| M-F13 | Parcial | S13-login-sesion.png (existente) | Login real como Ricardo (OPERATOR) | Pruebas automatizadas con usuario real; RLS (ver OW-A01, S11). |
| M-U01 | Cumple | — | — | Sin imagen nueva. |
| M-U02 | Cumple | txt/s22-a07.txt (apoyo parcial) | `localStorage 'greenai-theme'` en appearance.js (persistencia del tema) | Captura del conmutador claro/oscuro (manual). |
| M-U03 | Cumple | S06-racks.png (existente) | Racks con mapa de calor | — |
| M-U04 | Cumple | — | — | Sin imagen (botones «?» requieren captura de UI). |
| M-U05 | Cumple | — | — | Sin imagen (mensaje amigable en UI). |
| M-U06 | Parcial | S20-u06-accesibilidad-sin-lighthouse.png; txt/s20-u06.txt | lighthouse/axe/pa11y no instalados (sin escaneo WCAG); recuento: aria- 66, role= 28, `<label` 20, lang= 6, aria-live 11; el único `<canvas>` (dashboard.html) sin aria-label | Ejecutar Lighthouse manual en Chrome; añadir aria-label/tabla alternativa al canvas. LIMITACIÓN: el recuento no equivale a conformidad WCAG. |
| M-U07 | Cumple | S05-guia-rapida.png (existente) | Guía rápida con flujos ≤ 3 pasos | — |
| M-U08 | Parcial | — | — | Sin imagen: mostrar los 4 pasos del cálculo de energía exigiría usar el arnés con datos y capturas manuales; se explica en el texto del entregable. |
| M-R01 | Cumple | S28-r01-r02-errores-y-salud.png; txt/t2-rfc7807.txt | problem+json en data-processing (2), gateway-go (1) y monitoring (5 coincidencias) | **Discrepancia**: Prediction no emite problem+json; su 500 usa un sobre propio `{code,message}` (`_error_payload`, app.py:71/89), y Spring Gateway no tiene manejador propio. La frase «uniformes en todos los microservicios» no queda respaldada: revisar el texto. |
| M-R02 | Cumple | S28-r01-r02-errores-y-salud.png; txt/t2-health.txt | Rutas `/health`, `/health/live`, `/health/ready` (prediction), `/health` (data-processing), `/actuator/health[/liveness]` y `-healthcheck` (gateway-go), actuator con probes (monitoring, gateway) | Sin prueba en ejecución local (solo código y salud remota en S25). |
| M-R03 | Cumple | S32-r03-timeouts.png; txt/s32a-c.txt | gateway-go: 6 s por defecto (monitoring), 15 s (processing), 30 s (prediction), connect timeout configurable; Spring Gateway: connect 1 s, response 6/15/30 s; data-processing: `httpx.Client(timeout=...)` + `TimeoutException` | Sin ejecución de pruebas (`go test` no disponible). Es evidencia de configuración en código. |
| M-R04 | Cumple | S10-frontend-tests.png (existente); txt/t2-frontend-tests.txt | `node --test` frontend: 48 pass, 0 fail | Las otras suites (prediction, data-processing, simulator, gateway-go, monitoring, gateway) NO se ejecutaron: sin pytest/venv/Go y Maven sin `~/.m2` (requeriría descarga). «415+ pruebas» sin respaldo en esta sesión. |
| M-R05 | Parcial | S18-r05-sqlite-sin-prueba-de-carga.png; txt/s18-r05.txt | compose.sqlite-dev.yml aísla desarrollo (`HISTORICAL_SOURCE: sqlite`, `SUPABASE_ENABLED: false`); sin herramientas de carga (locust/k6/jmeter/vegeta) ni resultados; HANDOFF reconoce RLS permisiva sin corregir | Prueba de carga contra PostgREST remoto + corregir RLS (S11). |
| M-R06 | Cumple | S33-r06-errores-fuente.png; txt/s33a.txt, s33b.txt | Adaptadores mapean fallos a `SourceTimeout`/`SourceForbidden`/`ServiceError`; handler único los convierte en problem+json; SQLite abre con `mode=ro` | Sin pytest (no ejecutado); es evidencia de código. |
| M-P01 | Parcial | S25-p01-tiempos-render.png; txt/s25-p01-timing-1.txt | Gateway: 0.47 s y 0.25 s. Prediction: 1.º intento 9.30 s (conexión 8.48 s, > 7 s) y 2.º 0.77 s | Ver nota 1: no es un cold start limpio de ~60 s; para ello repetir tras ≥ 15 min sin tráfico. |
| M-P02 | Cumple | — | — | Sin imagen (docker stats no ejecutado: sin contenedores levantados). |
| M-P03 | Cumple | S34-p03-imagen-ligera.png; txt/s34.txt | Registro `docs/evidencias/prediction-imagen-ligera-20261107.md`: 2,85 GB → 510 MB; RAM 174 → 133/142/122 MiB | La imagen cita el registro del 2026-11-07 (`docker images`); NO se re-midió en esta sesión (Docker no ejecutado). Una medición por caso, sin carga. |
| M-S01 | Parcial | S19-s01-simulator-no-hexagonal.png; txt/s19-s01.txt | `simulator/application/runner.py` (líneas 5-10) importa adaptadores (json_parser, scenario_parser, RunLogger); en data-processing `application/` no importa infraestructura | Refactor con puertos. |
| M-S02 | Cumple | S26-s02-s04-openapi-monorepo.png; txt/t2-openapi.txt | 14 rutas versionadas con openapi/swagger (data-processing, gateway, monitoring, prediction) | Nota: la lista incluye archivos históricos e imágenes; los contratos vigentes son los de `software/`. |
| M-S03 | Cumple | S09-ci-sha.png (existente) | Workflows con acciones fijadas por SHA | — |
| M-S04 | Cumple | S26-s02-s04-openapi-monorepo.png; txt/t2-monorepo.txt | toplevel = raíz del monorepo; 0 gitlinks (160000); 0 `.gitmodules` | — |
| M-PL01 | Cumple | S27-pl-guias-compose.png; txt/t2-guias.txt | Existen docs/GUIA-DESPLIEGUE-RENDER.md y GUIA-GITHUB-PAGES-Y-CI.md | — |
| M-PL02 | Cumple | S27-pl-guias-compose.png; txt/t2-compose.txt | docker-compose.yml con 7 servicios (simulator, prometheus, monitoring, data-processing, prediction, gateway, frontend) y 5 overlays | No se ejecutó `docker compose up`. |
| M-PL03 | Parcial | S14-render-servicios.png (existente) | 6 servicios Render Free | Cuota 750 h/mes y suspensión. |
| M-PL04 | Cumple | S35-pl04-gateway-desacoplado.png; txt/s35a.txt, s35b.txt | Tabla de 4 grupos de rutas del gateway (monitoring, processing, prediction, recommendations); el frontend usa `GATEWAY_BASE_URL` para la API | **Matiz**: el frontend además usa `supabase.createClient` (autenticación, ver S22/S13); «solo habla con el gateway» vale para las APIs de datos, no para el login. |
| M-PL05 | Cumple | S36-pl05-licencias.png; txt/s36.txt | 0 archivos LICENSE/COPYING versionados; 0 menciones en README.md; `monitoring/pom.xml` con `<license/>` vacío | **Discrepancia: la fila no queda respaldada.** No hay licencia del proyecto; añadir LICENSE y mención en README, o cambiar la fila a Parcial/No cumple. |
| M-PL06 | Cumple | S27-pl-guias-compose.png; txt/t2-guias.txt | README.md L22-L38 (pruebas por servicio y Docker) y docs/CONTINUAR-EN-NUEVO-CHAT.md existen | — |
| OW-A01 | No cumple | S11-supabase-rls.png (existente); S07/S11 | Políticas «Permitir todo» ALL/true para public en hardware, logs, usuario (confirma OW-01) | Restringir RLS. |
| OW-A02 | Cumple | S07-nginx-conf.png (existente) | Cabeceras defensivas en nginx.conf | — |
| OW-A03 | Cumple | S08-sri-consola.png (existente) | SRI en scripts CDN | — |
| OW-A04 | No cumple | S12-supabase-password.png (existente) | `usuario` con columnas password y password_hash (confirma OW-03) | Eliminar columna password y contraseñas del dataset. |
| OW-A05 | Cumple | S37-a05-inyeccion.png; txt/s37a-c.txt | SQLite con parámetros `?`; PostgREST con `quoted()` (escape) y httpx codifica URL; Pydantic `extra='forbid'` (prediction/recommendations y data-processing/monitoring_contract); PrometheusQueryBuilder con `quote()` y `switch` de 5 métricas permitidas (default → «Métrica no permitida») | Sin pytest (no ejecutado). Evidencia de código, no prueba de ausencia de inyección. |
| OW-A06 | Parcial | S21-a06-sin-rate-limiting.png; txt/s21-a06.txt | Cero coincidencias de ratelimit/limiter/throttle/429 en gateway-go y de RequestRateLimiter/bucket4j/resilience4j en Spring Gateway; rutas sin filtro de límite | Implementar rate limiting. |
| OW-A07 | Parcial | S22-a07-sesion-localstorage.png; txt/s22-a07.txt | `createClient(... persistSession: true)` sin opción `storage` → supabase-js usa localStorage; el código propio solo guarda `greenai-theme` | Nota: la clave de sesión la crea la librería (no aparece en el código); no se leyó ningún valor. Migrar a cookies HttpOnly/otra estrategia. |
| OW-A08 | Cumple | S09-ci-sha.png (existente) | Acciones por SHA | Las imágenes base Docker sin digest (OW-11) siguen abiertas. |
| OW-A09 | Parcial | S23-a09-401-403-sin-auditoria.png; txt/s23-a09.txt | server.go responde 401 (L234) y 403 (L129/142/154/160); el único slog del gateway-go es de arranque (main.go:30, 66) | Registro estructurado de auditoría 401/403. |
| OW-A10 | Parcial | S24-a10-recover-ausente.png; txt/s24-a10.txt | Existen las 3 pruebas fail-closed (server_test.go:407/419/433) pero **no se ejecutaron: Go no instalado**; sin `recover()` en gateway-go; sin ControllerAdvice/ErrorWebExceptionHandler en Spring Gateway | Ejecutar `go test ./internal/httpapi/` en una máquina con Go; añadir middleware de recuperación. |

Notas:
1. M-P01: antes de la medición registrada hubo una ronda de curl no guardada (se descartó su salida) que pudo despertar los servicios; por ello el 9.3 s de Prediction no es un cold start completo. Los servicios están en Render Free con suspensión tras 15 min.
2. Todas las imágenes muestran la fecha de generación de la imagen; la hora de ejecución de cada comando está en la sección «Comandos ejecutados».

## Sección 6 (OW-01…OW-13)

| Hallazgo | Imagen | Qué muestra |
|---|---|---|
| OW-01 RLS «Permitir todo» | S11-supabase-rls.png | Políticas ALL/true para public |
| OW-02 Compose publica puertos internos | S29-ow02-puertos-compose.png; txt/s29-ow02.txt | 5 servicios con puerto publicado. **Matiz**: todos se enlazan a `127.0.0.1` (solo loopback), por lo que la exposición es local, no a la red; el hallazgo debe acotarse (p. ej. Prometheus y Monitoring accesibles desde el host sin autenticación) |
| OW-03 Columna password en `usuario` | S12-supabase-password.png | Columnas password y password_hash |
| OW-04 Contraseñas sintéticas en dataset versionado | S30-ow04-excel-passwords.png; txt/s29-ow04.txt | `BD_GreenAi.xlsx`, hoja Usuarios: columnas `password` y `password_hash` con 10/10 celdas no vacías (valores no impresos); Hardware 50 filas y Logs 100000 filas sin columnas de contraseña |
| OW-05 Sin rate limiting | S21-a06-sin-rate-limiting.png | Cero coincidencias de limitadores |
| OW-06 / OW-07 Cabeceras / SRI | S07-nginx-conf.png | nginx.conf |
| OW-08 | S08-sri-consola.png | SRI en CDN |
| OW-09 Sesión en localStorage | S22-a07-sesion-localstorage.png | persistSession sin storage |
| OW-10 | S09-ci-sha.png | Acciones por SHA |
| OW-11 Imágenes base sin digest | S31-ow11-from-sin-digest.png; txt/s29-ow11.txt | 11 líneas FROM; solo gateway-go (2) usa `@sha256`; el resto solo con tag |
| OW-12 Sin auditoría 401/403 | S23-a09-401-403-sin-auditoria.png | slog solo de arranque |
| OW-13 Sin recover() | S24-a10-recover-ausente.png | Sin middleware de recuperación |

Nota: OW-06/07 y OW-08/OW-10 siguen la asignación indicada por el coordinador (S07, S08, S09); revisar contra la numeración del entregable.

## Filas sin evidencia y motivo
- Falta toolchain para las suites: pytest no instalado y sin venv (prediction, data-processing, simulator), Go no instalado (gateway-go), Maven sin repositorio local (`~/.m2` ausente; descargaría dependencias). Afecta M-F01…F03 y M-F12 (M-R03, M-R06 y OW-A05 tienen ahora evidencia de código, no de ejecución) y la cifra «415+».
- Requieren captura manual de UI o Docker: M-F04, M-F06, M-U01, M-U02, M-U04, M-U05, M-U08, M-P02.

## Hallazgos confirmados
- S11 (políticas RLS «Permitir todo», ALL/true, rol public, en hardware, logs y usuario) **confirma OW-01**, antes «no verificado».
- S12 (columnas `password` y `password_hash` en `usuario`) **confirma OW-03**, antes «no verificado».
- Al exportar, el texto del entregable debería quitar «(no verificado)» de A01 y A04 (fila de severidad «Alto (no verificado)»). No se editó el entregable.
- Nuevo hallazgo: Prediction no usa problem+json (M-R01); revisar la redacción «uniformes en todos los microservicios».

## Comandos ejecutados
Fecha 2026-11-12, bash (Git Bash) desde la raíz del repo. «Salida» es el .txt en `docs/evidencias/semana13-salidas/`. El código de salida es el del script envolvente (0 en todos); los códigos internos de cada `grep` (1 = sin coincidencias) quedan impresos en el propio .txt.

| Hora | Salida | Comando (resumen; el detalle exacto está en el encabezado de la imagen) | Exit |
|---|---|---|---|
| 17:15:41 | s15-f07.txt | `grep -rn -i -E 'aprobar\|rechazar\|approv'` en software/frontend y prediction/src; `grep executionAllowed`; `grep -rln` tablas de decisiones | 0 |
| 17:15:42 | s16-f08.txt | `grep -n` MODELO lineal/IDLE_FRACTION/modelPower en energy.js; `grep` sensor/ipmi/rapl | 0 |
| 17:15:53 | s17-f11.txt | `grep -n` rutas/formato en routes.py; `grep -rli reportlab\|fpdf\|weasyprint\|jspdf...` en software | 0 |
| 17:16:06 | s18-r05.txt | `sed`/`grep` en compose.sqlite-dev.yml y compose.yaml; `grep -rli locust\|k6\|jmeter\|vegeta`; `grep` HANDOFF | 0 |
| 17:15:55 | s19-s01.txt | `grep` imports de runner.py; `grep` imports en data-processing/application; `ls` capas | 0 |
| 17:16:20 | s20-u06.txt | `command -v lighthouse axe pa11y`; conteo de atributos con `grep -o \| wc -l` en frontend/*.html | 0 |
| 17:16:08 | s21-a06.txt | `grep -rn -i` ratelimit/limiter/throttle/429 en gateway-go y software/gateway; `grep` filtros en application.yaml | 0 |
| 17:16:21 | s22-a07.txt | `grep` createClient/persistSession en app.js; `grep` storage:/sessionStorage/cookie; `grep -o` localStorage | 0 |
| 17:16:22 | s23-a09.txt | `grep` StatusUnauthorized/StatusForbidden; `grep` slog/audit; `sed` unauthorized() | 0 |
| 17:16:22 | s24-a10.txt | `command -v go` (no existe); `grep ^func Test…`; `grep recover()`; `grep ControllerAdvice` | 0 |
| 17:17:05 | s25-p01-timing-1.txt | `curl -s -o /dev/null --max-time 120 -w ...` x2 a gateway `/actuator/health` y prediction `/health/ready` | 0 |
| 17:16:34 | t2-openapi.txt | `git ls-files \| grep -i -E 'openapi\|swagger'` | 0 |
| 17:16:34 | t2-monorepo.txt | `git rev-parse --show-toplevel`; `git ls-files -s \| awk '$1=="160000"' \| wc -l`; `git ls-files .gitmodules \| wc -l` | 0 |
| 17:16:35 | t2-guias.txt | `ls docs/GUIA-* entregables/guia-de-uso/`; `sed -n 22,38p README.md` | 0 |
| 17:16:35 | t2-compose.txt | `awk` sobre services de docker-compose.yml; `ls compose.*` | 0 |
| 17:16:55 | t2-rfc7807.txt | `grep -rn` problem+json/ProblemDetail por servicio; `grep` INFERENCE_ERROR | 0 |
| 17:16:37 | t2-health.txt | `grep` rutas de salud en app.py, routes.py, server.go, main.go y application.yaml | 0 |
| 17:16:56 | t2-frontend-tests.txt | `cd software/frontend && node --test tests/*.test.cjs \| tail -12` (48 pass, 0 fail) | 0 |
| 17:38 | s29-ow02.txt, s29-ow04.txt, s29-ow11.txt | `grep -n -A3 ports:` en docker-compose.yml; openpyxl (solo cabecera y conteo) sobre BD_GreenAi.xlsx; `grep -n ^FROM` en los 9 Dockerfiles | 0 |
| 17:38 | s32a-c, s33a-b, s34, s35a-b, s36, s37a-c.txt | `grep` de timeouts, excepciones/`mode=ro`, líneas de tamaño del registro de imagen ligera, tabla de rutas/GATEWAY_BASE_URL, licencias, consultas parametrizadas | 0 |
| ~17:10 | (descartada) | Primera ronda de curl a los dos endpoints, sin guardar salida (ver nota 1) | 0 |

No ejecutados por falta de herramienta: `pytest` (prediction, data-processing, simulator), `go test` (gateway-go), `mvn verify` (monitoring, gateway), Lighthouse/axe.
