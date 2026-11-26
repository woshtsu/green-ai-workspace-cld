<<<resumen>>>
## RESUMEN EJECUTIVO

El proyecto Green AI aborda la variabilidad de la demanda computacional y el sobreaprovisionamiento de recursos en centros de datos universitarios. Su objetivo fue desarrollar y validar un prototipo que monitorea la telemetría de la infraestructura, predice la utilización de CPU a 15 minutos y emite recomendaciones explicables bajo supervisión humana (*Recommendation-Only*: ninguna recomendación se ejecuta automáticamente). Se desarrolló en tres PMV con Scrum adaptado y la guía PMBOK: PMV1 (telemetría, ingesta y persistencia), PMV2 (predicción, contratos OpenAPI y dashboard) y PMV3 (procesos de software, calidad FURPS+/OWASP, ingeniería inversa y ola 2 de mejoras). La solución usa microservicios con arquitectura hexagonal por servicio (Python/FastAPI, Java/Spring Boot y Go), Prometheus y Grafana, Supabase (PostgreSQL y Auth) y despliegue en Render y GitHub Pages. Con datos simulados, Random Forest obtuvo un MAE de 3,22 y un RMSE de 4,59 puntos porcentuales en validación (MAE de 3,85 en test), con un 30 % menos de error que la persistencia y un 14 % menos que la media móvil. Se aprobaron 492 pruebas automatizadas y el *smoke test* 14/14, y la ola 2 (decisión humana persistente, reporte PDF, tabla accesible y etiquetas de energía modelada) quedó desplegada en Render. La auditoría final dictaminó «cumple parcialmente» (FURPS+ 87 %, OWASP 86/100 estimado) y «no apto para producción» mientras no se cierren los hallazgos de RLS y de sesión real. El proyecto aporta a los ODS 7, 9 y 12, y al ODS 13 solo como método de estimación de CO2e, sin reducción medida.

**Palabras clave:** Green AI, predicción de demanda computacional, arquitectura hexagonal, microservicios, eficiencia energética, Recommendation-Only.

**Fecha de corte del informe final:** 25/11/2026. Las secciones heredadas de la Unidad III conservan la fecha de su medición (11/11/2026 o 19/11/2026), indicada en cada tabla o figura.

---

<<<abstract>>>
## ABSTRACT

The Green AI project addresses computational workload variability and resource over-provisioning in university data centers. Its goal was to develop and validate a prototype that monitors infrastructure telemetry, forecasts CPU utilization 15 minutes ahead, and issues explainable recommendations under human supervision (recommendation-only: nothing is executed automatically). It was built in three minimum viable products with adapted Scrum and PMBOK: MVP1 (telemetry, ingestion and persistence), MVP2 (forecasting, OpenAPI contracts and dashboard) and MVP3 (software processes, FURPS+/OWASP quality, reverse engineering and a second wave of improvements). The solution uses microservices with a hexagonal architecture per service (Python/FastAPI, Java/Spring Boot and Go), Prometheus and Grafana, Supabase, and deployment on Render and GitHub Pages. On simulated data, Random Forest achieved a validation MAE of 3.22 and RMSE of 4.59 percentage points (test MAE 3.85), 30% lower error than persistence and 14% lower than moving average. 492 automated tests and the 14/14 smoke test passed, and the second wave (persistent human decision, PDF report, accessible table and modeled-energy labels) was deployed on Render. The final audit rated the system "partially compliant" (FURPS+ 87%, OWASP 86/100 estimated) and "not production-ready" until the row-level security and real-session findings are closed. The project contributes to SDGs 7, 9 and 12, and to SDG 13 only as a CO2e estimation method, with no measured reduction.

**Keywords:** Green AI, computational workload forecasting, hexagonal architecture, microservices, energy efficiency, recommendation-only.

---

<<<ods13>>>
- **ODS 13 (Acción por el clima):** el proyecto aporta **un método de estimación**, no una reducción medida: la energía se modela con $P(u)$ y la huella de CO2e se etiqueta como «estimada» en el dashboard (F-06). No se dispone de mediciones eléctricas físicas ni de un factor de emisión oficial aplicado a datos reales, por lo que **no se declara ninguna reducción de emisiones**. Indicador propuesto para trabajo futuro: kWh medidos por PDU frente a kWh modelados, con el factor de emisión del SEIN publicado por el COES.

