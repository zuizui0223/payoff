"""Synthetic format/HTTP tests: no source data or novel effect simulated."""
import io
import json
import zipfile

import pytest
pytest.importorskip("requests")

from scripts.payoff_b_ruppel_figshare_source_gate import (
    _provider_download_url, _delimited_schema, _tabular_candidates,
    inspect_public_source, MAX_PUBLIC_BYTES, _zip_public_member_manifest,
)


def test_only_provider_bounded_file_paths_authorized():
    assert _provider_download_url("https://figshare.com/ndownloader/files/1234567")
    assert _provider_download_url("https://ndownloader.figshare.com/files/1234567")
    assert not _provider_download_url("http://figshare.com/ndownloader/files/123")
    assert not _provider_download_url("https://not-figshare.net/files/1234567")
    assert not _provider_download_url("https://api.figshare.com/v2/accounts/private")
    assert MAX_PUBLIC_BYTES==8_000_000


def test_plain_source_schema_is_not_claimed_a_linked_decision():
    raw=("bird_id,Date,depart_event,routing_choice,landing,wind_mps\n"
         "bird-a,2023-04-10,1,coast,0,5.0\n"
         "bird-b,2023-04-11,1,offshore,1,2.0\n").encode()
    z=_delimited_schema(raw,"synthetic.csv")
    assert z["n_original_rows"]==2
    assert z["aggregate_candidate_id_counts"]["bird_id"]["n_unique"]==2
    assert "Date" in z["candidate_time_columns"]
    assert "landing" in z["candidate_decision_columns"]
    assert "wind_mps" in z["candidate_weather_columns"]
    assert z["original_same_bird_all_three_decisions_certified"] is False
    assert "bird-a" not in str(z)


def test_original_zip_bounded_small_csv_can_be_inspected_without_raw_export():
    raw=("tag_id\tsunset_time\tdepart_event\twind\n"
         "A\t2023-04-09T19:30\t0\t2.4\n"
         "A\t2023-04-10T19:30\t1\t3.5\n").encode()
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,"w") as z:
        z.writestr("data/events.tsv",raw)
    out=_tabular_candidates(mem.getvalue(),"original.zip")
    assert len(out)==1
    assert out[0]["n_original_rows"]==2
    assert "tag_id" in out[0]["candidate_id_columns"]
    assert "A\t" not in str(out)


class _Response:
    def __init__(self,obj,status=200):
        self.status_code=status
        if isinstance(obj,bytes):
            self.raw=obj
        else:
            self.raw=json.dumps(obj).encode()
        self.headers={"Content-Length":str(len(self.raw))}
    def iter_content(self,n):
        yield self.raw
    def close(self):pass


class _FakePublicSession:
    def get(self,url,**kwargs):
        if url.endswith("/collections/6403996/articles"):
            return _Response([{"id":201,"title":"Original Rüppel supplemental item"}])
        if url.endswith("/articles/201"):
            return _Response({
                "id":201,"doi":"10.6084/m9.figshare.201",
                "title":"Original data","published_date":"2023-01-27",
                "files":[{"id":11,"name":"source_events.csv",
                           "size":63,
                           "download_url":"https://ndownloader.figshare.com/files/11"}]
            })
        if url.endswith("/files/11"):
            return _Response(b"bird_id,Date,departure,wind\nA,2023-04-10,1,3.2\n")
        return _Response({},status=404)


def test_mock_original_source_data_grain_stays_unverified():
    result=inspect_public_source(_FakePublicSession())
    assert result["source_status"]=="ORIGINAL_TABULAR_SCHEMA_FOUND_ID_JOIN_UNVERIFIED"
    assert result["n_original_linked_article_records"]==1
    assert result["n_original_tabular_tables"]==1
    assert result["new_biological_response_fitted"] is False
    assert result["source_assessment"]["matching_individual_ids_across_all_three_decisions"] is False
    assert "A,2023" not in str(result)


class _BlockedSession:
    def get(self,url,**kwargs):
        return _Response(b"forbidden",status=403)


def test_public_api_denial_is_not_a_biological_negative():
    result=inspect_public_source(_BlockedSession())
    assert result["source_status"]=="SOURCE_METADATA_ACCESS_BLOCKED"
    assert "403" in result["source_hold_reason"]
    assert result["natural_q_wait_D_eff_and_r_t_identified"] is False


def test_original_zip_member_inventory_keeps_binary_R_data_distinct_from_no_data():
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,"w") as z:
        z.writestr("analysis.R",b"# source analysis code, not a bird table")
        z.writestr("original_derived_data.rds",b"fake binary test fixture")
        z.writestr("manuscript_SI.pdf",b"not opened or parsed")
    got=_zip_public_member_manifest(mem.getvalue())
    assert len(got)==3
    assert {x["source_zip_member_suffix"] for x in got}=={".r",".rds",".pdf"}
    assert all(x["original_data_bytes_or_row_values_exported"] is False for x in got)
    assert _tabular_candidates(mem.getvalue(),"source.zip")==[]
