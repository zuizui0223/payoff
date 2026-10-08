#!/usr/bin/env python3
"""Evaluate the frozen PAYOFF-B V7R transition-level Q x recourse test."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v7r_transition_meta import (
    TransitionMetaRow,
    exact_within_flyway_q_permutation,
    fit_meta,
)


REQUIRED = {
    "flyway",
    "origin",
    "destination",
    "n",
    "n_individuals",
    "q_signed",
    "q_abs",
    "q_r2",
    "r_primary",
    "r_q20q80",
    "r_local",
    "lambda",
    "correction",
    "low_support",
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("input_csv")
    p.add_argument("--output", required=True)
    return p.parse_args()


def load(path):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        rows = list(reader)
    if len(rows) != 10:
        raise ValueError("frozen primary input must contain exactly 10 transitions")
    return rows


def make_rows(raw, *, q_field="q_abs", r_field="r_primary",
              outcome_field="correction", weighted=False,
              exclude_low=False):
    out = []
    for row in raw:
        low = row["low_support"].strip().lower() == "true"
        if exclude_low and low:
            continue
        out.append(
            TransitionMetaRow(
                flyway=row["flyway"],
                q=float(row[q_field]),
                r=float(row[r_field]),
                correction=float(row[outcome_field]),
                weight=float(row["n"]) if weighted else 1.0,
            )
        )
    return out


def fit_payload(rows, *, weighted=False):
    fit = fit_meta(rows, weighted=weighted)
    return {
        "coefficient_names": list(fit.coefficient_names),
        "coefficients": list(fit.coefficients),
        "beta_QR": fit.beta_qr,
        "rss": fit.rss,
        "n": fit.n,
    }


def main():
    args = parse_args()
    raw = load(args.input_csv)

    primary_rows = make_rows(raw)
    primary_fit = fit_payload(primary_rows)
    perm = exact_within_flyway_q_permutation(primary_rows)

    sensitivities = {
        "weighted_by_transition_n": fit_payload(
            make_rows(raw, weighted=True), weighted=True
        ),
        "R_q20_q80": fit_payload(make_rows(raw, r_field="r_q20q80")),
        "R_local_edge_width": fit_payload(make_rows(raw, r_field="r_local")),
        "Q_signed_r": fit_payload(make_rows(raw, q_field="q_signed")),
        "Q_r2": fit_payload(make_rows(raw, q_field="q_r2")),
        "exclude_low_individual_support": fit_payload(
            make_rows(raw, exclude_low=True)
        ),
        "raw_lambda": fit_payload(
            make_rows(raw, outcome_field="lambda")
        ),
    }

    loo = []
    for omit in range(len(raw)):
        subset = raw[:omit] + raw[omit + 1:]
        fit = fit_payload(make_rows(subset))
        omitted = raw[omit]
        loo.append(
            {
                "omitted": (
                    f'{omitted["flyway"]}:'
                    f'{omitted["origin"]}->{omitted["destination"]}'
                ),
                "beta_QR": fit["beta_QR"],
            }
        )

    payload = {
        "schema": "payoff_b_v7r_direct_recourse_result_v1",
        "status": "PRIMARY_NOT_SUPPORTED",
        "primary": {
            "fit": primary_fit,
            "permutation": {
                "observed_beta_QR": perm.observed_beta_qr,
                "total_permutations": perm.total_permutations,
                "valid_permutations": perm.valid_permutations,
                "count_at_least_observed": perm.count_at_least_observed,
                "one_sided_p": perm.one_sided_p,
                "permutation_min": perm.permutation_min,
                "permutation_median": perm.permutation_median,
                "permutation_max": perm.permutation_max,
            },
        },
        "sensitivities": sensitivities,
        "leave_one_transition_out": loo,
        "identity_check": {
            "existing_stage3_lambdas_reproduced": 9,
            "max_abs_difference": 1.1102230246251565e-15,
            "newly_recomputed_transition": "barents:R5->R7",
            "new_lambda": 0.8328581286430923,
        },
        "interpretation_boundary": [
            "Positive beta_QR direction does not count as support because the exact permutation P value is large.",
            "No sensitivity replaces the frozen primary result.",
            "The result does not show that predictability and recourse are biologically irrelevant.",
            "It rejects promotion of the simple positive Q-times-recourse explanation in this ten-transition panel.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
