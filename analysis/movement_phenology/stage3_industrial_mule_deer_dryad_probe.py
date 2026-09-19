#!/usr/bin/env python3
"""Audit and, when possible, download the public Aikens et al. 2022 Dryad bundle.

Dataset DOI:
  10.5061/dryad.7d7wm37z5

The current Dryad web file_stream endpoint may require an authenticated browser
session. This script first uses anonymous REST metadata, then tests the
documented /api/v2/files/{id}/download route without credentials. If the public
download is unavailable, it fails closed after writing a complete source
receipt instead of scraping around the access control.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
import zipfile

import pandas as pd
import requests


BASE = "https://datadryad.org/api/v2"
DOI = "doi:10.5061/dryad.7d7wm37z5"
ENCODED_DOI = "doi%3A10.5061%2Fdryad.7d7wm37z5"
OUT = Path("outputs/movement_phenology")
EXT = Path("external/industrial_mule_deer")
OUT.mkdir(parents=True, exist_ok=True)
EXT.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "payoff-movement-phenology/1.0"}


def get(url, timeout=60, stream=False):
    return requests.get(
        url,
        headers=UA,
        timeout=timeout,
        allow_redirects=True,
        stream=stream,
    )


def json_or_error(url):
    r = get(url)
    rec = {
        "request_url": url,
        "status": r.status_code,
        "final_url": str(r.url),
        "content_type": r.headers.get("content-type"),
    }
    if r.ok:
        try:
            rec["json"] = r.json()
        except Exception as exc:
            rec["parse_error"] = f"{type(exc).__name__}:{exc}"
    else:
        rec["body_preview"] = r.text[:1000]
    return rec


def flatten_files(payload):
    if not isinstance(payload, dict):
        return []
    if "_embedded" in payload:
        for key in ("stash:files", "files"):
            x = payload["_embedded"].get(key)
            if isinstance(x, list):
                return x
    for key in ("files", "data"):
        x = payload.get(key)
        if isinstance(x, list):
            return x
    return []


def inspect_tabular_bytes(name: str, raw: bytes):
    lower = name.lower()
    out = {
        "name": name,
        "bytes": len(raw),
    }

    if lower.endswith(".csv") or lower.endswith(".txt") or lower.endswith(".tsv"):
        for encoding in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                text = raw.decode(encoding)
            except Exception:
                continue
            for sep in (",", "\t", ";"):
                try:
                    df = pd.read_csv(
                        io.StringIO(text),
                        sep=sep,
                        low_memory=False,
                    )
                except Exception:
                    continue
                if df.shape[1] > 1:
                    out.update(
                        {
                            "table_rows": int(len(df)),
                            "table_cols": int(df.shape[1]),
                            "columns": [str(c) for c in df.columns],
                            "head": df.head(3)
                            .astype(object)
                            .where(pd.notna(df.head(3)), None)
                            .to_dict(orient="records"),
                        }
                    )
                    return out
    return out


def inspect_zip_bytes(raw: bytes, prefix: str = "", depth: int = 0):
    records = []
    if depth > 3:
        return records
    try:
        bio = io.BytesIO(raw)
        if not zipfile.is_zipfile(bio):
            return records
        bio.seek(0)
        with zipfile.ZipFile(bio) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                full = f"{prefix}{info.filename}"
                rec = {
                    "member": full,
                    "compressed_bytes": int(info.compress_size),
                    "uncompressed_bytes": int(info.file_size),
                    "archive_depth": int(depth),
                }
                if info.file_size <= 50_000_000:
                    try:
                        payload = zf.read(info.filename)
                        rec["content"] = inspect_tabular_bytes(full, payload)
                        if (
                            info.filename.lower().endswith(".zip")
                            or payload.startswith(b"PK")
                        ):
                            nested = inspect_zip_bytes(
                                payload,
                                prefix=full + "::",
                                depth=depth + 1,
                            )
                            rec["nested_member_count"] = len(nested)
                            records.extend(nested)
                    except Exception as exc:
                        rec["inspect_error"] = (
                            f"{type(exc).__name__}:{exc}"
                        )
                records.append(rec)
    except Exception:
        return records
    return records


def inspect_archive(path: Path):
    if not path.exists() or not zipfile.is_zipfile(path):
        return []
    return inspect_zip_bytes(path.read_bytes(), prefix="", depth=0)


def main():
    receipt = {
        "doi": DOI,
        "dataset": None,
        "versions": None,
        "version_files_requests": [],
        "files": [],
        "download_attempts": [],
        "bulk_download_attempts": [],
        "downloaded_archives": [],
    }

    dataset_url = f"{BASE}/datasets/{ENCODED_DOI}"
    versions_url = f"{BASE}/datasets/{ENCODED_DOI}/versions"

    receipt["dataset"] = json_or_error(dataset_url)
    receipt["versions"] = json_or_error(versions_url)

    version_ids = []
    vpayload = (receipt["versions"] or {}).get("json")
    if isinstance(vpayload, dict):
        embedded = vpayload.get("_embedded", {})
        candidates = (
            embedded.get("stash:versions")
            or embedded.get("versions")
            or vpayload.get("versions")
            or []
        )
        for v in candidates:
            if not isinstance(v, dict):
                continue
            vid = v.get("id") or v.get("version")
            if vid is None:
                href = (
                    (v.get("_links") or {})
                    .get("self", {})
                    .get("href")
                )
                if href and "/versions/" in str(href):
                    vid = str(href).rstrip("/").split("/")[-1]
            if vid is not None:
                version_ids.append(str(vid))

    # If the response shape changes, the dataset record often exposes a version.
    dpayload = (receipt["dataset"] or {}).get("json")
    if not version_ids and isinstance(dpayload, dict):
        for key in ("version", "versionId", "id"):
            value = dpayload.get(key)
            if isinstance(value, int):
                version_ids.append(str(value))

    version_ids = list(dict.fromkeys(version_ids))

    files = []
    for vid in version_ids:
        url = f"{BASE}/versions/{vid}/files"
        rec = json_or_error(url)
        receipt["version_files_requests"].append(rec)
        payload = rec.get("json")
        for f in flatten_files(payload):
            if not isinstance(f, dict):
                continue
            file_id = f.get("id")
            if file_id is None:
                self_href = (
                    ((f.get("_links") or {}).get("self") or {}).get("href")
                )
                if self_href and "/files/" in str(self_href):
                    token = str(self_href).rstrip("/").split("/")[-1]
                    if token.isdigit():
                        file_id = int(token)
            name = (
                f.get("path")
                or f.get("name")
                or f.get("filename")
                or f.get("fileName")
            )
            row = {
                "version_id": vid,
                "file_id": file_id,
                "name": name,
                "size": f.get("size"),
                "mime_type": f.get("mimeType"),
                "digest": f.get("digest"),
                "status": f.get("status"),
                "path": f.get("path"),
                "download_url_metadata": (
                    ((f.get("_links") or {}).get("stash:download") or {}).get("href")
                    or ((f.get("_links") or {}).get("download") or {}).get("href")
                ),
                "raw_metadata": f,
            }
            files.append(row)

    # Known web-page file IDs are included only as a fallback metadata target;
    # they originate from the public Dryad file links, not a guessed ID.
    known = [
        {"file_id": 1840631, "name": "DryadDataFor_Aikens_etal_NatEcoEvo.zip"},
        {"file_id": 1840632, "name": "README.txt"},
    ]
    seen_ids = {str(x.get("file_id")) for x in files if x.get("file_id") is not None}
    for row in known:
        if str(row["file_id"]) not in seen_ids:
            files.append({"version_id": None, **row})

    receipt["files"] = files

    for f in files:
        fid = f.get("file_id")
        if fid is None:
            continue
        name = str(f.get("name") or f"dryad_{fid}")
        url = f"{BASE}/files/{fid}/download"
        attempt = {
            "file_id": fid,
            "name": name,
            "url": url,
        }
        try:
            r = get(url, timeout=120, stream=True)
            attempt.update(
                {
                    "status": r.status_code,
                    "final_url": str(r.url),
                    "content_type": r.headers.get("content-type"),
                }
            )
            if r.ok:
                safe = Path(name).name
                target = EXT / safe
                with target.open("wb") as h:
                    for chunk in r.iter_content(1024 * 1024):
                        if chunk:
                            h.write(chunk)
                attempt["downloaded_bytes"] = int(target.stat().st_size)
                if target.stat().st_size > 0:
                    archive = {
                        "file_id": fid,
                        "name": safe,
                        "path": str(target),
                        "members": inspect_archive(target),
                    }
                    receipt["downloaded_archives"].append(archive)
            else:
                try:
                    attempt["body_preview"] = r.text[:500]
                except Exception:
                    pass
        except Exception as exc:
            attempt["error"] = f"{type(exc).__name__}:{exc}"
        receipt["download_attempts"].append(attempt)

    # Try public dataset/version bulk-download routes exposed by Dryad metadata.
    bulk_targets = [
        (
            "dataset",
            f"{BASE}/datasets/{ENCODED_DOI}/download",
        )
    ]
    for vid in version_ids:
        bulk_targets.append(
            ("version_" + str(vid), f"{BASE}/versions/{vid}/download")
        )

    for label, url in bulk_targets:
        attempt = {"label": label, "url": url}
        try:
            r = get(url, timeout=180, stream=True)
            attempt.update(
                {
                    "status": r.status_code,
                    "final_url": str(r.url),
                    "content_type": r.headers.get("content-type"),
                }
            )
            if r.ok:
                target = EXT / f"dryad_bulk_{label}.zip"
                with target.open("wb") as h:
                    for chunk in r.iter_content(1024 * 1024):
                        if chunk:
                            h.write(chunk)
                attempt["downloaded_bytes"] = int(target.stat().st_size)
                if target.stat().st_size > 0:
                    archive = {
                        "file_id": None,
                        "name": target.name,
                        "path": str(target),
                        "source": "bulk_" + label,
                        "members": inspect_archive(target),
                    }
                    receipt["downloaded_archives"].append(archive)
            else:
                try:
                    attempt["body_preview"] = r.text[:500]
                except Exception:
                    pass
        except Exception as exc:
            attempt["error"] = f"{type(exc).__name__}:{exc}"
        receipt["bulk_download_attempts"].append(attempt)

    receipt["public_zip_downloaded"] = any(
        str(x.get("name", "")).lower().endswith(".zip")
        and x.get("members")
        for x in receipt["downloaded_archives"]
    )
    receipt["claim_ceiling"] = (
        "Source-access and schema audit only. No disturbance/control-permeability "
        "effect is licensed until the published analysis grain and variables are "
        "reconstructed from the archived data."
    )

    (OUT / "stage3_industrial_mule_deer_dryad_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )

    rows = []
    for archive in receipt["downloaded_archives"]:
        for member in archive.get("members", []):
            content = member.get("content") or {}
            rows.append(
                {
                    "archive": archive.get("name"),
                    "member": member.get("member"),
                    "bytes": member.get("uncompressed_bytes"),
                    "table_rows": content.get("table_rows"),
                    "table_cols": content.get("table_cols"),
                    "columns": " | ".join(content.get("columns") or []),
                    "head_json": json.dumps(
                        content.get("head") or [],
                        ensure_ascii=False,
                        default=str,
                    ),
                    "archive_depth": member.get("archive_depth"),
                }
            )
    pd.DataFrame(rows).to_csv(
        OUT / "stage3_industrial_mule_deer_schema.csv",
        index=False,
    )

    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
