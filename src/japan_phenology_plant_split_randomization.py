"""Randomization sensitivity of disjoint plant reference in annual mismatch.

Keep fixed 20-year station/event observations and randomize which flowering
source files act as independent references. A random split is NOT a climate
null or a biological interaction significance test.
"""
from __future__ import annotations
from collections import defaultdict
from statistics import mean,median
import random
from src.japan_phenology_rm_sensitivity import leap_normalize
from src.japan_phenology_event_definition_audit import stage_from_label
from src.japan_phenology_coupling_robustness import _pearson, _detrend
from src.japan_phenology_fixed_interannual import WINDOWS

def plant_reference_randomization(events, *, repeats=200, seed=20261115, min_stations=10):
    if repeats<10:raise ValueError("At least ten source-file splits")
    events,_=leap_normalize(events)
    series=defaultdict(dict)
    for r in events:
        g=r["source_taxon_guess"]
        if (g,stage_from_label(r["event_label"])) not in {
            ("bird","first_sighting"),("insect","first_sighting"),("plant","flowering")}:
            continue
        key=(r["station_id"],r["source_file"],g)
        year=int(r["year"])
        if year in series[key]:raise ValueError("Duplicate source event")
        series[key][year]=int(r["day_of_year"])
    rng=random.Random(seed)
    results=[]
    for start,end in WINDOWS:
        years=list(range(start,end+1))
        station=defaultdict(lambda:defaultdict(dict))
        for (site,file,g),dates in series.items():
            if all(y in dates for y in years):
                vals=[dates[y] for y in years]
                center=mean(vals)
                station[site][g][file]=[v-center for v in vals]
        plant_files=sorted({f for s in station.values() for f in s["plant"]})
        if len(plant_files)<2:
            results.append({"window":[start,end],"status":"INSUFFICIENT_PLANT_SOURCE_FILES"})
            continue
        draws=[]
        for index in range(repeats):
            shuffled=plant_files[:]
            rng.shuffle(shuffled)
            midpoint=len(shuffled)//2
            pa=set(shuffled[:midpoint]);pb=set(shuffled[midpoint:])
            for swapped in (False,True):
                a,b=(pb,pa) if swapped else (pa,pb)
                eligible=[s for s,groups in station.items()
                          if groups["bird"] and groups["insect"]
                          and any(f in a for f in groups["plant"])
                          and any(f in b for f in groups["plant"])]
                if len(eligible)<min_stations:
                    continue
                annual_b=[];annual_i=[]
                for idx in range(len(years)):
                    annual_b.append(mean(
                        mean(v[idx] for v in station[s]["bird"].values())-
                        mean(v[idx] for f,v in station[s]["plant"].items() if f in a)
                        for s in eligible))
                    annual_i.append(mean(
                        mean(v[idx] for v in station[s]["insect"].values())-
                        mean(v[idx] for f,v in station[s]["plant"].items() if f in b)
                        for s in eligible))
                r=_pearson(annual_b,annual_i)
                d=_pearson(_detrend(years,annual_b),_detrend(years,annual_i))
                if r is not None:
                    draws.append({"r":r,"detrended_r":d,"stations":len(eligible)})
        if not draws:
            results.append({"window":[start,end],"status":"NO_ADMISSIBLE_DISJOINT_SPLITS"})
            continue
        rs=sorted(x["r"] for x in draws)
        dr=sorted(x["detrended_r"] for x in draws if x["detrended_r"] is not None)
        results.append({"window":[start,end],"status":"EXPLORATORY_DISJOINT_SOURCE_SPLIT_SENSITIVITY",
            "plant_source_file_count":len(plant_files),
            "valid_split_orientations":len(draws),
            "r_median":round(median(rs),6),
            "r_05_95_quantiles":[round(rs[int((len(rs)-1)*q)],6) for q in (0.05,0.95)],
            "fraction_positive_r":round(sum(x>0 for x in rs)/len(rs),6),
            "detrended_r_median":round(median(dr),6) if dr else None,
            "stations_min":min(x["stations"] for x in draws),
            "stations_max":max(x["stations"] for x in draws)})
    return {"status":"RANDOM_DISJOINT_PLANT_REFERENCE_SENSITIVITY_NOT_CLIMATE_NULL",
            "seed":seed,"requested_splits":repeats,
            "both_reference_orientations_tested":True,
            "source_rm_codes_certified":False,
            "weather_ndvi_biomass_fitted":False,
            "windows":results}
