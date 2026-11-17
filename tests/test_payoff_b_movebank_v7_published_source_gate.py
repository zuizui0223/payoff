"""Offline archive DOI and DSpace item contract fixtures only."""
from scripts.payoff_b_movebank_v7_published_source_gate import (
    DOIS,controlled_link,extract_items,doi_in_metadata,metadata_values
)


def test_only_official_dspace_api_links():
    assert controlled_link("/server/api/core/items/a")==(
       "https://datarepository.movebank.org/server/api/core/items/a")
    assert controlled_link("/api/core/items/a")==(
       "https://datarepository.movebank.org/server/api/core/items/a")
    assert controlled_link("https://evil.example.org/server/api/core/items/a") is None
    assert controlled_link("http://datarepository.movebank.org/server/api/secret") is None


def test_search_only_accepts_exact_doi_evidence():
    item={
       "uuid":"test-uuid",
       "name":"Migration timing in barnacle geese",
       "metadata":{"dc.identifier.doi":[{"value":DOIS["Greenland"]}]},
       "_links":{"self":{"href":"/server/api/core/items/a"}}
    }
    response={"_embedded":{"searchResult":{"_embedded":{
        "objects":[{"_embedded":{"indexableObject":item}}]
    }}}}
    items=extract_items(response)
    assert len(items)==1
    assert doi_in_metadata(items[0],DOIS["Greenland"]) is not None
    assert doi_in_metadata(items[0],DOIS["Svalbard"]) is None


def test_metadata_rights_are_structured():
    item={"metadata":{"dc.rights.uri":[
        {"value":"https://creativecommons.org/licenses/by/4.0/"}]}}
    assert len(metadata_values(item,"dc.rights.uri"))==1
