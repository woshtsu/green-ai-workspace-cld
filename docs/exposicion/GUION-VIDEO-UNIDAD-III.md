# GUION TÉCNICO Y DE PRODUCCIÓN DEL VIDEO DE SOFTWARE — UNIDAD III
## Proyecto Green AI: Optimización Energética y Predictiva en Centros de Datos

- **Asignatura:** Taller de Proyectos 1 — ISI (Universidad Continental)
- **Docente:** Jorge A. Guevara Jiménez
- **Duración objetivo:** 25 minutos exactos (rango reglamentario de 20 a 30 minutos)
- **Entorno de grabación:** Nube pública en producción/desarrollo (GitHub Pages + Render + Supabase; estrictamente sin localhost)
- **Resolución de pantalla:** Full HD (1920×1080), 30 o 60 fotogramas por segundo
- **Participación:** 100 % de los integrantes con cámara web activa y nombre completo visible en pantalla


> **Antes de grabar:** verificadas el 07/11/2026 solo las URLs de Gateway, Data Processing y Prediction (`https://green-ai-prediction-dev-zxly.onrender.com`). Copia las de Monitoring, Simulator y Prometheus desde el panel de Render: pueden tener un sufijo aleatorio.
>
> **Mantener despiertos los servicios:** 25 min antes de grabar ejecuta `python herramientas_IA/video/mantener_despierto.py` en una terminal que no se grabe (consulta los 6 servicios cada 4 min y se detiene sola a las 2 h). Un 429 o un 504 aislado es un límite del plan gratuito de Render entre servicios: espera al siguiente refresco (30 s) y explícalo con honestidad si sale en cámara.

---

## 0. CAMBIOS RECIENTES Y HERRAMIENTAS DE APOYO (leer antes de ensayar)

**URL que se graba (producción):** https://woshtsu.github.io/green-ai-workspace-cld/ (no `/dev/`). Abrirla con **Ctrl + F5** la primera vez.
El backend son los servicios de Render `green-ai-*-dev` (los únicos desplegados); en las escenas de terminal, Swagger o Prometheus se verá ese nombre: es el entorno en la nube que usa producción.

**Cambios del 08/11/2026 para que el video salga estable**
| Cambio | Antes | Ahora | Qué se nota en cámara |
|---|---|---|---|
| Refresco del dashboard, Racks y Red de flujos | 15 s | **30 s** | Los gráficos cambian cada 30 s: tras pulsar «Actualizar» o entrar a una vista, esperar hasta medio minuto para mostrar un cambio. El texto «Actualizado … · cada 30 s» lo confirma. |
| Prometheus → métricas internas de Prediction | 15 s | **60 s** | Nada en la app: la CPU de los 50 nodos sigue llegando del simulador cada 15 s. En Prometheus, el objetivo `green-ai-prediction` se actualiza cada minuto. |
Motivo: Render (plan gratuito) responde a veces **429** a las llamadas entre servicios por URL pública y **504** cuando un servicio arranca en frío. Menos llamadas = menos avisos en pantalla. No es un problema de rendimiento del código (Monitoring responde en ~0,5 s).

**Herramienta 1: mantener despiertos los servicios** (`herramientas_IA/video/mantener_despierto.py`)
1. 25 min antes de grabar, en una terminal que **no** se graba: `python herramientas_IA/video/mantener_despierto.py`
2. Cada 4 min imprime una línea como `12:01:10 gateway OK 0.8s | monitoring OK 0.4s | …`. El primer ciclo puede tardar 20–60 s por servicio (están despertando).
3. Empezar a grabar cuando 2 ciclos seguidos muestren los 6 en `OK` con menos de 2 s.
4. Se detiene sola a las 2 h (`--minutos 120`) para no gastar el cupo gratuito; Ctrl + C la detiene antes.

**Herramienta 2: carga masiva para el episodio 3** (`herramientas_IA/video/carga_transacciones.py`)
- `python herramientas_IA/video/carga_transacciones.py --login --iteraciones 200 --concurrencia 3` (601 transacciones reales: dataset + predicción + recomendación por iteración). Pide correo y contraseña sin mostrarlos.
- **Ensayarla antes** con `--iteraciones 5`. Durante la carga, la app puede mostrar algún aviso de espera: es normal.
- Si aparecen 429 o 504 en la tabla final, leerlos tal cual en cámara y explicarlos (límite de la capa gratuita); no repetir hasta «maquillar» el resultado.

**Si en cámara aparece un aviso de espera o error 429/504:** esperar el siguiente refresco (30 s); la app se recupera sola. Si persiste más de 2 min, revisar la terminal de la herramienta 1.

---

## 0.5 GRABACIÓN POR PARTES (modalidad acordada por el equipo)

Cada integrante graba **su** parte en su PC y **Jhonny Cristhian Quintana Carhuaricra** las une en la edición. La rúbrica exige que «participan de la exposición todos los integrantes del grupo con cámara y nombre completo»: cada clip lleva la cámara del presentador en la esquina inferior derecha y su nombre en un rótulo.

### Quién graba qué
| Clip | Episodio (minutos) | Graba | Necesita | Desde |
|---|---|---|---|---|
| 00 | Carátula: cada uno dice su nombre completo a cámara (5–10 s por persona) | **Los 4** (cada uno su clip) | Solo cámara | Cualquier PC |
| 01 | Introducción (00:00–01:30) | Jhonny + Gina (cada uno su tramo) | Diapositiva de portada | Cualquier PC |
| 02 | Ep. 1 PMV1 (01:30–04:30) | Leonid | Navegador + cuenta propia en producción | Cualquier PC |
| 03 | Ep. 2 PMV2 (04:30–08:00) | Leonid (racks, flujos) y Jhonny (CSV, energía) | Navegador + cuenta propia | Cualquier PC |
| 04 | Ep. 3 Data masiva (08:00–11:30) | **Ricardo** | Repo clonado + Python + `carga_transacciones.py` | PC de Ricardo |
| 05 | Ep. 4 Métricas (11:30–15:00) | Gina (ML) y Jhonny (pruebas) | **Solo navegador** (GitHub Actions y GitHub) | Cualquier PC |
| 06 | Ep. 5 Predicción ML (15:00–18:30) | Gina | Navegador + cuenta propia; simulador despierto ≥ 30 min | Cualquier PC, **dentro de la franja** |
| 07 | Ep. 6 Trello (18:30–21:00) | Gina y Jhonny | Tablero ya actualizado según `guias/trello/GUIA-TRELLO-POR-INTEGRANTE.md` | Cualquier PC |
| 08 | Ep. 7 Hexagonal y SQL (21:00–24:00) | **Ricardo** | Navegador (GitHub) | Cualquier PC |
| 09 | Cierre (24:00–25:00) | **Los 4** (cada uno su frase, 10–15 s, mirando a cámara) | Cámara | Cualquier PC |

### Franja común de grabación (obligatoria para los clips con la app: 02, 03, 04, 06)
1. Acordar una franja de 2 h (p. ej., 19:00–21:00).
2. **Ricardo**, 30 min antes de la franja: `python herramientas_IA/video/mantener_despierto.py --minutos 150` en una terminal que no se graba. Avisa por el grupo cuando dos ciclos seguidos muestren los 6 servicios en `OK`.
3. Gina graba el Ep. 5 a partir del minuto 30 de la franja (el simulador necesita historial; si sale «datos insuficientes», esperar 10 min y repetir).
4. Los clips 00, 01, 05, 07, 08 y 09 no usan la app en vivo: se pueden grabar en cualquier momento.

### Ajustes comunes (para que el montaje no se note)
- Pantalla completa a **1920×1080**, navegador **Chrome** o **Edge** con zoom al 100 %, tema claro, sin barra de marcadores ni pestañas personales, notificaciones del sistema desactivadas.
- **OBS Studio**: lienzo y salida a 1920×1080, 30 fps, grabación en **MP4**. Escena: captura de pantalla completa + cámara de 320×180 px en la esquina inferior derecha + rótulo de texto (Arial 28, blanco sobre franja verde) con el **nombre completo**.
- Audio: micrófono o audífonos con micrófono; grabar en un lugar silencioso; probar 10 s antes.
- Cada uno inicia sesión con **su propia cuenta** (`register.html` si no tiene). Nunca compartir contraseñas ni mostrar tokens (no abrir F12 → Application).
- Respetar la duración de su tramo (± 15 s); dejar 2 s de silencio al inicio y al final del clip para los cortes.

### Entrega de los clips
- Nombre del archivo: `clip-NN-apellido.mp4` (p. ej., `clip-04-porras.mp4`), subido a la carpeta compartida del grupo el día acordado.
- Jhonny Cristhian une los clips en orden (DaVinci Resolve, CapCut o Clipchamp), añade la portada y el cierre con los 4 rostros, revisa que dure 22–26 min y comprueba la lista de rúbrica de la sección «Cierre».
- Si un clip muestra un error real (429, 504, «datos insuficientes»), **no se corta para ocultarlo**: el presentador lo explica, como indica la sección 0.

---

## 1. CÓMO USAR ESTE GUION

Este documento es la partitura técnica y organizativa para la grabación del video de sustentación de la Unidad III. Para asegurar fluidez, profesionalismo y cumplimiento estricto de la rúbrica, el equipo debe seguir estas directrices operativas:

1. **Ensayo previo de sincronización:**
   - Realizar una corrida completa de ensayo sin grabación previa para cronometrar las intervenciones y verificar que el tiempo total se mantenga entre 22 y 26 minutos.
   - Sincronizar el momento exacto en que un presentador concluye y el siguiente toma la palabra, evitando silencios incómodos o interrupciones.
2. **Quién lleva el teclado y el ratón (operador de pantalla):**
   - Una sola persona física del equipo debe operar la computadora principal donde se graba la pantalla completa en OBS Studio (se recomienda a Leonid Huamán o Ricardo Porras).
   - Dicho operador es quien navega entre pestañas, hace clics en los botones, selecciona opciones y mueve el cursor para resaltar los elementos de la interfaz.
   - Los demás integrantes exponen su parte hablando con su cámara encendida mientras el operador ejecuta las acciones sincronizadas que marca el guion.
3. **Teleprompter y ayudas visuales en un segundo monitor:**
   - Nunca abras este archivo ni ningún apunte en la pantalla que está siendo grabada por OBS.
   - Abre este guion en un segundo monitor, en una tableta o en un teléfono móvil situado justo al lado o encima de la cámara web. Esto permite mantener la mirada orientada hacia la cámara mientras se leen las pautas y diálogos.
