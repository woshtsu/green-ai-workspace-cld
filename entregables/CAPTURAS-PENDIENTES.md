# Capturas pendientes para los dos documentos de la semana 13

Documentos (en `exportados/semana13/`, carpeta local no versionada; los comparte Ricardo):
- **Informe corregido:** `Porras-Huaman-Barrera-Quintana-informe-unidad-III-CORREGIDO.docx` (IDs `C1xx`, `C2xx` y `C3xx`).
- **Semana 13:** `Porras-Huaman-Barrera-Quintana-semana13-calidad-FURPS-OWASP.docx` (IDs `Sxx`).

## Estado al 11/11/2026 (noche)
Claude tomó en segundo plano (Chrome headless y salidas reales de las pruebas) e insertó: C101, C301, C303/S02, C304/S03, C305, C311, S05, S09, S10 (marcadas con ✅). Imágenes en `entregables/informe-corregido/evidencias-nube/captura-*.png`. Pendientes: las que requieren sesión iniciada (app web, Trello, Render) o Docker (C302, S07), el logo (C100/S00) y C310 (PR con revisión, planificado para el Sprint 7).

## Cómo insertar cada captura en Word (30 segundos por captura)
1. Abre el .docx, pulsa **Ctrl + B** y busca el ID exacto, por ejemplo `CAPTURA-PENDIENTE-C306`. Cada ID aparece una sola vez, en un **recuadro amarillo**.
2. Haz **triple clic** dentro del recuadro para seleccionar el párrafo completo.
3. Ve a **Insertar → Imágenes → Este dispositivo** y elige tu captura: la imagen **reemplaza** al recuadro.
4. No borres el pie «Figura N. …» que está debajo. Si la imagen queda grande, arrastra una esquina, nunca un lado, para no deformarla.
5. Antes de entregar, vuelve a buscar `CAPTURA-PENDIENTE`: Word debe responder que no encontró resultados.
6. Si Word pregunta «¿Desea actualizar los campos?», responde **Sí**: solo actualiza el índice y los números de página.

Reglas: captura solo la ventana (Win + Shift + S), en modo claro y sin pestañas, marcadores ni datos personales. Nunca muestres tokens, contraseñas ni claves (DevTools → Application no). Si algo falla, captura el error real y avisa: no se maquilla.

## Orden de trabajo por integrante

### Jhonny Cristhian Quintana Carhuaricra (Product Owner): carátulas y Trello
Hazlo **después** de completar los días 1 a 4 de `entregables/trello/GUIA-TRELLO-POR-INTEGRANTE.md`, para que el tablero tenga actividad real.
| # | ID | Documento | Qué capturar y dónde |
|---|---|---|---|
| 1 | ✅ `C100` | Informe | Logo oficial de la Universidad Continental (de la plantilla institucional o el portal UC). Pega la imagen del logo, no una captura de pantalla. |
| 2 | ✅ `S00` | Semana 13 | El mismo logo. |
| 3 | ✅ `C201` | Informe | Trello: vista completa del tablero con las 11 listas (aleja el zoom del navegador al 67 %). |
| 4 | ✅ `C202` | Informe | Trello: tarjeta HU-03 abierta, con descripción, checklist, miembros, etiquetas, fecha y comentarios visibles. |
| 5 | `C203` | Informe | Trello: la tarjeta de un Daily Scrum **real** (13/11 o uno del Sprint 7 desde el 17/11) con los comentarios de los 4 integrantes publicados ese mismo día. El Daily del 09/11 no se completó: no se retrofecha. |
| 6 | `C204` | Informe | Trello: tarjeta «Sprint Review — Sprint 3» o «Retrospectiva — PMV1» abierta. |
| 7 | ✅ `S05` | Semana 13 | `entregables/guia-de-uso/GUIA-RAPIDA-USUARIO.md` abierto en GitHub (rama `test`), con la tabla de roles y la tarea 1 visibles. |
| 8 | `C312` | Informe | Trello: tablero con los títulos de tarjeta `PMVn-HUxx` (p. ej. `PMV2-HU03`) y las tarjetas repartidas por estado (To Do, In Progress, QA-Testing, Done). Hacerlo tras aplicar la guía de Trello. |
| 9 | `C313` | Informe | Trello: una tarjeta abierta con el checklist de la Definition of Done completo, miembro y fecha visibles. |

