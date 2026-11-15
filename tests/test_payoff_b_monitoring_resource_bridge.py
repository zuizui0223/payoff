import copy
import pytest
from src.payoff_b_monitoring_resource_bridge import validate_site_year_bundle, EvidenceNotAdmitted

def valid():
    common={"site_id":"A","year":2020,"source_id":"independent"}
    return {"site_id":"A","year":2020,
        "monitoring":{**common,"quantity_kind":"abundance_index",
                      "effort_standardized":True,"observation_process_verified":True},
        "climate":{**common,"station_crosswalk_verified":True,
                   "quality_homogeneity_verified":True,"window_fixed_before_outcome":True,
                   "climate_variables":{"tmean":11.5}},
        "resource":{**common,"quantity_kind":"biomass_g_m2",
                    "independent_from_outcome":True,"sampling_effort_verified":True,
                    "mass_basis":"dry","resource_guild":"caterpillars",
                    "daily_series":[{"date":"2020-04-01","biomass_g_m2":2},
                                    {"date":"2020-04-02","biomass_g_m2":6}]},
        "consumer":{**common,"demand_curve_source_verified":True,
                    "daily_demand":[{"date":"2020-04-01","weight":1},
                                    {"date":"2020-04-02","weight":3}]}}

def test_valid_independent_resource_exposure():
    result=validate_site_year_bundle(valid())
    assert result["demand_weighted_resource_biomass_g_m2"]==5
    assert result["outcome_effect_estimated"] is False

@pytest.mark.parametrize("channel,key,value",[
    ("resource","quantity_kind","NDVI"),
    ("resource","independent_from_outcome",False),
    ("monitoring","effort_standardized",False),
    ("monitoring","observation_process_verified",False),
    ("climate","station_crosswalk_verified",False),
    ("climate","quality_homogeneity_verified",False),
    ("climate","window_fixed_before_outcome",False),
    ("consumer","demand_curve_source_verified",False),
])
def test_unverified_channel_rejected(channel,key,value):
    b=valid()
    b[channel][key]=value
    with pytest.raises(EvidenceNotAdmitted):validate_site_year_bundle(b)

def test_mismatched_site_year_and_missing_resource_day_rejected():
    b=valid();b["monitoring"]["year"]=2019
    with pytest.raises(EvidenceNotAdmitted):validate_site_year_bundle(b)
    b=valid();b["resource"]["daily_series"].pop()
    with pytest.raises(EvidenceNotAdmitted):validate_site_year_bundle(b)
