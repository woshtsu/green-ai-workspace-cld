# Diagnóstico inicial de la entrega

Fecha de revisión: 29 de octubre de 2026. Revisión de Git, configuración Compose y APIs locales; no se reconstruyeron contenedores ni se modificó el código.

## Versiones

- Monitoring: main local en d476c32; GitHub main consultado en 70b6f6b6cda464779ebdf6868d23c517563fa807. Git indica un commit local por delante de origin/main.
- Gateway: main local en 0a41e30; GitHub main consultado en 4977e17bff8c4113794497417341d69b92b7d460. Git indica un commit local por delante de origin/main.
- Frontend: rama local integration/design-monitoring en f55a82b; esa rama remota coincide. GitHub main está en 0ef8a5c9dbfa108c133e2d59392dc6b032757058. La diferencia de commits requiere comprobar integración; no prueba por sí sola qué cambios faltan en main.
- Prediction: rama local Criss, df883a9, sin diferencias respecto a la referencia local origin/Criss. No se consultó el HEAD remoto en esta comprobación.
- Data Processing: main local b6ccb2c, sin diferencias respecto a la referencia local origin/main. No se consultó el HEAD remoto en esta comprobación.
- Simulator: main local 47536d7, sin diferencias respecto a la referencia local origin/main. No se consultó el HEAD remoto en esta comprobación.
- Recommendations: su carpeta no pertenece a un repositorio Git detectado; publicación no acreditada.

## Docker y pruebas iniciales

- Siete servicios del proyecto aparecen corriendo: simulator, prometheus, monitoring, data-processing, prediction, gateway y frontend. Recommendations no aparece corriendo.
- El Compose principal construye imágenes del código local; no monta el código fuente de las aplicaciones. Reiniciar contenedores no incorpora cambios del código. Hay montajes de configuración, que son un caso diferente.
- Prediction y Data Processing se levantaron con docker-compose.yml y compose.swagger.yaml según las etiquetas Docker. Los puertos publicados son 8002 y 8003 respectivamente.
- GET http://127.0.0.1:8002/health/ready devolvió HTTP 200, modelLoaded=true, horizon=15m y precise=false. Esto acredita disponibilidad del artefacto, no calidad predictiva.
- GET http://127.0.0.1:8003/openapi.json devolvió HTTP 200 y rutas de históricos, entre otras. La documentación publicada incluye preparación de datasets.
- POST http://127.0.0.1:8081/api/prediction/v1/predictions sin credenciales devolvió HTTP 401. Es una comprobación de rechazo anónimo, no una prueba de inferencia autenticada.

## Diferencia que debe resolverse antes del build

El archivo local green-ai-data-processing/Green-IA/data-processing-service/infrastructure/adapters/input/api/routes.py contiene únicamente /health, mientras el OpenAPI del contenedor incluye rutas adicionales. El contenedor y el archivo local revisado no representan la misma implementación de rutas. Debe localizarse la versión completa antes de reconstruir; todavía no se investigó si existe otra fuente local que registre esas rutas.

## Próximos pasos

Hallazgo posterior: la rama local feature/data-processing-integration (92caeac) sí contiene las rutas /metrics/history, /historical-logs y /prediction/dataset en el mismo archivo. Es la candidata a reconciliar con main; aún no se comparó su contenido completo con la imagen en ejecución. En Frontend, git log main..integration/design-monitoring muestra commits de integración que no son ancestros del main local; esto no descarta una integración equivalente por squash y debe revisarse por contenido.

1. Localizar y comparar las ramas con la implementación completa, especialmente Data Processing y Frontend. No cambiar ramas ni reconstruir sin conservar la versión funcional.
2. Fijar los commits de entrega y reconciliar publicación remota con el código probado.
3. Reconstruir únicamente desde las fuentes correctas, preservando los archivos Compose usados y los datos existentes.
4. Ejecutar predicción y recomendación con sesión válida desde la aplicación; conservar entradas y respuestas sin tokens.
5. El usuario confirmó que no existen los experimentos de XGBoost ni el ahorro de 18,4 %. Retirar esas cifras del informe; no sustituirlas por otras sin una ejecución identificada.
6. Supabase: preparar evidencia de definición, invocación y resultado de las rutinas. Las capturas del esquema por sí solas no demuestran ejecución.

Los documentos Word anteriores corresponden a la revisión previa. Este diagnóstico registra comprobaciones nuevas; todavía no permite cambiar los criterios a suficiente.
