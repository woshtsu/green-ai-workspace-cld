# Supabase y las relaciones del diagrama de Green AI

La BD Supabase se relaciona directamente con Data Processing para históricos y, mediante un adaptador futuro, con Simulator para inventario. Monitoring consulta Prometheus; Gateway transporta peticiones; Prediction recibe datos preparados. Ninguno de estos últimos necesita consultar directamente Supabase en la arquitectura acordada.

Esa es una asignación de responsabilidades. No demuestra que todos esos adaptadores estén implementados: el Compose actual solo incluye Simulator, Prometheus, Monitoring y Gateway, y no configura credenciales Supabase.

## 1 Cómo leer la imagen indicada

![Diagrama general de capas y flujos de Green AI](../project-docs/diagrama.png)

La imagen es un diagrama de arquitectura, no el esquema de columnas de la base de datos. Las líneas sólidas representan el flujo que el diagrama marca como vigente; las discontinuas representan contratos futuros o pendientes. Las flechas indican quién inicia la solicitud, y la respuesta regresa por la misma conexión.

Así, Prometheus → Simulator significa que Prometheus inicia el scrape. No significa que Simulator invoque a Prometheus. Data Processing → Supabase significa que Data Processing solicita datos a la BD.

El diagrama agrupa por responsabilidad. Ubicar Workloads Kubernetes en la franja de observabilidad no convierte esas aplicaciones en una base de datos; las identifica como fuentes observables. Una flecha discontinua desde Gateway tampoco crea automáticamente una API en Simulator, cuya interfaz de control actual es CLI.

## 2 Qué es Supabase aquí

