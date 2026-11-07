# Entregables originales importados (con imágenes)

> **Actualización 2026-11-06.** Con las guías del docente ya disponibles (`guias/exportados_docente/`), se
> comprobó que las guías 0–6 están numeradas **por competencia, no por semana**. Las carpetas `semana01-02`,
> `semana06` y `semana-por-confirmar` contienen las versiones entregadas de los capítulos de Lineamientos (guía
> 0), Conocimientos de Ingeniería (portada «Guía 6») y Gestión del Proyecto (guía 4). La documentación
> **corregida y sin imágenes**, que es la que guía las próximas entregas, está en `docs/academico/`. Estos
> archivos se conservan como registro de lo entregado.

Plan del proyecto (`semana-por-confirmar/gestion-del-proyecto.md`, §4.6): 16 semanas, 8 sprints de 2 semanas,
PMV1 = semanas 1–6, PMV2 = semanas 7–12, PMV3 = semanas 13–16. La semana 8 no tiene entregable.
Los DOCX/PDF se generan solo a pedido en `exportados/` (no versionados).

| Semana | Entregable en este repo | Guía del docente | Estado |
|---|---|---|---|
| 1–2 | [semana01-02/lineamientos-y-requisitos.md](semana01-02/lineamientos-y-requisitos.md): kickoff, selección de idea por factores ponderados, antecedentes, requisitos, HU, PMV | Falta | El documento dice «SEMANA 2 (completar de semana 1)»; no se sabe qué pedía la guía de la semana 1 |
| 3 | — | Falta | Sin entregable identificado |
| 4 | ¿[semana-por-confirmar/gestion-del-proyecto.md](semana-por-confirmar/gestion-del-proyecto.md)? (capítulo «4. Gestión del Proyecto») | Falta | Semana sin confirmar: el documento no la indica |
| 5 | — | Falta | Sin entregable identificado |
| 6 | [semana06/conocimientos-de-ingenieria.md](semana06/conocimientos-de-ingenieria.md) («GUÍA 6: Conocimientos de ingeniería y diseño de la solución») | Falta (solo se conoce su título) | Importado |
| 7 | — | Falta | Sin entregable identificado |
| 8 | No aplica | — | Sin entregable |
| 9–12 | [semana09-12/informe-unidad-III.md](semana09-12/informe-unidad-III.md): **informe de la Unidad III entregado** (98 páginas, 54 imágenes, 41 tablas) | [S9 artículo](../guias/semana09/), [S12 consigna y lista de cotejo](../guias/semana12/) | Convertido del PDF entregado; contenido sin editar |
| 13–16 | Próximas entregas (PMV3) | Pendiente | Ver [notas/reestructuracion-monorepo.md](notas/reestructuracion-monorepo.md) |

## Orígenes y versiones descartadas
- Semanas 1–2, 4 y 6: copias de `project-docs/0.Lineamientos al proyecto.md`, `4. Gestión de Proyecto.md` y
  `2. Conocimiento de Ingenieria.md` del workspace antiguo, en `semana01-02/`, `semana-por-confirmar/` y `semana06/`. Las imágenes base64 se separaron con
  `herramientas_IA/exportacion/extraer_imagenes_base64.py`; el texto no se modificó.
- Semanas 9–12: `exportados/semana12/Porras-Huaman-Barrera-Quintana-informe-unidad-III.pdf` (local, no versionado), convertido con
  `herramientas_IA/exportacion/pdf_a_markdown.py`. Versiones intermedias **no** importadas para no duplicar:
  `project-docs/Consigna-Taller1-Actualizado-Icacit_semana9.md` (solo en el respaldo del workspace antiguo) (versión de la semana 9) y
  `project-docs/Semana12/Consigna-Taller1-ActualizadoDesarollado.docx.md` (solo en el respaldo del workspace antiguo) (borrador anterior, retirado de este repo).

## Advertencia de honestidad (afecta a las próximas entregas)
El informe entregado de las semanas 9–12 incluye resultados sin respaldo experimental según
`docs/HANDOFF.md`. Entre ellos: XGBoost como modelo final con RMSE 7,1 %, MAE 5,4 % y sMAPE 8,6 %; mejora de
57,7 %; 45 ms; RAM menor de 35 MB; ahorro de 18,4 %; y afirmaciones sobre Kubernetes y RabbitMQ. No se editó lo
ya entregado. **No reutilizar esas cifras** en semanas 13–16 sin un experimento reproducible que las sustente.
