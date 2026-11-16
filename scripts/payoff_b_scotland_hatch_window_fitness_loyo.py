"""Original EIDC Scottish blue tit hatch-window food proxy vs fledging: LOYO+LOSO.

Frozen analysis contract: docs/PAYOFF_B_SCOTLAND_HATCH_WINDOW_FIT_FREEZE_20261116.md
This is an *exploratory predictive* test on original source observations.
It is NOT measured ingestion, an experimental resource mechanism, or the
PAYOFF-B information/recourse model. Original ZIP SHA256 verified.
"""
import argparse,csv,hashlib,io,json,math,zipfile
from collections import Counter,defaultdict
from datetime import date
from pathlib import Path

import numpy as np
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict
from scripts.payoff_b_scotland_hatch_resource_admission import (
    candidate_nests, resources, iso_day, numeric
)
from scripts.payoff_b_scotland_resource_source_probe import EIDC_ID, open_url
from src.payoff_b_resource_contact import (
    ResourceContactNotAdmitted, daily_resource_rates, demand_window_contact
)

SOURCE_URL=f"https://data-package.ceh.ac.uk/data/{EIDC_ID}.zip"
ORIGINAL_ZIP_SHA256="e5e7fa4f2fe60420c11675a1d21fdc69b7b8d8fa5565f67b268e1ae070cd0d7d"
FILE_NAMES=("data/bird_phenology.csv","data/branch_beating.csv",
            "data/site_details.csv","data/temperatures.csv")
TMIN=-40.0
TMAX=60.0
TEMP_MIN_COVERAGE=0.80
FIT_MIN_SITEYEARS=75
FIT_MIN_YEARS=5
FIT_MIN_SITES=20


def source_data():
    r=open_url(SOURCE_URL,timeout=90,max_read=18_000_000)
    raw=r.get("body")
    if r.get("http_status")!=200 or not raw:
        raise RuntimeError("Original EIDC data unavailable; do not fit")
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_ZIP_SHA256:
        raise ValueError("Original EIDC ZIP sha256 changed; reject all")
    out={}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for f in FILE_NAMES:
            rows=csv.DictReader(io.StringIO(
                archive.read(f).decode("utf-8-sig",errors="replace"),newline=""))
            out[f]=list(rows)
    return out


def original_site_details(rows):
    out={}
    for row in rows:
        site=str(row.get("site") or "").strip()
        lat=numeric(row.get("MeanLat"))
        elev=numeric(row.get("MeanElev"))
        if not site or lat is None or elev is None:
            continue
        if not (50 <= lat <= 61 and -100 <= elev <= 1300):
            raise ValueError("Site coordinate/elevation invalid: "+site)
        if site in out:
            raise ValueError("Duplicate source site metadata")
        out[site]={"latitude":lat,"elevation":elev}
    return out


def source_temperature(rows):
    """March 1-April 15 original hourly iButton values; one siteyear average.

    Logger rows are averaged *after* filtering >=80% expected original hourly
    values from source wide columns, so 2 loggers never become 2 independent
    ecological units. No inferred dates, no interpolation.
    """
    if not rows:
        return {},{"missing_source":True}
    headers=list(rows[0])
    colnums={}
    for col in headers:
        if not col.startswith("X"):
            continue
        try:
            colnums[col]=float(col[1:])
        except ValueError:
            continue
    if len(colnums)<100:
        raise ValueError("Original logger ordinal-hour column schema not present")
    grouped=defaultdict(list)
    excluded=Counter()
    for row in rows:
        year=numeric(row.get("year"))
        site=str(row.get("site") or "").strip()
        if year is None or not site:
            excluded["invalid_site_year"]+=1
            continue
        yr=int(year)
        begin=date(yr,3,1).timetuple().tm_yday
        end=date(yr,4,15).timetuple().tm_yday+1
        cols=[k for k,v in colnums.items() if begin<=v<end]
        if not cols:
            raise ValueError("No logged data columns inside fixed temperature interval")
        vals=[]
        for c in cols:
            v=numeric(row.get(c))
            if v is None:
                continue
            if v<TMIN or v>TMAX:
                raise ValueError("Temperature source unit/physical range unexpected")
            vals.append(v)
        if len(vals)/len(cols)<TEMP_MIN_COVERAGE:
            excluded["logger_coverage_below_80pct"]+=1
            continue
        grouped[(site,yr)].append(sum(vals)/len(vals))
    out={}
    for key,logger_means in grouped.items():
        out[key]={"spring_temperature":sum(logger_means)/len(logger_means),
                  "n_valid_loggers":len(logger_means)}
    return out,{"logger_rows":len(rows),"n_siteyears_with_valid_loggers":len(out),
                "exclusions":dict(excluded),
                "fixed_window":"March 1-April 15",
                "no_temperature_gap_fill":True}


