"""Source-only synthetic DataCite/DSpace archive metadata tests (no GPS)."""
import pytest
from scripts import payoff_b_v7_barnacle_archived_source_audit_20261124 as s

def c():
    return {"archive_DOIs":[
      {"flyway":"greenland","doi":"10.5441/001/1.5d3f0664","expected_label":"Greenland"},
      {"flyway":"svalbard","doi":"10.5441/001/1.5k6b1364","expected_label":"Svalbard"},
      {"flyway":"barents","doi":"10.5441/001/1.ps244r11","expected_label":"Barents"}
    ],"metadata_transport":{"max_response_bytes":300000}}

def test_allowlist_only_three_registered_citation_dois_and_known_metadata():
    s.allowed_metadata_url(s.DATACITE+"10.5441/001/1.ps244r11",c())
    s.allowed_metadata_url(s.SEARCH,c())
    with pytest.raises(ValueError,match="Unregistered|Only original"):
        s.allowed_metadata_url("https://datarepository.movebank.org/server/api/core/bitstreams/secret/content",c())
    with pytest.raises(ValueError,match="Unregistered"):
        s.allowed_metadata_url(s.DATACITE+"10.5441/001/1.fake",c())
    with pytest.raises(ValueError,match="Unregistered"):
        s.allowed_metadata_url("https://www.movebank.org/movebank/service/direct-read?entity_type=event",c())


def test_datacite_original_title_license_and_doi_identity():
    doi="10.5441/001/1.5d3f0664"
    z={"data":{"attributes":{"doi":doi,"titles":[{"title":"Migration timing in barnacle geese (Greenland)"}],
        "publicationYear":2015,"publisher":"Movebank Data Repository",
        "url":"https://datarepository.movebank.org/handle/10255/move.123",
        "rightsList":[{"rights":"CC0 1.0 Universal","rightsUri":"https://creativecommons.org/publicdomain/zero/1.0/"}]}}}
    x=s.citation_record(z,doi,"Greenland")
    assert x["doi"]==doi
    assert x["CC0_metadata_confirmed"] is True
    assert x["metadata_only"] is True
    with pytest.raises(ValueError,match="DOI"):
        s.citation_record(z,"10.5441/001/1.ps244r11","Barents")


def test_public_dspace_search_is_only_original_public_item_uuid():
    uuid="a0a0a0a0-bbbb-cccc-dddd-eeeeeeeeeeee"
    z={"_embedded":{"searchResult":{"_embedded":{"objects":[
        {"_embedded":{"indexableObject":{"uuid":uuid,
        "name":"Migration timing in barnacle geese (Svalbard)","handle":"10255/move.164"}}},
        {"_embedded":{"indexableObject":{"uuid":"not-a-uuid","name":"Migration timing in barnacle geese (Greenland)"}}},
        {"_embedded":{"indexableObject":{"uuid":"a0a0a0a0-bbbb-cccc-dddd-ffffffffffff","name":"Other bird data"}}}
    ]}}}}
    x=s.dspace_discovery(z)
    assert x==[{"title":"Migration timing in barnacle geese (Svalbard)",
                "uuid":uuid,"handle":"10255/move.164"}]
    match=s.find_item_for_doi(
      {"landing":"https://datarepository.movebank.org/handle/10255/move.164",
       "title":"Migration timing in barnacle geese (Svalbard)"},x)
    assert match["uuid"]==uuid


def test_never_emits_original_bitstream_member_name_uuid_or_content():
    r=s.source_files([{"uuid":"PRIVATE_TAG_GOOSE",
       "name":"PRIVATE_GOOSE_TAG__GPS_events.zip","sizeBytes":10302,
       "checkSum":{"checkSumAlgorithm":"MD5","value":"PRIVATEHASH"}},
       {"name":"README.txt","sizeBytes":5000}])
    assert len(r)==2
    assert r[0]["name_contains_GPS"] is True
    assert r[0]["file_extension"]==".zip"
    assert r[0]["original_MD5_metadata_present"] is True
    assert r[0]["bitstream_content_downloaded"] is False
    assert "PRIVATE_TAG_GOOSE" not in str(r)
    assert "PRIVATEHASH" not in str(r)


def test_2014_published_archive_title_alias_is_not_wrongly_rejected():
    doi="10.5441/001/1.ps244r11"
    original="Data from: Forecasting spring from afar? Timing of migration and predictability of phenology along different migration routes of an avian herbivore [Barents Sea data]"
    citation={"data":{"attributes":{
        "doi":doi,"titles":[{"title":original}],
        "publisher":"Movebank","publicationYear":2014,
        "url":"https://datarepository.movebank.org/handle/10255/move.777",
        "rightsList":[{"rights":"CC BY 4.0"}]
    }}}
    x=s.citation_record(citation,doi,"Migration timing in barnacle geese (Barents Sea)")
    assert x["doi"]==doi
    assert x["CC0_metadata_confirmed"] is False  # no invented CC0
    uuid="a0a0a0a0-bbbb-cccc-dddd-eeeeeeeeeeee"
    discovered=[{"uuid":uuid,"title":original,"handle":"10255/move.777"}]
    z=s.find_item_for_doi(x,discovered)
    assert z["uuid"]==uuid
    s.allowed_metadata_url(s.SEARCH_ALIAS,c())
    # Different flyway with same DOI cannot sneak past source title matching.
    with pytest.raises(ValueError,match="flyway"):
        s.citation_record(citation,doi,"Migration timing in barnacle geese (Greenland)")
