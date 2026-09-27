#!/usr/bin/env python3
"""Materialize and audit the registered Hoge Veluwe Gate-A sources.

This script is intentionally source-readiness only. It may download and inspect
individual source files to certify immutable hashes, file identities, schemas
and year coverage. It must not join the migrant, resident, resource and cue
coordinates, calculate focal-partner mismatch, calculate cue-resource
connectivity, choose a breakpoint, or run the registered history test.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import quote, urljoin

ROOT = Path(__file__).resolve().parents[1]
DRYAD_API = "https://datadryad.org/api/v2"
DRYAD_WEB = "https://datadryad.org"

YEAR_HEADER_RE = re.compile(r"(?i)(^|[^a-z])(year|yr|jaar)([^a-z]|$)")
FILENAME_RE = re.compile(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', re.I)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--contract",
        type=Path,
        default=ROOT
        / "data"
        / "payoff_b_hoge_veluwe_network_hysteresis_contract_20260927.json",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/hoge_veluwe_source_gate_a"),
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=120,
    )
    return p.parse_args()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _session():
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "PAYOFF-B-Hoge-Veluwe-source-gate/1.0"}
    )
    retry = Retry(
        total=6,
        connect=4,
        read=4,
        status=6,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=2,
        pool_maxsize=2,
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _api_url(href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return urljoin(DRYAD_WEB, href)


def _get_json(session, url: str, timeout: int) -> dict:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def _dryad_latest_files(session, doi: str, timeout: int):
    encoded = quote(f"doi:{doi}", safe="")
    versions_url = f"{DRYAD_API}/datasets/{encoded}/versions"
    versions = _get_json(session, versions_url, timeout)
    rows = (
        versions.get("_embedded", {})
        .get("stash:versions", [])
    )
    if not rows:
        raise RuntimeError(f"Dryad DOI has no visible versions: {doi}")

    def version_key(row):
        return (
            int(row.get("versionNumber") or 0),
            str(row.get("publicationDate") or ""),
        )

    latest = max(rows, key=version_key)
    files_href = latest.get("_links", {}).get("stash:files", {}).get("href")
    if not files_href:
        raise RuntimeError(f"Dryad version has no files link: {doi}")

    files = []
    page = 1
    while True:
        separator = "&" if "?" in files_href else "?"
        url = _api_url(files_href) + f"{separator}per_page=100&page={page}"
        payload = _get_json(session, url, timeout)
        chunk = (
            payload.get("_embedded", {})
            .get("stash:files", [])
        )
        files.extend(chunk)
        total = int(payload.get("total") or len(files))
        if len(files) >= total:
            break
        if not chunk:
            raise RuntimeError(
                f"Dryad file pagination stopped early for {doi}: "
                f"{len(files)}/{total}"
            )
        page += 1
    return latest, files


def _dryad_download_file(
    session,
    doi: str,
    exact_name: str,
    output_dir: Path,
    timeout: int,
) -> dict:
    latest, files = _dryad_latest_files(session, doi, timeout)
    matches = [row for row in files if row.get("path") == exact_name]
    if len(matches) != 1:
        names = [row.get("path") for row in files]
        raise RuntimeError(
            f"expected one Dryad file {exact_name!r}, found {len(matches)}; "
            f"available={names}"
        )
    meta = matches[0]
    self_href = meta.get("_links", {}).get("self", {}).get("href", "")
    file_id = self_href.rstrip("/").split("/")[-1]
    download_href = (
        meta.get("_links", {})
        .get("stash:download", {})
        .get("href")
    )
    candidates = []
    if download_href:
        candidates.append(_api_url(download_href))
    if file_id:
        # Public Dryad landing pages expose file bytes through /downloads/
        # rather than the authenticated API /files/{id}/download endpoint.
        candidates.extend(
            [
                f"{DRYAD_WEB}/downloads/file_stream/{file_id}",
                f"http://datadryad.org/downloads/file_stream/{file_id}",
            ]
        )

    response = None
    errors = []
    for url in candidates:
        try:
            trial = session.get(url, timeout=timeout, allow_redirects=True)
            if trial.ok and trial.content:
                response = trial
                break
            errors.append(f"{url}: HTTP {trial.status_code}")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    if response is None:
        raise RuntimeError(
            f"could not download Dryad file {exact_name!r}: {errors}"
        )

    target = output_dir / exact_name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.content)
    digest = sha256_path(target)

    declared_digest = meta.get("digest")
    declared_type = str(meta.get("digestType") or "").lower()
    digest_match = None
    if declared_digest and declared_type in {"sha-256", "sha256"}:
        digest_match = digest.lower() == str(declared_digest).lower()
        if not digest_match:
            raise RuntimeError(
                f"Dryad SHA-256 mismatch for {exact_name}: "
                f"computed={digest} declared={declared_digest}"
            )

    return {
        "source_kind": "dryad",
        "doi": doi,
        "version_number": latest.get("versionNumber"),
        "publication_date": latest.get("publicationDate"),
        "file_id": file_id,
        "filename": exact_name,
        "declared_size": meta.get("size"),
        "downloaded_size": target.stat().st_size,
        "mime_type": meta.get("mimeType"),
        "declared_digest": declared_digest,
        "declared_digest_type": meta.get("digestType"),
        "sha256": digest,
        "declared_digest_match": digest_match,
        "download_url_used": response.url,
        "path": str(target),
    }


def _content_disposition_filename(headers) -> str | None:
    value = headers.get("Content-Disposition", "")
    match = FILENAME_RE.search(value)
    if not match:
        return None
    return match.group(1).strip().strip('"')


def _mda_download_file(session, url: str, output_dir: Path, timeout: int) -> dict:
    response = session.get(url, timeout=timeout, allow_redirects=True)
    response.raise_for_status()
    payload = response.content
    if not payload:
        raise RuntimeError("Marine Data Archive returned an empty source file")

    name = _content_disposition_filename(response.headers)
    content_type = response.headers.get("Content-Type", "")
    if not name:
        if payload[:4] == b"PK\x03\x04":
            name = "tomotani_migrant_source.xlsx"
        elif payload[:2] == b"\x1f\x8b":
            name = "tomotani_migrant_source.gz"
        else:
            name = "tomotani_migrant_source.dat"

    target = output_dir / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    return {
        "source_kind": "marine_data_archive",
        "registered_url": url,
        "download_url_used": response.url,
        "filename": name,
        "downloaded_size": target.stat().st_size,
        "content_type": content_type,
        "sha256": sha256_path(target),
        "path": str(target),
    }


def _normalized_header(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _year_value(value) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    rounded = int(round(number))
    if abs(number - rounded) > 1e-6:
        return None
    if 1900 <= rounded <= 2100:
        return rounded
    return None


def _inspect_xlsx_bytes(payload: bytes) -> dict:
    import openpyxl

    workbook = openpyxl.load_workbook(
        io.BytesIO(payload),
        read_only=True,
        data_only=True,
    )
    sheets = []
    for ws in workbook.worksheets:
        rows = ws.iter_rows(values_only=True)
        first_rows = []
        for _ in range(10):
            try:
                first_rows.append(next(rows))
            except StopIteration:
                break
        header_index = None
        header = None
        for idx, row in enumerate(first_rows):
            values = [_normalized_header(v) for v in row]
            nonempty = [v for v in values if v]
            if len(nonempty) >= 2:
                header_index = idx
                header = values
                break
        if header is None:
            sheets.append(
                {
                    "sheet": ws.title,
                    "header_row": None,
                    "columns": [],
                    "max_row": ws.max_row,
                    "max_column": ws.max_column,
                    "year_columns": [],
                }
            )
            continue

        year_columns = []
        for col_idx, name in enumerate(header):
            if not name or not YEAR_HEADER_RE.search(name):
                continue
            years = []
            # Include any rows already consumed after the header.
            for row in first_rows[header_index + 1 :]:
                if col_idx < len(row):
                    year = _year_value(row[col_idx])
                    if year is not None:
                        years.append(year)
            # Continue streaming the rest of the worksheet.
            for row in rows:
                if col_idx < len(row):
                    year = _year_value(row[col_idx])
                    if year is not None:
                        years.append(year)
            year_columns.append(
                {
                    "column": name,
                    "unique_year_count": len(set(years)),
                    "min_year": min(years) if years else None,
                    "max_year": max(years) if years else None,
                }
            )
            # Worksheet iterator is consumed by the first year column. There is
            # normally only one calendar-year column in these registered files.
            break

        sheets.append(
            {
                "sheet": ws.title,
                "header_row": header_index + 1,
                "columns": [name for name in header if name],
                "max_row": ws.max_row,
                "max_column": ws.max_column,
                "year_columns": year_columns,
            }
        )
    return {
        "format": "xlsx",
        "sheets": sheets,
    }


def _inspect_delimited_text(payload: bytes) -> dict:
    import csv

    text = payload.decode("utf-8-sig")
    sample = text[:8192]
    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    reader = csv.reader(io.StringIO(text), dialect)
    rows = list(reader)
    if not rows:
        return {"format": "delimited_text", "columns": [], "year_columns": []}
    header = [_normalized_header(v) for v in rows[0]]
    year_columns = []
    for col_idx, name in enumerate(header):
        if not name or not YEAR_HEADER_RE.search(name):
            continue
        years = []
        for row in rows[1:]:
            if col_idx < len(row):
                year = _year_value(row[col_idx])
                if year is not None:
                    years.append(year)
        year_columns.append(
            {
                "column": name,
                "unique_year_count": len(set(years)),
                "min_year": min(years) if years else None,
                "max_year": max(years) if years else None,
            }
        )
    return {
        "format": "delimited_text",
        "columns": [name for name in header if name],
        "row_count": len(rows),
        "year_columns": year_columns,
    }


def inspect_source(path: Path) -> dict:
    payload = path.read_bytes()
    try:
        return _inspect_xlsx_bytes(payload)
    except Exception as xlsx_error:
        xlsx_error_text = f"{type(xlsx_error).__name__}: {xlsx_error}"

    try:
        if b"\x00" not in payload[:4096]:
            result = _inspect_delimited_text(payload)
            result["xlsx_open_error"] = xlsx_error_text
            return result
    except Exception as text_error:
        text_error_text = f"{type(text_error).__name__}: {text_error}"
    else:
        text_error_text = "binary_or_not_delimited"

    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            members = sorted(archive.namelist())
        return {
            "format": "zip",
            "members": members,
            "xlsx_open_error": xlsx_error_text,
            "text_open_error": text_error_text,
        }

    return {
        "format": "unknown_binary",
        "bytes": len(payload),
        "magic_hex": payload[:16].hex(),
        "xlsx_open_error": xlsx_error_text,
        "text_open_error": text_error_text,
    }


def _coverage_candidates(schema: dict) -> list[dict]:
    if schema.get("format") == "xlsx":
        rows = []
        for sheet in schema.get("sheets", []):
            for year in sheet.get("year_columns", []):
                rows.append({"sheet": sheet.get("sheet"), **year})
        return rows
    return list(schema.get("year_columns", []))


def _covers(schema: dict, start: int, end: int) -> bool:
    for row in _coverage_candidates(schema):
        lo = row.get("min_year")
        hi = row.get("max_year")
        if lo is not None and hi is not None and lo <= start and hi >= end:
            return True
    return False


def _source_gate_status(
    contract: dict,
    migrant_schema: dict,
    resident_schema: dict,
    resource_schema: dict,
) -> tuple[str, list[str]]:
    reasons = []
    if not _covers(
        migrant_schema,
        contract["sources"]["migrant_timing"]["years"][0],
        contract["sources"]["migrant_timing"]["years"][1],
    ):
        reasons.append("MIGRANT_YEAR_COVERAGE_NOT_CERTIFIED")
    if not _covers(
        resident_schema,
        contract["sources"]["resident_partner_timing"]["years"][0],
        contract["sources"]["resident_partner_timing"]["years"][1],
    ):
        reasons.append("RESIDENT_YEAR_COVERAGE_NOT_CERTIFIED")
    if not _covers(
        resource_schema,
        contract["sources"]["destination_resource_state"]["years"][0],
        contract["sources"]["destination_resource_state"]["years"][1],
    ):
        reasons.append("RESOURCE_YEAR_COVERAGE_NOT_CERTIFIED")

    if reasons:
        return "SCHEMA_REVIEW_REQUIRED", reasons
    return "BIOLOGICAL_SOURCE_GATE_PASS_CUE_EXTENSION_PENDING", reasons


def main():
    args = parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sources_dir = args.output_dir / "source_files"
    if sources_dir.exists():
        shutil.rmtree(sources_dir)
    sources_dir.mkdir(parents=True)

    session = _session()

    migrant = _mda_download_file(
        session,
        contract["sources"]["migrant_timing"]["archive_url"],
        sources_dir,
        args.timeout,
    )
    resident = _dryad_download_file(
        session,
        contract["sources"]["resident_partner_timing"]["dataset_doi"],
        contract["sources"]["resident_partner_timing"]["file"],
        sources_dir,
        args.timeout,
    )
    resource = _dryad_download_file(
        session,
        contract["sources"]["destination_resource_state"]["dataset_doi"],
        contract["sources"]["destination_resource_state"]["file"],
        sources_dir,
        args.timeout,
    )

    migrant_schema = inspect_source(Path(migrant["path"]))
    resident_schema = inspect_source(Path(resident["path"]))
    resource_schema = inspect_source(Path(resource["path"]))

    status, reasons = _source_gate_status(
        contract,
        migrant_schema,
        resident_schema,
        resource_schema,
    )

    receipt = {
        "result_id": "payoff_b_hoge_veluwe_source_gate_a_20260927",
        "contract_id": contract["contract_id"],
        "status": status,
        "reasons": reasons,
        "registered_source_overlap": contract["population"]["primary_overlap_years"],
        "registered_history_span": contract["population"][
            "primary_history_years_after_connectivity_construction"
        ],
        "registered_history_year_count": contract["population"][
            "expected_primary_history_year_count"
        ],
        "site_alignment": {
            "registered_site": contract["population"]["site"],
            "resident_resource_basis": (
                "Dryad DOI 10.5061/dryad.f1vhhmgx6 is published for the "
                "Hoge Veluwe great-tit population and registered exact files"
            ),
            "migrant_basis": (
                "Tomotani et al. Marine Data Archive dataset linked to "
                "DOI 10.1111/gcb.14006 and the registered Hoge Veluwe lane"
            ),
            "joined_site_filter_applied": False,
        },
        "sources": {
            "migrant_timing": {
                "provenance": migrant,
                "schema": migrant_schema,
            },
            "resident_partner_timing": {
                "provenance": resident,
                "schema": resident_schema,
            },
            "destination_resource_state": {
                "provenance": resource,
                "schema": resource_schema,
            },
        },
        "cue_extension": {
            "status": "PENDING_SEPARATE_SOURCE_FAITHFUL_EXTENSION",
            "rule": contract["sources"]["precommitment_cue"]["spatial_rule"],
        },
        "outcome_firewall": {
            "cross_source_join_performed": False,
            "focal_partner_mismatch_computed": False,
            "cue_resource_connectivity_computed": False,
            "information_reversal_gate_opened": False,
            "history_test_opened": False,
            "migrant_timing_values_exported": False,
            "resident_timing_values_exported": False,
            "resource_peak_values_exported": False,
        },
        "claim_boundary": (
            "Gate A certifies source identity, immutable bytes, schema and year "
            "coverage only. It is not an empirical hysteresis result."
        ),
    }

    # Do not retain raw source files in the uploaded Gate-A artifact.
    receipt_path = args.output_dir / "source_gate_a_receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    shutil.rmtree(sources_dir)

    print(
        "PAYOFF_B_HV_SOURCE_GATE_A "
        f"status={status} "
        f"migrant_sha256={migrant['sha256']} "
        f"resident_sha256={resident['sha256']} "
        f"resource_sha256={resource['sha256']}"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
