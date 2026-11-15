from src.japan_phenology_fixed_cross_contrast import fixed_panel_cross_contrast_synchrony

def test_same_year_comparisons_are_descriptive_only():
    panels=[]
    for name,mult in [("bird_plant",1),("insect_plant",2),("bird_insect",-1)]:
        panels.append({"window":[2001,2020],"contrast":name,"coverage_passed":True,
            "annual":[{"year":y,"station_equal_mean_lag_anomaly_days":mult*(y-2010.5)} for y in range(2001,2021)]})
    out=fixed_panel_cross_contrast_synchrony({"windows":[[2001,2020]],"panels":panels})
    assert out["n_comparisons"]==3
    pair=next(x for x in out["comparisons"] if x["contrast_a"]=="bird_plant" and x["contrast_b"]=="insect_plant")
    assert pair["annual_mean_lag_anomaly_pearson_r"]==1
    assert pair["same_sign_fraction"]==1
    assert pair["shared_source_event_dates_not_independent"] is True
    assert out["no_weather_ndvi_biomass_fit"] is True
