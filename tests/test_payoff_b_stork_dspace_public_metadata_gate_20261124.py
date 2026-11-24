"""Public DSpace metadata-only source safety tests, without GPS/event files."""
import json
import pytest
from scripts import payoff_b_stork_dspace_public_metadata_gate_20261124 as s


class FakeResponse:
    def __init__(self,url,payload=b'{"_links":{}}',ctype="application/hal+json"):
        self._url=url;self.payload=payload;self.headers={"Content-Type":ctype};self.status=200
    def __enter__(self):return self
    def __exit__(self,*exc):return False
    def geturl(self):return self._url
    def read(self,n):
        assert n<=s.CAP_BYTES+1
        return self.payload[:n]


def test_allowlisted_root_is_json_only_and_no_event():
    def open_fn(req,timeout):
        assert req.full_url==s.ROOT
        return FakeResponse(s.ROOT)
    z=s.request_public_metadata(s.ROOT,open_fn=open_fn)
    assert z["status"]=="PUBLIC_JSON_RECEIVED"
    assert z["json"]=={"_links":{}}


def test_unregistered_event_and_tracking_download_rejected():
    for url in [
        "https://datarepository.movebank.org/server/api/core/bitstreams/id/content",
        "https://www.movebank.org/movebank/service/direct-read?entity_type=event",
        "https://datarepository.movebank.org/handle/10255/move.1627",
    ]:
        with pytest.raises(ValueError,match="Unregistered"):
            s.request_public_metadata(url)


def test_disallow_non_json_or_external_host_after_redirect():
    def bad_content(req,timeout):
        return FakeResponse(s.ROOT,b"<html>data</html>","text/html")
    assert s.request_public_metadata(s.ROOT,open_fn=bad_content)["status"]=="NO_PUBLIC_DSPACE_JSON_AVAILABLE"
    def bad_host(req,timeout):
        return FakeResponse("https://untrusted.invalid/server/api",b'{}')
    assert s.request_public_metadata(s.ROOT,open_fn=bad_host)["status"]=="NO_PUBLIC_DSPACE_JSON_AVAILABLE"


def test_extract_only_author_title_and_public_uuid_from_hal():
    z={"_embedded":{"searchResult":{"_embedded":{"objects":[
      {"_embedded":{"indexableObject":{
        "uuid":"public-id","handle":"10255/move.1627",
        "name":"original stork experiment",
        "metadata":{"dc.title":[{"value":"The price of being late: control birds"}]}
      }}},
      {"_embedded":{"indexableObject":{
        "uuid":"another","metadata":{"dc.title":[{"value":"unrelated paper"}]}
      }}}
    ]}}}}
    rows=s.only_public_source_summary(z)
    assert len(rows)==1
    assert rows[0]["uuid"]=="public-id"
    assert rows[0]["bitstreams_requested"] is False
