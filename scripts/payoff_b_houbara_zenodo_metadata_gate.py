#!/usr/bin/env python3
"""Audit the official Burnside 2021 houbara Zenodo archive without opening results.

Read only immutable-record file bytes and XLSX package metadata. No animal
observations, behavioral or fitness coefficients, climate cue correlations
or prediction errors are computed in this stage.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import posixpath
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ARCHIVE_RECORD = "4917565"
EXPECTED_FILES = {
    "MigrationData.xlsx": ("183edf4bc6b3ba9946e4145589ff1c2d", 18_000_000),
    "PNAS_code.R": ("73050bfb758fd8d7a290913d80315ce7", 150_000),
}

MAIN_XML_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"x": MAIN_XML_NS}


def _source_candidates(filename):
    return [
        f"https://zenodo.org/records/{ARCHIVE_RECORD}/files/{filename}?download=1",
        f"https://zenodo.org/api/records/{ARCHIVE_RECORD}/files/{filename}/content",
        f"https://zenodo.org/record/{ARCHIVE_RECORD}/files/{filename}?download=1",
    ]


def _download_verified(name):
    expected, limit = EXPECTED_FILES[name]
    errors = []
    for url in _source_candidates(name):
        try:
            req = urllib.request.Request(url, headers={
                "Accept": "application/octet-stream",
                "User-Agent": "PAYOFF-B-public-science-source-audit/1.0",
            })
            with urllib.request.urlopen(req, timeout=25) as response:
                size = int(response.headers.get("Content-Length", "0") or "0")
                if size > limit:
                    raise ValueError("reported content length exceeds cap")
                raw = response.read(limit + 1)
            if len(raw) > limit:
                raise ValueError("download exceeded cap")
            md5 = hashlib.md5(raw).hexdigest()
            if md5 != expected:
                errors.append({
                    "endpoint": url.split("?")[0],
                    "error": "MD5_MISMATCH",
                    "received_bytes": len(raw),
                })
                continue
            return raw, {
                "status": "PUBLISHER_MD5_VERIFIED",
                "source_url": url,
                "bytes": len(raw),
                "md5": md5,
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            errors.append({"endpoint": url.split("?")[0],
                           "error": type(e).__name__, "message": str(e)[:120]})
    return None, {"status": "ACCESS_OR_CHECKSUM_HOLD", "attempts": errors}


def _sheet_meta(raw):
    """Read sheet names, OOXML dimensions, and only first *header* row.

    ZIP-XML inspection avoids interpreting study outcomes, dates or model
    results. A declared Excel dimension is NOT proof of the number of usable
    individual-year observations. It will not establish chronological cue
    availability from column names alone.
    """
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        paths = set(z.namelist())
        required = {"xl/workbook.xml", "xl/_rels/workbook.xml.rels"}
        if not required.issubset(paths):
            raise ValueError("not a conventional OOXML workbook")
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        mapping = {}
        for el in rels.findall(f"{{{PKG_REL_NS}}}Relationship"):
            target = el.attrib.get("Target", "")
            if target.startswith("/"):
                target = target.lstrip("/")
            else:
                target = posixpath.normpath(posixpath.join("xl", target))
            mapping[el.attrib.get("Id")] = target

        sections = []
        needed_shared_indices = set()
        for el in wb.findall(".//x:sheets/x:sheet", NS):
            sheet_name = el.attrib["name"]
            rel_id = el.attrib.get(f"{{{DOC_REL_NS}}}id")
            xml_path = mapping.get(rel_id)
            if xml_path not in paths:
                raise ValueError(f"sheet target not found for {sheet_name}")
            sheet_info = {"sheet_name": sheet_name, "first_row": [],
                          "first_row_semantics": "UNVERIFIED_HEADERS_ONLY"}
            # Streaming parse (critical for 1000 null replicates in archive).
            with z.open(xml_path) as stream:
                parser = ET.iterparse(stream, events=("start", "end"))
                for event, element in parser:
                    tag = element.tag.rsplit("}", 1)[-1]
                    if event == "start" and tag == "dimension":
                        sheet_info["xlsx_declared_dimension"] = element.attrib.get("ref")
                    if event == "end" and tag == "row":
                        cells = []
                        for c in element.findall("x:c", NS):
                            location = c.attrib.get("r", "")
                            typ = c.attrib.get("t", "")
                            v = c.find("x:v", NS)
                            inline = c.find("x:is", NS)
                            value = None
                            if typ == "s" and v is not None and v.text is not None:
                                value = {"shared_index": int(v.text)}
                                needed_shared_indices.add(int(v.text))
                            elif typ == "inlineStr" and inline is not None:
                                value = "".join(inline.itertext())[:140]
                            elif v is not None and v.text is not None:
                                # A numeric first row may contain data, not a
                                # heading. Keep the first-row structure only.
                                value = {"numeric_cell": True}
                            cells.append({"cell": location, "value": value})
                            if len(cells) >= 45:
                                break
                        sheet_info["first_row"] = cells
                        element.clear()
                        break
                    # Do not clear cell nodes before reading the enclosing
                    # first row; it would erase shared-string index values.
                    # We terminate after the first row and never load the
                    # potentially enormous randomized-null worksheet body.
            sections.append(sheet_info)

        if needed_shared_indices:
            shared_path = "xl/sharedStrings.xml"
            if shared_path not in paths:
                raise ValueError("shared string indices but missing string table")
            captured = {}
            number = 0
            needed_max = max(needed_shared_indices)
            with z.open(shared_path) as stream:
                for event, el in ET.iterparse(stream, events=("end",)):
                    if el.tag == f"{{{MAIN_XML_NS}}}si":
                        if number in needed_shared_indices:
                            val = "".join(el.itertext())[:140]
                            captured[number] = val
                        number += 1
                        el.clear()
                        if number > needed_max:
                            break
            for section in sections:
                for c in section["first_row"]:
                    val = c.get("value")
                    if isinstance(val, dict) and "shared_index" in val:
                        c["value"] = captured.get(val["shared_index"], "UNRESOLVED_SHARED_STRING")

        # For an outcome-blind admission, do not expose test values even if
        # the first row is actually data rather than headers. Only text
        # labels in the first row are surfaced for manual schema admission.
        for section in sections:
            section["first_row_header_candidates"] = [
                c["value"] for c in section.pop("first_row")
                if isinstance(c["value"], str)
            ]
        return sections


def _self_test():
    workbook = f"""<?xml version="1.0" encoding="utf-8"?>
    <workbook xmlns="{MAIN_XML_NS}" xmlns:r="{DOC_REL_NS}">
    <sheets><sheet name="Spring" sheetId="1" r:id="rId1"/></sheets></workbook>"""
    rels = f"""<?xml version="1.0" encoding="utf-8"?>
    <Relationships xmlns="{PKG_REL_NS}">
    <Relationship Id="rId1" Target="worksheets/sheet1.xml"
    Type="{DOC_REL_NS}/worksheet"/></Relationships>"""
    sheet = f"""<worksheet xmlns="{MAIN_XML_NS}">
    <dimension ref="A1:B3"/><sheetData><row r="1">
    <c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c>
    </row><row r="2"><c r="A2"><v>55</v></c></row></sheetData></worksheet>"""
    strings = f"""<sst xmlns="{MAIN_XML_NS}">
    <si><t>bird_id</t></si><si><t>departure_day</t></si></sst>"""
    with io.BytesIO() as f:
        with zipfile.ZipFile(f, "w") as z:
            z.writestr("xl/workbook.xml", workbook)
            z.writestr("xl/_rels/workbook.xml.rels", rels)
            z.writestr("xl/worksheets/sheet1.xml", sheet)
            z.writestr("xl/sharedStrings.xml", strings)
        found = _sheet_meta(f.getvalue())
    assert len(found) == 1
    assert found[0]["sheet_name"] == "Spring"
    assert found[0]["xlsx_declared_dimension"] == "A1:B3"
    assert found[0]["first_row_header_candidates"] == ["bird_id", "departure_day"]
    print("HOUBARA_XLSX_METADATA_SYNTHETIC_PASS")


def main(output):
    payload = {
        "status": "SOURCE_ONLY_DATA_ACCESS_AND_SCHEMA_NOT_BIOLOGICAL_INFERENCE",
        "dataset": "Burnside et al. 2021 individual houbara climate-cue migration",
        "dataset_doi": "10.5281/zenodo.4917565",
        "article_doi": "10.1073/pnas.2026378118",
        "expected_file_md5": {
            name: fields[0] for name, fields in EXPECTED_FILES.items()
        },
        "prior_art": (
            "Original paper already established repeatable predeparture "
            "temperature cues, earlier population departure and arrival "
            "in warmer springs, and a wintering-site fidelity null"
        ),
        "source_outcome_rows_read": False,
        "behavioral_effect_estimated": False,
        "fitness_outcome_estimated": False,
    }
    workbook, wb_receipt = _download_verified("MigrationData.xlsx")
    payload["data_file"] = wb_receipt
    script, r_receipt = _download_verified("PNAS_code.R")
    payload["reproducibility_script"] = r_receipt
    if workbook is not None:
        try:
            payload["workbook_sheets_metadata"] = _sheet_meta(workbook)
            payload["data_file"]["status"] = "PUBLISHER_MD5_AND_OOXML_SCHEMA_PASS"
        except (ValueError, zipfile.BadZipFile, OSError, ET.ParseError) as exc:
            payload["data_file"]["status"] = "SCHEMA_HOLD"
            payload["schema_error"] = type(exc).__name__ + ": " + str(exc)[:200]
    if workbook is None:
        payload["overall_source_status"] = "ACCESS_HOLD"
    elif payload["data_file"]["status"] != "PUBLISHER_MD5_AND_OOXML_SCHEMA_PASS":
        payload["overall_source_status"] = "SCHEMA_HOLD"
    else:
        payload["overall_source_status"] = "SCHEMA_ONLY_PASS_PENDING_TEMPORAL_FIELDS"
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print("PAYOFF_B_HOUBARA_SOURCE_GATE " + json.dumps(payload, ensure_ascii=False)[:13000])
    return payload


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--output", default="outputs/payoff_b_houbara_source_gate_20261008.json")
    args = ap.parse_args()
    if args.self_test:
        _self_test()
    else:
        report = main(args.output)
        if (report.get("overall_source_status") !=
                "SCHEMA_ONLY_PASS_PENDING_TEMPORAL_FIELDS"):
            raise SystemExit(
                "SOURCE_GATE_FAILURE: pinned original Zenodo workbook "
                "was not retrieved with exact checksum and parsed "
                "in this execution. Failure receipt has been saved."
            )
        if (report.get("reproducibility_script", {}).get("status") !=
                "PUBLISHER_MD5_VERIFIED"):
            raise SystemExit(
                "SOURCE_GATE_FAILURE: matching original R-script MD5 "
                "was not verified during this execution."
            )
