"""Carátula y cierre del video de la Unidad III (diapositivas HTML a pantalla completa, sin voz) y montaje final.

Uso (con el runtime de .tools/video; requiere qrcode==7.4.2 para el cierre):
  .tools/video/Scripts/python herramientas_IA/video/portada_cierre.py caratula   # graba exportados/video/ep0-caratula.mp4
  .tools/video/Scripts/python herramientas_IA/video/portada_cierre.py cierre     # graba ep8-cierre.mp4 con los minutos reales
  .tools/video/Scripts/python herramientas_IA/video/portada_cierre.py unir       # une ep0..ep8 en green-ai-unidad-III.mp4
Opción --ensayo: genera el HTML y lo muestra sin grabar.

Los minutos del cierre y de la descripción de YouTube se calculan con ffprobe a partir de los clips elegidos
(el más reciente de cada episodio en exportados/video, ignorando los DESCARTADO-*).
Deja libre la esquina inferior derecha (400×240 px) para la cámara de cada integrante en la edición.
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grabar_episodios import OSCURO, PERFIL, PUERTO_CDP, REPO, cerrar_edge, edge_exe, ffmpeg_exe  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "exportados/video"
APP = "https://woshtsu.github.io/green-ai-workspace-cld/"
TITULO = ("Green AI: sistema de monitoreo y predicción de demanda computacional para apoyar la gestión "
          "eficiente de recursos en entornos universitarios")
INTEGRANTES = [
    ("Jhonny Cristhian Quintana Carhuaricra", "Product Owner"),
    ("Gina Diana Barrera Peña", "Scrum Master · Datos y Machine Learning"),
    ("Leonid Kisley Orlando Huamán Collazos", "Infraestructura y Frontend"),
    ("Ricardo Porras Veli", "Backend y Arquitectura"),
]
EPISODIOS = [
    (1, "Pruebas funcionales del PMV1"),
    (2, "Pruebas funcionales del PMV2"),
    (3, "Pruebas con data masiva (601 transacciones)"),
    (4, "Pruebas con métricas"),
    (5, "Predicciones con ML del PMV1 y PMV2"),
    (6, "Tablero Trello y contenidos"),
    (7, "Arquitectura hexagonal y procedimientos almacenados"),
]
RUBRICA = [  # (indicador, episodios que lo demuestran)
    ("Ind. 9 · Demostración con 500–1000 transacciones (PMV1 y PMV2)", [1, 2, 3]),
    ("Ind. 10 · 1.er y 2.º caso de uso de predicción con ML", [5]),
    ("Ind. 11 · Hexagonal, procedimientos almacenados y Kanban", [6, 7]),
    ("Ind. 5 · Métricas de ML, pruebas y calidad", [4]),
]

CSS = """
:root{--bg:#0b1020;--panel:#121a2e;--line:#1f2b48;--txt:#e6edf7;--mut:#94a3b8;--verde:#22c55e;--cian:#38bdf8}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100vw;height:100vh;overflow:hidden;background:radial-gradient(ellipse at 20% 0%,#13233f 0,#0b1020 60%);
 color:var(--txt);font-family:'Segoe UI',Arial,sans-serif}
.s{position:absolute;inset:0;padding:90px 120px 260px;display:flex;flex-direction:column;justify-content:center;
 opacity:0;transition:opacity .8s}
.s.on{opacity:1}
.marca{color:var(--verde);font-weight:700;letter-spacing:.18em;text-transform:uppercase;font-size:22px}
h1{font-size:64px;line-height:1.12;margin:18px 0 26px;max-width:1500px}
h2{font-size:48px;margin-bottom:34px}
.sub{color:var(--mut);font-size:28px;line-height:1.5}
.sub b{color:var(--txt);font-weight:600}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;max-width:1500px}
.card{background:var(--panel);border:1px solid var(--line);border-left:6px solid var(--verde);border-radius:14px;
 padding:26px 30px}
.card .n{font-size:32px;font-weight:600}.card .r{color:var(--cian);font-size:24px;margin-top:8px}
table{border-collapse:collapse;font-size:27px;max-width:1500px;width:100%}
td{padding:13px 18px;border-bottom:1px solid var(--line)}td.t{color:var(--verde);font-variant-numeric:tabular-nums;
 width:150px;font-weight:600}
