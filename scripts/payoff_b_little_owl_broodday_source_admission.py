"""PAYOFF-B Little Owl: pre-fit brood-day provenance, units and missingness audit.

Original Sailas et al. 2025/26 Zenodo 17521558. Data source is used as
a prior-art / measurement-conversion calibration, not a new ecological claim.
No outcome coefficient fits. No feeding->fitness because no fitness recorded.
"""
import argparse, csv, hashlib, io, json, math
from collections import Counter, defaultdict
from pathlib import Path
from scripts.payoff_b_scotland_resource_source_probe import open_url

RID=17521558
API=f"https://zenodo.org/api/records/{RID}"
ORIGINAL_SHA256={
    "Littleowl.dat.JAB.csv":"75042cdbd0f4019519b51ea1273ebbf8a736712f43fa7024361d969d752b0928",
    "all_hab_vars.csv":"8fcbaee54b4a8af215b7952e6cad2d5fc5fce47917f2e296ef87d4421ef028c3",
}
IMPORTANT_FIELDS=[
 "country","country2","broodID","nestID","Year","day","age","prov_rate",
 "number_juv.x","temp","humid","rain","wind","mammal","bird","insect",
 "earthworms","other","BM","prop.day.monitored","prov_rate2","BM2",
]
HAB_FIELDS=["nestID","Field area","Grassland area","Orchard area",
            "Hedges area","Garden area","country3"]

def parse_number(s):
    try:
        if s is None or str(s).strip()=="" or str(s).strip().lower() in ("na","nan","null"):
            return None
        x=float(s)
        return x if math.isfinite(x) else None
    except (TypeError,ValueError):
        return None

def download_original():
    z=open_url(API,timeout=50,max_read=1_500_000)
    raw=z.get("body")
    if z.get("http_status")!=200 or not raw:
        raise ValueError("Zenodo original metadata not admitted")
    record=json.loads(raw)
    available={f.get("key"):f for f in record.get("files",[])}
    result={}
    for name,digest in ORIGINAL_SHA256.items():
        f=available.get(name)
        if not f:
            raise ValueError("Missing original Zenodo named source file: "+name)
        url=f.get("links",{}).get("self")
        size=f.get("size")
        if not url or not isinstance(size,int) or size>2_000_000 or size<=0:
            raise ValueError("Source size/link contract violation: "+name)
        response=open_url(url,max_read=size,timeout=45)
        file=response.get("body")
        if response.get("http_status")!=200 or file is None or len(file)!=size:
            raise ValueError("Original file unavailable, size drift: "+name)
        if hashlib.sha256(file).hexdigest()!=digest:
            raise ValueError("Original verified Zenodo CSV SHA256 drift: "+name)
        source_hash=f.get("checksum") or ""
        if not source_hash.startswith("md5:") or hashlib.md5(file).hexdigest()!=source_hash[4:]:
            raise ValueError("Zenodo original MD5 not verified: "+name)
        try:
            text=file.decode("utf-8-sig",errors="strict")
        except UnicodeDecodeError:
            text=file.decode("cp1252")
        result[name]=list(csv.DictReader(io.StringIO(text,newline="")))
    return result

