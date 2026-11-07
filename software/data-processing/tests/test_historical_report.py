from __future__ import annotations

import csv
from datetime import datetime, timezone, timedelta
import importlib.util
import io
from pathlib import Path
import sqlite3

import pytest
from fastapi.testclient import TestClient

from application.use_cases.historical_report import HistoricalReportUseCase, ENERGY_WARNING
from application.use_cases.read_historical_logs import ReadHistoricalLogsUseCase
from domain.errors import InvalidQuery, SourceNotConfigured
from infrastructure.settings import Settings
from main import app

SERVICE_ROOT = Path(__file__).resolve().parents[1]
EXCEL = SERVICE_ROOT / "datasets/raw/synthetic_greenai/BD_GreenAi.xlsx"

START = datetime.fromisoformat("2026-09-21T15:00:00Z")
END = datetime.fromisoformat("2026-09-21T16:00:00Z")


def load_seed():
    spec = importlib.util.spec_from_file_location("seed_sqlite", SERVICE_ROOT / "scripts/seed_sqlite.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def seeded_db(tmp_path_factory):
    db = tmp_path_factory.mktemp("sqlite") / "dev.sqlite"
    hw, logs = load_seed().seed(db, EXCEL, max_logs=300, replace=False)
    assert hw == 50 and logs == 300
    return db


@pytest.fixture
def clean_env(monkeypatch):
    for name in ("HISTORICAL_SOURCE", "SQLITE_PATH", "APP_ENV", "SUPABASE_URL", "SUPABASE_API_KEY", "SUPABASE_READ_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("SUPABASE_ENABLED", "false")
    return monkeypatch


class MockSource:
    source = "sqlite"

    def __init__(self, pages: list[list[dict]], source: str = "sqlite"):
        self.pages = list(pages)
        self.call_count = 0
        self.source = source

    def read_page(self, hardware_id, start, end, limit, after=None):
        if self.call_count < len(self.pages):
            rows = self.pages[self.call_count]
            self.call_count += 1
            return rows
        return []


def row(
    log_id: str,
    ts: str,
    hw: str = "HW-01",
    cpu: float | None = 50.0,
    ram: float | None = 40.0,
    temp: float | None = 30.0,
    watts: float | None = 100.0,
) -> dict:
    return {
        "log_id": log_id,
        "hardware_id": hw,
        "timestamp": ts,
        "cpu_utilization_pct": cpu,
        "ram_utilization_pct": ram,
        "temperatura_celsius": temp,
        "energia_watts": watts,
    }


# ==============================================================================
# 1. Cálculo con datos conocidos (energía trapezoidal, hueco ignorado, calidad)
# ==============================================================================

def test_calculation_with_known_data_and_gap_ignored():
    """
    Datos conocidos:
    - R1: 15:00:00Z, CPU=50.0, RAM=40.0, Watts=100.0 (válido)
    - R2: 15:10:00Z, CPU=90.0, RAM=60.0, Watts=200.0 (dt=10 min <= 15 min; trapecio 1)
    - R3: 15:30:00Z, CPU=85.0, RAM=50.0, Watts=150.0 (dt=20 min > 15 min; hueco ignorado!)
    - R4: 15:40:00Z, CPU=75.0, RAM=50.0, Watts=150.0 (dt=10 min <= 15 min; trapecio 2)
    - R5: 15:50:00Z, CPU=105.0 (out_of_range -> ignorado!), RAM=50.0, Watts=150.0 (dt=10 min <= 15 min; trapecio 3)
    """
    rows = [
        row("LOG-01", "2026-09-21T15:00:00Z", cpu=50.0, ram=40.0, watts=100.0),
        row("LOG-02", "2026-09-21T15:10:00Z", cpu=90.0, ram=60.0, watts=200.0),
        row("LOG-03", "2026-09-21T15:30:00Z", cpu=85.0, ram=50.0, watts=150.0),
        row("LOG-04", "2026-09-21T15:40:00Z", cpu=75.0, ram=50.0, watts=150.0),
        row("LOG-05", "2026-09-21T15:50:00Z", cpu=105.0, ram=50.0, watts=150.0),
    ]
    source = MockSource([rows, []])
    use_case = HistoricalReportUseCase(source)
    summary = use_case.execute("HW-01", START, END)

    assert summary["recordCount"] == 5

    # CPU: 4 válidos (50.0, 90.0, 85.0, 75.0). R5 con 105.0 es out_of_range (ignorado).
    # Media = (50 + 90 + 85 + 75) / 4 = 75.0
    # Max = 90.0
    # P95 de [50, 75, 85, 90]: n=4, idx = 0.95 * 3 = 2.85 -> 85 + 0.85*(90-85) = 89.25
    # HighLoad (> 80): 90.0 y 85.0 -> 2 de 4 = 50.0%
    assert summary["cpu_utilization_pct"]["mean"] == pytest.approx(75.0)
    assert summary["cpu_utilization_pct"]["max"] == pytest.approx(90.0)
    assert summary["cpu_utilization_pct"]["p95"] == pytest.approx(89.25)
    assert summary["highLoadPct"] == pytest.approx(50.0)

    # RAM: 5 válidos [40, 60, 50, 50, 50]
    # Media = 250 / 5 = 50.0
    # P95 de [40, 50, 50, 50, 60]: n=5, idx = 0.95 * 4 = 3.8 -> 50 + 0.8*(60-50) = 58.0
    assert summary["ram_utilization_pct"]["mean"] == pytest.approx(50.0)
    assert summary["ram_utilization_pct"]["p95"] == pytest.approx(58.0)

    # Energía trapezoidal:
    # Segmento 1 (15:00 a 15:10, 10 min = 1/6 h): (100 + 200)/2 * (1/6) = 150/6 = 25.0 Wh
    # Segmento 2 (15:10 a 15:30, 20 min): hueco ignorado (> 15 min). gaps_ignored = 1
    # Segmento 3 (15:30 a 15:40, 10 min = 1/6 h): (150 + 150)/2 * (1/6) = 150/6 = 25.0 Wh
    # Segmento 4 (15:40 a 15:50, 10 min = 1/6 h): (150 + 150)/2 * (1/6) = 150/6 = 25.0 Wh
    # Total = 25 + 25 + 25 = 75.0 Wh
    assert summary["energyWh"] == pytest.approx(75.0)
    assert summary["gapsIgnored"] == 1

    # Metadatos obligatorios
    assert summary["source"] == "sqlite"
    assert summary["origin"] == "unknown"
    assert summary["period"]["start"] == "2026-09-21T15:00:00Z"
    assert summary["period"]["end"] == "2026-09-21T16:00:00Z"
    assert ENERGY_WARNING in summary["warnings"]


# ==============================================================================
# 2. Paginación de varias páginas y límite de páginas
# ==============================================================================

def test_pagination_multiple_pages():
    page1 = [
        row("LOG-01", "2026-09-21T15:00:00Z", cpu=10.0, watts=100.0),
        row("LOG-02", "2026-09-21T15:05:00Z", cpu=20.0, watts=100.0),
    ]
    page2 = [
        row("LOG-03", "2026-09-21T15:10:00Z", cpu=30.0, watts=100.0),
        row("LOG-04", "2026-09-21T15:15:00Z", cpu=40.0, watts=100.0),
    ]
    page3 = [
        row("LOG-05", "2026-09-21T15:20:00Z", cpu=50.0, watts=100.0),
    ]
    source = MockSource([page1, page2, page3, []], source="supabase")
    use_case = HistoricalReportUseCase(source, page_size=2)
    summary = use_case.execute("HW-01", START, END)

    assert summary["recordCount"] == 5
    assert summary["cpu_utilization_pct"]["mean"] == pytest.approx(30.0)
    assert summary["cpu_utilization_pct"]["max"] == pytest.approx(50.0)
    assert summary["source"] == "supabase"
    assert source.call_count == 4


def test_pagination_max_pages_exceeded():
    page1 = [row("LOG-01", "2026-09-21T15:00:00Z")]
    page2 = [row("LOG-02", "2026-09-21T15:05:00Z")]
    page3 = [row("LOG-03", "2026-09-21T15:10:00Z")]
    source = MockSource([page1, page2, page3], source="sqlite")
    # Configurar máximo 2 páginas; la tercera página con datos debe disparar InvalidQuery
    use_case = HistoricalReportUseCase(source, max_pages=2, page_size=1)
    with pytest.raises(InvalidQuery, match="excede el máximo permitido de 2 páginas"):
        use_case.execute("HW-01", START, END)


# ==============================================================================
# 3. Formato CSV
# ==============================================================================

def test_csv_format_structure_and_values():
    rows = [
        row("LOG-01", "2026-09-21T15:00:00Z", cpu=50.0, ram=40.0, watts=100.0),
        row("LOG-02", "2026-09-21T15:10:00Z", cpu=90.0, ram=60.0, watts=200.0),
    ]
    source = MockSource([rows, []])
    use_case = HistoricalReportUseCase(source)
    csv_text = use_case.execute("HW-01", START, END, format="csv")

    assert isinstance(csv_text, str)
    reader = list(csv.reader(io.StringIO(csv_text)))
    assert len(reader) == 2  # Una fila de cabecera y una de datos

    headers = reader[0]
    data = reader[1]

    expected_headers = [
        "cpu_mean",
        "cpu_p95",
        "cpu_max",
        "ram_mean",
        "ram_p95",
        "high_load_pct",
        "energy_wh",
        "record_count",
        "gaps_ignored",
        "source",
        "hardware_id",
        "start",
        "end",
    ]
    assert headers == expected_headers

    row_dict = dict(zip(headers, data))
    assert float(row_dict["cpu_mean"]) == pytest.approx(70.0)
    assert float(row_dict["cpu_max"]) == pytest.approx(90.0)
    assert float(row_dict["high_load_pct"]) == pytest.approx(50.0)
    assert int(row_dict["record_count"]) == 2
    assert int(row_dict["gaps_ignored"]) == 0
    assert row_dict["source"] == "sqlite"
    assert row_dict["hardware_id"] == "HW-01"
    assert row_dict["start"] == "2026-09-21T15:00:00Z"
    assert row_dict["end"] == "2026-09-21T16:00:00Z"


# ==============================================================================
# 4. Sin datos
# ==============================================================================

def test_no_data_returns_200_with_null_metrics():
    source = MockSource([[]], source="supabase")
    use_case = HistoricalReportUseCase(source)
    summary = use_case.execute("HW-EMPTY", START, END)

    assert summary["recordCount"] == 0
    assert summary["cpu_utilization_pct"] is None
    assert summary["ram_utilization_pct"] is None
    assert summary["highLoadPct"] is None
    assert summary["energyWh"] is None
    assert summary["gapsIgnored"] == 0
    assert summary["source"] == "supabase"
    assert summary["origin"] == "unknown"
    assert summary["warnings"] == [ENERGY_WARNING]


def test_no_data_csv():
    source = MockSource([[]], source="sqlite")
    use_case = HistoricalReportUseCase(source)
    csv_text = use_case.execute("HW-EMPTY", START, END, format="csv")

    reader = list(csv.reader(io.StringIO(csv_text)))
    assert len(reader) == 2
    row_dict = dict(zip(reader[0], reader[1]))

    assert row_dict["record_count"] == "0"
    assert row_dict["gaps_ignored"] == "0"
    assert row_dict["cpu_mean"] == ""
    assert row_dict["cpu_p95"] == ""
    assert row_dict["cpu_max"] == ""
    assert row_dict["ram_mean"] == ""
    assert row_dict["ram_p95"] == ""
    assert row_dict["high_load_pct"] == ""
    assert row_dict["energy_wh"] == ""
    assert row_dict["source"] == "sqlite"
    assert row_dict["hardware_id"] == "HW-EMPTY"


# ==============================================================================
# 5. Rango y parámetros inválidos -> 422
# ==============================================================================

@pytest.mark.parametrize("params,match", [
    # start >= end
    ({"hardwareId": "HW-01", "start": "2026-09-21T16:00:00Z", "end": "2026-09-21T15:00:00Z"}, "anterior a end"),
    # rango > 31 días
    ({"hardwareId": "HW-01", "start": "2026-08-01T00:00:00Z", "end": "2026-09-15T00:00:00Z"}, "31 días"),
    # end en el futuro
    ({"hardwareId": "HW-01", "start": "2026-09-21T15:00:00Z", "end": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()}, "futuro"),
    # sin zona horaria
    ({"hardwareId": "HW-01", "start": "2026-09-21T15:00:00", "end": "2026-09-21T16:00:00Z"}, "zona horaria"),
    # hardwareId inválido
    ({"hardwareId": "", "start": "2026-09-21T15:00:00Z", "end": "2026-09-21T16:00:00Z"}, "INVALID_QUERY"),
    ({"hardwareId": "A" * 21, "start": "2026-09-21T15:00:00Z", "end": "2026-09-21T16:00:00Z"}, "INVALID_QUERY"),
    # format no admitido
    ({"hardwareId": "HW-01", "start": "2026-09-21T15:00:00Z", "end": "2026-09-21T16:00:00Z", "format": "xml"}, "INVALID_QUERY"),
])
def test_invalid_range_and_params_422(clean_env, seeded_db, params, match):
    clean_env.setenv("HISTORICAL_SOURCE", "sqlite")
    clean_env.setenv("SQLITE_PATH", str(seeded_db))
    clean_env.setenv("APP_ENV", "development")

    with TestClient(app) as client:
        r = client.get("/api/v1/reports/historical-summary", params=params)
    assert r.status_code == 422
    assert match in r.text or r.json()["code"] == "INVALID_QUERY"


# ==============================================================================
# 6. Ruta HTTP con perfil SQLite (patrón de tests/test_sqlite_profile.py)
# ==============================================================================

def test_sqlite_profile_http_route_json_and_csv(clean_env, seeded_db):
    clean_env.setenv("HISTORICAL_SOURCE", "sqlite")
    clean_env.setenv("SQLITE_PATH", str(seeded_db))
    clean_env.setenv("APP_ENV", "development")

    with sqlite3.connect(seeded_db) as conn:
        hw, first, last = conn.execute(
            "SELECT hardware_id, min(timestamp), max(timestamp) FROM logs GROUP BY hardware_id "
            "ORDER BY count(*) DESC LIMIT 1"
        ).fetchone()

    with TestClient(app) as client:
        # 1. JSON
        r = client.get("/api/v1/reports/historical-summary", params={
            "hardwareId": hw, "start": first, "end": last, "format": "json"
        })
        assert r.status_code == 200, r.text
        assert r.headers["content-type"].startswith("application/json")
        body = r.json()
        assert body["hardwareId"] == hw
        assert body["recordCount"] >= 1
        assert body["source"] == "sqlite"
        assert body["origin"] == "unknown"
        assert body["cpu_utilization_pct"] is not None
        assert "mean" in body["cpu_utilization_pct"]
        assert "p95" in body["cpu_utilization_pct"]
        assert "max" in body["cpu_utilization_pct"]
        assert body["ram_utilization_pct"] is not None
        assert "mean" in body["ram_utilization_pct"]
        assert "p95" in body["ram_utilization_pct"]
        assert body["energyWh"] is not None
        assert ENERGY_WARNING in body["warnings"]

        # 2. CSV
        r_csv = client.get("/api/v1/reports/historical-summary", params={
            "hardwareId": hw, "start": first, "end": last, "format": "csv"
        })
        assert r_csv.status_code == 200, r_csv.text
        assert r_csv.headers["content-type"].startswith("text/csv")
        csv_rows = list(csv.reader(io.StringIO(r_csv.text)))
        assert len(csv_rows) == 2
        row_map = dict(zip(csv_rows[0], csv_rows[1]))
        assert row_map["hardware_id"] == hw
        assert row_map["source"] == "sqlite"
        assert int(row_map["record_count"]) == body["recordCount"]


def test_route_without_source_is_503(clean_env):
    with TestClient(app) as client:
        r = client.get("/api/v1/reports/historical-summary", params={
            "hardwareId": "HW001", "start": "2026-07-10T00:00:00Z", "end": "2026-07-11T00:00:00Z"
        })
    assert r.status_code == 503
    assert r.json()["code"] == "SOURCE_NOT_CONFIGURED"
