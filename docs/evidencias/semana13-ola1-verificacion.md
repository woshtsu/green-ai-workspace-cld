# Verificación de la ola 1 de mejoras (semana 13, 07/11/2026)

Ejecutado por Claude Code en la PC del equipo, rama `test`. Commit de código: `d24d86f`
(«fix(seguridad): ola 1 OWASP de la semana 13»). Documentación: `docs/GUIA-RAPIDA-USUARIO.md`.

## Cambios
| Hallazgo | Cambio | Archivo |
|---|---|---|
| OW-06 | `X-Frame-Options: DENY`, `Permissions-Policy`, `Cross-Origin-Opener-Policy` además de `nosniff` y `Referrer-Policy` | `software/frontend/nginx.conf` |
| OW-07 | Cabeceras de seguridad repetidas en `location = /config.local.js` (nginx no hereda `add_header` si el bloque define uno propio) | `software/frontend/nginx.conf` |
| OW-08 | `integrity="sha384-…"` y `crossorigin="anonymous"` en supabase-js 2.117.1, chart.js 4.4.8 y Font Awesome 6.4.0 (6 páginas HTML) | `software/frontend/*.html` |
| OW-10 | 8 acciones de GitHub fijadas por SHA de commit con la etiqueta como comentario (`# v4`) | `.github/workflows/ci.yml`, `pages.yml` |
| M-U07 | Guía rápida de usuario con 8 tareas en ≤ 3 pasos, basada en los textos reales de la interfaz | `docs/GUIA-RAPIDA-USUARIO.md` |

## Pruebas y resultados
| Verificación | Comando | Resultado |
|---|---|---|
| Hashes SRI estables | `curl -sSfL <url> \| openssl dgst -sha384 -binary \| openssl base64 -A` (2 descargas por recurso) | Mismo hash en ambas descargas para los 3 recursos |
| Pruebas del frontend | `cd software/frontend && node --test tests/*.test.cjs` | **48/48** pasan |
| Sintaxis nginx | `docker run --rm -v .../nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx:1.28.0-alpine nginx -t` | `syntax is ok`, `test is successful` |
| Cabeceras servidas (OW-06/OW-07) | `docker run nginx:1.28.0-alpine` con `nginx.conf` y `software/frontend` montados; `curl -sSI` a `/login.html` y `/config.local.js` | Ambas rutas devuelven `nosniff`, `no-referrer`, `X-Frame-Options: DENY`, `Permissions-Policy` y `COOP`; `config.local.js` además `Cache-Control: no-store` |
| Carga con SRI en navegador | `python -m http.server` + panel del navegador: `login.html` carga supabase-js y Font Awesome; chart.js cargado con el mismo `integrity` | Sin errores de integridad en consola; `window.supabase` y `window.Chart` definidos |
| YAML de workflows | `yaml.safe_load` de ambos archivos | OK |
| SHA de acciones | `gh api repos/actions/<acción>/commits/<etiqueta> --jq .sha` | 8 SHA resueltos |
| Textos de la guía | `grep` de cada botón citado en `software/frontend/*.html|*.js` | 10/10 textos existen |
| Regla VIEWER citada en la guía | `software/gateway-go/internal/policy/routes.go:72-77` | Solo GET para VIEWER |

## No verificado (pendiente)
- Workflows en GitHub Actions: no se ejecutaron (sin push).
- GitHub Pages no usa nginx: allí las cabeceras OW-06 no aplican (CSP por `<meta>` queda para la ola 2).
- Suites de backend y smoke 14/14: no se reejecutaron porque la ola 1 no toca el backend (último resultado: `docs/HANDOFF.md`).
