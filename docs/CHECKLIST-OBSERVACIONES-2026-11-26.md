# Checklist de observaciones pendientes (corte 26/11/2026)

Para continuar en otra PC y otro chat. Entrega aproximada: **primera semana de diciembre de 2026** (el 26/11 el usuario indicó «en 1 semana»).

Fuentes: observaciones del docente, [reporte ICACIT](../entregables/semana15/reporte-icacit.md) (§5 y §6), [auditoría del informe](evidencias/auditoria-20261126/auditoria-informe.md) y [auditoría ICACIT](evidencias/auditoria-20261126/auditoria-icacit.md). Las líneas «L…» corresponden al informe del commit `9e2d172`; buscar por texto si se desplazaron. La auditoría del informe es **anterior** a las correcciones: usarla sobre todo para la lista de capturas.

## 0. Antes de empezar
- [ ] `git checkout test && git pull --ff-only`; leer `AGENTS.md`, `docs/CONTINUAR-EN-NUEVO-CHAT.md` y este archivo.
- [ ] La fuente de verdad del informe es `entregables/semana15/informe-unidad-IV.md` (editar a mano; **no** correr `construir_informe_iv.py --forzar`).
- [ ] `.tools/` no está en Git: recrear el entorno de exportación (`herramientas_IA/README.md`); el QR del póster ya está guardado como SVG (`segno` solo si se regenera).

## Decisiones del usuario (no volver a preguntar)
- Por ahora el informe se corrige solo en Markdown; el avance de software viene después.
- Cap. VI con wireframes; prototipos = wireframes; capturas reales solo en pruebas.
- 4 conclusiones (una por objetivo específico); discusión en párrafos; referencias solo al final.
- FURPS+/OWASP oficial: semana 13 (86 %, 83,5, «apto con observaciones») + correcciones posteriores.
- Contraseñas de Supabase: «ya corregido» (falta evidencia). Usuarios finales: **se mantiene como pendiente**.
- Adaptador Supabase de HU-07: programar después; mientras, enlazar los existentes.
- **El dataset de 14 días / 80 640 muestras NO existe** (confirmado 26/11).

## 1. Correcciones de texto en el informe (se pueden hacer ya)
- [ ] **1. CRÍTICO, dataset:** `software/prediction/data/raw/sample_dataset.json` tiene 864 registros cada 5 min, 01–03/09/2026, un nodo (comprobado). Corregir L2293, tabla de L2497–2506 (80 640 / 78 059 / 96,8 %), L2990; revisar el texto y la Figura VIII.11 (L2489–2495) y buscar «80 640», «14 días», «15 segundos» en informe y póster.
- [ ] **2.** Variables del modelo (L230–231, L2962, L2991): retardos 1–3 solo de CPU, ventanas de 15 y 30 min (`software/prediction/config/config.yaml`).
- [ ] **3.** Rendimiento: p95 de 3,5 s con concurrencia 3 (L2731) frente a RNF-02 < 2 s (verificar en `docs/evidencias/carga-video.csv`); HU-03 «Parcial» en la nube; contrastar con H1 (L2319, L2419); añadir tabla de verificación de RNF-01 a RNF-09.
- [ ] **4.** Texto alternativo de imágenes con numeración antigua (L2178, L2216, L2663, L2697–2713; revisar L1900, L1954, L2099, L2105, L2134): Word lo imprime como leyenda.
- [ ] **5.** Figuras VIII.12–14 (L2592–2602) son hojas de cálculo sintéticas, no tablas de PostgreSQL: rotularlas así.
- [ ] **6.** Tapar contraseñas (Figura VIII.13 y script del Anexo B, ~L3305) y correos (Figuras VIII.15.c–e).
- [ ] **7.** L403 y L2366: retirar límites de memoria no hallados y «límites de tasa»; cadencia real de 15 s.
- [ ] **8.** L2768 y L2942: la latencia es H-04, no H-03.
- [ ] **9.** (confirmar) Unificar Scrum/Scrumban (L464, L1856), duración de sprints, total y nombres de HU (L2156, L2186–2187).
- [ ] **10.** L2772: «Video y póster» = Parcial (el video es el de la Unidad III).
- [ ] **11.** Versiones: Spring Boot 4.1.1 y Go 1.25 (L509–511, L2039); aclarar que `render.yaml` despliega el gateway Go (Tabla 8).
- [ ] **12.** Añadir PE4, responder PE3 en §X.1 y quitar «físico» de OE3 (L186–200).
- [ ] **13.** Referencias: citar o retirar [4], [5], [8], [9]; citar [14] en el cuerpo; ordenar por aparición; fecha de consulta en [15] y [16].
- [ ] **14.** (confirmar) P_idle 300 W / P_max 600 W como supuestos con fuente o sensibilidad (L2894).
- [ ] **15.** Añadir: matriz de impactos y ética de IA (falsos positivos/negativos), ODS → meta → indicador → evidencia, conocimiento → decisión de diseño, causa → RF/HU.
- [ ] **16.** (confirmar) Expansión de la sigla AGEN contra su fuente (L2991).
- [ ] **17.** L3096: beneficio no medido, no «evitado».
- [ ] **18.** (preguntar) Declaración de uso de IA: hoy el asistente figura bajo «Integrantes» (L45).
- [ ] **19.** Cerrar huecos de numeración (Figuras VIII.35–37; VIII.32 solo en texto alternativo).
- [ ] **20.** Tablas 35, D.1 y D.2: reflejar las brechas del ICACIT; Anexos A–H.
- [ ] Frases «planificado» / «olas 2 y 3» que contradicen lo ya hecho (junto con la tarea 31).

