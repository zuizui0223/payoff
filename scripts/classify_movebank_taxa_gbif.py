#!/usr/bin/env python3
"""Classify 446 Movebank publisher packages using GBIF, source metadata only."""
from __future__ import annotations
import argparse,csv,hashlib,json,re,time,urllib.request,urllib.parse,urllib.error
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

SHA_PARENT="a5bbc929c878367012c108f09996b8547bc9b70da8d52180b072ec6561f68d14"
SHA_CHILD="03cca4393d767fa1cc1538f0a0c32734911273b8500956829828430f352ba974"
GPS=re.compile(r"(?i)(?:^|[-_ /])(?:gps|gnss)(?:$|[-_ /.])")
REPRO=re.compile(r"(?i)(?:^|[-_ /])(?:breeding|fledglings?|reproduction|jae.meta.data)(?:$|[-_ /.])")

def csv_verified(path,sha):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:
        raise ValueError("Source SHA256 mismatch: "+path.name)
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def values(text):
    return [x.strip() for x in (text or "").split(";") if x.strip()]

def classify(name,fetch=None):
    if fetch is None:fetch=fetch_gbif
    try:
        data=fetch(name)
        typ=str(data.get("matchType") or "")
        rank=str(data.get("rank") or "")
        conf=int(data.get("confidence") or 0)
        cl=str(data.get("class") or "")
        valid=(typ=="EXACT" and rank in ("SPECIES","SUBSPECIES")
               and conf>=90 and bool(cl) and bool(data.get("kingdom")))
        return dict(name=name,status="EXACT_CLASS" if valid else "UNRESOLVED",
                    class_name=cl if valid else "",rank=rank,match_type=typ,
                    confidence=conf,usage_key=data.get("usageKey") or "",error="")
    except Exception as e:
        return dict(name=name,status="UNRESOLVED",class_name="",rank="",
                    match_type="",confidence="",usage_key="",
                    error=type(e).__name__+": "+str(e)[:120])

def fetch_gbif(name):
    if not name or len(name)>240:raise ValueError("invalid original name")
    url="https://api.gbif.org/v1/species/match?"+urllib.parse.urlencode(
        {"name":name,"strict":"true"})
    req=urllib.request.Request(url,headers={"Accept":"application/json",
        "User-Agent":"PAYOFF-B-Movebank-GBIF-source/1.0"})
    error=None
    for i in range(3):
        try:
            with urllib.request.urlopen(req,timeout=25) as res:
                if urllib.parse.urlsplit(res.geturl()).hostname!="api.gbif.org":
                    raise ValueError("unexpected taxonomy host")
                return json.load(res)
        except (OSError,ValueError,TimeoutError) as e:
            error=e
            if i<2:time.sleep(i+1)
    raise RuntimeError(str(error)[:160])

def enrich(parents,children,tax):
    child_titles=defaultdict(list)
    for c in children:child_titles[c["parent_doi"]].append(c["title_hint"])
    rows=[]
    for p in parents:
        names=values(p["taxon_scientific_names"])
        good={tax[n]["class_name"] for n in names if tax[n]["status"]=="EXACT_CLASS"}
        bad=[n for n in names if tax[n]["status"]!="EXACT_CLASS"]
        birds="Aves" in good
        scope=("NO_TAXON" if not names else "PARTIAL_CLASS" if bad
               else "AVES_ONLY" if birds and len(good)==1 else
               "AVES_MIXED" if birds else "NON_AVES")
        gps_title=any(GPS.search(x) for x in child_titles[p["doi"]])
        gps_sensor=bool(re.search(r"\b(?:GPS|GNSS)\b",p["sensor_names"],re.I))
        rows.append(dict(doi=p["doi"],title=p["title"],
             tier=p["metadata_screen_tier"],source_status=p["source_status"],
             taxa_original=p["taxon_scientific_names"],
             classes_verified="; ".join(sorted(good)),
             names_unresolved="; ".join(bad),class_scope=scope,
             aves_taxon_confirmed=birds,
             source_animal_count=p["n_published_animals"],
             source_location_count=p["n_published_locations"],
             source_study_ids=p["dspace_study_ids"],
             source_publications=p["linked_publication_dois"],
             previous_payoff_use=p["prior_payoff_source_flag"],
             sensor_names=p["sensor_names"],gps_sensor_hint=gps_sensor,
             gps_child_filename_hint=gps_title,
             reproduction_child_filename_hint=any(REPRO.search(x) for x in child_titles[p["doi"]]),
             either_gps_hint=gps_title or gps_sensor,
             raw_events_verified=False,independent_cohort_verified=False,
             cue_timing_or_fitness_tested=False))
    return rows