Supabase ofrece una base PostgreSQL y otros servicios asociados. PostgreSQL almacena tablas relacionadas, permite consultas SQL, restricciones e índices. Que Supabase tenga otros productos no implica que todos estén adoptados en Green AI. Véase [base de datos de Supabase](https://supabase.com/docs/guides/database/overview).

En particular, una tabla propia llamada usuario no demuestra que exista integración con Supabase Auth. El Gateway actual no valida JWT. También es una decisión del proyecto que el navegador no acceda directamente a Supabase: aunque la plataforma permite otros patrones, aquí se han definido servicios backend como frontera de acceso.

## 3 Quién accede directamente y para qué

| Componente | Acceso directo a Supabase según el diseño | Estado y alcance |
| --- | --- | --- |
| Data Processing | Sí, lectura autorizada de históricos logs y contexto acordado | Integración prevista; no servicio desplegado en este Compose |
| Simulator | Lectura de hardware mediante adaptador específico | Futuro; hoy usa JSON |
| Prediction | No | Recibe datasets/features de Data Processing |
| Monitoring | No | Consulta Prometheus; sin JPA/JDBC/SQL |
| API Gateway | No | Publica contratos HTTP de servicios |
| Frontend | No | Consume exclusivamente Gateway |
| Prometheus | No | Recolecta exporters y almacena series temporales |
| Workloads Kubernetes | No hay acceso definido por esa caja | Son fuentes a observar; no un cliente SQL único |

La tabla no concede propiedad de escritura. Decidir quién lee un histórico no decide quién inserta mediciones, predicciones, recomendaciones o evaluaciones SLA. Esas escrituras requieren contratos y un propietario explícito.

## 4 Prometheus y Supabase no son la misma historia

Prometheus conserva series para consultas de métricas. Supabase conserva registros relacionados del dominio. Ambos pueden contener información temporal, pero con identidades y esquemas distintos.

```text
Ruta de métricas actual
Frontend → Gateway → Monitoring → Prometheus → scrape a Simulator

Ruta analítica prevista
Data Processing → Monitoring para series normalizadas
Data Processing → Supabase para históricos autorizados
Data Processing → Prediction para inferencia con datos preparados

Ruta de inventario futura
Simulator → adaptador de inventario → Supabase.hardware
```

Las flechas de la primera línea resumen solicitudes; el scrape ocurre periódicamente, no necesariamente por cada consulta del frontend. No hay un flujo automático Prometheus → Supabase configurado. Si se requiere persistir resultados en PostgreSQL, habrá que implementar ese flujo y su semántica.

## 5 Qué tablas existen según la evidencia documental

El [modelo de BD](../project-docs/modelo-bd.md) y su [evidencia normalizada](../project-docs/assets/esquema-verificado.json) documentan una instantánea verificada el 22 de septiembre de 2026. Esta guía no ha consultado una BD en vivo.

```text
usuario 1 ─── N hardware 1 ─── N logs
```

`usuario.usuario_id` identifica al usuario. Cada hardware tiene un `usuario_id` obligatorio que lo relaciona con un usuario. Cada log tiene un `hardware_id` obligatorio que lo relaciona con un equipo.

Una clave primaria identifica una fila. Una clave foránea obliga a que su referencia exista. NOT NULL exige un valor; no acredita que ese valor sea correcto. UNIQUE en email evita repeticiones según la regla de PostgreSQL aplicada a esa columna.

Las FK documentadas tienen ON DELETE CASCADE: borrar un usuario puede eliminar sus equipos y, a través de ellos, sus logs. Esta es una característica que importa para diseñar conservación de evidencia; no se realizaron borrados ni se propone utilizarlos en la demo.

## 6 Lectura de hardware para un Simulator futuro

hardware contiene identificador, usuario, hostname, IP, cpu_cores, ram_gb, max_watts, ubicación, estado y fecha. No es directamente el JSON que entiende el motor actual.

| Campo SQL | Posible uso y condición |
| --- | --- |
| hardware_id | Identidad estable del nodo tras validar formato y correspondencia |
| cpu_cores | logical_cpus solo si se confirma que cuenta CPU lógicas |
| ram_gb | Conversión a bytes tras acordar GB o GiB |
| max_watts | Capacidad declarada; no potencia instantánea ni energía |
| hostname e ip_address | Metadatos, no sustituyen automáticamente node ni dirección del exporter |

Faltan interfaces, filesystems y sus capacidades, obligatorias para modelar esos recursos. El adaptador tendría que recibirlas de una fuente acordada o marcarlas como supuestos explícitos. No debe fabricarlas como observaciones físicas.

Ejemplo: un equipo registrado con ram_gb=16 podría significar 16 000 000 000 bytes o 17 179 869 184 bytes. Elegir una interpretación sin acuerdo modifica el experimento. Del mismo modo, ocho núcleos físicos no son necesariamente ocho CPU lógicas.

Una vez leído el hardware observado, los resultados del motor siguen siendo simulated. El origen de una capacidad de entrada y el origen de una salida modelada son conceptos diferentes.

## 7 Lectura de logs por Data Processing

logs contiene timestamp, CPU y RAM en porcentaje, temperatura, energia_watts, prediccion_watts, acción y cumple_sla, además de sus identificadores. No contiene las mismas cinco métricas ni el mismo sobre JSON que Monitoring.

Un ejemplo didáctico de consulta que podría efectuar un adaptador autorizado, usando parámetros enlazados por su biblioteca, sería:

```sql
SELECT hardware_id, "timestamp", cpu_utilization_pct,
       ram_utilization_pct, temperatura_celsius,
       energia_watts, prediccion_watts
FROM public.logs
WHERE hardware_id = :hardware_id
  AND "timestamp" >= :inicio
  AND "timestamp" < :fin
ORDER BY "timestamp";
```

`:hardware_id` y los otros nombres representan parámetros del cliente, no SQL listo para pegar sin enlazarlos. El rango semiabierto es una propuesta para particionar históricos SQL; Monitoring usa extremos inclusivos y al combinar fuentes hay que explicitar la diferencia.

Data Processing tendría que validar registros, alinear tiempos, conservar procedencia y preparar las features que Prediction espera. Convertir filas a un DataFrame es una decisión interna; la comunicación entre servicios se acuerda como JSON versionado.

## 8 Unidades que impiden una copia directa

`cpu_utilization_pct` está en porcentaje; `node.cpu.utilization` está en ratio. Dividir por cien solo es semánticamente válido si coinciden denominador y ventana. No basta con que ambos campos digan CPU.

`ram_utilization_pct` no se convierte en bytes sin conocer memoria total y definición del porcentaje. `energia_watts`, por su unidad, representa potencia en W aunque la columna se llame energía. `prediccion_watts` es estimación, no medición.

Temperatura y potencia no existen en el catálogo actual de Monitoring. Red y filesystem no tienen columnas equivalentes en el diagrama SQL. Por tanto, no se puede insertar la respuesta de Monitoring como si fuera una fila completa de logs.

Además logs no tiene columnas de cluster, origin o run ID para distinguir directamente ejecuciones simuladas. El diseño exige mantener separados los resultados sintéticos y los históricos reales.

## 9 Quién escribe predicciones y quién administra usuarios

La presencia de prediccion_watts no demuestra que Prediction escriba en PostgreSQL. El diseño prescribe que Prediction reciba datos de Data Processing y devuelva una respuesta estimada. El propietario de persistir esa respuesta aún debe acordarse; una opción futura sería un servicio responsable del resultado, pero no es una decisión implementada.

Tampoco se define aquí un servicio de usuarios listo. Los campos password y password_hash documentados no deben salir en contratos de métricas ni convertirse en parte del inventario. Un futuro diseño de identidad debe revisar cómo se autentica al usuario, qué se almacena y qué API tiene propiedad sobre esos datos.

`prediccion_watts`, `temperatura_celsius` y `energia_watts` son obligatorios sin defaults en la evidencia. Insertar solo CPU y RAM no satisface esas restricciones en una inserción ordinaria. No se arregla inventando ceros. El esquema, la fuente y el momento de escritura deben ser compatibles; no se inspeccionaron triggers para atribuirles un llenado automático.

`cumple_sla` admite null y tiene default true. Ese default no constituye una evaluación real de servicio: faltan criterios como umbral de latencia, disponibilidad y ventana. No hay que usarlo para afirmar calidad demostrada.

## 10 Acceso técnico y permisos

Un backend podría usar una conexión PostgreSQL o la API de datos de Supabase, según el adaptador y contrato elegidos. Esas son alternativas de implementación, no dos integraciones ya disponibles en estos servicios. Se deben configurar TLS, credenciales y permisos acordes al acceso necesario.

RLS significa control de filas mediante políticas. Estar habilitado no implica que las políticas restrinjan correctamente. Las credenciales con privilegios de bypass no deben exponerse al navegador. Véase [RLS de Supabase](https://supabase.com/docs/guides/database/postgres/row-level-security).

La evidencia local muestra RLS habilitada, no forzada, y políticas permisivas dirigidas a public con USING true en las tres tablas. No son un aislamiento por usuario. Los GRANT efectivos no se inspeccionaron, así que tampoco se puede concluir acceso público completo solo con esa información.

El acceso previsto de Simulator sería lectura mínima del inventario, sin usuarios o contraseñas. Data Processing tendría acceso autorizado a históricos y a los datos auxiliares estrictamente necesarios. Ninguna de esas credenciales debe añadirse a Monitoring o Gateway por comodidad.

## 11 Cómo encaja con Kubernetes

Si Supabase es un servicio alojado externo, los Pods autorizados se conectan a su endpoint externo. Kubernetes no crea esas tablas, no las replica y no las consulta por nosotros. Un Secret podría entregar la credencial a Data Processing o al adaptador futuro de Simulator; una política de salida podría limitar conectividad según capacidades de la red del clúster.

Esto no implica desplegar Supabase dentro del clúster. Elegir una instalación autogestionada sería otro alcance operativo, no deducible de la imagen actual.

## 12 Casos para defender el diagrama

**Mostrar CPU actual:** frontend → Gateway → Monitoring → Prometheus. Supabase no interviene.

**Preparar un histórico para inferencia:** Data Processing consulta las fuentes acordadas, transforma los datos y llama a Prediction. La lectura directa de Supabase corresponde a Data Processing; la API de predicción todavía necesita un contrato integrado.

**Simular un equipo inventariado:** un adaptador futuro lee hardware, valida y completa entradas, y entrega un inventario al motor. Los resultados permanecen simulados y se guardan como ejecuciones, sin insertarlos en logs reales.

**Guardar una recomendación:** falta acordar responsable y contrato de escritura, además de evaluación. El diagrama no permite afirmar que esa acción ya ocurre.

La explicación oral puede ser: «Supabase aporta datos relacionales del dominio; Prometheus aporta series observables. Data Processing es el punto previsto de preparación que puede combinar fuentes conservando su significado. Simulator solo tendría lectura de inventario mediante un adaptador futuro. La cadena vigente de Monitoring no depende de Supabase».
