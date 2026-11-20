"""Adaptador de salida SQLite (stdlib) del puerto DecisionRepository."""
from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

from src.decisions.domain.decision import (
    Decision, DecisionType, DuplicateDecisionError, Role,
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS recommendation_decisions (
    decision_id TEXT PRIMARY KEY,
    recommendation_id TEXT NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('APPROVED','REJECTED')),
    comment TEXT,
    decided_by TEXT NOT NULL,
    decided_by_role TEXT NOT NULL CHECK (decided_by_role IN ('ADMIN','OPERATOR','VIEWER')),
    decided_at TEXT NOT NULL,
    recommendation_sha256 TEXT NOT NULL,
    execution_allowed INTEGER NOT NULL DEFAULT 0 CHECK (execution_allowed = 0)
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_decisions_recommendation_user
    ON recommendation_decisions (recommendation_id, decided_by);
"""


class SqliteDecisionRepository:
    def __init__(self, path: str | Path):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as conn:
            conn.executescript(_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path, timeout=10)

    def add(self, d: Decision) -> None:
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute(
                    "INSERT INTO recommendation_decisions (decision_id, recommendation_id,"
                    " decision, comment, decided_by, decided_by_role, decided_at,"
                    " recommendation_sha256, execution_allowed) VALUES (?,?,?,?,?,?,?,?,0)",
                    (d.decision_id, d.recommendation_id, d.decision.value, d.comment,
                     d.decided_by, d.decided_by_role.value, d.decided_at.isoformat(),
                     d.recommendation_sha256))
        except sqlite3.IntegrityError as exc:
            raise DuplicateDecisionError() from exc

    def list_by_recommendation(self, recommendation_id: str) -> list[Decision]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                "SELECT decision_id, recommendation_id, decision, comment, decided_by,"
                " decided_by_role, decided_at, recommendation_sha256"
                " FROM recommendation_decisions WHERE recommendation_id = ?"
                " ORDER BY decided_at, rowid", (recommendation_id,)).fetchall()
        return [Decision(r[0], r[1], DecisionType(r[2]), r[3], r[4], Role(r[5]),
                         datetime.fromisoformat(r[6]), r[7]) for r in rows]
