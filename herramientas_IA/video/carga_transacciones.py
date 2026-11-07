"""Genera entre 500 y 1000 transacciones reales contra el Gateway (episodio 3 del video: data masiva).

Cada iteración ejecuta, con el JWT del usuario y a través del Gateway, el mismo flujo que la aplicación:
  1) GET  /api/processing/v1/prediction/dataset   (ventana de 2 h de CPU de un nodo)
  2) POST /api/prediction/v1/predictions          (caso de uso de IA 1: predicción a 15 min)
  3) POST /api/recommendations/v1/recommendations (caso de uso de IA 2: recomendación con restricciones)
Los nodos se descubren con GET /api/monitoring/v1/metrics/current (1 transacción más).

Uso:
  python herramientas_IA/video/carga_transacciones.py --gateway https://green-ai-gateway-dev.onrender.com \
      --iteraciones 200 --concurrencia 3 --out docs/evidencias/carga-video.csv

Autenticación (el token nunca se imprime ni se guarda):
  - Variable de entorno GREENAI_JWT, o
  - --login: pide correo y contraseña por consola (getpass) y usa la URL y la clave publishable de
    software/frontend/config.local.js (o SUPABASE_URL / SUPABASE_PUBLISHABLE_KEY).
Datos: la telemetría del simulador es SIMULADA; la carga mide disponibilidad y latencia, no ahorro energético.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import getpass
import json
import os
import re
import statistics
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
lock = threading.Lock()
rows: list[dict] = []


def http(method: str, url: str, token: str | None = None, body=None, headers=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    h = {"Accept": "application/json", **(headers or {})}
    if data is not None:
        h["Content-Type"] = "application/json"
    if token:
        h["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, raw = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read()
    except (urllib.error.URLError, TimeoutError) as e:
        status, raw = 0, str(e).encode()
    ms = (time.perf_counter() - t0) * 1000
    try:
        payload = json.loads(raw) if raw else None
    except json.JSONDecodeError:
        payload = None
    return status, payload, ms


def record(it: int, op: str, status: int, ms: float, node: str, extra: str = "") -> None:
    with lock:
        rows.append({"iteracion": it, "operacion": op, "http": status, "latencia_ms": round(ms, 1),
                     "nodo": node, "detalle": extra, "hora": dt.datetime.now().strftime("%H:%M:%S")})


def supabase_login() -> str:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_PUBLISHABLE_KEY")
    cfg = ROOT / "software/frontend/config.local.js"
    if (not url or not key) and cfg.exists():
        text = cfg.read_text(encoding="utf-8")
        url = url or re.search(r"supabaseUrl:\s*'([^']+)'", text).group(1)
        key = key or re.search(r"supabasePublishableKey:\s*'([^']+)'", text).group(1)
    if not url or not key:
        sys.exit("Falta SUPABASE_URL/SUPABASE_PUBLISHABLE_KEY (o software/frontend/config.local.js).")
    email = input("Correo de la cuenta Green AI: ").strip()
    password = getpass.getpass("Contraseña (no se muestra): ")
    status, p, _ = http("POST", f"{url}/auth/v1/token?grant_type=password", body={"email": email, "password": password},
                        headers={"apikey": key})
    if status != 200 or not p or "access_token" not in p:
        sys.exit(f"Inicio de sesión rechazado (HTTP {status}).")
    return p["access_token"]


def iteration(it: int, gw: str, token: str, node: dict) -> None:
    end = dt.datetime.now(dt.timezone.utc).replace(microsecond=0) - dt.timedelta(seconds=30)
    start = end - dt.timedelta(hours=2)
    fmt = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
    q = urllib.parse.urlencode({"cluster": node["cluster"], "resourceId": node["id"], "stepSeconds": "15",
                                "start": fmt(start), "end": fmt(end)})
    label = f"{node['cluster']}/{node['id']}"
    s, ds, ms = http("GET", f"{gw}/api/processing/v1/prediction/dataset?{q}", token)
    record(it, "dataset", s, ms, label, f"{len((ds or {}).get('features', []))} muestras" if s == 200 else "")
    if s != 200 or not ds or not ds.get("features"):
        return
    s, pr, ms = http("POST", f"{gw}/api/prediction/v1/predictions", token, body=ds)
    record(it, "prediccion", s, ms, label, f"{pr.get('value'):.2f} %" if s == 200 and pr else "")
    telemetry = {"resource": ds["resource"], "observedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
                 "origin": "simulated", "memoryPercent": 40, "latencyP95Ms": 100, "errorRatePercent": 0.1}
    s, rc, ms = http("POST", f"{gw}/api/recommendations/v1/recommendations", token,
                     body={"dataset": ds, "telemetry": telemetry})
    record(it, "recomendacion", s, ms, label, (rc or {}).get("status", "") if s == 200 else "")


def pct(values: list[float], p: float) -> float:
    if not values:
        return float("nan")
    v = sorted(values)
    return v[min(len(v) - 1, int(round(p / 100 * (len(v) - 1))))]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gateway", default="https://green-ai-gateway-dev.onrender.com")
    ap.add_argument("--iteraciones", type=int, default=200, help="3 transacciones por iteración (200 → 600)")
    ap.add_argument("--concurrencia", type=int, default=3)
    ap.add_argument("--login", action="store_true")
    ap.add_argument("--out", type=Path, default=ROOT / "docs/evidencias/carga-video.csv")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    gw = a.gateway.rstrip("/")
    token = os.environ.get("GREENAI_JWT") or (supabase_login() if a.login else None)
    if not token:
        sys.exit("Define GREENAI_JWT o usa --login.")

    s, cur, ms = http("GET", f"{gw}/api/monitoring/v1/metrics/current?metric=node.cpu.utilization", token)
    record(0, "descubrir_nodos", s, ms, "-")
    series = (cur or {}).get("series") or (cur or {}).get("data") or []
    nodes = [{"cluster": x["resource"]["cluster"], "id": x["resource"]["id"]} for x in series
             if isinstance(x, dict) and x.get("resource", {}).get("id")]
    if s != 200 or not nodes:
        sys.exit(f"No se pudieron descubrir nodos (HTTP {s}). ¿Servicios despiertos y sesión válida?")
    print(f"Gateway {gw} · {len(nodes)} nodos · {a.iteraciones} iteraciones × 3 = {a.iteraciones * 3 + 1} transacciones")

    t0 = time.perf_counter()
    with cf.ThreadPoolExecutor(max_workers=a.concurrencia) as ex:
        futs = [ex.submit(iteration, i + 1, gw, token, nodes[i % len(nodes)]) for i in range(a.iteraciones)]
        for k, _ in enumerate(cf.as_completed(futs), 1):
            if k % 10 == 0 or k == a.iteraciones:
                with lock:
                    ok = sum(1 for r in rows if r["http"] == 200)
                    print(f"  [{k:>4}/{a.iteraciones}] transacciones: {len(rows):>4} · HTTP 200: {ok}")
    total_s = time.perf_counter() - t0

    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["iteracion"], r["operacion"])))

    print(f"\nResumen ({len(rows)} transacciones en {total_s:.0f} s; datos de telemetría simulados)")
    print(f"{'operación':<16}{'n':>6}{'200':>6}{'otros':>7}{'p50 ms':>9}{'p95 ms':>9}")
    for op in ("descubrir_nodos", "dataset", "prediccion", "recomendacion"):
        sel = [r for r in rows if r["operacion"] == op]
        lat = [r["latencia_ms"] for r in sel if r["http"] == 200]
        ok = sum(1 for r in sel if r["http"] == 200)
        print(f"{op:<16}{len(sel):>6}{ok:>6}{len(sel) - ok:>7}{pct(lat, 50):>9.0f}{pct(lat, 95):>9.0f}")
    print("Códigos HTTP:", dict(Counter(r["http"] for r in rows)))
    recs = Counter(r["detalle"] for r in rows if r["operacion"] == "recomendacion" and r["http"] == 200)
    if recs:
        print("Estados de recomendación:", dict(recs))
    print(f"CSV: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
