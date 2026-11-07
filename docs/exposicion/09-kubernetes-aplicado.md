# Kubernetes desde cero y su aplicación prevista en Green AI

Kubernetes serviría para gestionar dónde se ejecutan los componentes, cómo se descubren y cómo se recuperan. Al revisar el workspace el 23 de septiembre de 2026, `green-ai-deployment` no contiene manifiestos. Esta guía propone un diseño didáctico; no declara un clúster desplegado ni ofrece un paquete completo para producción.

## 1 Diferencia respecto a Docker Compose

Una imagen de contenedor sigue siendo útil en Kubernetes. El cambio está en quién administra su ejecución. Compose describe servicios de una aplicación para un motor Docker; Kubernetes administra recursos declarados en un clúster y reconcilia lo deseado con lo observado.

No es necesario reescribir la lógica Java para que un contenedor pueda ejecutarse allí. Sí hay que preparar imágenes accesibles, configuración, almacenamiento, disponibilidad y conectividad. Tampoco es obligatorio que los nodos utilicen Docker Engine: Kubernetes utiliza runtimes compatibles con su interfaz de ejecución.

## 2 Clúster nodo Pod y contenedor

Un clúster agrupa máquinas y un plano de control. Los nodos aportan capacidad para ejecutar aplicaciones. Un Pod es la unidad en la que Kubernetes agrupa uno o más contenedores que comparten red y determinados recursos. En una primera propuesta, cada Pod de Monitoring contendría un contenedor Java.

```text
Clúster de laboratorio
  Nodo trabajador A
    Pod monitoring → contenedor Java
    Pod gateway → contenedor Java
  Nodo trabajador B
    Pod prometheus → contenedor Prometheus
    Pod de un experimento → contenedor Python
```

Es un ejemplo de distribución, no la topología existente. Los nodos node-01 y node-02 del JSON del Simulator son objetos modelados: no se convierten en nodos Kubernetes al ejecutar el simulador.

El plano de control recibe las declaraciones por su API. El scheduler elige nodos para Pods pendientes; los controladores observan diferencias con el estado deseado; el kubelet del nodo coordina la ejecución local con el runtime. `kubectl` es un cliente de esa API, no el propio clúster.

## 3 Deployment y reconciliación

