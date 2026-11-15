"""Independent-reference controls for apparent interannual phenology synchrony.

Compute source-event anomalies directly (not differences with a shared plant
reference), requiring identical station/event series across all years of each
20-year block. For B-P and I-P comparisons, split original plant event files
into disjoint deterministic groups to remove the algebraically shared P term.
"""
from __future__ import annotations
from collections import defaultdict
from statistics import mean
from itertools import combinations
from src.japan_phenology_rm_sensitivity import leap_normalize
from src.japan_phenology_event_definition_audit import stage_from_label
from src.japan_phenology_coupling_robustness import _pearson, _detrend
from src.japan_phenology_fixed_interannual import WINDOWS

def independent_reference_controls(events, *, min_stations=10):
    events, leap_excluded=leap_normalize(events)
    series=defaultdict(dict)
    for row in events:
        group=row["source_taxon_guess"]
        stage=stage_from_label(row["event_label"])
        if (group,stage) not in {("bird","first_sighting"),("insect","first_sighting"),("plant","flowering")}:
            continue
        key=(row["station_id"],row["source_file"],group)
        year=int(row["year"])
        if year in series[key]:
            raise ValueError("Duplicate station/source event/year")
        series[key][year]=int(row["day_of_year"])
    outputs=[]
    for start,end in WINDOWS:
        years=list(range(start,end+1))
        # Keep source files fixed over all 20 years, at each station.
        station_groups=defaultdict(lambda:defaultdict(list))
        for (station,file,group),dates in series.items():
            if all(year in dates for year in years):
                anomaly=[dates[year]-mean(dates[y] for y in years) for year in years]
                station_groups[station][group].append((file,anomaly))
        # Split plant references by source filename; disjoint even if stages
        # share a biological species elsewhere (only flowering is selected).
        plants=sorted({f for gs in station_groups.values() for f,_ in gs["plant"]})
        plant_group={file:("plant_a" if i%2==0 else "plant_b") for i,file in enumerate(plants)}
        station_year={}
        for station,groups in station_groups.items():
            values={}
            for group in ("bird","insect"):
                if groups[group]:
                    values[group]=[mean(series_y[i] for _,series_y in groups[group]) for i in range(len(years))]
            for ref in ("plant_a","plant_b"):
                rows=[v for file,v in groups["plant"] if plant_group[file]==ref]
                if rows:
                    values[ref]=[mean(v[i] for v in rows) for i in range(len(years))]
            station_year[station]=values
        for a,b in (("bird","insect"),("bird","plant_a"),("insect","plant_b"),
                    ("plant_a","plant_b")):
            eligible=sorted(station for station,v in station_year.items() if a in v and b in v)
            if len(eligible)<min_stations:
                outputs.append({"window":[start,end],"comparison":a+"__"+b,
                                "stations":len(eligible),"status":"INSUFFICIENT_MATCHED_STATIONS"})
                continue
            annual_a=[mean(station_year[s][a][i] for s in eligible) for i in range(len(years))]
            annual_b=[mean(station_year[s][b][i] for s in eligible) for i in range(len(years))]
            raw=_pearson(annual_a,annual_b)
            detr=_pearson(_detrend(years,annual_a),_detrend(years,annual_b))
            outputs.append({"window":[start,end],"comparison":a+"__"+b,
                "stations":len(eligible),"years":len(years),
                "annual_phenology_anomaly_correlation_r":round(raw,6) if raw is not None else None,
                "detrended_annual_anomaly_r":round(detr,6) if detr is not None else None,
                "same_sign_years":sum((x>0)==(y>0) for x,y in zip(annual_a,annual_b)),
                "annual_group_a_anomaly_days":[round(v,4) for v in annual_a],
                "annual_group_b_anomaly_days":[round(v,4) for v in annual_b],
                "status":"MATCHED_STATION_DIRECT_EVENT_ANOMALIES",
                "same_station_years":True,
                "shared_reference_in_difference_scores":False})
    return {"status":"DIRECT_EVENT_ANOMALIES_AND_DISJOINT_PLANT_REFERENCE",
            "leap_day_rows_excluded":leap_excluded,
            "plant_file_split":"sorted_original_source_file_alternating",
            "original_rm_semantics_certified":False,
            "weather_or_resource_effect_fitted":False,
            "comparisons":outputs}
