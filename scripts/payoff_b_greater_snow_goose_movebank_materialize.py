#!/usr/bin/env python3
"""Materialize authorized Greater Snow Goose GPS events from Movebank.

Operational only. This script does not analyze movement outcomes.

Security / governance:
- credentials are never accepted as command-line arguments;
- an API token must be supplied via MOVEBANK_API_TOKEN;
- license terms are NEVER accepted automatically;
- if Movebank returns a license-terms page, the script writes a blocked
  manifest and exits non-zero;
- raw event CSVs are written outside version-controlled data paths and are
  intended for workflow artifacts / local protected storage only.

The scientific analysis is frozen separately. Downloading raw events after the
pre-outcome freeze does not authorize any change to the preregistered model,
context, q definition, or threshold rule.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Iterable

import requests


ENDPOINT = "https://www.movebank.org/movebank/service/direct-read"
STUDY_ID = "1442516400"
GPS_SENSOR_TYPE_ID = "653"
YEARS = tuple(range(2019, 2024))
ATTRIBUTES = (
    "timestamp",
    "location_long",
    "location_lat",
    "individual_id",
    "individual_local_identifier",
    "tag_id",
    "tag_local_identifier",
    "visible",
)


class MaterializationBlocked(RuntimeError):
    """Operational access blocker; not a scientific failure."""


def movebank_timestamp_start(year: int) -> str:
    return f"{int(year):04d}0101000000000"


def movebank_timestamp_end(year: int) -> str:
    return f"{int(year):04d}1231235959999"


def expected_header_fields() -> set[str]:
    return set(ATTRIBUTES)


def looks_like_license_terms(prefix: bytes) -> bool:
    text = prefix.decode("utf-8", errors="ignore").lower()
    return "license terms:" in text or "<html" in text and "license" in text


def validate_csv_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise MaterializationBlocked("Movebank response CSV is empty") from exc
    normalized = [x.strip().strip('"') for x in header]
    missing = expected_header_fields() - set(normalized)
    if missing:
        raise MaterializationBlocked(
            "Movebank event response missing required columns: "
            + ",".join(sorted(missing))
        )
    return normalized


def count_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return max(0, sum(1 for _ in fh) - 1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_year(
    session: requests.Session,
    *,
    api_token: str,
    year: int,
    output_dir: Path,
) -> dict:
    """Download one full calendar year of GPS events, preserving raw rows."""

    output_dir.mkdir(parents=True, exist_ok=True)
    final_path = output_dir / f"greater_snow_goose_movebank_{year}.csv"
    part_path = final_path.with_suffix(".csv.part")

    params = {
        "entity_type": "event",
        "study_id": STUDY_ID,
        "sensor_type_id": GPS_SENSOR_TYPE_ID,
        "timestamp_start": movebank_timestamp_start(year),
        "timestamp_end": movebank_timestamp_end(year),
        "attributes": ",".join(ATTRIBUTES),
        "api-token": api_token,
    }

    try:
        response = session.get(
            ENDPOINT,
            params=params,
            timeout=(30, 900),
            stream=True,
            headers={"User-Agent": "PAYOFF-B-snow-goose-materializer/1.0"},
        )
    except requests.RequestException as exc:
        raise MaterializationBlocked(
            f"Movebank request failed for {year}: {type(exc).__name__}"
        ) from exc

    if response.status_code != 200:
        raise MaterializationBlocked(
            f"Movebank returned HTTP {response.status_code} for {year}"
        )

    prefix = bytearray()
    digest = hashlib.sha256()
    bytes_written = 0

    try:
        with part_path.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                if len(prefix) < 131072:
                    remaining = 131072 - len(prefix)
                    prefix.extend(chunk[:remaining])
                fh.write(chunk)
                digest.update(chunk)
                bytes_written += len(chunk)

        if looks_like_license_terms(bytes(prefix)):
            part_path.unlink(missing_ok=True)
            raise MaterializationBlocked(
                "Movebank returned license terms instead of event CSV. "
                "Accept the study terms in Movebank with the authorized account, "
                "then rerun. This script will not accept terms automatically."
            )

        if bytes_written == 0:
            part_path.unlink(missing_ok=True)
            raise MaterializationBlocked(
                f"Movebank returned an empty response for {year}"
            )

        header = validate_csv_header(part_path)
        rows = count_rows(part_path)

        if rows == 0:
            part_path.unlink(missing_ok=True)
            raise MaterializationBlocked(
                f"Movebank returned zero GPS event rows for {year}"
            )

        part_path.replace(final_path)
        return {
            "year": year,
            "status": "MATERIALIZED",
            "path": final_path.name,
            "bytes": bytes_written,
            "rows": rows,
            "sha256": digest.hexdigest(),
            "header": header,
            "timestamp_start": params["timestamp_start"],
            "timestamp_end": params["timestamp_end"],
        }
    except Exception:
        part_path.unlink(missing_ok=True)
        raise


def validate_output_dir(output_dir: Path, *, repo_root: Path) -> Path:
    """Require raw-event storage to live outside the Git checkout."""

    resolved = output_dir.expanduser().resolve()
    root = repo_root.resolve()
    try:
        resolved.relative_to(root)
        inside_repo = True
    except ValueError:
        inside_repo = False
    if inside_repo:
        raise ValueError(
            "raw Movebank output directory must be outside the Git repository"
        )
    return resolved


def write_manifest(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help=(
            "Protected local directory outside the Git repository. "
            "Raw Movebank events must not be committed or uploaded as CI artifacts."
        ),
    )
    p.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "outputs/payoff_b_greater_snow_goose_movebank_materialization_manifest.json"
        ),
    )
    p.add_argument(
        "--years",
        nargs="*",
        type=int,
        default=list(YEARS),
        help="Operational retry subset; scientific source years remain 2019-2023.",
    )
    return p.parse_args()


def main():
    args = parse_args()
    requested_years = tuple(sorted(set(int(y) for y in args.years)))
    repo_root = Path(__file__).resolve().parents[1]
    try:
        output_dir = validate_output_dir(
            args.output_dir,
            repo_root=repo_root,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    invalid = [y for y in requested_years if y not in YEARS]
    if invalid:
        raise SystemExit(
            "years outside frozen source range 2019-2023: "
            + ",".join(map(str, invalid))
        )

    token = os.environ.get("MOVEBANK_API_TOKEN", "").strip()
    if not token:
        manifest = {
            "materialization_id": (
                "payoff_b_greater_snow_goose_movebank_materialization_v1"
            ),
            "study_id": STUDY_ID,
            "status": "BLOCKED_MISSING_API_TOKEN",
            "event_data_opened": False,
            "years_requested": list(requested_years),
            "message": (
                "Set MOVEBANK_API_TOKEN in a protected environment or GitHub "
                "Actions secret. Do not commit or paste the token into files."
            ),
        }
        write_manifest(args.manifest, manifest)
        raise SystemExit(2)

    result = {
        "materialization_id": (
            "payoff_b_greater_snow_goose_movebank_materialization_v1"
        ),
        "study_id": STUDY_ID,
        "sensor_type_id": GPS_SENSOR_TYPE_ID,
        "source": "Movebank direct-read",
        "years_requested": list(requested_years),
        "attributes": list(ATTRIBUTES),
        "license_terms_auto_accepted": False,
        "raw_files_committed_to_git": False,
        "status": "IN_PROGRESS",
        "event_data_opened": False,
        "files": [],
        "freeze_reference": (
            "freeze/payoff-b-snow-goose-preoutcome-v2-20260929"
        ),
    }
    write_manifest(args.manifest, result)

    session = requests.Session()
    try:
        for year in requested_years:
            row = download_year(
                session,
                api_token=token,
                year=year,
                output_dir=output_dir,
            )
            result["files"].append(row)
            result["event_data_opened"] = True
            write_manifest(args.manifest, result)
    except MaterializationBlocked as exc:
        result["status"] = "BLOCKED"
        result["blocker"] = str(exc)
        write_manifest(args.manifest, result)
        raise SystemExit(3) from exc

    result["status"] = "COMPLETE"
    result["total_rows"] = sum(x["rows"] for x in result["files"])
    result["total_bytes"] = sum(x["bytes"] for x in result["files"])
    write_manifest(args.manifest, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
