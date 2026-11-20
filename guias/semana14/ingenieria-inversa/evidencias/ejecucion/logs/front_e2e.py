"""E2E del frontend REAL (copia de la auditoría) contra el Gateway Go local, con sesión de Supabase precargada.

Arnés: supabase-js 2.117.1 y Chart.js 4.4.8 se sirven desde los paquetes npm (los CDN están bloqueados en el entorno);
por eso la copia de prueba quita los atributos integrity (jsDelivr sirve builds auto-minificados no reproducibles offline).
La sesión se precarga en localStorage con el formato de supabase-js y un JWT ES256 del emisor local (rol configurable).
"""
import json, sys, time
from playwright.sync_api import sync_playwright
ROLE = sys.argv[1] if len(sys.argv) > 1 else "OPERATOR"
T = json.load(open("/home/claude/idp/tokens.json"))
LIBS = {"supabase-js@2.117.1": "/home/claude/cdn/supabase-supabase-js-2.117.1/package/dist/umd/supabase.js",
        "chart.js@4.4.8": "/home/claude/cdn/chart.js-4.4.8/package/dist/chart.umd.js"}
session = {"access_token": T[ROLE], "token_type": "bearer", "expires_in": 3600, "expires_at": int(time.time()) + 3500,
           "refresh_token": "audit-refresh", "user": {"id": "00000000-0000-4000-8000-000000000001", "aud": "authenticated",
           "role": "authenticated", "email": f"{ROLE.lower()}@auditoria.local", "user_metadata": {"full_name": f"Auditor {ROLE}"}}}
log = {"rol": ROLE, "api": [], "console": [], "pageerror": [], "pasos": []}

def route_cdn(route):
    url = route.request.url
    for key, path in LIBS.items():
        if key in url:
            return route.fulfill(path=path, content_type="application/javascript")
    return route.abort()

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 1000})
    ctx.route("https://cdn.jsdelivr.net/**", route_cdn)
    for host in ("https://cdnjs.cloudflare.com/**", "https://fonts.googleapis.com/**", "https://fonts.gstatic.com/**", "https://audit-placeholder.supabase.co/**"):
        ctx.route(host, lambda r: r.abort())
    ctx.add_init_script(f"localStorage.setItem('sb-audit-placeholder-auth-token', JSON.stringify({json.dumps(session)}));")
    pg = ctx.new_page()
    pg.on("console", lambda m: log["console"].append(f"[{m.type}] {m.text}"[:260]) if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: log["pageerror"].append(str(e)[:260]))
    pg.on("response", lambda r: log["api"].append({"status": r.status, "method": r.request.method,
        "url": r.url.split("?")[0].replace("http://127.0.0.1:18081", "GW")}) if ":18081/" in r.url else None)

    def step(name, fn, wait=2500, shot=None):
        try:
            fn(); pg.wait_for_timeout(wait); log["pasos"].append({"paso": name, "ok": True})
        except Exception as e:  # noqa: BLE001
            log["pasos"].append({"paso": name, "ok": False, "error": str(e)[:200]})
        if shot: pg.screenshot(path=f"/home/claude/run_logs/front/{ROLE.lower()}_{shot}.png", full_page=False)

    step("Abrir dashboard", lambda: pg.goto("http://127.0.0.1:13001/dashboard.html", wait_until="domcontentloaded"), 4000, "dashboard")
    log["usuario_mostrado"] = pg.evaluate("document.body.innerText.match(/(OPERATOR|ADMIN|VIEWER|PENDING)/)?.[0] || ''")
    step("Pestaña Reportes", lambda: pg.click("#tab-reportes"), 800)
    step("Ver resumen HW045", lambda: pg.click("#report-summary-btn"), 3000, "reportes")
    log["estado_reporte"] = pg.inner_text("#report-status")
    step("Pestaña Energía", lambda: pg.click("#tab-energia"), 800)
    step("Calcular con el ejemplo", lambda: pg.click("#energy-example"), 3000, "energia")
    log["estado_energia"] = pg.inner_text("#energy-status")[:300]
    step("Pestaña Predicción", lambda: pg.click("#tab-prediccion"), 2500, "prediccion")
    log["texto_prediccion"] = pg.inner_text("#panel-prediccion")[:400]
    step("Abrir Racks", lambda: pg.goto("http://127.0.0.1:13001/network.html", wait_until="domcontentloaded"), 4000, "racks")
    log["estado_racks"] = pg.evaluate("document.body.innerText.match(/Inventario[^\\n]*/)?.[0] || ''")[:300]
    b.close()
json.dump(log, open(f"/home/claude/run_logs/front/e2e_{ROLE.lower()}.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in log.items() if k != "api"}, ensure_ascii=False, indent=1)[:3000])
from collections import Counter
print("API:", Counter(f"{a['method']} {a['url']} {a['status']}" for a in log["api"]).most_common())
