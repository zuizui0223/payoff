#!/usr/bin/env python3
"""Audit shared physical-weather dependence in the full PAYOFF-B GPS risk set.

Post-outcome exploratory source robustness; NOT a preregistered test of
environmental cue uptake, active migration recourse, or evolutionary fitness.

Resample complete published 0.5-degree grid × year × month weather strata,
coarser 2-degree × year × month blocks, and whole year-month weather episodes,
rather than repeatedly treating GPS days of different birds in a shared
meteorological field as independent. Fixed 5,509 MD5-verified source at-risk
opportunities, original NASA daily predecision weather day -1 vs days -2..-8.

All original animal identities, times, GPS/weather-cell coordinates and
event-level data stay in ephemeral runner memory. Output is aggregate only.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import (
    SYSTEMS, daily_source_positions,
)
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.run_payoff_b_full_riskday_daily_weather import (
    EXPECTED, WORKERS, batch_key, download_batch, event_prior_weather,
    grid_cell,
)
from scripts.run_payoff_b_stork_stage_handoff_pilot import percentile
from scripts.audit_payoff_b_fullrisk_cluster_robustness import (
    weighted_gridmonth_contrast,
)

VARS = (
    "T2M_anomaly", "WS10M_anomaly", "V10M_anomaly",
    "ALLSKY_SFC_SW_DWN_anomaly",
)
CASE = "NORTHWARD_CANDIDATE"
STAY = "STAYED_TWO_DAYS"
BOOTSTRAP_DRAWS = 3000
RANDOM_SEED = 20261022
MIN_WEATHER_BLOCKS = 10
MIN_PAIRED_STRATA = 10
MIN_PAIRED_ANIMALS = 10
MAX_BATCHES_BY_ORIGINAL_SOURCE = 500
SOURCE_REFERENCE = {
    "stork": (61, 75, -0.5143160582010581, -17.098786065759636),
    "white_fronted_goose": (84, 89, 1.0368454527682056, 2.270251703009847),
    "curlew": (31, 51, 0.339625486796959, -0.9746087863952799),
}


def complete_matched_strata(observations, within_identity=False):
    """Construct paired *same-weather* contrasts, never event-level pseudo-N.

    observations: (private_original_ID, date, original_weather_cell,
                   source_move_or_stay_label, predecision_weather_mapping)
    With within_identity=True, require a case and stay from the same
    animal in a single fine weather cell and calendar year-month.
    """
    grouped = defaultdict(
        lambda: {
            CASE: {"n": 0, "sum": Counter(), "identities": set()},
            STAY: {"n": 0, "sum": Counter(), "identities": set()},
        }
    )
    for animal, day, cell, label, met in observations:
        if label not in (CASE, STAY):
            continue
        fine = (day.year, day.month, cell)
        key = (animal,) + fine if within_identity else fine
        record = grouped[key][label]
        record["n"] += 1
        record["identities"].add(animal)
        for v in VARS:
            record["sum"][v] += met[v]
    strata = []
    unique_animals = set()
    case_days = 0
    for key in sorted(grouped):
        case, stay = grouped[key][CASE], grouped[key][STAY]
        if not case["n"] or not stay["n"]:
            continue
        fine = key[1:] if within_identity else key
        case_days += case["n"]
        unique_animals.update(case["identities"])
        strata.append({
            # Private keys stay in memory and are never serialised.
            "fine": fine,
            "n_cases": case["n"],
            "n_stays": stay["n"],
            "difference": {
                v: case["sum"][v]/case["n"] -
                   stay["sum"][v]/stay["n"]
                for v in VARS
            },
        })
    return strata, {
        "matched_strata_count": len(strata),
        "case_risk_days_in_matched_strata": case_days,
        "distinct_case_animals_with_instrumental_overlap": len(unique_animals),
        "private_grid_ids_or_individual_ids_exported": False,
    }


def estimate_from_strata(strata, multiplicities=None):
    """Aggregate fine stratum contrasts weighted by original case-days."""
    sums = Counter()
    total = 0
    for i, stratum in enumerate(strata):
        weight = (
            multiplicities[i] if multiplicities is not None
            else 1
        )
        effective_cases = weight * stratum["n_cases"]
        if not effective_cases:
            continue
        total += effective_cases
        for var in VARS:
            sums[var] += effective_cases * stratum["difference"][var]
    return {
        "n_case_days_as_weights": total,
        "case_weighted_difference": {
            var: sums[var]/total if total else None for var in VARS
        },
    }


def _block_id(stratum, scale):
    """Do not expose the exact weather block key in any returned result."""
    year, month, (lat, lon) = stratum["fine"]
    if scale == "grid_half_degree":
        return year, month, lat, lon
    if scale == "weather_block_2_degree":
        return year, month, math.floor(lat/2), math.floor(lon/2)
    if scale == "weather_episode_year_month":
        return year, month
    raise ValueError("Unknown space/time weather block definition")


def block_sensitivity(strata, scale, *, draws=BOOTSTRAP_DRAWS,
                      seed=RANDOM_SEED):
    """A block is resampled once, with ALL bird-days in its fine strata."""
    index = defaultdict(list)
    for i, stratum in enumerate(strata):
        index[_block_id(stratum, scale)].append(i)
    # Ordered keys ensure data traversal does not alter stochastic receipt.
    blocks = [index[k] for k in sorted(index)]
    one_block = []
    for members in blocks:
        case_n = sum(strata[i]["n_cases"] for i in members)
        sums = {
            var: sum(
                strata[i]["n_cases"] * strata[i]["difference"][var]
                for i in members
            ) for var in VARS
        }
        one_block.append((case_n, sums))
    n_blocks = len(one_block)
    all_case_weight = sum(x[0] for x in one_block)
    base = estimate_from_strata(strata)
    effective_blocks = (
        (all_case_weight ** 2) / sum(x[0]**2 for x in one_block)
        if one_block and all_case_weight else None
    )
    out = {
        "weather_resampling_unit": scale,
        "n_distinct_weather_blocks": n_blocks,
        "weather_block_effective_case_weight_n": effective_blocks,
        "largest_single_block_case_weight_fraction": (
            max(x[0] for x in one_block)/all_case_weight
            if one_block and all_case_weight else None
        ),
        "case_weight_total": all_case_weight,
        "original_case_weighted_contrast": base["case_weighted_difference"],
        "bootstrap_requested": draws,
        "sample_validity": "EXPLORATORY_NOT_CONFIRMATORY",
        "resampling_accounts_for_between_block_weather_dependence": False,
        "resampling_keeps_birds_within_same_block_together": True,
        "source_weather_blocks_independent_in_nature": False,
        "private_block_locations_exported": False,
    }
    if n_blocks < MIN_WEATHER_BLOCKS:
        return {
            **out, "status": "NOT_ESTIMABLE_TOO_FEW_WEATHER_BLOCKS",
            "bootstrap_completed": 0,
            "bootstrap_interval_95pct_descriptive": None,
        }

    jackknife = defaultdict(list)
    for case_n, _ in one_block:
        if all_case_weight - case_n <= 0:
            raise ValueError("Weather block uniquely carries all source cases")
    for drop, (excluded_weight, excluded_sums) in enumerate(one_block):
        retained = all_case_weight - excluded_weight
        for var in VARS:
            overall_num = base["case_weighted_difference"][var] * all_case_weight
            jackknife[var].append(
                (overall_num-excluded_sums[var])/retained
            )

    rng = random.Random(seed + len(scale))
    boot = defaultdict(list)
    draws_valid = 0
    for _ in range(draws):
        indices = rng.choices(range(n_blocks), k=n_blocks)
        denominator = sum(one_block[i][0] for i in indices)
        if denominator == 0:
            continue
        draws_valid += 1
        for var in VARS:
            boot[var].append(
                sum(one_block[i][1][var] for i in indices)/denominator
            )
    min_completed = math.ceil(draws*0.95)
    if draws_valid < min_completed:
        return {
            **out, "status": "NOT_ESTIMABLE_BLOCK_RESAMPLE_FAILURE",
            "bootstrap_completed": draws_valid,
            "bootstrap_interval_95pct_descriptive": None,
        }

    return {
        **out, "status": "DESCRIPTIVE_BLOCK_SENSITIVITY_ESTIMABLE",
        "bootstrap_completed": draws_valid,
        "bootstrap_interval_95pct_descriptive": {
            var: [percentile(boot[var], .025), percentile(boot[var], .975)]
            for var in VARS
        },
        "leave_one_weather_block_out_range": {
            var: [min(jackknife[var]), max(jackknife[var])]
            for var in VARS
        },
        "leave_one_weather_block_sign_consistent": {
            var: all(v>0 for v in jackknife[var]) or
                 all(v<0 for v in jackknife[var])
            for var in VARS
        },
    }


def analyse_original(observations):
    standard, original_counts = complete_matched_strata(observations)
    individual, personal_counts = complete_matched_strata(
        observations, within_identity=True
    )
    old = weighted_gridmonth_contrast(observations)
    estimate = estimate_from_strata(standard)
    assert (
        original_counts["matched_strata_count"] ==
        old["n_gridmonth_strata_with_both_labels"]
    ), "source fine-grid strata do not match prior primary analysis"
    assert (
        estimate["n_case_days_as_weights"] ==
        old["n_original_case_day_weights_in_overlap"]
    ), "source fine-grid case weights do not match primary analysis"
    for var in VARS:
        if abs(
            estimate["case_weighted_difference"][var] -
            old["source_case_weighted_contrasts"][var]
        ) > 1e-8:
            raise ValueError("Weather block source estimator disagrees with original")

    base = {
        "original_fine_strata_counts": original_counts,
        "original_fine_strata_effect": estimate,
        "within_same_bird_gridmonth_strata_counts": personal_counts,
        "within_same_bird_gridmonth_effect": (
            estimate_from_strata(individual)["case_weighted_difference"]
            if personal_counts["matched_strata_count"] >= MIN_PAIRED_STRATA
            and personal_counts["distinct_case_animals_with_instrumental_overlap"]
            >= MIN_PAIRED_ANIMALS
            else None
        ),
        "within_same_bird_not_estimated_reason": (
            None if (
                personal_counts["matched_strata_count"]>=MIN_PAIRED_STRATA
                and personal_counts["distinct_case_animals_with_instrumental_overlap"]
                >=MIN_PAIRED_ANIMALS
            ) else "INSUFFICIENT_INDEPENDENT_IDENTITIES_OR_MATCHED_STRATA"
        ),
        "source_contrasts_within_individual_can_have_seasonal_trend": True,
        "bootstrap_weather_blocks": {
            scale: block_sensitivity(standard, scale)
            for scale in (
                "grid_half_degree",
                "weather_block_2_degree",
                "weather_episode_year_month",
            )
        },
        "input_observation_level":"repeated source riskday per original animal",
        "no_signed_route_control_or_fitness_measured":True,
        "exact_weather_grid_and_animal_source_keys_exported":False,
    }
    return base


def run_system(system, fetch=download_batch):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "pinned-public-gps.csv"
        doi, taxon, sensor, checksum = origin_source(system, path)
        groups, source_quality, idcol = daily_source_positions(path, taxon)
        risk, source_counts, _, _ = collect(groups)
        labels = (
            "all_at_risk_stationary_days", CASE, STAY,
            "OTHER_MOVEMENT", "CENSORED",
        )
        if (
            tuple(source_counts[k] for k in labels)
            != EXPECTED[system][:5]
        ):
            raise ValueError("Original 5,509-source riskday panel changed")
        requests = sorted({
            batch_key(day,site) for group,day,site,label in risk
        })
        if len(requests) != EXPECTED[system][5] or len(requests)>MAX_BATCHES_BY_ORIGINAL_SOURCE:
            raise ValueError("Original protected daily weather batch count changed")
        complete = {}
        failure = Counter()
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            jobs = {pool.submit(fetch, k):k for k in requests}
            for future in as_completed(jobs):
                key = jobs[future]
                try:
                    complete[key] = future.result()
                except Exception as exc:
                    failure[type(exc).__name__] += 1
        all_fixes = Counter()
        private = []
        for (tax, animal, year), day, site, label in risk:
            source = complete.get(batch_key(day,site))
            if source is None:
                all_fixes[label+"_SOURCE_WEATHER_MISSING"] += 1
                continue
            predictor = event_prior_weather(source,day)
            if predictor is None:
                all_fixes[label+"_PRIOR_DAY_WEATHER_MISSING"] += 1
                continue
            all_fixes[label] += 1
            if label in (CASE,STAY):
                private.append((animal,day,grid_cell(site),label,predictor))
        if any(all_fixes[k] != source_counts[k] for k in labels):
            return {
                "status":"NOT_ESTIMABLE_ORIGINAL_WEATHER_COMPLETENESS_CHANGED",
                "source_batch_count":len(requests),
                "source_request_errors":dict(sorted(failure.items())),
                "valid_riskday_labels":dict(sorted(all_fixes.items())),
            }

        data = analyse_original(private)
        should_be = SOURCE_REFERENCE[system]
        measured = data["original_fine_strata_counts"]
        differences = data["original_fine_strata_effect"]["case_weighted_difference"]
        if measured["matched_strata_count"] != should_be[0]:
            raise ValueError("Weather fine-strata count not identical to published source receipt")
        if measured["case_risk_days_in_matched_strata"] != should_be[1]:
            raise ValueError("Matched fine-strata source case count disagrees with prior")
        if abs(differences["T2M_anomaly"]-should_be[2])>1e-7:
            raise ValueError("Original temperature anomaly changed")
        if abs(differences["ALLSKY_SFC_SW_DWN_anomaly"]-should_be[3])>1e-7:
            raise ValueError("Original solar anomaly changed")

        return {
            "status":"WEATHER_BLOCK_DEPENDENCE_SOURCE_SENSITIVITY_COMPLETE",
            "source_doi":doi,"taxon":taxon,"sensor":sensor,
            "GPS_checksum_verified":checksum,
            "source_3day_riskday_count":len(risk),
            "source_valid_case_and_stay_day_count":len(private),
            "source_daily_weather_batch_request_count":len(requests),
            "source_daily_weather_batch_failure_types":dict(sorted(failure.items())),
            "source_weather_valid_counts":dict(sorted(all_fixes.items())),
            "analyses":data,
            "new_confirmatory_ecological_claim":False,
            "weather_shared_correlations_beyond_each_block_unresolved":True,
            "no_animal_ID_or_weather_cell_coordinates_in_output":True,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--system",choices=SYSTEMS,required=True)
    parser.add_argument("--out",type=Path,
                        default=Path("outputs/payoff_b_weather_block_dependence"))
    args = parser.parse_args()
    receipt = {
        "schema":"payoff_b_space_time_shared_weather_sensitivity_20261022",
        "system":args.system,
        "science_class":"POST_OUTCOME_SOURCE_ROBUSTNESS_NOT_CONFIRMATORY",
        "random_seed":RANDOM_SEED,
        "bootstrap_draws_per_weather_scale":BOOTSTRAP_DRAWS,
        "requested_weather_block_scales":[
            "grid_half_degree","weather_block_2_degree",
            "weather_episode_year_month",
        ],
    }
    try:
        receipt["result"] = run_system(args.system)
    except Exception as exc:
        receipt["result"]={
            "status":"SOURCE_OR_WEATHER_BLOCK_SENSITIVITY_FAILED",
            "error":type(exc).__name__ + ": " + str(exc)[:300],
        }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/(args.system+".json")).write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt,indent=2,ensure_ascii=False))
    if receipt["result"]["status"]!="WEATHER_BLOCK_DEPENDENCE_SOURCE_SENSITIVITY_COMPLETE":
        raise SystemExit("Weather block source sensitivity failed")


if __name__=="__main__":
    main()
