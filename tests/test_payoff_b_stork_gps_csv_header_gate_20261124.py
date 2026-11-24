"""Use only ZIP member first CSV header line, not original bird event rows."""
from pathlib import Path
import io
import zipfile
import pytest

from scripts import payoff_b_stork_gps_csv_header_gate_20261124 as s


def archive():
    out=io.BytesIO()
    with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("PRIVATE_BIRD_TAG_999.csv",
           "timestamp,tag-local-identifier,individual-local-identifier,location-lat,location-long\n"
           "2020-09-01 12:00:00,PRIVATE_TAG_999,PRIVATE_BIRD_999,50.0,8.0\n")
    return out.getvalue()


class FakeResp:
    def __init__(self,data,status=206,rng=""):
        self.data=data;self.status=status
        self.headers={"Content-Range":rng}
        self.read_called=False
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def geturl(self):return "https://datarepository.movebank.org/server/api/core/bitstreams/fixed/content"
    def read(self,n):
        self.read_called=True
        return self.data[:n]

class FakeOpener:
    def __init__(self,data,status=206):
        self.data=data;self.status=status
        self.calls=0
    def open(self,req,timeout):
        self.calls+=1
        header=req.get_header("Range")
        assert header.startswith("bytes=")
        pos=header[len("bytes="):]
        start,end=(int(x) for x in pos.split("-"))
        data=self.data[start:end+1]
        return FakeResp(data,self.status,f"bytes {start}-{end}/{len(self.data)}")

def contract():
    return {"transport":{
      "max_original_request_bytes":65557,
      "max_total_compressed_zip_bytes_read_per_cohort":200000,
      "max_http_range_calls_per_cohort":14
    },"metadata_scope":{"max_csv_header_bytes":4096,"max_column_count":120},
    "observed_original_directory":{"control":{"gps_zip_bytes":len(archive()),"members":1,"extension":".csv"}}}


def test_bounded_remote_zip_reads_only_schema_with_no_tracking_rows():
    blob=archive()
    op=FakeOpener(blob)
    url="https://datarepository.movebank.org/server/api/core/bitstreams/fixed/content"
    view=s.BoundedRemoteZipFile(url,len(blob),contract()["transport"],opener=op)
    with zipfile.ZipFile(view,"r") as zipped:
        members=zipped.infolist()
        assert len(members)==1
        columns=s.safe_member_header(zipped,members[0],contract())
    assert columns["status"]=="FIRST_LINE_PUBLIC_CSV_SCHEMA_RECOVERED"
    assert columns["n_csv_columns"]==5
    assert all(columns[x] for x in (
       "has_timestamp","has_tag_identifier","has_individual_identifier",
       "has_latitude","has_longitude"
    ))
    assert columns["source_event_rows_returned"] is False
    assert columns["original_member_name_returned"] is False
    assert "PRIVATE_BIRD_999" not in str(columns)
    assert "2020-09-01" not in str(columns)
    assert view.bytes_used<=200000
    assert op.calls<=14


def test_range_budget_prevents_massive_archive_read():
    blob=archive()
    url="https://datarepository.movebank.org/server/api/core/bitstreams/fixed/content"
    view=s.BoundedRemoteZipFile(url,1000000,contract()["transport"],opener=FakeOpener(blob))
    with pytest.raises(ValueError,match="budget"):
        view.read(65558)
    assert view.bytes_used==0
    assert view.calls==0


def test_server_ignored_range_returns_no_original_row():
    blob=archive()
    url="https://datarepository.movebank.org/server/api/core/bitstreams/fixed/content"
    view=s.BoundedRemoteZipFile(url,len(blob),contract()["transport"],opener=FakeOpener(blob,status=200))
    with pytest.raises(ValueError,match="Range"):
        view.read(20)
    assert view.bytes_used==0
