#!/usr/bin/env python3
"""Movebank CC0 cross-taxon GPS source audit. Never export raw IDs/locations.

This audits *availability*, NOT biological information-use or fitness effects.
Frozen original source files are checked by length + MD5 before parsing.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,tempfile,urllib.request
from pathlib import Path
from datetime import datetime
from collections import Counter,defaultdict

ROOT="https://datarepository.movebank.org/server/api/core/bitstreams/"
SOURCES={
 "bean_goose":dict(doi="10.5441/001/1.22kk5126",taxon="Anser fabalis",
     paper="10.1186/s40462-021-00284-4",
     context="moult_migration_not_spring_breeding",
     uuid="73f3b9a0-ac55-42b8-89d9-f08e996428df",
     md5="1dbba0044dea9e42f69a07cdee6fb1e4",size=152683274),
 "curlew":dict(doi="10.5441/001/1.715k46g2",taxon="Numenius arquata",
     paper="10.1186/s40462-021-00252-y",
     context="spring_departure_partial_route_prior_art",
     uuid="fb34f30f-9cac-4b92-b901-7e4e099deab8",
     md5="b847a97e4ebaedd3e2fd46e920c4f08e",size=159155287),
 "steppe_eagle":dict(doi="10.5441/001/1.695",taxon="Aquila nipalensis",
     paper="10.1016/j.cub.2025.07.061",
     context="age_and_anthropogenic_route_prior_art",
     uuid="3eda5fa0-7266-4d03-91d1-a1f67129775b",
     md5="eb3d377503c9d7fada00b07c9ff95675",size=111170648)
}
SEASONS={"winter":{12,1,2},"spring":{3,4,5},
         "summer":{6,7,8},"autumn":{9,10,11}}
MIN_DATES=10
ID_FIELDS=("individual-local-identifier","deployment-id","tag-local-identifier")
REQUIRED={"timestamp","location-lat","location-long"}

def download_verified(s,path):
    req=urllib.request.Request(ROOT+s["uuid"]+"/content",headers={
        "User-Agent":"PAYOFF-B-CC0-independent-source-readonly/1.0"})
    h=hashlib.md5();n=0
    with urllib.request.urlopen(req,timeout=120) as r,Path(path).open("wb") as f:
        if not r.geturl().startswith(ROOT):
            raise ValueError("unapproved source redirect")
        while True:
            chunk=r.read(1024*1024)
            if not chunk:break
            n+=len(chunk)
            if n>s["size"]+8192:raise ValueError("source too large")
            h.update(chunk);f.write(chunk)
    if n!=s["size"] or h.hexdigest()!=s["md5"]:
        raise ValueError("pinned original MD5 or length mismatch")
    return dict(bytes=n,md5=h.hexdigest(),original_source_verified=True)

def audit(path):
    rows=0;counts=Counter();years=Counter();animals=Counter()
    observed_years=defaultdict(set);dates=defaultdict(set)
    all_identity_years=set();sensor=Counter();id_field=None
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        reader=csv.DictReader(f);fields=reader.fieldnames or []
        if not REQUIRED.issubset(fields):
            raise ValueError("missing fields "+str(sorted(REQUIRED-set(fields))))
        id_field=next((x for x in ID_FIELDS if x in fields),None)
        if id_field is None:raise ValueError("no source animal/deployment/tag ID")
        for event in reader:
            rows+=1
            ident=(event.get(id_field) or "").strip()
            if not ident:counts["missing_id"]+=1;continue
            try:
                dt=datetime.fromisoformat((event.get("timestamp") or "").strip().replace("Z","+00:00"))
            except (TypeError,ValueError):
                counts["bad_time"]+=1;continue
            try:
                lat=float(event.get("location-lat") or "")
                lon=float(event.get("location-long") or "")
                if not math.isfinite(lat) or not math.isfinite(lon) or not -90<=lat<=90 or not -180<=lon<=180:
                    raise ValueError("invalid position")
            except (TypeError,ValueError):
                counts["bad_position"]+=1;continue
            counts["valid"]+=1;years[dt.year]+=1;animals[ident]+=1
            observed_years[ident].add(dt.year)
            all_identity_years.add((ident,dt.year))
            if "sensor-type" in fields:
                sensor[(event.get("sensor-type") or "UNKNOWN").strip()]+=1
            for name,ms in SEASONS.items():
                if dt.month in ms:
                    dates[(ident,dt.year,name)].add(dt.date())
    if rows==0:raise ValueError("zero rows")
    cover=Counter();spring_autumn=spring_winter=0
    for ident,year in all_identity_years:
        c={name:len(dates.get((ident,year,name),set()))>=MIN_DATES for name in SEASONS}
        cover.update(name for name,v in c.items() if v)
        spring_autumn+=int(c["spring"] and c["autumn"])
        spring_winter+=int(c["spring"] and c["winter"])
    return dict(
        original_rows=rows,valid_identified_georeferenced_fixes=counts["valid"],
        missing_identity_rows=counts["missing_id"],
        invalid_timestamp_rows=counts["bad_time"],
        invalid_position_rows=counts["bad_position"],
        id_column=id_field,
        id_is_animal_not_tag=(id_field=="individual-local-identifier"),
        unique_identity_labels=len(animals),
        labels_observed_in_multiple_years=sum(len(v)>=2 for v in observed_years.values()),
        identity_calendar_years=len(all_identity_years),
        source_calendar_year_counts={str(k):v for k,v in sorted(years.items())},
        years_covered=len(years),
        ten_day_calendar_season_identity_years=dict(sorted(cover.items())),
        same_year_spring_and_autumn=spring_autumn,
        same_year_spring_and_winter=spring_winter,
        observed_sensor_type_counts=dict(sorted(sensor.items())),
        season_threshold_days=MIN_DATES,
        season_months_are_migration_stages=False,
        actual_route_stage_or_stopover=False,
        decision_time_environmental_information_measured=False,
        correction_opportunity_measured=False,
        biological_fitness_response_measured=False,
        raw_ids_and_coordinates_exported=False)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--system",required=True,choices=sorted(SOURCES))
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_crossguild"))
    a=p.parse_args();s=SOURCES[a.system]
    result=dict(system=a.system,source_doi=s["doi"],paper_doi=s["paper"],
                species=s["taxon"],context=s["context"],license="CC0-1.0",
                cohort_independence="NOT_VERIFIED",
                ecological_hypothesis="NOT_TESTED")
    try:
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"source.csv"
            result["checksum"]=download_verified(s,path)
            result["coverage"]=audit(path)
            result["status"]="SOURCE_COVERAGE_VERIFIED"
    except (OSError,ValueError) as e:
        result["status"]="SOURCE_ADMISSION_FAILED"
        result["error"]=type(e).__name__+": "+str(e)[:270]
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if result["status"]!="SOURCE_COVERAGE_VERIFIED":
        raise SystemExit("source validation failed")
if __name__=="__main__":main()
