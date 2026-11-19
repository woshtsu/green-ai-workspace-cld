"""Pruebas funcionales de punta a punta de la auditoría (Fase 4).

Ejercita el stack nativo a través del Gateway Go con tokens ES256 de un emisor LOCAL de pruebas
(mismos claims que exige el Gateway: iss, aud=authenticated, role=authenticated, sub, exp, user_role).
Además prueba el acceso DIRECTO a los servicios internos (sin Gateway) para medir la superficie expuesta.
Solo biblioteca estándar. Salida: JSON con cada caso (estado, latencia, cabeceras relevantes).
"""
import json, time, sys, urllib.request, urllib.error, datetime as dt, random

T = json.load(open("/home/claude/idp/tokens.json"))
GW, PRED, DP, PROM, SIM, FRONT = (f"http://127.0.0.1:{p}" for p in (18081, 18002, 18003, 19090, 18000, 13001))
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
results = []


def call(method, url, body=None, headers=None, raw=False):
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    t0 = time.perf_counter()
    try:
        with opener.open(req, timeout=40) as r:
            payload, status, hdrs = r.read(), r.status, {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        payload, status, hdrs = e.read(), e.code, {k.lower(): v for k, v in e.headers.items()}
    except Exception as e:  # noqa: BLE001
        return 0, {"error": str(e)}, {}, (time.perf_counter() - t0) * 1000
    ms = (time.perf_counter() - t0) * 1000
    if raw:
        return status, payload.decode("utf-8", "replace"), hdrs, ms
    try:
        payload = json.loads(payload) if payload else None
    except json.JSONDecodeError:
        payload = payload[:400].decode("utf-8", "replace")
    return status, payload, hdrs, ms


def case(cid, name, method, url, expected, body=None, token=None, headers=None, check=None, raw=False, note=""):
    h = dict(headers or {})
    if token:
        h["Authorization"] = f"Bearer {T[token]}"
    status, payload, hdrs, ms = call(method, url, body, h, raw)
    ok = status == expected and (check is None or bool(check(payload, hdrs)))
    excerpt = payload if isinstance(payload, (str, type(None))) else json.dumps(payload, ensure_ascii=False)
    results.append({"id": cid, "caso": name, "metodo": method, "url": url.replace("http://127.0.0.1", ""),
                    "token": token or "-", "esperado": expected, "obtenido": status, "ok": ok,
                    "latencia_ms": round(ms, 1), "x_request_id": hdrs.get("x-request-id", ""),
                    "extracto": (excerpt or "")[:260], "nota": note})
    print(f"{'PASS' if ok else 'FAIL'} {cid} {status:>3} (esp. {expected}) {ms:7.1f} ms  {name}")
    return status, payload


def dataset(n=960, step=15, resource_id="HW001"):
    rnd = random.Random(7)
    end = dt.datetime.now(dt.timezone.utc).replace(microsecond=0) - dt.timedelta(seconds=step)
    start = end - dt.timedelta(seconds=step * (n - 1))
    ts = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
    feats = [{"timestamp": ts(start + dt.timedelta(seconds=i * step)),
              "cpu_utilization": round(55 + 20 * rnd.uniform(-1, 1), 3), "origin": "simulated", "quality": "ok"}
             for i in range(n)]
    period = {"start": ts(start), "end": ts(end)}
    return {"schemaVersion": "1.0", "contractStatus": "provisional", "datasetId": "auditoria-e2e-001",
            "requestedPeriod": period, "period": period,
            "resource": {"type": "node", "cluster": "sim-lab", "id": resource_id},
            "features": feats, "units": {"cpu_utilization": "%"}, "origins": ["simulated"], "dataStatus": "partial",
            "excludedSampleCount": 0, "warnings": ["Dataset SIMULADO de la auditoría."]}


def now_iso():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


hist = "start=2026-07-10T00:00:00Z&end=2026-07-12T00:00:00Z&hardwareId=HW045"
ds = dataset()
tele = {"resource": ds["resource"], "observedAt": now_iso(), "origin": "simulated",
        "memoryPercent": 60, "latencyP95Ms": 120, "errorRatePercent": 0.2}
energy = {"origin": "simulated", "samples": [
    {"timestamp": "2026-11-19T10:00:00Z", "watts": 400}, {"timestamp": "2026-11-19T10:05:00Z", "watts": 420},
    {"timestamp": "2026-11-19T10:10:00Z", "watts": 410}]}

# --- Gateway: rutas públicas y autenticación ---
case("E01", "Gateway liveness pública", "GET", f"{GW}/actuator/health/liveness", 200)
case("E02", "Gateway sirve OpenAPI publicado", "GET", f"{GW}/openapi/gateway-v0.1.yaml", 200, raw=True)
case("E03", "Sin token → 401 + WWW-Authenticate", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}", 401,
     check=lambda p, h: h.get("www-authenticate", "").startswith("Bearer"))