def summary(rows,taxa):
    t1=[x for x in rows if x["tier"]=="T1_CUE_AND_DECISION_METADATA"]
    aves=[x for x in rows if x["aves_taxon_confirmed"]]
    classes=Counter()
    for x in rows:
        classes.update(values(x["classes_verified"]))
    return dict(schema="payoff_b_movebank_taxonomic_gbif_source_screen_v1",
        source_metadata_only=True,packages=len(rows),
        original_taxon_labels=len(taxa),
        exact_class_resolved=sum(x["status"]=="EXACT_CLASS" for x in taxa),
        unresolved_taxon_labels=sum(x["status"]!="EXACT_CLASS" for x in taxa),
        package_class_mentions=dict(sorted(classes.items())),
        package_scope=dict(sorted(Counter(x["class_scope"] for x in rows).items())),
        aves_packages=len(aves),t1_title_hints=len(t1),
        aves_t1_packages=sum(x["aves_taxon_confirmed"] for x in t1),
        t1_unverified_aves=sum(not x["aves_taxon_confirmed"] for x in t1),
        gps_sensor_packages=sum(x["gps_sensor_hint"] for x in rows),
        gps_child_hint_packages=sum(x["gps_child_filename_hint"] for x in rows),
        either_gps_hint_packages=sum(x["either_gps_hint"] for x in rows),
        aves_any_gps_hint=sum(x["either_gps_hint"] for x in aves),
        aves_t1_any_gps_hint=sum(x["aves_taxon_confirmed"] and x["either_gps_hint"] for x in t1),
        aves_gps_child_without_gps_sensor=sum(x["aves_taxon_confirmed"] and x["gps_child_filename_hint"] and not x["gps_sensor_hint"] for x in rows),
        raw_tracking_sample_size="NOT_ESTIMATED",
        ecological_cue_action_effect="NOT_TESTED",
        source_parent_sha256=SHA_PARENT,source_child_sha256=SHA_CHILD)

def write_csv(path,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--parents",type=Path,required=True)
    a.add_argument("--children",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    q=a.parse_args()
    p=csv_verified(q.parents,SHA_PARENT);c=csv_verified(q.children,SHA_CHILD)
    if len(p)!=446 or len({r["doi"] for r in p})!=446:
        raise ValueError("446 frozen parent DOI source mismatch")
    if any(r["parent_doi"] not in {v["doi"] for v in p} for r in c):
        raise ValueError("child DOI points to unknown parent")
    names=sorted({x for r in p for x in values(r["taxon_scientific_names"])})
    results={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        fs={pool.submit(classify,n):n for n in names}
        for f in as_completed(fs):results[fs[f]]=f.result()
    taxa=[results[n] for n in names]
    rows=enrich(p,c,results);s=summary(rows,taxa)
    q.out.mkdir(parents=True,exist_ok=True)
    write_csv(q.out/"gbif_name_classes.csv",taxa)
    write_csv(q.out/"movebank_446_taxon_sensor_source_candidates.csv",rows)
    (q.out/"gbif_source_summary.json").write_text(
        json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(s,ensure_ascii=False,indent=2))
    if s["exact_class_resolved"]<int(len(taxa)*0.75):
        raise SystemExit("taxonomy exact-class recovery below 75%")

if __name__=="__main__":main()
