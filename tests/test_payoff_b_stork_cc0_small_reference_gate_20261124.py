"""Source-only CC0 README/reference CSV guardrails; never GPS ZIP bytes."""
from hashlib import md5
import pytest

from scripts import payoff_b_stork_cc0_small_reference_gate_20261124 as s

U="eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"
URL=s.ROOT+"/server/api/core/bitstreams/"+U+"/content"
LIMITS={"file_access":{"max_file_bytes":80000,"expected_file_count_per_cohort":2}}


def fileinfo(name,raw):
    return {
      "name":name,
      "uuid":U,
      "sizeBytes":len(raw),
      "checkSum":{"checkSumAlgorithm":"MD5","value":md5(raw).hexdigest()},
      "_links":{"content":{"href":URL}},
    }


class FakeResponse:
    def __init__(self,raw):self.raw=raw
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def geturl(self):return URL
    def read(self,n):
        assert n<=80001
        return self.raw[:n]


class FakeOpener:
    def __init__(self,raw):self.raw=raw
    def open(self,request,timeout=25):
        assert request.full_url==URL
        assert request.get_method()=="GET"
        return FakeResponse(self.raw)


def test_read_aggregate_small_reference_csv_without_any_raw_identifiers():
    raw=b"tag.local.identifier,release_date,sex\nPRIVATE_TAG_123,2019-09-12,F\nPRIVATE_TAG_456,2019-09-13,M\n"
    result=s.small_verified_file(fileinfo("reference.csv",raw),LIMITS,opener=FakeOpener(raw))
    assert result["status"]=="PUBLIC_CC0_SOURCE_METADATA_COMPANION_VERIFIED"
    assert result["extension"]==".csv"
    assert result["content_metadata_only"]["n_data_rows"]==2
    assert result["content_metadata_only"]["unique_tag_or_individual_count"]==2
    assert "PRIVATE_TAG_123" not in str(result)
    assert "PRIVATE_TAG_456" not in str(result)
    assert result["raw_source_file_or_rows_committed"] is False


def test_readme_keyword_presence_not_prose():
    raw=b"This CC0 License dataset has GPS, ACC, timestamp UTC and a 1 minute interval"
    result=s.small_verified_file(fileinfo("README.txt",raw),LIMITS,opener=FakeOpener(raw))
    assert result["content_metadata_only"]["word_present"]["gps"] is True
    assert result["content_metadata_only"]["word_present"]["timestamp"] is True
    assert result["content_metadata_only"]["word_present"]["utc"] is True
    assert "This CC0 License" not in str(result)


def test_binary_and_large_files_fail_before_read():
    raw=b"PK\x03\x04"+b"X"*20
    with pytest.raises(ValueError,match="Binary"):
        s.content_meta_gate(fileinfo("GPS.zip",raw),LIMITS)
    big=fileinfo("README.txt",raw)
    big["sizeBytes"]=80001
    with pytest.raises(ValueError,match="size cap"):
        s.content_meta_gate(big,LIMITS)


def test_invalid_md5_or_wrong_href_fails_before_read():
    raw=b"data"
    x=fileinfo("README.txt",raw)
    x["checkSum"]["value"]="z"*32
    with pytest.raises(ValueError,match="MD5"):
        s.content_meta_gate(x,LIMITS)
    y=fileinfo("README.txt",raw)
    y["_links"]["content"]["href"]="https://unverified.invalid/GPS.csv"
    with pytest.raises(ValueError,match="exact"):
        s.content_meta_gate(y,LIMITS)


def test_same_source_md5_mismatch_does_not_publish_raw_values():
    claimed=b"abc"
    actual=b"xyz"
    result=s.small_verified_file(fileinfo("reference.csv",claimed),LIMITS,
                                 opener=FakeOpener(actual))
    assert result["status"]=="SOURCE_REFERENCE_CONTENT_NOT_VERIFIED"
    assert result["error_class"]=="ValueError"
    assert "abc" not in str(result)
    assert "xyz" not in str(result)
