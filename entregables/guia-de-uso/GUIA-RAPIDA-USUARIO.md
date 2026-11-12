# Guía Rápida de Usuario — Green AI Observatorio

Manual operativo para el usuario final: Administrador de TI, Operador de Infraestructura y Observador / Auditor.

---

## 1. Requisitos del Sistema y Direcciones de Acceso

### 1.1. Requisitos Técnicos
* **Navegador web moderno:** Google Chrome 110+, Mozilla Firefox 110+, Microsoft Edge 110+ o Apple Safari 16+ con JavaScript y almacenamiento local (localStorage) habilitados.
* **Cuenta institucional:** Usuario registrado y confirmado en la plataforma de autenticación Supabase Auth del proyecto.
* **Resolución recomendada:** 1280 x 720 píxeles o superior para visualización óptima del mapa de calor de Racks y gráficos temporales.

### 1.2. Direcciones de Acceso (URLs)
* **Entorno de Desarrollo y Demostración (Staging):**  
  `https://woshtsu.github.io/green-ai-workspace-cld/dev/`
* **Entorno de Producción:**  
  `https://woshtsu.github.io/green-ai-workspace-cld/`

---

## 2. Roles de Usuario y Nivel de Acceso (RBAC)

La plataforma aplica control de acceso perimetral en el API Gateway validando el atributo `user_role` de tu credencial:

* **ADMIN (Administrador de TI):** Acceso integral. Puede consultar toda la telemetría, topología y gráficos, ejecutar predicciones de demanda de CPU, evaluar recomendaciones operacionales, descargar reportes históricos en CSV (el PDF está planificado) y gestionar configuraciones.
* **OPERATOR (Operador de Infraestructura):** Acceso operativo diario. Puede consultar métricas en tiempo real, visualizar Racks y Red de flujos, solicitar predicciones a 15 minutos, evaluar recomendaciones de capacidad bajo políticas de umbrales y exportar reportes históricos en CSV.
* **VIEWER (Observador / Auditor):** Acceso de solo lectura. Puede navegar por el catálogo de métricas, el resumen de los 50 servidores, el mapa de calor de Racks y el histórico. No tiene permisos para ejecutar inferencias de CPU ni solicitar recomendaciones (las solicitudes responden HTTP 403 amigable).

---

## 3. Tareas Principales en Tres Pasos o Menos

### Tarea 1: Iniciar Sesión o Registrarse
* **Registro de nuevo usuario:**
  1. Accede a `register.html` y completa: "Nombre completo", "Correo institucional", "Contraseña" y "Confirmar contraseña".
  2. Pulsa el botón "Registrar operador".
  3. Pulsa el enlace inferior "Iniciar sesión" para ingresar con tus credenciales creadas.
* **Inicio de sesión regular:**
  1. Accede a `login.html` e ingresa tu "Correo institucional" y "Contraseña".
  2. Pulsa el botón "Entrar al sistema".
  3. El sistema valida la sesión y te redirige automáticamente al Observatorio (`dashboard.html`).

### Tarea 2: Ver Métricas de los 50 Servidores
1. En la sección superior "Centro de operación", selecciona la "Métrica" deseada (ej. CPU) y el rango "Histórico" ("5 minutos", "15 minutos" o "1 hora").
2. Pulsa el botón "Actualizar".
3. Consulta las tarjetas KPI en la pestaña "Resumen" ("Media del conjunto", "Más cargado", "Menos cargado") o pulsa la pestaña "Detalle por servidor" para revisar la tabla paginada con los 50 servidores, su calidad ("valid") y el buscador por código (ej. HW045).

### Tarea 3: Ver Racks con Mapa de Calor
1. En la barra superior de navegación, pulsa el enlace "Racks" (`network.html`).
2. Observa la disposición de los 50 servidores agrupados en 5 racks coloreados por estado semafórico: Verde (Normal, menos de 40 %), Ámbar (Moderado, 40 a 80 %) y Rojo (Crítico, mayor a 80 %).
3. Haz clic sobre cualquier casilla de servidor para desplegar en el panel lateral derecho sus datos específicos ("CPU actual", "Núcleos", "Potencia máx." y "Procedencia").

### Tarea 4: Predecir CPU a 15 Minutos de un Servidor
* **Método directo desde Racks (Recomendado):**
  1. En `network.html`, haz clic sobre el servidor que deseas evaluar.
  2. En el panel lateral "Detalle del servidor", pulsa el botón "Predecir 15 min".
  3. Lee el porcentaje proyectado en "Estimación futura de CPU" junto con la hora estimada.
* **Método alternativo desde el Observatorio:**
  1. En `dashboard.html`, selecciona el clúster y servidor en los desplegables del "Centro de operación".
  2. Pulsa la pestaña "Predicción y recomendación".
  3. Pulsa el botón "Estimar CPU del servidor seleccionado".

