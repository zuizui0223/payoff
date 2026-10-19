"""Offline contract tests for the public Movebank DOI metadata inventory."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_movebank_doi_registry import (
    collect_dois, normalise_doi, parse_doi_record, write_registry,
)


def fixture(
    doi="10.5441/001/1.abcdef12",
    title="Migration timing in barnacle geese (Svalbard)",
    rights=True,
):
    return {
        "id": doi,
        "attributes": {
            "doi": doi,
            "titles": [{"title": title}],
            "subjects": [{"subject": "GPS animal tracking"}],
            "descriptions": [{"description": "Animal movement research"}],
            "publicationYear": 2022,
            "publisher": "Movebank Data Repository",
            "types": {"resourceTypeGeneral": "Dataset"},
            "rightsList": (
                [{"rightsIdentifier": "CC-BY-4.0"}] if rights else []
            ),
        },
    }


def test_doi_is_restricted_to_frozen_prefix():
    assert normalise_doi("https://doi.org/10.5441/001/1.abcdef12") == (
        "10.5441/001/1.abcdef12"
    )
    with pytest.raises(ValueError, match="outside"):
        normalise_doi("10.5061/dryad.abcdef")


def test_metadata_hints_do_not_establish_real_permissions_or_biology():
    row = parse_doi_record(fixture())
    assert row["dataset_record"]
    assert row["migration_keyword_hint"]
    assert row["bird_keyword_hint"]
    assert row["tracking_keyword_hint"]
    assert row["license_metadata_present"]
    assert row["raw_event_permission_verified"] is False
    assert row["animal_taxon_verified"] is False
    assert row["route_timestamps_verified"] is False


def test_non_english_or_latin_name_records_remain_even_without_hints():
    row = parse_doi_record(
        fixture(title="Studies of Anas platyrhynchos", rights=False)
    )
    assert not row["bird_keyword_hint"]
    assert row["rights_identifiers"] == "NOT_RECORDED"
    assert row["dataset_record"]


def test_collect_all_pages_without_keyword_filters():
    records = [fixture(), fixture(
        doi="10.5441/001/1.other000", title="Herbivore seasonal movement"
    )]
    calls = []

    def fetch(url):
        calls.append(url)
        if len(calls) == 1:
            return {
                "data": records[:1],
                "meta": {"total": 2},
                "links": {
                    "next": "https://api.datacite.org/dois?page[number]=2"
                },
            }
        return {
            "data": records[1:],
            "meta": {"total": 2},
            "links": {"next": None},
        }

    rows, pages = collect_dois(fetch)
    assert pages == 2
    assert len(rows) == 2
    assert rows[0]["doi"] != rows[1]["doi"]


def test_incomplete_pagination_fails_closed():
    def fetch(url):
        return {"data": [fixture()], "meta": {"total": 2}, "links": {}}

    with pytest.raises(ValueError, match="incomplete"):
        collect_dois(fetch)


def test_unapproved_next_url_fails_closed():
    def fetch(url):
        return {
            "data": [fixture()], "meta": {"total": 2},
            "links": {"next": "https://example.com/dois"},
        }

    with pytest.raises(ValueError, match="outside API"):
        collect_dois(fetch)


def test_output_is_explicitly_metadata_only(tmp_path: Path):
    summary = write_registry([parse_doi_record(fixture())], 1, tmp_path)
    loaded = json.loads(
        (tmp_path / "movebank_registry_summary.json").read_text("utf-8")
    )
    assert summary == loaded
    assert summary["doi_records"] == 1
    assert summary["raw_event_permission_verified"] == 0
    assert summary["biological_outcomes_measured"] == 0
    assert "animal_taxon_verified" in (
        tmp_path / "movebank_doi_registry.csv"
    ).read_text("utf-8")
