"""Adaptador de entrada HTTP (FastAPI) de decisiones humanas (HU-07)."""
from __future__ import annotations

import hmac
import os
from datetime import timezone
from pathlib import Path
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Path as PathParam
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from src.decisions.adapters.sqlite_repository import SqliteDecisionRepository
from src.decisions.application.use_cases import ForbiddenError, ListDecisions, RecordDecision
from src.decisions.domain.decision import Decision, DecisionType, DuplicateDecisionError, Role
from src.service.recommendations import Recommendation

SERVICE_ROOT = Path(__file__).resolve().parents[2]
PROBLEM_MEDIA_TYPE = "application/problem+json"


class ProblemError(Exception):
    def __init__(self, status: int, title: str, detail: str):
        self.status, self.title, self.detail = status, title, detail


def problem_response(status: int, title: str, detail: str, errors: Any = None) -> JSONResponse:
    body: dict[str, Any] = {"type": "about:blank", "title": title, "status": status, "detail": detail}
    if errors is not None:
        body["errors"] = errors
    return JSONResponse(status_code=status, content=body, media_type=PROBLEM_MEDIA_TYPE)


def decisions_enabled() -> bool:
    return os.environ.get("DECISIONS_ENABLED", "true").strip().lower() not in ("false", "0", "no", "off")


def db_path() -> Path:
    configured = os.environ.get("DECISIONS_DB_PATH", "").strip()
    path = Path(configured) if configured else Path("data/decisions.db")
    return path if path.is_absolute() else SERVICE_ROOT / path


def get_repository() -> SqliteDecisionRepository:
    return SqliteDecisionRepository(db_path())


def require_enabled() -> None:
    if not decisions_enabled():
        raise ProblemError(404, "Not Found", "Funcionalidad de decisiones desactivada.")


class Identity(BaseModel):
    user_id: str
    role: Role


def require_gateway() -> None:
    """Falla cerrado: sin GATEWAY_SHARED_SECRET las rutas no operan."""
    require_enabled()
    expected = os.environ.get("GATEWAY_SHARED_SECRET", "")
    if not expected:
        raise ProblemError(503, "Service Unavailable",
                           "decisiones deshabilitadas: falta GATEWAY_SHARED_SECRET")


def identity(x_green_user_id: str | None = Header(default=None, alias="X-Green-User-Id"),
             x_green_user_role: str | None = Header(default=None, alias="X-Green-User-Role"),
             x_green_gateway_secret: str | None = Header(default=None, alias="X-Green-Gateway-Secret")) -> Identity:
    require_gateway()
    expected = os.environ["GATEWAY_SHARED_SECRET"]
    if not hmac.compare_digest((x_green_gateway_secret or "").encode(), expected.encode()):
        raise ProblemError(401, "Unauthorized", "Petición no originada en el Gateway.")
    user = (x_green_user_id or "").strip()
    if not user or not x_green_user_role:
        raise ProblemError(401, "Unauthorized", "Faltan las cabeceras de identidad del Gateway.")
    try:
        role = Role(x_green_user_role.strip().upper())
    except ValueError:
        raise ProblemError(401, "Unauthorized", "Rol de identidad no reconocido.") from None
    return Identity(user_id=user, role=role)


def recommendation_id_param(recommendationId: str = PathParam()) -> str:
    require_gateway()
    try:
        return str(UUID(recommendationId))
    except ValueError:
        raise ProblemError(422, "Unprocessable Entity", "recommendationId debe ser un UUID.") from None


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: DecisionType
    comment: str | None = Field(default=None, max_length=500)
    recommendation: dict[str, Any]


class DecisionResponse(BaseModel):
    decisionId: str
    recommendationId: str
    decision: DecisionType
    comment: str | None
    decidedBy: str
    decidedByRole: Role
    decidedAt: str
    recommendationSha256: str
    executionAllowed: bool = False


class DecisionList(BaseModel):
    recommendationId: str
    decisions: list[DecisionResponse]


def to_response(d: Decision) -> DecisionResponse:
    at = d.decided_at if d.decided_at.tzinfo else d.decided_at.replace(tzinfo=timezone.utc)
    return DecisionResponse(
        decisionId=d.decision_id, recommendationId=d.recommendation_id, decision=d.decision,
        comment=d.comment, decidedBy=d.decided_by, decidedByRole=d.decided_by_role,
        decidedAt=at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        recommendationSha256=d.recommendation_sha256, executionAllowed=False)


def _problem_doc(text: str) -> dict:
    return {"description": text, "content": {PROBLEM_MEDIA_TYPE: {}}}


router = APIRouter(tags=["Decisions"])
COMMON = {401: _problem_doc("Secreto del Gateway o cabeceras de identidad ausentes/inválidos"),
          503: _problem_doc("Falta GATEWAY_SHARED_SECRET (falla cerrado)"),
          404: _problem_doc("Decisiones desactivadas (DECISIONS_ENABLED=false)"),
          422: _problem_doc("Parámetros o cuerpo inválidos")}


@router.post("/v1/recommendations/{recommendationId}/decisions", status_code=201,
             response_model=DecisionResponse,
             responses={**COMMON, 403: _problem_doc("Rol VIEWER"),
                        409: _problem_doc("Decisión duplicada del usuario")})
def create_decision(body: DecisionRequest, recommendation_id: str = Depends(recommendation_id_param),
                    who: Identity = Depends(identity),
                    repository: SqliteDecisionRepository = Depends(get_repository)):
    if who.role is Role.VIEWER:
        raise ProblemError(403, "Forbidden", "El rol VIEWER no puede registrar decisiones.")
    rec = body.recommendation
    if rec.get("recommendationId") != recommendation_id:
        raise ProblemError(422, "Unprocessable Entity",
                           "recommendation.recommendationId no coincide con la ruta.")
    if rec.get("executionAllowed") is not False:
        raise ProblemError(422, "Unprocessable Entity", "recommendation.executionAllowed debe ser false.")
    try:
        Recommendation.model_validate(rec)
    except ValidationError:
        raise ProblemError(422, "Unprocessable Entity",
                           "recommendation no es un objeto Recommendation completo y válido.") from None
    try:
        record = RecordDecision(repository)(
            recommendation_id=recommendation_id, decision=body.decision, comment=body.comment,
            recommendation=rec, user_id=who.user_id, role=who.role)
    except ForbiddenError as exc:
        raise ProblemError(403, "Forbidden", str(exc)) from None
    except DuplicateDecisionError:
        raise ProblemError(409, "Conflict",
                           "Este usuario ya registró una decisión para esta recomendación.") from None
    return to_response(record)


@router.get("/v1/recommendations/{recommendationId}/decisions", response_model=DecisionList,
            responses=COMMON)
def list_decisions(recommendation_id: str = Depends(recommendation_id_param),
                   who: Identity = Depends(identity),
                   repository: SqliteDecisionRepository = Depends(get_repository)):
    items = ListDecisions(repository)(recommendation_id)
    return DecisionList(recommendationId=recommendation_id, decisions=[to_response(d) for d in items])
