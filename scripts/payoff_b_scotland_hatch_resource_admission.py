"""PAYOFF-B: pre-fit nest/food common-support audit from official EIDC ZIP.

No coefficients fitted. Primary will use unmanipulated nests with observed
hatch date, fledged count and positive clutch size, then *observed* supply
support for the fixed 14-day hatch-based proxy window. Count supply and
mass supply are separate. Mass <0.02g is interval-censored, not zero.
"""
import argparse
import csv
import io
import json
import math
import zipfile
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from scripts.payoff_b_scotland_eidc_original_csv_gate import get_support
from scripts.payoff_b_scotland_resource_source_probe import EIDC_ID, open_url
from src.payoff_b_resource_contact import (
    ResourceContactNotAdmitted, demand_window_contact
)

URL=f"https://data-package.ceh.ac.uk/data/{EIDC_ID}.zip"
HEAD_CENSOR="<0.02g"
WINDOW=14


def original():
    manifest,_=get_support()
    sizes={x["path"]:x["bytes"] for x in manifest}
    r=open_url(URL,timeout=80,max_read=25_000_000)
    raw=r.get("body")
    if r.get("http_status")!=200 or not raw:
        raise ValueError("No original EIDC data ZIP")
    files={}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for name in ("data/bird_phenology.csv","data/branch_beating.csv"):
            b=z.read(name)
            if len(b)!=sizes[name]:
                raise ValueError("Official RO-Crate file size mismatch: "+name)
            files[name]=list(csv.DictReader(io.StringIO(
                b.decode("utf-8-sig",errors="replace"),newline="")))
    return files


def numeric(x):
    if x is None:
        return None
    s=str(x).strip()
    if s in ("","-999","-999.0","NA","N/A","nan","NaN"):
        return None
    try:
        v=float(s)
        return v if math.isfinite(v) else None
    except ValueError:
        return None


def iso_day(year,doy):
    y=int(year)
    d=int(doy)
    upper=366 if y%4==0 and (y%100!=0 or y%400==0) else 365
    if not 1<=d<=upper:
        raise ValueError("Invalid source year/ordinal day")
    return (date(y,1,1)+timedelta(days=d-1)).isoformat()


def candidate_nests(rows):
    flags=Counter()
    out=[]
    categories=Counter()
    species=Counter()
    for row in rows:
        species[str(row.get("species","")).strip()]+=1
        treat=str(row.get("clutch_swap_treatment","")).strip()
        categories[treat]+=1
        if treat.lower() not in ("unmanipulated",""):
            flags["manipulated_or_odd"]+=1
            continue
        yr=numeric(row.get("year"))
        hatch=numeric(row.get("hatching_first_recorded"))
        succ=numeric(row.get("suc"))
        clutch=numeric(row.get("cs"))
        if yr is None:
            flags["no_year"]+=1;continue
        if hatch is None:
            flags["no_hatch"]+=1;continue
        if succ is None or succ<0:
            flags["no_fledglings_or_sentinel"]+=1;continue
        if clutch is None or clutch<=0:
            flags["no_clutch"]+=1;continue
        if succ>clutch:
            flags["fledged_exceeds_clutch"]+=1;continue
        site=str(row.get("site","")).strip()
        box=str(row.get("box","")).strip()
        if not site or not box:
            flags["no_site_or_nestbox"]+=1;continue
        out.append({"site":site,"year":int(yr),"box":box,"hatch":int(hatch),
                    "fledged":succ,"clutch":clutch,
                    "treatment":treat})
    return out,dict(flags),dict(categories),dict(species)