case("E04", "Token expirado → 401", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}", 401, token="EXPIRED")
case("E05", "Token anónimo (is_anonymous) → 401", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}", 401, token="ANON")
case("E06", "Token válido sin user_role → 403", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}", 403, token="NONE")
case("E07", "Ruta no publicada con ADMIN → 403 (deny-all)", "GET", f"{GW}/api/prediction/v1/health", 403, token="ADMIN",
     note="Fuera de la tabla de rutas")
case("E08", "Método no publicado (DELETE) con ADMIN → 403", "DELETE", f"{GW}/api/prediction/v1/predictions", 403, token="ADMIN")

# --- Históricos (Data Processing con SQLite) ---
case("E10", "Históricos paginados (OPERATOR)", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}&limit=5", 200,
     token="OPERATOR", check=lambda p, h: p["recordCount"] == 5 and p["nextCursor"] and p["records"][0]["source"] == "sqlite")
s, page1 = call("GET", f"{GW}/api/processing/v1/historical-logs?{hist}&limit=5", headers={"Authorization": f"Bearer {T['VIEWER']}"})[:2]
cur = page1.get("nextCursor") if isinstance(page1, dict) else ""
case("E11", "Página 2 por cursor keyset (VIEWER)", "GET",
     f"{GW}/api/processing/v1/historical-logs?{hist}&limit=5&cursor={cur}", 200, token="VIEWER",
     check=lambda p, h: p["records"][0]["timestamp"] >= page1["records"][-1]["timestamp"])
case("E12", "Cursor manipulado → 422", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}&limit=5&cursor=abc", 422, token="VIEWER")
case("E13", "Rango > 31 días → 422", "GET",
     f"{GW}/api/processing/v1/historical-logs?start=2026-07-01T00:00:00Z&end=2026-09-01T00:00:00Z&hardwareId=HW001", 422, token="VIEWER")
case("E14", "Fecha sin zona horaria → 422", "GET",
     f"{GW}/api/processing/v1/historical-logs?start=2026-07-10T00:00:00&end=2026-07-11T00:00:00&hardwareId=HW001", 422, token="VIEWER")
case("E15", "Reporte resumen JSON (VIEWER)", "GET", f"{GW}/api/processing/v1/reports/historical-summary?{hist}", 200,
     token="VIEWER", check=lambda p, h: p.get("recordCount", 0) > 0)
case("E16", "Reporte resumen CSV (VIEWER)", "GET", f"{GW}/api/processing/v1/reports/historical-summary?{hist}&format=csv", 200,
     token="VIEWER", raw=True, check=lambda p, h: p.startswith("cpu_mean"))

# --- Predicción, recomendación y energía ---
case("E20", "Predicción 15 min (OPERATOR)", "POST", f"{GW}/api/prediction/v1/predictions", 200, body=ds, token="OPERATOR",
     check=lambda p, h: p["origin"] == "estimated" and 0 <= p["value"] <= 100)
case("E21", "Predicción con VIEWER → 403 (solo lectura)", "POST", f"{GW}/api/prediction/v1/predictions", 403, body=ds, token="VIEWER")
case("E22", "Recomendación con telemetría (ADMIN)", "POST", f"{GW}/api/recommendations/v1/recommendations", 200,
     body={"dataset": ds, "telemetry": tele}, token="ADMIN", check=lambda p, h: p["executionAllowed"] is False)
case("E23", "Recomendación sin telemetría → not_evaluable", "POST", f"{GW}/api/recommendations/v1/recommendations", 200,
     body={"dataset": ds}, token="OPERATOR", check=lambda p, h: p["status"] == "not_evaluable")
case("E24", "Energía trapezoidal (OPERATOR)", "POST", f"{GW}/api/recommendations/v1/energy", 200, body=energy, token="OPERATOR",
     check=lambda p, h: abs(p["energyKwh"] - 0.06875) < 1e-9)
case("E25", "Energía con hueco > 300 s → 422", "POST", f"{GW}/api/recommendations/v1/energy", 422, token="OPERATOR",
     body={"origin": "simulated", "samples": [{"timestamp": "2026-11-19T10:00:00Z", "watts": 1},
                                               {"timestamp": "2026-11-19T11:00:00Z", "watts": 1}]})