4. **Regla de oro: lectura en vivo de datos y resultados (marcadores `[leer ...]`)**:
   - Para ser rigurosamente honestos con el evaluador y no incurrir en falseamiento de datos, **está terminantemente prohibido anticipar cifras que dependan de la ejecución en vivo** (como latencias milimétricas, conteos exactos de peticiones exitosas o estados puntuales).
   - Donde el diálogo indique corchetes como `[leer en vivo el total de HTTP 200 de la tabla]` o `[leer la latencia p50 registrada]`, el expositor debe mirar directamente la pantalla y pronunciar la cifra exacta que arrojó el sistema en ese instante.
   - Si la prueba arroja errores controlados (por ejemplo, respuestas HTTP 503 por arranque en frío de Render o HTTP 422 por acumulación de historial), el guion incluye las pautas para explicar con madurez de ingeniería por qué ocurren y cómo los gestiona el software.

---

## 2. RESUMEN EJECUTIVO Y CRONOGRAMA DE EPISODIOS

### 2.1 Integrantes y Roles en la Demostración

| Integrante | Rol en el Proyecto | Responsabilidad en la Demostración | Episodios Asignados |
|---|---|---|---|
| Jhonny Cristhian Quintana Carhuaricra | Product Owner | Introducción, gestión de requerimientos, auditoría de pruebas y métricas | Carátula, Ep. 2, Ep. 4, Ep. 6, Cierre |
| Gina Diana Barrera Peña | Scrum Master | Gestión ágil, ingeniería de datos, métricas y modelos de Machine Learning | Carátula, Ep. 4, Ep. 5, Ep. 6, Cierre |
| Leonid Kisley Orlando Huamán Collazos | Infraestructura / Frontend | Operación de UI, telemetría en tiempo real, topología y observabilidad | Ep. 1, Ep. 2, Cierre |
| Ricardo Porras Veli | Backend / Arquitectura | Pruebas de carga masiva, arquitectura hexagonal, procedimientos SQL y CI/CD | Ep. 3, Ep. 7, Cierre |

### 2.2 Cronograma Maestro por Episodio

| Minuto | Episodio / Sección | Criterio de Rúbrica | Presentador | Descripción Sintética |
|---|---|---|---|---|
| 00:00 – 01:30 | Carátula e Introducción | Guion — Carátula | Jhonny Quintana / Gina Barrera | Presentación de integrantes, objetivos técnicos de la Unidad III y arquitectura general en la nube. |
| 01:30 – 04:30 | Episodio 1: Pruebas funcionales PMV1 | Guion — Ep. 1 | Leonid Huamán | Autenticación Supabase, observabilidad de 50 nodos, telemetría CPU/memoria/red/disco con procedencia declarada. |
| 04:30 – 08:00 | Episodio 2: Pruebas funcionales PMV2 | Guion — Ep. 2 / Ind. 9 | Leonid Huamán / Jhonny Quintana | Vista Racks con calor, Red de flujos con rebalanceo simulado, reporte histórico CSV y cálculo de energía/CO₂e. |
| 08:00 – 11:30 | Episodio 3: Pruebas con data masiva | Guion — Ep. 3 / Ind. 9 | Ricardo Porras | Ejecución del script `carga_transacciones.py` (601 transacciones autenticadas), percentiles p50/p95, control de errores y CSV. |
| 11:30 – 15:00 | Episodio 4: Pruebas con métricas | Guion — Ep. 4 / Ind. 5 | Gina Barrera / Jhonny Quintana | Métricas ML (MAE/RMSE/mejora vs persistencia), 433 pruebas por componente (+ 14 de smoke = 447), optimización Docker y Prometheus. |
| 15:00 – 18:30 | Episodio 5: Predicciones con ML PMV1 y PMV2 | Guion — Ep. 5 / Ind. 10 | Gina Barrera | Caso 1: Demanda a 15 min con Random Forest. Caso 2: Recomendación con restricciones de memoria/latencia y bloqueo de ejecución. |
| 18:30 – 21:00 | Episodio 6: Tablero Trello y contenidos | Guion — Ep. 6 / Ind. 4, 11 | Gina Barrera / Jhonny Quintana | Trazabilidad Scrum/Kanban, historias de usuario PMV1 y PMV2, criterios Given/When/Then y políticas de calidad. |
| 21:00 – 24:00 | Episodio 7: Arquitectura hexagonal y SQL | Guion — Ep. 7 / Ind. 11 | Ricardo Porras | Inspección de repositorios en GitHub (Data Processing y Monitoring), triggers/funciones PL/pgSQL en Supabase y CI/CD. |
| 24:00 – 25:00 | Cierre, créditos y matriz de rúbrica | Cierre y formalidad | Los 4 integrantes | Resumen de lecciones aprendidas, confirmación de requisitos y despedida formal del equipo. |

---

## 3. PROTOCOLO DE PREPARACIÓN TÉCNICA (T-60 A T-0)

El despliegue en la nube utiliza el plan gratuito de Render. Dado que las instancias inactivas se suspenden tras 15 minutos sin tráfico, y que el servicio de predicción requiere al menos 20 minutos de historial continuo emitido por el simulador para no arrojar HTTP 422 `INSUFFICIENT_DATA`, es imperativo ejecutar esta secuencia cronometrada.

### 3.1 Cronograma de Despertar de Servicios (T-60 a T-25)

1. **T-60 min: Despertar el simulador de telemetría**
   - URL: `https://green-ai-simulator-dev.onrender.com/health` (*verificar antes de grabar*)
   - Acción: Enviar petición GET mediante navegador o curl.
   - Propósito: Iniciar la generación continua de series de tiempo de los 50 servidores (muestreo a 5 y 15 segundos).
2. **T-55 min: Despertar Prometheus**
   - URL: `https://green-ai-prometheus-dev.onrender.com/-/healthy` (*verificar antes de grabar*)
   - Acción: GET `/-/healthy` y verificar en `/api/v1/targets` que los targets `green-ai-simulator` y `green-ai-prediction` figuren en estado `UP`.
3. **T-50 min: Despertar Monitoring Service (Java)**
   - URL: `https://green-ai-monitoring-dev.onrender.com/actuator/health` (*verificar antes de grabar*)
   - Acción: GET `/actuator/health` y validar respuesta HTTP 200 con estado `UP`.
4. **T-45 min: Despertar Data Processing Service (FastAPI)**
   - URL: `https://green-ai-data-processing-dev.onrender.com/api/v1/health`
   - Acción: GET `/api/v1/health` y validar respuesta HTTP 200 `{"status":"healthy","service":"data-processing-service","project":"Green AI"}`.
5. **T-40 min: Despertar Prediction Service (FastAPI / Inferencia)**
   - URL: `https://green-ai-prediction-dev-zxly.onrender.com/health/ready`
   - Acción: GET `/health/ready` y confirmar `{"modelLoaded": true}`. Tarda ~45 segundos si la instancia estaba suspendida.
6. **T-35 min: Despertar API Gateway (Go)**
   - URL: `https://green-ai-gateway-dev.onrender.com/actuator/health`
   - Acción: GET `/actuator/health` (o `-healthcheck`) confirmando que enruta correctamente hacia Prediction, Data Processing y Monitoring.
7. **T-30 a T-10 min: Ventana de acumulación de telemetría**
   - Dejar correr el stack durante al menos 20 a 25 minutos sin interrumpir para acumular la ventana deslizante requerida por los modelos predictivos.

### 3.2 Preparación del Entorno de Navegación (T-15 a T-5)

1. **Pestañas del navegador (orden estricto de izquierda a derecha en una ventana dedicada):**
   - Pestaña 1: Frontend Green AI — Inicio / Login (`https://woshtsu.github.io/green-ai-workspace-cld/login.html`)
   - Pestaña 2: Frontend Green AI — Dashboard (`https://woshtsu.github.io/green-ai-workspace-cld/dashboard.html`)
   - Pestaña 3: Frontend Green AI — Racks con calor (`https://woshtsu.github.io/green-ai-workspace-cld/network.html`)
   - Pestaña 4: Frontend Green AI — Red de flujos (`https://woshtsu.github.io/green-ai-workspace-cld/flows.html`)
   - Pestaña 5: Prometheus UI (`https://green-ai-prometheus-dev.onrender.com/targets`) (*verificar antes de grabar*)
   - Pestaña 6: Tablero Trello oficial del proyecto Green AI
   - Pestaña 7: Repositorio GitHub (`https://github.com/woshtsu/green-ai-workspace-cld`) abierto en la rama `test`
2. **Configuración de la interfaz gráfica:**
   - Ocultar la barra de marcadores del navegador (`Ctrl + Shift + B`).
   - Zoom del navegador configurado al 100 % (verificar legibilidad en 1920×1080).
   - Modo oscuro activo en el frontend (para coherencia visual con la estética Cyber Fleet).
   - Cerrar mensajerías instantáneas (WhatsApp, Discord, Telegram, Slack) y activar el modo Asistente de concentración de Windows para evitar notificaciones emergentes.
   - Seguridad y privacidad: Verificar que no haya contraseñas visibles, tokens de Supabase ni llaves API expuestas en pantalla.

### 3.3 Configuración de OBS Studio y Dispositivos (T-10 a T-0)

1. **Resolución de lienzo y salida:** 1920×1080 píxeles a 30 fps o 60 fps estables.
2. **Escena única de grabación:**
   - Fuente principal: Captura de pantalla completa (Display Capture) del monitor principal.
   - Fuente secundaria: Cámara web de los integrantes (o videoconferencia en Google Meet/Zoom donde los 4 miembros estén con cámara activa) ubicada en la esquina superior o inferior derecha, sin obstruir menús, tablas ni gráficos de KPIs.
   - Rótulos (Lower Thirds): Cuadro de texto identificador en la esquina inferior con el nombre completo y rol del estudiante que tiene la palabra en cada segmento.
3. **Parámetros de grabación en OBS:**
   - Formato de grabación: MKV (Matroska). Regla crítica: nunca grabar directamente en MP4 para evitar la pérdida del archivo completo ante un corte de energía o fallo de proceso.
   - Remux automático: Activar en OBS *Configuración → Avanzado → Remux automático a MP4*.
   - Codificador de video: Hardware (NVENC H.264 o AMD AMF); tasa de bits de 8000 a 10000 Kbps; perfil `high`.
   - Audio: 48 kHz, filtro de cancelación de ruido (RNNoise) y limitador a -2 dB en los micrófonos de los 4 integrantes.
4. **Verificación de audio:** Prueba de voz de 15 segundos con cada presentador para equilibrar volúmenes relativos.

---

## 4. ARQUITECTURA DE PRUEBAS CON DATA MASIVA (EPISODIO 3)

### 4.1 Especificación del Script de Carga (`herramientas_IA/video/carga_transacciones.py`)

Para cumplir rigurosamente con el Indicador 9 de la rúbrica (demostración con datos de 500 a 1000 transacciones sobre el entorno de calidad en la nube), el repositorio cuenta con el script automatizado en Python:

```bash
python herramientas_IA/video/carga_transacciones.py --login \
    --gateway https://green-ai-gateway-dev.onrender.com \
    --iteraciones 200 --concurrencia 3 \
    --out docs/evidencias/carga-video.csv
```

1. **Flujo transaccional real del script:**
   - **Transacción inicial (1):** Descubrimiento de nodos con `GET /api/monitoring/v1/metrics/current?metric=node.cpu.utilization`.
   - **Iteraciones en bucle concurrente (200 iteraciones × 3 transacciones = 600 transacciones):**
     1. `GET /api/processing/v1/prediction/dataset`: Extrae la ventana histórica de 2 horas de CPU del nodo correspondiente.
     2. `POST /api/prediction/v1/predictions`: Ejecuta la inferencia del primer caso de uso de ML (demanda futura a 15 min).
     3. `POST /api/recommendations/v1/recommendations`: Evalúa el segundo caso de uso (recomendación prescriptiva bajo restricciones).
   - **Total de transacciones ejecutadas:** Exactamente $1 + 600 = 601$ transacciones reales atravesando el API Gateway en Render.
2. **Gestión de credenciales y seguridad:**
   - Al pasar el parámetro `--login`, el script solicita interactivamente el correo y la contraseña mediante `getpass` (la contraseña no se muestra en pantalla) y obtiene el JWT comunicándose directamente con Supabase Auth mediante la llave publicable de `software/frontend/config.local.js`. Alternativamente, acepta la variable de entorno `GREENAI_JWT`.
   - El token nunca se imprime en consola ni se guarda en texto plano en archivos de registro.
3. **Concurrencia controlada y protección del plan gratuito:**
   - Concurrencia establecida en `--concurrencia 3` workers mediante `ThreadPoolExecutor`.
   - Razón técnica: Evita saturar el límite de 512 MB de RAM de los contenedores gratuitos en Render, minimizando la aparición de errores 502/504 por ahogamiento de socket.
4. **Salida en consola y tabla de resultados:**
   - Barra de progreso periódica: `[   10/200] transacciones:   31 · HTTP 200: 31`.
   - Tabla final tabulada:
     ```text
     operación            n   200   otros   p50 ms   p95 ms
     descubrir_nodos      1   ...     ...      ...      ...
     dataset            200   ...     ...      ...      ...
     prediccion         200   ...     ...      ...      ...
     recomendacion      200   ...     ...      ...      ...
     Códigos HTTP: {200: ...}
     Estados de recomendación: {'eligible_for_review': ..., 'blocked': ...}
     CSV: docs/evidencias/carga-video.csv
     ```
5. **Persistencia de auditoría:** Guarda todas las filas en `docs/evidencias/carga-video.csv` con columnas: `iteracion`, `operacion`, `http`, `latencia_ms`, `nodo`, `detalle`, `hora`.

### 4.2 Pautas de Interpretación y Honestidad Experimental

Durante la ejecución del script en vivo, el presentador debe destacar los siguientes puntos técnicos:
- **Resiliencia del Gateway:** Se valida la autenticación continua, la comprobación criptográfica de firmas mediante JWKS y el enrutamiento inverso hacia Data Processing y Prediction.
- **Lectura en vivo:** Se leen directamente los datos que arroje la consola al terminar la prueba.
- **Gestión transparente de contingencias:** Si aparecen respuestas HTTP 503 o 504 debido al arranque en frío de algún contenedor de Render, o HTTP 422 por requerir mayor acumulación de historial, se explica con naturalidad al evaluador que el sistema registra fielmente las condiciones de un entorno gratuito en la nube sin falsear las estadísticas.
- **Aclaración honesta:** Se reitera que la prueba demuestra capacidad transaccional y funcional del software, pero que la telemetría subyacente proviene del simulador, por lo que no se reclaman ahorros físicos de energía hasta las mediciones reales del PMV3.

---

## 5. GUION PASO A PASO POR EPISODIO

---

### CARÁTULA E INTRODUCCIÓN INSTITUCIONAL (00:00 – 01:30)

#### Datos de la Escena
- **Minuto inicio:** 00:00 | **Minuto fin:** 01:30 | **Duración:** 1 minuto 30 segundos
- **Presentadores:** Jhonny Cristhian Quintana Carhuaricra (Product Owner) y Gina Diana Barrera Peña (Scrum Master)
- **Cámaras:** en la edición se abre con los clips 00 (los 4 integrantes, cada uno diciendo su nombre completo a cámara con su rótulo) y luego Jhonny y Gina graban cada uno su tramo de introducción.
- **Criterio de rúbrica:** Guion del video de software — Carátula con nombre de proyecto e integrantes.

#### Acción en Pantalla
1. Mostrar la diapositiva o pantalla de carátula institucional conteniendo:
   - Logotipo oficial de la Universidad Continental.
   - Asignatura: Taller de Proyectos 1 — ISI (Semana 12 / Unidad III).
   - Docente: Jorge A. Guevara Jiménez.
   - Título del proyecto: Green AI — Plataforma Inteligente de Observabilidad y Optimización Energética Predictiva en Centros de Datos.
   - Nombres completos de los 4 integrantes con sus roles.
   - Entorno tecnológico: Despliegue en la Nube (GitHub Pages, Render, Supabase).
2. Transicionar suavemente a la pestaña del navegador con la página de inicio del frontend (`https://woshtsu.github.io/green-ai-workspace-cld/index.html`).

#### Diálogo del Presentador
- **Jhonny Quintana (00:00 – 00:50):**
  > "Estimado profesor Jorge Guevara y compañeros, un cordial saludo. Mi nombre es Jhonny Cristhian Quintana Carhuaricra, Product Owner del proyecto Green AI. En este video de sustentación de la Unidad III, nuestro equipo presentará la demostración funcional completa del software desarrollado para el Primer y Segundo Mínimo Viable. Cumpliendo rigurosamente con los lineamientos de la asignatura y la lista de cotejo de la Semana 12, esta grabación se realiza a pantalla completa sobre nuestro entorno de calidad desplegado en la nube pública, sin recurrir a localhost. Participamos los cuatro integrantes del equipo, cada uno con su cámara y su nombre completo en pantalla. A continuación, mi compañera Gina Barrera presentará el alcance de los integrantes."

- **Gina Barrera (00:50 – 01:30):**
  > "Buenas tardes, profesor. Mi nombre es Gina Diana Barrera Peña, Scrum Master del equipo y responsable del área de datos y modelos. Me acompañan en esta presentación Ricardo Porras Veli, encargado de backend, integración y despliegue; y Leonid Kisley Orlando Huamán Collazos, a cargo de infraestructura, observabilidad y frontend. A lo largo de esta sesión cubriremos siete episodios técnicos: desde las pruebas funcionales de observabilidad del PMV1, las capacidades avanzadas del PMV2, una prueba transaccional masiva con más de 600 peticiones en vivo, la sustentación de métricas de calidad y Machine Learning, los dos casos de uso predictivos, nuestro tablero de gestión ágil en Trello y la auditoría de arquitectura hexagonal y procedimientos almacenados en GitHub. Doy pase a Leonid para iniciar con el Episodio 1."

#### Resultado Esperado y Plan B
- **Resultado esperado:** Transición limpia de carátula a navegador, audio balanceado sin eco y nombres plenamente identificables.
- **Plan B si falla:** Si la diapositiva no renderiza en OBS, presentar directamente la carátula integrada en el pie de página del `index.html` del frontend que contiene el copyright y los datos del proyecto.

---

### EPISODIO 1: PRUEBAS FUNCIONALES DEL PMV1 (01:30 – 04:30)

#### Datos de la Escena
- **Minuto inicio:** 01:30 | **Minuto fin:** 04:30 | **Duración:** 3 minutos 00 segundos
- **Presentador:** Leonid Kisley Orlando Huamán Collazos
- **Criterio de rúbrica:** Guion del video de software — Episodio 1: Pruebas funcionales del PMV1 (HU-01, HU-02, HU-15).

#### Acción en Pantalla
1. Navegar a `https://woshtsu.github.io/green-ai-workspace-cld/login.html`.
2. Mostrar el formulario de inicio de sesión con Supabase. Escribir credenciales de un usuario autenticado con rol `OPERATOR` (por ejemplo, `operador@greenai.continental.edu.pe`).
3. Hacer clic en «Iniciar sesión». Mostrar la redirección instantánea hacia `dashboard.html`.
4. Señalar en la barra superior (topbar):
   - El distintivo de perfil: Nombre del usuario y la etiqueta del rol `OPERATOR`.
   - La etiqueta de la plataforma: «PMV 2 · Demostración».
5. En la sección «Centro de operación», seleccionar:
   - Métrica: «Utilización de CPU» (`node.cpu.utilization`).
   - Clúster: «Todos los clústeres».
   - Periodo histórico: «15 minutos».
6. Clic en «Actualizar».
7. Mostrar el panel de KPIs en la pestaña «Resumen»:
   - Media del conjunto: Señalar el valor numérico en pantalla.
   - Servidor más cargado y servidor menos cargado.
   - Cantidad de servidores en respuesta: Confirmar 50 nodos detectados.
   - Metadato crítico de honestidad: «Procedencia: Simulado» y «Cobertura: Completa».
8. Desplazarse al gráfico interactivo Chart.js («Evolución de la métrica»):
   - Mostrar la curva de la media temporal y las bandas de máximo y mínimo.
   - Abrir la barra de comparación: presionar «5 más cargados» para observar las 5 series individuales superpuestas.
9. Cambiar a la pestaña «Detalle por servidor»:
   - Mostrar la tabla paginada con 50 servidores.
   - Utilizar el buscador de servidor: escribir `HW045`.
   - Mostrar columnas: Clúster, Servidor, Valor de CPU actual, Procedencia (`simulated`), Calidad (`ok`) e Instante de lectura.
   - Probar la ordenación por columnas haciendo clic en la cabecera «Valor».

