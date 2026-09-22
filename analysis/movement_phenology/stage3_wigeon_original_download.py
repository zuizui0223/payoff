#!/usr/bin/env python3
"""Download the original public Eurasian-wigeon Movebank study data.

Study DOI: 10.5441/001/1.dv5mm289
Movebank/DSpace item UUID: 86f824b7-1973-4ba8-bc6a-fa8956e830a1
ORIGINAL bundle UUID: 90b7bdbb-4746-4020-9cad-cf30e3f268bf

The UUIDs are not guessed: they were recovered from the repository discovery
API and are frozen in the wigeon discovery receipt. This downloader uses longer
timeouts and retry logic than the discovery probe, then selects the original
bitstream by parsed GPS schema rather than filename.
"""

from __future__ import annotations

import gzip
import io
import json
from pathlib import Path
import time
import zipfile

import pandas as pd
import requests


BASE = "https://datarepository.movebank.org"
BUNDLE_UUID = "90b7bdbb-4746-4020-9cad-cf30e3f268bf"
DOI = "10.5441/001/1.dv5mm289"
OUT = Path("outputs/movement_phenology")
EXT = Path("external/wigeon_original")
UA = {"User-Agent": "payoff-movement-phenology-wigeon/1.0"}


def get(url: str, timeout: int = 120, attempts: int = 4) -> requests.Response:
    last = None
    for i in range(attempts):
        try:
            r = requests.get(url, headers=UA, timeout=timeout)
            r.raise_for_status()
            return r
        except Exception as exc:
            last = exc
            if i + 1 < attempts:
                time.sleep(2 ** i)
    raise RuntimeError(f"GET failed after {attempts} attempts: {url}: {last}")


def table_candidates(raw: bytes):
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

    for member, payload in payloads:
        for encoding in ("utf-8-sig", "utf-16", "latin-1"):
            try:
                text = payload.decode(encoding)
            except Exception:
                continue
            for sep in (",", "\t", ";"):
                try:
                    df = pd.read_csv(io.StringIO(text), sep=sep, low_memory=False)
                except Exception:
                    continue
                if df.shape[1] > 1:
                    yield member, encoding, sep, df


def find_col(columns, exacts):
    lower = {str(c).lower(): c for c in columns}
    for x in exacts:
        if x.lower() in lower:
            return lower[x.lower()]
    return None


def is_gps_table(df: pd.DataFrame) -> bool:
    cols = df.columns
    return all(
        find_col(cols, group) is not None
        for group in (
            ["timestamp", "eventDate"],
            ["location-lat", "decimalLatitude", "latitude"],
            ["location-long", "decimalLongitude", "longitude"],
            [
                "individual-local-identifier",
                "organismID",
                "individual.id",
                "individual",
            ],
        )
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    EXT.mkdir(parents=True, exist_ok=True)

    url = f"{BASE}/server/api/core/bundles/{BUNDLE_UUID}/bitstreams?size=100"
    response = get(url)
    payload = response.json()
    bitstreams = payload.get("_embedded", {}).get("bitstreams", [])
    if not bitstreams:
        raise SystemExit(f"No bitstreams returned for ORIGINAL bundle: {payload}")

    attempts = []
    selected = None

    for bit in bitstreams:
        bid = bit.get("uuid")
        name = bit.get("name")
        size = bit.get("sizeBytes")
        if not bid:
            continue
        content_url = f"{BASE}/server/api/core/bitstreams/{bid}/content"
        rec = {
            "uuid": bid,
            "name": name,
            "declared_size": size,
            "content_url": content_url,
        }
        try:
            rr = get(content_url, timeout=180, attempts=3)
            rec["downloaded_bytes"] = len(rr.content)
            parsed = []
            for member, encoding, sep, df in table_candidates(rr.content):
                item = {
                    "member": member,
                    "encoding": encoding,
                    "separator": sep,
                    "n_rows": int(len(df)),
                    "n_cols": int(df.shape[1]),
                    "columns": [str(c) for c in df.columns],
                    "gps_schema": bool(is_gps_table(df)),
                }
                parsed.append(item)
                if is_gps_table(df):
                    selected = {
                        **rec,
                        **item,
                        "dataframe": df,
                    }
                    break
            rec["parsed_candidates"] = parsed
        except Exception as exc:
            rec["error"] = f"{type(exc).__name__}:{exc}"
        attempts.append(rec)
        if selected is not None:
            break

    if selected is None:
        raise SystemExit(
            "No ORIGINAL bitstream parsed as a GPS table. "
            + json.dumps(attempts, default=str)[:12000]
        )

    df = selected.pop("dataframe")
    target = EXT / "wigeon_original_gps.csv"
    df.to_csv(target, index=False)

    receipt = {
        "doi": DOI,
        "bundle_uuid": BUNDLE_UUID,
        "selected": selected,
        "saved_path": str(target),
        "saved_rows": int(len(df)),
        "saved_columns": [str(c) for c in df.columns],
        "attempts": attempts,
        "claim_ceiling": (
            "Original Movebank ORIGINAL bundle selected by GPS schema. "
            "Analytical spring-track inclusion still requires reproduction of "
            "the published preprocessing and HMM."
        ),
    }
    (OUT / "stage3_wigeon_original_movebank_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
