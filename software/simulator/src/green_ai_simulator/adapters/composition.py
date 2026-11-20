"""Punto de composición: ensambla los adaptadores concretos del Simulator."""
from green_ai_simulator.application.ports import SimulatorDependencies
from green_ai_simulator.adapters.configuration.json_parser import parse_inventory_json
from green_ai_simulator.adapters.configuration.scenario_parser import parse_scenario_json
from green_ai_simulator.adapters.persistence.run_logger import RunLogger


class PrometheusMetricsExporter:
    """Registra el colector y sirve /metrics (import perezoso: solo modo realtime)."""

    def __init__(self, inventory, run_uuid: str, host: str, port: int):
        self._inventory = inventory
        self._run_uuid = run_uuid
        self._host = host
        self._port = port
        self._collector = None
        self._registry = None

    def start(self) -> None:
        from prometheus_client import start_http_server, REGISTRY
        from green_ai_simulator.adapters.prometheus.exporter import SimulatorCollector
        self._collector = SimulatorCollector(self._inventory, self._run_uuid)
        self._registry = REGISTRY
        REGISTRY.register(self._collector)
        print(f"Starting Prometheus exporter on {self._host}:{self._port}/metrics")
        start_http_server(self._port, addr=self._host)

    def update_state(self, state) -> None:
        if self._collector is not None:
            self._collector.update_state(state)

    def close(self) -> None:
        if self._collector is not None:
            self._registry.unregister(self._collector)
            self._collector = None


def build_dependencies() -> SimulatorDependencies:
    return SimulatorDependencies(
        read_inventory=parse_inventory_json,
        read_scenario=parse_scenario_json,
        create_run_recorder=RunLogger,
        create_metrics_exporter=PrometheusMetricsExporter,
    )
