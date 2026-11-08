"""Arnés de verificación visual: sirve el frontend del worktree con sesión Supabase simulada
y proxifica /api/* a los servicios públicos de Render (datos reales simulados, sin JWT).
Uso: python harness.py <carpeta_frontend> <puerto>
Solo para pruebas locales; no se versiona."""
import base64, json, re, sys, urllib.request, urllib.error
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial

ROOT, PORT = sys.argv[1], int(sys.argv[2])
B = {
    "monitoring": "https://green-ai-monitoring-dev.onrender.com/api/",
    "processing": "https://green-ai-data-processing-dev.onrender.com/api/",
    "prediction": "https://green-ai-prediction-dev-zxly.onrender.com/",
    "recommendations": "https://green-ai-prediction-dev-zxly.onrender.com/",
}

def b64(d):
    return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")

TOKEN = f"{b64({'alg':'none'})}.{b64({'user_role':'OPERATOR','sub':'demo'})}.x"
STUB = f"""window.supabase={{createClient:()=>({{auth:{{
getSession:async()=>({{data:{{session:{{access_token:'{TOKEN}',user:{{email:'demo@greenai.test',user_metadata:{{full_name:'Demo Verificación'}}}}}}}},error:null}}),
refreshSession:async()=>({{data:{{session:null}},error:null}}),signOut:async()=>({{error:null}}),
onAuthStateChange:()=>({{data:{{subscription:{{unsubscribe(){{}}}}}}}})}}}})}};"""
CONFIG = f"window.GREEN_AI_CONFIG=Object.freeze({{supabaseUrl:'https://stub.supabase.co',supabasePublishableKey:'stub',gatewayBaseUrl:'http://127.0.0.1:{PORT}'}});"

class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def _send(self, code, body, ctype):
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def _proxy(self, method):
        m = re.match(r"^/api/(monitoring|processing|prediction|recommendations)/(.*)$", self.path)
        if not m: return self._send(404, b"{}", "application/json")
        url = B[m.group(1)] + m.group(2)
        n = int(self.headers.get("Content-Length") or 0)
        data = self.rfile.read(n) if n else None
        req = urllib.request.Request(url, data=data, method=method,
                                     headers={"Content-Type": self.headers.get("Content-Type", "application/json")})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                self._send(r.status, r.read(), r.headers.get("Content-Type", "application/json"))
        except urllib.error.HTTPError as e:
            self._send(e.code, e.read(), e.headers.get("Content-Type", "application/json"))
        except Exception as e:
            self._send(504, json.dumps({"code": "TIMEOUT", "detail": str(e)}).encode(), "application/json")
    def do_POST(self): self._proxy("POST")
    def do_OPTIONS(self): self._send(204, b"", "text/plain")
    def do_GET(self):
        p = self.path.split("?")[0]
        if p.startswith("/api/"): return self._proxy("GET")
        if p == "/config.local.js": return self._send(200, CONFIG.encode(), "application/javascript")
        if p == "/__stub_supabase.js": return self._send(200, STUB.encode(), "application/javascript")
        if p.endswith(".html"):
            try:
                t = open(ROOT + p, encoding="utf-8").read()
            except OSError:
                return self._send(404, b"nf", "text/plain")
            t = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/@supabase[^"]*"></script>',
                       '<script src="/__stub_supabase.js"></script>', t)
            return self._send(200, t.encode(), "text/html; charset=utf-8")
        return super().do_GET()

ThreadingHTTPServer(("127.0.0.1", PORT), partial(H, directory=ROOT)).serve_forever()
