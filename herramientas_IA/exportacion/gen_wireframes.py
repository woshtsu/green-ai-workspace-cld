"""Genera los wireframes SVG y los renderiza a PNG con Edge headless."""
from pathlib import Path
from html import escape
import subprocess, tempfile

OUT = Path(__file__).resolve().parents[2] / "entregables" / "semana15" / "wireframes"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
INK, MID, LINE, SOFT, PAGE = "#222222", "#666666", "#999999", "#e6e6e6", "#f7f7f7"


class W:
    def __init__(s, w, h):
        s.w, s.h, s.e = w, h, []
        s.rect(1, 1, w - 2, h - 2, PAGE, MID)

    def rect(s, x, y, w, h, fill="#ffffff", stroke=LINE, r=4, dash=False):
        d = ' stroke-dasharray="6 4"' if dash else ""
        s.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>')

    def line(s, x1, y1, x2, y2, c=LINE, sw=1.5, dash=False):
        d = ' stroke-dasharray="6 4"' if dash else ""
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"{d}/>')

    def poly(s, pts, c, sw=2, dash=False):
        d = ' stroke-dasharray="7 5"' if dash else ""
        s.e.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="{sw}"{d}/>')

    def text(s, x, y, t, size=16, c=INK, bold=False, anchor="start", under=False, italic=False):
        a = (' font-weight="bold"' if bold else "") + (' text-decoration="underline"' if under else "") + (' font-style="italic"' if italic else "")
        s.e.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" text-anchor="{anchor}"{a}>{escape(t)}</text>')

    def button(s, x, y, w, t, primary=False, h=38, size=15):
        s.rect(x, y, w, h, "#555555" if primary else "#ffffff", "#444444")
        s.text(x + w / 2, y + h / 2 + 5, t, size, "#ffffff" if primary else INK, True, "middle")

    def field(s, x, y, w, t, select=False, h=36, size=15):
        s.rect(x, y, w, h)
        s.text(x + 12, y + h / 2 + 5, t, size, MID)
        if select:
            s.text(x + w - 12, y + h / 2 + 5, "▾", 15, MID, anchor="end")

    def n(s, x, y, num):
        """Rótulo numerado."""
        s.e.append(f'<circle cx="{x}" cy="{y}" r="13" fill="#000000" stroke="#ffffff" stroke-width="2"/>')
        s.text(x, y + 5, str(num), 15, "#ffffff", True, "middle")

    def save(s, name):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}" '
               f'font-family="Segoe UI, Arial, sans-serif">\n' + "\n".join(s.e) + "\n</svg>\n")
        p = OUT / f"{name}.svg"
        p.write_text(svg, encoding="utf-8")
        with tempfile.TemporaryDirectory() as prof:
            subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                            f"--user-data-dir={prof}", f"--window-size={s.w},{s.h}",
                            f"--screenshot={OUT / (name + '.png')}", p.as_uri()], check=True, capture_output=True, timeout=90)


OUT.mkdir(parents=True, exist_ok=True)

# 00 Inicio (index.html)
w = W(1000, 620)
w.rect(40, 24, 920, 56)
w.text(60, 59, "Green AI Cyber Ops", 19, bold=True)
for x, t in [(420, "Inicio"), (500, "Dashboard"), (620, "Login"), (700, "Registro")]:
    w.text(x, 58, t, 15, under=(t == "Inicio"))
w.button(820, 34, 124, "Tema claro", h=36)
w.n(40, 24, 1)
w.rect(40, 100, 920, 300)
w.text(70, 140, "ESTACIÓN DE OPERACIÓN", 14, MID, True)
w.text(70, 184, "Plataforma Green AI para", 31, bold=True)
w.text(70, 222, "data centers inteligentes.", 31, bold=True)
w.text(70, 258, "Consulta CPU, memoria, red y almacenamiento por nodo.", 16, MID)
w.text(70, 282, "Valores actuales e histórico con la procedencia de cada medición.", 16, MID)
w.button(70, 304, 170, "Iniciar sesión", True)
w.button(256, 304, 150, "Registrarse")
w.n(70, 304, 2); w.n(406, 304, 3)
for x, t in [(70, "Acceso autenticado"), (260, "Métricas por nodo"), (450, "Histórico disponible")]:
    w.rect(x, 358, 175, 28, SOFT); w.text(x + 87, 377, t, 14, anchor="middle")
