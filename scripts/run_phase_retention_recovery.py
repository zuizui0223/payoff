#!/usr/bin/env python3
"""Run one frozen PAYOFF-B phase-retention recovery simulation."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.phase_retention_recovery import (
    LambdaRecoveryDesign,
    lower_tail_null_probability,
    recovery_design_from_observed_predictor_sd,
    simulate_lambda_recovery,
    simulate_naive_lambda_once,
)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--true-lambda", type=float, required=True)
    phase_sd = p.add_mutually_exclusive_group(required=True)
    phase_sd.add_argument("--latent-phase-sd", type=float)
    phase_sd.add_argument("--observed-predictor-sd", type=float)
    p.add_argument("--predictor-error-sd", type=float, required=True)
    p.add_argument("--outcome-error-sd", type=float, required=True)
    p.add_argument("--error-correlation", type=float, default=0.0)
    p.add_argument("--process-noise-sd", type=float, default=0.0)
    p.add_argument("--n-pairs", type=int, required=True)
    p.add_argument("--replicates", type=int, default=5000)
    p.add_argument("--seed", type=int, default=20260922)
    p.add_argument("--observed-lambda", type=float)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_lambda_recovery.json"),
    )
    args = p.parse_args()

    if args.observed_predictor_sd is not None:
        design = recovery_design_from_observed_predictor_sd(
            true_lambda=args.true_lambda,
            observed_predictor_sd=args.observed_predictor_sd,
            predictor_error_sd=args.predictor_error_sd,
            outcome_error_sd=args.outcome_error_sd,
            error_correlation=args.error_correlation,
            process_noise_sd=args.process_noise_sd,
            n_pairs=args.n_pairs,
        )
        phase_variance_source = "observed_predictor_sd_minus_error_variance"
    else:
        design = LambdaRecoveryDesign(
            true_lambda=args.true_lambda,
            latent_phase_sd=args.latent_phase_sd,
            predictor_error_sd=args.predictor_error_sd,
            outcome_error_sd=args.outcome_error_sd,
            error_correlation=args.error_correlation,
            process_noise_sd=args.process_noise_sd,
            n_pairs=args.n_pairs,
        )
        phase_variance_source = "direct_latent_phase_sd_benchmark"
    summary = simulate_lambda_recovery(
        design,
        replicates=args.replicates,
        seed=args.seed,
    )

    payload = {
        "status": "lambda_recovery_complete",
        "design": asdict(design),
        "phase_variance_source": phase_variance_source,
        "summary": asdict(summary),
        "observed_lambda": args.observed_lambda,
        "lower_tail_null_probability": None,
        "claim_boundary": (
            "observation-layer parameter recovery only; empirical interpretation "
            "requires source-backed measurement-error calibration"
        ),
    }

    if args.observed_lambda is not None:
        null_estimates = tuple(
            simulate_naive_lambda_once(
                design,
                seed=args.seed + index * 1_000_003,
            )
            for index in range(args.replicates)
        )
        payload["lower_tail_null_probability"] = (
            lower_tail_null_probability(
                args.observed_lambda,
                null_estimates,
            )
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "lambda_recovery "
        f"true={design.true_lambda:.6g} "
        f"expected_naive={summary.expected_naive_lambda:.6g} "
        f"mean_naive={summary.mean_naive_lambda:.6g} "
        f"q025={summary.q025:.6g} "
        f"q975={summary.q975:.6g} "
        f"replicates={summary.replicates}"
    )


if __name__ == "__main__":
    main()