<<<t4_29733>>>
| **Ley N.° 29733 y D.S. N.° 016-2024-JUS** (Protección de Datos Personales) | Cuentas de usuario para administradores y operadores técnicos. | **Implementado:** la telemetría técnica no contiene datos personales; Supabase Auth gestiona correos y roles. **Pendiente (H-02 / F-01):** el snapshot del repositorio registra políticas RLS «Permitir todo» y una columna `password` en texto plano; su revisión y corrección en Supabase requiere acceso administrativo y **no está verificada** al 25/11/2026. |

<<<t4_30096>>>
| **Ley N.° 30096** (Delitos Informáticos) | Seguridad perimetral y prevención de accesos no autorizados. | **Implementado y verificado:** JWT y RBAC (ADMIN, OPERATOR, VIEWER) en los Gateways Java y Go (19 y 40 pruebas al 19/11/2026). **Parcial (H-01):** Prediction y Data Processing siguen accesibles directamente en Render; desde el Sprint 7 las rutas de decisiones de Prediction exigen el secreto `X-Green-Gateway-Secret` y responden 401 sin él (verificado el 25/11/2026). **Pendiente:** *rate limiting* y auditoría de 401/403 (OW-05, OW-12). |

<<<t4_iso>>>
| **ISO/IEC 21031:2024 (SCI)** | Especificación de intensidad de carbono del software. | **Implementado:** la energía y el CO2e se muestran con la etiqueta «modelada/estimada» (F-06). **Pendiente:** factor de emisión oficial aplicado a mediciones reales (HU-10 sin resultado medido). |

<<<t32>>>
| Dimensión de prueba | Entornos probados | Comportamiento observado | Dictamen (solo lo verificado) |
|---|---|---|---|
| Sistemas operativos | • Windows 11 con Docker Desktop (equipo de desarrollo)<br>• Contenedores Linux oficiales `python:3.12` y `golang:1.25` | El 19/11/2026 las suites de Prediction, Data Processing, Frontend, Gateway Java y Monitoring se ejecutaron en Windows, y las de Gateway Go y Simulator en contenedores Linux (Figuras VIII.38 a VIII.44). | Verificado en Windows 11 y en Linux dentro de contenedores. **No se probó** macOS ni Ubuntu nativo, por lo que no se declara portabilidad en ellos. |
| Plataformas heterogéneas | • Persistencia: SQLite y Supabase (PostgreSQL)<br>• Despliegue: Render (Linux) y GitHub Pages | Data Processing: 128 pruebas aprobadas y 8 omitidas (las omitidas requieren PostgreSQL). Servicios desplegados en Render (Figura VIII.47). | Desacoplamiento hexagonal efectivo entre dominio y adaptadores de persistencia. |
| Hardware restringido | Instancia gratuita de Render | Imagen de Prediction reducida de 2,85 GB a 510 MB; memoria en reposo de 122 a 142 MiB (medición única). Arranque en frío: primera petición entre 12,6 y 69,5 s y segunda < 0,8 s (Figura VIII.45). | Funciona en la capa gratuita con la latencia de arranque en frío documentada. |

<<<pmv3>>>
#### VIII.2.3. Pruebas del PMV3: procesos, calidad y ola 2 de mejoras (ejecutadas en el Sprint 7)

El PMV3 (Sprints 7 y 8, 17/11–30/11/2026) se centró en los procesos de software, la calidad del producto y los entregables de la Unidad IV. A diferencia de la versión de la Unidad III, en la que estas verificaciones estaban planificadas, la Tabla 30 recoge su **estado real al 25/11/2026**, incluidos los pendientes.

Tabla 30. Verificaciones del PMV3 y su estado real al 25/11/2026

