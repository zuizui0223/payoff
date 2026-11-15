import datetime as dt
from src.japan_phenology_fixed_interannual import fixed_panel_interannual

def test_fixed_panel_requires_all_years_and_equal_station_weight():
    rows=[]
    for station in ("401","402","403","404","405"):
        for year in range(1961,1981):
            for source,label,group,doy in (
                ("bird.csv","つばめ初見","bird",90+((year-1961)%4)),
                ("plant.csv","さくら開花","plant",95+((year-1961)%3)),
            ):
                date=dt.date(year,1,1)+dt.timedelta(days=doy-1)
                rows.append({"station_id":station,"source_file":source,
                             "event_label":label,"source_taxon_guess":group,
                             "year":year,"event_date":date.isoformat(),"day_of_year":doy})
    out=fixed_panel_interannual(rows)
    panel=next(p for p in out["panels"] if p["window"]==[1961,1980] and p["contrast"]=="bird_plant")
    assert panel["fixed_station_count"]==5
    assert panel["fixed_source_event_pair_count"]==5
    assert len(panel["annual"])==20
    assert abs(sum(v["station_equal_mean_lag_anomaly_days"] for v in panel["annual"]))<0.001
    assert out["climate_resource_mismatch_effect_fitted"] is False
