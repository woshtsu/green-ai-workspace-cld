Universidad Continental

Facultad de Ingeniería

Ingeniera de Sistemas e Informática

INFORME UNIDAD IV

UNIDAD DIDÁCTICA: TALLER DE PROYECTOS I

PROFESOR: Jorge Alfredo Guevara Jimenez

NRC: 15956

AUTORES:

● MUNIVE GUERRA, José Alejandro

● SINCHE ALVARADO, Yerald Cristhian

● VILCHEZ DE LA CRUZ, Marvin Omar

● BOT, Jorgito (Asistente IA)

2024

“Desarrollo de un software de consumo, monitoreo del nivel y calidad

del agua en tanques de sistemas educativos (Santa Isabel y Tambo

Huari) integrando IoT y Machine Learning”

1
𝐽𝑜𝑠é 𝑀𝑢𝑛𝑖𝑣𝑒

;

2
𝑌𝑒𝑟𝑎𝑙𝑑  𝑆𝑖𝑛𝑐ℎ𝑒

;

3
𝑂𝑚𝑎𝑟 𝑉𝑖𝑙𝑐ℎ𝑒𝑧

Escuela Académica Profesional de Ingeniería de Sistemas e Informática,

Universidad Continental, Junín, Perú.

RESUMEN EJECUTIVO

El proyecto "Desarrollo de un software de consumo, monitoreo del nivel y calidad del agua

en tanques de sistemas educativos (Santa Isabel y Tambo Huari) integrando IoT y

Machine Learning" tuvo como objetivo mejorar la gestión del agua en entornos educativos

mediante la implementación de tecnologías accesibles y eficientes. Se desarrolló una

aplicación web con integración IoT y predicción de datos mediante Machine Learning.

Se realizaron 21 pruebas por cada historia de usuario organizado en los 3 Sprints

,asimismo se alcanzó un 99.7% de precisión en la identificación del consumo de agua,

del mismo modo se alcanzó un 93 en el nivel de agua y un 75% de exactitud en la

medición de la calidad del agua, considerando parámetros como pH , turbidez , tds,

temperatura y humedad. Los datos estadísticos resaltan la relevancia del monitoreo en

este proyecto, ya que según un estudio, una parte significativa de las muestras analizadas

mostró contaminación por microorganismos dañinos como coliformes, Escherichia coli y

Pseudomonas aeruginosa en tanques en Perú, sin mencionar

las enfermedades

relacionadas con el agua.

Este proyecto contribuye principalmente al Objetivo de Desarrollo Sostenible (ODS) 6:

Agua Limpia y Saneamiento, promoviendo la sensibilización y una mejor gestión del agua

en instituciones educativas.

Palabras clave: Monitoreo del agua, IoT educativo, Machine Learning aplicado.

ÍNDICE

I. INTRODUCCIÓN......................................................................................................... 8
1.1 Antecedentes...................................................................................................... 8
1.2 Identificación y formulación del problema:.......................................................... 9
1.2.1 Contexto..................................................................................................... 9
1.2.2 Problema Central........................................................................................9
1.2.3 Consecuencias del Problema...................................................................12
1.2.4 Necesidad................................................................................................ 13
1.2.5 Justificación.............................................................................................. 13
1.3 Marco teórico.....................................................................................................14
1.3.1 Contexto del Problema............................................................................. 14
1.3.2 Importancia del Monitoreo del Agua.........................................................14
1.3.3 Tecnología IoT en el Monitoreo del Agua................................................. 14
1.3.4 Aplicación del Machine Learning en el Análisis de Datos de Agua..........14
1.3.5 Integración de IoT y Machine Learning para la Gestión del Agua........... 15
1.3.6 Sensor de Consumo de Agua.................................................................. 15
1.3.7 Sensor de Nivel de Agua..........................................................................15
1.3.8 Sensor de Turbidez.................................................................................. 16
1.3.9 Sensor de pH........................................................................................... 16
1.3.10 Sensor de Temperatura.......................................................................... 16
1.3.11 Sensor de TDS (Total de Sólidos Disueltos)...........................................17
1.4 Objetivos del proyecto.......................................................................................17
II. CONOCIMIENTOS DE INGENIERÍA APLICADOS / RELACIONADOS...................19
2.1 Conocimiento en Matemáticas:......................................................................... 19
2.2 Conocimiento en ciencias naturales..................................................................19
2.3 Conocimiento en Ingeniería:............................................................................. 20
III. INGENIERO Y LA SOCIEDAD:............................................................................... 21
3.1 Justificación social:............................................................................................21
3.2 Justificación Económica:................................................................................... 21
3.3 Acontecimientos tecnológicos y científicos:...................................................... 21
IV. METODOLOGÍA EMPLEADA.................................................................................. 22
4.1 Metodología SCRUM....................................................................................... 22
4.2 Metodologia Cascada........................................................................................26
V. USO DE HERRAMIENTAS MODERNAS................................................................. 34
5.1 Framework: Laravel...........................................................................................34
5.2 Lenguaje: PHP.................................................................................................. 35
5.3 Base de datos: MySQL..................................................................................... 35
5.4 Herramienta de Machine Learning: Google Colab............................................ 36

5.5 Servidor web: Apache http................................................................................ 37
5.6 XAMPP:.............................................................................................................37
5.7 Proveedor de Hosting: AlwaysData...................................................................38
5.8 Control de Versiones: Git.................................................................................. 38
5.9 Placa de Hardware: ESP32...............................................................................39
VI. DISEÑO DE INGENIERÍA....................................................................................... 40
VI.1 Listado de Requerimientos funcionales........................................................... 40
VI.2 Arquitectura de la solución planteada..............................................................79
VII. GESTIÓN DEL PROYECTO...................................................................................84
7.1 LÍNEA BASE..................................................................................................... 84
7.2 DIAGRAMA GANTT EJECUTADO................................................................... 93
IX. PRUEBAS Y RESULTADOS Y DISCUSIÓN........................................................... 98
X. LECCIONES APRENDIDAS POR PMV................................................................. 145
PMV 1: Consumo del agua................................................................................... 145
PMV 2: Nivel del agua...........................................................................................145
PMV 3: Calidad del Agua...................................................................................... 146
XI. CONCLUSIONES.................................................................................................. 147
Anexos........................................................................................................................ 150
XII. BIBLIOGRAFÍA................................................................................................... 151
ANEXOS..................................................................................................................... 154
Aplicaciones :........................................................................................................ 171
1. HydroColor........................................................................................................ 172
2. Water Quality App............................................................................................. 172
3. AquaCheck........................................................................................................173
4. TurbAqua...........................................................................................................174
ACTA DE CONSTITUCIÓN DEL PROYECTO......................................................179

ÍNDICE DE FIGURAS

Figura 1. Uso de Laravel en SYSMONWA....................................................................... 32
Figura 2. Uso de PHP en SYSMONWA............................................................................ 32
Figura 3. Uso de MSQL en SYSMONWA......................................................................... 33
Figura 4. Uso de Google Collab en SYSMONWA........................................................... 33
Figura 5. Uso de Apache en SYSMONWA.......................................................................34
Figura 6. Uso de XAMP en SYSMONWA......................................................................... 34
Figura 7. Uso de AlwaysData en SYSMONWA............................................................... 35
Figura 8. Uso de PHP en SYSMONWA............................................................................ 36
Figura 9. Uso de PHP en SYSMONWA............................................................................ 36
Figura 10. Prototipos Gestión de usuarios.....................................................................52
Figura 11. Prototipos de Gestión de clientes................................................................. 55
Figura 12. Prototipos de Gestión de tanques y sensores.............................................57
Figura 13. Prototipo de Registro de datos en tiempo real............................................ 61
Figura 14. Prototipos de Visualización de datos del consumo del agua en tiempo
real......................................................................................................................................61
Figura 15. Prototipo de Visualización de datos del consumo del agua historico.... 62
Figura 16. Prototipo de Visualización de datos del consumo del agua en tiempo real
62
Figura 17. Prototipo de Alerta Semanal de consumo de agua..................................... 63
Figura 18. Prototipo de Predicción del consumo del agua...........................................64
Figura 19. Prototipo de Visualización de datos del nivel del agua en tiempo real.... 65
Figura 20 . Prototipo de Visualización de datos del nivel del agua historico............ 65
Figura 21. Prototipo de Alerta de nivel del agua............................................................66
Figura 22 Prototipo de Exportación de datos de nivel del agua.................................. 66
Figura 23. Prototipo de Predicción del tiempo restante para vaciar el tanque...........67
Figura 24. Prototipo de Visualización de datos de la calidad del agua en tiempo real..
67
Figura 25. Prototipo de Visualización de datos de la calidad del agua historico....... 68
Figura 26. Prototipo de Exportación y predicción de la calidad del agua...................68
Figura 27. Flujo de pantallas de prototipos....................................................................69
Figura 28. Base de datos SYSMONWA........................................................................... 75
Figura 29. Arquitectura de solución elaborada en Archimate...................................... 76
Figura 30. Arquitectura de aplicación. Elaboración propia.......................................... 77
Figura 31. Diagrama de EDT. Elaboración propia.......................................................... 79

ÍNDICE DE TABLAS

Tabla N° 1. Product Backlog - SYSMONWA........................................... 19
Tabla N° 2. Sprint Backlog - SYSMONWA............................................. 21
Tabla N° 3. Cuadro de Línea de tiempo y PMV...................................... 37
Tabla N° 4. Cuadro de criterios de aceptación HU1 - 2024 Gestión de
usuarios......................................................................................................40
Tabla N° 5. Cuadro de criterios de aceptación HU2 - 2024 Gestión de
clientes....................................................................................................... 40
Tabla N° 6. Cuadro de criterios de aceptación HU3 - 2024 Gestión de
tanques y sensores................................................................................... 41
Tabla N° 6. Cuadro de criterios de aceptación HU4 - 2024 Registro de
datos del consumo de agua en tiempo real de los sensores................41
Tabla N° 7. Cuadro de criterios de aceptación HU5 - 2024
Visualización de los datos del consumo de agua en tiempo real.........42
Tabla N° 8. Cuadro de criterios de aceptación HU6 - 2024
Visualización de los datos histórico del consumo de agua.................. 42
Tabla N° 9. Cuadro de criterios de aceptación HU7 - 2024 Exportación
de datos del consumo del agua............................................................... 43
Tabla N° 10. Cuadro de criterios de aceptación HU8 - 2024 Alertas
semanales por correo electrónico del consumo del agua.................... 43
Tabla N° 11. Cuadro de criterios de aceptación HU9 - 2024 Predicción
del consumo de agua................................................................................44
Tabla N° 12. Cuadro de criterios de aceptación HU10 - 2024 Registro
del nivel de agua en tiempo real.............................................................. 44
Tabla N° 13. Cuadro de criterios de aceptación HU11 - 2024
Visualización del nivel de agua en tiempo real...................................... 45
Tabla N° 14. Cuadro de criterios de aceptación HU12 - 2024
Visualización de los datos históricos del nivel de agua........................45
Tabla N° 15. Cuadro de criterios de aceptación HU13 - 2024
Visualización de los datos históricos del nivel de agua........................46
Tabla N° 16. Cuadro de criterios de aceptación HU14 - 2024
Exportación de datos históricos de nivel de agua.................................46
Tabla N° 17. Cuadro de criterios de aceptación HU15 - 2024 Predicción
del tiempo restante para vaciar el tanque...............................................47
Tabla N° 18. Cuadro de criterios de aceptación HU16 - 2024 Registro
de datos de calidad del agua en tiempo real.......................................... 47
Tabla N° 19. Cuadro de criterios de aceptación HU17 - 2024
Visualización de la calidad del agua en tiempo real.............................. 48
Tabla N° 20. Cuadro de criterios de aceptación HU18 - 2024
Visualización de datos históricos de la calidad del agua......................48
Tabla N° 21. Cuadro de criterios de aceptación HU19 - 2024 Alertas
automáticas por correo cuando los parámetros de calidad estén fuera
de los límites..............................................................................................49

Tabla N° 22. Cuadro de criterios de aceptación HU20 - 2024
Exportación de datos de calidad del agua..............................................49
Tabla N° 23. Cuadro de criterios de aceptación HU21 - 2024 Predicción
de la calidad del agua............................................................................... 50
Tabla N° 24. Cuadro de Machine Learning............................................. 51
Tabla N° 25. Prueba , resultado y discusión del PM1............................96
Elaboración propia.................................................................................... 96
Tabla N° 26. Cuadro de Evidencia FURPS............................................114
Tabla N° 27. Cuadro Resultados obtenidos en los modelos de
machine learning..................................................................................... 116
Tabla N° 28. Cuadro Discusión, Similitudes y diferencias del PMV1.119
Tabla N° 29. Cuadro de Evaluación herramientas por método de
factores ponderados - Lenguaje de programación..............................132
Tabla N° 30. Cuadro de Evaluación herramientas por método de
factores ponderados - Framework de programación.......................... 132
Tabla N° 31. Cuadro de Evaluación herramientas por método de
factores ponderados - Base de datos................................................... 132
Tabla N° 32. Cuadro de Evaluación herramientas por método de
factores ponderados - Herramienta Machine Learning....................... 133
Tabla N° 33. Cuadro de Evaluación herramientas por método de
factores ponderados - Servidor Web.....................................................133
Tabla N° 34. Cuadro de Evaluación herramientas por método de
factores ponderados - Placa de Hardware............................................133

I.

INTRODUCCIÓN

1.1 Antecedentes

1.1.1 Integration of Cloud computing and Internet of Things: A survey

Las soluciones inteligentes para el monitoreo de la calidad del agua están

ganando relevancia con los avances en la tecnología de comunicación. El artículo

“Internet of things enable real time water quality monitoring system” [6] presenta

una visión detallada de los trabajos recientes realizados en el campo del

monitoreo inteligente de la calidad del agua. Además, se propone una solución

más simple y eficiente en cuanto al consumo de energía para el monitoreo de la

calidad del agua en tuberías, basada en tecnología de Internet de las Cosas (IoT).

El modelo desarrollado se utiliza para probar muestras de agua y los datos se

suben a Internet para su análisis. El sistema también envía una alerta a un

usuario remoto cuando los parámetros de calidad del agua se desvían de los

valores estándar predefinidos.

1.1.2 Smart water quality monitoring system with cost-effective using IoT

Los avances en la comunicación inalámbrica y el Internet de las Cosas (IoT) están

impulsando nuevas capacidades para sensores, lo que es clave para aplicaciones

ambientales. El artículo “Smart water quality monitoring system with cost-effective

using IoT” [7] propone un sistema de monitoreo de la calidad del agua (WQM)

utilizando tecnología IoT. El sistema emplea sensores para medir parámetros

como el pH,

turbidez, nivel del agua,

temperatura y humedad. Los datos

recopilados se procesan mediante una Unidad de Microcontrolador (MCU) y se

envían a la nube a través de la plataforma ThinkSpeak para supervisar la calidad

del agua. Esto busca asegurar el suministro de agua potable, un aspecto crucial

dado que el 40% de las muertes en el mundo son causadas por agua

contaminada.

1.1.3 Sistema de monitoreo basado en IoT para la medición de calidad de

agua de riego

Dado que la agricultura es una de las principales actividades económicas en el

Valle del Mantaro, como lo indica el Censo Nacional 2017,

la región Junín

presenta una gran fortaleza agrícola con más de 2.3 millones de hectáreas de

superficie agraria y más de 120 mil productores agropecuarios. Huancayo

concentra el 22.4% del total de productores. Las aguas del río Mantaro, utilizadas

para riego, se ven afectadas por

la contaminación de metales pesados

provenientes de empresas mineras y aguas residuales domésticas,

lo que

aumenta la turbidez del agua y afecta la producción agrícola. Además, el cambio

climático ha incrementado la temperatura del agua de riego, lo que reduce el

rendimiento de cultivos como papa, zanahoria, quinua, maíz, entre otros. El

objetivo de la investigación “Sistema de monitoreo basado en IoT para la

medición de calidad de agua de riego” [8] es implementar un sistema de

monitoreo en tiempo real basado en IoT para medir la temperatura, el pH y la

turbidez del agua de riego, mediante prototipos diseñados para capturar estas

variables clave.

1.2 Identificación y formulación del problema:

1.2.1 Contexto

Las comunidades de Santa Isabel y Tambo Huari, ubicadas en zona urbana y

zona rural respectivamente, enfrentan desafíos significativos en la gestión y

seguridad del suministro de agua potable en sus sistemas educativos. La falta

de un monitoreo continuo y efectivo del agua almacenada en los tanques de

las escuelas pone en riesgo la salud de los estudiantes y el personal educativo

debido a la posible contaminación y deterioro de la calidad del agua.

1.2.2 Problema Central

La escasez y contaminación del agua son problemas críticos que afectan a

nivel global y particularmente a Perú, donde el 31,15% de la población

consume agua contaminada con metales pesados y el 73,7% carece de

acceso a agua gestionada de forma segura, según la ONU y el INEI. En áreas

rurales como Junín, la situación es alarmante, con una brecha del 52.07% en

el acceso a agua potable, lo que obliga a muchas comunidades a depender de

fuentes de agua no seguras.

Actualmente, no existe un sistema eficiente de monitoreo que permita a las

autoridades educativas y municipales evaluar en tiempo real el nivel y la

calidad del agua en los tanques de las instituciones educativas. Esto conlleva

a una gestión reactiva en lugar de proactiva, donde las intervenciones solo se

realizan cuando se detecta un problema grave,

lo que podría generar

situaciones críticas de salud pública. El siguiente gráfico ayuda a entender que

el agua que consumen los peruanos de sus tanques evidencias lo siguiente:

Fuente: Calidad microbiológica del agua de tanques y pozos artesianos

de establecimientos de salud.

Por lo tanto es crucial actuar monitoreando que los tanques no tengan estos

microorganismos o sustancias que se puedan formar en el tanque.

De igual manera se debe de tomar en cuenta las enfermedades relacionadas

con el agua de un estudio hecho en Lima:

Fuente: Enfermedades infecciosas relacionadas con el agua en el Perú

Para tener un enfoque más detallado sobre las instituciones educativas “Santa

Isabel” y “Tambo Huari” la falta de un sistema de monitoreo eficiente de los

tanques de agua conlleva problemas como la acumulación de sedimentos y

bacterias, afectando la calidad del agua y la salud de la comunidad educativa.

Actualmente, el mantenimiento de los tanques se realiza de forma reactiva,

solo cuando surge un problema grave,

lo cual

incrementa el riesgo de

situaciones críticas para la salud pública. Nos enfocaremos en los datos de

Junín en donde se evidencia que la mayoría de la población no tiene acceso al

servicio de agua gestionada de manera segura.

Para abordar estos problemas, se propone implementar un software de

monitoreo que utilice tecnologías de IoT y Machine Learning. Este sistema

permitiría monitorear en tiempo real el nivel, consumo y calidad del agua en

los tanques, optimizando la gestión hídrica en el centro educativo. Con esta

solución, se podría asegurar un ambiente seguro y saludable, además de

promover mejores prácticas en la administración del

recurso hídrico,

contribuyendo así al Objetivo de Desarrollo Sostenible 6, que busca garantizar

acceso universal al agua limpia y saneamiento gestionado de manera

sostenible.

1.2.3 Consecuencias del Problema

● Riesgo de Salud: Los estudiantes y el personal corren el riesgo de

consumir agua contaminada,

lo que puede provocar enfermedades

transmitidas por el agua, como diarrea, fiebre tifoidea y otras infecciones.

● Interrupción Educativa: La mala calidad del agua podría llevar a cierres

temporales de las escuelas, afectando el aprendizaje continuo de los

estudiantes.

● Gestión Ineficiente: Sin datos precisos y en tiempo real sobre la calidad y

cantidad de agua, las decisiones se basan en suposiciones o inspecciones

periódicas que no son suficientes para prevenir problemas a tiempo.

1.2.4 Necesidad

Es necesario desarrollar un sistema de monitoreo que combine tecnologías de

Internet de las Cosas (IoT) y Machine Learning para medir y analizar

constantemente el nivel y la calidad del agua en los tanques de las escuelas.

Este sistema debe ser capaz de alertar a las autoridades sobre posibles

contaminaciones o niveles críticos de agua, permitiendo intervenciones

rápidas y efectivas.

1.2.5 Justificación

El desarrollo de este sistema es crucial para garantizar que las comunidades

de Santa Isabel y Tambo Huari tengan acceso continuo a agua potable segura

en sus instituciones educativas. Al

incorporar IoT y Machine Learning, se

busca no solo monitorear de manera eficiente el agua, sino también anticipar y

prevenir problemas antes de que afecten a la comunidad. Además, se espera

obtener información valiosa que permita comparar las medidas tomadas por

escuelas rurales y urbanas, por ejemplo, cómo las prácticas de manejo y

mantenimiento en una escuela rural como Tambo Huari podrían diferir de

aquellas en una institución educativa de ciudad en caso de obtener resultados

positivos, como menor contaminación o niveles de acidez controlados.

Por ejemplo, si

los resultados del monitoreo en la escuela de Tambo Huari

muestran que el agua se mantiene limpia y sin niveles ácidos significativos, se

podrían investigar las prácticas locales, como la frecuencia de limpieza de

tanques, el

tipo de tratamiento del agua utilizado, o las técnicas de

almacenamiento, que podrían ser distintas a las aplicadas en las instituciones

educativas de la ciudad. Esta comparación no solo permite aprender de los

métodos eficaces, sino que también puede inspirar a otras instituciones a