| Proceso | Verificación | Resultado | Evidencia | Estado |
| --- | --- | --- | --- | --- |
| Ingeniería inversa | 7 fases sobre el repositorio | 23 hallazgos (2 críticos, 4 altos, 10 medios y 7 bajos); críticos H-01 (elusión del Gateway en la nube) y H-02 (RLS permisiva y `password` en texto plano) | `guias/semana14/ingenieria-inversa/docs/ingenieria_inversa.md` | Ejecutada |
| Calidad FURPS+ y OWASP | Auditoría final con re-medición | FURPS+ 87,00 % bruto (174/200) y 87,62 % ponderado; OWASP 86,0/100 estimado; dictamen «cumple parcialmente» y **«no apto para producción»** | `08_Auditoria_Final.md` (FURPS+ y OWASP) | Ejecutada |
| Ola 2 de mejoras | HU-07, HU-13, U-02, F-06 y S-01 | Implementadas, probadas (492 pruebas) y desplegadas en Render el 25/11/2026 | Figuras VIII.38 a VIII.46 | Ejecutada |
| Desarrollo (flujo Git) | PR revisado por otro integrante | PR #7 (`test`→`main`) aprobado por Jhonny Quintana y fusionado con 12 checks en verde | Figuras VIII.36 y VIII.36.a | Ejecutada |
| Integración continua | Historial de `ci.yml` | Ejecuciones en verde en los PR integrados | Figura VIII.37 | Ejecutada |
| Rendimiento y ML | Latencia, *throughput* y métricas de ML | Prediction: latencia mediana de 97 ms con 1 usuario y 1,14 s con 8 concurrentes; *throughput* de 9,8 a 7,0 req/s (H-03). Arranque en frío de 12,6–69,5 s. Métricas de ML sin cambios (§VIII.1.3) | Ingeniería inversa; Figura VIII.45 | Ejecutada |
| Seguridad de datos (F-01) | RLS y columna `password` en Supabase | No verificado: requiere acceso administrativo | — | **Pendiente** |
| Sesión real (F-03) | Dashboard `/dev/` con cuenta del equipo | Validación de punta a punta no realizada | — | **Parcial** |
| Usuarios finales | Sesión con usuarios ajenos al desarrollo y acta | Sin acta registrada en el repositorio a la fecha de corte | — | **Pendiente** |
| Video y póster | Lista de cotejo de la Unidad IV | Video de la Unidad III reutilizado sin cambios (Anexo A); póster en `exportados/semana15/` | Anexo A | Ejecutada |

##### a) Ola 2 de mejoras implementada

- **HU-07 · Decisión humana persistente (F-02):** `POST` y `GET /v1/recommendations/{recommendationId}/decisions` en Prediction. Cada decisión guarda usuario, rol, decisión, comentario, fecha y el SHA-256 de la recomendación evaluada; `executionAllowed` sigue en `false` y nada se ejecuta. Un usuario decide una sola vez por recomendación (409) y el rol VIEWER puede consultar, pero no decidir (403). **Limitación:** en Render se guarda en SQLite sobre disco efímero; la migración equivalente para Supabase (`software/prediction/migrations/001_recommendation_decisions.sql`, con RLS) **no está aplicada**.
- **Remediación parcial de H-01:** como Prediction es accesible en Render sin pasar por el Gateway, la identidad solo se acepta si llega el secreto `X-Green-Gateway-Secret` (variable `GATEWAY_SHARED_SECRET`, configurada en Render el 25/11/2026). Sin la variable, las rutas responden 503 (falla cerrada); con cabeceras de identidad falsas y sin secreto, 401 (Figura VIII.46). Los Gateways Java y Go eliminan las cabeceras de identidad del cliente y las reponen desde el JWT validado. Las demás rutas de Prediction y Data Processing siguen públicas: H-01 queda **mitigado parcialmente**.
- **HU-13 · Reporte en PDF (F-05):** Data Processing acepta `format=pdf` con los mismos datos y validaciones que JSON y CSV y la leyenda «Datos simulados; energía modelada, no medida». Coste medido: la imagen pasa de 426 MB a 498 MB.
- **U-02, F-06 y S-01:** tabla accesible equivalente al gráfico (sin escaneo axe/Lighthouse), etiquetas «modelada/estimada» en energía y CO2e, y el caso de uso del Simulator ya no importa adaptadores (salida con semilla 42 idéntica antes y después).

##### b) Pruebas automatizadas del Sprint 7 (19/11/2026)

