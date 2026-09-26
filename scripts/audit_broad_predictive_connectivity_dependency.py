#!/usr/bin/env python3
"""Post-primary dependency audit for the Amaral predictive-connectivity result.

This does not replace the preregistered GAM.  It asks whether the sign survives
fixed-effect re-expression and whether uncertainty widens when observations are
clustered by ecological dependence units.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--rows",
        type=Path,
        default=Path(
            "outputs/payoff_b_broad_predictive_connectivity_rows.csv"
        ),
    )
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_broad_predictive_connectivity_dependency_audit.json"
        ),
    )
    return p.parse_args()


def main():
    args = parse_args()
    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf

    data = pd.read_csv(args.rows)
    formula = (
        "primary_response ~ z_connectivity "
        "+ z_destination_greenup_anomaly + z_bird_speed "
        "+ C(year) + C(species_cell)"
    )
    fit = smf.ols(formula, data=data).fit()
    term_index = list(fit.model.exog_names).index("z_connectivity")

    cluster_results = {}
    for cluster in (
        "species",
        "cell_year",
        "source_target_pair",
    ):
        robust = fit.get_robustcov_results(
            cov_type="cluster",
            groups=data[cluster].astype(str),
        )
        estimate = float(robust.params[term_index])
        se = float(robust.bse[term_index])
        cluster_results[cluster] = {
            "clusters": int(data[cluster].astype(str).nunique()),
            "estimate": estimate,
            "cluster_se": se,
            "ci_low_95": estimate - 1.96 * se,
            "ci_high_95": estimate + 1.96 * se,
            "p_value_two_sided": float(robust.pvalues[term_index]),
        }

    loo_species = []
    for species in sorted(data["species"].astype(str).unique()):
        subset = data[data["species"].astype(str) != species].copy()
        model = smf.ols(formula, data=subset).fit()
        loo_species.append(
            {
                "left_out": species,
                "coefficient": float(model.params["z_connectivity"]),
            }
        )

    loo_year = []
    for year in sorted(data["year"].unique()):
        subset = data[data["year"] != year].copy()
        model = smf.ols(formula, data=subset).fit()
        loo_year.append(
            {
                "left_out": int(year),
                "coefficient": float(model.params["z_connectivity"]),
            }
        )

    species_coefficients = np.asarray(
        [row["coefficient"] for row in loo_species],
        dtype=float,
    )
    year_coefficients = np.asarray(
        [row["coefficient"] for row in loo_year],
        dtype=float,
    )

    within_species = []
    for species in sorted(data["species"].astype(str).unique()):
        subset = data[data["species"].astype(str) == species].copy()
        if len(subset) < 20 or float(subset["z_connectivity"].std()) <= 0.0:
            continue
        model = smf.ols(formula, data=subset).fit()
        if "z_connectivity" not in model.params.index:
            continue
        within_species.append(
            {
                "species": species,
                "rows": int(len(subset)),
                "species_cells": int(subset["species_cell"].nunique()),
                "coefficient": float(model.params["z_connectivity"]),
                "standard_error": float(model.bse["z_connectivity"]),
                "p_value_two_sided": float(model.pvalues["z_connectivity"]),
            }
        )

    within_coef = np.asarray(
        [row["coefficient"] for row in within_species],
        dtype=float,
    )
    within_se = np.asarray(
        [row["standard_error"] for row in within_species],
        dtype=float,
    )
    negative_count = int(np.sum(within_coef < 0.0))
    n_within = int(len(within_coef))
    sign_p_one_sided = (
        sum(
            comb(n_within, k)
            for k in range(negative_count, n_within + 1)
        )
        / (2 ** n_within)
        if n_within > 0
        else None
    )
    valid_meta = np.isfinite(within_se) & (within_se > 0.0)
    if np.any(valid_meta):
        weights = 1.0 / np.square(within_se[valid_meta])
        meta_estimate = float(
            np.sum(weights * within_coef[valid_meta])
            / np.sum(weights)
        )
        meta_se = float(np.sqrt(1.0 / np.sum(weights)))
        meta = {
            "estimate": meta_estimate,
            "standard_error": meta_se,
            "ci_low_95": meta_estimate - 1.96 * meta_se,
            "ci_high_95": meta_estimate + 1.96 * meta_se,
        }
    else:
        meta = None

    result = {
        "status": "POST_PRIMARY_DEPENDENCY_AUDIT",
        "primary_inference_unchanged": True,
        "audit_model": formula,
        "rows": int(len(data)),
        "species": int(data["species"].nunique()),
        "fixed_effect_estimate": float(fit.params["z_connectivity"]),
        "fixed_effect_naive_se": float(fit.bse["z_connectivity"]),
        "cluster_robust": cluster_results,
        "leave_one_species_out": {
            "runs": len(loo_species),
            "negative_fraction": float(
                np.mean(species_coefficients < 0)
            ),
            "minimum_coefficient": float(species_coefficients.min()),
            "maximum_coefficient": float(species_coefficients.max()),
            "rows": loo_species,
        },
        "leave_one_year_out": {
            "runs": len(loo_year),
            "negative_fraction": float(
                np.mean(year_coefficients < 0)
            ),
            "minimum_coefficient": float(year_coefficients.min()),
            "maximum_coefficient": float(year_coefficients.max()),
            "rows": loo_year,
        },
        "within_species_effects": {
            "estimable_species": n_within,
            "negative_species": negative_count,
            "negative_fraction": (
                float(negative_count / n_within)
                if n_within > 0 else None
            ),
            "median_coefficient": (
                float(np.median(within_coef))
                if n_within > 0 else None
            ),
            "one_sided_sign_test_p_for_negative_majority": (
                sign_p_one_sided
            ),
            "inverse_variance_fixed_summary": meta,
            "rows": within_species,
        },
        "interpretation_rule": (
            "the preregistered GAM support rule remains primary; clustered "
            "intervals and within-species effects audit ecological dependence. "
            "If species-clustered or species-level summaries cross zero, the "
            "result must be described as a pooled directional signal rather "
            "than species-independent confirmation"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
