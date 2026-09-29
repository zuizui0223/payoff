#!/usr/bin/env python3
"""Authorized Movebank fetcher for the preregistered greater-snow-goose lane.

Safety / governance rules:
- credentials come only from environment variables;
- default mode is metadata-only and never requests event rows;
- event download requires the explicit --download-events flag;
- license terms are NEVER accepted automatically;
- if Movebank returns license terms, the script saves them for review and exits;
- raw GPS files are written only to a user-selected output directory and are
  never committed by this script.

Expected environment variables:
    MOVEBANK_USERNAME
    MOVEBANK_PASSWORD
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
from typing import Any, Iterable


ENDPOINT = "https://www.movebank.org/movebank/service/direct-read"
DEFAULT_STUDY_ID = "1442516400"
GPS_SENSOR_TYPE_ID = "653"
REPO_ROOT = Path(__file__).resolve().parents[1]

EVENT_ATTRIBUTES = [
    "timestamp",
    "location_lat",
    "location_long",
    "visible",
    "individual_local_identifier",
    "individual_id",
    "deployment_id",
    "tag_id",
    "sensor_type_id",
]

STUDY_ATTRIBUTES = [
    "id",
    "name",
    "license_type",
    "go_public_date",
    "suspend_license_terms",
    "i_can_see_data",
    "there_are_data_which_i_cannot_see",
    "i_have_download_access",
    "number_of_individuals",
    "number_of_deployed_locations",
    "sensor_type_ids",
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--study-id", default=DEFAULT_STUDY_ID)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument(
        "--download-events",
        action="store_true",
        help="Explicitly request GPS event rows after access checks pass.",
    )
    p.add_argument(
        "--max-individuals",
        type=int,
        default=None,
        help="Optional development cap; omit for the full authorized study.",
    )
    return p.parse_args()


def truthy(value: str | None) -> bool | None:
    if value is None or value == "":
        return None
    norm = value.strip().lower()
    if norm in {"true", "t", "1", "yes"}:
        return True
    if norm in {"false", "f", "0", "no"}:
        return False
    return None


def has_license_terms(text: str) -> bool:
    return "License Terms:" in text


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_csv_rows(text: str) -> list[dict[str, str]]:
    if not text.strip():
        return []
    return list(csv.DictReader(io.StringIO(text)))


def ensure_output_outside_repository(output_dir: Path) -> Path:
    """Refuse to place raw or licensed Movebank material inside the git tree."""

    resolved = output_dir.expanduser().resolve()
    root = REPO_ROOT.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return resolved
    raise ValueError(
        "--output-dir must be outside the PAYOFF-B repository so raw "
        "Movebank material cannot be accidentally committed."
    )


def require_credentials() -> tuple[str, str]:
    username = os.environ.get("MOVEBANK_USERNAME")
    password = os.environ.get("MOVEBANK_PASSWORD")
    if not username or not password:
        raise RuntimeError(
            "Set MOVEBANK_USERNAME and MOVEBANK_PASSWORD before running "
            "the authorized Movebank fetcher."
        )
    return username, password


def get_text(
    session: Any,
    *,
    params: dict[str, str],
    auth: tuple[str, str],
) -> Any:
    return session.get(
        ENDPOINT,
        params=params,
        auth=auth,
        timeout=180,
        headers={"User-Agent": "PAYOFF-B-authorized-movebank-fetch/1.0"},
    )


def study_metadata(
    session: Any,
    *,
    study_id: str,
    auth: tuple[str, str],
) -> tuple[dict[str, str], int]:
    response = get_text(
        session,
        params={
            "entity_type": "study",
            "study_id": study_id,
            "attributes": ",".join(STUDY_ATTRIBUTES),
        },
        auth=auth,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Movebank study metadata request failed: HTTP {response.status_code}"
        )
    rows = parse_csv_rows(response.text)
    if len(rows) != 1:
        raise RuntimeError(
            f"Expected one study row for {study_id}, got {len(rows)}"
        )
    return rows[0], response.status_code


def individual_metadata(
    session: Any,
    *,
    study_id: str,
    auth: tuple[str, str],
) -> list[dict[str, str]]:
    response = get_text(
        session,
        params={
            "entity_type": "individual",
            "study_id": study_id,
        },
        auth=auth,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Movebank individual request failed: HTTP {response.status_code}"
        )
    rows = parse_csv_rows(response.text)
    if not rows:
        raise RuntimeError("Movebank returned no individuals")
    return rows


def validate_event_csv(text: str) -> tuple[list[str], int]:
    if has_license_terms(text):
        raise ValueError("LICENSE_TERMS_REQUIRED")
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration as exc:
        raise ValueError("EMPTY_EVENT_RESPONSE") from exc
    required = {"timestamp", "location_lat", "location_long"}
    missing = required - set(header)
    if missing:
        raise ValueError(
            "EVENT_SCHEMA_MISMATCH:" + ",".join(sorted(missing))
        )
    rows = sum(1 for _ in reader)
    return header, rows


def safe_file_stem(local_identifier: str, internal_id: str) -> str:
    raw = local_identifier.strip() or f"individual_{internal_id}"
    cleaned = "".join(
        ch if ch.isalnum() or ch in {"-", "_", "."} else "_"
        for ch in raw
    ).strip("._")
    return cleaned or f"individual_{internal_id}"


def main():
    args = parse_args()
    if args.max_individuals is not None and args.max_individuals < 1:
        raise ValueError("--max-individuals must be >= 1")

    try:
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "Install the empirical dependency set before using Movebank fetch: "
            "python -m pip install -e '.[empirical]'"
        ) from exc

    auth = require_credentials()
    output_dir = ensure_output_outside_repository(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "movebank_fetch_manifest.json"

    session = requests.Session()
    meta, status_code = study_metadata(
        session,
        study_id=str(args.study_id),
        auth=auth,
    )

    access = truthy(meta.get("i_have_download_access"))
    visible = truthy(meta.get("i_can_see_data"))
    hidden = truthy(meta.get("there_are_data_which_i_cannot_see"))

    manifest: dict[str, object] = {
        "fetch_contract": "payoff_b_greater_snow_goose_authorized_fetch_v1",
        "study_id": str(args.study_id),
        "study_name": meta.get("name"),
        "metadata_http_status": status_code,
        "i_can_see_data": visible,
        "there_are_data_which_i_cannot_see": hidden,
        "i_have_download_access": access,
        "license_type": meta.get("license_type"),
        "sensor_type_ids": meta.get("sensor_type_ids"),
        "event_download_requested": bool(args.download_events),
        "license_terms_auto_accepted": False,
        "status": "METADATA_ONLY",
        "files": [],
    }

    if access is not True:
        manifest["status"] = "DOWNLOAD_ACCESS_NOT_CONFIRMED"
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        raise RuntimeError(
            "Authenticated study metadata does not report "
            "i_have_download_access=true."
        )

    individuals = individual_metadata(
        session,
        study_id=str(args.study_id),
        auth=auth,
    )
    manifest["individuals_returned"] = len(individuals)

    if not args.download_events:
        manifest["status"] = "AUTHORIZED_METADATA_GATE_PASS"
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(manifest, indent=2))
        return

    chosen = individuals
    if args.max_individuals is not None:
        chosen = chosen[: args.max_individuals]

    event_dir = output_dir / "gps_events_by_individual"
    event_dir.mkdir(parents=True, exist_ok=True)

    files = []
    for index, individual in enumerate(chosen):
        internal_id = individual.get("id", "").strip()
        local_id = individual.get("local_identifier", "").strip()
        if not internal_id:
            raise RuntimeError(
                f"Individual row {index} lacks internal id"
            )

        response = get_text(
            session,
            params={
                "entity_type": "event",
                "study_id": str(args.study_id),
                "individual_id": internal_id,
                "sensor_type_id": GPS_SENSOR_TYPE_ID,
                "attributes": ",".join(EVENT_ATTRIBUTES),
            },
            auth=auth,
        )

        if response.status_code != 200:
            manifest["status"] = "EVENT_DOWNLOAD_HTTP_FAILURE"
            manifest["failed_individual_id"] = internal_id
            manifest["failed_http_status"] = int(response.status_code)
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
            )
            raise RuntimeError(
                f"Event request failed for individual {internal_id}: "
                f"HTTP {response.status_code}"
            )

        if has_license_terms(response.text):
            terms_path = output_dir / "movebank_license_terms.html"
            terms_path.write_text(response.text, encoding="utf-8")
            manifest["status"] = "LICENSE_TERMS_ACCEPTANCE_REQUIRED"
            manifest["license_terms_path"] = str(terms_path)
            manifest["failed_individual_id"] = internal_id
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
            )
            raise RuntimeError(
                "Movebank returned license terms. They were saved for "
                "review but NOT accepted. Accept the terms explicitly in "
                "Movebank, then rerun this script."
            )

        header, row_count = validate_event_csv(response.text)
        stem = safe_file_stem(local_id, internal_id)
        path = event_dir / f"{stem}.csv"
        path.write_text(response.text, encoding="utf-8")
        files.append(
            {
                "individual_id": internal_id,
                "individual_local_identifier": local_id,
                "path": str(path),
                "rows": row_count,
                "header": header,
                "sha256": sha256_file(path),
            }
        )

    manifest["files"] = files
    manifest["status"] = "AUTHORIZED_EVENT_DOWNLOAD_COMPLETE"
    manifest["individuals_downloaded"] = len(files)
    manifest["event_rows_downloaded"] = sum(
        int(row["rows"]) for row in files
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
