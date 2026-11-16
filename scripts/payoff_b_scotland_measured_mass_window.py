"""PAYOFF-B EIDC original observed mass versus count: censor-bounded exploratory test.

Prior count-only HOLD is preserved. Frozen before this new fit in:
docs/PAYOFF_B_SCOTLAND_MEASURED_MASS_WINDOW_FREEZE_20261116.md
Source is the exact-content SHA256-verified official EIDC OGL ZIP.
Food is potential branch-beating availability, not ingested resource.
"""
import argparse
import json
import math
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict
from scripts.payoff_b_scotland_hatch_resource_admission import (
    candidate_nests, numeric, iso_day, resources
)
from scripts.payoff_b_scotland_hatch_window_fitness_loyo import (
    source_data, original_site_details, source_temperature
)
from src.payoff_b_resource_contact import (
    ResourceContactNotAdmitted, daily_resource_rates, demand_window_contact
)

MIN_SITEYEARS=60
MIN_SITES=20
MIN_YEARS=3
MIN_NESTS=150
MASS_DATE_COVERAGE=0.8
BASE=["year","latitude","elevation","hatch_doy","clutch_size",
      "spring_temperature","log_season_peak","signed_peak_minus_hatch_days"]
FEATURES={
  "A_climate_peak_gap":BASE,
  "B_plus_count":BASE+["log_hatch_window"],
  "C0_mass_lower":BASE+["log_mass_window_lower"],
  "C1_mass_upper":BASE+["log_mass_window_upper"],
  "D0_count_mass_lower":BASE+["log_hatch_window","log_mass_window_lower"],
  "D1_count_mass_upper":BASE+["log_hatch_window","log_mass_window_upper"],
}


def original_mass_bounds(row, counters):
    count=numeric(row.get("caterpillars"))
    if count is None or count<0:
        counters["invalid_original_caterpillar_count"]+=1
        return None
    flag=str(row.get("mass.uncertain") or "").strip()
    if flag not in ("","0"):
        counters["uncertain_original_mass_excluded"]+=1
        return None
    raw=str(row.get("caterpillar.mass") or "").strip()
    if raw=="<0.02g":
        counters["censored_lt_0_02_g"]+=1
        return (0.0,0.02)
    mass=numeric(raw)
    if mass is not None:
        if mass<0 or (count==0 and mass>0):
            counters["contradictory_numeric_mass_excluded"]+=1
            return None
        counters["observed_numeric_mass_g"]+=1
        return mass,mass
    if raw=="" and count==0:
        counters["structural_zero_from_count_zero"]+=1
        return 0.0,0.0
    if raw=="":
        counters["positive_count_missing_mass"]+=1
        return None
    if raw.startswith("<"):
        raise ValueError("Unknown source censor threshold "+raw)
    counters["unknown_mass_text_excluded"]+=1
    return None


def source_mass(rows):
    groups=defaultdict(lambda: [0,0,0.0,0.0])
    categories=Counter()
    for r in rows:
        year=numeric(r.get("year"))
        day=numeric(r.get("date"))
        site=str(r.get("site") or "").strip()
        if year is None or day is None or not site:
            categories["invalid_source_date_or_site"]+=1
            continue
        key=(site,int(year),iso_day(year,day))
        groups[key][0]+=1
        bounds=original_mass_bounds(r,categories)
        if bounds is not None:
            groups[key][1]+=1
            groups[key][2]+=bounds[0]
            groups[key][3]+=bounds[1]
    lower,upper=defaultdict(list),defaultdict(list)
    date_qc=Counter()
    for (site,year,day),(total,valid,lo,hi) in sorted(groups.items()):
        if not valid or valid/total < MASS_DATE_COVERAGE:
            date_qc["date_below_80pct_mass_support"]+=1
            continue
        date_qc["date_admitted"]+=1
        base={"source_id":"EIDC_2022_measured_caterpillar_mass",
              "site_id":site,"year":year,"guild":"caterpillars",
              "observation_date":day,
              "effort_n_beats":1,"currency":"measured_mg_per_beating"}
        lower[(site,year)].append({**base,"amount":lo/valid*1000})
        upper[(site,year)].append({**base,"amount":hi/valid*1000})
    if set(lower)!=set(upper):
        raise ValueError("Mass lower/upper site-year admission differs")
    qa={"rows":len(rows),"source_date_rows":len(groups),
        "mass_class_counts":dict(categories),"date_qa":dict(date_qc),
        "admitted_siteyears":len(lower),
        "g_per_beating_conversion":"Original g converted to mg for contact, then back to g",
        "censor_bounds_g":[0.0,0.02],
        "zero_missing_mass_only_if_count_zero":True}
    return lower,upper,qa