adoptar prácticas más sostenibles y efectivas para la gestión del agua,

contribuyendo a una mejora integral del manejo de recursos hídricos en

diversas comunidades.

1.3 Marco teórico

1.3.1 Contexto del Problema

El acceso a agua potable segura es crucial para el bienestar y la salud [9] en

las escuelas, especialmente en áreas rurales como Santa Isabel y Tambo

Huari. La falta de un sistema de monitoreo continuo en estas instituciones

educativas puede llevar a problemas graves de salud pública, ya que no se

pueden detectar oportunamente las contaminaciones del agua almacenada en

tanques, lo cual es vital para proteger a los estudiantes y al personal.

1.3.2 Importancia del Monitoreo del Agua

Monitorear la calidad del agua en tiempo real permite identificar y prevenir la

contaminación antes de que afecte a la comunidad escolar. Actualmente, las

inspecciones periódicas no son suficientes para garantizar que el agua se

mantenga en condiciones óptimas. Un sistema automatizado de monitoreo

puede ofrecer datos más precisos y permitir una gestión más proactiva [8].

1.3.3 Tecnología IoT en el Monitoreo del Agua

El Internet de las Cosas (IoT) se refiere a la interconexión de dispositivos

como sensores que pueden medir la calidad y el nivel del agua en tiempo real

[10]. Estos sensores pueden detectar cambios en el pH,

la turbidez,

la

temperatura y otros indicadores importantes de la calidad del agua. Los datos

recopilados se transmiten automáticamente a una plataforma centralizada

para su análisis.

1.3.4 Aplicación del Machine Learning en el Análisis de Datos de Agua

El Machine Learning (ML) es una tecnología que permite analizar grandes

cantidades de datos y predecir posibles problemas antes de que ocurran [11].

En el contexto del monitoreo del agua, los algoritmos de ML pueden detectar

patrones y anomalías en los datos proporcionados por los sensores IoT, lo que

facilita la identificación de riesgos potenciales y la toma de decisiones

informadas para evitar la contaminación o el desperdicio de agua.

1.3.5 Integración de IoT y Machine Learning para la Gestión del Agua

Combinar IoT con Machine Learning permite una gestión más eficiente y

anticipativa del suministro de agua [12]. Mientras los sensores proporcionan

datos en tiempo real, los algoritmos de ML procesan esta información para

ofrecer alertas tempranas y recomendaciones, lo que mejora la respuesta a

posibles contaminaciones o fallas en el sistema de agua de las escuelas.

1.3.6 Sensor de Consumo de Agua

Los sensores de consumo de agua están diseñados para medir el flujo de

agua en un sistema y proporcionar datos precisos sobre la cantidad de agua

utilizada [14]. Estos sensores pueden emplear tecnologías como el

flujo

magnético, el ultrasonido o el rotor, cada una con sus propias ventajas y

limitaciones. Los sensores de flujo magnético utilizan campos magnéticos para

medir el movimiento del agua, mientras que los sensores de ultrasonido envía

ondas ultrasónicas que se reflejan en el flujo de agua para determinar su

velocidad. La medición precisa del consumo de agua es crucial para la gestión

eficiente del recurso y para la identificación de fugas o pérdidas en sistemas

de distribución.

1.3.7 Sensor de Nivel de Agua

Los sensores de nivel de agua son dispositivos utilizados para medir el nivel

de agua en un contenedor o reservorio. Estos sensores pueden ser de tipo

flotador, capacitivo, ultrasónico o por presión. Los sensores de flotador utilizan

un flotador que sube y baja con el nivel del agua, activando un interruptor a

medida que alcanza ciertos niveles [13]. Los sensores capacitivos detectan

cambios en la capacitancia entre dos placas debido al cambio en el nivel del

agua. Los sensores ultrasónicos emiten pulsos ultrasónicos que se reflejan en

la superficie del agua, y el tiempo de respuesta se utiliza para calcular el nivel.

Estos sensores son esenciales para el control automático del

llenado de

tanques y la prevención de desbordamientos.

1.3.8 Sensor de Turbidez

Los sensores de turbidez miden la claridad del agua detectando la cantidad de

partículas suspendidas que dispersan la luz. La turbidez se expresa

generalmente en unidades de NTU (Unidades Neftométricas). Estos sensores

emiten una luz a través del agua y miden la cantidad de luz que se dispersa a

diferentes ángulos [15]. La turbidez del agua es un indicador importante de la

calidad del agua, ya que niveles elevados pueden indicar contaminación o la

presencia de partículas que afectan la potabilidad del agua. Estos sensores

son utilizados en sistemas de tratamiento de agua y en la monitorización

ambiental para asegurar que el agua cumpla con los estándares de calidad.

1.3.9 Sensor de pH

Los sensores de pH miden la acidez o alcalinidad de una solución, en este

caso, el agua. El pH se mide en una escala de 0 a 14, donde un valor de 7

indica neutralidad, valores menores a 7 indican acidez y valores mayores a 7

indican alcalinidad. Los sensores de pH funcionan mediante electrodos que

reaccionan con iones de hidrógeno en la solución, generando una señal

eléctrica que es proporcional al nivel de pH [16]. Estos sensores son

esenciales en aplicaciones de tratamiento de agua, agricultura, y procesos

industriales, ya que el pH del agua puede afectar la eficiencia de los procesos

y la salud de los ecosistemas.

1.3.10 Sensor de Temperatura

Los sensores de temperatura miden la temperatura del agua para asegurar

que se mantenga dentro de un rango óptimo para su uso o procesamiento.

Los sensores de temperatura pueden ser de tipo termistor, termopar o RTD

(Detector de Temperatura de Resistencia). Los termistores cambian su

resistencia con la temperatura, mientras que los termopares generan una

pequeña tensión eléctrica en respuesta a cambios de temperatura. Los

sensores RTD utilizan cambios en la resistencia de un metal con la

temperatura [17]. La temperatura del agua puede influir en la disolución de

gases y en la velocidad de reacciones químicas, por lo que su monitoreo es

crucial para mantener las condiciones adecuadas en sistemas de tratamiento

y procesos industriales.

1.3.11 Sensor de TDS (Total de Sólidos Disueltos)

Los sensores de TDS miden la concentración total de sólidos disueltos en el

agua, lo que incluye sales, minerales y otros compuestos [18]. Estos sensores

funcionan midiendo la conductividad eléctrica del agua, ya que los sólidos

disueltos aumentan la capacidad del agua para conducir electricidad. Los

sensores de TDS suelen ser utilizados en sistemas de tratamiento de agua y

en la agricultura para evaluar la calidad del agua y ajustar los procesos de

filtración y purificación. Una alta concentración de sólidos disueltos puede

afectar la potabilidad del agua y la eficiencia de los sistemas de tratamiento,

por lo que el monitoreo constante es esencial para asegurar la calidad del

agua.

1.4 Objetivos del proyecto

1.4.1 Objetivo general

Desarrollar un software de monitoreo para medir y analizar el consumo, nivel y la calidad

del agua en tanques de los sistemas educativos de Santa Isabel y Tambo Huari, utilizando

tecnologías de Internet de las Cosas (IoT) y Machine Learning para mejorar la gestión y

seguridad del suministro de agua.

1.4.2 Objetivos específicos

● Gestión de datos y visualización del consumo del agua - Administración eficiente

en el registro de usuarios, clientes, tanques, sensores y autenticación:

Objetivo: Desarrollar un sistema integral de gestión y análisis del consumo de agua

que permita el registro y autenticación de usuarios, la gestión de clientes, sensores y

tanques , la captura y visualización en tiempo real de datos de consumo, la exportación

y análisis de datos históricos, el envío de alertas semanales por correo electrónico, y la

predicción del consumo futuro para una gestión eficiente y proactiva del recurso.

Medición del Éxito: El éxito se medirá mediante la precisión y actualización oportuna de

los datos sobre tanques, sensores,clientes y usuarios con un objetivo de 100% de

registros correctos y actualizados. Asimismo si

la exactitud de las predicciones del

consumo futuro del agua del agua, tiene una precisión del 80% o superior.

● Gestión de datos y visualización del nivel de agua:

Objetivo: Desarrollar e implementar un módulo web que registre y almacene datos de

nivel del agua provenientes de los sensores, permita a los usuarios visualizar estos

niveles en tiempo real, acceder a historiales históricos, predecir el tiempo restante

hasta el agotamiento del agua y estimar el consumo mensual en litros.

Medición del Éxito: Se considerará que el objetivo se ha logrado sí existe facilidad y

precisión con la que los usuarios pueden acceder a datos históricos de nivel del agua,

evaluada a través de encuestas de satisfacción y pruebas de funcionalidad . Asimismo

si la exactitud de las predicciones del tiempo restante hasta el agotamiento del agua,

comparada con el tiempo real hasta el agotamiento, apuntando a una tasa de precisión

del 80% o superior.

● Gestión de datos y visualización de calidad del agua:

Objetivo: Desarrollar e implementar un módulo web que registre y almacene datos

sobre los parámetros de calidad del agua; permita a los usuarios visualizar estos datos

en tiempo real y acceder a historiales históricos, y ofrezca capacidades para predecir la

calidad del agua basándose en tendencias y datos registrados.

Medición del Éxito: Se considerará que el objetivo se ha logrado sí existe facilidad y

precisión con la que los usuarios pueden acceder a datos de la calidad del agua,

evaluada a través de encuestas de satisfacción y pruebas de funcionalidad . Asimismo

si

la precisión de las predicciones sobre la calidad del agua se determinará por la

exactitud de las predicciones comparadas con los datos reales futuros, apuntando a

una tasa de precisión del 80% o superior.

II.

CONOCIMIENTOS DE INGENIERÍA APLICADOS / RELACIONADOS

2.1 Conocimiento en Matemáticas:

- Cálculo para modelar el flujo de agua, analizar tasas de cambio y optimizar

sistemas.

- Estadística para analizar datos de sensores, realizar inferencias y construir

modelos predictivos.

- Álgebra lineal para representar datos multidimensionales y aplicar técnicas

de machine learning.

- Regresión lineal será una herramienta útil en el desarrollo de un software

de monitoreo del nivel y calidad del agua en tanques, especialmente

cuando se integra con IoT y Machine Learning ya que se usará para

predecir el comportamiento del nivel y calidad del agua; y estimacion de

consumo del agua.

2.2 Conocimiento en ciencias naturales

- Sensores y parámetros de medición: Utilizar el conocimiento de química del

agua para seleccionar y calibrar los sensores adecuados para medir

parámetros como pH, turbidez y cloro. La precisión en la medición es

crucial para la efectividad del monitoreo.

-

Interpretación de datos: Aplicar principios de biología y ecología para

interpretar los datos recogidos. Por ejemplo, correlacionar variaciones en

pH con posibles fuentes de contaminación o cambios en el ecosistema

acuático.

- Modelado y predicción: Usar conocimientos de física para entender cómo

los modelos de Machine Learning deben ser ajustados para capturar el

comportamiento del agua en los tanques. Por ejemplo, cómo el flujo de

agua y las características físicas del tanque afectan las mediciones.

- Alertas y notificaciones: Desarrollar algoritmos que detecten desviaciones

en los parámetros de calidad del agua que podrían indicar problemas

ambientales, basándose en el conocimiento de la química y biología del

agua.

-

Informes y visualización: Crear interfaces que muestran datos y tendencias

en términos comprensibles, utilizando principios de física y biología para

interpretar la información de manera efectiva.

2.3 Conocimiento en Ingeniería:

- Diseño y desarrollo de software: Conocimientos en ingeniería de software

son esenciales para diseñar y desarrollar una aplicación robusta y

escalable. Esto incluye la arquitectura del software, la implementación de

algoritmos de Machine Learning, y la integración con sistemas IoT.

- Desarrollo de modelos predictivos: Aplicar técnicas de Machine Learning

para desarrollar modelos predictivos que puedan estimar el consumo de

agua, la calidad futura del agua, o detectar anomalías. Esto incluye la

selección de algoritmos adecuados, la formación de modelos y la validación

de su precisión.

III.

INGENIERO Y LA SOCIEDAD:

3.1 Justificación social:

El sistema de monitoreo de calidad y nivel de agua en tanques en tiempo

real

tiene un impacto social significativo. Contribuye directamente a

mejorar la salud pública al garantizar el acceso a agua limpia y segura. La

detección temprana de problemas en la calidad del agua permite una

intervención rápida, previniendo enfermedades transmitidas por el agua.

Además, el sistema promueve la conservación del recurso hídrico al

optimizar su uso y reducir el desperdicio, lo cual es crucial en regiones con

escasez de agua [1].

3.2 Justificación Económica:

Desde el punto de vista económico, el sistema ofrece beneficios

sustanciales. La predicción del consumo y costos permite una mejor

planificación financiera tanto para los usuarios como para las empresas de

servicios públicos. La detección temprana de fugas o problemas de calidad

reduce los costos de mantenimiento a largo plazo. Además,

la

optimización del uso del agua puede resultar en ahorros significativos en el

consumo y, por ende, en la factura del servicio [2].

3.3 Acontecimientos tecnológicos y científicos:

El proyecto se basa en avances recientes en varias áreas tecnológicas:

Internet de las Cosas (IoT): Permite la interconexión de sensores y

dispositivos para recopilar datos en tiempo real.

Ciencia de Datos: Permite extraer

insights valiosos de los datos

recopilados.

Machine Learning: Posibilita la creación de modelos predictivos para

anticipar consumo, costos y calidad del agua [3].

IV. METODOLOGÍA EMPLEADA

4.1 Metodología SCRUM

Se empleó una metodología Ágil, combinado con elementos de Scrum – planificación

previa. No se consideraron los Sprints porque teníamos una fecha límite.

Para la gestión del proyecto se utilizó el enfoque del PMI basado en la guía PMBOK,

y para el desarrollo el marco de trabajo ágil SCRUM [4].

4.1.2 Product Backlog

Se identificaron las historias de usuario según los requerimientos de cada PMV,

siendo un total de 21 historias de usuario.

Tabla N° 1. Product Backlog - SYSMONWA

ID

Iteración
(Sprint )

Título Historia de
Usuario

Historia de Usuario

HU1-2024

Sprint 01

Gestión de Usuarios (Registro
y Autenticación)

HU2-2024

Sprint 01 Gestión de Clientes

HU3-2024

Sprint 01

Gestión de Tanques y
Sensores

HU4-2024

Sprint 01

Registro de datos del
consumo de agua en tiempo
real de los sensores

Como usuario administrador necesito
gestionar la creación, autenticación y
asignación de roles de los usuarios, con la
finalidad de asegurar que solo los usuarios
autorizados puedan acceder al sistema y
realizar las acciones adecuadas según sus
permisos.

Como usuario administrador, necesito
gestionar la creación, edición y eliminación
de clientes en el sistema, con la finalidad de
mantener la información de los clientes
actualizada y asegurar que la gestión de
datos esté siempre correcta.

Como usuario administrador, necesito
gestionar la creación, edición y eliminación
de tanques y sensores en el sistema, con la
finalidad de mantener un registro
actualizado y detallado de los tanques y
sensores, lo que es crucial para la operación
y monitoreo efectivos.

Como usuario, necesito recolectar los datos
del consumo de agua en tiempo real, con la
finalidad de registrar los datos del consumo
de agua para su análisis y monitoreo.

HU5-2024

Sprint 01

Visualización de los datos del
consumo de agua en tiempo
real

Como usuario, necesito visualizar los datos
del consumo de agua en tiempo real, con la
finalidad de monitorear el consumo de agua
en tiempo real y detectar anomalías.

HU6-2024

Sprint 01

Visualización de los datos
histórico del consumo de
agua

HU7-2024

Sprint 01

Exportación de datos del
consumo del agua

HU8-2024

Sprint 01

Alertas semanales por correo
electrónico del consumo del
agua

HU9-2024

Sprint 01

Predicción del consumo de
agua

HU10-2024

Sprint 02

Registro del nivel de agua en
tiempo real

HU11-2024

Sprint 02

Visualización del nivel de
agua en tiempo real

HU12-2024

Sprint 02

Visualización de los datos
históricos del nivel de agua

HU13-2024

Sprint 02

Alertas automáticas de
niveles críticos del agua

HU14-2024

Sprint 02

Exportación de datos
históricos de nivel de agua

HU15-2024

Sprint 02

Predicción del tiempo restante
para vaciar el tanque

Como usuario, necesito consultar y
visualizar los datos históricos del consumo
de agua, con la finalidad de analizar
patrones y comparaciones del consumo de
agua en diferentes periodos.

Como usuario, necesito exportar los datos
del consumo de agua, con la finalidad de
analizar los datos externamente o generar
reportes.

Como usuario, necesito recibir alertas
semanales por correo electrónico del
consumo de agua, con la finalidad de tomar
decisiones rápidas si el consumo excede el
promedio.

Como usuario, necesito saber la predicción
del consumo de agua mensual , con la
finalidad de planificar el uso eficiente de
agua basándose en estimaciones precisas.

Como usuario, necesito recolectar los datos
del nivel de agua en tiempo real, con la
finalidad de monitorear el nivel del agua en
el tanque para evitar desbordamientos o
escasez.

Como usuario, necesito visualizar los datos
del nivel de agua en tiempo real, con la
finalidad de evitar que el tanque se llene
demasiado o se vacíe.

Como usuario, necesito consultar el historial
del nivel de agua en el tanque, con la
finalidad de analizar el comportamiento del
nivel de agua a lo largo del tiempo.

Como usuario, necesito recibir alertas
cuando el nivel del agua alcance ciertos
umbrales, con la finalidad de prevenir
desbordamientos o niveles peligrosamente
bajos.

Como usuario, necesito exportar los datos
del nivel de agua, con la finalidad de
analizarlos externamente o generar informes
de uso.

Como usuario, necesito saber en qué tiempo
se vaciará el tanque, con la finalidad de
anticipar cambios en el nivel del agua y
tomar acciones preventivas.

HU16-2024

Sprint 03

Registro de datos de calidad
del agua en tiempo real

HU17-2024

Sprint 03

Visualización de la calidad del
agua en tiempo real

HU18-2024

Sprint 03

Visualización de datos
históricos de la calidad del
agua

Como usuario, necesito recolectar datos
sobre la calidad del agua en tiempo real, con
la finalidad de asegurar que el agua cumple
con los estándares de calidad requeridos.

Como usuario, necesito visualizar los datos
de la calidad del agua en tiempo real, con la
finalidad de reaccionar rápidamente a
cualquier anomalía en los niveles de calidad.

Como usuario, necesito consultar el historial
de calidad del agua con la finalidad de
analizar la evolución de la calidad del agua a
lo largo del tiempo.

HU19-2024

Sprint 03

Alertas automáticas por
correo cuando los parámetros
de calidad estén fuera de los
límites

Como usuario, necesito recibir alertas
cuando la calidad del agua no cumpla con
los estándares, con la finalidad de tomar
acciones correctivas cuando se detecten
problemas en la calidad del agua.

HU20-2024

Sprint 03

Exportación de datos de
calidad del agua

HU21-2024

Sprint 03

Predicción de la calidad del
agua

Como usuario, necesito exportar los datos
de calidad del agua con la finalidad de
analizarlos externamente o generar informes
de calidad.

Como usuario, necesito saber la predicción
de la calidad del agua a lo largo del tiempo,
con la finalidad de anticipar problemas
potenciales en la calidad del agua y
planificar intervenciones.

4.1.3 Sprint Backlog

Cada PMV identificado se gestionó como un sprint backlog. Se utilizó MS Project para

la planificación de los cronograma, facilitando la organización del trabajo por sprint en

el monitoreo y gestión de datos del sistema de tanques y sensores.

Tabla N° 2. Sprint Backlog - SYSMONWA

ID

ID de la
Historia de
Usuario

Tiempo de entrega

PMV1

HU1-2024

HU2-2024

HU3-2024

HU4-2024

HU5-2024

HU6-2024

HU7-2024

Semana 7

HU8-2024

HU9-2024

HU10-2024

HU11-2024

HU12-2024

HU13-2024

HU14-2024

HU15-2024

HU16-2024

HU17-2024

HU18-2024

HU19-2024

HU20-2024

HU21-2024

PMV2

PMV3

Semana 12

Semana 14

• Requisitos:

Durante la fase de requisitos, el Product Owner (que podría ser el cliente o

el principal interesado en el proyecto) trabajará en identificar las

funcionalidades clave del sistema que se desean implementar,

priorizándolas según el valor que ofrecen al usuario final. Para el proyecto

de monitoreo de agua, los principales requisitos podrían ser:

- Se definieron los requisitos funcionales y no funcionales del sistema

de manera detallada.

- Se priorizaron los requisitos según su valor para el negocio y

complejidad técnica.

• Diseño:

El diseño del sistema se realiza en colaboración entre el equipo de

desarrollo, el Product Owner, y el Scrum Master, tomando en cuenta los

requerimientos funcionales y no funcionales. Algunas decisiones de diseño

claves incluyen:

- El diseño del sistema se basó en una arquitectura distribuida,

integrando sensores IoT para la recolección de datos, un sistema

centralizado en la nube para el almacenamiento y procesamiento de

datos, y aplicaciones móviles y web para la presentación y

monitoreo de la información.

- Se optó por servicios de almacenamiento y procesamiento en la

nube para garantizar escalabilidad y accesibilidad.

•

Implementación:

La ejecución de este proyecto sigue estrictamente la estructura definida,

adoptando un enfoque secuencial y lineal para el desarrollo de la

