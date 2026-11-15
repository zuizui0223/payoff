import pytest
from src.japan_phenology_jma_daily_import import admit_normalized_daily_export, JmaDailySourceError

def sample():
    return "date,Tmean,quality_Tmean,Precip,quality_Precip\n2020-04-01,12.0,8,3.0,8\n2020-04-02,13.0,9,4.0,8\n"

def ingest(raw=None):
    return admit_normalized_daily_export(raw or sample(),station_metadata_id="SYNTHETIC",
        source_id="SYNTHETIC_TEST",variable_columns={"tmean":"Tmean","precip":"Precip"},
        quality_columns={"tmean":"quality_Tmean","precip":"quality_Precip"},
        allowed_quality_codes={"tmean":{"8"},"precip":{"8"}})

def test_source_quality_is_not_guessed():
    out=ingest()
    assert out["daily_rows"][0]["values"]["tmean"]==12
    assert out["daily_rows"][1]["values"]["tmean"] is None
    assert out["daily_rows"][1]["values"]["precip"]==4
    assert out["rejected_by_variable"]=={"tmean:unadmitted_flag":1}
    assert out["daily_rows"][0]["station_valid_for_date"] is False
    assert out["no_environmental_effect_fitted"] is True

@pytest.mark.parametrize("raw",[
    "date,Tmean,quality_Tmean,Precip,quality_Precip\n2020-04-01,12,8,3,8\n2020-04-01,12,8,3,8\n",
    "date,Tmean,quality_Tmean,Precip,quality_Precip\nwrong,12,8,3,8\n",
    "date,Tmean,quality_Tmean,Precip,quality_Precip\n2020-04-01,abc,8,3,8\n",
])
def test_bad_source_rejected(raw):
    with pytest.raises(JmaDailySourceError):
        ingest(raw)
