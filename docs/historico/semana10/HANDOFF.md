# Handoff PMV2

Actualizado por Codex el 29 de octubre de 2026. Estado comprobado con Git, pruebas y Docker.

## Decisión del usuario

Recomendaciones pertenece a Prediction. No desplegar un servicio separado.
La recomendación reutiliza `predict_from_payload` en el mismo proceso; no hay HTTP a sí mismo.
El handoff anterior proponía mantener un microservicio independiente: esa propuesta contradice
la instrucción del usuario y queda reemplazada. Se conserva como documento histórico en
`HANDOFF-previo-reconciliacion.md`.

## Ramas reconciliadas localmente

- Data Processing: main, 92caeac; integración por fast-forward; 8 commits por delante de origin/main.
- Frontend: main, 59d0fd2; une historiales independientes de origin/main e integration/design-monitoring.
  Conserva autenticación, integración funcional y favicon remoto; 10 commits por delante de origin/main.
- Prediction: Criss, 8585d6b; incorpora origin/Criss (1016ea0) y recomendaciones; 1 commit por delante.
- Gateway: main, 9d043fa; usa GATEWAY_PREDICTION_BASE_URL para recomendaciones; 2 commits por delante.
- Monitoring: main, d476c32; conserva su commit previo; 1 commit por delante.
- Simulator: main, 47536d7; coincide con origin/main.

Los seis árboles de trabajo quedaron limpios. NO se ejecutó push. Monitoring requiere autorización
explícita para publicar según su AGENTS.md. Respaldos de ramas previas: output/semana10/git-backup/*.bundle.
No se borraron ramas ni se reescribieron commits remotos.

## Código y despliegue

- Prediction: src/service/recommendations.py (API y coordinación), src/recommendations/policy.py (reglas sin HTTP).
- Endpoints internos /v1/predictions, /v1/recommendations y /v1/energy comparten servicio, imagen y Swagger.
- Los prefijos externos /api/recommendations/v1/... se conservan para compatibilidad del frontend.
- Gateway mantiene JWT/RBAC, tamaño máximo y timeout. No se añadió bypass de autenticación.
- Contratos generados: Prediction/contracts/*.openapi.json y Gateway/static/openapi/recommendations-v1.json.
- Compose raíz ya NO contiene servicio recommendations. DEMO_POLICY_JSON pertenece a prediction.
- Prometheus recolecta prediction:8000 bajo job green-ai-prediction; alerta de disponibilidad actualizada.
- Código del servicio anterior archivado en output/semana10/legacy/green-ai-recommendations.
- La configuración Compose/Prometheus del workspace no pertenece a los commits de los repositorios hijos.
  Conservar esos archivos también al compartir o publicar la entrega.

Se reconstruyeron Prediction, Gateway, Frontend y Data Processing. Se actualizaron sus contenedores
junto con Prometheus usando docker-compose.yml + compose.swagger.yaml, sin down ni eliminación de volúmenes.
Los siete servicios aparecen running; Prediction y Data Processing healthy.

## Pruebas ejecutadas

- Data Processing: 88 passed, incluyendo el dataset Excel original montado read-only.
  Un primer intento tuvo 2 fallos por no montar ese dataset; corregido el entorno, pasan todos.
- Prediction: 96 passed; incluye 13 pruebas de recomendaciones/energía.
- Después de precisar los esquemas de errores OpenAPI: 13 pruebas de recomendaciones repetidas y aprobadas.
- Gateway: Maven verify, 11 tests, 0 fallos/errores, BUILD SUCCESS.
- Frontend: 13 tests, 0 fallos.
- Hay avisos de deprecación de dependencias en pytest; no se ocultaron ni cambiaron umbrales.
- Graphify actualizado con graphify update . (AST, sin LLM).

Smoke HTTP con fixtures explícitamente simulados:
- Prediction ready: 200; OpenAPI contiene ambas funciones.
- Predicción: 200, origin=estimated.
- Recomendación con telemetría simulada: 200, eligible_for_review, executionAllowed=false.
- Dataset inválido para recomendación: 422.
- Gateway sin JWT: 401 para predicción y recomendación.
- Prometheus: job green-ai-prediction UP.

Evidencia: output/semana10/evidencias/smoke-reconciliacion.json y dataset-simulado-reconciliacion.json.
Construcción: output/semana10/reconcile-build.log.
Para repetir el smoke hay que regenerar el fixture con fechas recientes; las reglas rechazan datos vencidos.
Estas pruebas NO demuestran precisión observada, ahorro energético ni acceso de un usuario real de Supabase.

## Pendientes

1. Publicar los commits reconciliados cuando el usuario autorice el push; sin force push.
2. Probar el recorrido desde Frontend con sesión real del usuario y guardar capturas sin tokens.
3. El usuario prepara evidencia de definición, ejecución y resultado de rutinas Supabase.
4. Retirar del informe las afirmaciones de XGBoost final y ahorro 18,4 %: el usuario confirmó
   que no existen experimentos que las sustenten. No se ha editado el PDF original.
5. Las evaluaciones Word anteriores son diagnósticos históricos; actualizarlas solo con evidencia nueva.

URL de Swagger unificado: http://127.0.0.1:8002/docs
Frontend: http://127.0.0.1:3001

## Continuación con Gemini — contexto del criterio 5

El usuario encargó a Gemini la revisión punto por punto. Sus avances están en
`output/semana10/Revision_Arquitectura_Hexagonal.md`. Ese documento reporta avances
posteriores, incluida publicación remota, que no fueron verificados nuevamente por
Codex en la sesión de preparación del contexto. El estado «sin push» anterior es
histórico; consultar evidencias actuales antes de tomarlo como estado presente.

Para el criterio Supabase, leer `output/semana10/Contexto_Gemini_Criterio5_Supabase.md`.
Contiene requisitos docentes, funciones existentes, consultas de inspección,
evidencias esperadas y condiciones de cierre. Codex no ejecutó SQL en Supabase
ni recalificó los criterios al preparar ese documento.

## Migración a monorepo (2026-11-06, Claude Code)

El trabajo continúa en `green-ai-monorepo/` (Git propio, excluido del workspace por `.git/info/exclude`).
Estado, pruebas y pendientes actualizados: `green-ai-monorepo/docs/HANDOFF.md`. Este workspace no se modificó
salvo `.graphifyignore` (excluye el monorepo) y esta nota.
