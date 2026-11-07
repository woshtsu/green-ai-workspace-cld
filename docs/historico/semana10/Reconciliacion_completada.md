# Reconciliación local y recomendaciones integradas

Verificación del 29 de octubre de 2026.

## Resultado

Data Processing y Frontend quedaron reconciliados en `main`. Prediction permanece
en `Criss` y contiene ahora recomendaciones y cálculo energético. Gateway enruta
esas funciones a Prediction, conservando los prefijos públicos y la autenticación.
La política de recomendaciones está separada del adaptador HTTP y la inferencia
se invoca localmente, sin otro contenedor ni llamada HTTP a sí mismo.

| Repositorio | Rama | Commit local | Publicación pendiente |
| --- | --- | --- | --- |
| Data Processing | main | 92caeac | 8 commits |
| Frontend | main | 59d0fd2 | 10 commits |
| Prediction | Criss | 8585d6b | 1 commit |
| Gateway | main | 9d043fa | 2 commits |
| Monitoring | main | d476c32 | 1 commit previo |
| Simulator | main | 47536d7 | Ninguna respecto a origin/main |

No se hizo push. Los árboles de trabajo de estos repositorios quedaron limpios.
El historial previo de Data Processing, Frontend y Prediction está respaldado en
`git-backup/*.bundle`. Frontend conserva ambos historiales originales mediante un
commit de merge; no se borraron ramas ni se sobrescribieron commits remotos.

El código del antiguo servicio independiente está archivado en
`legacy/green-ai-recommendations`, fuera de la configuración activa. No se borró.

## Verificación

| Componente | Resultado |
| --- | --- |
| Data Processing | 88 pruebas aprobadas |
| Prediction | 96 pruebas aprobadas |
| Recomendaciones en la imagen final | 13 pruebas aprobadas; incluidas en la suite anterior |
| Gateway | 11 pruebas aprobadas durante Maven verify |
| Frontend | 13 pruebas aprobadas |

Los contenedores de Prediction, Gateway, Frontend y Data Processing fueron
reconstruidos y actualizados; Prometheus fue actualizado para recolectar métricas
de Prediction. Los siete servicios están corriendo. Se conservaron los volúmenes.

El smoke HTTP comprobó predicción y recomendación con respuestas 200, entrada
inválida con 422 y acceso anónimo por Gateway con 401. Prometheus reportó Prediction
UP. Las solicitudes y respuestas están en `evidencias/smoke-reconciliacion.json`.
Los datos utilizados son simulados: no representan precisión experimental ni ahorro.

## Cómo comprobarlo

1. Abrir `http://127.0.0.1:8002/docs`: Prediction muestra `/v1/predictions`,
   `/v1/recommendations` y `/v1/energy` en el mismo Swagger.
2. Abrir `http://127.0.0.1:3001` e iniciar sesión para la prueba de usuario real
   pendiente. No compartir tokens ni contraseñas en capturas.
3. Conservar `docker-compose.yml`, `compose.swagger.yaml`, `prometheus-demo.yml`
   y `observability/alerts.yml` al compartir el workspace: los archivos de la raíz
   no están incluidos en los commits de los repositorios hijos.

Quedan pendientes publicación en GitHub, capturas autenticadas y evidencia Supabase.
Los Word previos no se han recalificado automáticamente. El PDF original tampoco
se editó: deben retirarse XGBoost como resultado final y el ahorro 18,4 % sin respaldo.

El estado técnico detallado para continuar está en `HANDOFF.md`.
