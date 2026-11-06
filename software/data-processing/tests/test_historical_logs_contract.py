"""Pruebas de contrato del puerto HistoricalLogsSource, comunes a todos los adaptadores.

- sqlite: siempre (base temporal creada con infrastructure/persistence/sqlite/schema.sql).
- postgrest: PostgreSQL + PostgREST reales de PRUEBAS (software/infraestructura/compose.contract-postgres.yml),
  usando el adaptador de Supabase sin modificar su consulta. Se activa con CONTRACT_POSTGREST_URL y
  CONTRACT_JWT_SECRET; si faltan, se omite y queda NO verificado.
  Limitación: valida la semántica PostgREST/PostgreSQL del adaptador, no Supabase Auth, RLS ni la red de Supabase.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import hashlib
import hmac
import json
import os
import sqlite3
import time
from pathlib import Path

import httpx
import pytest

from application.use_cases.read_historical_logs import ReadHistoricalLogsUseCase
from infrastructure.adapters.input.sqlite_historical_logs_adapter import SqliteHistoricalLogsAdapter, canonical
from infrastructure.adapters.input.supabase_historical_logs_adapter import SupabaseHistoricalLogsAdapter

SCHEMA = Path(__file__).resolve().parents[1] / "infrastructure/persistence/sqlite/schema.sql"
COLUMNS = {"log_id", "hardware_id", "timestamp", "cpu_utilization_pct", "ram_utilization_pct",
           "temperatura_celsius", "energia_watts"}
START = datetime(2026, 9, 21, 15, 0, tzinfo=timezone.utc)
END = datetime(2026, 9, 21, 16, 0, tzinfo=timezone.utc)
T_MID = datetime(2026, 9, 21, 15, 30, 0, 123456, tzinfo=timezone.utc)


def log(log_id, ts, hw="CT-HW1", cpu=10.5):
    return {"log_id": log_id, "hardware_id": hw, "timestamp": ts, "cpu_utilization_pct": cpu,
            "ram_utilization_pct": 40.25, "temperatura_celsius": 35.5, "energia_watts": 120.75,
            "prediccion_watts": 999.99, "accion_recomendada": "no-exponer", "cumple_sla": True}


ROWS = [
    log("CT-BEFORE", datetime(2026, 9, 21, 14, 59, 59, 999999, tzinfo=timezone.utc)),
    log("CT-A-START", START),
    log("CT-M2", T_MID), log("CT-M1", T_MID), log("CT-M3", T_MID),   # mismo instante, desempate por log_id
    log("CT-OTHER", T_MID, hw="CT-HW2"),
    log("CT-Z-END", END),
    log("CT-AFTER", datetime(2026, 9, 21, 16, 0, 0, 1, tzinfo=timezone.utc)),
]
EXPECTED_ORDER = ["CT-A-START", "CT-M1", "CT-M2", "CT-M3", "CT-Z-END"]


# ---------- backends ----------

def sqlite_backend(tmp_path):
    db = tmp_path / "contract.sqlite"
    with sqlite3.connect(db) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        for hw in ("CT-HW1", "CT-HW2"):
            conn.execute("INSERT INTO hardware (hardware_id, usuario_id, hostname, ip_address, cpu_cores, ram_gb, max_watts)"
                         " VALUES (?, 'US-CT', 'ct-host', '10.0.0.1', 4, 8, 300)", (hw,))
        for r in ROWS:
            conn.execute("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (r["log_id"], r["hardware_id"], canonical(r["timestamp"]), r["cpu_utilization_pct"],
                          r["ram_utilization_pct"], r["temperatura_celsius"], r["energia_watts"],
                          r["prediccion_watts"], r["accion_recomendada"], int(r["cumple_sla"])))
    return SqliteHistoricalLogsAdapter(db), lambda: None


def jwt(secret: str, role: str) -> str:
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d, separators=(",", ":")).encode()).rstrip(b"=")
    head, body = enc({"alg": "HS256", "typ": "JWT"}), enc({"role": role, "exp": int(time.time()) + 600})
    sig = base64.urlsafe_b64encode(hmac.new(secret.encode(), head + b"." + body, hashlib.sha256).digest()).rstrip(b"=")
    return (head + b"." + body + b"." + sig).decode()


def postgrest_backend(_tmp_path):
    url, secret = os.environ.get("CONTRACT_POSTGREST_URL"), os.environ.get("CONTRACT_JWT_SECRET")
    if not url or not secret:
        pytest.skip("PostgREST de pruebas no configurado (CONTRACT_POSTGREST_URL, CONTRACT_JWT_SECRET): NO verificado")
    writer = {"Authorization": f"Bearer {jwt(secret, 'contract_writer')}", "Content-Type": "application/json"}
    with httpx.Client(base_url=url, headers=writer, timeout=10) as c:
        c.delete("/logs", params={"log_id": "like.CT-*"}).raise_for_status()
        c.delete("/hardware", params={"hardware_id": "like.CT-*"}).raise_for_status()
        c.post("/hardware", json=[{"hardware_id": hw, "usuario_id": "US-CT", "hostname": "ct-host",
                                   "ip_address": "10.0.0.1", "cpu_cores": 4, "ram_gb": 8, "max_watts": 300}
                                  for hw in ("CT-HW1", "CT-HW2")]).raise_for_status()
        c.post("/logs", json=[r | {"timestamp": r["timestamp"].isoformat()} for r in ROWS]).raise_for_status()
    adapter = SupabaseHistoricalLogsAdapter("https://contract.invalid", "contract-apikey", jwt(secret, "web_reader"))
    # Solo en pruebas: el adaptador exige HTTPS; el PostgREST local de pruebas escucha en HTTP loopback.
    adapter.base_url = url.rstrip("/").removesuffix("/rest/v1")

    def cleanup():
        with httpx.Client(base_url=url, headers=writer, timeout=10) as c:
            c.delete("/logs", params={"log_id": "like.CT-*"})
            c.delete("/hardware", params={"hardware_id": "like.CT-*"})
    return adapter, cleanup


@pytest.fixture(params=[sqlite_backend, postgrest_backend], ids=["sqlite", "postgrest"])
def source(request, tmp_path):
    adapter, cleanup = request.param(tmp_path)
    yield adapter
    cleanup()


def ids(rows):
    return [r["log_id"] for r in rows]


def instant(row):
    return datetime.fromisoformat(row["timestamp"]).astimezone(timezone.utc)


# ---------- contrato ----------

def test_inclusive_range_hardware_filter_and_total_order(source):
    rows = source.read_page("CT-HW1", START, END, 500)
    assert ids(rows) == EXPECTED_ORDER


def test_only_contract_columns_are_returned(source):
    rows = source.read_page("CT-HW1", START, END, 500)
    assert rows and all(set(r) == COLUMNS for r in rows)


def test_values_and_microseconds_are_preserved(source):
    row = next(r for r in source.read_page("CT-HW1", START, END, 500) if r["log_id"] == "CT-M1")
    assert instant(row) == T_MID
    assert row["cpu_utilization_pct"] == 10.5 and row["energia_watts"] == 120.75


def test_limit(source):
    assert ids(source.read_page("CT-HW1", START, END, 2)) == EXPECTED_ORDER[:2]


def test_keyset_cursor_breaks_ties_by_log_id(source):
    assert ids(source.read_page("CT-HW1", START, END, 500, (T_MID, "CT-M1"))) == ["CT-M2", "CT-M3", "CT-Z-END"]
    assert ids(source.read_page("CT-HW1", START, END, 500, (T_MID, "CT-M3"))) == ["CT-Z-END"]


def test_empty_window(source):
    assert source.read_page("CT-HW1", datetime(2026, 9, 20, tzinfo=timezone.utc),
                            datetime(2026, 9, 20, 1, tzinfo=timezone.utc), 10) == []


def test_use_case_paginates_identically_and_declares_source(source):
    use_case, seen, cursor = ReadHistoricalLogsUseCase(source), [], None
    for _ in range(10):
        page = use_case.execute("CT-HW1", START, END, 2, cursor)
        assert all(r["source"] == source.source for r in page["records"])
        assert all("prediccion_watts" not in r for r in page["records"])
        seen += [r["log_id"] for r in page["records"]]
        cursor = page["nextCursor"]
        if cursor is None:
            break
    assert seen == EXPECTED_ORDER


def test_reader_identity_cannot_write():
    """Solo PostgREST: el token de lectura (web_reader) no puede insertar en logs."""
    url, secret = os.environ.get("CONTRACT_POSTGREST_URL"), os.environ.get("CONTRACT_JWT_SECRET")
    if not url or not secret:
        pytest.skip("PostgREST de pruebas no configurado: NO verificado")
    reader = {"Authorization": f"Bearer {jwt(secret, 'web_reader')}", "Content-Type": "application/json"}
    r = httpx.post(f"{url.rstrip('/')}/logs", headers=reader, timeout=10,
                   json=[log("CT-FORBIDDEN", START) | {"timestamp": START.isoformat()}])
    assert r.status_code in (401, 403)
