"""Verify no-redirect, no-body, no-event Movebank archive access probes."""
import pytest

from scripts import payoff_b_stork_archive_head_probe_20261124 as s


class FakeResponse:
    def __init__(self):
        self.status=302
        self.headers={"Location":"https://new-archive.example/handle/10255/move.1627",
                      "Content-Type":"text/html"}
        self.closed=False
    def close(self):
        self.closed=True
    def read(self,*a,**k):
        raise AssertionError("HEAD-only client must not read any payload")


class FakeOpener:
    def __init__(self):
        self.response=FakeResponse()
        self.observed=None
    def open(self,req,timeout=20):
        self.observed=(req.full_url,req.get_method())
        return self.response


def test_only_pinned_original_doIs_and_landings():
    allowed={"https://doi.org/10.5441/001/1.271"}
    for bad in [
        "https://doi.org/10.5441/001/1.277",
        "https://datarepository.movebank.org/server/api/core/bitstreams/secret/content",
        "https://www.movebank.org/movebank/service/direct-read?entity_type=event",
        "http://doi.org/10.5441/001/1.271",
    ]:
        with pytest.raises(ValueError):
            s.check_pinned_url(bad,allowed)
    s.check_pinned_url("https://doi.org/10.5441/001/1.271",allowed)


def test_head_never_reads_body_or_follows_redirect():
    opener=FakeOpener()
    url="https://doi.org/10.5441/001/1.271"
    row=s.metadata_head(url,{url},opener)
    assert opener.observed==(url,"HEAD")
    assert opener.response.closed
    assert row["status"]=="REDIRECT_ONLY"
    assert row["redirect_hostname"]=="new-archive.example"
    assert row["no_response_body_read"] is True
    assert row["tracking_or_event_bytes_downloaded"] is False


def test_source_cohorts_three_and_no_raw_downloads(monkeypatch):
    c={"date":"2026-11-24","2023_archives":[
        {"cohort":"control","doi":"10.5441/001/1.271",
         "landing":"https://datarepository.movebank.org/handle/10255/move.1627",
         "cc0_metadata_verified":True},
        {"cohort":"delayed","doi":"10.5441/001/1.276",
         "landing":"https://datarepository.movebank.org/handle/10255/move.1632",
         "cc0_metadata_verified":True},
        {"cohort":"naturally_timed","doi":"10.5441/001/1.277",
         "landing":"https://datarepository.movebank.org/handle/10255/move.1633",
         "cc0_metadata_verified":True},
    ]}
    def fake_head(url,allowed,opener=None):
        assert url in allowed
        return {"status":"REDIRECT_ONLY","tracking_or_event_bytes_downloaded":False}
    monkeypatch.setattr(s,"metadata_head",fake_head)
    result=s.audit(c)
    assert len(result["archive_status"])==3
    assert result["events_or_tracking_files_downloaded"] is False
    assert result["social_cue_reliability_or_remain_recourse_estimated"] is False
    assert result["status"]=="ARCHIVE_EVENT_DOWNLOAD_NOT_VERIFIED"
