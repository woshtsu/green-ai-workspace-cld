# API Gateway rutas WebFlux y acceso del frontend

API Gateway es la entrada HTTP prevista para el frontend. Actualmente publica tres operaciones de Monitoring. Centraliza rutas, prefijos, CORS y plazos de comunicación. No calcula métricas ni consulta directamente Prometheus, Simulator o Supabase.

## 1 Para qué separar una entrada pública

Si el frontend conociera cada dirección interna, quedaría acoplado a puertos y nombres de todos los servicios. El Gateway le ofrece una superficie estable. La red interna puede reorganizarse cambiando configuración del Gateway sin cambiar necesariamente las URLs públicas.

La separación introduce un salto adicional de red y otro proceso que debe funcionar. No elimina las validaciones del servicio interno. Monitoring sigue comprobando sus entradas incluso si la petición proviene del Gateway.

La regla arquitectónica dice que el frontend utiliza Gateway. El Compose de demostración, sin embargo, también publica los puertos de Monitoring y Prometheus al host. Eso facilita diagnóstico, pero no impone aislamiento de red. No afirmes que es físicamente imposible acceder directamente a los demás servicios en esta demo.

## 2 Ruta predicado y filtro

Una ruta contiene un identificador, destino, condiciones de coincidencia y filtros. En `application.yaml` existe `monitoring-metrics` con destino configurable mediante `GATEWAY_MONITORING_BASE_URL`.

Los predicados son condiciones: el path debe ser uno de tres valores explícitos y el método debe ser GET. Los filtros transforman la petición seleccionada. El framework encadena filtros antes y después de la comunicación con el destino, según el [funcionamiento oficial de Spring Cloud Gateway](https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/how-it-works.html).

No hay una ruta general que permita enviar cualquier path a cualquier microservicio. Un path no registrado queda fuera del proxy. Los endpoints propios de salud y el archivo OpenAPI siguen siendo superficies locales distintas.

## 3 Reescritura explicada segmento por segmento

```text
Entrada pública:         /api/monitoring/v1/metrics/current
StripPrefix=3 elimina:   /api/monitoring/v1
Ruta restante:           /metrics/current
PrefixPath=/api/v1:      /api/v1/metrics/current
```

El destino ya incluye host y puerto; los filtros resuelven la ruta. Los parámetros de consulta se conservan. El Gateway no convierte el cuerpo JSON ni vuelve a calcular los valores.

| URL pública | URL interna |
| --- | --- |
| `/api/monitoring/v1/metrics/catalog` | `/api/v1/metrics/catalog` |
| `/api/monitoring/v1/metrics/current` | `/api/v1/metrics/current` |
| `/api/monitoring/v1/metrics/history` | `/api/v1/metrics/history` |

La versión v1 pertenece al contrato de URL. La versión de aplicación o del archivo OpenAPI puede tener otro número. No hay obligación de que todas esas numeraciones sean iguales.

## 4 MVC frente a WebFlux

Monitoring usa Spring MVC, con API servlet y un filtro `OncePerRequestFilter`. Gateway utiliza Spring Cloud Gateway Server WebFlux y un `WebFilter` reactivo. Son modelos distintos de atender trabajo HTTP, aunque ambos participen en la misma cadena de red.

En un estilo bloqueante un hilo puede quedar esperando la respuesta de otra operación. En un estilo no bloqueante la operación pendiente permite que el mecanismo de ejecución atienda otros eventos. Esto resulta útil para un proxy que pasa tiempo esperando red. No significa que desaparezcan los hilos ni que todas las tareas sean paralelas.

`Mono<T>` representa una operación reactiva que puede producir como máximo un valor o terminar con un error. El filtro devuelve `Mono<Void>` porque su resultado representa la finalización del procesamiento, sin un objeto de datos propio.

La llamada `chain.filter(exchange)` entrega el intercambio al siguiente eslabón. El filtro no invoca `.block()`. Agregar una espera bloqueante indiscriminada en este recorrido reduciría las ventajas del modelo.

`exchange` agrupa petición y respuesta. `mutate()` crea una variante de la petición con la cabecera deseada; no se cambia un campo arbitrario de un objeto compartido. `beforeCommit` registra una operación para ajustar la cabecera de respuesta antes de que se envíe.

## 5 Correlación y su límite actual

Un request ID es un identificador para relacionar una petición con su respuesta y registros. No autentica al usuario ni prueba su identidad.

El Gateway acepta un `X-Request-Id` entrante si contiene de uno a 128 caracteres del conjunto permitido. En otro caso genera un UUID. Lo envía a Monitoring y lo fija nuevamente en la respuesta con `beforeCommit`.

Monitoring siempre genera su propio UUID, ignorando el recibido. Su respuesta de error incluye ese identificador local dentro de `requestId`. Por tanto, en una petición que pasa por ambos pueden existir dos IDs:

