#!/usr/bin/env python3
"""Probe the public Ortega et al. 2023 Source Data XLSX without external libs.

This is a transport/schema audit only. It does not alter any preregistered
PAYOFF-B empirical result and does not infer route-wise controller parameters.

The parser reads workbook XML directly from the XLSX ZIP and reports:
- HTTP status / byte size / SHA256;
- workbook sheet names and dimensions;
- first non-empty rows per sheet;
- cells whose text contains candidate phase/migration identifiers.

It is intentionally dependency-free so GitHub Actions can run it in a minimal
Python environment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET


DEFAULT_URL = (
    "https://media.springernature.com/original/springer-static/esm/"
    "art%3A10.1038%2Fs41467-023-37750-z/MediaObjects/"
    "41467_2023_37750_MOESM4_ESM.xlsx"
)

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkg": "http://schemas.openxmlformats.org/package/2006/relationships",
}

CANDIDATE_TERMS = (
    "animal",
    "individual",
    "id",
    "year",
    "migration",
    "start",
    "end",
    "days",
    "peak",
    "irg",
    "phase",
    "green",
    "stopover",
    "speed",
    "duration",
)


def col_index(cell_ref: str) -> int:
    m = re.match(r"([A-Z]+)", cell_ref)
    if not m:
        return 0
    value = 0
    for ch in m.group(1):
        value = value * 26 + (ord(ch) - 64)
    return value - 1


def shared_strings(zf: zipfile.ZipFile) -> list[str]:
    path = "xl/sharedStrings.xml"
    if path not in zf.namelist():
        return []
    root = ET.fromstring(zf.read(path))
    out: list[str] = []
    for si in root.findall("main:si", NS):
        texts = [t.text or "" for t in si.findall(".//main:t", NS)]
        out.append("".join(texts))
    return out


def cell_value(cell: ET.Element, strings: list[str]) -> str:
    kind = cell.attrib.get("t")
    if kind == "inlineStr":
        return "".join(t.text or "" for t in cell.findall(".//main:t", NS))
    value = cell.find("main:v", NS)
    raw = "" if value is None or value.text is None else value.text
    if kind == "s" and raw:
        try:
            return strings[int(raw)]
        except (ValueError, IndexError):
            return raw
    if kind == "b":
        return "TRUE" if raw == "1" else "FALSE"
    return raw


def workbook_sheet_paths(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("pkg:Relationship", NS)
    }
    out = []
    for sheet in wb.findall("main:sheets/main:sheet", NS):
        name = sheet.attrib.get("name", "")
        rid = sheet.attrib.get(f"{{{NS['rel']}}}id")
        target = rel_map.get(rid or "", "")
        if target.startswith("/"):
            path = target.lstrip("/")
        elif target.startswith("xl/"):
            path = target
        else:
            path = "xl/" + target.lstrip("/")
        out.append((name, path))
    return out


def inspect_sheet(
    zf: zipfile.ZipFile,
    path: str,
    strings: list[str],
    *,
    max_nonempty_rows: int,
    max_scan_rows: int,
    max_cols: int,
) -> dict:
    root = ET.fromstring(zf.read(path))
    dim = root.find("main:dimension", NS)
    dimension = None if dim is None else dim.attrib.get("ref")
    first_rows = []
    matches = []

    scanned = 0
    for row in root.findall("main:sheetData/main:row", NS):
        scanned += 1
        if scanned > max_scan_rows:
            break
        values: dict[int, str] = {}
        for cell in row.findall("main:c", NS):
            ref = cell.attrib.get("r", "")
            idx = col_index(ref)
            if idx >= max_cols:
                continue
            val = cell_value(cell, strings)
            if val != "":
                values[idx] = val
                low = val.lower()
                if any(term in low for term in CANDIDATE_TERMS):
                    matches.append(
                        {
                            "row": int(row.attrib.get("r", scanned)),
                            "cell": ref,
                            "value": val[:300],
                        }
                    )
        if values and len(first_rows) < max_nonempty_rows:
            width = min(max(values) + 1, max_cols)
            row_values = [""] * width
            for idx, val in values.items():
                if idx < width:
                    row_values[idx] = val[:300]
            first_rows.append(
                {
                    "row": int(row.attrib.get("r", scanned)),
                    "values": row_values,
                }
            )

    return {
        "dimension": dimension,
        "first_nonempty_rows": first_rows,
        "candidate_text_matches": matches[:250],
        "rows_scanned": min(scanned, max_scan_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_ortega_source_data_probe.json"),
    )
    parser.add_argument("--max-nonempty-rows", type=int, default=12)
    parser.add_argument("--max-scan-rows", type=int, default=2000)
    parser.add_argument("--max-cols", type=int, default=80)
    args = parser.parse_args()

    req = urllib.request.Request(
        args.url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "Chrome/130 Safari/537.36"
            ),
            "Accept": (
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet,application/octet-stream,*/*"
            ),
        },
    )

    receipt: dict = {
        "date": "2026-10-03",
        "source": "Ortega et al. 2023 Nature Communications 14:2008",
        "doi": "10.1038/s41467-023-37750-z",
        "url": args.url,
        "status": "UNOPENED",
        "frozen_submission_affected": False,
        "purpose": (
            "transport/schema audit for prospective phase-variance analysis; "
            "not a preregistered outcome"
        ),
    }

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read()
            receipt["http_status"] = getattr(response, "status", None)
            receipt["resolved_url"] = response.geturl()
            receipt["content_type"] = response.headers.get("Content-Type")
    except Exception as exc:
        receipt["status"] = "DOWNLOAD_FAILED"
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(receipt, indent=2))
        return

    receipt["bytes"] = len(raw)
    receipt["sha256"] = hashlib.sha256(raw).hexdigest()

    if not raw.startswith(b"PK"):
        receipt["status"] = "NOT_XLSX_ZIP"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(receipt, indent=2))
        return

    try:
        with zipfile.ZipFile(BytesIO(raw)) as zf:
            strings = shared_strings(zf)
            sheets = []
            for name, path in workbook_sheet_paths(zf):
                if path not in zf.namelist():
                    sheets.append(
                        {"name": name, "path": path, "status": "MISSING_XML"}
                    )
                    continue
                info = inspect_sheet(
                    zf,
                    path,
                    strings,
                    max_nonempty_rows=args.max_nonempty_rows,
                    max_scan_rows=args.max_scan_rows,
                    max_cols=args.max_cols,
                )
                sheets.append({"name": name, "path": path, **info})
            receipt["status"] = "DOWNLOADED_AND_PARSED"
            receipt["shared_string_count"] = len(strings)
            receipt["sheets"] = sheets
            receipt["sheet_count"] = len(sheets)
    except Exception as exc:
        receipt["status"] = "XLSX_PARSE_FAILED"
        receipt["parse_error"] = f"{type(exc).__name__}: {exc}"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
