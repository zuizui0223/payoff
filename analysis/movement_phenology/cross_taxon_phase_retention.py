#!/usr/bin/env python3
"""Taxon-level synthesis of direct movement–phenology phase retention.

The direct registry contains multiple barnacle-goose routes from one species.
This script prevents pseudoreplication by reducing direct rows to one
taxon-level descriptive record before any cross-taxon comparison.

No pooled mean or random-effects meta-analysis is claimed at n=3 taxa.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE = Path("data/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_REGISTRY.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)


def main():
    d = pd.read_csv(SOURCE)
    d = d[d["status"].astype(str).str.startswith("DIRECT_")].copy()

    for c in (
        "phase_transfer_lambda",
        "phase_transfer_se",
        "phase_retention_abs",
        "correction_fraction",
        "n_events",
        "n_individuals",
        "stopover_gain",
        "speed_gain_log_per_day",
    ):
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")

    d = d[np.isfinite(d["phase_retention_abs"])].copy()
    if d.empty:
        raise SystemExit("No finite direct phase-retention rows")

    rows = []
    for taxon, x in d.groupby("taxon", dropna=False):
        vals = x["phase_retention_abs"].dropna().to_numpy(float)
        lambdas = x["phase_transfer_lambda"].dropna().to_numpy(float)
        corr = 1.0 - vals

        architectures = sorted(
            set(x["controller_architecture"].dropna().astype(str))
        )
        statuses = sorted(set(x["status"].dropna().astype(str)))

        rows.append(
            {
                "taxon": str(taxon),
                "n_direct_rows": int(len(x)),
                "n_stable_rows": int(np.sum(vals < 1.0)),
                "all_direct_rows_stable": bool(np.all(vals < 1.0)),
                "median_abs_lambda": float(np.median(vals)),
                "min_abs_lambda": float(np.min(vals)),
                "max_abs_lambda": float(np.max(vals)),
                "median_correction_strength": float(np.median(corr)),
                "min_correction_strength": float(np.min(corr)),
                "max_correction_strength": float(np.max(corr)),
                "median_signed_lambda": float(np.median(lambdas)),
                "n_events_sum_descriptive": int(
                    np.nansum(x["n_events"].to_numpy(float))
                ),
                "n_individuals_max_descriptive": int(
                    np.nanmax(x["n_individuals"].to_numpy(float))
                ),
                "architectures": " | ".join(architectures),
                "statuses": " | ".join(statuses),
                "has_detected_speed_actuator": bool(
                    np.any(
                        np.isfinite(x["speed_gain_p"])
                        & (pd.to_numeric(x["speed_gain_p"], errors="coerce") < 0.05)
                    )
                ),
                "has_detected_stopover_actuator": bool(
                    np.any(
                        np.isfinite(x["stopover_slope_p"])
                        & (
                            pd.to_numeric(
                                x["stopover_slope_p"], errors="coerce"
                            )
                            < 0.05
                        )
                    )
                ),
            }
        )

    taxa = pd.DataFrame(rows).sort_values("median_abs_lambda").reset_index(
        drop=True
    )
    taxa.to_csv(OUT / "cross_taxon_phase_retention_summary.csv", index=False)

    # Figure-ready taxon intervals: point = taxon median, whisker = observed
    # route/population range within that taxon. These are descriptive ranges,
    # not confidence intervals.
    fig = taxa[
        [
            "taxon",
            "n_direct_rows",
            "median_abs_lambda",
            "min_abs_lambda",
            "max_abs_lambda",
            "median_correction_strength",
            "min_correction_strength",
            "max_correction_strength",
            "has_detected_speed_actuator",
            "has_detected_stopover_actuator",
            "architectures",
        ]
    ].copy()
    fig.to_csv(
        OUT / "cross_taxon_phase_retention_figure_data.csv", index=False
    )

    receipt = {
        "n_taxa": int(len(taxa)),
        "taxa": taxa["taxon"].tolist(),
        "all_taxa_have_at_least_one_stable_direct_row": bool(
            np.all(taxa["n_stable_rows"] >= 1)
        ),
        "all_registered_direct_rows_stable": bool(
            np.all(taxa["all_direct_rows_stable"])
        ),
        "taxon_median_abs_lambda_range": [
            float(taxa["median_abs_lambda"].min()),
            float(taxa["median_abs_lambda"].max()),
        ],
        "taxon_median_correction_strength_range": [
            float(taxa["median_correction_strength"].min()),
            float(taxa["median_correction_strength"].max()),
        ],
        "common_coordinate": "R_phi = |lambda|",
        "aggregation_rule": (
            "one descriptive record per taxon; repeated flyways/routes enter "
            "only as within-taxon observed ranges"
        ),
        "claim_ceiling": (
            "Three-taxon descriptive synthesis. Do not interpret the taxon "
            "medians as independent estimates of one universal lambda and do "
            "not run a conventional meta-analysis at n=3."
        ),
    }
    (OUT / "cross_taxon_phase_retention_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(receipt, indent=2))
    print(taxa.to_string(index=False))


if __name__ == "__main__":
    main()
