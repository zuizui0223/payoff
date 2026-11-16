"""Source-only pre-fit Scottish EIDC nestling body-mass ↔ prey-mass admission.

No phenotype coefficient or model fitted. Independent nests and siteyears only,
no conditioning on fledgling success (prevents outcome-based selection).
Original EIDC DOIs, SHA256, treatment, stage, early resource support required.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from scripts.payoff_b_scotland_hatch_resource_admission import (
    numeric, iso_day, resources
)
from scripts.payoff_b_scotland_hatch_window_fitness_loyo import (
    SOURCE_URL, original_site_details, source_temperature
)
from scripts.payoff_b_scotland_measured_mass_window import source_mass
from scripts.payoff_b_scotland_resource_source_probe import open_url
from src.payoff_b_resource_contact import (
    ResourceContactNotAdmitted, daily_resource_rates, demand_window_contact
)

SHA={
  "data/bird_phenology.csv":"eb3f8d9faaa30ee3363f515f97873f287a918bb8a3ad31d180e2ac3a81d89257",
  "data/nestlings.csv":"e292c06e9256700782ebd66c59741f5e8d50514c948fb4b83c4aa698113322e2",
  "data/branch_beating.csv":"38f5c34cf656bab33c5d5b3516648306549049deebfbe693e4b4cad09ac4004c",
  "data/site_details.csv":"f2a65cd96b2241ae6ff9d1207888d1453fef2738545c52a6ace1222fb56e2165",
  "data/temperatures.csv":"4686a544858e707b3844eee8bcd2ce26f1bf5d8daf3c3a0166843524734aa33b",
}


def load_original():
    r=open_url(SOURCE_URL, timeout=90, max_read=18_000_000)
    raw=r.get("body")
    if r.get("http_status")!=200 or not raw:
        raise ValueError("Original EIDC OGL ZIP unavailable")
    out={}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for path,expected in SHA.items():
            b=archive.read(path)
            if hashlib.sha256(b).hexdigest()!=expected:
                raise ValueError("EIDC source content drift: "+path)
            out[path]=list(csv.DictReader(io.StringIO(
                 b.decode("utf-8-sig",errors="replace"),newline="")))
    return out


def admit_source_nests(rows):
    out={}
    excluded=Counter()
    labels=Counter()
    for r in rows:
        yr=numeric(r.get("year"))
        sp=str(r.get("species") or "").strip().lower()
        treat=str(r.get("clutch_swap_treatment") or "").strip().lower()
        labels[sp+"|"+treat]+=1
        if sp!="bluti":
            excluded["nonverified_blue_tit"]+=1;continue
        if yr is None or int(yr)<2017:
            excluded["no_measured_mass_year"]+=1;continue
        if treat not in ("","unmanipulated") or (2017<=int(yr)<=2019 and treat==""):
            excluded["manipulated_or_treatment_unknown"]+=1;continue
        hatch=numeric(r.get("hatching_first_recorded"))
        clutch=numeric(r.get("cs"))
        if hatch is None or clutch is None or clutch<=0:
            excluded["missing_hatch_or_clutch"]+=1;continue
        site=str(r.get("site") or "").strip()
        box=str(r.get("box") or "").strip()
        if not site or not box:
            excluded["no_site_or_box"]+=1;continue
        k=(site,int(yr),box)
        if k in out:
            raise ValueError("Duplicate EIDC nest-box key: "+str(k))
        out[k]={"site":site,"year":int(yr),"box":box,
                "hatch":int(hatch),"clutch":clutch}
    return out,{"candidate_source_nests":len(out),
                "source_nest_filter_exclusions":dict(excluded),
                "source_species_and_treatment_labels":dict(labels),
                "no_fledged_outcome_conditioning":True}


def link_nestlings(source_nests,source_chicks):
    members=defaultdict(list)
    excluded=Counter()
    ids=defaultdict(set)
    for r in source_chicks:
        year=numeric(r.get("year"))
        if year is None:
            excluded["invalid_nestling_year"]+=1;continue
        k=(str(r.get("site") or "").strip(),int(year),
           str(r.get("box") or "").strip())
        if k not in source_nests:
            excluded["no_admitted_blue_tit_nest_or_manipulated"]+=1
            continue
        mass=numeric(r.get("v1mass"))
        visit=numeric(r.get("v1date"))
        if mass is None or mass<=0 or visit is None:
            excluded["missing_or_nonpositive_v1_mass_date"]+=1
            continue
        delta=int(visit)-source_nests[k]["hatch"]
        if not (5<=delta<=9):
            excluded["v1_visit_outside_prespecified_day5_9"]+=1
            continue
        ring=str(r.get("ring") or "").strip()
        if ring and ring not in ("unringed","NA"):
            if ring in ids[k]:
                raise ValueError("Duplicate source nestling ring in first visit")
            ids[k].add(ring)
        members[k].append((mass,delta))
    nest={}
    for key,items in members.items():
        if len(items)<2:
            excluded["nest_has_fewer_than_two_v1_measured_chicks"]+=1
            continue
        nest[key]={**source_nests[key],
                   "n_chicks":len(items),
                   "mean_v1mass_g":sum(x for x,offset in items)/len(items),
                   "mean_first_visit_offset_days":
                       sum(offset for x,offset in items)/len(items)}
    return nest,{"original_nestling_rows":len(source_chicks),
                 "linked_nests_after_v1_and_age":len(nest),
                 "linked_nestling_v1_rows":sum(x["n_chicks"] for x in nest.values()),
                 "excluded":dict(excluded),
                 "not_conditioned_on_eventual_fledging":True}


def common_support(data, *, return_panel=False):
    nests,sourceqa=admit_source_nests(data["data/bird_phenology.csv"])
    linked,linkqa=link_nestlings(nests,data["data/nestlings.csv"])
    counts,_,_,_=resources(data["data/branch_beating.csv"])
    lower,upper,massqa=source_mass(data["data/branch_beating.csv"])
    source_sites=original_site_details(data["data/site_details.csv"])
    source_temp,tempqa=source_temperature(data["data/temperatures.csv"])
    admitted=defaultdict(list)
    support=Counter()
    for (site,yr,box),nest in linked.items():
        key=(site,yr)
        if key not in counts or key not in lower:
            support["no_source_count_mass_siteyear"]+=1
            continue
        if site not in source_sites or key not in source_temp:
            support["no_source_climate_or_geography"]+=1
            continue
        try:
            hatch=iso_day(yr,nest["hatch"])
            amounts=[]
            for source in (counts[key],lower[key],upper[key]):
                amounts.append(demand_window_contact(
                    source,hatch_date=hatch,duration_days=5,
                    max_observation_gap_days=8,min_coverage_fraction=1.0
                )["prey_mean_per_beating_during_demand_proxy"])
        except (ValueError,ResourceContactNotAdmitted):
            support["no_pre_visit_5day_full_food_support"]+=1
            continue
        if amounts[1]>amounts[2]:
            raise ValueError("Mass lower bound greater than upper")
        admitted[key].append({"box":box,"mean_v1mass_g":nest["mean_v1mass_g"],
                              "n_chicks":nest["n_chicks"],"mean_first_visit_offset_days":
                              nest["mean_first_visit_offset_days"],
                              "clutch":nest["clutch"],"hatch":nest["hatch"],
                              "count_5days":amounts[0],
                              "mass_5days_lower_g":amounts[1]/1000,
                              "mass_5days_upper_g":amounts[2]/1000})
    eligible_years=sorted({y for s,y in admitted})
    summary = {
        "status":"PAYOFF_B_SCOTLAND_NESTLING_V1MASS_RESOURCE_SOURCE_PREFIT",
        "record_units":"nestling first-visit body mass g, prey source g/standardized beating",
        "source_sha256_verified":True,
        "measurement_years_from_2017_only":True,
        "no_future_prey_after_visit_window":True,
        "outcome_coefficient_fitted":False,
        "bird_source":sourceqa,
        "nestling_source":linkqa,
        "mass_source":massqa,
        "temperature_source":tempqa,
        "contact_admission_exclusions":dict(support),
        "n_supported_nests":sum(len(rows) for rows in admitted.values()),
        "n_supported_nestling_v1_rows":
            sum(n["n_chicks"] for rows in admitted.values() for n in rows),
        "n_supported_siteyears":len(admitted),
        "n_supported_sites":len({s for s,y in admitted}),
        "n_supported_years":len(eligible_years),
        "supported_years":eligible_years,
        "nests_by_year":dict(Counter(str(y) for (s,y),rows in admitted.items() for n in rows)),
        "siteyears_by_year":dict(Counter(str(y) for (s,y) in admitted)),
        "source_gate_pass": (
            len(admitted)>=60 and len({s for s,y in admitted})>=20
            and len(eligible_years)>=3
            and sum(len(rows) for rows in admitted.values())>=150
            and sum(n["n_chicks"] for rows in admitted.values() for n in rows)>=400
        ),
        "no_fitness_or_biomass_conversion_effect_fitted":True,
    }
    if not return_panel:
        return summary
    panel=[]
    for (site,year),nests in sorted(admitted.items()):
        n=len(nests)
        if n==0:
            continue
        mean=lambda field:sum(z[field] for z in nests)/n
        events,_=daily_resource_rates(counts[(site,year)])
        peak=max(v for d,v in events)
        peakdate=min(d for d,v in events if v==peak)
        peak_doy=date.fromordinal(peakdate).timetuple().tm_yday
        hatch=mean("hatch")
        panel.append({
            "site":site,"year":year,"n_nests":n,
            "n_chicks":sum(z["n_chicks"] for z in nests),
            "y_mean_v1mass_g":mean("mean_v1mass_g"),
            "latitude":source_sites[site]["latitude"],
            "elevation":source_sites[site]["elevation"],
            "spring_temperature":source_temp[(site,year)]["spring_temperature"],
            "hatch_doy":hatch,
            "clutch_size":mean("clutch"),
            "v1_first_visit_age_proxy":mean("mean_first_visit_offset_days"),
            "log_season_peak":math.log1p(peak),
            "signed_peak_minus_hatch_days":peak_doy-hatch,
            "log_count_window5":math.log1p(mean("count_5days")),
            "log_mass_lower_window5":math.log1p(mean("mass_5days_lower_g")),
            "log_mass_upper_window5":math.log1p(mean("mass_5days_upper_g")),
        })
    if len(panel)!=summary["n_supported_siteyears"]:
        raise ValueError("Source support panel site-year count drift")
    return summary,panel


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    out=common_support(load_original())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(out,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
