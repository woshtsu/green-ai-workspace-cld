"""Lista los párrafos CAPTURA-PENDIENTE de un .md con su sección y la página del PDF exportado.

Uso: .tools/docx/Scripts/python herramientas_IA/exportacion/lista_capturas.py <doc.md> <doc.pdf>
Salida: tabla Markdown (ID | página | sección | qué capturar) por la salida estándar.
"""
from __future__ import annotations

import re
import sys

import pypdfium2 as pdfium


def main() -> int:
    md, pdf_path = sys.argv[1], sys.argv[2]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    pdf = pdfium.PdfDocument(pdf_path)
    pages = [pdf[i].get_textpage().get_text_range().replace("\r", "").replace("\n", " ") for i in range(len(pdf))]
    section = ""
    print("| ID | Página | Sección | Qué capturar |\n|---|---|---|---|")
    for line in open(md, encoding="utf-8"):
        h = re.match(r"#{1,4}\s+(.*)", line)
        if h:
            section = h.group(1).strip()
        m = re.match(r"CAPTURA-PENDIENTE-([A-Z]?\d+):\s*(.*)", line.strip())
        if m:
            cid = f"CAPTURA-PENDIENTE-{m.group(1)}"
            page = next((str(i + 1) for i, t in enumerate(pages) if cid in t.replace(" ", "") or cid in t), "?")
            print(f"| `{cid}` | {page} | {section[:60]} | {m.group(2).strip()} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
