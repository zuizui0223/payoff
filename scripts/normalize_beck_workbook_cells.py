#!/usr/bin/env python3
"""Normalize Beck et al. XLSX cells to deterministic long-form TSV.

Lane R only. This transformation preserves cell address/type/formula/value and
never assigns game or architecture semantics.
"""
from __future__ import annotations

import csv
import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

OUT = Path("outputs")
XLSX = OUT / "22_0519_SupplementaryDataSets.xlsx"
CELLS = OUT / "beck_nonempty_cells_v1.tsv"
METRICS = OUT / "beck_metric_rows_v1.tsv"

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
METRIC_RE = re.compile(r"^(X/pH(?: max)?|YXS|g/L biomass|ΔX \(g/L\)|CDW avg)$", re.I)


def shared_strings(z: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(t.text or "" for t in si.iterfind(".//m:t", NS))
            for si in root.findall("m:si", NS)]


def workbook_sheets(z: zipfile.ZipFile) -> list[tuple[str, str]]:
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall("pr:Relationship", NS)}
    out = []
    for s in wb.findall("m:sheets/m:sheet", NS):
        rid = s.attrib[f"{{{NS['r']}}}id"]
        target = targets[rid]
        if not target.startswith("xl/"):
            target = "xl/" + target.lstrip("/")
        out.append((s.attrib["name"], target))
    return out


def decoded_value(c: ET.Element, shared: list[str]) -> tuple[str, str, str]:
    typ = c.attrib.get("t", "n")
    formula = ""
    f = c.find("m:f", NS)
    if f is not None:
        formula = f.text or ""
    if typ == "inlineStr":
        value = "".join(t.text or "" for t in c.iterfind(".//m:t", NS))
        return typ, formula, value
    v = c.find("m:v", NS)
    raw = "" if v is None or v.text is None else v.text
    if typ == "s" and raw:
        try:
            raw = shared[int(raw)]
        except (ValueError, IndexError):
            raw = f"#BAD_SHARED:{raw}"
    elif typ == "b" and raw:
        raw = "TRUE" if raw == "1" else "FALSE"
    return typ, formula, raw


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not XLSX.exists():
        raise SystemExit(f"missing {XLSX}; run reconstruct_beck_public_workbook.py first")

    nonempty = 0
    metric_rows: list[tuple[int, str, int, str]] = []
    with zipfile.ZipFile(XLSX) as z, CELLS.open("w", newline="") as cell_f:
        shared = shared_strings(z)
        sheets = workbook_sheets(z)
        cw = csv.writer(cell_f, delimiter="\t")
        cw.writerow(["sheet_order", "sheet", "row", "cell_ref", "cell_type", "formula", "value"])

        for sheet_order, (sheet_name, path) in enumerate(sheets, start=1):
            root = ET.fromstring(z.read(path))
            for row in root.findall("m:sheetData/m:row", NS):
                row_number = int(row.attrib.get("r", "0"))
                row_values: list[str] = []
                for c in row.findall("m:c", NS):
                    ref = c.attrib.get("r", "")
                    typ, formula, value = decoded_value(c, shared)
                    if value != "" or formula != "":
                        nonempty += 1
                        cw.writerow([sheet_order, sheet_name, row_number, ref, typ, formula, value])
                    row_values.append(value)
                labels = [v for v in row_values if METRIC_RE.match(v.strip())]
                if labels:
                    metric_rows.append((sheet_order, sheet_name, row_number, " | ".join(row_values)))

    with METRICS.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["sheet_order", "sheet", "row", "raw_row_values"])
        w.writerows(metric_rows)

    cells_sha = sha256_file(CELLS)
    metrics_sha = sha256_file(METRICS)
    print(f"BECK_R_NORMALIZED_NONEMPTY_CELLS={nonempty}")
    print(f"BECK_R_NORMALIZED_TSV_SHA256={cells_sha}")
    print(f"BECK_R_METRIC_ROW_COUNT={len(metric_rows)}")
    print(f"BECK_R_METRIC_TSV_SHA256={metrics_sha}")
    for row in metric_rows[:40]:
        print("BECK_R_METRIC_ROW=" + repr(row))
    print("BECK_R3_TRANSFORMATION_DETERMINISTIC=True")
    print("BECK_R3_SEMANTIC_CLAIMS_ALLOWED=False")


if __name__ == "__main__":
    main()
