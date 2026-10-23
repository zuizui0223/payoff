"""Integrity tests for event-coverage summary, without real animal locations."""
from pathlib import Path
from scripts.qc_public_movebank_geese_2016 import DOI, FILES, event_coverage


def test_pinned_source_identity():
    assert DOI == "10.5441/001/1.31c2v92f"
    assert len(FILES) == 3
    for uuid, md5, size in FILES.values():
        assert len(uuid) == 36 and len(md5) == 32 and size > 0


def test_aggregate_schema_excludes_raw_ids_and_coordinates(tmp_path: Path):
    path = tmp_path / "mock.csv"
    path.write_text(
        "timestamp,individual-local-identifier,location-lat,location-long\n"
        "2016-03-17 13:00:00,A,54.5,9.2\n"
        "2017-04-17 13:00:00,A,54.6,9.3\n"
        "2017-04-17 13:00:00,A,54.6,9.3\n"
        "2017-03-17 13:00:00,B,notnum,9.3\n")
    result = event_coverage(path)
    assert result["unique_individual_identifiers"] == 1
    assert result["identifiers_present_in_multiple_calendar_years"] == 1
    assert result["duplicate_individual_timestamp_rows"] == 1
    assert result["invalid_coordinate_rows"] == 1
    assert result["has_required_event_columns"]
    assert not result["cue_chronology_verified"]
    assert not result["fitness_outcome_verified"]
    assert "animal_ids" not in result


def test_missing_required_columns_are_rejected(tmp_path: Path):
    path = tmp_path / "missing.csv"
    path.write_text("timestamp,animal-id\n2016-01-01,A\n")
    result = event_coverage(path)
    assert result["status"] == "REQUIRED_FIELDS_MISSING"
