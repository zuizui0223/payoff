"""Even a user-uploaded source q table cannot substitute annual spring or GPS joins."""
import csv
from pathlib import Path
from scripts.payoff_b_v7_original_join_readiness import (
    gate,REQUIRED_ANNUAL,REQUIRED_STOPS,REQUIRED_GEOMETRY
)

def test_source_aggregates_q_count_pass_but_v7_outcome_held():
    x=gate()
    assert x["source_30year_q_pairs"]==23
    assert x["consecutive_candidate_q_pairs"]==13
    assert x["consecutive_q_without_unresolved_alias"]==11
    assert x["meets_at_least_10_independent_q_transition_minimum_if_GPS_regions_confirm"]
    assert x["stop_reason"]=="MISSING_FOCAL_YEAR_REGION_SPECIFIC_GDD_ONSETS"
    assert x["V7_REGISTERED_PRIMARY_GATE"]=="HOLD_NOT_ESTIMABLE"
    assert not x["focal_bird_phenology_coefficient_fitted"]

def _one_row_csv(path,columns):
    with path.open("w",newline="") as out:
        writer=csv.DictWriter(out,fieldnames=sorted(columns))
        writer.writeheader()
        writer.writerow({key:"placeholder" for key in sorted(columns)})

def test_source_schema_alone_does_not_authorize_actual_q_U_effect(tmp_path):
    annual=tmp_path/"annual.csv";stops=tmp_path/"stops.csv";geo=tmp_path/"geo.csv"
    _one_row_csv(annual,REQUIRED_ANNUAL)
    _one_row_csv(stops,REQUIRED_STOPS)
    _one_row_csv(geo,REQUIRED_GEOMETRY)
    x=gate(annual,stops,geo)
    assert x["annual_GDD_jerk_region_year_data"]["status"]=="SCHEMA_COLUMNS_PRESENT_NOT_YET_ADMITTED"
    assert x["stop_reason"]=="ORIGINAL_ROW_AND_Q_U_ADMISSION_UNVERIFIED"
    assert x["V7_REGISTERED_PRIMARY_GATE"]=="HOLD_NOT_ESTIMABLE"

def test_missing_focal_year_GDD_julian_still_blocks(tmp_path):
    annual=tmp_path/"annual.csv"
    _one_row_csv(annual,REQUIRED_ANNUAL-{"gdd_jerk_onset_julian"})
    x=gate(annual=annual)
    assert "gdd_jerk_onset_julian" in x["annual_GDD_jerk_region_year_data"]["missing_columns"]
    assert x["V7_REGISTERED_PRIMARY_GATE"]=="HOLD_NOT_ESTIMABLE"
