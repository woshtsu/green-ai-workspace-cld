# GUION TÉCNICO Y DE PRODUCCIÓN DEL VIDEO DE SOFTWARE — UNIDAD III
## Proyecto Green AI: Optimización Energética y Predictiva en Centros de Datos

- **Asignatura:** Taller de Proyectos 1 — ISI (Universidad Continental)
- **Docente:** Jorge A. Guevara Jiménez
- **Duración del video montado:** 24:26 (rango reglamentario de 20 a 30 minutos); pantalla grabada el 10/11/2026
- **Entorno de grabación:** Nube pública en producción/desarrollo (GitHub Pages + Render + Supabase; estrictamente sin localhost)
- **Resolución de pantalla:** Full HD (1920×1080), 30 o 60 fotogramas por segundo
- **Participación:** los 4 integrantes ponen voz y cámara encima del video, con su nombre completo en un rótulo (sección 0.5)


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

## 0.5 VIDEO YA GRABADO: CADA INTEGRANTE PONE VOZ Y CÁMARA ENCIMA (actualizado 10/11/2026)

La pantalla de todo el video **ya está grabada y montada**: `exportados/video/green-ai-unidad-III.mp4` (24:26, 1920×1080, sin audio; en el Drive del grupo, no en GitHub). Contiene la carátula, los 7 episodios y el cierre. **Nadie vuelve a operar la app.** Cada integrante:
1. Reproduce el video en su PC desde el minuto de su tramo (tabla de abajo) y graba con OBS **solo cámara y micrófono** (cámara de 400×240 px; la esquina inferior derecha del video quedó libre para ella) leyendo su diálogo de la sección 5 al ritmo de la pantalla.
2. Entrega `voz-NN-apellido.mp4` (NN = minuto de inicio, p. ej. `voz-0459-porras.mp4`) a Jhonny, que lo coloca sobre el video en el minuto indicado y añade el rótulo con el nombre completo.
3. Las cifras ya salen en pantalla: se leen del video (en la sección 5 se anotan las que se ven); no se inventa ninguna.

### Quién habla en cada tramo (minutos del video montado)
| Minuto | Tramo | Habla | Rol |
|---|---|---|---|
| 00:00–00:13 | Carátula: proyecto, docente, entorno | Jhonny | Product Owner |
| 00:13–00:29 | Carátula: integrantes (cada uno dice su nombre completo y rol, ~4 s) | Los 4 | — |
| 00:29–00:44 | Carátula: los 7 episodios | Gina | Scrum Master |
| 00:44–02:33 | Ep. 1 PMV1 | Leonid | Infraestructura y Frontend |
| 02:33–03:55 | Ep. 2 Racks y Red de flujos | Leonid | Infraestructura y Frontend |
| 03:55–04:57 | Ep. 2 Históricos, CSV, experimento y energía | Jhonny | Product Owner |
| 04:57–12:55 | Ep. 3 Data masiva (601 transacciones) | Ricardo | Backend y Arquitectura |
| 12:55–13:30 | Ep. 4 Métricas de ML | Gina | Scrum Master (datos y ML) |
| 13:30–15:44 | Ep. 4 CI, pruebas, imagen ligera y Prometheus | Jhonny | Product Owner |
| 15:44–17:33 | Ep. 5 Predicción y recomendación | Gina | Scrum Master (datos y ML) |
| 17:33–18:16 | Ep. 6 Tablero Trello | Gina | Scrum Master |
| 18:16–19:44 | Ep. 6 Tarjetas HU-03 y HU-06 | Jhonny | Product Owner |
| 19:44–23:39 | Ep. 7 Hexagonal, SQL y CI/CD | Ricardo | Backend y Arquitectura |
| 23:39–23:55 | Cierre: indicadores | Jhonny | Product Owner |
| 23:55–24:09 | Cierre: enlaces | Gina y Leonid | — |
| 24:09–24:26 | Cierre: despedida (mosaico 2×2 con los 4 rostros) | Ricardo y los 4 | — |

Carga por persona: Ricardo ≈ 11:55; Jhonny ≈ 5:05; Gina ≈ 3:45; Leonid ≈ 3:11 (+ carátula y cierre para todos).

