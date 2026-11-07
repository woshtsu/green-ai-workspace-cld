# Fundamentos de Java Spring y arquitectura para Green AI

Para entender este proyecto necesitas reconocer cómo se representan datos, cómo se conectan objetos y dónde termina cada responsabilidad. Monitoring usa Java 21 y Spring Boot 4.1.1. Gateway declara además Spring Cloud 2025.1.3. Simulator usa Python y requiere Python 3.12 o superior. Estos valores proceden de la configuración del proyecto.

## 1 De una clase a un servicio

Una clase define datos y operaciones. Un objeto es una instancia concreta de esa clase. Un constructor recibe lo necesario para dejar el objeto listo. En `MonitoringService`, el constructor recibe una fuente de métricas y un reloj:

```java
public MonitoringService(MetricsSource source, Clock clock) {
    this.source = source;
    this.clock = clock;
}
```

`private` restringe el acceso al campo. `final` impide reasignar su referencia después de inicializarla; no convierte automáticamente todo objeto referenciado en inmutable. `this.source` identifica el campo del objeto, mientras que `source` identifica el parámetro.

La clase no construye dentro de sí un cliente HTTP ni decide qué servidor usar. Recibe esas decisiones mediante una dependencia. Esto permite trabajar con una fuente ficticia para pruebas, una fuente Prometheus para integración o una fuente que informa que no está configurada.

## 2 Interfaces y polimorfismo

Una interfaz describe qué operaciones debe ofrecer un objeto. `MetricsSource` declara la operación de consulta que necesita Monitoring. Distintas clases pueden implementar esa misma interfaz.

```text
MetricsSource
  ├── FixtureMetricsSource
  ├── PrometheusMetricsSource
  ├── UnavailableMetricsSource
  └── BoundedMetricsSource
```

El servicio utiliza `source.query(query)` sin preguntar qué clase concreta hay detrás. Eso es polimorfismo: la llamada usa un contrato común y cada implementación resuelve la operación a su manera. No significa que todas las fuentes tengan el mismo comportamiento de disponibilidad; sí deben respetar los tipos y reglas del contrato.

`BoundedMetricsSource` es especial porque envuelve a otra fuente. Añade protección de tiempo y concurrencia antes de delegar la consulta. Es un ejemplo del patrón decorador: un objeto mantiene la interfaz de otro y añade comportamiento alrededor.

Una analogía útil es un tomacorriente: el consumidor necesita una conexión compatible, no conocer cómo se genera la electricidad. La interfaz representa la conexión; el adaptador concreto resuelve el detalle externo.

## 3 Records colecciones y enums

Un `record` de Java sirve para representar datos y genera constructor, accesores, igualdad y representación textual. El proyecto utiliza records para `MetricDefinition`, `MetricQuery`, `Resource`, `Sample` y `Response`.

```java
public record Sample(Instant timestamp, Double value, Quality quality) { }
```

El acceso al valor se escribe `sample.value()`. `Double` permite `null`; `double` no. Esta diferencia es necesaria porque una muestra ausente no tiene un número válido. El campo `quality` explica la causa.

Los records no garantizan inmutabilidad profunda. Una lista recibida podría modificarse desde otro lugar. Por eso aparecen `List.copyOf` y `Map.copyOf`: producen colecciones no modificables y evitan conservar directamente la colección mutable recibida. Esto simplifica razonar sobre respuestas durante su procesamiento.

Un `enum` limita los valores posibles a un conjunto con nombre. `Quality` admite `valid`, `missing` y `non_finite`. Es más seguro que escribir cadenas arbitrarias en cada método: reduce errores tipográficos y permite un `switch` explícito.

Una `List` guarda una secuencia de elementos. Un `Map` relaciona claves con valores, como timestamp → número. Un `Set` evita duplicados; Monitoring lo utiliza para comprobar identidades de series. En `MetricCatalog.require`, un stream recorre las definiciones, filtra por identificador y lanza un fallo si no encuentra una métrica permitida.

## 4 Inyección de dependencias y beans