#### Diálogo del Presentador
- **Leonid Huamán (01:30 – 04:30):**
  > "Gracias, Gina. Saludos, profesor. Mi nombre es Leonid Huamán. Iniciamos el Episodio 1 con la validación funcional del Primer Mínimo Viable, cuyo objetivo central es dotar a los operadores de centros de datos de una observabilidad integral y en tiempo real.
  > Como se aprecia en pantalla, nos encontramos en la URL pública de producción en GitHub Pages. El acceso está protegido por Supabase Authentication. Inicio sesión con una cuenta de operador. Al ingresar, el API Gateway valida el token JWT emitido por Supabase mediante su conjunto de llaves públicas JWKS. En la cabecera superior confirmamos mi identidad y el rol `OPERATOR` inyectado dinámicamente en los claims del token.
  > En el Centro de Operación, consulto la métrica de utilización de CPU para los 50 servidores del centro de datos simulado. Al pulsar 'Actualizar', el frontend invoca al Gateway en Render, el cual consulta al microservicio de Monitoring en Java y a Prometheus.
  > Observen los indicadores clave: se procesan exactamente 50 servidores. [Mirar la pantalla y leer en vivo]: la media global se sitúa en [leer el valor de stat-mean en pantalla, ej. 85 %], con el servidor [leer el nombre de stat-max] como el más cargado. Destaco un principio de diseño fundamental de nuestro equipo: la procedencia declarada. La plataforma indica explícitamente que el origen es 'Simulado', cumpliendo con la exigencia académica de honestidad técnica.
  > En el gráfico central de Chart.js visualizamos la evolución temporal de los últimos 15 minutos con agregación de media, máximo y mínimo. Mediante la barra de comparación rápida, podemos filtrar instantáneamente los cinco servidores más cargados para diagnosticar puntos calientes.
  > Finalmente, en la pestaña 'Detalle por servidor', accedemos a la tabla paginada con búsqueda instantánea. Filtro el servidor HW045 y verificamos su carga actual, estado de calidad y marca de tiempo. Con esto demostramos la operatividad completa de las historias de usuario HU-01 y HU-02 del PMV1 sobre la nube."

#### Resultado Esperado y Plan B
- **Resultado esperado:** Carga de 50 servidores en menos de 2 segundos, procedencia `simulated`, gráfico Chart.js fluido y tabla paginada operativa.
- **Plan B si falla:** Si el Gateway devuelve HTTP 504 Gateway Timeout por arranque en frío de Monitoring o Prometheus en Render, esperar 30 segundos, presionar «Actualizar» nuevamente y explicar en cámara que las instancias del plan gratuito se reaniman en la primera llamada de red.

---

### EPISODIO 2: PRUEBAS FUNCIONALES DEL PMV2 (04:30 – 08:00)

#### Datos de la Escena
- **Minuto inicio:** 04:30 | **Minuto fin:** 08:00 | **Duración:** 3 minutos 30 segundos
- **Presentadores:** Leonid Kisley Orlando Huamán Collazos y Jhonny Cristhian Quintana Carhuaricra
- **Criterio de rúbrica:** Guion del video de software — Episodio 2: Pruebas funcionales del PMV2 / Indicador 9.

#### Acción en Pantalla
1. En la barra de navegación superior, hacer clic en «Racks» (`network.html`).
2. Demostrar la vista «Racks con calor» (Topología física de infraestructura):
   - Señalar las 3 tarjetas KPI superiores: Nodos > 80 % de CPU, CPU media del clúster y Rack más cargado.
   - Mostrar la cuadrícula de 50 servidores agrupados en 5 racks físicos (Rack A a Rack E, 10 servidores por rack).
   - Explicar la escala térmica de colores: celdas verdes (< 50 %), amarillas (50–70 %), naranjas (70–80 %) y rojas (> 80 %).
   - Pasar el cursor sobre un servidor crítico (ej. `HW012` o `HW045` en rojo): mostrar el tooltip con ID de nodo, utilización exacta, memoria y procedencia de datos.
   - Presionar el botón «Actualizar» para evidenciar la sincronización en vivo cada 30 segundos.
3. En la barra superior, hacer clic en «Red de flujos» (`flows.html`):
   - Mostrar el lienzo con líneas interconectadas y partículas en movimiento simulando rebalanceo de carga.
   - Señalar la franja de advertencia técnica: «Propuesta ilustrativa sobre datos simulados. No se ejecuta ninguna acción (`executionAllowed=false`)».
   - Ajustar los controles interactivos: slider de «Sensibilidad» a 0.8 y «Máx. flujos» a 15. Mostrar cómo se recalculan dinámicamente los flujos propuestos entre servidores sobrecargados y servidores con holgura.
4. Volver a `dashboard.html` y abrir la pestaña «Reportes y experimento»:
   - En la tarjeta «Reporte de históricos»: consultar `HW045`, fechas del 2026-07-10 al 2026-07-11.
   - Clic en «Ver resumen»: mostrar la agregación de muestras procesadas por el Data Processing Service.
   - Clic en «Descargar CSV»: evidenciar la descarga real del archivo tabular en el navegador.
   - En la tarjeta «Baseline vs Green AI»: mostrar los KPIs comparativos de riesgo de SLA y energía modelada entre la heurística reactiva tradicional y la optimización Green AI.
5. Cambiar a la pestaña «Energía y CO₂e»:
   - Clic en «Calcular con el simulador» (opción 1): mostrar la conversión de series de CPU a potencia modelada según la fórmula física $P = P_{idle} + (P_{max} - P_{idle}) \times CPU$.
   - Mostrar el cálculo resultante en kWh.
   - Introducir en el campo «Factor de emisión»: `0.245` kg CO₂e/kWh y fuente «Sistema Eléctrico Interconectado Nacional — MINEM 2025». Mostrar el cálculo resultante de emisiones evitables.

#### Diálogo del Presentador
- **Leonid Huamán (04:30 – 06:15):**
  > "Continuando con el Episodio 2, pasamos a las innovaciones funcionales del Segundo Mínimo Viable.
  > Nos trasladamos a la vista 'Racks con calor'. En esta pantalla transformamos las series temporales en una representación topológica real de centros de datos. Los 50 servidores se distribuyen en cinco racks estándar de 10 unidades cada uno. La visualización utiliza un mapa de calor dinámico donde cada celda representa un nodo físico: los tonos naranjas y rojos advierten de cuellos de botella térmicos y de cómputo. [Leer en pantalla]: actualmente registramos [leer el valor de kpi-high-cpu] nodos por encima del 80 % de carga. Al interactuar con el servidor HW012, el sistema despliega telemetría granular en tiempo real.
  > Pasamos ahora a la 'Red de flujos', una funcionalidad visual pionera de Green AI. Esta vista mapea un algoritmo heurístico de balanceo de cargas: identifica qué servidores están saturados y proyecta flujos de reasignación hacia nodos fríos con capacidad ociosa. Las partículas animadas representan la transferencia de carga computacional. Destaco fuertemente la leyenda inferior: se trata de una propuesta ilustrativa basada en telemetría simulada; nuestro sistema mantiene por diseño la política `executionAllowed=false`, garantizando que ninguna acción se ejecute automáticamente sin supervisión humana."

- **Jhonny Quintana (06:15 – 08:00):**
  > "Tomando la palabra, profesor, en la pestaña 'Reportes y experimento' del panel principal, demostramos la persistencia y recuperación histórica gestionada por el microservicio de Data Processing. Ejecutamos una consulta agregada para el servidor HW045 y descargamos el reporte en formato CSV, listo para auditorías operacionales. Asimismo, en el cuadro de experimentación exponemos la comparativa entre la política base reactiva y el enfoque preventivo de Green AI, destacando la reducción de riesgo de degradación de SLA.
  > Finalmente, en la sección 'Energía y CO₂e', el sistema integra un modelo matemático de potencia lineal donde un servidor en reposo consume el 40 % de su potencia máxima. Al presionar 'Calcular con el simulador', se integran las áreas bajo la curva en kilovatios-hora mediante la regla trapezoidal. [Mirar la pantalla y leer]: obtenemos un consumo modelado de [leer el valor en kWh calculado]. Demostrando nuestra honestidad académica, el impacto de huella de carbono se mantiene como 'no evaluable' hasta que el usuario ingresa un factor de emisión validado con su respectiva fuente bibliográfica, como el factor oficial del SEIN de Perú. Con esto completamos el alcance funcional del PMV2."

#### Resultado Esperado y Plan B
- **Resultado esperado:** Renderizado sin errores de Racks, animación fluida en Red de flujos, descarga exitosa del CSV y cálculo numérico de kWh.
- **Plan B si falla:** Si el cálculo de energía con el simulador tarda más de 5 segundos, hacer clic en «Calcular con el ejemplo» (opción 2) que procesa 12 muestras locales precargadas en el cliente y muestra exactamente el mismo flujo matemático.

---

### EPISODIO 3: PRUEBAS CON DATA MASIVA (08:00 – 11:30)

#### Datos de la Escena
- **Minuto inicio:** 08:00 | **Minuto fin:** 11:30 | **Duración:** 3 minutos 30 segundos
- **Presentador:** Ricardo Porras Veli
- **Criterio de rúbrica:** Guion del video de software — Episodio 3: Pruebas con data masiva (500 a 1000 transacciones) / Indicador 9 (4 puntos).

#### Acción en Pantalla
1. Cambiar a una ventana de terminal (PowerShell o bash) con fuente grande (16 pt) y fondo oscuro de alto contraste.
2. Mostrar el comando listo para ejecutar el script desarrollado para la prueba:
   ```bash
   python herramientas_IA/video/carga_transacciones.py --login \
       --gateway https://green-ai-gateway-dev.onrender.com \
       --iteraciones 200 --concurrencia 3 \
       --out docs/evidencias/carga-video.csv
   ```
3. Explicar brevemente la arquitectura del script antes de presionar Enter:
   - Señalar que el script utiliza `--login` para autenticarse interactivamente contra Supabase Auth mediante `getpass` sin imprimir credenciales ni exponer el JWT en pantalla.
   - Explicar la matemática transaccional: 1 transacción inicial de descubrimiento de topología de nodos más 200 iteraciones compuestas cada una por 3 llamadas consecutivas (dataset histórico + predicción ML a 15 min + recomendación bajo políticas), totalizando exactamente **601 transacciones reales** contra el Gateway en Render.
   - Destacar la concurrencia de 3 workers para respetar la memoria de 512 MB del tier gratuito.
4. Presionar Enter, ingresar el correo y contraseña (oculta):
   - Observar cómo se descubren los 50 nodos: `Gateway ... · 50 nodos · 200 iteraciones × 3 = 601 transacciones`.
   - Mostrar el avance periódico de la consola cada 10 iteraciones.
5. Finalizada la ejecución, enfocar la tabla final de resumen en la consola:
   - Señalar las filas: `descubrir_nodos`, `dataset`, `prediccion`, `recomendacion`.
   - Señalar las columnas: cantidad $n$, respuestas HTTP 200, otros códigos, latencia mediana p50 y percentil 95 (p95).
   - Mostrar el diccionario de códigos HTTP resultantes y los estados de recomendación (`eligible_for_review`, etc.).
6. Abrir o mostrar las primeras líneas del archivo generado mediante `head -n 5 docs/evidencias/carga-video.csv` para constatar la persistencia de las métricas.
7. Alternar al navegador en la pestaña de Prometheus (`/-/targets`) y mostrar que los targets de los microservicios se mantuvieron en estado `UP` durante toda la prueba masiva.

