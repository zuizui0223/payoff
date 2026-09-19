#!/usr/bin/env python3
"""Discover public archive assets for the supplementary Lithuania wigeon study.

Target Movebank study name:
  Dabbling duck migration Lithuania 2019

This is one of the four tracking files named in the van Toor et al. (2021)
supplement. The script searches both DataCite and the public Movebank Data
Repository (DSpace 7) and records exact item/bundle/bitstream URLs when found.
It never guesses UUIDs.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

import requests


TITLE = "Dabbling duck migration Lithuania 2019"
BASE = "https://datarepository.movebank.org"
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "payoff-wigeon-lithuania-discovery/1.0"}


def get_json(url: str, timeout=45):
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.json(), str(r.url)


def main():
    receipt = {
        "target_title": TITLE,
        "datacite_matches": [],
        "movebank_searches": [],
        "items": [],
        "bitstreams": [],
        "errors": [],
    }

    # DataCite title search in case the study has an archived dataset DOI.
    try:
        query = quote(f'titles.title:"{TITLE}"')
        dc, final = get_json(
            f"https://api.datacite.org/dois?query={query}&page[size]=100"
        )
        for obj in dc.get("data", []):
            a = obj.get("attributes", {})
            titles = [x.get("title") for x in a.get("titles", [])]
            if any(TITLE.lower() in str(x).lower() for x in titles):
                receipt["datacite_matches"].append(
                    {
                        "doi": a.get("doi"),
                        "url": a.get("url"),
                        "publisher": a.get("publisher"),
                        "titles": titles,
                    }
                )
    except Exception as exc:
        receipt["errors"].append(
            f"datacite:{type(exc).__name__}:{exc}"
        )

    queries = [
        TITLE,
        f'"{TITLE}"',
        "Dabbling duck migration Lithuania",
        "European Wigeon Lithuania 2019",
    ]
    item_uuids = set()

    for query_text in queries:
        for field_query in (
            query_text,
            f"dc.title:{query_text}",
            f'dc.title:"{query_text}"',
        ):
            try:
                q = quote(field_query)
                data, final = get_json(
                    f"{BASE}/server/api/discover/search/objects"
                    f"?query={q}&size=100"
                )
                objs = (
                    data.get("_embedded", {})
                    .get("searchResult", {})
                    .get("_embedded", {})
                    .get("objects", [])
                )
                compact = []
                for obj in objs:
                    idx = obj.get("_embedded", {}).get(
                        "indexableObject", {}
                    )
                    uuid = idx.get("uuid") or idx.get("id")
                    name = idx.get("name")
                    handle = idx.get("handle")
                    typ = idx.get("type")
                    compact.append(
                        {
                            "uuid": uuid,
                            "name": name,
                            "handle": handle,
                            "type": typ,
                        }
                    )
                    if uuid and (
                        TITLE.lower() in str(name).lower()
                        or "lithuania" in str(name).lower()
                    ):
                        item_uuids.add(uuid)
                receipt["movebank_searches"].append(
                    {
                        "query": field_query,
                        "url": final,
                        "n_results": len(objs),
                        "objects": compact[:100],
                    }
                )
            except Exception as exc:
                receipt["errors"].append(
                    f"search:{field_query}:{type(exc).__name__}:{exc}"
                )

    # Follow candidate items and enumerate ORIGINAL bitstreams.
    for uuid in sorted(item_uuids):
        item_rec = {"uuid": uuid, "bundles": []}
        try:
            item, _ = get_json(f"{BASE}/server/api/core/items/{uuid}")
            item_rec.update(
                {
                    "name": item.get("name"),
                    "handle": item.get("handle"),
                }
            )
            bundles, _ = get_json(
                f"{BASE}/server/api/core/items/{uuid}/bundles?size=100"
            )
            for bundle in bundles.get("_embedded", {}).get("bundles", []):
                buuid = bundle.get("uuid")
                bname = bundle.get("name")
                brec = {"uuid": buuid, "name": bname, "bitstreams": []}
                if buuid:
                    bits, _ = get_json(
                        f"{BASE}/server/api/core/bundles/{buuid}"
                        "/bitstreams?size=100"
                    )
                    for bit in bits.get("_embedded", {}).get("bitstreams", []):
                        bid = bit.get("uuid")
                        row = {
                            "item_uuid": uuid,
                            "item_name": item.get("name"),
                            "bundle_uuid": buuid,
                            "bundle_name": bname,
                            "bitstream_uuid": bid,
                            "bitstream_name": bit.get("name"),
                            "sizeBytes": bit.get("sizeBytes"),
                            "content_url": (
                                f"{BASE}/server/api/core/bitstreams/"
                                f"{bid}/content"
                                if bid else None
                            ),
                        }
                        brec["bitstreams"].append(row)
                        receipt["bitstreams"].append(row)
                item_rec["bundles"].append(brec)
        except Exception as exc:
            item_rec["error"] = f"{type(exc).__name__}:{exc}"
        receipt["items"].append(item_rec)

    receipt["found_public_bitstream"] = bool(receipt["bitstreams"])
    (OUT / "stage3_wigeon_lithuania_discovery.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
