## Resumen para el equipo: hallazgo del Congreso de Ingeniería y cambio CHG-001-2026

**Ponencia elegida:** «Tecnología satelital y su impacto en ciudades inteligentes y sostenibilidad urbana», del Ing. Alejandro Manuel Martínez (decano de Ingeniería de la UBA), en el VIII Congreso Internacional de Ingeniería y Arquitectura.

### Qué dijo la ponencia (lo que nos sirve)

- Los satélites meteorológicos y de observación, combinados con IA, permiten pronosticar fenómenos (incendios, inundaciones, clima urbano) más rápido que los métodos tradicionales.
- El gran reto es reducir el tiempo entre que el satélite capta el dato y el dato llega a tierra, para tener información «en línea».
- El GPS sincroniza los relojes de las redes eléctricas y de telecomunicaciones: muchos servicios dependen de una marca de tiempo común.

### El hallazgo para Green AI

Nuestro modelo de energía $P(u)$ solo cuenta los servidores. Un centro de datos también gasta energía en **refrigeración**, que depende de la **temperatura exterior**. En la práctica asumimos un PUE de 1,0, mientras que el promedio mundial reportado por el Uptime Institute en 2024 es de 1,56; es decir, hay una causa de consumo que no estamos modelando. La ponencia muestra que existen datos climáticos satelitales abiertos que pueden cubrir esa brecha.

### El cambio propuesto (CHG-001-2026)

- **Qué:** traer la temperatura exterior horaria desde la API gratuita de NASA POWER (datos derivados de satélite), estimar el PUE y la energía de refrigeración (etiquetadas como «modeladas») y probar si la temperatura mejora la predicción.
- **Historias nuevas:** HU-17 (ver clima y refrigeración estimada en el dashboard; si la API falla, se muestra «no disponible» y todo sigue funcionando) y HU-18 (comparar el modelo con y sin temperatura; se adopta solo si baja el MAE).
- **Arquitectura hexagonal:** un puerto nuevo `ClimaExternoPort` en Prediction y dos adaptadores: `NasaPowerClimaAdapter` (real) y `ClimaSinteticoAdapter` (para pruebas sin internet). El dominio no cambia.
- **Cuándo:** PMV3, Sprint 8, después de cerrar los pendientes de seguridad F-01 (RLS de Supabase) y F-03 (sesión real).
- **Esfuerzo:** 26 horas-hombre estimadas.
- **Dictamen del CCB:** aprobado y planificado. **Todavía no está implementado.**

### Qué cambió en el informe final

- Nueva sección §VII.8 con la ficha del cambio CHG-001-2026 y dos referencias nuevas: [15] Uptime Institute y [16] NASA POWER.
- Una línea nueva en «Trabajo futuro» para implementar el cambio.
- Anexo E con la foto de participación en el congreso.

### Qué debe hacer cada uno

- **Todos:** leer este resumen y la sección §VII.8 antes de la sustentación. Si alguno asistió a otra ponencia, envíe su captura para sumarla al Anexo E.
- **Si se pregunta en la sustentación:** el cambio está aprobado, pero no implementado. No es un resultado medido, sino una mejora planificada.

Archivos: informe del congreso en `exportados/semana15/Porras-Huaman-Barrera-Quintana-informe-congreso.pdf`; informe final en `exportados/semana15/Porras-Huaman-Barrera-Quintana-informe-unidad-IV.pdf`.
