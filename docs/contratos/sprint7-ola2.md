# Contratos del Sprint 7 — ola 2 (19/11/2026)

Fuente de verdad compartida por los encargos paralelos. Cambiar este archivo antes que el código.

## HU-07 · Decisión humana persistente sobre recomendaciones (F-02)

La decisión es un **registro de auditoría**, nunca una orden de ejecución: `executionAllowed` sigue siendo `false`.

### Prediction Service (interno)

`POST /v1/recommendations/{recommendationId}/decisions`

Cuerpo:
```json
{
  "decision": "APPROVED | REJECTED",
  "comment": "texto opcional, máx. 500 caracteres",
  "recommendation": { "...": "objeto Recommendation completo tal como lo devolvió POST /v1/recommendations" }
}
```
Reglas:
- `recommendation.recommendationId` debe ser igual al `{recommendationId}` de la ruta (UUID) → si no, 422.
- `recommendation.executionAllowed` debe ser `false` → si no, 422.
- Identidad: solo cabeceras puestas por el Gateway: `X-Green-User-Id` (claim `sub`) y `X-Green-User-Role` (`ADMIN`/`OPERATOR`/`VIEWER`). Faltan → 401 problem+json. Rol `VIEWER` → 403.
- **Confianza en el Gateway (H-01: Prediction es accesible en Render sin pasar por el Gateway):** las cabeceras de identidad solo se aceptan si la petición trae `X-Green-Gateway-Secret` igual a la variable `GATEWAY_SHARED_SECRET` (comparación en tiempo constante). Si la variable no está configurada, ambas rutas de decisiones responden 503 problem+json («decisiones deshabilitadas: falta GATEWAY_SHARED_SECRET») — falla cerrado. Secreto ausente o distinto → 401. El valor real solo vive en variables de entorno (nunca en el repositorio); en `.env.example` va vacío.
- Un mismo usuario solo decide una vez por recomendación → 409 problem+json.
- Se guarda `recommendationSha256` (SHA-256 del JSON canónico de `recommendation`, claves ordenadas, sin espacios).

Respuesta 201:
```json
{
  "decisionId": "uuid",
  "recommendationId": "uuid",
  "decision": "APPROVED",
  "comment": "…",
  "decidedBy": "sub del usuario",
  "decidedByRole": "OPERATOR",
  "decidedAt": "2026-11-19T22:00:00Z",
  "recommendationSha256": "hex",
  "executionAllowed": false
}
```

`GET /v1/recommendations/{recommendationId}/decisions` → 200 `{ "recommendationId": "…", "decisions": [ …mismo formato… ] }` (cualquier rol, incluido VIEWER; requiere las cabeceras de identidad).

Persistencia: puerto `DecisionRepository` en el dominio; adaptador SQLite (`DECISIONS_DB_PATH`, por defecto `data/decisions.db` relativo al servicio). En Render el disco es efímero: limitación documentada. Migración equivalente para PostgreSQL/Supabase en `software/prediction/migrations/001_recommendation_decisions.sql` (**no se aplica** a Supabase sin autorización del usuario). Feature flag `DECISIONS_ENABLED` (por defecto `true`; `false` → 404 en ambas rutas).

### Gateway (Java y Go, mismo comportamiento)

| Método | Ruta pública | Destino en Prediction | Roles |
|---|---|---|---|
| POST | `/api/recommendations/v1/recommendations/{id}/decisions` | `/v1/recommendations/{id}/decisions` | ADMIN, OPERATOR |
| GET | `/api/recommendations/v1/recommendations/{id}/decisions` | `/v1/recommendations/{id}/decisions` | ADMIN, OPERATOR, VIEWER |

- `{id}` debe ser un UUID; cualquier otro valor → 404 (ruta no publicada).
- El Gateway **elimina** `X-Green-User-Id`, `X-Green-User-Role` y `X-Green-Gateway-Secret` de la petición del cliente y **vuelve a poner** los dos primeros desde el JWT validado (`sub` y `user_role`) en todas las rutas reenviadas, y `X-Green-Gateway-Secret` con el valor de su variable `GATEWAY_SHARED_SECRET` (si está vacía, no la envía). La variable se documenta vacía en `.env.example` / configuración de ejemplo.
- Límite de cuerpo 2 MB y timeout 30 s, como las demás rutas de recomendaciones.

## HU-13 · Reporte histórico en PDF (F-05)

`GET /api/v1/reports/historical-summary?hardwareId=…&start=…&end=…&format=pdf` (Data Processing; ruta pública sin cambios: `/api/processing/v1/reports/historical-summary`).
- `format` admite `json`, `csv` y `pdf`. JSON y CSV no cambian.
- `application/pdf`, `Content-Disposition: attachment; filename="reporte_historico_<hardwareId>_<start>_<end>.pdf"` (mismo patrón de nombre que el CSV).
- Contenido: título, filtro (hardware, rango), fecha de generación, mismos totales y estadísticos que el JSON, y la leyenda «Datos simulados; energía modelada, no medida».
- Mismos límites de rango y validaciones que CSV; dataset vacío → PDF válido que lo indique.

## Frontend

- Botón «Descargar PDF» junto a «Descargar CSV» (Reportes y experimento).
- En «Predicción y recomendación», tras evaluar: botones «Aprobar» y «Rechazar» con comentario opcional (no se muestran a VIEWER) y lista de decisiones registradas. Texto fijo: «Registrar una decisión no ejecuta ningún cambio».
- U-02: tabla textual accesible equivalente a cada gráfico Chart.js (sin retirar el canvas).
- F-06: toda potencia/energía mostrada o exportada se etiqueta como «modelada/estimada».
