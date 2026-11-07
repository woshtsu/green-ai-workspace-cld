# GitHub Actions y GitHub Pages: `main` = producción, `test` = desarrollo

Repositorio: `woshtsu/green-ai-workspace-cld`. Flujo: rama temporal → `test` (desarrollo) → `main` (producción), siempre tras pruebas.

## Qué hay en el repo
| Archivo | Cuándo corre | Qué hace |
|---|---|---|
| `.github/workflows/ci.yml` | push y PR a `main` y `test` | Pruebas de frontend, Prediction, Data Processing, Gateway Go y Monitoring; valida el Compose y construye las imágenes (no las publica). **No despliega.** |
| `.github/workflows/pages.yml` | push a `main` o `test` que toque `software/frontend/**`, o manual | Publica **un** sitio: `main` en la raíz (producción) y `test` en `/dev/` (desarrollo). Genera `config.local.js` con las variables de Actions. |

Se retiró `software/frontend/.github/workflows/deploy.yml`: no corría (GitHub solo lee `.github/` en la raíz) y apuntaba a un Gateway antiguo.

## URLs resultantes
- Producción: `https://woshtsu.github.io/green-ai-workspace-cld/`
- Desarrollo: `https://woshtsu.github.io/green-ai-workspace-cld/dev/`

## Puesta en marcha (una vez, en GitHub → Settings)
1. **Pages** → *Build and deployment* → Source: **GitHub Actions**.
2. **Environments** → `github-pages` → *Deployment branches and tags*: permitir **`main` y `test`** (por defecto solo `main`; sin esto el despliegue de `test` falla).
3. **Secrets and variables → Actions → Variables** (son variables, no secretos):
   - `SUPABASE_URL`
   - `SUPABASE_PUBLISHABLE_KEY` (clave *publishable*; **nunca** `service_role`)
   - `GATEWAY_URL_PROD` = URL https del Gateway de producción en Render (sin `/` final)
   - `GATEWAY_URL_DEV` = URL https del Gateway de desarrollo en Render
4. (Recomendado) **Branches** → regla de protección en `main`: exigir PR y que pase el CI.
5. Subir la rama `test` y ejecutar *Actions → Frontend (GitHub Pages) → Run workflow* (el flujo debe existir en la rama desde la que se lanza).

## Supabase y Render
- Supabase → Authentication → URL Configuration: añadir **ambas** URLs (producción y `/dev/`) en *Site URL* / *Redirect URLs*.
- Render: dos Gateways. En cada servicio, *Branch*: `main` para los de producción, `test` para los de desarrollo. `GATEWAY_CORS_ALLOWED_ORIGIN=https://woshtsu.github.io` (solo el origen, igual en ambos).
- Mantener *Auto-Deploy* apagado en Render hasta probar; despliegues con *Manual Deploy*.

## Límites y notas
- Un repositorio tiene un solo sitio de Pages: por eso desarrollo vive en `/dev/` y no en otra URL.
- Cada ejecución reconstruye ambos entornos desde la punta de `main` y de `test`; un push a una rama no borra la otra.
- Sin ejecutar todavía: los flujos solo se validaron como YAML. La primera ejecución en GitHub puede mostrar ajustes (p. ej. Python 3.14 en Data Processing o el tiempo de `imagenes-docker`). Registrar el resultado en `docs/HANDOFF.md`.
- Nada se publica ni despliega hasta que alguien haga push (requiere autorización del usuario según `AGENTS.md`).