w.rect(680, 125, 250, 250, SOFT)
w.line(680, 125, 930, 375); w.line(930, 125, 680, 375)
w.rect(735, 232, 140, 34); w.text(805, 254, "Ilustración", 15, MID, anchor="middle")
for i, (t, a, b) in enumerate([("Telemetría en tiempo real", "CPU, memoria, red y disco.", "Actualización cada 30 segundos."),
                               ("IA predictiva", "Rótulo «En desarrollo»:", "predicciones y recomendaciones."),
                               ("Infraestructura resiliente", "Rótulo «En desarrollo»:", "inventario y topología.")]):
    x = 40 + i * 312
    w.rect(x, 424, 296, 130); w.rect(x + 18, 440, 30, 30, SOFT)
    w.text(x + 18, 498, t, 17, bold=True); w.text(x + 18, 522, a, 14, MID); w.text(x + 18, 542, b, 14, MID)
w.n(40, 424, 4)
w.text(500, 592, "© 2026 Universidad Continental | Proyecto Green AI | Ley N° 29733", 14, MID, anchor="middle")
w.save("wf-00-inicio")


def auth(name, brand, title, sub, fields, button, footer, link, msg, note=None):
    h = 360 + len(fields) * 52 + (36 if note else 0) + 60
    w = W(640, h)
    w.rect(90, 24, 460, h - 48)
    w.text(120, 66, brand, 20, bold=True)
    w.rect(390, 48, 52, 26, SOFT, r=13); w.e.append(f'<circle cx="403" cy="61" r="10" fill="{MID}"/>')
    w.text(522, 66, "← Volver", 15, anchor="end")
    w.n(90, 61, 1)
    w.text(320, 124, title, 28, bold=True, anchor="middle")
    w.text(320, 154, sub, 15, MID, anchor="middle")
    y = 180
    for i, f in enumerate(fields):
        w.field(120, y, 400, f, h=40, size=16)
        w.n(90, y + 20, i + 2)
        y += 52
    k = len(fields) + 2
    if note:
        w.text(120, y + 14, note, 15, MID); y += 36
    w.button(120, y + 4, 400, button, True, h=44, size=17)
    w.n(90, y + 26, k)
    w.rect(120, y + 68, 400, 40, SOFT, dash=True)
    w.text(320, y + 93, msg, 14, anchor="middle")
    w.n(90, y + 88, k + 1)
    w.text(320, y + 146, footer + " ", 15, MID, anchor="end")
    w.text(326, y + 146, link, 15, under=True)
    w.n(90, y + 141, k + 2)
    w.save(name)


auth("wf-01-registro", "Green AI", "Crear Cuenta", "Registra un operador para acceder a paneles, métricas y topología.",
     ["Nombre completo", "Correo institucional", "Contraseña", "Confirmar contraseña"], "Registrar operador",
     "¿Ya tienes una cuenta?", "Iniciar sesión", "Revisa tu correo y confirma la cuenta antes de iniciar sesión.",
     "Tu cuenta recibirá los permisos asignados por el sistema.")
auth("wf-03-login", "Green AI", "Iniciar Sesión", "Accede al panel de telemetría y gestión del clúster.",
     ["Correo institucional", "Contraseña"], "Entrar al sistema",
     "¿No tienes cuenta?", "Crear usuario", "¡Bienvenido! Redirigiendo...")

# 02 correo (plantilla externa de Supabase Auth)
w = W(800, 460)
w.rect(24, 20, 752, 44, SOFT)
w.text(60, 48, "Cliente de correo del usuario (servicio externo)", 15, MID)
w.rect(24, 80, 752, 358)
w.text(60, 124, "Confirm your email address", 24, bold=True)
w.n(40, 116, 1)
w.e.append(f'<circle cx="80" cy="168" r="20" fill="{SOFT}" stroke="{LINE}"/>')
w.text(112, 164, "Supabase Auth <noreply@mail.app.supabase.io>", 16, bold=True)
w.text(112, 186, "para: correo institucional registrado", 14, MID)
w.n(40, 168, 2)
w.line(60, 210, 740, 210)
w.text(60, 250, "Confirm your email address", 19, bold=True)
w.text(60, 284, "Follow the link below to confirm this email address and finish signing up.", 15, MID)
w.text(60, 328, "Confirm email address", 17, under=True, bold=True)
w.n(40, 322, 3)
w.text(400, 394, "You're receiving this email because you signed up for an application powered by Supabase", 13, MID, anchor="middle")
w.save("wf-02-correo-confirmacion")