### Leonid Kisley Orlando Huamán Collazos: aplicación web en la nube
Antes de empezar, Ricardo despierta los servicios de Render (25 minutos antes; ver `entregables/video/GUION-VIDEO-UNIDAD-III.md`, §2). Inicia sesión en https://woshtsu.github.io/green-ai-workspace-cld/dev/.
| # | ID | Documento | Qué capturar y dónde |
|---|---|---|---|
| 1 | ✅ `S01` | Semana 13 | `dashboard.html`: el tablero con las pestañas visibles y el gráfico con datos. |
| 2 | ✅ `S06` | Semana 13 | Racks (`network.html`): los 50 servidores con colores y el panel lateral de un servidor seleccionado. |
| 3 | ✅ `C306` | Informe | Caso de uso de IA 1: en Racks, selecciona un servidor y pulsa «Predecir 15 min». Captura el resultado. Si sale «datos insuficientes», espera 20 minutos y repite. |
| 4 | ✅ `C307` | Informe | Caso de uso de IA 2: en el dashboard, pestaña «Predicción y recomendación» → «Usar valores de ejemplo» → «Evaluar recomendación». Captura el resultado, con las restricciones y `executionAllowed=false`. |
| 5 | ✅ `C308` | Informe | Pestaña «Reportes y experimento» → «Descargar CSV». Abre el CSV en Excel y captura la hoja. |
| 6 | `S08` | Semana 13 | F12 → pestaña **Console** en `login.html` y en `dashboard.html`, sin errores de *integrity* (SRI). Una captura que muestre la consola limpia. |
| 7 | ✅ `C304` y `S03` | Ambos | Prometheus de Render: servicio `green-ai-prometheus-dev`: abre su URL desde el panel de Render y añade `/alerts`, con las 4 reglas. Usa la misma imagen en los dos documentos. |

### Gina Diana Barrera Peña: modelo de ML
| # | ID | Documento | Qué capturar y dónde |
|---|---|---|---|
| 1 | ✅ `C303` y `S02` | Ambos | MLflow UI con el experimento `computational-demand-prediction` y el run `random_forest_15m` (MAE de test 3,85). En `software/prediction`: ejecuta el pipeline sin `--skip-mlflow` (ver `software/prediction/README.md`) con `python scripts/run_pipeline.py` (README, línea 62) y luego `mlflow ui --backend-store-uri ./mlruns` → http://127.0.0.1:5000. Si no se puede en tu PC, lo hace Ricardo, que ya tiene `mlruns/`. Misma imagen en los dos documentos. |

### Ricardo Porras Veli: repositorio, pruebas y nube
| # | ID | Documento | Qué capturar y dónde |
|---|---|---|---|
| 1 | ✅ `C101` | Informe | GitHub, rama `test`: `software/frontend/supabase-auth-setup.sql` abierto (función PL/pgSQL y *trigger*). |
| 2 | ✅ `S09` | Semana 13 | GitHub: `.github/workflows/ci.yml` con las acciones fijadas por SHA y su comentario `# v4`. |
| 3 | `S04` | Semana 13 | Panel de Render (workspace «My Workspace») con los 6 servicios `green-ai-*-dev`. No incluyas `SoftwareAnemia`. |
| 4 | ✅ `C305` | Informe | Swagger de Prediction en Render: `https://green-ai-prediction-dev-zxly.onrender.com/docs`, con `/v1/predictions` y `/v1/recommendations`. |
| 5 | ✅ `S10` | Semana 13 | Terminal: `cd software/frontend` y `node --test tests/*.test.cjs`, que debe terminar con `pass 48`. |
| 6 | ✅ `S07` | Semana 13 | Terminal: cabeceras de nginx (comandos en `docs/evidencias/semana13-ola1-verificacion.md`). |
| 7 | ✅ `C301` | Informe | Terminal con las suites por servicio (una captura por suite o un mosaico; comandos en `docs/CONTINUAR-EN-NUEVO-CHAT.md`). |
| 8 | ✅ `C302` | Informe | Terminal: stack local levantado y `python software/infraestructura/smoke/smoke.py`, que debe dar 14/14. |
| 9 | `C309` | Informe | **Hecha el 10/11/2026** (fotograma del episodio 3: 601/601 HTTP 200). Insertada en `informe-unidad-III.md` como `evidencias-nube/carga-601-transacciones-render.png`; falta reexportar el Word. |
| 10 | 🟡 `C310` | Informe | GitHub: un Pull Request real del Sprint 7 (rama de trabajo hacia `test`) con la revisión aprobada y los checks de CI en verde (pestaña Pull requests). Solo cuando exista el PR integrado; no se simula. |
| 11 | ✅ `C311` | Informe | GitHub → pestaña Actions → workflow `ci.yml`: historial de ejecuciones recientes con su resultado real. |

