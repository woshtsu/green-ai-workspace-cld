from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class ReportRenderer(ABC):
    """Puerto de salida: convierte el resumen histórico (mismo dict que el JSON) en un documento binario."""

    media_type: str = "application/octet-stream"

    @abstractmethod
    def render(self, summary: dict[str, Any], generated_at: datetime) -> bytes:
        raise NotImplementedError
