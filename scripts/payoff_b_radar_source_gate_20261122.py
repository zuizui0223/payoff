#!/usr/bin/env python3
"""Provider-source-only Figshare audit for PAYOFF-B independent radar candidate.

Explicitly DOES NOT FIT animal effects, use eBird, or equate satellite greenup
with information available to any bird at departure. Output contains aggregate
provenance/schema/cardinality only, never original station/animal/space rows.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
from pathlib import Path
import urllib.error
import urllib.request
import zipfile

ARTICLE_ID = 26050390
API_URL = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
ALLOWED_DOWNLOAD_PREFIX = "https://ndownloader.figshare.com/files/"
MAX_BYTES = 12_000_000
MAX_FILES = 12
MAX_ZIP_EXPANDED_BYTES = 12_000_000


def bounded_download(url: str, cap: int = MAX_BYTES) -> bytes:
    if url != API_URL and not re.fullmatch(
        r"https://ndownloader\.figshare\.com/files/[0-9]+", url
    ):
        raise ValueError("provider URL not allowlisted")
    req = urllib.request.Request(url, headers={
        "User-Agent": "PAYOFF-source-audit/1.0 (academic reproducibility)",
        "Accept": "application/json,application/octet-stream,*/*",
    })
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read(cap + 1)
    if len(data) > cap:
        raise ValueError("provider response larger than declared limit")
    return data


def safe_fields(row: dict) -> dict:
    """Only numerical cardinalities and field names, never original records."""
    return {
        "n_rows": row.get("n_rows"),
        "columns": row.get("columns", []),
        "n_years": row.get("n_years"),
        "year_range": row.get("year_range"),
        "n_sites": row.get("n_sites"),
        "year_field": row.get("year_field"),
        "site_field": row.get("site_field"),
        "year_site_fields_verified": row.get("year_site_fields_verified", False),
    }


def csv_schema(payload: bytes, max_rows: int = 120_000) -> dict:
    # Only aggregate approved variable names; never return source rows or IDs.
    # First reject binary blobs; strict text decode avoids fabricating a table.
    sample = payload[:20_000].decode("utf-8-sig", errors="strict")
    delimiter = "\t" if sample.split("\n", 1)[0].count("\t") > sample.split("\n", 1)[0].count(",") else ","
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig")), delimiter=delimiter)
    columns = reader.fieldnames or []
    names = {c.strip().lower(): c for c in columns}
    candidate_year_names = ("year", "yr", "year_bio", "year_spring", "seasonyear")
    candidate_site_names = ("station", "site", "radar", "radar_id", "station_id", "site_id", "radar_station", "id")
    year_col = next((names[c] for c in candidate_year_names if c in names), None)
    site_col = next((names[c] for c in candidate_site_names if c in names), None)
    observed_years: set[int] = set()
    observed_sites: set[str] = set()
    rows = 0
    trunc = False
    for row in reader:
        if rows >= max_rows:
            trunc = True
            break
        rows += 1
        if year_col:
            raw = str(row.get(year_col, "")).strip()
            if re.fullmatch(r"(?:19|20)\d{2}", raw):
                observed_years.add(int(raw))
        if site_col:
            raw = str(row.get(site_col, "")).strip()
            if raw:
                observed_sites.add(raw)
    return safe_fields({
        "n_rows": rows if not trunc else None,
        "columns": columns[:100],
        "year_field": year_col,
        "site_field": site_col,
        "n_years": len(observed_years) if year_col and not trunc else None,
        "year_range": [min(observed_years), max(observed_years)] if observed_years and not trunc else None,
        "n_sites": len(observed_sites) if site_col and not trunc else None,
        "year_site_fields_verified": bool(year_col and site_col and not trunc),
    })


def inspect_archive(payload: bytes) -> dict:
    result: list[dict] = []
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        entries = zf.infolist()
        if len(entries) > 2000:
            raise ValueError("unreasonably large ZIP member count")
        for entry in entries:
            name = entry.filename
            if entry.is_dir():
                continue
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError("unsafe ZIP member")
            info = {"name": name, "uncompressed_size": entry.file_size}
            if entry.file_size <= MAX_ZIP_EXPANDED_BYTES and name.lower().endswith((".csv", ".tsv")):
                raw = zf.read(entry)
                info["schema"] = csv_schema(raw)
            result.append(info)
    return {"members": result[:200], "member_count": len(result)}


def audit() -> dict:
    record = {
        "status": "SOURCE_ONLY_NO_EFFECT_FIT",
        "article_id": ARTICLE_ID,
        "api_url": API_URL,
        "ecological_claim": "RADAR_ASSEMBLAGE_MEASUREMENT_NOT_INDIVIDUAL_BIRD_INFORMATION",
        "no_ebird_allowed": True,
        "new_biological_coefficient_fitted": False,
        "files": [],
    }
    article = json.loads(bounded_download(API_URL, 1_000_000))
    published_doi = str(article.get("doi", "")).lower()
    if "26050390" not in published_doi:
        raise ValueError("original Figshare DOI mismatch")
    record["source"] = {
        "doi": published_doi,
        "title": str(article.get("title", "")),
        "version": article.get("version"),
        "published_date": article.get("published_date"),
        "license": article.get("license", {}).get("name") if isinstance(article.get("license"), dict) else None,
    }
    files = article.get("files", [])
    record["provider_file_count"] = len(files)
    record["provider_total_bytes"] = sum(int(f.get("size", 0)) for f in files)
    for idx, f in enumerate(files):
        fid = int(f["id"])
        name = str(f["name"])
        entry = {
            "file_id": fid,
            "name": name,
            "provider_size": int(f.get("size", 0)),
            "provider_md5": f.get("computed_md5") or f.get("supplied_md5"),
            "status": "METADATA_ONLY",
        }
        if idx >= MAX_FILES:
            entry["status"] = "SKIP_MAX_FILE_COUNT"
        elif not (0 < entry["provider_size"] <= MAX_BYTES):
            entry["status"] = "SKIP_SIZE_CAP"
        else:
            try:
                raw = bounded_download(f"{ALLOWED_DOWNLOAD_PREFIX}{fid}")
                md5 = hashlib.md5(raw).hexdigest()
                if entry["provider_md5"] and md5.lower() != str(entry["provider_md5"]).lower():
                    raise ValueError("provider MD5 mismatch")
                entry["actual_size"] = len(raw)
                if len(raw) != entry["provider_size"]:
                    raise ValueError("actual bytes disagree with provider size")
                entry["sha256"] = hashlib.sha256(raw).hexdigest()
                if name.lower().endswith((".csv", ".tsv")):
                    entry["schema"] = csv_schema(raw)
                elif name.lower().endswith(".zip"):
                    entry["archive"] = inspect_archive(raw)
                else:
                    entry["status"] = "PROVENANCE_VERIFIED_SCHEMA_UNSUPPORTED"
                    record["files"].append(entry)
                    continue
                entry["status"] = "SOURCE_BYTES_VERIFIED_AGGREGATE_SCHEMA"
            except Exception as exc:
                entry["status"] = "DOWNLOAD_OR_SCHEMA_NOT_VERIFIED"
                entry["error_type"] = type(exc).__name__
                entry["error_summary"] = str(exc)[:200]
        record["files"].append(entry)
    # Fit eligibility is *not* decided by names alone; source claims are fixed.
    record["can_fit_new_radar_greenup_effect"] = False
    record["next_gate"] = (
        "Original station-year spring passage quantiles, greenup and climate"
        " must be matched without invented keys; predeclare heldout-year model"
        " and validate predictor support before opening any association."
    )
    return record


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    try:
        result = audit()
    except Exception as exc:
        result = {
            "status": "SOURCE_NOT_ADMITTED",
            "article_id": ARTICLE_ID,
            "new_biological_coefficient_fitted": False,
            "failure": type(exc).__name__,
            "message": str(exc)[:200],
        }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("PAYOFF_RADAR_SOURCE_RECEIPT=" + json.dumps(result, separators=(",", ":"), ensure_ascii=False))


if __name__ == "__main__":
    main()
