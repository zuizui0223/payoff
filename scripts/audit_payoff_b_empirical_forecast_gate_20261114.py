"""Source-backed aggregate audit of already opened PAYOFF-B strict GPS weather CV.

No new bird effect is fitted. Inputs are pinned, published-source aggregate
receipts from the 2026-10-22 exploratory analysis. Never pool risk-days as
independent ecological replicates or infer bird cue use from reanalysis.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE = Path("data/payoff_b_strict_weather_heldout_predictive_result_20261022.json")
EXPECTED_SCHEMA = "payoff_b_strict_stationary_source_out_of_year_weather_predictive_value_20261022"
TAXA = ("stork", "white_fronted_goose", "curlew")


def audit(source: dict) -> dict:
    if source.get("schema") != EXPECTED_SCHEMA:
        raise ValueError("Unrecognized source receipt schema")
    if source.get("result_status") != "POST_OUTCOME_EXPLORATORY_PREDICTION_NO_CONSISTENT_HELDOUT_YEAR_SKILL":
        raise ValueError("Source outcome status changed")
    if source.get("predictor_uses_future_GPS_or_weather") is not False:
        raise ValueError("Predecision chronology gate failed")
    if source.get("direct_control_capacity_or_fitness_measured") is not False:
        raise ValueError("Unexpected fitness/recourse identification change")
    if set(source.get("per_source", {})) != set(TAXA):
        raise ValueError("Unexpected source membership")

    rows = []
    total_year_days = 0
    weighted_year_gain = 0.0
    positive_year = 0
    positive_animal = 0
    for key in TAXA:
        src = source["per_source"][key]
        year = src["heldout_year"]
        animal = src["heldout_animal"]
        if year["split_scheme"] != "calendar_year" or animal["split_scheme"] != "whole_animal":
            raise ValueError("CV split semantics changed")
        if year["status"] != "OUT_OF_FOLD_OBSERVATIONAL_PREDICTION_ESTIMABLE":
            raise ValueError("Year-heldout result unavailable")
        if animal["status"] != "OUT_OF_FOLD_OBSERVATIONAL_PREDICTION_ESTIMABLE":
            raise ValueError("Animal-heldout result unavailable")
        n = year["heldout_original_source_days"]
        if n <= 0 or n > src["total_strict_source_case_or_stay_days"]:
            raise ValueError("Invalid heldout denominator")
        for split in (year, animal):
            if split["heldout_original_source_cases"] + split["heldout_original_source_stays"] != split["heldout_original_source_days"]:
                raise ValueError("Case/stay denominator mismatch")
            if abs(
                split["baseline_log_loss"]
                - split["baseline_plus_weather_log_loss"]
                - split["incremental_lag_weather_log_loss_gain"]
            ) > 1e-10:
                raise ValueError("Log-loss sign/identity mismatch")
        yg = year["incremental_lag_weather_log_loss_gain"]
        ag = animal["incremental_lag_weather_log_loss_gain"]
        total_year_days += n
        weighted_year_gain += n * yg
        positive_year += yg > 0
        positive_animal += ag > 0
        rows.append({
            "taxon": src["taxon"],
            "year_test_days": n,
            "year_test_cases": year["heldout_original_source_cases"],
            "year_logloss_gain": yg,
            "animal_logloss_gain": ag,
            "year_brier_gain": year["incremental_lag_weather_Brier_gain"],
            "year_fold_count": year["n_folds_admitted"],
            "year_folds_excluded": year["n_folds_excluded"],
            "split_sign_disagrees": (yg > 0) != (ag > 0),
        })
    if total_year_days != source["source_days_evaluated_in_heldout_year_folds"]:
        raise ValueError("Source-level year-test count does not reconcile")
    if sum(source["per_source"][k]["total_strict_source_case_or_stay_days"] for k in TAXA) != source["full_original_source_strict_case_stay_days"]:
        raise ValueError("Original strict source count does not reconcile")

    return {
        "status": "REANALYSIS_OF_ALREADY_OPENED_AGGREGATE_SOURCE_NOT_NEW_CONFIRMATION",
        "source_schema": EXPECTED_SCHEMA,
        "taxon_count": len(rows),
        "year_test_days_total": total_year_days,
        "positive_year_logloss_gain_taxa": positive_year,
        "positive_animal_logloss_gain_taxa": positive_animal,
        "split_sign_disagreement_taxa": sum(x["split_sign_disagrees"] for x in rows),
        "equal_taxon_mean_year_logloss_gain": sum(x["year_logloss_gain"] for x in rows) / len(rows),
        "day_weighted_descriptive_year_logloss_gain": weighted_year_gain / total_year_days,
        "day_weighted_value_is_not_an_independent_meta_analysis": True,
        "direct_bird_cue_perception_identified": False,
        "independent_recourse_identified": False,
        "destination_fitness_identified": False,
        "information_capacity_coordination_decomposition_identified": False,
        "species": rows,
        "next_admission": "Independent cohort with predecision cue chronology, stage-specific feasible recourse, destination timing and vital rates; no coefficient before gate",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.source.read_text(encoding="utf-8")))
    txt = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(txt, encoding="utf-8")
    else:
        print(txt, end="")


if __name__ == "__main__":
    main()
