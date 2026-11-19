#!/usr/bin/env python3
"""Validate native-R aggregate original individual decision joins, no bird rows."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

NUMERIC_KEYS={
 "original_event_rows",
 "original_flight_rows",
 "original_event_ID_count",
 "original_flight_ID_count",
 "original_ID_intersection_count",
 "original_event_only_ID_count",
 "original_flight_only_ID_count",
 "original_duplicate_flight_ID_count",
 "original_status_valid_0_or_1_count",
 "original_status_missing_or_invalid_count",
 "original_at_risk_non_departure_days",
 "original_departure_event_rows",
 "original_IDs_with_at_least_one_departure_event",
 "original_IDs_with_more_than_one_terminal_event",
 "original_flight_landing_valid_0_or_1_count",
 "original_flight_landing_missing_or_invalid_count",
 "original_observed_landing_events",
 "original_observed_nonlanding_flights",
 "original_route_onshore_label_count",
 "original_route_offshore_label_count",
 "original_route_label_missing_count",
 "original_flightStart_available",
 "original_flightEnd_available",
 "original_flightStart_before_end_count",
 "original_start_wind_cloud_all_present",
 "original_end_wind_cloud_all_present",
 "original_start_and_end_weather_all_present",
 "original_departure_event_UTCday_comparable",
 "original_departure_event_same_UTCday",
 "original_departure_event_within_UTC_plusminus1day",
}
BOOLEAN_KEYS={
 "original_key_merging_uses_coordinateless_motusTagID",
 "direct_q_wait_D_eff_r_t_and_fitness_estimable",
 "original_weather_three_decision_effects_novel_to_PAYOFF",
}

def summarize(path:Path)->dict:
    with path.open(encoding="utf-8",newline="") as f:
        raw=list(csv.DictReader(f))
    if len(raw)!=len(NUMERIC_KEYS|BOOLEAN_KEYS):
        raise ValueError("Original native-R metric ledger row count drift")
    d={}
    for r in raw:
        k=r.get("metric","")
        v=r.get("value","")
        if k in d:
            raise ValueError("Duplicate original metric")
        if k in NUMERIC_KEYS:
            if not v.isdigit():
                raise ValueError("Original metric count is not integer")
            d[k]=int(v)
        elif k in BOOLEAN_KEYS:
            if v not in ("TRUE","FALSE"):
                raise ValueError("Original R logical source metric invalid")
            d[k]=(v=="TRUE")
        else:
            raise ValueError("Unexpected source join metric / possible row values")
    if set(d)!=(NUMERIC_KEYS|BOOLEAN_KEYS):
        raise ValueError("Original source aggregate metric names incomplete")
    if d["original_event_rows"]!=1783 or d["original_flight_rows"]!=178:
        raise ValueError("Original 2023 event/flight row grain changed")
    if d["original_event_ID_count"]!=178 or d["original_flight_ID_count"]!=178:
        raise ValueError("Original source individual counts changed")
    if d["original_event_rows"]!=(
        d["original_status_valid_0_or_1_count"]+
        d["original_status_missing_or_invalid_count"]
    ):
        raise ValueError("Event status sums inconsistent")
    if d["original_flight_rows"]!=(
        d["original_flight_landing_valid_0_or_1_count"]+
        d["original_flight_landing_missing_or_invalid_count"]
    ):
        raise ValueError("Landing status counts inconsistent")
    if (d["original_route_onshore_label_count"]+
        d["original_route_offshore_label_count"]+
        d["original_route_label_missing_count"] != d["original_flight_rows"]):
        raise ValueError("Author's coasting/sea-crossing route source totals inconsistent")
    if (d["original_route_onshore_label_count"],
        d["original_route_offshore_label_count"]) != (154, 24):
        raise ValueError("Original published route category counts drifted")
    if d["original_event_ID_count"] != (
        d["original_ID_intersection_count"]+
        d["original_event_only_ID_count"]
    ):
        raise ValueError("Event-only original IDs inconsistent")
    if d["original_flight_ID_count"] != (
        d["original_ID_intersection_count"]+
        d["original_flight_only_ID_count"]
    ):
        raise ValueError("Flight-only original IDs inconsistent")
    if d["original_departure_event_same_UTCday"] > d[
        "original_departure_event_within_UTC_plusminus1day"
    ]:
        raise ValueError("Source event UTC time matching reverses inclusion")
    eligible=(
        d["original_ID_intersection_count"]>=30
        and d["original_observed_landing_events"]>=10
        and d["original_duplicate_flight_ID_count"]==0
        and d["original_status_missing_or_invalid_count"]==0
        and d["original_departure_event_UTCday_comparable"]>=30
        and d["original_start_and_end_weather_all_present"]>=30
    )
    return {
        "as_of":"2026-11-19",
        "source_original_paper":"Rüppel et al. 2023 Royal Society Open Science DOI 10.1098/rsos.221420",
        "original_figshare_DOI":"10.6084/m9.figshare.c.6403996",
        "original_source_ZIP_SHA256_verified":"0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6",
        "original_join_key":"motusTagID (individual ID, never geographic position)",
        "aggregated_original_source_metrics":d,
        "source_key_and_temporal_support_status":(
          "SOURCE_SCHEMA_POTENTIALLY_SUITABLE_FOR_EXPLORATORY_SEQUENTIAL_DECISIONS"
          if eligible else "SOURCE_JOIN_OR_TIMING_NOT_ESTIMABLE_WITH_FROZEN_SUPPORT"
        ),
        "source_bird_event_rows_exported":False,
        "source_individual_IDs_exported":False,
        "weather_measurement_is_bird_forecast_belief":False,
        "individual_precommitment_environment_predictability_q_identified":False,
        "independent_delayed_actionability_and_fitness_identified":False,
        "original_published_2023_weather_decision_results_prior_art":True,
        "novel_biological_effect_fitted":False,
        "theory_information_deadline":"NOT_IDENTIFIED",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original-aggregate-csv",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    o=p.parse_args()
    result=summarize(o.original_aggregate_csv)
    o.output.parent.mkdir(parents=True,exist_ok=True)
    o.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    stats=result["aggregated_original_source_metrics"]
    print(json.dumps({
        "source_status":result["source_key_and_temporal_support_status"],
        "n_published_original_event_rows":stats["original_event_rows"],
        "n_published_original_flights":stats["original_flight_rows"],
        "n_original_matching_IDs":stats["original_ID_intersection_count"],
        "n_original_landings":stats["original_observed_landing_events"],
        "n_terminal_departure_events":stats["original_departure_event_rows"],
        "no_new_effect_fitted":True,
        "natural_information_deadline":"NOT_IDENTIFIED",
    },ensure_ascii=False))


if __name__=="__main__":
    main()
