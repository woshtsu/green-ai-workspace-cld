"""Decisión humana sobre una recomendación: registro de auditoría, nunca una orden.

El dominio no depende de FastAPI, sqlite3 ni de ningún adaptador.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol


class DecisionType(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Role(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class DuplicateDecisionError(Exception):
    """El mismo usuario ya decidió sobre esta recomendación."""


@dataclass(frozen=True)
class Decision:
    decision_id: str
    recommendation_id: str
    decision: DecisionType
    comment: str | None
    decided_by: str
    decided_by_role: Role
    decided_at: datetime
    recommendation_sha256: str
    # Invariante: registrar una decisión no autoriza ninguna ejecución.
    execution_allowed: bool = False

    def __post_init__(self):
        if self.execution_allowed:
            raise ValueError("executionAllowed debe ser false")


class DecisionRepository(Protocol):
    def add(self, decision: Decision) -> None:
        """Persiste la decisión; lanza DuplicateDecisionError si ya existe
        una del mismo usuario para la recomendación."""

    def list_by_recommendation(self, recommendation_id: str) -> list[Decision]:
        """Decisiones de la recomendación, de la más antigua a la más reciente."""