def topbar(w):
    w.rect(40, 20, 920, 56)
    w.text(58, 55, "Green AI Observatorio", 18, bold=True)
    w.rect(252, 36, 116, 24, SOFT, r=12); w.text(310, 52, "PMV 2 · Demostración", 10.5, MID, anchor="middle")
    w.text(376, 54, "Resumen", 15, under=True); w.text(450, 54, "Racks", 15); w.text(505, 54, "Red de flujos", 15)
    w.text(624, 54, "Usuario", 14, MID)
    w.rect(684, 36, 82, 24, SOFT, r=12); w.text(725, 53, "ROL", 12, anchor="middle", bold=True)
    w.button(776, 30, 50, "◐", h=36)
    w.button(836, 30, 112, "Cerrar sesión", h=36, size=13)


def filters(w, y):
    w.rect(40, y, 920, 150)
    w.text(60, y + 32, "Tu infraestructura, en contexto", 22, bold=True)
    for i, (l, v) in enumerate([("Métrica", "CPU"), ("Clúster", "Todos los clústeres"), ("Servidor", "Todos los servidores"), ("Histórico", "15 minutos")]):
        x = 60 + i * 192
        w.text(x, y + 62, l, 14, MID); w.field(x, y + 70, 178, v, True, size=14)
    w.button(832, y + 70, 112, "Actualizar", True, h=36)
    w.text(60, y + 134, "Estado de la consulta (hora y zona) · descripción y unidad de la métrica", 14, MID)


def tabs(w, y, active):
    xs = [(40, 108, "Resumen"), (154, 180, "Detalle por servidor"), (340, 232, "Predicción y recomendación"),
          (578, 190, "Reportes y experimento"), (774, 186, "Energía y CO2e")]
    for i, (x, wd, t) in enumerate(xs):
        w.button(x, y, wd, t, i == active, h=36, size=14)


def stat(w, x, y, wd, label, value, note):
    w.rect(x, y, wd, 86); w.text(x + 14, y + 24, label, 14, MID)
    w.text(x + 14, y + 54, value, 22, bold=True); w.text(x + 14, y + 75, note, 12, MID)


def chart(w, x, y, wd, h):
    w.rect(x, y, wd, h, PAGE)
    for i in range(1, 5):
        w.line(x + 50, y + i * h / 5, x + wd - 20, y + i * h / 5, SOFT)
    w.line(x + 50, y + 10, x + 50, y + h - 24, MID); w.line(x + 50, y + h - 24, x + wd - 20, y + h - 24, MID)
    w.text(x + 14, y + 22, "%", 13, MID); w.text(x + wd / 2, y + h - 6, "Hora", 13, MID, anchor="middle")
    span = wd - 90
    for off, c, sw, d in [(0.28, LINE, 1.5, True), (0.50, INK, 3, False), (0.70, LINE, 1.5, True)]:
        w.poly([(round(x + 60 + span * i / 8), round(y + h * off + [0, -14, 6, -8, 12, -4, 10, -10, 0][i])) for i in range(9)], c, sw, d)


# 04 dashboard resumen
w = W(1000, 860)
topbar(w); w.n(30, 48, 1)
filters(w, 92); w.n(30, 170, 2)
tabs(w, 256, 0); w.n(30, 274, 3)
for i, (l, nt) in enumerate([("Media del conjunto", "Calculada en pantalla"), ("Más cargado", "Servidor"), ("Menos cargado", "Servidor"), ("Por encima del 80 %", "Solo porcentajes")]):
    stat(w, 40 + i * 233, 308, 221, l, "— %" if i < 3 else "—", nt)