plataforma de monitoreo inteligente del agua. Cada etapa se lleva a cabo

de manera ordenada y debe completarse antes de pasar a la siguiente.

Este método asegura que el proyecto se desarrolle de forma organizada y

coherente, lo cual es crucial para su éxito.

• Pruebas:

Las pruebas desempeñan un papel crucial en el desarrollo de la plataforma

de seguimiento de monitoreo inteligente del agua . Se llevan a cabo en

diferentes fases del ciclo de vida del proyecto con el propósito de confirmar

que el sistema cumple con los requisitos establecidos y funciona de

manera adecuada. Estas pruebas son esenciales para asegurar que la

plataforma alcance los estándares de calidad y funcionalidad necesarios y

son una parte fundamental del proceso de desarrollo.

4.2 Metodologia Cascada

Aunque el proyecto se desarrolló principalmente con metodología ágil, se

incorporaron algunos elementos de la metodología en cascada para ciertas fases del

proyecto, especialmente en la planificación inicial y la documentación final [5].

La metodología en cascada es un enfoque tradicional para la gestión y desarrollo de

proyectos que sigue un proceso secuencial y estructurado, donde cada fase debe

completarse antes de que la siguiente pueda comenzar. En el contexto del proyecto

de monitoreo del nivel y calidad del agua en tanques, la metodología en cascada

puede implementarse de la siguiente manera [5]:

● Requisitos

En esta fase inicial, se realiza un análisis exhaustivo para definir

qué es lo que necesita el sistema. El objetivo es obtener una

comprensión clara de los requisitos funcionales y no funcionales del

proyecto. En el caso del sistema de monitoreo de agua:

Requisitos funcionales:

- Monitorear el nivel del agua en tiempo real.

- Medir y analizar

la calidad del agua (pH,

turbidez,

temperatura, TDS).

- Enviar alertas automáticas cuando la calidad del agua esté

fuera de los parámetros normales o cuando el tanque esté

lleno.

- Almacenar los datos en la nube (como Firebase) para su

acceso desde aplicaciones móviles y web.

- Proporcionar informes y métricas sobre el consumo de agua,

el costo por litro y otros indicadores clave.

-

Implementar un sistema de predicción de consumo y calidad

utilizando machine learning.

Requisitos no funcionales:

- El sistema debe ser escalable para permitir la integración

con más tanques.

- El sistema debe tener una alta disponibilidad, minimizando el

tiempo de inactividad.

-

La interfaz de usuario debe ser intuitiva y fácil de usar, tanto

en la aplicación móvil como en la web.

- Compatibilidad con diferentes tipos de sensores para medir

las variables necesarias (pH, turbidez, TDS, temperatura,

etc.).

● Diseño

Una vez definidos los requisitos, se procede a la fase de diseño,

donde se crea la arquitectura del sistema y los diagramas

necesarios para su construcción.

Diseño del sistema de monitoreo de agua:

Diseño de hardware:

● Se seleccionarán los sensores que medirán las métricas de

calidad del agua (pH, turbidez, TDS, temperatura).

● Se elegirá el microcontrolador, como el ESP32 con

capacidad Wi-Fi, para integrar los sensores y enviar los

datos a la nube.

● Se planificarán los esquemas de conexión de los sensores al

microcontrolador y su instalación en el tanque de agua.

Diseño de software:

● Se definirá la arquitectura del software, dividiendo el sistema

en componentes (aplicación móvil, servidor web, bases de

datos en la nube, etc.).

● Se diseñará la base de datos en Firebase o cualquier otra

plataforma, asegurando que puede almacenar y organizar

los datos de monitoreo en tiempo real.

● Se crearán los diagramas UML para la estructura de clases,

relaciones entre componentes y secuencia de eventos.

Diseño de la interfaz de usuario (UI):

Se esbozan los prototipos de la interfaz gráfica,

tanto para la

aplicación móvil como para la web, considerando que la interfaz

permite:

● Ver los datos del nivel y calidad del agua.

● Recibir alertas en tiempo real.

● Acceder a informes históricos y predicciones basadas en

machine learning.

● Implementación

La aplicación de la metodología en cascada implica el uso de un

enfoque secuencial y lineal para el desarrollo de proyectos. Este

método sigue una estructura estricta, donde cada etapa del

proyecto se realiza en orden y debe ser completada antes de pasar

a la siguiente.

● Pruebas

En la metodología en cascada, las pruebas son fundamentales para

asegurar la calidad del software. Se realizan en varias fases a lo

largo del ciclo de vida del proyecto, con el propósito de confirmar

que el sistema cumple con los requisitos establecidos y opera de

manera adecuada.

4.2.1 Aportes/Descubrimientos:

PMV1

HU1-2024: Gestión de Usuarios (Registro y Autenticación)

Descubrimiento: El sistema necesita manejar la creación y autenticación de

usuarios. Esto incluye el registro de nuevos usuarios, el inicio de sesión y la

gestión de roles para garantizar que los usuarios puedan acceder a las

funcionalidades adecuadas según sus permisos.

Aporte: Facilita la incorporación de nuevos usuarios al sistema y asegura que

solo usuarios autorizados puedan acceder a funciones específicas. Además,

proporciona una base para el control de acceso y la administración de

permisos, lo cual es crucial para mantener la seguridad y la integridad del

sistema.

HU2-2024: Gestión de Clientes

Descubrimiento: El sistema debe permitir la creación, edición y eliminación

de clientes. Además, debe proporcionar la capacidad para gestionar la

información asociada a cada cliente, asegurando que los datos estén

actualizados y sean accesibles para la administración del sistema.

Aporte: Permite una administración eficiente de la información de los

clientes, facilitando la gestión y el mantenimiento de datos importantes. Esto

ayuda a asegurar que los clientes estén correctamente registrados y que su

información esté siempre disponible para futuras consultas o acciones.

HU3-2024: Gestión de Tanques y Sensores

Descubrimiento: El sistema debe gestionar la creación, edición y eliminación

de tanques y sensores. Debe proporcionar una forma de mantener un

registro detallado y actualizado de cada tanque y sensor, incluyendo

información relevante como ubicación, tipo y estado.

Aporte: Facilita la administración y supervisión de los tanques y sensores,

permitiendo una gestión eficaz de los recursos y asegurando que la

información crítica esté actualizada. Esto es fundamental para el monitoreo

preciso y la operación efectiva del sistema de gestión de agua.

HU4-2024: Registro de datos del consumo de agua en tiempo real de los

sensores

Descubrimiento: El sistema debe registrar y almacenar datos del consumo

del agua provenientes de sensores.

Aporte: Esta funcionalidad asegura que el usuario tenga acceso inmediato a

la información sobre el consumo de agua, lo que permite un control eficiente

del recurso.

HU5-2024: Visualización de los datos del consumo de agua en tiempo real

Descubrimiento: El sistema debe permitir visualizar los datos del consumo de

agua en tiempo real.

Aporte: Esta funcionalidad permite que el usuario pueda monitorear el

consumo actual y detectar cualquier anomalía o cambio inmediato.

HU6-2024: Visualización de los datos histórico del consumo de agua

Descubrimiento: El sistema debe permitir consultar y visualizar datos

históricos del consumo de agua

Aporte: Esta funcionalidad permite que el usuario pueda analizar el consumo

pasado y realizar comparaciones a lo largo del tiempo.

HU7-2024: Exportación de datos del consumo del agua

Descubrimiento: El sistema debe permitir exportar los datos del consumo de

agua.

Aporte: Esta funcionalidad permite que el usuario pueda monitorear el

consumo actual y analizarlos externamente en herramientas como hojas de

cálculo o informes.

HU8-2024: Alertas semanales por correo electrónico del consumo del agua

Descubrimiento: Los usuarios deben recibir alertas automáticas cuando se

excede al consumo promedio.

Aporte: Mejora la capacidad de respuesta del usuario al enviar notificaciones

inmediatas que le permiten actuar y reducir el consumo del agua,

HU9-2024: Predicción del consumo de agua

Descubrimiento: El sistema debe ser capaz de predecir el consumo de agua

por mes utilizando machine learning, brindando así estimaciones precisas

para la planificación.

Aporte: Proporciona una funcionalidad avanzada que optimiza la gestión de

recursos hídricos, mejorando la eficiencia del consumo de agua.

PMV2

HU10-2024: Registro del nivel de agua en tiempo real

Descubrimiento: El sistema debe registrar el nivel de agua en

tiempo real, utilizando sensores de nivel.

Aporte: Proporciona al usuario información precisa sobre la

capacidad actual del tanque, ayudando a prevenir desbordamientos

o niveles bajos.

HU11-2024: Visualización del nivel de agua en tiempo real

Descubrimiento: El sistema debe permitir visualizar el nivel de agua

en tiempo real desde una interfaz web.

Aporte: Facilita el monitoreo remoto del nivel del tanque,

permitiendo que el usuario controle el estado del agua sin necesidad

de presencia física.

HU12-2024: Visualización de los datos históricos del nivel de agua

Descubrimiento: El sistema debe permitir al usuario acceder y

visualizar datos históricos del nivel de agua.

Aporte: Proporciona una visión a largo plazo del comportamiento del

nivel del tanque, útil para la toma de decisiones informadas sobre la

gestión del recurso.

HU13-2024: Alertas automáticas de niveles críticos del agua

Descubrimiento: Los usuarios deben recibir alertas automáticas

cuando el nivel del agua alcanza puntos críticos, ya sea por

sobrellenado o niveles bajos.

Aporte: Ayuda a prevenir problemas como el desbordamiento o la

falta de agua, permitiendo una intervención oportuna.

HU14-2024: Exportación de datos históricos de nivel de agua

Descubrimiento: El sistema debe permitir exportar datos históricos

del nivel de agua para su análisis externo.

Aporte: Facilita el análisis detallado de los niveles a lo largo del

tiempo y permite su uso en informes o herramientas de análisis

externas.

HU15-2024: Predicción del tiempo restante para vaciar el tanque

Descubrimiento: El sistema debe predecir cuánto tiempo falta para

que el tanque se vacíe, basado en el consumo actual y el nivel de

agua.

Aporte: Optimiza la planificación de recursos hídricos, evitando

interrupciones en el suministro y anticipando la necesidad de

rellenar el tanque.

PMV 3

HU16-2024: Registro de datos de calidad del agua en tiempo real

Descubrimiento: El sistema debe registrar los parámetros de calidad del

agua (pH, turbidez, temperatura) en tiempo real.

Aporte: Proporciona información crucial sobre la calidad del agua

disponible, asegurando que esté dentro de los estándares de seguridad

y consumo.

HU17-2024: Visualización de la calidad del agua en tiempo real

Descubrimiento: El sistema debe permitir visualizar los datos de calidad

del agua en tiempo real desde una interfaz web.

Aporte: Facilita la supervisión continua de la calidad del agua,

permitiendo al usuario tomar decisiones inmediatas si los parámetros

están fuera de los límites.

HU18-2024: Visualización de datos históricos de la calidad del agua

Descubrimiento: El sistema debe permitir la consulta de datos históricos

sobre la calidad del agua.

Aporte: Ayuda a detectar patrones de deterioro o mejora en la calidad

del agua a lo largo del tiempo, permitiendo acciones correctivas basadas

en análisis históricos.

HU19-2024: Alertas automáticas por correo cuando los parámetros de

calidad estén fuera de los límites

Descubrimiento: El sistema debe enviar alertas automáticas por correo

electrónico cuando la calidad del agua esté fuera de los parámetros

normales.

Aporte: Permite una intervención rápida para evitar el uso de agua de

mala calidad, garantizando la seguridad del recurso hídrico.

HU20-2024: Exportación de datos de calidad del agua

Descubrimiento: El sistema debe permitir la exportación de datos de

calidad del agua para su análisis externo.

Aporte: Proporciona al usuario la capacidad de analizar los datos en

herramientas avanzadas y de presentar informes detallados sobre la

calidad del agua.

HU21-2024: Predicción de la calidad del agua

Descubrimiento: El sistema debe predecir la calidad futura del agua

basándose en los datos históricos y en modelos de machine learning.

Aporte: Proporciona la capacidad de prever cambios en la calidad del

agua, lo que permite tomar medidas preventivas para evitar su deterioro.

V.

USO DE HERRAMIENTAS MODERNAS

5.1 Framework: Laravel

Laravel es un framework de desarrollo web en PHP que se destaca por su sintaxis
elegante y su enfoque en la facilidad de uso. Basado en el patrón
(MVC), Laravel proporciona una estructura clara y
Modelo-Vista-Controlador
organizada que facilita el desarrollo de aplicaciones web robustas y mantenibles.
Ofrece características avanzadas como enrutamiento intuitivo, autenticación
simplificada y migraciones de bases de datos, lo que permite a los desarrolladores
construir aplicaciones de manera eficiente. Su ecosistema incluye herramientas
como Eloquent ORM para la gestión de bases de datos y Blade para el
renderizado de vistas, mejorando la productividad y escalabilidad de las
aplicaciones.

Figura 1. Uso de Laravel en SYSMONWA

Elaboración propia.

5.2 Lenguaje: PHP

PHP es un lenguaje de programación del lado del servidor ampliamente utilizado
para el desarrollo web. Su capacidad para integrarse fácilmente con bases de
datos, su sintaxis flexible y su amplia comunidad de desarrolladores lo han
convertido en una opción popular para aplicaciones web dinámicas. PHP es
conocido por su compatibilidad con diversos sistemas de gestión de bases de
datos y su capacidad para generar contenido web dinámico en tiempo real.
Laravel, como uno de los frameworks más populares para PHP, aprovecha las
capacidades del lenguaje para ofrecer una plataforma robusta y eficiente para el
desarrollo de aplicaciones.

Figura 2. Uso de PHP en SYSMONWA

Elaboración propia.

5.3 Base de datos: MySQL

MySQL es un sistema de gestión de bases de datos relacional de código abierto
que es conocido por su fiabilidad, rendimiento y escalabilidad. Utiliza SQL para la
gestión de datos, permitiendo realizar operaciones eficientes de almacenamiento y
consulta de información. La integración de MySQL con Laravel, facilitada por
Eloquent ORM, simplifica la gestión de datos y mejora la eficiencia en el desarrollo
de aplicaciones web al proporcionar una capa de abstracción para interactuar con
la base de datos.

Figura 3. Uso de MSQL en SYSMONWA

Elaboración propia.

5.4 Herramienta de Machine Learning: Google Colab

Google Colab es una herramienta basada en la nube que proporciona un entorno
interactivo para el desarrollo y ejecución de modelos de Machine Learning. Colab
ofrece soporte para Python y bibliotecas populares como TensorFlow, Keras y
PyTorch,
facilitando la implementación y el entrenamiento de modelos de
aprendizaje automático sin necesidad de configuraciones complejas. Su
integración con Google Drive permite almacenar y compartir proyectos fácilmente,
y su capacidad para utilizar GPUs y TPUs acelera el proceso de entrenamiento de
modelos, haciendo que Colab sea una herramienta valiosa para la investigación y
desarrollo en Machine Learning.

Figura 4. Uso de Google Collab en SYSMONWA

Elaboración propia.

5.5 Servidor web: Apache http

Apache HTTP es un servidor web de código abierto que proporciona un entorno
confiable para servir aplicaciones web. Conocido por su estabilidad y flexibilidad,
Apache maneja eficientemente las solicitudes de los usuarios y puede ser
configurado para soportar una amplia gama de módulos y funcionalidades. Su uso
es común en entornos de producción para ejecutar aplicaciones web construidas
con frameworks como Laravel, garantizando un rendimiento óptimo y una gestión
efectiva de las comunicaciones entre el servidor y los clientes.

Figura 5. Uso de Apache en SYSMONWA

Elaboración propia.

5.6 XAMPP:
XAMPP es un paquete de software libre que combina Apache, PHP y MySQL en
un solo entorno de desarrollo. Proporciona una solución fácil de instalar y
configurar para crear un entorno de desarrollo local que simula un servidor en
producción. XAMPP permite a los desarrolladores construir, probar y depurar
aplicaciones web en un entorno controlado antes de su despliegue en un entorno
real,
facilitando el proceso de desarrollo y asegurando que las aplicaciones
funcionen correctamente antes de ser publicadas.

Figura 6. Uso de XAMP en SYSMONWA

Elaboración propia.

5.7 Proveedor de Hosting: AlwaysData

AlwaysData es un proveedor de servicios de alojamiento web que ofrece
soluciones confiables y escalables para aplicaciones web. Con soporte para una
variedad de tecnologías, incluyendo PHP y bases de datos MySQL, AlwaysData
proporciona un entorno seguro y de alto rendimiento para el despliegue de
aplicaciones. Su infraestructura permite gestionar aplicaciones web y bases de
datos con alta disponibilidad, y su enfoque en la seguridad y el soporte técnico
asegura una operación continua y eficiente.

Figura 7. Uso de AlwaysData en SYSMONWA

Elaboración propia.

5.8 Control de Versiones: Git

Git es un sistema de control de versiones distribuido que permite gestionar el
código fuente de manera efectiva. Git
facilita el seguimiento de cambios, la
colaboración en equipo y la integración de múltiples versiones del código mediante
ramas y fusiones. El uso de Git en plataformas como GitHub, GitLab o Bitbucket
mejora la gestión del desarrollo del software, proporcionando una herramienta
clave para la colaboración y el mantenimiento del código.

Figura 8. Uso de PHP en SYSMONWA

Elaboración propia.

5.9 Placa de Hardware: ESP32

El ESP32 es una placa de hardware de bajo costo que integra Wi-Fi y Bluetooth,
adecuada para aplicaciones de Internet de las Cosas (IoT). Su capacidad para
conectar sensores y dispositivos inalámbricos permite la recolección de datos en
tiempo real y su transmisión a aplicaciones web para análisis y procesamiento. La
integración del ESP32 con Laravel facilita la creación de soluciones avanzadas
que combinan hardware y software para ofrecer funcionalidades innovadoras.

Figura 9. Uso de PHP en SYSMONWA

Elaboración propia.

VI.

DISEÑO DE INGENIERÍA

VI.1

Listado de Requerimientos funcionales

Tabla N° 3. Cuadro de Línea de tiempo y PMV

PMV

Meta

Valor

Tipo de Requerimiento

Requerimiento/Funcionali
dad

0

Elaborar Plan

Tener guia de trabajo

No aplica

No aplica

Desarrollo web para
el registro de datos,
visualización y
predicción del
consumo del agua

1

Desarrollo web para
el registro de
usuarios, clientes,
tanques, sensores y
login

El sistema debe registrar y
almacenar datos del
consumo de agua de
sensores, permitiendo a los
usuarios visualizar estos
datos en tiempo real y
consultar históricos.
Además, debe ofrecer
capacidades predictivas
para estimar el consumo
futuro de agua basándose
en datos históricos y
patrones de uso.

El sistema debe ofrecer una
plataforma integral para la
gestión eficiente de tanques
y sensores, permitiendo el
registro detallado y la
actualización de la
información relevante sobre
cada tanque y sensor. Debe

Requerimiento Funcional

Requerimiento Funcional

Requerimiento Machine
Learning

Requerimiento Funcional

El sistema debe registrar y
almacenar datos del
consumo del agua
provenientes de sensores.

Los usuarios deben poder
visualizar los datos del
consumo del agua en
tiempo real y en historiales
históricos.

El sistema debe predecir el
consumo futuro de agua
basado en datos históricos
y patrones de uso.

El sistema debe permitir el
registro y gestión de
información sobre los
tanques, incluyendo
nombre, ubicación,
capacidad máxima, tipo, y
fecha de instalación.

Requerimient
o No
Funcionales

- Eficiencia:
Optimizar el
sistema para
garantizar un
procesamiento
rápido y
eficiente de los
datos,
minimizando
tiempos de
respuesta y
consumo de
recursos.
- Escalabilidad:
Diseñar el
sistema de
manera que
pueda escalar
fácilmente
para manejar
un mayor
volumen de
datos en el
futuro.

Hito

Tiempo de
desarrollo

10/09

19/08 - 10/09

08/10

16/09 - 08/10

incluir mecanismos robustos
de autenticación y
autorización para garantizar
que solo usuarios
autorizados puedan acceder
y modificar datos
específicos, así como
funcionalidades para
registrar, modificar y
eliminar usuarios y clientes.

Desarrollo web para
el registro de datos
y visualización del
nivel de agua

El sistema debe registrar y
almacenar datos de nivel del
agua de los sensores,
permitiendo a los usuarios
visualizar estos niveles en
tiempo real y acceder a
historiales históricos.
Además, debe incluir
funcionalidades para
predecir el tiempo restante
hasta el agotamiento del
agua y estimar el consumo
mensual en litros.

Requerimiento Funcional

Requerimiento Funcional

Requerimiento Funcional

Requerimiento Funcional

Requerimiento Funcional

Requerimiento Funcional

El sistema debe permitir el
registro de sensores,
incluyendo tipo, modelo,
fecha de instalación y
estado.

El sistema debe tener
mecanismos de
autenticación y
autorización para asegurar
que solo usuarios
autorizados puedan
acceder a funcionalidades
específicas

El sistema debe permitir
registrar usuarios en el
sistema

El sistema debe permitir
clientes.

El sistema debe registrar y
almacenar datos de nivel
del agua provenientes de
sensores.

Los usuarios deben poder
visualizar los niveles de
agua en tiempo real y en
historiales históricos.

Requerimiento Machine
Learning

Predicción de cuánto
tiempo durará el agua

