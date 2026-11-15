"""Original-data year-level audit: peak resource magnitude x breeding mismatch.

Exploratory follow-up to PR #387, not a prospective confirmatory test.
Annual differential = within-year association between standardized first-egg
date and relative *first-brood fledging*; not lifetime selection or causal.
The annual caterpillar resource is shared by all broods, and each year is
one LOYO observation, avoiding use of individual broods as independent
resource-year replicates. Source byte checks are enforced by load().
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scripts.payoff_b_2023_filtered_descriptive_join import number
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict

OFFSET_DAYS = 33
MIN_BROODS = 10
MIN_YEARS = 12
PRIMARY_SPECIES = "Great Tit"
PRIMARY_SITES = ("Hoge Veluwe", "Oosterhout", "Vlieland")


def prepare(data):
    resources = {}
    for row in data["resource"]:
        site = str(row.get("AreaName") or "").strip()
        year = number(row.get("Year"))
        if not site or year is None:
            continue
        key = (site, int(year))
        if key in resources:
            raise ValueError("Duplicate resource site-year")
        resources[key] = row

    grouped = defaultdict(list)
    mothers = defaultdict(set)
    excluded = Counter()
    for row in data["fitness"]:
        if str(row.get("Include")).strip() not in ("1", "1.0"):
            excluded["manipulated_or_not_included"] += 1
            continue
        site = str(row.get("Area") or "").strip()
        yr = number(row.get("YearOfBreeding"))
        if yr is None or (site, int(yr)) not in resources:
            excluded["no_exact_resource_site_year"] += 1
            continue
        species = str(row.get("Species") or "").strip()
        if species not in ("Great Tit", "Blue Tit"):
            excluded["other_species"] += 1
            continue

        res = resources[(site, int(yr))]
        lay = number(row.get("LayDateApril"))
        peak = number(res.get("MidDate"))
        peak_mass = number(res.get("MaxBiom"))
        fledged = number(row.get("NumberFledged"))
        deviation = number(row.get("NumberFledgedDeviation"))
        if None in (lay, peak, peak_mass, fledged, deviation):
            excluded["missing_dates_peak_or_corrected_fledglings"] += 1
            continue
        if peak_mass < 0 or fledged < 0 or deviation < 0:
            excluded["invalid_negative_resource_or_fledglings"] += 1
            continue
        key = (site, species, int(yr))
        mother = str(row.get("Mother") or "").strip()
        if mother:
            if mother in mothers[key]:
                raise ValueError("Duplicate first brood for mother in same site/species/year")
            mothers[key].add(mother)
        corrected = fledged + 0.5 * deviation
        grouped[key].append((lay, corrected, peak, peak_mass))

    panel = defaultdict(list)
    for (site, species, yr), broods in sorted(grouped.items()):
        if len(broods) < MIN_BROODS:
            excluded["site_species_year_too_few_broods"] += 1
            continue
        lay = np.asarray([r[0] for r in broods], dtype=float)
        fledged = np.asarray([r[1] for r in broods], dtype=float)
        if len(np.unique(lay)) < 3 or lay.std() <= 1e-12:
            excluded["site_species_year_no_timing_spread"] += 1
            continue
        if fledged.mean() <= 0:
            excluded["site_species_year_zero_mean_fledgling"] += 1
            continue
        z = (lay - lay.mean()) / lay.std()
        w = fledged / fledged.mean()
        differential = float(np.mean(z * (w - 1.0)))
        panel[(site, species)].append({
            "year": yr,
            "n_broods": len(broods),
            "differential": differential,
            "mismatch_days": float(lay.mean() + OFFSET_DAYS - broods[0][2]),
            "log_peak_biomass": float(np.log1p(broods[0][3])),
            "peak_biomass_g_per_day_m2": float(broods[0][3]),
        })
    return panel, dict(excluded)


def evaluate_stratum(years):
    if len(years) < MIN_YEARS:
        return None
    years = sorted(years, key=lambda x: x["year"])
    if len({r["year"] for r in years}) != len(years):
        raise ValueError("Repeated held-out year in a stratum")
    y = np.asarray([r["differential"] for r in years], dtype=float)
    m = np.asarray([r["mismatch_days"] for r in years], dtype=float)
    b = np.asarray([r["log_peak_biomass"] for r in years], dtype=float)
    features = {
        "I_intercept": np.empty((len(years), 0)),
        "M_mismatch": m[:, None],
        "MB_mismatch_plus_biomass": np.column_stack((m, b)),
        "MBI_mismatch_biomass_interaction": np.column_stack((m, b, m * b)),
    }
    errors = {}
    for name, x in features.items():
        preds = []
        for held_out in range(len(years)):
            train = np.arange(len(years)) != held_out
            pred = float(fit_predict(x[train], y[train], x[~train])[0])
            preds.append(pred)
        errors[name] = float(np.mean((y - np.asarray(preds)) ** 2))
    delta_m = errors["M_mismatch"] - errors["MBI_mismatch_biomass_interaction"]
    delta_i = errors["I_intercept"] - errors["MBI_mismatch_biomass_interaction"]
    return {
        "years": len(years),
        "year_range": [int(years[0]["year"]), int(years[-1]["year"])],
        "broods": int(sum(r["n_broods"] for r in years)),
        "mean_annual_relative_fledging_differential": round(float(y.mean()), 6),
        "fraction_years_earlier_laying_advantaged": round(float(np.mean(y < 0)), 6),
        "mismatch_days_minmax": [round(float(m.min()), 3), round(float(m.max()), 3)],
        "biomass_g_day_m2_minmax": [
            round(float(min(r["peak_biomass_g_per_day_m2"] for r in years)), 6),
            round(float(max(r["peak_biomass_g_per_day_m2"] for r in years)), 6),
        ],
        "loyo_mse": {k: round(v, 9) for k, v in errors.items()},
        "delta_mse_M_minus_MBI": round(delta_m, 9),
        "delta_mse_I_minus_MBI": round(delta_i, 9),
        "passes_incremental_and_intercept": bool(delta_m > 0 and delta_i > 0),
    }


def audit(panel, excluded):
    out = {}
    for (site, species), years in sorted(panel.items()):
        tested = evaluate_stratum(years)
        if tested is None:
            continue
        tested["species_offset_validation"] = (
            "great_tit_literature_33_days" if species == PRIMARY_SPECIES
            else "blue_tit_33_day_UNVALIDATED_sensitivity_only"
        )
        out[site + "|" + species] = tested
    primary_keys = [site + "|" + PRIMARY_SPECIES for site in PRIMARY_SITES]
    admitted = all(key in out for key in primary_keys)
    passing = sum(out[key]["passes_incremental_and_intercept"]
                  for key in primary_keys if key in out)
    return {
        "status": "PAYOFF_B_DRYAD_2023_YEAR_LEVEL_SELECTION_BIOMASS_AUDIT",
        "source_integrity": "original_Dryad_SHA256_verified_in_load",
        "source_readme_verified": True,
        "resource_unit": "peak g/(day*m2); not integrated food availability",
        "offset_days": OFFSET_DAYS,
        "offset_validated_for_great_tits_only": True,
        "outcome": "phenotypic within-year relative first-brood fledging differential",
        "not_total_fitness_or_causal_selection": True,
        "independent_unit": "site-species-year annual differential",
        "do_not_pool_shared_resource_years_across_species": True,
        "minimum_broods_per_year": MIN_BROODS,
        "minimum_years_per_stratum": MIN_YEARS,
        "loyo": "entire_year_held_out; fixed_ridge_1; predictors_standardized_training_only",
        "primary_sites_all_admitted": admitted,
        "primary_sites_passing": passing,
        "primary_gate": "EXPLORATORY_PASS" if admitted and passing >= 2
                        else "HOLD_NO_CONSISTENT_INCREMENT",
        "multiple_exploratory_models_no_confirmatory_p": True,
        "food_demand_and_daily_biomass_observed": False,
        "excluded_counts": excluded,
        "strata": out,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    panel, excluded = prepare(load())
    results = audit(panel, excluded)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()