#### Diálogo del Presentador
- **Ricardo Porras (08:00 – 11:30):**
  > "Buenas tardes, profesor Jorge Guevara. Mi nombre es Ricardo Porras Veli. En este Episodio 3 abordamos el Indicador 9 de la lista de cotejo, el cual exige demostrar el funcionamiento del software con una carga transaccional masiva de 500 a 1000 transacciones sobre el entorno de calidad en la nube.
  > Para cumplir con este criterio, ejecutamos el script oficial del proyecto `carga_transacciones.py`. Configuramos 200 iteraciones con concurrencia 3 hacia nuestro API Gateway en Render. Cada iteración ejecuta el flujo completo de la aplicación: solicita la ventana histórica al servicio de Data Processing, infiere la demanda futura a 15 minutos en Prediction y evalúa la política de recomendación. Sumando la consulta inicial de descubrimiento de nodos, la prueba genera exactamente 601 transacciones reales protegidas por token JWT.
  > Inicio la ejecución con el parámetro `--login`. Ingreso mis credenciales de operador; como observan, la contraseña no se imprime en pantalla y el token permanece exclusivamente en memoria.
  > Presiono Enter y vemos cómo se inicia el procesamiento concurrente. En la consola observamos el progreso continuo de las peticiones atravesando el Gateway en Go, el cual valida las firmas criptográficas JWKS y distribuye la carga.
  > [Al finalizar la ejecución, mirar la consola y leer directamente de la tabla final]:
  > La prueba ha concluido. Observamos en la tabla de la terminal un total de [leer el número total de transacciones registradas, ej. 601] transacciones ejecutadas.
  > De ellas, [leer el número de respuestas HTTP 200 para predicción y recomendación] respondieron con código exitoso 200.
  > En cuanto a tiempos de respuesta, la latencia mediana p50 se situó en [leer el valor de p50 ms de la tabla] milisegundos, mientras que el percentil 95 alcanzó [leer el valor de p95 ms de la tabla] milisegundos.
  > [Si la tabla muestra peticiones con códigos 503 o 504 por latencia de Render o 422 por datos insuficientes, explicar con honestidad]: como podemos constatar, se registraron [leer número de otros códigos] peticiones con código [mencionar 503/504 o 422]. Esto responde fielmente a las condiciones de latencia internacional y límites de memoria del plan gratuito en Render, evidenciando que el software registra con transparencia cualquier eventualidad sin enmascarar los resultados.
  > Todos los registros han quedado auditados en el archivo CSV `docs/evidencias/carga-video.csv` que muestro en pantalla, y al revisar Prometheus confirmamos que los microservicios se mantuvieron operativos con sus targets en estado UP. Doy paso a Gina Barrera para presentar el Episodio 4."

#### Resultado Esperado y Plan B
- **Resultado esperado:** 601 transacciones ejecutadas, tabla tabulada con desglose por operación, generación del archivo CSV y targets en Prometheus en estado `UP`.
- **Plan B si falla:** Si la conexión a Render se interrumpe al inicio por expiración de sesión, verificar las credenciales, reintentar la ejecución y explicar que la prueba valida la tolerancia a fallos del cliente HTTP.

---

### EPISODIO 4: PRUEBAS CON MÉTRICAS (11:30 – 15:00)

#### Datos de la Escena
- **Minuto inicio:** 11:30 | **Minuto fin:** 15:00 | **Duración:** 3 minutos 30 segundos
- **Presentadores:** Gina Diana Barrera Peña y Jhonny Cristhian Quintana Carhuaricra
- **Criterio de rúbrica:** Guion del video de software — Episodio 4: Pruebas con métricas / Indicador 5.
- **Grabación por partes:** todo se muestra desde el **navegador** (GitHub); no requiere instalar Java, Go, Python ni Docker.

#### Acción en Pantalla
1. **(Gina)** Abrir en GitHub, rama `main`: `docs/academico/06-prueba-de-concepto.md`, sección «3. Resultados» (`model_comparison.csv` no está en GitHub: `results/metrics/*` está en `.gitignore`). Señalar (validación, 15 min, puntos porcentuales de CPU):
   * Persistencia: MAE 4,61 | RMSE 6,39
   * Media móvil: MAE 3,74 | RMSE 5,19
   * XGBoost: MAE 3,46 | RMSE 4,79
   * **Random Forest (modelo desplegado): MAE 3,22 | RMSE 4,59** → 30 % mejor que la persistencia y 14 % mejor que la media móvil. En test: MAE 3,85.
   * Limitación honesta: en picos el error sube a 6,1–8,4 pp.
2. **(Jhonny)** Abrir GitHub → pestaña **Actions** → workflow **CI** → la última ejecución en `main` con check verde. Mostrar la lista de trabajos aprobados (prediction, data-processing, gateway-go, frontend, monitoring, imagenes-docker) y entrar a uno (p. ej., `prediction`) para enseñar la línea final de pytest con las pruebas aprobadas.
3. **(Jhonny)** Abrir `docs/academico/08-pruebas-resultados-discusion.md` en GitHub y mostrar la tabla de suites por servicio; luego `docs/evidencias/smoke-20261106.json` para el smoke 14/14.
4. **(Jhonny)** Abrir `docs/evidencias/prediction-imagen-ligera-20261107.md`: imagen de Prediction 2,85 GB → 510 MB; RAM en reposo 174 → 122–142 MiB (una medición).
5. **(Gina, opcional, dentro de la franja)** Abrir Prometheus en Render (URL del servicio `green-ai-prometheus-dev` + `/targets`): `green-ai-simulator` UP cada 15 s y `green-ai-prediction` cada 1 min.

#### Diálogo del Presentador
- **Gina Barrera (11:30 – 13:15):**
  > "Continuamos con el Episodio 4, enfocado en la sustentación rigurosa de métricas de Machine Learning, calidad de software y eficiencia de infraestructura, respondiendo al Indicador 5 de la rúbrica.
  > En el ámbito de Inteligencia Artificial, nuestro objetivo fue predecir la demanda de cómputo a 15 minutos. En la tabla comparativa proyectada se evidencia el desempeño de los modelos evaluados. Nuestro modelo de producción, basado en Random Forest, obtuvo en validación un Error Absoluto Medio (MAE) de 3,22 puntos porcentuales de CPU y un RMSE de 4,59 puntos, mientras que en el conjunto de prueba independiente alcanzó un MAE de 3,85.
  > Esto representa una mejora cuantificable del 30 % frente al modelo de referencia por persistencia y de un 14 % frente a la media móvil. Con total rigor científico, documentamos también la principal limitación del modelo: en escenarios de cambios abruptos o ráfagas inestables de carga, el error se incrementa a rangos de entre 6,1 y 8,4 puntos porcentuales, comportamiento esperado que nuestro motor de políticas compensa mediante márgenes de seguridad."

- **Jhonny Quintana (13:15 – 15:00):**
  > "En cuanto a la calidad de la ingeniería de software, Green AI no se sustenta en afirmaciones vacías, sino en una cobertura de pruebas automatizadas masiva e integral.
  > Como se ve en GitHub Actions, cada cambio ejecuta automáticamente las pruebas de todos los servicios; la suma de nuestras suites por componente alcanza 433 pruebas automatizadas: 112 pruebas en el microservicio de Monitoring con JUnit; 12 en el Gateway Java; 30 en el Gateway Go verificadas con `-race` para garantizar la ausencia de colisiones de memoria; 121 en Data Processing; 100 en Prediction; 48 en Frontend y 10 en Simulator. Al sumar las 14 pruebas de contrato de nuestra suite de humo de integración de extremo a extremo, alcanzamos un gran total de 447 comprobaciones automatizadas completamente aprobadas.
  > Finalmente, en términos de eficiencia de nube, rediseñamos el contenedor de Prediction: redujimos el tamaño de la imagen Docker de 2,85 gigabytes a solo 510 megabytes, y recortamos el uso de memoria RAM en reposo de 174 a 122 megabytes. Esto permitió que el servicio opere de manera estable en los entornos gratuitos de 512 megabytes de Render, con sus targets en estado UP en Prometheus."

#### Resultado Esperado y Plan B
- **Resultado esperado:** Tablas claras y legibles, desglose de las 433 pruebas por componente más las 14 de smoke (447 totales) sin confusiones matemáticas.
- **Plan B si falla:** si GitHub Actions no carga, mostrar `docs/academico/08-pruebas-resultados-discusion.md` y `docs/evidencias/smoke-20261106.json`. No ejecutar suites en vivo.

---

### EPISODIO 5: PREDICCIONES CON ML DEL PMV1 Y PMV2 (15:00 – 18:30)

#### Datos de la Escena
- **Minuto inicio:** 15:00 | **Minuto fin:** 18:30 | **Duración:** 3 minutos 30 segundos
- **Presentador:** Gina Diana Barrera Peña
- **Criterio de rúbrica:** Guion del video de software — Episodio 5: Pruebas de predicciones con ML del PMV1 y PMV2 / Indicador 10 (3 puntos).

#### Acción en Pantalla
1. Regresar al navegador en `dashboard.html` y situarse en la pestaña «Predicción y recomendación».
2. **Demostración del Primer Caso de Uso de ML: Predicción de demanda futura a 15 minutos:**
   - En los filtros superiores del dashboard, seleccionar el clúster activo en Render y el servidor `HW045`.
   - Mostrar el botón principal: «Estimar CPU del servidor seleccionado».
   - Hacer clic en el botón. Observar el estado «Consultando predicción...».
   - Al recibir la respuesta HTTP 200 desde el Prediction Service a través del Gateway, señalar los datos renderizados:
     * CPU estimada: [Mirar la pantalla y leer el valor porcentual devuelto, ej. 78,4 %].
     * Recurso consultado: `node / HW045`.
     * Instante estimado: Marca de tiempo proyectada a +15 minutos exactos del presente UTC.
     * Horizonte y modelo: `15m / Random Forest (versión ligera de inferencia)`.
     * Procedencia de entrada: `simulated`.
     * Dataset utilizado: Hash o identificador de ventana histórica de 2 horas.
   - Explicar la lógica interna: El servicio Data Processing recolectó 960 muestras históricas (paso de 15 segundos), generó el vector de características (lags, medias móviles, desviaciones estándar) y el estimador infirió la carga esperada.