w.n(30, 350, 4)
stat(w, 40, 406, 298, "Servidores en respuesta", "—", "Series válidas: —")
stat(w, 351, 406, 298, "Procedencia", "Simulado", "Simulado, observado o estimado")
stat(w, 662, 406, 298, "Cobertura", "Completo / Parcial", "Completitud de la telemetría")
w.n(30, 448, 5)
w.rect(40, 508, 920, 332)
w.text(60, 538, "Evolución de la métrica", 19, bold=True)
w.text(940, 537, "Media, máximo y mínimo del conjunto", 13, MID, anchor="end")
w.field(60, 552, 250, "Añadir servidor (ej. HW045)", size=14)
for x, wd, t in [(322, 140, "5 más cargados"), (472, 160, "5 menos cargados"), (642, 90, "Limpiar")]:
    w.button(x, 552, wd, t, h=36, size=14)
w.n(30, 570, 6)
chart(w, 60, 602, 880, 196); w.n(30, 690, 7)
w.text(60, 824, "▸ Ver datos en tabla", 15, bold=True); w.n(30, 818, 8)
w.save("wf-04-dashboard-resumen")


def table(w, x, y, cols, rows, rh=32, size=14):
    wd = sum(c[1] for c in cols)
    w.rect(x, y, wd, rh * (len(rows) + 1), r=0)
    w.rect(x, y, wd, rh, SOFT, r=0)
    cx = x
    for i, (t, c) in enumerate(cols):
        w.text(cx + 8, y + rh / 2 + 5, t, size, bold=True)
        for j, row in enumerate(rows):
            w.text(cx + 8, y + rh * (j + 1) + rh / 2 + 5, row[i], size, MID)
        cx += c
        if i < len(cols) - 1:
            w.line(cx, y, cx, y + rh * (len(rows) + 1), SOFT)
    for j in range(len(rows)):
        w.line(x, y + rh * (j + 1), x + wd, y + rh * (j + 1))


# 05 detalle por servidor
w = W(1000, 650)
topbar(w); filters(w, 92); tabs(w, 256, 1); w.n(30, 274, 1)
w.rect(40, 308, 920, 322)
w.text(60, 340, "Detalle por servidor", 20, bold=True)
w.text(60, 366, "Estado de la consulta y advertencias", 14, MID); w.n(30, 361, 2)
w.field(60, 380, 280, "Buscar servidor (ej. HW045)", size=14); w.text(356, 404, "Servidores listados: —", 14, MID); w.n(30, 398, 3)
table(w, 60, 428, [("Clúster ⇅", 120), ("Servidor ▲", 110), ("Interfaz / filesystem", 180), ("Valor ⇅", 90), ("Procedencia", 115), ("Calidad", 90), ("Instante", 175)],
      [["clúster", f"HW00{i}", "—", "— %", "Simulado", "valid", "fecha y hora"] for i in range(1, 5)])
w.n(30, 444, 4)
w.text(60, 614, "Rango de filas mostrado", 14, MID)
w.button(690, 592, 100, "‹ Anterior", h=32, size=14); w.text(825, 613, "Página", 14, MID, anchor="middle"); w.button(860, 592, 90, "Siguiente ›", h=32, size=14)
w.n(30, 608, 5)
w.save("wf-05-dashboard-detalle")

