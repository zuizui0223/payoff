#!/usr/bin/env python3
"""Identify PAYOFF-B tracking fitness terms from matched growth contrasts."""

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
    identify_tracking_fitness_from_matched_contrasts,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-growth", type=float, required=True)
    parser.add_argument("--abiotic-growth", type=float, required=True)
    parser.add_argument("--abiotic-mismatch", type=float, required=True)
    parser.add_argument("--interaction-growth", type=float, required=True)
    parser.add_argument("--interaction-mismatch", type=float, required=True)
    parser.add_argument("--migration-growth", type=float, required=True)
    parser.add_argument("--migration-rate", type=float, required=True)
    parser.add_argument("--phenology-growth", type=float, required=True)
    parser.add_argument("--phenology-rate", type=float, required=True)
    parser.add_argument("--joint-growth", type=float, required=True)
    parser.add_argument("--joint-migration-rate", type=float, required=True)
    parser.add_argument("--joint-phenology-rate", type=float, required=True)
    parser.add_argument(
        "--allow-negative",
        action="store_true",
        help=(
            "allow identified negative coefficients instead of treating them "
            "as incompatibility with the declared penalty model"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_tracking_fitness_parameterization.json"
        ),
    )
    args = parser.parse_args()

    estimate = identify_tracking_fitness_from_matched_contrasts(
        baseline_growth=args.baseline_growth,
        abiotic_growth=args.abiotic_growth,
        abiotic_mismatch=args.abiotic_mismatch,
        interaction_growth=args.interaction_growth,
        interaction_mismatch=args.interaction_mismatch,
        migration_growth=args.migration_growth,
        migration_rate=args.migration_rate,
        phenology_growth=args.phenology_growth,
        phenology_rate=args.phenology_rate,
        joint_growth=args.joint_growth,
        joint_migration_rate=args.joint_migration_rate,
        joint_phenology_rate=args.joint_phenology_rate,
        require_nonnegative=not args.allow_negative,
    )

    receipt = {
        "status": "identified_from_matched_growth_contrasts",
        "fitness_estimate": asdict(estimate),
        "design_contract": {
            "reference": "e=M=m=h=0",
            "abiotic_contrast": "e!=0, M=m=h=0",
            "interaction_contrast": "M!=0, e=m=h=0",
            "migration_cost_contrast": "m!=0, e=M=h=0",
            "phenology_cost_contrast": "h!=0, e=M=m=0",
            "joint_cost_contrast": "m,h!=0, e=M=0",
        },
        "claim_boundary": (
            "exact algebraic identification under matched background ecology "
            "and a common low-density growth scale"
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
        f"baseline={estimate.baseline_growth:.12g} "
        f"A={estimate.abiotic_strength:.12g} "
        f"I={estimate.interaction_strength:.12g} "
        f"c_m={estimate.migration_cost:.12g} "
        f"c_h={estimate.phenology_cost:.12g} "
        f"c_mh={estimate.joint_cost:.12g}"
    )


if __name__ == "__main__":
    main()