### Tarea 5: Solicitar Recomendación y Verificar Restricciones
1. En `dashboard.html`, pulsa la pestaña "Predicción y recomendación" y desplázate al bloque "Recomendación con restricciones".
2. Pulsa el botón "Usar valores de ejemplo" (o completa "Memoria (%)", "Latencia p95 (ms)", "Errores (%)" y pulsa "Usar ahora" en "Instante de telemetría").
3. Pulsa el botón "Evaluar recomendación". El sistema verifica los límites operacionales y emite la propuesta con la declaración expresa de que no se ejecutan cambios de infraestructura (`executionAllowed=false`), requiriendo siempre autorización humana.

### Tarea 6: Descargar Reporte Histórico en CSV
1. En `dashboard.html`, pulsa la pestaña "Reportes y experimento".
2. En la tarjeta "Reporte de históricos", verifica o escribe el "Código de hardware" (ej. HW045) y define las fechas "Desde" y "Hasta".
3. Pulsa el botón "Descargar CSV" (se iniciará la descarga del archivo plano consolidado) o pulsa "Ver resumen" para visualización tabular en pantalla.

### Tarea 7: Estimar Consumo de Energía y CO2e
1. En `dashboard.html`, pulsa la pestaña "Energía y CO₂e".
2. En la tarjeta "1 · Con datos del simulador", pulsa el botón "Calcular con el simulador" (o en la tarjeta 2, pulsa "Calcular con el ejemplo").
3. Lee el consumo de energía integrado en kilovatios-hora (kWh) mostrado en el panel de resultados. Para estimar emisiones, ingresa voluntariamente los valores oficiales en "kg CO₂e por kWh" y "Fuente del factor".

### Tarea 8: Usar la Ayuda Contextual («?»)
1. Ubica cualquier título de tarjeta, métrica o campo que cuente con el botón circular «?».
2. ¿Necesitas orientación sobre un indicador? Haz clic sobre el botón «?».
3. ¡Listo! Se abrirá una ventana emergente que explica de forma transparente: qué es la métrica, para qué sirve, cómo se calcula, qué valores ingresar y sus límites experimentales. Ciérrala con la tecla Escape o pulsando fuera de la ventana.

---

## 4. Mensajes de Error Frecuentes y Acciones de Resolución

La interfaz traduce automáticamente cualquier excepción técnica a un mensaje comprensible en lenguaje natural:

| Mensaje en Pantalla | Causa Técnica | Acción Requerida por el Usuario |
|---|---|---|
| **Tu sesión venció** | Código HTTP 401 (token JWT expirado o sesión cerrada). | Pulsa el botón "Ir a iniciar sesión", ingresa nuevamente tus credenciales y repite la operación. |
| **Aún estamos reuniendo datos** | Código HTTP 422 con error INSUFFICIENT_DATA o INVALID_DATASET. | El modelo Random Forest requiere una ventana acumulada mínima (~20 minutos de telemetría). Espera unos minutos a que el simulador registre muestras y pulsa "Reintentar". |
| **El servicio está despertando** | Error de red, timeout o cold start en Render Free Tier. | Los microservicios en la nube gratuita se suspenden tras 15 minutos sin uso. El contenedor toma entre 45 y 60 segundos en iniciar. Espera un minuto y pulsa "Reintentar". |
| **Tu rol no permite esta acción** | Código HTTP 403 (permisos insuficientes). | Tu cuenta posee rol VIEWER y solicitaste una predicción o recomendación. Si requieres operar, solicita a un Administrador que actualice tu rol a OPERATOR o ADMIN. |
| **Hay datos por corregir** | Código HTTP 400 o 422 por valores inválidos en el formulario. | Revisa los valores ingresados: memoria y porcentaje de errores deben situarse entre 0 y 100, latencia mayor o igual a 0 ms, o pulsa "Usar valores de ejemplo". |
| **El archivo es demasiado grande** | Código HTTP 413 (tamaño de carga útil excedido). | El archivo JSON de potencia cargado supera el límite permitido de 1,5 MB. Reduce la ventana de tiempo o la frecuencia de las muestras. |

---

## 5. Principio de Honestidad Experimental

Ten en cuenta las siguientes consideraciones técnicas al interpretar la información del sistema:
* Todos los datos del entorno de demostración provienen de generación sintética determinista mediante el microservicio Simulator.
* La potencia en vatios y la energía en kWh calculadas son **modeladas** a partir de la utilización de CPU mediante relación lineal, no medidas por sensores físicos de hardware.
* Toda propuesta del módulo de recomendaciones es estrictamente consultiva y cuenta con salvaguarda de no ejecución automática (`executionAllowed=false`).
