"""Second, source-certified Scotland archive schema and join-key audit.

Examines the two DOI-backed Zenodo ZIPs and open EIDC support docs.
Does not fit any phenology/biomass/reproduction effects and does not bypass
password, login, or click-through licence terms.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

from scripts.payoff_b_scotland_resource_source_probe import (
    EIDC_ID, ZENODO, MAX_DOWNLOAD_BYTES,
    open_url, read_zenodo_metadata, validate_checksum,
)

ZIP_LIMIT = 9_000_000
CSV_COLUMN_LIMIT = 120
CSV_ROW_LIMIT = 250_000
DOI_BASE = "https://zenodo.org/api/records/"


def csv_manifest(zipf, name):
    info = zipf.getinfo(name)
    if info.file_size > 28_000_000:
        return {"name": name, "size": info.file_size,
                "status": "TOO_LARGE_FOR_BOUNDED_SCAN"}
    h = hashlib.sha256()
    with zipf.open(name) as fh:
        raw = fh.read(info.file_size + 1)
    if len(raw) != info.file_size:
        raise ValueError("Archive member truncated")
    h.update(raw)
    decoded = io.TextIOWrapper(io.BytesIO(raw), encoding="utf-8-sig",
                               errors="replace", newline="")
    rd = csv.DictReader(decoded)
    headers = rd.fieldnames or []
    if len(headers) > CSV_COLUMN_LIMIT:
        return {"name": name, "status": "TOO_MANY_COLUMNS",
                "n_columns": len(headers)}
    # Limit sample values/identifiers to non-sensitive field-schema audit.
    sample = []
    values = Counter()
    audit_fields = [
        x for x in headers
        if re.search(r"^site$|^year$|date|mass|biomass|caterpillar|beetle|spider|abund|habitat|tree", x, re.I)
    ]
    for j, row in enumerate(rd, 1):
        if j <= 4:
            sample.append({x:row.get(x) for x in audit_fields[:15]})
        if j >= CSV_ROW_LIMIT:
            break
    return {"name": name, "size": info.file_size,
            "sha256": h.hexdigest(), "status": "CSV_SCHEMA_READ",
            "n_columns": len(headers), "headers": headers,
            "audited_rows": j if 'j' in locals() else 0,
            "row_limit": CSV_ROW_LIMIT,
            "first_rows_relevant_fields": sample,
            "date_columns": [x for x in headers if re.search("date|doy|year", x, re.I)],
            "site_columns": [x for x in headers if re.search("site|tree|plot", x, re.I)],
            "prey_columns": [x for x in headers if re.search("caterpillar|beetle|spider|biomass|mass", x, re.I)],
            "outcome_columns": [x for x in headers if re.search("hatch|egg|fledg|nest", x, re.I)]}


def zenodo_zip_archive_schema(record_id):
    obj = read_zenodo_metadata(record_id)
    out = {"record": record_id, "record_status": obj["status"],
           "metadata_sha256": obj.get("metadata_sha256"), "files":[]}
    if obj["status"] != "METADATA_READABLE":
        return out
    for file in obj["files"]:
        name = file.get("key") or ""
        if not name.lower().endswith(".zip") or (file.get("size") or 0) > ZIP_LIMIT:
            continue
        r = open_url(file["link"], max_read=ZIP_LIMIT)
        raw = r.get("body")
        item = {"file": name, "http_status": r.get("http_status"),
                "size_manifest": file["size"]}
        if not raw:
            item["status"] = "NOT_DOWNLOADED"
        else:
            item["source_checksum"] = validate_checksum(raw, file.get("checksum"))
            if not item["source_checksum"]["verified"]:
                item["status"] = "CHECKSUM_MISMATCH_STOP"
            else:
                item["status"] = "SOURCE_VERIFIED"
                with zipfile.ZipFile(io.BytesIO(raw)) as z:
                    members = []
                    for name2 in z.namelist():
                        if name2.lower().endswith((".csv", ".tsv")):
                            members.append(csv_manifest(z, name2))
                        elif name2.lower().endswith(("readme.md","readme.txt")):
                            with z.open(name2) as f:
                                members.append({"name":name2,"readme_excerpt":f.read(3500).decode("utf-8",errors="replace")})
                    item["members"] = members
        out["files"].append(item)
    return out


def eidc_supporting_docs():
    url = f"https://data-package.ceh.ac.uk/sd/{EIDC_ID}.zip"
    res = open_url(url, timeout=45, max_read=ZIP_LIMIT)
    raw = res.get("body")
    out = {"supporting_url":url, "status_code":res.get("http_status"),
           "content_type":res.get("content_type")}
    if not raw:
        out["status"] = "NO_BOUNDED_SUPPORT_DOCUMENT"
        return out
    out["zip_sha256"] = hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        out["file_list"] = [{"name":i.filename,"size":i.file_size}
                            for i in z.infolist()[:100]]
        candidates = [i.filename for i in z.infolist()
                      if i.filename.endswith("ro-crate-metadata.json") and i.file_size < 4_000_000]
        if candidates:
            with z.open(candidates[0]) as f:
                meta = json.load(f)
            graph = meta.get("@graph",[])
            files = []
            for x in graph:
                if "File" not in str(x.get("@type", "")):
                    continue
                path = x.get("@id", "")
                if isinstance(path,str):
                    files.append({"path":path,
                                  "bytes":x.get("bytes"),
                                  "format":x.get("encodingFormat")})
            out["rocrate_files"] = files[:200]
        for info in z.infolist():
            if info.file_size > 0 and info.file_size <= 250_000 and info.filename.lower().endswith((".txt",".md")):
                with z.open(info.filename) as f:
                    out.setdefault("readme_excerpts",{})[info.filename] = f.read(12000).decode("utf-8",errors="replace")
    out["status"] = "PUBLIC_SUPPORT_DOCS_READ"
    return out


def audit():
    return {
        "status": "SCOTLAND_ZENODO_ARCHIVE_SCHEMA_AND_EIDC_SUPPORT_DOCS",
        "oikos_caterpillar": zenodo_zip_archive_schema(ZENODO["caterpillar_tree_taxon_2024"]),
        "beetles_spiders": zenodo_zip_archive_schema(ZENODO["alternative_prey_2026"]),
        "eidc": eidc_supporting_docs(),
        "bird_hatch_fledging_data_available_at_row_level": False,
        "real_prey_bird_join_performed": False,
        "real_fitness_effect_fitted": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args=parser.parse_args()
    result=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))


if __name__ == "__main__":
    main()
