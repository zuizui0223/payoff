#!/usr/bin/env python3
"""Run the frozen event-structure wigeon SIMEX sensitivity."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.wigeon_phase_simex import run_wigeon_simex


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--transitions", type=Path, required=True)
    p.add_argument(
        "--contract-json",
        type=Path,
        default=Path(
            "data/wigeon_phase_simex_sensitivity_contract_20260923.json"
        ),
    )
    p.add_argument(
        "--curve-output",
        type=Path,
        default=Path("outputs/wigeon_phase_simex_curve.csv"),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path("outputs/wigeon_phase_simex_receipt.json"),
    )
    args = p.parse_args()

    import pandas as pd

    contract = json.loads(
        args.contract_json.read_text(encoding="utf-8")
    )
    frame = pd.read_csv(args.transitions)
    expected = contract["source"]
    if len(frame) != int(expected["expected_pairs"]):
        raise SystemExit(
            "wigeon SIMEX transition count mismatch: "
            f"{len(frame)} != {expected['expected_pairs']}"
        )
    individuals = int(
        frame["individual_id"].astype(str).nunique()
    )
    if individuals != int(expected["expected_individuals"]):
        raise SystemExit(
            "wigeon SIMEX individual count mismatch: "
            f"{individuals} != {expected['expected_individuals']}"
        )

    design = contract["simulation_design"]
    zeta = tuple(float(v) for v in design["simex_zeta"])
    replicates = int(design["replicates_per_zeta"])
    base_seed = int(design["seed"])

    results = []
    curve_rows = []
    for scenario_index, scenario in enumerate(contract["scenarios"]):
        result = run_wigeon_simex(
            frame,
            scenario_name=str(scenario["name"]),
            error_sd_days=float(scenario["error_sd_days"]),
            error_correlation=float(scenario["error_correlation"]),
            zeta_values=zeta,
            replicates_per_zeta=replicates,
            seed=base_seed + scenario_index * 10_000_019,
        )
        if (
            abs(
                result.observed_lambda_hat
                - float(expected["expected_naive_lambda_hat"])
            )
            > float(expected["identity_tolerance"])
        ):
            raise SystemExit(
                "wigeon SIMEX observed-lambda identity gate failed"
            )
        results.append(asdict(result))
        for point in result.zeta_points:
            curve_rows.append(
                {
                    "scenario": result.scenario_name,
                    "error_sd_days": result.error_sd_days,
                    "error_correlation": result.error_correlation,
                    **asdict(point),
                }
            )

    args.curve_output.parent.mkdir(parents=True, exist_ok=True)
    with args.curve_output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(curve_rows[0]),
        )
        writer.writeheader()
        writer.writerows(curve_rows)

    receipt = {
        "status": "wigeon_phase_simex_sensitivity_complete",
        "contract_source": str(args.contract_json),
        "transition_source": str(args.transitions),
        "pairs": len(frame),
        "individuals": individuals,
        "results": results,
        "claim_boundary": contract["claim_boundary"],
    }
    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.receipt_output)
    for result in results:
        print(
            "wigeon_simex "
            f"scenario={result['scenario_name']} "
            f"observed={result['observed_lambda_hat']:.6f} "
            "extrapolated="
            f"{result['simex_extrapolated_lambda_at_minus_one']:.6f}"
        )


if __name__ == "__main__":
    main()
