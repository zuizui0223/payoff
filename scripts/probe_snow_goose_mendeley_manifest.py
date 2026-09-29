#!/usr/bin/env python3
"""Probe public metadata for the snow-goose Mendeley dataset.

This is a metadata-only gate. It does not fit ecological models or inspect
tabular response values.

Resolution order:
1. Digital Commons Data REST public endpoints.
2. Open OAI-PMH metadata, which Mendeley documents as authorization-free.
3. Public human dataset page Schema.org / JSON-LD metadata.

Only dataset identity and file-manifest-like metadata are retained.
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import requests


ARTICLE_DOI = "10.1016/j.biocon.2023.110240"
DATASET_DOI = "10.17632/ycxxrg8497.1"
SLUG = "ycxxrg8497"
API = "https://api.data.mendeley.com"
OAI = "https://data.mendeley.com/oai"
PUBLIC_PAGES = (
    f"https://data.mendeley.com/datasets/{SLUG}/1",
    f"https://data.mendeley.com/datasets/{SLUG}",
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_snow_goose_mendeley_manifest_probe.json"
        ),
    )
    return p.parse_args()


def get_response(session, url, **params):
    try:
        r = session.get(url, params=params, timeout=60)
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": None,
            "error": type(exc).__name__,
            "text": None,
            "url": url,
        }
    return {
        "ok": bool(r.ok),
        "status": int(r.status_code),
        "error": None,
        "text": r.text,
        "url": str(r.url),
    }


def as_json(response):
    if not response.get("ok") or response.get("text") is None:
        return None
    try:
        return json.loads(response["text"])
    except (TypeError, ValueError):
        return None


def slim_file(row):
    if not isinstance(row, dict):
        return None
    content = row.get("content_details") or {}
    return {
        "id": row.get("id"),
        "filename": row.get("filename") or row.get("name"),
        "description": row.get("description"),
        "size": row.get("size") or content.get("size"),
        "content_type": content.get("content_type") or row.get("encodingFormat"),
        "sha256_hash": content.get("sha256_hash"),
        "has_download_url": bool(
            content.get("download_url")
            or row.get("contentUrl")
            or row.get("content_url")
        ),
    }


def oai_records(session):
    """Search a narrow publication-date window for the frozen dataset DOI."""

    params = {
        "verb": "ListRecords",
        "metadataPrefix": "oai_dc",
        "from": "2023-08-28",
        "until": "2023-08-30",
    }
    pages = 0
    statuses = []
    while pages < 10:
        response = get_response(session, OAI, **params)
        statuses.append(response.get("status"))
        if not response.get("ok") or not response.get("text"):
            return None, statuses

        try:
            root = ET.fromstring(response["text"])
        except ET.ParseError:
            return None, statuses

        ns = {
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        for record in root.findall(".//oai:record", ns):
            header_id = record.findtext("oai:header/oai:identifier", default="", namespaces=ns)
            datestamp = record.findtext("oai:header/oai:datestamp", default="", namespaces=ns)
            titles = [
                (x.text or "").strip()
                for x in record.findall(".//dc:title", ns)
            ]
            identifiers = [
                (x.text or "").strip()
                for x in record.findall(".//dc:identifier", ns)
            ]
            relations = [
                (x.text or "").strip()
                for x in record.findall(".//dc:relation", ns)
            ]
            all_text = "\n".join(
                [header_id, datestamp, *titles, *identifiers, *relations]
            ).lower()
            if (
                DATASET_DOI.lower() in all_text
                or SLUG.lower() in all_text
                or "fattening of migratory snow geese" in all_text
            ):
                return {
                    "header_identifier": header_id or None,
                    "datestamp": datestamp or None,
                    "titles": titles,
                    "identifiers": identifiers,
                    "relations": relations,
                }, statuses

        token = root.findtext(".//oai:resumptionToken", default="", namespaces=ns).strip()
        if not token:
            break
        params = {"verb": "ListRecords", "resumptionToken": token}
        pages += 1

    return None, statuses


def walk_jsonld(node):
    """Collect safe manifest-like fields from arbitrary Schema.org JSON-LD."""

    files = []
    dataset = {}

    def visit(value):
        nonlocal dataset
        if isinstance(value, dict):
            typ = value.get("@type")
            if (
                typ == "Dataset"
                or (isinstance(typ, list) and "Dataset" in typ)
            ):
                dataset = {
                    "name": value.get("name"),
                    "identifier": value.get("identifier"),
                    "doi": value.get("doi"),
                    "datePublished": value.get("datePublished"),
                    "url": value.get("url"),
                }
            if typ == "DataDownload" or any(
                key in value
                for key in ("contentUrl", "encodingFormat", "contentSize")
            ):
                files.append(
                    {
                        "id": None,
                        "filename": value.get("name"),
                        "description": value.get("description"),
                        "size": value.get("contentSize"),
                        "content_type": value.get("encodingFormat"),
                        "sha256_hash": None,
                        "has_download_url": bool(value.get("contentUrl")),
                    }
                )
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(node)
    return dataset or None, files


def public_page_schema(session):
    statuses = []
    for url in PUBLIC_PAGES:
        response = get_response(session, url)
        statuses.append(response.get("status"))
        if not response.get("ok") or not response.get("text"):
            continue

        blocks = re.findall(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            response["text"],
            flags=re.IGNORECASE | re.DOTALL,
        )
        all_files = []
        dataset_meta = None
        for block in blocks:
            try:
                payload = json.loads(block.strip())
            except ValueError:
                continue
            meta, files = walk_jsonld(payload)
            if meta:
                dataset_meta = meta
            all_files.extend(files)
        if dataset_meta or all_files:
            return {
                "page_url": response["url"],
                "dataset": dataset_meta,
                "files": all_files,
            }, statuses
    return None, statuses


def main():
    args = parse_args()
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "PAYOFF-B-public-mendeley-manifest-probe/2.0",
            "Accept": "application/json,text/html,application/xml;q=0.9,*/*;q=0.1",
        }
    )

    discovery_response = get_response(
        session,
        f"{API}/datasets/publics",
        article_doi=ARTICLE_DOI,
        **{"$limit": 20},
    )
    discovery = as_json(discovery_response)
    candidates = [
        x for x in discovery
        if isinstance(x, dict)
    ] if isinstance(discovery, list) else []

    direct_response = get_response(
        session,
        f"{API}/datasets/{SLUG}",
        version=1,
    )
    direct = as_json(direct_response)

    direct_public_response = get_response(
        session,
        f"{API}/datasets/publics/{SLUG}",
        version=1,
    )
    direct_public = as_json(direct_public_response)

    dataset_id = None
    dataset_meta = None
    for row in (direct, direct_public):
        if isinstance(row, dict):
            dataset_id = row.get("id") or SLUG
            dataset_meta = row
            break

    if dataset_id is None:
        for row in candidates:
            doi = row.get("doi")
            doi_value = (
                doi.get("id") if isinstance(doi, dict) else doi
            )
            if (
                str(doi_value).lower() == DATASET_DOI.lower()
                or "snow geese" in str(row.get("name", "")).lower()
            ):
                dataset_id = row.get("id")
                dataset_meta = row
                break

    files_status = None
    file_manifest = []
    if dataset_id:
        files_response = get_response(
            session,
            f"{API}/datasets/{dataset_id}/files",
            version=1,
            **{"$limit": 100},
        )
        files_status = files_response.get("status")
        files_json = as_json(files_response)
        if not isinstance(files_json, list):
            files_response = get_response(
                session,
                f"{API}/datasets/publics/{dataset_id}/files",
                version=1,
                **{"$limit": 100},
            )
            files_status = files_response.get("status")
            files_json = as_json(files_response)
        if isinstance(files_json, list):
            file_manifest = [
                slim_file(x) for x in files_json
                if slim_file(x) is not None
            ]

    oai_record, oai_statuses = oai_records(session)
    page_schema, page_statuses = public_page_schema(session)

    if not file_manifest and page_schema:
        file_manifest = page_schema.get("files", [])

    meta_summary = None
    if isinstance(dataset_meta, dict):
        doi = dataset_meta.get("doi")
        doi_value = doi.get("id") if isinstance(doi, dict) else doi
        meta_summary = {
            "id": dataset_meta.get("id"),
            "name": dataset_meta.get("name"),
            "version": dataset_meta.get("version"),
            "doi": doi_value,
        }
    elif page_schema and page_schema.get("dataset"):
        meta_summary = page_schema["dataset"]
    elif oai_record:
        meta_summary = {
            "id": oai_record.get("header_identifier"),
            "name": (
                oai_record["titles"][0]
                if oai_record.get("titles") else None
            ),
            "version": 1,
            "doi": DATASET_DOI,
        }

    if file_manifest:
        classification = "PUBLIC_FILE_MANIFEST_RESOLVED"
    elif dataset_id:
        classification = "REST_DATASET_RESOLVED_FILE_MANIFEST_UNAVAILABLE"
    elif page_schema:
        classification = "PUBLIC_PAGE_SCHEMA_RESOLVED_NO_FILE_MANIFEST"
    elif oai_record:
        classification = "OAI_DATASET_RECORD_RESOLVED_NO_FILE_MANIFEST"
    else:
        classification = "PUBLIC_DATASET_METADATA_UNRESOLVED"

    result = {
        "probe_id": "payoff_b_snow_goose_mendeley_manifest_v2",
        "date": "2026-09-29",
        "article_doi": ARTICLE_DOI,
        "dataset_doi": DATASET_DOI,
        "human_slug": SLUG,
        "classification": classification,
        "rest": {
            "discovery_http_status": discovery_response.get("status"),
            "direct_slug_http_status": direct_response.get("status"),
            "direct_public_slug_http_status": direct_public_response.get("status"),
            "files_http_status": files_status,
            "resolved_dataset_id": dataset_id,
        },
        "oai": {
            "http_status_sequence": oai_statuses,
            "record": oai_record,
        },
        "public_page": {
            "http_status_sequence": page_statuses,
            "resolved_schema": bool(page_schema),
            "page_url": page_schema.get("page_url") if page_schema else None,
        },
        "dataset": meta_summary,
        "file_count": len(file_manifest),
        "files": file_manifest,
        "claim_boundary": [
            "metadata/file manifest only",
            "no ecological response model fitted",
            "body condition and behavior are D-like state information, not PAYOFF-B D",
            "this auxiliary lane cannot identify q_wait(D)",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
