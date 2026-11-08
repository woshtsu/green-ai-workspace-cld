"""Mantiene despiertos los 6 servicios de Render durante la grabación del video (plan gratuito: se duermen
tras 15 min sin tráfico) y muestra su estado.

Uso:  python herramientas_IA/video/mantener_despierto.py [--intervalo 240] [--minutos 120]
Ctrl + C para terminar. Ejecutarlo ~25 min antes de grabar (el primer ciclo los despierta) y dejarlo
corriendo en una terminal que NO se grabe.

Cada servicio despierto consume horas del cupo gratuito (750 h/mes compartidas por todo el workspace,
también con SoftwareAnemia): 6 servicios × 2 h = 12 h. Por eso el script se detiene solo tras --minutos.
Solo hace GET a rutas de salud públicas; no usa tokens ni datos.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import time
import urllib.error
import urllib.request

SERVICIOS = {
    "gateway": "https://green-ai-gateway-dev.onrender.com/actuator/health",
    "monitoring": "https://green-ai-monitoring-dev.onrender.com/actuator/health",
    "prediction": "https://green-ai-prediction-dev-zxly.onrender.com/health/ready",
    "data-processing": "https://green-ai-data-processing-dev.onrender.com/api/v1/health",
    "simulator": "https://green-ai-simulator-dev.onrender.com/health",
    "prometheus": "https://green-ai-prometheus-dev.onrender.com/-/healthy",
}


def ping(url: str) -> tuple[int, float]:
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "green-ai-keepalive"})
        with urllib.request.urlopen(req, timeout=90) as r:
            r.read(256)
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except (urllib.error.URLError, TimeoutError):
        code = 0
    return code, time.perf_counter() - t0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--intervalo", type=int, default=240, help="segundos entre ciclos (< 900)")
    ap.add_argument("--minutos", type=int, default=120, help="duración máxima")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    fin = time.time() + a.minutos * 60
    print(f"Manteniendo despiertos {len(SERVICIOS)} servicios cada {a.intervalo} s durante {a.minutos} min. Ctrl+C para salir.")
    try:
        while time.time() < fin:
            linea = []
            for nombre, url in SERVICIOS.items():
                code, seg = ping(url)
                marca = "OK" if code == 200 else f"!{code or 'sin respuesta'}"
                linea.append(f"{nombre} {marca} {seg:.1f}s")
            print(dt.datetime.now().strftime("%H:%M:%S"), " | ".join(linea), flush=True)
            time.sleep(a.intervalo)
    except KeyboardInterrupt:
        pass
    print("Fin: los servicios se dormirán tras 15 min sin tráfico.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
