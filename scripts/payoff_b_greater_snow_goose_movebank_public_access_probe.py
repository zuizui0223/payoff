#!/usr/bin/env python3
"""Probe public Movebank study-level access without opening event data.

This script requests only study metadata for the frozen greater-snow-goose
study. It must never request entity_type=event. The purpose is to distinguish
an API/environment blocker from a study-permission blocker while preserving
the preregistered movement outcome as unopened.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path

import requests


DEFAULT_STUDY_ID = "1442516400"
ENDPOINT = "https://www.movebank.org/movebank/service/direct-read"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--study-id", default=DEFAULT_STUDY_ID)
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_greater_snow_goose_movebank_public_access_probe.json"
        ),
    )
    return p.parse_args()


def _truthy(value: str | None) -> bool | None:
    if value is None or value == "":
        return None
    norm = value.strip().lower()
    if norm in {"true", "t", "1", "yes"}:
        return True
    if norm in {"false", "f", "0", "no"}:
        return False
    return None


def main():
    args = parse_args()
    params = {
        "entity_type": "study",
        "study_id": str(args.study_id),
        "attributes": ",".join(
            [
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
        ),
    }

    try:
        response = requests.get(
            ENDPOINT,
            params=params,
            timeout=60,
            headers={"User-Agent": "PAYOFF-B-preoutcome-access-probe/1.0"},
        )
        status_code = int(response.status_code)
        text = response.text
        network_error = None
    except requests.RequestException as exc:
        status_code = None
        text = ""
        network_error = type(exc).__name__

    result = {
        "probe_id": "payoff_b_greater_snow_goose_movebank_public_access_probe_v1",
        "study_id": str(args.study_id),
        "entity_type_requested": "study",
        "event_data_requested": False,
        "http_status": status_code,
        "network_error": network_error,
        "classification": "UNRESOLVED",
        "metadata": None,
        "claim_boundary": [
            "study metadata only",
            "no event rows opened",
            "public-download metadata does not prove license terms are already accepted",
        ],
    }

    if network_error is not None:
        result["classification"] = "MOVE_BANK_NETWORK_UNAVAILABLE"
    elif status_code != 200:
        result["classification"] = "STUDY_METADATA_HTTP_FAILURE"
    elif "License Terms:" in text:
        # Unexpected for entity_type=study, but fail closed if Movebank returns
        # a terms page rather than metadata.
        result["classification"] = "LICENSE_TERMS_RETURNED_AT_METADATA_PROBE"
    else:
        rows = list(csv.DictReader(io.StringIO(text)))
        if len(rows) != 1:
            result["classification"] = "STUDY_METADATA_NOT_UNIQUE"
            result["row_count"] = len(rows)
        else:
            row = rows[0]
            metadata = {
                "id": row.get("id"),
                "name": row.get("name"),
                "license_type": row.get("license_type"),
                "go_public_date": row.get("go_public_date"),
                "suspend_license_terms": _truthy(
                    row.get("suspend_license_terms")
                ),
                "i_can_see_data": _truthy(row.get("i_can_see_data")),
                "there_are_data_which_i_cannot_see": _truthy(
                    row.get("there_are_data_which_i_cannot_see")
                ),
                "i_have_download_access": _truthy(
                    row.get("i_have_download_access")
                ),
                "number_of_individuals": row.get("number_of_individuals"),
                "number_of_deployed_locations": row.get(
                    "number_of_deployed_locations"
                ),
                "sensor_type_ids": row.get("sensor_type_ids"),
            }
            result["metadata"] = metadata
            if metadata["i_have_download_access"] is True:
                result["classification"] = (
                    "PUBLIC_DOWNLOAD_ACCESS_REPORTED_STUDY_LEVEL"
                )
            elif metadata["i_have_download_access"] is False:
                result["classification"] = (
                    "NO_PUBLIC_DOWNLOAD_ACCESS_REPORTED_STUDY_LEVEL"
                )
            else:
                result["classification"] = (
                    "PUBLIC_DOWNLOAD_ACCESS_FIELD_UNRESOLVED"
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
