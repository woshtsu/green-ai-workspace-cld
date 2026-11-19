from __future__ import annotations

from datetime import datetime
from typing import Any

from fpdf import FPDF

from domain.ports.report_renderer import ReportRenderer

LEGEND = "Datos simulados; energía modelada, no medida"
TITLE = "Green AI - Reporte histórico"


def _latin1(text: Any) -> str:
    """Las fuentes core de fpdf2 solo admiten latin-1 (á, é, ñ sí; —, comillas tipográficas no)."""
    text = str(text).replace("—", "-").replace("–", "-").replace("“", '"').replace("”", '"').replace("’", "'")
    return text.encode("latin-1", "replace").decode("latin-1")


def _num(value: Any, suffix: str = "") -> str:
    return "sin datos" if value is None else f"{float(value):.2f}{suffix}"


class FpdfReportRenderer(ReportRenderer):
    media_type = "application/pdf"

    def __init__(self, compress: bool = True):
        self.compress = compress

    def render(self, summary: dict[str, Any], generated_at: datetime) -> bytes:
        cpu = summary.get("cpu_utilization_pct") or {}
        ram = summary.get("ram_utilization_pct") or {}
        period = summary.get("period") or {}
        rows = [
            ("Hardware", summary.get("hardwareId", "")),
            ("Periodo inicio", period.get("start", "")),
            ("Periodo fin", period.get("end", "")),
            ("Fuente", summary.get("source", "")),
            ("Registros", summary.get("recordCount", 0)),
            ("CPU media", _num(cpu.get("mean"), " %")),
            ("CPU p95", _num(cpu.get("p95"), " %")),
            ("CPU máxima", _num(cpu.get("max"), " %")),
            ("RAM media", _num(ram.get("mean"), " %")),
            ("RAM p95", _num(ram.get("p95"), " %")),
            ("Carga alta (CPU > 80 %)", _num(summary.get("highLoadPct"), " %")),
            ("Energía modelada", _num(summary.get("energyWh"), " Wh")),
            ("Huecos ignorados", summary.get("gapsIgnored", 0)),
        ]
        pdf = FPDF(format="A4")
        pdf.set_compression(self.compress)
        pdf.set_title(_latin1(TITLE))
        pdf.set_creator("Green AI Data Processing")
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, _latin1(TITLE), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, _latin1(f"Generado: {generated_at.strftime('%Y-%m-%dT%H:%M:%SZ')}"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        if not summary.get("recordCount"):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, _latin1("Sin datos para el filtro indicado: no hay registros históricos en el periodo."),
                           new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        for label, value in rows:
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(70, 7, _latin1(label), border="B")
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(0, 7, _latin1(value), border="B", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, _latin1(LEGEND + "."), new_x="LMARGIN", new_y="NEXT")
        for warning in summary.get("warnings") or []:
            pdf.multi_cell(0, 5, _latin1(warning), new_x="LMARGIN", new_y="NEXT")
        return bytes(pdf.output())
