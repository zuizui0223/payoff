"""Pure synthetic source-grain tests: no real GPS event downloaded or emitted."""
from datetime import date
from hashlib import md5
import io
import json
from pathlib import Path
import zipfile

import pytest
from scripts import payoff_b_stork_original_gps_date_coverage_20261124 as g

HEADER=[
 "event-id","visible","timestamp","location-long","location-lat",
 "tag-local-identifier","individual-local-identifier","sensor-type"
]


def make_csv(rows):
    import csv
    out=io.StringIO()
    writer=csv.writer(out)
    writer.writerow(HEADER)
    writer.writerows(rows)
    return out.getvalue().encode()


def test_UTC_time_is_parsed_without_post_outcome_temperature_or_decision():
    assert g.parse_event_date("2020-09-01 23:59:59.000",date(2026,11,24))==(date(2020,9,1),"OK")
    assert g.parse_event_date("2020-09-01T23:30:00-02:00",date(2026,11,24))==(date(2020,9,2),"OK")
    assert g.parse_event_date("2030-01-01 12:00:00",date(2026,11,24))[1]=="FUTURE_TIME"
    assert g.parse_event_date("NA",date(2026,11,24))[1]=="MISSING_TIME"
    assert g.parse_event_date("2020/09/01",date(2026,11,24))[1]=="UNPARSEABLE_TIME"


def test_original_GPS_rows_only_aggregate_by_day_and_year():
    raw=make_csv([
        ["1","true","2020-09-01 12:00:00","8.1","47.7","PRIVATE_TAG_A","PRIVATE_ANIMAL_A","GPS"],
        ["2","true","2020-09-01 12:01:00","8.1","47.7","PRIVATE_TAG_B","PRIVATE_ANIMAL_B","GPS"],
        ["3","true","2020-09-01 12:04:00","8.2","47.8","PRIVATE_TAG_A","PRIVATE_ANIMAL_A","GPS"],
        ["4","false","2020-09-02 00:00:00","8.3","47.9","PRIVATE_TAG_A","PRIVATE_ANIMAL_A","GPS"],
        ["5","true","bad-date","8.2","47.8","PRIVATE_TAG_C","PRIVATE_ANIMAL_C","GPS"],
        ["6","true","2020-09-02 00:10:00","200","47.8","PRIVATE_TAG_C","PRIVATE_ANIMAL_C","GPS"],
        ["7","true","2020-09-02 00:11:00","8.2","47.8","","PRIVATE_ANIMAL_C","GPS"],
    ])
    z=g.stream_csv_support(io.StringIO(raw.decode()),HEADER,date(2026,11,24),"control")
    assert z["n_original_main_member_GPS_CSV_rows"]==7
    assert z["n_valid_georeferenced_event_rows"]==4
    assert z["n_unusable_timestamp_rows"]==1
    assert z["n_unusable_coordinate_rows"]==1
    assert z["n_unusable_tag_rows"]==1
    assert z["n_distinct_UTC_dates_with_valid_events"]==2
    assert z["n_UTC_dates_with_at_least_two_distinct_tag_strings"]==1
    assert z["daily_aggregate_only"]==[
       {"UTC_date":"2020-09-01","n_valid_georeferenced_event_rows":3,"n_distinct_observed_tag_strings":2},
       {"UTC_date":"2020-09-02","n_valid_georeferenced_event_rows":1,"n_distinct_observed_tag_strings":1},
    ]
    assert z["yearly_aggregate"][0]["n_distinct_observed_tag_strings"]==2
    assert z["yearly_aggregate"][0]["n_distinct_observed_animal_strings"]==2
    assert z["raw_identifiers_geolocation_or_event_timestamps_exported"] is False
    assert z["no_actual_same_place_same_time_evidence_claimed"] is True
    for secret in ("PRIVATE_TAG_A","PRIVATE_ANIMAL_B","47.7","47.8","8.1","12:00"):
        assert secret not in json.dumps(z)


def test_bad_header_rejected_before_outcome_or_event_values():
    with pytest.raises(ValueError,match="header differs"):
        g.stream_csv_support(io.StringIO("event-id,lat\n1,10\n"),
                             HEADER,date(2026,11,24),"control")


def test_exact_selected_main_zip_member_gate_rejects_changed_source_size(tmp_path):
    archive=tmp_path/"synthetic.zip"
    src=make_csv([
        ["1","true","2020-01-01 12:00:00","8.1","47.7","PRIVATE_A","PRIVATE_B","GPS"]
    ])
    with zipfile.ZipFile(archive,"w") as z:
        z.writestr("private_fake_gps.csv",src)
        z.writestr("tiny.csv","")
    with zipfile.ZipFile(archive,"r") as z:
        info=g.choose_main_member(z,"control",{"source_origins":{
          "control":{"main_member_uncompressed_bytes":len(src)}
        }})
        assert info.file_size==len(src)
        with pytest.raises(ValueError,match="exactly one"):
            g.choose_main_member(z,"control",{"source_origins":{
              "control":{"main_member_uncompressed_bytes":len(src)+1}
            }})


class FakeDownload:
    def __init__(self,payload,source_url,status=200):
        self.payload=payload
        self.source_url=source_url
        self.status=status
        self.pos=0
        self.headers={"Content-Length":str(len(payload)),"Content-Type":"application/zip"}
    def __enter__(self):return self
    def __exit__(self,*a):return False
    def geturl(self):return self.source_url
    def read(self,n):
        part=self.payload[self.pos:self.pos+n];self.pos+=len(part)
        return part

class FakeOpener:
    def __init__(self,payload,url,status=200):
        self.payload=payload;self.url=url;self.status=status
    def open(self,req,timeout):
        return FakeDownload(self.payload,self.url,self.status)


def test_full_source_file_hash_and_declared_size_required(tmp_path):
    url="https://datarepository.movebank.org/server/api/core/bitstreams/abcd/content"
    raw=b"PK\x03\x04small fake ZIP bytes"
    out=tmp_path/"small.zip"
    z=g.download_original_zip(url,len(raw),md5(raw).hexdigest(),out,
                              opener=FakeOpener(raw,url))
    assert z["full_original_zip_md5_source_verified"] is True
    assert out.read_bytes()==raw
    with pytest.raises(ValueError,match="MD5"):
        g.download_original_zip(url,len(raw),"0"*32,out,opener=FakeOpener(raw,url))
    with pytest.raises(ValueError,match="HTTP 200"):
        g.download_original_zip(url,len(raw),md5(raw).hexdigest(),out,
                                opener=FakeOpener(raw,url,status=206))


def test_false_claim_about_GPS_total_study_prevented_by_contract():
    import json
    c=json.loads(g.DEFAULT_CONTRACT.read_text())
    assert c["source_origins"]["control"]["size_bytes"]==289189615
    assert c["source_origins"]["delayed"]["size_bytes"]==297340370
    assert c["source_origins"]["naturally_timed"]["size_bytes"]==311814202
    assert c["no_ebird"] is not False if "no_ebird" in c else c["source_fidelity"]["no_ebird"]
    assert "smallest" in c["zip_selection"].lower()
