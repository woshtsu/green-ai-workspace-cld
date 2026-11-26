"""Genera entregables/semana15/informe-unidad-IV.md a partir del informe corregido de la Unidad III,
aplicando las mejoras de prioridad Alta del reporte ICACIT (semana 14) y los resultados del PMV3 (Sprint 7).
Uso: python herramientas_IA/exportacion/construir_informe_iv.py
"""
from pathlib import Path
import re

R = Path(__file__).resolve().parents[2]
src = (R / "entregables/informe-corregido/informe-unidad-III.md").read_text(encoding="utf-8")
out = R / "entregables/semana15/informe-unidad-IV.md"
ext = (R / "herramientas_IA/exportacion/informe_iv_secciones.md").read_text(encoding="utf-8")
S = {}
for bloque in re.split(r"^<<<(\w+)>>>\s*$", ext, flags=re.M)[1:]:
    pass
partes = re.split(r"^<<<(\w+)>>>\s*$", ext, flags=re.M)
for i in range(1, len(partes), 2):
    S[partes[i]] = partes[i + 1].strip("\n")

t = src
t = t.replace("](evidencias/", "](../informe-corregido/evidencias/").replace("](evidencias-nube/", "](../informe-corregido/evidencias-nube/")


def rep(old, new, count=1):
    global t
    if old not in t:
        raise SystemExit(f"No encontrado: {old[:80]!r}")
    t = t.replace(old, new, count)


def rep_linea(prefijo, nueva):
    global t
    lineas = t.split("\n")
    idx = [i for i, l in enumerate(lineas) if l.startswith(prefijo)]
    if len(idx) != 1:
        raise SystemExit(f"Línea {prefijo!r}: {len(idx)} coincidencias")
    lineas[idx[0]] = nueva
    t = "\n".join(lineas)


def rep_bloque(inicio, fin, nuevo):
    """Reemplaza desde la línea que empieza por `inicio` hasta antes de la que empieza por `fin`."""
    global t
    a = t.index("\n" + inicio) + 1
    b = t.index("\n" + fin, a) + 1
    t = t[:a] + nuevo.rstrip("\n") + "\n\n" + t[b:]


# Carátula
rep("Taller de Proyectos 1 · Informe de la Unidad III (semanas 9–12)", "Taller de Proyectos 1 · Informe final de la Unidad IV (semanas 13–16)")
rep("Versión corregida tras la revisión docente – noviembre de 2026", "Informe final del proyecto (PMV1, PMV2 y PMV3) – 25 de noviembre de 2026")

# Resumen y abstract
rep_bloque("## RESUMEN EJECUTIVO", "## ABSTRACT", S["resumen"])
rep_bloque("## ABSTRACT", "# I. ANÁLISIS DEL PROBLEMA", S["abstract"])

# Dato 1 000 a 8 000 (ICACIT Alta 5)
rep("a picos de 8 000 concurrentes, motivando incrementos reactivos de capacidad en nube.",
    "a picos de 8 000 concurrentes, motivando incrementos reactivos de capacidad en nube (dato **referencial no verificado**: proviene de registros públicos no archivados y no se dispone de una fuente citable en ISO 690; se conserva solo como contexto y no sustenta ningún resultado del proyecto).")

# OE4 ya ejecutado
rep("Este objetivo se encuentra **planificado** para los Sprints 7 y 8 (17/11–30/11/2026).",
    "Este objetivo se ejecutó en el Sprint 7 (17/11–23/11/2026) y se cierra en el Sprint 8; sus resultados reales, incluidos los pendientes, se reportan en §VIII.2.3.")

# ODS 13 (ICACIT Alta 2)
rep_linea("- **ODS 13 (Acción por el clima):**", S["ods13"])

# Tabla 4 (ICACIT Alta 1)
rep_linea("| **Ley N.° 29733", S["t4_29733"])
rep_linea("| **Ley N.° 30096", S["t4_30096"])
rep_linea("| **ISO/IEC 21031:2024", S["t4_iso"])
rep("Asimismo, se detectó en snapshots históricos un riesgo de políticas RLS excesivamente permisivas en Supabase, el cual se documenta formalmente para su corrección estricta en el entorno productivo.",
    "Asimismo, la ingeniería inversa (Unidad IV) registró dos hallazgos críticos de seguridad: H-01 (los servicios Prediction y Data Processing pueden invocarse en Render sin pasar por el Gateway) y H-02 (políticas RLS «Permitir todo» y columna `password` en texto plano según el snapshot del repositorio). H-01 está mitigado de forma parcial con el secreto compartido del Gateway en las rutas de decisiones; H-02 no está verificado ni corregido en Supabase a la fecha de corte (25/11/2026). Su estado y plan se detallan en §VIII.2.3.")

# PMV3: sección completa con resultados reales
rep_bloque("#### VIII.2.3. Pruebas del PMV3", "#### VIII.2.4.", S["pmv3"])

# Tabla 32 (ICACIT Alta 3)
rep_bloque("| Dimensión de prueba | Entornos probados |", "---", S["t32"])

