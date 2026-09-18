#!/usr/bin/env python3
"""Discover original Movebank Data Repository bitstreams for three barnacle-goose flyways."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests


BASE = "https://datarepository.movebank.org"
UA = {"User-Agent": "payoff-movement-phenology/1.0"}
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "greenland": "10.5441/001/1.5d3f0664",
    "svalbard": "10.5441/001/1.5k6b1364",
    "barents": "10.5441/001/1.ps244r11",
}


def get_json(url: str, timeout=120):
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.json(), str(r.url)


def discover_one(name: str, doi: str) -> dict:
    rec = {"flyway": name, "doi": doi, "errors": []}
    qurl = (
        f"{BASE}/server/api/discover/search/objects?"
        f"query={quote('dc.identifier.doi:'+doi)}&size=20"
    )
    try:
        data, final = get_json(qurl)
        objs = (
            data.get("_embedded", {})
            .get("searchResult", {})
            .get("_embedded", {})
            .get("objects", [])
        )
    except Exception as exc:
        rec["errors"].append(f"discover:{type(exc).__name__}:{exc}")
        return rec

    candidates = []
    for obj in objs:
        idx = obj.get("_embedded", {}).get("indexableObject", {})
        candidates.append(
            {
                "uuid": idx.get("uuid") or idx.get("id"),
                "name": idx.get("name"),
                "handle": idx.get("handle"),
                "type": idx.get("type"),
            }
        )
    rec["candidates"] = candidates

    item = next((x for x in candidates if x.get("uuid")), None)
    if item is None:
        return rec

    uuid = item["uuid"]
    rec["item_uuid"] = uuid
    bundles_url = f"{BASE}/server/api/core/items/{uuid}/bundles?size=100"
    try:
        bundles, _ = get_json(bundles_url)
        barr = bundles.get("_embedded", {}).get("bundles", [])
    except Exception as exc:
        rec["errors"].append(f"bundles:{type(exc).__name__}:{exc}")
        return rec

    rec["bundles"] = []
    for b in barr:
        buuid = b.get("uuid")
        bname = b.get("name")
        br = {"uuid": buuid, "name": bname, "bitstreams": []}
        if buuid:
            url = f"{BASE}/server/api/core/bundles/{buuid}/bitstreams?size=100"
            try:
                bs, _ = get_json(url)
                for bit in bs.get("_embedded", {}).get("bitstreams", []):
                    bid = bit.get("uuid")
                    br["bitstreams"].append(
                        {
                            "uuid": bid,
                            "name": bit.get("name"),
                            "sizeBytes": bit.get("sizeBytes"),
                            "content_url": (
                                f"{BASE}/server/api/core/bitstreams/{bid}/content"
                                if bid else None
                            ),
                        }
                    )
            except Exception as exc:
                br["error"] = f"{type(exc).__name__}:{exc}"
        rec["bundles"].append(br)

    return rec


def main():
    records = [discover_one(name, doi) for name, doi in DATASETS.items()]
    (OUT / "stage3_barnacle_multiflyway_discovery.json").write_text(
        json.dumps(records, indent=2) + "\n", encoding="utf-8"
    )

    rows = []
    for rec in records:
        for b in rec.get("bundles", []):
            for bit in b.get("bitstreams", []):
                rows.append(
                    {
                        "flyway": rec["flyway"],
                        "doi": rec["doi"],
                        "item_uuid": rec.get("item_uuid"),
                        "bundle": b.get("name"),
                        **bit,
                    }
                )
    pd.DataFrame(rows).to_csv(
        OUT / "stage3_barnacle_multiflyway_bitstreams.csv", index=False
    )

    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
