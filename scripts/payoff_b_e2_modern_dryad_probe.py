#!/usr/bin/env python3
"""Modern Dryad DOI-discovery probe for Samplonius & Both 2017.

Unlike the historical probe, this script never hard-codes Dryad file IDs.
It resolves the current dataset/version/file manifest from the DOI, matches
files by filename, downloads current links, and inspects source structure.

This is still a source-reproduction probe, not an outcome analysis.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests


DOI = "10.5061/dryad.bs427"
TARGETS = {
    "arrival_early_late.R": "code",
    "arrival.csv": "data",
    "arrorder.csv": "data",
    "population.csv": "data",
    "replicates.csv": "data",
    "swaps14.csv": "data",
    "swaps15.csv": "data",
}
API = "https://datadryad.org/api/v2"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _get_json(session, url):
    response = session.get(url, timeout=120)
    response.raise_for_status()
    return response.json(), {
        "url": url,
        "status_code": response.status_code,
        "final_url": response.url,
    }


def _link(obj, suffix):
    links = obj.get("_links", {})
    for key, value in links.items():
        if key.endswith(suffix):
            if isinstance(value, dict):
                return value.get("href")
            if isinstance(value, str):
                return value
    return None


def _embedded_list(obj):
    embedded = obj.get("_embedded", {})
    for value in embedded.values():
        if isinstance(value, list):
            return value
    return []


def inspect_csv(data: bytes) -> dict:
    last = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            df = pd.read_csv(io.BytesIO(data), encoding=enc)
            break
        except Exception as exc:
            last = repr(exc)
    else:
        return {"parse_error": last}

    low = {}
    for col in df.columns:
        values = df[col].dropna().unique()
        if len(values) <= 40:
            low[str(col)] = [str(x) for x in values[:50]]

    return {
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "dtypes": {str(c): str(df[c].dtype) for c in df.columns},
        "low_cardinality": low,
        "head": (
            df.head(8)
            .where(pd.notna(df.head(8)), None)
            .to_dict(orient="records")
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update({
        "User-Agent": "PAYOFF-B-modern-dryad-probe/1.0",
        "Accept": "application/json,text/csv,*/*",
    })

    result = {
        "probe_id": "payoff_b_e2_modern_dryad_probe_v1_20260930",
        "doi": DOI,
        "status": "UNRESOLVED",
        "dataset": None,
        "versions": [],
        "files": {},
        "diagnostics": [],
        "claim_boundary": [
            "source reproduction only",
            "no ecological model fit",
            "arrival timing is not D_eff",
            "experimental early/late treatment is not q_wait",
        ],
    }

    dataset_url = f"{API}/datasets/doi%3A{quote(DOI, safe='')}"
    try:
        dataset, diag = _get_json(session, dataset_url)
        result["diagnostics"].append({"stage": "dataset", **diag})
    except Exception as exc:
        result["status"] = "DATASET_METADATA_BLOCKED"
        result["error"] = repr(exc)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return

    result["dataset"] = {
        "identifier": dataset.get("identifier"),
        "title": dataset.get("title"),
        "versionNumber": dataset.get("versionNumber"),
        "versionStatus": dataset.get("versionStatus"),
    }

    versions_url = _link(dataset, "versions")
    versions = []
    if versions_url:
        try:
            versions_obj, diag = _get_json(session, versions_url)
            result["diagnostics"].append({"stage": "versions", **diag})
            versions = _embedded_list(versions_obj)
        except Exception as exc:
            result["diagnostics"].append({
                "stage": "versions",
                "error": repr(exc),
            })

    if not versions:
        versions = [dataset]

    result["versions"] = [
        {
            "versionNumber": v.get("versionNumber"),
            "versionStatus": v.get("versionStatus"),
            "id": v.get("id"),
        }
        for v in versions
    ]

    def version_key(v):
        value = v.get("versionNumber")
        try:
            return int(value)
        except Exception:
            return -1

    latest = sorted(versions, key=version_key)[-1]
    files_url = _link(latest, "files") or _link(dataset, "files")
    if not files_url:
        result["status"] = "FILES_LINK_UNRESOLVED"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return

    try:
        files_obj, diag = _get_json(session, files_url)
        result["diagnostics"].append({"stage": "files", **diag})
        manifest = _embedded_list(files_obj)
    except Exception as exc:
        result["status"] = "FILES_MANIFEST_BLOCKED"
        result["error"] = repr(exc)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return

    by_name = {}
    for row in manifest:
        path = row.get("path") or row.get("filename") or row.get("name")
        if path:
            by_name[Path(str(path)).name] = row

    acquired = 0
    for name, kind in TARGETS.items():
        row = by_name.get(name)
        entry = {
            "type": kind,
            "manifest_found": row is not None,
        }
        if row is None:
            entry["status"] = "NOT_IN_CURRENT_MANIFEST"
            result["files"][name] = entry
            continue

        entry["file_id"] = row.get("id")
        entry["path"] = row.get("path")
        entry["size"] = row.get("size")
        download_url = _link(row, "download")
        if not download_url and row.get("id") is not None:
            download_url = f"{API}/files/{row['id']}/download"
        entry["download_url"] = download_url

        if not download_url:
            entry["status"] = "DOWNLOAD_LINK_UNRESOLVED"
            result["files"][name] = entry
            continue

        try:
            response = session.get(
                download_url,
                timeout=120,
                allow_redirects=True,
            )
            entry["http_status"] = response.status_code
            entry["final_url"] = response.url
            entry["bytes"] = len(response.content)
            entry["content_type"] = response.headers.get("content-type")
            if (
                response.status_code == 200
                and response.content
                and b"<html" not in response.content[:500].lower()
            ):
                acquired += 1
                entry["status"] = "ACQUIRED"
                entry["sha256"] = sha256_bytes(response.content)
                if kind == "data":
                    entry["inspection"] = inspect_csv(response.content)
                else:
                    text = response.content.decode("utf-8", errors="replace")
                    entry["inspection"] = {
                        "lines": len(text.splitlines()),
                        "first_180_lines": "\n".join(
                            text.splitlines()[:180]
                        ),
                    }
            else:
                entry["status"] = "DOWNLOAD_BLOCKED"
                entry["prefix"] = response.content[:160].decode(
                    "utf-8",
                    errors="replace",
                )
        except Exception as exc:
            entry["status"] = "DOWNLOAD_ERROR"
            entry["error"] = repr(exc)

        result["files"][name] = entry

    result["summary"] = {
        "manifest_file_count": len(manifest),
        "targets": len(TARGETS),
        "acquired": acquired,
        "missing_or_blocked": len(TARGETS) - acquired,
        "all_acquired": acquired == len(TARGETS),
    }
    result["status"] = (
        "SOURCE_BYTES_ACQUIRED"
        if acquired == len(TARGETS)
        else "SOURCE_PARTIAL_OR_BLOCKED"
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
