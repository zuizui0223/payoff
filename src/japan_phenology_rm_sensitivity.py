"""Sensitivity of JMA cross-taxon associations to original rm code and leap day.

The rm meanings remain unverified: these are code-defined strata, NOT
quality-filtered observations. Exclude Feb 29 from normalized 365-day DOY.
"""
from __future__ import annotations
import datetime as dt
import calendar
from collections import Counter
from src.japan_phenology_coupling_robustness import station_balanced_coupling

PAIRS = [
    ("amphibian","plant_or_unclassified"),
    ("bird","plant_or_unclassified"),
    ("insect","plant_or_unclassified"),
    ("amphibian","bird"),
    ("bird","insect"),
    ("amphibian","insect"),
]

def leap_normalize(events):
    normalized=[]
    feb29=0
    for row in events:
        d=dt.date.fromisoformat(row["event_date"])
        if d.month==2 and d.day==29:
            feb29+=1
            continue
        new=dict(row)
        new["day_of_year"]=d.timetuple().tm_yday - int(calendar.isleap(d.year) and d.month>2)
        normalized.append(new)
    return normalized, feb29

def rm_sensitivity(events, *, min_shared_years=10, bootstrap_reps=300):
    base, excluded=leap_normalize(events)
    codes=Counter(str(e["rm_original_code"]) for e in base)
    results=[]
    for name, keep in [
        ("all_rm_codes",lambda r: True),
        ("rm_code_8_only",lambda r: str(r["rm_original_code"])=="8"),
        ("rm_code_9_only",lambda r: str(r["rm_original_code"])=="9"),
        ("rm_codes_8_or_9",lambda r: str(r["rm_original_code"]) in ("8","9")),
    ]:
        subset=[r for r in base if keep(r)]
        comparisons=[station_balanced_coupling(subset,a,b,
                     min_shared_years=min_shared_years,
                     bootstrap_reps=bootstrap_reps)
                     for a,b in PAIRS]
        results.append({"stratum":name,"source_event_cells":len(subset),
                        "comparisons":comparisons})
    return {"status":"UNINTERPRETED_RM_CODE_STRATIFIED_DESCRIPTIVE_SENSITIVITY",
            "leap_day_rows_excluded":excluded,
            "rm_original_code_counts":dict(codes),
            "source_quality_code_meanings_certified":False,
            "causal_weather_ndvi_biomass_effect_estimated":False,
            "strata":results}
