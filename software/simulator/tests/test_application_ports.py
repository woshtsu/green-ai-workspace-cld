import ast
import unittest
from pathlib import Path
from types import SimpleNamespace

from green_ai_simulator.adapters.configuration.json_parser import parse_inventory_json
from green_ai_simulator.adapters.configuration.scenario_parser import parse_scenario_json
from green_ai_simulator.application.ports import SimulatorDependencies
from green_ai_simulator.application.runner import run_simulation

APP_DIR = Path(__file__).resolve().parents[1] / "src" / "green_ai_simulator" / "application"


def _imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            yield node.module or ""


class ApplicationLayerIsolationTests(unittest.TestCase):
    def test_application_does_not_import_adapters(self):
        for path in APP_DIR.glob("*.py"):
            for module in _imports(path):
                self.assertFalse(
                    module.startswith("green_ai_simulator.adapters"),
                    f"{path.name} importa {module}",
                )


class FakeRecorder:
    def __init__(self, *args, **kwargs):
        self.uuid = "fake-uuid"
        self.run_dir = "fake-dir"
        self.samples = []
        self.statuses = []
        self.closed = False

    def update_status(self, new_status, reason=None):
        self.statuses.append(new_status)

    def write_sample(self, state):
        self.samples.append(state.logical_time)
        return True

    def close(self):
        self.closed = True


class FakeExporter:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.started = False
        self.states = []
        self.closed = False

    def start(self):
        self.started = True

    def update_state(self, state):
        self.states.append(state.logical_time)

    def close(self):
        self.closed = True


class RunSimulationWithInMemoryDoublesTests(unittest.TestCase):
    def _run(self, mode):
        made = {}

        def recorder_factory(*args, **kwargs):
            made["rec"] = FakeRecorder(*args, **kwargs)
            return made["rec"]

        def exporter_factory(*args):
            made["exp"] = FakeExporter(*args)
            return made["exp"]

        deps = SimulatorDependencies(
            read_inventory=lambda p: parse_inventory_json("configs/inventory.synthetic.json"),
            read_scenario=lambda p: parse_scenario_json("configs/scenarios/high.json"),
            create_run_recorder=recorder_factory,
            create_metrics_exporter=exporter_factory,
        )
        args = SimpleNamespace(
            inventory="i", scenario="s", seed=7, duration_seconds=3, tick_seconds=1,
            mode=mode, output_dir="o", host="127.0.0.1", port=9999,
        )
        return run_simulation(args, deps), made

    def test_offline_run_completes_without_exporter(self):
        code, made = self._run("offline")
        self.assertEqual(code, 0)
        self.assertNotIn("exp", made)
        self.assertEqual(made["rec"].samples, [0, 1, 2, 3])
        self.assertEqual(made["rec"].statuses, ["RUNNING", "COMPLETED"])
        self.assertTrue(made["rec"].closed)

    def test_realtime_run_uses_exporter_port(self):
        code, made = self._run("realtime")
        self.assertEqual(code, 0)
        self.assertTrue(made["exp"].started)
        self.assertTrue(made["exp"].closed)
        self.assertEqual(made["exp"].args[1:], ("fake-uuid", "127.0.0.1", 9999))
        self.assertEqual(made["exp"].states, [0, 1, 2, 3])

    def test_configuration_error_returns_2(self):
        def boom(path):
            raise ValueError("bad")

        deps = SimulatorDependencies(boom, boom, FakeRecorder, FakeExporter)
        args = SimpleNamespace(duration_seconds=1, tick_seconds=1, inventory="i", scenario="s")
        self.assertEqual(run_simulation(args, deps), 2)


if __name__ == "__main__":
    unittest.main()
