#!/usr/bin/env python3
"""PAYOFF-B source-only Bylot long-run breeding/climate feasibility gate.

This is NOT a bird-level cue/actionability/fitness analysis. No owner terms are
accepted or bypassed, no protected GPS is fetched and no climate/nest outcomes
are opened. Source calendar ceilings are necessary but not sufficient.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"data/payoff_b_bylot_independent_outyear_source_contract_20261119.json"
REQUIRED_SOURCE_KEYS={
    "D41_nest_summary",
    "D41_nest_visits",
    "D2_BYLCAMP_daily_climate",
    "greater_snow_goose_movebank",
}

def _range_years(start:int,end:int)->set[int]:
    if not (1900 <= start <= end <= 2100):
        raise ValueError("Impossible source year limits")
    return set(range(start,end+1))

def source_calendar_gate(config:dict)->dict:
    if config["contract_id"]!="payoff_b_bylot_independent_outyear_source_gate_20261119_v1":
        raise ValueError("Wrong original scientific gate contract")
    sources={r["key"]:r for r in config["source_roles"]}
    if set(sources)!=REQUIRED_SOURCE_KEYS or len(config["source_roles"])!=4:
        raise ValueError("Missing or duplicate source roles")
    d41=sources["D41_nest_summary"]
    visits=sources["D41_nest_visits"]
    d2=sources["D2_BYLCAMP_daily_climate"]
    gps=sources["greater_snow_goose_movebank"]
    if not (
        d41["doi"]=="10.5885/45570CE-2D00DCA728074FA7"
        and d41["version"]=="1.2"
        and d41["nominal_calendar_span"]==[1989,2025]
        and sorted(d41["documented_missing_years"])==[2020,2021,2024]
        and visits["nominal_calendar_span"]==[1989,2019]
        and d2["doi"]=="10.5885/45039SL-EE76C1BDAADC4890"
        and d2["station"]=="Bylot Lac du camp (BYLCAMP)"
        and d2["nominal_full_calendar_spring_year_span"]==[1994,2023]
        and gps["study_id"]==1442516400
        and gps["documented_calendar_span"]==[2019,2023]
    ):
        raise ValueError("Frozen source identity or coverage changed")
    if config["eligibility_contract"]["minimum_independent_post_2015_holdout_years"]!=10:
        raise ValueError("Do not retune post-2015 support threshold")
    if config["eligibility_contract"]["fixed_pre_egg_temperature_window"]!="May 1–15":
        raise ValueError("Temporal cue window changed after source inspection")
    possible_nests=_range_years(*d41["nominal_calendar_span"]) - set(d41["documented_missing_years"])
    weather_spring=_range_years(*d2["nominal_full_calendar_spring_year_span"])
    nom_climate_nest=sorted(possible_nests & weather_spring)
    historical=sorted(y for y in nom_climate_nest if y<=2015)
    independent=sorted(y for y in nom_climate_nest if y>=2016)
    if historical!=list(range(1994,2016)) or independent!=[2016,2017,2018,2019,2022,2023]:
        raise ValueError("Expected historical and post-2015 source coverage changed")
    visit_years=_range_years(*visits["nominal_calendar_span"])
    gps_years=_range_years(*gps["documented_calendar_span"])
    year_only_visit_gps=sorted(visit_years & gps_years)
    year_only_summary_gps=sorted(possible_nests & gps_years)
    if year_only_visit_gps != [2019] or year_only_summary_gps != [2019,2022,2023]:
        raise ValueError("Unexpected original GPS vs nesting source-year support")
    # No fake individual join just because source years overlap.
    source_ready=config["source_admission"]
    assert set(source_ready)=={
        "annual_nest_summary_original_bytes_obtained",
        "daily_climate_original_bytes_obtained",
        "nest_visit_original_bytes_obtained",
        "gps_original_bytes_permission_confirmed",
        "nest_outcome_codebook_and_sampling_strata_verified",
        "climate_daily_time_zone_and_units_verified",
        "interactor_individual_crosswalk_verified",
    }, "Original source gate fields changed"
    if any(bool(x) for x in source_ready.values()):
        raise ValueError("Access/verification facts cannot be marked admitted without original receipts")
    if any(source.get("original_bytes_sha256") is not None for source in sources.values()):
        raise ValueError("Source SHA256 cannot be invented before original bytes are obtained")
    n_post=len(independent)
    return {
        "status":"SOURCE_ONLY_NOMINAL_YEAR_OVERLAP_AUDITED_NO_NEW_BIOLOGICAL_FIT",
        "scientific_contract":config["contract_id"],
        "predecision_temperature_window":"May 1–15 (calendar proxy, not animal-observed cue)",
        "nest_summary_source_version":d41["version"],
        "climate_station":d2["station"],
        "climate_source_version":d2["version"],
        "historical_calendar_overlap_years":historical,
        "historical_calendar_overlap_n":len(historical),
        "post_2015_calendar_overlap_years":independent,
        "post_2015_nominal_max_n":n_post,
        "minimum_outyear_independent_years":10,
        "registered_strong_outyear_gate":"FAIL_MAX_6_YEARS_LESS_THAN_10",
        "source_coverage_is_actual_row_level_coverage":False,
        "site_year_schema_observed":False,
        "actual_predecision_weather_data_opened":False,
        "actual_annual_laying_outcomes_opened":False,
        "original_nest_visits_vs_GPS_overlap_years_only":year_only_visit_gps,
        "original_nest_summary_vs_GPS_overlap_years_only":year_only_summary_gps,
        "individual_GPS_to_nest_join_admitted":False,
        "nest_summary_breeding_success_is_one_year_offspring_fitness":False,
        "breeding_temperature_observed_by_migrants_before_decision":False,
        "prior_2020_fitness_surface_reused_as_new_independent_2016_plus_finding":False,
        "user_terms_for_nordicana_data_accepted":False,
        "movebank_download_permission_confirmed":False,
        "original_source_files_obtained":False,
        "next_source_gate":"ORIGINAL_USER_AUTHORIZED_NORDICANA_ZIPS_AND_CODEBOOK_AND_EXPLICIT_RIGHTS_RECEIPT",
        "V7_genuine_animal_q_urgency_fitness":"NOT_ESTIMABLE",
        "new_focal_biological_effect":"NOT_FITTED",
    }

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest",type=Path,default=MANIFEST)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    content=json.loads(args.manifest.read_text(encoding="utf-8"))
    answer=source_calendar_gate(content)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(answer,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(answer,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
