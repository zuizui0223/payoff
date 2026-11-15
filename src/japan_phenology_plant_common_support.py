"""Common-support disjoint plant references: fixed stations across all splits.

Select a fixed set of 4 original flowering source files with the largest
20-year intersection of bird, insect and all four plant source files.
Enumerate unique balanced 2-vs-2 partitions, both orientations. This
removes station-composition drift across partitions, but changes the
plant-source target population and cannot identify climate effects.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations
from statistics import mean, median
from src.japan_phenology_rm_sensitivity import leap_normalize
from src.japan_phenology_event_definition_audit import stage_from_label
from src.japan_phenology_coupling_robustness import _pearson, _detrend
from src.japan_phenology_fixed_interannual import WINDOWS

def fixed_common_support_plant_splits(events, *, min_stations=10, core_plant_files=4):
    if core_plant_files != 4:
        raise ValueError("Exactly four plant source files for exhaustive balanced partitions")
    events,_=leap_normalize(events)
    series=defaultdict(dict)
    for row in events:
        group=row["source_taxon_guess"]
        if (group,stage_from_label(row["event_label"])) not in {
            ("bird","first_sighting"),("insect","first_sighting"),("plant","flowering")}:
            continue
        key=(row["station_id"],row["source_file"],group)
        year=int(row["year"])
        if year in series[key]:
            raise ValueError("Duplicate station/source/year")
        series[key][year]=int(row["day_of_year"])
    outputs=[]
    for start,end in WINDOWS:
        years=list(range(start,end+1))
        station=defaultdict(lambda:defaultdict(dict))
        for (site,file,group),dates in series.items():
            if not all(year in dates for year in years):
                continue
            vals=[dates[year] for year in years]
            center=mean(vals)
            station[site][group][file]=[v-center for v in vals]
        base_sites={site for site,groups in station.items() if groups["bird"] and groups["insect"]}
        plant_sites=defaultdict(set)
        for site in base_sites:
            for file in station[site]["plant"]:
                plant_sites[file].add(site)
        best_files=None;best_sites=set()
        # Source files and station sets selected once per 20-year window,
        # independently of the observed anomaly correlations.
        for files in combinations(sorted(plant_sites),core_plant_files):
            sites=set(base_sites)
            for file in files:
                sites.intersection_update(plant_sites[file])
            if len(sites)>len(best_sites) or (len(sites)==len(best_sites) and (best_files is None or files<best_files)):
                best_sites=sites;best_files=files
        if len(best_sites)<min_stations:
            outputs.append({"window":[start,end],"status":"INSUFFICIENT_FIXED_COMMON_SUPPORT",
                            "maximum_fixed_station_count":len(best_sites),
                            "selected_plant_files":list(best_files or [])})
            continue
        sites=sorted(best_sites)
        draws=[]
        # 4 choose 2 = 6 oriented assignments; no pseudo-replication of
        # repeated random splits or duplicated reference orientations.
        for pa in combinations(best_files,2):
            pb=tuple(f for f in best_files if f not in pa)
            annual_b=[];annual_i=[]
            for idx in range(len(years)):
                annual_b.append(mean(
                    mean(v[idx] for v in station[s]["bird"].values())-
                    mean(station[s]["plant"][f][idx] for f in pa) for s in sites))
                annual_i.append(mean(
                    mean(v[idx] for v in station[s]["insect"].values())-
                    mean(station[s]["plant"][f][idx] for f in pb) for s in sites))
            r=_pearson(annual_b,annual_i)
            detr=_pearson(_detrend(years,annual_b),_detrend(years,annual_i))
            draws.append({"plant_a":list(pa),"plant_b":list(pb),
                          "r":round(r,6) if r is not None else None,
                          "detrended_r":round(detr,6) if detr is not None else None})
        rs=sorted(d["r"] for d in draws if d["r"] is not None)
        outputs.append({"window":[start,end],"status":"FIXED_STATIONS_EXHAUSTIVE_DISJOINT_REFERENCES",
            "fixed_station_count":len(sites),"fixed_station_ids":sites,
            "selected_plant_files":list(best_files),
            "unique_oriented_splits":len(draws),
            "r_median":round(median(rs),6) if rs else None,
            "r_min":min(rs) if rs else None,"r_max":max(rs) if rs else None,
            "fraction_positive_r":round(sum(x>0 for x in rs)/len(rs),6) if rs else None,
            "draws":draws})
    return {"status":"FIXED_COMMON_SUPPORT_EXHAUSTIVE_FOUR_PLANT_REFERENCES",
            "source_file_selection":"maximize_20_year_shared_station_coverage_not_effect_size",
            "split_draws_are_not_independent":True,
            "phenology_rm_codes_certified":False,
            "weather_ndvi_biomass_fitted":False,
            "windows":outputs}
