#!/usr/bin/env python3
"""Download original public Movebank GPS files for Greenland and Barents
barnacle-goose flyways by discovering DOI-associated repository bitstreams.

The script does not guess filenames. It downloads candidate repository files
and selects the file whose parsed schema contains timestamp, latitude,
longitude, and individual identifiers.
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
from pathlib import Path
import tempfile
import zipfile

import pandas as pd
import requests

from analysis.movement_phenology.stage3_barnacle_multiflyway_discover import (
    dspace_fallback,
    mets_discover,
)


DATASETS = {
    "greenland": "10.5441/001/1.5d3f0664",
    "barents": "10.5441/001/1.ps244r11",
}
OUT = Path("outputs/movement_phenology")
EXT = Path("external/barnacle_raw")
UA = {"User-Agent": "payoff-movement-phenology/1.0"}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--flyway", required=True, choices=sorted(DATASETS))
    return p.parse_args()


def table_from_bytes(raw: bytes):
    payloads = []
    if raw.startswith(b"PK"):
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for name in zf.namelist():
                if not name.endswith("/"):
                    payloads.append((name, zf.read(name)))
    elif raw.startswith(b"\x1f\x8b"):
        payloads.append(("gzip", gzip.decompress(raw)))
    else:
        payloads.append(("raw", raw))

    for name, payload in payloads:
        for encoding in ("utf-8-sig", "utf-16", "latin-1"):
            try:
                text = payload.decode(encoding)
            except Exception:
                continue
            for sep in (",", "\t", ";"):
                try:
                    df = pd.read_csv(
                        io.StringIO(text), sep=sep, low_memory=False
                    )
                except Exception:
                    continue
                if df.shape[1] > 1:
                    yield name, sep, df, payload


def gps_schema(df: pd.DataFrame) -> bool:
    cols = {str(c).lower() for c in df.columns}
    required_groups = [
        {"timestamp", "eventdate"},
        {"location-lat", "decimallatitude", "latitude"},
        {"location-long", "decimallongitude", "longitude"},
        {
            "individual-local-identifier",
            "organismid",
            "individual",
            "individual_id",
        },
    ]
    return all(any(x in cols for x in group) for group in required_groups)


def robust_dspace_files(objects):
    """Retry the slow DSpace bundle endpoints with a larger read timeout."""
    base = "https://datarepository.movebank.org"
    files = []
    errors = []
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=4)
    session.mount("https://", adapter)

    for obj in objects or []:
        uuid = obj.get("uuid")
        if not uuid:
            continue
        try:
            b = session.get(
                f"{base}/server/api/core/items/{uuid}/bundles?size=100",
                headers=UA,
                timeout=(20, 150),
            )
            b.raise_for_status()
            bundles = b.json().get("_embedded", {}).get("bundles", [])
            for bundle in bundles:
                buuid = bundle.get("uuid")
                if not buuid:
                    continue
                bs = session.get(
                    f"{base}/server/api/core/bundles/{buuid}/bitstreams?size=100",
                    headers=UA,
                    timeout=(20, 150),
                )
                bs.raise_for_status()
                for bit in bs.json().get("_embedded", {}).get("bitstreams", []):
                    bid = bit.get("uuid")
                    if not bid:
                        continue
                    files.append(
                        {
                            "title": bit.get("name"),
                            "label": bundle.get("name"),
                            "mime": None,
                            "url": (
                                f"{base}/server/api/core/bitstreams/"
                                f"{bid}/content"
                            ),
                        }
                    )
        except Exception as exc:
            errors.append(f"{uuid}:{type(exc).__name__}:{exc}")
    return files, errors


def main():
    args = parse_args()
    doi = DATASETS[args.flyway]
    OUT.mkdir(parents=True, exist_ok=True)
    EXT.mkdir(parents=True, exist_ok=True)

    rec = mets_discover(doi)
    source = "legacy_mets"
    files = rec.get("files", [])
    if not files:
        fallback = dspace_fallback(doi)
        files = fallback.get("files", [])
        rec["dspace_fallback"] = fallback
        source = "dspace_api"
        if not files and fallback.get("objects"):
            files, retry_errors = robust_dspace_files(fallback.get("objects"))
            rec["dspace_long_retry_errors"] = retry_errors
            if files:
                source = "dspace_api_long_retry"
    if not files:
        raise SystemExit(f"No repository files discovered for {doi}: {rec}")

    attempts = []
    selected = None

    # Prefer obvious CSV/tabular files but still inspect all discovered assets.
    ordered = sorted(
        files,
        key=lambda x: (
            0 if any(
                token in str(x.get("title", "")).lower()
                for token in ("gps", "location", "event", "data")
            ) else 1,
            str(x.get("title", "")),
        ),
    )

    for item in ordered:
        url = item.get("url")
        if not url:
            continue
        try:
            r = requests.get(url, headers=UA, timeout=180)
            status = r.status_code
            size = len(r.content)
            attempt = {
                "title": item.get("title"),
                "label": item.get("label"),
                "mime": item.get("mime"),
                "url": url,
                "status": status,
                "bytes": size,
            }
            if status != 200 or size == 0:
                attempts.append(attempt)
                continue

            parsed = False
            for member, sep, df, payload in table_from_bytes(r.content):
                parsed = True
                attempt["member"] = member
                attempt["separator"] = sep
                attempt["n_rows"] = int(len(df))
                attempt["columns"] = [str(c) for c in df.columns]
                if gps_schema(df):
                    selected = {
                        **attempt,
                        "df": df,
                    }
                    break
            attempt["parsed"] = parsed
            attempts.append(attempt)
            if selected is not None:
                break
        except Exception as exc:
            attempts.append(
                {
                    "title": item.get("title"),
                    "url": url,
                    "error": f"{type(exc).__name__}:{exc}",
                }
            )

    if selected is None:
        raise SystemExit(
            "No discovered file had a GPS schema. "
            + json.dumps(attempts, default=str)[:8000]
        )

    target = EXT / f"{args.flyway}_gps.csv"
    df = selected.pop("df")
    df.to_csv(target, index=False)

    receipt = {
        "flyway": args.flyway,
        "doi": doi,
        "discovery_source": source,
        "selected": selected,
        "saved_path": str(target),
        "saved_rows": int(len(df)),
        "saved_columns": [str(c) for c in df.columns],
        "attempts": attempts,
        "claim_ceiling": (
            "Original public Movebank repository file selected by schema, "
            "not by guessed filename."
        ),
    }
    (OUT / f"stage3_{args.flyway}_raw_download_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