# Tabla 33 (ICACIT Alta 1)
rep_linea("| Pipeline ETL y limpieza |", "| Pipeline ETL y limpieza | Tratamiento de brechas temporales (3,2 % nulos) | PMV1 | Demostrado | Suite Data Processing (128 aprobadas y 8 omitidas al 19/11/2026) | Interpolación lineal en brechas breves (< 1 min) e imputación por mediana. 0,0 % nulos post-tratamiento. |")
rep_linea("| Prediction Service |", "| Prediction Service | API REST de inferencia de demanda | PMV2 | Demostrado | Microservicio FastAPI; 116 pruebas aprobadas al 19/11/2026 | Endpoints `/v1/predictions` y `/v1/recommendations`. Latencia mediana de 97 ms con un usuario; 1,14 s con 8 concurrentes (cuello de botella H-03, ingeniería inversa). |")
rep_linea("| Frontend Web |", "| Frontend Web | Interfaz de visualización y control | PMV1–3 | Demostrado | GitHub Pages (`dev/`); 63 pruebas Node al 19/11/2026 | Interfaz HTML/JS estática (Racks, Métricas, Detalle, Flujos), tabla accesible (U-02) y etiquetas «modelada/estimada» (F-06). Sin escaneo axe/Lighthouse ni validación con sesión real (F-03 parcial). |")
rep_linea("| Reportes estructurados |", "| Reportes estructurados | Resumen histórico descargable | PMV2–3 | Demostrado | `/reports/historical-summary` (JSON, CSV y PDF desde el Sprint 7) | PDF con la leyenda «Datos simulados; energía modelada, no medida»; desplegado en Render el 25/11/2026. |")
rep_linea("| Control perimetral (RBAC) |", "| Control perimetral (RBAC) | Roles de seguridad en API Gateway | PMV2–3 | Demostrado en el Gateway; elusible en la nube (H-01), mitigado parcialmente | Gateway Java (19 pruebas) y Gateway Go (40 pruebas); secreto `X-Green-Gateway-Secret` | ADMIN, OPERATOR y VIEWER con validación JWT. Prediction y Data Processing siguen siendo accesibles directamente en Render; solo las rutas de decisiones exigen el secreto del Gateway (401 sin él, verificado el 25/11/2026). |")
rep_linea("| Experimento comparativo |", "| Experimento comparativo | Aprovisionamiento reactivo vs predictivo | PMV3 | Demostrado | Manifiesto de experimento en test set ($n = 126$) | Margen 10 % reduce riesgo de SLA de 15,9 % a 9,5 % (−6,35 pp). Energía modelada −0,16 % (sin ahorro probado). |\n"
          "| Decisión humana (HU-07) | Aprobar o rechazar recomendaciones con auditoría | PMV3 | Demostrado (persistencia efímera) | Rutas `/v1/recommendations/{id}/decisions`; 16 pruebas en Prediction | Registro con usuario, rol, comentario y SHA-256; `executionAllowed=false`. En Render se guarda en SQLite efímero: la migración a Supabase no está aplicada. |\n"
          "| Seguridad de datos (RLS) | Políticas RLS y columna `password` en Supabase (F-01 / H-02) | PMV3 | Parcial / pendiente | Snapshot del repositorio; captura S11 y S12 (semana 13) | Requiere acceso administrativo a Supabase; no verificado ni corregido al 25/11/2026. |\n"
          "| Sesión real en el dashboard | Validación con cuenta del equipo (F-03) | PMV3 | Parcial | Captura S13 (semana 13) | Sesión en `localStorage`; falta la validación de punta a punta con sesión real de Aprobar/Rechazar, PDF y tabla accesible. |")

# Conclusiones y limitaciones
rep_bloque("#### Conclusión del objetivo específico 4 de proceso", "---", S["concl_oe4"])
rep("- Los procesos del PMV3 y sus métricas están planificados y aún sin evidencia de ejecución a la fecha de corte.",
    "- Seguridad parcial: H-01 solo mitigado en las rutas de decisiones y H-02 (RLS y columna `password`) sin verificar en Supabase; la auditoría final dictamina «no apto para producción».\n- Las decisiones HU-07 se guardan en SQLite efímero en Render y se pierden al reiniciar el servicio.\n- La prueba con usuarios finales y su acta están pendientes de registro por el equipo.")
rep("- Culminar la exportación automatizada de reportes consolidados en formato PDF para auditorías técnicas (fuera del alcance del periodo lectivo).\n",
    "- Aplicar la migración `001_recommendation_decisions.sql` en Supabase, endurecer RLS y retirar la columna `password` (F-01), y validar el dashboard con sesión real (F-03).\n- Volver privados Prediction y Data Processing o exigir el secreto del Gateway en todas sus rutas, e implementar *rate limiting* y auditoría de 401/403 (OW-05, OW-12).\n")

# Anexo A: video (sin cambios respecto a la Unidad III) y póster
rep("* **Video de sustentación de la Unidad III (Google Drive):**",
    "* **Video demostrativo del producto (Google Drive; es el mismo video entregado en la Unidad III, sin cambios para la Unidad IV):**")
rep("* **Formulario de consulta con el experto temático:**",
    "* **Póster científico del proyecto (Unidad IV):** `exportados/semana15/poster-green-ai.pdf` (fuente editable en `entregables/semana15/poster/`).\n\n* **Formulario de consulta con el experto temático:**")

t = t.rstrip("\n") + "\n\n" + S["anexo_d"] + "\n"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(t, encoding="utf-8")
print("OK", out, len(t.split()), "palabras")
