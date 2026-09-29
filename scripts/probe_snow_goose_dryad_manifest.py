#!/usr/bin/env python3
"""Probe published Dryad metadata for the greater-snow-goose perturbation data.

Metadata/file-manifest only.  No table contents are opened here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote

import requests


DOI = "10.5061/dryad.cjsxksn6t"
BASE = "https://datadryad.org/api/v2"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_snow_goose_dryad_manifest_probe.json"
        ),
    )
    return p.parse_args()


def request_json(session, url):
    try:
        r = session.get(url, timeout=60)
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": None,
            "error": type(exc).__name__,
            "json": None,
            "url": url,
        }
    payload = None
    if r.ok:
        try:
            payload = r.json()
        except ValueError:
            pass
    return {
        "ok": bool(r.ok),
        "status": int(r.status_code),
        "error": None,
        "json": payload,
        "url": str(r.url),
    }


def embedded(payload, key):
    if not isinstance(payload, dict):
        return []
    emb = payload.get("_embedded") or {}
    rows = emb.get(key) or []
    return rows if isinstance(rows, list) else []


def main():
    args = parse_args()
    encoded = quote("doi:" + DOI, safe="")
    dataset_url = f"{BASE}/datasets/{encoded}"

    session = requests.Session()
    session.headers.update({
        "User-Agent": "PAYOFF-B-Dryad-manifest-probe/1.0",
        "Accept": "application/json",
    })

    dataset = request_json(session, dataset_url)
    versions = request_json(session, dataset_url + "/versions")

    version_rows = embedded(versions["json"], "stash:versions")
    version_summaries = []
    for row in version_rows:
        if not isinstance(row, dict):
            continue
        version_summaries.append({
            "id": row.get("id"),
            "versionNumber": row.get("versionNumber"),
            "versionStatus": row.get("versionStatus"),
            "publicationDate": row.get("publicationDate"),
            "lastModificationDate": row.get("lastModificationDate"),
        })

    published = [
        x for x in version_summaries
        if str(x.get("versionStatus", "")).lower() == "published"
    ]
    candidates = published or version_summaries
    selected = None
    if candidates:
        selected = max(
            candidates,
            key=lambda x: (
                x.get("versionNumber")
                if isinstance(x.get("versionNumber"), int)
                else -1,
                x.get("id") if isinstance(x.get("id"), int) else -1,
            ),
        )

    files_result = None
    files = []
    if selected and selected.get("id") is not None:
        files_result = request_json(
            session,
            f"{BASE}/versions/{selected['id']}/files",
        )
        file_rows = embedded(files_result["json"], "stash:files")
        for row in file_rows:
            if not isinstance(row, dict):
                continue
            links = row.get("_links") or {}
            download = links.get("stash:download") or {}
            files.append({
                "id": row.get("id"),
                "path": row.get("path"),
                "size": row.get("size"),
                "mimeType": row.get("mimeType"),
                "status": row.get("status"),
                "digest": row.get("digest"),
                "digestType": row.get("digestType"),
                "download_href": download.get("href"),
            })

    meta = dataset.get("json") if isinstance(dataset.get("json"), dict) else {}
    result = {
        "probe_id": "payoff_b_snow_goose_dryad_manifest_v1_20260929",
        "date": "2026-09-29",
        "doi": DOI,
        "classification": (
            "PUBLIC_FILE_MANIFEST_RESOLVED"
            if files
            else "DRYAD_MANIFEST_UNRESOLVED"
        ),
        "dataset_http_status": dataset.get("status"),
        "versions_http_status": versions.get("status"),
        "files_http_status": (
            files_result.get("status") if files_result else None
        ),
        "dataset": {
            "identifier": meta.get("identifier"),
            "title": meta.get("title"),
            "versionNumber": meta.get("versionNumber"),
            "versionStatus": meta.get("versionStatus"),
            "publicationDate": meta.get("publicationDate"),
            "license": meta.get("license"),
            "storageSize": meta.get("storageSize"),
        },
        "versions": version_summaries,
        "selected_version": selected,
        "file_count": len(files),
        "files": files,
        "claim_boundary": [
            "file manifest only",
            "no data-table response values opened",
            "captivity duration remains D-like, not identified PAYOFF-B D",
            "analysis model must be frozen after manifest/README inspection and before response-value analysis",
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
