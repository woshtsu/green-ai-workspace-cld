# Handoff PMV2 — continuación para Codex
Última actualización: 2026-10-29 01:44 COT
Redactado por: Gemini (revisión directa de código) a partir del diagnóstico de Codex.
Estado de Codex al corte: límite de uso tras reconciliar Data Processing y actualizar Prediction.

## Lo que hizo Codex antes de cortarse

| Tarea | Estado |
|---|---|
| Data Processing: merge feature/data-processing-integration a main | HECHO |
| Prediction: pull de rama Criss del remote | HECHO |
| Frontend: unir main + integration/design-monitoring | EN PROGRESO |
| Pytest data-processing en Docker | NO ejecutado (rechazado por política) |

## Arquitectura de Recommendations — aclaración importante

El usuario indicó que Recommendations no es un módulo independiente.
Sin embargo, tras revisar el código, la situación real es:

green-ai-recommendations/app.py tiene DOS endpoints:
  POST /v1/recommendations — orquestador: llama a Prediction via HTTP
                             y aplica política de umbrales sobre el resultado.
                             NO es una función interna de Prediction;
                             Prediction no puede llamarse a sí mismo.
  POST /v1/energy          — cálculo matemático puro (integral trapecio watts->kWh).
                             Este sí podría moverse a Prediction en el futuro.

El Gateway (application.yaml:39) ya tiene la ruta declarada:
  /api/recommendations/v1/recommendations -> servicio: recommendations
  /api/recommendations/v1/energy         -> servicio: recommendations

SecurityConfiguration.java ya protege esas rutas con JWT.

DECISION PARA ESTA ENTREGA: NO mover el código. Levantar el contenedor
de recommendations que ya existe. Es la ruta de menor riesgo.
La consolidacion arquitectonica es deuda tecnica documentada para despues.

## Estado verificado por Gemini

### Data Processing — routes.py completo en main local
El archivo .../data-processing-service/infrastructure/adapters/input/api/routes.py
YA TIENE los 4 endpoints en main local (el merge de Codex funcionó):
  GET /api/v1/health
  GET /api/v1/metrics/history
  GET /api/v1/historical-logs
  GET /api/v1/prediction/dataset

### Frontend — verificar estado post-merge
Archivos presentes en green-ai-front-end/Frontend-GreenAi/:
  index.html, dashboard.html, login.html, register.html, network.html
  app.js, monitoring.js, prediction.js, recommendations.js (5.1 KB — EXISTE)
  favicon.svg (EXISTE), appearance.js, metrics.js, supabase-auth-setup.sql
Verificar: cd green-ai-front-end && git log --oneline -10 && git status

### Recommendations — no corre, código completo en disco
  Código: green-ai-recommendations/app.py (248 líneas, completo)
  Dependencias: fastapi, pydantic, httpx, uvicorn, prometheus-client
  NO hay entrada en docker-compose.yml del workspace raíz
  El Gateway SÍ tiene las rutas configuradas (ya espera el servicio)

## Próximos pasos en orden

### 1. Verificar frontend post-merge
  cd green-ai-front-end
  git log --oneline -10
  git status

### 2. Levantar recommendations
  Verificar si tiene su propio Dockerfile:
    green-ai-recommendations/Dockerfile — SÍ existe (confirmar con: cat green-ai-recommendations/Dockerfile)

  Construir y levantar:
    docker build -t green-ai-recommendations green-ai-recommendations/
    docker run -d --name recommendations --network green-ai-workspace_default \
      -e PREDICTION_BASE_URL=http://prediction:8000 \
      -p 8004:8000 green-ai-recommendations

  O agregar al docker-compose.yml del workspace:
    recommendations:
      build: ./green-ai-recommendations
      environment:
        - PREDICTION_BASE_URL=http://prediction:8000
      expose:
        - "8000"
      depends_on:
        - prediction

  IMPORTANTE: el Gateway lo busca como host "recommendations" en la red Docker.
  El nombre del contenedor o el service name debe ser "recommendations".

### 3. Pytest data-processing (fue rechazado — ejecutar manualmente)
  $testRoot = (Resolve-Path green-ai-data-processing/Green-IA/data-processing-service).Path
  $dataRoot = (Resolve-Path green-ai-data-processing/Green-IA/datasets).Path
  docker run --rm --network none `
    --mount "type=bind,source=$testRoot,target=/app" `
    --mount "type=bind,source=$dataRoot,target=/datasets,readonly" `
    --entrypoint python green-ai-workspace-data-processing `
    -m pytest -q -p no:cacheprovider

### 4. Flujo autenticado completo
  Gateway rechaza sin JWT (HTTP 401 confirmado).
  Pasos:
    - Abrir frontend, registrar/iniciar sesion con Supabase
    - Navegar a prediccion: capturar request + response
    - Navegar a recomendaciones: capturar request + response
    - Guardar capturas en output/semana10/evidencias/

### 5. Limpiar informe — cifras sin respaldo (usuario confirmó que no existen)
  RETIRAR sin reemplazar:
    "XGBoost como modelo final" — no hay experimento que lo sustente
    "Ahorro del 18,4 %" — no existe ninguna ejecucion identificada
  El modelo activo es el que responde /health/ready con modelLoaded=true.

### 6. Evidencia Supabase (el usuario la está preparando)
  Necesita 3 capturas:
    - Definicion de la funcion (on_auth_user_created_green_ai / public.handle_new_auth_user)
    - Ejecucion que la activa (registro de usuario nuevo)
    - Resultado (fila creada en user_profiles o user_roles)
  El diagrama de tablas solo NO basta.

## Ramas actuales

| Repo | Rama local | Nota |
|---|---|---|
| green-ai-data-processing | main | feature/data-processing-integration mergeado |
| green-ai-prediction | Criss | actualizado desde remote |
| green-ai-monitoring | main | 1 commit adelante de origin |
| green-ai-gateway | main | 1 commit adelante de origin |
| green-ai-simulator | main | sin diferencias |
| green-ai-front-end | integration/design-monitoring | merge en progreso |
| green-ai-recommendations | sin repo git | solo carpeta con codigo |

## Docker activo
7 contenedores: simulator, prometheus, monitoring, data-processing, prediction, gateway, frontend
recommendations: NO corre — levantar con el paso 2 de arriba
Puertos: Prediction 8002, Data Processing 8003, Gateway 8081

## Reglas para el agente que retome
- NO reconstruir imagenes Docker sin confirmar que la rama es la correcta
- graphify-out/graph.json existe (2026-10-28) — consultar antes de leer archivos raw
- git rm --cached masivo ya se hizo en el workspace raiz; archivos sin trackear son normales
- target/ de Maven y __pycache__ fueron removidos del indice raiz — no re-agregar
