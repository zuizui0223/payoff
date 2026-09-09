#!/usr/bin/env python3
"""Reconstruct provenance/schema from Beck et al. public XLSX using stdlib only.

This is Lane R tooling. It emits no game or architecture claim.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

URL = "https://raw.githubusercontent.com/rosspcarlson/becketal-syntheticconsortia/main/22_0519_SupplementaryDataSets.xlsx"
EXPECTED_GIT_BLOB = "0ed48b34713d08dbdb17d9ca626387d63c673dbf"
OUT = Path("outputs")
XLSX = OUT / "22_0519_SupplementaryDataSets.xlsx"
REPORT = OUT / "beck_raw_reconstruction_v1.json"
MATCHES = OUT / "beck_keyword_rows_v1.tsv"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
KEYWORDS = re.compile(
    r"\b(wt|wild\s*type|consorti|producer|consumer|buffer|buffered|unbuffered|"
    r"lactate|acetate|glucose|growth|biomass|od\b|yield|figure|fig\.?|ph\b)\b",
    re.I,
)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def colnum(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref)
    if not letters:
        return 0
    n = 0
    for ch in letters.group(0):
        n = n * 26 + ord(ch) - 64
    return n


def shared_strings(z: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    out = []
    for si in root.findall("m:si", NS):
        out.append("".join(t.text or "" for t in si.iterfind(".//m:t", NS)))
    return out


def workbook_sheets(z: zipfile.ZipFile) -> list[tuple[str, str]]:
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall("pr:Relationship", NS)}
    rows = []
    for s in wb.findall("m:sheets/m:sheet", NS):
        rid = s.attrib[f"{{{NS['r']}}}id"]
        target = targets[rid]
        if not target.startswith("xl/"):
            target = "xl/" + target.lstrip("/")
        rows.append((s.attrib["name"], target))
    return rows


def cell_value(c: ET.Element, shared: list[str]) -> str:
    typ = c.attrib.get("t")
    if typ == "inlineStr":
        return "".join(t.text or "" for t in c.iterfind(".//m:t", NS))
    v = c.find("m:v", NS)
    if v is None or v.text is None:
        f = c.find("m:f", NS)
        return "=" + (f.text or "") if f is not None else ""
    raw = v.text
    if typ == "s":
        try:
            return shared[int(raw)]
        except (ValueError, IndexError):
            return f"#BAD_SHARED:{raw}"
    if typ == "b":
        return "TRUE" if raw == "1" else "FALSE"
    return raw


def parse_sheet(z: zipfile.ZipFile, path: str, shared: list[str]) -> dict:
    root = ET.fromstring(z.read(path))
    dim = root.find("m:dimension", NS)
    dimension = dim.attrib.get("ref") if dim is not None else None
    decoded_rows = []
    keyword_rows = []
    max_col = 0
    row_count = 0
    for row in root.findall("m:sheetData/m:row", NS):
        row_count += 1
        vals = {}
        for c in row.findall("m:c", NS):
            ref = c.attrib.get("r", "")
            col = colnum(ref)
            max_col = max(max_col, col)
            vals[col] = cell_value(c, shared)
        if vals:
            dense = [vals.get(i, "") for i in range(1, max(vals) + 1)]
        else:
            dense = []
        if len(decoded_rows) < 12:
            decoded_rows.append({"row": int(row.attrib.get("r", row_count)), "values": dense[:24]})
        text = " | ".join(dense)
        if KEYWORDS.search(text):
            keyword_rows.append({"row": int(row.attrib.get("r", row_count)), "values": dense[:32]})
    return {
        "dimension": dimension,
        "xml_row_count": row_count,
        "max_observed_column": max_col,
        "first_rows": decoded_rows,
        "keyword_rows": keyword_rows[:250],
        "keyword_row_count": len(keyword_rows),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    print(f"BECK_R_DOWNLOAD_URL={URL}")
    with urllib.request.urlopen(URL, timeout=60) as r:
        data = r.read()
    XLSX.write_bytes(data)
    sha256 = hashlib.sha256(data).hexdigest()
    blob = git_blob_sha1(data)
    print(f"BECK_R_BYTES={len(data)}")
    print(f"BECK_R_SHA256={sha256}")
    print(f"BECK_R_GIT_BLOB_SHA1={blob}")
    print(f"BECK_R_GIT_BLOB_MATCH={blob == EXPECTED_GIT_BLOB}")
    if blob != EXPECTED_GIT_BLOB:
        raise SystemExit("downloaded bytes do not match registered Git blob")

    with zipfile.ZipFile(XLSX) as z:
        entries = sorted(z.namelist())
        shared = shared_strings(z)
        sheets = workbook_sheets(z)
        report = {
            "lane": "R",
            "source_url": URL,
            "source_filename": XLSX.name,
            "byte_size": len(data),
            "sha256": sha256,
            "git_blob_sha1": blob,
            "expected_git_blob_sha1": EXPECTED_GIT_BLOB,
            "git_blob_match": blob == EXPECTED_GIT_BLOB,
            "zip_entry_count": len(entries),
            "shared_string_count": len(shared),
            "sheet_count": len(sheets),
            "sheets": {},
            "semantic_claims_allowed": False,
            "generic_game_claims_allowed_from_this_report_alone": False,
            "architecture_mapping_claims_allowed_from_this_report_alone": False,
        }
        for name, path in sheets:
            parsed = parse_sheet(z, path, shared)
            report["sheets"][name] = parsed
            print(
                "BECK_R_SHEET=" + json.dumps(
                    {"name": name, "path": path, "dimension": parsed["dimension"],
                     "rows": parsed["xml_row_count"], "keyword_rows": parsed["keyword_row_count"]},
                    sort_keys=True,
                )
            )

    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    with MATCHES.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["sheet", "row", "values_json"])
        for name, s in report["sheets"].items():
            for row in s["keyword_rows"]:
                w.writerow([name, row["row"], json.dumps(row["values"], ensure_ascii=False)])

    print("BECK_R_SHEET_NAMES=" + json.dumps(list(report["sheets"])))
    for name, s in report["sheets"].items():
        print("BECK_R_FIRST_ROWS=" + json.dumps({"sheet": name, "rows": s["first_rows"][:5]}, ensure_ascii=False))
        if s["keyword_rows"]:
            print("BECK_R_KEYWORD_SAMPLE=" + json.dumps({"sheet": name, "rows": s["keyword_rows"][:8]}, ensure_ascii=False))
    print(f"BECK_R_REPORT={REPORT}")
    print(f"BECK_R_MATCHES={MATCHES}")


if __name__ == "__main__":
    main()
