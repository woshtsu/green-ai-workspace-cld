from abc import ABC, abstractmethod
from datetime import datetime


class HistoricalLogsSource(ABC):
    # Procedencia declarada por cada adaptador ("supabase" | "sqlite"); se publica en cada registro.
    source: str = ""

    @abstractmethod
    def read_page(self, hardware_id: str, start: datetime, end: datetime,
                  limit: int, after: tuple[datetime, str] | None = None) -> list[dict]:
        """Read at most limit rows ordered by (timestamp, log_id), without writes.

        Contract shared by all adapters (see tests/test_historical_logs_contract.py):
        rows of hardware_id with start <= timestamp <= end, strictly after the (timestamp, log_id)
        keyset cursor when given, ordered ascending by (timestamp, log_id), only COLUMNS.
        """
        raise NotImplementedError
