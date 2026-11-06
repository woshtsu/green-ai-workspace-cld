"""Smoke HTTP del stack local green-ai-mono (solo biblioteca estándar).

Uso: python software/infraestructura/smoke/smoke.py [--out docs/evidencias/smoke-AAAAMMDD.json]
Requiere el stack levantado con docker-compose.yml + compose.swagger.yaml (puertos MONO_* por defecto).

Datos: fixture SIMULADO regenerado con fechas actuales (las reglas de recomendación rechazan datos vencidos).
Limitaciones: no autentica a un usuario real de Supabase; no prueba precisión del modelo ni ahorro energético.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import urllib.error
import urllib.request

P = {k: int(os.environ.get(f"MONO_{k}_PORT", v)) for k, v in
     {"SIMULATOR": 18000, "PROMETHEUS": 19090, "MONITORING": 18080, "GATEWAY": 18081,
      "FRONTEND": 13001, "PREDICTION_SWAGGER": 18002, "DATAPROC_SWAGGER": 18003}.items()}
H = "http://127.0.0.1"
FRONT_ORIGIN = f"{H}:{P['FRONTEND']}"


def call(method: str, url: str, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw, status, hdrs = r.read(), r.status, dict(r.headers)
    except urllib.error.HTTPError as e:
        raw, status, hdrs = e.read(), e.code, dict(e.headers)
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, {"error": str(e)}, {}
    try:
        payload = json.loads(raw) if raw else None
    except json.JSONDecodeError:
        payload = raw[:300].decode("utf-8", "replace")
    return status, payload, hdrs


def fixture(n: int = 960, step: int = 15) -> dict:
    rnd = random.Random(42)
    end = dt.datetime.now(dt.timezone.utc).replace(microsecond=0) - dt.timedelta(seconds=step)
    start = end - dt.timedelta(seconds=step * (n - 1))
    ts = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
    feats = [{"timestamp": ts(start + dt.timedelta(seconds=i * step)),
              "cpu_utilization": round(50 + 5 * rnd.uniform(-1, 1), 4), "origin": "simulated", "quality": "ok"}
             for i in range(n)]
    period = {"start": ts(start), "end": ts(end)}
    return {"schemaVersion": "1.0", "contractStatus": "provisional", "datasetId": "mono-smoke-simulated-001",
            "requestedPeriod": period, "period": period,
            "resource": {"type": "node", "cluster": "fixture-lab", "id": "fixture-node-01"},
            "features": feats, "units": {"cpu_utilization": "%"}, "origins": ["simulated"], "dataStatus": "partial",
            "excludedSampleCount": 0,
            "warnings": ["Fixture SIMULADO del smoke del monorepo (forma de GET /api/v1/prediction/dataset)."]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    ds = fixture()
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    telemetry = {"resource": ds["resource"], "observedAt": now, "origin": "simulated",
                 "memoryPercent": 40, "latencyP95Ms": 100, "errorRatePercent": 0.1}
    pred = f"{H}:{P['PREDICTION_SWAGGER']}"
    gw = f"{H}:{P['GATEWAY']}"
    results = []

    def check(name, method, url, expected, check_fn=None, body=None, headers=None):
        status, payload, hdrs = call(method, url, body, headers)
        ok = status == expected and (check_fn is None or bool(check_fn(payload, hdrs)))
        results.append({"name": name, "method": method, "url": url, "expected": expected, "status": status,
                        "passed": ok, "response": payload if not isinstance(payload, dict) or len(json.dumps(payload)) < 4000
                        else {k: payload[k] for k in list(payload)[:12]}})
        print(f"{'PASS' if ok else 'FAIL'} {status:>3} (esperado {expected}) {name}")

    check("prediction ready", "GET", f"{pred}/health/ready", 200, lambda p, h: p.get("modelLoaded") is True)
    check("OpenAPI de prediction incluye predicción y recomendaciones", "GET", f"{pred}/openapi.json", 200,
          lambda p, h: {"/v1/predictions", "/v1/recommendations"} <= set(p.get("paths", {})))
    check("predicción con fixture simulado", "POST", f"{pred}/v1/predictions", 200,
          lambda p, h: p.get("origin") == "estimated", body=ds)
    check("recomendación con telemetría simulada", "POST", f"{pred}/v1/recommendations", 200,
          lambda p, h: p.get("executionAllowed") is False and p.get("status") == "eligible_for_review",
          body={"dataset": ds, "telemetry": telemetry})
    check("recomendación inválida", "POST", f"{pred}/v1/recommendations", 422, body={"dataset": {}})
    check("data-processing health", "GET", f"{H}:{P['DATAPROC_SWAGGER']}/api/v1/health", 200)
    check("monitoring catálogo", "GET", f"{H}:{P['MONITORING']}/api/v1/metrics/catalog", 200)
    check("monitoring CPU actual (vía Prometheus, datos simulados)", "GET",
          f"{H}:{P['MONITORING']}/api/v1/metrics/current?metric=node.cpu.utilization", 200)
    for path in ("/api/prediction/v1/predictions", "/api/recommendations/v1/recommendations"):
        check(f"gateway rechaza anónimo {path}", "POST", gw + path, 401, body={})
    check("gateway rechaza JWT inválido", "GET", f"{gw}/api/monitoring/v1/metrics/catalog", 401,
          headers={"Authorization": "Bearer no.es.un.jwt"})
    check("gateway CORS preflight desde el frontend", "OPTIONS", f"{gw}/api/monitoring/v1/metrics/catalog", 200,
          lambda p, h: h.get("Access-Control-Allow-Origin") == FRONT_ORIGIN,
          headers={"Origin": FRONT_ORIGIN, "Access-Control-Request-Method": "GET",
                   "Access-Control-Request-Headers": "authorization"})
    check("frontend sirve login", "GET", f"{FRONT_ORIGIN}/login.html", 200)
    check("prometheus: targets prediction y simulator UP", "GET", f"{H}:{P['PROMETHEUS']}/api/v1/targets", 200,
          lambda p, h: {t["labels"]["job"] for t in p["data"]["activeTargets"] if t["health"] == "up"}
          >= {"green-ai-prediction", "green-ai-simulator"})

    report = {"timestamp": now, "dataKind": "simulated",
              "limitation": "No autentica un usuario real de Supabase; no prueba precisión observada ni ahorro.",
              "passed": sum(r["passed"] for r in results), "total": len(results), "results": results}
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n{report['passed']}/{report['total']} casos correctos")
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
