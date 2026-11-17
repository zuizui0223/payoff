"""Synthetic schema checks only; never bird outcome results."""
import pytest
pytest.importorskip("openpyxl")
from scripts.payoff_b_goose_gps_fitness_dryad_gate import (
    columns_and_counts,REQUIRED_FILES
)


def test_gps_coordinates_and_nest_success_are_not_same_column():
    src=(b"bird_id,year,date,longitude,latitude,nesting_success,temperature\n"
         b"A,2020,2020-04-14,4.0,51.0,1,10\n")
    r=columns_and_counts(src,"GPS.csv")
    assert r["n_source_rows"]==1
    assert "latitude" in r["field_groups"]["spatial"]
    assert "nesting_success" in r["field_groups"]["breeding"]
    assert "temperature" in r["field_groups"]["environment"]


def test_no_cues_in_source_are_not_inferred():
    src=b"BirdID,Year,Longitude,Latitude\nA,2020,4.0,51.0\n"
    r=columns_and_counts(src,"track.csv")
    assert not r["field_groups"]["environment"]
    assert r["n_columns"]==4


def test_exact_four_original_csv_and_readme_requirements():
    assert len(REQUIRED_FILES)==5
    assert "1.NestLocationData.csv" in REQUIRED_FILES
    assert "2.RawTrackingData_GPSACC.csv" in REQUIRED_FILES
