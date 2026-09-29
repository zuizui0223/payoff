import pytest

from scripts.fetch_greater_snow_goose_movebank_authorized import (
    ensure_output_outside_repository,
    has_license_terms,
    parse_csv_rows,
    safe_file_stem,
    truthy,
    validate_event_csv,
)


def test_truthy_parser():
    assert truthy("true") is True
    assert truthy("FALSE") is False
    assert truthy("") is None


def test_license_terms_are_detected_and_never_treated_as_events():
    text = "<html><h1>License Terms:</h1><p>review me</p></html>"
    assert has_license_terms(text)
    with pytest.raises(ValueError, match="LICENSE_TERMS_REQUIRED"):
        validate_event_csv(text)


def test_event_csv_schema_and_count():
    text = (
        "timestamp,location_lat,location_long,visible\n"
        "2020-05-01 00:00:00,45.0,-70.0,true\n"
        "2020-05-01 01:00:00,45.1,-70.1,true\n"
    )
    header, rows = validate_event_csv(text)
    assert header[:3] == [
        "timestamp", "location_lat", "location_long"
    ]
    assert rows == 2


def test_event_csv_missing_location_fails_closed():
    text = "timestamp,visible\n2020-05-01 00:00:00,true\n"
    with pytest.raises(ValueError, match="EVENT_SCHEMA_MISMATCH"):
        validate_event_csv(text)


def test_parse_csv_rows():
    rows = parse_csv_rows("id,name\n1,goose\n")
    assert rows == [{"id": "1", "name": "goose"}]


def test_safe_file_stem():
    assert safe_file_stem("Bird 12/A", "99") == "Bird_12_A"
    assert safe_file_stem("", "99") == "individual_99"


def test_output_directory_must_be_outside_repository(tmp_path, monkeypatch):
    import scripts.fetch_greater_snow_goose_movebank_authorized as fetch

    repo = tmp_path / "repo"
    repo.mkdir()
    outside = tmp_path / "private"
    monkeypatch.setattr(fetch, "REPO_ROOT", repo)

    assert ensure_output_outside_repository(outside) == outside.resolve()

    with pytest.raises(ValueError, match="outside the PAYOFF-B repository"):
        ensure_output_outside_repository(repo / "raw_movebank")
