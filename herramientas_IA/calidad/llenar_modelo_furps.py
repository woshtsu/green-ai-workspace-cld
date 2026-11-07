"""Llena una copia del modelo FURPS+ del docente (guias/semana13/MODELO-FURPSPLUS.xlsx) con la matriz de
docs/calidad/01_auditoria_furps.md y el estado OWASP, en tres hojas: Inicial, Actual (tras la ola 1) y Esperado.

Uso:
  .tools/docx/Scripts/python herramientas_IA/calidad/llenar_modelo_furps.py <salida.xlsx>

El modelo original no se modifica. Puntajes: Cumple = 5, Parcial = 3, No cumple = 1; PD = 5.
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "guias/semana13/MODELO-FURPSPLUS.xlsx"
AUDIT = ROOT / "docs/calidad/01_auditoria_furps.md"

# Mejoras implementadas en la ola 1 de la semana 13 (verificadas): id -> evidencia
OLA1_FURPS = {"M-U07": "Implementado: docs/GUIA-RAPIDA-USUARIO.md (semana 13)"}
# Filas que el plan no lleva a «Cumple» (restricciones aceptadas en 01_auditoria_furps.md §5)
NO_MEJORAN = {"M-F08", "M-PL03"}

# OWASP: (id, categoría, puntaje inicial, puntaje tras ola 1, esperado, evidencia/acción, responsable, fecha)
OWASP = [
    ("A01", "Broken Access Control", 1, 1, 5, "OW-01 RLS «Permitir todo» en Supabase (no verificado); OW-02 puertos locales. Revisar pg_policies", "Dueño de Supabase / Ricardo Porras", "28/11/2026"),
    ("A02", "Cryptographic Failures", 1, 1, 5, "OW-03 columna password en esquema; OW-04 contraseñas sintéticas en Excel", "Dueño de Supabase / Gina Barrera", "28/11/2026"),
    ("A03", "Injection", 5, 5, 5, "Consultas parametrizadas (PostgREST/SQLite) y validación Pydantic", "—", "—"),
    ("A04", "Insecure Design", 3, 3, 5, "OW-05 sin rate limiting en el Gateway", "Ricardo Porras", "28/11/2026"),
    ("A05", "Security Misconfiguration", 3, 5, 5, "OW-06/OW-07 corregidos: cabeceras en nginx.conf (commit d24d86f)", "Ricardo Porras", "07/11/2026"),
    ("A06", "Vulnerable and Outdated Components", 3, 5, 5, "OW-08 corregido: SRI SHA-384 en scripts y estilos de CDN (commit d24d86f)", "Ricardo Porras", "07/11/2026"),
    ("A07", "Identification and Authentication Failures", 3, 3, 3, "OW-09 sesión en localStorage (ola 3, riesgo aceptado temporalmente)", "Leonid Huamán", "12/12/2026"),
    ("A08", "Software and Data Integrity Failures", 3, 5, 5, "OW-10 corregido: Actions fijadas por SHA; OW-11 digest de imágenes pendiente (bajo)", "Ricardo Porras", "07/11/2026"),
    ("A09", "Security Logging and Monitoring Failures", 3, 3, 5, "OW-12 sin registro/métrica de 401/403 en Gateway", "Ricardo Porras", "28/11/2026"),
    ("A10", "Server-Side Request Forgery (SSRF)", 5, 5, 5, "URLs de destino fijas por configuración", "—", "—"),
]

GREEN, YELLOW, RED = (PatternFill("solid", fgColor=c) for c in ("C6EFCE", "FFEB9C", "FFC7CE"))


def parse_audit() -> list[dict]:
    rows = []
    for line in AUDIT.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\*\*(F|U|R|P|S|PLUS)\*\*\s*\|\s*(M-[A-Z]+\d+)\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        score = int(re.sub(r"\D", "", cells[-2]) or 0)
        rows.append({"factor": m.group(1), "id": m.group(2), "q": cells[2], "art": cells[3],
                     "evid": re.sub(r"\*\*", "", cells[5]), "resp": cells[6], "fecha": cells[7], "po": score})
    if not rows:
        sys.exit("No se encontró la matriz en 01_auditoria_furps.md")
    return rows


def fill(ws, title: str, furps: list[dict], owasp_col: int) -> tuple[int, int]:
    ws["A1"] = f"MODELO DE EVALUACIÓN FURPS+ APLICADO AL PROYECTO GREEN AI — {title}"
    style_src = {c: copy.copy(ws.cell(3, c)._style) for c in range(1, 15)}
    for r in range(3, max(ws.max_row, 80) + 1):
        for c in range(1, 15):
            ws.cell(r, c).value = None
    for rng in list(ws.merged_cells.ranges):
        if rng.min_row >= 3:
            ws.unmerge_cells(str(rng))
    r = 3
    totals = {}
    items = [(x["factor"], x["id"], x["q"], x["art"], x["po"], x["evid"], x["resp"], x["fecha"]) for x in furps]
    items += [("OWASP", o[0], f"¿Se tiene controlado el riesgo {o[0]} {o[1]}?", "SOFTWARE", o[owasp_col], o[5], o[6], o[7]) for o in OWASP]
    first_of = {}
    for factor, iid, q, art, po, evid, resp, fecha in items:
        for c in range(1, 15):
            ws.cell(r, c)._style = copy.copy(style_src[c])
        first_of.setdefault(factor, r)
        ws.cell(r, 1, factor if first_of[factor] == r else None)
        ws.cell(r, 2, iid)
        ws.cell(r, 3, q)
        ws.cell(r, 4, art)
        col = {5: 5, 3: 6, 1: 7}[po]
        ws.cell(r, col, "X")
        ws.cell(r, 8, evid)
        ws.cell(r, 9, resp if po < 5 else None)
        ws.cell(r, 10, fecha if po < 5 else None)
        ws.cell(r, 11, po)
        ws.cell(r, 12, 5)
        ws.cell(r, 13, f"=(K{r}/L{r})*100")
        fill_color = GREEN if po == 5 else YELLOW if po == 3 else RED
        for c in (5, 6, 7, 11):
            ws.cell(r, c).fill = fill_color
        for c in range(1, 15):
            ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
        t = totals.setdefault(factor, [0, 0, r, r])
        t[0] += po
        t[1] += 5
        t[3] = r
        r += 1
    for factor, (po, pd, r0, r1) in totals.items():
        ws.cell(r0, 14, f"=SUM(K{r0}:K{r1})/SUM(L{r0}:L{r1})*100")
        ws.cell(r0, 14).number_format = "0.0"
    po_all = sum(t[0] for t in totals.values())
    pd_all = sum(t[1] for t in totals.values())
    r += 1
    ws.cell(r, 3, "TOTAL (PO / PD) y nivel de calidad global").font = Font(bold=True)
    ws.cell(r, 11, f"=SUM(K3:K{r - 2})").font = Font(bold=True)
    ws.cell(r, 12, f"=SUM(L3:L{r - 2})").font = Font(bold=True)
    ws.cell(r, 13, f"=K{r}/L{r}*100").font = Font(bold=True)
    ws.cell(r, 13).number_format = "0.0"
    for c, w in zip("ABCDEFGHIJKLMN", (9, 8, 48, 14, 8, 8, 8, 52, 20, 11, 8, 8, 10, 11)):
        ws.column_dimensions[c].width = w
    return po_all, pd_all


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "exportados/semana13/MODELO-FURPSPLUS-Green-AI.xlsx"
    furps = parse_audit()
    wb = openpyxl.load_workbook(MODEL)
    base = wb["Hoja1"]
    actual = [dict(x, po=5, evid=OLA1_FURPS[x["id"]]) if x["id"] in OLA1_FURPS else x for x in furps]
    esperado = [x if x["id"] in NO_MEJORAN else dict(x, po=5) for x in furps]
    sheets = [("1-Inicial", "NIVEL INICIAL AL 07/11/2026", furps, 2),
              ("2-Actual", "TRAS LA OLA 1 (SEMANA 13)", actual, 3),
              ("3-Esperado", "NIVEL ESPERADO TRAS EL PLAN (28/11/2026)", esperado, 4)]
    for name, title, rows, col in sheets:
        ws = wb.copy_worksheet(base)
        ws.title = name
        po, pd = fill(ws, title, rows, col)
        print(f"{name}: PO {po} / PD {pd} = {po / pd * 100:.1f} %")
    wb.remove(base)
    if "Hoja2" in wb.sheetnames:
        wb.remove(wb["Hoja2"])
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"XLSX: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