3. **Demostración del Segundo Caso de Uso de ML: Recomendación prescriptiva con restricciones:**
   - Desplazarse al panel inferior: «Recomendación con restricciones».
   - Hacer clic en el botón «Usar valores de ejemplo» para poblar el formulario con telemetría fresca:
     * Memoria: `65 %`
     * Latencia p95: `120 ms`
     * Errores: `0.2 %`
     * Instante: presionar «Usar ahora» para garantizar marca de tiempo actual (menor a la ventana de expiración de 120 segundos).
     * Procedencia: `Simulada`.
   - Hacer clic en «Evaluar recomendación».
   - Mostrar la respuesta generada por el motor de políticas puras (`src/recommendations/policy.py`):
     * Estado: `eligible_for_review` (Elegible para revisión humana) o el estado que arroje.
     * Acción propuesta: `review_capacity_increase`, `review_capacity_reduction` o `maintain`.
     * Restricción de seguridad inviolable: `executionAllowed: false`.
     * Desglose de verificaciones: Frescura de predicción (`pass`), frescura de telemetría (`pass`), límite de memoria (`pass`), límite de latencia (`pass`) y tasa de error (`pass`).
4. **Demostración del Manejo de Restricciones y Errores (Resiliencia):**
   - Modificar intencionalmente el valor de «Memoria» a `95 %` (superando el umbral de seguridad del 85 %) o seleccionar una fecha desfasada en 1 hora.
   - Clic en «Evaluar recomendación».
   - Observar cómo el estado cambia inmediatamente a `blocked` o `not_evaluable`, y la acción se fija en `none`.

#### Diálogo del Presentador
- **Gina Barrera (15:00 – 18:30):**
  > "En el Episodio 5 presentamos la demostración práctica de los dos casos de uso de Machine Learning integrados en la aplicación web, respondiendo al Indicador 10 de la rúbrica.
  > En primer lugar, abordamos la predicción de demanda futura de CPU a 15 minutos, correspondiente a la historia HU-03. Selecciono en el panel superior el servidor HW045 y presiono 'Estimar CPU'.
  > La aplicación web contacta al Gateway, el cual orquesta la llamada al servicio de Data Processing para consolidar la ventana histórica reciente y la envía al microservicio de Prediction. En pantalla observamos el resultado: [leer en vivo el valor de CPU estimada en pantalla, ej. 78,4 % de utilización] proyectada exactamente para dentro de 15 minutos. Se especifican el modelo empleado, el conjunto de características y, crucialmente, la procedencia declarada 'simulated'. Esta capacidad anticipatoria permite al operador actuar antes de que un servidor entre en saturación térmica o computacional.
  > Pasamos ahora al segundo caso de uso: la generación de recomendaciones operacionales bajo restricciones multidimensionales, según las historias HU-06 y HU-08. Un pronóstico aislado no es suficiente para operar infraestructura crítica; se requiere verificar la salud integral del nodo.
  > Cargamos telemetría con valores de operación normales: 65 % de memoria, 120 milisegundos de latencia y 0.2 % de errores. Al presionar 'Evaluar recomendación', el motor de políticas ejecuta las compuertas de seguridad. Como todas las condiciones se cumplen, el estado resultante es [leer en pantalla el estado devuelto, ej. eligible_for_review] y se sugiere la acción [leer la acción propuesta]. Resalto el campo clave `executionAllowed=false`: por diseño de seguridad, Green AI nunca aplica cambios autónomos sin autorización.
  > Si forzamos una violación de políticas —por ejemplo, elevando la memoria al 95 %—, observen cómo el sistema bloquea inmediatamente la recomendación, arrojando estado `blocked`. Con esto demostramos la madurez de la integración entre Machine Learning y gobernanza de software."

#### Resultado Esperado y Plan B
- **Resultado esperado:** Predicción numérica devuelta en tiempo real con procedencia `estimated`, recomendación evaluada con bloqueo `executionAllowed: false` y comportamiento correcto ante violación de políticas.
- **Plan B si falla:** Si la llamada devuelve HTTP 422 `INSUFFICIENT_DATA` porque el simulador en Render se reinició recientemente y acumula menos de 20 minutos de historial, explicar al profesor en cámara que este es exactamente el comportamiento de protección diseñado: el modelo rehúsa inferir sobre ventanas incompletas para evitar alucinaciones numéricas. Luego, demostrar la recomendación utilizando telemetría de ejemplo.

---

### EPISODIO 6: DEMOSTRACIÓN DEL TABLERO TRELLO Y CONTENIDOS (18:30 – 21:00)

#### Datos de la Escena
- **Minuto inicio:** 18:30 | **Minuto fin:** 21:00 | **Duración:** 2 minutos 30 segundos
- **Presentadores:** Gina Diana Barrera Peña (Scrum Master) y Jhonny Cristhian Quintana Carhuaricra (Product Owner)
- **Criterio de rúbrica:** Guion del video de software — Episodio 6: Demostración del tablero Trello y contenidos / Indicadores 4 y 11.

#### Acción en Pantalla
1. Cambiar a la pestaña del navegador con el tablero oficial de Trello del proyecto Green AI.
2. Mostrar la estructura completa del tablero Kanban / Scrum:
   - Columnas visibles: Product Backlog, Sprint Planning (Sprint 3 / Unidad III), In Progress, Code Review / QA, Done (Completado) e Impediments / Retrospective.
3. Señalar la organización de las Historias de Usuario:
   - Etiquetas por épica y PMV: Etiquetas para PMV1 (HU-01 Visualizar métricas, HU-02 Históricos, HU-15 Registro), etiquetas para PMV2 (HU-03 Predicción, HU-06 Recomendaciones, HU-09 Energía, HU-11 Dashboard) y etiquetas de arquitectura (Hexagonal, Docker Slim, Supabase Auth).
4. Abrir la tarjeta de una Historia de Usuario central, por ejemplo HU-03 («Predicción de demanda a 15 minutos»):
   - Mostrar la descripción formal redactada bajo la estructura estándar: Como [rol], Quiero [funcionalidad], Para [beneficio de negocio].
   - Mostrar los Criterios de Aceptación redactados en sintaxis Gherkin (Given / When / Then).
   - Mostrar la lista de chequeo interna (Checklist) con tareas técnicas: desarrollo de puerto, implementación de adaptador, suite de pruebas unitarias y verificación de no fuga de datos.
   - Mostrar los enlaces cruzados a los Pull Requests cerrados en GitHub y capturas de evidencia adjuntas.
5. Abrir la tarjeta de HU-06 («Recomendación con restricciones») o HU-14 («Control de acceso basado en roles RBAC»):
   - Mostrar la trazabilidad del criterio de aceptación contra la prueba automatizada que lo verifica.

#### Diálogo del Presentador
- **Gina Barrera (18:30 – 19:45):**
  > "En el Episodio 6 sustentamos la gestión ágil de la ingeniería de producto a través de nuestro tablero oficial en Trello, cumpliendo con los lineamientos de la metodología Scrum y el flujo Kanban exigidos en la rúbrica.
  > Como Scrum Master, he facilitado la planificación y seguimiento de los sprints. Nuestro tablero refleja la trazabilidad completa del ciclo de vida del software. En las columnas de la izquierda gestionamos el Product Backlog priorizado por valor de negocio y deuda técnica.
  > Hacia la derecha documentamos el flujo de valor: tareas en curso, revisión de código entre pares y la columna 'Done', la cual solo admite historias que cumplan estrictamente nuestra Definición de Terminado (Definition of Done): código en la rama `test`, pruebas unitarias aprobadas, documentación actualizada y despliegue exitoso en la nube."

- **Jhonny Quintana (19:45 – 21:00):**
  > "Complementando desde la perspectiva de producto, abro la tarjeta de la historia HU-03, correspondiente a la predicción de demanda.
  > Como se observa, cada historia cuenta con una definición formal del usuario y criterios de aceptación rigurosos en formato Given/When/Then. Por ejemplo: 'Dado un conjunto de telemetría reciente con ventana válida de 2 horas, cuando el operador solicita la estimación a 15 minutos, entonces el sistema retorna un valor con procedencia declarada estimated y código 200'.
  > Cada criterio está directamente vinculado a una prueba de contrato automatizada en nuestro repositorio de GitHub. De igual modo, gestionamos historias de infraestructura como la reducción de las imágenes Docker y la implementación de roles en Supabase. Este nivel de trazabilidad asegura que ningún entregable del software carezca de sustento y validación funcional."

#### Resultado Esperado y Plan B
- **Resultado esperado:** Tablero Trello fluido, tarjetas bien documentadas con criterios Given/When/Then legibles y visualización de checklists completos.
- **Plan B si falla:** Si Trello experimenta demoras de carga de red, mostrar la matriz completa de historias de usuario y criterios de aceptación documentada en la Sección 2 de `docs/academico/08-pruebas-resultados-discusion.md`.

---

### EPISODIO 7: CUMPLIMIENTO DE ARQUITECTURA HEXAGONAL Y PROCEDIMIENTOS ALMACENADOS (21:00 – 24:00)

#### Datos de la Escena
- **Minuto inicio:** 21:00 | **Minuto fin:** 24:00 | **Duración:** 3 minutos 00 segundos
- **Presentador:** Ricardo Porras Veli
- **Criterio de rúbrica:** Guion del video de software — Episodio 7: Cumplimiento de arquitectura hexagonal con código en GitHub y procedimientos almacenados / Indicador 11 (3 puntos).

#### Acción en Pantalla
1. Cambiar a la pestaña del navegador con el repositorio en GitHub: `https://github.com/woshtsu/green-ai-workspace-cld` en la rama `test`.
2. **Demostración de Arquitectura Hexagonal en el Servicio 1: `software/data-processing`:**
   - Navegar a `software/data-processing`:
     * Mostrar la carpeta `domain/`: abrir `domain/ports/historical_logs_source.py`. Resaltar que es una clase abstracta pura (`HistoricalLogsSource`) sin dependencias de base de datos ni frameworks externos.
     * Mostrar la carpeta `application/`: abrir `application/use_cases/read_historical_logs.py`. Mostrar cómo el caso de uso orquesta la lógica de negocio interactuando únicamente a través del puerto.
     * Mostrar la carpeta `infrastructure/adapters/`: mostrar `infrastructure/historical_sources.py` (patrón Factory) y los dos adaptadores concretos: `sqlite_historical_logs_adapter.py` (para desarrollo local) y `supabase_historical_logs_adapter.py` (para producción en la nube).
     * Destacar: El dominio jamás importa infraestructura; la infraestructura implementa los puertos del dominio (inversión de dependencias).
3. **Demostración de Arquitectura Hexagonal en el Servicio 2: `software/monitoring` (Java 21):**
   - Navegar a `software/monitoring/src/main/java/pe/edu/continental/greenai/monitoring`:
     * Carpeta `domain/`: entidades `MetricDefinition` y `MetricData`.
     * Carpeta `application/port/in/`: interfaz de caso de uso `QueryMetrics.java`.
     * Carpeta `application/port/out/`: puerto de salida `MetricsSource.java`.
     * Carpeta `adapter/in/web/`: controlador REST `MetricsController.java` (adaptador primario).
     * Carpeta `adapter/out/prometheus/`: cliente HTTP de Prometheus (adaptador secundario).
     * Carpeta `adapter/out/fixture/`: adaptador de fixture para pruebas desacopladas de red.