La inyección de dependencias consiste en entregar a un objeto sus colaboradores desde fuera. Spring administra objetos llamados beans y los conecta usando su configuración. En este proyecto, `MonitoringConfiguration` construye el servicio con `new MonitoringService(source, clock)` dentro de un método `@Bean`. El servicio participa en Spring sin importar clases de Spring en su propio archivo. La terminología de bean e inyección corresponde al [contenedor IoC de Spring](https://docs.spring.io/spring-framework/reference/core/beans/introduction.html).

La ventaja concreta aparece en las pruebas: se puede construir el servicio con una fuente controlada y un reloj fijo. No es necesario arrancar Prometheus para comprobar cómo se rellenan los huecos de una serie.

No todo servicio de negocio necesita `@Service`. Aquí se ha preferido registrar explícitamente el bean para mantener el núcleo independiente del framework. El punto importante no es acumular anotaciones, sino saber quién construye cada objeto.

## 5 Anotaciones que sí aparecen

| Anotación | Lectura práctica en este proyecto |
| --- | --- |
| `@SpringBootApplication` | Marca la clase de arranque y activa la configuración habitual de Boot |
| `@Configuration` | Reúne métodos que conectan los componentes |
| `@Bean` | Registra el objeto devuelto por un método |
| `@Profile("fixture")` | Activa una configuración cuando se selecciona ese perfil |
| `@Profile("!fixture")` | Activa la alternativa cuando fixture no está activo |
| `@ConfigurationProperties` | Agrupa propiedades externas en un objeto tipado |
| `@RestController` | Declara el adaptador que atiende peticiones y devuelve cuerpos HTTP |
| `@RequestMapping` | Define el prefijo de rutas del controlador |
| `@GetMapping` | Asocia un método Java a una operación GET |
| `@RequestParam` | Recibe parámetros de la URL |
| `@RestControllerAdvice` | Centraliza el tratamiento de excepciones web |
| `@ExceptionHandler` | Indica qué excepción maneja un método |
| `@Component` | Registra un componente detectado por Spring |
| `@Order` | Establece prioridad de ejecución en componentes ordenados |

Aunque el POM incluye validación, las reglas importantes de consulta que vemos aquí están escritas en `QueryParameters` y `MetricQuery`. No debes explicar este código como si toda su validación dependiera de `@Valid` o de anotaciones en campos.

## 6 Arquitectura hexagonal

La arquitectura hexagonal organiza el software alrededor de su lógica y de los contratos con el exterior. El nombre no exige seis carpetas ni seis conexiones.

El dominio define qué es una métrica, una consulta válida o un fallo. La aplicación coordina el trabajo: consultar, verificar y normalizar. Los puertos son interfaces que expresan lo que la aplicación ofrece o necesita. Los adaptadores conectan esos puertos con HTTP, Prometheus o archivos. La configuración ensambla los objetos.

```text
HTTP → MetricsController → QueryMetrics → MonitoringService
                                              ↓
                                         MetricsSource
                                              ↑
                         Fixture o Prometheus o fuente no disponible
```

Las flechas de invocación y las dependencias de código no son idénticas. El servicio invoca una fuente, pero solo importa su interfaz. El adaptador Prometheus depende de los tipos del núcleo para implementarla. Así, cambiar el proveedor externo no exige introducir HTTP en el dominio.

Un puerto hexagonal no es un puerto TCP. `MetricsSource` es un contrato Java; `8080` es un número de comunicación de red. Es frecuente que ambas palabras aparezcan en la misma explicación y conviene diferenciarlas.

En Simulator el dominio también está aislado. Sin embargo, su `runner.py` importa adaptadores concretos y los crea directamente. Es una separación por capas con ensamblaje directo en la aplicación; no es una réplica exacta de los puertos explícitos de Monitoring. Esta precisión demuestra que estás describiendo el código y no solo un diagrama ideal.

## 7 HTTP JSON y contrato

Una petición HTTP contiene método, ruta, parámetros y cabeceras; algunas operaciones llevan cuerpo. En `GET /api/v1/metrics/current?metric=node.memory.used`, GET expresa consulta, la ruta selecciona la operación y `metric` selecciona una métrica.

JSON representa datos mediante objetos, listas, cadenas, números, booleanos y null. No transporta objetos Java directamente. La serialización convierte los records a bytes JSON; la deserialización interpreta el JSON que devuelve Prometheus.

`ResponseEntity` permite controlar estado, cabeceras y cuerpo. Monitoring devuelve `ResponseEntity<byte[]>` porque primero serializa con un límite de tamaño. Así puede rechazar una respuesta demasiado grande antes de enviar un cuerpo exitoso incompleto.

Un contrato define campos, tipos, unidades, rutas y errores. OpenAPI lo describe en un archivo que otros desarrolladores y herramientas pueden consultar. Aquí es estático: modificar un controlador no actualiza mágicamente el contrato. Las pruebas de contrato ayudan a detectar diferencias.

## 8 Maven Boot y ejecución

Maven gestiona dependencias y fases de construcción. El POM declara qué necesita el proyecto. El parent de Boot aporta gestión de versiones y convenciones; el BOM de Spring Cloud coordina dependencias de Cloud. Tener una versión declarada no sustituye probar la compatibilidad efectiva.

`test` ejecuta las pruebas de esa fase. `package` produce el artefacto, normalmente un JAR. `verify` recorre las fases hasta la verificación y ejecuta los controles configurados. No significa que exista automáticamente una prueba end-to-end de todos los contenedores.

El wrapper permite usar la versión de Maven configurada por el repositorio. El Dockerfile de Monitoring usa su wrapper; el de Gateway utiliza Maven de la imagen de construcción. Ambos Dockerfiles Java omiten la ejecución de pruebas con `-DskipTests`, por lo que construir la imagen no demuestra que la suite haya pasado.

## 9 Comprobación de aprendizaje

**¿Por qué inyectar `Clock`?** Para controlar qué significa ahora en pruebas de rangos y evitar resultados dependientes de la hora real.

**¿Por qué `Double` en Sample?** Porque la ausencia y los valores no finitos se representan con null, acompañados de calidad.

**¿Puede existir un servicio de negocio sin `@Service`?** Sí. En este proyecto se construye desde un método `@Bean`.

**¿Arquitectura hexagonal significa microservicios?** No. La primera organiza el código; los microservicios separan procesos y responsabilidades desplegables. Pueden combinarse.

## Archivos para acompañar la lectura

- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/application/MonitoringService.java`
- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/domain/MetricData.java`
- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/configuration/MonitoringConfiguration.java`
- `green-ai-monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/in/web/MetricsController.java`
- Los archivos `pom.xml` de Monitoring y Gateway.