def source_counts(data):
    provision=data["Littleowl.dat.JAB.csv"]
    habitat=data["all_hab_vars.csv"]
    if not provision or not habitat:
        raise ValueError("Empty source")
    if not set(IMPORTANT_FIELDS).issubset(provision[0]):
        raise ValueError("Unexpected original data schema / missing source fields")
    if not set(HAB_FIELDS).issubset(habitat[0]):
        raise ValueError("Missing original source habitat covariates")
    bynest={}
    for row in habitat:
        k=(row.get("nestID") or "").strip()
        if not k or k in bynest:
            raise ValueError("Duplicate or absent source nest habitat ID")
        bynest[k]=row
    missing=Counter()
    bad=Counter()
    year=Counter()
    country=Counter()
    nests=set()
    broods=set()
    keys=set()
    admitted=[]
    observed=Counter()
    for row in provision:
        nid=(row.get("nestID") or "").strip()
        brood=(row.get("broodID") or "").strip()
        yr=(row.get("Year") or "").strip()
        day=(row.get("day") or "").strip()
        place=(row.get("country") or "").strip()
        if not nid or not brood or not yr or not day or not place:
            bad["missing_primary_brood_day_key"]+=1
            continue
        k=(brood,day)
        if k in keys:
            bad["duplicate_brood_day"]+=1
            continue
        keys.add(k)
        if nid not in bynest:
            bad["no_exact_habitat_nest"]+=1
            continue
        for f in IMPORTANT_FIELDS:
            if parse_number(row.get(f)) is None and f not in (
               "country","country2","broodID","nestID","Year","day"
            ):
                missing[f]+=1
        age=parse_number(row.get("age"))
        chicks=parse_number(row.get("number_juv.x"))
        visits=parse_number(row.get("prov_rate"))
        mass=parse_number(row.get("BM"))
        fraction=parse_number(row.get("prop.day.monitored"))
        adjvisit=parse_number(row.get("prov_rate2"))
        adjmass=parse_number(row.get("BM2"))
        if age is None or not (1<=age<=31):
            bad["invalid_age"]+=1;continue
        if chicks is None or chicks<=0:
            bad["invalid_chick_count"]+=1;continue
        if visits is None or mass is None or visits<0 or mass<0:
            bad["missing_negative_visits_or_mass"]+=1;continue
        if fraction is None or not(0<fraction<=1):
            bad["invalid_observation_fraction"]+=1;continue
        if adjvisit is None or adjmass is None or adjvisit<0 or adjmass<0:
            bad["missing_adjusted_rate_mass"]+=1;continue
        if visits==0 and mass>0:
            bad["mass_without_visits"]+=1;continue
        rate_mismatch=abs(adjvisit-visits/fraction)
        mass_mismatch=abs(adjmass-mass/fraction)
        if rate_mismatch>max(1e-3, 0.02*max(1,adjvisit)):
            observed["visit_adjustment_not_exact"]+=1
        if mass_mismatch>max(1e-3, 0.02*max(1,adjmass)):
            observed["mass_adjustment_not_exact"]+=1
        nests.add(nid);broods.add(brood);year[yr]+=1;country[place]+=1
        admitted.append(row)
    bybrood=Counter(x["broodID"] for x in admitted)
    unique_broods_by_nest=defaultdict(set)
    for x in admitted:
        unique_broods_by_nest[x["nestID"]].add(x["broodID"])
    summary={
        "status":"PAYOFF_B_LITTLE_OWL_ORIGINAL_BROOD_DAY_SUPPORT_PREFIT",
        "original_zenodo_id":RID,
        "source_csv_sha256":ORIGINAL_SHA256,
        "source_rows":len(provision),
        "habitat_rows":len(habitat),
        "admitted_brood_day_rows":len(admitted),
        "n_admitted_nests":len(nests),
        "n_admitted_broods":len(broods),
        "unique_years":len(year),
        "year_rows":dict(sorted(year.items())),
        "country_rows":dict(sorted(country.items())),
        "days_per_brood_min":min(bybrood.values()) if bybrood else None,
        "days_per_brood_median":sorted(bybrood.values())[len(bybrood)//2] if bybrood else None,
        "days_per_brood_max":max(bybrood.values()) if bybrood else None,
        "reused_nests_across_broods":sum(len(v)>1 for v in unique_broods_by_nest.values()),
        "field_missing_count":dict(missing),
        "excluded_or_duplicated":dict(bad),
        "source_rate_normalization_qc":dict(observed),
        "all_4_countries":len(country)>=4,
        "all_input_variables_are_real_source_values":True,
        "food_mass_is_original_estimated_delivery_not_actual_ingested_energy":True,
        "source_study_has_fitness_outcomes":False,
        "published_paper_already_tested_habitat_weather_delivery":True,
        "no_new_effect_fitted":True
    }
    summary["ready_for_separate_brood_holdout_measurement_diagnostic"]=(
        len(admitted)>=500 and len(broods)>=30 and len(nests)>=20
        and len(country)>=3 and len(year)>=4 and bad["duplicate_brood_day"]==0
    )
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    d=source_counts(download_original())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(d,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