```text
Frontend envía:             ensayo-42
Gateway reenvía:            ensayo-42
Monitoring genera:          UUID-B
Problem JSON de Monitoring: requestId = UUID-B
Gateway fija cabecera:      X-Request-Id = ensayo-42
```

Este es el comportamiento inferido de los dos filtros actuales. No debe presentarse como trazabilidad distribuida unificada. El test del Gateway usa un servidor sustituto que devuelve el ID recibido; no reproduce la generación local de Monitoring.

Una futura decisión de integración tendría que acordar qué ID es confiable, cuándo generarlo y cómo propagarlo. Documentar esa mejora no equivale a haberla implementado.

## 6 CORS explicado con un caso real

Un origen del navegador combina esquema, host y puerto. `http://localhost:3001` y `http://127.0.0.1:3001` son orígenes distintos. Cuando una página llama a otro origen, el navegador aplica reglas CORS según las cabeceras del servidor.

Gateway permite un origen configurado, método GET y ciertas cabeceras. Expone `X-Request-Id` para que JavaScript pueda leerla. La configuración permite credenciales y fija un maxAge de 3600 segundos para la política correspondiente.

El valor por defecto en el YAML de Gateway es `http://127.0.0.1:3000`; el Compose del workspace establece `http://127.0.0.1:3001` salvo que la variable se sobrescriba. Debe coincidir con la URL real con la que se abre el frontend.

CORS no es un firewall ni autenticación. Un cliente como PowerShell no aplica las restricciones del navegador. Por eso una petición que funciona con `Invoke-RestMethod` puede fallar desde la página por CORS.

Permitir la cabecera Authorization no implementa JWT. Tampoco `allowCredentials: true` crea login o roles. No existe aquí autenticación real implementada.

Algunas peticiones provocan una comprobación previa OPTIONS del navegador. La ruta de negocio solo declara GET; la negociación CORS depende de la configuración y del framework. No conviene prometer cualquier caso de preflight sin probarlo con las cabeceras reales del frontend.

## 7 Timeouts y errores

Gateway configura un segundo para conectar con Monitoring y seis segundos de timeout de respuesta. Monitoring tiene su propio presupuesto de fuente. Dejar algo más de margen fuera permite, normalmente, recibir el error del servicio antes de que venza el proxy; no constituye una garantía absoluta bajo cualquier carga.

Si Monitoring devuelve un problema contractual, el proxy transporta su respuesta. Si Gateway falla antes de recibirla, el error es propio del Gateway. El código actual no incluye un traductor personalizado que garantice que todos esos errores locales usen el mismo esquema de Monitoring.

No hay filtros Retry, CircuitBreaker o RateLimiter configurados. Timeout limita espera; rate limiting limitaría frecuencia por cliente; circuit breaker cortaría temporalmente llamadas tras determinados fallos. Son conceptos relacionados con resiliencia, pero no intercambiables ni todos implementados.

## 8 Salud y documentación

`/actuator/health/liveness` y `/actuator/health/readiness` exponen estado del proceso. `/actuator/prometheus` expone instrumentación técnica del Gateway. Ninguno sustituye una consulta funcional que atraviese la cadena hasta Prometheus.

El archivo `/openapi/gateway-v0.1.yaml` describe la superficie externa. La definición de datos de Monitoring conserva la propiedad del esquema de respuesta, evitando mantener dos copias independientes que puedan divergir.

## 9 Qué comprueban las pruebas existentes

`GatewayApplicationTests` arranca un servidor HTTP sustituto, configura su URL como Monitoring y levanta el Gateway en un puerto aleatorio. Comprueba la ruta registrada, que una ruta desconocida devuelve 404, conservación de un request ID seguro y reescritura con preservación de parámetros.

Es una prueba útil de transporte. No demuestra por sí sola que la consulta Prometheus funcione, que todos los preflights sean correctos o que la correlación coincida con el Monitoring real. Cada afirmación requiere la prueba del nivel correspondiente.

## 10 Explicación oral breve

«El Gateway publica únicamente tres rutas GET de Monitoring. Reescribe el prefijo público al interno, conserva los parámetros y aplica configuración de origen y plazos. Usa WebFlux para encadenar operaciones de red sin introducir esperas bloqueantes en nuestro filtro. No incorpora autenticación ni lógica de métricas. La política de request IDs aún necesita unificarse con Monitoring».

## Archivos de referencia

- `green-ai-gateway/src/main/resources/application.yaml`
- `green-ai-gateway/src/main/java/pe/edu/continental/greenai/gateway/RequestIdFilter.java`
- `green-ai-gateway/src/test/java/pe/edu/continental/greenai/gateway/GatewayApplicationTests.java`
- `green-ai-gateway/src/main/resources/static/openapi/gateway-v0.1.yaml`
- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/in/web/RequestIdFilter.java`
