"""Decompose flowering-reference versus station-support sensitivity.

For each four-file flowering subset, compute the same six oriented disjoint
lag correlations on (i) strict four-file common stations and (ii) pair-specific
station sets. Within each subset this isolates changing station support.
Across subsets at strict support it describes plant-file selection sensitivity,
though strict station sets still vary across subsets.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations
from statistics import mean, median
from src.japan_phenology_rm_sensitivity import leap_normalize
from src.japan_phenology_event_definition_audit import stage_from_label
from src.japan_phenology_coupling_robustness import _pearson
from src.japan_phenology_fixed_interannual import WINDOWS

def factorial_reference_station_sensitivity(events, *, min_stations=10, max_subsets=500):
    events,_=leap_normalize(events)
    series=defaultdict(dict)
    for row in events:
        group=row["source_taxon_guess"]
        if (group,stage_from_label(row["event_label"])) not in {
            ("bird","first_sighting"),("insect","first_sighting"),("plant","flowering")}:
            continue
        key=(row["station_id"],row["source_file"],group)
        year=int(row["year"])
        if year in series[key]:raise ValueError("Duplicate station/source/year")
        series[key][year]=int(row["day_of_year"])
    output=[]
    for start,end in WINDOWS:
        years=list(range(start,end+1))
        station=defaultdict(lambda:defaultdict(dict))
        for (site,file,group),dates in series.items():
            if not all(y in dates for y in years):continue
            vals=[dates[y] for y in years]
            center=mean(vals)
            station[site][group][file]=[v-center for v in vals]
        base={s for s,g in station.items() if g["bird"] and g["insect"]}
        plant_sites=defaultdict(set)
        for s in base:
            for f in station[s]["plant"]:plant_sites[f].add(s)
        files=sorted(plant_sites)
        subset_summaries=[]
        subsets=0
        for fs in combinations(files,4):
            if subsets>=max_subsets:break
            subsets+=1
            strict=set(base)
            for f in fs:strict.intersection_update(plant_sites[f])
            strict=sorted(strict)
            if len(strict)<min_stations:continue
            paired=[]
            for a in combinations(fs,2):
                b=tuple(f for f in fs if f not in a)
                variable=sorted(s for s in base
                    if any(f in station[s]["plant"] for f in a)
                    and any(f in station[s]["plant"] for f in b))
                def corr(sites):
                    x=[];y=[]
                    for i in range(len(years)):
                        x.append(mean(mean(v[i] for v in station[s]["bird"].values())-
                            mean(station[s]["plant"][f][i] for f in a if f in station[s]["plant"])
                            for s in sites))
                        y.append(mean(mean(v[i] for v in station[s]["insect"].values())-
                            mean(station[s]["plant"][f][i] for f in b if f in station[s]["plant"])
                            for s in sites))
                    return _pearson(x,y)
                r_fixed=corr(strict);r_variable=corr(variable)
                if r_fixed is None or r_variable is None:continue
                paired.append((r_fixed,r_variable,len(variable)))
            if not paired:continue
            subset_summaries.append({"plant_files":list(fs),
                "strict_stations":len(strict),
                "variable_stations_min":min(x[2] for x in paired),
                "variable_stations_max":max(x[2] for x in paired),
                "fixed_r_median":round(median(x[0] for x in paired),6),
                "variable_r_median":round(median(x[1] for x in paired),6),
                "paired_variable_minus_fixed_r_median":round(median(x[1]-x[0] for x in paired),6),
                "fixed_positive_orientations":sum(x[0]>0 for x in paired),
                "variable_positive_orientations":sum(x[1]>0 for x in paired)})
        if not subset_summaries:
            output.append({"window":[start,end],"status":"NO_FOUR_FILE_SUBSET_WITH_MIN_COMMON_STATIONS",
                           "subsets_examined":subsets})
            continue
        diffs=[x["paired_variable_minus_fixed_r_median"] for x in subset_summaries]
        fixed=[x["fixed_r_median"] for x in subset_summaries]
        output.append({"window":[start,end],
            "status":"WITHIN_FILE_SUBSET_STATION_SUPPORT_PAIRED_COMPARISON",
            "subsets_examined":subsets,
            "subsets_admitted":len(subset_summaries),
            "fixed_subset_median_r_range":[min(fixed),max(fixed)],
            "median_within_subset_station_support_delta_r":round(median(diffs),6),
            "fraction_subsets_fixed_median_positive":round(sum(x>0 for x in fixed)/len(fixed),6),
            "subsets":subset_summaries})
    return {"status":"FACTORIAL_REFERENCE_SITE_SENSITIVITY_DESCRIPTIVE",
        "max_subsets_per_window":max_subsets,
        "subset_selection":"lexicographic_source_file_combinations_without_effect_screen",
        "different_subsets_still_have_different_strict_station_sets":True,
        "weather_ndvi_biomass_fitted":False,
        "windows":output}