Desarrollo web y
móvil para el
registro de datos y
visualización de la

El sistema debe registrar y
almacenar datos sobre los
parámetros de calidad del
agua, incluyendo pH,

Requerimiento Funcional

El sistema debe registrar y
almacenar datos sobre los
parámetros de calidad del
agua, como pH, turbidez y

- Fiabilidad:
Garantizar la
fiabilidad del
sistema para
que los datos
recolectados y
procesados
sean precisos y
confiables.
- Seguridad:
Implementar
medidas de
seguridad para
proteger los
datos
recolectados y
procesados
de accesos no
autorizados.
Precisión:
Garantizar
la precisión de
las
predicciones
generadas por
los modelos,
minimizando
el margen de
error.
- Rendimiento:
Optimizar el
rendimiento
del sistema
para que
pueda
generar
predicciones

2

3

05/11

14/10 - 05/11

03/12

11/11 - 03/12

calidad de agua

turbidez y cloro, y permitir a
los usuarios visualizar estos
datos en tiempo real así
como en historiales
históricos. Además, debe
ofrecer capacidades para
predecir la calidad del agua
en función de las tendencias
y datos registrados.

Requerimiento Funcional

cloro.

Los usuarios deben poder
visualizar los datos de
calidad del agua en tiempo
real y en historiales
históricos.

Requerimiento Machine
Learning

Predicción de calidad de
agua

en
tiempo real o
en intervalos
regulares
según sea
necesario.
-
Interpretabilida
d:
Diseñar los
modelos de
predicción de
manera que
sean
fácilmente
interpretables
por los
usuarios,
incluso
aquellos
sin experiencia
en Machine
Learning.

Cuadros de criterios de aceptación por Historia de Usuario.

PMV1

Tabla N° 4. Cuadro de criterios de aceptación HU1 - 2024 Gestión de usuarios

Tabla N° 5. Cuadro de criterios de aceptación HU2 - 2024 Gestión de clientes

Tabla N° 6. Cuadro de criterios de aceptación HU3 - 2024 Gestión de tanques y

sensores

Tabla N° 6. Cuadro de criterios de aceptación HU4 - 2024 Registro de datos del

consumo de agua en tiempo real de los sensores

Tabla N° 7. Cuadro de criterios de aceptación HU5 - 2024 Visualización de los

datos del consumo de agua en tiempo real

Tabla N° 8. Cuadro de criterios de aceptación HU6 - 2024 Visualización de los

datos histórico del consumo de agua

Tabla N° 9. Cuadro de criterios de aceptación HU7 - 2024 Exportación de datos

del consumo del agua

Tabla N° 10. Cuadro de criterios de aceptación HU8 - 2024 Alertas semanales

por correo electrónico del consumo del agua

Tabla N° 11. Cuadro de criterios de aceptación HU9 - 2024 Predicción del

consumo de agua

Tabla N° 12. Cuadro de criterios de aceptación HU10 - 2024 Registro del nivel de

agua en tiempo real

Tabla N° 13. Cuadro de criterios de aceptación HU11 - 2024 Visualización del

nivel de agua en tiempo real

Tabla N° 14. Cuadro de criterios de aceptación HU12 - 2024 Visualización de los

datos históricos del nivel de agua

Tabla N° 15. Cuadro de criterios de aceptación HU13 - 2024 Visualización de los

datos históricos del nivel de agua

Tabla N° 16. Cuadro de criterios de aceptación HU14 - 2024 Exportación de

datos históricos de nivel de agua

Tabla N° 17. Cuadro de criterios de aceptación HU15 - 2024 Predicción del

tiempo restante para vaciar el tanque

Tabla N° 18. Cuadro de criterios de aceptación HU16 - 2024 Registro de datos

de calidad del agua en tiempo real

Tabla N° 19. Cuadro de criterios de aceptación HU17 - 2024 Visualización de la

calidad del agua en tiempo real

Tabla N° 20. Cuadro de criterios de aceptación HU18 - 2024 Visualización de

datos históricos de la calidad del agua

Tabla N° 21. Cuadro de criterios de aceptación HU19 - 2024 Alertas automáticas

por correo cuando los parámetros de calidad estén fuera de los límites

Tabla N° 22. Cuadro de criterios de aceptación HU20 - 2024 Exportación de

datos de calidad del agua

Tabla N° 23. Cuadro de criterios de aceptación HU21 - 2024 Predicción de la

calidad del agua

CUADRO DE ML

Tabla N° 24. Cuadro de Machine Learning

Caso de uso de
ML

Tipo de motor

Tipo de ML

Modelo

Algoritmo

Técnica de
aprendizaje
del modelo

Requerimie
nto
funcional

Requerimie
nto no
funcional

Fuente de
datos

¿Cómo puedo
predecir el nivel
de agua?

Motor de
predicción

Supervisado Regresión

Motor de
predicción

Supervisado Regresión

Motor de
predicción

Supervisado Clasificación

/Regresión

¿Cómo puedo
predecir el
consumo de
agua?

¿Cómo puedo
predecir la calidad
del agua (turbidez,
pH, TDS,
temperatura)?

Random
Forest

Random
Forest

Algoritmo de
Random
Forest

Algoritmo de
Random
Forest

Árbol de
Decisión /
Red
Neuronal

Algoritmo de
Árbol de
Decisión /
Red
Neuronal

Predecir el
nivel futuro
del agua en
tanques

Estimar el
consumo de
agua
basado en
patrones
históricos

Predecir
valores de
calidad del
agua y
detectar
anomalías

Tiempo de
respuesta
rápido

Alta
precisión en
las
predicciones

Interfaz de
usuario
intuitiva

Datos
históricos de
niveles de
agua

Datos
históricos de
consumo de
agua,
patrones
estacionales

Datos de
sensores
sobre
turbidez,
pH, TDS,
temperatura

Diseño y prototipado

PMV1. Administración de datos / Gestión y visualización del consumo del agua

1. Prototipo de Gestión de Usuarios (Registro y Autenticación)

Figura 10. Prototipos Gestión de usuarios

Elaboración propia.

Inicio de Sesión

2. Gestión de de Usuario

3. Registro de Usuario

4. Actualizacion de Usuario

5. Eliminación de usuario

Prototipo de Gestión de Clientes

Figura 11. Prototipos de Gestión de clientes

1. Gestión de clientes

2. Registro de clientes

3. Actualización de cliente

4. Eliminación de cliente

Prototipo de Gestión de Tanques y Sensores

Figura 12. Prototipos de Gestión de tanques y sensores

1. Gestión de Tanques

2. Registro de tanques

3. Actualización de tanques

4. Eliminación de tanques

5. Gestión de sensores

6. Registro de sensores

7. Actualización de sensores

8. Eliminación de sensores

Prototipo de Registro de datos del consumo de agua en tiempo real de los

sensores

Figura 13. Prototipo de Registro de datos en tiempo real

Prototipo de Visualización de los datos del consumo de agua en tiempo real

Figura 14. Prototipos de Visualización de datos del consumo del agua en tiempo real

Prototipo de Visualización de los datos histórico del consumo de agua

Figura 15. Prototipo de Visualización de datos del consumo del agua historico

Prototipo de Exportación de datos del consumo del agua

Figura 16. Prototipo de Visualización de datos del consumo del agua en tiempo real

Prototipo de Alertas semanales por correo electrónico del consumo del agua

Figura 17. Prototipo de Alerta Semanal de consumo de agua

Prototipo de Predicción del consumo de agua

Figura 18. Prototipo de Predicción del consumo del agua

PMV2. Gestión y visualización del nivel del agua

Visualización de los datos del Nivel de agua en tiempo real

Figura 19. Prototipo de Visualización de datos del nivel del agua en tiempo real

Visualización de los datos histórico del nivel de agua

Figura 20 . Prototipo de Visualización de datos del nivel del agua historico

Alertas automáticas de niveles críticos del agua

Figura 21. Prototipo de Alerta de nivel del agua

Exportación de datos del Nivel del agua

Figura 22 Prototipo de Exportación de datos de nivel del agua

Predicción del tiempo restante para vaciar el tanque

Figura 23. Prototipo de Predicción del tiempo restante para vaciar el tanque

PM3 :

Prototipo de Visualización de los datos de la calidad del agua en tiempo real

Figura 24. Prototipo de Visualización de datos de la calidad del agua en tiempo real

Prototipo de Visualización de los datos históricos de la calidad del agua

Figura 25. Prototipo de Visualización de datos de la calidad del agua historico

Prototipo de Exportación y Predicción de la calidad del agua

Figura 26. Prototipo de Exportación y predicción de la calidad del agua

Flujo de Pantallas de los prototipos

Figura 27. Flujo de pantallas de prototipos

Diseño de base de datos:

A continuación se puede visualizar el diseño de la base de datos realizado en

MySQL.

Figura 28. Base de datos SYSMONWA

VI.2

Arquitectura de la solución planteada

Figura 29. Arquitectura de solución elaborada en Archimate.

Elaboración propia.

Esta arquitectura ArchiMate representa un sistema web de monitoreo del consumo, nivel y

calidad del agua. Se compone de cuatro capas principales:

1. Capa de Negocio: Define los procesos principales del sistema, incluyendo la

gestión de consumo, monitoreo de calidad y control de nivel de agua.

2. Capa de Aplicación: Contiene los componentes de software que implementan las

funcionalidades del negocio, como la aplicación web de monitoreo, el servicio de

análisis de datos y el sistema de alertas.

3. Capa de Tecnología: Representa la infraestructura tecnológica que soporta las

aplicaciones, incluyendo servidores web, aplicaciones y bases de datos.

4. Capa Física: Incluye los dispositivos físicos como sensores de consumo, calidad y

nivel de agua que recopilan datos del mundo real.

Los componentes están interconectados para mostrar cómo los datos fluyen desde los

sensores físicos hasta las aplicaciones de monitoreo y análisis, y cómo estas aplicaciones

se apoyan en la infraestructura tecnológica para proporcionar servicios a los procesos de

negocio.

A continuación se presentará también la arquitectura de aplicación que se

encuentra relacionada con la arquitectura de solución planteada.

Figura 30. Arquitectura de aplicación. Elaboración propia.

Por otro lado, se diseñó una arquitectura detallada para la integración con machine

learning , mostrando como es la interacción entre el Frontend, Backend, base de datos .

Figura 30. Arquitectura de integración de machine learning con la aplicación. Elaboración propia.

VI.3

Código de la aplicación por capas

Repositorio en GitHub:

https://github.com/i1920929/sysmonwa/

Código por capas:

Modelo

Vista

Controlador

VII.

GESTIÓN DEL PROYECTO

7.1 LÍNEA BASE

Proyecto: Desarrollo de un software de consumo, monitoreo del nivel y calidad del agua en tanques de sistema educativos
(Santa Isabel y Tambo Huari) integrando IoT y Machine Learning
MVP1: Administración de datos y gestión del consumo del agua
MVP2: Gestión del nivel del agua
MVP3: Gestión de la calidad del agua

EDT

Figura 31. Diagrama de EDT. Elaboración propia.

Figura 32. Gestión del proyecto, elaborado en Monday.
Elaboración propia.

Tabla 1. Diagrama de Gantt base.
Elaboración propia.

7.2 DIAGRAMA GANTT EJECUTADO

Tabla 2. Diagrama de Gantt ejecutado.
Elaboración propia.

ENLACE:

https://drive.google.com/file/d/1VeJezbylCmBDKzzxYwgl0WLQonWkPLfk/view?usp=shari

ng

VIII.

Tablero Scrum – Kanban

Figura 2. Tablero Scrum elaborado en Trello.

Elaboración propia.

Repositorio del Tablero Scrum:

https://trello.com/invite/b/670d8b39ed9ae277440301dd/ATTIffd8d924bf95a5ad066fd

877f8eaece2AB8954AF/tablero-kanban-scrum-sysmonwa-3

IX.

PRUEBAS Y RESULTADOS Y DISCUSIÓN

Tabla N° 25. Prueba , resultado y discusión del PMV1.

Elaboración propia.

PRUEBAS EN EL PMV 1

Historia de Usuario - Gestión de Usuarios (Registro y Autenticación)

Código: HU1-2024

Como usuario administrador necesito gestionar la
creación, autenticación y asignación de roles de
los usuarios, con la finalidad de asegurar que solo
los usuarios autorizados puedan acceder al
sistema y realizar las acciones adecuadas según
sus permisos.

Resultados:

-
-
-
-
-
-
-

Validación correcta de usuario y contraseña.
Funcionamiento correcto de logueo de usuarios.
Vista correcta de gestión de usuarios.
Vista y funcionalidad correcta de la creación de usuarios
Vista y funcionalidad correcta de la actualización de usuarios.
Vista y funcionalidad correcta de la visualización de usuarios.
Funcionalidad correcta de eliminación de usuarios.

Discusión: La gestión de usuarios es un componente crítico para la seguridad y la integridad
del sistema. La implementación exitosa de la creación, autenticación y asignación de roles
asegura que solo los usuarios autorizados tengan acceso a las funciones pertinentes. La
validación correcta de usuario y contraseña y el logueo sin problemas son aspectos positivos
que reflejan un sistema robusto. Sin embargo, se pueden identificar áreas de mejora. Por
ejemplo, la incorporación de un sistema de recuperación de contraseña y autenticación de
dos factores aumentaría la seguridad, protegiendo aún más el acceso al sistema. También
sería útil
lo que
permitiría una mejor supervisión de actividades y la identificación de comportamientos
inusuales. Además, la interfaz podría beneficiarse de una mejor usabilidad, facilitando la
gestión de usuarios y sus roles de manera más intuitiva.

incluir funciones de auditoría que registren acciones de los usuarios,

Historia de Usuario - Gestión de Clientes

Código: HU2-2024

Como usuario administrador, necesito gestionar la
creación, edición y eliminación de clientes en el
sistema, con la finalidad de mantener la
información de los clientes actualizada y asegurar
que la gestión de datos esté siempre correcta.

Resultados:

-
-
-
-
-

Vista correcta de gestión de clientes.
Vista y funcionalidad correcta de la creación de clientes
Vista y funcionalidad correcta de la actualización de clientes.
Vista y funcionalidad correcta de la visualización de clientes.
Funcionalidad correcta de eliminación de clientes.

Discusión:
La historia de usuario enfatiza la necesidad de que los administradores tengan herramientas
efectivas para gestionar la información de los clientes. Se sugiere implementar un registro de
cambios para rastrear las modificaciones realizadas, aumentando así la transparencia y la
seguridad en la administración de datos. Esto no solo optimizaría la gestión, sino que
también podría contribuir a una experiencia más confiable para los usuarios.

Historia de Usuario - Gestión de Tanques y Sensores

Código: HU3-2024

Como usuario administrador, necesito gestionar la
creación, edición y eliminación de tanques y
sensores en el sistema, con la finalidad de

mantener un registro actualizado y detallado de los
tanques y sensores, lo que es crucial para la
operación y monitoreo efectivos.

Resultados:

-
-
-
-
-
-
-
-
-
-

Vista correcta de gestión de tanques.
Vista y funcionalidad correcta de la creación de tanques
Vista y funcionalidad correcta de la actualización de tanques.
Vista y funcionalidad correcta de la visualización de tanques.
Funcionalidad correcta de eliminación de tanques.
Vista correcta de gestión de sensores.
Vista y funcionalidad correcta de la creación de sensores
Vista y funcionalidad correcta de la actualización de sensores.
Vista y funcionalidad correcta de la visualización de sensores.
Funcionalidad correcta de eliminación de sensores.

Discusión:
Se podría mejorar la funcionalidad al incluir características de automatización que notifique al
administrador sobre el mantenimiento necesario o las anomalías detectadas en los sensores.
Además, sería beneficioso implementar una interfaz más intuitiva que facilite la visualización
de la información de cada tanque y sensor, permitiendo así una gestión más rápida y

efectiva. Estas mejoras no sólo optimizarán la operación, sino que también garantizarían un
monitoreo más efectivo de los recursos.

Historia de Usuario - Registro de datos del consumo de agua en tiempo real de los
sensores

Código: HU4-2024

Como usuario, necesito recolectar los datos del
consumo de agua en tiempo real, con la finalidad
de registrar los datos del consumo de agua para
su análisis y monitoreo.

Resultados:

- Desarrollo exitoso del prototipo del consumo del agua implementando el sensor de
flujo de agua.
- Conexión exitosa a Wi-Fi para envío de datos al servidor.
- Envío éxito a la base de datos con un rango de 2s desde el ESPS32.

Discusión:
La implementación del sistema para recolectar datos de consumo de agua en tiempo real ha
sido exitosa, evidenciada por la integración efectiva del sensor de flujo y la conexión Wi-Fi,

logrando un envío de datos en un tiempo óptimo de 2 segundos. Sin embargo, se debe
prestar atención a la escalabilidad del sistema, especialmente al manejar múltiples sensores
simultáneamente, para garantizar un rendimiento consistente. Además, es crucial establecer
mecanismos de validación de datos para prevenir errores en la base de datos, como
implementar alertas para lecturas anómalas. Estas mejoras no solo incrementarían la
fiabilidad del sistema, sino que también optimizarían la gestión del recurso hídrico

Historia de Usuario - Visualización de los datos del consumo de agua en tiempo real

Código: HU5-2024

Como usuario, necesito visualizar los datos del
consumo de agua en tiempo real, con la ﬁnalidad
de monitorear el consumo de agua en tiempo real y
detectar anomalías.

Resultados:

-Vista en tiempo real de la velocidad de consumo en L/min
- Vista en tiempo real del consumo actual

-Vista de gráfico del consumo real , asimismo se muestra tooltip con el detalle del
consumo.
- La actualización de la gráfica se realiza aproximadamente cada 2 segundos.

Discusión: La visualización de datos del consumo de agua en tiempo real ha sido
implementada con éxito, proporcionando al usuario una vista clara de la velocidad de
consumo en L/min, así como del consumo actual. La inclusión de gráficos interactivos y
tooltips para detalles específicos mejora la experiencia del usuario y facilita la identificación
de patrones o anomalías en el consumo. Sin embargo, se podría mejorar la frecuencia de
actualización de la gráfica, ya que cada 2 segundos puede no ser suficiente en situaciones
de alto flujo o cambios rápidos en el consumo. Implementar notificaciones o alertas en
tiempo real para anomalías detectadas también podría ser beneficioso, permitiendo a los
usuarios actuar
la optimización del
rendimiento en la visualización podría ayudar a manejar más datos sin comprometer la
velocidad de carga.

rápidamente ante posibles problemas. Además,

Historia de Usuario - Visualización de los datos histórico del consumo de agua

Código: HU6-2024

Como usuario, necesito consultar y visualizar los
datos históricos del consumo de agua, con la
ﬁnalidad de analizar patrones y comparaciones del
consumo de agua en diferentes periodos.

Resultados:

- Vista de gráfico del consumo real según las fechas consultadas, en caso que no se ingrese
se muestra del último mes.
- Vista de gráfico del consumo real , asimismo se muestra tooltip con el detalle del consumo.
- La actualización de la gráfica se realiza aproximadamente cada 2 segundos

Discusión: : La implementación de la funcionalidad para consultar y visualizar datos
históricos de consumo de agua ha sido exitosa, permitiendo a los usuarios analizar patrones
a través de gráficos detallados. La opción de mostrar datos del último mes si no se ingresa
fechas específicas es una característica útil que facilita el acceso a información relevante sin
requerir configuración adicional. Sin embargo, el tiempo de actualización de la gráfica cada 2
segundos podría no ser necesario para datos históricos, ya que estos no requieren cambios
en tiempo real. Se podría considerar aumentar este intervalo para optimizar el rendimiento
del sistema y reducir la carga en el servidor. Además, la adición de herramientas analíticas
que permitan realizar comparaciones más profundas entre diferentes periodos de tiempo
podría enriquecer el análisis de datos, mejorando la toma de decisiones en la gestión del
consumo de agua.

Historia de Usuario - Exportación de datos del consumo del agua

Código: HU7-2024

Como usuario, necesito exportar los datos del
consumo de agua, con la finalidad de analizar los
datos externamente o generar reportes.

Resultados:

- Descarga exitosa en formato xlsx con los datos necesarios.
- Descarga exitosa en formato xlsx según la fecha inicio y fecha fin.

Discusión: La funcionalidad de exportar datos del consumo de agua se ha implementado
con éxito, permitiendo a los usuarios descargar la información necesaria en formato XLSX, lo
que facilita el análisis externo y la generación de reportes. La capacidad de filtrar los datos
según fechas específicas es un aspecto positivo que mejora la utilidad de la herramienta,
permitiendo a los usuarios concentrarse en períodos relevantes para su análisis. Sin
embargo, se podría considerar agregar opciones para exportar en otros formatos, como CSV
o PDF, para ampliar la flexibilidad del uso de los datos. Además, sería beneficioso
implementar una validación que confirme la selección de fechas adecuadas antes de la
exportación, evitando posibles confusiones o errores por parte del usuario.

Historia de Usuario - Alertas semanales por correo electrónico del consumo del agua

Código: HU8-2024

Como usuario, necesito recibir alertas
semanales por correo electrónico del
consumo de agua, con la finalidad de tomar
decisiones rápidas si el consumo excede el
promedio.

Resultados:

-

-

Programación exitosa para que el correo se envio de manera semanal a las 9:00
a.m.
Envio demo correcto con la estructura deseada.