### Ajustes para la voz
- Audio 48 kHz, lugar silencioso, prueba de 10 s; 2 s de silencio al inicio y al final.
- El ritmo cómodo es ~2,3 palabras por segundo: los diálogos de la sección 5 ya están medidos para su tramo. Si sobra tiempo, callar mientras la pantalla avanza; no rellenar con cifras no vistas.
- Si en pantalla se ve un aviso o error, se nombra tal cual (no se cortó nada del video).

### Regrabar un episodio (solo si hace falta)
Ver `docs/CONTINUAR-EN-NUEVO-CHAT.md` § «Video Unidad III»: `mantener_despierto.py` ≥ 25 min antes, ensayo con `grabar_episodios.py --ensayo N`, grabación con `--ritmo 1.6 N` y montaje con `portada_cierre.py cierre` + `unir` (recalcula los minutos del cierre). Las secciones 1 y 3 de este guion solo aplican si se vuelve a grabar la pantalla.

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
| 00:00 – 00:44 | Carátula e integrantes | Guion — Carátula | Jhonny, los 4, Gina | Proyecto, docente, integrantes con rol y los 7 episodios. |
| 00:44 – 02:33 | Episodio 1: Pruebas funcionales PMV1 | Guion — Ep. 1 / Ind. 9 | Leonid | Login Supabase, KPI de 50 servidores, gráfico, comparación y tabla. |
| 02:33 – 04:57 | Episodio 2: Pruebas funcionales PMV2 | Guion — Ep. 2 / Ind. 9 | Leonid → Jhonny (03:55) | Racks, Red de flujos, históricos de Supabase con CSV, experimento y energía. |
| 04:57 – 12:55 | Episodio 3: Data masiva | Guion — Ep. 3 / Ind. 9 | Ricardo | 601 transacciones reales contra Render, tabla p50/p95 y Prometheus. |
| 12:55 – 15:44 | Episodio 4: Métricas | Guion — Ep. 4 / Ind. 5 | Gina → Jhonny (13:30) | PoC (RF vs baselines), CI, suites, smoke, imagen ligera, Prometheus. |
| 15:44 – 17:33 | Episodio 5: Predicciones con ML | Guion — Ep. 5 / Ind. 10 | Gina | Predicción a 15 min (HU-03) y recomendación con restricciones (HU-06). |
| 17:33 – 19:44 | Episodio 6: Trello | Guion — Ep. 6 / Ind. 4, 11 | Gina → Jhonny (18:16) | Columnas Scrum/Kanban y tarjetas HU-03 y HU-06. |
| 19:44 – 23:39 | Episodio 7: Hexagonal y SQL | Guion — Ep. 7 / Ind. 11 | Ricardo | Puertos y adaptadores en Python y Java, funciones PL/pgSQL y CI/CD. |
| 23:39 – 24:26 | Cierre | Cierre y formalidad | Los 4 | Indicadores con su minuto, QR y despedida. |

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

## 5. GUION DE LOCUCIÓN SINCRONIZADO CON EL VIDEO (24:26)

Cada bloque indica el minuto **del video montado** en que empieza la frase y lo que se ve en ese momento. Los textos están medidos para su tramo (~2,3 palabras/s). Las cifras entre «» son las que **se ven en el video grabado el 10/11/2026**; si se regraba un episodio, se leen las nuevas.

---

### CARÁTULA (00:00 – 00:44)

| Minuto | En pantalla | Habla | Diálogo |
|---|---|---|---|
| 00:00 | Título, docente, entorno en la nube | **Jhonny** | «Buenas tardes, profesor Jorge Guevara. Presentamos Green AI, nuestro sistema de monitoreo y predicción de demanda computacional, demostrado en la nube sobre GitHub Pages, Render y Supabase.» |
| 00:13 | Tarjetas de los 4 integrantes | **Jhonny** | «Soy Jhonny Cristhian Quintana Carhuaricra, Product Owner.» |
| 00:17 | | **Gina** | «Soy Gina Diana Barrera Peña, Scrum Master y responsable de datos y modelos.» |
| 00:21 | | **Leonid** | «Soy Leonid Kisley Orlando Huamán Collazos, de infraestructura y frontend.» |
| 00:25 | | **Ricardo** | «Soy Ricardo Porras Veli, de backend y arquitectura.» |
| 00:29 | Lista de los 7 episodios | **Gina** | «En siete episodios mostraremos las pruebas funcionales del PMV1 y del PMV2, una carga de seiscientas una transacciones, las métricas, los dos casos de uso de Machine Learning, nuestro tablero Trello y la arquitectura hexagonal en GitHub.» |

