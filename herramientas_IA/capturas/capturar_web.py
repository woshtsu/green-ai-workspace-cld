"""Captura páginas web públicas en segundo plano con Chrome headless (no toca la pantalla del usuario).

Uso: python herramientas_IA/capturas/capturar_web.py <url> <salida.png> [--ancho 1440] [--alto 900] [--espera-ms 8000]
Solo páginas públicas: no usa sesiones, cookies ni credenciales (perfil temporal vacío).
"""
import argparse, os, shutil, subprocess, sys, tempfile

CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("salida")
    ap.add_argument("--ancho", type=int, default=1440); ap.add_argument("--alto", type=int, default=900)
    ap.add_argument("--espera-ms", type=int, default=8000)
    a = ap.parse_args()
    exe = next((c for c in CHROME if os.path.exists(c)), None)
    if not exe:
        print("No se encontró Chrome ni Edge"); return 1
    perfil = tempfile.mkdtemp(prefix="cap-")
    try:
        cmd = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               f"--user-data-dir={perfil}", f"--window-size={a.ancho},{a.alto}",
               f"--virtual-time-budget={a.espera_ms}", "--force-device-scale-factor=1", "--blink-settings=preferredColorScheme=1", "--lang=es",
               f"--screenshot={os.path.abspath(a.salida)}", a.url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        ok = os.path.exists(a.salida)
        print(("OK " if ok else "FALLO ") + a.salida)
        return 0 if ok else 1
    finally:
        shutil.rmtree(perfil, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
