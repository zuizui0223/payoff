import pytest
from src.japan_phenology_cross_taxon import paired_station_year_anomaly_correlation

def fixture():
    result=[]
    for year in range(2000,2010):
        for group,source,day in (("bird","bird.csv",100+year-2000),
                                 ("plant","plant.csv",110+year-2000),
                                 ("amphibian","frog.csv",95-(year-2000))):
            result.append({"source_taxon_guess":group,"source_file":source,
                           "station_id":"401","year":year,"day_of_year":day})
    return result

def test_perfect_positive_cross_taxon_coupling():
    r=paired_station_year_anomaly_correlation(fixture(),group_a="bird",group_b="plant")
    assert r["pooled_anomaly_pearson_r"]==1
    assert r["station_count"]==1
    assert r["paired_station_year_cells_not_independent"]==10
    assert r["fitness_or_biomass_effect_identified"] is False

def test_negative_cross_taxon_coupling():
    r=paired_station_year_anomaly_correlation(fixture(),group_a="amphibian",group_b="bird")
    assert r["pooled_anomaly_pearson_r"]==-1

def test_insufficient_shared_years():
    r=paired_station_year_anomaly_correlation(fixture(),group_a="bird",group_b="insect")
    assert r["status"]=="INSUFFICIENT_SHARED_STATION_YEARS"

def test_duplicate_year_rejected():
    rows=fixture()
    rows.append(dict(rows[0]))
    with pytest.raises(ValueError,match="Duplicate"):
        paired_station_year_anomaly_correlation(rows,group_a="bird",group_b="plant")