4. **Demostración de Procedimientos Almacenados y Triggers en Supabase:**
   - Abrir el archivo `software/frontend/supabase-auth-setup.sql` en GitHub:
     * Líneas 45 a 66: Mostrar la función PL/pgSQL `public.handle_new_auth_user()` con directiva `security definer`. Explicar que se activa automáticamente mediante el trigger `on_auth_user_created_green_ai` tras cada inserción en `auth.users`, aprovisionando el perfil y asignando el rol predeterminado `OPERATOR`.
     * Líneas 79 a 100: Mostrar la función almacenada de Auth Hook `public.custom_access_token_hook(event jsonb)` que extrae el rol de la tabla `user_roles` e inyecta dinámicamente el claim `{user_role}` en el token JWT que el Gateway valida vía JWKS.
5. **Demostración de Integración Continua (CI/CD):**
   - Navegar a la pestaña «Actions» de GitHub:
     * Mostrar el pipeline `.github/workflows/ci.yml`: ejecución automatizada de las suites de pruebas ante cada push a la rama `test`.
     * Mostrar el pipeline `.github/workflows/pages.yml`: despliegue continuo del frontend estático hacia GitHub Pages.

#### Diálogo del Presentador
- **Ricardo Porras (21:00 – 24:00):**
  > "En el Episodio 7 auditamos el cumplimiento estricto del Indicador 11 de la rúbrica: arquitectura hexagonal por microservicio, uso de procedimientos almacenados en base de datos e integración continua en GitHub.
  > Como se observa en nuestro repositorio en la rama `test`, la arquitectura hexagonal o de puertos y adaptadores es una realidad implementada en el código, no un diagrama teórico.
  > En el servicio `data-processing`, en Python, exploramos la capa `domain/ports`: aquí reside la abstracción pura `HistoricalLogsSource`. La capa de aplicación utiliza este puerto sin conocer cómo se almacenan los datos. En `infrastructure/adapters` encontramos los adaptadores reales: uno para SQLite en desarrollo y otro para Supabase mediante API REST en la nube. Una factoría selecciona el adaptador en tiempo de arranque según las variables de entorno, sin alterar una sola línea de lógica de negocio.
  > Lo mismo se replica en el servicio de `monitoring` desarrollado en Java 21 con Spring Boot: en `application/port/in` definimos la interfaz `QueryMetrics`, mientras que en `adapter/out` desacoplamos la recolección de métricas entre el cliente real de Prometheus y un adaptador de fixture para aislamiento de pruebas.
  > Respecto al uso de procedimientos almacenados, mostramos en el archivo `supabase-auth-setup.sql` la función PL/pgSQL `handle_new_auth_user()`. Esta función opera como un trigger transaccional con privilegios `security definer`: cada vez que un usuario se registra en Supabase Auth, el trigger inicializa de forma atómica su perfil y le asigna el rol `OPERATOR` en la tabla `user_roles` protegida por políticas RLS. Asimismo, la función `custom_access_token_hook` intercepta la emisión de tokens para incrustar el rol en el JWT.
  > Finalmente, en GitHub Actions evidenciamos nuestros flujos de CI/CD: cada cambio enviado a la rama `test` dispara la compilación y validación de las suites de prueba de todos los componentes antes de permitir cualquier despliegue. Doy pase a mis compañeros para el cierre."

#### Resultado Esperado y Plan B
- **Resultado esperado:** Navegación fluida por el árbol de archivos en GitHub, explicación precisa de puertos y adaptadores, visualización del código SQL y flujos de GitHub Actions en verde.
- **Plan B si falla:** Si GitHub experimenta lentitud de carga, abrir los mismos archivos directamente en el entorno de desarrollo local (VS Code / terminal) que mantiene copia exacta sincronizada con la rama `test`.

---

### CIERRE, CRÉDITOS Y MATRIZ DE RÚBRICA (24:00 – 25:00)

#### Datos de la Escena
- **Minuto inicio:** 24:00 | **Minuto fin:** 25:00 | **Duración:** 1 minuto 00 segundos
- **Presentadores:** Los 4 integrantes (Jhonny Quintana, Gina Barrera, Leonid Huamán, Ricardo Porras)
- **Cámaras:** cada integrante graba su frase en un clip propio (clip 09); en la edición se muestran los 4 rostros en mosaico 2×2 durante los últimos 10 s.
- **Criterio de rúbrica:** Guion del video de software — Cierre, participación de todos los integrantes con cámara y duración reglamentaria (25 minutos).

#### Acción en Pantalla
1. Mostrar la diapositiva final o matriz resumen de cumplimiento de la rúbrica:
   - Tabla que mapea los 11 indicadores de la guía de Semana 12 contra las evidencias demostradas en el video.
   - Enlace y código QR de acceso al repositorio público en GitHub.
   - Enlace y código QR de acceso a la aplicación desplegada en GitHub Pages.
2. Mosaico 2×2 con los 4 integrantes despidiéndose a cámara (montado en la edición a partir de los clips 09).

#### Diálogo del Presentador
- **Jhonny Quintana (24:00 – 24:20):**
  > "Para concluir, profesor Guevara, hemos demostrado el cumplimiento integral de los requerimientos funcionales, arquitecturales y experimentales de la Unidad III para el PMV1 y PMV2. En pantalla dejamos la matriz de trazabilidad con los minutos exactos de cada demostración."

- **Gina Barrera (24:20 – 24:35):**
  > "Validamos nuestros modelos de Machine Learning con métricas reales de MAE y RMSE, manteniendo siempre una postura de absoluta honestidad académica frente a los datos simulados de telemetría."

- **Leonid Huamán (24:35 – 24:45):**
  > "El frontend y la observabilidad operan de forma fluida sobre la nube en GitHub Pages y Render, brindando una experiencia moderna y resiliente."

- **Ricardo Porras (24:45 – 25:00):**
  > "Y el backend sostiene una arquitectura hexagonal estricta con alta capacidad transaccional y seguridad perimetral. Agradecemos su atención y quedamos a su disposición. Muchas gracias."

---

## 6. DETALLE DE MÉTRICAS Y REGISTRO DE EVIDENCIAS (EPISODIO 4)

Para respaldar las explicaciones del Episodio 4, se consolidan aquí los valores numéricos exactos verificados en el monorepo que deben ser expuestos con absoluta precisión:

### 6.1 Métricas de Modelos de Machine Learning (Inferencia a 15 Minutos)

| Modelo Evaluado | MAE Validación (pp CPU) | RMSE Validación (pp CPU) | MAE Test (pp CPU) | Ganancia vs Persistencia | Estado en el Proyecto |
|---|---|---|---|---|---|
| Persistencia (Baseline Heurístico) | 4,61 | 6,39 | — | 0,0 % (Referencia) | Descartado (Línea base) |
| Media Móvil (Ventana deslizante) | 3,74 | 5,19 | — | + 18,9 % | Descartado (Referencia) |
| Random Forest (Pipeline ligero) | **3,22** | **4,59** | **3,85** | **+ 30,2 %** | **Seleccionado en Producción** |
| XGBoost (Evaluación experimental) | 3,46 | 4,79 | — | + 25,1 % | Descartado (peor MAE que RF) |

*Fuente:* `software/prediction/results/metrics/model_comparison.csv` (filas `15m`, `validation`) y `docs/academico/06-prueba-de-concepto.md` (test del modelo seleccionado, n = 129). Revisado el 09/11/2026: la versión anterior de esta tabla tenía cifras que no estaban en el CSV.

*Nota técnica de limitación:* Durante regímenes de carga dinámica no estacionaria (picos de utilización repentinos simulados), el error puntual MAE asciende a rangos de entre 6,1 y 8,4 puntos porcentuales de CPU. Este margen es asumido y mitigado por los umbrales de seguridad de la política de recomendación.

### 6.2 Inventario y Suma Exacta de Pruebas Automatizadas

| Componente del Sistema | Tecnología de Prueba | Casos Aprobados | Foco de Verificación |
|---|---|---|---|
| Monitoring Service | JUnit 5 / Spring Boot Test | 112 | Contratos REST, agregación temporal y puente a Prometheus. |
| API Gateway (Java) | JUnit 5 / Spring Cloud | 12 | Validación JWT, CORS y filtros perimetrales. |
| API Gateway (Go) | `go test -race` (×5 corridas) | 30 | Concurrencia sin memory leaks, validación criptográfica JWKS. |
| Data Processing Service | pytest / FastAPI TestClient | 121 | Contratos SQLite y PostgreSQL, agregación y transformación. |
| Prediction Service | pytest / scikit-learn | 100 | Integridad de artefactos, no-fuga de datos (leakage) e inferencia. |
| Frontend Web | `node --test` (CommonJS) | 48 | Lógica de transformación UI, cálculo de energía y manejo de errores. |
| Simulator Engine | unittest en Docker | 10 | Generación estocástica, ciclo de vida e inventario de hardware. |
| **SUMA POR COMPONENTES** | **Pruebas unitarias y de integración** | **433 pruebas** | **Suma exacta: 112 + 12 + 30 + 121 + 100 + 48 + 10.** |
| Suite de Humo Extremo a Extremo | Python (`smoke.py`) | 14 | Verificación de contratos HTTP reales entre microservicios. |
| **TOTAL ACUMULADO** | **Multiplataforma** | **447 comprobaciones** | **433 pruebas por componente + 14 de suite de humo.** |

### 6.3 Métricas de Recursos y Optimización de Infraestructura

| Parámetro de Rendimiento | Medición Previa (Semana 10) | Medición Optimizada (Semana 12) | Factor de Mejora |
|---|---|---|---|
| Tamaño imagen Docker Prediction | 2,85 GB (con stack de entrenamiento) | **510 MB** (imagen slim de inferencia) | **Reducción del 82,1 % de peso** |
| Consumo de RAM en reposo (Prediction) | 174 MiB | **122 MiB** (con `PYTHONOPTIMIZE=2`) | **Ahorro del 29,8 % de memoria** |

*Retirado el 09/11/2026:* las filas de arranque en frío (140 → 45 s) e inferencia (85 → 28 ms) no tenían medición en `docs/evidencias/`; no mencionarlas en el video. Las latencias de la PoC (sección 3 de `docs/academico/06-prueba-de-concepto.md`) son por lote y de una sola ejecución; no presentarlas como latencia por petición.

---

## 7. AUDITORÍA DE ARQUITECTURA HEXAGONAL Y PROCEDIMIENTOS ALMACENADOS (EPISODIO 7)

### 7.1 Desglose de Carpetas Hexagonales en `software/data-processing`

