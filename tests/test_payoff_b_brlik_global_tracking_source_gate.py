"""Synthetic-only schema and verification tests; no movement effects."""
import hashlib
from scripts.payoff_b_brlik_global_tracking_source_gate import (
    check_hash,csv_schema
)


def test_zenodo_checksum_fail_close():
    b=b"year,id,depart\n2020,B1,125\n"
    expected="md5:"+hashlib.md5(b).hexdigest()
    assert check_hash(b,expected)["verified"]
    assert not check_hash(b+b"z",expected)["verified"]
    assert not check_hash(b,None)["verified"]


def test_stage_fields_separate_from_geo_and_fitness():
    b=(b"bird_id,species,year,spring_departure,spring_arrival,latitude,"
       b"longitude,fledgling_success\nAB,T,2020,122,161,55,5,1\n")
    s=csv_schema(b,"events.csv")
    assert s["n_rows_scanned"]==1
    assert "spring_departure" in s["candidate_fields"]["date_or_event"]
    assert "latitude" in s["candidate_fields"]["geography"]
    assert "fledgling_success" in s["candidate_fields"]["outcome"]


def test_no_geography_not_assumed_to_exist():
    b=b"individual,year,departure_date,arrival_date\nX,2020,127,138\n"
    s=csv_schema(b,"phenology.csv")
    assert not s["candidate_fields"]["geography"]
    assert s["candidate_fields"]["date_or_event"]==["departure_date","arrival_date"]
