#!/usr/bin/env python3
"""Exploratory within-species predictability versus phase-correction synthesis.

Combines fixed-transition STEP-controller estimates for Greenland and Barents
barnacle geese with independently reconstructed NASA-POWER annual spring-onset
anomaly correlations for the same region pairs.

The initial directional hypothesis was that higher environmental predictability
would be associated with stronger correction. Direct results do not support
that monotonic coupling. The revised analysis treats environmental forecast
innovation and behavioral phase retention as separate control channels.

This transition-level screen is exploratory because transition estimates share
individuals and route segments. It is a Gate-B diagnostic, not a definitive
meta-regression.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr


OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

FLYWAYS = ("greenland", "barents")


def normalized_pair(a: str, b: str):
    return tuple(sorted((str(a), str(b))))


def main():
    rows = []

    for flyway in FLYWAYS:
        ctl_path = OUT / f"stage3_{flyway}_goose_step_controller_by_transition.csv"
        pred_path = OUT / f"stage3_{flyway}_goose_power_predictability_all_pairs.csv"
        if not ctl_path.exists() or not pred_path.exists():
            continue

        ctl = pd.read_csv(ctl_path)
        pred = pd.read_csv(pred_path)
        if ctl.empty or pred.empty:
            continue

        pred_lookup = {}
        for _, p in pred.iterrows():
            pred_lookup[normalized_pair(p["region_a"], p["region_b"])] = p

        for _, c in ctl.iterrows():
            key = normalized_pair(c["origin_region"], c["destination_region"])
            p = pred_lookup.get(key)
            if p is None:
                continue
            lam = float(c["phase_transfer_lambda"])
            rows.append(
                {
                    "flyway": flyway,
                    "origin_region": str(c["origin_region"]),
                    "destination_region": str(c["destination_region"]),
                    "n": int(c["n"]),
                    "n_individuals": int(c["n_individuals"]),
                    "predictability_r": float(p["phenology_correlation_r"]),
                    "predictability_slope": float(p["anomaly_slope_ols"]),
                    "predictability_r2": float(
                        p.get("phenology_predictability_r2",
                              p["phenology_correlation_r"] ** 2)
                    ),
                    "environmental_innovation_sd_days": float(
                        p.get("environmental_innovation_sd_days", np.nan)
                    ),
                    "destination_anomaly_sd_days": float(
                        p.get("destination_anomaly_sd_days", np.nan)
                    ),
                    "lambda": lam,
                    "lambda_se": float(c["phase_transfer_se_cluster"]),
                    "abs_lambda": abs(lam),
                    "correction_strength": 1.0 - abs(lam),
                    "signed_correction_fraction": 1.0 - lam,
                    "stopover_gain": float(c["stopover_gain"]),
                    "stopover_p": float(c["stopover_slope_p_cluster"]),
                    "lambda_p_vs_one": float(
                        c["phase_transfer_p_vs_no_correction_one"]
                    ),
                }
            )

    table = pd.DataFrame(rows)
    table.to_csv(
        OUT / "stage3_barnacle_predictability_controller_pairs.csv",
        index=False,
    )

    receipt = {
        "n_transition_pairs": int(len(table)),
        "n_flyways": int(table["flyway"].nunique()) if len(table) else 0,
        "initial_hypothesis": "higher predictability -> smaller |lambda| / stronger correction",
        "revised_model": (
            "feed-forward environmental innovation and feedback phase retention "
            "are separate channels; no monotonic coupling is assumed"
        ),
    }

    if len(table) >= 4:
        sp = spearmanr(
            table["predictability_r"],
            table["correction_strength"],
        )
        pe = pearsonr(
            table["predictability_r"],
            table["correction_strength"],
        )
        sp_stop = spearmanr(
            table["predictability_r"],
            table["stopover_gain"],
        )
        valid_innov = table.dropna(
            subset=["environmental_innovation_sd_days", "correction_strength"]
        )
        if len(valid_innov) >= 4:
            sp_innov = spearmanr(
                valid_innov["environmental_innovation_sd_days"],
                valid_innov["correction_strength"],
            )
        else:
            sp_innov = None

        receipt.update(
            {
                "spearman_predictability_vs_correction_rho": float(sp.statistic),
                "spearman_predictability_vs_correction_p": float(sp.pvalue),
                "pearson_predictability_vs_correction_r": float(pe.statistic),
                "pearson_predictability_vs_correction_p": float(pe.pvalue),
                "spearman_predictability_vs_stopover_gain_rho": float(
                    sp_stop.statistic
                ),
                "spearman_predictability_vs_stopover_gain_p": float(
                    sp_stop.pvalue
                ),
                "spearman_innovation_vs_correction_rho": (
                    float(sp_innov.statistic) if sp_innov is not None else None
                ),
                "spearman_innovation_vs_correction_p": (
                    float(sp_innov.pvalue) if sp_innov is not None else None
                ),
                "positive_predictability_feedback_coupling_supported": bool(
                    sp.statistic > 0 and sp.pvalue < 0.1
                ),
            }
        )

        # Leave-one-transition-out sign stability of the Spearman relation.
        loo = []
        for i in range(len(table)):
            d = table.drop(table.index[i])
            if len(d) < 3:
                continue
            s = spearmanr(d["predictability_r"], d["correction_strength"])
            loo.append(
                {
                    "left_out": (
                        f"{table.iloc[i]['flyway']}:"
                        f"{table.iloc[i]['origin_region']}->"
                        f"{table.iloc[i]['destination_region']}"
                    ),
                    "rho": float(s.statistic),
                    "p": float(s.pvalue),
                }
            )
        receipt["leave_one_out"] = loo
        receipt["leave_one_out_positive_fraction"] = (
            float(np.mean([x["rho"] > 0 for x in loo])) if loo else None
        )

    receipt["claim_ceiling"] = (
        "Exploratory transition-level channel screen. Region pairs share "
        "individuals/routes and are not independent studies. The direct data "
        "do not support interpreting predictability as feedback gain; treat "
        "environmental innovation and lambda as separate quantities."
    )

    (OUT / "stage3_barnacle_predictability_controller_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2))
    if len(table):
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