def panel_from_original(data):
    nests,filters,_,species=candidate_nests(data["data/bird_phenology.csv"])
    counts,_,_,_=resources(data["data/branch_beating.csv"])
    lo,hi,massqa=source_mass(data["data/branch_beating.csv"])
    site=original_site_details(data["data/site_details.csv"])
    temp,tempqa=source_temperature(data["data/temperatures.csv"])
    groups=defaultdict(list)
    peaks={}
    rejected=Counter()
    for nest in nests:
        k=(nest["site"],nest["year"])
        if k not in counts or k not in lo:
            rejected["no_joint_site_year_count_mass"]+=1
            continue
        try:
            hatch=iso_day(nest["year"],nest["hatch"])
            supply={}
            for label,sample in (("count",counts[k]),("low",lo[k]),("high",hi[k])):
                supply[label]=demand_window_contact(sample,hatch_date=hatch,
                    duration_days=14,max_observation_gap_days=8,
                    min_coverage_fraction=1.0)["prey_mean_per_beating_during_demand_proxy"]
        except (ResourceContactNotAdmitted,ValueError):
            rejected["incomplete_14_day_count_or_mass"]+=1
            continue
        if supply["low"]>supply["high"]:
            raise ValueError("mass bounds inverted")
        if k not in peaks:
            events,_=daily_resource_rates(counts[k])
            val=max(v for day,v in events)
            peakday=min(day for day,v in events if v==val)
            peaks[k]=(val,date.fromordinal(peakday).timetuple().tm_yday)
        groups[k].append((nest,supply))
    panel=[]
    for (s,y),records in sorted(groups.items()):
        if s not in site or (s,y) not in temp:
            rejected["no_exact_site_climate"]+=len(records)
            continue
        n=len(records)
        mean=lambda key:sum(b[key] for b,sup in records)/n
        c=lambda label:sum(sup[label] for b,sup in records)/n
        hatch=mean("hatch")
        season_peak,peak_date=peaks[(s,y)]
        panel.append({
            "site":s,"year":y,"n_nests":n,
            "y_fledged_fraction":sum(b["fledged"]/b["clutch"] for b,sup in records)/n,
            "latitude":site[s]["latitude"],"elevation":site[s]["elevation"],
            "hatch_doy":hatch,"clutch_size":mean("clutch"),
            "spring_temperature":temp[(s,y)]["spring_temperature"],
            "log_season_peak":math.log1p(season_peak),
            "signed_peak_minus_hatch_days":peak_date-hatch,
            "log_hatch_window":math.log1p(c("count")),
            "log_mass_window_lower":math.log1p(c("low")/1000),
            "log_mass_window_upper":math.log1p(c("high")/1000),
            "raw_count_window":c("count"),
            "mass_window_lower_g_per_beat":c("low")/1000,
            "mass_window_upper_g_per_beat":c("high")/1000
        })
    qa={"original_verified_blue_tit_candidates":len(nests),
        "source_nests_with_count_and_mass_windows_before_climate":
            sum(len(v) for v in groups.values()),
        "after_climate_siteyears":len(panel),
        "after_climate_nests":sum(r["n_nests"] for r in panel),
        "after_climate_sites":len({r["site"] for r in panel}),
        "after_climate_years":sorted({r["year"] for r in panel}),
        "siteyears_by_year":dict(Counter(str(r["year"]) for r in panel)),
        "rejections":dict(rejected),
        "nest_source_filters":filters,
        "nest_species_labels":species,
        "mass_source":massqa,"temperature_source":tempqa}
    return panel,qa


def cv(rows, group):
    y=np.asarray([r["y_fledged_fraction"] for r in rows],float)
    lab=sorted({r[group] for r in rows})
    masks={l:np.asarray([r[group]==l for r in rows]) for l in lab}
    out={}
    for name,fields in FEATURES.items():
        X=np.asarray([[r[k] for k in fields] for r in rows],float)
        errors=np.zeros(len(rows))
        folds={}
        for label,held in masks.items():
            fit=~held
            if fit.sum()<max(12,len(fields)+3):
                raise ValueError("Not enough independent training site-years")
            pred=fit_predict(X[fit],y[fit],X[held])
            sq=(y[held]-pred)**2
            errors[held]=sq
            folds[str(label)]={"siteyears":int(held.sum()),"mse":float(sq.mean())}
        out[name]={"equal_fold_mse":float(np.mean([f["mse"] for f in folds.values()])),
                   "pooled_siteyear_mse":float(errors.mean()),"heldout_folds":folds}
    return {"models":out,"n_folds":len(lab),"n_siteyears":len(rows)}