Discusión:
La implementación de alertas semanales por correo electrónico para el consumo de agua es
un avance significativo que permite a los usuarios tomar decisiones informadas y rápidas en
caso de que el consumo exceda los promedios establecidos. La programación del envío a
una hora específica (9:00 a.m.) garantiza que los usuarios reciban la información de manera
la funcionalidad incluyendo la opción de
oportuna. Sin embargo, se podría mejorar
personalizar la frecuencia de las alertas (diarias, semanales, o mensuales) y la posibilidad de
ajustar
los umbrales de alerta, permitiendo a los usuarios definir límites según sus
necesidades específicas. Además, sería útil añadir una funcionalidad para que los usuarios
puedan ver un historial de las alertas recibidas, facilitando el seguimiento de tendencias a lo
largo del tiempo.

Historia de Usuario - Predicción del consumo de agua

Código: HU9-2024

Como usuario, necesito saber la predicción el
consumo de agua mensual , con la ﬁnalidad de
planiﬁcar el uso eﬁciente de agua basándome en
estimaciones precisas.

Resultados:
Los modelos predictivos desarrollados para el consumo de agua, tanto con datos simulados
como con datos reales, mostraron un rendimiento notable. En el caso de los datos

simulados, el modelo alcanzó un grado de precisión superior a 0.9, lo que indica que el
modelo puede explicar una gran parte de la variabilidad en los datos. Para los datos reales,
se obtuvo un resultado similar, lo que sugiere que el modelo es igualmente efectivo en
condiciones del mundo real. Las gráficas que comparan los valores reales con las
predicciones confirmaron la precisión del modelo, mostrando una alineación cercana entre
ambos conjuntos de datos.

Discusión: Estos resultados destacan la efectividad del algoritmo Random Forest para
predecir el consumo de agua en función de variables temporales. La capacidad del modelo
para manejar relaciones no lineales y su robustez ante variaciones en los datos son
características clave que contribuyen a su éxito. Sin embargo, también se identificaron áreas
de mejora, como la incorporación de variables adicionales que podrían influir en el consumo,
como factores climáticos o demográficos. Además, la implementación de técnicas avanzadas
de modelado podría ofrecer mejoras en la precisión y utilidad del modelo. En general, estos
hallazgos subrayan la importancia de utilizar enfoques basados en datos para optimizar la
gestión del agua y mejorar la planificación de recursos hídricos. Este ítem proporciona un
resumen claro de los resultados obtenidos y una discusión sobre su significado y posibles
mejoras. Si necesitas más ajustes o información adicional, no dudes en preguntar.

Tabla N° 26. Prueba , resultado y discusión del PMV2.

Elaboración propia.

PRUEBAS EN EL PMV 2

Historia de Usuario - Registro del nivel de agua en tiempo real

Código: HU10-2024

Como usuario, necesito recolectar los datos del
nivel de agua en tiempo real, con la finalidad de
monitorear el nivel del agua en el tanque para
evitar desbordamientos o escasez.

Resultados:

- Desarrollo exitoso del prototipo del nivel del agua implementando el sensor ultrasónico en
el tanque del agua.
- Conexión exitosa a Wi-Fi para envío de datos al servidor.
- Envío éxito a la base de datos con un rango de 2s desde el ESPS32.

Discusión: El desarrollo del prototipo para medir el nivel de agua ha sido exitoso, utilizando
tanque. La conexión a Wi-Fi se
un sensor ultrasónico para mediciones precisas en el

estableció eficazmente, permitiendo el envío de datos al servidor, y se logró una
actualización a la base de datos cada 2 segundos desde el ESP32. Para futuras mejoras, se
sugiere calibrar adecuadamente el sensor,
implementar un manejo de errores robusto,
asegurar la transmisión de datos, desarrollar una interfaz de usuario intuitiva y agregar
capacidades de análisis para optimizar la gestión del recurso hídrico.

Historia de Usuario - Visualización del nivel de agua en tiempo real

Código: HU11-2024

Como usuario, necesito visualizar los datos del
nivel de agua en tiempo real, con la finalidad de
evitar que el tanque se llene demasiado o se
vacíe.

Resultados:

-
-
-
-
-

Vista de gráfico simulado del tanque con nivel del agua real con colores.
Vista en tiempo real del nivel del agua en cm
Vista en tiempo real del porcentaje del nivel de agua
Vista en tiempo real del estado del nivel de agua
La actualización de la gráfica se realiza aproximadamente cada 2 segundos.

Discusión:

Los resultados de la prueba demuestran la efectividad del sistema de monitoreo del nivel de
agua en el tanque, con una visualización gráfica intuitiva que utiliza colores para identificar
niveles críticos. La medición en centímetros y porcentaje facilita el control del sistema,
mientras que el estado del agua permite decisiones informadas. La actualización cada 2
segundos garantiza información actualizada, lo que es crucial en entornos dinámicos. Se
sugiere integrar alertas automáticas y análisis predictivos en futuras versiones para mejorar
la eficiencia y seguridad del sistema.

Historia de Usuario - Visualización de los datos históricos del nivel de agua

Código: HU12-2024

Como usuario, necesito consultar el historial
del nivel de agua en el tanque, con la
finalidad de analizar el comportamiento del
nivel de agua a lo largo del tiempo.

Resultados:

-
-
-

Vista de gráfico de datos históricos de nivel del agua
Vista de datos históricos del nivel máximo del agua
La actualización de la gráfica se realiza aproximadamente cada 2 segundos.

Discusión:
La implementación de la funcionalidad para consultar y visualizar datos históricos de nivel de
agua ha sido exitosa, permitiendo a los usuarios analizar patrones a través de gráficos
detallados. Sin embargo, el tiempo de actualización de la gráfica cada 2 segundos podría no
ser necesario para datos históricos, ya que estos no requieren cambios en tiempo real. Se
podría considerar aumentar este intervalo para optimizar el rendimiento del sistema y reducir
la carga en el servidor.

Historia de Usuario - Alertas automáticas de niveles críticos del agua

Código: HU13-2024

Como usuario, necesito recibir alertas cuando
el nivel del agua alcance ciertos umbrales,
con la finalidad de prevenir desbordamientos
o niveles peligrosamente bajos.

Resultados:
La implementación de la función de alerta por correo para el nivel de agua ha demostrado
ser efectiva en la supervisión del estado del
tanque. Al ajustar la lógica para enviar
notificaciones cuando el nivel del agua se aproxima a los 17 cm (específicamente a 16.9 cm),
se ha mejorado la capacidad de respuesta ante posibles desbordamientos. Esta medida
proactiva permite a los usuarios tomar acciones preventivas antes de que el nivel alcance un
umbral crítico, lo que puede evitar situaciones de emergencia y optimizar la gestión del
recurso hídrico.

Discusión:
Los resultados obtenidos resaltan la importancia de contar con un sistema de monitoreo que
no solo informe sobre el estado actual, sino que también anticipe cambios significativos en
los niveles de agua. La implementación de alertas por correo ha facilitado una comunicación
rápida y eficiente, permitiendo a los responsables del manejo del agua actuar con prontitud.
Sin embargo, es crucial considerar la posibilidad de integrar otros métodos de notificación,
como mensajes de texto o aplicaciones móviles, para garantizar que las alertas sean
recibidas en tiempo real, especialmente en situaciones críticas. Además, sería beneficioso
evaluar la frecuencia y el contenido de las alertas para asegurar que los usuarios no se
sientan abrumados por notificaciones innecesarias.

Historia de Usuario - Exportación de datos históricos de nivel de agua

Código: HU14-2024

Como usuario, necesito exportar los datos del
nivel de agua, con la finalidad de analizarlos
externamente o generar informes de uso.

Resultados:

-
-
-

Vista de tabla de datos históricos de nivel del agua
Vista de tabla de datos históricos de nivel del agua actualizable cada 2 segundos
Exportación de la tabla a excel o csv

Discusión:
La funcionalidad de exportar datos del consumo de agua se ha implementado con éxito,
permitiendo a los usuarios descargar la información necesaria en formato XLSX y CSV, lo
que facilita el análisis externo y la generación de reportes. La capacidad de filtrar los datos
según fechas específicas es un aspecto positivo que mejora la utilidad de la herramienta,
permitiendo a los usuarios concentrarse en períodos relevantes para su análisis.

Historia de Usuario - Predicción del tiempo restante para vaciar el tanque

Código: HU15-2024

Como usuario, necesito saber en qué tiempo
se vaciará el tanque, con la finalidad de
anticipar cambios en el nivel del agua y tomar
acciones preventivas.

Resultados:
El modelo de Random Forest alcanzó una precisión R² significativa, lo que indica que logra
predecir con razonable eficacia el nivel de agua en función del tiempo, alineándose bien con

los datos observados. Las predicciones de tiempo de vaciado y llenado muestran un ajuste
adecuado para los niveles de agua superiores e inferiores, aunque se observaron algunas
limitaciones para ciertos puntos intermedios. Al graficar, se observó una buena
lo cual
correspondencia visual entre los datos reales y las predicciones del modelo,
demuestra que el modelo responde de manera precisa al cambio en el
tiempo. Los
resultados sugieren que, para mejorar aún más la precisión, podría considerarse un ajuste
más complejo o incorporar datos adicionales sobre las condiciones de flujo del tanque,
asegurando así una predicción más robusta para un sistema de monitoreo de agua eficiente.

Discusión:
La implementación de un modelo de Random Forest para la predicción del nivel de agua en
función del tiempo mostró resultados prometedores, aunque enfrentó desafíos relacionados
con la precisión del
tiempo estimado de vaciado y llenado en un sistema de tanque
controlado. Este modelo aprovecha datos históricos de niveles de agua para construir una
logrando captar patrones que
relación no lineal entre el
responden a variaciones en la tasa de vaciado y llenado. Sin embargo, dada la simplicidad
del modelo en relación con el contexto físico del tanque, el modelo puede ser sensible a
cambios en el flujo de entrada y salida, lo que podría afectar la precisión en casos donde las
condiciones no son estables. A pesar de estos desafíos, el enfoque basado en Random
Forest resultó ser una herramienta efectiva, pero idealmente debería complementarse con
técnicas adicionales para mejorar la capacidad del modelo de adaptarse dinámicamente a
diferentes estados de funcionamiento del tanque.

tiempo y el nivel del

tanque,

Tabla N° 27. Prueba , resultado y discusión del PMV3.

Elaboración propia.

PRUEBAS EN EL PMV 3

Historia de Usuario - Registro de datos de calidad del agua en tiempo real

Código: HU16-2024

Como usuario, necesito recolectar datos sobre la
calidad del agua en tiempo real, con la finalidad de
asegurar que el agua cumple con los estándares
de calidad requeridos.

Resultados:

- Desarrollo exitoso del prototipo que incluye calidad del agua implementando el sensor
php, tds, turbidez, temperatura, humedad en el tanque del agua.
- Conexión exitosa a Wi-Fi para envío de datos al servidor.
- Envío éxito a la base de datos con un rango de 2s desde el ESPS32.

Discusión:
La implementación del prototipo ha sido exitosa, logrando integrar diversos sensores para
medir la calidad del agua, incluyendo parámetros como el pH, TDS, turbidez, temperatura y
humedad en el
tanque de agua. Estos datos se capturan en tiempo real y se envían
correctamente al servidor mediante una conexión Wi-Fi estable. Además, se ha logrado un
rendimiento eficiente, con un tiempo de envío de datos a la base de datos de
aproximadamente 2 segundos desde el ESP32. Este avance resalta la capacidad del sistema
para monitorear y transmitir información crucial para el control de la calidad del agua de
manera ágil y precisa.

Historia de Usuario - Visualización de la calidad de agua en tiempo real

Código: HU17-2024

Como usuario, necesito visualizar los datos de la
calidad del agua en tiempo real, con la finalidad de
reaccionar rápidamente a cualquier anomalía en
los niveles de calidad.

Resultados:

-
-
-
-
-
-

Vista de gráfico simulado del tanque con la calidad del agua.
Vista en tiempo real del parámetro de ph.
Vista en tiempo real del parámetro de tds.
Vista en tiempo real del parámetro de turbidez.
Vista en tiempo real del parámetro de humedad y temperatura.
La actualización de la gráfica se realiza aproximadamente cada 2 segundos.

Discusión:

Se ha implementado con éxito la vista de un gráfico simulado del tanque que muestra los
parámetros de calidad del agua en tiempo real, incluyendo pH, TDS, turbidez, humedad y
temperatura. Cada uno de estos parámetros se actualiza cada 2 segundos, asegurando que
los datos reflejen de manera precisa las condiciones actuales del agua. La actualización en
tiempo real de los parámetros facilita un monitoreo constante y efectivo, lo que permite a los
usuarios detectar cualquier variación en la calidad del agua de manera inmediata. Sin
embargo, se debe continuar monitoreando el rendimiento para asegurar que la actualización
frecuente no afecte la fluidez de la visualización en situaciones de alta carga de datos.

Historia de Usuario - Visualización de datos históricos de la calidad del agua

Código: HU18-2024

Como usuario, necesito consultar el historial de
calidad del agua con la finalidad de analizar la

evolución de la calidad del agua a lo largo del
tiempo.

Resultados:

-
-

Vista de gráfico de datos históricos de la calidad del agua
Vista de datos históricos de la calidad máximo del agua

Discusión:
La vista de gráfico de datos históricos de la calidad del agua facilita el análisis de tendencias
a lo largo del tiempo, mientras que la vista de datos históricos de la calidad máxima del agua
ayuda a identificar picos críticos. Ambas vistas son esenciales para un monitoreo efectivo y
la toma de decisiones informadas sobre la gestión del agua.

Historia de Usuario - Alertas automáticas por correo cuando los parámetros de calidad
estén fuera de los límites

Código: HU19-2024

Como usuario, necesito recibir alertas cuando la
calidad del agua no cumpla con los estándares,
con la finalidad de tomar acciones correctivas
cuando se detecten problemas en la calidad del
agua.

Resultados:

La implementación de un sistema de alertas para la calidad del agua ha permitido a los
usuarios recibir notificaciones inmediatas cuando los parámetros de calidad, como pH, TDS,
turbidez y temperatura, no cumplen con los estándares establecidos. Este sistema se basa
en el monitoreo continuo de estos parámetros, utilizando sensores que envían datos en
tiempo real a una base de datos. Cuando se detectan anomalías, se generan alertas
automáticas que son enviadas a los usuarios a través de correo electrónico o SMS,
facilitando así la toma de decisiones rápidas y efectivas para abordar problemas en la calidad
del agua.

Discusión:
La capacidad de recibir alertas sobre la calidad del agua es crucial para la salud pública y la
gestión ambiental. Este sistema no solo empodera a los usuarios al proporcionar información
crítica en tiempo real, sino que también fomenta una mayor responsabilidad en la gestión de
recursos hídricos. Sin embargo, su efectividad depende de varios factores, incluyendo la
precisión de los sensores, la claridad en la interpretación de las alertas y la educación
continua de los usuarios sobre cómo responder adecuadamente a estas notificaciones.
Además, es importante considerar los desafíos técnicos asociados con el mantenimiento del
sistema y la necesidad de actualizar continuamente los umbrales y protocolos según las
condiciones cambiantes del entorno.

Historia de Usuario - Exportación de datos de calidad del agua

Código: HU20-2024

Como usuario, necesito exportar los datos de
calidad del agua con la finalidad de analizarlos
externamente o generar informes de calidad.

Resultados:

-
-

Descarga exitosa en formato xlsx y csv con los datos de calidad de agua necesarios.
Descarga exitosa en formato xlsx y csv según la fecha inicio y fecha fin.

Discusión:

Los resultados muestran que las descargas de datos se realizaron correctamente en formato
XLSX y CSV. La primera descarga incluyó todos los datos de calidad de agua necesarios,
mientras que la segunda se ajustó al rango de fechas especificado, lo que garantiza una
gestión precisa y accesible de la información.

Historia de Usuario - Predicción de la calidad del agua

Código: HU21-2024

Como usuario, necesito saber la predicción de la
calidad del agua a lo largo del tiempo, con la
finalidad de anticipar problemas potenciales en la
calidad del agua y planificar intervenciones.

Resultados:
La implementación de un sistema de predicción de la calidad del agua permite a los usuarios
anticipar problemas potenciales mediante el análisis de datos históricos y la aplicación de
modelos predictivos. Al utilizar algoritmos de aprendizaje automático y técnicas estadísticas,
se pueden generar proyecciones sobre cómo los parámetros de calidad del agua, como pH,
TDS, turbidez y temperatura, pueden cambiar a lo largo del tiempo. Esto proporciona a los
usuarios información valiosa que les permite planificar intervenciones adecuadas antes de

que se presenten problemas significativos en la calidad del agua.

Discusión:
La capacidad de prever la calidad del agua es fundamental para la gestión proactiva de
recursos hídricos. Al conocer las tendencias y patrones esperados, los usuarios pueden
implementar medidas preventivas, como ajustes en el tratamiento del agua o intervenciones
en fuentes de contaminación. Sin embargo, la efectividad de estas predicciones depende de
la calidad y cantidad de datos disponibles, así como de la precisión de los modelos
utilizados. Además, es esencial que los usuarios comprendan cómo interpretar
las
predicciones y actuar en consecuencia. La educación continua y la comunicación clara sobre
las implicaciones de las predicciones son cruciales para maximizar el impacto positivo del
sistema en la gestión del agua.

Tabla N° 26. Cuadro de Evidencia FURPS

Evidencia FURPS

Funcionalidad:

- Autenticación de usuarios

- Creación, edición y eliminación de usuarios, clientes, tanques y sensores

- Recolección de datos en tiempo real

Resultados: Todas las funciones operativas, se le da un valor del 100% debido a

que las historias de usuario han sido cubiertas y funcionan como se esperaba.

Usabilidad:

- Interfaz intuitiva para la gestión de usuarios, clientes, tanques y sensores

- Facilidad para recolectar datos y visualizar resultados

Resultados:

Interfaz intuitiva, se requieren mejoras en las instrucciones de

recolección de datos. Sin embargo se un nuevo usuario puede completar la

configuración inicial con un valor de 3 minutos, además de que se espera que el

98% de usuarios lograrán usar el programa sin ayuda.

Rendimiento:

- Respuesta rápida al autenticar usuarios

- Capacidad para procesar datos en tiempo real sin latencias significativas

Resultados: Tiempos de respuesta aceptables,

latencias ocasionales en

recolección de datos. Durante las pruebas se da un valor de 2 segundos como

máximo para la carga de la página y gráficos con un uso del CPU del 25% variable

dependiendo de los recursos y un uso de memoria del 35% normalmente.

Fiabilidad:

- Sistema que garantice la disponibilidad de la información y el acceso

- Mecanismos de recuperación ante fallos en la recolección de datos

Resultados: Sistema en general fiable, sin embargo se espera que en una prueba

de 30 días se encuentren una tasa de errores del 0.5% y que funcione por 1000

horas por semana lo cual indicaría que es ideal.

Soporte:

- Documentación para la gestión de usuarios y datos

- Asistencia técnica para resolver problemas de acceso y manejo de datos

Resultados: Documentación recién en beta, sin embargo se debe de hacer esta

prueba a largo plazo en donde se enfocarán los esfuerzos en solucionar el 85% de

problemas resueltos en una primera interacción con el usuario.

Link

Modelo

FURPS

SYSMONWA

:

https://docs.google.com/spreadsheets/d/1BbdP2t69W_2hyWnYLwPFmMvbhf3lNVK

x/edit?usp=sharing&ouid=102285367331457502263&rtpof=true&sd=true

Evidencia Understand

Pruebas de Calidad:

Métricas:

Resultados obtenidos en los modelos de machine learning:

Tabla N° 27. Cuadro Resultados obtenidos en los modelos de machine learning

Caso de

Tipo de ML

Técnica de

Algoritmo Definición del Algoritmo

Resultado Obtenido

uso de ML

aprendizaje

del modelo

Porcentaj

e de

precisión

Predicción

Supervisado.

Regresión.

Random

Random Forest

es

un

El modelo puede explicar una gran parte de la

90% o más

del consumo

de agua.

Forest.

algoritmo

de

aprendizaje

variabilidad

en

los

datos

simulados.

automático

basado

en

árboles

de

decisión.

Funciona

construyendo

múltiples

árboles

decisión

durante

de

el

entrenamiento y produce la

clase que es el modo de las

clases (clasiﬁcación) o la

media/valor

promedio

(regresión)

de

las

predicciones de los árboles

individuales. Este enfoque

ayuda a mejorar la precisión

y controla el sobreajuste.

Predicción

Supervisado.

Regresión.

Random

El modelo es efectivo para anticipar patrones

90% o más

del consumo

de agua.

Forest.

en el consumo real.

Predicción

Supervisado

Regresión.

Random

El modelo es efectivo para anticipar patrones

90% o más

del nivel de

agua.

Forest.

en el nivel de agua real.

Tabla N° 28. Cuadro Discusión, Similitudes y diferencias del PMV1

Discusión PMV 1 - Consumo del agua

El PMV1 - Consumo del agua presenta un enfoque práctico para el monitoreo

eficiente del uso del agua a través de tecnologías de IoT, similar a los sistemas

avanzados de monitoreo de calidad del agua mencionados en los antecedentes. [6]

Estos antecedentes subrayan la creciente relevancia de la IoT en la gestión de

recursos hídricos, donde la recopilación de datos en tiempo real juega un papel

crucial. Si bien el PMV1 se enfoca en la cantidad de agua consumida, es similar en

esencia a los proyectos que miden parámetros de calidad del agua, ya que ambos

buscan optimizar el uso del recurso a través de la monitorización constante y la

