"""Build the registered PAYOFF-B asymptotic-error audit.

This is an implementation/model-prediction diagnostic. It is not used to prove
uniqueness and does not declare an approximation-validity cutoff.
"""

from __future__ import annotations

import csv
import json
from io import StringIO
from math import log
from pathlib import Path

from src.anti_phase_temporal import (
    dimensionless_premium,
    exact_optimal_dimensionless_migration,
    weak_contrast_optimal_dimensionless_migration,
    weak_contrast_shape,
)

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "PAYOFF_B_ASYMPTOTIC_ERROR_TABLE_V1.csv"
DOC_PATH = ROOT / "docs" / "PAYOFF_B_ASYMPTOTIC_ERROR_TABLE_V1.md"
JSON_PATH = ROOT / "data" / "PAYOFF_B_ASYMPTOTIC_ERROR_READOUT_V1.json"

REGISTERED_V = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0)


def _relative_error_pct(approx: float, exact: float) -> float:
    return 100.0 * abs(approx - exact) / abs(exact)


def build_report() -> dict:
    weak_u = weak_contrast_optimal_dimensionless_migration()
    weak_shape_max = weak_contrast_shape(weak_u)
    rows = []
    for v in REGISTERED_V:
        exact_u = exact_optimal_dimensionless_migration(v)
        exact_f = dimensionless_premium(exact_u, v)
        weak_u_approx = weak_u
        strong_u_approx = 1.0 + 1.0 / v
        weak_f_approx = weak_shape_max * v * v
        strong_f_approx = v - log(v) - 1.0

        rows.append(
            {
                "v": v,
                "exact_u_star": exact_u,
                "weak_u_approx": weak_u_approx,
                "weak_u_absolute_error": abs(weak_u_approx - exact_u),
                "weak_u_relative_error_pct": _relative_error_pct(weak_u_approx, exact_u),
                "strong_u_approx": strong_u_approx,
                "strong_u_absolute_error": abs(strong_u_approx - exact_u),
                "strong_u_relative_error_pct": _relative_error_pct(strong_u_approx, exact_u),
                "exact_max_F": exact_f,
                "weak_max_F_approx": weak_f_approx,
                "weak_max_F_relative_error_pct": _relative_error_pct(weak_f_approx, exact_f),
                "strong_max_F_approx": strong_f_approx,
                "strong_max_F_relative_error_pct": _relative_error_pct(strong_f_approx, exact_f),
            }
        )
    return {
        "analysis": "payoff_b_asymptotic_error_table_v1",
        "role": "MODEL_PREDICTION_DIAGNOSTIC_NOT_THEOREM_PROOF",
        "registered_v": list(REGISTERED_V),
        "validity_cutoff_declared": False,
        "weak_u_limit": weak_u,
        "weak_max_F_coefficient": weak_shape_max,
        "strong_u_approximation": "1+1/v",
        "strong_max_F_approximation": "v-log(v)-1",
        "rows": rows,
        "claim_ceiling": (
            "Approximation errors for the declared symmetric anti-phase model only; "
            "no empirical calibration and no theorem proof by numerical grid."
        ),
    }


def render_csv(report: dict) -> str:
    fieldnames = [
        "v",
        "exact_u_star",
        "weak_u_approx",
        "weak_u_absolute_error",
        "weak_u_relative_error_pct",
        "strong_u_approx",
        "strong_u_absolute_error",
        "strong_u_relative_error_pct",
        "exact_max_F",
        "weak_max_F_approx",
        "weak_max_F_relative_error_pct",
        "strong_max_F_approx",
        "strong_max_F_relative_error_pct",
    ]
    out = StringIO()
    writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator=chr(10))
    writer.writeheader()
    for row in report["rows"]:
        writer.writerow({k: f"{row[k]:.15g}" for k in fieldnames})
    return out.getvalue()


def render_markdown(report: dict) -> str:
    by_v = {row["v"]: row for row in report["rows"]}
    lines = [
        "# PAYOFF-B asymptotic error table V1",
        "",
        "## Purpose",
        "",
        "This receipt compares the exact registered scaling curve with the weak- and strong-contrast asymptotes on a small fixed grid. It is a `MODEL-PREDICTION` diagnostic and implementation audit. The theorem does not depend on this table.",
        "",
        "```text",
        f"REGISTERED_V_POINTS = {len(report['registered_v'])}",
        "MODEL_ROLE = MODEL-PREDICTION",
        "VALIDITY_CUTOFF_DECLARED = false",
        f"WEAK_U_RELATIVE_ERROR_AT_V_0.1_PCT = {by_v[0.1]['weak_u_relative_error_pct']:.9f}",
        f"STRONG_U_RELATIVE_ERROR_AT_V_10_PCT = {by_v[10.0]['strong_u_relative_error_pct']:.9f}",
        f"STRONG_U_RELATIVE_ERROR_AT_V_100_PCT = {by_v[100.0]['strong_u_relative_error_pct']:.9f}",
        f"WEAK_MAX_F_RELATIVE_ERROR_AT_V_0.1_PCT = {by_v[0.1]['weak_max_F_relative_error_pct']:.9f}",
        f"STRONG_MAX_F_RELATIVE_ERROR_AT_V_10_PCT = {by_v[10.0]['strong_max_F_relative_error_pct']:.9f}",
        f"STRONG_MAX_F_RELATIVE_ERROR_AT_V_100_PCT = {by_v[100.0]['strong_max_F_relative_error_pct']:.9f}",
        "```",
        "",
        "| v | exact u* | weak u approx | weak u rel. err. % | strong u approx | strong u rel. err. % | exact max F | weak max F rel. err. % | strong max F rel. err. % |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["rows"]:
        lines.append(
            "| {v:g} | {exact_u_star:.9f} | {weak_u_approx:.9f} | "
            "{weak_u_relative_error_pct:.6f} | {strong_u_approx:.9f} | "
            "{strong_u_relative_error_pct:.6f} | {exact_max_F:.9g} | "
            "{weak_max_F_relative_error_pct:.6f} | "
            "{strong_max_F_relative_error_pct:.6f} |".format(**row)
        )
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "The endpoints converge as the analysis predicts: the weak approximation is extremely close at small `v`, while `1+1/v` and `v-log(v)-1` become accurate at large `v`. The table deliberately declares **no validity cutoff**; it reports error rather than inventing a threshold for when an asymptotic formula is 'valid'.",
        "",
        "There is **no empirical calibration** in this audit. The nine `v` values are registered numerical checkpoints, not biological observations and not evidence for the uniqueness theorem. The exact theorem covers every `v>0`; the grid only makes the endpoint approximations quantitatively inspectable.",
        "",
    ]
    return chr(10).join(lines)


def main() -> None:
    report = build_report()
    CSV_PATH.write_text(render_csv(report), encoding="utf-8")
    DOC_PATH.write_text(render_markdown(report), encoding="utf-8")
    JSON_PATH.write_text(json.dumps(report, indent=2) + chr(10), encoding="utf-8")


if __name__ == "__main__":
    main()
