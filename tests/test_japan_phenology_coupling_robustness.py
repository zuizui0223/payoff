import pytest
from src.japan_phenology_coupling_robustness import station_balanced_coupling

def fixture():
    rows=[]
    for station, sign in [("401",1),("402",-1)]:
        for year in range(2000,2012):
            for taxon,src,value in [
                ("bird","bird.csv",100+year-2000),
                ("plant_or_unclassified","plant.csv",120+sign*(year-2000)),
            ]:
                rows.append({"station_id":station,"source_file":src,
                             "source_taxon_guess":taxon,"year":year,"day_of_year":value})
    return rows

def test_balanced_stations_not_event_year_pseudoreplicates():
    r=station_balanced_coupling(fixture(),"bird","plant_or_unclassified")
    assert r["stations_with_pairs"]==2
    assert r["event_pairs_used_not_independent"]==2
    assert r["mean_station_equal_weight_r"]==0
    assert r["fraction_stations_positive_r"]==0.5
    assert r["statistical_significance_estimated"] is False

def test_min_shared_years():
    r=station_balanced_coupling(fixture()[:6],"bird","plant_or_unclassified")
    assert r["status"]=="NO_ADMISSIBLE_PAIRS"

def test_duplicate_rejected():
    x=fixture()
    x.append(dict(x[0]))
    with pytest.raises(ValueError,match="Duplicate"):
        station_balanced_coupling(x,"bird","plant_or_unclassified")
