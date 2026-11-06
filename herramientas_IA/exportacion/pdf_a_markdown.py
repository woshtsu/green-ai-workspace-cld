"""Convierte un informe PDF (exportado desde Word) a Markdown con imágenes y tablas.

Uso: python herramientas_IA/exportacion/pdf_a_markdown.py <informe.pdf> <salida.md> [--dir evidencias]

- Requiere PyMuPDF (fitz) >= 1.23 (tablas con Page.find_tables). No usa servicios externos.
- Títulos: entradas del índice del PDF (marcadores) y líneas en negrita de 13 pt o más.
- Imágenes: se guardan en --dir y se insertan en su posición vertical. Se omiten las imágenes
  repetidas en muchas páginas (logos de cabecera) y las líneas de cabecera/pie repetidas.
- Une las líneas de un mismo párrafo, también entre páginas; marca cada página con un comentario.
- Normaliza letras matemáticas Unicode (𝑅𝑖𝑐𝑎𝑟𝑑𝑜 -> Ricardo) y elimina espacios de ancho cero.
El resultado es una base fiel para editar; revisar visualmente tablas complejas y fórmulas.
"""
from __future__ import annotations

import argparse
import html
import re
import unicodedata
from collections import Counter
from pathlib import Path

import fitz

ZW = dict.fromkeys(map(ord, "​‌‍﻿"), None)
TERMINAL = (".", ":", ";", "?", "!", ")", "”", '"')


