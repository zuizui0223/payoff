#!/usr/bin/env python3
"""Frozen source-only screening of unopened avian GPS Movebank packages.

Cross-joins the exact original 446-parent DSpace, DataCite and GBIF ledgers.
Does not open animal trajectories, ecological outcomes or GPS positions.
"""
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
from collections import Counter

PREVIOUS=frozenset({
 "10.5441/001/1.v8d24552","10.5441/001/1.31c2v92f",
 "10.5441/001/1.715k46g2","10.5441/001/1.8764q39q",
 "10.5441/001/1.22kk5126","10.5441/001/1.695",
 "10.5441/001/1.3fv21n7m","10.5441/001/1.5d3f0664",
 "10.5441/001/1.5k6b1364","10.5441/001/1.ps244r11",
 "10.5441/001/1.137cn005"
})
CC0=re.compile(r"\bCC\s*0\b|CC0[-_ ]?1\.0|PUBLIC DOMAIN",re.I)
MIN_ANIMAL_COUNT=10
MIN_LOCATIONS=10000
QUEUE_LIMIT=8

def indexed(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:
        lines=list(csv.DictReader(f))
    ids=[r["doi"].strip().lower() for r in lines]
    if len(lines)!=446 or len(set(ids))!=446:
        raise ValueError("Must use exact original 446-parent inventory")
    return dict(zip(ids,lines))

def toks(s):
    return {x.strip().lower() for x in (s or "").split(";") if x.strip()}

def number(s):
    try:return int((s or "").replace(",","").strip())
    except (ValueError,TypeError):return None

def yes(s):
    return str(s).casefold().strip()=="true"

def decide(g,a,b,opened_studies,opened_papers):
    doi=g["doi"].strip().lower()
    if a["doi"].strip().lower()!=doi or b["doi"].strip().lower()!=doi:
        raise ValueError("Parent DOI mismatch across source records")
    study=toks(g.get("source_study_ids"))
    paper=toks(g.get("source_publications"))
    taxa=[x.strip() for x in (g.get("taxa_original") or "").split(";") if x.strip()]
    rights=" ".join((a.get("metadata_rights") or "",b.get("published_license") or "",b.get("rights_uri") or ""))
    count=number(g.get("source_animal_count"))
    loc=number(g.get("source_location_count"))
    why=[]
    if doi in PREVIOUS or g.get("previous_payoff_use")!="UNREVIEWED":
        why.append("PREVIOUSLY_OPENED_SOURCE_DOI")
    if study & opened_studies:why.append("SHARED_PRIOR_MOVEbank_STUDY_ID")
    if paper & opened_papers:why.append("SHARED_PRIOR_PUBLICATION_DOI")
    if not study:why.append("NO_RECORDED_STUDY_ID")
    if not paper:why.append("NO_RECORDED_PUBLICATION_DOI")
    if g.get("source_status")!="PUBLIC_ITEM_METADATA_PARSED":
        why.append("PUBLIC_ITEM_METADATA_UNVERIFIED")
    if g.get("class_scope")!="AVES_ONLY":why.append("NOT_EXCLUSIVELY_EXACT_AVES")
    if len(taxa)!=1:why.append("NOT_SINGLE_NAMED_BIRD_TAXON")
    if not yes(g.get("gps_child_filename_hint")):
        why.append("PUBLISHED_GPS_FILENAME_HINT_ABSENT")
    if not CC0.search(rights):why.append("EXPLICIT_CC0_METADATA_ABSENT")
    if count is None or count<MIN_ANIMAL_COUNT:
        why.append("PUBLISHER_ANIMAL_COUNT_INSUFFICIENT_OR_MISSING")
    if loc is None or loc<MIN_LOCATIONS:
        why.append("PUBLISHER_LOCATION_COUNT_INSUFFICIENT_OR_MISSING")
    return dict(
      doi=doi,scientific_name=taxa[0] if len(taxa)==1 else "; ".join(taxa),
      title=g.get("title") or "",study_ids="; ".join(sorted(study)),
      publication_dois="; ".join(sorted(paper)),
      reported_animals=count if count is not None else "",
      reported_locations=loc if loc is not None else "",
      original_license=b.get("published_license") or a.get("metadata_rights") or "",
      original_gps_name_hint=g.get("gps_child_filename_hint"),
      original_title_cue_tier=g.get("tier") or "",
      admission="PUBLIC_METADATA_QUEUE" if not why else "SOURCE_NOT_ADMITTED",
      reasons="; ".join(sorted(why)),
      actual_independent_animal_cohort_proven=False,
      source_event_permissions_verified=False,
      raw_GPS_file_verified=False,
      migration_stages_measured=False,
      predecision_information_or_fitness_tested=False,
    )

def build_queue(gbif,stage2,stage3):
    if gbif.keys()!=stage2.keys() or gbif.keys()!=stage3.keys():
        raise ValueError("Source DOI inventories differ")
    opened_studies=set()
    opened_papers=set()
    for doi in PREVIOUS:
        if doi in gbif:
            opened_studies |= toks(gbif[doi].get("source_study_ids"))
            opened_papers |= toks(gbif[doi].get("source_publications"))
    allrows=[decide(gbif[d],stage2[d],stage3[d],opened_studies,opened_papers)
             for d in sorted(gbif)]
    approved=[r for r in allrows if r["admission"]=="PUBLIC_METADATA_QUEUE"]
    # Ranking by published source coverage, never effect size or spring response.
    approved.sort(key=lambda x:(-x["reported_animals"],-x["reported_locations"],x["doi"]))
    queue=[]; seen_species=set();seen_study=set();seen_publication=set()
    for row in approved:
        if row["scientific_name"] in seen_species:continue
        if toks(row["study_ids"]) & seen_study:continue
        if toks(row["publication_dois"]) & seen_publication:continue
        queue.append(row)
        seen_species.add(row["scientific_name"])
        seen_study |= toks(row["study_ids"])
        seen_publication |= toks(row["publication_dois"])
        if len(queue)>=QUEUE_LIMIT:break
    receipt=dict(
      schema="payoff_b_movebank_unopened_bird_GPS_source_review_v1",
      source_doi_records=len(allrows),
      previously_opened_DOIs_present=sum(x in gbif for x in PREVIOUS),
      publisher_GPS_source_metadata_admitted=len(approved),
      first_distinct_taxon_study_paper_review_queue=len(queue),
      original_source_minimum_animals=MIN_ANIMAL_COUNT,
      original_source_minimum_locations=MIN_LOCATIONS,
      excluded_reasons_nonexclusive=dict(sorted(Counter(
          x for row in allrows for x in toks(row["reasons"])
      ).items())),
      ecological_results_read=False,
      independent_GPS_cohorts_verified=0,
      observed_decision_time_cues=0,
      no_selection_based_on_effect_sign=True,
    )
    return allrows,queue,receipt

def write_csv(rows,path):
    if not rows:raise ValueError("Empty original source ledger")
    with Path(path).open("w",encoding="utf-8",newline="") as h:
        writer=csv.DictWriter(h,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--gbif",required=True,type=Path)
    p.add_argument("--stage2",required=True,type=Path)
    p.add_argument("--stage3",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    rows,queue,receipt=build_queue(
        indexed(a.gbif),indexed(a.stage2),indexed(a.stage3))
    a.out.mkdir(parents=True,exist_ok=True)
    write_csv(rows,a.out/"all_446_independent_source_exclusions.csv")
    if queue:
        write_csv(queue,a.out/"first_8_original_CC0_bird_GPS_sources.csv")
    (a.out/"source_gate_summary.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    print("FROZEN_SOURCE_QUEUE")
    for row in queue:
        print(json.dumps({k:row[k] for k in (
            "doi","scientific_name","title","reported_animals",
            "reported_locations","original_license","publication_dois","study_ids"
        )},ensure_ascii=False))
    print("END_SOURCE_QUEUE")

if __name__=="__main__":main()