posibilidad de alertas o respuestas automáticas. [7]

El artículo sobre la "Integración de la computación en la nube e IoT" señala que la

combinación de estas tecnologías permite que los datos se envíen a servidores

remotos para su análisis en tiempo real, algo que también se implementa en PMV1,

donde los datos de consumo de agua son visualizados y gestionados en tiempo

real a través de una plataforma digital. [6] Asimismo, tanto en PMV1 como en el

estudio sobre "Monitoreo inteligente de la calidad del agua", la tecnología no solo

recolecta información, sino que también permite que los usuarios finales

(propietarios, administradores, agricultores) actúen proactivamente en la gestión

del recurso, ya sea para reducir el desperdicio de agua o mejorar la calidad del

agua para consumo o riego. [7]

El artículo sobre el "Sistema de monitoreo basado en IoT para la medición de

calidad de agua de riego" presenta una visión clara de cómo el IoT es clave para

aplicaciones agrícolas y urbanas. [8] Aunque el PMV1 no mide calidad de agua,

comparte la misma base tecnológica y operativa, como la utilización de sensores,

controladores y la transmisión de datos hacia la nube para su posterior análisis. De

hecho,

los desafíos abordados en la gestión del consumo del agua pueden

expandirse a nuevas áreas, como la calidad del agua y el monitoreo de niveles en

sistemas futuros, aprovechando las capacidades actuales de IoT y computación en

la nube que ya han demostrado ser efectivas en otros contextos de monitoreo

hídrico. [6]

Similitudes

Las similitudes entre el PMV1 y los sistemas de monitoreo de calidad del agua

incluyen el uso de tecnología IoT para la recolección y análisis de datos. Ambos

sistemas dependen de la conectividad a Internet para enviar datos a la nube,

permitiendo a los usuarios acceder a información en tiempo real desde cualquier

lugar. [6] Además, tanto el PMV1 como los sistemas de calidad utilizan alertas

para notificar a los usuarios sobre situaciones anormales,

facilitando una

respuesta rápida. Por último, ambos enfoques tienen el potencial de mejorar la

eficiencia en la gestión del agua, ya que permiten a los usuarios tomar decisiones

informadas basadas en datos precisos y actualizados. [6, 7]

Diferencias

Las diferencias entre el PMV1 y los sistemas de monitoreo de calidad del agua

son significativas. En primer lugar, el PMV1 se centra en medir y optimizar el

consumo de agua, utilizando sensores que registran el volumen de agua utilizado,

mientras que los sistemas de calidad del agua requieren sensores más

avanzados y especializados para medir parámetros físicos y químicos. [6, 7, 8]

Además, el ámbito de aplicación de cada sistema varía: el PMV1 se puede

implementar fácilmente en hogares y entornos industriales, mientras que los

sistemas de calidad del agua suelen aplicarse en contextos específicos, como en

la agricultura o en plantas de tratamiento. Esta especialización en el monitoreo de

calidad del agua implica que estos sistemas a menudo involucran un análisis más

complejo y un diseño de sensor más elaborado, en comparación con el enfoque

más directo y accesible del PMV1. [8]

Discusión PMV 2 - Nivel del agua

El PMV2 - Nivel de agua representa un avance significativo en la gestión y

monitoreo del nivel de agua en tanques, utilizando tecnologías de IoT para

proporcionar una solución accesible y eficiente. [7] Este enfoque es un reflejo de la

creciente importancia de la conectividad y la recopilación de datos en tiempo real

en la administración de recursos hídricos. A diferencia de los sistemas que se

centran únicamente en el consumo, el PMV2 busca prevenir problemas asociados

con el desbordamiento y la escasez, permitiendo una gestión más equilibrada del

recurso hídrico.

La integración de la computación en la nube con el IoT permite que los datos de

nivel de agua sean transmitidos a servidores remotos, donde son analizados y

presentados a los usuarios a través de una interfaz digital intuitiva. [7] Este flujo de

información en tiempo real empodera a los usuarios, ya sean propietarios de

viviendas, administradores de instalaciones o agricultores, para tomar decisiones

informadas y rápidas, contribuyendo a una gestión más sostenible del agua.

La tecnología empleada en el PMV2 incluye sensores avanzados que no solo

miden el nivel del agua, sino que también facilitan alertas automáticas cuando se

alcanzan umbrales críticos. Esto no solo ayuda a prevenir desbordamientos, sino

que también permite a los usuarios anticipar situaciones de escasez. El diseño del

sistema fomenta la proactividad, permitiendo que los usuarios respondan

adecuadamente a las fluctuaciones en los niveles de agua. [7]

Similitudes

El PMV2 - Nivel de agua presenta similitudes con sistemas como “Integración en la

nube y IoT” y “Smart water quality monitoring system with cost-effective using IoT”

en su uso de tecnologías IoT para la recolección y transmisión de datos en tiempo

real.

[6, 7] Los sistemas dependen de la conectividad a Internet para enviar

información a la nube, lo que permite a los usuarios acceder a datos históricos y

recibir alertas automáticas sobre situaciones críticas. Además,

todos buscan

empoderar a los usuarios, ya sean propietarios, administradores o agricultores,

brindándoles herramientas para tomar decisiones informadas que contribuyan a

una gestión sostenible de los recursos hídricos. [8]

A pesar de enfocarse en aspectos diferentes —consumo, nivel y calidad del

agua—, comparten un objetivo común: optimizar la utilización del agua y prevenir

problemas potenciales. A través de plataformas digitales, los usuarios pueden

visualizar datos y actuar de manera proactiva, lo que mejora la eficiencia en la

gestión del agua y promueve la sostenibilidad en su uso. [6, 7, 8]

Diferencias

El PMV2 y los sistemas de los antecedentes presentan diferencias clave en su

enfoque y aplicación. Mientras el PMV2 monitorea el nivel del agua en tanques

usando sensores de nivel mientras que las demás se enfocan en la calidad,

teniendo un enfoque completo en esa variable. [6, 7, 8]

Además, cada proyecto tiene un contexto de uso distinto: relevantes en sectores

específicos como la agricultura y el suministro de agua potable, donde la calidad es

crucial. Aunque todos comparten el objetivo de mejorar la gestión del agua, sus

enfoques y las intervenciones del usuario son diferentes,

lo que resalta la

importancia de cada sistema en su respectivo ámbito. [7, 8]

Discusión PMV 3 - Calidad del agua

El PMV3 de calidad del agua se destaca frente a los tres antecedentes analizados

al integrar capacidades de monitoreo en tiempo real y consulta de datos históricos.

En comparación con “Integration of Cloud Computing and Internet of Things: A

Survey”, el PMV3 añade valor con la visualización de tendencias históricas, lo que

permite anticipar problemas futuros y tomar decisiones basadas en análisis

prolongados. [6]

Además, frente a “Smart water quality monitoring system with cost-effective

using IoT”, el PMV3 incorpora un sistema de alertas que no solo recopila datos,

sino que interpreta los valores medidos para informar automáticamente si el agua

es apta para consumo. Esto mejora significativamente la funcionalidad práctica del

sistema respecto a los datos transmitidos en bruto propuestos en este

antecedente. [7]

En relación con “IoT-Based Monitoring System for Irrigation Water Quality

Measurement”, el PMV3 abarca un rango más amplio de aplicaciones al incluir

variables como TDS, esenciales para evaluar la potabilidad del agua, además de

ser útil tanto en el ámbito agrícola como en el consumo humano. Esto lo convierte

en una herramienta más versátil y de mayor impacto. [8]

Finalmente, el uso del ESP32 como microcontrolador aporta una ventaja

competitiva frente a los tres antecedentes, al ofrecer una solución más eficiente en

términos de costos y consumo energético, favoreciendo su implementación en

áreas remotas. Estas mejoras posicionan al PMV3 como una solución avanzada y

escalable para monitorear y garantizar la calidad del agua. [6, 7, 8]

Similitudes

El PMV3 comparte varias similitudes con los antecedentes analizados. Al igual que

ellos, utiliza IoT para capturar y transmitir datos en tiempo real sobre parámetros

clave como pH,

turbidez,

temperatura y humedad, permitiendo un monitoreo

automatizado y eficiente. [6, 7, 8] Además, todos los sistemas buscan garantizar la

calidad del agua mediante soluciones tecnológicas sostenibles, y emplean

plataformas en la nube para almacenar y analizar datos, facilitando el acceso

remoto. [7, 8]

Asimismo, comparten el enfoque en la sostenibilidad y la seguridad del agua,

abordando problemas críticos como la contaminación y su impacto en la salud y la

agricultura.

[7,8] Estas similitudes destacan que el PMV3 sigue prácticas

establecidas en el campo, mejorando aspectos clave para optimizar su

funcionalidad.

Diferencias

El PMV3 presenta varias diferencias clave en comparación con los antecedentes. A

diferencia de los sistemas descritos en “Integration of Cloud Computing and

Internet of Things: A Survey” [6] y “Smart water quality monitoring system with

cost-effective using IoT” [7], el PMV3 incluye un sistema de alertas integrado que

notifica automáticamente si el agua es apta para consumo, lo que permite una

acción inmediata ante la detección de problemas. Además, el PMV3 permite

visualizar datos históricos, una capacidad que no está presente en los

antecedentes que se enfocan solo en el monitoreo en tiempo real [6, 7].

El PMV3 también mide el TDS, un parámetro crucial para evaluar la potabilidad del

agua, lo que lo diferencia de “IoT-Based Monitoring System for Irrigation Water

Quality Measurement” [8], que se concentra únicamente en parámetros como la

turbidez y el pH para el riego. En cuanto al hardware, el PMV3 utiliza el ESP32, un

microcontrolador eficiente en términos de costo y consumo energético, algo que no

se especifica en los antecedentes, lo que hace al PMV3 más escalable y adecuado

para entornos con recursos limitados [6, 7, 8].

Finalmente, el PMV3 tiene un enfoque integral, siendo útil tanto para la calidad del

agua potable como para el agua de riego,

lo que lo hace más versátil en

comparación con los sistemas que se centran solo en el ámbito agrícola o en el

análisis de datos en tiempo real [6, 8]. Estas diferencias posicionan al PMV3 como

una solución avanzada y más completa para monitorear la calidad del agua.

X.

LECCIONES APRENDIDAS POR PMV

PMV 1: Consumo del agua

1. Estructura modular facilita la escalabilidad: Al organizar el sistema en módulos

separados para gráficos en tiempo real, tablas históricas y exportación de datos,

es más fácil mantener y expandir la aplicación, lo cual será clave para futuros

proyectos como PMV2 y PMV3.

2. La integración de herramientas externas agiliza el desarrollo: Utilizar servicios

como Pusher para actualizaciones en tiempo real y librerías como Chart.js para

gráficos interactivos permite desarrollar rápidamente funcionalidades avanzadas,

optimizando el tiempo y los recursos.

3. Filtrado y visualización de datos es crucial: Aprender a implementar

correctamente filtros por rango de fecha, junto con una paginación adecuada y una

visualización clara de los datos, mejora considerablemente la experiencia del

usuario y la utilidad del sistema para tomar decisiones informadas.

4.

Importancia de la Calidad de los Datos: Una de las lecciones más significativas

aprendidas durante el desarrollo de los modelos predictivos es que la calidad y la

cantidad de los datos son fundamentales para el éxito del análisis. La precisión de

las predicciones depende en gran medida de contar con datos históricos fiables y

representativos. Esto resalta la necesidad de implementar buenas prácticas en la

recopilación y el mantenimiento de datos, así como la importancia de realizar un

preprocesamiento adecuado para manejar valores faltantes y asegurar que los

datos sean aptos para el entrenamiento del modelo. Este ítem resume una lección

clave aprendida a lo largo del proceso. Si necesitas más ajustes o información

adicional, no dudes en preguntar.

PMV 2: Nivel del agua

1. Utilizar la estructura de manera estandarizada: Al utilizar un estándar se puede

integrar de manera eficiente el software sin que haya inconvenientes.

2. La integración de herramientas externas y código puro agiliza el desarrollo:

Utilizar servicios como Chart.js para gráficos interactivos permite desarrollar

rápidamente funcionalidades avanzadas, optimizando el tiempo y los recursos;

utilizando solo código se puede realizar el cálculo y muestra de las vistas.

3. Filtrado y visualización de datos es crucial: Aprender a implementar

correctamente filtros por rango de fecha, junto con una paginación adecuada y una

visualización clara de los datos, mejora considerablemente la experiencia del

usuario y la utilidad del sistema para tomar decisiones informadas.

4. Calidad de los Datos y buena filtración: La calidad de los datos es fundamental

para garantizar que la información que se maneja sea confiable, precisa y útil para

la toma de decisiones. Una buena filtración de datos contribuye a mejorar esta

calidad, eliminando duplicados, errores y valores que no aporten valor.

PMV 3: Calidad del Agua

1. La Importancia de una Visualización clara y Comprensible: Decidir el tipo de

gráfico adecuado es crucial para la interpretación efectiva de los datos. El uso de

un gráfico de barras para representar las cinco variables (pH, humedad, turbidez,

temperatura, TDS) permite una visualización clara y facilita la comparación de los

valores. A veces, la elección de un gráfico simple puede ser la más efectiva.

2. Tomar Decisiones Basadas en el Usuario: Priorizar la facilidad de uso y la

comprensión de los usuarios es esencial. Al ofrecer opciones claras sobre si el

agua es apta para el consumo según las variables, se mejora la experiencia del

usuario, permitiéndoles tomar decisiones informadas de manera rápida y sencilla.

3. La Complejidad de Manejar Múltiples Variables: Manejar y visualizar múltiples

variables puede ser desafiante, especialmente cuando se busca representar una

gran cantidad de datos de manera comprensible. El enfoque de usar un gráfico de

barras para mostrar estas variables simultáneamente demuestra la importancia de

simplificar la presentación de la información sin perder detalle.

4.

Iteración en el Diseño de Funcionalidades: La decisión de incluir un sistema de

alertas y opciones claras para determinar la potabilidad del agua resalta la

necesidad de iterar sobre el diseño para hacer que las funcionalidades sean útiles

y comprensibles. A través de pruebas y ajustes, se puede llegar a una solución

que balancee bien la precisión técnica y la usabilidad.

XI.

CONCLUSIONES

PMV 1 - Consumo del agua:

● La importancia de la visualización clara de datos: Lograr una presentación

eficiente y accesible de los datos históricos y en tiempo real, mediante gráficos y

tablas bien estructuradas, es clave para un monitoreo efectivo del consumo de

agua.

● Automatización y exportación de datos como valor añadido: La funcionalidad

para filtrar, paginar y exportar los datos en formatos como CSV y Excel añade un

valor significativo, permitiendo un análisis posterior más detallado y flexible.

● Sólida base para futuros proyectos: La experiencia adquirida en la

implementación de PMV1 sienta una base sólida para expandir el sistema con

PMV2 - Nivel del agua y PMV3 - Calidad del agua, dado que muchos de los

enfoques y soluciones adoptados pueden ser reutilizados o adaptados a nuevos

contextos.

● Desafíos técnicos resueltos con herramientas externas: El uso de

herramientas como Pusher para el manejo de datos en tiempo real y bibliotecas de

visualización permite superar barreras técnicas y optimizar el rendimiento del

sistema.

● Modelo Predictivo de Consumo de Agua: Los modelos desarrollados para

predecir el consumo de agua, tanto con datos simulados como con datos reales,

han demostrado ser efectivos y precisos. La capacidad del algoritmo Random

Forest para manejar datos complejos resalta la importancia de utilizar datos

históricos de calidad, lo que permite a las autoridades gestionar mejor los recursos

hídricos. Además,

la visualización clara de los resultados facilita la toma de

decisiones informadas, estableciendo una base sólida para futuras investigaciones

y desarrollos en el ámbito del consumo de agua.

PMV 2 - Nivel del agua:

● Implementación exitosa de Tecnología IoT: La implementación del sistema de

monitoreo del nivel de agua mediante tecnología IoT ha permitido la recolección en

tiempo real de datos precisos y fiables, mejorando significativamente la gestión de

recursos hídricos.

● Accesibilidad de Datos Históricos: La capacidad de visualizar y analizar datos

históricos de niveles de agua facilita la toma de decisiones informadas. Los

usuarios pueden identificar patrones y tendencias, lo que es crucial para la

planificación y optimización del uso del agua.

● Alertas Proactivas: El sistema de alertas automáticas para niveles críticos

garantiza que los usuarios puedan actuar rápidamente en situaciones de riesgo,

como desbordamientos o niveles peligrosamente bajos, minimizando pérdidas y

mejorando la seguridad.

● Optimización de Recursos: El monitoreo continuo del nivel del agua contribuye a

una gestión más eficiente de los recursos hídricos, permitiendo a las

organizaciones adaptar su consumo y almacenamiento según las condiciones

actuales.

● Facilitación de Informes y Exportaciones: La funcionalidad de exportar datos a

formatos como CSV y Excel simplifica la generación de informes, permitiendo a los

usuarios compartir información de manera efectiva con otras partes interesadas y

cumplir con requisitos regulatorios.

● Mejora en la Toma de Decisiones: Los datos presentados en gráficos y tablas

proporcionan a los usuarios una comprensión clara del estado del agua en sus

sistemas, lo que apoya la toma de decisiones estratégicas y mejora la planificación

a largo plazo.

● Futuras Mejoras: Aunque el sistema ha sido efectivo, se han identificado áreas

para futuras mejoras, como la integración de análisis predictivo que permita

anticipar cambios en los niveles de agua basados en datos históricos y

condiciones ambientales.

● Sostenibilidad y Conciencia Ambiental: Este proyecto fomenta la sostenibilidad

al permitir una gestión más consciente del agua, un recurso vital. La visibilidad y el

control del nivel de agua contribuyen a la conservación y uso responsable de este

recurso.

PMV 3 - Calidad del agua:

● El Uso de Gráficos Simples es Crucial: Elegir un gráfico de barras para

representar las variables de calidad del agua resultó ser la solución más efectiva.

A pesar de la variedad de datos, un gráfico sencillo facilita la comparación y

comprensión, destacando la importancia de la simplicidad en la visualización de

datos complejos.

● La Accesibilidad de la Información es Fundamental: Ofrecer una opción clara

para indicar si el agua es segura para el consumo mejora la accesibilidad y toma

de decisiones del usuario,

lo que demuestra que las interfaces deben estar

diseñadas para ser intuitivas y fáciles de interpretar.

● Adaptabilidad al Usuario Final: Las decisiones de diseño deben centrarse en las

necesidades del usuario. Incorporar alertas sobre la potabilidad del agua refleja

una solución adaptada a los requisitos reales de los usuarios, dándoles una

herramienta útil y directa.

● El Desafío de Representar Datos Múltiples: Manejar múltiples variables como

pH, temperatura, turbidez, TDS y humedad en un solo gráfico representa un reto.

Sin embargo, el uso de gráficos de barras mostró ser una estrategia exitosa para

organizar y presentar estos datos de forma efectiva.

● La Relevancia del Monitoreo en Tiempo Real: El monitoreo en tiempo real es

crucial para la toma de decisiones rápidas. Integrar funcionalidades de alerta sobre

la calidad del agua en tiempo real puede prevenir riesgos y mejorar la respuesta

ante problemas de calidad hídrica.

● Mejora Continua en el Diseño: El proceso de tomar decisiones sobre qué

mostrar y cómo mostrarlo (como las alertas de potabilidad y los gráficos) es

iterativo. El refinamiento del diseño basado en las pruebas y las necesidades de

los usuarios es un paso necesario para optimizar cualquier solución tecnológica.

● La Importancia de las Herramientas de Visualización en Sistemas Complejos:

La elección adecuada de herramientas de visualización es crucial cuando se trata

de sistemas que manejan múltiples parámetros. En este caso, un gráfico de barras

proporcionó una solución que equilibró la simplicidad y la efectividad para el

monitoreo de la calidad del agua.

● El Éxito radica en la Usabilidad y funcionalidad: A medida que el proyecto

avanzaba, se demostró que la clave del éxito no solo está en la precisión de los

datos, sino también en su presentación y en las funcionalidades adicionales como

las alertas. Un sistema que es tanto funcional como fácil de usar tiene más

posibilidades de tener un impacto positivo en los usuarios.

Anexos

Evidencias de la funcionalidad de la aplicación por PMV:

● Link del video del PMV 1 y código QR:

https://drive.google.com/file/d/1185tb-bW0NkeT7vfZWqCItVrTDDOMdjO/view

● Link del video del PMV 2 y código de

QR:https://drive.google.com/file/d/17NiDpcmJhszEx3aVY9dtIxiK-t-R1f0G/view

● Link del video del PMV 3 y código de QR:

https://drive.google.com/drive/folders/19irvS7SIiZBqe9tW0xAlb5MwXe8jZIdM?usp

=sharing

Evidencias para evaluación parcial:

● Link del video de la presentación:

https://drive.google.com/file/d/1r3ZTT2P9qyPubAX-XXaEX5NtRg3chnQe/view

● Link de la ppt

https://drive.google.com/file/d/1HHfKriwp5m7p0AssZRrjJ7KeLkioXBDE/view?usp=

sharing

Evidencias del código implementado de la aplicación:

● Repositorio en GitHub: https://github.com/i1920929/sysmonwa

Evidencias del código implementado con tecnologías emergentes:

● Link de Machine Learning implementado en Google Colab:

Consumo

https://colab.research.google.com/drive/1g7dDMZvqrNdRCesKVvzU62frG9gLcv0-

