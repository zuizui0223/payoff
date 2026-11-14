import datetime as dt
import pytest
from src.japan_phenology_jma_multivariate import build_pre_event_features, MeteorologyNotAdmitted

def data():
    return [{"date": (dt.date(2020, 4, 1) + dt.timedelta(days=i)).isoformat(),
             "station_metadata_id": "SYNTHETIC", "station_valid_for_date": True,
             "source_id": "SYNTHETIC", "values": {"tmean": 10., "tmin": 1.,
             "precip": 2., "sunshine": 4.}, "quality_flags": {"tmean": "SYNTHETIC",
             "tmin": "SYNTHETIC", "precip": "SYNTHETIC", "sunshine": "SYNTHETIC"}}
            for i in range(30)]

def test_multivariate_features_not_promoted_without_qa_certification():
    result = build_pre_event_features(data(), "2020-05-01")
    assert result["features"]["gdd_5.0"] == 150
    assert result["features"]["precip_total"] == 60
    assert result["features"]["rain_days_ge1mm"] == 30
    assert result["features"]["sunshine_mean"] == 4
    assert result["ready_for_model"] is False
    assert result["quality_codes_certified"] is False

@pytest.mark.parametrize("change", [
    lambda x: x[0].update(date="2020-05-01"),
    lambda x: x[0].update(station_valid_for_date=False),
    lambda x: x[0].update(source_id=""),
    lambda x: x[0]["values"].update(precip=-1),
    lambda x: x[0]["values"].update(sunshine=30),
    lambda x: x[0]["values"].update(relative_humidity=150),
    lambda x: x[0]["values"].update(wrongfield=1),
    lambda x: x[0]["quality_flags"].pop("precip"),
])
def test_weather_source_fail_closed(change):
    x = data()
    change(x)
    with pytest.raises(MeteorologyNotAdmitted):
        build_pre_event_features(x, "2020-05-01")

def test_missingness_is_variable_specific():
    x = data()
    for r in x[:4]:
        r["values"]["precip"] = None
    result = build_pre_event_features(x, "2020-05-01")
    assert "precip_total" not in result["features"]
    assert "tmean_mean" in result["features"]
