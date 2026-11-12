# Revisión y confirmación de los entregables de la semana 13

Qué revisa cada integrante antes de entregar, según su rol en el proyecto (acta de constitución y gestión del proyecto).

**Documentos que se revisan:**

| Abreviatura | Archivo |
|---|---|
| **Word** | `exportados/semana13/Porras-Huaman-Barrera-Quintana-semana13-calidad-FURPS-OWASP.docx` (fuente editable: `entregables/semana13/semana13-calidad-furps-owasp.md`) |
| **Excel** | `exportados/semana13/MODELO-FURPSPLUS-Green-AI.xlsx` (hojas `1-Inicial`, `2-Actual`, `3-Esperado`) |
| **01–08** | Documentos del ciclo de calidad en `docs/calidad/` (los pide la guía; el Word los cita en el §12) |

El informe corregido de la Unidad III **no** entra en esta revisión.

## Qué se comprueba en cada parte
1. **Hechos:** lo que dice el texto es cierto en el proyecto. No se acepta nada que no se haya hecho o medido (ver «Honestidad experimental» en `docs/HANDOFF.md`).
2. **Cifras:** cada puntaje coincide entre el Word, el Excel y los documentos 01–08. Los totales correctos son 198 / 208 / 244 de 250 (79,2 % / 83,2 % / 97,6 %) y la seguridad pasa de 79,0 a 83,5 / 100.
3. **Responsable y fecha:** cada pendiente de la matriz tiene tu nombre solo si de verdad lo vas a hacer en esa fecha.
4. **OWASP 2025:** los códigos son `A01:2025 … A10:2025` (https://top10.owasp.org/2025/). No debe quedar ningún `:2021`, salvo las menciones históricas que lo dicen expresamente.
5. **Forma:** ortografía, nombres completos, tablas legibles y figuras con su pie.

## Reparto

### Jhonny Cristhian Quintana Carhuaricra: Product Owner (documentación, pruebas y gobernanza)
| Documento | Partes | Qué confirmar |
|---|---|---|
| Word | Portada, §1, §2, §3.1 | Datos de la portada (integrantes, docente, NRC 30170) y redacción general |
| Word | §4 completo (4.1, 4.2 y **4.3 tabla de roles**) | Que los roles y factores de los cuatro integrantes sean los acordados |
| Word | §5.1 y §5.2 | Auditoría y plan FURPS+ en cuanto a funcionalidad (HU-01 a HU-15) |
| Word | §7.1: filas M-F01 a M-F13 | Que el estado de cada HU coincida con el backlog y Trello (M-F07 «No cumple»; M-F05, F08, F09, F11 y F13 «Parcial») |
| Word | §11 y §12 | Conclusiones; que los enlaces del §12 abran en GitHub (rama `test`) |
| Excel | Filas F en las tres hojas | Las mismas cifras que el §7.1 |
| 01–08 | `01_auditoria_furps.md`, `02_plan_furps.md` | Que la matriz y el plan describan lo mismo que el Word |

### Gina Diana Barrera Peña: Scrum Master y ML Lead (datos y modelos)
| Documento | Partes | Qué confirmar |
|---|---|---|
| Word | §5.3 y §5.4 | Ola 1 de FURPS+ y su auditoría (85,00 % → 87,00 %) |
| Word | §7.1: filas M-F05, M-F08, M-P01 a M-P03, M-S01 a M-S04 y **OW-A04** | Evidencias de MLflow, cálculo de energía, imágenes ligeras e integración continua. OW-A04 lleva tu nombre por las contraseñas del Excel del dataset (OW-04) |
| Word | §7.2 tabla de apego y §8 brechas | Sumar la tabla del §7.2 contra el Excel; la explicación honesta de M-F08 (potencia modelada, no medida) |
| Word | §9.2 (M-F05 MLflow) | Que la evidencia corresponda a una corrida real |
| Word | §10 dictamen | Que el dictamen y sus cifras coincidan con 07 y 08 |
| Excel | Totales de las tres hojas (198 / 208 / 244) y filas P, S y A04:2025 | Totales y responsables |
| 01–08 | `03_auditoria_implementacion_furps.md`, `07_auditoria_final.md` | Coherencia con el Word |
| Como Scrum Master | Este archivo | Fijar el plazo, reunir las confirmaciones y avisar a Ricardo para reexportar |

### Ricardo Porras Veli: backend, contratos e integración (coordina la evaluación de seguridad)
| Documento | Partes | Qué confirmar |
|---|---|---|
| Word | §3.2 OWASP Top 10:2025 | La lista y el resumen de cambios frente a 2021 |
| Word | §6 completo (6.1 a 6.4) | Tabla OWASP 2025, plan por olas con OW-01 a OW-13 y recálculo 79,0 → 83,5 |
| Word | §7.1: filas M-R01 a M-R06, M-F07, M-F11, M-F13, M-S01 y OW-A01, A03, A05, A06, A08, A09, A10 | Estado, evidencia, responsable y fecha |
| Word | §9.8 (SRI), §9.9 (GitHub Actions por SHA) y §9.10 (regresiones, M-R04) | Que los comandos y salidas sean reales |
| Excel | Filas R y OWASP de las tres hojas | Lo mismo que en el Word |
| 01–08 | `04_auditoria_owasp.md`, `05_plan_owasp.md`, `06_auditoria_implementacion_owasp.md`, `08_reclasificacion_owasp_2025.md` | Que el 08 sea la clasificación vigente y que 04–07 lleven la nota de «histórico 2021» |
| Cierre | Reexportación | Aplicar las correcciones en el `.md` y volver a exportar el Word y el Excel (`herramientas_IA/README.md` § Exportación DOCX) |

### Leonid Kisley Orlando Huamán Collazos: infraestructura, Docker y observabilidad (con interfaz UI/UX)
| Documento | Partes | Qué confirmar |
|---|---|---|
| Word | §7.1: filas M-U01 a M-U08, M-F09, M-F10, M-P01, M-PL01 a M-PL06 y **OW-A02, OW-A07** | OW-A07 lleva tu nombre por la sesión en `localStorage` (OW-09, 30/11) |
| Word | §9.1 (dashboard), §9.3 (alertas Prometheus), §9.4 (hosting a costo cero), §9.5 (guía rápida), §9.6 (racks) | Que las capturas y textos correspondan a la interfaz y a Render reales |
| Word | §9.7 (cabeceras de Nginx, OW-A02) | Salidas de `nginx -t` y de las cabeceras |
| Word | §10.3 recomendaciones | Despertar los servicios de Render al menos 25 minutos antes de la sustentación |
| Excel | Filas U y PL, y las filas A02:2025 y A07:2025 | Lo mismo que en el Word |
| Evidencias | `docs/evidencias/semana13-ola1-verificacion.md` | Que los comandos registrados se puedan repetir |

## Confirmación
Cada uno marca su fila cuando termina. Las observaciones van a Ricardo (o como comentario en este archivo, en la rama `test`). Nadie edita el Word directamente: los cambios se hacen en el `.md` y se reexporta.

| Integrante | Revisado (✅) | Fecha | Observaciones |
|---|---|---|---|
| Jhonny Quintana | Parcial | 12/11/2026 | Revisó 01 y 02: M-F11 (responsable) y M-U07 (fecha) no coinciden. Falta confirmar el resto de su bloque (ver «Pendiente»). |
| Gina Barrera | ✅ (reconfirmar total) | 12/11/2026 | Aprobado con observaciones: pie de figura del §9.2, texto de M-F05, fechas de OW-A04 y M-S01, columna H de «3-Esperado». Revisó con 198/208; ahora son 196/206 (ver «Cambios después de la revisión»). |
| Ricardo Porras | ✅ | 12/11/2026 | §3.2 conforme a top10.owasp.org/2025. §6: recálculo 79,0 → 83,5 bien realizado (podrá ajustarse levemente). §7.1: todas mis filas conformes; M-F07 (HU-07, 20/11) y M-F11 (HU-13, PDF, 18/11) se mantienen como pendientes de la Ola 2 según el plan aprobado. §9.8–§9.10: comandos y salidas verificados al ejecutarlos y capturarlos. 08 es la clasificación vigente; 04 a 07 llevan la nota de «histórico 2021». Excel: se adapta a la versión revisada del Word en la reexportación. |
| Leonid Huamán | ✅ (con 1 pendiente) | 12/11/2026 | §7.1, §9.1, §9.3–9.7 y §10.3 conformes. Pide en §9.7 la salida del curl a /login.html y la ruta completa del docker run. |

Plazo: lo fija Gina (Scrum Master), antes de la entrega de la semana 13.

## Estado de la revisión al 12/11/2026 (noche)

### Cambios después de la revisión (afectan a todos)
- **M-R01 pasa a Parcial (3):** Prediction no responde errores en problem+json (usa `{code, message}`), los demás servicios sí. Evidencia: captura S28. Responsable Ricardo, 23/11 (Ola 2).
- **Nuevas cifras:** FURPS+ 168 → 172 / 200 (84,0 % → 86,0 %; ponderado 84,78 → 86,28). **Global 196 → 206 → 244 de 250 (78,4 % → 82,4 % → 97,6 %).** OWASP sin cambios (28 / 34 / 48; 79,0 → 83,5 / 100).
- El «85,00 ponderado» inicial no seguía las ponderaciones (era el bruto 170/200). Queda corregido.
- Se añade un archivo **LICENSE (MIT)** al repositorio para respaldar M-PL05.
- **Evidencias nuevas** S11–S37 en `entregables/semana13/evidencias/` (S11–S14 tomadas por el equipo). S11 y S12 confirman OW-01 (RLS «Permitir todo») y OW-03 (columna `password`). Ya no son «no verificados».
- La sección 6 tiene captura para cada hallazgo OW-01 … OW-13. Matices: OW-02 solo escucha en `127.0.0.1`; OW-11 es parcial (gateway-go sí fija digest); M-PL04 = «APIs de datos por el gateway» (el login va directo a Supabase).

### Decisiones pendientes del equipo (responde en este archivo o a Ricardo)
La auditoría 01 y el plan 02 no coinciden en:

| Fila | 01 auditoría | 02 plan | Propuesta | Decisión |
|---|---|---|---|---|
| M-F11 (reporte PDF) | Ricardo, 18/11 | Jhonny, 18/11 | Ricardo (backend) | |
| M-U07 (guía rápida) | 16/11 | 09/11 | 09/11 (se hizo en la Ola 1) | |
| M-R05 | 13/11 | 11/11 | Elegir una | |
| M-P01 (arranque en frío) | Leonid | Ricardo | Leonid (infraestructura) | |
| M-S01 (refactor Simulator) | Ricardo, 24/11 | Leonid, 24/11 | Ricardo, 23/11 (dentro de la Ola 2) | |
| OW-A04 (contraseñas Excel/BD) | 23/11 | Ola 3 (hasta 30/11) | 30/11 | |

### Pendiente por integrante
**Jhonny**
- [ ] Confirmar el resto de su bloque: portada, §1 a §4 (incluida la tabla de roles §4.3), filas M-F01 a M-F13 del §7.1, §11 y §12.
- [ ] Decidir M-F11 y M-U07 (tabla de arriba).

**Gina**
- [ ] Reconfirmar con las cifras nuevas: 196 / 206 / 244 y FURPS+ 86,0 % (86,28 ponderado) en §7.2, §8 y §10.
- [ ] Decidir la fecha de OW-A04 y M-S01 (tabla de arriba).

**Leonid**
- [ ] Pasar a Ricardo la **salida real** de `curl -sSI` a `/login.html` (y a `/config.local.js`) con el contenedor nginx de la Ola 1. Si no la guardó: `docker run --rm -d -p 8088:80 -v "$PWD/software/frontend/nginx.conf:/etc/nginx/conf.d/default.conf:ro" -v "$PWD/software/frontend:/usr/share/nginx/html:ro" nginx:1.28.0-alpine`, luego `curl -sSI http://127.0.0.1:8088/login.html`. En el documento la ruta irá relativa al repositorio (`software/frontend/nginx.conf`), sin rutas personales.
- [ ] Decidir M-P01 (tabla de arriba).

**Ricardo: capturas para las filas «Cumple» sin figura**
Guardar en `entregables/semana13/evidencias/` con este nombre. Reglas: solo la ventana (Win + Shift + S), modo claro, sin tokens, claves ni DevTools; usar `https://woshtsu.github.io/green-ai-workspace-cld/dev/` con los servicios de Render despiertos (≥ 25 min antes).

| Archivo | Fila(s) | Qué capturar exactamente |
|---|---|---|
| `captura-S40-f01-metricas.png` | M-F01 | Pestaña **Resumen** con las 7 tarjetas con valores (no «—») y el gráfico «Evolución de la métrica» con líneas. Esperar a que deje de decir «Conectando…». |
| `captura-S41-f02-historico.png` | M-F02 | Pestaña **Detalle por servidor**: tabla del histórico con filas y el paginador («Siguiente» / número de página) visible. |
| `captura-S42-f03-f06-prediccion.png` | M-F03, M-F06 | Pestaña **Predicción y recomendación** → «Predecir 15 min»: resultado de la predicción y la recomendación (con su estado y restricciones). |
| `captura-S43-f04-experimento.png` | M-F04 | Pestaña **Reportes y experimento**: la comparación de modelos o estrategias. |
| `captura-S44-f12-rbac.png` | M-F12 | Con una cuenta de rol **VIEWER**: el mensaje que impide predecir o aprobar. Si no hay cuenta VIEWER, avisar (se usará la prueba automática del Gateway). |
| `captura-S45-u02-modo-claro.png` | M-U02 | La misma vista que S13, pulsando el botón de modo para que quede en **modo claro** (S13 ya muestra el oscuro). |
| `captura-S46-u04-ayuda.png` | M-U04 | Un botón **«?»** abierto (por ejemplo, el de «Media del conjunto») con su texto de ayuda visible. |
| `captura-S47-u05-error-amigable.png` | M-U05 | Un mensaje de error amigable, por ejemplo el aviso de «servicio despertando» al entrar con Render dormido (sin códigos técnicos). |
| `captura-S48a-u08-paso1.png`, `S48b-…paso2`, `S48c-…paso3` | M-U08 | Una operación principal en tres pasos: (1) elegir servidor, (2) pulsar «Predecir 15 min», (3) ver la recomendación. |
| `captura-S49-p02-render-ram.png` | M-P02 | Render → `green-ai-prediction-dev` → **Metrics**: gráfico de **Memory** por debajo de 512 MB (no abrir Environment). |
| `captura-S50a-pruebas-prediction.png` | M-R04, M-F03, M-F06 | En tu equipo, terminal con el **resumen final** de `pytest` en `software/prediction` (línea «N passed»). |
| `captura-S50b-pruebas-data-processing.png` | M-R04, M-F02, M-R06 | Igual, `pytest` en `software/data-processing`. |
| `captura-S50c-pruebas-gateway-go.png` | M-R04, M-F12, OW-A10 | `go test ./...` en `software/gateway-go` (todas las líneas `ok`). |
| `captura-S50d-pruebas-java.png` | M-R04 | `mvn test` en `software/monitoring` y `software/gateway` («BUILD SUCCESS» y «Tests run: …»). |

Con S50a–S50d queda respaldada la cifra de 415+ pruebas.

### Cierre (Ricardo, con Claude)
Cuando estén las decisiones, las confirmaciones y las capturas: aplicar las observaciones en el `.md`, enlaces fijos a GitHub (commit `d24d86f` y etiqueta de la entrega), «Figura N» en cada fila de la matriz, LICENSE, y reexportar el Word y el Excel. Plazo (Gina): revisiones hasta el viernes 13/11, 18:00; reexportación el viernes 13/11, 21:00.


## Cierre (12/11/2026, noche)
Revisión cerrada y aplicada. Exportados: Word y su PDF (54 págs.) y Excel (196 / 206 / 244). Evidencias S11–S48c en el anexo §13. Versión del repositorio: etiqueta `semana13-entrega`. Pendientes, solo si el docente los pide: S44 (rol VIEWER) y S50a–S50d (resúmenes de pruebas).
