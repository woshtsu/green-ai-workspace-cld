from __future__ import annotations

import csv
from datetime import datetime
import io
import math
from typing import Any

from application.use_cases.read_historical_logs import ReadHistoricalLogsUseCase
from domain.errors import InvalidQuery
from domain.ports.historical_logs_source import HistoricalLogsSource
from domain.validation import interval, timestamp, utc

CSV_COLUMNS = [
    "cpu_mean",
    "cpu_p95",
    "cpu_max",
    "ram_mean",
    "ram_p95",
    "high_load_pct",
    "energy_wh",
    "record_count",
    "gaps_ignored",
    "source",
    "hardware_id",
    "start",
    "end",
]

ENERGY_WARNING = "Energía calculada desde energia_watts de la fuente; no es medición directa del proyecto."


def percentile_95(values: list[float]) -> float | None:
    if not values:
        return None
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 1:
        return float(sorted_vals[0])
    idx = 0.95 * (n - 1)
    low = int(math.floor(idx))
    high = int(math.ceil(idx))
    if low == high:
        return float(sorted_vals[low])
    weight = idx - low
    return float(sorted_vals[low] + weight * (sorted_vals[high] - sorted_vals[low]))


class HistoricalReportUseCase:
    DEFAULT_PAGE_SIZE = 500
    MAX_PAGES = 200

    def __init__(
        self,
        source: HistoricalLogsSource | ReadHistoricalLogsUseCase,
        max_pages: int = MAX_PAGES,
        page_size: int = DEFAULT_PAGE_SIZE,
    ):
        if isinstance(source, ReadHistoricalLogsUseCase):
            self.read_use_case = source
        else:
            self.read_use_case = ReadHistoricalLogsUseCase(source, max_page_size=page_size)
        self.max_pages = max_pages
        self.page_size = min(page_size, 500)

    @staticmethod
    def to_csv(summary: dict[str, Any]) -> str:
        cpu = summary.get("cpu_utilization_pct") or {}
        ram = summary.get("ram_utilization_pct") or {}
        period = summary.get("period") or {}

        flat = {
            "cpu_mean": cpu.get("mean") if cpu and cpu.get("mean") is not None else "",
            "cpu_p95": cpu.get("p95") if cpu and cpu.get("p95") is not None else "",
            "cpu_max": cpu.get("max") if cpu and cpu.get("max") is not None else "",
            "ram_mean": ram.get("mean") if ram and ram.get("mean") is not None else "",
            "ram_p95": ram.get("p95") if ram and ram.get("p95") is not None else "",
            "high_load_pct": summary.get("highLoadPct") if summary.get("highLoadPct") is not None else "",
            "energy_wh": summary.get("energyWh") if summary.get("energyWh") is not None else "",
            "record_count": summary.get("recordCount", 0),
            "gaps_ignored": summary.get("gapsIgnored", 0),
            "source": summary.get("source", ""),
            "hardware_id": summary.get("hardwareId", ""),
            "start": period.get("start", ""),
            "end": period.get("end", ""),
        }

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS, lineterminator="\r\n")
        writer.writeheader()
        writer.writerow(flat)
        return output.getvalue()

    def execute(
        self,
        hardware_id: str,
        start: datetime | str,
        end: datetime | str,
        format: str = "json",
    ) -> dict[str, Any] | str:
        if format not in ("json", "csv"):
            raise InvalidQuery("format debe ser json o csv.")

        if not isinstance(hardware_id, str) or not 1 <= len(hardware_id) <= 20:
            raise InvalidQuery("hardwareId debe tener entre 1 y 20 caracteres.")

        start_dt, end_dt = interval(start, end)
        source_name = getattr(self.read_use_case.source, "source", "unknown")

        cursor = None
        all_records: list[dict[str, Any]] = []
        pages_read = 0

        while True:
            page = self.read_use_case.execute(
                hardware_id, start_dt, end_dt, limit=self.page_size, cursor=cursor
            )
            records = page.get("records", [])
            if not records:
                break

            pages_read += 1
            if pages_read > self.max_pages:
                raise InvalidQuery(
                    f"La consulta excede el máximo permitido de {self.max_pages} páginas de históricos."
                )

            all_records.extend(records)
            cursor = page.get("nextCursor")
            if not cursor:
                break

        period_dict = {"start": timestamp(start_dt), "end": timestamp(end_dt)}

        if not all_records:
            summary = {
                "hardwareId": hardware_id,
                "period": period_dict,
                "recordCount": 0,
                "cpu_utilization_pct": None,
                "ram_utilization_pct": None,
                "highLoadPct": None,
                "energyWh": None,
                "gapsIgnored": 0,
                "source": source_name,
                "origin": "unknown",
                "warnings": [ENERGY_WARNING],
            }
            return self.to_csv(summary) if format == "csv" else summary

        actual_source = all_records[0].get("source", source_name)

        # CPU metrics
        valid_cpu = [
            float(r["cpu_utilization_pct"])
            for r in all_records
            if r.get("quality", {}).get("cpu_utilization_pct") == "valid"
            and r.get("cpu_utilization_pct") is not None
        ]
        if valid_cpu:
            cpu_summary = {
                "mean": float(sum(valid_cpu) / len(valid_cpu)),
                "p95": percentile_95(valid_cpu),
                "max": float(max(valid_cpu)),
            }
            high_load_pct = float(
                (sum(1 for v in valid_cpu if v > 80) / len(valid_cpu)) * 100.0
            )
        else:
            cpu_summary = None
            high_load_pct = None

        # RAM metrics
        valid_ram = [
            float(r["ram_utilization_pct"])
            for r in all_records
            if r.get("quality", {}).get("ram_utilization_pct") == "valid"
            and r.get("ram_utilization_pct") is not None
        ]
        if valid_ram:
            ram_summary = {
                "mean": float(sum(valid_ram) / len(valid_ram)),
                "p95": percentile_95(valid_ram),
            }
        else:
            ram_summary = None

        # Energy integration
        valid_energy: list[tuple[datetime, float]] = []
        for r in all_records:
            if (
                r.get("quality", {}).get("energia_watts") == "valid"
                and r.get("energia_watts") is not None
            ):
                ts = r["timestamp"]
                dt = datetime.fromisoformat(ts) if isinstance(ts, str) else ts
                valid_energy.append((utc(dt), float(r["energia_watts"])))

        gaps_ignored = 0
        if not valid_energy:
            energy_wh = None
        else:
            energy_wh = 0.0
            if len(valid_energy) >= 2:
                for i in range(len(valid_energy) - 1):
                    t1, w1 = valid_energy[i]
                    t2, w2 = valid_energy[i + 1]
                    dt_seconds = (t2 - t1).total_seconds()
                    if dt_seconds > 15 * 60:
                        gaps_ignored += 1
                    elif dt_seconds >= 0:
                        energy_wh += 0.5 * (w1 + w2) * (dt_seconds / 3600.0)

        summary = {
            "hardwareId": hardware_id,
            "period": period_dict,
            "recordCount": len(all_records),
            "cpu_utilization_pct": cpu_summary,
            "ram_utilization_pct": ram_summary,
            "highLoadPct": high_load_pct,
            "energyWh": energy_wh,
            "gapsIgnored": gaps_ignored,
            "source": actual_source,
            "origin": "unknown",
            "warnings": [ENERGY_WARNING],
        }

        if format == "csv":
            return self.to_csv(summary)
        return summary
