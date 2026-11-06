"""Extrae imágenes base64 incrustadas en un Markdown a archivos y las enlaza por ruta relativa.

Uso: python herramientas_IA/exportacion/extraer_imagenes_base64.py <origen.md> <destino.md> [--dir evidencias]
Mantiene el Markdown como fuente de verdad legible y deja las imágenes versionables por separado.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import re
from pathlib import Path

PATTERN = re.compile(r"data:image/(png|jpe?g|gif|svg\+xml|webp);base64,([A-Za-z0-9+/=\s]+)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--dir", default="evidencias")
    a = ap.parse_args()
    text = a.src.read_text(encoding="utf-8")
    out_dir = a.dst.parent / a.dir
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        ext = {"jpeg": "jpg", "svg+xml": "svg"}.get(m.group(1), m.group(1))
        data = base64.b64decode(re.sub(r"\s+", "", m.group(2)))
        name = f"img-{hashlib.sha256(data).hexdigest()[:12]}.{ext}"
        (out_dir / name).write_bytes(data)
        count += 1
        return f"{a.dir}/{name}"

    a.dst.write_text(PATTERN.sub(repl, text), encoding="utf-8")
    print(f"{count} imágenes extraídas en {out_dir}")


if __name__ == "__main__":
    main()
