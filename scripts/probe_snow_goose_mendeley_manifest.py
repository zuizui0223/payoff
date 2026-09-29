#!/usr/bin/env python3
"""Probe the public Mendeley/Digital Commons snow-goose dataset.

Metadata only.  This script does not fit ecological models.  It records the
public dataset identity and file manifest for DOI 10.17632/ycxxrg8497.1 so a
separate, pre-specified hidden-deadline auxiliary analysis can be designed
without opening response values opportunistically.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests


ARTICLE_DOI = "10.1016/j.biocon.2023.110240"
DATASET_DOI = "10.17632/ycxxrg8497.1"
SLUG = "ycxxrg8497"
API = "https://api.data.mendeley.com"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_snow_goose_mendeley_manifest_probe.json"
        ),
    )
    return p.parse_args()


def get_json(session, url, **params):
    try:
        r = session.get(url, params=params, timeout=60)
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": None,
            "error": type(exc).__name__,
            "text_prefix": None,
            "json": None,
        }
    payload = None
    if r.ok:
        try:
            payload = r.json()
        except ValueError:
            payload = None
    return {
        "ok": bool(r.ok),
        "status": int(r.status_code),
        "error": None,
        "text_prefix": r.text[:300] if not r.ok else None,
        "json": payload,
    }


def slim_file(row):
    if not isinstance(row, dict):
        return None
    content = row.get("content_details") or {}
    return {
        "id": row.get("id"),
        "filename": row.get("filename"),
        "description": row.get("description"),
        "size": row.get("size") or content.get("size"),
        "content_type": content.get("content_type"),
        "sha256_hash": content.get("sha256_hash"),
        # Record whether a public download URL is supplied, but do not emit a
        # short-lived signed URL into repository provenance.
        "has_download_url": bool(content.get("download_url")),
    }


def main():
    args = parse_args()
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "PAYOFF-B-public-mendeley-manifest-probe/1.0",
            "Accept": "application/json",
        }
    )

    discovery = get_json(
        session,
        f"{API}/datasets/publics",
        article_doi=ARTICLE_DOI,
        **{"$limit": 20},
    )

    candidates = []
    if isinstance(discovery.get("json"), list):
        candidates = [
            x for x in discovery["json"] if isinstance(x, dict)
        ]

    # The human-facing public slug often also resolves directly.  Probe it
    # regardless so the manifest records whether the current API accepts it.
    direct = get_json(
        session,
        f"{API}/datasets/{SLUG}",
        version=1,
    )
    direct_public = get_json(
        session,
        f"{API}/datasets/publics/{SLUG}",
        version=1,
    )

    dataset_id = None
    dataset_meta = None
    for source in (direct, direct_public):
        row = source.get("json")
        if source.get("ok") and isinstance(row, dict):
            dataset_id = row.get("id") or SLUG
            dataset_meta = row
            break

    if dataset_id is None:
        for row in candidates:
            doi = row.get("doi")
            doi_value = (
                doi.get("id") if isinstance(doi, dict) else doi
            )
            if (
                str(doi_value).lower() == DATASET_DOI.lower()
                or str(row.get("name", "")).lower().find("snow geese") >= 0
            ):
                dataset_id = row.get("id")
                dataset_meta = row
                break

    files_probe = None
    file_manifest = []
    if dataset_id:
        files_probe = get_json(
            session,
            f"{API}/datasets/{dataset_id}/files",
            version=1,
            **{"$limit": 100},
        )
        if not files_probe["ok"]:
            files_probe = get_json(
                session,
                f"{API}/datasets/publics/{dataset_id}/files",
                version=1,
                **{"$limit": 100},
            )
        if isinstance(files_probe.get("json"), list):
            file_manifest = [
                slim_file(x)
                for x in files_probe["json"]
                if slim_file(x) is not None
            ]

    meta_summary = None
    if isinstance(dataset_meta, dict):
        doi = dataset_meta.get("doi")
        doi_value = doi.get("id") if isinstance(doi, dict) else doi
        meta_summary = {
            "id": dataset_meta.get("id"),
            "name": dataset_meta.get("name"),
            "version": dataset_meta.get("version"),
            "doi": doi_value,
            "description_prefix": (
                str(dataset_meta.get("description"))[:500]
                if dataset_meta.get("description") is not None
                else None
            ),
        }

    if file_manifest:
        classification = "PUBLIC_FILE_MANIFEST_RESOLVED"
    elif dataset_id:
        classification = "DATASET_RESOLVED_FILE_MANIFEST_UNAVAILABLE"
    else:
        classification = "PUBLIC_DATASET_ID_UNRESOLVED"

    result = {
        "probe_id": "payoff_b_snow_goose_mendeley_manifest_v1",
        "date": "2026-09-29",
        "article_doi": ARTICLE_DOI,
        "dataset_doi": DATASET_DOI,
        "human_slug": SLUG,
        "classification": classification,
        "discovery_http_status": discovery["status"],
        "direct_slug_http_status": direct["status"],
        "direct_public_slug_http_status": direct_public["status"],
        "resolved_dataset_id": dataset_id,
        "dataset": meta_summary,
        "file_count": len(file_manifest),
        "files": file_manifest,
        "claim_boundary": [
            "metadata/file manifest only",
            "no ecological response model fitted",
            "body condition and behavior are D-like state information, not PAYOFF-B D",
            "this auxiliary lane cannot identify q_wait(D)",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