---

### EPISODIO 1: PRUEBAS FUNCIONALES DEL PMV1 (00:44 – 02:33) · Leonid

| Minuto | En pantalla | Diálogo |
|---|---|---|
| 00:44 | Formulario de inicio de sesión | «Episodio uno, en la URL pública de producción. El acceso usa Supabase Auth y la contraseña nunca se muestra; al entrar, el Gateway valida el token JWT.» |
| 00:56 | Dashboard con el nombre y el rol | «Arriba se ve el usuario y su rol, «OPERATOR». Consultamos la CPU de todos los servidores en los últimos quince minutos.» |
| 01:06 | KPI resaltados uno a uno | «La media del conjunto es «85 %»; el servidor más cargado llega a «89,4 %» y el menos cargado a «80,6 %».» |
| 01:21 | Servidores en respuesta y procedencia | «Responden «50» servidores, y la procedencia se declara como «Simulado»: la telemetría viene del simulador, y así lo decimos.» |
| 01:30 | Gráfico de evolución | «El gráfico muestra la media en el tiempo con bandas de máximo y mínimo.» |
| 01:40 | Comparación de 5 servidores | «Con un clic comparamos los cinco servidores más cargados, cada uno con su propia serie.» |
| 01:53 | Tabla de detalle | «En «Detalle por servidor» está la tabla paginada con los cincuenta servidores, su valor, procedencia, calidad e instante.» |
| 02:01 | Búsqueda de HW045 | «Podemos buscar un servidor, por ejemplo HW045,» |
| 02:11 | Orden por «Valor» | «y ordenar por valor. Así queda demostrado el monitoreo del PMV1, historias HU-01 y HU-02, en la nube.» |

---

### EPISODIO 2: PRUEBAS FUNCIONALES DEL PMV2 (02:33 – 04:57)

| Minuto | En pantalla | Habla | Diálogo |
|---|---|---|---|
| 02:34 | Racks con calor, KPI | **Leonid** | «Episodio dos, el PMV2. La vista Racks distribuye los cincuenta servidores en cinco racks. Arriba: «50» nodos sobre el ochenta por ciento y una CPU media de «85,1 %».» |
| 02:48 | Cuadrícula de racks | **Leonid** | «Cada celda es un servidor: verde bajo cuarenta por ciento, amarillo de cuarenta a ochenta, rojo por encima de ochenta.» |
| 02:58 | Todas las celdas en rojo | **Leonid** | «¿Por qué todo está rojo? El simulador en la nube corre un escenario de carga alta: los cincuenta servidores superan el ochenta por ciento.» |
| 03:11 | Botón «Actualizar» | **Leonid** | «Es telemetría simulada, justo donde Green AI propone mover carga o revisar capacidad.» |
| 03:18 | Red de flujos | **Leonid** | «La Red de flujos propone cómo mover carga de los servidores saturados a los que tienen holgura. Es una propuesta ilustrativa: el sistema no ejecuta ninguna acción, executionAllowed es falso.» |
| 03:31 | Sensibilidad 0,8 y 15 flujos | **Leonid** | «Si cambiamos la sensibilidad y el máximo de flujos, la propuesta se recalcula al instante: ahora «15» flujos. Le paso la palabra a Jhonny.» |
| 03:55 | Reporte de históricos HW045 | **Jhonny** | «Gracias. En Reportes consultamos el histórico del servidor HW045 del diez al once de julio. Data Processing lo lee de Supabase y devuelve el resumen;» |
| 04:07 | Descarga del CSV | **Jhonny** | «el mismo reporte se descarga en CSV para auditoría.» |
| 04:14 | Baseline vs Green AI | **Jhonny** | «Aquí comparamos la política reactiva con Green AI en riesgo de SLA y energía. Son datos simulados y energía modelada.» |
| 04:27 | Energía y CO₂e | **Jhonny** | «En Energía, la potencia se modela como reposo más la parte proporcional a la CPU.» |
| 04:34 | Resultado del cálculo | **Jhonny** | «Con el simulador obtenemos «7,34 kWh» modelados; con un factor de emisión y su fuente, el sistema calcula el CO₂e. Sin factor, no lo inventa.» |

