#!/usr/bin/env python3
"""Calendar-aligned original Greenland white-fronted goose exposure nulls.

Fixed post-open observational diagnostics; no source bird IDs or rows emitted,
no information-deadline causation claim, no biological effect re-estimated.
The date+duration exact-match design is intentionally FAIL-CLOSED.
"""
from __future__ import annotations

import argparse
import json
import hashlib
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.payoff_b_gwfg_lagged_weather_to_feeding import (
    original_source_digest,
    make_bird_years,
    _predictive_group_cv,
    PREDICTION_BASE,
    PREDICTION_WITH_EARLY_FREEZE,
)
from scripts.payoff_b_gwfg_within_year_freeze_permutation import (
    updated_ridge_mse,
)

ITERATIONS = 99
MIN_ELIGIBLE = 40
MIN_GROUPS = 8
MIN_YEARS = 3
ORIGINAL_GRAIN = (107, 49, 5)
SPECS = (
    ("same_year_exact_start_day", 20261119),
    ("same_year_7day_bin_and_3day_duration_band", 20261120),
    ("same_year_exact_start_and_exact_duration", None),
)
EXPECTED_SUPPORT = {
    "same_year_exact_start_day": (48, 14, 5),
    "same_year_7day_bin_and_3day_duration_band": (52, 11, 5),
    "same_year_exact_start_and_exact_duration": (17, 7, 4),
}


def block_key(row, kind: str) -> tuple[int, ...]:
    year = int(row.year_index)
    start = float(row.first_day3)
    end = float(row.first_day4)
    if not (start.is_integer() and end.is_integer() and end > start):
        raise ValueError("Original first_day stages must be increasing integer DOYs")
    start, duration = int(start), int(end - start)
    if kind == "same_year_exact_start_day":
        return year, start
    if kind == "same_year_7day_bin_and_3day_duration_band":
        return year, (start - 1) // 7, (duration - 1) // 3
    if kind == "same_year_exact_start_and_exact_duration":
        return year, start, duration
    raise ValueError("Unregistered temporal matching design")


def eligible_blocks(x: pd.DataFrame, kind: str) -> dict[tuple[int, ...], list[int]]:
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for i, row in x.reset_index(drop=True).iterrows():
        groups[block_key(row, kind)].append(i)
    eligible: dict[tuple[int, ...], list[int]] = {}
    for key, indexes in groups.items():
        vals = x.iloc[indexes].freeze3_10pp.to_numpy(float)
        if len(indexes) >= 2 and len(np.unique(vals)) >= 2:
            eligible[key] = indexes
    return eligible


def admission(x: pd.DataFrame, kind: str) -> dict:
    blocks = eligible_blocks(x, kind)
    n = sum(len(v) for v in blocks.values())
    years = len({key[0] for key in blocks})
    summary = {
        "design": kind,
        "candidate_swappable_bird_year_rows": n,
        "n_eligible_nonconstant_groups": len(blocks),
        "n_original_years_with_nonconstant_groups": years,
        "all_other_rows_frozen_in_place": len(x) - n,
        "minimum_eligible_rows_frozen": MIN_ELIGIBLE,
        "minimum_blocks_frozen": MIN_GROUPS,
        "minimum_independent_years_frozen": MIN_YEARS,
        "source_original_bird_years": len(x),
        "source_original_birds": int(x.bird_id.nunique()),
        "source_original_calendar_years": int(x.year_index.nunique()),
    }
    if kind not in EXPECTED_SUPPORT:
        raise ValueError("Not a frozen temporal matching design")
    if (n, len(blocks), years) != EXPECTED_SUPPORT[kind]:
        raise ValueError(f"Original source matching support changed for {kind}")
    passed = n >= MIN_ELIGIBLE and len(blocks) >= MIN_GROUPS and years >= MIN_YEARS
    summary["admission"] = "PASS_POST_OPEN_SUPPORT_CHECK" if passed else "FAIL_NOT_ESTIMABLE_NO_SHUFFLES"
    summary["effect_estimated"] = False
    return summary


def shuffle_temporally_matched(
    x: pd.DataFrame, kind: str, rng: np.random.Generator
) -> pd.DataFrame:
    original = x.reset_index(drop=True)
    out = original.copy()
    blocks = eligible_blocks(original, kind)
    for group in blocks.values():
        raw = original.iloc[group].freeze3_10pp.to_numpy(float)
        moved = rng.permutation(raw)
        out.loc[group, "freeze3_10pp"] = moved
        after = out.loc[group, "freeze3_10pp"].to_numpy(float)
        if not np.array_equal(np.sort(raw), np.sort(after)):
            raise ValueError("Temporal-block freeze marginal distributions changed")
    for col in original.columns:
        if col != "freeze3_10pp" and not original[col].equals(out[col]):
            raise ValueError("Accidental change to source weather date, bird or outcome")
    return out


