# herramientas_IA

| Carpeta | Uso |
|---|---|
| `agentes/agy_task.py` | Delegar un encargo a Antigravity CLI en modo headless (ver docstring y `docs/TOOLS_EVALUATION.md`). |
| `migracion/copiar_fuentes.py` | Copia reproducible desde el workspace antiguo (sin `.git`, secretos ni caches) + manifiesto. |
| `exportacion/extraer_imagenes_base64.py` | Separa imágenes base64 de un Markdown en archivos enlazados. |
| `exportacion/crear_paquete.py`, `exportar.ps1` | Scripts heredados de `deployment/` del workspace (sin adaptar todavía; ver HANDOFF). |
| `instalar-graphify.ps1` | Crea `.tools/graphify` con la versión fijada de Graphify. |

## Graphify
Versión fijada: paquete PyPI `graphifyy==0.9.96` (la misma que el workspace antiguo).

```powershell
.\herramientas_IA\instalar-graphify.ps1          # crea .tools\graphify (ignorado por Git)
& .\.tools\graphify\Scripts\graphify.exe query "pregunta" --budget 1500
& .\.tools\graphify\Scripts\graphify.exe update .
```
Mientras no se ejecute el instalador, puede usarse el runtime `.tools/graphify` (instalar con `herramientas_IA/instalar-graphify.ps1`):
`& .\.tools\graphify\Scripts\graphify.exe ...` desde la raíz del monorepo.

## Antigravity
```powershell
python herramientas_IA\agentes\agy_task.py --cwd software\simulator --prompt-file encargo.md --readonly
```
- Lanza `agy` con `--cwd` en la carpeta del servicio: las reglas `command(regex:^...$)` se comparan con la línea
  completa y, si el agente necesita `cd`, una regex anclada no coincide.
- `--allow-write <ruta absoluta>` y `--allow-command 'regex:^...$'` limitan los permisos al encargo.
- Revisa `summary.json` (`warnings`, `denied_actions`, `git_changed`) y el diff real antes de integrar.

## Exportación DOCX
Entorno local (no global): `python -m venv .tools/docx` y `.tools/docx/Scripts/python -m pip install pypandoc-binary==1.15 python-docx==1.1.2 openpyxl pypdfium2 pillow`.
```powershell
.tools/docx/Scripts/python herramientas_IA/exportacion/md_a_docx.py <doc.md> exportados/<salida>.docx --encabezado "Green AI · ..." --toc-antes "RESUMEN EJECUTIVO"
powershell -File herramientas_IA/exportacion/actualizar_word.ps1 -Docx exportados/<salida>.docx [-Pdf vista.pdf]   # rellena índice y páginas (Word)
.tools/docx/Scripts/python herramientas_IA/exportacion/lista_capturas.py <doc.md> vista.pdf                         # IDs CAPTURA-PENDIENTE y página
```
- Carátula: divs `::: {custom-style="Portada Titulo"}` (estilos `Portada Institucion|Escuela|Curso|Titulo|Subtitulo|Etiqueta|Texto|Nota`).
- Tablas de ≥ 9 columnas pasan solas a una sección horizontal. Párrafos `CAPTURA-PENDIENTE-<ID>: …` salen en recuadro amarillo.
- Diagramas: `java -jar .tools/plantuml/plantuml.jar -tpng herramientas_IA/diagramas/*.puml` (jar de Maven Central 1.2024.7).
- Matriz FURPS+ del docente: `.tools/docx/Scripts/python herramientas_IA/calidad/llenar_modelo_furps.py exportados/semana13/MODELO-FURPSPLUS-Green-AI.xlsx`.

## Trello y video
- `trello/validar_trello.py <export.json>`: aplica los chequeos del prompt del docente (tarjetas sin fecha/checklist/miembros/etiquetas/descripción/comentarios, PMV1/PMV2 por lista, participación por integrante).
- `video/carga_transacciones.py --login --iteraciones 200`: 601 transacciones reales contra el Gateway de Render (episodio 3); CSV en `docs/evidencias/carga-video.csv`. **No ejecutado aún** (servicios suspendidos).
