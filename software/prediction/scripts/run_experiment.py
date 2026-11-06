"""Experimento PMV3 (Sprint 7): aprovisionamiento reactivo (baseline) frente a predictivo (Green AI).

Uso (desde software/prediction, después de scripts/run_pipeline.py):
  python scripts/run_experiment.py [--headroom 0.20] [--pmax 600] [--idle-ratio 0.5]

Diseño (condiciones equivalentes: mismo periodo de test, mismo margen, mismo modelo de potencia):
- Serie: results/predictions/test_predictions.csv (CPU real y predicha a t+h, en el split de TEST).
- Baseline reactivo = persistencia: reserva para t+h la CPU observada en t, más un margen.
- Green AI: reserva para t+h la CPU predicha por el modelo seleccionado, más el mismo margen.
- Métricas por estrategia:
  * riesgo de SLA = % de intervalos con CPU real > capacidad reservada (subaprovisionamiento);
  * capacidad ociosa media = media de max(0, reservado - real) en puntos de CPU;
  * energía MODELADA (no medida): P = Pidle + (Pmax - Pidle) * reservado/100, integrada en el periodo.
Limitaciones: datos simulados; la capacidad reservada es un proxy; el modelo lineal de potencia es una
aproximación de la literatura (consumo en reposo de ~50 % del pico), no una medición.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/predictions/test_predictions.csv"
OUT = ROOT / "results/experiments"


def load(path: Path):
    rows = []
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((datetime.fromisoformat(r["timestamp"]), float(r["y_true"]), float(r["y_pred"]),
                         r["model"], r["horizon"]))
    return rows


def reserve(forecast: float, headroom: float) -> float:
    return min(100.0, max(0.0, forecast * (1 + headroom)))


def evaluate(actual, reserved, step_h: float, pmax: float, idle_ratio: float) -> dict:
    n = len(actual)
    under = sum(a > c for a, c in zip(actual, reserved))
    idle = [max(0.0, c - a) for a, c in zip(actual, reserved)]
    pidle = pmax * idle_ratio
    energy_wh = sum((pidle + (pmax - pidle) * c / 100.0) * step_h for c in reserved)
    return {"intervals": n, "sla_risk_pct": 100.0 * under / n, "mean_idle_capacity_pp": sum(idle) / n,
            "mean_reserved_pp": sum(reserved) / n, "modeled_energy_wh": energy_wh}


def run(rows, headroom: float, pmax: float, idle_ratio: float) -> dict:
    if len(rows) < 10:
        raise SystemExit("Muy pocas filas de test; ejecute antes scripts/run_pipeline.py")
    step = rows[1][0] - rows[0][0]
    if any(b[0] - a[0] != step for a, b in zip(rows, rows[1:])):
        raise SystemExit("La serie de test no es contigua; el experimento requiere intervalos regulares")
    horizon_steps = {"5m": 1, "15m": 3, "30m": 6}[rows[0][4]]
    usable = rows[horizon_steps:]
    actual = [r[1] for r in usable]
    reactive = [reserve(rows[i][1], headroom) for i in range(len(usable))]   # CPU observada en t
    predictive = [reserve(r[2], headroom) for r in usable]                   # predicción para t+h
    step_h = step / timedelta(hours=1)
    base = evaluate(actual, reactive, step_h, pmax, idle_ratio)
    green = evaluate(actual, predictive, step_h, pmax, idle_ratio)
    delta = {k: green[k] - base[k] for k in ("sla_risk_pct", "mean_idle_capacity_pp", "modeled_energy_wh")}
    delta["modeled_energy_pct"] = 100.0 * delta["modeled_energy_wh"] / base["modeled_energy_wh"]
    return {"generatedAt": datetime.now(timezone.utc).isoformat(), "dataOrigin": "simulated",
            "source": str(SOURCE.relative_to(ROOT)), "model": rows[0][3], "horizon": rows[0][4],
            "period": {"start": usable[0][0].isoformat(), "end": usable[-1][0].isoformat()},
            "parameters": {"headroom": headroom, "pmax_w": pmax, "idle_ratio": idle_ratio},
            "baseline_reactive": base, "green_ai_predictive": green, "delta_green_minus_baseline": delta,
            "limitations": ["Datos simulados (dataset-sim-001).", "Energía modelada, no medida.",
                            "Capacidad reservada como proxy de recursos activos.", "Un solo nodo de referencia."]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--headroom", type=float, default=0.20)
    ap.add_argument("--pmax", type=float, default=600.0)
    ap.add_argument("--idle-ratio", type=float, default=0.5)
    a = ap.parse_args()
    result = run(load(SOURCE), a.headroom, a.pmax, a.idle_ratio)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "experiment_baseline_vs_green_ai.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    b, g, d = result["baseline_reactive"], result["green_ai_predictive"], result["delta_green_minus_baseline"]
    print(f"intervalos={b['intervals']}  margen={a.headroom:.0%}")
    print(f"riesgo SLA:       baseline {b['sla_risk_pct']:.1f}%  green {g['sla_risk_pct']:.1f}%  (Δ {d['sla_risk_pct']:+.1f} pp)")
    print(f"capacidad ociosa: baseline {b['mean_idle_capacity_pp']:.2f}  green {g['mean_idle_capacity_pp']:.2f} pp")
    print(f"energía modelada: baseline {b['modeled_energy_wh']:.0f} Wh  green {g['modeled_energy_wh']:.0f} Wh  ({d['modeled_energy_pct']:+.1f}%)")


if __name__ == "__main__":
    main()
