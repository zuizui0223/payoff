"""Offline integrity checks: no raw tracking or outcome access."""
from __future__ import annotations

import csv
from pathlib import Path
import pytest
from scripts.screen_movebank_package_metadata import (
    build_stage2, collect_raw_dois, related_publication_dois,
    save_outputs, screen_package, source_family_key,
)
from scripts.build_movebank_doi_registry import parse_doi_record


def item(doi, title, text="GPS tracking of migratory birds from spring"):
    return {
        "id": doi,
        "attributes": {
            "doi": doi, "titles": [{"title": title}],
            "publisher": "Movebank Data Repository", "publicationYear": 2020,
            "types": {"resourceTypeGeneral": "Dataset"},
            "subjects": [{"subject": "GPS tracking"}],
            "descriptions": [{"description": text}],
            "relatedIdentifiers": [{"relatedIdentifierType": "DOI",
                                    "relatedIdentifier": "10.1111/example-paper"}],
            "rightsList": [{"rightsIdentifier": "cc0-1.0"}],
        }
    }


def normalized(items):
    return {x["id"]: (x, parse_doi_record(x)) for x in items}


def base(doi, title):
    return {"doi": doi, "title": title, "rights_identifiers": "cc0-1.0",
            "publication_year": "2020", "bird_keyword_hint": "True",
            "migration_keyword_hint": "True"}


def test_full_census_and_pagination():
    x = item("10.5441/001/1.test1", "Bird migration weather and stopover")
    y = item("10.5441/001/1.test1/1", "bird file.csv")
    calls = []
    def fetch(url):
        calls.append(url)
        return ({
            "data": [x], "meta": {"total": 2},
            "links": {"next": "https://api.datacite.org/dois?page%5Bnumber%5D=2"}
        } if len(calls) == 1 else
        {"data": [y], "meta": {"total": 2}, "links": {}})
    records, pages = collect_raw_dois(fetch)
    assert pages == 2 and len(records) == 2


def test_missing_parent_fails_closed():
    with pytest.raises(ValueError, match="parent set changed"):
        build_stage2([], normalized([
            item("10.5441/001/1.test1", "Bird migration")
        ]))


def test_parent_child_file_is_not_a_biological_replicate():
    title = "Data from: Spring migration weather and stopover decisions in geese"
    parent = item("10.5441/001/1.test1", title)
    child = item("10.5441/001/1.test1/1", "bird_locations.csv")
    rows, manifest = build_stage2(
        [base(parent["id"], title)], normalized([parent, child])
    )
    assert len(rows) == len(manifest) == 1
    assert rows[0]["metadata_screen_tier"] == "T1_CUE_AND_DECISION_METADATA"
    assert rows[0]["n_child_doi_files"] == 1
    assert rows[0]["access_study_and_event_permission"] == "NOT_VERIFIED"
    assert rows[0]["eligible_for_biological_inference"] == "NOT_ESTABLISHED"
    assert manifest[0]["extension_hints"] == "csv"
    assert not manifest[0]["track_data_file_verified"]


def test_shared_article_and_title_family_are_a_review_signal_only():
    title = "Data from: Forecasting spring from afar? [Greenland data]"
    assert source_family_key(title) == source_family_key(
        "Data from: Forecasting spring from afar? [Svalbard data]"
    )
    assert related_publication_dois(item(
        "10.5441/001/1.test1", title
    )["attributes"]) == ["10.1111/example-paper"]


def test_text_cue_not_misreported_as_observed_action_or_independence():
    title = "Data from: Migration timing and climate response in geese"
    record = item("10.5441/001/1.test1", title)
    row = screen_package(base(record["id"], title), record, [])
    assert row["forecast_cue_hint"]
    assert row["animal_year_sensor_and_route"] == "NOT_VERIFIED"
    assert row["independent_cohort"] == "NOT_VERIFIED"


def test_first40_never_excludes_original_full_corpus(tmp_path: Path):
    rows = []
    for i in range(45):
        doi = f"10.5441/001/1.test{i}"
        title = "Migration and stopover climate in geese" if i % 2 else "Fish home range"
        rows.append(screen_package(base(doi, title), item(doi, title), []))
    result = save_outputs(rows, [], 3, tmp_path)
    assert result["stage1_parent_packages_reconciled"] == 45
    assert result["first_review_queue"] == 40
    with (tmp_path / "movebank_package_metadata_screen.csv").open() as f:
        assert len(list(csv.DictReader(f))) == 45
    with (tmp_path / "movebank_review_queue_first40.csv").open() as f:
        assert len(list(csv.DictReader(f))) == 40
    assert result["raw_animal_tracks_loaded"] == 0
