# Logs de frontend — Prompt 6 (frontend)

> **Fase 4 · Ejecución** · `software/frontend` servido en `http://127.0.0.1:13001` (servidor estático; nginx no disponible en el entorno) contra el Gateway Go local.
> Navegador: Google Chrome *headless* vía Playwright. Logs y capturas: [`logs/frontend/`](logs/frontend/).

## 1. Pruebas unitarias (`node --test tests/*.test.cjs`)

| Suite | Qué cubre | Resultado |
|---|---|---|
| `frontend.test.cjs` (5) | Valores nulos/no finitos no se convierten en cero, timestamps RFC 3339, el JWT no se envía a orígenes arbitrarios, un 401 renueva el token una vez y reintenta | OK |
| `prediction.test.cjs` (3) | Predicción con dataset preparado y Gateway autenticado; datos insuficientes sin reintentar el POST; exige clúster y nodo | OK |
| `recommendations.test.cjs` (5) | Telemetría ausente → «no evaluable»; sin recurso no hay petición; estado desconocido falla cerrado | OK |
| `pmv2.test.cjs` (11) | Mapeo de errores de API (INSUFFICIENT_DATA, INVALID_DATASET, 403 de solo lectura), reporte y experimento | OK |
| `racks.test.cjs` (7) | Conversión ratio → %, umbrales de color 40/80 %, nodos sin dato, 50 nodos en 5 racks | OK |
| `aggregate.test.cjs` (6) | Media, máximo, mínimo y p95 por instante sin inventar ceros; ranking de nodos | OK |
| `energy.test.cjs` (6) | Potencia modelada (reposo = 40 % de P_max), suma por instante, validación del cuerpo de `/energy` | OK |
| `flows.test.cjs` (5) | Red de flujos: sin flujos con carga equilibrada, conservación, nodos sin dato, determinismo | OK |
| **Total** | | **48/48 OK en 0,56 s** |

Con `node --test tests/` (carpeta) el *runner* falla (exit 1): hay que pasar los archivos.

## 2. Carga de páginas sin dependencias externas (CDN bloqueados)

| Página | Resultado | Consola |
|---|---|---|
| `index.html` | Renderiza | Falla Font Awesome y Google Fonts (`ERR_TUNNEL_CONNECTION_FAILED`, `ERR_BLOCKED_BY_ORB`) |
| `login.html`, `register.html` | Renderizan; formularios sin función | supabase-js no carga; aviso de Chrome: `Input elements should have autocomplete attributes (suggested: "current-password"/"new-password")` |
| `dashboard.html` | Renderiza el armazón; sin datos | supabase-js y Chart.js no cargan; mensaje en pantalla **«Supabase Auth no está configurado…»** aunque `config.local.js` sí existe |
| `network.html` | Inventario de 50 nodos visible, métricas pendientes | `[warning] No se pudieron obtener métricas en vivo: Supabase Auth no está configurado…` |
| `flows.html` | Renderiza | supabase-js no carga |

**Hallazgo:** sin acceso a los CDN la aplicación queda **inoperante** y el mensaje atribuye el fallo a la configuración (diagnóstico engañoso). No hay *fallback* local de las bibliotecas.

## 3. Recorrido E2E con el frontend real (sesión precargada)

Arnés: supabase-js 2.117.1 y Chart.js 4.4.8 servidos desde sus paquetes npm; atributos `integrity` retirados **solo en la copia de prueba** (jsDelivr entrega builds auto-minificados no reproducibles sin red); sesión de supabase-js precargada en `localStorage` con un JWT ES256 del emisor local.

### 3.1 Rol OPERATOR
| Paso | Llamada al Gateway | HTTP | Lo que ve el usuario |
|---|---|---|---|
| Abrir dashboard | `GET /api/monitoring/v1/metrics/catalog` | 503 | «No pudimos completar la operación… Espera un minuto y vuelve a intentarlo» (rol `OPERATOR` visible) |
| Reportes → «Ver resumen» (HW045, 10–11/07/2026) | `GET /api/processing/v1/reports/historical-summary` | **200** | «Resumen cargado con éxito» (datos SQLite) |
| Energía → «Calcular con el ejemplo» | `POST /api/recommendations/v1/energy` | **200** | «Ejemplo: 0.281 kWh calculados. Potencia modelada, no medida.» |
| Predicción | — (requiere elegir servidor; sin catálogo no hay lista) | — | «Selecciona un servidor para comenzar.» |
| Racks | `GET /api/monitoring/v1/metrics/current` | 503 | «Inventario cargado · Métricas pendientes (El servicio no está disponible.)» |

### 3.2 Rol VIEWER (solo lectura)
| Paso | Llamada | HTTP | Lo que ve el usuario |
|---|---|---|---|
| Reporte de históricos | `GET .../reports/historical-summary` | 200 | Resumen cargado |
| Energía con el ejemplo | `POST .../recommendations/v1/energy` | **403** | Tarjeta «Tu rol no permite esta acción» |

Consola en ambos roles: solo `Failed to load resource: 503/403` (esperados) y el aviso de métricas; **0 errores de JavaScript (`pageerror`)**.

## 4. Matriz de hallazgos de frontend

| ID | Tipo | Hallazgo | Evidencia | Severidad |
|---|---|---|---|---|
| F-01 | Dependencia faltante | Dependencia dura de CDNs (supabase-js, Chart.js, Font Awesome, Google Fonts) sin *fallback*; sin ellos no hay login ni gráficos | `console.json` | **Medio** |
| F-02 | Problema de configuración | Mensaje «Supabase Auth no está configurado» cuando el problema real es que la biblioteca no cargó | `dashboard.png`, `network.png` | **Bajo** |
| F-03 | Problema de configuración | Sin Content-Security-Policy; sesión de Supabase en `localStorage` | `nginx.conf`, `app.js` (`persistSession: true`) | **Medio** |
| F-04 | Problema de autorización (UX) | Los controles de acciones no permitidas se muestran a VIEWER; el bloqueo llega tras el 403 (correcto en seguridad, mejorable en UX). Además `/energy`, un cálculo sin efectos, se trata como operación de escritura | `viewer_energia.png` | **Bajo** |
| F-05 | Advertencia | Campos de contraseña sin `autocomplete` | Consola de Chrome en login/register | **Bajo** |
| F-06 | Problema de red | Dependencia total de Monitoring: catálogo vacío impide seleccionar servidor y, por tanto, predecir/recomendar desde la UI | `operator_prediccion.png` | **Alto** (hereda L-03) |
| F-07 | Advertencia | `styles2.css` no referenciado; `favicon.svg` no se copia en la imagen nginx (404) | `Dockerfile`, búsqueda en HTML | **Bajo** |
| F-08 | Verificación positiva | Errores de API traducidos a mensajes comprensibles (`friendly-errors.js`), rol visible, sin errores JS, `authenticatedFetch` bloquea destinos fuera del Gateway | Capturas y pruebas | — |
