# Guía de despliegue del backend en Render (para el dueño de la cuenta)

Rama de trabajo: **`test`**. Fecha: 2026-11-07. Sin secretos en este documento: los valores sensibles los pone el dueño de la cuenta en el panel de Render.

## 1. Contexto en 2 minutos
- Monorepo único: `software/<servicio>/` con un `Dockerfile` por servicio. Contexto extenso: [HANDOFF.md](HANDOFF.md), decisión de hosting: [DECISIONES.md](DECISIONES.md) (D-07).
- **Frontend**: estático, ya en GitHub Pages. Solo necesita la URL pública HTTPS del Gateway.
- **Auth**: Supabase (el Gateway valida el JWT contra el JWKS de Supabase). No hay BD propia que desplegar.
- **Backend** (qué subir):

| Servicio | Carpeta (Root Directory) | Puerto | Healthcheck | Subir |
|---|---|---|---|---|
| Gateway (Go, recomendado: 16 MB, arranque 0,5 s) | `software` (Dockerfile Path `./gateway-go/Dockerfile`) | 8081 | binario `-healthcheck` | **Sí** |
| Prediction (incluye recomendaciones) | `software/prediction` | 8000 | `/health/ready` | **Sí** |
| Data Processing | `software/data-processing` | 8000 | `/api/v1/health` | **Sí** |
| Monitoring (Java) | `software/monitoring` | 8080 | `/actuator/health` (sin verificar) | Opcional (necesita Prometheus) |
| Simulator + Prometheus | `software/simulator` / infraestructura | — | — | **No**: se quedan locales para la demo |

- El Gateway Java (`software/gateway`, ~290 MiB) cabe mal en 512 MB; usar el de Go (equivalente verificado, 0 diferencias en 39 casos).

## 2. Limitaciones del plan gratuito (importan para la demo)
- 512 MB de RAM por servicio; se **suspende tras 15 min** sin tráfico y tarda ~1 min en despertar (la primera petición falla o tarda). Despertar los 3 servicios antes de demostrar.
- **Sin red privada**: los servicios se hablan por sus URLs públicas `https://….onrender.com`.
- Prediction pesa mucho (imagen 2,85 GB, build ~10+ min). Si se queda sin memoria al arrancar, avisar: hay que separar dependencias de entrenamiento (pendiente 2 del HANDOFF).
- Las predicciones necesitan historial: sin el Simulator conectado, `POST /predictions` puede devolver `INSUFFICIENT_DATA`. Es esperado; para la demo se ejecuta Simulator + Prometheus + Monitoring en local (o se acepta el límite y se documenta).

## 3. Preparación (una sola vez)
1. Cuenta de Render con el repo de GitHub conectado (Account → GitHub → permitir el repositorio `green-ai`).
2. Clonar y usar la rama `test`:
   ```bash
   git clone <URL-del-repo> && cd green-ai && git switch test
   ```
3. Tener a mano (los aporta el equipo, nunca por chat público):
   - `GATEWAY_AUTH_ISSUER_URI` = `https://<ref-supabase>.supabase.co/auth/v1`
   - `GATEWAY_AUTH_JWK_SET_URI` = `https://<ref-supabase>.supabase.co/auth/v1/.well-known/jwks.json`
   - URL exacta del frontend en GitHub Pages **solo el origen**, sin ruta: `https://<usuario>.github.io`

## 4. Crear los servicios (en este orden)
En Render: **New → Web Service → Build and deploy from a Git repository** → elegir el repo. Repetir para cada servicio con estos campos comunes:
- **Branch:** `test` para desarrollo; para producción repetir los servicios con **Branch** `main` (nombres `green-ai-*-prod`). Ver [GUIA-GITHUB-PAGES-Y-CI.md](GUIA-GITHUB-PAGES-Y-CI.md)
- **Runtime/Language:** `Docker`
- **Instance Type:** `Free`
- **Dockerfile Path:** `./Dockerfile` (relativo al Root Directory). **Instance Type: Free** (el formulario propone Starter, $7/mes: cambiarlo antes de crear)
- **Auto-Deploy:** *Off* (evita despliegues no revisados; se despliega a mano con *Manual Deploy*)

### 4.1 Prediction
- Name: `green-ai-prediction` · Root Directory: `software/prediction`
- Variables: `ML_ENV=experimental`, `ML_PORT=8000`
- Health Check Path: `/health/ready`
- Anotar la URL resultante → `PREDICTION_URL`.

### 4.2 Data Processing
- Name: `green-ai-data-processing` · Root Directory: `software/data-processing`
- Variables:
  - `APP_ENV=production`
  - `HISTORICAL_SOURCE=supabase` (activo en `green-ai-data-processing-dev` desde el 2026-11-09; antes `none` → el reporte de históricos respondía 503)
  - `MONITORING_BASE_URL=` URL pública de Monitoring si se despliega; si no, dejar la URL de relleno `https://example.invalid` (los endpoints de Monitoring responderán error controlado)
  - `REQUEST_TIMEOUT_SECONDS=10`
  - Supabase: `SUPABASE_ENABLED=true`, `SUPABASE_URL`, `SUPABASE_API_KEY` (la `sb_publishable_…` del frontend) y `SUPABASE_READ_TOKEN` (un JWT, no una `sb_…`; hoy la clave legacy `anon`, que puede leer `logs` porque la RLS es permisiva; si se endurece la RLS, hará falta un JWT de lectura dedicado). Pegar solo en Render.
  - Verificación (2026-11-09): `GET /api/v1/reports/historical-summary?hardwareId=HW045&start=2026-07-10T00:00:00Z&end=2026-07-11T23:59:59Z` → 200, `source=supabase`, 40 registros.
