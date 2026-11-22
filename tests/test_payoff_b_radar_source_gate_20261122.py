"""Source provenance and admission guardrails; no source rows or animal effects."""
from __future__ import annotations
import io
import zipfile

import pytest

from scripts import payoff_b_radar_source_gate_20261122 as s


def test_reject_unverified_urls_without_fetching():
    with pytest.raises(ValueError, match="allowlisted"):
        s.bounded_download("https://example.org/evil.csv", cap=100)


def test_capture_csv_column_names_not_raw_identifiers():
    data = (
        "station,year,passage_spring50,greenup_doy,temperature\n"
        "SECRET_STATION,2019,103,101,17\n"
        "ANOTHER_STATION,2020,102,105,15\n"
    ).encode()
    obj = s.csv_schema(data)
    assert obj["year_site_fields_verified"] is True
    assert obj["n_years"] == 2
    assert obj["n_sites"] == 2
    assert "SECRET_STATION" not in str(obj)
    assert "ANOTHER_STATION" not in str(obj)
    assert "2019,103" not in str(obj)


def test_unknown_join_keys_not_invented():
    obj = s.csv_schema(b"date,velocity,signal\n1,0.5,0.4\n")
    assert obj["year_site_fields_verified"] is False
    assert obj["n_sites"] is None


def test_zip_schema_inspection_bounds_and_traversal():
    with io.BytesIO() as out:
        with zipfile.ZipFile(out, "w") as z:
            z.writestr("data/measurements.csv", "year,station,greenup_doy\n2018,SECRET_SITE,112\n")
        good = out.getvalue()
    inspected = s.inspect_archive(good)
    assert inspected["member_count"] == 1
    assert inspected["members"][0]["schema"]["n_years"] == 1
    assert "SECRET_SITE" not in str(inspected)

    with io.BytesIO() as out:
        with zipfile.ZipFile(out, "w") as z:
            z.writestr("../unsafe.csv", "year,site\n2019,SECRET\n")
        evil = out.getvalue()
    with pytest.raises(ValueError, match="unsafe ZIP"):
        s.inspect_archive(evil)


def test_prefit_original_source_doi_is_pinned():
    assert s.ARTICLE_ID == 26050390
    assert s.API_URL == "https://api.figshare.com/v2/articles/26050390"
    assert s.MAX_BYTES <= 12_000_000
