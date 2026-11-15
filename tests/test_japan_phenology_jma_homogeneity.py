from src.japan_phenology_jma_homogeneity import audit_homogeneity_regimes

def records(regimes):
    return [{"date":f"2020-04-{i+1:02d}","station_metadata_id":"401",
             "station_valid_for_date":True,"values":{"tmean":10},
             "homogeneity_numbers":{"tmean":v}} for i,v in enumerate(regimes)]

def test_one_regime_is_eligible():
    x=audit_homogeneity_regimes(records(["1"]*30),variable="tmean")
    assert x["status"]=="ADMITTED_ONE_REGIME"
    assert x["ready_for_unstratified_time_series"] is True

def test_multi_regime_blocks_unstratified_trend():
    x=audit_homogeneity_regimes(records(["1"]*15+["2"]*15),variable="tmean")
    assert x["status"]=="MULTIPLE_REGIMES_REQUIRE_STRATIFICATION"
    assert x["ready_for_unstratified_time_series"] is False

def test_missing_homogeneity_fails_closed():
    x=audit_homogeneity_regimes(records([None]*30),variable="tmean")
    assert x["status"]=="INSUFFICIENT_SINGLE_REGIME"
    assert x["rejected_day_counts"]["homogeneity_number_missing"]==30
