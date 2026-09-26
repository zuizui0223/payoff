#!/usr/bin/env python3
"""Post-primary dependency audit for the Amaral predictive-connectivity result.

This does not replace the preregistered GAM.  It asks whether the sign survives
fixed-effect re-expression and whether uncertainty widens when observations are
clustered by ecological dependence units.
"""

from __future__ import annotations

import argparse
import json
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
        "interpretation_rule": (
            "sign stability supports robustness of direction; clustered "
            "intervals are an uncertainty audit and do not overwrite the "
            "preregistered GAM support rule"
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
