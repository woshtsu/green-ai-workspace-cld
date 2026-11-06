"""Adaptador SQLite de históricos para el perfil de DESARROLLO (solo lectura).

Mismo contrato que SupabaseHistoricalLogsAdapter (ver HistoricalLogsSource). No replica Auth,
RLS ni procedimientos de Supabase; no debe usarse en producción (lo impide Settings).
"""
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from domain.errors import InvalidResponse, ServiceError
from domain.ports.historical_logs_source import HistoricalLogsSource

COLUMNS = ("log_id", "hardware_id", "timestamp", "cpu_utilization_pct",
           "ram_utilization_pct", "temperatura_celsius", "energia_watts")


def canonical(value: datetime) -> str:
    """Formato almacenado: UTC con 6 decimales y 'Z' (orden lexicográfico = cronológico)."""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class SqliteHistoricalLogsAdapter(HistoricalLogsSource):
    source = "sqlite"

    def __init__(self, path):
        self.path = Path(path)

    def _connect(self):
        if not self.path.is_file():
            raise ServiceError("La base SQLite de desarrollo no existe.")
        # mode=ro: el puerto es de solo lectura, igual que el token de Supabase.
        return sqlite3.connect(f"{self.path.resolve().as_uri()}?mode=ro", uri=True, timeout=5)

    def read_page(self, hardware_id: str, start: datetime, end: datetime,
                  limit: int, after: tuple[datetime, str] | None = None) -> list[dict]:
        if not 1 <= limit <= 500:
            raise ValueError("Límite de lectura inválido")
        sql = (f"SELECT {', '.join(COLUMNS)} FROM logs "
               "WHERE hardware_id = ? AND timestamp >= ? AND timestamp <= ?")
        params: list = [hardware_id, canonical(start), canonical(end)]
        if after:
            instant = canonical(after[0])
            sql += " AND (timestamp > ? OR (timestamp = ? AND log_id > ?))"
            params += [instant, instant, after[1]]
        sql += " ORDER BY timestamp ASC, log_id ASC LIMIT ?"
        params.append(limit)
        try:
            with self._connect() as conn:
                rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError as exc:
            if "no such table" in str(exc) or "no such column" in str(exc):
                raise InvalidResponse("El contrato de históricos no está disponible en la fuente.") from exc
            raise ServiceError("La base SQLite de desarrollo no está disponible.") from exc
        except sqlite3.DatabaseError as exc:
            raise ServiceError("La base SQLite de desarrollo no está disponible.") from exc
        return [dict(zip(COLUMNS, row)) for row in rows]
