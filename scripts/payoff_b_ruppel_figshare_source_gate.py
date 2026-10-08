#!/usr/bin/env python3
"""Figshare source-only admission for Rüppel et al. 2023, DOI 10.6084/m9.figshare.c.6403996.

Public collection and article metadata are checked. Data file contents
are only inspected for format/headers/row counts, never modeled. No
departure, routing, landing, cue or fitness associations are evaluated.

This test fails closed when metadata retrieval fails rather than
misreporting a successful scientific source audit from synthetic tests.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

COLLECTION_ID = 6403996
API_ROOT = "https://api.figshare.com/v2"
MAX_SOURCE_BYTES = 20_000_000
MAX_FILES_TO_INSPECT = 30


def request(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={
            "User-Agent": "PAYOFF-B-public-figshare-source-audit/1.0",
            "Accept": "application/json,application/octet-stream",
        }
    )
    with urllib.request.urlopen(req, timeout=28) as response:
        n = int(response.headers.get("Content-Length", "0") or 0)
        if n > MAX_SOURCE_BYTES:
            raise ValueError("source exceeds per-file byte cap")
        raw = response.read(MAX_SOURCE_BYTES + 1)
        if len(raw) > MAX_SOURCE_BYTES:
            raise ValueError("source exceeded per-file byte cap")
        return raw


def fetch_json(url):
    data = request(url)
    x = json.loads(data)
    return x


def known_file_shape(name: str):
    lower = name.lower()
    if lower.endswith((".csv", ".tsv", ".txt")):
        return "DELIMITED"
    if lower.endswith(".zip"):
        return "ZIP"
    if lower.endswith((".xlsx", ".xls")):
        return "SPREADSHEET"
    if lower.endswith((".r", ".rmd", ".py")):
        return "CODE"
    if lower.endswith((".pdf", ".doc", ".docx")):
        return "DOCUMENT"
    return "OTHER"


def source_content_schema(filename, raw):
    kind = known_file_shape(filename)
    info = {"kind": kind, "body_phenological_results_examined": False}
    if kind == "ZIP":
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            info["archive_names"] = [
                {"name": e.filename, "bytes": e.file_size}
                for e in z.infolist()[:150]
                if not e.is_dir()
            ]
        return info
    if kind != "DELIMITED":
        return info
    if len(raw) > 2_000_000:
        info["schema_status"] = "TOO_LARGE_FOR_LINE_INSPECTION"
        return info
    try:
        txt = raw.decode("utf-8-sig")
        sep = "\t" if filename.lower().endswith(".tsv") else ","
        rdr = csv.reader(io.StringIO(txt), delimiter=sep)
        rows = iter(rdr)
        headers = next(rows, [])
        info["header_candidates"] = [c[:100] for c in headers[:45]]
        info["data_rows"] = sum(1 for _ in rows)
        info["schema_status"] = "HEADER_AND_ROW_COUNT_ONLY"
    except (UnicodeError, csv.Error):
        info["schema_status"] = "ENCODING_OR_FORMAT_HOLD"
    return info


def inspect_listing(collection, articles, *, allow_files=True):
    if not isinstance(collection, dict):
        raise ValueError("no collection metadata")
    if not isinstance(articles, list):
        raise ValueError("collection articles endpoint did not return a list")
    if not articles:
        raise ValueError("collection did not resolve any deposited study item")
    out = {
        "status": "SOURCE_COLLECTION_METADATA_PASS_CONTENT_NOT_YET_CLASSIFIED",
        "collection_id": COLLECTION_ID,
        "figshare_doi": "10.6084/m9.figshare.c.6403996",
        "original_study_doi": "10.1098/rsos.221420",
        "collection_title": collection.get("title"),
        "collection_doi": collection.get("doi"),
        "collection_published_date": collection.get("published_date"),
        "article_items": [],
        "source_data_analyses_run": False,
        "original_authors_already_analyzed_weather_dependent_departure_routing_landing": True,
    }
    if len(articles) > 50:
        raise ValueError("unexpected >50 collection items, avoid runaway audit")
    used_file_count = 0
    for item in articles:
        aid = item.get("id")
        if not isinstance(aid, int):
            raise ValueError("collection article lacks numeric ID")
        meta = fetch_json(f"{API_ROOT}/articles/{aid}") if allow_files else item
        filereceipts = []
        for file in meta.get("files", []):
            name = file.get("name")
            size = file.get("size")
            fid = file.get("id")
            entry = {
                "file_id": fid,
                "filename": name,
                "bytes": size,
                "figshare_checksum": file.get("supplied_md5") or file.get("computed_md5") or file.get("md5"),
                "format": known_file_shape(name or ""),
            }
            if not allow_files:
                entry["status"] = "METADATA_ONLY_SYNTHETIC"
            elif used_file_count >= MAX_FILES_TO_INSPECT or not isinstance(size, int) or size > MAX_SOURCE_BYTES:
                entry["status"] = "FILE_INSPECTION_CAP_HOLD"
            else:
                used_file_count += 1
                download_url = file.get("download_url") or f"https://ndownloader.figshare.com/files/{fid}"
                try:
                    raw = request(download_url)
                    actual_md5 = hashlib.md5(raw).hexdigest()
                    expected = entry["figshare_checksum"]
                    if expected and actual_md5.lower() != str(expected).lower():
                        raise ValueError("file content differs from Figshare MD5")
                    entry["status"] = "ACTUAL_SOURCE_MD5_AND_SCHEMA_PASS" if expected else "SOURCE_BYTES_SCHEMA_PASS_NO_PUBLISHED_MD5"
                    entry["actual_sha256"] = hashlib.sha256(raw).hexdigest()
                    entry["inspection"] = source_content_schema(name, raw)
                except (urllib.error.URLError, OSError, ValueError, zipfile.BadZipFile) as exc:
                    entry["status"] = "FILE_ACCESS_OR_SCHEMA_HOLD"
                    entry["error_type"] = type(exc).__name__
            filereceipts.append(entry)
        out["article_items"].append({
            "article_id": aid,
            "title": meta.get("title"),
            "doi": meta.get("doi"),
            "published_date": meta.get("published_date"),
            "license": meta.get("license"),
            "files": filereceipts,
        })
    out["files_listed"] = sum(len(a["files"]) for a in out["article_items"])
    out["files_actual_inspected"] = sum(
        x["status"] in ("ACTUAL_SOURCE_MD5_AND_SCHEMA_PASS", "SOURCE_BYTES_SCHEMA_PASS_NO_PUBLISHED_MD5")
        for a in out["article_items"] for x in a["files"]
    )
    if out["files_listed"] == 0:
        out["status"] = "COLLECTION_METADATA_PASS_NO_FILES_LISTED"
    elif out["files_actual_inspected"] > 0:
        out["status"] = "SOURCE_METADATA_AND_FILE_SCHEMA_PARTIAL_PASS"
    else:
        out["status"] = "SOURCE_METADATA_PASS_FILE_CONTENT_HOLD"
    return out


def audit():
    receipt = {"audit_kind": "Figshare_2023_original_source_only",
               "collection_id": COLLECTION_ID,
               "outcome_model_fitted": False}
    try:
        coll = fetch_json(f"{API_ROOT}/collections/{COLLECTION_ID}")
        articles = fetch_json(f"{API_ROOT}/collections/{COLLECTION_ID}/articles")
        receipt.update(inspect_listing(coll, articles))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        receipt["status"] = "SOURCE_COLLECTION_ACCESS_HOLD"
        receipt["error_type"] = type(exc).__name__
        receipt["error"] = str(exc)[:240]
    return receipt


def synthetic_test():
    coll = {"title": "Toy source", "doi": "10.6084/example"}
    items = [{"id": 12, "title": "Departure, routing, landing", "doi": "10.6084/foo",
              "files": [{"id": 8, "name": "source.csv", "size": 40, "md5": "aaa"}]}]
    d = inspect_listing(coll, items, allow_files=False)
    assert d["files_listed"] == 1
    assert d["files_actual_inspected"] == 0
    assert d["article_items"][0]["files"][0]["status"] == "METADATA_ONLY_SYNTHETIC"
    csvx = source_content_schema("toy.csv", b"id,stage,weather\n1,depart,1\n2,land,2\n")
    assert csvx["header_candidates"] == ["id", "stage", "weather"]
    assert csvx["data_rows"] == 2
    assert source_content_schema("toy.r", b"a=2")["kind"] == "CODE"
    print("PAYOFF_B_RUPPEL_SOURCE_METADATA_SYNTHETIC_PASS")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--output", default="outputs/payoff_b_ruppel_original_source_gate.json")
    args = p.parse_args()
    if args.self_test:
        synthetic_test()
    else:
        data = audit()
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n")
        print("PAYOFF_B_RUPPEL_ORIGINAL_DATA_SOURCE_GATE")
        print(json.dumps(data, ensure_ascii=False)[:15000])
        if not str(data.get("status", "")).startswith("SOURCE_METADATA_AND_FILE_SCHEMA_PARTIAL_PASS"):
            raise SystemExit("SOURCE_GATE_HOLD: no deposited source file schema successfully admitted")
