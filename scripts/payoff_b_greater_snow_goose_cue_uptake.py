#!/usr/bin/env python3
"""Execute the preregistered greater-snow-goose behavioral cue-uptake model.

Input is a preprocessed decision-day table. Movement segmentation and climate
construction are upstream frozen procedures. This script never downloads or
re-segments GPS data and never constructs predictive connectivity from focal
outcomes.

The strongest licensed result from this script is behavioral cue-uptake
support. It cannot identify PAYOFF-B D or q_wait(D).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cue_uptake_empirics import (
    ThresholdCandidateScore,
    mean_standard_error,
    select_threshold_one_se,
)
from src.greater_snow_goose_information_bridge import gaussian_binary_accuracy


REQUIRED = {
    "individual",
    "year",
    "context",
    "decision_date",
    "depart_next_24h",
    "local_temp_anom3",
    "same_day_temp_anom",
    "day_of_year_within_context",
    "wind_support",
    "precipitation",
    "predictive_connectivity_rho",
    "connectivity_training_n",
    "connectivity_window_end_year",
}

PRIMARY_FORMULA = (
    "depart_next_24h ~ "
    "local_temp_anom3 * z_predictive_connectivity "
    "+ day_of_year_within_context + wind_support + precipitation "
    "+ same_day_temp_anom + C(context) + C(year)"
)

NO_THRESHOLD_FORMULA = PRIMARY_FORMULA

THRESHOLD_FORMULA = (
    "depart_next_24h ~ "
    "local_temp_anom3 * cue_active "
    "+ z_predictive_connectivity "
    "+ day_of_year_within_context + wind_support + precipitation "
    "+ same_day_temp_anom + C(context) + C(year)"
)

Q_GRID = [0.50, 0.525, 0.55, 0.575, 0.60, 0.625, 0.65, 0.675, 0.70]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--decision-days", type=Path, required=True)
    p.add_argument(
        "--result-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_greater_snow_goose_cue_uptake_result.json"
        ),
    )
    p.add_argument(
        "--threshold-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_greater_snow_goose_threshold_scores.csv"
        ),
    )
    return p.parse_args()


def _log_loss(y, p):
    eps = 1e-12
    total = 0.0
    for yi, pi in zip(y, p):
        prob = min(1.0 - eps, max(eps, float(pi)))
        total -= (
            float(yi) * math.log(prob)
            + (1.0 - float(yi)) * math.log(1.0 - prob)
        )
    return total / len(y)


def _prepare(data):
    import numpy as np
    import pandas as pd

    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    out = data.copy()
    if out.empty:
        raise ValueError("decision-day table is empty")

    if out[list(REQUIRED)].isna().any().any():
        raise ValueError("required decision-day columns contain missing values")

    out["year"] = out["year"].astype(int)
    out["depart_next_24h"] = out["depart_next_24h"].astype(int)
    if not set(out["depart_next_24h"].unique()).issubset({0, 1}):
        raise ValueError("depart_next_24h must be binary 0/1")

    key = ["individual", "context", "decision_date"]
    if out.duplicated(key).any():
        raise ValueError("duplicate individual x context x decision_date rows")

    if (out["connectivity_training_n"].astype(int) < 15).any():
        raise ValueError(
            "predictive-connectivity training n below preregistered minimum"
        )
    if (
        out["connectivity_window_end_year"].astype(int)
        > out["year"].astype(int) - 1
    ).any():
        raise ValueError("predictive connectivity leaks focal or future year")

    numeric = [
        "local_temp_anom3",
        "same_day_temp_anom",
        "day_of_year_within_context",
        "wind_support",
        "precipitation",
        "predictive_connectivity_rho",
    ]
    for col in numeric:
        out[col] = pd.to_numeric(out[col], errors="raise")
        if not np.isfinite(out[col].to_numpy(dtype=float)).all():
            raise ValueError(f"{col} contains non-finite values")

    if (
        (out["predictive_connectivity_rho"] < -1.0)
        | (out["predictive_connectivity_rho"] > 1.0)
    ).any():
        raise ValueError("predictive_connectivity_rho must lie in [-1,1]")

    out["predictive_q"] = out["predictive_connectivity_rho"].map(
        gaussian_binary_accuracy
    )

    rho = out["predictive_connectivity_rho"].astype(float)
    rho_sd = float(rho.std(ddof=0))
    if not math.isfinite(rho_sd) or rho_sd <= 0.0:
        raise ValueError("predictive connectivity has no variance")
    out["z_predictive_connectivity"] = (
        rho - float(rho.mean())
    ) / rho_sd

    return out, rho_sd


def _estimability(data, rho_sd):
    import numpy as np

    within = (
        data["predictive_connectivity_rho"].astype(float)
        - data.groupby("context")[
            "predictive_connectivity_rho"
        ].transform("mean")
    )
    within_sd = float(np.std(within.to_numpy(dtype=float), ddof=0))
    diagnostics = {
        "rows": int(len(data)),
        "individuals": int(data["individual"].astype(str).nunique()),
        "years": int(data["year"].nunique()),
        "contexts": int(data["context"].astype(str).nunique()),
        "departure_events": int(data["depart_next_24h"].sum()),
        "predictive_connectivity_sd": float(rho_sd),
        "within_context_predictive_connectivity_sd": within_sd,
    }
    passes = (
        diagnostics["individuals"] >= 30
        and diagnostics["years"] >= 4
        and diagnostics["contexts"] >= 3
        and diagnostics["departure_events"] >= 100
        and diagnostics["predictive_connectivity_sd"] >= 0.03
        and diagnostics["within_context_predictive_connectivity_sd"] > 1e-12
    )
    diagnostics["passes"] = bool(passes)
    return diagnostics


def _fit_formula(formula, train):
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    fit = smf.glm(
        formula,
        data=train,
        family=sm.families.Binomial(),
    ).fit()
    if not getattr(fit, "converged", True):
        raise ValueError("binomial model did not converge")
    return fit


def _loio_losses(data, formula, *, threshold_q=None):
    losses = []
    individuals = sorted(data["individual"].astype(str).unique())

    for individual in individuals:
        train = data[
            data["individual"].astype(str) != individual
        ].copy()
        test = data[
            data["individual"].astype(str) == individual
        ].copy()

        for col in ("context", "year"):
            known = set(train[col].astype(str))
            unseen = set(test[col].astype(str)) - known
            if unseen:
                raise ValueError(
                    f"LOIO fold has unseen {col} levels for individual "
                    f"{individual}: {sorted(unseen)}"
                )

        if threshold_q is not None:
            train["cue_active"] = (
                train["predictive_q"].astype(float) >= threshold_q
            ).astype(int)
            test["cue_active"] = (
                test["predictive_q"].astype(float) >= threshold_q
            ).astype(int)
            if train["cue_active"].nunique() < 2:
                raise ValueError(
                    f"threshold q={threshold_q} has no training variation "
                    f"in LOIO fold for {individual}"
                )

        fit = _fit_formula(formula, train)
        pred = fit.predict(test)
        losses.append(
            {
                "individual": individual,
                "rows": int(len(test)),
                "log_loss": _log_loss(
                    test["depart_next_24h"].to_numpy(dtype=float),
                    pred,
                ),
            }
        )
    return losses


def _primary_fit(data):
    import numpy as np
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    raw = smf.glm(
        PRIMARY_FORMULA,
        data=data,
        family=sm.families.Binomial(),
    ).fit()

    clustered = smf.glm(
        PRIMARY_FORMULA,
        data=data,
        family=sm.families.Binomial(),
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": data["individual"].astype(str)},
    )

    term = "local_temp_anom3:z_predictive_connectivity"
    if term not in clustered.params.index:
        raise RuntimeError(f"primary interaction term missing: {term}")

    estimate = float(clustered.params[term])
    se = float(clustered.bse[term])
    p_value = float(clustered.pvalues[term])

    two_way = {"status": "NOT_AVAILABLE"}
    try:
        from statsmodels.stats.sandwich_covariance import cov_cluster_2groups

        covariance, _, _ = cov_cluster_2groups(
            raw,
            data["individual"].astype(str),
            data["year"].astype(str),
        )
        i = list(raw.params.index).index(term)
        se2 = float(np.sqrt(covariance[i, i]))
        two_way = {
            "status": "COMPUTED",
            "estimate": float(raw.params[term]),
            "two_way_cluster_se": se2,
            "ci_low_95": float(raw.params[term]) - 1.96 * se2,
            "ci_high_95": float(raw.params[term]) + 1.96 * se2,
        }
    except Exception as exc:
        two_way = {
            "status": "NOT_AVAILABLE",
            "reason": type(exc).__name__,
        }

    return {
        "formula": PRIMARY_FORMULA,
        "term": term,
        "estimate": estimate,
        "cluster_se": se,
        "ci_low_95": estimate - 1.96 * se,
        "ci_high_95": estimate + 1.96 * se,
        "p_value_two_sided": p_value,
        "registered_direction": "positive",
        "support_status": (
            "SUPPORTED"
            if estimate > 0.0 and estimate - 1.96 * se > 0.0
            else "NOT_SUPPORTED"
        ),
        "two_way_cluster_sensitivity": two_way,
    }


def main():
    args = parse_args()
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError(
            "greater-snow-goose cue uptake requires the empirical extra"
        ) from exc

    data = pd.read_csv(args.decision_days)
    data, rho_sd = _prepare(data)
    gate = _estimability(data, rho_sd)

    result = {
        "registration_id": (
            "payoff_b_greater_snow_goose_gps_cue_uptake_v1_20260929"
        ),
        "status": "NOT_ESTIMABLE",
        "claim_role": (
            "behavioral cue-uptake proxy; not a direct D-to-q theorem test"
        ),
        "estimability_gate": gate,
        "primary": None,
        "threshold_secondary": {
            "status": "NOT_OPENED_PRIMARY_NOT_ESTIMABLE"
        },
        "claim_boundary": [
            "does not identify PAYOFF-B D",
            "does not identify q_wait(D)",
            "predictive q is a Gaussian sign-agreement bridge from rho",
            "same-year future Bylot conditions are forbidden from q construction",
        ],
    }

    threshold_rows = []
    if gate["passes"]:
        result["status"] = "PRIMARY_ESTIMABLE"
        result["primary"] = _primary_fit(data)

        try:
            baseline_losses = _loio_losses(
                data,
                NO_THRESHOLD_FORMULA,
            )
            baseline_mean, baseline_se = mean_standard_error(
                row["log_loss"] for row in baseline_losses
            )

            scores = []
            for q in Q_GRID:
                losses = _loio_losses(
                    data,
                    THRESHOLD_FORMULA,
                    threshold_q=q,
                )
                mean_loss, se_loss = mean_standard_error(
                    row["log_loss"] for row in losses
                )
                score = ThresholdCandidateScore(
                    threshold_q=q,
                    mean_loio_log_loss=mean_loss,
                    se_loio_log_loss=se_loss,
                )
                scores.append(score)
                threshold_rows.append(
                    {
                        "threshold_q": q,
                        "mean_loio_log_loss": mean_loss,
                        "se_loio_log_loss": se_loss,
                        "individual_folds": len(losses),
                        "status": "ESTIMABLE",
                    }
                )

            selection = select_threshold_one_se(
                scores,
                no_threshold_mean_log_loss=baseline_mean,
            )
            result["threshold_secondary"] = {
                "status": selection.status,
                "selected_q": selection.selected_q,
                "reason": selection.reason,
                "no_threshold_mean_loio_log_loss": baseline_mean,
                "no_threshold_se_loio_log_loss": baseline_se,
                "best_threshold_mean_loio_log_loss": (
                    selection.best_mean_log_loss
                ),
                "grid": Q_GRID,
                "one_se_definition": (
                    "adjacent mean loss must exceed best mean loss + best "
                    "candidate SE"
                ),
                "interpretation": (
                    "behavioral/phenomenological threshold only; never q_wait(D)"
                ),
            }
        except (ValueError, RuntimeError) as exc:
            result["threshold_secondary"] = {
                "status": "THRESHOLD_NOT_IDENTIFIED",
                "selected_q": None,
                "reason": "LOIO_NOT_ESTIMABLE",
                "detail": str(exc),
                "grid": Q_GRID,
                "interpretation": (
                    "behavioral/phenomenological threshold only; never q_wait(D)"
                ),
            }

    args.result_output.parent.mkdir(parents=True, exist_ok=True)
    args.result_output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    pd.DataFrame(threshold_rows).to_csv(
        args.threshold_output,
        index=False,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
