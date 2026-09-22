#!/usr/bin/env python3
"""Discover original Movebank Data Repository files for three barnacle-goose flyways.

Prefer the legacy DOI -> handle -> METS route used by the historical move
package, because these datasets were published in the pre-DSpace7 repository.
Use the current DSpace API only as a fallback.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote, urljoin
import xml.etree.ElementTree as ET

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


def doi_landing(doi: str) -> str:
    url = f"https://doi.org/{doi}"
    try:
        r = requests.head(url, headers=UA, timeout=30, allow_redirects=True)
        if r.ok and "/handle/" in str(r.url):
            return str(r.url)
    except Exception:
        pass
    r = requests.get(url, headers=UA, timeout=30, allow_redirects=True)
    r.raise_for_status()
    return str(r.url)


def mets_discover(doi: str) -> dict:
    rec: dict = {"doi": doi, "files": [], "errors": []}
    try:
        landing = doi_landing(doi)
        rec["landing_url"] = landing
        if "/handle/" not in landing:
            rec["errors"].append("DOI did not resolve to legacy /handle/ URL")
            return rec
        candidates = []
        for host in {
            landing,
            landing.replace("www.datarepository.movebank.org", "datarepository.movebank.org"),
            landing.replace("datarepository.movebank.org", "www.datarepository.movebank.org"),
        }:
            candidates.append(
                host.replace("/handle/", "/metadata/handle/").rstrip("/")
                + "/mets.xml"
            )
        rec["mets_candidates"] = candidates
        for mets_url in candidates:
            try:
                r = requests.get(mets_url, headers=UA, timeout=45, allow_redirects=True)
                if r.status_code != 200 or not r.content:
                    rec["errors"].append(f"{mets_url}:HTTP{r.status_code}")
                    continue
                root = ET.fromstring(r.content)
                files = []
                for file_el in root.findall(".//{http://www.loc.gov/METS/}file"):
                    mime = file_el.attrib.get("MIMETYPE")
                    floc = file_el.find(".//{http://www.loc.gov/METS/}FLocat")
                    if floc is None:
                        continue
                    href = floc.attrib.get("{http://www.w3.org/1999/xlink}href")
                    title = floc.attrib.get("{http://www.w3.org/1999/xlink}title")
                    label = floc.attrib.get("{http://www.w3.org/1999/xlink}label")
                    if not href:
                        continue
                    files.append(
                        {
                            "title": title,
                            "label": label,
                            "mime": mime,
                            "url": urljoin(str(r.url), href),
                        }
                    )
                if files:
                    rec["working_mets_url"] = str(r.url)
                    rec["files"] = files
                    return rec
            except Exception as exc:
                rec["errors"].append(f"{mets_url}:{type(exc).__name__}:{exc}")
    except Exception as exc:
        rec["errors"].append(f"doi:{type(exc).__name__}:{exc}")
    return rec


def dspace_fallback(doi: str) -> dict:
    rec = {"files": [], "errors": []}
    qurl = (
        f"{BASE}/server/api/discover/search/objects?"
        f"query={quote('dc.identifier.doi:'+doi)}&size=10"
    )
    try:
        r = requests.get(qurl, headers=UA, timeout=25)
        r.raise_for_status()
        data = r.json()
        objs = (
            data.get("_embedded", {})
            .get("searchResult", {})
            .get("_embedded", {})
            .get("objects", [])
        )
        rec["objects"] = []
        for obj in objs:
            idx = obj.get("_embedded", {}).get("indexableObject", {})
            uuid = idx.get("uuid") or idx.get("id")
            rec["objects"].append(
                {"uuid": uuid, "name": idx.get("name"), "handle": idx.get("handle")}
            )
            if not uuid:
                continue
            try:
                b = requests.get(
                    f"{BASE}/server/api/core/items/{uuid}/bundles?size=100",
                    headers=UA,
                    timeout=25,
                )
                b.raise_for_status()
                bundles = b.json().get("_embedded", {}).get("bundles", [])
                for bundle in bundles:
                    buuid = bundle.get("uuid")
                    if not buuid:
                        continue
                    bs = requests.get(
                        f"{BASE}/server/api/core/bundles/{buuid}/bitstreams?size=100",
                        headers=UA,
                        timeout=25,
                    )
                    bs.raise_for_status()
                    for bit in bs.json().get("_embedded", {}).get("bitstreams", []):
                        bid = bit.get("uuid")
                        if bid:
                            rec["files"].append(
                                {
                                    "title": bit.get("name"),
                                    "label": bundle.get("name"),
                                    "mime": None,
                                    "url": f"{BASE}/server/api/core/bitstreams/{bid}/content",
                                }
                            )
            except Exception as exc:
                rec["errors"].append(f"item:{uuid}:{type(exc).__name__}:{exc}")
    except Exception as exc:
        rec["errors"].append(f"discover:{type(exc).__name__}:{exc}")
    return rec


def main():
    records = []
    for flyway, doi in DATASETS.items():
        rec = {"flyway": flyway, **mets_discover(doi)}
        if not rec.get("files"):
            fallback = dspace_fallback(doi)
            rec["dspace_fallback"] = fallback
            rec["files"] = fallback.get("files", [])
        records.append(rec)

    (OUT / "stage3_barnacle_multiflyway_discovery.json").write_text(
        json.dumps(records, indent=2) + "\n", encoding="utf-8"
    )
    rows = []
    for rec in records:
        for file_rec in rec.get("files", []):
            rows.append(
                {
                    "flyway": rec["flyway"],
                    "doi": rec["doi"],
                    **file_rec,
                }
            )
    pd.DataFrame(rows).to_csv(
        OUT / "stage3_barnacle_multiflyway_bitstreams.csv", index=False
    )
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
