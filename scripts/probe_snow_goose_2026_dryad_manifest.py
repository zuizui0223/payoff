#!/usr/bin/env python3
"""Probe the 2026 Dryad same-experiment snow-goose source.

Metadata/file-manifest only. No table rows are opened.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote, urljoin

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

    # Dryad's current public API exposes the canonical/latest version through
    # the dataset HAL link even when rows returned by /versions omit a literal
    # integer "id" field. Prefer the canonical HAL route.
    dataset_payload = (
        dataset.get("json")
        if isinstance(dataset.get("json"), dict)
        else {}
    )
    dataset_links = dataset_payload.get("_links") or {}
    latest_link = dataset_links.get("stash:version") or {}
    latest_href = latest_link.get("href")

    selected = None
    version_detail = None
    version_url = None

    if latest_href:
        version_url = urljoin("https://datadryad.org", str(latest_href))
        version_detail = request_json(session, version_url)
        if isinstance(version_detail.get("json"), dict):
            selected = version_detail["json"]

    if selected is None:
        candidates = [
            row for row in version_rows
            if isinstance(row, dict)
            and str(row.get("versionStatus", "")).lower() == "published"
        ]
        if not candidates:
            candidates = [
                row for row in version_rows
                if isinstance(row, dict)
            ]

        if candidates:
            selected = max(
                candidates,
                key=lambda row: (
                    row.get("versionNumber")
                    if isinstance(row.get("versionNumber"), int)
                    else -1
                ),
            )
            links = selected.get("_links") or {}
            self_link = links.get("self") or {}
            self_href = self_link.get("href")
            if self_href:
                version_url = urljoin(
                    "https://datadryad.org",
                    str(self_href),
                )
                version_detail = request_json(session, version_url)
                if isinstance(version_detail.get("json"), dict):
                    selected = version_detail["json"]

    files_result = None
    files = []
    if isinstance(selected, dict):
        selected_links = selected.get("_links") or {}
        files_link = selected_links.get("stash:files") or {}
        files_href = files_link.get("href")
        if not files_href and version_url:
            files_href = version_url.replace(
                "https://datadryad.org",
                "",
            ).rstrip("/") + "/files"

        if files_href:
            files_url = urljoin(
                "https://datadryad.org",
                str(files_href),
            )
            files_result = request_json(session, files_url)

        for row in embedded(
            files_result["json"] if files_result else None,
            "stash:files",
        ):
            if not isinstance(row, dict):
                continue
            links = row.get("_links") or {}
            download = links.get("stash:download") or {}
            download_href = download.get("href")
            files.append({
                "id": row.get("id"),
                "path": row.get("path"),
                "size": row.get("size"),
                "mimeType": row.get("mimeType"),
                "digest": row.get("digest"),
                "digestType": row.get("digestType"),
                "download_href": (
                    urljoin(
                        "https://datadryad.org",
                        str(download_href),
                    )
                    if download_href
                    else None
                ),
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
            "version_url": version_url,
            "detail_http_status": (
                version_detail.get("status")
                if version_detail
                else None
            ),
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
