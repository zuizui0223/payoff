#!/usr/bin/env python3
"""Probe anonymous AWS Open Data access for frozen Aikens MODIS V061 products.

Technical transport probe only. No environmental values or lambda outcome are
opened. The scientific product identities remain MOD09Q1.061 + MOD10A2.061.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGETS = (
    {
        "name": "MOD09Q1.061",
        "bucket": "lp-prod-protected",
        "prefix": "MOD09Q1.061/",
        "region": "us-west-2",
    },
    {
        "name": "MOD10A2.061",
        "bucket": "nsidc-cumulus-prod-protected",
        "prefix": "MODIS/MOD10A2/61/",
        "region": "us-west-2",
    },
)


def probe(target: dict) -> dict:
    try:
        import boto3
        from botocore import UNSIGNED
        from botocore.config import Config
    except ImportError as exc:
        raise RuntimeError("anonymous S3 probe requires boto3") from exc

    client = boto3.client(
        "s3",
        region_name=target["region"],
        config=Config(signature_version=UNSIGNED),
    )
    result = {
        **target,
        "anonymous_list": False,
        "anonymous_get_head": False,
        "sample_keys": [],
        "error": None,
    }
    try:
        response = client.list_objects_v2(
            Bucket=target["bucket"],
            Prefix=target["prefix"],
            MaxKeys=5,
        )
        keys = [
            str(row["Key"])
            for row in response.get("Contents", [])
        ]
        result["sample_keys"] = keys
        result["anonymous_list"] = bool(keys)
        if keys:
            head = client.head_object(
                Bucket=target["bucket"],
                Key=keys[0],
            )
            result["anonymous_get_head"] = True
            result["sample_object"] = {
                "key": keys[0],
                "content_length": int(head.get("ContentLength", 0)),
                "etag": str(head.get("ETag", "")),
            }
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/aikens_modis_anonymous_s3_probe.json"),
    )
    args = parser.parse_args()

    rows = [probe(target) for target in TARGETS]
    payload = {
        "status": (
            "ANONYMOUS_S3_BOTH_PRODUCTS_ACCESSIBLE"
            if all(
                row["anonymous_list"]
                and row["anonymous_get_head"]
                for row in rows
            )
            else "ANONYMOUS_S3_ACCESS_INCOMPLETE"
        ),
        "products": rows,
        "scientific_contract_changed": False,
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "transport discovery only; no MODIS environmental values, IRG, "
            "phase pairs, or Aikens lambda result are opened"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
