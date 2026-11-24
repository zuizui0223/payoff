"""No GPS events, no original identifier strings, Svalbard noncommercial."""
from hashlib import md5
import json
import pytest

from scripts import payoff_b_v7_barnacle_small_reference_gate_20261124 as g

UUID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
URL=g.ROOT+f"/core/bitstreams/{UUID}/content"

def fake_file(name,payload):
    return {"name":name,"uuid":UUID,"sizeBytes":len(payload),
            "checkSum":{"checkSumAlgorithm":"MD5","value":md5(payload).hexdigest()},
            "_links":{"content":{"href":URL}}}

class FakeResp:
    def __init__(self,data):self.data=data;self.status=200
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def geturl(self):return URL
    def read(self,n):
        assert n<=20001
        return self.data[:n]

class FakeOpener:
    def __init__(self,data):self.data=data
    def open(self,req,timeout):
        assert req.full_url==URL
        return FakeResp(self.data)


def test_only_tiny_non_event_reference_files_allowed():
    blob=b"private metadata"
    with pytest.raises(ValueError,match="small source extension"):
        g.source_file_gate(fake_file("gps_events.zip",blob),len(blob),".csv")
    with pytest.raises(ValueError,match="Tracking/event"):
        g.source_file_gate(fake_file("source_GPS.csv",blob),len(blob),".csv")
    with pytest.raises(ValueError,match="file size changed"):
        g.source_file_gate(fake_file("reference.csv",blob),20001,".csv")


def test_original_MD5_reference_csv_only_schema_and_counts():
    payload=b"tag-id,animal-id,deploy-on-date\nPRIVATE_TAG_G,PRIVATE_BIRD_G,2006-01-01\nPRIVATE_TAG_G,PRIVATE_BIRD2,2006-02-02\n"
    z=g.read_small_public_reference(fake_file("study-reference.csv",payload),len(payload),".csv",
                                    opener=FakeOpener(payload))
    assert z["status"]=="ORIGINAL_TINY_SOURCE_MD5_VERIFIED"
    assert z["summary_only"]["n_data_rows"]==2
    assert z["summary_only"]["n_distinct_tag_strings"]==1
    assert z["summary_only"]["n_distinct_animal_strings"]==2
    assert z["summary_only"]["original_1982_2011_environment_anomaly_pair_fields_present"] is False
    assert "PRIVATE_TAG" not in str(z)
    assert "PRIVATE_BIRD" not in str(z)
    assert z["raw_source_rows_or_identifiers_exported"] is False


def test_readme_keyword_evidence_not_source_prose():
    payload=b"GPS fix timestamp UTC CC BY-NC License. No GDD data here."
    z=g.read_small_public_reference(fake_file("README.txt",payload),len(payload),".txt",
                                    opener=FakeOpener(payload))
    assert z["status"]=="ORIGINAL_TINY_SOURCE_MD5_VERIFIED"
    assert z["summary_only"]["keywords_present"]["GPS"]
    assert z["summary_only"]["keywords_present"]["timestamp"]
    assert z["summary_only"]["keywords_present"]["UTC"]
    assert "CC BY-NC License" not in str(z)


def test_public_metadata_original_MD5_or_same_host_mismatch_fails_before_fetch():
    payload=b"abc"
    f=fake_file("reference.csv",payload)
    f["checkSum"]["value"]="x"*32
    with pytest.raises(ValueError,match="MD5"):
        g.source_file_gate(f,len(payload),".csv")
    f=fake_file("reference.csv",payload)
    f["_links"]["content"]["href"]="https://untrusted.invalid/track.csv"
    with pytest.raises(ValueError,match="not exact"):
        g.source_file_gate(f,len(payload),".csv")


def test_registered_svalbard_license_is_noncommercial_not_cc0():
    c=json.loads(g.DEFAULT_CONTRACT.read_text())
    assert c["source_flyways"]["svalbard"]["license"]=="CC BY-NC 4.0"
    assert c["source_flyways"]["greenland"]["license"]=="CC0 1.0"
    assert c["source_flyways"]["barents"]["license"]=="CC0 1.0"
    assert c["no_original_GPS_event_rows_downloaded"] is True
    assert c["no_ebird"] is True
