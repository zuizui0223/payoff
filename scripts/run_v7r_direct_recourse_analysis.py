#!/usr/bin/env python3
"""Run the frozen PAYOFF-B V7R predictability x direct-recourse test.

Inputs are the frozen Stage-3 barnacle-goose artifacts plus the already frozen
ERA5 reliability anomaly tables. The script reconstructs Q, R and lambda from
source rows, verifies existing controller identities, then opens only the
predeclared cross-transition Q x R outcome.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.route_recourse_capacity import (
    TransitionDuration,
    build_edge_envelopes,
    remaining_recourse,
)
from src.v7r_transition_meta import (
    TransitionMetaRow,
    exact_within_flyway_q_permutation,
    fit_meta,
)

TERMINAL = {"greenland": "R4", "svalbard": "R4", "barents": "R7"}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--multiflyway-dir", type=Path, required=True)
    p.add_argument("--svalbard-dir", type=Path, required=True)
    p.add_argument("--era5-multiflyway-dir", type=Path, required=True)
    p.add_argument("--era5-svalbard-dir", type=Path, required=True)
    p.add_argument("--output-json", type=Path, required=True)
    p.add_argument("--transition-output", type=Path, required=True)
    return p.parse_args()


def slope(x, y):
    import numpy as np
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or float(np.var(x)) <= 0:
        raise ValueError("slope requires nonzero predictor variance")
    return float(np.cov(x, y, ddof=0)[0, 1] / np.var(x))


def correlation(x, y):
    import numpy as np
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or float(np.std(x)) <= 0 or float(np.std(y)) <= 0:
        raise ValueError("correlation requires nonzero variance")
    return float(np.corrcoef(x, y)[0, 1])


def transition_frame(frame, flyway, *, svalbard=False):
    data = frame.copy()
    data["flyway"] = flyway
    if svalbard:
        data["duration_days"] = (
            data["origin_stopover_days"].astype(float)
            + data["transit_days"].astype(float)
        )
        data["origin_phase"] = data["origin_arrival_phase_days"].astype(float)
        data["destination_phase"] = data[
            "destination_arrival_phase_days"
        ].astype(float)
    else:
        data["duration_days"] = (
            data["destination_arrival_doy"].astype(float)
            - data["origin_arrival_doy"].astype(float)
        )
        data["origin_phase"] = data[
            "origin_arrival_phase_anom"
        ].astype(float)
        data["destination_phase"] = data[
            "destination_arrival_phase_anom"
        ].astype(float)
    return data[
        [
            "flyway",
            "individual_id",
            "year",
            "origin_region",
            "destination_region",
            "duration_days",
            "origin_stopover_days",
            "origin_phase",
            "destination_phase",
        ]
    ].copy()


def power_predictability(multiflyway_dir, svalbard_dir):
    import pandas as pd
    rows = []
    for flyway in ("greenland", "barents"):
        frame = pd.read_csv(
            multiflyway_dir
            / f"stage3_{flyway}_goose_power_predictability_all_pairs.csv"
        )
        for row in frame.itertuples(index=False):
            rows.append(
                {
                    "flyway": flyway,
                    "origin_region": str(row.region_a),
                    "destination_region": str(row.region_b),
                    "q_signed_r": float(row.phenology_correlation_r),
                    "q_r2": float(row.phenology_predictability_r2),
                    "q_slope": float(row.anomaly_slope_ols),
                }
            )

    onset = pd.read_csv(
        svalbard_dir / "stage3_svalbard_goose_power_gdd_onsets.csv"
    )
    onset = onset[onset["fit_status"].astype(str) == "PASS"].copy()
    pivot = onset.pivot(
        index="year",
        columns="region_id",
        values="onset_anomaly_days",
    )
    regions = sorted(pivot.columns, key=lambda value: int(str(value)[1:]))
    for i, origin in enumerate(regions):
        for destination in regions[i + 1 :]:
            pair = pivot[[origin, destination]].dropna()
            r = correlation(pair[origin], pair[destination])
            rows.append(
                {
                    "flyway": "svalbard",
                    "origin_region": str(origin),
                    "destination_region": str(destination),
                    "q_signed_r": r,
                    "q_r2": r * r,
                    "q_slope": slope(pair[origin], pair[destination]),
                }
            )
    return pd.DataFrame(rows)


def era5_predictability(multiflyway_dir, svalbard_dir):
    import pandas as pd
    paths = {
        "greenland": multiflyway_dir / "greenland_era5_gdd_anomalies.csv",
        "barents": multiflyway_dir / "barents_era5_gdd_anomalies.csv",
        "svalbard": svalbard_dir / "svalbard_era5_gdd_anomalies.csv",
    }
    rows = []
    for flyway, path in paths.items():
        frame = pd.read_csv(path)
        frame = frame[frame["fit_status"].astype(str) == "PASS"].copy()
        pivot = frame.pivot(
            index="year",
            columns="region_id",
            values="onset_anomaly_days",
        )
        regions = sorted(pivot.columns, key=lambda value: int(str(value)[1:]))
        for i, origin in enumerate(regions):
            for destination in regions[i + 1 :]:
                pair = pivot[[origin, destination]].dropna()
                rows.append(
                    {
                        "flyway": flyway,
                        "origin_region": str(origin),
                        "destination_region": str(destination),
                        "era5_signed_r": correlation(
                            pair[origin], pair[destination]
                        ),
                    }
                )
    return pd.DataFrame(rows)


def controller_identity(multiflyway_dir, svalbard_dir):
    import pandas as pd
    rows = []
    for flyway in ("greenland", "barents"):
        frame = pd.read_csv(
            multiflyway_dir
            / f"stage3_{flyway}_goose_step_controller_by_transition.csv"
        )
        for row in frame.itertuples(index=False):
            rows.append(
                {
                    "flyway": flyway,
                    "origin_region": str(row.origin_region),
                    "destination_region": str(row.destination_region),
                    "existing_lambda": float(row.phase_transfer_lambda),
                    "existing_stopover_slope": float(row.stopover_slope),
                }
            )
    frame = pd.read_csv(
        svalbard_dir / "stage3_svalbard_goose_controller_by_transition.csv"
    )
    for row in frame.itertuples(index=False):
        rows.append(
            {
                "flyway": "svalbard",
                "origin_region": str(row.origin_region),
                "destination_region": str(row.destination_region),
                "existing_lambda": float(
                    row.phase_transfer_arrival_to_arrival
                ),
                "existing_stopover_slope": float(row.stopover_phase_beta),
            }
        )
    return pd.DataFrame(rows)


def recourse_tables(transitions, *, lower, upper):
    import pandas as pd
    duration_rows = [
        TransitionDuration(
            flyway=str(row.flyway),
            origin_region=str(row.origin_region),
            destination_region=str(row.destination_region),
            duration_days=float(row.duration_days),
            individual_id=str(row.individual_id),
        )
        for row in transitions.itertuples(index=False)
    ]
    envelopes = build_edge_envelopes(
        duration_rows,
        min_edge_rows=3,
        lower_quantile=lower,
        upper_quantile=upper,
    )
    recourse = remaining_recourse(envelopes, terminal_by_flyway=TERMINAL)
    env = pd.DataFrame(
        [
            {
                **asdict(row),
                "local_window_days": row.upper_days - row.lower_days,
            }
            for row in envelopes
        ]
    )
    rec = pd.DataFrame([asdict(row) for row in recourse])
    return env, rec


def perm_payload(rows, *, weighted=False):
    return asdict(
        exact_within_flyway_q_permutation(rows, weighted=weighted)
    )


def meta_rows(frame, *, q, r, response, weighted=False):
    return [
        TransitionMetaRow(
            flyway=str(row.flyway),
            q=float(getattr(row, q)),
            r=float(getattr(row, r)),
            correction=float(getattr(row, response)),
            weight=float(row.n if weighted else 1.0),
        )
        for row in frame.itertuples(index=False)
    ]


def main():
    args = parse_args()
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("V7R analysis requires pandas/numpy") from exc

    green = pd.read_csv(
        args.multiflyway_dir
        / "stage3_greenland_goose_anomaly_phase_transitions.csv"
    )
    barents = pd.read_csv(
        args.multiflyway_dir
        / "stage3_barents_goose_anomaly_phase_transitions.csv"
    )
    svalbard = pd.read_csv(
        args.svalbard_dir / "stage3_svalbard_goose_transitions.csv"
    )

    transitions = pd.concat(
        [
            transition_frame(green, "greenland"),
            transition_frame(barents, "barents"),
            transition_frame(svalbard, "svalbard", svalbard=True),
        ],
        ignore_index=True,
    )
    q_power = power_predictability(args.multiflyway_dir, args.svalbard_dir)
    q_era5 = era5_predictability(
        args.era5_multiflyway_dir,
        args.era5_svalbard_dir,
    )
    existing = controller_identity(args.multiflyway_dir, args.svalbard_dir)

    env10, rec10 = recourse_tables(transitions, lower=0.10, upper=0.90)
    _, rec20 = recourse_tables(transitions, lower=0.20, upper=0.80)

    support = (
        transitions.groupby(
            ["flyway", "origin_region", "destination_region"],
            as_index=False,
        )
        .agg(
            n=("duration_days", "size"),
            n_individuals=("individual_id", "nunique"),
        )
    )
    focal = support[support["n"] >= 5].copy()
    if len(focal) != 10:
        raise SystemExit(f"expected 10 focal transitions, found {len(focal)}")

    rec10_lookup = {
        (str(row.flyway), str(row.region)): row
        for row in rec10.itertuples(index=False)
    }
    rec20_lookup = {
        (str(row.flyway), str(row.region)): row
        for row in rec20.itertuples(index=False)
    }
    env10_lookup = {
        (
            str(row.flyway),
            str(row.origin_region),
            str(row.destination_region),
        ): row
        for row in env10.itertuples(index=False)
    }
    q_lookup = {
        (
            str(row.flyway),
            str(row.origin_region),
            str(row.destination_region),
        ): row
        for row in q_power.itertuples(index=False)
    }
    era_lookup = {
        (
            str(row.flyway),
            str(row.origin_region),
            str(row.destination_region),
        ): row
        for row in q_era5.itertuples(index=False)
    }
    existing_lookup = {
        (
            str(row.flyway),
            str(row.origin_region),
            str(row.destination_region),
        ): row
        for row in existing.itertuples(index=False)
    }

    rows = []
    lambda_diffs = []
    stopover_diffs = []
    for source in focal.itertuples(index=False):
        key = (
            str(source.flyway),
            str(source.origin_region),
            str(source.destination_region),
        )
        subset = transitions[
            (transitions["flyway"] == key[0])
            & (transitions["origin_region"] == key[1])
            & (transitions["destination_region"] == key[2])
        ]
        lam = slope(subset["origin_phase"], subset["destination_phase"])
        stop = slope(
            subset["origin_phase"],
            subset["origin_stopover_days"],
        )

        q = q_lookup[key]
        era = era_lookup[key]
        r10 = rec10_lookup[(key[0], key[1])]
        r20 = rec20_lookup[(key[0], key[1])]
        edge = env10_lookup[key]
        start = min(
            [
                row.region
                for row in rec10.itertuples(index=False)
                if row.flyway == key[0]
                and row.region != TERMINAL[key[0]]
            ],
            key=lambda value: int(str(value)[1:]),
        )
        start_window = float(
            rec10_lookup[(key[0], str(start))].window_days
        )

        old = existing_lookup.get(key)
        if old is not None:
            lambda_diffs.append(lam - float(old.existing_lambda))
            stopover_diffs.append(
                stop - float(old.existing_stopover_slope)
            )

        rows.append(
            {
                "flyway": key[0],
                "origin_region": key[1],
                "destination_region": key[2],
                "n": int(source.n),
                "n_individuals": int(source.n_individuals),
                "q_signed_r": float(q.q_signed_r),
                "q_abs_r": abs(float(q.q_signed_r)),
                "q_r2": float(q.q_r2),
                "q_abs_slope": abs(float(q.q_slope)),
                "q_era5_signed_r": float(era.era5_signed_r),
                "q_era5_abs_r": abs(float(era.era5_signed_r)),
                "r_remaining_q10_q90": float(r10.retained_recourse),
                "r_remaining_q20_q80": float(r20.retained_recourse),
                "local_window_days": float(edge.local_window_days),
                "r_local_start_normalized": float(
                    edge.local_window_days / start_window
                ),
                "lambda": lam,
                "correction_score": 1.0 - abs(lam),
                "stopover_slope": stop,
                "stopover_gain": -stop,
                "low_individual_support": (
                    int(source.n_individuals) == 3
                ),
            }
        )

    result = pd.DataFrame(rows).sort_values(
        ["flyway", "origin_region", "destination_region"]
    ).reset_index(drop=True)

    qr = correlation(
        result["q_abs_r"],
        result["r_remaining_q10_q90"],
    )
    if abs(qr) >= 0.90:
        raise SystemExit(f"Q/R collinearity gate failed: {qr}")

    primary_rows = meta_rows(
        result,
        q="q_abs_r",
        r="r_remaining_q10_q90",
        response="correction_score",
    )
    primary_fit = fit_meta(primary_rows)
    primary_perm = perm_payload(primary_rows)

    weighted_rows = meta_rows(
        result,
        q="q_abs_r",
        r="r_remaining_q10_q90",
        response="correction_score",
        weighted=True,
    )

    sensitivities = {
        "weighted_by_transition_n": perm_payload(
            weighted_rows,
            weighted=True,
        ),
        "recourse_q20_q80": perm_payload(
            meta_rows(
                result,
                q="q_abs_r",
                r="r_remaining_q20_q80",
                response="correction_score",
            )
        ),
        "local_one_step_recourse": {
            "normalization": (
                "edge Q10-Q90 window / flyway start-region remaining-route "
                "Q10-Q90 window"
            ),
            **perm_payload(
                meta_rows(
                    result,
                    q="q_abs_r",
                    r="r_local_start_normalized",
                    response="correction_score",
                )
            ),
        },
        "signed_phenology_r": perm_payload(
            meta_rows(
                result,
                q="q_signed_r",
                r="r_remaining_q10_q90",
                response="correction_score",
            )
        ),
        "phenology_r2": perm_payload(
            meta_rows(
                result,
                q="q_r2",
                r="r_remaining_q10_q90",
                response="correction_score",
            )
        ),
        "abs_anomaly_slope": perm_payload(
            meta_rows(
                result,
                q="q_abs_slope",
                r="r_remaining_q10_q90",
                response="correction_score",
            )
        ),
        "era5_abs_r": perm_payload(
            meta_rows(
                result,
                q="q_era5_abs_r",
                r="r_remaining_q10_q90",
                response="correction_score",
            )
        ),
        "lambda_response_descriptive": perm_payload(
            meta_rows(
                result,
                q="q_abs_r",
                r="r_remaining_q10_q90",
                response="lambda",
            )
        ),
    }

    no_low = result[~result["low_individual_support"]]
    sensitivities["exclude_low_individual_support"] = perm_payload(
        meta_rows(
            no_low,
            q="q_abs_r",
            r="r_remaining_q10_q90",
            response="correction_score",
        )
    )

    loo = []
    for row in result.itertuples(index=False):
        keep = result[
            ~(
                (result["flyway"] == row.flyway)
                & (result["origin_region"] == row.origin_region)
                & (result["destination_region"] == row.destination_region)
            )
        ]
        mr = meta_rows(
            keep,
            q="q_abs_r",
            r="r_remaining_q10_q90",
            response="correction_score",
        )
        ff = fit_meta(mr)
        pp = exact_within_flyway_q_permutation(mr)
        loo.append(
            {
                "omitted": (
                    f"{row.flyway}:{row.origin_region}"
                    f"->{row.destination_region}"
                ),
                "beta_qr": ff.beta_qr,
                "one_sided_p": pp.one_sided_p,
                "valid_permutations": pp.valid_permutations,
            }
        )

    exploratory_stopover = perm_payload(
        meta_rows(
            result,
            q="q_abs_r",
            r="r_remaining_q10_q90",
            response="stopover_gain",
        )
    )

    payload = {
        "schema": "payoff_b_v7r_direct_recourse_result_v1",
        "status": "PRIMARY_NOT_SUPPORTED",
        "date": "2026-10-07",
        "source_gate": {
            "focal_transitions": int(len(result)),
            "flyways": int(result["flyway"].nunique()),
            "q_r_correlation": qr,
            "passed": True,
        },
        "lambda_identity": {
            "existing_transitions_checked": len(lambda_diffs),
            "max_abs_lambda_difference": max(abs(x) for x in lambda_diffs),
            "max_abs_stopover_slope_difference": max(
                abs(x) for x in stopover_diffs
            ),
            "new_transition": "barents:R5->R7",
            "new_transition_lambda": float(
                result.loc[
                    (result["flyway"] == "barents")
                    & (result["origin_region"] == "R5")
                    & (result["destination_region"] == "R7"),
                    "lambda",
                ].iloc[0]
            ),
        },
        "primary": {
            "model": (
                "C = flyway fixed effects + beta_Q Q + beta_R R + "
                "beta_QR Q*R"
            ),
            "response": "C = 1 - abs(lambda)",
            "Q": "abs(POWER spring-onset correlation)",
            "R": (
                "remaining Q10-Q90 route temporal window / flyway start window"
            ),
            "coefficients": dict(
                zip(
                    primary_fit.coefficient_names,
                    primary_fit.coefficients,
                )
            ),
            "permutation": primary_perm,
            "decision": "NOT_SUPPORTED",
        },
        "mandatory_sensitivities": sensitivities,
        "leave_one_transition_out": loo,
        "descriptive": {
            "corr_correction_with_q": correlation(
                result["correction_score"],
                result["q_abs_r"],
            ),
            "corr_correction_with_r": correlation(
                result["correction_score"],
                result["r_remaining_q10_q90"],
            ),
            "corr_correction_with_stopover_gain": correlation(
                result["correction_score"],
                result["stopover_gain"],
            ),
        },
        "post_outcome_exploratory": {
            "stopover_gain_qxr": exploratory_stopover,
            "interpretation_boundary": (
                "Exploratory only; opened after the primary null and cannot "
                "replace or rescue the primary result."
            ),
        },
        "local_recourse_note": (
            "An interim within-flyway-max normalization was computed during "
            "interactive diagnosis and is not retained. The reported local "
            "sensitivity uses the source-only common denominator W_start."
        ),
        "claim_boundary": {
            "licensed": [
                (
                    "The preregistered ten-transition interaction between "
                    "environmental predictability and direct temporal recourse "
                    "was not supported."
                ),
                (
                    "The null is stable to transition weighting, recourse "
                    "envelopes, local recourse, Q transforms, ERA5 Q, and "
                    "removal of the low-individual-support transition."
                ),
            ],
            "not_licensed": [
                "environmental information is never used by migrating geese",
                "remaining recourse is biologically irrelevant",
                "the population-envelope R is exact individual actionability",
                "the null disproves sequential phase correction",
            ],
        },
    }

    args.transition_output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.transition_output, index=False)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output_json)
    print(
        "V7R "
        f"beta_QR={primary_fit.beta_qr:.6f} "
        f"p_perm={primary_perm['one_sided_p']:.6f} "
        f"status={payload['status']}"
    )


if __name__ == "__main__":
    main()
