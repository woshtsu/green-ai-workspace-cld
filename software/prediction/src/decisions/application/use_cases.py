"""Casos de uso de decisiones. Dependen solo del dominio (puerto DecisionRepository)."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4

from src.decisions.domain.decision import (
    Decision, DecisionRepository, DecisionType, Role,
)


class ForbiddenError(Exception):
    """El rol no puede registrar decisiones."""


def canonical_sha256(recommendation: dict[str, Any]) -> str:
    """SHA-256 del JSON canónico: claves ordenadas, sin espacios, UTF-8."""
    canonical = json.dumps(recommendation, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class RecordDecision:
    def __init__(self, repository: DecisionRepository,
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)):
        self._repository = repository
        self._clock = clock

    def __call__(self, *, recommendation_id: str, decision: DecisionType,
                 comment: str | None, recommendation: dict[str, Any],
                 user_id: str, role: Role) -> Decision:
        if role is Role.VIEWER:
            raise ForbiddenError("El rol VIEWER no puede registrar decisiones.")
        record = Decision(
            decision_id=str(uuid4()), recommendation_id=recommendation_id,
            decision=decision, comment=comment, decided_by=user_id,
            decided_by_role=role, decided_at=self._clock().replace(microsecond=0),
            recommendation_sha256=canonical_sha256(recommendation))
        self._repository.add(record)  # puede lanzar DuplicateDecisionError
        return record


class ListDecisions:
    def __init__(self, repository: DecisionRepository):
        self._repository = repository

    def __call__(self, recommendation_id: str) -> list[Decision]:
        return self._repository.list_by_recommendation(recommendation_id)
