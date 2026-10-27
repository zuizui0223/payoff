#!/usr/bin/env python3
"""Outcome-blind DataCite metadata screen for Movebank parent package DOIs.

This is a complete metadata-source audit, not a tracking-data analysis.
Parent and child DOIs are never treated as independent biological samples.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import unicodedata
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path

from scripts.build_movebank_doi_registry import (
    API_ROOT, MAX_PAGES, MAX_RECORDS, PER_PAGE, PREFIX,
    _fetch_json, parse_doi_record,
)

KNOWN_FOCAL_DOIS = {
    "10.5441/001/1.5d3f0664": "PREVIOUS_V7_KOLZSCH_2015",
    "10.5441/001/1.5k6b1364": "PREVIOUS_V7_KOLZSCH_2015",
    "10.5441/001/1.ps244r11": "PREVIOUS_V7_KOLZSCH_2015",
    "10.5441/001/1.137cn005": "PREVIOUS_V4_PUBLICATION_SCREEN",
}

HINTS = {
    "bird": r"\b(bird|avian|goos\w*|gees\w*|duck\w*|wader\w*|shorebird\w*|songbird\w*|swallow\w*|flycatcher\w*|godwit\w*|curlew\w*|warbler\w*|shrike\w*|wheatear\w*|sandpiper\w*|woodcock\w*|redstart\w*|rosefinch\w*|stork\w*|tern\w*|petrel\w*|albatross\w*|snipe\w*|sparrow\w*|passerine\w*|waterfowl|dunlin|mallard\w*|eagle\w*|falcon\w*)\b",
    "annual_migration": r"\b(migrat\w*|annual cycle|flyway\w*|stopover\w*|winter\w*|spring passage|return journey|long.distance movement\w*)\b",
    "forecast_cues": r"\b(phenolog\w*|green.wave|vegetation|spring onset|weather|climat\w*|temperature|warming|thermal\w*|wind\w*|rainfall|snow\w*|environmental cue\w*|information|forecast\w*|predict\w*|photoperiod|day length)\b",
    "commitment": r"\b(depart\w*|arrival|arriv\w*|stopover\w*|migrat\w* timing|decision\w*|onset|schedule|when to leave|temporal\w*|annual timing|spring migration)\b",
    "recourse": r"\b(speed|fast\w*|slow\w*|stopover\w*|duration|pace|accelerat\w*|compensat\w*|route\w*|travel\w*|flight\w*|detour\w*|delay\w*|flexib\w*)\b",
    "fitness": r"\b(fitness|surviv\w*|reproduct\w*|breeding success|nest\w* success|mortality|fecund\w*|life.history|body condition|fat|energetic\w*)\b",
    "sensor": r"\b(gps|argos|satellite.track\w*|geolocat\w*|radiotelemetry|radio.telemetry|telemetry|tracking|acceleromet\w*)\b",
}
REGEX = {k: re.compile(v, re.I) for k, v in HINTS.items()}
FILE_EXT = re.compile(r"\.(csv|tsv|txt|json|zip|rds|xlsx|kml|gpx)(?:\b|$)", re.I)
HTML_TAGS = re.compile(r"<[^>]+>")
WHITESPACE = re.compile(r"\s+")


def metadata_text(value):
    return WHITESPACE.sub(" ", html.unescape(HTML_TAGS.sub(" ", str(value or "")))).strip()


def list_text(attrs, key, field):
    v = attrs.get(key) or []
    if not isinstance(v, list):
        return ""
    return "; ".join(metadata_text(row.get(field)) for row in v
                     if isinstance(row, dict) and row.get(field))


def collect_raw_dois(fetch=_fetch_json):
    """Fail closed unless all DOI records and stable DataCite pages are read."""
    query = urllib.parse.urlencode({
        "prefix": PREFIX, "page[size]": PER_PAGE, "page[number]": 1
    })
    next_url, total, pages, records = API_ROOT + "?" + query, None, 0, {}
    while next_url:
        parts = urllib.parse.urlparse(next_url)
        if (parts.scheme != "https" or parts.netloc != "api.datacite.org"
                or parts.path != "/dois"):
            raise ValueError("unexpected DataCite pagination URL")
        pages += 1
        if pages > MAX_PAGES:
            raise ValueError("pagination limit exceeded")
        payload = fetch(next_url)
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("unexpected DOI API payload")
        reported = (payload.get("meta") or {}).get("total")
        if reported is not None:
            if total is not None and int(reported) != total:
                raise ValueError("DataCite total changed mid-census")
            total = int(reported)
        for item in payload["data"]:
            norm = parse_doi_record(item)
            doi = norm["doi"]
            if doi in records:
                raise ValueError("duplicate DOI in API census: " + doi)
            records[doi] = (item, norm)
        if len(records) > MAX_RECORDS:
            raise ValueError("DOI count exceeded declared safety bound")
        next_url = (payload.get("links") or {}).get("next")
        if next_url and not payload["data"]:
            raise ValueError("empty page with further pagination")
    if total is None or len(records) != total:
        raise ValueError("incomplete DOI census")
    return records, pages


def source_family_key(title):
    title = metadata_text(title)
    title = re.sub(r"^Data from:\s*", "", title, flags=re.I)
    title = re.sub(r"\s*\[[^]]+\]\s*$", "", title)
    title = unicodedata.normalize("NFKD", title).casefold()
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return " ".join(title.split())[:170]


def related_publication_dois(attrs):
    matched = set()
    for row in attrs.get("relatedIdentifiers") or []:
        if not isinstance(row, dict):
            continue
        if str(row.get("relatedIdentifierType", "")).upper() != "DOI":
            continue
        doi = metadata_text(row.get("relatedIdentifier")).lower()
        doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi)
        if doi and not doi.startswith("10.5441/"):
            matched.add(doi)
    return sorted(matched)


def child_file_info(item):
    attrs = item.get("attributes") or {}
    titles = list_text(attrs, "titles", "title")
    description = list_text(attrs, "descriptions", "description")
    ext = sorted({x.lower() for x in FILE_EXT.findall(titles + " " + description)})
    formats = attrs.get("formats") or []
    if not isinstance(formats, list):
        formats = []
    sizes = attrs.get("sizes") or []
    return {
        "titles": titles[:600],
        "extensions": ext,
        "formats": sorted(set(str(x) for x in formats if x))[:8],
        "sizes": sizes,
    }


def screen_package(base, parent_item, child_items):
    attrs = parent_item.get("attributes") or {}
    description = list_text(attrs, "descriptions", "description")
    subjects = list_text(attrs, "subjects", "subject")
    title = base["title"]
    corpus_text = " ".join((title, description, subjects))
    flags = {key: bool(rx.search(corpus_text)) for key, rx in REGEX.items()}
    bird = flags["bird"] or base["bird_keyword_hint"] == "True"
    migrating = flags["annual_migration"] or base["migration_keyword_hint"] == "True"
    cue, commitment = flags["forecast_cues"], flags["commitment"]
    if bird and migrating and cue and commitment:
        tier = "T1_CUE_AND_DECISION_METADATA"
    elif bird and migrating and commitment:
        tier = "T2_DECISION_METADATA"
    elif bird and migrating:
        tier = "T3_MIGRATION_METADATA"
    else:
        tier = "T4_OTHER_OR_UNCERTAIN"
    extensions = sorted({x for child in child_items for x in child["info"]["extensions"]})
    formats = sorted({x for child in child_items for x in child["info"]["formats"]})
    landing = str(attrs.get("url") or "").strip()
    if landing and not landing.startswith("https://"):
        landing = ""
    return {
        "doi": base["doi"],
        "title": title,
        "publication_year": base["publication_year"],
        "metadata_rights": base["rights_identifiers"],
        "metadata_landing_url": landing,
        "linked_publication_dois": "; ".join(related_publication_dois(attrs)),
        "title_family_review_key": source_family_key(title),
        "subject_metadata": subjects[:1000],
        "description_metadata": description[:1800],
        "n_child_doi_files": len(child_items),
        "child_format_hints": "; ".join(formats),
        "child_extension_hints": "; ".join(extensions),
        "bird_hint": bird,
        "migration_hint": migrating,
        "forecast_cue_hint": cue,
        "commitment_hint": commitment,
        "recourse_hint": flags["recourse"],
        "fitness_hint": flags["fitness"],
        "tracking_sensor_hint": flags["sensor"],
        "metadata_screen_tier": tier,
        "prior_payoff_source_flag": KNOWN_FOCAL_DOIS.get(base["doi"], "UNREVIEWED"),
        "access_study_and_event_permission": "NOT_VERIFIED",
        "animal_year_sensor_and_route": "NOT_VERIFIED",
        "actual_cue_before_decision": "NOT_VERIFIED",
        "independent_cohort": "NOT_VERIFIED",
        "actuator_and_vital_rate": "NOT_VERIFIED",
        "eligible_for_biological_inference": "NOT_ESTABLISHED",
    }


def build_stage2(candidate_rows, raw):
    parents, children = {}, defaultdict(list)
    for doi, (item, norm) in raw.items():
        if norm["is_movebank_parent"]:
            parents[doi] = item
        if norm["is_movebank_component_file"]:
            children[norm["parent_package_doi"]].append({
                "doi": doi,
                "info": child_file_info(item),
                "parent_doi": norm["parent_package_doi"],
            })
    base = {}
    for row in candidate_rows:
        doi = row["doi"].lower()
        if doi in base:
            raise ValueError("repeated parent in stage-1 source")
        base[doi] = row
    raw_candidates = {
        doi for doi, item in parents.items()
        if not str((((item.get("attributes") or {}).get("titles") or [{}])[0])
                   .get("title", "")).casefold().startswith("moveapps workflow:")
    }
    if set(base) != raw_candidates:
        raise ValueError(
            f"parent set changed between stage 1 and stage 2: "
            f"new={len(raw_candidates - set(base))} "
            f"missing={len(set(base) - raw_candidates)}"
        )
    rows = [
        screen_package(base[doi], parents[doi], children[doi])
        for doi in sorted(base)
    ]
    manifest = []
    for parent in sorted(base):
        for child in sorted(children[parent], key=lambda x: x["doi"]):
            manifest.append({
                "parent_doi": parent,
                "child_doi": child["doi"],
                "title_hint": child["info"]["titles"],
                "format_hints": "; ".join(child["info"]["formats"]),
                "extension_hints": "; ".join(child["info"]["extensions"]),
                "size_hints": "; ".join(str(x) for x in child["info"]["sizes"]),
                "track_data_file_verified": False,
                "permission_verified": False,
            })
    return rows, manifest


def write_table(rows, path):
    if not rows:
        raise ValueError("refuse empty output")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_outputs(rows, manifest, pages, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    write_table(rows, out / "movebank_package_metadata_screen.csv")
    if manifest:
        write_table(manifest, out / "movebank_child_file_metadata.csv")
    review = sorted(rows, key=lambda r: (
        int(r["metadata_screen_tier"][1]),
        r["prior_payoff_source_flag"] != "UNREVIEWED",
        not r["fitness_hint"],
        not r["recourse_hint"],
        not r["tracking_sensor_hint"],
        r["doi"],
    ))
    queue = review[:40]
    write_table(queue, out / "movebank_review_queue_first40.csv")
    tiers = dict(sorted(Counter(r["metadata_screen_tier"] for r in rows).items()))
    summary = {
        "schema": "payoff_b_independent_tracking_metadata_screen_v1",
        "classification": "METADATA_ONLY_NOT_AN_ANIMAL_TRACK_ANALYSIS",
        "stage1_parent_packages_reconciled": len(rows),
        "stage2_datacite_pages": pages,
        "linked_child_doi_records": len(manifest),
        "tiers": tiers,
        "first_review_queue": len(queue),
        "cue_and_decision_hints": tiers.get("T1_CUE_AND_DECISION_METADATA", 0),
        "metadata_fitness_hints": sum(r["fitness_hint"] for r in rows),
        "candidate_package_rights_recorded": sum(
            r["metadata_rights"] != "NOT_RECORDED" for r in rows
        ),
        "prior_payoff_focal_package_dois_flagged": sum(
            r["prior_payoff_source_flag"] != "UNREVIEWED" for r in rows
        ),
        "raw_animal_tracks_loaded": 0,
        "independent_cohorts_verified": 0,
        "behavioral_and_fitness_outcomes_tested": 0,
        "limitations": [
            "Classification is metadata-based and can mislabel taxa, techniques or content.",
            "Child DOI records are files, not independent migration studies.",
            "Shared article DOIs and title families do not prove cohort identity.",
            "Metadata license does not independently establish per-event access consent.",
            "The review queue is not an analytic sample or a representative subset.",
            "No animal GPS, migration timestamps, behavioral outcomes or vital rates accessed.",
        ],
    }
    (out / "movebank_stage2_screen_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage1-candidates", type=Path, required=True)
    ap.add_argument(
        "--output-dir", type=Path, default=Path("outputs/payoff_b_independent_stage2")
    )
    args = ap.parse_args()
    with args.stage1_candidates.open(encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    raw, pages = collect_raw_dois()
    rows, manifest = build_stage2(candidates, raw)
    print(json.dumps(save_outputs(rows, manifest, pages, args.output_dir),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
