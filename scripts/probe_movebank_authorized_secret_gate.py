#!/usr/bin/env python3
"""Credential-safe metadata-only Movebank gate for PAYOFF-B.

This probe never requests event rows and never prints credentials.
It classifies only whether repository Actions secrets are configured and
whether authenticated study metadata report download access for the frozen
greater-snow-goose study.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from scripts.fetch_greater_snow_goose_movebank_authorized import (
    DEFAULT_STUDY_ID,
    individual_metadata,
    study_metadata,
    truthy,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--study-id", default=DEFAULT_STUDY_ID)
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


def main():
    args = parse_args()
    username = os.environ.get("MOVEBANK_USERNAME", "")
    password = os.environ.get("MOVEBANK_PASSWORD", "")

    result = {
        "probe_id": "payoff_b_movebank_authorized_secret_metadata_gate_v1_20261001",
        "study_id": str(args.study_id),
        "event_data_requested": False,
        "credentials_echoed": False,
        "license_terms_auto_accepted": False,
        "classification": "UNRESOLVED",
        "metadata": None,
    }

    if not username or not password:
        result["classification"] = "CREDENTIALS_NOT_CONFIGURED"
        _write(args.output, result)
        return

    try:
        import requests
    except ImportError as exc:
        result["classification"] = "REQUESTS_DEPENDENCY_MISSING"
        result["error_type"] = type(exc).__name__
        _write(args.output, result)
        return

    session = requests.Session()
    try:
        meta, status = study_metadata(
            session,
            study_id=str(args.study_id),
            auth=(username, password),
        )
    except Exception as exc:
        result["classification"] = "AUTHENTICATED_METADATA_REQUEST_FAILED"
        result["error_type"] = type(exc).__name__
        result["error_message"] = str(exc)[:300]
        _write(args.output, result)
        return

    access = truthy(meta.get("i_have_download_access"))
    visible = truthy(meta.get("i_can_see_data"))
    hidden = truthy(meta.get("there_are_data_which_i_cannot_see"))

    result["metadata"] = {
        "name": meta.get("name"),
        "license_type": meta.get("license_type"),
        "go_public_date": meta.get("go_public_date"),
        "i_can_see_data": visible,
        "there_are_data_which_i_cannot_see": hidden,
        "i_have_download_access": access,
        "number_of_individuals_reported": meta.get("number_of_individuals"),
        "number_of_deployed_locations_reported": meta.get(
            "number_of_deployed_locations"
        ),
        "sensor_type_ids": meta.get("sensor_type_ids"),
        "metadata_http_status": int(status),
    }

    if access is not True:
        result["classification"] = "AUTHENTICATED_BUT_DOWNLOAD_ACCESS_NOT_CONFIRMED"
        _write(args.output, result)
        return

    try:
        individuals = individual_metadata(
            session,
            study_id=str(args.study_id),
            auth=(username, password),
        )
        result["metadata"]["individual_rows_visible"] = len(individuals)
    except Exception as exc:
        result["metadata"]["individual_rows_visible"] = None
        result["metadata"]["individual_metadata_error_type"] = type(exc).__name__

    result["classification"] = "AUTHORIZED_METADATA_GATE_PASS"
    _write(args.output, result)


if __name__ == "__main__":
    main()
