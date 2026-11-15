"""Interannual synchrony of cross-taxon timing mismatch in original JMA observations.

Define mismatch anomaly as annual event-date difference minus each
station/event-pair's long-run mean. This is NOT resource mismatch or fitness.
Aggregate to one mean per station-year before national year statistics.
"""
from __future__ import annotations
from collections import defaultdict
from statistics import mean,median
from src.japan_phenology_rm_sensitivity import leap_normalize
from src.japan_phenology_event_definition_audit import stage_from_label

def interannual_mismatch(events, *, min_pair_years=10, min_stations_per_year=10,
                         year_min=1961, year_max=2020):
    events, leap_excluded=leap_normalize(events)
    by_series=defaultdict(dict)
    for r in events:
        year=int(r["year"])
        if not year_min<=year<=year_max:continue
        group=r["source_taxon_guess"]
        stage=stage_from_label(r["event_label"])
        if (group,stage) not in {("bird","first_sighting"),("insect","first_sighting"),
                                ("plant","flowering")}:
            continue
        key=(r["station_id"],r["source_file"],group,stage)
        if year in by_series[key]:raise ValueError("Duplicate event-year")
        by_series[key][year]=int(r["day_of_year"])
    by_station=defaultdict(lambda: {"bird":[],"insect":[],"plant":[]})
    for (station,source,group,stage),years in by_series.items():
        by_station[station][group].append((source,years))
    output={}
    for name,a,b in (("bird_plant","bird","plant"),("insect_plant","insect","plant"),
                     ("bird_insect","bird","insect")):
        station_year=defaultdict(list)
        n_pairs=0
        for station,groups in by_station.items():
            for sa,ya in groups[a]:
                for sb,yb in groups[b]:
                    common=sorted(set(ya)&set(yb))
                    if len(common)<min_pair_years:continue
                    # The mean raw lag is source-specific. Subtract it to avoid
                    # mixing species' different expected seasonal dates.
                    lag={year:ya[year]-yb[year] for year in common}
                    baseline=mean(lag.values())
                    n_pairs+=1
                    for year in common:
                        station_year[(station,year)].append(lag[year]-baseline)
        year_values=defaultdict(list)
        for (station,year),lags in station_year.items():
            year_values[year].append(mean(lags))
        annual=[]
        for year in sorted(year_values):
            vals=year_values[year]
            if len(vals)<min_stations_per_year:continue
            annual.append({"year":year,"stations":len(vals),
                           "station_equal_mean_mismatch_anomaly_days":round(mean(vals),3),
                           "station_median_mismatch_anomaly_days":round(median(vals),3),
                           "fraction_stations_positive_mismatch_anomaly":round(sum(x>0 for x in vals)/len(vals),4),
                           "mean_absolute_station_mismatch_anomaly_days":round(mean(abs(x) for x in vals),3)})
        output[name]={"eligible_event_pairs":n_pairs,"annual":annual,
                      "years_with_min_station_coverage":len(annual)}
    return {"status":"OBSERVED_EVENT_LAG_ANOMALY_ONLY_NOT_FOOD_OR_FITNESS_MISMATCH",
            "reference_year_range":[year_min,year_max],
            "min_pair_overlap_years":min_pair_years,
            "min_stations_per_year":min_stations_per_year,
            "leap_day_records_excluded":leap_excluded,
            "phenology_rm_quality_certified":False,
            "weather_climate_ndvi_biomass_fitted":False,
            "annual_contrasts":output}
