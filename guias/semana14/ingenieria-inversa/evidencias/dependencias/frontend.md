# Dependencias de frontend — Prompt 3: Auditoría de Dependencias

> **Fase 2** · Servicio `software/frontend` (HTML/CSS/JS estático).
> No existe `package.json`: todas las dependencias de terceros se cargan **por CDN** en las etiquetas `<script>`/`<link>`; las pruebas usan solo el *runner* nativo `node:test` (Node 22). Últimas versiones consultadas en el registro npm el 2026-11-19.

## 1. Inventario completo

| Dependencia | Versión | Origen | Integridad (SRI) | Páginas | Última publicada |
|---|---|---|---|---|---|
| `@supabase/supabase-js` | 2.117.1 | `cdn.jsdelivr.net/npm/...` | `sha384-q36VSR1k…` + `crossorigin` | login, register, dashboard, flows | 2.119.2 |
| `chart.js` (UMD) | 4.4.8 | `cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js` | `sha384-T/4KgSWu…` | dashboard | 4.6.1 |
| Font Awesome (CSS) | 6.4.0 | `cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/...` | `sha384-iw3OoTEr…` + `referrerpolicy=no-referrer` | todas | 7.3.1 |
| Google Fonts (Inter, Fira Code) | — | `fonts.googleapis.com` / `fonts.gstatic.com` | No aplica (CSS dinámico, sin SRI) | todas | — |
| nginx | 1.28.0-alpine | Imagen Docker (`frontend/Dockerfile`) | Etiqueta, **sin digest** | — | — |
| Node.js (solo pruebas/CI) | 22 | `actions/setup-node` fijada por SHA | — | — | — |

Módulos propios (17 `.js`, 2 406 líneas): `app.js`, `appearance.js`, `metrics.js`, `monitoring.js`, `prediction.js`, `recommendations.js`, `pmv2.js`, `racks.js`, `flows.js`, `flows-logic.js`, `aggregate.js`, `energy.js`, `friendly-errors.js`, `help-content.js`, `ui-kit.js`, `dashboard-ui.js`, `config.example.js`. Datos estáticos: `racks.json` (50 nodos en 5 racks), `experiment.json` (resultado del experimento baseline vs Green AI).

## 2. Producción vs. desarrollo

| Tipo | Elementos |
|---|---|
| Producción (navegador) | supabase-js, Chart.js, Font Awesome, Google Fonts, módulos propios, `config.local.js` generado en el despliegue |
| Desarrollo/CI | Node 22 + `node:test` + `node:assert` (8 suites `.cjs`, 48 pruebas). Sin bundler, linter ni *transpiler* |

## 3. Dependencias críticas
- **supabase-js**: sin ella no hay inicio de sesión, renovación de token ni llamadas autenticadas (`authenticatedFetch` exige sesión).
- **Chart.js**: gráficos de evolución de métricas del panel; su falla degrada pero no bloquea el resto del panel.
- **`config.local.js`**: no es una biblioteca, pero sin él la aplicación lanza «Supabase Auth no está configurado».

## 4. Dependencias obsoletas
| Dependencia | Usada | Última | Brecha |
|---|---|---|---|
| Font Awesome | 6.4.0 | 7.3.1 | Mayor |
| Chart.js | 4.4.8 | 4.6.1 | Menor |
| supabase-js | 2.117.1 | 2.119.2 | Parche/menor |

## 5. Vulnerabilidades potenciales
- No se conocen avisos publicados para las versiones fijadas de Chart.js, supabase-js y Font Awesome en la fecha de análisis (no hay `package-lock.json` que permita ejecutar `npm audit`; revisión manual).
- **SRI presente** en los tres recursos de CDN versionados (mitiga la manipulación del CDN). Google Fonts no admite SRI.
- **Sin Content-Security-Policy** en `nginx.conf` ni en `<meta>`: un XSS no tendría contención adicional. Hay `X-Frame-Options DENY`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` y `COOP`.
- Uso de `innerHTML` con interpolación en `racks.js` (líneas 472 y 495) con `rackName` y `node.id` procedentes de `racks.json` (mismo origen, estático): riesgo bajo mientras esa fuente no sea editable por usuarios.
- El token de sesión de Supabase se persiste en `localStorage` (`persistSession: true`, comportamiento por defecto de supabase-js): ante XSS sería exfiltrable.
- En GitHub Pages las cabeceras de `nginx.conf` **no aplican** (Pages no permite cabeceras personalizadas).

## 6. Relacionadas con seguridad
supabase-js (PKCE, `autoRefreshToken`, `detectSessionInUrl`), SRI en CDN, `authenticatedFetch` con lista blanca de origen (`target.origin === gateway.origin` y ruta `/api/`), `AbortSignal.timeout(10000)`.

## 7. Relacionadas con persistencia
`localStorage` (tema visual `greenai-theme` y sesión de supabase-js). Tablas Supabase `user_profiles`/`user_roles` mediante el SQL `supabase-auth-setup.sql` (no se accede desde el JS de negocio; el rol llega como claim `user_role` del JWT).

## 8. Relacionadas con APIs
supabase-js (Auth API de Supabase) y `fetch` nativo contra el Gateway: `/api/monitoring/v1/metrics/{catalog,current,history}`, `/api/processing/v1/{prediction/dataset,reports/historical-summary}`, `/api/prediction/v1/predictions`, `/api/recommendations/v1/{recommendations,energy}`.

## 9. Conclusión
Superficie de terceros reducida (3 bibliotecas por CDN con SRI) y sin cadena de *build*. Riesgos principales: ausencia de CSP, token en `localStorage` y dependencia de CDNs públicos (disponibilidad y privacidad: Google Fonts recibe la IP del usuario). Se recomienda fijar la imagen nginx por digest, añadir CSP y valorar *self-hosting* de las bibliotecas.
