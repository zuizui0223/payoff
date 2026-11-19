"""Original Rüppel 2023 bird/flight metrics must be aggregate and source-consistent."""
import csv

import pytest

from scripts.payoff_b_ruppel_join_source_receipt import (
    NUMERIC_KEYS, BOOLEAN_KEYS, summarize
)


def fake_metrics():
    m={name:0 for name in NUMERIC_KEYS}
    m.update({
        "original_event_rows":1783,
        "original_flight_rows":178,
        "original_event_ID_count":178,
        "original_flight_ID_count":178,
        "original_ID_intersection_count":178,
        "original_status_valid_0_or_1_count":1783,
        "original_at_risk_non_departure_days":1605,
        "original_departure_event_rows":178,
        "original_IDs_with_at_least_one_departure_event":178,
        "original_flight_landing_valid_0_or_1_count":178,
        "original_observed_landing_events":24,
        "original_observed_nonlanding_flights":154,
        "original_route_onshore_label_count":154,
        "original_route_offshore_label_count":24,
        "original_flightStart_available":178,
        "original_flightEnd_available":178,
        "original_flightStart_before_end_count":178,
        "original_start_and_end_weather_all_present":178,
        "original_departure_event_UTCday_comparable":178,
        "original_departure_event_same_UTCday":178,
        "original_departure_event_within_UTC_plusminus1day":178,
    })
    m.update({name:(name=="original_key_merging_uses_coordinateless_motusTagID")
              for name in BOOLEAN_KEYS})
    return m


def write_metrics(path, rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["metric","value"])
        w.writeheader()
        for name,v in rows.items():
            w.writerow({"metric":name,"value":str(v).upper() if isinstance(v,bool) else v})


def test_compatible_source_aggregates_produce_only_source_admission(tmp_path):
    p=tmp_path/"source_aggregates.csv"
    write_metrics(p,fake_metrics())
    result=summarize(p)
    assert result["source_key_and_temporal_support_status"]==(
        "SOURCE_SCHEMA_POTENTIALLY_SUITABLE_FOR_EXPLORATORY_SEQUENTIAL_DECISIONS"
    )
    assert result["original_published_2023_weather_decision_results_prior_art"] is True
    assert result["novel_biological_effect_fitted"] is False
    assert result["theory_information_deadline"]=="NOT_IDENTIFIED"


def test_missing_bird_join_fails_source_admission(tmp_path):
    p=tmp_path/"source_aggregates.csv"
    x=fake_metrics()
    x.update({
        "original_ID_intersection_count":0,
        "original_event_only_ID_count":178,
        "original_flight_only_ID_count":178,
    })
    write_metrics(p,x)
    result=summarize(p)
    assert result["source_key_and_temporal_support_status"]==(
        "SOURCE_JOIN_OR_TIMING_NOT_ESTIMABLE_WITH_FROZEN_SUPPORT"
    )


def test_impossible_count_or_raw_values_detected(tmp_path):
    p=tmp_path/"source_aggregates.csv"
    d=fake_metrics()
    d["original_ID_intersection_count"]=190
    write_metrics(p,d)
    with pytest.raises(ValueError,match="Original source|individual counts|Event-only|Flight-only"):
        summarize(p)
    d=fake_metrics()
    d["original_public_bird_identifier"]="SECRET_123"
    write_metrics(p,d)
    with pytest.raises(ValueError,match="ledger row count drift"):
        summarize(p)


def test_unmarked_raw_flag_cannot_be_silently_promoted(tmp_path):
    p=tmp_path/"source_aggregates.csv"
    d=fake_metrics()
    d["direct_q_wait_D_eff_r_t_and_fitness_estimable"]=True
    write_metrics(p,d)
    result=summarize(p)
    # The source report must NOT turn a boolean metadata value into a causal
    # information inference; the declared scientific ceilings stay false.
    assert result["individual_precommitment_environment_predictability_q_identified"] is False
    assert result["weather_measurement_is_bird_forecast_belief"] is False
