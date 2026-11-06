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
Mientras no se ejecute el instalador, puede usarse el runtime del workspace antiguo:
`& ..\.tools\graphify\Scripts\graphify.exe ...` desde la raíz del monorepo.

## Antigravity
```powershell
python herramientas_IA\agentes\agy_task.py --cwd software\simulator --prompt-file encargo.md --readonly
```
- Lanza `agy` con `--cwd` en la carpeta del servicio: las reglas `command(regex:^...$)` se comparan con la línea
  completa y, si el agente necesita `cd`, una regex anclada no coincide.
- `--allow-write <ruta absoluta>` y `--allow-command 'regex:^...$'` limitan los permisos al encargo.
- Revisa `summary.json` (`warnings`, `denied_actions`, `git_changed`) y el diff real antes de integrar.

## Exportación DOCX (pendiente)
Pandoc no está instalado en el equipo. Ver HANDOFF, "Pendientes".