def admitted_siteyears(data):
    nests,filters,_,_=candidate_nests(data["data/bird_phenology.csv"])
    prey,_,mass_audit,_=resources(data["data/branch_beating.csv"])
    sites=original_site_details(data["data/site_details.csv"])
    temperature,temp_qc=source_temperature(data["data/temperatures.csv"])
    records=defaultdict(list)
    by_prey={}
    exclusions=Counter()
    for n in nests:
        key=(n["site"],n["year"])
        if key not in prey:
            exclusions["no_source_prey"]+=1
            continue
        try:
            sample=demand_window_contact(
                prey[key],hatch_date=iso_day(n["year"],n["hatch"]),
                duration_days=14,max_observation_gap_days=8,min_coverage_fraction=1.0)
        except (ResourceContactNotAdmitted,ValueError):
            exclusions["no_full_hatch_window"]+=1
            continue
        if key not in by_prey:
            counts,_=daily_resource_rates(prey[key])
            max_count=max(v for d,v in counts)
            peak_first_day=min(d for d,v in counts if v==max_count)
            by_prey[key]={"season_peak":max_count,
                          "peak_doy":date.fromordinal(peak_first_day).timetuple().tm_yday}
        records[key].append((n,sample["prey_mean_per_beating_during_demand_proxy"]))
    panel=[]
    for (site,year),nests in sorted(records.items()):
        if site not in sites:
            exclusions["no_source_site_metadata"]+=len(nests)
            continue
        if (site,year) not in temperature:
            exclusions["no_complete_climate_covariate"]+=len(nests)
            continue
        mean_hatch=sum(n["hatch"] for n,v in nests)/len(nests)
        mean_clutch=sum(n["clutch"] for n,v in nests)/len(nests)
        proportion=sum(n["fledged"]/n["clutch"] for n,v in nests)/len(nests)
        exposure=sum(v for n,v in nests)/len(nests)
        p=by_prey[(site,year)]
        panel.append({
            "site":site,"year":year,"n_nests":len(nests),
            "y_fledged_fraction":proportion,
            "hatch_doy":mean_hatch,"clutch_size":mean_clutch,
            "latitude":sites[site]["latitude"],"elevation":sites[site]["elevation"],
            "spring_temperature":temperature[(site,year)]["spring_temperature"],
            "log_season_peak":math.log1p(p["season_peak"]),
            "signed_peak_minus_hatch_days":p["peak_doy"]-mean_hatch,
            "log_hatch_window":math.log1p(exposure),
            "raw_peak_count_per_beating":p["season_peak"],
            "raw_mean_hatch_window_count_per_beating":exposure,
        })
    qa={"source_n_bird_nests_after_species_treatment_hatch":len(nests),
        "all_nests_hatch_proxy_admitted":sum(len(x) for x in records.values()),
        "after_climate_siteyear_rows":len(panel),
        "after_climate_sites":len({r["site"] for r in panel}),
        "after_climate_years":sorted({r["year"] for r in panel}),
        "after_climate_nests":sum(r["n_nests"] for r in panel),
        "excluded":dict(exclusions),"nest_filters":filters,
        "temperature":temp_qc,"mass_classes":mass_audit}
    return panel,qa


FEATURE_SETS={
    "M0_intercept":[],
    "M1_climate_hatch": ["year","latitude","elevation","hatch_doy",
                         "clutch_size","spring_temperature"],
    "M2_plus_peak_and_gap": ["year","latitude","elevation","hatch_doy",
                            "clutch_size","spring_temperature",
                            "log_season_peak","signed_peak_minus_hatch_days"],
    "M3_plus_window_supply": ["year","latitude","elevation","hatch_doy",
                              "clutch_size","spring_temperature",
                              "log_season_peak","signed_peak_minus_hatch_days",
                              "log_hatch_window"],
}


