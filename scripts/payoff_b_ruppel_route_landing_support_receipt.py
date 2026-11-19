#!/usr/bin/env python3
"""Aggregate-only Rüppel 2023 published route/landing source support audit.

Reads only native-R 3 species x 3 years x 2 routes x 2 landing categories
contingency cells. Does not read individual bird IDs, route coordinates,
weather responses or original individual events. No biological effect fit.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

SOURCE_SHA256 = "0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6"
ROUTES = ("coasting", "sea-crossing")
LANDING = ("0","1")
YEARS = ("2019","2020","2021")
MIN_EACH_ROUTE_LANDING = 5
MIN_YEARS_EACH_ROUTE_WITH_LANDING = 2
MIN_SPECIES_EACH_ROUTE_WITH_LANDING = 2


def audit_cross_tab(source: Path) -> dict:
    with source.open(encoding="utf-8",newline="") as handle:
        rows=list(csv.DictReader(handle))
    if not rows or not {"species","year","route","landing","count"}.issubset(rows[0]):
        raise ValueError("Native original species×year route/landing source columns absent")
    if len(rows)!=36:
        raise ValueError("Expected exactly 3 original taxa × 3 years × 2 routes × 2 landing codes")
    species = sorted({row["species"] for row in rows})
    if len(species)!=3:
        raise ValueError("Original published three-taxon sampling changed")
    items={}
    for row in rows:
        sp,year,route,land = (row[k] for k in ("species","year","route","landing"))
        count=row["count"]
        if year not in YEARS or route not in ROUTES or land not in LANDING:
            raise ValueError("Unregistered original route/year/landing category")
        if not count.isdigit():
            raise ValueError("Original original-source frequency is not nonnegative integer")
        key=(sp,year,route,land)
        if key in items:
            raise ValueError("Duplicate source contingency stratum")
        items[key]=int(count)
    required={
        (sp,year,route,land)
        for sp in species for year in YEARS for route in ROUTES for land in LANDING
    }
    if set(items)!=required:
        raise ValueError("Incomplete original category combination or missing zero cells")
    route_landing={}
    for route in ROUTES:
        by_landing={}
        for land in LANDING:
            by_landing[land]=sum(
                items[(sp,year,route,land)]
                for sp in species for year in YEARS
            )
        route_landing[route]={
            "observed_nonlandings":by_landing["0"],
            "observed_landings":by_landing["1"],
            "observed_total":by_landing["0"]+by_landing["1"],
            "years_with_at_least_one_landing":sum(
                any(items[(sp,year,route,"1")]>0 for sp in species)
                for year in YEARS
            ),
            "species_with_at_least_one_landing":sum(
                any(items[(sp,year,route,"1")]>0 for year in YEARS)
                for sp in species
            ),
        }
    if (route_landing["coasting"]["observed_total"],
        route_landing["sea-crossing"]["observed_total"])!=(154,24):
        raise ValueError("Original coasting/sea-crossing totals not reproduced")
    if sum(v["observed_landings"] for v in route_landing.values())!=24:
        raise ValueError("Original 24 observed landing events not reproduced")
    if sum(v["observed_nonlandings"] for v in route_landing.values())!=154:
        raise ValueError("Original 154 nonlanding flight events not reproduced")
    supported=all(
        v["observed_landings"]>=MIN_EACH_ROUTE_LANDING
        and v["observed_nonlandings"]>=MIN_EACH_ROUTE_LANDING
        and v["years_with_at_least_one_landing"]>=MIN_YEARS_EACH_ROUTE_WITH_LANDING
        and v["species_with_at_least_one_landing"]>=MIN_SPECIES_EACH_ROUTE_WITH_LANDING
        for v in route_landing.values()
    )
    by_year=[]
    for year in YEARS:
        by_year.append({
            "source_year":int(year),
            "original_flights":sum(
                v for (sp,y,r,l),v in items.items() if y==year
            ),
            "observed_landings":sum(
                v for (sp,y,r,l),v in items.items() if y==year and l=="1"
            ),
            "sea_crossing_flights":sum(
                v for (sp,y,r,l),v in items.items() if y==year and r=="sea-crossing"
            ),
        })
    by_species=[]
    for sp in species:
        by_species.append({
            "source_species":sp,
            "original_flights":sum(v for (s,y,r,l),v in items.items() if s==sp),
            "observed_landings":sum(v for (s,y,r,l),v in items.items() if s==sp and l=="1"),
            "sea_crossing_flights":sum(v for (s,y,r,l),v in items.items() if s==sp and r=="sea-crossing"),
        })
    return {
        "as_of":"2026-11-19",
        "source":"Rüppel et al 2023 Royal Society Open Science 10:221420 original Figshare 6403996",
        "original_public_data_zip_sha256_verified":SOURCE_SHA256,
        "analysis":"SOURCE_ONLY_ORIGINAL_ROUTE_BY_LANDING_SUPPORT_NOT_BIOLOGICAL_MODEL",
        "individual_animal_bird_or_event_rows_exported":False,
        "source_2by2_route_landing":route_landing,
        "by_original_year_aggregate":by_year,
        "by_original_taxon_aggregate":by_species,
        "frozen_min_observed_landings_and_nonlandings_per_route":MIN_EACH_ROUTE_LANDING,
        "frozen_min_original_years_with_landing_per_route":MIN_YEARS_EACH_ROUTE_WITH_LANDING,
        "frozen_min_original_species_with_landing_per_route":MIN_SPECIES_EACH_ROUTE_WITH_LANDING,
        "route_landing_modifier_source_support":(
            "DESIGN_SUPPORT_PRESENT_NO_EFFECT_FITTED"
            if supported else
            "ROUTE_LANDING_MODIFIER_NOT_ESTIMABLE_UNDER_FROZEN_SUPPORT"
        ),
        "weather_start_and_end_temporally_distinct":True,
        "postflight_weather_measured_at_end_is_a_predeparture_forecast":False,
        "source_has_weather_forecast_issue_timestamp_for_each_bird":False,
        "original_route_landing_weather_association_already_published":True,
        "novel_biological_effect_fitted":False,
        "natural_qwait_D_eff_r_t_or_fitness_identified":False,
        "detector_coverage_bias_independently_resolved":False,
        "original_source_178_flights_only_not_independent_replication":True,
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original-route-contingency-csv",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    opts=p.parse_args()
    result=audit_cross_tab(opts.original_route_contingency_csv)
    opts.output.parent.mkdir(parents=True,exist_ok=True)
    opts.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "source_route_landing":result["source_2by2_route_landing"],
        "support_status":result["route_landing_modifier_source_support"],
        "n_biological_coefficients_estimated":0,
        "natural_payoff_information_deadline_identified":False,
    },ensure_ascii=False))


if __name__=="__main__":
    main()
