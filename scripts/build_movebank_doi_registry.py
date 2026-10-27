#!/usr/bin/env python3
"""Build an outcome-blind DOI inventory for independent migratory tracking data.

This inventories DataCite *metadata*, not GPS events. In particular, DOI titles,
keywords and licenses do not establish animal taxon, raw-data permissions,
tracked route, temporal overlap, cue availability, or evolutionary fitness.

Run:
  python scripts/build_movebank_doi_registry.py --output-dir outputs/movebank
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

API_ROOT = "https://api.datacite.org/dois"
PREFIX = "10.5441"
PER_PAGE = 1000
MAX_RECORDS = 5000
MAX_PAGES = 25
# The 10.5441 DOI prefix is shared with OpenProceedings.org. A Movebank
# dataset *package* has a top-level DOI; /1, /2, ... are child files.
MOVEBANK_PARENT_RE = re.compile(r"^10\.5441/001/1\.[^/]+$")
MOVEBANK_CHILD_RE = re.compile(r"^(10\.5441/001/1\.[^/]+)/[0-9]+$")

HEADERS = {
    "Accept": "application/vnd.api+json",
    "User-Agent": "PAYOFF-independent-movement-inventory/0.1 "
    "(https://github.com/zuizui0223/payoff)",
}

COLUMNS = (
    "doi", "parent_package_doi", "title", "publisher", "publication_year", "resource_type",
    "is_movebank_parent", "is_movebank_component_file",
    "candidate_package_record", "moveapps_workflow_record",
    "rights_identifiers", "license_metadata_present", "bird_keyword_hint",
    "migration_keyword_hint", "tracking_keyword_hint",
    "dataset_record", "raw_event_permission_verified",
    "animal_taxon_verified", "route_timestamps_verified",
    "doi_url", "metadata_url",
)

BIRD_RE = re.compile(
    r"\b(birds?|avian|waterfowl|geese?|goose|storks?|ducks?|"
    r"shorebirds?|swallows?|flycatchers?|warblers?|gulls?|"
    r"waders?|eagles?|falcons?|raptors?|songbirds?|"
    r"godwits?|sandpipers?|terns?|albatross(?:es)?)\b", re.I,
)
MIGRATION_RE = re.compile(
    r"\b(migrat\w*|seasonal movement|annual cycle|"
    r"stopover\w*|flyway\w*)\b", re.I,
)
TRACKING_RE = re.compile(
    r"\b(track\w*|gps|geolocator\w*|telemetry|"
    r"satellite tag\w*|animal movement\w*)\b", re.I,
)


def _strings(values, key):
    if values is None:
        return []
    if isinstance(values, dict):
        values = [values]
    if not isinstance(values, list):
        return []
    return [
        str(row.get(key, "")).strip()
        for row in values
        if isinstance(row, dict) and str(row.get(key, "")).strip()
    ]


def normalise_doi(doi):
    doi = str(doi).strip().lower()
    if doi.startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    if not doi.startswith(PREFIX + "/"):
        raise ValueError("DOI outside frozen Movebank prefix: " + doi)
    return doi


def parse_doi_record(item):
    if not isinstance(item, dict) or not isinstance(item.get("attributes"), dict):
        raise ValueError("invalid DataCite DOI item")
    a = item["attributes"]
    doi = normalise_doi(a.get("doi", item.get("id", "")))
    titles = _strings(a.get("titles"), "title")
    subjects = _strings(a.get("subjects"), "subject")
    descriptions = _strings(a.get("descriptions"), "description")
    rights = _strings(a.get("rightsList"), "rightsIdentifier")
    rights = rights + [
        r for r in _strings(a.get("rightsList"), "rights")
        if r not in rights
    ]
    resource_type = str(
        (a.get("types") or {}).get("resourceTypeGeneral")
        or (a.get("types") or {}).get("resourceType")
        or "UNSPECIFIED"
    )
    year = a.get("publicationYear")
    title = titles[0] if titles else "UNTITLED"
    publisher = str(a.get("publisher") or "UNKNOWN")
    movebank = publisher.strip().casefold() == "movebank data repository"
    is_parent = bool(movebank and MOVEBANK_PARENT_RE.fullmatch(doi))
    child_match = MOVEBANK_CHILD_RE.fullmatch(doi) if movebank else None
    is_child = child_match is not None
    parent_package_doi = doi if is_parent else (
        child_match.group(1) if child_match else ""
    )
    is_workflow = bool(
        is_parent and title.casefold().startswith("moveapps workflow:")
    )
    package_candidate = is_parent and not is_workflow
    # Hints aid *manual data discovery*, never automatic taxon exclusions.
    search_text = " ".join([title, *subjects, *descriptions])
    return {
        "doi": doi,
        "title": title,
        "publisher": publisher,
        "parent_package_doi": parent_package_doi,
        "is_movebank_parent": is_parent,
        "is_movebank_component_file": is_child,
        "candidate_package_record": package_candidate,
        "moveapps_workflow_record": is_workflow,
        "publication_year": str(year) if year is not None else "",
        "resource_type": resource_type,
        "rights_identifiers": "; ".join(sorted(set(rights))) or "NOT_RECORDED",
        "license_metadata_present": bool(rights),
        "bird_keyword_hint": bool(BIRD_RE.search(search_text)),
        "migration_keyword_hint": bool(MIGRATION_RE.search(search_text)),
        "tracking_keyword_hint": bool(TRACKING_RE.search(search_text)),
        "dataset_record": resource_type.casefold() == "dataset",
        # Rights metadata DOES NOT certify access at the event/animal level.
        "raw_event_permission_verified": False,
        "animal_taxon_verified": False,
        "route_timestamps_verified": False,
        "doi_url": "https://doi.org/" + doi,
        "metadata_url": "https://api.datacite.org/dois/" + doi,
    }


def _fetch_json(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, timeout=55) as response:
                return json.load(response)
        except (OSError, TimeoutError, urllib.error.URLError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
    raise AssertionError("unreachable")


def collect_dois(fetch=_fetch_json):
    params = urllib.parse.urlencode(
        {"prefix": PREFIX, "page[size]": PER_PAGE, "page[number]": 1}
    )
    next_url = API_ROOT + "?" + params
    records = {}
    expected_total = None
    pages = 0
    while next_url:
        parsed = urllib.parse.urlparse(next_url)
        if parsed.scheme != "https" or parsed.hostname != "api.datacite.org":
            raise ValueError("DataCite pagination redirected outside API")
        pages += 1
        if pages > MAX_PAGES:
            raise ValueError("DataCite pagination exceeded frozen limit")
        payload = fetch(next_url)
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("unexpected DataCite response")
        reported_total = (payload.get("meta") or {}).get("total")
        if reported_total is not None:
            if expected_total is None:
                expected_total = int(reported_total)
            elif int(reported_total) != expected_total:
                raise ValueError("DataCite total changed during pagination")
        for item in payload["data"]:
            row = parse_doi_record(item)
            if row["doi"] in records:
                raise ValueError("DOI repeated on multiple DataCite pages")
            records[row["doi"]] = row
        if len(records) > MAX_RECORDS:
            raise ValueError("unexpected corpus size; review discovery policy")
        next_url = (payload.get("links") or {}).get("next")
        if next_url and not isinstance(next_url, str):
            raise ValueError("invalid next-page link")
        if not payload["data"] and next_url:
            raise ValueError("empty DataCite page with next-page link")
    if expected_total is None:
        raise ValueError("DataCite omitted corpus total")
    if len(records) != expected_total:
        raise ValueError(
            f"DataCite corpus incomplete: {len(records)} of {expected_total}"
        )
    return [records[key] for key in sorted(records)], pages


def write_registry(rows, pages, output_dir):
    dest = Path(output_dir)
    dest.mkdir(parents=True, exist_ok=True)
    with (dest / "movebank_doi_registry.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    package_rows = [r for r in rows if r["candidate_package_record"]]
    with (dest / "movebank_parent_package_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(package_rows)

    publisher_counts = dict(sorted(Counter(r["publisher"] for r in rows).items()))
    summary = {
        "schema": "payoff_b_independent_movebank_doi_inventory_v1",
        "classification": "OUTCOME_BLIND_PUBLIC_METADATA_ONLY",
        "source": API_ROOT + "?prefix=" + PREFIX,
        "prefix": PREFIX,
        "pages": pages,
        "doi_records": len(rows),
        "publisher_doi_records": publisher_counts,
        "movebank_parent_dois": sum(r["is_movebank_parent"] for r in rows),
        "movebank_component_file_dois": sum(
            r["is_movebank_component_file"] for r in rows
        ),
        "moveapps_workflow_parent_dois": sum(
            r["moveapps_workflow_record"] for r in rows
        ),
        "movebank_parent_package_candidates": len(package_rows),
        "candidate_package_bird_keyword_hints": sum(
            r["bird_keyword_hint"] for r in package_rows
        ),
        "candidate_package_migration_keyword_hints": sum(
            r["migration_keyword_hint"] for r in package_rows
        ),
        "candidate_package_bird_migration_keyword_overlap": sum(
            r["bird_keyword_hint"] and r["migration_keyword_hint"]
            for r in package_rows
        ),
        "dataset_records": sum(r["dataset_record"] for r in rows),
        "migration_keyword_hints": sum(r["migration_keyword_hint"] for r in rows),
        "bird_keyword_hints": sum(r["bird_keyword_hint"] for r in rows),
        "bird_migration_keyword_overlap": sum(
            r["bird_keyword_hint"] and r["migration_keyword_hint"]
            for r in rows
        ),
        "tracking_keyword_hints": sum(r["tracking_keyword_hint"] for r in rows),
        "publication_year_counts": dict(sorted(Counter(
            r["publication_year"] or "UNKNOWN" for r in rows
        ).items())),
        "raw_event_permission_verified": 0,
        "route_validated": 0,
        "biological_outcomes_measured": 0,
        "limitations": [
            "10.5441 is shared by Movebank, OpenProceedings and other publishers; "
            "the prefix is not a repository-specific inclusion criterion.",
            "Movebank package parent DOIs and child file DOIs are not independent "
            "datasets; component files are excluded from package candidates.",
            "Even one parent DOI need not mean one independent biological cohort.",
            "DOI counts and keyword hints are not biological study sample sizes.",
            "A DOI can reference multiple files, animals, species or analyses.",
            "The DataCite publication year is not a tracking-data collection year.",
            "No track downloads are attempted; license terms and per-study data "
            "permissions require separate review before any reuse.",
            "Latin species names and studies without English migration terms "
            "remain in the FULL inventory; keyword hints are not exclusions.",
            "No spring cue, actual stopover, phase error, behavioral correction, "
            "survival or reproduction is estimated by this stage.",
        ],
    }
    (dest / "movebank_registry_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default="outputs/payoff_b_independent_movebank",
    )
    args = parser.parse_args()
    rows, pages = collect_dois()
    summary = write_registry(rows, pages, args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
