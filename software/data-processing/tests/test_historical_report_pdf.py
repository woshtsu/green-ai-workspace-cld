from __future__ import annotations

import csv
from datetime import datetime, timezone
import io
import re
import sqlite3

import pytest
from fastapi.testclient import TestClient

from application.use_cases.historical_report import HistoricalReportUseCase
from domain.errors import InvalidQuery
from infrastructure.adapters.input.api import routes
from infrastructure.adapters.output.fpdf_report_renderer import FpdfReportRenderer, LEGEND
from main import app
from tests.test_historical_report import END, START, MockSource, clean_env, row, seeded_db  # noqa: F401

PARAMS_BASE = {"start": "2026-09-21T15:00:00Z", "end": "2026-09-21T16:00:00Z"}


def pdf_text(content: bytes) -> str:
    """Contenido sin comprimir: extrae las cadenas de los operadores Tj."""
    raw = content.decode("latin-1")
    return "\n".join(m.replace("\\(", "(").replace("\\)", ")") for m in re.findall(r"\((.*)\) Tj", raw))


def test_use_case_does_not_import_pdf_library():
    import application.use_cases.historical_report as module
    assert "fpdf" not in open(module.__file__, encoding="utf-8").read()


def test_renderer_produces_valid_pdf_with_accents_and_dash():
    summary = {
        "hardwareId": "HW—ñá", "period": {"start": "a", "end": "b"}, "recordCount": 0,
        "cpu_utilization_pct": None, "ram_utilization_pct": None, "highLoadPct": None,
        "energyWh": None, "gapsIgnored": 0, "source": "sqlite", "warnings": ["Energía — modelada"],
    }
    data = FpdfReportRenderer(compress=False).render(summary, datetime.now(timezone.utc))
    assert data.startswith(b"%PDF")
    assert data.rstrip().endswith(b"%%EOF")


def test_use_case_pdf_with_data_matches_json_totals():
    records = [
        row("1", "2026-09-21T15:00:00Z", cpu=40, ram=30, watts=100),
        row("2", "2026-09-21T15:10:00Z", cpu=90, ram=50, watts=200),
    ]
    for r in records:
        r["quality"] = {"cpu_utilization_pct": "valid", "ram_utilization_pct": "valid", "energia_watts": "valid"}

    def build():
        return HistoricalReportUseCase(MockSource([list(records)]), pdf_renderer=FpdfReportRenderer(compress=False))

    summary = build().execute("HW-01", START, END)
    pdf = build().execute("HW-01", START, END, format="pdf")
    assert isinstance(pdf, bytes) and pdf.startswith(b"%PDF")
    text = pdf_text(pdf)
    for value in (summary["cpu_utilization_pct"]["mean"], summary["cpu_utilization_pct"]["p95"],
                  summary["cpu_utilization_pct"]["max"], summary["ram_utilization_pct"]["mean"],
                  summary["highLoadPct"], summary["energyWh"]):
        assert f"{value:.2f}" in text
    assert f"{summary['recordCount']}" in text
    assert LEGEND in text


def test_use_case_pdf_empty_dataset_says_so():
    uc = HistoricalReportUseCase(MockSource([[]]), pdf_renderer=FpdfReportRenderer(compress=False))
    pdf = uc.execute("HW-EMPTY", START, END, format="pdf")
    assert pdf.startswith(b"%PDF")
    assert "Sin datos" in pdf_text(pdf)


def test_use_case_pdf_without_renderer_and_invalid_format():
    uc = HistoricalReportUseCase(MockSource([[]]))
    with pytest.raises(InvalidQuery):
        uc.execute("HW-01", START, END, format="pdf")
    with pytest.raises(InvalidQuery, match="json, csv o pdf"):
        uc.execute("HW-01", START, END, format="xml")


def _first_hw(db):
    with sqlite3.connect(db) as conn:
        return conn.execute(
            "SELECT hardware_id, min(timestamp), max(timestamp) FROM logs GROUP BY hardware_id "
            "ORDER BY count(*) DESC LIMIT 1"
        ).fetchone()


def test_http_pdf_headers_filename_and_totals_match_json(clean_env, seeded_db, monkeypatch):  # noqa: F811
    clean_env.setenv("HISTORICAL_SOURCE", "sqlite")
    clean_env.setenv("SQLITE_PATH", str(seeded_db))
    clean_env.setenv("APP_ENV", "development")
    monkeypatch.setattr(routes, "FpdfReportRenderer", lambda: FpdfReportRenderer(compress=False))
    hw, first, last = _first_hw(seeded_db)
    params = {"hardwareId": hw, "start": first, "end": last}

    with TestClient(app) as client:
        body = client.get("/api/v1/reports/historical-summary", params={**params, "format": "json"}).json()
        csv_r = client.get("/api/v1/reports/historical-summary", params={**params, "format": "csv"})
        r = client.get("/api/v1/reports/historical-summary", params={**params, "format": "pdf"})

    assert r.status_code == 200, r.text
    assert r.headers["content-type"] == "application/pdf"
    assert r.content.startswith(b"%PDF")
    disposition = r.headers["content-disposition"]
    assert re.fullmatch(rf'attachment; filename="reporte_historico_{re.escape(hw)}_\d{{8}}T\d{{6}}Z_\d{{8}}T\d{{6}}Z\.pdf"', disposition)

    text = pdf_text(r.content)
    assert f"{body['cpu_utilization_pct']['mean']:.2f}" in text
    assert f"{body['cpu_utilization_pct']['max']:.2f}" in text
    assert f"{body['energyWh']:.2f}" in text
    assert str(body["recordCount"]) in text
    assert LEGEND in text

    # JSON y CSV siguen igual
    assert body["recordCount"] >= 1 and body["source"] == "sqlite"
    assert csv_r.headers["content-type"].startswith("text/csv")
    assert "content-disposition" not in csv_r.headers
    assert len(list(csv.reader(io.StringIO(csv_r.text)))) == 2


def test_http_pdf_empty_dataset_and_invalid_format(clean_env, seeded_db, monkeypatch):  # noqa: F811
    clean_env.setenv("HISTORICAL_SOURCE", "sqlite")
    clean_env.setenv("SQLITE_PATH", str(seeded_db))
    clean_env.setenv("APP_ENV", "development")
    monkeypatch.setattr(routes, "FpdfReportRenderer", lambda: FpdfReportRenderer(compress=False))
    with TestClient(app) as client:
        r = client.get("/api/v1/reports/historical-summary",
                       params={"hardwareId": "NO-EXISTE", **PARAMS_BASE, "format": "pdf"})
        assert r.status_code == 200 and r.content.startswith(b"%PDF")
        assert "Sin datos" in pdf_text(r.content)
        bad = client.get("/api/v1/reports/historical-summary",
                         params={"hardwareId": "HW-01", **PARAMS_BASE, "format": "xml"})
        assert bad.status_code == 422
        long_range = client.get("/api/v1/reports/historical-summary",
                                params={"hardwareId": "HW-01", "start": "2026-08-01T00:00:00Z",
                                        "end": "2026-09-15T00:00:00Z", "format": "pdf"})
        assert long_range.status_code == 422