def clean(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(ZW)
    return re.sub(r"[ \t]+", " ", text).strip()


def shape(s: str) -> str:
    """Forma de una línea sin números: detecta pies como 'Página 12' repetidos en cada página."""
    return re.sub(r"\d+", "#", s)


def norm(s: str) -> str:
    return re.sub(r"[\W_]+", "", s.lower())


def inside(rect, boxes) -> bool:
    r = fitz.Rect(rect)
    return any(fitz.Rect(b).contains(r.tl + (1, 1)) for b in boxes)


def join(a: str, b: str) -> str:
    if a.endswith("-") and b[:1].islower():
        return a[:-1] + b
    return (a + " " + b).strip()


def table_markdown(rows) -> str:
    """Tabla Markdown desde las celdas: une con espacio las líneas de cada celda y escapa '|'."""
    rows = [[clean(html.unescape(c or "").replace("\n", " ")).replace("|", "\\|") for c in r] for r in rows if r]
    rows = [r for r in rows if any(r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = ["|" + "|".join(rows[0]) + "|", "|" + "|".join(["---"] * width) + "|"]
    lines += ["|" + "|".join(r) + "|" for r in rows[1:]]
    return "\n".join(lines)


def page_items(doc, page, pno, toc, skip_lines, skip_imgs, saved, out_dir, rel, state):
    items = []  # (y, x, kind, text)
    try:
        tables = page.find_tables().tables
    except Exception:
        tables = []
    tboxes = [t.bbox for t in tables]
    for t in tables:
        md = table_markdown(t.extract())
        if md:
            items.append((t.bbox[1], t.bbox[0], "tbl", md))
    page_toc = list(toc.get(pno, []))
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0 or inside(b["bbox"], tboxes):
            continue
        for l in b["lines"]:
            spans = [s for s in l["spans"] if s["text"].strip()]
            text = clean("".join(s["text"] for s in l["spans"]))
            if not text or shape(text) in skip_lines or re.fullmatch(r"\d{1,3}", text):
                continue
            bold = bool(spans) and all("Bold" in s["font"] or s["flags"] & 16 for s in spans)
            size = max((s["size"] for s in spans), default=0)
            kind = "p"
            for lvl, title in page_toc:
                if norm(title) and (norm(text) == norm(title) or norm(title).startswith(norm(text)) and len(norm(text)) > 8):
                    kind = f"h{lvl}"
                    break
            if kind.startswith("h") and ROMAN_PREFIX.match(text):
                kind = "h1"  # capítulos I..X de la consigna
            if kind == "p" and bold and len(text) < 160:
                kind = "h2" if size >= 15.5 else "h3" if size >= 12.5 else "b"
            code_font = not bold and 10.3 <= size <= 10.7
            if kind == "p" and code_font and (CODE.match(text) or state.get("code")):
                kind = "code"
            state["code"] = kind == "code"
            items.append((l["bbox"][1], l["bbox"][0], kind, text))
    for img in page.get_images(full=True):
        xref = img[0]
        if xref in skip_imgs:
            continue
        rects = page.get_image_rects(xref)
        if not rects or rects[0].width < 40 or rects[0].height < 25:
            continue  # iconos o separadores
        if xref not in saved:
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            name = f"p{pno:03d}-img{len(saved) + 1:03d}.png"
            pix.save(out_dir / name)
            saved[xref] = name
        for r in rects:
            items.append((r.y0, r.x0, "img", f"![Figura (página {pno})]({rel}/{saved[xref]})"))
    items.sort(key=lambda i: (round(i[0]), i[1]))
    return [(k, t) for _, _, k, t in items]


ROMAN = re.compile(r"^[IVX]{1,4}\.$")
ROMAN_PREFIX = re.compile(r"^[IVX]{1,4}\.\s")
ROMAN_SUFFIX = re.compile(r"^(.+?)\s+([IVX]{1,4}\.)$")
CODE = re.compile(r"^(import |from \w+ import |#\s|\w+(\[.+\])?\s*[+\-*/]?=\s*\S|for .+:$|if .+:$|def |return |print\(|\w+\.\w+\()")
NUMBERED = re.compile(r"^(?:\d+\.\d+(?:\.\d+)?|[IVX]{1,4}\.\d+(?:\.\d+)?)\.?\s")


def merge(parts, toc_titles=frozenset()):
    """Une líneas del mismo párrafo (también entre páginas) y títulos partidos en varias líneas."""
    out = []
    for kind, text in parts:
        prev = next((i for i in range(len(out) - 1, -1, -1) if out[i][0] != "page"), None)
        adjacent = prev is not None and prev == len(out) - 1
        # Numeral romano en línea aparte DESPUÉS del texto: "METODOLOGÍA EMPLEADA" + "IV."
        if (adjacent and ROMAN.match(text) and out[prev][0] in ("b", "h2", "h3") and not ROMAN.match(out[prev][1])
                and out[prev][1].isupper()):
            out[prev] = ("h1", f"{text} {out[prev][1].rstrip(':')}")
            continue
        if kind == "code":
            if out and out[-1][0] == "code":  # el código continúa aunque haya un salto de página
                out[-1] = ("code", out[-1][1] + "\n" + text)
                continue
            if adjacent and out[prev][0] == "code":
                out[prev] = ("code", out[prev][1] + "\n" + text)
            else:
                out.append(("code", text))
            continue
        # Numeral detrás del texto en la misma línea: "METODOLOGÍA EMPLEADA IV." -> "# IV. METODOLOGÍA EMPLEADA"
        m = ROMAN_SUFFIX.match(text) if kind in ("b", "h2", "h3") else None
        if m:
            kind, text = "h1", f"{m.group(2)} {m.group(1).rstrip(':')}"
        # Capítulo de la consigna: "**II.**" seguido de "**CONOCIMIENTOS ...**" -> "# II. CONOCIMIENTOS ..."
        if adjacent and out[prev][0] == "b" and ROMAN.match(out[prev][1]) and kind in ("b", "h2", "h3"):
            out[prev] = ("h1", f"{out[prev][1]} {text.rstrip(':')}")
            continue
        if kind == "b" and NUMBERED.match(text) and len(text) < 140:
            kind = "h3" if text.count(".") >= 2 and not text.endswith(".") else "h2"
            text = text.rstrip(":")
        # Título partido aunque su segunda línea se detectara con otro nivel.
        if (adjacent and out[prev][0].startswith("h") and kind.startswith("h") and len(text) < 60
                and not out[prev][1].endswith(TERMINAL) and norm(text) not in toc_titles
                and not NUMBERED.match(text) and not ROMAN.match(text)):
            out[prev] = (out[prev][0], join(out[prev][1], text))
            continue
        if prev is not None and out[prev][0] == kind and kind in ("p", "b", "h2", "h3", "h4"):
            last = out[prev][1]
            if kind == "p":
                ok = not last.endswith(TERMINAL) or text[:1].islower()
            else:  # títulos y negritas: solo líneas contiguas de un título partido
                ok = prev == len(out) - 1 and not last.endswith((".", ":")) and len(last) + len(text) < 220
            if ok:
                out[prev] = (kind, join(last, text))
                continue
        out.append((kind, text))
    return out


def captions(parts):
    """Usa el pie 'Figura ...' siguiente (aunque haya un salto de página) como texto alternativo."""
    parts = list(parts)
    for i, (kind, text) in enumerate(parts):
        if kind != "img":
            continue
        nxt = next((p for p in parts[i + 1:i + 4] if p[0] != "page"), None)
        if nxt and nxt[0] == "p" and re.match(r"^(Figura|Fig\.|Imagen|Gráfico)\s", nxt[1]) and len(nxt[1]) < 200:
            alt = nxt[1].replace("[", "(").replace("]", ")")
            parts[i] = ("img", re.sub(r"^!\[[^\]]*\]", f"![{alt}]", text))
    return parts


def render(parts):
    for kind, text in parts:
        if kind.startswith("h"):
            yield "#" * int(kind[1]) + " " + text
        elif kind == "b":
            yield f"**{text}**"
        elif kind == "code":
            yield f"```python\n{text}\n```"
        elif text.startswith("#"):
            yield "\\" + text  # no convertir en título un párrafo que empieza por '#'
        else:
            yield text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--dir", default="evidencias")
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    out_dir = a.out.parent / a.dir
    out_dir.mkdir(parents=True, exist_ok=True)

    img_pages, line_pages = Counter(), Counter()
    for page in doc:
        img_pages.update({x[0] for x in page.get_images(full=True)})
        line_pages.update({shape(clean(l)) for l in page.get_text().splitlines() if clean(l)})
    threshold = max(3, doc.page_count // 3)
    skip_imgs = {x for x, n in img_pages.items() if n >= threshold}
    skip_lines = {t for t, n in line_pages.items() if n >= threshold}

    toc = {}
    for lvl, title, pno in doc.get_toc():
        t = clean(title).rstrip(":")
        if t:
            toc.setdefault(pno, []).append((min(lvl + 1, 4), t))

    saved: dict[int, str] = {}
    parts, state = [], {}
    for pno, page in enumerate(doc, start=1):
        parts.append(("page", f"<!-- página {pno} -->"))
        parts.extend(page_items(doc, page, pno, toc, skip_lines, skip_imgs, saved, out_dir, a.dir, state))
    merged = merge(parts, frozenset(norm(t) for entries in toc.values() for _, t in entries))
    merged = captions(merged)
    text = "\n\n".join(render(merged))
    a.out.write_text(re.sub(r"\n{3,}", "\n\n", text) + "\n", encoding="utf-8")
    print(f"{doc.page_count} páginas, {len(saved)} imágenes, {sum(k == 'tbl' for k, _ in merged)} tablas, "
          f"{sum(k.startswith('h') for k, _ in merged)} títulos -> {a.out}")


if __name__ == "__main__":
    main()
