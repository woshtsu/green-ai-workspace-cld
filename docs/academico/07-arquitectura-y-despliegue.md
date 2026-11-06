# C6-B · Arquitectura híbrida (microservicios + hexagonal) y despliegue

Base: §VI.3 del informe entregado, las guías S6 (consigna y trazabilidad), S10, el Lab. 11 y
`0.Lineamientos al proyecto.md` §3. Fuentes técnicas: `docs/DECISIONES.md`, `software/*`.
**Corrección:** se describe la arquitectura **implementada**, no la planeada (sin Kubernetes, sin RabbitMQ, sin
MLflow Registry en ejecución).

## 1. Selección de arquitectura (la guía S2 pide 3 alternativas ponderadas)
| Criterio (peso) | Monolito por capas | Microservicios | Microservicios + hexagonal por servicio (híbrida) |
|---|---|---|---|
| Desacoplamiento dominio/infraestructura (25) | 3 | 3 | 5 |
| Independencia de tecnología por componente: Java, Python, Go (20) | 1 | 5 | 5 |
| Testabilidad sin infraestructura (20) | 3 | 3 | 5 |
| Despliegue en planes gratuitos (20) | 5 | 2 | 3 |
| Complejidad para un equipo de 4 (15) | 5 | 2 | 3 |
| **Ponderado** | 3,30 | 3,05 | **4,30** |
El costo de la opción híbrida está en el despliegue (varios procesos). Por eso D-06 evalúa un Gateway ligero y
D-07 compara hosting.

## 2. Componentes (vista de paquetes) y cumplimiento hexagonal
| Servicio | Tecnología | Capas en el código | Puertos / adaptadores | Estado hexagonal |
|---|---|---|---|---|
| Monitoring | Java 21, Spring Boot | `domain/`, `application/port/{in,out}`, `adapter/{in/web,out/prometheus,out/fixture}` | `QueryMetrics` (in), `MetricsSource` (out) → Prometheus o fixture | **Completo** |
| Simulator | Python 3.12 CLI | `domain/`, `application/`, `adapters/` | Exportador Prometheus, persistencia JSONL | Parcial: `application/runner.py` importa adaptadores y gestiona señales (hallazgo de la revisión 01 de Antigravity) |
| Data Processing | Python, FastAPI | `domain/` (con `ports/`), `application/use_cases`, `infrastructure/adapters/{input,output}` | `HistoricalLogsSource` → Supabase/PostgREST o SQLite; `DatasetRepository` → CSV | **Completo**; los adaptadores se eligen en `infrastructure/historical_sources.py` |
| Prediction (+ recomendaciones + energía) | Python, FastAPI, scikit-learn, XGBoost | `domain/`, `application/{ports,use_cases}`, `infrastructure/` **y** `src/` (servicio, ML, política) | Modelo como artefacto; política de recomendación pura (`src/recommendations/policy.py`, sin HTTP) | Mixto: el núcleo ML vive en `src/`; documentar o reorganizar |
| Gateway | Java, Spring Cloud Gateway | Configuración (`application.yaml`) + seguridad | Sin dominio propio (proxy) | No aplica (componente de infraestructura) |
| Gateway Go (alternativa) | Go 1.25 stdlib | `internal/policy` (dominio), `internal/auth` (puerto `Verifier` + adaptador JWKS), `internal/httpapi` | Inyección por constructor | Completo |
| Frontend | HTML/JS estático + nginx | — | Consume solo el Gateway | Adaptador de entrada |
| Supabase | PostgreSQL + Auth | Tablas `hardware`, `logs`, `user_profiles`, `user_roles`; RLS; función y trigger | — | Servicio externo |

**Patrones con evidencia:**
- **Repository:** `HistoricalLogsSource`, `DatasetRepository`.
- **Adapter:** Supabase y SQLite; PrometheusClient.
- **Factory:** `historical_source(settings)`.
- **Dependency Injection:** Spring (`MonitoringConfiguration`), constructores en Go, FastAPI `app.state`.
- **Strategy:** modelos intercambiables (persistencia, media móvil, RF, XGBoost) en `src/training`.

## 3. Procedimientos almacenados (ind. 11 de la lista de cotejo)
- **Evidencia en GitHub:** `software/frontend/supabase-auth-setup.sql` define la función PL/pgSQL
  `public.handle_new_auth_user()` (`security definer`), su *trigger* sobre `auth.users`, las tablas con RLS y las
  políticas por usuario.
- **Falta:**
  1. Que el informe lo muestre y explique.
  2. Comprobar en Supabase qué otras funciones existen y versionarlas en el repo.
  3. Una prueba que las ejercite contra un Supabase de pruebas.
- SQLite (perfil de desarrollo) **no** tiene procedimientos: la evidencia debe venir de Supabase.

## 4. Despliegue (vista de despliegue)
| Entorno | Topología | Estado |
|---|---|---|
| Local / desarrollo | Docker Compose `green-ai-mono`: Simulator, Prometheus, Monitoring, Data Processing, Prediction, Gateway (Java o Go), Frontend (nginx); Supabase externo | Funciona: smoke 14/14 (`docs/evidencias/smoke-20261106.json`) |
| Producción actual (informe 9–12) | Servicios en Render (`*.onrender.com`): Data Processing, Gateway, Monitoring, Simulator…; frontend en GitHub Pages | Vigente; **no modificado** |
| Staging propuesto (Lab. 11: no localhost) | Por decidir (D-07): Gateway Go (16 MB, ~10 MiB) + servicios Python en un PaaS gratuito; frontend estático; Supabase de pruebas | Pendiente: requiere investigación de proveedores y autorización |
Requisitos del Lab. 11 por cubrir:
1. CI/CD desde GitHub.
2. URL pública HTTPS del frontend y del backend.
3. BD remota con DDL y *seeding*.
4. Secretos en el panel del proveedor.
5. Pruebas G/W/T con capturas que muestren la URL.

## 5. Flujo end-to-end (video y E3 de la lista de cotejo S7)
Usuario → Frontend → Gateway (JWT + RBAC) → Prediction (adaptador de entrada REST) → caso de uso → modelo
(puerto de salida: artefacto) + política → respuesta con `executionAllowed=false`. Observabilidad: Simulator →
Prometheus ← Monitoring ← Gateway ← Frontend.