---

### EPISODIO 3: PRUEBAS CON DATA MASIVA (04:57 – 12:55) · Ricardo

La carga real tarda ~7 min en pantalla: los bloques están repartidos; entre ellos se puede callar mientras avanza el contador.

| Minuto | En pantalla | Diálogo |
|---|---|---|
| 04:57 | Terminal con el comando | «Episodio tres: el indicador nueve pide demostrar el software con quinientas a mil transacciones. Ejecutamos el script carga_transacciones contra el Gateway en Render.» |
| 05:08 | Se escribe correo y contraseña | «Inicio sesión con mi cuenta; la contraseña no se muestra y el token queda solo en memoria.» |
| 05:23 | «50 nodos · 200 iteraciones × 3 = 601» | «El script descubre los cincuenta servidores y hace doscientas iteraciones. Cada una repite el flujo de la aplicación: pide a Data Processing la ventana de dos horas de CPU, pide a Prediction la estimación a quince minutos y evalúa la recomendación. Con el descubrimiento inicial son seiscientas una transacciones reales, todas con token.» |
| 06:28 | Contador avanzando | «Usamos tres hilos en paralelo para no saturar los quinientos doce megas de los contenedores gratuitos de Render. Cada diez iteraciones se imprime el avance y cuántas respondieron con código doscientos.» |
| 07:58 | Contador avanzando | «Cada petición atraviesa el Gateway en Go, que valida la firma del token antes de reenviarla. Todo queda registrado en un CSV con la operación, el código HTTP, la latencia y el servidor.» |
| 09:58 | Contador avanzando | «Si apareciera un error por el plan gratuito, como un cuatrocientos veintinueve o un quinientos cuatro, quedaría en la tabla tal cual: no repetimos la prueba para maquillarla.» |
| 12:11 | Tabla final | «Terminó: «601» transacciones en «414» segundos, y «601» con código doscientos. La mediana fue de «892» milisegundos en dataset y de unos «2,7» segundos en predicción y recomendación; el percentil noventa y cinco, «3,5» segundos. Las doscientas recomendaciones quedaron «elegibles para revisión».» |
| 12:30 | Prometheus, objetivos | «Prometheus muestra los servicios en estado UP después de la carga. Recordamos que la telemetría es simulada: medimos capacidad y latencia, no ahorro de energía. Pasa Gina con las métricas.» |

---

### EPISODIO 4: PRUEBAS CON MÉTRICAS (12:55 – 15:44)

| Minuto | En pantalla | Habla | Diálogo |
|---|---|---|---|
| 12:56 | PoC, «3. Resultados» | **Gina** | «Episodio cuatro. Para predecir la CPU a quince minutos comparamos cuatro modelos. El Random Forest desplegado logra un error absoluto medio de «3,22» puntos y un RMSE de «4,59», frente a «4,61» y «6,39» de la persistencia: treinta por ciento mejor. En picos el error sube, y lo declaramos.» |
| 13:30 | GitHub Actions, CI | **Jhonny** | «En calidad, cada cambio dispara GitHub Actions, que prueba todos los servicios y construye las imágenes Docker.» |
| 13:44 | Última ejecución en verde | **Jhonny** | «Aquí la última ejecución en main, con todos los trabajos aprobados.» |
| 14:04 | Tabla de suites por servicio | **Jhonny** | «Suites por servicio: Monitoring, ciento doce de ciento doce; Gateway en Java, once de once; Gateway en Go, treinta de treinta con el detector de carreras; Data Processing, ciento catorce de ciento catorce; Prediction, noventa y seis de noventa y seis; frontend trece, simulador diez. Las unitarias prueban una pieza aislada; las de contrato, que la API responda con la forma acordada; las de integración, piezas reales juntas, como Data Processing con SQLite y PostgreSQL.» |
| 14:42 | Smoke 14/14 | **Jhonny** | «La prueba de humo de extremo a extremo pasó «14 de 14» contratos entre microservicios.» |
| 14:59 | Prediction ligera | **Jhonny** | «Además rediseñamos la imagen de Prediction: de «2,85 gigas» a «510 megas», y bajó su memoria en reposo, en una sola medición.» |
| 15:23 | Prometheus en Render | **Jhonny** | «Y Prometheus en Render recoge el simulador cada quince segundos y Prediction cada minuto.» |

