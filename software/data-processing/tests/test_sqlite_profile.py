"""Perfil SQLite de desarrollo: selección por entorno, bloqueo en producción, semilla y ruta HTTP."""
import importlib.util
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from infrastructure.settings import Settings
from main import app

SERVICE_ROOT = Path(__file__).resolve().parents[1]
EXCEL = SERVICE_ROOT / "datasets/raw/synthetic_greenai/BD_GreenAi.xlsx"


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


def test_seed_never_loads_users_and_keeps_utc_canonical_timestamps(seeded_db):
    with sqlite3.connect(seeded_db) as conn:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        stamps = [r[0] for r in conn.execute("SELECT timestamp FROM logs LIMIT 5")]
    assert tables == {"hardware", "logs"}
    assert all(s.endswith("Z") and len(s) == 27 for s in stamps)


def test_schema_rejects_non_canonical_timestamp(seeded_db, tmp_path):
    db = tmp_path / "copy.sqlite"
    db.write_bytes(seeded_db.read_bytes())
    with sqlite3.connect(db) as conn, pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO logs VALUES ('X1','HW001','2026-07-10 07:35:04',1,1,1,1,1,NULL,1)")


def test_sqlite_is_rejected_in_production(clean_env, seeded_db):
    clean_env.setenv("HISTORICAL_SOURCE", "sqlite")
    clean_env.setenv("SQLITE_PATH", str(seeded_db))
    with pytest.raises(ValueError, match="APP_ENV"):
        Settings.from_env()          # APP_ENV ausente = production
    clean_env.setenv("APP_ENV", "production")
    with pytest.raises(ValueError, match="APP_ENV"):
        Settings.from_env()


@pytest.mark.parametrize("env", [
    {"HISTORICAL_SOURCE": "sqlite", "APP_ENV": "development"},                         # sin SQLITE_PATH
    {"HISTORICAL_SOURCE": "sqlite", "APP_ENV": "development", "SQLITE_PATH": "no-existe.sqlite"},
    {"HISTORICAL_SOURCE": "sqlite", "APP_ENV": "development", "SUPABASE_ENABLED": "true"},
    {"HISTORICAL_SOURCE": "postgres"}, {"APP_ENV": "staging"},
])
def test_invalid_profile_configuration(clean_env, env):
    for k, v in env.items():
        clean_env.setenv(k, v)
    with pytest.raises(ValueError):
        Settings.from_env()


def test_default_profile_is_unchanged(clean_env):
    s = Settings.from_env()
    assert s.historical_source == "none" and s.app_env == "production"


def test_historical_route_reads_sqlite_and_declares_source(clean_env, seeded_db):
    clean_env.setenv("HISTORICAL_SOURCE", "sqlite")
    clean_env.setenv("SQLITE_PATH", str(seeded_db))
    clean_env.setenv("APP_ENV", "development")
    with sqlite3.connect(seeded_db) as conn:
        hw, first, last = conn.execute(
            "SELECT hardware_id, min(timestamp), max(timestamp) FROM logs GROUP BY hardware_id "
            "ORDER BY count(*) DESC LIMIT 1").fetchone()
    with TestClient(app) as client:
        r = client.get("/api/v1/historical-logs", params={"hardwareId": hw, "start": first, "end": last, "limit": 500})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["recordCount"] >= 1
    assert {rec["source"] for rec in body["records"]} == {"sqlite"}
    assert "prediccion_watts" not in r.text and "password" not in r.text


def test_route_without_source_is_503(clean_env):
    with TestClient(app) as client:
        r = client.get("/api/v1/historical-logs", params={"hardwareId": "HW001",
                       "start": "2026-07-10T00:00:00Z", "end": "2026-07-11T00:00:00Z"})
    assert r.status_code == 503 and r.json()["code"] == "SOURCE_NOT_CONFIGURED"
