"""Synthetic-only Dryad HAL API, checksum and file-schema gate tests."""
import hashlib
from scripts.payoff_b_dryad_food_supplement_provisioning_probe import (
    DOI_ARG, embedded_nodes, version_ids_from_listing,
    file_rows_from_listing, validate_manifest_digest
)


def test_doi_is_urlencoded_with_slash_not_literal():
    assert DOI_ARG=="doi%3A10.5061%2Fdryad.qbzkh18dj"


def test_api_versions_from_structured_nodes_only():
    payload={"_embedded":{"stash:versions":[
        {"id":1003,"versionNumber":1},
        {"id":1120,"versionNumber":2}
    ]},"total":2}
    x=version_ids_from_listing(payload)
    assert [z[0] for z in x]==[1003,1120]


def test_files_parse_from_official_api_only():
    payload={"_embedded":{"stash:files":[
        {"id":21,"path":"video.xlsx","size":1200,
         "digestType":"md5","digest":"abcd"},
        {"id":22,"path":"README.md","size":120}
    ]}}
    f=file_rows_from_listing(payload)
    assert f[0]["id"]==21 and f[0]["size"]==1200
    assert f[1]["digest"] is None


def test_source_bytes_digest_fail_closed():
    content=b"Original synthetic source only"
    f={"digestType":"md5","digest":hashlib.md5(content).hexdigest()}
    assert validate_manifest_digest(content,f)["verified"] is True
    assert validate_manifest_digest(content+b"changed",f)["verified"] is False
    assert validate_manifest_digest(content,{})["verified"] is False
