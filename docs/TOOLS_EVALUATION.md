# Evaluación de herramientas de agentes

Fecha de verificación: 2026-11-06. Documentación oficial consultada ese día (páginas sin fecha propia):
antigravity.google/docs/cli/headless, /docs/install (autenticación), /docs/rules, /docs/permissions,
/docs/cli/modes, /docs/plans, /docs/cli/credits, /pricing y
developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals.

| Herramienta | Versión | Estado | Utilidad concreta | Costo / riesgo | Reversión |
|---|---|---|---|---|---|
| Claude Code | sesión actual | Adoptada | Coordinación, revisión, integración | Suscripción del usuario | — |
| Antigravity CLI (`agy`) | 1.5.2 (`C:\Users\Riss\AppData\Local\agy\bin\agy.exe`) | Adoptada, validada | Revisiones y cambios acotados delegados | Cuota del plan; créditos de pago desactivados por sesión (`useG1Credits:false`) | No invocar el adaptador |
| Graphify | `graphifyy` 0.9.96 | Adoptada | Índice AST de código/documentación para lectura económica | Local, sin API en `update` | Borrar `.tools/graphify` y `graphify-out/` |
| Ponytail (skill) | copia local `.agents/skills/ponytail*` | Adoptada | Preferir el cambio mínimo suficiente | Ninguno | Borrar la skill |
| Agency Agents | — | Pendiente | Perfiles de rol (backend, pruebas, despliegue) | Ninguno | — |
| Caveman | — | Diferida | Compresión de respuestas | Riesgo de pérdida de fidelidad | — |
| FreeLLMAPI | — | Diferida, no necesaria | — | Cambia proveedor/modelo y envía código a terceros | — |
| Gemini CLI | — | Descartada | — | Desde 2026-06-18 no atiende cuentas Google AI Pro/individuales con Login with Google (aviso oficial) | — |

## Antigravity CLI: hechos verificados en este equipo
- Autenticación: realizada por el usuario previamente; `agy models` lista modelos (Gemini 3.8 Flash, Claude Sonnet/Opus 4.6, GPT-OSS 120B). El log muestra avisos "not logged in" al arrancar que no impidieron las ejecuciones.
- Plan: la documentación indica que Google AI Pro tiene cuota que se renueva cada 5 h hasta un límite semanal, y que los créditos AI se consumen solo si la opción de sobreuso está activa. El usuario confirmó el 2026-11-06 en `agy` la cuenta ricardoporrasveli@gmail.com con Google AI Pro. No hay `~/.gemini/antigravity-cli/settings.json`; el adaptador fuerza `useG1Credits:false` por sesión, sin guardar nada.
- Reglas: `agy` lee `AGENTS.md`/`GEMINI.md` del directorio de inicio y padres hasta la raíz del repo, más `.agents/rules/*.md` con frontmatter. No hace falta un puente: `AGENTS.md` es la fuente común y `CLAUDE.md` la importa.
- Permisos: `--settings` (JSON solo para la sesión) con `permissions.allow/deny`; Deny > Ask > Allow. En headless, una acción sin permiso se deniega "suavemente": **exit 0 y `status: SUCCESS`** con `denied_actions` en el JSON.
- Permisos globales heredados del IDE (`~/.gemini/config/config.json`, 116 concesiones) incluyen `command(powershell)`; el adaptador lo deniega siempre junto con `pwsh`, `cmd`, `bash`, URLs, MCP y git destructivo.
- Las reglas `command(...)` se comparan con la línea completa que compone el modelo (p. ej. `cd software/simulator; uv --version`). Solución: lanzar con `cwd` en la carpeta del servicio y usar regex anclada.

## Prueba inicial (registro)
| # | Encargo | Permisos | Resultado | Tokens (total) |
|---|---|---|---|---|
| 01 | Revisión solo lectura de software/simulator (workspace antiguo) | deny escritura/comandos/URL/MCP | 1.er turno: `SUCCESS`, respuesta "Wait for subagent response." tras agotar `--print-timeout` 480 s → **sin informe**. 2.º turno (`--conversation`): 6 hallazgos con archivo:línea; Claude verificó los n.º 1, 3 y 6 en `application/runner.py` (imports de adaptadores L5-L10, señales L77-83, `REGISTRY` global L58). No pudo listar `tests/` por falta de comandos. | 143 924 + 181 287 |
| 02a | Cambio RunLogger (cwd = raíz del worktree) | allow write 2 archivos + regex anclada | Comando denegado (`cd ...;` no coincide); respuesta vacía, `SUCCESS`. Sin cambios. | 57 146 |
| — | Sondas de permisos | `command(uv)`, `command(uv --version)` denegados; `command(*)` permitido; regex anclada con cwd del servicio permitido | — | ~8 000 c/u |
| 02b | Cambio RunLogger (cwd = software/simulator) | ídem | Diff limitado a los 2 archivos, 4 pruebas nuevas; Claude reejecutó: 10 tests, 1 fallo previo de Windows. Integrado. | 135 385 |

| 03 | Revisión de seguridad solo lectura de `software/gateway-go` (cwd del servicio) | deny escritura/comandos/URL/MCP | 384 s, `SUCCESS`, sin denegaciones. 8 hallazgos con archivo:línea; Claude verificó cada uno: 7 ciertos (3 sobre recarga JWKS, la más grave un reintento por petición tras fallo), 1 falso (X-Forwarded-For). Todos los ciertos se corrigieron con prueba. `git_changed=true` se debió a ediciones de Claude en paralelo, no del agente. | 110 278 |

| 04 | Fichas de 9 artículos (cwd `guias/articulos`, modelo `claude-sonnet-4-6` porque la barra de estado del CLI mostraba «AI: Out of credits») | deny escritura/comandos/URL/MCP | 739 s, `SUCCESS`, 254 582 tokens. El agente **intentó escribir un archivo** pese a la instrucción y la regla de denegación lo bloqueó (lo declaró en su respuesta). Fichas con origen de cada cifra; Claude verificó 3 (Khan 87,48 %, Verdecchia 13–115 %, Sharma 45/71 %): correctas. Destapó un error del informe entregado (el 87,48 % de Khan no es precisión de predicción) | 254 582 |

Consumo informado por la herramienta en tokens; no informa costo ni cuota restante.
Cuenta (confirmada por el usuario con `agy`): ricardoporrasveli@gmail.com, **Google AI Pro**. La barra de estado
mostraba «AI: Out of credits»: se refiere a los créditos de pago adicionales, que el adaptador ya desactiva
(`useG1Credits:false`), no necesariamente a la cuota base.
Lección del encargo 03: `git_changed` compara el árbol completo; si Claude edita en paralelo, verificar el diff
de los archivos del encargo (o usar un worktree) antes de atribuir cambios al agente.
Conclusión: la integración funciona para revisiones y cambios pequeños **con revisión obligatoria**; un `SUCCESS` puede venir vacío.
