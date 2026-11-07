# Verificación — 2026-09-30 (America/Lima)

## Ejecutado en Docker

- Data Processing, Python 3.14: 88 pruebas aprobadas; dos avisos de deprecación de dependencias de test. Regresiones finales de filtros y paginación: 33 pruebas aprobadas.
- Gateway, Java 21: 9 pruebas aprobadas, incluyendo JWT de prueba firmado, roles, rutas, query codificada, errores y correlación.
- Compose del workspace incorpora Data Processing en la red interna y configura Gateway. Lee opcionalmente el `.env` del servicio sin copiar secretos a la imagen.
- Simulator, Prometheus, Monitoring, Data Processing y Gateway arrancados.
- Comparación HTTP real entre Monitoring y Data Processing: CPU, memoria y filesystem, 42 muestras cada uno; red recibida y transmitida, 63 cada una. Se compararon valores, calidad, labels, recurso, origen y unidad. Datos del simulador, no infraestructura observada.
- Dataset preparado: HTTP 200 y 21 muestras de CPU en porcentaje. No se ejecutó Prediction.
- Supabase sin configurar: 503 `SOURCE_NOT_CONFIGURED`, sin fallback ni datos ficticios.

## Cambios

Orden estricto `(timestamp, log_id)` dentro de páginas y contra el cursor; comprobación de filtros explícitos de Monitoring; tres rutas GET de Gateway con roles OPERATOR/ADMIN y timeout de 15 segundos; documentación actualizada.

## Repetir la comparación

Desde la raíz del workspace en PowerShell, con servicios levantados y muestras CPU disponibles:

```powershell
Get-Content -Raw software/data-processing/scripts/check_monitoring_integration.py | docker compose exec -T data-processing python -
```

El script solo consulta servicios privados. Falla si los valores no coinciden o no hay muestras válidas; recibir 200 por sí solo no basta.

## Pendientes externos

- Configurar permisos y acceso dedicado de lectura a Supabase; no se comprobó una lectura real en esta sesión.
- Probar una sesión Supabase real hacia Data Processing por Gateway. Las pruebas usan claves y emisor aislados, no una sesión real.
- Conectar inferencia y presentación en Frontend en la siguiente etapa. Preparar un dataset no implica haber ejecutado una predicción.

Esta evidencia reemplaza los estados de Docker/Gateway anteriores; no certifica funcionalidades externas pendientes.
