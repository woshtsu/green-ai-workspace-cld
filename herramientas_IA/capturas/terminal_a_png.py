"""Convierte la salida REAL de un comando (archivo de texto) en una imagen con aspecto de terminal.

Uso: python herramientas_IA/capturas/terminal_a_png.py <salida.png> --titulo T --bloque "comando" archivo.txt [--ultimas N] [--bloque ...]
Cada bloque muestra el prompt con el comando y las últimas N líneas de su salida. No modifica el texto, solo lo recorta.
La imagen se genera con Chrome headless (capturar_web.py), en segundo plano.
"""
import argparse, html, os, subprocess, sys, tempfile, datetime

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("salida"); ap.add_argument("--titulo", default="Terminal")
    ap.add_argument("--bloque", nargs=2, action="append", metavar=("COMANDO", "ARCHIVO"), required=True)
    ap.add_argument("--ultimas", type=int, default=12)
    a = ap.parse_args()
    partes = []
    for cmd, f in a.bloque:
        lineas = open(f, encoding="utf-8", errors="replace").read().rstrip().splitlines()
        lineas = [l for l in lineas if not l.startswith("exit ")][-a.ultimas:]
        partes.append(f'<div class="p">PS C:\\green-ai&gt; <b>{html.escape(cmd)}</b></div><pre>{html.escape(chr(10).join(lineas))}</pre>')
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    doc = f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#fff;font-family:Consolas,monospace}}
.w{{margin:16px;border:1px solid #c8c8c8;border-radius:8px;overflow:hidden}}
.t{{background:#e8e8e8;padding:8px 14px;font:13px Segoe UI,sans-serif;color:#333}}
.c{{background:#f8f8f8;padding:10px 16px;font-size:13px;color:#1e1e1e}}
.p{{color:#0b5394;margin-top:8px}} pre{{margin:2px 0 6px;white-space:pre-wrap}}
</style><div class="w"><div class="t">{html.escape(a.titulo)} — ejecutado el {fecha}</div><div class="c">{''.join(partes)}</div></div>"""
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8"); tmp.write(doc); tmp.close()
    alto = 120 + sum(min(a.ultimas, len(open(f, encoding='utf-8', errors='replace').read().splitlines())) * 19 + 40 for _, f in a.bloque)
    aqui = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, os.path.join(aqui, "capturar_web.py"), "file:///" + tmp.name.replace("\\", "/"),
                        a.salida, "--ancho", "1100", "--alto", str(alto), "--espera-ms", "500"])
    os.unlink(tmp.name)
    try:  # recorta el blanco sobrante
        from PIL import Image, ImageChops
        im = Image.open(a.salida).convert('RGB'); bg = Image.new('RGB', im.size, 'white')
        box = ImageChops.difference(im, bg).getbbox()
        if box: im.crop((0, 0, im.size[0], min(im.size[1], box[3] + 16))).save(a.salida)
    except ImportError:
        pass
    return r.returncode

if __name__ == "__main__":
    sys.exit(main())
