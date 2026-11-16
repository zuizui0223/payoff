"""PAYOFF-B Scotland: source-faithful prefit catalogue and optional small-file schema audit.

Do NOT estimate ecological effects here. Never guess access tokens, scrape
private endpoints, or substitute synthetic data. Open/public Zenodo material is
fetched with source checksum verification. EIDC dataset requires separate
anonymous-access check; only metadata/header checked here.
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
from pathlib import Path

ZENODO = {
    "caterpillar_tree_taxon_2024": 14170139,
    "alternative_prey_2026": 23335990,
}
EIDC_ID = "b63d53ae-2fe7-4ce9-82a2-2325098489e3"
MAX_DOWNLOAD_BYTES = 24_000_000
MAX_TOTAL_BYTES = 38_000_000
MAX_CSV_SCAN_BYTES = 5_000_000
USER_AGENT = "PAYOFF-B-public-source-audit/1.0 (scientific citation; schema check)"


def open_url(url, *, method="GET", timeout=40, max_read=None):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            headers = dict(res.headers)
            if method == "HEAD":
                return {"http_status": res.status, "final_url": res.url,
                        "content_type": headers.get("Content-Type"),
                        "content_length": headers.get("Content-Length")}
            if max_read is None:
                raw = res.read()
            else:
                raw = res.read(max_read + 1)
                if len(raw) > max_read:
                    return {"http_status": res.status, "final_url": res.url,
                            "too_large": True, "max_bytes": max_read,
                            "content_type": headers.get("Content-Type")}
            return {"http_status": res.status, "final_url": res.url,
                    "content_type": headers.get("Content-Type"), "body": raw}
    except urllib.error.HTTPError as e:
        return {"http_status": e.code, "final_url": e.url,
                "error": "HTTPError", "content_type": e.headers.get("Content-Type")}
    except Exception as e:
        return {"http_status": None, "error": type(e).__name__,
                "detail": str(e)[:220]}


def read_zenodo_metadata(record_id):
    url = f"https://zenodo.org/api/records/{record_id}"
    response = open_url(url, max_read=2_000_000)
    raw = response.pop("body", None)
    if response.get("http_status") != 200 or not raw:
        return {"record_id": record_id, "metadata_url": url, "status": "BLOCKED", **response}
    rec = json.loads(raw)
    files = []
    for f in rec.get("files", []):
        files.append({
            "key": f.get("key"), "size": f.get("size"),
            "checksum": f.get("checksum"),
            "link": f.get("links", {}).get("self"),
        })
    return {
        "record_id": record_id,
        "metadata_url": url,
        "status": "METADATA_READABLE",
        "metadata_sha256": hashlib.sha256(raw).hexdigest(),
        "record_updated": rec.get("updated"),
        "record_created": rec.get("created"),
        "license": rec.get("metadata", {}).get("license"),
        "resource_type": rec.get("metadata", {}).get("resource_type"),
        "files": files,
    }


def validate_checksum(raw, expected):
    if not expected:
        return {"verified": False, "reason": "manifest_checksum_unavailable"}
    if ":" not in expected:
        return {"verified": False, "reason": "unknown_checksum_format"}
    name, value = expected.split(":", 1)
    if name not in ("md5", "sha256"):
        return {"verified": False, "reason": "unsupported_checksum_algorithm"}
    observed = hashlib.new(name, raw).hexdigest()
    return {"verified": observed.lower() == value.lower(), "algorithm": name,
            "expected": value.lower(), "observed": observed.lower()}


def inspect_csv_bytes(raw):
    # The raw file may use a BOM or Windows newline. Inspect column names only.
    sample = raw[:min(len(raw), MAX_CSV_SCAN_BYTES)]
    decoded = sample.decode("utf-8-sig", errors="replace")
    first_line = decoded.splitlines()[0] if decoded.splitlines() else ""
    sniff = "\t" if first_line.count("\t") > first_line.count(",") else ","
    try:
        header = next(csv.reader(io.StringIO(first_line), delimiter=sniff))
    except (StopIteration, csv.Error):
        header = []
    dates = [x for x in header if re.search("date|year|doy|time|julian", x, re.I)]
    site_ids = [x for x in header if re.search("site|locat|plot|wood|transect", x, re.I)]
    outcomes = [x for x in header if re.search("fledg|hatch|egg|brood|nest|surviv|mass", x, re.I)]
    return {"header": header[:100], "n_columns": len(header),
            "date_like": dates[:30], "site_like": site_ids[:30],
            "reproduction_or_mass_like": outcomes[:30],
            "delimiter": "tab" if sniff == "\t" else "comma",
            "sample_lines": len(decoded.splitlines()),
            "full_scan": len(raw) <= MAX_CSV_SCAN_BYTES}


def inspect_zip_bytes(raw):
    out = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos = z.infolist()
        for info in infos[:120]:
            member = {"name": info.filename, "size_uncompressed": info.file_size}
            if (info.filename.lower().endswith((".csv", ".tsv"))
                    and info.file_size <= MAX_CSV_SCAN_BYTES):
                with z.open(info) as f:
                    member["csv"] = inspect_csv_bytes(f.read())
            out.append(member)
    return {"zip_members": out, "zip_member_count": len(infos)}


def audit():
    receipts = {k: read_zenodo_metadata(v) for k, v in ZENODO.items()}
    total = 0
    for label, record in receipts.items():
        inspected = []
        if record.get("status") != "METADATA_READABLE":
            record["small_source_files"] = []
            continue
        files = sorted(record["files"], key=lambda f: f.get("size") or 10**30)
        for f in files:
            name = f.get("key") or ""
            url = f.get("link")
            size = f.get("size")
            candidate = name.lower().endswith((".csv", ".tsv", ".zip", ".txt", ".json", ".rdata", ".rds"))
            if (not candidate or not url or not isinstance(size, int)
                    or size > MAX_DOWNLOAD_BYTES or size + total > MAX_TOTAL_BYTES):
                continue
            res = open_url(url, max_read=MAX_DOWNLOAD_BYTES)
            raw = res.pop("body", None)
            item = {"file": name, "size_manifest": size, "http_status": res.get("http_status")}
            if raw:
                total += len(raw)
                item["size_downloaded"] = len(raw)
                item["sha256"] = hashlib.sha256(raw).hexdigest()
                item["manifest_checksum"] = validate_checksum(raw, f.get("checksum"))
                if not item["manifest_checksum"]["verified"]:
                    item["admitted"] = False
                    item["block_reason"] = "CHECKSUM_NOT_VERIFIED"
                else:
                    item["admitted"] = True
                    if name.lower().endswith((".csv", ".tsv")):
                        item["table_schema"] = inspect_csv_bytes(raw)
                    elif name.lower().endswith(".zip"):
                        try:
                            item["zip_schema"] = inspect_zip_bytes(raw)
                        except (OSError, zipfile.BadZipFile) as e:
                            item["zip_error"] = type(e).__name__
            else:
                item["block_reason"] = res.get("error") or "not_downloaded"
            inspected.append(item)
        record["small_source_files"] = inspected
    eidc = {}
    endpoints = {
        "catalogue_metadata": f"https://catalogue.ceh.ac.uk/documents/{EIDC_ID}",
        "packaged_data": f"https://data-package.ceh.ac.uk/data/{EIDC_ID}",
        "supporting_docs": f"https://data-package.ceh.ac.uk/sd/{EIDC_ID}.zip",
    }
    for key, url in endpoints.items():
        result = open_url(url, method="HEAD", timeout=25)
        eidc[key] = {"url": url, **result}
    return {
        "status": "SCOTLAND_ORIGINAL_SOURCE_ACCESS_SCHEMA_PREFLIGHT",
        "source_audit_date": "2026-11-16",
        "source_doi_main": "10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3",
        "source_zenodo_dois": ["10.5281/zenodo.14170139", "10.5281/zenodo.23335990"],
        "zenodo": receipts,
        "eidc_anonymous_head_only": eidc,
        "downloaded_candidate_bytes": total,
        "direct_joint_site_year_crosswalk_certified": False,
        "food_supply_is_dietary_intake": False,
        "real_caterpillar_biomass_and_blue_tit_fitness_model_fitted": False,
        "ready_to_fit": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    r = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(r, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
