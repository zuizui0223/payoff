"""The stork original-archive screen MUST NOT download Movebank events."""
import pytest
from scripts import payoff_b_stork_experiment_source_metadata_audit_20261124 as s


def test_datacite_source_doi_exact_match():
    raw={"data":{"attributes":{
        "doi":"10.5441/001/1.271",
        "titles":[{"title":"Data from: delayed juvenile white stork experiment"}],
        "publicationYear":2023,"publisher":"Movebank Data Repository",
        "rightsList":[{"rights":"CC BY-NC"}],
        "url":"https://datarepository.movebank.org/handle/test"
    }}}
    r=s.read_datacite(raw,"10.5441/001/1.271")
    assert r["doi"]=="10.5441/001/1.271"
    assert r["tracking_event_rows_requested"] is False
    with pytest.raises(ValueError,match="DOI"):
        s.read_datacite(raw,"10.5441/001/1.276")


def test_zenodo_code_manifest_does_not_include_file_bytes_or_download_url():
    z={"id":8108611,"metadata":{"title":"Code for stork delay"},
       "files":[{"key":"analysis.zip","size":500,"checksum":"md5:abc",
                 "links":{"self":"https://secret/download"}}]}
    a=s.read_zenodo(z)
    assert a["file_count"]==1
    assert a["source_archive_files_downloaded"] is False
    assert "https://secret/download" not in str(a)
    assert a["files"][0]["size_bytes"]==500


def test_disallow_movebank_event_url_as_source_metadata():
    with pytest.raises(ValueError,match="allowlisted"):
        s.fetch_json("https://www.movebank.org/movebank/service/direct-read?entity_type=event")
    with pytest.raises(ValueError,match="allowlisted"):
        s.fetch_json("https://zenodo.org/api/records/8108611/files/data.csv")


def test_source_provenance_only():
    assert s.STORK_ARCHIVES==[
        "10.5441/001/1.271",
        "10.5441/001/1.276",
        "10.5441/001/1.277"
    ]
    assert s.BYTE_CAP<=1_000_000
