# Calidad de la arquitectura — Prompt 10: Evaluación Arquitectónica

> **Fase 6** · Escala: 1 (deficiente) · 2 (insuficiente) · 3 (aceptable) · 4 (bueno) · 5 (excelente).
> Cada valoración se apoya en evidencia de código, configuración o ejecución recopilada en las Fases 1–5.

## 1. Resumen de calificaciones

| Criterio | Calificación | Tendencia principal |
|---|---|---|
| Cohesión | **4 / 5** | Servicios alineados a capacidades de negocio; Prediction y Data Processing acumulan responsabilidades secundarias |
| Acoplamiento | **3 / 5** | Contratos explícitos y validados, pero cadena síncrona de 6 componentes y contrato de dataset «provisional» |
| Escalabilidad | **2 / 5** | Servicios sin estado, pero Prediction no escala con la concurrencia y la nube gratuita impone techos fuertes |
| Mantenibilidad | **3 / 5** | Código limpio y ADRs, pero políglota, con dos gateways, deriva de versiones y de infraestructura |
| Testabilidad | **4 / 5** | 311 pruebas ejecutadas sin fallos, puertos inyectables, simulador determinista; huecos en contrato real y carga |
| Seguridad | **2 / 5** | Diseño del Gateway robusto, pero el despliegue permite eludirlo y la RLS de Supabase registrada es permisiva |
| **Promedio** | **3,0 / 5** | Arquitectura sólida en diseño, frágil en operación y seguridad del despliegue |

```text
Cohesión        ████████░░  4
Acoplamiento    ██████░░░░  3
Escalabilidad   ████░░░░░░  2
Mantenibilidad  ██████░░░░  3
Testabilidad    ████████░░  4
Seguridad       ████░░░░░░  2
```

## 2. Justificación técnica

### 2.1 Cohesión — 4/5
**A favor**
- Cada servicio corresponde a una capacidad: observar (Monitoring), preparar datos (Data Processing), predecir y recomendar (Prediction), simular (Simulator), controlar el acceso (Gateway).
- Dentro de Monitoring, Data Processing y Gateway Go las responsabilidades están separadas por puertos y adaptadores; la política de recomendación es una función pura de 29 líneas.
- El frontend separa lógica pura testeable (`aggregate.js`, `energy.js`, `flows-logic.js`) de la manipulación del DOM.

**En contra**
- Prediction aloja tres capacidades (inferencia, recomendación, energía) y un endpoint de métricas; `/v1/energy` es un cálculo genérico de integración que no depende del modelo.
- Data Processing combina ETL batch del Excel, lectura de históricos, reportes y ACL de Monitoring.

### 2.2 Acoplamiento — 3/5
**A favor**
- Integración exclusivamente por HTTP con contratos versionados (OpenAPI/JSON Schema) y validación estricta en el consumidor (Data Processing valida el sobre completo de Monitoring; Prediction valida identidad y `datasetId`).
- URLs inyectadas por entorno; adaptadores intercambiables (Supabase/SQLite, Prometheus/fixture).

**En contra**
- **Acoplamiento temporal fuerte:** la predicción en vivo requiere Simulator → Prometheus → Monitoring → Data Processing → Gateway → Prediction disponibles a la vez; no hay caché, reintentos ni *circuit breaker*. Verificado: con Monitoring caído, el panel, Racks y la predicción quedan inoperantes (L-03, F-06).
- Contrato de dataset marcado como `provisional`; el modelo exige frecuencia de 5 min mientras Data Processing emite 15 s (acoplamiento implícito resuelto por remuestreo).
- Identidad de servidor compartida por convención (`HW001…`) entre Simulator, Supabase y `racks.json`; `cluster=sim-run-<uuid>` cambia en cada ejecución.
- Dos gateways que deben mantenerse equivalentes (Java y Go) y un OpenAPI del Gateway copiado en el build de Go.

### 2.3 Escalabilidad — 2/5
**A favor**
- Todos los servicios de negocio son *stateless* (salvo el artefacto de modelo de solo lectura) → escalables horizontalmente en principio.
- Monitoring limita la concurrencia hacia Prometheus (*bulkhead* de 16) y acota series/puntos; los históricos usan paginación *keyset*.
- Gateway Go: 15 MiB de RSS y latencias sub-milisegundo en rechazos.

