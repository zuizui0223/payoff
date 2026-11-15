"""Fixed-composition year-to-year cross-taxon event lag panel.

Keep exactly the same station and original event pair throughout each
predeclared period; remove panel composition drift as an explanation for
annual national lag changes. No climate or resource inference.
"""
from collections import defaultdict
from statistics import mean
from src.japan_phenology_rm_sensitivity import leap_normalize
from src.japan_phenology_event_definition_audit import stage_from_label

CONTRASTS=(("bird_plant","bird","plant"),
           ("insect_plant","insect","plant"),
           ("bird_insect","bird","insect"))
WINDOWS=((1961,1980),(1981,2000),(2001,2020))

def fixed_panel_interannual(events, *, min_stations=5):
    events, leap_excluded=leap_normalize(events)
    series=defaultdict(dict)
    for r in events:
        group=r["source_taxon_guess"]
        stage=stage_from_label(r["event_label"])
        if (group,stage) not in {("bird","first_sighting"),
                                ("insect","first_sighting"),
                                ("plant","flowering")}:
            continue
        key=(r["station_id"],r["source_file"],group)
        year=int(r["year"])
        if year in series[key]:
            raise ValueError("Duplicate station-event-year")
        series[key][year]=int(r["day_of_year"])
    station_groups=defaultdict(lambda:defaultdict(list))
    for (station,file,group),ys in series.items():
        station_groups[station][group].append((file,ys))
    results=[]
    for start,end in WINDOWS:
        years=list(range(start,end+1))
        for name,ga,gb in CONTRASTS:
            per_station=defaultdict(list)
            pair_count=0
            for station,groups in station_groups.items():
                for fa,ya in groups[ga]:
                    for fb,yb in groups[gb]:
                        if not all(y in ya and y in yb for y in years):
                            continue
                        lag=[ya[y]-yb[y] for y in years]
                        center=mean(lag)
                        pair_count+=1
                        per_station[station].append([v-center for v in lag])
            stations=sorted(per_station)
            annual=[]
            if len(stations)>=min_stations:
                for idx,year in enumerate(years):
                    station_means=[mean(pair[idx] for pair in per_station[station])
                                   for station in stations]
                    annual.append({"year":year,"stations":len(stations),
                                   "station_equal_mean_lag_anomaly_days":round(mean(station_means),4),
                                   "fraction_stations_positive":round(sum(v>0 for v in station_means)/len(stations),4),
                                   "station_mean_abs_lag_anomaly_days":round(mean(abs(v) for v in station_means),4)})
            results.append({"window":[start,end],"contrast":name,
                            "fixed_station_count":len(stations),
                            "fixed_source_event_pair_count":pair_count,
                            "coverage_passed":len(stations)>=min_stations,
                            "annual":annual})
    return {"status":"FIXED_STATION_EVENT_PAIR_20_YEAR_PANELS_OBSERVED_TIMING_ONLY",
            "windows":[list(w) for w in WINDOWS],
            "leap_days_excluded":leap_excluded,
            "phenology_quality_codes_certified":False,
            "climate_resource_mismatch_effect_fitted":False,
            "panels":results}
