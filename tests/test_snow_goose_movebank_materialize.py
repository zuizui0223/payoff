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
    validate_output_dir,
)
from scripts.validate_greater_snow_goose_movebank_manifest import (
    validate_manifest,
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


def test_raw_output_must_be_outside_repo(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    inside = repo / "raw"
    with pytest.raises(ValueError, match="outside the Git repository"):
        validate_output_dir(inside, repo_root=repo)

    outside = tmp_path / "private_raw"
    assert validate_output_dir(outside, repo_root=repo) == outside.resolve()


def complete_manifest():
    files = []
    for index, year in enumerate(range(2019, 2024), start=1):
        files.append(
            {
                "year": year,
                "status": "MATERIALIZED",
                "path": f"greater_snow_goose_movebank_{year}.csv",
                "bytes": index * 100,
                "rows": index * 10,
                "sha256": f"{index:064x}",
                "header": list(ATTRIBUTES),
            }
        )
    return {
        "status": "COMPLETE",
        "study_id": "1442516400",
        "sensor_type_id": "653",
        "event_data_opened": True,
        "years_requested": list(range(2019, 2024)),
        "files": files,
        "total_rows": sum(x["rows"] for x in files),
        "total_bytes": sum(x["bytes"] for x in files),
    }


def test_complete_manifest_passes():
    result = validate_manifest(complete_manifest())
    assert result["valid"]
    assert result["errors"] == []


def test_missing_year_fails_manifest_gate():
    payload = complete_manifest()
    payload["files"] = payload["files"][:-1]
    payload["total_rows"] = sum(x["rows"] for x in payload["files"])
    payload["total_bytes"] = sum(x["bytes"] for x in payload["files"])
    result = validate_manifest(payload)
    assert not result["valid"]
    assert "file_years_not_exactly_2019_2023" in result["errors"]


def test_bad_header_and_digest_fail_manifest_gate():
    payload = complete_manifest()
    payload["files"][0]["header"] = ["timestamp"]
    payload["files"][0]["sha256"] = "bad"
    result = validate_manifest(payload)
    assert not result["valid"]
    assert any(x.startswith("missing_header_fields:2019") for x in result["errors"])
    assert "invalid_sha256:2019" in result["errors"]
