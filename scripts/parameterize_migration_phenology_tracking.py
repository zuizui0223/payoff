#!/usr/bin/env python3
"""Convert empirical movement/phenology observables to PAYOFF-B parameters."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking_empirical_parameterization import (
    build_tracking_parameterization,
    infer_movement_kernel_from_component_variances,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variance-x", type=float, required=True)
    parser.add_argument("--variance-y", type=float, required=True)
    parser.add_argument("--patch-spacing", type=float, required=True)
    parser.add_argument("--spatial-gradient", type=float, required=True)
    parser.add_argument("--wave-speed", type=float, required=True)
    parser.add_argument(
        "--phenology-correction-fraction",
        type=float,
        required=True,
    )
    parser.add_argument("--phenology-scale", type=float, required=True)
    parser.add_argument(
        "--max-abs-phenology-shift",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_empirical_tracking_parameterization.json"
        ),
    )
    args = parser.parse_args()

    movement = infer_movement_kernel_from_component_variances(
        args.variance_x,
        args.variance_y,
        args.patch_spacing,
    )
    parameterization = build_tracking_parameterization(
        variance_x=args.variance_x,
        variance_y=args.variance_y,
        patch_spacing=args.patch_spacing,
        spatial_gradient=args.spatial_gradient,
        wave_speed=args.wave_speed,
        phenology_correction_fraction=(
            args.phenology_correction_fraction
        ),
        phenology_scale=args.phenology_scale,
        max_abs_phenology_shift=args.max_abs_phenology_shift,
    )

    receipt = {
        "status": "directly_identified_subset",
        "declared_kernel": (
            "one-step nearest-neighbor anisotropic movement + "
            "first-order phenology correction"
        ),
        "observables": {
            "variance_x": args.variance_x,
            "variance_y": args.variance_y,
            "patch_spacing": args.patch_spacing,
            "spatial_gradient": args.spatial_gradient,
            "wave_speed": args.wave_speed,
            "phenology_correction_fraction": (
                args.phenology_correction_fraction
            ),
            "phenology_scale": args.phenology_scale,
            "max_abs_phenology_shift": (
                args.max_abs_phenology_shift
            ),
        },
        "movement_inverse": asdict(movement),
        "tracking_parameterization": asdict(parameterization),
        "not_identified_from_these_inputs": [
            "baseline_growth",
            "abiotic_mismatch_strength",
            "interaction_strength",
            "migration_cost",
            "phenology_cost",
            "joint_cost",
            "density_coefficient",
            "local_carrying_capacity",
        ],
        "claim_boundary": (
            "algebraic inverse under the declared kernel; "
            "not a generic movement-model fit"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(
        "identified "
        f"migration_rate={parameterization.migration_rate:.12g} "
        f"x_weight={parameterization.dispersal_x_weight:.12g} "
        f"y_weight={parameterization.dispersal_y_weight:.12g} "
        f"climate_velocity={parameterization.climate_velocity:.12g} "
        f"phenology_rate={parameterization.phenology_rate:.12g}"
    )


if __name__ == "__main__":
    main()
