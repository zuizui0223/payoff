#!/usr/bin/env python3
"""Census Movebank's public *package* taxon, sensor and cohort metadata.

This reads DSpace item JSON only. No GPS or animal events are downloaded.
A metadata animal count is not a verified count of independent biological
replicates. The input is the COMPLETE DataCite parent package registry.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HOST="datarepository.movebank.org"
ITEM_PREFIX=f"https://{HOST}/server/api/core/items/"
UUID=re.compile(r"/entities/datapackage/([0-9a-fA-F-]{36})(?:/|$)")
RETRIES=3
WORKERS=3
MAX_PACKAGES=1000

def _request(url):
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme!="https" or parsed.hostname != HOST:
        raise ValueError("Request host outside verified public Movebank repository")
    req=urllib.request.Request(url,headers={
        "User-Agent":"PAYOFF-B-source-ecology-inventory/0.1",
        "Accept":"application/json,text/html",
    })
    with urllib.request.urlopen(req,timeout=65) as response:
        final=response.geturl()
        parsed2=urllib.parse.urlsplit(final)
        if parsed2.scheme!="https" or parsed2.hostname!=HOST:
            raise ValueError("Redirect to unapproved host")
        if parsed.path.startswith("/server/api/"):
            body=response.read(3_000_000)
            return final,json.loads(body)
        return final,None

def canonical_landing(url):
    value=(url or "").strip()
    parsed=urllib.parse.urlsplit(value)
    if parsed.scheme!="https" or parsed.hostname not in (HOST,"www."+HOST):
        raise ValueError("DataCite landing URL not on official Movebank")
    if not (parsed.path.startswith("/handle/10255/") or
            parsed.path.startswith("/entities/datapackage/")):
        raise ValueError("Unknown package landing pattern")
    return urllib.parse.urlunsplit(("https",HOST,parsed.path,"",""))

def final_uuid(url):
    p=urllib.parse.urlsplit(url)
    match=UUID.search(p.path)
    if match:
        return match.group(1).lower()
    final,_=_request(url)
    match=UUID.search(urllib.parse.urlsplit(final).path)
    if not match:
        raise ValueError("Handle did not resolve to a DSpace datapackage UUID")
    return match.group(1).lower()

def attempt(fn):
    last=None
    for trial in range(RETRIES):
        try:
            return fn()
        except (urllib.error.HTTPError,urllib.error.URLError,OSError,ValueError,
                json.JSONDecodeError) as exc:
            last=exc
            if trial<RETRIES-1:
                time.sleep(1.5*(trial+1))
    raise RuntimeError(type(last).__name__+": "+str(last)[:180])

def values(meta,key):
    entries=meta.get(key) or []
    if not isinstance(entries,list):
        return []
    return sorted(set(str(x.get("value","")).strip() for x in entries
                      if isinstance(x,dict) and str(x.get("value","")).strip()))

def numeric_field(meta,key):
    candidates=values(meta,key)
    if len(candidates)!=1:
        return None
    s=candidates[0].replace(",","")
    return int(s) if s.isdecimal() else None

def doi_from_item(metadata):
    vals=values(metadata,"dc.identifier.doi")
    return {re.sub(r"^(doi:|https?://doi\.org/)", "",v,flags=re.I).lower()
            for v in vals}

def parse_item(attrs,item):
    if not isinstance(item,dict) or not isinstance(item.get("metadata"),dict):
        raise ValueError("No DSpace item metadata")
    meta=item["metadata"]
    declared=doi_from_item(meta)
    doi=attrs["doi"].lower()
    if declared and doi not in declared:
        raise ValueError("DataCite parent DOI does not match DSpace source item DOI")
    return {
        "doi":doi,
        "title":attrs["title"],
        "metadata_screen_tier":attrs["metadata_screen_tier"],
        "linked_publication_dois":attrs["linked_publication_dois"],
        "prior_payoff_source_flag":attrs["prior_payoff_source_flag"],
        "dspace_item_uuid":str(item.get("uuid") or item.get("id") or ""),
        "dspace_study_ids":"; ".join(values(meta,"mdr.study.id")),
        "taxon_scientific_names":"; ".join(values(meta,"dwc.ScientificName")),
        "n_taxon_names":len(values(meta,"dwc.ScientificName")),
        "sensor_names":"; ".join(values(meta,"sensor.name")),
        "n_published_animals":numeric_field(meta,"mdr.animal.count"),
        "n_published_locations":numeric_field(meta,"mdr.location.count"),
        "dspace_package_type":"; ".join(values(meta,"dspace.entity.type")),
        "published_license":"; ".join(values(meta,"dc.rights")),
        "rights_uri":"; ".join(values(meta,"dc.rights.uri")),
        "doi_consistency":("MATCHED" if declared else "NOT_LISTED"),
        "study_independence_verified":False,
        "movement_decisions_extracted":False,
        "cue_chronology_verified":False,
        "fitness_association_estimated":False,
        "source_status":"PUBLIC_ITEM_METADATA_PARSED",
        "source_error":"",
    }

def process_parent(row):
    time.sleep(0.12) # modest per-request courtesy spacing
    try:
        url=canonical_landing(row["metadata_landing_url"])
        uuid=attempt(lambda:final_uuid(url))
        _,obj=attempt(lambda:_request(ITEM_PREFIX+uuid))
        result=parse_item(row,obj)
        if result["dspace_item_uuid"] and result["dspace_item_uuid"].lower()!=uuid:
            raise ValueError("DSpace item UUID identity mismatch")
        return result
    except Exception as e:
        return {
            "doi":row["doi"],"title":row["title"],
            "metadata_screen_tier":row["metadata_screen_tier"],
            "linked_publication_dois":row["linked_publication_dois"],
            "prior_payoff_source_flag":row["prior_payoff_source_flag"],
            "dspace_item_uuid":"","dspace_study_ids":"",
            "taxon_scientific_names":"","n_taxon_names":0,
            "sensor_names":"","n_published_animals":None,
            "n_published_locations":None,"dspace_package_type":"",
            "published_license":"","rights_uri":"","doi_consistency":"UNAVAILABLE",
            "study_independence_verified":False,
            "movement_decisions_extracted":False,
            "cue_chronology_verified":False,
            "fitness_association_estimated":False,
            "source_status":"SOURCE_NOT_VERIFIED",
            "source_error":type(e).__name__+": "+str(e)[:160]
        }

def _numeric_distribution(rows,key):
    vals=[x[key] for x in rows if isinstance(x.get(key),int)]
    if not vals:return {"count":0}
    vals=sorted(vals)
    return {
        "count":len(vals),
        "min":vals[0],
        "median":statistics.median(vals),
        "max":vals[-1],
    }

def summarise(rows):
    accepted=[r for r in rows if r["source_status"]=="PUBLIC_ITEM_METADATA_PARSED"]
    taxa=Counter()
    sensors=Counter()
    studies=defaultdict(list)
    for row in accepted:
        for tx in row["taxon_scientific_names"].split("; "):
            if tx:taxa[tx]+=1
        for sensor in row["sensor_names"].split("; "):
            if sensor:sensors[sensor]+=1
        for study in row["dspace_study_ids"].split("; "):
            if study:studies[study].append(row["doi"])
    tiers=Counter(x["metadata_screen_tier"] for x in rows)
    identified=sum(bool(x["taxon_scientific_names"]) for x in accepted)
    return {
        "schema":"payoff_b_complete_movebank_taxon_sensor_census_v1",
        "status":"COMPLETE" if len(accepted)==len(rows) else "PARTIAL",
        "parent_dois":len(rows),
        "item_metadata_verified":len(accepted),
        "item_metadata_not_verified":len(rows)-len(accepted),
        "stage2_tier_counts":dict(sorted(tiers.items())),
        "packages_with_taxon_name":identified,
        "unique_scientific_name_strings":len(taxa),
        "top_taxon_name_metadata_mentions":[{"name":a,"packages":b}
                                            for a,b in taxa.most_common(15)],
        "sensor_metadata_counts":dict(sorted(sensors.items())),
        "reported_animal_count_distribution":_numeric_distribution(accepted,"n_published_animals"),
        "reported_location_count_distribution":_numeric_distribution(accepted,"n_published_locations"),
        "unique_movebank_study_id_strings":len(studies),
        "study_id_shared_by_multiple_parent_dois":sum(len(v)>1 for v in studies.values()),
        "study_id_reused_parent_doi_count":len(set(
            doi for v in studies.values() if len(v)>1 for doi in v
        )),
        "t1_with_confirmed_scientific_names":sum(
            r["metadata_screen_tier"]=="T1_CUE_AND_DECISION_METADATA"
            and bool(r["taxon_scientific_names"]) for r in accepted
        ),
        "source_level_unverified_reasons":Counter(
            r["source_error"].split(":")[0] for r in rows
            if r["source_status"]!="PUBLIC_ITEM_METADATA_PARSED"
        ),
        "independent_biological_studies_count":"NOT_ESTIMABLE",
        "independent_taxon_samples_count":"NOT_ESTIMABLE",
        "limitations":[
            "ScientificName and sensor fields are publisher metadata, not verified per-event records.",
            "A single package can contain many animals or taxa; the same animals can appear in multiple packages.",
            "Animal and location counts are publisher metadata, not independently verified totals; do not sum as independent samples.",
            "Shared Movebank study IDs and publication DOIs flag potential dependence, not proof of identical cohorts.",
            "T1 is a text-search tier; it may contain mammal or other nonbird taxa.",
            "No bird response, spring cue, travel action, stopover or fitness outcome was analyzed.",
        ],
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",required=True,type=Path)
    ap.add_argument("--output-dir",required=True,type=Path)
    args=ap.parse_args()
    with args.input.open(encoding="utf-8",newline="") as f:
        parents=list(csv.DictReader(f))
    if not parents or len(parents)>MAX_PACKAGES or len({x["doi"] for x in parents})!=len(parents):
        raise ValueError("No valid nonduplicated Movebank parent DOI input")
    rows=[]
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures=[pool.submit(process_parent,row) for row in parents]
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda r:r["doi"])
    args.output_dir.mkdir(parents=True,exist_ok=True)
    with (args.output_dir/"movebank_taxon_sensor_source_registry.csv").open(
        "w",encoding="utf-8",newline=""
    ) as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary=summarise(rows)
    (args.output_dir/"movebank_taxon_sensor_census_receipt.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if summary["item_metadata_verified"] < int(len(rows)*0.90):
        raise SystemExit("Less than 90 percent of public item metadata was resolvable")

if __name__=="__main__":
    main()