---

### EPISODIO 5: PREDICCIONES CON ML DEL PMV1 Y PMV2 (15:44 – 17:33) · Gina

| Minuto | En pantalla | Diálogo |
|---|---|---|
| 15:44 | Pestaña «Predicción y recomendación», HW045 | «Episodio cinco, los dos casos de uso de Machine Learning. Primero, la predicción de CPU a quince minutos, historia HU-03, para el servidor HW045.» |
| 15:53 | Resultado de la predicción | «El Gateway pide a Data Processing la ventana histórica y Prediction estima «59,44 %» para dentro de quince minutos. Se indica el modelo, el instante y la procedencia: datos simulados, valor estimado.» |
| 16:23 | Formulario de recomendación | «Segundo caso, HU-06: una predicción sola no basta para operar.» |
| 16:28 | Valores de ejemplo | «Cargamos memoria al sesenta y cinco por ciento, latencia de ciento veinte milisegundos y errores del cero coma cinco.» |
| 16:38 | Respuesta de la recomendación | «El motor de políticas revisa cada restricción: todas cumplen, así que propone «Mantener capacidad» y queda «Lista para revisión humana». Siempre con executionAllowed en falso: un humano decide.» |
| 16:59 | Memoria 95 % | «Ahora forzamos una violación: memoria al noventa y cinco por ciento, por encima del umbral de ochenta y cinco.» |
| 17:06 | Nueva respuesta | «La respuesta cambia: estado «Bloqueada por restricciones» y salida «Sin propuesta». La memoria excede el límite; vigencia, telemetría, latencia p95 y errores cumplen. Son umbrales de demostración, no un SLA aprobado: no garantizan SLA futuro ni ahorro cuantificado, y toda propuesta requiere revisión humana.» |

---

### EPISODIO 6: TABLERO TRELLO Y CONTENIDOS (17:33 – 19:44)

| Minuto | En pantalla | Habla | Diálogo |
|---|---|---|---|
| 17:38 | Tablero completo, desplazamiento lateral | **Gina** | «Episodio seis, la gestión ágil. Nuestro tablero tiene el Product Backlog, el Sprint Backlog, el refinamiento con expertos, To Do, In Progress, QA y Done, y además los roles de Scrum, los Daily, la Sprint Review y la retrospectiva. Las historias avanzan por columnas según nuestra definición de terminado.» |
| 18:16 | Tarjeta HU-03 | **Jhonny** | «Abro la historia HU-03, la predicción, con los miembros, etiquetas PMV2, Machine Learning y Backend, y fecha de entrega cumplida. La historia: como administrador de TI, necesito la predicción de CPU por nodo a quince minutos, para anticipar saturación.» |
| 18:38 | HU-03: alcance y comentarios | **Jhonny** | «El alcance: un pipeline de inferencia en el microservicio Prediction, con FastAPI y un Random Forest de resolución de cinco minutos, con ventana de dos horas. El endpoint devuelve valor estimado, intervalo de tiempo, recurso y procedencia.» |
| 18:59 | Tarjeta HU-06 | **Jhonny** | «En los comentarios, Jhonny dejó el endpoint /v1/predictions y Ricardo la suite pytest. Ahora la HU-06, también en Done: el administrador de TI recibe recomendaciones basadas en predicciones y contexto operativo, para evaluar ajustes de capacidad con uso eficiente de recursos.» |
| 19:20 | HU-06: alcance y comentarios | **Jhonny** | «Su alcance: propuestas explicables sujetas a revisión humana; sin datos suficientes no calcula redistribuciones. Leonid la probó por el Gateway en Go, con respuesta menor a cuarenta y cinco milisegundos; Ricardo implementó el PolicyEngine con pytest y Gina verificó su coherencia con el modelo.» |