- **Capa de Dominio (`software/data-processing/domain/`):**
  * `ports/historical_logs_source.py`: Define la interfaz abstracta `HistoricalLogsSource` con el método contractual `read_page(hardware_id, start, end, limit, after)`. No contiene referencias a bases de datos ni bibliotecas externas.
  * `errors.py`: Definición de excepciones semánticas de negocio (`ServiceError`, `InvalidQuery`, `SourceNotConfigured`).
  * `monitoring_contract.py`: Tipos y restricciones de métricas admitidas.
- **Capa de Aplicación (`software/data-processing/application/`):**
  * `use_cases/read_historical_logs.py`: Implementa el caso de uso `ReadHistoricalLogsUseCase`, consumiendo únicamente el puerto `HistoricalLogsSource`.
  * `use_cases/prepare_prediction_dataset.py`: Limpieza y formateo de ventanas históricas.
  * `use_cases/process_metrics.py`: Procesamiento y validación de procedencia.
  * `use_cases/historical_report.py`: Agregación de estadísticas para reportes.
- **Capa de Adaptadores e Infraestructura (`software/data-processing/infrastructure/`):**
  * `historical_sources.py`: Fábrica que instancia el adaptador requerido según la variable de entorno `HISTORICAL_SOURCE`.
  * `adapters/input/sqlite_historical_logs_adapter.py`: Adaptador concreto que lee bases de datos SQLite locales para desarrollo sin dependencias de red.
  * `adapters/input/supabase_historical_logs_adapter.py`: Adaptador concreto que consume la API REST de Supabase en entornos de producción.
  * `adapters/input/api/routes.py`: Adaptador de entrada que expone los endpoints HTTP a través de FastAPI.

### 7.2 Desglose de Carpetas Hexagonales en `software/monitoring` (Java)

- **Capa de Dominio:** `pe.edu.continental.greenai.monitoring.domain.MetricDefinition` y `MetricData`.
- **Puertos de Aplicación:**
  * Puerto de entrada: `pe.edu.continental.greenai.monitoring.application.port.in.QueryMetrics`.
  * Puerto de salida: `pe.edu.continental.greenai.monitoring.application.port.out.MetricsSource`.
- **Adaptadores:**
  * Adaptador primario (Web): `pe.edu.continental.greenai.monitoring.adapter.in.web.MetricsController`.
  * Adaptador secundario (Prometheus): `pe.edu.continental.greenai.monitoring.adapter.out.prometheus.PrometheusMetricsSource`.
  * Adaptador de contingencia (Fixture): `pe.edu.continental.greenai.monitoring.adapter.out.fixture.FixtureMetricsSource`.

### 7.3 Procedimientos Almacenados y Triggers en Supabase SQL

El archivo versionado en GitHub `software/frontend/supabase-auth-setup.sql` contiene la evidencia verificable del uso de lógica procedimental en el motor de base de datos relacional PostgreSQL de Supabase:

```sql
-- Procedimiento almacenado (Trigger Function) ejecutado tras el registro
CREATE OR REPLACE FUNCTION public.handle_new_auth_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = ''
AS $$
BEGIN
  -- 1. Aprovisionamiento automático de perfil de usuario
  INSERT INTO public.user_profiles (id, full_name)
  VALUES (new.id, coalesce(new.raw_user_meta_data ->> 'full_name', ''))
  ON CONFLICT (id) DO NOTHING;

  -- 2. Asignación obligatoria del rol por defecto OPERATOR
  INSERT INTO public.user_roles (user_id, role)
  VALUES (new.id, 'OPERATOR')
  ON CONFLICT (user_id) DO NOTHING;

  RETURN new;
END;
$$;

-- Trigger asociado sobre la tabla auth.users
DROP TRIGGER IF EXISTS on_auth_user_created_green_ai ON auth.users;
CREATE TRIGGER on_auth_user_created_green_ai
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE PROCEDURE public.handle_new_auth_user();

-- Procedimiento almacenado de Auth Hook para enriquecimiento de JWT
CREATE OR REPLACE FUNCTION public.custom_access_token_hook(event jsonb)
RETURNS jsonb
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
  claims jsonb;
  assigned_role public.app_role;
BEGIN
  -- Consulta el rol asignado en la base de datos
  SELECT role INTO assigned_role
  FROM public.user_roles
  WHERE user_id = (event ->> 'user_id')::uuid;

  -- Inyecta el claim {user_role} en la carga útil del JWT
  claims := event -> 'claims';
  claims := jsonb_set(
    claims,
    '{user_role}',
    to_jsonb(coalesce(assigned_role, 'OPERATOR'::public.app_role))
  );
  RETURN jsonb_build_object('claims', claims);
END;
$$;
```

---

## 8. MATRIZ DE TRAZABILIDAD Y VERIFICACIÓN DE RÚBRICA

Esta tabla permite al docente y evaluadores contrastar de manera directa cada indicador oficial de la guía con el minuto exacto del video donde se demuestra:

| Indicador de la Rúbrica (Semana 12) | Puntaje | Episodio del Video | Minuto en Video | Evidencia Demostrada en Pantalla |
|---|---|---|---|---|
| **Indicador 9:** Demostración con datos (500 a 1000 transacciones) del PMV1 y PMV2 sobre entorno de calidad. | 4 pts | Episodio 1, 2 y 3 | 01:30 – 11:30 | Operación del frontend en GitHub Pages; ejecución en vivo de 601 transacciones con `carga_transacciones.py` contra Render, lectura en vivo de percentiles p50/p95 y auditoría en CSV. |
| **Indicador 10:** Demostración con datos de integración con ML (1.er y 2.º caso de uso predictivo en calidad). | 3 pts | Episodio 5 | 15:00 – 18:30 | Caso 1: Estimación de demanda a 15 min con Random Forest sobre ventana histórica. Caso 2: Recomendación bajo políticas con `executionAllowed=false`. |
| **Indicador 11:** Demostración de arquitectura hexagonal, procedimientos almacenados en GitHub y Kanban. | 3 pts | Episodio 6 y 7 | 18:30 – 24:00 | Tablero Trello completo; inspección en GitHub de capas domain/application/adapters de 2 servicios; triggers PL/pgSQL y CI/CD. |
| **Guion de software:** Carátula con nombre del proyecto e integrantes completos. | Requisito | Introducción | 00:00 – 01:30 | Carátula formal con logo UC, nombre de asignatura, docente, proyecto y 4 integrantes con sus roles. |
| **Guion de software:** Participación del 100 % de integrantes con cámara y nombre completo. | Requisito | Todo el video | 00:00 – 25:00 | Cámara web activa de los 4 estudiantes a lo largo de toda la exposición; rótulos identificadores en cada transición. |
| **Guion de software:** Duración estimada del video entre 20 y 30 minutos. | Requisito | Video global | 25:00 exactos | Cronometraje ajustado a 25 minutos exactos, respetando los límites de la guía docente. |

---

## 9. CONSEJOS DE EDICIÓN, POSTPRODUCCIÓN Y PUBLICACIÓN

### 9.1 Pautas de Grabación y Edición
1. **Grabación de una sola toma guiada:**
   - Utilizar este documento en una segunda pantalla como teleprompter técnico.
   - Si un presentador tropieza con una palabra, hacer una pausa en silencio de 3 segundos y retomar desde el inicio de la frase. Eso facilita realizar cortes de salto (jump-cuts) limpios en edición.
2. **Software de edición recomendado:**
   - DaVinci Resolve (gratuito y profesional), CapCut Desktop o Clipchamp (integrado en Windows 11).
3. **Tratamiento de tiempos muertos de red:**
   - Si la primera petición a Render toma 20 segundos por el despertar de una instancia inactiva, recortar el tiempo muerto en edición o acelerar el fragmento a velocidad 2× con un rótulo explicativo: «Conexión inicial a Render (acelerado 2×)».
4. **Rotulación y elementos gráficos:**
   - Insertar un rótulo inferior (Lower Third) durante los primeros 7 segundos de la intervención de cada miembro:
     * `Jhonny Cristhian Quintana Carhuaricra | Product Owner`
     * `Gina Diana Barrera Peña | Scrum Master`
     * `Leonid Kisley Orlando Huamán Collazos | Infraestructura y Frontend`
     * `Ricardo Porras Veli | Backend y Arquitectura`
   - Insertar una pequeña etiqueta en la esquina superior izquierda con el nombre del episodio activo: ej. `Episodio 3: Pruebas con data masiva (601 transacciones)`.

### 9.2 Parámetros de Renderizado y Exportación
- **Formato contenedor:** MP4
- **Códec de video:** H.264
- **Resolución:** 1920×1080 (Full HD)
- **Relación de aspecto:** 16:9
- **Tasa de fotogramas:** Constante a 30 fps (o 60 fps si se capturó a esa tasa)
- **Tasa de bits (Bitrate):** 10 Mbps a 12 Mbps (VBR de 2 pases recomendado)
- **Códec de audio:** AAC estéreo, 48 kHz, 320 Kbps

### 9.3 Publicación en YouTube y Generación de Código QR
1. **Subida a YouTube:**
   - Subir el video a la cuenta de uno de los integrantes.
   - Título del video: `Green AI — Demostración de Software PMV1 y PMV2 | Unidad III — Taller de Proyectos 1`
   - Visibilidad obligatoria: **No listado (Unlisted)**. De este modo, el video es privado para el público general pero plenamente accesible para el docente y cualquier persona que cuente con el enlace directo.
   - En la descripción de YouTube:
     * Copiar la tabla de marcas de tiempo (Timestamps) para navegación automática:
       ```text
       00:00 Carátula e Introducción Institucional
       01:30 Episodio 1: Pruebas funcionales del PMV1
       04:30 Episodio 2: Pruebas funcionales del PMV2
       08:00 Episodio 3: Pruebas con data masiva (601 transacciones)
       11:30 Episodio 4: Pruebas con métricas (ML, pruebas y Docker)
       15:00 Episodio 5: Predicciones con ML del PMV1 y PMV2
       18:30 Episodio 6: Tablero Trello y contenidos ágiles
       21:00 Episodio 7: Arquitectura hexagonal y procedimientos SQL
       24:00 Cierre y conclusiones
       ```
     * Incluir los enlaces al repositorio en GitHub y a la aplicación en GitHub Pages.
2. **Generación del Código QR:**
   - Tomar la URL final del video en YouTube (ej. `https://youtu.be/xxxxxxxxxxx`).
   - Utilizar un generador de QR vectorial o PNG de alta resolución (mínimo 500×500 píxeles, nivel de corrección de error M o Q).
   - Insertar el código QR generado en:
     * La carátula del informe académico escrito (`informe-unidad-III.md` o formato entregable).
     * La diapositiva final de cierre del video para permitir que el evaluador acceda al recurso desde cualquier dispositivo móvil.
