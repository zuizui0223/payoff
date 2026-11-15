import pytest
from scripts.payoff_b_monisen_overlap_preflight import (
    read_channel_csv, overlap_preflight, OverlapNotAdmitted)

def test_original_source_receipts_and_overlap(tmp_path):
    a=tmp_path/"flower.csv";b=tmp_path/"temperature.csv"
    a.write_text("site,year,stage\nA,2020,flower\nA,2021,flower\nA,2022,flower\nB,2020,flower\n",encoding="utf-8")
    b.write_text("site,year,temp\nA,2020,10\nA,2021,11\nA,2022,12\nB,2021,9\n",encoding="utf-8")
    x=read_channel_csv(a,site_column="site",year_column="year",source_id="flower")
    y=read_channel_csv(b,site_column="site",year_column="year",source_id="temp")
    result=overlap_preflight({"flower":x,"temp":y})
    assert result["matched_site_years"]==3
    assert result["sites_with_minimum_years"]==1
    assert result["eligible_site_years"]=={"A":[2020,2021,2022]}
    assert result["site_id_crosswalk_verified"] is False
    assert result["weather_biomass_effect_fitted"] is False
    assert len(x["sha256"])==64

def test_reject_missing_schema_and_no_valid_records(tmp_path):
    p=tmp_path/"a.csv"
    p.write_text("name,date\nA,2020\n",encoding="utf-8")
    with pytest.raises(OverlapNotAdmitted):
        read_channel_csv(p,site_column="site",year_column="year",source_id="a")
    p.write_text("site,year\nA,unknown\n",encoding="utf-8")
    with pytest.raises(OverlapNotAdmitted):
        read_channel_csv(p,site_column="site",year_column="year",source_id="a")
