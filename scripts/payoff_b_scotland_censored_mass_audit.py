"""PAYOFF-B original EIDC mass/count source measurement audit, NO fitness fit.

EIDC records caterpillar.mass in grams per 30-hit branch sample from 2017;
'<0.02g' is a left-censored interval 0..0.02g, not zero. Uncertain mass
and blank mass on a positive count never become zero. Daily per-beating rates
are calculated on identical source samples for mass-versus-count peaks.
"""
import argparse
import json
import math
from collections import Counter,defaultdict
from datetime import date
from pathlib import Path

from scripts.payoff_b_scotland_hatch_resource_admission import (
    candidate_nests,iso_day,numeric
)
from scripts.payoff_b_scotland_hatch_window_fitness_loyo import source_data
from src.payoff_b_resource_contact import (
    ResourceContactNotAdmitted,demand_window_contact
)

CENSOR_UPPER_G=0.02
MIN_DAY_VALID_FRACTION=0.90
FIRST_MASS_YEAR=2017


def mass_raw(r):
    """Return (lower, upper, admissible, mass category) in milligrams."""
    n=numeric(r.get("caterpillars"))
    if n is None or n<0:
        return 0.0,0.0,False,"invalid_caterpillar_count"
    if str(r.get("mass.uncertain") or "").strip():
        return 0.0,0.0,False,"source_flagged_mass_uncertain"
    m=str(r.get("caterpillar.mass") or "").strip()
    if m.startswith("<"):
        if m.replace(" ","") not in ("<0.02g","<0.02","<0.02 g"):
            return 0.0,0.0,False,"unknown_censor_interval"
        return 0.0,1000*CENSOR_UPPER_G,True,"left_censored_0_to_0p02g"
    if m in ("", "NA", "N/A","nan","NaN"):
        if n==0:
            return 0.0,0.0,True,"zero_caterpillar_count_structural_zero"
        return 0.0,0.0,False,"positive_count_without_mass"
    v=numeric(m)
    if v is None or v<0:
        return 0.0,0.0,False,"negative_or_unreadable_mass"
    if n==0 and v>0:
        return 0.0,0.0,False,"zero_count_positive_mass"
    return 1000*v,1000*v,True,"original_numeric_g_to_mg"


def dated_mass(rows):
    groups=defaultdict(list)
    reasons=Counter()
    for r in rows:
        year=numeric(r.get("year"))
        if year is None or year<FIRST_MASS_YEAR:
            reasons["pre2017_unmeasured_mass"]+=1
            continue
        site=str(r.get("site") or "").strip()
        d=numeric(r.get("date"))
        if not site or d is None:
            reasons["no_site_or_date"]+=1
            continue
        try:
            iso=iso_day(int(year),d)
        except ValueError:
            reasons["invalid_ordinal_date"]+=1
            continue
        low,up,ok,reason=mass_raw(r)
        reasons[reason]+=1
        groups[(site,int(year),iso)].append((low,up,ok,numeric(r.get("caterpillars"))))
    by=defaultdict(list)
    days=Counter()
    for (site,yr,iso),samples in groups.items():
        good=[v for v in samples if v[2]]
        if len(good)<2:
            days["fewer_than_two_mass_qualified_beats"]+=1
            continue
        if len(good)/len(samples)<MIN_DAY_VALID_FRACTION:
            days["mass_source_coverage_below_90pct"]+=1
            continue
        n=len(good)
        cnt=sum(v[3] for v in good)/n
        lower=sum(v[0] for v in good)/n
        upper=sum(v[1] for v in good)/n
        if not (0<=lower<=upper):
            raise ValueError("Incorrect mass censor bounds")
        by[(site,yr)].append((iso,lower,upper,cnt,n))
        days["admitted_site_day"]+=1
    return by,dict(reasons),dict(days)


def samples_from_daily(rows,field):
    return [
        {"source_id":"EIDC_2022_CATERPILLAR_MASS",
         "site_id":"SITE","year":0,"guild":"caterpillars",
         "observation_date":d,"amount":v[field],"effort_n_beats":1,
         "currency":"measured_mg_per_beating"}
        for v in ({"day":r[0],"low":r[1],"up":r[2],"cnt":r[3]} for r in rows)
        for d in [v["day"]]
    ]


def make_samples(rows,kind):
    ix={"low":1,"up":2}[kind]
    return [{"source_id":"ORIGINAL_EIDC_2022_MASS_CENSOR_INTERVAL",
             "site_id":"WITHIN_SINGLE_SITE_YEAR",
             "year":0,"guild":"caterpillars",
             "observation_date":iso,"amount":r[ix],
             "effort_n_beats":1,"currency":"measured_mg_per_beating"}
            for r in rows for iso in [r[0]]]


def peak_date(rows,index):
    # First observed max on ties and no model-based smoothing.
    return min(r[0] for r in rows if r[index]==max(x[index] for x in rows))


