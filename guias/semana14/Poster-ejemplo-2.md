> Transcripción del póster ejemplo 2 (Poster2-parte1.png y Poster2-parte2.png, alta resolución; la parte 2 solo contiene el borde inferior del póster). Los textos muy pequeños se marcan como [ilegible] o con «lectura aproximada».

## Maquetación

- Página de la Universidad Continental: logotipo arriba a la izquierda y número de página «92» arriba a la derecha.
- Póster centrado sobre fondo lila/morado claro con una cuadrícula sutil en la esquina inferior derecha.
- Cabecera: título en recuadro blanco redondeado con logotipo tipo emblema a la izquierda e ícono de gota de sangre con latido a la derecha.
- Bajo el título, los autores en una línea centrada, y un recuadro de dos columnas «PROBLEMA» (izquierda) y «OBJETIVOS» (derecha).
- Cuerpo en dos columnas grandes: «METODOS Y MATERIALES» (izquierda) y «RESULTADOS» (derecha), cada una con tres bloques PMV en recuadros blancos redondeados.
- Banda inferior a ancho completo «RESULTADOS Y CONCLUSIÓN», con dos columnas: «Conclusiones» (específicas y generales) y «Recomendaciones».
- Abundantes capturas de pantalla de teléfono móvil, una fotografía de ojo, una salida de código y un mapa de calor. No se distinguen códigos QR.

## Bloques en orden de lectura

**Título**
«Implementación de aplicativo móvil interactivo usando inteligencia artificial para la prevención, evaluación del riesgo de anemia infantil y recomendación de planes nutricionales personalizados en el puesto de salud Tunanmarca en el año 2025»

**Autores**
Acevedo Jordan – Rojas Franklin – Landa Gabriel – Vilcarano Fran [apellido final de lectura aproximada]

**PROBLEMA** (recuadro izquierdo)
Texto de varias líneas: la anemia infantil es un problema crítico de salud pública en el Perú, que afecta el desarrollo físico, cognitivo y emocional de niños menores de cinco años. En el Puesto de Salud de Tunanmarca, la detección temprana es limitada debido a procesos manuales, falta de herramientas tecnológicas y escasa información personalizada sobre nutrición, lo que dificulta el seguimiento y la prevención oportuna de esta enfermedad.

**OBJETIVOS** (recuadro derecho)
Implementar un aplicativo móvil interactivo con inteligencia artificial que permita la prevención y el seguimiento del riesgo de anemia infantil en niños menores de cinco años en el Puesto de Salud de Tunanmarca durante el año 2025. Viñetas: evaluar el riesgo de anemia mediante datos antropométricos e imágenes; generar planes nutricionales personalizados con apoyo de IA; monitorear el estado nutricional del niño mediante seguimiento continuo.

**MÉTODOS Y MATERIALES** (columna izquierda)
- **PMV 1 – Evaluación inicial**: viñetas: registro de usuarios y creación de perfiles; cuestionario dinámico del MINSA; ingreso de peso y talla → cálculo automático del IMC; modelo predictivo de IMC (precisión 92 %). Dos capturas de teléfono con pie: RF-01 registro básico del menor; RF-02 cálculo automático del IMC; RF-03 mostrar nivel de riesgo nutricional.
- **PMV 2 – Análisis inteligente**: viñetas: captura de foto del ojo (conjuntiva); modelo de visión por computadora con TensorFlow Lite; clasificación de palidez (sensibilidad 91 %, especificidad 87 %); diagnóstico automático del riesgo. Figura: fotografía de ojo y dos capturas de teléfono con pie: RF-04 tomar fotografía del ojo; RF-05 analizar la imagen usando IA (modelo CNN); RF-06 mostrar diagnóstico de palidez (leve, moderada, severa).
- **PMV 3 – Nutrición personalizada**: viñetas: generación automática de plan nutricional semanal; recomendaciones con alimentos locales ricos en hierro; descarga del plan en PDF o WhatsApp; dashboard de progreso (peso, talla, riesgo). Dos capturas de teléfono con pie: RF-07 generar menú nutricional según nivel de riesgo; RF-08 descargar menú en PDF.

**RESULTADOS** (columna derecha)
- **PMV 1 – Registro y evaluación inicial**: requisitos funcionales RF-01 a RF-03 e historias de usuario (madre o padre que registra los datos del hijo; usuario que recibe una clasificación fácil de entender). Figura: diagrama de visualización de datos y bloque «ML (Modelo de Machine Learning)»: modelo predictivo de IMC con precisión del 92 %.
- **PMV 2 – Análisis inteligente**: requisitos RF-04 a RF-06 e historias HU-03 y HU-04. Bloque de salida de consola con «AUC (test): 0.2500», matriz de confusión [[0 2] [0 4]], Accuracy 0.6667, Precisión 0.6667 y F1 0.8000 (lectura aproximada). Texto del modelo CNN: precisión global cercana al 90 %, especificidad 87 %, tiempo de procesamiento de 1.8 a 3 s en celulares de gama media, capaz de identificar anemia leve con alta fiabilidad [lectura aproximada].
- **PMV 3 – Nutrición personalizada con análisis inteligente**: requisitos RF-07 y RF-08 e historias HU-02 y HU-06 (menú semanal adecuado al estado del hijo; compartir la recomendación con otros familiares o cuidadores). Figura: mapa de calor. Bloque «ML / Lógica inteligente»: mejor coherencia nutricional y menús adaptados al nivel de riesgo, disponibilidad local y edad del niño; aumento de la adherencia por comprensión del menú (evaluado en pruebas piloto) [lectura aproximada].

**RESULTADOS Y CONCLUSIÓN** (banda inferior)
- *Conclusiones específicas* (3): el análisis antropométrico y la visión por computadora mejoran la precisión en la detección del riesgo de anemia infantil; los planes nutricionales personalizados basados en alimentos locales incrementan la adherencia de los usuarios; la app facilita el uso y la comprensión incluso en padres con baja alfabetización digital.
- *Conclusiones generales* (2): el aplicativo con IA es una herramienta efectiva, accesible y novedosa para la prevención y seguimiento de la anemia infantil; la integración de evaluación, análisis visual y recomendaciones nutricionales contribuye directamente a mejorar la salud infantil en comunidades rurales.
- *Recomendaciones*: **Capacitación**: implementar sesiones de enseñanza sobre el uso de la app y la importancia de la alimentación rica en hierro. **Integración con el sistema de salud local**: escalar reportes automáticos de niños en riesgo desde la app hacia el sistema de monitoreo del puesto de salud [lectura aproximada].

**Referencias y agradecimientos**: no se distinguen en la imagen.