---

### EPISODIO 7: ARQUITECTURA HEXAGONAL Y PROCEDIMIENTOS ALMACENADOS (19:44 – 23:39) · Ricardo

| Minuto | En pantalla | Diálogo |
|---|---|---|
| 19:45 | `data-processing` en GitHub | «Episodio siete, el indicador once. La arquitectura hexagonal está en el código: en Data Processing, en Python, hay dominio, aplicación e infraestructura. El dominio es independiente.» |
| 19:59 | `domain/ports/historical_logs_source.py` | «En el dominio está el puerto HistoricalLogsSource: una interfaz pura, sin base de datos ni frameworks. Define el método read_page, con servidor, rango de fechas, límite y cursor. Así el dominio queda independiente de cualquier tecnología.» |
| 20:19 | `read_historical_logs.py` | «El caso de uso ReadHistoricalLogsUseCase, en la capa de aplicación, solo conoce ese puerto: no sabe si los datos vienen de SQLite o de Supabase. Por eso se puede cambiar el origen sin tocar la lógica.» |
| 20:40 | `historical_sources.py` | «Una factoría, en historical_sources.py, elige el adaptador al arrancar según la variable de entorno HISTORICAL_SOURCE. La lógica de negocio no cambia.» |
| 20:57 | Carpeta de adaptadores | «Aquí los adaptadores: SQLite para desarrollo y Supabase para la nube, el del episodio dos; las rutas FastAPI son el adaptador de entrada.» |
| 21:10 | `monitoring` en Java | «El servicio Monitoring, en Java 21, sigue el mismo patrón: dominio con MetricDefinition y MetricData, y puertos de entrada y de salida.» |
| 21:24 | `QueryMetrics.java` | «QueryMetrics es el puerto de entrada: define qué ofrece la aplicación, y lo invoca el adaptador web, MetricsController.» |
| 21:38 | `MetricsSource.java` | «MetricsSource es el puerto de salida: lo que la aplicación necesita del exterior, las métricas. Depende de esta interfaz, no de Prometheus.» |
| 21:52 | `adapter/out` | «En adapter out están el adaptador de Prometheus y uno de fixture, con datos fijos para las pruebas. Se intercambian sin tocar el dominio.» |
| 22:06 | SQL, líneas 45–66 | «Sobre procedimientos almacenados, en supabase-auth-setup.sql: la función PL/pgSQL handle_new_auth_user, con SECURITY DEFINER, inserta el perfil en user_profiles y asigna el rol OPERATOR en user_roles. Un trigger, on_auth_user_created_green_ai, la dispara después de cada alta en auth.users. Así todo usuario nuevo nace como operador.» |
| 22:32 | SQL, líneas 79–104 | «Y custom_access_token_hook es un Auth Hook: lee en user_roles el rol del usuario, por defecto OPERATOR, y lo inyecta como claim user_role en el token JWT. El Gateway valida ese token y aplica el control de acceso por rol, RBAC.» |
| 22:58 | `ci.yml` | «Por último, la integración continua: ci.yml se ejecuta en cada push o pull request a main y test, con seis trabajos: frontend, Prediction, Data Processing, Gateway Go, Monitoring e imágenes Docker.» |
| 23:17 | GitHub Actions | «El frontend se despliega con otro workflow, pages.yml: publica en GitHub Pages producción desde main y desarrollo desde test, en la ruta dev. Solo usa la clave pública, nunca service_role.» |

---

### CIERRE (23:39 – 24:26)