Tabla 30.a. Pruebas automatizadas por servicio antes y después del Sprint 7

| Servicio | Resultado al 19/11/2026 | Antes del Sprint 7 |
|---|---|---|
| Prediction | 116 aprobadas | 100 |
| Data Processing | 128 aprobadas y 8 omitidas | 121 y 8 omitidas |
| Gateway Java | 19 pruebas, 0 fallos | 12 |
| Gateway Go | 40 PASS, 0 FAIL (`go test -race`) | 32 |
| Simulator | 14 pruebas, OK | 10 |
| Frontend | 63 aprobadas, 0 fallos | 48 |
| Monitoring | 112 pruebas, 0 fallos | 112 |
| **Total** | **492 aprobadas** | 435 |

![Consola de Windows (19/11/2026): pytest en software/prediction, 116 passed](../informe-corregido/evidencias-nube/captura-S7-prediction-pytest.png)
Figura VIII.38. Prediction Service: 116 pruebas aprobadas, incluidas las 16 de decisiones HU-07.

![Consola de Windows (19/11/2026): pytest en software/data-processing, 128 passed y 8 skipped](../informe-corregido/evidencias-nube/captura-S7-data-processing-pytest.png)
Figura VIII.39. Data Processing: 128 aprobadas y 8 omitidas, incluidas las 7 del reporte PDF.

![Consola de Windows (19/11/2026): mvnw verify en software/gateway, 19 pruebas y BUILD SUCCESS](../informe-corregido/evidencias-nube/captura-S7-gateway-java-mvn.png)
Figura VIII.40. Gateway Java: 19 pruebas, BUILD SUCCESS.

![Consola de Windows (19/11/2026): go test -race en Docker golang:1.25, 40 PASS](../informe-corregido/evidencias-nube/captura-S7-gateway-go.png)
Figura VIII.41. Gateway Go: 40 pruebas con detector de carreras, 0 fallos.

![Consola de Windows (19/11/2026): unittest del Simulator en Docker python:3.12, Ran 14 tests, OK](../informe-corregido/evidencias-nube/captura-S7-simulator-unittest.png)
Figura VIII.42. Simulator: 14 pruebas, incluida la que verifica que la aplicación no importa adaptadores.

![Consola de Windows (19/11/2026): node --test en software/frontend, 63 pass y 0 fail](../informe-corregido/evidencias-nube/captura-S7-frontend-tests.png)
Figura VIII.43. Frontend: 63 pruebas (tabla accesible, URL del PDF, decisiones y etiquetas modeladas).

![Consola de Windows (19/11/2026): mvnw verify en software/monitoring, 112 pruebas y BUILD SUCCESS](../informe-corregido/evidencias-nube/captura-S7-monitoring-mvn.png)
Figura VIII.44. Monitoring sin regresiones: 112 pruebas.

##### c) Despliegue y rendimiento en la nube

![Consola de Windows (19/11/2026 17:45): curl a las rutas de salud de los 6 servicios de Render; primera petición entre 12,6 y 69,5 s y segunda entre 0,36 y 0,78 s](../semana13/evidencias/captura-P01-arranque-frio-render.png)
Figura VIII.45. Arranque en frío medido en Render Free: primera petición tras inactividad (12,6–69,5 s) y segunda (< 0,8 s).

![Consola de Windows (25/11/2026 22:11): curl directo a Prediction en Render con cabeceras de identidad falsas responde 401 «Petición no originada en el Gateway» y el Gateway sin token responde 401](evidencias/captura-S15-ola2-render-401.png)
Figura VIII.46. Ola 2 desplegada en Render: Prediction rechaza con 401 la identidad falsificada sin el secreto del Gateway y el Gateway exige token en la ruta de decisiones HU-07.

![Panel de Render con los 6 servicios desplegados](../informe-corregido/evidencias-nube/render-6-servicios-desplegados.png)
Figura VIII.47. Servicios del proyecto desplegados en Render.

##### d) Proceso: revisión por pares e integración continua