def audit(data):
    mass_by,classes,day_qc=dated_mass(data["data/branch_beating.csv"])
    source_nests,excluded,_,_=candidate_nests(data["data/bird_phenology.csv"])
    sample_years=Counter()
    peak_deltas=[]
    count_peaks=[]
    bound_disagrees=0
    available_daily=Counter()
    for (site,year),rows in sorted(mass_by.items()):
        rows.sort()
        if len(rows)<2:continue
        p_count=peak_date(rows,3)
        p_lower=peak_date(rows,1)
        p_upper=peak_date(rows,2)
        lower_gap=(date.fromisoformat(p_lower)-date.fromisoformat(p_count)).days
        upper_gap=(date.fromisoformat(p_upper)-date.fromisoformat(p_count)).days
        if p_lower!=p_upper:bound_disagrees+=1
        peak_deltas.append({"site":site,"year":year,"lower_mass_minus_count_peak_days":lower_gap,
                            "upper_mass_minus_count_peak_days":upper_gap,
                            "n_admitted_mass_days":len(rows)})
        sample_years[year]+=1
    eligible=Counter()
    siteyears=defaultdict(lambda:{"nests":0,"mean_mass_low_mg":0.0,"mean_mass_high_mg":0.0})
    blocked=Counter()
    for n in source_nests:
        key=(n["site"],n["year"])
        if key not in mass_by:
            blocked["no_admitted_mass_siteyear"]+=1
            continue
        rows=mass_by[key]
        try:
            low=demand_window_contact(
                make_samples(rows,"low"),hatch_date=iso_day(n["year"],n["hatch"]),
                duration_days=14,max_observation_gap_days=8,min_coverage_fraction=1.0)
            high=demand_window_contact(
                make_samples(rows,"up"),hatch_date=iso_day(n["year"],n["hatch"]),
                duration_days=14,max_observation_gap_days=8,min_coverage_fraction=1.0)
        except (ResourceContactNotAdmitted,ValueError):
            blocked["mass_window_not_fully_measured"]+=1
            continue
        if low["prey_mean_per_beating_during_demand_proxy"]>high["prey_mean_per_beating_during_demand_proxy"]:
            raise ValueError("Censor bound crossing")
        row=siteyears[key]
        row["nests"]+=1
        row["mean_mass_low_mg"]+=low["prey_mean_per_beating_during_demand_proxy"]
        row["mean_mass_high_mg"]+=high["prey_mean_per_beating_during_demand_proxy"]
        eligible[n["year"]]+=1
    deltas=[p["lower_mass_minus_count_peak_days"] for p in peak_deltas]
    absolute=sorted(abs(x) for x in deltas)
    median_abs=(
        absolute[len(absolute)//2] if len(absolute)%2 else
        (absolute[len(absolute)//2-1]+absolute[len(absolute)//2])/2
    ) if absolute else None
    return {
        "status":"PAYOFF_B_EIDC_ORIGINAL_MASS_COUNT_PEAK_AND_HATCH_SOURCE_AUDIT",
        "source_mass_original_unit":"g per standardized branch sample",
        "source_mass_converted_unit":"mg per 30-hit branch beating",
        "mass_censor_interval_original":"[0,0.02g)",
        "mass_censor_imputation_not_performed":True,
        "mass_fit_to_fitness_performed":False,
        "number_of_mass_source_siteyears":len(mass_by),
        "peak_compare_siteyears":len(peak_deltas),
        "peak_compare_source_years":dict(sample_years),
        "peak_mass_lower_versus_count_median_abs_days":median_abs,
        "fraction_abs_peak_difference_ge7days":None if not deltas else sum(abs(x)>=7 for x in deltas)/len(deltas),
        "fraction_abs_peak_difference_ge14days":None if not deltas else sum(abs(x)>=14 for x in deltas)/len(deltas),
        "fraction_signed_mass_peak_after_count_peak":None if not deltas else sum(x>0 for x in deltas)/len(deltas),
        "mass_peak_lower_upper_date_disagrees_siteyears":bound_disagrees,
        "source_mass_categories":classes,
        "source_day_quality":day_qc,
        "original_confirmed_blue_tit_nests_before_mass_window":len(source_nests),
        "mass_window_supported_nests":sum(eligible.values()),
        "mass_window_supported_by_year":dict(sorted(eligible.items())),
        "mass_window_supported_siteyears":len(siteyears),
        "mass_window_supported_sites":len({s for s,y in siteyears}),
        "mass_window_blocked_counts":dict(blocked),
        "source_example_peak_delta_first_five":peak_deltas[:5],
        "same_primary_five_year_LOYO_admission_rule_met":len(eligible)>=5,
        "biomass_is_not_real_food_intake":True,
        "outcome_fit_not_allowed_from_this_source_audit":True,
    }


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    x=audit(source_data())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(x,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