| Minuto | En pantalla | Habla | Diálogo |
|---|---|---|---|
| 23:39 | Indicadores con su minuto | **Jhonny** | «Para cerrar, en pantalla queda el minuto exacto donde se demuestra cada indicador de la rúbrica.» |
| 23:48 | | **Gina** | «Todo con datos simulados declarados y métricas reales del modelo.» |
| 23:55 | QR del repositorio y de la app | **Leonid** | «Aquí están los enlaces al código y a la aplicación en la nube.» |
| 24:02 | | **Gina** | «Pueden revisarlos con estos códigos QR.» |
| 24:09 | Agradecimiento | **Ricardo** | «Gracias por su atención, profesor.» |
| 24:13 | Mosaico 2×2 | **Los 4** | «¡Muchas gracias!» |

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

> **Ojo (10/11/2026):** en el video (Ep. 4, 14:06) se ve la tabla de `docs/academico/08-pruebas-resultados-discusion.md`, con otras cifras (Gateway Java 11, Data Processing 114, Prediction 96, Frontend 13). Esta tabla 6.2 y ese documento no coinciden: no decir «433» ni «447» en la locución; leer solo lo que sale en pantalla. Pendiente: actualizar el documento 08 con los conteos actuales y verificarlos.

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
| **Indicador 9:** Demostración con datos (500 a 1000 transacciones) del PMV1 y PMV2 sobre entorno de calidad. | 4 pts | Episodio 1, 2 y 3 | 00:44 – 12:55 | Operación del frontend en GitHub Pages; ejecución en vivo de 601 transacciones con `carga_transacciones.py` contra Render, lectura en vivo de percentiles p50/p95 y auditoría en CSV. |
| **Indicador 10:** Demostración con datos de integración con ML (1.er y 2.º caso de uso predictivo en calidad). | 3 pts | Episodio 5 | 15:44 – 17:33 | Caso 1: Estimación de demanda a 15 min con Random Forest sobre ventana histórica. Caso 2: Recomendación bajo políticas con `executionAllowed=false`. |
| **Indicador 11:** Demostración de arquitectura hexagonal, procedimientos almacenados en GitHub y Kanban. | 3 pts | Episodio 6 y 7 | 17:33 – 23:39 | Tablero Trello completo; inspección en GitHub de capas domain/application/adapters de 2 servicios; triggers PL/pgSQL y CI/CD. |
| **Guion de software:** Carátula con nombre del proyecto e integrantes completos. | Requisito | Carátula | 00:00 – 00:44 | Carátula con universidad, asignatura, docente, proyecto y 4 integrantes con sus roles. |
| **Guion de software:** Participación del 100 % de integrantes con cámara y nombre completo. | Requisito | Todo el video | 00:00 – 24:26 | Voz y cámara de los 4 encima del video, con rótulo de nombre completo en cada tramo (sección 0.5). |
| **Guion de software:** Duración estimada del video entre 20 y 30 minutos. | Requisito | Video global | 24:26 | Video montado de 24:26, respetando los límites de la guía docente. |

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
       00:00 Carátula e integrantes
       00:44 Episodio 1: Pruebas funcionales del PMV1
       02:33 Episodio 2: Pruebas funcionales del PMV2
       04:57 Episodio 3: Pruebas con data masiva (601 transacciones)
       12:55 Episodio 4: Pruebas con métricas
       15:44 Episodio 5: Predicciones con ML del PMV1 y PMV2
       17:33 Episodio 6: Tablero Trello y contenidos
       19:44 Episodio 7: Arquitectura hexagonal y procedimientos almacenados
       23:39 Cierre
       ```
     * Incluir los enlaces al repositorio en GitHub y a la aplicación en GitHub Pages.
2. **Generación del Código QR:**
   - Tomar la URL final del video en YouTube (ej. `https://youtu.be/xxxxxxxxxxx`).
   - Utilizar un generador de QR vectorial o PNG de alta resolución (mínimo 500×500 píxeles, nivel de corrección de error M o Q).
   - Insertar el código QR generado en:
     * La carátula del informe académico escrito (`informe-unidad-III.md` o formato entregable).
     * La diapositiva final de cierre del video para permitir que el evaluador acceda al recurso desde cualquier dispositivo móvil.