def cross_validate(rows,groupkey):
    y=np.asarray([r["y_fledged_fraction"] for r in rows],dtype=float)
    labels=sorted({r[groupkey] for r in rows})
    masks={g:np.asarray([r[groupkey]==g for r in rows]) for g in labels}
    out={}
    for name,columns in FEATURE_SETS.items():
        X=np.asarray([[r[k] for k in columns] for r in rows],
                     dtype=float).reshape(len(rows),len(columns))
        squared=np.zeros(len(rows),dtype=float)
        per_fold={}
        for label,hold in masks.items():
            train=~hold
            if train.sum()<max(12,len(columns)+3):
                raise ValueError("Too few independent site-years in fold train")
            pred=fit_predict(X[train],y[train],X[hold])
            err=(y[hold]-pred)**2
            squared[hold]=err
            per_fold[str(label)]={"test_siteyears":int(hold.sum()),
                                  "mse":float(err.mean())}
        out[name]={
            "equal_fold_mse":float(np.mean([p["mse"] for p in per_fold.values()])),
            "pooled_equal_siteyear_mse":float(squared.mean()),
            "heldout_folds":per_fold,
        }
    m2=out["M2_plus_peak_and_gap"]["equal_fold_mse"]
    m3=out["M3_plus_window_supply"]["equal_fold_mse"]
    m1=out["M1_climate_hatch"]["equal_fold_mse"]
    return {"n_folds":len(labels),"n_source_siteyears":len(rows),
            "model_results":out,
            "improvement_over_peak_and_gap":m2-m3,
            "improvement_over_climate_hatch":m1-m3}


def audit(rows,qa):
    years=sorted({r["year"] for r in rows})
    sites=sorted({r["site"] for r in rows})
    admitted=(len(rows)>=FIT_MIN_SITEYEARS and len(years)>=FIT_MIN_YEARS
              and len(sites)>=FIT_MIN_SITES)
    result={
        "status":"PAYOFF_B_EIDC_HATCH_WINDOW_ORIGINAL_LOYO_LOSO",
        "source_zip_sha256":ORIGINAL_ZIP_SHA256,
        "source_grain":"independent site-year mean of admitted blue tit nests",
        "resource_measure":"count per standardized 30-hit branch beating, not biomass or intake",
        "admitted_for_fitness_prediction":admitted,
        "model_specification_frozen_before_outcome":"docs/PAYOFF_B_SCOTLAND_HATCH_WINDOW_FIT_FREEZE_20261116.md",
        "no_parameter_tuning_after_outcome":True,
        "causal_effect_identified":False,
        "individual_bird_information_or_recourse_observed":False,
        "qa":qa
    }
    if not admitted:
        result["gate"]="NO_GO_INSUFFICIENT_CLIMATE_COMPLETE_SITEYEAR_PANEL"
        return result
    loyo=cross_validate(rows,"year")
    loso=cross_validate(rows,"site")
    yearly=[]
    for yr,stat in loyo["model_results"]["M2_plus_peak_and_gap"]["heldout_folds"].items():
        m3=loyo["model_results"]["M3_plus_window_supply"]["heldout_folds"][yr]["mse"]
        yearly.append({"year":yr,"siteyears":stat["test_siteyears"],
                       "mse_improvement_M2_minus_M3":stat["mse"]-m3})
    improving=sum(r["mse_improvement_M2_minus_M3"]>0 for r in yearly)
    threshold=(loyo["improvement_over_peak_and_gap"]>0
               and loyo["improvement_over_climate_hatch"]>0
               and loso["improvement_over_peak_and_gap"]>0
               and loso["improvement_over_climate_hatch"]>0
               and improving>=4)
    result.update({
        "gate":"EXPLORATORY_GO_PREDICTIVE_INCREMENT" if threshold
               else "HOLD_NO_GENERAL_PREDICTIVE_INCREMENT",
        "loyo":loyo,"loso":loso,"years_improving_window_over_peak":improving,
        "yearly_incremental":yearly,
        "siteyear_counts_by_year":dict(Counter(str(r["year"]) for r in rows)),
        "nests_per_siteyear":{"min":min(r["n_nests"] for r in rows),
                              "max":max(r["n_nests"] for r in rows),
                              "mean":sum(r["n_nests"] for r in rows)/len(rows)},
        "y_mean":sum(r["y_fledged_fraction"] for r in rows)/len(rows),
    })
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    panel,qa=admitted_siteyears(source_data())
    result=audit(panel,qa)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
