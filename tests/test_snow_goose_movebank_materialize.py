from pathlib import Path

import pytest

from scripts.payoff_b_greater_snow_goose_movebank_materialize import (
    ATTRIBUTES,
    MaterializationBlocked,
    expected_header_fields,
    looks_like_license_terms,
    movebank_timestamp_end,
    movebank_timestamp_start,
    validate_csv_header,
)


def test_frozen_year_timestamp_bounds():
    assert movebank_timestamp_start(2019) == "20190101000000000"
    assert movebank_timestamp_end(2023) == "20231231235959999"


def test_license_terms_detection_is_fail_closed():
    assert looks_like_license_terms(
        b"<html><body><h1>License Terms:</h1></body></html>"
    )
    assert not looks_like_license_terms(
        b"timestamp,location_long,location_lat,individual_id\n"
    )


def test_required_raw_columns_are_exact():
    assert expected_header_fields() == set(ATTRIBUTES)
    assert {
        "timestamp",
        "location_long",
        "location_lat",
        "individual_id",
        "individual_local_identifier",
        "tag_id",
        "tag_local_identifier",
        "visible",
    } == set(ATTRIBUTES)


def test_csv_header_validation(tmp_path: Path):
    path = tmp_path / "ok.csv"
    path.write_text(
        ",".join(ATTRIBUTES) + "\n"
        "2020-01-01 00:00:00.000,-70,60,1,a,2,b,true\n",
        encoding="utf-8",
    )
    header = validate_csv_header(path)
    assert set(header) == set(ATTRIBUTES)


def test_csv_header_missing_visible_fails(tmp_path: Path):
    path = tmp_path / "bad.csv"
    header = [x for x in ATTRIBUTES if x != "visible"]
    path.write_text(",".join(header) + "\n", encoding="utf-8")
    with pytest.raises(MaterializationBlocked, match="visible"):
        validate_csv_header(path)
