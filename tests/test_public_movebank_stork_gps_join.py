"""GPS-to-breeding source gates on fully synthetic animal tracks only."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.qc_public_movebank_stork_gps_join_2018 import (
    GPS_EXPECTED_MD5, GPS_EXPECTED_BYTES, identifier_mappings,
    load_reference_and_breeding, gps_breeding_join_summary,
)


def _write(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def setup_synthetic(tmp_path: Path):
    ref = tmp_path/"reference.csv"
    birth = tmp_path/"birth.csv"
    gps = tmp_path/"gps.csv"
    _write(ref, [
        {"deployment-id":"11","animal-id":"bird-a","tag-id":"tag-a"},
        {"deployment-id":"12","animal-id":"bird-b","tag-id":"tag-b"},
    ])
    _write(birth,[
        {"id":"11","Year":"2014","Fledglings":"2"},
        {"id":"11","Year":"2015","Fledglings":"NA"},
        {"id":"12","Year":"2014","Fledglings":"0"},
    ])
    gpsrows=[]
    for dep,animal,year in [("11","bird-a",2014),("11","bird-a",2015),
                             ("12","bird-b",2014)]:
        for month,n in [(1,7),(3,11),(5,8)]:
            for day in range(1,n+1):
                gpsrows.append({
                    "timestamp":f"{year}-{month:02d}-{day:02d} 10:00:00.000",
                    "individual-local-identifier":animal,
                    "location-lat":"49.5", "location-long":"10.0",
                    "ground-speed":"4.1"
                })
    gpsrows.append(dict(gpsrows[0])) # explicit duplicate check
    gpsrows.append({**gpsrows[0], "individual-local-identifier":"unmapped"})
    _write(gps,gpsrows)
    return ref,birth,gps


def test_real_source_integrity_is_pinned():
    assert len(GPS_EXPECTED_MD5) == 32
    assert GPS_EXPECTED_BYTES == 273153305


def test_synthetic_gps_joins_breeding_without_public_animal_ids(tmp_path):
    ref,birth,gps=setup_synthetic(tmp_path)
    refs,pairs,numeric=load_reference_and_breeding(ref,birth)
    r=gps_breeding_join_summary(gps, refs,pairs,numeric)
    assert r["identity_method"] == "individual-local-identifier"
    assert r["breeding_total_animal_years"] == 3
    assert r["breeding_numeric_fledgling_animal_years"] == 2
    assert r["breeding_animal_years_with_any_valid_gps"] == 3
    assert r["breeding_animal_years_with_any_gps_and_numeric_fledglings"] == 2
    assert r["matched_duplicate_individual_timestamp_rows"] == 1
    assert r["source_gps_unmatched_identity_rows"] == 1
    w=r["coverage_calendar_windows"]
    assert w["winter_spring_late_all"] == 3
    assert w["winter_spring_late_all_numeric_fledglings"] == 2
    assert r["fitness_association_estimated"] is False
    assert r["migration_start_end_derived"] is False
    assert "bird-a" not in str(r) and "49.5" not in str(r)


def test_duplicate_breeding_rows_fail_closed(tmp_path):
    ref,birth,gps=setup_synthetic(tmp_path)
    with birth.open("a") as f:
        f.write("11,2014,4\n")
    with pytest.raises(ValueError, match="duplicate breeding animal-year"):
        load_reference_and_breeding(ref,birth)


def test_missing_coordinates_fail_closed(tmp_path):
    ref,birth,gps=setup_synthetic(tmp_path)
    gps.write_text("timestamp,individual-local-identifier\n2014-01-01,a\n")
    refs,pairs,numeric=load_reference_and_breeding(ref,birth)
    with pytest.raises(ValueError, match="GPS essential columns missing"):
        gps_breeding_join_summary(gps,refs,pairs,numeric)