**En contra**
- **Prediction no escala con la concurrencia** (medido): concurrencia 1 → 9,8 req/s, p50 97 ms; concurrencia 8 → **7,0 req/s, p50 1 143 ms**. Causa: `load_selected_model()` deserializa y re-hashea el modelo **dos veces por petición** (≈ 15 ms cada vez) y los endpoints CPU-bound corren en un solo *worker*.
- El reporte de históricos lee de forma síncrona hasta 200 páginas × 500 filas dentro de una sola petición con timeout de 15 s en el Gateway.
- Prometheus sin persistencia ni alta disponibilidad; en Render, retención de 6 h en `/tmp`.
- Plan gratuito de Render: 512 MB, suspensión a los 15 min, ~1 min de arranque en frío, HTTP 429 entre servicios por URL pública (documentado por el equipo).
- Sin limitación de tasa: un cliente puede saturar Prediction o Data Processing.

### 2.4 Mantenibilidad — 3/5
**A favor**
- Código legible, tipado (records Java, Pydantic, dataclasses), nombres de dominio claros y mensajes de error en español coherentes.
- Decisiones documentadas como ADR (`docs/DECISIONES.md`, D-01…D-07), HANDOFF detallado, OpenAPI exportado, CI por servicio con acciones fijadas por SHA.
- Configuración *fail-fast* validada.

**En contra**
- **Heterogeneidad:** 3 versiones de Python (3.11, 3.12, 3.14), Java 21 y Go 1.25; pandas 2.3 vs 3.0; starlette 1.6 vs 1.10.
- **Duplicación** de Gateway (Java predeterminado en local, Go desplegado en la nube).
- Prediction declara una estructura hexagonal vacía y organiza la lógica en otra jerarquía (`src/`): induce a error a quien llega nuevo.
- **Deriva documental:** la auditoría interna afirma RFC 7807 en todos los servicios, hexagonal en todos y punto de entrada único; ninguna se cumple por completo.
- **Deriva de infraestructura:** `render.yaml` declara 3 servicios; 3 más se crearon a mano.
- El monorepo mezcla ~48 % de material no ejecutable (informes, Word/Excel, capturas, guías docentes).

### 2.5 Testabilidad — 4/5
**A favor**
- **311 pruebas ejecutadas en esta auditoría, 0 fallos** (Data Processing 121, Prediction 100, Frontend 48, Gateway Go 32, Simulator 10) + 123 pruebas Java documentadas por el repo.
- Diseño que facilita las pruebas: puertos inyectables, `Clock` inyectado en Monitoring, perfil `fixture`, simulador determinista por semilla, política pura, fixtures de contrato compartidas, prueba diferencial Java vs Go, pruebas anti-fuga temporal del modelo, `-race` en Go.
- Batería de contrato común SQLite/PostgreSQL+PostgREST para el adaptador de históricos.

**En contra**
- Las 8 pruebas contra PostgREST se omiten por defecto (no corren en CI) y no existe prueba contra un proyecto Supabase de pruebas.
- No hay pruebas E2E autenticadas en CI (el smoke del repo no autentica un usuario) ni pruebas de carga automatizadas.
- Cobertura relativa baja en Simulator (0,27 líneas de prueba por línea de código) y Frontend (0,25).
- `pytest.ini` de Prediction silencia `DeprecationWarning` y `FutureWarning`.

### 2.6 Seguridad — 2/5
**A favor (controles de diseño sólidos)**
- Validación JWT exhaustiva: `iss` exacto, `aud`, `exp` sin holgura, `nbf` con 60 s, `sub`, `role`, rechazo de anónimos; solo ES256/RS256; RSA ≥ 2048 bits; JWKS con caché y *backoff* (Go).
- RBAC por ruta con *deny-all*; VIEWER de solo lectura verificado de punta a punta.
- CORS de origen único; límites de cabeceras (16 KB) y cuerpo (2 MB); timeouts; errores sin fugas de detalles internos.
- Contenedores no root, distroless en Go, acciones de CI fijadas por SHA, SRI en CDN, cabeceras de seguridad en nginx, sin secretos versionados, validación de entradas exhaustiva (regex de IDs, rangos, zona horaria, cursor ligado al alcance).

**En contra (riesgos del sistema tal como está desplegado)**
- **Elusión del Gateway en la nube:** Prediction y Data Processing son servicios web públicos en Render y **no autentican**; cualquiera puede invocar la inferencia o leer históricos de Supabase con el token de servicio a través de Data Processing (comportamiento sin autenticación reproducido en E50/E51).
- **RLS permisiva registrada en Supabase** («Permitir todo» para `public` en `hardware`, `logs`, `usuario`) y columna `password` en texto plano junto a `password_hash` (snapshot del 22/09/2026, estado actual no verificable desde el repo); combinada con la clave *publishable* pública del frontend, permitiría leer y modificar esas tablas.
- Token de lectura en Render = clave legacy `anon` (sin mínimo privilegio).
- Sin CSP; sesión en `localStorage`; `/metrics`, `/docs` y la UI de Prometheus públicos; sin limitación de tasa; sin registro de eventos de seguridad (401/403) en el Gateway Go.
- Entorno de entrenamiento con MLflow 2.22.5 (29 avisos de seguridad).

