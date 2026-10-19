import csv
from pathlib import Path
import pytest
from scripts.qc_public_movebank_crossguild import SOURCES,audit

def test_original_sources_frozen():
    assert len(SOURCES)==3
    assert len({s["taxon"] for s in SOURCES.values()})==3
    for s in SOURCES.values():
        assert len(s["md5"])==32 and len(s["uuid"])==36 and s["size"]>1e6
def test_synthetic_track_coverage_without_id_output(tmp_path:Path):
    path=tmp_path/"mock.csv"
    head=["timestamp","individual-local-identifier","location-lat",
          "location-long","sensor-type"]
    rows=[]
    for year in [2017,2018]:
        for mon in [1,4,10]:
            for day in range(1,13):
                rows.append(dict(timestamp=f"{year}-{mon:02d}-{day:02d} 10:00:00",
                                 **{"individual-local-identifier":"secret",
                                    "location-lat":"52.0","location-long":"12.0",
                                    "sensor-type":"GPS"}))
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=head);w.writeheader();w.writerows(rows)
    x=audit(path)
    assert x["valid_identified_georeferenced_fixes"]==72
    assert x["labels_observed_in_multiple_years"]==1
    assert x["same_year_spring_and_autumn"]==2
    assert x["same_year_spring_and_winter"]==2
    assert not x["actual_route_stage_or_stopover"]
    assert "secret" not in str(x)
def test_missing_columns_fails(tmp_path:Path):
    path=tmp_path/"bad.csv"
    path.write_text("timestamp,individual-local-identifier\n2020-01-01,secret\n")
    with pytest.raises(ValueError,match="missing fields"):audit(path)
def test_invalid_fixes_not_counted(tmp_path:Path):
    path=tmp_path/"bad.csv"
    path.write_text("timestamp,tag-local-identifier,location-lat,location-long\n"
                    "2020-03-01 12:00:00,t1,35,10\n"
                    "bad,t1,35,10\n"
                    "2020-03-02 12:00:00,t1,500,10\n"
                    "2020-03-02 12:00:00,,35,10\n")
    x=audit(path)
    assert x["valid_identified_georeferenced_fixes"]==1
    assert x["invalid_timestamp_rows"]==1 and x["invalid_position_rows"]==1
    assert x["missing_identity_rows"]==1
    assert not x["id_is_animal_not_tag"]
