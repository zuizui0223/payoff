import pytest
from src.japan_phenology_coupling_robustness import station_balanced_coupling

def fixture():
    rows=[]
    for station, sign in [("401",1),("402",-1)]:
        for year in range(2000,2012):
            for taxon,src,value in [
                ("bird","bird.csv",100+year-2000),
                ("plant","plant.csv",120+sign*(year-2000)),
            ]:
                rows.append({"station_id":station,"source_file":src,
                             "source_taxon_guess":taxon,"year":year,"day_of_year":value})
    return rows

def test_balanced_stations_not_event_year_pseudoreplicates():
    r=station_balanced_coupling(fixture(),"bird","plant")
    assert r["stations_with_pairs"]==2
    assert r["event_pairs_used_not_independent"]==2
    assert r["mean_station_equal_weight_r"]==0
    assert r["fraction_stations_positive_r"]==0.5
    assert r["statistical_significance_estimated"] is False

def test_min_shared_years():
    r=station_balanced_coupling(fixture()[:6],"bird","plant")
    assert r["status"]=="NO_ADMISSIBLE_PAIRS"

def test_duplicate_rejected():
    x=fixture()
    x.append(dict(x[0]))
    with pytest.raises(ValueError,match="Duplicate"):
        station_balanced_coupling(x,"bird","plant")


def test_bootstrap_reproducible_with_ten_independent_station_units():
    rows=[]
    for station in range(10):
        for year in range(2000,2012):
            for group,source,value in (
                ("bird","bird.csv",100+(year-2000)),
                ("plant","plant.csv",110+(year-2000)*(1 if station<8 else -1)),
            ):
                rows.append({"station_id":str(station),"source_file":source,
                             "source_taxon_guess":group,"year":year,"day_of_year":value})
    a=station_balanced_coupling(rows,"bird","plant",bootstrap_reps=200)
    b=station_balanced_coupling(rows,"bird","plant",bootstrap_reps=200)
    assert a["station_resample_percentile_95_interval"]==b["station_resample_percentile_95_interval"]
    assert a["station_resample_percentile_95_interval"][0]<=a["mean_station_equal_weight_r"]<=a["station_resample_percentile_95_interval"][1]
    assert a["interval_is_not_causal_or_quality_adjusted"] is True
