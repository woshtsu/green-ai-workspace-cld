![](../../informe-corregido/evidencias/logo-uc.png){width=40%}

::: {custom-style="Portada Institucion"}
UNIVERSIDAD CONTINENTAL
:::

::: {custom-style="Portada Escuela"}
Facultad de Ingeniería · Escuela Académico Profesional de Ingeniería de Sistemas e Informática
:::

::: {custom-style="Portada Curso"}
Taller de Proyectos 1 (ASUC01584) · Evaluación y gestión de cambios del congreso de ingeniería
:::

::: {custom-style="Portada Titulo"}
Del satélite al centro de datos: solicitud de cambio CHG-001-2026 para incorporar datos climáticos satelitales en Green AI
:::

::: {custom-style="Portada Subtitulo"}
VIII Congreso Internacional de Ingeniería y Arquitectura – noviembre de 2026
:::

::: {custom-style="Portada Etiqueta"}
INTEGRANTES
:::

::: {custom-style="Portada Texto"}
Ricardo Porras Veli
:::

::: {custom-style="Portada Texto"}
Leonid Kisley Orlando Huamán Collazos
:::

::: {custom-style="Portada Texto"}
Gina Diana Barrera Peña
:::

::: {custom-style="Portada Texto"}
Jhonny Cristhian Quintana Carhuaricra
:::

::: {custom-style="Portada Etiqueta"}
DOCENTE
:::

::: {custom-style="Portada Texto"}
Jorge Alfredo Guevara Jiménez
:::

::: {custom-style="Portada Etiqueta"}
NRC
:::

::: {custom-style="Portada Texto"}
30170
:::

::: {custom-style="Portada Nota"}
Huancayo – Perú, 2026-20
:::

## 1. Ponencia seleccionada y alineamiento con las competencias

**Ponencia:** «Tecnología satelital y su impacto en ciudades inteligentes y sostenibilidad urbana», Ing. Alejandro Manuel Martínez, decano de la Facultad de Ingeniería de la Universidad de Buenos Aires (UBA).

**Síntesis.** El expositor describió los tres segmentos de un sistema espacial (acceso al espacio, segmento de vuelo e infraestructura terrena) y las órbitas GEO, MEO y LEO, y explicó cómo los satélites resuelven problemas urbanos: posicionamiento y catastro, monitoreo de clima urbano y calidad ambiental, detección de hundimientos por interferometría de radar, movilidad y prevención de desastres. Destacó tres ideas útiles para nuestro proyecto: (1) los satélites meteorológicos y de observación, combinados con modelos de inteligencia artificial, permiten pronosticar fenómenos con mayor rapidez que las plataformas tradicionales; (2) el gran desafío actual es reducir el tiempo entre la captura del dato y su disponibilidad en tierra para ofrecer información «verdaderamente en línea»; y (3) las señales GPS sincronizan los relojes de las redes eléctricas y de telecomunicaciones, de modo que una interrupción afectaría servicios que dependen de una marca de tiempo común.

**Hallazgo para Green AI.** Green AI predice la demanda de CPU y modela la energía de los servidores con $P(u)$, pero **no considera la refrigeración**, que depende de la temperatura exterior. La ponencia muestra que existen datos climáticos derivados de satélite, accesibles y procesables con IA, que pueden incorporarse como variable externa. Esta es la innovación que se formaliza en la solicitud de cambio CHG-001-2026.

Tabla 1. Alineamiento de la ponencia con las competencias del curso

| Competencia | Cómo la activa la ponencia en Green AI |
|---|---|
| C1 Análisis del problema | Nueva causa del consumo energético no modelada: la carga térmica de refrigeración depende del clima exterior. |
| C2 Conocimientos de ingeniería | Datos de observación terrestre y meteorológica como variables exógenas de un modelo de regresión de series temporales. |
| C3 Ingeniero y sociedad | Sostenibilidad urbana y climática (ODS 13) y uso responsable de datos abiertos. |
| C4 Gestión del proyecto | Solicitud de cambio formal sobre la línea base del PMV3 y su priorización en el backlog. |
| C5 Herramientas modernas | Servicio de datos climáticos satelitales vía API REST (NASA POWER) y su matriz de limitaciones. |
| C6 Prueba de concepto y arquitectura | Nuevo puerto de salida y adaptador en la arquitectura hexagonal, sin acoplar el dominio. |

## 2. Trazabilidad en las 6 competencias ICACIT

**C1 – Análisis del problema (AG-T08 / AG-C08).** El problema de Green AI es el sobreaprovisionamiento por falta de anticipación de la demanda. El análisis actual cuantifica la carga de cómputo (MAE de 3,22 puntos porcentuales en validación con Random Forest), pero su modelo energético considera solo los servidores. La energía total de un centro de datos es $E_{total} = E_{TI} \times PUE$, donde el PUE (*Power Usage Effectiveness*) refleja la refrigeración y otras cargas auxiliares; la encuesta global del Uptime Institute reporta un PUE medio de 1,56 en 2024 [1], es decir, alrededor de un tercio de la energía total no corresponde a TI. En Green AI el PUE es implícitamente 1,0: es una causa no modelada. Indicadores propuestos: temperatura exterior horaria (°C), PUE modelado y diferencia entre la energía modelada con y sin refrigeración (kWh y %).