case("E26", "Factor CO2e sin fuente → 422", "POST", f"{GW}/api/recommendations/v1/energy", 422, token="OPERATOR",
     body={**energy, "emissionFactorKgPerKwh": 0.2})
short = dataset(n=10)
case("E27", "Ventana de 10 muestras de 15 s (remuestreo a 5 min) → 422 INSUFFICIENT_DATA", "POST", f"{GW}/api/prediction/v1/predictions", 422, body=short, token="OPERATOR")

# --- Dependencias caídas (Monitoring Java no construible en el entorno) ---
case("E30", "Monitoring vía Gateway con upstream caído → 503 sin detalles", "GET",
     f"{GW}/api/monitoring/v1/metrics/catalog", 503, token="OPERATOR")
e = (dt.datetime.now(dt.timezone.utc).replace(microsecond=0) - dt.timedelta(minutes=1))
st = e - dt.timedelta(hours=1)
f = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
case("E31", "Dataset de predicción sin Monitoring → 503 SOURCE_UNAVAILABLE", "GET",
     f"{GW}/api/processing/v1/prediction/dataset?start={f(st)}&end={f(e)}&cluster=sim-lab&resourceId=HW001", 503, token="OPERATOR")

# --- CORS y correlación ---
case("E40", "Preflight CORS origen permitido", "OPTIONS", f"{GW}/api/prediction/v1/predictions", 200,
     headers={"Origin": "http://127.0.0.1:13001", "Access-Control-Request-Method": "POST",
              "Access-Control-Request-Headers": "authorization,content-type"})
case("E41", "Preflight CORS origen ajeno → 403", "OPTIONS", f"{GW}/api/prediction/v1/predictions", 403,
     headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"})
case("E42", "X-Request-Id del cliente se conserva", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}&limit=1", 200,
     token="VIEWER", headers={"X-Request-Id": "audit-req-0001"}, check=lambda p, h: h.get("x-request-id") == "audit-req-0001")
case("E43", "X-Request-Id malicioso se reemplaza", "GET", f"{GW}/api/processing/v1/historical-logs?{hist}&limit=1", 200,
     token="VIEWER", headers={"X-Request-Id": "<script>"}, check=lambda p, h: h.get("x-request-id") != "<script>")

# --- Superficie expuesta: acceso DIRECTO a servicios internos (sin Gateway) ---
case("E50", "Data Processing directo sin token (históricos)", "GET", f"{DP}/api/v1/historical-logs?{hist}&limit=2", 200,
     note="Sin autenticación propia: depende de que el puerto no sea público")
case("E51", "Prediction directo sin token (inferencia)", "POST", f"{PRED}/v1/predictions", 200, body=ds,
     note="Sin autenticación propia")
case("E52", "Prediction /metrics público", "GET", f"{PRED}/metrics", 200, raw=True)
case("E53", "Prediction /docs (Swagger) público", "GET", f"{PRED}/docs", 200, raw=True)
case("E54", "Prediction X-Request-Id sin validar se refleja", "GET", f"{PRED}/health/live", 200,
     headers={"X-Request-Id": "<b>x</b>"}, check=lambda p, h: h.get("x-request-id") == "<b>x</b>",
     note="Gateway y Data Processing sí validan el formato")

# --- Observabilidad ---
case("E60", "Prometheus: targets UP", "GET", f"{PROM}/api/v1/targets", 200,
     check=lambda p, h: all(t["health"] == "up" for t in p["data"]["activeTargets"]))
case("E61", "Prometheus: reglas de alerta cargadas", "GET", f"{PROM}/api/v1/rules", 200,
     check=lambda p, h: sum(len(g["rules"]) for g in p["data"]["groups"]) == 6)
case("E62", "Simulator expone node_cpu_seconds_total", "GET", f"{SIM}/metrics", 200, raw=True,
     check=lambda p, h: "node_cpu_seconds_total" in p)
case("E63", "Frontend sirve dashboard.html", "GET", f"{FRONT}/dashboard.html", 200, raw=True)

ok = sum(r["ok"] for r in results)
print(f"\n{ok}/{len(results)} casos conformes")
json.dump({"ejecutado": now_iso(), "conformes": ok, "total": len(results), "casos": results},
          open(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/run_logs/e2e.json", "w"), ensure_ascii=False, indent=1)
