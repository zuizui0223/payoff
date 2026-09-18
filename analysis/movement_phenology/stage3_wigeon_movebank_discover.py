#!/usr/bin/env python3
"""Discover public Movebank repository assets for Eurasian wigeon DOI.

DOI: 10.5441/001/1.dv5mm289

The script queries DataCite, DOI redirects, the Movebank DSpace discovery API,
and any resolved landing page links. It records machine-readable item and
bitstream candidates but does not guess UUIDs.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote, urljoin

import requests


DOI = "10.5441/001/1.dv5mm289"
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://datarepository.movebank.org"
UA = {"User-Agent": "payoff-movement-phenology-reanalysis/1.0"}


def get_json(url, *, timeout=60):
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.json(), str(r.url)


def get_text(url, *, timeout=60):
    r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.text, str(r.url), dict(r.headers)


def collect_links(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("href", "url") and isinstance(v, str):
                out.add(v)
            collect_links(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_links(v, out)


def main():
    receipt = {
        "doi": DOI,
        "datacite": None,
        "doi_redirect": None,
        "discover_queries": [],
        "candidate_item_urls": [],
        "candidate_bitstream_urls": [],
        "errors": [],
    }

    # DataCite is often the cleanest way to learn the current landing URL.
    try:
        dc, url = get_json(f"https://api.datacite.org/dois/{DOI}")
        attrs = dc.get("data", {}).get("attributes", {})
        receipt["datacite"] = {
            "request_url": url,
            "url": attrs.get("url"),
            "titles": attrs.get("titles"),
            "publisher": attrs.get("publisher"),
            "types": attrs.get("types"),
        }
    except Exception as exc:
        receipt["errors"].append(f"datacite:{type(exc).__name__}:{exc}")

    try:
        _, resolved, headers = get_text(f"https://doi.org/{DOI}")
        receipt["doi_redirect"] = {
            "resolved_url": resolved,
            "content_type": headers.get("content-type"),
        }
    except Exception as exc:
        receipt["errors"].append(f"doi_redirect:{type(exc).__name__}:{exc}")

    queries = [
        DOI,
        "dv5mm289",
        '"Eurasian wigeon"',
        '"Mareca penelope"',
        '"Eurasian wigeon (Mareca penelope) Netherlands Lithuania 2018-2019"',
    ]

    candidate_item_urls = set()
    all_links = set()

    for q in queries:
        urls = [
            f"{BASE}/server/api/discover/search/objects?query={quote(q)}&size=50",
            f"{BASE}/server/api/discover/search/objects?query={quote('dc.identifier.doi:'+q)}&size=50",
        ]
        for url in urls:
            try:
                data, final = get_json(url)
                links = set()
                collect_links(data, links)
                all_links |= links
                embedded = data.get("_embedded", {}) if isinstance(data, dict) else {}
                objs = embedded.get("searchResult", {}).get("_embedded", {}).get("objects", [])
                compact = []
                for obj in objs:
                    idx = obj.get("_embedded", {}).get("indexableObject", {})
                    uuid = idx.get("uuid") or idx.get("id")
                    name = idx.get("name")
                    typ = idx.get("type")
                    handle = idx.get("handle")
                    compact.append(
                        {"uuid": uuid, "name": name, "type": typ, "handle": handle}
                    )
                    if uuid:
                        candidate_item_urls.add(f"{BASE}/server/api/core/items/{uuid}")
                receipt["discover_queries"].append(
                    {
                        "query": q,
                        "request_url": final,
                        "n_objects": len(objs),
                        "objects": compact,
                    }
                )
            except Exception as exc:
                receipt["errors"].append(
                    f"discover:{q}:{type(exc).__name__}:{exc}"
                )

    # Try any item URLs found from API links as well as embedded result UUIDs.
    for link in list(all_links):
        if "/server/api/core/items/" in link:
            candidate_item_urls.add(link)

    item_receipts = []
    bitstream_urls = set()

    for item_url in sorted(candidate_item_urls):
        try:
            item, final = get_json(item_url)
            uuid = item.get("uuid") or item.get("id")
            item_rec = {
                "url": final,
                "uuid": uuid,
                "name": item.get("name"),
                "handle": item.get("handle"),
                "metadata_url": None,
                "bundles_url": None,
                "bundles": [],
            }

            if uuid:
                metadata_url = f"{BASE}/server/api/core/items/{uuid}/metadata"
                item_rec["metadata_url"] = metadata_url
                try:
                    md, _ = get_json(metadata_url)
                    md_values = [
                        str(x.get("value", ""))
                        for x in md
                        if isinstance(x, dict)
                    ]
                    item_rec["doi_metadata_match"] = any(
                        DOI.lower() in x.lower() for x in md_values
                    )
                    item_rec["metadata_values_matching_wigeon"] = [
                        x for x in md_values
                        if ("wigeon" in x.lower() or "dv5mm289" in x.lower()
                            or DOI.lower() in x.lower())
                    ][:30]
                except Exception as exc:
                    item_rec["metadata_error"] = str(exc)

                bundles_url = f"{BASE}/server/api/core/items/{uuid}/bundles?size=100"
                item_rec["bundles_url"] = bundles_url
                try:
                    bundles, _ = get_json(bundles_url)
                    barr = bundles.get("_embedded", {}).get("bundles", [])
                    for bundle in barr:
                        buuid = bundle.get("uuid")
                        bname = bundle.get("name")
                        brec = {"uuid": buuid, "name": bname, "bitstreams": []}
                        if buuid:
                            bs_url = (
                                f"{BASE}/server/api/core/bundles/{buuid}"
                                "/bitstreams?size=100"
                            )
                            try:
                                bs, _ = get_json(bs_url)
                                for bit in bs.get("_embedded", {}).get("bitstreams", []):
                                    bid = bit.get("uuid")
                                    name = bit.get("name")
                                    size = bit.get("sizeBytes")
                                    fmt = bit.get("format")
                                    content_url = (
                                        f"{BASE}/server/api/core/bitstreams/"
                                        f"{bid}/content"
                                        if bid else None
                                    )
                                    brec["bitstreams"].append(
                                        {
                                            "uuid": bid,
                                            "name": name,
                                            "sizeBytes": size,
                                            "format": fmt,
                                            "content_url": content_url,
                                        }
                                    )
                                    if content_url:
                                        bitstream_urls.add(content_url)
                            except Exception as exc:
                                brec["bitstream_error"] = str(exc)
                        item_rec["bundles"].append(brec)
                except Exception as exc:
                    item_rec["bundles_error"] = str(exc)

            item_receipts.append(item_rec)
        except Exception as exc:
            receipt["errors"].append(
                f"item:{item_url}:{type(exc).__name__}:{exc}"
            )

    receipt["candidate_item_urls"] = sorted(candidate_item_urls)
    receipt["items"] = item_receipts
    receipt["candidate_bitstream_urls"] = sorted(bitstream_urls)

    (OUT / "stage3_wigeon_movebank_discovery.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    rows = []
    for item in item_receipts:
        for bundle in item.get("bundles", []):
            for bit in bundle.get("bitstreams", []):
                rows.append(
                    {
                        "item_uuid": item.get("uuid"),
                        "item_name": item.get("name"),
                        "doi_metadata_match": item.get("doi_metadata_match"),
                        "bundle": bundle.get("name"),
                        **bit,
                    }
                )
    import pandas as pd
    pd.DataFrame(rows).to_csv(
        OUT / "stage3_wigeon_movebank_bitstreams.csv", index=False
    )

    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
