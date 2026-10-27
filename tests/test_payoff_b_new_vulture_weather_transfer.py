"""Holdout source replication controls, without GPS or weather network."""
from scripts.run_payoff_b_new_vulture_weather_transfer import (
    validate_counts,describe_transfer,EXPECTED,SOLAR_FIELD,VAR_ORDER
)

def test_preopened_source_cohort_is_not_changed():
    keys=("all_at_risk_stationary_days","NORTHWARD_CANDIDATE",
          "STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED",
          "deduplicated_frozen_cases")
    counts=dict(zip(keys,EXPECTED[:6]))
    plan={
       "unique_grid_calendar_months":EXPECTED[6],
       "grid_months_with_both_northward_and_stay_observations":EXPECTED[7],
       "northward_case_days_in_overlap_gridmonths":EXPECTED[8]
    }
    validate_counts([None]*EXPECTED[0],counts,plan)
    counts["NORTHWARD_CANDIDATE"]=99
    try:validate_counts([None]*EXPECTED[0],counts,plan)
    except ValueError:pass
    else:raise AssertionError("Original source drift must fail closed")

def test_same_sign_only_descriptive_source_result():
    assert SOLAR_FIELD in VAR_ORDER
    result=describe_transfer(
        {SOLAR_FIELD:-8.0},
        {"bootstrap_interval_95pct_descriptive":{SOLAR_FIELD:[-15,-1]}})
    assert result["descriptive_same_sign_as_stork"] is True
    assert result["source_fine_gridmonth_block_ci_excludes_zero_in_negative_direction"] is True
    assert result["source_weather_replication_is_Payoff_B_information_causality"] is False
    other=describe_transfer(
        {SOLAR_FIELD:3.0},
        {"bootstrap_interval_95pct_descriptive":{SOLAR_FIELD:[-1,6]}})
    assert not other["descriptive_same_sign_as_stork"]
    assert not other["source_fine_gridmonth_block_ci_excludes_zero_in_negative_direction"]
