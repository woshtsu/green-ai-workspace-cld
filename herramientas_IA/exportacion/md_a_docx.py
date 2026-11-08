"""Exporta un Markdown del repositorio a un DOCX con diseño institucional (pandoc local + python-docx).

Uso (entorno local .tools/docx, ver herramientas_IA/README.md):
  .tools/docx/Scripts/python herramientas_IA/exportacion/md_a_docx.py <entrada.md> <salida.docx> \
      --encabezado "Green AI · Informe de la Unidad III" [--toc-antes "RESUMEN EJECUTIVO"]

Diseño (inspirado en la skill docx de Anthropic):
- Plantilla de estilos generada al vuelo desde la de pandoc: Calibri 11 justificado, títulos en verde Green AI
  con filete inferior, H1 en página nueva, bloques de cita y código sombreados, pies de figura centrados.
- Carátula: los párrafos con estilos «Portada …» (divs `::: {custom-style="Portada Titulo"}` en el .md) se
  centran y quedan en su propia página, sin encabezado ni pie.
- Encabezado con el título corto y pie «Página X de Y».
- Tablas a todo el ancho con cabecera verde, filas alternas y texto de 9 pt; imágenes centradas y ajustadas.
- Índice (campo TOC) antes del párrafo indicado; se rellena con actualizar_word.ps1 (sin aviso al abrir).
- Párrafos «CAPTURA-PENDIENTE…» en un recuadro amarillo para encontrarlos con Ctrl+B.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import pypandoc
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

MARK = "CAPTURA-PENDIENTE"
VERDE = "1F4E3D"     # primario
ACENTO = "2E7D32"    # acento
SUAVE = "EEF5F0"     # filas alternas / bloques
BORDE = "C9D6CE"
GRIS = "5F6B66"
FUENTE = "Calibri"

PORTADA = {  # estilo: (tamaño pt, negrita, color, espacio antes, espacio después, mayúsculas)
    "Portada Institucion": (16, True, VERDE, 0, 4, True),
    "Portada Escuela": (11, False, GRIS, 0, 36, False),
    "Portada Curso": (13, True, ACENTO, 0, 4, False),
    "Portada Titulo": (22, True, VERDE, 30, 12, False),
    "Portada Subtitulo": (13, False, GRIS, 0, 36, False),
    "Portada Etiqueta": (10, True, ACENTO, 14, 2, True),
    "Portada Texto": (11, False, "222222", 0, 0, False),
    "Portada Nota": (9, False, GRIS, 30, 0, False),
}


# ---------- utilidades XML ----------
def _set(el, tag: str, **attrs) -> OxmlElement:
    child = el.find(qn(tag))
    if child is None:
        child = OxmlElement(tag)
        el.append(child)
    for k, v in attrs.items():
        child.set(qn(k), str(v))
    return child


def shade(el_pr, fill: str) -> None:
    for old in el_pr.findall(qn("w:shd")):
        el_pr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    el_pr.append(shd)


def para_border(p_pr, sides: dict[str, tuple[str, int, int]]) -> None:
    """sides: {'bottom': (color, tamaño en 1/8 pt, espacio)}"""
    bdr = p_pr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        p_pr.append(bdr)
    for side, (color, sz, space) in sides.items():
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), str(space))
        e.set(qn("w:color"), color)
        bdr.append(e)


def add_field(paragraph, instr: str, placeholder: str = "") -> None:
    run = paragraph.add_run()
    for tag, kind in (("w:fldChar", "begin"), ("w:instrText", None), ("w:fldChar", "separate")):
        e = OxmlElement(tag)
        if kind:
            e.set(qn("w:fldCharType"), kind)
        else:
            e.set(qn("xml:space"), "preserve")
            e.text = instr
        run._r.append(e)
    if placeholder:
        paragraph.add_run(placeholder)
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    paragraph.add_run()._r.append(end)


# ---------- plantilla de estilos ----------
def style_font(st, size=None, bold=None, italic=None, color=None, font=FUENTE):
    f = st.font
    f.name = font
    rpr = st.element.get_or_add_rPr()
    fonts = _set(rpr, "w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(a), font)
    if size:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color:
        f.color.rgb = RGBColor.from_string(color)


def build_reference(path: Path) -> None:
    pandoc = pypandoc.get_pandoc_path()
    raw = subprocess.run([pandoc, "--print-default-data-file", "reference.docx"], capture_output=True, check=True).stdout
    path.write_bytes(raw)
    doc = Document(str(path))
    st = doc.styles
    normal = st["Normal"]
    style_font(normal, 11, color="222222")
    _set(normal.element.get_or_add_rPr(), "w:lang", **{"w:val": "es-PE"})
    pf = normal.paragraph_format
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.15
    for name in ("Body Text", "First Paragraph"):
        s = st[name]
        style_font(s, 11, color="222222")
        s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        s.paragraph_format.space_before = Pt(0)
        s.paragraph_format.space_after = Pt(6)
    st["Compact"].paragraph_format.space_after = Pt(2)
    heads = {"Heading 1": (18, VERDE, 0, 10), "Heading 2": (14, ACENTO, 14, 6), "Heading 3": (12, VERDE, 12, 4),
             "Heading 4": (11, ACENTO, 10, 4), "Heading 5": (11, GRIS, 8, 2)}
    for name, (size, color, before, after) in heads.items():
        s = st[name]
        style_font(s, size, bold=True, italic=False, color=color)
        s.paragraph_format.space_before = Pt(before)
        s.paragraph_format.space_after = Pt(after)
        s.paragraph_format.keep_with_next = True
        s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h1 = st["Heading 1"]
    h1.paragraph_format.page_break_before = True
    para_border(h1.element.get_or_add_pPr(), {"bottom": (ACENTO, 12, 4)})
    para_border(st["Heading 2"].element.get_or_add_pPr(), {"bottom": (BORDE, 4, 2)})
    for name in ("Title", "Subtitle"):
        style_font(st[name], 24 if name == "Title" else 14, bold=name == "Title", color=VERDE)
    bt = st["Block Text"]
    style_font(bt, 10.5, italic=False, color="2B3A33")
    bpr = bt.element.get_or_add_pPr()
    shade(bpr, SUAVE)
    para_border(bpr, {"left": (ACENTO, 18, 8)})
    bt.paragraph_format.left_indent = Cm(0.4)
    bt.paragraph_format.right_indent = Cm(0.2)
    for name in ("Image Caption", "Table Caption"):
        s = st[name]
        style_font(s, 9, italic=True, bold=False, color=GRIS)
        s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        s.paragraph_format.space_before = Pt(2)
        s.paragraph_format.space_after = Pt(10)
    if "Captioned Figure" in [x.name for x in st]:
        st["Captioned Figure"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if "Figure" in [x.name for x in st]:
        st["Figure"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if "Source Code" in [x.name for x in st]:
        sc = st["Source Code"]
        style_font(sc, 8.5, font="Consolas")
        shade(sc.element.get_or_add_pPr(), "F4F6F5")
    if "Verbatim Char" in [x.name for x in st]:
        style_font(st["Verbatim Char"], 9, font="Consolas", color="1F4E3D")
    if "Hyperlink" in [x.name for x in st]:
        st["Hyperlink"].font.color.rgb = RGBColor.from_string(ACENTO)
    for name, (size, bold, color, before, after, caps) in PORTADA.items():
        s = st[name] if name in [x.name for x in st] else st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = normal
        style_font(s, size, bold=bold, color=color)
        s.font.all_caps = caps
        s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        s.paragraph_format.space_before = Pt(before)
        s.paragraph_format.space_after = Pt(after)
    fix_ppr(doc.styles.element)
    doc.save(str(path))


# ---------- post-proceso ----------
def style_tables(doc, width) -> None:
    for t in doc.tables:
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_pr = t._tbl.tblPr
        for old in tbl_pr.findall(qn("w:tblBorders")):
            tbl_pr.remove(old)
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{edge}")
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), "4")
            e.set(qn("w:color"), BORDE)
            borders.append(e)
        tbl_pr.append(borders)
        _set(tbl_pr, "w:tblW", **{"w:w": "5000", "w:type": "pct"})
        mar = _set(tbl_pr, "w:tblCellMar")
        for side in ("top", "bottom"):
            _set(mar, f"w:{side}", **{"w:w": "40", "w:type": "dxa"})
        for side in ("left", "right"):
            _set(mar, f"w:{side}", **{"w:w": "80", "w:type": "dxa"})
        for i, row in enumerate(t.rows):
            if i == 0:
                tr_pr = row._tr.get_or_add_trPr()
                _set(tr_pr, "w:tblHeader")
            for cell in row.cells:
                tc_pr = cell._tc.get_or_add_tcPr()
                if i == 0:
                    shade(tc_pr, VERDE)
                    _set(tc_pr, "w:vAlign", **{"w:val": "center"})
                elif i % 2 == 0:
                    shade(tc_pr, SUAVE)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(1)
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for r in p.runs:
                        r.font.size = Pt(9)
                        if i == 0:
                            r.font.bold = True
                            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


TBLPR_ORDER = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize",
               "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook",
               "tblCaption", "tblDescription"]
TCPR_ORDER = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap", "tcMar",
              "textDirection", "tcFitText", "vAlign", "hideMark"]


def reorder(el, order: list[str]) -> None:
    rank = {qn(f"w:{n}"): i for i, n in enumerate(order)}
    kids = list(el)
    for k in kids:
        el.remove(k)
    for k in sorted(kids, key=lambda k: rank.get(k.tag, len(order))):
        el.append(k)


PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr",
             "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
             "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid",
             "spacing", "ind", "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc", "textDirection",
             "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"]


def fix_ppr(root) -> None:
    for ppr in root.iter(qn("w:pPr")):
        reorder(ppr, PPR_ORDER)


def fix_table_xml(doc) -> None:
    for t in doc.tables:
        reorder(t._tbl.tblPr, TBLPR_ORDER)
        for tc in t._tbl.iter(qn("w:tc")):
            pr = tc.find(qn("w:tcPr"))
            if pr is not None:
                reorder(pr, TCPR_ORDER)


def set_column_widths(t, total_emu: int) -> None:
    """Anchos proporcionales al contenido (raíz de la longitud media, con mínimos), diseño fijo."""
    import math
    ncols = len(t.columns)
    lens = [[] for _ in range(ncols)]
    for row in t.rows:
        for j, cell in enumerate(row.cells[:ncols]):
            lens[j].append(len(cell.text.strip()))
    weights = []
    for j in range(ncols):
        avg = sum(lens[j]) / max(1, len(lens[j]))
        longest_word = max((len(w) for c in t.columns[j].cells for w in c.text.split()), default=4)
        head_word = max((len(w) for w in t.rows[0].cells[j].text.split()), default=2)
        weights.append(max(math.sqrt(max(avg, 1)) * 3, min(longest_word, 16) * 1.25, min(head_word, 14) * 1.6, 4))
    total_twips = int(total_emu / 635)
    widths = [int(total_twips * w / sum(weights)) for w in weights]
    tbl = t._tbl
    tbl_pr = tbl.tblPr
    _set(tbl_pr, "w:tblLayout", **{"w:type": "fixed"})
    _set(tbl_pr, "w:tblW", **{"w:w": str(sum(widths)), "w:type": "dxa"})
    grid = tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(w))
    for row in t.rows:
        for j, cell in enumerate(row.cells[:ncols]):
            _set(cell._tc.get_or_add_tcPr(), "w:tcW", **{"w:w": str(widths[j]), "w:type": "dxa"})


def landscape_wide_tables(doc, min_cols: int = 9) -> int:
    """Coloca cada tabla ancha en su propia sección horizontal."""
    import copy
    body = doc.element.body
    base = body.sectPr
    count = 0
    for t in list(doc.tables):
        if len(t.columns) < min_cols:
            continue
        tbl = t._tbl
        before = OxmlElement("w:p")
        sp = copy.deepcopy(base)
        if count:
            for tp in sp.findall(qn("w:titlePg")):
                sp.remove(tp)
        before.append(OxmlElement("w:pPr"))
        before[0].append(sp)
        tbl.addprevious(before)
        after = OxmlElement("w:p")
        lp = copy.deepcopy(base)
        for tp in lp.findall(qn("w:titlePg")):
            lp.remove(tp)
        pgsz = lp.find(qn("w:pgSz"))
        w, h = pgsz.get(qn("w:w")), pgsz.get(qn("w:h"))
        pgsz.set(qn("w:w"), h)
        pgsz.set(qn("w:h"), w)
        pgsz.set(qn("w:orient"), "landscape")
        after.append(OxmlElement("w:pPr"))
        after[0].append(lp)
        tbl.addnext(after)
        # el título/párrafo previo a la tabla (p. ej. «Tabla …») pasa a la hoja horizontal
        set_column_widths(t, Cm(29.7 - 5.0))
        count += 1
    if count:
        for tp in base.findall(qn("w:titlePg")):
            base.remove(tp)
    return count


def mark_pending(p) -> None:
    ppr = p._p.get_or_add_pPr()
    shade(ppr, "FFF4C2")
    para_border(ppr, {s: ("E0A800", 8, 4) for s in ("top", "left", "bottom", "right")})
    for r in p.runs:
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x6B, 0x4E, 0x00)


def insert_toc(doc, before_text: str) -> bool:
    target = next((p for p in doc.paragraphs if p.text.strip().upper().startswith(before_text.upper())), None)
    if target is None:
        return False
    title = target.insert_paragraph_before()
    title.paragraph_format.page_break_before = True
    title.paragraph_format.space_after = Pt(12)
    run = title.add_run("Índice")
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor.from_string(VERDE)
    para_border(title._p.get_or_add_pPr(), {"bottom": (ACENTO, 12, 4)})
    fld = target.insert_paragraph_before()
    add_field(fld, r'TOC \o "1-2" \h \z \u', "Índice: se genera al actualizar los campos (F9).")
    target.paragraph_format.page_break_before = True
    return True


def header_footer(doc, encabezado: str) -> None:
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.top_margin, sec.bottom_margin = Cm(2.5), Cm(2.2)
    sec.header_distance = sec.footer_distance = Cm(1.1)
    sec.different_first_page_header_footer = True
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = hp.add_run(encabezado)
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor.from_string(GRIS)
    para_border(hp._p.get_or_add_pPr(), {"bottom": (BORDE, 4, 4)})
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for txt, instr in (("Página ", "PAGE"), (" de ", "NUMPAGES")):
        t = fp.add_run(txt)
        t.font.size = Pt(8.5)
        t.font.color.rgb = RGBColor.from_string(GRIS)
        add_field(fp, instr, "1")
    for r in fp.runs:
        r.font.size = Pt(8.5)


def postprocess(path: Path, encabezado: str, toc_before: str | None) -> int:
    doc = Document(str(path))
    header_footer(doc, encabezado)
    sec = doc.sections[0]
    width = sec.page_width - sec.left_margin - sec.right_margin
    marks = 0
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt.startswith(MARK):
            marks += 1
            mark_pending(p)
        elif (txt.startswith(("Figura ", "Tabla ")) and len(txt) < 400
              and p.runs and all(r.italic for r in p.runs if r.text.strip())):
            p.style = doc.styles["Image Caption"]
        if p._p.findall(".//" + qn("w:drawing")):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
    style_tables(doc, width)
    for t in doc.tables:
        if len(t.columns) < 9:
            set_column_widths(t, width)
    landscape_wide_tables(doc)
    fix_table_xml(doc)
    fix_ppr(doc.element.body)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if p.text.strip().startswith(MARK):
                        marks += 1
                        mark_pending(p)
    for shape in doc.inline_shapes:
        if shape.width > width:
            ratio = width / shape.width
            shape.width, shape.height = int(shape.width * ratio), int(shape.height * ratio)
        max_h = Cm(18)
        if shape.height > max_h:
            ratio = max_h / shape.height
            shape.width, shape.height = int(shape.width * ratio), int(shape.height * ratio)
    # El primer H1 tras la carátula no necesita salto extra si ya lo pone el índice
    if toc_before:
        insert_toc(doc, toc_before)
    fix_ppr(doc.element.body)
    for part in (doc.sections[0].header, doc.sections[0].footer):
        fix_ppr(part._element)
    doc.save(str(path))
    return marks


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", type=Path)
    ap.add_argument("salida", type=Path)
    ap.add_argument("--encabezado", default="Green AI")
    ap.add_argument("--toc-antes", default=None, metavar="TEXTO",
                    help="Inserta el índice antes del primer párrafo que empieza por TEXTO")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    src, out = a.entrada.resolve(), a.salida.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        ref = Path(tmp) / "reference.docx"
        build_reference(ref)
        pypandoc.convert_file(str(src), "docx", format="markdown+pipe_tables+grid_tables+tex_math_dollars",
                              outputfile=str(out),
                              extra_args=[f"--resource-path={src.parent}", "--wrap=none", f"--reference-doc={ref}"])
    marks = postprocess(out, a.encabezado, a.toc_antes)
    print(f"DOCX: {out} | párrafos {MARK}: {marks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
