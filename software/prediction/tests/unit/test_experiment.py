from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("run_experiment", Path(__file__).resolve().parents[2] / "scripts/run_experiment.py")
exp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp)

T0 = datetime(2026, 9, 1, tzinfo=timezone.utc)


def rows(values, preds, horizon="15m"):
    return [(T0 + timedelta(minutes=5 * i), v, p, "random_forest", horizon) for i, (v, p) in enumerate(zip(values, preds))]


def test_reserve_is_clipped():
    assert exp.reserve(90, 0.2) == 100 and exp.reserve(-5, 0.2) == 0 and exp.reserve(50, 0.2) == 60


def test_perfect_forecast_never_underprovisions_and_beats_reactive_on_a_ramp():
    ramp = [10.0 + 5 * i for i in range(14)]                  # demanda creciente: el reactivo llega tarde
    result = exp.run(rows(ramp, ramp), headroom=0.0, pmax=600, idle_ratio=0.5)
    assert result["green_ai_predictive"]["sla_risk_pct"] == 0
    assert result["baseline_reactive"]["sla_risk_pct"] == 100
    assert result["dataOrigin"] == "simulated"


def test_energy_follows_linear_power_model():
    flat = [50.0] * 13
    r = exp.run(rows(flat, flat), headroom=0.0, pmax=600, idle_ratio=0.5)
    n = r["baseline_reactive"]["intervals"]
    assert r["baseline_reactive"]["modeled_energy_wh"] == pytest.approx(n * (300 + 300 * 0.5) * (5 / 60))


def test_rejects_non_contiguous_series():
    bad = rows([1.0] * 12, [1.0] * 12)
    bad[5] = (bad[5][0] + timedelta(minutes=1),) + bad[5][1:]
    with pytest.raises(SystemExit):
        exp.run(bad, 0.2, 600, 0.5)
