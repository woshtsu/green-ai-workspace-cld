"""Graba la pantalla (sin voz) de los 7 episodios del video de la Unidad III para poner la locución encima.

Sigue docs/exposicion/GUION-VIDEO-UNIDAD-III.md. Un MP4 por episodio (ffmpeg gdigrab, escritorio completo,
1920x1080) y un archivo «-pasos.md» con el minuto de cada paso, que sirve de guion de locución.

Requisitos (una vez):
  python -m venv .tools/video
  .tools/video/Scripts/python -m pip install playwright==1.48.0   # usa el Edge instalado; no descarga navegadores
  ffmpeg (winget install --id Gyan.FFmpeg -e)

Uso:
  .tools/video/Scripts/python herramientas_IA/video/grabar_episodios.py --ensayo 1 2 5     # sin grabar
  .tools/video/Scripts/python herramientas_IA/video/grabar_episodios.py 1 2 3 4 5 6 7     # graba
Opciones: --base (URL del frontend, producción por defecto), --out (carpeta de salida, exportados/video).

Inicio de sesión: el perfil de Edge vive en .tools/video/perfil-edge (no versionado). Si no hay sesión, el
script espera a que la inicies a mano en la ventana (nunca ve la contraseña). El episodio 1 cierra la
sesión antes de grabar y graba el inicio de sesión que haces tú. El episodio 3 abre Windows Terminal con la
carga real (carga_transacciones.py): tú pulsas Enter y escribes correo y contraseña.

Errores reales (429, 504, 422): no se ocultan. El paso queda en pantalla con el aviso de la app y el
resumen final lo marca como FALLO; repite el episodio solo si el fallo impide ver la funcionalidad.
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PWTimeout, sync_playwright

ROOT = Path(__file__).resolve().parents[2]
REPO = "https://github.com/woshtsu/green-ai-workspace-cld"
TRELLO = "https://trello.com/b/PL8uQ4rF/green-ai-para-centros-de-datos-universitarios"
PROMETHEUS = "https://green-ai-prometheus-dev.onrender.com/targets"
PERFIL = ROOT / ".tools/video/perfil-edge"
SENAL_EP3 = ROOT / ".tools/video/ep3-terminado.txt"
RITMO = 1.0  # lo fija --ritmo
PUERTO_CDP = 9333


def edge_exe() -> str:
    for p in (Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
              Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")):
        if p.exists():
            return str(p)
    sys.exit("No encuentro msedge.exe.")

ROTULO_JS = """([arriba, abajo]) => {
  const mk = (id, css) => { let e = document.getElementById(id);
    if (!e) { e = document.createElement('div'); e.id = id; document.documentElement.appendChild(e); }
    Object.assign(e.style, css); return e; };
  const base = {position:'fixed', left:'0', right:'0', zIndex:'2147483647', pointerEvents:'none',
    fontFamily:'Segoe UI, Arial, sans-serif', textAlign:'center', color:'#fff'};
  mk('__rot_top', {...base, top:'0', padding:'6px 12px', fontSize:'18px', fontWeight:'600',
    background:'rgba(21,128,61,.92)', display: arriba ? 'block' : 'none'}).textContent = arriba;
  const b = mk('__rot_bot', {...base, bottom:'18px', left:'50%', right:'auto', transform:'translateX(-50%)',
    maxWidth:'80vw', padding:'8px 18px', fontSize:'20px', borderRadius:'8px', background:'rgba(15,23,42,.85)'});
  b.textContent = abajo; b.style.display = abajo ? 'block' : 'none';
}"""
RESALTAR_JS = """(sel) => { document.querySelectorAll('.__resaltado').forEach(e => {
    e.classList.remove('__resaltado'); e.style.outline = ''; e.style.outlineOffset = ''; });
  const e = document.querySelector(sel); if (!e) return false;
  e.scrollIntoView({block:'center', behavior:'smooth'}); e.classList.add('__resaltado');
  e.style.outline = '4px solid #f59e0b'; e.style.outlineOffset = '3px'; return true; }"""
RANGO_JS = """([sel, v]) => { const e = document.querySelector(sel); e.value = v;
  e.dispatchEvent(new Event('input', {bubbles:true})); e.dispatchEvent(new Event('change', {bubbles:true})); }"""


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    for p in (Path.home() / "AppData/Local/Microsoft/WinGet/Packages").glob("Gyan.FFmpeg*/**/bin/ffmpeg.exe"):
        return str(p)
    sys.exit("No encuentro ffmpeg (winget install --id Gyan.FFmpeg -e).")


class Grabacion:
    """Un episodio: rótulos, pasos con tiempos y verificación de respuestas de la API."""

    def __init__(self, pg: Page, titulo: str, ensayo: bool, salida: Path | None):
        self.pg, self.titulo, self.ensayo, self.salida = pg, titulo, ensayo, salida
        self.t0 = time.perf_counter()
        self.pasos: list[tuple[str, str, str]] = []  # (mm:ss, texto, estado)
        self.texto = ""
        self.ff: subprocess.Popen | None = None

    # --- grabación ---
    def iniciar(self) -> None:
        if not self.ensayo:
            self.ff = subprocess.Popen(
                [ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30", "-draw_mouse", "1",
                 "-i", "desktop", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
                 str(self.salida)], stdin=subprocess.PIPE)
            time.sleep(1.5)
        self.t0 = time.perf_counter()

    def detener(self) -> None:
        if self.ff and self.ff.poll() is None:
            self.ff.stdin.write(b"q")
            self.ff.stdin.flush()
            self.ff.wait(timeout=60)

    # --- utilidades de escena ---
    def marca(self) -> str:
        s = int(time.perf_counter() - self.t0)
        return f"{s // 60:02d}:{s % 60:02d}"

    def rotulo(self, texto: str | None = None) -> None:
        if texto is not None:
            self.texto = texto
        try:
            arriba = "" if "github.com" in self.pg.url else self.titulo  # sin banda verde sobre GitHub
            self.pg.evaluate(ROTULO_JS, [arriba, self.texto])
        except Exception:
            pass

    def paso(self, texto: str, estado: str = "OK") -> None:
        self.pasos.append((self.marca(), texto, estado))
        print(f"  {self.marca()} [{estado}] {texto}", flush=True)
        self.rotulo(texto)

    def fallo(self, texto: str) -> None:
        self.paso(texto, "FALLO")

    def ir(self, url: str, esperar: str | None = None, timeout: int = 90_000) -> None:
        self.pg.goto(url, wait_until="domcontentloaded", timeout=timeout)
        if esperar:
            try:
                self.pg.wait_for_selector(esperar, state="visible", timeout=timeout)
            except PWTimeout:
                self.fallo(f"No apareció {esperar} en {url}")
        if "github.com" in url and self.pg.get_by_text("404 - page not found").count():
            self.fallo(f"GitHub 404: {url}")
        self.rotulo()

    def leer(self, segundos: float) -> None:
        """Pausa solo para que el espectador lea (las esperas de datos van en api())."""
        self.pg.wait_for_timeout(int(segundos * RITMO * 1000))

    def resaltar(self, sel: str, segundos: float = 3) -> None:
        if not self.pg.evaluate(RESALTAR_JS, sel):
            self.fallo(f"No existe {sel}")
        self.leer(segundos)

    def api(self, fragmento: str, accion, nombre: str, timeout: int = 90_000) -> int:
        """Ejecuta la acción y espera la respuesta de la API cuyo URL contiene `fragmento`."""
        try:
            with self.pg.expect_response(lambda r: fragmento in r.url and r.request.method != "OPTIONS",
                                         timeout=timeout) as info:
                accion()
            r = info.value
            status = r.status
        except PWTimeout:
            status = 0
        if 200 <= status < 300:
            self.paso(f"{nombre}: HTTP {status}")
        else:
            self.fallo(f"{nombre}: HTTP {status or 'sin respuesta'} (se muestra tal cual)")
        return status

    def guardar_pasos(self, ruta: Path) -> None:
        lineas = [f"# {self.titulo}", "", f"Grabado: {dt.datetime.now():%Y-%m-%d %H:%M}. "
                  "Minuto de cada paso dentro del clip (para la locución).", "",
                  "| Minuto | Paso | Estado |", "|---|---|---|"]
        lineas += [f"| {m} | {t} | {e} |" for m, t, e in self.pasos]
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def asegurar_sesion(pg: Page, base: str) -> None:
    pg.goto(base + "dashboard.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    if "login.html" in pg.url:
        print(">> Inicia sesión en la ventana de Edge (el script espera sin límite).", flush=True)
        pg.wait_for_url("**/dashboard.html*", timeout=0)
    pg.wait_for_selector("#user-name-display", state="visible", timeout=90_000)


# ----------------------------------------------------------------------------------------------- episodios
def ep1(g: Grabacion, base: str) -> None:
    pg = g.pg
    g.ir(base + "login.html", "input[type=email]")
    g.paso("Inicio de sesión con Supabase Auth (lo escribe el presentador; la contraseña no se ve)")
    pg.wait_for_url("**/dashboard.html*", timeout=0)
    pg.wait_for_selector("#user-name-display", state="visible", timeout=90_000)
    g.rotulo()
    g.paso("Sesión iniciada: el Gateway valida el JWT con JWKS")
    g.resaltar("#user-role-badge", 4)
    g.paso("Centro de operación: CPU, todos los clústeres, 15 minutos")
    pg.select_option("#metric", "node.cpu.utilization")
    pg.select_option("#period", "15")
    g.api("/api/monitoring/", lambda: pg.click("#refresh"), "Actualizar métricas (Monitoring + Prometheus)")
    pg.wait_for_timeout(1500)
    g.paso("KPI: media, servidor más cargado y menos cargado")
    for sel in ("#stat-mean", "#stat-max", "#stat-min"):
        g.resaltar(sel, 3)
    g.paso("Servidores en respuesta y procedencia declarada «Simulado»")
    g.resaltar("#summary-nodes", 3)
    g.resaltar("#summary-origin", 4)
    g.paso("Evolución de la métrica: media con bandas de máximo y mínimo")
    g.resaltar("#history-chart", 6)
    g.paso("Comparar los 5 servidores más cargados")
    pg.click("#compare-top")
    g.resaltar("#history-chart", 8)
    g.paso("Detalle por servidor: tabla paginada de 50 servidores")
    pg.click("#tab-detalle")
    g.resaltar("#metric-rows", 5)
    g.paso("Búsqueda del servidor HW045")
    pg.fill("#table-search", "")
    pg.type("#table-search", "HW045", delay=150)
    g.leer(6)
    pg.fill("#table-search", "")
    pg.dispatch_event("#table-search", "input")
    g.paso("Ordenar por la columna «Valor»")
    pg.click("th[data-sort=value]")
    g.leer(5)
    pg.click("th[data-sort=value]")
    g.leer(5)
    g.paso("Fin del episodio 1")
    g.leer(2)


def ep2(g: Grabacion, base: str) -> None:
    pg = g.pg
    g.ir(base + "network.html", ".rack-node-cell")
    g.paso("Racks con calor: 50 servidores en 5 racks")
    for sel in ("#kpi-high-cpu", "#kpi-avg-cpu", "#kpi-busiest-rack"):
        g.resaltar(sel, 3)
    g.paso("Escala de color: verde < 50 %, amarillo, naranja, rojo > 80 %")
    g.resaltar("#racks-container", 6)
    celdas = pg.locator(".rack-node-cell")
    caliente = max(range(celdas.count()), key=lambda i: int((celdas.nth(i).inner_text().split()[-1]
                                                              .rstrip("%") or "0").replace("—", "0")))
    celda = celdas.nth(caliente)
    g.paso("Servidor más cargado: detalle de CPU, núcleos, potencia y procedencia")
    celda.hover()
    g.leer(2)
    celda.click()
    g.resaltar("#rack-detail-panel", 6)
    g.api("/api/monitoring/", lambda: pg.click("#refresh-racks-btn"), "Actualizar racks (refresco cada 30 s)")
    g.leer(4)

    g.ir(base + "flows.html", "#flows-svg")
    g.paso("Red de flujos: propuesta ilustrativa de rebalanceo (executionAllowed=false)")
    g.leer(8)
    g.paso("Sensibilidad 0,8 y máximo 15 flujos: se recalculan los flujos")
    pg.evaluate(RANGO_JS, ["#fc-k", "0.8"])
    g.leer(3)
    pg.evaluate(RANGO_JS, ["#fc-max", "15"])
    g.resaltar("#flows-stats", 6)
    g.resaltar("#flows-svg", 6)

    g.ir(base + "dashboard.html", "#tab-reportes")
    pg.click("#tab-reportes")
    g.paso("Reporte de históricos: HW045, 10/07/2026 – 11/07/2026")
    pg.fill("#report-hardware-id", "HW045")
    pg.fill("#report-start", "2026-07-10")
    pg.fill("#report-end", "2026-07-11")
    g.api("/api/processing/", lambda: pg.click("#report-summary-btn"), "Ver resumen (Data Processing)")
    g.resaltar("#report-summary-container", 6)
    try:
        with pg.expect_download(timeout=20_000) as dl:
            pg.click("#report-csv-btn")
        g.paso(f"Descargar CSV: {dl.value.suggested_filename}")
    except PWTimeout:
        g.fallo("Descargar CSV: no llegó la descarga")
    g.leer(4)
    g.paso("Experimento baseline vs Green AI (datos simulados, energía modelada)")
    g.resaltar("#pmv2-card-experiment", 8)

    pg.click("#tab-energia")
    g.paso("Energía y CO₂e: P = P_idle + (P_max − P_idle) × CPU")
    g.leer(4)
    pg.fill("#energy-factor", "0.245")
    pg.fill("#energy-factor-source", "Sistema Eléctrico Interconectado Nacional — MINEM 2025")
    g.api("/api/", lambda: pg.click("#energy-sim"), "Calcular con el simulador")
    pg.wait_for_timeout(1500)
    g.resaltar("#energy-results", 10)
    g.paso("Fin del episodio 2")
    g.leer(2)


def ep3(g: Grabacion, base: str) -> None:
    pg = g.pg
    SENAL_EP3.unlink(missing_ok=True)
    if g.ensayo:  # la carga real (601 transacciones) solo se lanza al grabar; ensayarla con --iteraciones 5
        g.paso("Ensayo: se omite la carga real; prueba carga_transacciones.py --iteraciones 5 aparte")
        g.ir(PROMETHEUS, "body")
        g.paso("Prometheus: estado de los objetivos")
        return
    g.paso("Carga masiva: 200 iteraciones × 3 + 1 = 601 transacciones reales contra el Gateway en Render")
    subprocess.Popen(["wt.exe", "-w", "new", "--maximized", "powershell.exe", "-ExecutionPolicy",
                      "Bypass", "-File", str(ROOT / "herramientas_IA/video/ep3_terminal.ps1")], cwd=ROOT)
    print(">> En Windows Terminal: pulsa Enter, escribe correo y contraseña. Espero a que termine.", flush=True)
    while not SENAL_EP3.exists():
        time.sleep(1)
    estado = SENAL_EP3.read_text(encoding="utf-8-sig").strip()  # PowerShell 5.1 escribe BOM
    g.paso(f"Carga terminada ({estado}); tabla final y primeras líneas del CSV en la terminal",
           "OK" if estado == "codigo 0" else "FALLO")
    g.ir(PROMETHEUS, "body")  # se carga detrás mientras la terminal enseña la tabla 15 s y se cierra sola
    time.sleep(17)
    pg.bring_to_front()
    subprocess.run(["powershell", "-NoProfile", "-Command",  # traer la ventana de Edge al frente del escritorio
                    "(New-Object -ComObject WScript.Shell).AppActivate('Prometheus') | Out-Null"], check=False)
    g.rotulo()
    g.paso("Prometheus: estado de los objetivos después de la carga")
    g.leer(12)
    g.paso("Fin del episodio 3")
    g.leer(2)


def ep4(g: Grabacion, base: str) -> None:
    # model_comparison.csv no está versionado (results/metrics/* en .gitignore): se muestra la PoC, que lo resume.
    g.ir(f"{REPO}/blob/main/docs/academico/06-prueba-de-concepto.md", "body")
    try:
        g.pg.get_by_role("heading", name="3. Resultados").first.scroll_into_view_if_needed(timeout=15_000)
    except PWTimeout:
        g.fallo("No encontré la sección «3. Resultados» de la PoC")
    g.paso("Métricas a 15 min (validación): Random Forest MAE 3,22 · RMSE 4,59 frente a persistencia 4,61 · 6,39")
    g.leer(20)
    g.ir(f"{REPO}/actions/workflows/ci.yml?query=branch%3Amain", "body")
    g.paso("GitHub Actions: CI en main (pruebas por servicio e imágenes Docker)")
    g.leer(8)
    run = g.pg.locator("a[href*='/actions/runs/']").first
    try:
        run.click(timeout=15_000)
        g.pg.wait_for_load_state("domcontentloaded")
        g.rotulo()
        g.paso("Última ejecución: trabajos aprobados")
        g.leer(12)
    except PWTimeout:
        g.fallo("No se pudo abrir la última ejecución de CI")
    g.ir(f"{REPO}/blob/main/docs/academico/08-pruebas-resultados-discusion.md", "body")
    g.paso("Suites de pruebas por servicio")
    g.leer(12)
    g.pg.mouse.wheel(0, 900)
    g.leer(10)
    g.ir(f"{REPO}/blob/main/docs/evidencias/smoke-20261106.json", "body")
    g.paso("Smoke de integración 14/14")
    g.leer(10)
    g.ir(f"{REPO}/blob/main/docs/evidencias/prediction-imagen-ligera-20261107.md", "body")
    g.paso("Prediction ligera: imagen 2,85 GB → 510 MB; RAM en reposo 174 → 122–142 MiB (una medición)")
    g.leer(14)
    g.ir(PROMETHEUS, "body")
    g.paso("Prometheus en Render: simulador cada 15 s y Prediction cada 1 min")
    g.leer(10)
    g.paso("Fin del episodio 4")
    g.leer(2)


def ep5(g: Grabacion, base: str) -> None:
    pg = g.pg
    g.ir(base + "dashboard.html", "#tab-prediccion")
    pg.wait_for_function("document.querySelectorAll('#node option').length > 1", timeout=90_000)
    pg.click("#tab-prediccion")
    g.paso("Caso de uso 1: predicción de CPU a 15 minutos (HU-03), servidor HW045")
    valor = pg.eval_on_selector("#node", "s => [...s.options].map(o => o.value).find(v => v.includes('HW045'))")
    if valor:
        pg.select_option("#node", valor)
    else:
        g.fallo("HW045 no está en la lista de servidores")
    g.leer(3)
    g.api("/api/prediction/", lambda: pg.click("#predict-button"), "Estimar CPU (Data Processing → Prediction)")
    pg.wait_for_timeout(1500)
    g.resaltar("#prediction-result", 6)
    for sel in ("#prediction-value", "#prediction-time", "#prediction-model", "#prediction-origin"):
        g.resaltar(sel, 3)
    g.paso("Caso de uso 2: recomendación con restricciones (HU-06, HU-08)")
    g.resaltar("#pmv2-card-recommendation", 3)
    pg.click("#policy-example")
    pg.click("#policy-now")
    g.paso("Memoria 65 %, latencia p95 120 ms, errores 0,2 %, procedencia simulada")
    g.resaltar("#recommendation-form", 5)
    g.api("/api/recommendations/", lambda: pg.click("#recommend-button"), "Evaluar recomendación")
    pg.wait_for_timeout(1500)
    g.resaltar("#recommendation-result", 12)
    g.paso("Violación de política: memoria 95 % (umbral 85 %)")
    pg.fill("#policy-memory", "95")
    pg.click("#policy-now")
    g.leer(3)
    g.api("/api/recommendations/", lambda: pg.click("#recommend-button"), "Evaluar recomendación con memoria 95 %")
    pg.wait_for_timeout(1500)
    g.resaltar("#recommendation-result", 12)
    g.paso("Fin del episodio 5")
    g.leer(2)


def ep6(g: Grabacion, base: str) -> None:
    pg = g.pg
    g.ir(TRELLO, "body")
    pg.wait_for_timeout(5000)
    g.rotulo()
    g.paso("Tablero Trello del proyecto: columnas Scrum/Kanban")
    g.leer(10)
    pg.mouse.move(960, 600)
    for _ in range(4):
        pg.mouse.wheel(600, 0)
        g.leer(3)
    for hu in ("HU-03", "HU-06"):
        tarjeta = pg.locator(f"[data-testid='card-name']:has-text('{hu}')").first
        try:
            tarjeta.scroll_into_view_if_needed(timeout=10_000)
            tarjeta.click(timeout=10_000)
            pg.wait_for_timeout(2000)
            g.rotulo()
            g.paso(f"Tarjeta {hu}: historia, criterios Given/When/Then, checklist y evidencias")
            g.leer(14)
            pg.mouse.wheel(0, 700)
            g.leer(10)
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(1500)
        except PWTimeout:
            g.fallo(f"No encontré la tarjeta {hu} en el tablero")
    g.paso("Fin del episodio 6")
    g.leer(2)


def ep7(g: Grabacion, base: str) -> None:
    rama = f"{REPO}/blob/test/software"
    arbol = f"{REPO}/tree/test/software"
    escenas = [
        (f"{arbol}/data-processing", "Data Processing (Python): capas domain, application e infrastructure", 8),
        (f"{rama}/data-processing/domain/ports/historical_logs_source.py",
         "Puerto del dominio HistoricalLogsSource: sin base de datos ni frameworks", 12),
        (f"{rama}/data-processing/application/use_cases/read_historical_logs.py",
         "Caso de uso: solo conoce el puerto", 12),
        (f"{rama}/data-processing/infrastructure/historical_sources.py",
         "Factoría: elige el adaptador según HISTORICAL_SOURCE", 10),
        (f"{arbol}/data-processing/infrastructure/adapters/input",
         "Adaptadores SQLite (desarrollo) y Supabase (nube)", 8),
        (f"{arbol}/monitoring/src/main/java/pe/edu/continental/greenai/monitoring",
         "Monitoring (Java 21): domain, application/port y adapter", 8),
        (f"{rama}/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/application/port/in/QueryMetrics.java",
         "Puerto de entrada QueryMetrics", 8),
        (f"{rama}/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/application/port/out/MetricsSource.java",
         "Puerto de salida MetricsSource", 8),
        (f"{arbol}/monitoring/src/main/java/pe/edu/continental/greenai/monitoring/adapter/out",
         "Adaptadores secundarios: Prometheus y fixture", 8),
        (f"{rama}/frontend/supabase-auth-setup.sql#L45-L66",
         "Función PL/pgSQL handle_new_auth_user() + trigger on_auth_user_created_green_ai", 16),
        (f"{rama}/frontend/supabase-auth-setup.sql#L79-L104",
         "Función custom_access_token_hook: inyecta el rol en el JWT", 16),
        (f"{REPO}/blob/test/.github/workflows/ci.yml", "CI: pruebas de todos los servicios en cada push", 10),
        (f"{REPO}/actions", "GitHub Actions: CI y despliegue a GitHub Pages", 10),
    ]
    for url, texto, seg in escenas:
        g.ir(url, "body")
        g.paso(texto)
        g.leer(seg)
    g.paso("Fin del episodio 7")
    g.leer(2)


EPISODIOS = {
    1: ("Episodio 1 · Pruebas funcionales del PMV1", ep1),
    2: ("Episodio 2 · Pruebas funcionales del PMV2", ep2),
    3: ("Episodio 3 · Pruebas con data masiva (601 transacciones)", ep3),
    4: ("Episodio 4 · Pruebas con métricas", ep4),
    5: ("Episodio 5 · Predicciones con ML del PMV1 y PMV2", ep5),
    6: ("Episodio 6 · Tablero Trello y contenidos", ep6),
    7: ("Episodio 7 · Arquitectura hexagonal y procedimientos almacenados", ep7),
}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episodios", nargs="*", type=int, default=list(EPISODIOS))
    ap.add_argument("--ensayo", action="store_true", help="recorre los pasos sin grabar")
    ap.add_argument("--base", default="https://woshtsu.github.io/green-ai-workspace-cld/")
    ap.add_argument("--out", type=Path, default=ROOT / "exportados/video")
    ap.add_argument("--ritmo", type=float, default=1.6,
                    help="multiplica las pausas de lectura (1.6 ≈ duración del guion)")
    a = ap.parse_args()
    global RITMO
    RITMO = a.ritmo
    base =a.base.rstrip("/") + "/"
    a.out.mkdir(parents=True, exist_ok=True)
    PERFIL.mkdir(parents=True, exist_ok=True)
    resumen = []
    with sync_playwright() as p:
        # Edge normal + CDP: launch_persistent_context sale con código 0 en Edge 157 con este perfil (10/11/2026),
        # y así Edge no queda marcado como automatizado (Google/Trello permiten iniciar sesión).
        edge = subprocess.Popen([edge_exe(), f"--user-data-dir={PERFIL}", f"--remote-debugging-port={PUERTO_CDP}",
                                 "--no-first-run", "--no-default-browser-check", "--start-maximized",
                                 "--lang=es-PE", "--force-dark-mode", "about:blank"])
        for _ in range(30):
            try:
                browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PUERTO_CDP}")
                break
            except Exception:
                time.sleep(1)
        else:
            sys.exit("No pude conectar con Edge (¿otra ventana de Edge usa el perfil del grabador?).")
        ctx = browser.contexts[0]
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        # Tema oscuro fijo en todo el video: la app (greenai-theme) y los sitios que siguen al sistema
        # (GitHub, Trello, Prometheus), aunque Windows esté en modo claro.
        ctx.add_init_script("try { if (location.hostname.endsWith('github.io'))"
                            " localStorage.setItem('greenai-theme', 'dark'); } catch (e) {}")
        pg.emulate_media(color_scheme="dark")
        for n in a.episodios:
            titulo, fn = EPISODIOS[n]
            sello = dt.datetime.now().strftime("%Y%m%d-%H%M")
            mp4 = a.out / f"ep{n}-{sello}.mp4"
            print(f"\n== {titulo} ({'ensayo' if a.ensayo else mp4.name})", flush=True)
            if n == 1:  # se graba el inicio de sesión: cerrar la sesión antes
                pg.goto(base + "dashboard.html", wait_until="domcontentloaded")
                pg.wait_for_timeout(3000)
                if "login.html" not in pg.url:
                    pg.click("#logout-btn")
                    pg.wait_for_url("**/login.html*", timeout=30_000)
                print(">> Episodio 1: inicia sesión en la app cuando aparezca el formulario.", flush=True)
            elif n in (2, 5):
                asegurar_sesion(pg, base)
            elif n == 6:  # el tablero es privado: iniciar sesión en Trello una vez en este perfil
                pg.goto(TRELLO, wait_until="domcontentloaded")
                try:
                    pg.get_by_role("button", name="Solo necesarias").click(timeout=5_000)
                except PWTimeout:
                    pass
                try:
                    pg.wait_for_selector("[data-testid='card-name']", state="visible", timeout=15_000)
                except PWTimeout:
                    print(">> Inicia sesión en Trello (Google sirve) en la ventana de Edge y abre el tablero."
                          " Espero hasta 10 min.", flush=True)
                try:
                    pg.wait_for_selector("[data-testid='card-name']", state="visible", timeout=600_000)
                    if "PL8uQ4rF" not in pg.url:
                        pg.goto(TRELLO, wait_until="domcontentloaded")
                except PWTimeout:  # sin acceso a Trello: se omite (no se graba un tablero vacío)
                    print(">> Episodio 6 OMITIDO: no hay sesión de Trello en el perfil de Edge.", flush=True)
                    resumen.append((n, "00:00", "omitido"))
                    continue
            pg.goto("about:blank")
            g = Grabacion(pg, titulo, a.ensayo, mp4)
            try:
                g.iniciar()
                fn(g, base)
            except Exception as e:  # el error se registra y no deja ffmpeg huérfano
                g.fallo(f"Excepción: {type(e).__name__}: {str(e).splitlines()[0][:200]}")
                pg.screenshot(path=str(a.out / f"ep{n}-{sello}-error.png"))
            finally:
                g.detener()
            g.guardar_pasos(a.out / f"ep{n}-{sello}-pasos.md")
            fallos = sum(1 for _, _, e in g.pasos if e == "FALLO")
            resumen.append((n, g.marca(), fallos))
        browser.close()
        edge.terminate()
    print("\nResumen:")
    for n, dur, fallos in resumen:
        print(f"  Episodio {n}: {dur} · {'OK' if not fallos else f'{fallos} FALLO(S)'}")
    return 1 if any(f for *_, f in resumen) else 0


if __name__ == "__main__":
    sys.exit(main())