## 2. Póster
- [ ] **21. NUEVO (docente, 26/11):** agregar una imagen del MVP, la más representativa, o una por cada MVP si cabe de forma adecuada (propuesta: una por PMV usando capturas reales o los wireframes de `entregables/semana15/wireframes/`; confirmar con el usuario cuál). Fuente `entregables/semana15/poster/poster-green-ai.html`; exportar con `bash herramientas_IA/exportacion/render_poster.sh` y verificar 1 página sin solapes. Luego actualizar la imagen en el informe (usa el mismo PNG).
- [ ] **22.** Incorporar lo que diga la revisión del póster del 26/11.
- [ ] **23.** Confirmar nombres abreviados (Porras R., Huamán L., Barrera G., Quintana J.), logo del proyecto (hecho desde el favicon), escanear el QR, permisos del Drive, imprimir prueba (referencias bajo 18 pt) y decidir si falta un libro técnico en referencias.
- [ ] **24.** Revisar que el póster no contradiga las correcciones 1–3 (dataset: la Tabla de la Unidad I habla de 100 000 registros y «80 640 muestras» en la PoC).

## 3. Trabajo del equipo (otra PC, con sesiones propias)
- [ ] **30.** Recapturar evidencias **mostrando el link**: Cap. VI retiradas ahora en VIII.15.a–g, Fig. 8–9 antiguas, Trello VII.6.3–6.9, Cap. VIII y Anexo A.2–A.9 (algunas con repositorios o Render antiguos). Lista por archivo en la auditoría, sección f (numeración anterior). Preguntar si las capturas de consola también requieren URL.
- [ ] **31.** % de avance del PMV y **Gantt ejecutado** (fuente `entregables/informe-corregido/fuentes/gantt_render.py`, corte 11/11: PMV1 13/13, PMV2 8/13, PMV3 0/14); confirmar Sprints 7–8 y Trello; corregir «Cluster Kubernetes desplegado» marcado como completado; actualizar Tablas 23–24.
- [ ] **32.** Evidencia de la corrección de `password` y restricción de RLS (rol de solo lectura para históricos).
- [ ] **33.** Validar puntajes de factores ponderados (Tablas 3.a–3.d y 8.1–8.47).
- [ ] **34.** Usuarios finales y acta (pendiente declarado; no fabricar). Revisar pie y enlace de la Figura A.1.
- [ ] **35.** Confirmar si existe el artículo en inglés (OE4) y a qué «6 competencias» se refería el docente (el sílabo tiene 4 transversales + 3 específicas; una guía S6 menciona C1–C6).
- [ ] **36.** Validar P_idle/P_max y factor de emisión del SEIN.

## 4. Software (posterior)
- [ ] **40.** Adaptador Supabase para decisiones HU-07, migración `001_recommendation_decisions.sql`, pruebas, Anexo G.
- [ ] **41.** Sesión real (F-03), cierre de H-01, latencia H-04 y nueva medición frente a RNF-02.
- [ ] **42.** (opcional) Tasa de falsos positivos: ver nota abajo.

## 5. Cierre
- [ ] **50.** Reexportar Word y PDF (`md_a_docx.py`, `actualizar_word.ps1`; revisar índices y tamaño del póster). Los de `exportados/semana15/` son **anteriores** a las correcciones.
- [ ] **51.** Volver a ejecutar el ICACIT sobre el PDF nuevo y actualizar el reporte.
- [ ] **52.** HANDOFF, CONTINUAR, commit; `test` → `main` solo con autorización.

## Nota para la exposición (pregunta del docente: falsos positivos)
Hoy **no se mide** la tasa de falsos positivos. Es regresión de CPU a 15 min, evaluada con MAE/RMSE/sMAPE frente a persistencia, con datos simulados; toda recomendación requiere aprobación humana. Para medirla: positivo = CPU predicha > T (p. ej. 80 %), comparar con la real en t+15 y calcular FPR = FP/(FP+VN), precisión y recall. Con los datos actuales no sería concluyente (2 de 864 filas superan 80 %). `eligible_for_review` indica frescura y restricciones cumplidas, no acierto.
