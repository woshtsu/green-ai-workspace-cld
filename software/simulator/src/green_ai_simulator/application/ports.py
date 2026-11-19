"""Puertos de la capa de aplicación del Simulator (solo typing.Protocol)."""
from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol

from green_ai_simulator.domain.inventory import Inventory
from green_ai_simulator.domain.scenario import Scenario
from green_ai_simulator.domain.state import EngineState


class InventoryReader(Protocol):
    def __call__(self, path: str) -> Inventory: ...


class ScenarioReader(Protocol):
    def __call__(self, path: str) -> Scenario: ...


class RunRecorder(Protocol):
    uuid: str
    run_dir: Any

    def update_status(self, new_status: str, reason: Optional[str] = None) -> None: ...
    def write_sample(self, state: EngineState) -> bool: ...
    def close(self) -> None: ...


class RunRecorderFactory(Protocol):
    def __call__(
        self, output_dir_base: str, mode: str, seed: int, duration_sec: int,
        tick_sec: int, inv_path: str, scn_path: str,
    ) -> RunRecorder: ...


class MetricsExporter(Protocol):
    def start(self) -> None: ...
    def update_state(self, state: EngineState) -> None: ...
    def close(self) -> None: ...


class MetricsExporterFactory(Protocol):
    def __call__(
        self, inventory: Inventory, run_uuid: str, host: str, port: int,
    ) -> MetricsExporter: ...


@dataclass(frozen=True)
class SimulatorDependencies:
    read_inventory: Callable[[str], Inventory]
    read_scenario: Callable[[str], Scenario]
    create_run_recorder: RunRecorderFactory
    create_metrics_exporter: MetricsExporterFactory