def result(rows,qa):
    years=sorted({r["year"] for r in rows})
    sites=sorted({r["site"] for r in rows})
    n=len(rows)
    nests=sum(r["n_nests"] for r in rows)
    eligible=(n>=MIN_SITEYEARS and nests>=MIN_NESTS and
              len(years)>=MIN_YEARS and len(sites)>=MIN_SITES)
    result={
      "status":"PAYOFF_B_EIDC_ORIGINAL_MEASURED_MASS_VS_COUNT_LOYO_LOSO",
      "source":"EIDC 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3",
      "freeze":"docs/PAYOFF_B_SCOTLAND_MEASURED_MASS_WINDOW_FREEZE_20261116.md",
      "count_only_prior_gate":"HOLD_NO_GENERAL_PREDICTIVE_INCREMENT",
      "admitted":eligible,"n_siteyears":n,"n_sites":len(sites),
      "n_years":len(years),"years":years,"n_nests":nests,"qa":qa,
      "independence":"site-year; hold out whole site or year",
      "source_mass_units":"g per standardized branch beat, NOT g/m2",
      "interval_censor_bounds_g":[0.0,0.02],
      "intake_observed":False,"causal_or_info_game_supported":False,
      "exploratory_after_previous_negative_result":True
    }
    if not eligible:
        result["gate"]="NO_GO_INSUFFICIENT_MASS_COMMON_SUPPORT"
        return result
    loyo,loso=cv(rows,"year"),cv(rows,"site")
    contrasts={}
    for label,x in (("loyo",loyo),("loso",loso)):
        models=x["models"]
        m=lambda key:models[key]["equal_fold_mse"]
        contrasts[label]={
          "count_vs_peak":m("A_climate_peak_gap")-m("B_plus_count"),
          "lower_mass_vs_peak":m("A_climate_peak_gap")-m("C0_mass_lower"),
          "upper_mass_vs_peak":m("A_climate_peak_gap")-m("C1_mass_upper"),
          "lower_mass_additional_to_count":m("B_plus_count")-m("D0_count_mass_lower"),
          "upper_mass_additional_to_count":m("B_plus_count")-m("D1_count_mass_upper"),
        }
    year_a=[]
    models=loyo["models"]
    for yr in years:
        d=lambda key:models[key]["heldout_folds"][str(yr)]["mse"]
        lv=d("B_plus_count")-d("D0_count_mass_lower")
        uv=d("B_plus_count")-d("D1_count_mass_upper")
        year_a.append({"year":yr,
           "n_siteyears":models["B_plus_count"]["heldout_folds"][str(yr)]["siteyears"],
           "lower_gain":lv,"upper_gain":uv,"both_positive":lv>0 and uv>0})
    required=math.ceil(0.8*len(years))
    passed=all(contrasts[s][c]>0 for s in ("loyo","loso") for c in
          ("lower_mass_vs_peak","upper_mass_vs_peak",
           "lower_mass_additional_to_count","upper_mass_additional_to_count")
          ) and sum(r["both_positive"] for r in year_a)>=required
    result.update({
      "gate":"EXPLORATORY_MASS_SPECIFIC_INCREMENT" if passed
             else "HOLD_NO_GENERAL_MASS_SPECIFIC_INCREMENT",
      "loyo":loyo,"loso":loso,"contrasts":contrasts,
      "heldout_year_mass_increment":year_a,
      "years_required_both_censor_bounds":required,
      "years_observed_both_censor_bounds":sum(r["both_positive"] for r in year_a)
    })
    remaining=[r for r in rows if r["year"]!=2020]
    if (len(remaining)>=MIN_SITEYEARS and len({r["year"] for r in remaining})>=MIN_YEARS
        and len({r["site"] for r in remaining})>=MIN_SITES):
        result["exclude_2020_sensitivity"]={
          "status":"EXPLORATORY_SECONDARY_ONLY","n_siteyears":len(remaining),
          "loyo":cv(remaining,"year"),"loso":cv(remaining,"site")}
    else:
        result["exclude_2020_sensitivity"]={
          "status":"NOT_ADMITTED","n_siteyears":len(remaining),
          "n_years":len({r["year"] for r in remaining})}
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    rows,qa=panel_from_original(source_data())
    r=result(rows,qa)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(r,ensure_ascii=False,separators=(",",":"))


if __name__=="__main__":
    main()