?hl=es#scrollTo=NGWvYHSNDoEh

Tiempo de vaciado:

https://colab.research.google.com/drive/1QLxj-c3BVbENakCeYht12wQPqtQCJiRL

?usp=sharing

Calidad de agua :

https://colab.research.google.com/drive/1DK2ICXaieQHsELfKYnH6q6iq-GDcySRB

?usp=sharing

● Link IOT - código

https://github.com/i1920929/sysmonwa/blob/main/resources/views/IoT/water-monit

oring-Iot-Sysmonwa.ino

Evidencia de la implementación del proyecto completo y poster:

● Link del video completo:

XII. BIBLIOGRAFÍA

[1] ORGANIZACIÓN MUNDIAL DE LA SALUD. Guías para la calidad del agua de

consumo humano [en línea]. 4a ed. Ginebra: OMS, 2022 [fecha de consulta: 3

septiembre

2024].

Disponible

en:

https://www.who.int/es/publications/i/item/9789240045064

[2] BANERJEE, S. y MORELLA, E. Africa's Water and Sanitation Infrastructure: Access,

Affordability, and Alternatives. Washington, D.C.: The World Bank, 2021.

ISBN

978-0-8213-8457-2.

[3] GUBBI, J., et al. Internet of Things (IoT): A vision, architectural elements, and future

directions. Future Generation Computer Systems [en línea]. 2013, 29(7), 1645-1660

[fecha de consulta: 3 septiembre 2024].

ISSN 0167-739X. Disponible en:

https://doi.org/10.1016/j.future.2013.01.010

[4] SCHWABER, K. y SUTHERLAND, J. The Scrum Guide [en línea]. Scrum.org, 2020

[fecha

de

consulta:

3

septiembre

2024].

Disponible

en:

https://scrumguides.org/scrum-guide.html

[5] PRESSMAN, R.S. y MAXIM, B.R. Software Engineering: A Practitioner's Approach. 9a

ed. New York: McGraw-Hill Education, 2020. ISBN 978-1-259-87256-7.

[6] ALESSIO, B., WALTER, D., VALERIO, P., y ANTONIO, P., “Integration of Cloud

computing and Internet of Things: A survey”, Future Gener Comput Syst, vol. 56, pp.

684–700, 2016.

[7] PASIKA, S. y GANDLA, S., “Smart water quality monitoring system with cost-effective

using IoT”, Heliyon, vol. 6, p. e04096, 2020.

[8] GAMARRA, A. H., TAIPE, J. A., ARELLANO, M. A., LOZANO, Y. D., y SUAZO, Á. C.,

“Sistema de monitoreo basado en IoT para la medición de calidad de agua de riego”,

Prospectiva Universitaria, vol. 20, núm. 01, pp. 31–39, 2023. Disponible en:

https://doi.org/10.26490/uncp.

[9] SALAS, J., MARAVER, F., RODRÍGUEZ, L., SÁENZ, M., VITORIA, I., y MORENO, A.,

“The importance of water consumption in health and disease prevention: the current

situation”,

Nutr.

Hosp.,

vol.

37,

núm.

5,

2020.

Disponible

en:

https://dx.doi.org/10.20960/nh.03160.

[10] GONZÁLEZ, L., SOFÍA, O., LAGUÍA, D., GESTO, E., y HALLAR, K., "Future Internet -

Survey of

IoT technologies",

ICT-UNPA, núm. 256, 2020. Disponible en:

http://doi.org/10.22305/ict-unpa.v12.n3.744.

[11] JAMES, A., HSIEN, W., y MATTHEW, A., "Machine learning: applications of artificial

intelligence to imaging and diagnosis", Biophys Rev, vol. 11, núm. 1, pp. 111–118,

2019. doi: 10.1007/s12551-018-0449-9.

[12] FAZEL, E., NEZHAD, M., ROUHANI, J., MOHAMMADI, M., y ADAMS, J., "IoT

convergence with machine learning & blockchain: A review", Internet of Things, vol. 26,

p. 101187, 2024. http:/doi.org/10.1016/j.iot.2024.101187.

[13] LOIZOU, Konstantinos y KOUTROULIS, Eftichios, "Water level sensing: State of the

art

review and performance evaluation of a low-cost measurement system",

Measurement, vol. 89, pp. 204-214, 2016. doi: 10.1016/j.measurement.2016.04.019.

[14] RUI, L., ARWA, A., ELHOSINY, A., JOFFIN, J., TAMIM, A., FAHAD, A., y HAMID, A.,

"Wireless water consumption sensing system for building energy efficiency: A

visual-based approach with self-powered operation", Energy and Buildings, vol. 301, p.

113584, 15 diciembre 2023. doi: 10.1016/j.enbuild.2023.113584.

[15] MULYANA, Y., y HAKIM, D., "Prototype of Water Turbidity Monitoring System", IOP

Conference Series: Materials Science and Engineering, vol. 384, n.º 1, p. 012052, julio

2018. doi: 10.1088/1757-899X/384/1/012052.

[16] MUHAMMAD, K., KOUSHIK, M., SHOUKAT, R., y HUANG, D., "A review on pH

sensitive materials for sensors and detection methods", Microsystem Technologies, vol.

23, n.º 34–38, octubre 2017. doi: 10.1007/s00542-017-3495-5.

[17] SETIAWAN, E., ANDA, J., HANDANDI, Z., y HIDAYANA, E., "UTILIZING TOTAL

DISSOLVED SOLIDS (TDS) SENSOR FOR DISSOLVED SOLIDS MEASUREMENT IN

THE WATER", JISO Journal of Industrial and Systems Optimization, vol. 7, n.º 1, pp.

22-30, junio 2024. doi: 10.51804/jiso.v7i1.22-30.

[18] WANG, B., CHEN, H., QI, J., PAN, H., LI, B., y FANG, L., "Smart Temperature Sensor

Design and High-Density Water Temperature Monitoring in Estuarine and Coastal

Areas", Sensors,

vol.

23,

n.º

17,

artículo 7659,

septiembre 2023. doi:

10.3390/s23177659.

[19] ESTIGARRIBIA, G.; KENNEDY, C.; GONZALEZ, A.

y CABRIZA, C. Calidad

microbiológica

del

agua

procedente

de

tanques

y

pozos artesianos de

establecimientos sanitarios. Rev. cuba. hig. epidemiol. [online]. 2023, vol.60 [citado

2024-11-03]

.

Disponible

en:

http://scielo.sld.cu/scielo.php?script=sci_arttext&pid=S1561-30032023000100003&lng

=es&nrm=iso. ISSN 1561-3003.

[20] CABEZAS, C. Enfermedades infecciosas relacionadas con el agua en el Perú. Revista

Peruana de Medicina Experimental y Salud Pública [en línea]. 2018, vol.35, n.º 2,

abr./jun. Disponible en: http://dx.doi.org/10.17843/rpmesp.2018.352.3761.

ANEXOS

INFOGRAFÍA

Link:https://www.canva.com/design/DAGW3VIj07I/PKI-Ur_7hT2ILaEmEPjpGA/edit?utm_c
ontent=DAGW3VIj07I&utm_campaign=designshare&utm_medium=link2&utm_source=sha
rebutton

PANTALLAZO DE REUNIÓN

ACTA DE REUNIÓN CON EL EXPERTO

PERFIL DEL EXPERTO:

Docente universitario en Pregrado y Postgrado en diversas instituciones académicas

incluyendo la Universidad Continental desde 2005. Con credenciales académicas de

Doctor en Ingeniería, Magíster en Administración, Ingeniero de sistemas, Bachiller en

Educación y Bachiller en Ingeniería Mecánica. Además, ha sido Director de Servicios

Educativos en la Universidad Continental y ha ejercido como Consultor en Tecnología

de Información y Comunicación.

NOMBRE COMPLETO DEL EXPERTO: Job Daniel Gamarra Moreno

N° DE COLEGIATURA: 68278

Ubicación: J205

Fecha: 13/09/2024

Hora: 6:30 P.M.

Duración: 30 min

HALLAZGOS Y OPORTUNIDADES DE MEJORA

N°

DESCRIPCIÓN

OPORTUNIDAD DE MEJORA

1

Definir Requisitos y Casos de

Asegúrate de documentar

y definir

Uso Claros

claramente los requisitos del sistema y

los casos de uso específicos para los

usuarios en Santa Isabel y Tambo Huari.

Esto

incluye

funcionalidades

de

monitoreo, alertas, y predicciones, así

como los parámetros que se deben

medir (pH,

turbidez,

temperatura, nivel

del agua).

2

Seleccionar Sensores de Alta

Elige sensores de alta precisión y

Calidad y Fiables

confiabilidad para medir los parámetros

del agua. Asegúrate de que los sensores

sean compatibles con tu sistema IoT y

estén calibrados adecuadamente para

obtener datos precisos y consistentes.

3

Implementar un Sistema de

Diseña una arquitectura de backend

Gestión de Datos Eficiente

robusta para manejar y procesar grandes

volúmenes de datos en tiempo real.

Considera el uso de bases de datos

escalables

y

eficientes,

así

como

técnicas

de

almacenamiento

y

recuperación de datos que optimicen el

rendimiento.

4

Aplicar Algoritmos de Machine

Selecciona

y

ajusta

algoritmos de

Learning Adecuados

Machine Learning adecuados para el

análisis de datos del agua. Asegúrate de

que los modelos sean entrenados con

datos representativos y que se validen

regularmente para mantener la precisión

de las predicciones y el análisis.

5

Desarrollar una Interfaz de

Diseña una interfaz web que sea fácil de

Usuario Intuitiva y Responsiva

usar

y

accesible

desde

diferentes

dispositivos,

incluyendo móviles

y

tabletas. La interfaz debe proporcionar

una visualización clara de los datos,

alertas

y

análisis,

así

como

funcionalidades

de

configuración

y

monitoreo.

6

Implementar Mecanismos de

Asegura la protección de los datos y la

Seguridad y Privacidad

privacidad de los usuarios mediante la

implementación

de

protocolos

de

seguridad robustos. Esto incluye cifrado

de datos, autenticación de usuarios y

controles de acceso para proteger

la

integridad y la confidencialidad de la

información.

7

Realizar Pruebas Exhaustivas

Lleva a cabo pruebas exhaustivas del

y Monitoreo Continuo

sistema para identificar y corregir errores

antes del lanzamiento. Una vez en

funcionamiento, implementa un sistema

de monitoreo continuo para asegurar el

buen desempeño del software, la

integridad de los datos y la disponibilidad

del servicio.

EVIDENCIA

Evaluación herramientas por método de factores ponderados

-

Lenguaje de programación

Tabla N° 29. Cuadro de Evaluación herramientas por método de factores

ponderados - Lenguaje de programación

PHP

C#

Java

Porcentaje

Dimensión

Nota Puntaje

Nota

Puntaje

Nota

Puntaje

40%

20%

20%

20%

Funcionalidad

Soporte

Garantía

Disponibilidad

8

7

8

9

3,2

1,4

1,6

1,8

9

7

7

7

3,6

1,4

1,4

1,4

6

7

5

8

2,4

1,4

1

1,6

TOTAL

8

7,8

6,4

-

Framework de programación

Tabla N° 30. Cuadro de Evaluación herramientas por método de factores

ponderados - Framework de programación

Laravel

Django

React

Porcentaje

Dimensión

Nota

Puntaje

Nota

Puntaje

Nota

Puntaje

30%

20%

25%

25%

Disponibilidad

Soporte

Garantía

Funcionalidad

8

7

8

9

2,4

1,4

2

2,25

9

7

7

8

2,7

1,4

1,75

2

6

7

5

8

1,8

1,4

1,25

2

TOTAL

8,05

7,85

6,45

- Base de datos

Tabla N° 31. Cuadro de Evaluación herramientas por método de factores

ponderados - Base de datos

Mongo-DB

MySQL

SQLite

Porcentaje

Dimensión

Nota Puntaje

Nota

Puntaje

Nota

Puntaje

30%

30%

20%

20%

Funcionalidad

Soporte

Garantía

Disponibilidad

7

7

8

9

2,1

2,1

1,6

1,8

9

7

7

8

2,7

2,1

1,4

1,6

6

7

5

8

1,8

2,1

1

1,6

TOTAL

7,6

7,8

6,5

Herramienta Machine Learning

Tabla N° 32. Cuadro de Evaluación herramientas por método de factores

ponderados - Herramienta Machine Learning

Google Collab

TensorFlow

Jupiter

Porcentaje

Criterios

Nota Puntaje

Nota

Puntaje

Nota

Puntaje

30%

30%

20%

20%

Funcionalidad

Soporte

Garantía

Disponibilidad

8

9

9

7

2,4

2,7

1,8

1,4

8

7

7

6

2,4

2,1

1,4

1,2

7

7

5

6

2,1

2,1

1

1,2

TOTAL

8,3

7,1

6,4

- Servidor Web

Tabla N° 33. Cuadro de Evaluación herramientas por método de factores

ponderados - Servidor Web

Apache HTTP

Microsoft IIS

Heroku

Porcentaje

Criterios

Nota Puntaje

Nota

Puntaje

Nota

Puntaje

30%

30%

20%

20%

Funcionalidad

Soporte

Garantía

Disponibilidad

9

8

9

8

2,7

2,4

1,8

1,6

8

7

7

8

2,4

2,1

1,4

1,6

6

7

5

8

1,8

2,1

1

1,6

TOTAL

8,5

7,5

6,5

- Placa de Hardware

Tabla N° 34. Cuadro de Evaluación herramientas por método de factores

ponderados - Placa de Hardware

Rasberry Pi

Arduino

ESP32

Porcentaje

Dimensión

Nota Puntaje

Nota

Puntaje

Nota

Puntaje

30%

20%

25%

25%

Disponibilidad

Procesamiento

Conectividad

Funcionalidad

8

7

8

7

2,4

1,4

2

1,75

9

7

7

8

2,7

1,4

1,75

2

8

7

8

8

2,4

1,4

2

2

TOTAL

7,55

7,85

7,8

Concepción de la Idea del Producto

Sistema de Monitoreo del Consumo, Nivel y Calidad del Agua en Tanques fue

seleccionada de forma unánime por él grupo debido a qué se consideró la idea más

interesante y qué en posterioridad se podría trabajar como instrumento de titulación. A

continuación se muestra los criterios de selección:

1. Sistema Simple de Página Web para la Predicción de Alzheimer

Conocimientos teóricos y técnicos:

● Teóricos:

○ Enfermedad de Alzheimer: Conocimiento sobre los síntomas, etapas y

factores de riesgo asociados a Alzheimer.

○ Machine Learning y Modelos Predictivos: Técnicas y algoritmos para la

predicción de enfermedades basados en datos médicos, como regresión

logística, redes neuronales y análisis de patrones en datos clínicos.

● Técnicos:

○ Desarrollo Web: Conocimientos en HTML, CSS y JavaScript para la

interfaz de usuario.

○ Backend y APIs: Familiaridad con frameworks como Flask o Django en

Python para manejar la lógica de predicción.

○ Bases de Datos: Uso de bases de datos para almacenar datos médicos y

resultados de predicción.

Impacto de la solución a implementar:

● Beneficios: Mejora en la detección temprana y la gestión de la enfermedad de

Alzheimer, proporcionando herramientas para que médicos y pacientes evalúen

riesgos basados en datos históricos y pruebas.

● Impacto Social: Puede contribuir a la salud pública al permitir intervenciones

tempranas y planificación de cuidados.

Preferencia personal por el tema:

● La predicción de enfermedades es un área relevante e interesante, especialmente

en el campo de la salud. La posibilidad de usar tecnología para apoyar la

detección temprana de condiciones graves puede ser altamente gratificante.

Factibilidad técnica de la solución:

● Alta: Utilizando tecnologías web y herramientas de Machine Learning accesibles,

se puede desarrollar un prototipo funcional. La implementación dependerá de la

disponibilidad de datos médicos adecuados y la capacidad para integrar modelos

predictivos en la web.

2. Sistema de Monitoreo del Consumo, Nivel y Calidad del Agua en Tanques

Conocimientos teóricos y técnicos:

● Teóricos:

○ Hidrometría y Control de Calidad del Agua: Conocimiento sobre los

parámetros de calidad del agua, como pH, turbidez, y nivel de

contaminantes.

○ IoT (Internet de las Cosas): Técnicas para la integración de sensores en

redes para monitoreo en tiempo real.

● Técnicos:

○ Hardware: Uso de sensores para medir el consumo, nivel y calidad del

agua. Placas como ESP32 para la conexión y transmisión de datos.

○ Desarrollo Web: Frameworks como Laravel para crear la interfaz web que

visualiza y analiza los datos.

○ Base de Datos: MySQL para almacenar datos históricos y en tiempo real.

Impacto de la solución a implementar:

● Beneficios: Mejora en la gestión del agua al proporcionar datos precisos y en

tiempo real, lo que facilita la toma de decisiones y la implementación de

estrategias de conservación y mantenimiento.

● Impacto Ambiental y Económico: Puede reducir el desperdicio de agua y mejorar la

eficiencia operativa de los sistemas de agua.

Preferencia personal por el tema:

● El monitoreo de recursos naturales es crucial para la sostenibilidad y la gestión

ambiental. Trabajar en este área puede tener un impacto directo en la

conservación del agua, un recurso vital.

Factibilidad técnica de la solución:

● Alta: Con la tecnología de sensores y plataformas web disponibles, el

desarrollo es factible. La integración de hardware con software es compleja

pero manejable con las herramientas actuales.

3. Aplicación para Localizar Restaurantes de Forma Personalizada

Conocimientos teóricos y técnicos:

● Teóricos:

○ Geolocalización y Mapas: Comprender cómo funcionan los servicios de

localización y cómo se integran con aplicaciones móviles y web.

○ Sistemas de Recomendación: Algoritmos para recomendar restaurantes

basados en preferencias personales y comportamientos previos.

● Técnicos:

○ Desarrollo de Aplicaciones: Uso de tecnologías como React Native para

aplicaciones móviles o frameworks web para crear la interfaz.

○ APIs de Localización y Mapas: Integración con APIs de servicios de mapas

como Google Maps para obtener y mostrar ubicaciones.

○ Machine Learning: Implementación de sistemas de recomendación para

personalizar las sugerencias de restaurantes.

Impacto de la solución a implementar:

● Beneficios: Mejora la experiencia del usuario al ofrecer recomendaciones

personalizadas basadas en preferencias y ubicaciones actuales. Facilita la

búsqueda de opciones de restaurantes de manera eficiente.

● Impacto Social: Aumenta la satisfacción del cliente y puede impulsar el negocio de

restaurantes al conectar mejor con los consumidores.

Preferencia personal por el tema:

● El desarrollo de aplicaciones móviles y sistemas de recomendación ofrece una

experiencia directa con la tecnología que puede tener un impacto significativo en la

vida cotidiana de las personas.

Factibilidad técnica de la solución:

● Alta: La tecnología para la localización y los sistemas de recomendación está bien

desarrollada. Con las herramientas y APIs actuales, la creación de una aplicación

funcional es factible y puede ser realizada con los recursos disponibles.

Ideas de Proyecto

1. Título de la Propuesta 1:

Sistema simple de página web para la predicción de Alzheimer

2. Problema / Oportunidad detectado: Describir el problema, es importante

adjuntar alguna fuente estadística.

El problema detectado se enfoca en que el Alzheimer es el problema mental de
demencia más recurrente en el país y que de no atenderse a tiempo puede llevar
a las personas al punto de perder su autonomía para realizar sus actividades de
vida diaria.

De acuerdo al Ministerio de Salud en junio del presente año se atendieron a 7474
casos por demencia donde un 4705 (63%) corresponden a mujeres y 2769 (37%)
a varones; también es bueno mencionar que el año pasado se atendieron 16260
casos.

La intervención en una etapa temprana puede mejorar la calidad de vida del
paciente y también la de su familia; cabe mencionar que es importante educar a la
población sobre estos conceptos, porque los nuevos medicamentos para tratar la
enfermedad funcionan cuando existe un deterioro cognitivo leve y no cuando hay
una demencia determinada.

Fuente estadística:
https://www.gob.pe/institucion/minsa/noticias/968278-minsa-atendio-mas-de-7000-
casos-de-demencia-en-lo-que-va-del-ano-2024

3. Descripción de la solución Propuesta/Investigación a desarrollar:

Elaborar una página web de recolección de datos para analizar las tres principales
variables; niveles bajos de la proteína cistatina C, niveles negativos altos de la
enzima MMP-10 (metaloproteinasa de matriz 10) y niveles altos de proteína tau,
ambas que fueron estudiadas por el laborato.

Estos datos serán recogidos a través de una interfaz y que será rellenada por el
doctor para que compare sus propias conclusiones y las del dispositivo.

Luego se hará uso de machine learning para que se pueda predecir el porcentaje
de que la persona sufra de alzheimer, y de esa manera se pueda llevar a cabo el
tratamiento adecuado por el doctor.

Antecedentes:

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8927715/pdf/fpubh-10-853294.pdf

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8542726/pdf/fpubh-09-751536.pdf

Análisis de la competencia/avances similares

Estado del arte: Nombre una aplicación/investigación/tesis (mínimamente 2)