## Datos que completa Ricardo en ambos documentos
- `NRC-PENDIENTE` (Ctrl + B): número NRC de la sección.
- `VIDEO-URL-PENDIENTE` (solo en el informe, en Anexos): enlace del video cuando esté subido.

## Control final antes de enviar
- [ ] Buscar `CAPTURA-PENDIENTE`, `NRC-PENDIENTE` y `VIDEO-URL-PENDIENTE` → 0 resultados en ambos documentos.
- [ ] Clic derecho en el índice → **Actualizar campo → Actualizar toda la tabla**.
- [ ] Revisar que ninguna captura muestre tokens, contraseñas ni correos de terceros.

## Estado al 12/11/2026 — capturas sacadas del video

Claude extrajo fotogramas a 1920×1030 del video grabado el 10/11/2026 (`exportados/video/ep*.mp4`) y los insertó: S01 (ep1), S06 y C308 (ep2), C302 (ep4, el smoke 14/14 de `docs/evidencias/smoke-20261106.json`), C306 y C307 (ep5), C201 y C202 (ep6). No se usó ningún fotograma del inicio de sesión (muestra el correo). Notas de honestidad: C201 muestra 7 de las 11 listas; C308 muestra la descarga del CSV en la app, no el CSV abierto en Excel; C307 muestra «Lista para revisión humana», no el campo `executionAllowed`.

Siguen pendientes: C100/S00 (logo), C203, C204, C312, C313 (Trello, posteriores al video), C310 (PR del Sprint 7), S04 (panel de Render), S07 (cabeceras nginx, requiere Docker) y S08 (consola sin errores SRI).

## Estado al 12/11/2026 (00:40)
- ✅ C100/S00: logo de la UC que pasó el usuario (fondo negro convertido a PNG transparente: `evidencias/logo-uc.png`).
- ✅ S07: captura de `software/frontend/nginx.conf` en GitHub. Es evidencia de **configuración**; la de ejecución (`curl -sSI` contra nginx en Docker) sigue siendo opcional.
- 🟡 C310: insertada la captura del PR #6 abierto (CI 6/6 en verde a las 00:40). Cuando otro integrante lo apruebe, reemplazar `evidencias-nube/captura-C310-pr-sprint7.png` por una captura con la revisión aprobada.
- C203: el Daily del 09/11 no se completó; se capturará un Daily real posterior, sin retrofechar.
- Pendientes: C203, C204, C312, C313 (Trello), S04 (Render), S08 (consola SRI).

## Estado al 12/11/2026 (mediodía) — sin marcadores pendientes
- Insertadas las capturas del equipo: C203 (Daily 09/11, solo con el comentario de la Scrum Master), C204 (Sprint Review — Sprint 3), C312 (tablero en dos vistas), C313 (PMV2-HU-04; en la vista no aparece el checklist de la DoD) y S04 (Render, 6 servicios Deployed).
- S08: Claude la verificó en segundo plano en GitHub Pages (login.html y los recursos de dashboard.html cargan con `integrity`; consola sin mensajes) y generó la imagen; no depende del Gateway bloqueado por Cloudflare.
- Mejora opcional: reemplazar C310 cuando el PR #6 tenga la aprobación, y C313 por una vista con el checklist de la DoD desplegado.