![Pull Request #7 del Sprint 7 (test hacia main) aprobado por Jhonny Quintana (CristhianQuintana) con «Changes approved» y 12 checks de CI en verde](../informe-corregido/evidencias-nube/captura-C310-pr7-aprobado.png)
Figura VIII.36. Pull Request #7 del Sprint 7 (ola 2) aprobado por otro integrante antes de fusionar, con los 12 checks de CI en verde, conforme al criterio 3 de la Definición de Terminado.

![Pull Request #7 fusionado en main por woshtsu tras la aprobación de CristhianQuintana, con 12 checks aprobados](../informe-corregido/evidencias-nube/captura-C310b-pr7-fusionado.png)
Figura VIII.36.a. Fusión del Pull Request #7 en main después de la aprobación.

![Historial de ejecuciones del workflow ci.yml en la pestaña Actions de GitHub](../informe-corregido/evidencias-nube/captura-C311-actions.png)
Figura VIII.37. Historial de ejecuciones de GitHub Actions (workflow ci.yml).

##### e) Indicadores 8, 9 y 10 de la lista de cotejo de la Unidad IV

- **Indicador 8 (arquitectura hexagonal, entorno de calidad y reportes):** arquitectura hexagonal por servicio (S-01 completó el Simulator), ejecución sobre la rama `test` y su despliegue de desarrollo, y reportes de ingeniería inversa, FURPS+ y OWASP con dictamen. **Cumple, con el dictamen de seguridad parcial.**
- **Indicador 9 (usuarios finales):** no hay acta de reunión con usuarios finales registrada a la fecha de corte.

PENDIENTE-EQUIPO: adjuntar el acta de la sesión con usuarios finales (fecha, asistentes ajenos al desarrollo, tareas de la guía rápida ejecutadas, retroalimentación y acuerdos) y su captura. Si no se realizó, dejar constancia de ello aquí.

- **Indicador 10 (rendimiento y métricas de ML):** métricas de ML de §VIII.1.3 (MAE 3,22 en validación y 3,85 en test), latencia y *throughput* con concurrencia (Tabla 30) y arranque en frío medido (Figura VIII.45).

<<<concl_oe4>>>
#### Conclusión del objetivo específico 4 de proceso — Procesos de software, calidad y entregables (PMV3)
Los procesos del PMV3 se ejecutaron y tienen evidencia: ingeniería inversa en 7 fases (23 hallazgos), auditoría final FURPS+ (87 %) y OWASP (86/100 estimado), ola 2 de mejoras implementada con 492 pruebas aprobadas y desplegada en Render, y revisión por pares del PR #7 con CI en verde. Se concluye que el flujo `test`→`main` con PR revisado y CI es operativo. Sin embargo, el producto **no es apto para producción**: H-01 está mitigado solo en las rutas de decisiones, H-02 (RLS y columna `password`) no está verificado en Supabase, la sesión real (F-03) es parcial y las decisiones se guardan en SQLite efímero. La prueba con usuarios finales y su acta quedan pendientes de registro.

<<<anexo_d>>>
### Anexo D. Correspondencia con la plantilla del informe final (semana 14)

Tabla D.1. Ubicación de cada apartado de la plantilla del docente en este informe

| Apartado de la plantilla | Sección de este informe |
|---|---|
| Resumen ejecutivo (≤ 250 palabras), ODS y palabras clave | Resumen ejecutivo y Abstract |
| Introducción: antecedentes | Antecedentes (tras el Capítulo III), §1.1 |
| Identificación y formulación del problema | §1.1 |
| Marco teórico | Capítulo II (conocimientos de ingeniería) y antecedentes |
| Objetivos (general y específicos por PMV) | §1.2 |
| Conocimientos de ingeniería aplicados | Capítulo II |
| Ingeniero y sociedad | Capítulo III |
| Metodología y aportes por PMV | Capítulo IV |
| Herramientas modernas | Capítulo V |
| Diseño de ingeniería (requerimientos, BD, arquitectura, código) | Capítulo VI y Anexo A |
| Gestión del proyecto (Gantt y tablero) | Capítulo VII |
| Pruebas, resultados y discusión | Capítulo VIII (PMV3 en §VIII.2.3) |
| Lecciones aprendidas y conclusiones | Capítulos IX y X |
| Anexos (video, GitHub, experto, evidencias) | Anexos A a C |