# 06 predicción
w = W(1000, 760)
topbar(w); filters(w, 92); w.n(30, 170, 1); tabs(w, 256, 2); w.n(30, 274, 2)
w.rect(40, 308, 920, 432)
w.rect(60, 324, 180, 24, SOFT, r=12); w.text(150, 341, "Predicción experimental", 13, anchor="middle")
w.text(60, 384, "Demanda futura de CPU", 21, bold=True); w.button(332, 364, 28, "?", h=28)
w.text(60, 414, "Horizonte de 15 min con Random Forest sobre ventana histórica de 2 h (datos sintéticos).", 15, MID)
w.button(60, 432, 350, "Estimar CPU del servidor seleccionado", True, h=42); w.n(30, 453, 3)
w.text(60, 506, "Mensaje de estado: estimación generada (no se actualiza automáticamente)", 15, MID); w.n(30, 501, 4)
for i, (l, v) in enumerate([("CPU estimada", "— % · Estimado"), ("Recurso consultado", "clúster / servidor"), ("Instante estimado", "t + 15 min"),
                            ("Horizonte / modelo", "15m / versión"), ("Procedencia de entrada", "Simulado"), ("Dataset utilizado", "identificador")]):
    x, y = 60 + (i % 3) * 300, 530 + (i // 3) * 76
    w.rect(x, y, 284, 62); w.text(x + 12, y + 23, l, 14, MID); w.text(x + 12, y + 48, v, 18, bold=True)
w.n(30, 561, 5); w.n(30, 637, 6)
w.rect(60, 686, 884, 40, SOFT, dash=True); w.text(74, 711, "Advertencias del servicio (muestras excluidas, remuestreo)", 14); w.n(30, 706, 7)
w.save("wf-06-prediccion")

# 07 recomendación
w = W(1000, 860)
topbar(w); tabs(w, 92, 2)
w.rect(40, 144, 920, 696)
w.rect(60, 160, 80, 24, SOFT, r=12); w.text(100, 177, "Política", 13, anchor="middle")
w.text(60, 218, "Recomendación con restricciones", 21, bold=True)
w.text(60, 246, "Propuesta para revisión humana sobre el servidor seleccionado. No se ejecuta ningún cambio.", 15, MID)
for i, (l, v) in enumerate([("Memoria (%)  ?", "Ej. 65"), ("Latencia p95 (ms)  ?", "Ej. 120"), ("Errores (%)  ?", "Ej. 0.5")]):
    x = 60 + i * 300
    w.text(x, 278, l, 14, MID); w.field(x, 286, 284, v)
w.n(30, 304, 1)
w.text(60, 350, "Instante de telemetría  ?", 14, MID); w.field(60, 358, 280, "dd/mm/aaaa hh:mm:ss"); w.button(352, 358, 110, "Usar ahora", h=36)
w.text(660, 350, "Procedencia declarada  ?", 14, MID); w.field(660, 358, 284, "Simulada", True)
w.n(30, 376, 2)
w.button(60, 414, 220, "Evaluar recomendación", True); w.button(292, 414, 230, "Usar valores de ejemplo"); w.n(30, 433, 3)
w.text(60, 484, "Estado: Lista para revisión humana / Bloqueada por restricciones / No evaluable · clúster / servidor", 15, bold=True); w.n(30, 479, 4)
w.rect(60, 504, 884, 316, PAGE)
w.text(78, 536, "Acción: Mantener capacidad (u otra propuesta, o Sin propuesta)", 17, bold=True); w.n(30, 530, 5)
table(w, 78, 552, [("Restricción evaluada", 470), ("Resultado", 378)],
      [[a, "Cumple / Excede límite / Sin evidencia suficiente"] for a in
       ["Vigencia de la predicción", "Recurso y vigencia de telemetría", "Memoria", "Latencia p95", "Errores"]], rh=30)
w.n(30, 582, 6)
w.text(78, 756, "Límites demo: CPU, memoria, p95 y errores (valores devueltos por la política)", 14, MID)
w.text(78, 780, "Advertencias de la política", 14, MID)
w.text(78, 804, "Referencia: identificador de la recomendación", 14, MID); w.n(30, 774, 7)
w.save("wf-07-recomendacion")

# 08 aprobación humana HU-07
w = W(1000, 620)
topbar(w); tabs(w, 92, 2)
w.rect(40, 144, 920, 456)
w.text(60, 176, "Recomendación con restricciones", 19, bold=True)
w.rect(60, 190, 884, 52, PAGE); w.text(76, 213, "Resultado vigente: acción propuesta y restricciones evaluadas", 15)
w.text(76, 233, "Referencia: identificador de la recomendación", 13, MID); w.n(30, 216, 1)
w.rect(60, 258, 884, 326, "#ffffff", INK)
w.text(76, 290, "Decisión humana", 20, bold=True)
w.text(76, 316, "Registrar una decisión no ejecuta ningún cambio. Queda guardada solo como registro de auditoría.", 15); w.n(30, 311, 2)
w.text(76, 346, "Comentario (opcional, máx. 500 caracteres)", 14, MID)
w.rect(76, 354, 852, 62); w.n(30, 385, 3)
w.button(76, 430, 130, "Aprobar", True); w.button(218, 430, 130, "Rechazar"); w.n(30, 449, 4)
w.text(366, 454, "Visibles solo para los roles ADMIN y OPERATOR", 13, MID, italic=True)
w.text(76, 498, "Decisión registrada. Registrar una decisión no ejecuta ningún cambio.", 14, MID); w.n(30, 493, 5)
w.text(76, 530, "Decisiones registradas", 16, bold=True)
w.text(92, 556, "• Aprobada / Rechazada · usuario (rol) · fecha y hora · «comentario»", 15); w.n(30, 548, 6)
w.save("wf-08-aprobacion-hu07")

# 09 reporte PDF
w = W(1000, 760)
topbar(w); tabs(w, 92, 3); w.n(30, 110, 1)
w.rect(40, 144, 440, 596)
w.text(60, 178, "Reporte de históricos", 19, bold=True)
w.text(60, 202, "Exportación en CSV o PDF del historial.", 14, MID)
for i, (l, v) in enumerate([("Código de hardware", "HW045"), ("Desde", "dd/mm/aaaa"), ("Hasta", "dd/mm/aaaa")]):
    y = 232 + i * 66
    w.text(60, y, l, 14, MID); w.field(60, y + 8, 400, v)
w.n(30, 258, 2)
w.button(60, 436, 124, "Ver resumen", True, size=14); w.button(192, 436, 132, "Descargar CSV", size=14); w.button(332, 436, 128, "Descargar PDF", size=14)
w.n(30, 455, 3)
w.text(60, 508, "PDF descargado con éxito", 15, MID); w.n(30, 503, 4)
w.text(260, 560, "La API genera el archivo y el", 14, MID, anchor="middle", italic=True)
w.text(260, 580, "navegador lo descarga  →", 14, MID, anchor="middle", italic=True)
w.rect(520, 144, 440, 596, "#ffffff", INK, r=0)
w.text(548, 184, "Green AI - Reporte histórico", 21, bold=True)
w.text(548, 208, "Generado: fecha y hora UTC", 14, MID); w.n(520, 188, 5)
rows = ["Hardware", "Periodo inicio", "Periodo fin", "Fuente", "Registros", "CPU media", "CPU p95", "CPU máxima", "RAM media",
        "RAM p95", "Carga alta (CPU > 80 %)", "Energía modelada", "Huecos ignorados"]
for i, t in enumerate(rows):
    y = 244 + i * 30
    w.text(548, y, t, 15, bold=True); w.text(790, y, "—", 15, MID); w.line(548, y + 9, 932, y + 9, SOFT)
w.n(520, 360, 6)
w.text(548, 660, "Datos simulados; energía modelada, no medida.", 15, italic=True); w.n(520, 655, 7)
w.text(548, 690, "Advertencias del resumen (si existen)", 14, MID, italic=True)
w.save("wf-09-reporte-pdf")

# 10 tabla accesible
w = W(1000, 690)
topbar(w); tabs(w, 92, 0)
w.rect(40, 144, 920, 526)
w.text(60, 176, "Evolución de la métrica", 19, bold=True)
chart(w, 60, 192, 880, 170); w.n(30, 275, 1)
w.text(60, 394, "▾ Ver datos en tabla", 16, bold=True); w.n(30, 389, 2)
w.rect(60, 408, 884, 246, PAGE, INK, dash=True)
w.text(76, 434, "Evolución de la métrica: media, rango y servidores comparados (unidad: %)", 15, bold=True); w.n(30, 429, 3)
table(w, 76, 448, [("Hora", 150), ("Mínimo (%)", 150), ("Máximo (%)", 150), ("Media del conjunto (%)", 220), ("HW045 (%)", 180)],
      [[f"hora {i}", "—", "—", "—", "—"] for i in range(1, 6)], rh=32)
w.n(30, 464, 4); w.n(30, 528, 5)
w.save("wf-10-tabla-accesible")
print("OK", len(list(OUT.glob("*.png"))), "PNG")