def run(x: pd.DataFrame) -> dict:
    if (len(x), x.bird_id.nunique(), x.year_index.nunique()) != ORIGINAL_GRAIN:
        raise ValueError("Original published bird/year scope changed")
    x = x.reset_index(drop=True)
    # Reproduce exact earlier source-specified ridge gains before ANY shuffling.
    base = {}
    for grouping in ("bird_id", "year_index"):
        ref = _predictive_group_cv(
            x, PREDICTION_BASE, PREDICTION_WITH_EARLY_FREEZE, grouping
        )
        independent_aug = updated_ridge_mse(x, grouping)
        if abs(independent_aug - ref["augmented_loss"]) > 1e-11:
            raise ValueError("Previous source prediction cannot be reproduced")
        base[grouping] = {
            "original_baseline_MSE": ref["baseline_loss"],
            "original_augmented_MSE": ref["augmented_loss"],
            "original_improvement_MSE": ref["baseline_loss"] - ref["augmented_loss"],
            "n_blocked_holdout_folds": ref["n_holdout_folds"],
        }
    results = {}
    for kind, seed in SPECS:
        support = admission(x, kind)
        if support["admission"].startswith("FAIL"):
            results[kind] = {
                "support": support,
                "status": "NOT_ESTIMABLE_TOO_FEW_MATCHED_ORIGINAL_BIRD_YEARS",
                "permutation_forecast_was_executed": False,
                "original_bird_level_feedback_identified": False,
            }
            continue
        assert seed is not None
        rng = np.random.default_rng(seed)
        gains = {name: [] for name in base}
        # Count only assignments, not raw bird data. All source year/day/length
        # matching rules and alpha=1 ridge models are held fixed.
        changed_counts = []
        for _ in range(ITERATIONS):
            perm = shuffle_temporally_matched(x, kind, rng)
            changed_counts.append(int(np.sum(
                perm.freeze3_10pp.to_numpy() != x.freeze3_10pp.to_numpy()
            )))
            for grouping in base:
                sse = updated_ridge_mse(perm, grouping)
                gains[grouping].append(base[grouping]["original_baseline_MSE"] - sse)
        output = {}
        for grouping, vals in gains.items():
            vals = np.asarray(vals, dtype=float)
            observed = base[grouping]["original_improvement_MSE"]
            count = int(np.sum(vals >= observed))
            output[grouping] = {
                **base[grouping],
                "null_gain_median": float(np.median(vals)),
                "null_gain_mean": float(np.mean(vals)),
                "null_gain_quantiles_05_95": list(map(float, np.quantile(vals, [.05, .95]))),
                "n_null_assignments_ge_original": count,
                "n_shuffles": ITERATIONS,
                "empirical_post_open_upper_tail_fraction_NOT_CAUSAL_P_VALUE": (
                    count + 1
                ) / (ITERATIONS + 1),
                "n_shuffles_with_positive_gain": int(np.sum(vals >= 0)),
            }
        results[kind] = {
            "support": support,
            "status": "EXPLORATORY_MATCHED_OBSERVATIONAL_NULL_COMPLETE",
            "random_generator_seed": seed,
            "n_shuffles": ITERATIONS,
            "changed_weather_row_count_median": float(np.median(changed_counts)),
            "changed_weather_row_count_max": max(changed_counts),
            "source_groupwise_calendar_and_duration_bins_preserved": True,
            "holdout_gains": output,
            "bird_exposure_cue_or_causal_adaptation_fitted": False,
        }
    if results["same_year_exact_start_and_exact_duration"]["permutation_forecast_was_executed"]:
        raise ValueError("Unlicensed strict-match weather null was executed")
    return {
        "result_id": "PAYOFF_B_GWFG_CALENDAR_MATCHED_WEATHER_NULLS_20261119",
        "source": "Schindler et al 2024 Proc R Soc B original 2024 GitHub source",
        "analysis": "POST_OPEN_SOURCE_WEATHER_ASSIGNMENT_DIAGNOSTICS_NOT_CAUSAL_INFERENCE",
        "frozen_document": "docs/PAYOFF_B_GWFG_CALENDAR_MATCHED_PERMUTATION_FREEZE_20261119.md",
        "bird_years": len(x),
        "birds": int(x.bird_id.nunique()),
        "original_years": [2018, 2019, 2020, 2021, 2022],
        "original_frozen_OLS_beta": -0.0013725255396581735,
        "original_frozen_OLS_CI95": [-0.013697070348722811, 0.010952019269406464],
        "original_frozen_OLS_p": 0.8237739635307635,
        "two_non_nested_supported_temporal_nulls": results,
        "claims": {
            "original_paper_prior_art": True,
            "source_effect_new_independent_replication": False,
            "date_and_duration_alignment_fully_controlled": False,
            "original_individual_habitat_held_fixed_by_permutation": False,
            "source_weather_exposure_randomized_in_nature": False,
            "individual_use_of_future_information_identified": False,
            "observed_downstream_actionability_budget": False,
            "fitness_mediation_or_information_deadline_identified": False,
            "frozen_V7_goose_qxU": "NOT_ESTIMABLE",
            "eBird_used": False,
            "raw_bird_ids_exported": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    opts = parser.parse_args()
    source = original_source_digest(opts.source)
    bird_years = make_bird_years(pd.read_csv(opts.source), strict=True)
    result = run(bird_years)
    result["original_source_provenance"] = source
    opts.output.parent.mkdir(parents=True, exist_ok=True)
    opts.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "result_id": result["result_id"],
        "calendar_matched_results": {
            key: {
                "support": value["support"],
                "status": value["status"],
                "heldout_gains": value.get("holdout_gains"),
            }
            for key, value in result["two_non_nested_supported_temporal_nulls"].items()
        },
        "causal_information_use_mechanism": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