def resources(rows):
    by=defaultdict(list)
    categories=Counter()
    issues=Counter()
    mass=Counter()
    for row in rows:
        site=str(row["site"]).strip()
        year=numeric(row.get("year"));d=numeric(row.get("date"))
        c=numeric(row.get("caterpillars"))
        if year is None or d is None or c is None or c<0:
            issues["bad_year_date_or_count"]+=1;continue
        un=str(row.get("mass.uncertain","")).strip()
        m=str(row.get("caterpillar.mass","")).strip()
        if m.startswith("<"):mass["censored_less_than"]+=1
        elif m=="":mass["blank"]+=1
        elif numeric(m) is not None:mass["numeric"]+=1
        else:mass["other_text"]+=1
        if un=="1":issues["mass_uncertain_flagged"]+=1
        else:categories[un]+=1
        try:
            day=iso_day(year,d)
        except ValueError:
            issues["invalid_ordinal_date"]+=1
            continue
        by[(site,int(year))].append({
            "source_id":"EIDC_2022_DOI_10.5285/b63d53ae",
            "site_id":site,"year":int(year),"guild":"caterpillars",
            "observation_date":day,
            "currency":"count_per_beating",
            "amount":c,"effort_n_beats":1})
    return by,dict(issues),dict(mass),dict(categories)


def audit():
    x=original()
    bird=x["data/bird_phenology.csv"]
    food=x["data/branch_beating.csv"]
    nests,excluded,treatments,species=candidate_nests(bird)
    supply,issues,mass,uncertain=resources(food)
    out=Counter()
    by_year=defaultdict(Counter)
    n_eff=[]
    results_by_siteyear=defaultdict(lambda:{"n_candidates":0,"n_supported":0})
    for n in nests:
        key=(n["site"],n["year"])
        results_by_siteyear[key]["n_candidates"]+=1
        if key not in supply:
            out["no_exact_site_year_prey"]+=1;continue
        try:
            exposure=demand_window_contact(
                supply[key],hatch_date=iso_day(n["year"],n["hatch"]),
                duration_days=WINDOW,max_observation_gap_days=8,
                min_coverage_fraction=1.0)
        except (ResourceContactNotAdmitted,ValueError):
            out["prey_window_not_fully_supported"]+=1;continue
        out["fully_supported_nests"]+=1
        by_year[n["year"]]["supported"]+=1
        results_by_siteyear[key]["n_supported"]+=1
        n_eff.append((n["site"],n["year"],n["hatch"],exposure["prey_mean_per_beating_during_demand_proxy"]))
    observed_years=sorted({n["year"] for n in nests})
    admitted_years=sorted(by_year)
    return {
        "status":"PAYOFF_B_SCOTLAND_OBSERVED_HATCH_PREY_COMMON_SUPPORT_PREFIT",
        "source":"EIDC 2022 44-site tritrophic original under OGL",
        "source_records_bird":len(bird),
        "source_records_branch_beating":len(food),
        "bird_species_labels":species,
        "clutch_swap_labels":treatments,
        "nest_exclusion_counts":excluded,
        "eligible_unmanipulated_nests_before_food":len(nests),
        "candidate_nest_years":observed_years,
        "food_source_issues":issues,
        "mass_source_categories":mass,
        "mass_uncertain_categories":uncertain,
        "food_siteyears":len(supply),
        "food_years":sorted({y for s,y in supply}),
        "food_beating_unit":"per standardized 30-hit branch beat",
        "mass_is_left_censored_and_not_fitted":True,
        "fixed_window":"hatch to hatch+13 inclusive, count per beating, full measured support",
        "support_exclusions":dict(out),
        "supported_years":admitted_years,
        "supported_siteyears":sum(x["n_supported"]>0 for x in results_by_siteyear.values()),
        "supported_sites":len({s for (s,y),x in results_by_siteyear.items() if x["n_supported"]>0}),
        "nests_with_full_observed_resource_support":len(n_eff),
        "supported_by_year":{str(y):dict(c) for y,c in sorted(by_year.items())},
        "fitness_effect_fitted":False,
        "ready_for_year_heldout_fitness_model":len(admitted_years)>=5 and len(n_eff)>=100,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    x=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(x,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
