"""Carga las páginas del frontend en Chrome headless y registra consola, errores y peticiones fallidas."""
import json
from playwright.sync_api import sync_playwright
PAGES = ["index.html", "login.html", "register.html", "dashboard.html", "network.html", "flows.html"]
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
                          proxy={"server": "http://127.0.0.1:35621", "bypass": "127.0.0.1,localhost"})
    for name in PAGES:
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page(); log = {"console": [], "pageerror": [], "failed": [], "responses": []}
        pg.on("console", lambda m, log=log: log["console"].append(f"[{m.type}] {m.text}"[:300]))
        pg.on("pageerror", lambda e, log=log: log["pageerror"].append(str(e)[:300]))
        pg.on("requestfailed", lambda r, log=log: log["failed"].append(f"{r.url[:120]} -> {r.failure}"))
        pg.on("response", lambda r, log=log: log["responses"].append(f"{r.status} {r.url[:110]}") if r.status >= 400 else None)
        try:
            pg.goto(f"http://127.0.0.1:13001/{name}", wait_until="networkidle", timeout=30000)
        except Exception as e:
            log["pageerror"].append(f"goto: {e}"[:300])
        pg.wait_for_timeout(1500)
        log["final_url"] = pg.url.replace("http://127.0.0.1:13001/", "")
        log["title"] = pg.title()
        pg.screenshot(path=f"/home/claude/run_logs/front/{name.replace('.html','')}.png")
        out[name] = log; ctx.close()
    b.close()
json.dump(out, open("/home/claude/run_logs/front/console.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(f"== {k} -> {v['final_url']} | título: {v['title']}")
    for key in ("console", "pageerror", "failed", "responses"):
        for line in v[key][:6]: print(f"   {key}: {line}")
