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
| Jhonny Quintana | | | |
| Gina Barrera | | | |
| Ricardo Porras | | | |
| Leonid Huamán | | | |

Plazo: lo fija Gina (Scrum Master), antes de la entrega de la semana 13.