Un Deployment administra Pods mediante ReplicaSets y permite actualizaciones declarativas. Si se desean dos réplicas, el controlador busca mantenerlas; si un Pod desaparece, puede crear otro. No recupera la memoria del proceso anterior ni convierte el disco local en persistente. Véase [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

Para Monitoring y Gateway, un Deployment es una propuesta razonable porque no guardan una base de datos local de negocio. Dos réplicas requieren, además, revisar la capacidad del upstream: dos instancias Monitoring con límite de dieciséis consultas cada una pueden ejercer más presión agregada sobre Prometheus.

Incrementar replicas no significa distribuirlas obligatoriamente entre máquinas distintas. La ubicación depende del scheduler y las restricciones configuradas. Tampoco garantiza que una consulta individual sea más rápida.

## 4 Service y DNS

Las IP de Pods pueden cambiar. Un Service ofrece una identidad de red estable y selecciona Pods mediante etiquetas. Un Service ClusterIP permite acceso interno; no ejecuta por sí mismo la aplicación. Un selector incorrecto puede dejarlo sin endpoints. Véase [Services](https://kubernetes.io/docs/concepts/services-networking/service/).

Si se acuerda un namespace green-ai y un Service monitoring, el Gateway del mismo namespace podría consultar `http://monitoring:8080`. Desde otro namespace se podría usar `monitoring.green-ai`, o el nombre completo con el dominio real del clúster. `cluster.local` es un dominio común, no un dato confirmado del laboratorio.

No existe una traducción automática de los nombres del Compose a Services: hay que crearlos y configurar sus puertos. Un Namespace organiza recursos, pero no constituye por sí solo aislamiento de red.

## 5 Ingress y API Gateway son capas diferentes

Una propuesta de acceso sería:

```text
Navegador → entrada HTTP del clúster → Service gateway → Pod Gateway
                                                    → Service monitoring
                                                    → Pod Monitoring
```

La entrada del clúster podría usar un controlador Ingress o una implementación de Kubernetes Gateway API. Debe instalarse/configurarse la implementación correspondiente. Spring Cloud Gateway es nuestra aplicación proxy; no es el mismo producto que Kubernetes Gateway API.

En esta arquitectura se expondría al frontend la entrada del Gateway y se mantendrían internos Monitoring y Prometheus. El dominio público, HTTPS y CORS requieren coordinación. Crear un Service interno no reemplaza una política de acceso y autenticación.

## 6 ConfigMap Secret y almacenamiento

Una ConfigMap puede contener configuración no confidencial, como la URL de Monitoring o los intervalos de scrape. Un Secret puede suministrar material sensible a los componentes que lo necesiten. No corresponde entregar secretos Supabase a Monitoring o Gateway, porque no tienen ese rol.

Base64 en un Secret no equivale a cifrado. El acceso se controla con permisos y configuración del clúster; la protección en reposo debe tratarse explícitamente. No se incluyen credenciales en estos ejemplos. Véase [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).

Un PersistentVolumeClaim solicita almacenamiento. El volumen que lo satisface depende de la infraestructura y StorageClass. Para Prometheus y archivos de experimentos se tendría que acordar capacidad, modos de acceso y política de conservación. Un PVC no reemplaza las copias de seguridad. Véase [volúmenes persistentes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

## 7 Probes y recursos

Readiness indica si un contenedor está listo para recibir tráfico; una comprobación fallida permite retirarlo de endpoints preparados. Liveness puede provocar reinicio cuando falla repetidamente. Startup protege el período de arranque antes de activar las otras comprobaciones. Véase [probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/).

Para los servicios Java existen rutas Actuator de liveness y readiness. No garantizan datos disponibles en Prometheus. Una caída externa no debería convertirse sin análisis en reinicios constantes de todos los consumidores.

Los requests orientan la planificación de recursos; los limits limitan su uso. `250m` de CPU representa 0.25 unidades de CPU; `256Mi` representa 256 MiB de memoria. Superar el límite de CPU puede producir throttling; superar el de memoria puede terminar en OOM. Estos valores son de configuración, no porcentajes de las métricas sintéticas. Véase [gestión de recursos](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

## 8 Ejemplo explicado de Monitoring

Este manifiesto es ilustrativo y parcial. Requiere namespace green-ai, imagen publicada con el nombre real y un Service prometheus disponible. El registro y los recursos son valores de ejemplo; no se ha aplicado al clúster ni medido su capacidad.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitoring
  namespace: green-ai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: monitoring
  template:
    metadata:
      labels:
        app: monitoring
    spec:
      containers:
        - name: monitoring
          image: registry.example.com/green-ai-monitoring:ejemplo
          ports:
            - name: http
              containerPort: 8080
          env:
            - name: MONITORING_PROMETHEUS_URL
              value: http://prometheus:9090
            - name: MONITORING_PROMETHEUS_INSTANCE_LABEL
              value: node
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: "1"
              memory: 512Mi
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: http
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: http
            periodSeconds: 10
          startupProbe:
            httpGet:
              path: /actuator/health/liveness
              port: http
            periodSeconds: 5
            failureThreshold: 30
---
apiVersion: v1
kind: Service
metadata:
  name: monitoring
  namespace: green-ai
spec:
  selector:
    app: monitoring
  ports:
    - name: http
      port: 8080
      targetPort: http
  type: ClusterIP
```

El selector coincide con la etiqueta del template. El Service dirige al puerto llamado http del contenedor. El Deployment elige la imagen y las variables; el Service proporciona dirección de acceso. La configuración node supone fuentes con esa etiqueta; si se incorporan exporters de equipos reales también deben alinearse las identidades.

## 9 Cómo se trasladaría cada componente

| Componente | Propuesta y decisión pendiente |
| --- | --- |
| Gateway | Deployment y Service; acceso externo controlado |
| Monitoring | Deployment y Service internos; fuente configurada |
| Prometheus | Despliegue con almacenamiento y descubrimiento; podría administrarse con un operador |
| Simulator finito | Job por experimento, almacenamiento de resultados y scrape mientras viva |
| Data Processing | Deployment para API o Job para procesamiento finito según su contrato |
| Prediction | Deployment si sirve inferencia; Jobs para tareas de entrenamiento si se acuerdan |
| Supabase | Servicio externo si se usa una instancia alojada; no hay que replicarlo dentro por usar Kubernetes |

Un StatefulSet puede servir para aplicaciones que requieren identidad persistente y almacenamiento asociado; no es una obligación universal para cualquier base de datos. La elección de Prometheus debe considerar la instalación de observabilidad que ya tenga el laboratorio.

## 10 Inspección y criterios de aceptación

Comandos de lectura para un futuro clúster autorizado, sustituyendo el namespace si difiere:

```powershell
kubectl config current-context
kubectl get namespaces
kubectl -n green-ai get deployments,pods,services,jobs
kubectl -n green-ai get endpointslices
kubectl -n green-ai logs deployment/monitoring --tail=60
```

Antes de cambios hay que verificar contexto y namespace. Aquí no se ejecutaron comandos kubectl ni se crearon recursos.

El despliegue se consideraría comprobado cuando imágenes y Pods arranquen, Services resuelvan, probes funcionen, Prometheus recolecte cada fuente prevista y las consultas actuales e históricas conserven identidad y origen. Habría que verificar además reinicios, persistencia y la ruta pública. Convertir un YAML no cierra esas pruebas.

**Pregunta de defensa:** «¿Por qué Kubernetes?» Respuesta: «Para administrar ejecución, recuperación, descubrimiento y escalado de componentes en el entorno acordado. La demo local todavía usa Compose. Kubernetes no implementa el análisis de energía ni las métricas de negocio por nosotros».
