#!/usr/bin/env python3
"""Run a frozen-control PAYOFF-B 2D tracking projection from JSON receipts."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking_empirical_bridge import EmpiricalTrackingControls
from src.tracking_empirical_parameterization import TrackingFitnessEstimate
from src.tracking_empirical_prediction import (
    build_empirical_landscape_bundle,
    simulate_empirical_landscape_prediction,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tracking-controls-json",
        type=Path,
        required=True,
        help=(
            "JSON produced by audit_interval_tracking_calibration.py with "
            "all environmental control arguments supplied"
        ),
    )
    parser.add_argument(
        "--fitness-json",
        type=Path,
        required=True,
        help=(
            "JSON produced by parameterize_migration_phenology_fitness.py"
        ),
    )
    parser.add_argument("--prediction-wave-speed", type=float)
    parser.add_argument("--prediction-spatial-gradient", type=float)
    parser.add_argument("--width", type=int, default=41)
    parser.add_argument("--height", type=int, default=21)
    parser.add_argument("--initial-distribution-sd", type=float, default=2.0)
    parser.add_argument("--initial-total-abundance", type=float, default=500.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=100.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--extinction-threshold", type=float, default=1.0)
    parser.add_argument("--boundary-retention", type=float, default=1.0)
    parser.add_argument("--barrier-retention", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--burn-in", type=int, default=30)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_empirical_landscape_projection.json"
        ),
    )
    args = parser.parse_args()

    tracking_receipt = load_json(args.tracking_controls_json)
    controls_payload = tracking_receipt.get("tracking_controls")
    if controls_payload is None:
        raise SystemExit(
            "tracking-controls receipt has no simulation-ready controls"
        )
    controls = EmpiricalTrackingControls(**controls_payload)
    if not controls.full_tracking_controls_ready:
        raise SystemExit(
            "tracking-controls receipt is partial: timing-axis h is not licensed"
        )

    fitness_receipt = load_json(args.fitness_json)
    fitness_payload = fitness_receipt.get("fitness_estimate")
    if fitness_payload is None:
        raise SystemExit(
            "fitness receipt has no identified fitness_estimate"
        )
    fitness = TrackingFitnessEstimate(**fitness_payload)

    bundle = build_empirical_landscape_bundle(
        controls,
        fitness,
        width=args.width,
        height=args.height,
        prediction_spatial_gradient=args.prediction_spatial_gradient,
        prediction_wave_speed=args.prediction_wave_speed,
        initial_distribution_sd=args.initial_distribution_sd,
        initial_total_abundance=args.initial_total_abundance,
        local_carrying_capacity=args.local_carrying_capacity,
        density_coefficient=args.density_coefficient,
        extinction_threshold=args.extinction_threshold,
        boundary_retention=args.boundary_retention,
        barrier_retention=args.barrier_retention,
        steps=args.steps,
        burn_in=args.burn_in,
    )
    prediction = simulate_empirical_landscape_prediction(bundle)

    prediction_class = (
        "calibration_environment_mechanistic_projection"
        if bundle.prediction_is_calibration_environment
        else "held_out_forcing_projection"
    )

    receipt = {
        "status": prediction_class,
        "tracking_controls_source": str(args.tracking_controls_json),
        "fitness_source": str(args.fitness_json),
        "decision_interval_seconds": bundle.decision_interval_seconds,
        "frozen_strategy": asdict(bundle.strategy),
        "movement_kernel": {
            "kind": controls.movement_kernel_kind,
            "x_weight": controls.dispersal_x_weight,
            "y_weight": controls.dispersal_y_weight,
            "x_bias": controls.dispersal_x_bias,
            "y_bias": controls.dispersal_y_bias,
        },
        "calibration_environment": {
            "spatial_gradient": controls.spatial_gradient,
            "wave_speed": controls.environmental_wave_speed,
            "climate_velocity": controls.climate_velocity,
        },
        "prediction_environment": {
            "spatial_gradient": bundle.prediction_spatial_gradient,
            "wave_speed": bundle.prediction_wave_speed,
            "climate_velocity": bundle.scenario.climate_velocity,
        },
        "phenology_control": {
            "rate": controls.phenology_rate,
            "scale": controls.phenology_scale,
            "max_abs_shift": controls.max_abs_phenology_shift,
        },
        "fitness_estimate": asdict(fitness),
        "landscape_assumptions": {
            "width": bundle.scenario.width,
            "height": bundle.scenario.height,
            "patch_spacing": bundle.scenario.patch_spacing,
            "initial_distribution_sd": (
                bundle.scenario.initial_distribution_sd
            ),
            "initial_total_abundance": (
                bundle.scenario.initial_total_abundance
            ),
            "local_carrying_capacity": (
                bundle.scenario.local_carrying_capacity
            ),
            "density_coefficient": (
                bundle.scenario.density_coefficient
            ),
            "boundary_retention": (
                bundle.scenario.boundary_retention
            ),
            "barrier_retention": (
                bundle.scenario.barrier_retention
            ),
            "habitat": "open_regular_grid",
            "steps": bundle.scenario.steps,
            "burn_in": bundle.scenario.burn_in,
        },
        "prediction": {
            "mean_low_density_growth": (
                prediction.mean_low_density_growth
            ),
            "mean_realized_growth": prediction.mean_realized_growth,
            "final_abundance": prediction.final_abundance,
            "minimum_abundance": prediction.minimum_abundance,
            "final_climate_centroid": (
                prediction.final_climate_centroid
            ),
            "final_phenology_shift": (
                prediction.final_phenology_shift
            ),
            "rms_abiotic_mismatch": (
                prediction.rms_abiotic_mismatch
            ),
            "phenology_limit_fraction": (
                prediction.phenology_limit_fraction
            ),
            "persisted": prediction.persisted,
        },
        "claim_boundary": (
            "frozen-control open-grid mechanistic projection; not empirical "
            "validation unless forcing, habitat, fitness scale and held-out "
            "outcome are independently observed"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "empirical_tracking_projection "
        f"status={prediction_class} "
        f"migration_rate={bundle.strategy.migration_rate:.12g} "
        f"phenology_rate={bundle.strategy.phenology_rate:.12g} "
        f"calibration_velocity={controls.climate_velocity:.12g} "
        f"prediction_velocity={bundle.scenario.climate_velocity:.12g} "
        f"mean_low_density_growth={prediction.mean_low_density_growth:.12g} "
        f"final_abundance={prediction.final_abundance:.12g} "
        f"persisted={int(prediction.persisted)}"
    )


if __name__ == "__main__":
    main()
