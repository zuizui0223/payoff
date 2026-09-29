#!/usr/bin/env python3
"""Probe the 2026 Dryad same-experiment snow-goose source.

Metadata/file-manifest only. No table rows are opened.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote

import requests


DOI = "10.5061/dryad.c2fqz61jr"
BASE = "https://datadryad.org/api/v2"
REQUIRED_NAMES = {
    "data_exp_Feb2025.txt",
    "cond2009_July2024.txt",
    "CortFitness_April2025_clean2.R",
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_snow_goose_2026_dryad_manifest.json"
        ),
    )
    return p.parse_args()


def request_json(session, url):
    try:
        response = session.get(url, timeout=60)
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": None,
            "json": None,
            "error": type(exc).__name__,
            "url": url,
        }
    payload = None
    if response.ok:
        try:
            payload = response.json()
        except ValueError:
            pass
    return {
        "ok": bool(response.ok),
        "status": int(response.status_code),
        "json": payload,
        "error": None,
        "url": str(response.url),
    }


def embedded(payload, key):
    if not isinstance(payload, dict):
        return []
    return (payload.get("_embedded") or {}).get(key) or []


def main():
    args = parse_args()
    encoded = quote("doi:" + DOI, safe="")
    dataset_url = f"{BASE}/datasets/{encoded}"
    session = requests.Session()
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": "PAYOFF-B-2026-Dryad-schema-probe/1.0",
    })

    dataset = request_json(session, dataset_url)
    versions = request_json(session, dataset_url + "/versions")
    version_rows = embedded(versions["json"], "stash:versions")

    candidates = [
        row for row in version_rows
        if isinstance(row, dict)
        and str(row.get("versionStatus", "")).lower() == "published"
    ]
    if not candidates:
        candidates = [row for row in version_rows if isinstance(row, dict)]

    selected = None
    if candidates:
        selected = max(
            candidates,
            key=lambda row: (
                row.get("versionNumber")
                if isinstance(row.get("versionNumber"), int) else -1,
                row.get("id") if isinstance(row.get("id"), int) else -1,
            ),
        )

    files_result = None
    files = []
    if selected and selected.get("id") is not None:
        files_result = request_json(
            session,
            f"{BASE}/versions/{selected['id']}/files",
        )
        for row in embedded(files_result["json"], "stash:files"):
            if not isinstance(row, dict):
                continue
            links = row.get("_links") or {}
            download = links.get("stash:download") or {}
            files.append({
                "id": row.get("id"),
                "path": row.get("path"),
                "size": row.get("size"),
                "mimeType": row.get("mimeType"),
                "digest": row.get("digest"),
                "digestType": row.get("digestType"),
                "download_href": download.get("href"),
            })

    names = {
        str(row.get("path"))
        for row in files
        if row.get("path") is not None
    }
    missing = sorted(REQUIRED_NAMES - names)

    result = {
        "probe_id": "payoff_b_snow_goose_2026_dryad_manifest_v1",
        "date": "2026-09-30",
        "doi": DOI,
        "dataset_http_status": dataset.get("status"),
        "versions_http_status": versions.get("status"),
        "files_http_status": (
            files_result.get("status") if files_result else None
        ),
        "selected_version": {
            "id": selected.get("id"),
            "versionNumber": selected.get("versionNumber"),
            "versionStatus": selected.get("versionStatus"),
        } if selected else None,
        "file_count": len(files),
        "files": files,
        "required_names": sorted(REQUIRED_NAMES),
        "missing_required_names": missing,
        "classification": (
            "PUBLIC_J_MECHANISM_SOURCE_READY"
            if files and not missing
            else "PUBLIC_J_MECHANISM_SOURCE_UNRESOLVED"
        ),
        "claim_boundary": [
            "manifest only; no table rows opened",
            "2009 source cannot replace the frozen 3-year duration-fitness gate",
            "future fed-only analysis is J-like physiology only",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