.links{display:flex;gap:70px;align-items:center}
.qr{background:#fff;padding:14px;border-radius:12px;width:250px;height:250px}
.qr img{width:100%;height:100%}
.lk{font-size:24px;color:var(--mut);margin-top:14px;max-width:520px;word-break:break-all}
.pie{position:absolute;left:120px;bottom:60px;color:var(--mut);font-size:20px}
"""


def pagina(diapositivas: list[tuple[str, float]], titulo: str) -> str:
    """Diapositivas que avanzan solas; cada una (html, segundos)."""
    secs = "".join(f'<section class="s" data-t="{t}">{h}</section>' for h, t in diapositivas)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>
<style>{CSS}</style></head><body>{secs}
<div class="pie">Green AI · Taller de Proyectos 1 · Universidad Continental · 2026-20</div>
<script>
const s=[...document.querySelectorAll('.s')];let i=0;
function ver(){{s.forEach((e,k)=>e.classList.toggle('on',k===i));
 if(i<s.length-1)setTimeout(()=>{{i++;ver();}},s[i].dataset.t*1000);else document.title='FIN '+document.title;}}
ver();
</script></body></html>"""


def caratula() -> tuple[str, float]:
    e = html.escape
    d1 = (f'<div class="marca">Universidad Continental · Ingeniería de Sistemas e Informática</div>'
          f'<h1>{e(TITULO)}</h1>'
          '<p class="sub"><b>Taller de Proyectos 1</b> · Unidad III · Demostración del software (PMV1 y PMV2)<br>'
          'Docente: <b>Jorge Alfredo Guevara Jiménez</b><br>'
          'Entorno de calidad en la nube: GitHub Pages · Render · Supabase</p>', 13)
    cards = "".join(f'<div class="card"><div class="n">{e(n)}</div><div class="r">{e(r)}</div></div>'
                    for n, r in INTEGRANTES)
    d2 = (f'<div class="marca">Integrantes</div><h2>Equipo Green AI</h2><div class="grid">{cards}</div>', 16)
    filas = "".join(f'<tr><td class="t">Ep. {n}</td><td>{e(t)}</td></tr>' for n, t in EPISODIOS)
    d3 = (f'<div class="marca">Contenido</div><h2>Siete episodios</h2><table>{filas}</table>', 14)
    return pagina([d1, d2, d3], "Green AI · Carátula"), 13 + 16 + 14


def inicio_util(p: Path) -> float:
    """Segundo en que termina el blanco inicial (about:blank antes de cargar la primera página)."""
    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-t", "12", "-i", str(p), "-vf",
                        "fps=4,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    brillos = [float(x.split("=")[1]) for x in r.stderr.split() if x.startswith("lavfi.signalstats.YAVG=")]
    for i, y in enumerate(brillos):
        if y < 150:
            return i / 4
    return 0.0


def clips() -> dict[int, Path]:
    """El clip más reciente de cada episodio (0 = carátula, 8 = cierre), sin el blanco inicial."""
    res = {}
    recortes = OUT / "slides" / "recortes"
    recortes.mkdir(parents=True, exist_ok=True)
    for n in range(0, 9):
        cand = sorted(p for p in OUT.glob(f"ep{n}-*.mp4"))
        if not cand:
            continue
        clip = cand[-1]
        t = inicio_util(clip)
        if t > 0:
            dest = recortes / clip.name
            if not dest.exists() or dest.stat().st_mtime < clip.stat().st_mtime:
                subprocess.run([ffmpeg_exe(), "-y", "-loglevel", "error", "-ss", f"{t + 0.25:.2f}", "-i", str(clip),
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-r", "30",
                                "-pix_fmt", "yuv420p", str(dest)], check=True)
            print(f"  {clip.name}: recortados {t + 0.25:.2f} s de blanco inicial")
            clip = dest
        res[n] = clip
    return res


def duracion(p: Path) -> float:
    fp = str(Path(ffmpeg_exe()).with_name("ffprobe.exe"))
    r = subprocess.run([fp, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def mmss(s: float) -> str:
    s = int(round(s))
    return f"{s // 60:02d}:{s % 60:02d}"


def inicios(c: dict[int, Path]) -> dict[int, float]:
    t, ini = 0.0, {}
    for n in sorted(c):
        ini[n] = t
        t += duracion(c[n])
    ini["total"] = t
    return ini


def qr_png(url: str) -> str:
    import qrcode
    buf = io.BytesIO()
    qrcode.make(url, box_size=10, border=1).save(buf)  # PNG (PyPNG, sin Pillow)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def cierre() -> tuple[str, float]:
    e = html.escape
    c = clips()
    faltan = [n for n in range(0, 8) if n not in c]
    if faltan:
        sys.exit(f"Faltan clips para calcular los minutos: {faltan}")
    ini = inicios(c)
    filas = "".join(
        f'<tr><td>{e(ind)}</td><td class="t" style="width:auto">'
        f'{" · ".join(f"Ep. {n} ({mmss(ini[n])})" for n in eps)}</td></tr>' for ind, eps in RUBRICA)
    d1 = (f'<div class="marca">Cierre</div><h2>Dónde se demuestra cada indicador</h2><table>{filas}</table>'
          '<p class="sub" style="margin-top:28px">Telemetría <b>simulada</b> y energía <b>modelada</b>: '
          'no se reclaman ahorros físicos medidos.</p>', 16)
    d2 = (f'<div class="marca">Enlaces</div><h2>Código y aplicación</h2><div class="links">'
          f'<div><div class="qr"><img src="{qr_png(REPO)}" alt=""></div><div class="lk">{e(REPO)}</div></div>'
          f'<div><div class="qr"><img src="{qr_png(APP)}" alt=""></div><div class="lk">{e(APP)}</div></div></div>', 14)
    nombres = "<br>".join(e(n) for n, _ in INTEGRANTES)
    d3 = ('<div class="marca">Gracias</div><h1>Green AI · Unidad III</h1>'
          f'<p class="sub"><b>{nombres}</b><br><br>Asistente de IA declarado en el informe: Claude (Anthropic), '
          'bajo supervisión del equipo.</p>', 14)
    return pagina([d1, d2, d3], "Green AI · Cierre"), 16 + 14 + 14


def grabar(html_txt: str, nombre: str, segundos: float, ensayo: bool) -> Path:
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    pag = OUT / "slides" / f"{nombre}.html"
    pag.parent.mkdir(exist_ok=True)
    pag.write_text(html_txt, encoding="utf-8")
    mp4 = OUT / f"{nombre}.mp4"
    edge = subprocess.Popen([edge_exe(), f"--user-data-dir={PERFIL}", f"--remote-debugging-port={PUERTO_CDP}",
                             "--no-first-run", "--no-default-browser-check", "--start-fullscreen",
                             "--force-dark-mode", "about:blank"])
    ff = None
    try:
        with sync_playwright() as p:
            for _ in range(30):
                try:
                    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PUERTO_CDP}")
                    break
                except Exception:
                    time.sleep(1)
            else:
                sys.exit("No pude conectar con Edge.")
            ctx = browser.contexts[0]
            pg = ctx.new_page()  # pestaña nueva y visible; se cierran las restauradas
            for otra in ctx.pages:
                if otra is not pg:
                    otra.close()
            pg.bring_to_front()
            pg.goto(OSCURO)
            cdp = ctx.new_cdp_session(pg)  # --start-fullscreen no se aplica al conectar por CDP
            ventana = cdp.send("Browser.getWindowForTarget")["windowId"]
            cdp.send("Browser.setWindowBounds", {"windowId": ventana, "bounds": {"windowState": "fullscreen"}})
            time.sleep(2)
            if not ensayo:
                ff = subprocess.Popen([ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30",
                                       "-draw_mouse", "0", "-i", "desktop", "-c:v", "libx264", "-preset", "veryfast",
                                       "-crf", "23", "-pix_fmt", "yuv420p", str(mp4)], stdin=subprocess.PIPE)
                time.sleep(1.5)
            pg.goto(pag.as_uri())
            pg.wait_for_function("document.title.startsWith('FIN')", timeout=int(segundos * 1000) + 60_000)
            time.sleep(15)  # «FIN» se marca al mostrar la última diapositiva (14 s): esperar a que termine
            cerrar_edge(browser, edge)
    finally:
        if ff and ff.poll() is None:
            ff.stdin.write(b"q")
            ff.stdin.flush()
            ff.wait(timeout=60)
        if edge.poll() is None:
            edge.terminate()
    return mp4


def unir() -> Path:
    c = clips()
    faltan = [n for n in range(0, 9) if n not in c]
    if faltan:
        sys.exit(f"Faltan clips: {faltan}")
    lista = OUT / "slides" / "concat.txt"
    lista.parent.mkdir(exist_ok=True)
    lista.write_text("".join(f"file '{c[n].as_posix()}'\n" for n in sorted(c)), encoding="utf-8")
    final = OUT / "green-ai-unidad-III.mp4"
    subprocess.run([ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                    # recodificar: con «-c copy» quedaban DTS repetidos en las uniones
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-r", "30", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(final)], check=True)
    ini = inicios(c)
    nombres = {0: "Carátula e integrantes", 8: "Cierre"} | {n: f"Episodio {n}: {t}" for n, t in EPISODIOS}
    desc = ["Green AI — Demostración de software PMV1 y PMV2 | Unidad III — Taller de Proyectos 1", ""]
    desc += [f"{mmss(ini[n])} {nombres[n]}" for n in sorted(c)]
    desc += ["", f"Repositorio: {REPO}", f"Aplicación: {APP}",
             "Telemetría simulada y energía modelada; no se reclaman ahorros físicos medidos."]
    (OUT / "descripcion-youtube.txt").write_text("\n".join(desc) + "\n", encoding="utf-8")
    print("\n".join(desc))
    print(f"\nVideo: {final} ({mmss(duracion(final))}) · clips: {[c[n].name for n in sorted(c)]}")
    return final


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", choices=["caratula", "cierre", "unir"])
    ap.add_argument("--ensayo", action="store_true")
    a = ap.parse_args()
    if a.accion == "unir":
        unir()
        return 0
    html_txt, seg = caratula() if a.accion == "caratula" else cierre()
    nombre = "ep0-caratula" if a.accion == "caratula" else "ep8-cierre"
    mp4 = grabar(html_txt, nombre, seg, a.ensayo)
    print("ensayo sin grabar" if a.ensayo else f"{mp4} ({mmss(duracion(mp4))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