**C2 – Conocimientos de ingeniería (AG-I07).** Se incorporan variables exógenas $x_t$ (temperatura exterior) al modelo $\hat{y}_{t+h} = f(y_t, y_{t-1}, \dots, x_t)$ y un modelo de PUE dependiente de la temperatura, por ejemplo lineal por tramos $PUE(T) = PUE_0 + k \cdot \max(0, T - T_0)$, con parámetros calibrados y declarados como supuestos. La temperatura solo se usará como predictor si reduce el MAE en validación cronológica sin fuga de información; en caso contrario, se usará únicamente para estimar la energía de refrigeración.

**C3 – El ingeniero y la sociedad (AG-I01 / AG-I02).** Los datos climáticos son abiertos y no contienen datos personales, por lo que no afectan la Ley N.° 29733. Éticamente, el PUE y la energía de refrigeración se etiquetarán como «modelados», igual que el resto de la energía del proyecto, y no se declarará ningún ahorro medido. El impacto ambiental esperado es una estimación más completa de la huella de CO2e (ODS 13). La visualización debe conservar la accesibilidad lograda en el Sprint 7 (tabla textual equivalente al gráfico).

**C4 – Gestión del proyecto (PMBOK / Ágil).** El cambio se registra como CHG-001-2026, pasa por el Comité de Control de Cambios (CCB) y se prioriza en el backlog del PMV3 detrás de los pendientes críticos de seguridad (F-01, RLS de Supabase, y F-03, sesión real). Impacto en el cronograma: un incremento independiente de 26 horas-hombre estimadas, sin modificar las historias ya cerradas.

**C5 – Uso de herramientas modernas (AG-I11).** Herramienta evaluada: API pública de NASA POWER (datos meteorológicos derivados de satélites y modelos de reanálisis). La Tabla 2 resume sus limitaciones.

Tabla 2. Matriz de limitaciones técnicas de la herramienta evaluada

| Aspecto | Limitación | Mitigación en Green AI |
|---|---|---|
| Resolución espacial | Celda del orden de medio grado: no representa el microclima del campus. | Usar el dato como contexto regional; calibrar con un sensor local en trabajo futuro. |
| Latencia de publicación | Los datos no son instantáneos (el desafío de «información en línea» señalado en la ponencia). | Consultar por hora pasada y cachear; la predicción no depende de que el dato llegue a tiempo. |
| Disponibilidad | Servicio externo sin acuerdo de nivel de servicio. | Adaptador con *timeout*, reintento y respuesta «dato no disponible» (falla segura). |
| Despliegue | Render Free duerme los servicios (arranque en frío de 12,6–69,5 s medido). | Precalentamiento controlado ya documentado; caché del último valor. |
| Pruebas | Los tests no deben depender de internet. | Adaptador sintético determinista para pruebas y modo local. |

**C6 – Prueba de concepto y arquitectura hexagonal.** El dominio de Prediction (predicción y recomendaciones) no conocerá la API externa. Se añade un puerto de salida en la capa de aplicación y dos adaptadores de salida en infraestructura, ensamblados en la composición del servicio, igual que se hizo con `DecisionRepository` en el Sprint 7.

Tabla 3. Puerto y adaptadores propuestos

| Capa | Elemento | Responsabilidad |
|---|---|---|
| Dominio | `CondicionClimatica` (objeto de valor) | Temperatura (°C), instante y procedencia («satelital», «sintética» o «no disponible»). |
| Aplicación (puerto de salida) | `ClimaExternoPort.obtener(ubicacion, instante) -> CondicionClimatica` | Contrato que usa el caso de uso de recomendación para estimar el PUE. |
| Infraestructura (adaptador OUT) | `NasaPowerClimaAdapter` | Llama a la API REST, valida, cachea y aplica *timeout*; ante error devuelve «no disponible». |
| Infraestructura (adaptador OUT) | `ClimaSinteticoAdapter` | Serie determinista con semilla para pruebas y desarrollo sin red. |
| Composición | `adapters/composition.py` | Elige el adaptador por variable de entorno (`CLIMA_FUENTE=nasa_power` o `sintetico`). |

## 3. Solicitud y gestión del cambio (CHG-001-2026)

Tabla 4. Ficha de la solicitud de cambio

| Campo | Contenido |
|---|---|
| Código | CHG-001-2026 |
| Ponencia de origen | «Tecnología satelital y su impacto en ciudades inteligentes y sostenibilidad urbana» (Alejandro Manuel Martínez, UBA) |
| Solicitante | Equipo Green AI (NRC 30170) |
| Descripción | Incorporar la temperatura exterior horaria derivada de satélite mediante un puerto y adaptador nuevos en Prediction, estimar el PUE y la energía de refrigeración modelada, mostrarlos en el dashboard con la etiqueta «modelada» y evaluar la temperatura como variable exógena del modelo de demanda. |
| Justificación | El modelo energético actual omite la refrigeración (PUE implícito 1,0); la ponencia evidencia que los datos satelitales abiertos permiten cubrir esa brecha. |
| Prioridad | Media (por debajo de F-01 y F-03, que son críticos de seguridad). |