Sistema de Diagnóstico del Alzheimer basado en Imágenes de Resonancia
Magnética mediante el Algoritmo de redes neuronales VGG16, 2024: Se
recopilaron y procesaron imágenes de resonancia magnética de pacientes con y
sin Alzheimer. Estas imágenes se utilizaron para entrenar al algoritmo, el cual
aprendió a identificar y asociar patrones con la enfermedad. Posteriormente, se
realizaron pruebas con un conjunto de imágenes (de la base de datos Oasis-1
de Alzheimer) no vistas para evaluar la capacidad de diagnóstico del sistema.

Mediante el análisis de las imágenes de resonancia magnética, el algoritmo
VGG16 ha demostrado una capacidad superior al 82% para reconocer
correctamente dichos signos. Estos resultados validan la efectividad del enfoque
basado en inteligencia artificial para el diagnóstico del Alzheimer.

La imagen muestra la clasificación de las categorías de Alzheimer; demencia
mediana = 0, demencia moderada = 1, sin demencia = 2, demencia leve = 3.

En el sistema se sube una imagen y esta da su predicción, en la imagen de
arriba se muestra el resultado de una persona sana: sin alzheimer.

Finalmente, esta imagen muestra que el paciente tiene alzheimer leve.

https://lajc.epn.edu.ec/index.php/LAJC/article/view/379/262

A Predictive and Preventive Model for Onset of Alzheimer's Disease, 2021:

https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2021.751
536/full

1. Título de la Propuesta 2:

Sistema de monitoreo del nivel y calidad del agua en tanques de Chongos Bajo

2. Problema / Oportunidad detectado: Describir el problema, es importante

adjuntar alguna fuente estadística.

Uno de los problemas más preocupantes e importantes a nivel mundial es la
escasez de agua y su contaminación , ya que esta es una fuente importante para
la existencia humana. Asimismo se tiene un ODS 06 que indica garantizar la
disponibilidad y la gestión sostenible del agua y el saneamiento y buena calidad
del agua para todos. Según la ONU : “Más de diez millones de peruanos, el
31,15% de la población, ingiere tóxicos como metales pesados en el agua que
bebe” demostrando que en los últimos años hubo una creciente contaminación del
agua en nuestro país afectando a muchos ciudadanos en su salud y calidad de
vida . Del mismo modo, basado en los datos del último informe sobre la situación
de la pobreza en el Perú INEI, el 73,1% de los peruanos enfrentó la falta de
acceso a agua gestionada de manera segura :

En Junín, muchas áreas enfrentan problemas de acceso a agua potable. La
disponibilidad de agua en las zonas rurales es particularmente preocupante ya que
existe un brecha del 52.07 % , con muchas comunidades dependiendo de fuentes
de agua no siempre seguras o sostenibles.

Los resultados de la tabla 2 (Montero,2021, p. 6 ) , muestran que :

Por ende, la necesidad de mantener altos estándares de calidad para el consumo
del agua y la falta de monitoreo en tiempo real de los niveles de agua en tanques,

son de relevancia para analizar estas problemáticas y proponer una solución
tecnológica, impactando así en la salud pública y en el uso eficiente de este
recurso.

3. Descripción de la solución Propuesta/Investigación a desarrollar:

Desarrollar e implementar un Sistema de monitoreo del nivel y calidad del agua en
tanques en tiempo real el cual contempla la integración de IoT , Big Data , Cloud
Computing , Ciencia de Datos y Machine learning . Para el monitoreo se
desarrollará un arquitectura de hardware usando sensores para capturar cada
métrica como el nivel de Ph, turbidez, temperatura , nivel del agua ,etc. Con ello se
logrará una integración con IoT y guardar los datos en la nube y posteriormente
estos datos se consumirá en un sistema web y móvil. Una funcionalidad relevante
es la implementación de alertas cuando la calidad del agua no esté entre los
estándares y cuando el tanque del agua esté lleno.

Aplicación de Ciencia de datos:

Dar métricas por:

Porcentaje de llenado del tanque

Cantidad de consumo por Litro

Costo de Consumo por Litro

Nivel de Ph

Nivel de turbidez

Nivel de la temperatura

Calidad del agua

Aplicación de Machine Learning:

Predicción de cuánto tiempo durará el agua

Predicción de costos por mes

Predicción de cuanto litros se consume por mes

Predicción de calidad del agua

Diagrama de contexto:

Análisis de la competencia/avances similares

Estado del arte: Nombre una aplicación/investigación/tesis (mínimamente 2)

Aplicaciones :

1. HydroColor

● Versión: 1.2.0
● Año: 2023
● Funcionalidades:

○ Medición de Turbidez: Estima la turbidez del agua en un rango de

0 a 80 NTU.

○ Concentración de Partículas: Calcula la concentración de

partículas suspendidas (SPM) en gramos por metro cúbico.

○ Coeficiente de Retrodispersión: Mide el coeficiente de

retrodispersión en rojo (1/m).

○ Requiere Tarjeta de Referencia: Necesita una tarjeta de referencia

con un 18% de gris para obtener mediciones precisas.

○ Interfaz de Usuario: Permite tomar fotos del agua y analizar los

datos mediante la cámara del teléfono.

2. Water Quality App

● Versión: 1.0.8
● Año: 2023
● Funcionalidades:

○ Registro de Datos: Permite registrar y almacenar datos de calidad

del agua, como pH, turbidez, y temperatura.

○ Integración con sensores: Puede integrarse con sensores externos

para mediciones precisas.

○ Análisis de Datos: Ofrece herramientas para analizar los datos

registrados y generar informes.

○ Historial de Mediciones: Mantiene un historial de mediciones para

monitorear cambios en el tiempo.

3. AquaCheck

● Versión: 2.1.3
● Año: 2023
● Funcionalidades:

○ Pruebas de Calidad: Realiza pruebas para parámetros como pH,

concentración de cloro, dureza del agua, entre otros.

○ Interfaz con Kits de Prueba: Compatible con varios kits de prueba

de agua para una medición más precisa.

○ Informes y Alertas: Genera informes detallados y envía alertas si

los niveles de los parámetros están fuera de rango.

○ Visualización de Datos: Ofrece gráficos y visualizaciones para

interpretar los resultados de manera efectiva.

4. TurbAqua

● Versión: 1.0.5
● Año: 2023
● Funcionalidades:

○ Medición de Turbidez: Utiliza la cámara del teléfono para estimar la

turbidez del agua en unidades NTU (Nephelometric Turbidity
Units).

○ Calibración Automática: Ofrece una función de calibración
automática para mejorar la precisión de las mediciones.

○ Historial de Mediciones: Permite guardar y revisar un historial de
mediciones para el seguimiento de la calidad del agua a lo largo
del tiempo.

○ Informes y Gráficos: Genera informes detallados y gráficos para

facilitar la interpretación de los datos de turbidez.

○ Interfaz de Usuario Amigable: Diseñada para ser fácil de usar,
incluso para aquellos sin experiencia técnica en la medición de
calidad del agua

Artículos :

Low-Cost Internet-of-Things Water-Quality Monitoring System for Rural Areas

https://doi.org/10.3390/s23083919

Real-time water quality monitoring using Internet of Things in SCADA
https://doi.org/10.1007/s10661-018-6914-x

Sistema IoT para el control del nivel de tanques en Aguas de La Habana
https://dialnet.unirioja.es/descarga/articulo/8992128.pdf

“Diseño de una red iot basada en sensores para monitorear el nivel de agua en
un reservorio de espoL”
https://www.dspace.espol.edu.ec/bitstream/123456789/47438/1/D-CD106612.pd
f

1. Título de la Propuesta 3:

Aplicación para localizar restaurantes de forma personalizada

2. Problema / Oportunidad detectado: Describir el problema, es importante

adjuntar alguna fuente estadística.

El problema detectado se enfoca en que la población adulta en el Perú sufre de
problemas de salud debido a la mala alimentación, debido a varios factores, como
estrés por el trabajo y malos hábitos alimenticios.

Según el Ministerio de Salud de Perú, se estima que para 2024, al menos 1 millón
721 mil peruanos padecen de diabetes mellitus.

La diabetes es un problema de salud pública creciente en Perú, y una dieta
adecuada es fundamental para su control.

Fuente estadística:

https://www.gob.pe/institucion/minsa/noticias/32832-cifra-de-diabeticos-aumentaria
-a-mas-de-1-700-000-en-2024

3. Descripción de la solución Propuesta/Investigación a desarrollar:

La app ayudaría al usuario a localizar establecimientos de comida cercanas a él
con las características de platos más similares a las que solicitó, incluso puede
ayudar a los turistas a localizar comida sana de su preferencia en el sitio donde se
encuentre. Ya que estará implementada con IA posteriormente podría recomendar
establecimientos a fin al usuario.Algunas características de la app serían:

-Recomendaciones basadas en el historial a fin de analizar el historial de
búsquedas y visitas del usuario para sugerir restaurantes similares a los que ya le
han gustado.

-Crear perfiles de sabor personalizados basados en las preferencias alimenticias
del usuario, como tipo de cocina, ingredientes favoritos y restricciones dietéticas.

-Ofrecer recomendaciones en tiempo real basadas en la ubicación del usuario y su
historial de movimiento.

Algunas funcionalidades de la aplicación consistirán en:

- Reservas instantáneas que permiten a los usuarios reservar mesa directamente
desde la aplicación, ahorrándoles tiempo y esfuerzo.

-Opiniones y reseñas para fomentar la participación de los usuarios al permitirles
dejar reseñas y calificaciones de los restaurantes.

-Integración con redes sociales para permitir a los usuarios compartir sus
experiencias en redes sociales y descubrir nuevos restaurantes a través de las
recomendaciones de sus amigos.

Análisis de la competencia/avances similares

Estado del arte: Nombre una aplicación/investigación/tesis (mínimamente 2)

1. Yelp: Aunque Yelp es una plataforma norteamericana de reseñas de negocios,
ha evolucionado para incluir filtros muy detallados de búsqueda de alimentos,
incluyendo opciones veganas, vegetarianas, sin gluten, y más. Además, muchos
usuarios comparten fotos de sus platos, lo que permite a otros evaluar
visualmente las opciones disponibles.

2. HappyCow: Esta aplicación se enfoca específicamente en encontrar
restaurantes veganos y vegetarianos. Permite buscar por ubicación, tipo de

cocina y otros filtros, y ofrece información detallada sobre cada restaurante,
incluyendo menús y direcciones.

3. FoodMaestro: Esta aplicación utiliza inteligencia artificial para analizar los
ingredientes de los productos alimenticios y determinar si son adecuados para
personas con alergias o intolerancias alimentarias. También ofrece
recomendaciones de recetas personalizadas.

ACTA DE CONSTITUCIÓN DEL PROYECTO

Nombre del Proyecto/SIGLAS: Desarrollo de un software de consumo,
monitoreo del nivel y calidad del agua en tanques de sistema
educativos (Santa Isabel y Tambo Huari) integrando IoT y Machine
Learning (SYSMONWA).

Fecha:

20/08/2024

Justificación del Proyecto:
El proyecto justifica su desarrollo al garantizar acceso continuo a agua potable segura en
instituciones educativas de Santa Isabel y Tambo Huari. Utilizando IoT y Machine Learning,
permitirá un monitoreo eficiente, prevención de problemas y comparación de prácticas de gestión
hídrica entre escuelas rurales y urbanas, promoviendo la adopción de métodos sostenibles para
mejorar la calidad y el manejo del agua.

Objetivos del Proyecto:

Criterios de Éxito:

- Sistema operativo con monitoreo en tiempo real

de nivel y calidad de agua.

- Alerta por correo cuando el nivel de agua es bajo

o la calidad no es la adecuada.

- Predicciones precisas de consumo de agua y

análisis de calidad utilizando machine learning.

- Exportación de datos históricos para análisis de

tendencias y reportes.

consumo

1.Gestión de datos y visualización
del
-
Administración eficiente en el
clientes,
registro de usuarios,
tanques, sensores y autenticación.

agua

del

2. Reducción de los errores en la
publicación de notas de

prensa, esto se reduce en más de un
90%.

3. Mejora en la calidad de la
publicación de las notas de prensa,

la nota de prensa se publicará de
forma más actualizada.

Breve Descripción del Proyecto

El proyecto consiste en desarrollar un software web para el consumo y monitoreo en
tiempo real del nivel y calidad del agua en tanques de los sistemas educativos de Santa
Isabel y Tambo Huari,
integrando IoT y Machine Learning. Se implementará una
arquitectura de sensores para medir parámetros como pH, turbidez, temperatura y nivel
del agua. Los datos se procesarán y analizarán mediante técnicas de Machine Learning,
proporcionando insights valiosos sobre el consumo y la calidad del agua. El sistema
incluirá alertas para condiciones fuera de los estándares y funciones predictivas,
accesibles a través de una interfaz web responsiva optimizada para diversos
dispositivos..

Productos Entregables Principales del Proyecto

Análisis del proceso, documentación de requerimientos, diseño de solución RPA, prototipo,
implementación piloto, soporte y mantenimiento

Cronograma de Hitos Principales del Proyecto

Fase 1 (PMV1): Monitoreo del consumo de agua (Duración: 4 semanas)

Instalación de sensores y configuración básica de la plataforma web.

Desarrollo de funcionalidad para visualizar el consumo de agua en tiempo real.

Fase 2 (PMV2): Monitoreo del nivel de agua (Duración: 4 semanas)

Implementación de sensores para medir el nivel de agua y alertas de llenado.

Desarrollo de funcionalidad para visualizar datos históricos y emitir alertas automáticas.

Fase 3 (PMV3): Monitoreo de la calidad del agua (Duración: 4 semanas)

Instalación de sensores de calidad (pH, turbidez, temperatura) y desarrollo de algoritmos

de predicción.

Estructura Organizativa del Proyecto

Yerald Cristhian Sinche Alvarado: Líder del proyecto y responsable de la integración de

sensores, conectividad con la plataforma y pruebas de hardware.

José Alejandro Munive Guerra: Desarrollador frontend, encargado de la interfaz web y

diseño de la experiencia del usuario.

Marvin Omar Vilchez De la Cruz: Responsable de machine learning y backend.

Principales Interesados

- Administración de las instituciones educativas de Santa Isabel y Tambo Huari
- Estudiantes y personal de las escuelas
- Autoridades educativas locales y regionales
- Departamento de salud pública local
- Equipo de desarrollo del proyecto
- Proveedores de tecnología (sensores, servicios cloud)
- Municipalidades de Santa Isabel y Tambo Huari
- Padres de familia y comunidad local

Requisitos Generales

- Sistema de sensores para medir pH, turbidez, temperatura y nivel del agua en los

tanques escolares

- Conectividad IoT para transmisión de datos en tiempo real
- Plataforma de almacenamiento y procesamiento de datos
- Aplicación web responsiva para visualización de datos de consumo y calidad
- Sistema de alertas web para condiciones fuera de los estándares de calidad del

agua

- Análisis de datos para métricas de consumo y calidad del agua en entornos

educativos

- Modelos de Machine Learning para predicciones de consumo y calidad
-
- Seguridad de datos y cumplimiento con normativas educativas

Interfaz web intuitiva adaptada a las necesidades de administradores escolares

Supuestos del Proyecto

-

Las escuelas de Santa Isabel y Tambo Huari cuentan con infraestructura básica
para implementar el sistema

- Existe acceso a una red de internet estable en las instituciones educativas
- El personal escolar tiene acceso a computadoras o tablets para usar la aplicación

web

- Hay apoyo de las autoridades locales para la implementación del proyecto
-

Los datos de consumo histórico de agua están disponibles para el entrenamiento
inicial de modelos

- Existe una colaboración efectiva entre el equipo de desarrollo y el personal

escolar

Restricciones del Proyecto

- Variabilidad en la infraestructura de los tanques de agua entre las diferentes

escuelas

- Necesidad de que la interfaz web sea de fácil uso por personal no técnico
Limitaciones en la capacidad de procesamiento y almacenamiento de datos in situ
-
- Requerimiento de que el sistema web sea escalable a otras instituciones

educativas en el futuro

- Necesidad de adaptar el sistema a las condiciones específicas de Santa Isabel y

Tambo Huari
Limitaciones en el ancho de banda de internet disponible en las escuelas

-

Riesgos Principales del Proyecto

Riesgo de conexión inestable: La plataforma requiere una conectividad constante entre los
sensores y Firebase. Si hay problemas de red, los datos no podrán ser transmitidos en tiempo
real.
Falla en los sensores: La precisión de las métricas puede verse afectada si algún sensor
presenta errores o fallas técnicas.
Modelos de predicción inexactos: Los modelos de machine learning podrían no ser precisos en
la fase inicial si no se dispone de suficientes datos históricos para entrenarlos.

Duración Total del Proyecto (Estimado)

La duración estimada del proyecto es de 96 días.

Presupuesto Total del Proyecto (Estimado)

El presupuesto total del proyecto es de s/.1100

Aprobado por:

FRONT IA

Elaborar un breve caso de uso con prediccion de datos con machine learning para una

Sistema Sistema web de monitoreo del consumo, nivel y calidad del agua en tanques de

agua instaladas en una institución educativa

Claro, aquí tienes un caso de uso breve para un sistema web que utiliza machine learning

para monitorear el consumo, nivel y calidad del agua en tanques de agua instalados en

una institución educativa:

### **Caso de Uso: Sistema Web de Monitoreo del Agua "AquaMonitor" para Instituciones

Educativas**

#### **Objetivo:**

Desarrollar un sistema web llamado "AquaMonitor" que utilice machine learning para

monitorear el consumo, nivel y calidad del agua en los tanques de agua instalados en una

institución educativa, con el fin de optimizar el uso del recurso hídrico y garantizar su

calidad.

#### **Usuarios Principales:**

1. **Administradores de la Institución:** Encargados del mantenimiento y gestión de los

recursos hídricos.

2. **Personal de Mantenimiento:** Técnicos responsables del monitoreo y mantenimiento

de los tanques de agua.

3. **Estudiantes:** Usuarios que se benefician de un suministro de agua potable

adecuado y seguro.

#### **Escenario:**

La escuela secundaria "El Saber" utiliza "AquaMonitor" para gestionar el consumo y la

calidad del agua en sus tanques. El sistema permite al personal de mantenimiento recibir

alertas proactivas y realizar ajustes para asegurar que el agua siempre esté disponible y

en buenas condiciones.

#### **Funcionalidades y Predicción de Datos:**

1. **Monitoreo del Nivel de Agua:**

- **Entrada:** Sensores instalados en los tanques de agua envían datos en tiempo real

sobre el nivel del agua.

- **Proceso:** La aplicación web recibe y almacena datos históricos del nivel del agua.

Utiliza modelos de machine learning para analizar patrones de consumo y niveles típicos.

- **Predicción:** Predice posibles niveles bajos de agua en función del consumo

histórico y patrones de uso, generando alertas para evitar desbordamientos o falta de

suministro.

2. **Monitoreo del Consumo de Agua:**

- **Entrada:** Datos de sensores de flujo que registran el consumo de agua en

diferentes áreas de la institución.

- **Proceso:** Los datos de consumo se analizan para identificar patrones y tendencias.

El sistema usa algoritmos de machine learning para detectar anomalías en el consumo

(por ejemplo, picos inesperados).

- **Predicción:** Predice futuras demandas de agua basadas en el consumo histórico y

patrones de uso, ayudando a planificar mejor los recursos y detectar posibles fugas.

3. **Monitoreo de la Calidad del Agua:**

- **Entrada:** Sensores de calidad del agua proporcionan datos sobre parámetros clave

como pH, turbidez, y niveles de contaminantes.

- **Proceso:** La aplicación web analiza los datos de calidad en tiempo real y los

compara con estándares de calidad del agua. Utiliza modelos predictivos para anticipar

cambios en la calidad.

- **Predicción:** Detecta posibles deterioros en la calidad del agua antes de que lleguen

a niveles críticos, emitiendo alertas y recomendaciones para el tratamiento del agua.

4. **Alertas y Recomendaciones:**

- **Entrada:** El sistema genera alertas basadas en las predicciones de los niveles de

agua, consumo y calidad.

- **Proceso:** Las alertas se envían al personal de mantenimiento y administradores

para que tomen acciones correctivas. Las recomendaciones incluyen ajustes en el

suministro de agua y acciones correctivas si se detectan problemas de calidad.

- **Predicción:** Sugiere intervenciones basadas en datos históricos y patrones actuales

para evitar problemas futuros y optimizar la gestión del agua.

#### **Beneficios:**

- **Optimización del Recurso Hídrico:** Mejora la gestión del agua, asegurando un

suministro adecuado y eficiente.

- **Prevención de Problemas:** Anticipa problemas potenciales en el nivel, consumo y

calidad del agua, permitiendo una respuesta proactiva.

- **Seguridad del Agua:** Garantiza que el agua suministrada cumpla con los estándares

de calidad, protegiendo la salud de los estudiantes.

- **Reducción de Costos:** Minimiza desperdicios y costos asociados con el

mantenimiento reactivo mediante una gestión más eficiente.

#### **Desafíos y Consideraciones:**

- **Precisión de los Sensores:** Asegurar la precisión y calibración adecuada de los

sensores de nivel, consumo y calidad del agua.

- **Privacidad y Seguridad:** Proteger los datos del sistema y garantizar la seguridad en la

transmisión y almacenamiento de datos.

- **Mantenimiento del Sistema:** Garantizar que el sistema web y los algoritmos de

machine learning se actualicen regularmente para mantener su precisión y eficacia.

Este caso de uso ilustra cómo un sistema web basado en machine learning puede mejorar

la gestión del agua en una institución educativa, asegurando un suministro adecuado y

seguro a través de un monitoreo y predicción efectivos.

Reporte Turnitin Draft Coach

