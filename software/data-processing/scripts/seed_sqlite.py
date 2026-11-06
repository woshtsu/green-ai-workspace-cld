"""Crea la base SQLite de desarrollo y la llena con Hardware y Logs de BD_GreenAi.xlsx (datos sintéticos).

Uso (desde software/data-processing):
  python scripts/seed_sqlite.py --db .local/greenai-dev.sqlite [--max-logs 5000] [--replace]

- Nunca carga la hoja Usuarios (contiene contraseñas en texto plano): las identidades son de Supabase Auth.
- Las fechas del Excel no tienen zona horaria; se interpretan como UTC (supuesto documentado).
- La base generada es un artefacto local ignorado por Git (*.sqlite).
"""
from __future__ import annotations

import argparse
import math
import sqlite3
import sys
from datetime import timezone
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE_ROOT))

from infrastructure.adapters.input.greenai_excel_adapter import GreenAIExcelAdapter  # noqa: E402

SCHEMA = SERVICE_ROOT / "infrastructure/persistence/sqlite/schema.sql"
DEFAULT_EXCEL = SERVICE_ROOT / "datasets/raw/synthetic_greenai/BD_GreenAi.xlsx"
HW_COLS = ["hardware_id", "usuario_id", "hostname", "ip_address", "cpu_cores", "ram_gb", "max_watts",
           "ubicacion_rack", "estado", "fecha_registro"]
LOG_COLS = ["log_id", "hardware_id", "timestamp", "cpu_utilization_pct", "ram_utilization_pct",
            "temperatura_celsius", "energia_watts", "prediccion_watts", "accion_recomendada", "cumple_sla"]


def utc_text(value) -> str:
    ts = value.to_pydatetime()
    ts = ts.replace(tzinfo=timezone.utc) if ts.tzinfo is None else ts.astimezone(timezone.utc)
    return ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def clean(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return value.item() if hasattr(value, "item") else value


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))


def seed(db: Path, excel: Path, max_logs: int | None, replace: bool) -> tuple[int, int]:
    if db.exists():
        if not replace:
            raise SystemExit(f"{db} ya existe; use --replace para regenerarla.")
        db.unlink()
    db.parent.mkdir(parents=True, exist_ok=True)
    data = GreenAIExcelAdapter(excel).extract()
    hardware, logs = data["hardware"], data["logs"]
    if max_logs:
        logs = logs.head(max_logs)
    with sqlite3.connect(db) as conn:
        create_schema(conn)
        conn.executemany(
            f"INSERT INTO hardware ({', '.join(HW_COLS)}) VALUES ({', '.join('?' * len(HW_COLS))})",
            [[utc_text(r.fecha_registro) if c == "fecha_registro" and r.fecha_registro is not None
              else clean(getattr(r, c)) for c in HW_COLS] for r in hardware.itertuples(index=False)])
        conn.executemany(
            f"INSERT INTO logs ({', '.join(LOG_COLS)}) VALUES ({', '.join('?' * len(LOG_COLS))})",
            [[utc_text(r.timestamp) if c == "timestamp" else
              (int(bool(r.cumple_sla)) if c == "cumple_sla" and clean(r.cumple_sla) is not None else clean(getattr(r, c)))
              for c in LOG_COLS] for r in logs.itertuples(index=False)])
        return (conn.execute("SELECT count(*) FROM hardware").fetchone()[0],
                conn.execute("SELECT count(*) FROM logs").fetchone()[0])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--excel", type=Path, default=DEFAULT_EXCEL)
    ap.add_argument("--max-logs", type=int, default=None)
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    hw, lg = seed(a.db, a.excel, a.max_logs, a.replace)
    print(f"SQLite de desarrollo: {a.db} — hardware={hw}, logs={lg} (sintéticos; sin usuarios)")


if __name__ == "__main__":
    main()
