#!/usr/bin/env python3
"""Prospective fed-only snow-goose physiological J-mechanism analysis.

Inputs
------
data_exp_Feb2025.txt:
    Collar, UNIKCAPT, DaysInCap, FoodTreatment, ...
cond2009_July2024.txt:
    Collar, cond1, cond2, delta

Primary subset
--------------
FoodTreatment == FED and non-missing cond1/cond2/DaysInCap/UNIKCAPT.

Primary model
-------------
cond2 ~ cond1 + DaysInCap

Uncertainty is cluster-robust by UNIKCAPT because treatment duration is assigned
at capture-group level. Individual birds are not treated as independent
treatment replicates.

Claim ceiling
-------------
Physiological J-like mechanism only. Never natural J, D_eff, or q_wait.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.snow_goose_j_mechanism import (
    classify_j_mechanism,
    evaluate_j_mechanism_gate,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--experiment", type=Path, required=True)
    p.add_argument("--condition", type=Path, required=True)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_snow_goose_j_mechanism.json"),
    )
    return p.parse_args()


def _read_table(pd, path):
    # Public Dryad text files may be tab/whitespace delimited. Use python
    # inference rather than hard-coding a separator before bytes are acquired.
    return pd.read_csv(path, sep=None, engine="python")


def main():
    args = parse_args()
    try:
        import numpy as np
        import pandas as pd
        import statsmodels.formula.api as smf
    except ImportError as exc:
        raise RuntimeError(
            "J-mechanism lane requires empirical dependencies"
        ) from exc

    exp = _read_table(pd, args.experiment)
    cond = _read_table(pd, args.condition)

    exp_required = {"Collar", "UNIKCAPT", "DaysInCap", "FoodTreatment"}
    cond_required = {"Collar", "cond1", "cond2"}
    if not exp_required.issubset(exp.columns):
        raise ValueError(
            "experiment table missing: "
            + ",".join(sorted(exp_required - set(exp.columns)))
        )
    if not cond_required.issubset(cond.columns):
        raise ValueError(
            "condition table missing: "
            + ",".join(sorted(cond_required - set(cond.columns)))
        )

    if exp["Collar"].duplicated().any():
        raise ValueError("experiment Collar must be unique")
    if cond["Collar"].duplicated().any():
        raise ValueError("condition Collar must be unique")

    data = exp.merge(
        cond[["Collar", "cond1", "cond2"]],
        on="Collar",
        how="inner",
        validate="one_to_one",
    )
    data["FoodTreatment_norm"] = (
        data["FoodTreatment"].astype(str).str.strip().str.upper()
    )
    fed = data[data["FoodTreatment_norm"] == "FED"].copy()

    for col in ("DaysInCap", "cond1", "cond2"):
        fed[col] = pd.to_numeric(fed[col], errors="coerce")
    fed = fed.dropna(
        subset=["UNIKCAPT", "DaysInCap", "cond1", "cond2"]
    ).copy()

    if not fed.empty:
        numeric = fed[["DaysInCap", "cond1", "cond2"]].to_numpy(dtype=float)
        if not np.isfinite(numeric).all():
            raise ValueError("fed primary variables contain non-finite values")
        if (fed["DaysInCap"] <= 0).any():
            raise ValueError(
                "FED primary subset must contain only positive captivity durations"
            )

    group_sizes = (
        fed.groupby("UNIKCAPT").size()
        if not fed.empty
        else pd.Series(dtype=int)
    )
    gate = evaluate_j_mechanism_gate(
        females=len(fed),
        capture_groups=fed["UNIKCAPT"].nunique(),
        duration_levels=fed["DaysInCap"].nunique(),
        min_group_size=int(group_sizes.min()) if len(group_sizes) else 0,
    )

    result = {
        "registration_id": (
            "payoff_b_snow_goose_public_2009_j_mechanism_v1_20260930"
        ),
        "status": "NOT_ESTIMABLE",
        "gate": {
            "estimable": gate.estimable,
            "reasons": list(gate.reasons),
            "females": gate.females,
            "capture_groups": gate.capture_groups,
            "duration_levels": gate.duration_levels,
            "min_group_size": gate.min_group_size,
        },
        "primary": None,
        "claim_boundary": [
            "2009-only source cannot be a substitute primary duration-fitness test",
            "fed-only body-condition mechanism avoids deliberate fasting but not handling/confinement stress",
            "capture group is assignment/uncertainty cluster",
            "positive result is J-like physiology only, not natural J",
            "does not estimate D_eff or q_wait",
        ],
    }

    if gate.estimable:
        formula = "cond2 ~ cond1 + DaysInCap"
        fit = smf.ols(formula, data=fed).fit(
            cov_type="cluster",
            cov_kwds={"groups": fed["UNIKCAPT"].astype(str)},
        )
        term = "DaysInCap"
        classification = classify_j_mechanism(
            estimable=True,
            days_estimate=float(fit.params[term]),
            days_se=float(fit.bse[term]),
        )
        result["status"] = classification.status
        result["primary"] = {
            "formula": formula,
            "term": term,
            "estimate": classification.estimate,
            "cluster_se": classification.se,
            "ci_low_95": classification.ci_low_95,
            "ci_high_95": classification.ci_high_95,
            "registered_direction": "negative",
            "interpretation": classification.interpretation,
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
