#!/usr/bin/env python3
"""Frozen historical predictive-connectivity bridge for Eurasian wigeon."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.calibrate_wigeon_phase_error_era5 import (
    finite_daily_pairs,
    request_batch,
)
from src.predictive_connectivity import detrended_predictive_connectivity
from src.wigeon_phase_error_calibration import tgs_onset_from_daily_mean


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--staging-events", type=Path, required=True)
    p.add_argument("--transitions", type=Path, required=True)
    p.add_argument("--training-start", type=int, default=2000)
    p.add_argument("--training-end", type=int, default=2017)
    p.add_argument("--max-retries", type=int, default=5)
    p.add_argument(
        "--pairs-output",
        type=Path,
        default=Path("outputs/wigeon_predictive_connectivity_pairs.csv"),
    )
    p.add_argument(
        "--transitions-output",
        type=Path,
        default=Path("outputs/wigeon_predictive_connectivity_transitions.csv"),
    )
    p.add_argument(
        "--summary-output",
        type=Path,
        default=Path("outputs/wigeon_predictive_connectivity_result.json"),
    )
    return p.parse_args()


def main():
    args = parse_args()
    try:
        import pandas as pd
        import requests
        import statsmodels.formula.api as smf
    except ImportError as exc:
        raise RuntimeError(
            "wigeon predictive connectivity requires empirical dependencies"
        ) from exc

    staging = pd.read_csv(args.staging_events)
    transitions = pd.read_csv(args.transitions)
    required_events = {"segment", "lat", "lon"}
    required_transitions = {
        "individual_id",
        "year",
        "origin_segment",
        "destination_segment",
        "origin_phase",
        "phase_change",
        "origin_progress_km",
        "endpoint_distance_km",
    }
    if not required_events.issubset(staging.columns):
        raise ValueError("staging-event columns incomplete")
    if not required_transitions.issubset(transitions.columns):
        raise ValueError("transition columns incomplete")
    if len(transitions) != 224:
        raise ValueError(
            f"expected 224 frozen transitions, got {len(transitions)}"
        )

    locations = (
        staging.groupby("segment", as_index=False)
        .agg(lat=("lat", "median"), lon=("lon", "median"))
        .sort_values("segment")
        .reset_index(drop=True)
    )
    if len(locations) < 5:
        raise ValueError("too few staging segments")

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "PAYOFF-B-predictive-connectivity/1.0"}
    )
    endpoint = "https://archive-api.open-meteo.com/v1/archive"

    historical_rows = []
    request_log = []
    for year in range(args.training_start, args.training_end + 1):
        payloads, meta = request_batch(
            session,
            endpoint,
            locations,
            year,
            max_retries=args.max_retries,
        )
        request_log.append(meta)
        for loc, payload in zip(locations.itertuples(index=False), payloads):
            daily = finite_daily_pairs(payload)
            if len(daily) < 210:
                raise RuntimeError(
                    "insufficient ERA5 Jan-Jul data for "
                    f"segment={loc.segment}, year={year}"
                )
            onset = tgs_onset_from_daily_mean(
                [row[0] for row in daily],
                [row[1] for row in daily],
                threshold_c=5.0,
            )
            historical_rows.append(
                {
                    "segment": int(loc.segment),
                    "year": int(year),
                    "tgs_onset_doy": float(onset),
                }
            )
        time.sleep(0.15)

    historical = pd.DataFrame(historical_rows)
    unique_pairs = (
        transitions[["origin_segment", "destination_segment"]]
        .drop_duplicates()
        .sort_values(["origin_segment", "destination_segment"])
    )

    pair_rows = []
    for pair in unique_pairs.itertuples(index=False):
        origin = historical[
            historical["segment"] == int(pair.origin_segment)
        ][["year", "tgs_onset_doy"]].rename(
            columns={"tgs_onset_doy": "origin"}
        )
        destination = historical[
            historical["segment"] == int(pair.destination_segment)
        ][["year", "tgs_onset_doy"]].rename(
            columns={"tgs_onset_doy": "destination"}
        )
        paired = origin.merge(destination, on="year", how="inner")
        estimate = detrended_predictive_connectivity(
            paired["year"],
            paired["origin"],
            paired["destination"],
            min_pairs=6,
        )
        pair_rows.append(
            {
                "origin_segment": int(pair.origin_segment),
                "destination_segment": int(pair.destination_segment),
                "training_years": int(estimate.n_pairs),
                "connectivity_rho": float(estimate.rho),
                "connectivity_r2": float(estimate.r_squared),
                "gaussian_binary_agreement": float(
                    estimate.gaussian_binary_agreement
                ),
            }
        )

    pairs = pd.DataFrame(pair_rows)
    if len(pairs) < 4:
        raise ValueError("fewer than four unique pair connectivities")

    data = transitions.merge(
        pairs,
        on=["origin_segment", "destination_segment"],
        how="left",
        validate="many_to_one",
    )
    if data["connectivity_rho"].isna().any():
        raise ValueError("missing connectivity after transition join")

    rho_sd = float(data["connectivity_rho"].std(ddof=0))
    if not math.isfinite(rho_sd) or rho_sd <= 0:
        raise ValueError("connectivity has no transition-row variance")
    data["z_connectivity"] = (
        data["connectivity_rho"] - float(data["connectivity_rho"].mean())
    ) / rho_sd

    for source, output in (
        ("origin_progress_km", "z_progress"),
        ("endpoint_distance_km", "z_endpoint"),
    ):
        values = data[source].astype(float)
        sd = float(values.std(ddof=0))
        if sd <= 0:
            raise ValueError(f"{source} has no variation")
        data[output] = (values - float(values.mean())) / sd

    fit = smf.ols(
        "phase_change ~ origin_phase * z_connectivity "
        "+ z_progress + z_endpoint + z_progress:z_endpoint + C(year)",
        data=data,
    ).fit().get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"].astype(str),
    )
    term = "origin_phase:z_connectivity"
    index = list(fit.model.exog_names).index(term)
    estimate = float(fit.params[index])
    se = float(fit.bse[index])
    p_value = float(fit.pvalues[index])
    ci_low = estimate - 1.96 * se
    ci_high = estimate + 1.96 * se
    supported = estimate < 0 and ci_high < 0

    args.pairs_output.parent.mkdir(parents=True, exist_ok=True)
    pairs.to_csv(args.pairs_output, index=False)
    data.to_csv(args.transitions_output, index=False)

    result = {
        "contract_id": "payoff_b_predictive_connectivity_v1_20260926",
        "lane": "wigeon_retrospective_mechanistic_bridge",
        "training_period": [args.training_start, args.training_end],
        "outcome_period": [
            int(data["year"].min()),
            int(data["year"].max()),
        ],
        "transition_rows": int(len(data)),
        "individuals": int(data["individual_id"].nunique()),
        "segments": int(len(locations)),
        "unique_segment_pairs": int(len(pairs)),
        "connectivity_rho": {
            "min": float(pairs["connectivity_rho"].min()),
            "max": float(pairs["connectivity_rho"].max()),
            "mean": float(pairs["connectivity_rho"].mean()),
            "sd_across_transition_rows": rho_sd,
        },
        "primary_interaction": {
            "term": term,
            "estimate": estimate,
            "cluster_se": se,
            "ci_low_95": ci_low,
            "ci_high_95": ci_high,
            "p_value_two_sided": p_value,
            "registered_direction": "negative",
            "support_status": "SUPPORTED" if supported else "NOT_SUPPORTED",
        },
        "request_count": len(request_log),
        "claim_boundary": [
            "basic wigeon phase-retention outcomes were known before this predictor analysis",
            "connectivity uses only 2000-2017 historical ERA5 TGS onset",
            "this lane does not test community-level hysteresis",
        ],
    }
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
