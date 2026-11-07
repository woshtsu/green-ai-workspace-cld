# Entregables

## `informe-corregido/` — lo que se entrega
Única carpeta del informe de la Unidad III que se corrige y entrega.
- [informe-unidad-III.md](informe-corregido/informe-unidad-III.md): texto del informe (convertido del PDF entregado; 98 páginas, 54 imágenes, 41 tablas). Aquí se hacen las correcciones.
- `evidencias/`: imágenes que usa el informe (rutas relativas; mantener junto al `.md`).
- [cambios-tecnicos-a-reflejar.md](informe-corregido/cambios-tecnicos-a-reflejar.md): qué cambió en el sistema (monorepo, SQLite, Gateway Go, despliegue en Render, Prediction ligera) y en qué sección del informe va cada cosa, con su evidencia y lo que falta.

Guía de redacción corregida (sin imágenes, no se entrega): [../docs/academico/](../docs/academico/README.md).

## `trabajos-previos/` — material de consulta, no se entrega
Versiones entregadas de capítulos anteriores, organizadas por tema (no por semana: las guías del docente están numeradas por competencia).
| Carpeta | Contenido |
|---|---|
| `lineamientos-y-requisitos/` | Kickoff, selección de idea, antecedentes, requisitos, HU, PMV (guía 0; semanas 1–2) |
| `conocimientos-de-ingenieria/` | «Guía 6: Conocimientos de ingeniería y diseño de la solución» |
| `gestion-del-proyecto/` | Capítulo «4. Gestión del Proyecto» (plan: 16 semanas, 8 sprints, PMV1 = 1–6, PMV2 = 7–12, PMV3 = 13–16) |
| `evidencias-del-sistema/` | Capturas históricas: sistema, Swagger, Supabase, evidencias por HU |

## Orígenes
- Capítulos previos: copias de `project-docs` del workspace antiguo (solo en el zip del usuario). Las imágenes base64 se separaron con `herramientas_IA/exportacion/extraer_imagenes_base64.py`; el texto no se modificó.
- Informe: `exportados/semana12/Porras-Huaman-Barrera-Quintana-informe-unidad-III.pdf` (local, no versionado), convertido con `herramientas_IA/exportacion/pdf_a_markdown.py`.
- DOCX/PDF solo a pedido, en `exportados/` (no versionado).

## Advertencia de honestidad
El informe entregado incluye resultados sin respaldo experimental según `docs/HANDOFF.md`: XGBoost como modelo final con RMSE 7,1 %, MAE 5,4 % y sMAPE 8,6 %; mejora de 57,7 %; 45 ms; RAM menor de 35 MB; ahorro de 18,4 %; y afirmaciones sobre Kubernetes y RabbitMQ. **Corregir o retirar esas cifras** al editar `informe-corregido/`, salvo que haya un experimento reproducible que las sustente.