Si se corrigen los tres primeros puntos, la calificación subiría a **4/5**: los controles de diseño ya existen.

## 3. Recomendaciones de mejora (priorizadas)

| # | Recomendación | Criterio que mejora | Esfuerzo | Prioridad |
|---|---|---|---|---|
| R-01 | Cerrar la elusión del Gateway: servicios privados (`type: pserv` o red privada) o autenticación servicio a servicio (validar el JWT también en Prediction/Data Processing, o cabecera firmada por el Gateway + lista de IPs) | Seguridad | Medio | P1 |
| R-02 | Revisar y endurecer la RLS de Supabase (eliminar «Permitir todo», borrar columna `password`), crear un rol de solo `SELECT` sobre `logs` y emitir un JWT dedicado para `SUPABASE_READ_TOKEN` | Seguridad | Bajo | P1 |
| R-03 | Cargar el modelo una vez al arrancar (caché con verificación SHA-256 inicial o `lru_cache` invalidable), varios *workers* (`--workers` = núcleos) y endpoints de inferencia en *threadpool* acotado | Escalabilidad | Bajo | P1 |
| R-04 | Resiliencia de la cadena en vivo: caché de corta duración de `metrics/current` y del dataset, reintentos con *backoff* y *circuit breaker* en Data Processing; degradar a «último valor conocido» en el panel | Acoplamiento, Escalabilidad | Medio | P2 |
| R-05 | Limitación de tasa y cuotas por usuario/rol en el Gateway; límite de páginas/tiempo en el reporte de históricos o generación asíncrona | Seguridad, Escalabilidad | Medio | P2 |
| R-06 | Infraestructura como código completa: incluir Monitoring, Prometheus y Simulator en `render.yaml` (o migrar a un único host con Compose); separar backend de producción y desarrollo | Mantenibilidad | Bajo | P2 |
| R-07 | Observabilidad: *access log* estructurado en el Gateway Go (método, ruta, estado, latencia, `X-Request-Id`, `sub` anonimizado), registrar 401/403/5xx con causa, validar `X-Request-Id` en Prediction, propagar trazas (OpenTelemetry) | Mantenibilidad, Seguridad | Medio | P2 |
| R-08 | Unificar el contrato de errores en RFC 7807 en Prediction | Acoplamiento | Bajo | P3 |
| R-09 | Elegir un único Gateway (Go, ya desplegado) y retirar el otro, o automatizar la prueba diferencial en CI | Mantenibilidad | Bajo | P3 |
| R-10 | Homogeneizar runtimes (una versión de Python para los tres servicios) y dependencias (pandas, numpy, starlette); locks completos con hashes; actualizar MLflow ≥ 3.17; separar dependencias de desarrollo en Data Processing; fijar imágenes por digest | Mantenibilidad, Seguridad | Medio | P2 |
| R-11 | Endurecer el frontend: CSP estricta, *self-hosting* de bibliotecas, sesión en memoria/almacenamiento con menor exposición, ocultar acciones no permitidas por rol | Seguridad | Medio | P2 |
| R-12 | Ejecutar en CI las pruebas de contrato PostgREST (servicios de GitHub Actions) y una prueba E2E autenticada con un emisor JWT de pruebas (como el usado en esta auditoría) | Testabilidad | Medio | P2 |
| R-13 | Completar el hexágono de Prediction (mover `Recommendation`, `Policy` y energía a `domain/`; puertos para el repositorio de modelos) y desacoplar `runner.py` del Simulator | Cohesión, Mantenibilidad | Medio | P3 |
| R-14 | Validar el modelo con datos multi-nodo (dataset ETL de 100 000 filas o telemetría del simulador) y evaluación *walk-forward* frente a persistencia | Calidad funcional | Medio | P3 |
| R-15 | Persistir el ciclo de vida de las recomendaciones (propuesta → aprobada/rechazada) con auditoría | Funcionalidad | Medio | P3 |
| R-16 | Separar el material académico del código (otro repositorio o Git LFS) | Mantenibilidad | Bajo | P4 |
