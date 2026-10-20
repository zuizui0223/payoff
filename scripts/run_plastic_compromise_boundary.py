#!/usr/bin/env python3
"""Print a reproducible *synthetic* three-architecture regime transition.

Does not use Wurmbea, AusTraits, GenBank or measured field fitness parameters.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.plastic_compromise_architecture import (
    PlasticCompromise,
    analytic_turnover_crossover,
)

REGISTERED_PARAMETERS = {
    "a": 3.0,
    "b": 1.0,
    "delta": 2.0,
    "q": 0.9,
    "plastic_running_cost": 0.05,
    "plastic_switch_cost": 1.0,
    "module_cost": 3.8,
}
SWITCHING_GRID = (0.0, 0.1, 0.25, 0.5, 0.65625, 0.75, 0.9, 1.0)


def run() -> dict:
    outcomes = [
        PlasticCompromise(rho=rho, **REGISTERED_PARAMETERS).result()
        for rho in SWITCHING_GRID
    ]
    cutoff = analytic_turnover_crossover(
        PlasticCompromise(rho=0.5, **REGISTERED_PARAMETERS)
    )
    return {
        "schema": "PAYOFF_PLASTICITY_VS_MODULES_SYNTHETIC_WITNESS_V1",
        "status": "EXACT_MODEL_WITNESS_NOT_REAL_BIOLOGICAL_DATA",
        "parameters": REGISTERED_PARAMETERS,
        "environment_flip_probability_grid": SWITCHING_GRID,
        "outcomes": outcomes,
        "analytic_crossover": cutoff,
        "sister_repo_roles": {
            "SCH": "same-coordinate causal conflict L, not supplied by this witness",
            "BALANCE": "empirical shared/plastic versus alternative worldlines, not supplied",
            "SLK": "owns architecture value and realization hierarchy",
            "PAYOFF": "derives model-specific stationary ecological turnover and possible coordination invasion barrier",
            "BITA": "selective ecological mechanism identification, not supplied",
        },
        "scientific_claim_boundary": (
            "A conditional, memoryless two-demand toy model; not evidence of "
            "historically evolved new sexual or floral structures, nor a "
            "genetically demonstrated transition in Wurmbea."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=False)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as fh:
            fh.write(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
