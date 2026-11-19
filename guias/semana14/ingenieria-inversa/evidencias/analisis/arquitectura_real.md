# Arquitectura real — Prompt 9: Reconstrucción Arquitectónica

> **Rol:** Arquitecto Empresarial · **Fase 5** · Insumos: código fuente, dependencias, configuración (Compose, Render, Prometheus, CI), logs de ejecución de esta auditoría y diagramas del repo (`herramientas_IA/diagramas/*.puml`, `docs/historico/arquitectura-hibrida/*.puml`).
> Se describe **lo que el código y la configuración hacen**, señalando dónde difiere de lo que la documentación del proyecto afirma.

## 1. Arquitectura general

Sistema de **microservicios síncronos HTTP/JSON** detrás de un **API Gateway** con autenticación delegada a **Supabase**, más un **pipeline de observabilidad tipo *pull*** (Simulator → Prometheus → Monitoring). Cada servicio aplica, en distinto grado, **puertos y adaptadores**. El frontend es una **aplicación web estática multipágina** que habla solo con Supabase Auth y con el Gateway.

### 1.1 Diagrama de contexto (C4 nivel 1)
```text
                  ┌──────────────────────┐
  Operador /      │                      │  JWT (PKCE)      ┌──────────────────────┐
  Observador /    │   Green AI           │◄────────────────►│ Supabase             │
  Administrador ─►│   (observatorio y    │  históricos      │ Auth + PostgreSQL    │
   (navegador)    │   predicción de CPU) │◄────────────────►│ (logs, user_roles)   │
                  │                      │                  └──────────────────────┘
                  └──────────┬───────────┘
                             │ bibliotecas JS y fuentes
                             ▼
                  ┌──────────────────────┐   hosting: GitHub Pages (frontend) · Render (backend)
                  │ CDNs (jsDelivr,      │
                  │ cdnjs, Google Fonts) │
                  └──────────────────────┘
```

