#!/usr/bin/env python3
"""Probe public Dryad sources for PAYOFF-B E7 without promoting any claim."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import html
import re
import shutil
import urllib.parse
import zipfile
from pathlib import Path

import pandas as pd
import requests

API = "https://datadryad.org/api/v2/datasets/{doi}/download"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(name: str) -> str:
    name = name.replace("\\", "_").replace("/", "_")
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)


def landing_probe(doi: str, expected_names: list[str]) -> dict:
    encoded = urllib.parse.quote("doi:" + doi, safe="")
    url = "https://datadryad.org/dataset/" + encoded
    r = requests.get(url, timeout=120, allow_redirects=True)
    out = {
        "url": r.url,
        "status_code": r.status_code,
        "content_type": r.headers.get("content-type"),
        "href_candidates": [],
        "filename_context": {},
    }
    if r.status_code != 200:
        return out
    text = html.unescape(r.text)
    hrefs = re.findall(r'href=["\\\']([^"\\\']+)["\\\']', text, flags=re.I)
    keep = []
    for href in hrefs:
        low = href.lower()
        if any(token in low for token in ("file_stream", "download", "/api/v2/files/", "/stash/")):
            keep.append(href)
    out["href_candidates"] = sorted(set(keep))[:300]
    for name in expected_names:
        i = text.find(name)
        if i >= 0:
            out["filename_context"][name] = text[max(0, i - 800): i + 1200]
    return out


def download_dataset(doi: str, expected_names: list[str]) -> tuple[list[tuple[str, bytes, str]], dict]:
    encoded = urllib.parse.quote("doi:" + doi, safe="")
    url = API.format(doi=encoded)
    diagnostics = {"api_url": url}
    try:
        r = requests.get(url, timeout=120, allow_redirects=True)
        diagnostics["api_status_code"] = r.status_code
        diagnostics["api_content_type"] = r.headers.get("content-type")
        r.raise_for_status()
        ctype = (r.headers.get("content-type") or "").lower()

        # Current Dryad API may return either an archive response or a JSON
        # listing of files with per-file download links.
        if "zip" in ctype or r.content[:2] == b"PK":
            out = []
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    out.append((Path(info.filename).name, z.read(info), "zip-member"))
            return out, diagnostics

        payload = r.json()
        rows = payload.get("data", payload if isinstance(payload, list) else [])
        out = []
        for row in rows:
            attrs = row.get("attributes", {})
            links = row.get("links", {})
            name = attrs.get("name") or attrs.get("path") or row.get("name")
            link = links.get("download") or row.get("download")
            if not name or not link:
                continue
            if link.startswith("/"):
                link = "https://datadryad.org" + link
            rr = requests.get(link, timeout=120, allow_redirects=True)
            rr.raise_for_status()
            out.append((Path(name).name, rr.content, link))
        if out:
            return out, diagnostics
        diagnostics["api_payload_keys"] = list(payload) if isinstance(payload, dict) else str(type(payload))
    except Exception as e:
        diagnostics["api_error"] = repr(e)

    diagnostics["landing"] = landing_probe(doi, expected_names)
    return [], diagnostics


def inspect_csv(name: str, data: bytes) -> dict:
    last = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            df = pd.read_csv(io.BytesIO(data), encoding=enc)
            break
        except Exception as e:
            last = repr(e)
    else:
        return {"kind": "csv", "parse_error": last}

    low = {}
    for col in df.columns:
        try:
            n = int(df[col].nunique(dropna=True))
            if n <= 20:
                low[str(col)] = [str(x) for x in df[col].dropna().unique()[:30]]
        except Exception:
            pass
    return {
        "kind": "csv",
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "dtypes": {str(c): str(df[c].dtype) for c in df.columns},
        "low_cardinality": low,
        "head": df.head(3).where(pd.notna(df), None).to_dict(orient="records"),
    }


def inspect_xlsx(name: str, data: bytes) -> dict:
    try:
        book = pd.ExcelFile(io.BytesIO(data), engine="openpyxl")
    except Exception as e:
        return {"kind": "xlsx", "parse_error": repr(e)}
    sheets = {}
    for sheet in book.sheet_names:
        try:
            df = pd.read_excel(book, sheet_name=sheet, nrows=8)
            sheets[str(sheet)] = {
                "columns": [str(c) for c in df.columns],
                "preview_rows": int(len(df)),
                "head": df.head(3).where(pd.notna(df), None).to_dict(orient="records"),
            }
        except Exception as e:
            sheets[str(sheet)] = {"parse_error": repr(e)}
    return {"kind": "xlsx", "sheets": sheets, "sheet_count": len(book.sheet_names)}


def inspect(name: str, data: bytes) -> dict:
    lower = name.lower()
    if lower.endswith(".csv"):
        return inspect_csv(name, data)
    if lower.endswith((".xlsx", ".xls")):
        return inspect_xlsx(name, data)
    if lower.endswith(".zip"):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                return {
                    "kind": "zip",
                    "members": [x.filename for x in z.infolist() if not x.is_dir()][:200],
                    "member_count": sum(not x.is_dir() for x in z.infolist()),
                }
        except Exception as e:
            return {"kind": "zip", "parse_error": repr(e)}
    return {"kind": "other", "bytes": len(data)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    result = {
        "result_id": "payoff_b_e7_dryad_source_probe_20260928",
        "status": "SOURCE_SCHEMA_PROBE",
        "contract_id": contract["contract_id"],
        "sources": {},
    }
    for src in contract["candidate_sources"]:
        doi = src.get("data_doi")
        if not doi:
            continue
        print(f"PROBE {src['source_id']} {doi}", flush=True)
        entry = {"doi": doi, "files": []}
        try:
            expected_names = list(src.get("data_files") or [])
            files, diagnostics = download_dataset(doi, expected_names)
            entry["diagnostics"] = diagnostics
            for name, data, route in files:
                row = {
                    "name": name,
                    "bytes": len(data),
                    "sha256": sha256_bytes(data),
                    "download_route": route,
                    "inspection": inspect(name, data),
                }
                entry["files"].append(row)
            entry["status"] = "ACQUIRED" if files else "URL_RESOLUTION_PENDING"
        except Exception as e:
            entry["status"] = "ACCESS_OR_PARSE_FAILED"
            entry["error"] = repr(e)
        result["sources"][src["source_id"]] = entry

    acquired = sum(v.get("status") == "ACQUIRED" for v in result["sources"].values())
    result["summary"] = {
        "source_count": len(result["sources"]),
        "acquired": acquired,
        "failed": len(result["sources"]) - acquired,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