- Health Check Path: `/api/v1/health` · anotar URL → `DATA_URL`.
- **No usar** `HISTORICAL_SOURCE=sqlite` (solo desarrollo).

### 4.3 Monitoring (opcional)
- Name: `green-ai-monitoring` · Root Directory: `software/monitoring` · Java: puede exceder 512 MB; si falla por memoria, omitir.
- Variable: `MONITORING_PROMETHEUS_URL` = URL pública de un Prometheus (no existe en Render; sin él devuelve error). Por eso se deja local por ahora.

### 4.4 Gateway (al final: necesita las URLs anteriores)
- Name: `green-ai-gateway` · Root Directory: `software` · **Dockerfile Path: `./gateway-go/Dockerfile`** (el Dockerfile copia `gateway-go/` y los OpenAPI de `gateway/`, por eso el contexto es `software`)
- Variables:
  - `GATEWAY_PORT=8081`
  - `GATEWAY_PREDICTION_BASE_URL=<PREDICTION_URL>`
  - `GATEWAY_DATA_PROCESSING_BASE_URL=<DATA_URL>`
  - `GATEWAY_MONITORING_BASE_URL=<URL de Monitoring o https://example.invalid>`
  - `GATEWAY_AUTH_ISSUER_URI` y `GATEWAY_AUTH_JWK_SET_URI` (sección 3)
  - `GATEWAY_CORS_ALLOWED_ORIGIN=https://<usuario>.github.io` (exacto, sin `/` final ni ruta)
- Si Render no detecta el puerto: en *Environment* añadir `PORT=8081`.
- Anotar URL → `GATEWAY_URL`.

## 5. Conectar el frontend y Supabase
1. En el repo, rama `test`, el frontend lee `config.local.js` (ver `software/frontend/config.example.js`): `gatewayBaseUrl: '<GATEWAY_URL>'`, más `supabaseUrl` y la clave *publishable* (esa sí es pública). **Nunca** `service_role` ni secretos.
2. Supabase → Authentication → URL Configuration: añadir la URL de GitHub Pages en *Site URL* y *Redirect URLs*.
3. Publicar el frontend (workflow o carpeta Pages) — lo hace quien administre el repo.

## 6. Verificación (anotar resultados en HANDOFF.md)
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://<PREDICTION_URL>/health/ready        # 200 (tarda ~1 min si dormía)
curl -s -o /dev/null -w "%{http_code}\n" https://<DATA_URL>/api/v1/health             # 200
curl -s -o /dev/null -w "%{http_code}\n" https://<GATEWAY_URL>/api/prediction/v1/predictions         # 401 sin JWT (correcto)
curl -si -X OPTIONS https://<GATEWAY_URL>/api/prediction/v1/predictions \
  -H "Origin: https://<usuario>.github.io" -H "Access-Control-Request-Method: POST" | head   # CORS aceptado
```
Después, iniciar sesión en el frontend publicado y abrir el dashboard. Un 401 con sesión válida suele ser issuer/JWKS mal copiado; un error CORS en el navegador, `GATEWAY_CORS_ALLOWED_ORIGIN` distinto del origen real.

## 7. Qué NO hacer
- No pegar claves en el repo, issues ni chats; solo en *Environment* de Render.
- No activar planes de pago ni tarjeta; si Render lo pide, detenerse y avisar al equipo.
- No tocar `main`: los cambios van por `test`, y a `main` solo tras pruebas.
- No desplegar los servicios antiguos de Render con los nuevos nombres: suspender o borrar los antiguos solo si el equipo lo confirma.

## 8. Si algo falla
| Síntoma | Causa probable |
|---|---|
| Build "out of memory" / timeout en Prediction | Imagen grande; reintentar, o avisar para reducir dependencias |
| Servicio "Deploying" sin pasar a Live | Health Check Path o puerto incorrecto |
| 502/504 desde el Gateway | El servicio destino estaba dormido; reintentar a los 60 s |
| `INSUFFICIENT_DATA` al predecir | Falta historial (Simulator no conectado); esperado |

## 9. Atajo: crear los tres servicios de una vez (Blueprint)
El archivo `render.yaml` de la raíz define Prediction, Data Processing y Gateway (desarrollo, rama `test`, plan gratuito, Auto-Deploy apagado). Render → **New → Blueprint** → repo → rama `test`. Pide los valores `sync: false` (URLs de Prediction y Data Processing, issuer y JWKS de Supabase); como esas URLs no existen hasta el primer despliegue, pon un valor provisional y corrígelo después en *Environment* del Gateway.

**Nota sobre rutas al crear a mano:** en el formulario de Render, *Docker Build Context Directory* y *Dockerfile Path* son relativos a la **raíz del repositorio** (no a *Root Directory*). Prediction: contexto `software/prediction`, Dockerfile `software/prediction/Dockerfile`. Gateway Go: contexto `software`, Dockerfile `software/gateway-go/Dockerfile`. *Auto-Deploy* en *Off*.
