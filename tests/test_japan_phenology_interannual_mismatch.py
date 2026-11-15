from src.japan_phenology_interannual_mismatch import interannual_mismatch
import datetime as dt

def test_annual_lag_anomaly_tracks_shift_and_not_absolute_stage_gap():
    events=[]
    for year in range(2000,2012):
        for station in ("401","402"):
            for source,label,group,doy in (
                ("bird.csv","つばめ初見","bird",90+(year-2000)),
                ("plant.csv","さくら開花","plant",100+2*(year-2000)),
            ):
                date=dt.date(year,1,1)+dt.timedelta(days=doy-1)
                events.append({"source_file":source,"event_label":label,
                    "source_taxon_guess":group,"station_id":station,
                    "year":year,"day_of_year":doy,"event_date":date.isoformat()})
    out=interannual_mismatch(events,min_stations_per_year=2,year_min=2000,year_max=2011)
    annual=out["annual_contrasts"]["bird_plant"]["annual"]
    assert len(annual)==12
    assert annual[0]["station_equal_mean_mismatch_anomaly_days"]>0
    assert annual[-1]["station_equal_mean_mismatch_anomaly_days"]<0
    assert all(x["stations"]==2 for x in annual)
    assert out["weather_climate_ndvi_biomass_fitted"] is False

def test_insufficient_station_years_not_promoted():
    out=interannual_mismatch([],min_stations_per_year=10)
    assert out["annual_contrasts"]["bird_plant"]["years_with_min_station_coverage"]==0
