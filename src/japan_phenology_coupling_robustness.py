"""Equal-weight station-level cross-taxon timing correlations on original JMA events.

This descriptive robustness check corrects the pooled event-pair-year
pseudo-replication problem by aggregating within station before nationwide
summary. It also reports a linear-detrended comparison to expose shared
long-term trends; neither is a causal or quality-screened estimate.
"""
from __future__ import annotations
from collections import defaultdict
from statistics import median
import math


def _pearson(a, b):
    if len(a) < 3 or len(a) != len(b):
        return None
    ma, mb = sum(a)/len(a), sum(b)/len(b)
    xa, xb = [v-ma for v in a], [v-mb for v in b]
    denom = math.sqrt(sum(v*v for v in xa)*sum(v*v for v in xb))
    return sum(x*y for x,y in zip(xa,xb))/denom if denom > 1e-12 else None


def _detrend(years, values):
    my, mv = sum(years)/len(years), sum(values)/len(values)
    xx = sum((y-my)**2 for y in years)
    slope = sum((y-my)*(v-mv) for y,v in zip(years,values))/xx if xx else 0
    return [v-mv-slope*(y-my) for y,v in zip(years,values)]


def station_balanced_coupling(events, group_a, group_b, *, min_shared_years=10):
    if group_a == group_b:
        raise ValueError("Different source groups required")
    series = defaultdict(dict)
    for r in events:
        if r["source_taxon_guess"] not in (group_a,group_b):
            continue
        key=(r["station_id"],r["source_file"],r["source_taxon_guess"])
        year=int(r["year"])
        if year in series[key]:
            raise ValueError("Duplicate event station-year")
        series[key][year]=int(r["day_of_year"])
    by_station=defaultdict(lambda: {group_a:[],group_b:[]})
    for (station,source,group), years in series.items():
        by_station[station][group].append((source,years))
    stations=[]
    total_pairs=0
    for station,grouped in sorted(by_station.items()):
        raw_pairs=[]
        detrended_pairs=[]
        for _,a in grouped[group_a]:
            for _,b in grouped[group_b]:
                common=sorted(set(a)&set(b))
                if len(common)<min_shared_years:
                    continue
                av=[a[y] for y in common]
                bv=[b[y] for y in common]
                raw=_pearson(av,bv)
                detrended=_pearson(_detrend(common,av),_detrend(common,bv))
                if raw is not None:
                    raw_pairs.append(raw)
                if detrended is not None:
                    detrended_pairs.append(detrended)
        if raw_pairs:
            total_pairs+=len(raw_pairs)
            stations.append({"station_id":station,"raw_station_mean_r":sum(raw_pairs)/len(raw_pairs),
                             "detrended_station_mean_r":(sum(detrended_pairs)/len(detrended_pairs)
                                                      if detrended_pairs else None),
                             "event_pairs":len(raw_pairs)})
    raw=[s["raw_station_mean_r"] for s in stations]
    detr=[s["detrended_station_mean_r"] for s in stations if s["detrended_station_mean_r"] is not None]
    return {
        "status":"STATION_BALANCED_DESCRIPTIVE_ONLY" if raw else "NO_ADMISSIBLE_PAIRS",
        "group_a":group_a,"group_b":group_b,
        "stations_with_pairs":len(stations),
        "event_pairs_used_not_independent":total_pairs,
        "mean_station_equal_weight_r":round(sum(raw)/len(raw),6) if raw else None,
        "median_station_r":round(median(raw),6) if raw else None,
        "fraction_stations_positive_r":round(sum(v>0 for v in raw)/len(raw),6) if raw else None,
        "mean_station_equal_weight_detrended_r":round(sum(detr)/len(detr),6) if detr else None,
        "stations_with_detrended_r":len(detr),
        "min_shared_years":min_shared_years,
        "rm_codes_screened":False,"statistical_significance_estimated":False,
        "biomass_or_weather_causal_effect_identified":False,
    }