### 1.2 Diagrama de contenedores (C4 nivel 2)
```text
┌──────────────────────────────────────────────── Green AI ────────────────────────────────────────────────┐
│                                                                                                          │
│  [Frontend]  HTML/JS + nginx :3001 ───HTTPS/JSON (Bearer)───►  [Gateway] Spring Cloud GW :8081          │
│     │  supabase-js (PKCE)                                        │   ó Gateway Go :8081 (alternativa)    │
│     ▼                                                            │   JWT/JWKS · RBAC · CORS · X-Request-Id│
│  Supabase Auth                                                   │                                       │
│                    ┌─────────────────────────────────────────────┼──────────────────────┐                │
│                    ▼ GET /api/v1/metrics/*                       ▼ GET /api/v1/*        ▼ POST /v1/*     │
│        [Monitoring] Spring Boot :8080            [Data Processing] FastAPI :8000   [Prediction] FastAPI  │
│        hexagonal · PromQL · RFC 7807 ◄──HTTP──── hexagonal · ETL · históricos     :8000 · RF · política │
│                    │ /api/v1/query(_range)        │ PostgREST (HTTPS)  │ SQLite ro    · energía · /metrics│
│                    ▼                              ▼                    ▼                    ▲            │
│              [Prometheus] :9090 ◄── scrape ── [Simulator] :8000   Supabase DB      [artefacto joblib]    │
│              6 reglas de alerta   └── scrape ─────────────────────────────────────────────┘             │
│              (Grafana :3000 opcional)                                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Componentes

| Componente | Responsabilidad | Tecnología | Estado / Persistencia | Interfaces |
|---|---|---|---|---|
| Frontend | Presentación, sesión, orquestación de llamadas, cálculos ilustrativos (potencia modelada, flujos) | HTML/CSS/JS, supabase-js, Chart.js, nginx | `localStorage` (sesión, tema) | Supabase Auth; Gateway `/api/*` |
| Gateway | Punto de entrada: autenticación, RBAC, CORS, correlación, límites, timeouts, proxy | Spring Cloud Gateway (Java) / stdlib (Go) | Sin estado (caché JWKS) | 9 rutas + health + OpenAPI |
| Monitoring | Traducir métricas de negocio a PromQL y devolver series con calidad y procedencia | Spring Boot 4 | Sin estado | `/api/v1/metrics/{catalog,current,history}` |
| Data Processing | ACL frente a Monitoring; dataset para Prediction; históricos y reportes; ETL | FastAPI, pandas, httpx | Lee Supabase/SQLite; escribe CSV en ETL | `/api/v1/*` |
| Prediction | Inferencia de CPU, política de recomendación, energía, métricas de negocio | FastAPI, scikit-learn | Artefacto en disco (inmutable en runtime) | `/v1/predictions`, `/v1/recommendations`, `/v1/energy`, `/metrics` |
| Simulator | Telemetría determinista de 50 nodos | Python, prometheus-client | `runs/<uuid>/samples.jsonl` | `/metrics` |
| Prometheus | Almacenar series, evaluar alertas | Prometheus 3.13 | TSDB local (efímera en Render) | HTTP API, UI |
| Grafana (opc.) | Dashboard PMV2 | Grafana 12.4 | Volumen `grafana-data` | UI |
| Supabase | Identidad, roles (hook de claims), históricos | PostgreSQL + PostgREST + GoTrue | Tablas `hardware`, `logs`, `usuario`, `user_profiles`, `user_roles` | Auth API, JWKS, Data API |

## 3. Relaciones

| De → A | Tipo | Contrato | Sincronía | Tolerancia a fallos |
|---|---|---|---|---|
| Frontend → Gateway | Cliente/servidor | `gateway-v0.1.yaml` | Síncrona, timeout 10 s, refresco 30 s | Reintento único tras 401; mensajes amigables |
| Gateway → Monitoring/DP/Prediction | Proxy inverso | Rutas exactas con reescritura | Síncrona; 6 s / 15 s / 30 s | 503/504 sin detalles; sin reintentos ni *circuit breaker* |
| DP → Monitoring | Cliente HTTP | `monitoring-v0.1` validado con Pydantic (ACL) | Síncrona, `REQUEST_TIMEOUT_SECONDS` | Errores tipados → 422/502/503/504 |
| DP → Supabase | Cliente PostgREST | Columnas y filtros explícitos | Síncrona | 401/403 → `SOURCE_ACCESS_DENIED` |
| Monitoring → Prometheus | Cliente HTTP API | PromQL generado | Síncrona, 5 s, 16 concurrentes | *Bulkhead* sin cola |
| Prometheus → Simulator/Prediction | *Scrape* | Formato de exposición | Periódica 5 s (local) / 15–60 s (Render) | `up == 0` → alertas |
| Gateway → Supabase JWKS | Descubrimiento de claves | JWKS | Bajo demanda + caché | Go: *backoff* 30 s, 503 si no hay claves |
| Frontend → Supabase Auth | SDK | GoTrue | Síncrona | `autoRefreshToken` |

## 4. Dependencias

- **Runtime:** JVM 21 (2 servicios), CPython 3.11/3.12/3.14 (3 servicios), binario Go estático, nginx.
- **Críticas externas:** Supabase (sin él no hay login ni JWKS), Prometheus (sin él no hay métricas en vivo), CDNs (sin ellos el frontend no funciona).
- **Cadena crítica de la predicción en vivo:** Frontend → Gateway → Data Processing → Monitoring → Prometheus → Simulator, y después Frontend → Gateway → Prediction. **Seis componentes en serie**: la disponibilidad compuesta es el producto de las disponibilidades individuales.
- Detalle de bibliotecas: `evidencias/dependencias/*.md`.

## 5. Integraciones

| Integración | Mecanismo | Seguridad | Observaciones |
|---|---|---|---|
| Supabase Auth | supabase-js (PKCE), Custom Access Token Hook (PL/pgSQL) | JWT ES256/RS256, JWKS | El rol viaja como claim `user_role`; por defecto OPERATOR |
| Supabase Data API | PostgREST `/rest/v1/logs` | `apikey` + JWT de lectura | En Render se usa la clave legacy `anon` como token (HANDOFF); funciona por la RLS permisiva |
| Prometheus | Exposición + PromQL | Ninguna | Etiquetas de identidad configurables (`cluster`, `node`, `origin`) |
| GitHub Pages | Workflow `pages.yml` | Variables de Actions | Genera `config.local.js` por entorno (main/test) |
| Render | Blueprint `render.yaml` + servicios manuales | Variables `sync: false` | Sin red privada; servicios con URL pública |
| GitHub Actions | `ci.yml` | Acciones por SHA, `permissions: contents: read` | 6 jobs; construye imágenes sin publicarlas |

## 6. Flujo de datos

### 6.1 Telemetría (escritura continua)
```text
Simulator (tick 5 s) ──► estado por nodo (contadores CPU idle/user, memoria, red, FS)
   ├─► /metrics (4 254 series, cluster=sim-run-<uuid>, origin=simulated) ──► Prometheus (scrape 5 s, TSDB)
   └─► runs/<uuid>/samples.jsonl (~2,8 KB/s, sin rotación)
```

### 6.2 Lectura de métricas
```text
Usuario ─► Gateway ─► Monitoring: MetricQuery validada ─► PromQL ─► Prometheus /query_range
Prometheus ─► Monitoring: valida identidad, grilla, duplicados; calidad valid/missing/non_finite; estado complete/partial/no_data
Monitoring ─► (Gateway ─► Frontend)  ó  (Data Processing: ratio→%, exclusión sin imputación ─► dataset v1 ─► Prediction)
```

### 6.3 Inferencia y decisión
```text
dataset v1 (15 s) ─► input_adapter (remuestreo 5 min) ─► limpieza ─► 20 variables (calendario, lags, ventanas)
 ─► anti-fuga ─► RandomForest (joblib, SHA-256 verificado) ─► CPU +15 min (estimated)
 ─► política (frescura, identidad, memoria, latencia, error) ─► status/action ─► Counter/Gauge ─► Prometheus ─► alertas
```

### 6.4 Históricos y reportes
```text
BD_GreenAi.xlsx ──(carga externa, fuera del repo)──► Supabase public.logs ──PostgREST──► Data Processing
BD_GreenAi.xlsx ──seed_sqlite.py──► SQLite (dev, ro) ──────────────────────────────────► Data Processing
Data Processing: páginas keyset de 500 ─► calidad por campo ─► resumen (media, p95, máx, Wh) ─► JSON/CSV
BD_GreenAi.xlsx ──run_greenai_etl.py──► dataset_green_ai_v2.csv (100 000 filas) ──► (no lo consume ningún servicio)
```

### 6.5 Entrenamiento (offline)
```text
src/data/generate.py ─► data/raw/sample_dataset.json (1 nodo sintético, 3 días, 5 min, 864 registros)
 ─► validación ─► split temporal 70/15/15 ─► persistencia, media móvil, RF, XGBoost × horizontes 5/15/30 min
 ─► selección en validación ─► reentrenamiento train+val ─► métricas en test ─► model.joblib + metadata.json (SHA-256)
```
El entrenamiento ocurre **dentro del `docker build`** de Prediction (etapa *builder*).

## 7. Vistas de despliegue

### 7.1 Local (Compose `green-ai-mono`)
7 contenedores en una red de Compose; solo se publican puertos en `127.0.0.1`; Data Processing y Prediction no se publican (salvo overlay de Swagger). Buen aislamiento por defecto.

### 7.2 Nube (desarrollo y producción comparten backend)
```text
Navegador ─► GitHub Pages: /green-ai-workspace-cld/ (main)  y  /dev/ (test)
              │  config.local.js → gatewayBaseUrl = https://green-ai-gateway-dev.onrender.com (ambos entornos)
              ▼
Render (Oregon, free, sin red privada, suspensión a los 15 min):
   green-ai-gateway-dev (Go) ──HTTPS público──► green-ai-prediction-dev-zxly.onrender.com
                              ──HTTPS público──► green-ai-data-processing-dev.onrender.com ──► Supabase
                              ──► Monitoring *-dev (creado a mano; en render.yaml figura https://example.invalid)
   green-ai-prometheus-dev ──HTTPS público (scrape 60 s)──► prediction ; (15 s)──► green-ai-simulator-dev
```

## 8. Arquitectura documentada vs. arquitectura real

| Afirmación del proyecto | Realidad observada |
|---|---|
| «Punto de entrada único perimetral» (auditoría interna 07) | Cierto en local. **En Render, Prediction y Data Processing son servicios web públicos** y no autentican: el Gateway puede eludirse (E50/E51 reproducen la ausencia de autenticación interna) |
| «Arquitectura hexagonal desacoplada en todos sus servicios» | Alta en Monitoring, Data Processing y Gateway Go; parcial en Simulator; **nominal en Prediction** (carpetas hexagonales vacías) |
| «RFC 7807 estricto en todos los servicios» | Monitoring, Data Processing y Gateway sí. **Prediction usa `{code, message, details}` y `{detail}`** |
| Gateway Java como predeterminado | En local sí; **en la nube se despliega el Gateway Go** (`render.yaml`) |
| Despliegue reproducible con Blueprint (`render.yaml`) | El Blueprint declara 3 servicios; **Monitoring, Prometheus y Simulator se crearon a mano** (6 servicios según `CONTINUAR-EN-NUEVO-CHAT.md`). La infraestructura como código no reproduce el entorno real |
| Producción y desarrollo separados | El frontend sí (Pages raíz y `/dev/`), pero **ambos usan el mismo Gateway `-dev`** y el mismo backend |
| Kubernetes / RabbitMQ (documentación histórica) | No existen en este repositorio (el propio HANDOFF lo reconoce) |

## 9. Síntesis
La arquitectura real es **coherente, segura por defecto en local y con contratos explícitos entre servicios**; su punto más débil es la **traducción a la nube gratuita**, donde la ausencia de red privada rompe el supuesto de confianza en la red sobre el que descansa el diseño (servicios internos sin autenticación) y donde la mitad de los servicios (Monitoring, Prometheus, Simulator) se desplegó a mano, fuera del Blueprint.
