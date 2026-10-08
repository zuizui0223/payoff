"""Source-only gate for Schindler et al. (2024) Greenland white-fronted geese.

DOI 10.5061/dryad.2547d7wzn. No breeding-outcome association is fitted.
All results here are source eligibility, schema, chronology, dependence and
reproducibility receipts; they cannot confirm a PAYOFF-B information mechanism.

Run:
  python scripts/audit_payoff_b_goose_fitness_source.py --output outputs/payoff_b_goose_fitness_source_gate.json
  python scripts/audit_payoff_b_goose_fitness_source.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zipfile import ZipFile, BadZipFile

DOI = "10.5061/dryad.2547d7wzn"
API_BASE = "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.2547d7wzn"
AUTHOR_REPO_COMMIT = "2171bcd36bf37022c8716e15c0f75412103b0f3f"
AUTHOR_SOURCE_BASE = (
    "https://raw.githubusercontent.com/aschindler23/"
    "Schindler_etal_2024_ProcB/" + AUTHOR_REPO_COMMIT + "/"
)
DRYAD_MANIFEST_SHA256 = {
    "spring_data.csv": "9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd",
    "autumn_data.csv": "4dc6fe4e91b2130596bb5d5a2c3620fc183ce5e4809ab4c7d80cf2e2d9f34288",
}
EXPECTED_FIELDS = (
    "id", "year", "sub_season", "breeding_outcome", "breeding_success",
    "first_day", "log_ODBA", "num_feed_fixes", "num_ACC_fixes",
    "mean_precip", "prop_days_below_freezing", "prop_storm_days",
    "prop_grass", "prop_ag", "prop_bog",
)
ALLOWED_SPRING_SEASONS = {1, 2, 3, 4, 5, 6}
MAX_BYTES = 3_000_000


def retrieve(url: str, accept: str, timeout: int = 25) -> tuple[bytes, str]:
    headers = {
        "User-Agent": "PAYOFF-B-public-source-eligibility/1.0",
        "Accept": accept,
    }
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        size = int(response.headers.get("Content-Length", "0") or 0)
        if size > MAX_BYTES:
            raise ValueError("source exceeds declared size gate")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("source archive exceeds declared byte cap")
        return raw, response.headers.get("Content-Type", "")


def parse_csv_bytes(raw: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text_data = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text_data))
    fields = list(reader.fieldnames or [])
    if not fields or len(fields) != len(set(fields)):
        raise ValueError("empty/duplicate header fields")
    rows = list(reader)
    if not rows:
        raise ValueError("source CSV is empty")
    if any(None in row for row in rows):
        raise ValueError("malformed CSV with extra unheadered columns")
    return fields, rows


def audit_spring_csv(raw: bytes) -> dict:
    fields, rows = parse_csv_bytes(raw)
    absent = sorted(set(EXPECTED_FIELDS) - set(fields))
    verdict = "SOURCE_SCHEMA_HOLD" if absent else "SOURCE_SCHEMA_PASS"
    keys: set[tuple[str, str, str]] = set()
    duplicates = 0
    bird_year_seasons: dict[tuple[str, str], set[int]] = defaultdict(set)
    outcome_sets: dict[tuple[str, str], set[str]] = defaultdict(set)
    timing_failures = 0
    feeding_range_failures = 0
    years: set[str] = set()
    # This loop checks only admissibility and internal consistency, and does
    # not show or regress reproductive outcome values, despite verifying
    # that a bird-year is not coded with mutually inconsistent outcomes.
    for row in rows:
        bird_id = (row.get("id") or "").strip()
        year = (row.get("year") or "").strip()
        sub = (row.get("sub_season") or "").strip()
        if not bird_id or not year or not sub:
            verdict = "SOURCE_SCHEMA_HOLD"
            continue
        k = (bird_id, year, sub)
        if k in keys:
            duplicates += 1
        keys.add(k)
        years.add(year)
        try:
            iv = int(float(sub))
            if float(sub) != iv or iv not in ALLOWED_SPRING_SEASONS:
                timing_failures += 1
            else:
                bird_year_seasons[(bird_id, year)].add(iv)
        except ValueError:
            timing_failures += 1
        outcome = (row.get("breeding_outcome") or "").strip()
        if outcome and outcome.upper() not in {"NA", "NAN"}:
            outcome_sets[(bird_id, year)].add(outcome)
        try:
            d = float((row.get("first_day") or ""))
            if not math.isfinite(d) or not 1 <= d <= 366:
                timing_failures += 1
        except ValueError:
            timing_failures += 1
        fed = (row.get("num_feed_fixes") or "").strip()
        allacc = (row.get("num_ACC_fixes") or "").strip()
        if fed and allacc and fed.upper() != "NA" and allacc.upper() != "NA":
            try:
                f, a = float(fed), float(allacc)
                if not (math.isfinite(f) and math.isfinite(a)
                        and 0 <= f <= a and a > 0):
                    feeding_range_failures += 1
            except ValueError:
                feeding_range_failures += 1

    conflicting_bird_years = sum(len(v) > 1 for v in outcome_sets.values())
    complete_bird_years = sum(s == ALLOWED_SPRING_SEASONS for s in bird_year_seasons.values())
    distinct_bird_years = len(bird_year_seasons)
    if duplicates or timing_failures or feeding_range_failures or conflicting_bird_years:
        verdict = "SOURCE_SCHEMA_HOLD"
    return {
        "status": verdict,
        "row_count": len(rows),
        "distinct_birds": len({b for b, _ in bird_year_seasons}),
        "distinct_bird_years": distinct_bird_years,
        "full_six_subseason_bird_years": complete_bird_years,
        "listed_year_codes": sorted(years),
        "field_names": fields,
        "required_fields_absent": absent,
        "duplicate_id_year_subseason": duplicates,
        "subseason_or_first_day_out_of_range": timing_failures,
        "ACC_feeding_range_errors": feeding_range_failures,
        "conflicting_bird_year_outcome_codes": conflicting_bird_years,
        "outcome_values_not_reported": True,
        "outcome_model_fitted": False,
    }


def audit_zip(raw: bytes) -> dict:
    with ZipFile(io.BytesIO(raw)) as zipped:
        names = zipped.namelist()
        candidates = [
            n for n in names
            if Path(n).name.lower() in ("spring_data.csv", "spring_dat.csv")
        ]
        if len(candidates) != 1:
            return {
                "status": "SOURCE_ARCHIVE_SCHEMA_HOLD",
                "source_archive_files": names,
                "candidate_spring_file_count": len(candidates),
                "outcome_model_fitted": False,
            }
        spring = zipped.read(candidates[0])
        result = audit_spring_csv(spring)
        result["spring_filename"] = candidates[0]
        result["spring_sha256"] = hashlib.sha256(spring).hexdigest()
        result["source_archive_files"] = names
        return result


def run(output: str) -> dict:
    receipt = {
        "source": "Schindler et al. 2024, Proceedings of the Royal Society B",
        "doi": DOI,
        "source_url": "https://doi.org/" + DOI,
        "api_download_endpoint": API_BASE + "/download",
        "source_data_classification": "INDEPENDENT_FITNESS_SOURCE_SCREEN",
        "previous_authors_already_established": (
            "spring feeding/energy expenditure predicts reproductive outcome"
        ),
        "accessed_at_utc": datetime.now(timezone.utc).isoformat(),
        "outcome_model_fitted": False,
    }
    try:
        meta, _ = retrieve(API_BASE, "application/json")
        meta_json = json.loads(meta)
        receipt["dataset_title"] = meta_json.get("title")
        receipt["version_number"] = meta_json.get("versionNumber")
        receipt["data_license"] = meta_json.get("license")
        receipt["metadata_access"] = "PASS"
        # Public read-only metadata lists the exact version's file entries
        # even when bulk download requires authorization. This is not a
        # substitute for having the bytes to audit.
        try:
            from urllib.parse import urljoin
            v = (meta_json.get("_links", {}).get("stash:version") or
                 meta_json.get("_links", {}).get("version") or {})
            version_url = urljoin("https://datadryad.org", v.get("href", ""))
            if version_url.endswith("/") or not version_url.startswith("https://datadryad.org/api/v2/versions/"):
                raise ValueError("published version ID was not available")
            data, _ = retrieve(version_url + "/files", "application/json")
            listing = json.loads(data)
            files = listing.get("_embedded", {})
            enumerated = [v for val in files.values() if isinstance(val, list) for v in val if isinstance(v, dict)]
            receipt["public_manifest"] = [
                {k: x.get(k) for k in ("path", "size", "mimeType", "digest", "digestType", "id")}
                for x in enumerated
            ]
            receipt["file_manifest_access"] = "PASS"
        except (HTTPError, URLError, ValueError, TimeoutError, json.JSONDecodeError) as manifest_exc:
            receipt["file_manifest_access"] = "UNAVAILABLE"
            receipt["manifest_error"] = type(manifest_exc).__name__ + ": " + str(manifest_exc)[:200]
    except (HTTPError, URLError, ValueError, TimeoutError, json.JSONDecodeError) as exc:
        receipt["metadata_access"] = "UNAVAILABLE"
        receipt["metadata_error"] = type(exc).__name__ + ": " + str(exc)[:200]

    try:
        raw, content_type = retrieve(API_BASE + "/download", "application/zip")
        receipt["download_content_type"] = content_type
        receipt["archive_size_bytes"] = len(raw)
        receipt["archive_sha256"] = hashlib.sha256(raw).hexdigest()
        audit = audit_zip(raw)
        receipt.update(audit)
    except (HTTPError, URLError, ValueError, BadZipFile, TimeoutError) as exc:
        receipt["status"] = "SOURCE_ARCHIVE_ACCESS_HOLD"
        receipt["access_error"] = type(exc).__name__ + ": " + str(exc)[:200]

    # A public, independently maintained AUTHOR repository hosts plaintext
    # spring and autumn tables. Query its pinned historical commit, never an
    # unspecified moving branch. Read values for source/schema validation only:
    # do not fit fertility/survival or transfer hypotheses at this stage.
    mirror = {
        "repository": "aschindler23/Schindler_etal_2024_ProcB",
        "commit": AUTHOR_REPO_COMMIT,
    }
    for filename in ("spring_data.csv", "autumn_data.csv"):
        try:
            tab, _ = retrieve(AUTHOR_SOURCE_BASE + filename, "text/csv")
            meta = audit_spring_csv(tab)
            checksum_lf = hashlib.sha256(tab).hexdigest()
            normalized_crlf = tab.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            checksum_crlf = hashlib.sha256(normalized_crlf).hexdigest()
            target = DRYAD_MANIFEST_SHA256[filename]
            mirror[filename] = {
                "source_url": AUTHOR_SOURCE_BASE + filename,
                "size_bytes": len(tab),
                "sha256_author_bytes": checksum_lf,
                "sha256_normalized_crlf": checksum_crlf,
                "sha256_published_dryad_manifest": target,
                "exact_bytes_match_dryad": checksum_lf == target,
                "crlf_normalized_bytes_match_dryad": checksum_crlf == target,
                "admission": meta,
            }
            if meta["status"] != "SOURCE_SCHEMA_PASS":
                mirror[filename]["status"] = "AUTHOR_SOURCE_SCHEMA_HOLD"
            elif checksum_lf == target or checksum_crlf == target:
                mirror[filename]["status"] = "AUTHOR_SOURCE_DRYAD_DIGEST_VERIFIED"
            else:
                mirror[filename]["status"] = "AUTHOR_SOURCE_SCHEMA_PASS_VERSION_IDENTITY_HOLD"
        except (HTTPError, URLError, ValueError, TimeoutError, UnicodeDecodeError) as author_exc:
            mirror[filename] = {
                "status": "AUTHOR_SOURCE_ACCESS_HOLD",
                "error": type(author_exc).__name__ + ": " + str(author_exc)[:200],
            }
    receipt["author_repository_source_gate"] = mirror
    spring_status = mirror.get("spring_data.csv", {}).get("status")
    autumn_status = mirror.get("autumn_data.csv", {}).get("status")
    if (spring_status == "AUTHOR_SOURCE_DRYAD_DIGEST_VERIFIED" and
            autumn_status == "AUTHOR_SOURCE_DRYAD_DIGEST_VERIFIED"):
        receipt["fitness_raw_source_status"] = (
            "AUTHOR_SOURCE_VALIDATED_VS_DRYAD_CHECKSUMS; "
            "OUTCOME_UNOPENED_IN_PAYOFF"
        )
    else:
        receipt["fitness_raw_source_status"] = "AUTHOR_SOURCE_INCOMPLETE_OR_UNMATCHED"

    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        "PAYOFF_B_GOOSE_FITNESS_SOURCE_GATE "
        + json.dumps({
            k: receipt.get(k)
            for k in ("status", "metadata_access", "version_number",
                      "file_manifest_access", "public_manifest", "fitness_raw_source_status", "row_count", "distinct_birds", "distinct_bird_years",
                      "full_six_subseason_bird_years", "required_fields_absent",
                      "duplicate_id_year_subseason", "archive_sha256",
                      "access_error")
        }, ensure_ascii=False)
    )
    return receipt


def self_test() -> None:
    import zipfile
    fixture = io.StringIO()
    w = csv.DictWriter(fixture, fieldnames=list(EXPECTED_FIELDS))
    w.writeheader()
    for season in range(1, 7):
        w.writerow({
            "id": "bird-test", "year": "1", "sub_season": str(season),
            "breeding_outcome": "1", "breeding_success": "1",
            "first_day": str(30 + season * 20), "log_ODBA": "0.2",
            "num_feed_fixes": "4", "num_ACC_fixes": "10",
            "mean_precip": "2", "prop_days_below_freezing": "0.2",
            "prop_storm_days": "0.1", "prop_grass": "0.3",
            "prop_ag": "0.4", "prop_bog": "0.3",
        })
    with io.BytesIO() as stream:
        with ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("spring_data.csv", fixture.getvalue())
        x = audit_zip(stream.getvalue())
    assert x["status"] == "SOURCE_SCHEMA_PASS", x
    assert x["full_six_subseason_bird_years"] == 1
    assert x["row_count"] == 6
    assert x["outcome_model_fitted"] is False

    bad = fixture.getvalue().replace("bird-test,1,3,", "bird-test,1,2,")
    y = audit_spring_csv(bad.encode())
    assert y["status"] == "SOURCE_SCHEMA_HOLD"
    assert y["duplicate_id_year_subseason"] == 1
    print("PAYOFF_B_GOOSE_FITNESS_SOURCE_SYNTHETIC_TEST_PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--output", default="outputs/payoff_b_goose_fitness_source_gate.json"
    )
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        run(args.output)
