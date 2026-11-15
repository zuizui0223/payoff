"""Post-outcome influence check for the already-open 2023 biomass gate.

A leave-one-source-year-out *analysis* of LOYO-model-comparison stability.
This sensitivity is post hoc and cannot turn exploratory results into
preregistered support.
"""
import argparse
import json
from pathlib import Path

from scripts.payoff_b_2023_biomass_selection_gate import evaluate_stratum, prepare
from scripts.payoff_b_2023_real_fitness_resource_join import load


def check(panel):
    results = {}
    for (site, species), rows in sorted(panel.items()):
        original = evaluate_stratum(rows)
        if original is None:
            continue
        base = original["delta_mse_M_minus_MBI"]
        checks = []
        for dropped in sorted(row["year"] for row in rows):
            subset = [r for r in rows if r["year"] != dropped]
            metric = evaluate_stratum(subset)
            if metric is None:
                continue
            checks.append({
                "dropped_year": dropped,
                "delta_mse_M_minus_MBI": metric["delta_mse_M_minus_MBI"],
                "passes_incremental_and_intercept":
                    metric["passes_incremental_and_intercept"],
            })
        gap_outliers = [
            {"year": int(r["year"]), "mismatch_days": round(r["mismatch_days"], 3)}
            for r in sorted(rows, key=lambda x: x["year"])
            if abs(r["mismatch_days"]) > 30
        ]
        values = [r["delta_mse_M_minus_MBI"] for r in checks]
        sorted_changes = sorted(checks,
            key=lambda r: abs(r["delta_mse_M_minus_MBI"] - base), reverse=True)
        results[site + "|" + species] = {
            "years": len(rows),
            "original_delta_mse_M_minus_MBI": base,
            "n_drop_one_year_checks": len(checks),
            "fraction_drop_one_year_positive_increment":
                None if not checks else round(sum(v > 0 for v in values) / len(values), 6),
            "fraction_drop_one_year_passes_both_baselines":
                None if not checks else round(sum(x["passes_incremental_and_intercept"]
                    for x in checks) / len(checks), 6),
            "min_max_drop_one_year_increment": None if not checks else
                [round(min(values), 9), round(max(values), 9)],
            "top_three_influential_years": sorted_changes[:3],
            "unexcluded_extreme_abs_mismatch_gt_30_days": gap_outliers,
        }
    return {
        "status": "PAYOFF_B_BIOMASS_SELECTION_POSTHOC_INFLUENCE",
        "year_is_unit": True,
        "posthoc_not_confirmatory": True,
        "extreme_years_flagged_not_removed_from_primary": True,
        "data_has_daily_food_exposure": False,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    panel, ignored_exclusions = prepare(load())
    result = check(panel)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
