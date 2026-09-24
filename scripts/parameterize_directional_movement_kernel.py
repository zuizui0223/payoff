#!/usr/bin/env python3
"""Identify the biased nearest-neighbor movement kernel from moments."""

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
    infer_directional_movement_kernel_from_moments,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mean-x", type=float, required=True)
    parser.add_argument("--mean-y", type=float, required=True)
    parser.add_argument(
        "--second-moment-x",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--second-moment-y",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--patch-spacing",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_directional_movement_kernel.json"
        ),
    )
    args = parser.parse_args()

    estimate = infer_directional_movement_kernel_from_moments(
        args.mean_x,
        args.mean_y,
        args.second_moment_x,
        args.second_moment_y,
        args.patch_spacing,
    )

    receipt = {
        "status": "directional_one_step_kernel_identified",
        "observed_moments": {
            "mean_x": args.mean_x,
            "mean_y": args.mean_y,
            "second_moment_x": args.second_moment_x,
            "second_moment_y": args.second_moment_y,
            "patch_spacing": args.patch_spacing,
        },
        "movement_kernel": asdict(estimate),
        "claim_boundary": (
            "exact inverse for the declared biased nearest-neighbor "
            "one-step kernel only"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "directional_kernel "
        f"migration_rate={estimate.migration_rate:.12g} "
        f"x_weight={estimate.x_weight:.12g} "
        f"y_weight={estimate.y_weight:.12g} "
        f"x_bias={estimate.x_bias:.12g} "
        f"y_bias={estimate.y_bias:.12g}"
    )


if __name__ == "__main__":
    main()