**Impacto en el alcance (Product Backlog).** Se añaden dos historias de usuario:

- **HU-17. Contexto climático y refrigeración estimada.** Como operador, quiero ver la temperatura exterior y la energía de refrigeración estimada junto a la predicción, para decidir con una visión completa del consumo.
  - *Dado* que el adaptador de clima devuelve una temperatura válida, *cuando* consulto una recomendación, *entonces* veo la temperatura, el PUE modelado y la energía de refrigeración con la etiqueta «modelada».
  - *Dado* que la API externa no responde en 5 s, *cuando* consulto una recomendación, *entonces* la recomendación se muestra igual y el clima aparece como «no disponible».
- **HU-18. Evaluación de la temperatura como predictor.** Como analista, quiero comparar el modelo con y sin temperatura exterior en validación cronológica, para incorporarla solo si mejora el MAE.
  - *Dado* el mismo corte temporal sin fuga, *cuando* ejecuto el experimento, *entonces* MLflow registra el MAE y el RMSE de ambas variantes y el modelo con temperatura solo se adopta si su MAE es menor.

**Impacto en los PMV.** El cambio se asigna al PMV3 (Sprint 8, ampliación del alcance), porque reutiliza la experimentación del PMV2 y la arquitectura consolidada del PMV3. No modifica PMV1 ni PMV2.

**Impacto en la arquitectura hexagonal.** Un puerto de salida nuevo y dos adaptadores (Tabla 3); el dominio y los contratos existentes no cambian. El contrato OpenAPI de recomendaciones añade un campo opcional `climate` (compatible hacia atrás), por lo que el Gateway y el frontend actuales siguen funcionando sin cambios obligatorios.

Tabla 5. Estimación del esfuerzo (horas-hombre)

| Actividad | Horas-hombre |
|---|---|
| Puerto, objeto de valor y adaptadores (real y sintético) | 6 |
| Modelo de PUE y experimento con y sin temperatura (HU-18) | 8 |
| Campo `climate` en OpenAPI y vista en el frontend | 4 |
| Pruebas unitarias, de contrato y de falla segura | 6 |
| Documentación y registro en el informe | 2 |
| **Total estimado** | **26** |

**Dictamen del Comité de Control de Cambios (CCB).** Factibilidad técnica: **alta**, porque el patrón puerto-adaptador ya se aplicó en el Sprint 7 y la API es gratuita y sin credenciales de pago. Riesgos: baja resolución espacial y dependencia de un servicio externo, ambos mitigados con falla segura y adaptador sintético. Decisión: **APROBADO** para su incorporación al backlog del PMV3 (Sprint 8), condicionado a cerrar antes los pendientes de seguridad F-01 y F-03. A la fecha de este informe el cambio está aprobado y planificado, pero **no implementado**.

## 4. Conclusiones

1. El cambio es técnicamente factible con bajo riesgo arquitectónico: el puerto `ClimaExternoPort` y sus adaptadores aíslan la API externa del dominio, del mismo modo que `DecisionRepository` aisló la persistencia en el Sprint 7, de modo que el núcleo de predicción y las 492 pruebas existentes no se ven afectados.
2. El cambio mejora la validez del análisis energético más que la precisión de la predicción: incorpora la refrigeración (PUE) que el modelo actual omite, aunque la temperatura solo se adoptará como predictor si reduce el MAE en validación cronológica (HU-18).
3. La gestión formal del cambio protege la línea base: el CCB lo prioriza detrás de los hallazgos críticos de seguridad y acota su esfuerzo en 26 horas-hombre, evitando que una innovación del congreso desplace trabajo de mayor riesgo.

## Referencias

[1] UPTIME INSTITUTE. *Global Data Center Survey 2024* [en línea]. Nueva York: Uptime Institute, 2024. Disponible en: https://uptimeinstitute.com/resources/research-and-reports/uptime-institute-global-data-center-survey-results-2024

[2] NASA LANGLEY RESEARCH CENTER. *POWER: Prediction Of Worldwide Energy Resources* [en línea]. Disponible en: https://power.larc.nasa.gov/

[3] MARTÍNEZ, A. M. *Tecnología satelital y su impacto en ciudades inteligentes y sostenibilidad urbana*. Ponencia en el VIII Congreso Internacional de Ingeniería y Arquitectura, Universidad Continental, 2026.

## Anexo. Evidencia de participación

![](../evidencias/foto-congreso-ricardo-porras.jpg){width=75%}

Figura 1. Ricardo Porras Veli siguiendo en modalidad virtual (Zoom) la transmisión del VIII Congreso Internacional de Ingeniería y Arquitectura.
