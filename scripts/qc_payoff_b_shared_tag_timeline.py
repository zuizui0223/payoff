#!/usr/bin/env python3
"""Read-only published Movebank shared-tag deployment chronology audit.

Cross-check the surprising 35 shared tag IDs between two *distinct*
white-stork CC0 paper archives. Never publish original deployment dates,
tag IDs, animal IDs, GPS locations or individual survival events.
"""
from __future__ import annotations
import argparse,json,tempfile
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path

from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_public_movebank_stork_breeding_2018 import download_cc0
from scripts.qc_payoff_b_stork_cohort_overlap import (
    source_rows,compare_refs,key,NEW_REF,NEW_DOI,PREVIOUS_STORK_DOI,
)

EXPECTED_OVERLAPPING_TAGS=35
EXPECTED_OVERLAPPING_ANIMALS=0
DATETIME_KEYS=("deploy-on-date","deploy-off-date")


def parse_time(value):
    s=key(value)
    if not s:return None
    try:
        v=datetime.fromisoformat(s.replace("Z","+00:00"))
    except ValueError:
        return None
    if v.tzinfo:
        v=v.astimezone(timezone.utc).replace(tzinfo=None)
    return v


def tag_timeline(new,old):
    coll=compare_refs(new,old)["original_identifier_overlap_by_field"]
    if (coll["tag-id"]["overlapping_identifier_values"] != EXPECTED_OVERLAPPING_TAGS
            or coll["animal-id"]["overlapping_identifier_values"]!=EXPECTED_OVERLAPPING_ANIMALS):
        raise ValueError("Original shared-tag source identity changed")
    by_source=[]
    for rows in (new,old):
        m=defaultdict(list)
        for row in rows:
            tag=key(row.get("tag-id"))
            if tag:m[tag].append({
                "start":parse_time(row.get("deploy-on-date")),
                "end":parse_time(row.get("deploy-off-date")),
                "animal":key(row.get("animal-id")),
                "ring":key(row.get("animal-ring-id")),
            })
        by_source.append(m)
    shared=sorted(set(by_source[0])&set(by_source[1]))
    result=Counter()
    gap_days=[]
    for tag in shared:
        left,right=by_source[0][tag],by_source[1][tag]
        result["shared_tag_identifiers"]+=1
        if len(left)>1:result["new_source_tags_reused_in_multiple_deployments"]+=1
        if len(right)>1:result["prior_source_tags_reused_in_multiple_deployments"]+=1
        overlaps=False
        has_finite_comparison=False
        sequential=False
        for n in left:
            for o in right:
                if n["start"] and n["end"] and o["start"] and o["end"]:
                    has_finite_comparison=True
                    if max(n["start"],o["start"])<=min(n["end"],o["end"]):
                        overlaps=True
                    else:
                        sequential=True
                        gap=min(
                            abs((n["end"]-o["start"]).total_seconds()),
                            abs((o["end"]-n["start"]).total_seconds()),
                        )/86400
                        gap_days.append(gap)
        if has_finite_comparison:
            result["tag_ids_with_finite_deployment_periods"]+=1
        else:
            result["tag_ids_missing_comparable_on_off_dates"]+=1
        if overlaps:result["tag_ids_with_any_simultaneous_deployment_interval"]+=1
        if sequential and not overlaps:
            result["tag_ids_with_nonoverlapping_valid_deployment_interval"]+=1
    return {
        "original_published_shared_tag_ids":len(shared),
        "tag_timeline_status_counts":dict(sorted(result.items())),
        "observed_sequential_gap_days_aggregate":{
            "min":min(gap_days) if gap_days else None,
            "max":max(gap_days) if gap_days else None,
            "count_pairs":len(gap_days)
        },
        "same_tag_id_is_definitive_same_bird":False,
        "no_animal_ID_collision_is_definitive_independence":False,
        "same_tag_source_identifier_may_represent_hardware_reuse_or_an_identifier_policy":True,
        "source_bird_IDs_original_dates_or_sensitive_locations_exported":False
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,default=Path("outputs/payoff_b_tag_chronology"))
    a=ap.parse_args()
    report={"schema":"payoff_b_shared_stork_tag_timeline_20261022",
            "old_doi":PREVIOUS_STORK_DOI,"new_doi":NEW_DOI}
    try:
        with tempfile.TemporaryDirectory() as temp:
            pnew=Path(temp)/"new.csv"
            pold=Path(temp)/"old.csv"
            report["checksum_new"]=download_verified(NEW_REF,pnew)
            report["checksum_prior"]=download_cc0("reference",pold)
            new,old=source_rows(pnew),source_rows(pold)
            report["aggregate_tag_timeline"]=tag_timeline(new,old)
            report["status"]="SHARED_TAG_DEPLOYMENT_CHRONOLOGY_QC_COMPLETE"
    except (ValueError,OSError,TypeError) as e:
        report["status"]="SOURCE_OR_DEPLOYMENT_TIMELINE_FAILED"
        report["error"]=type(e).__name__+": "+str(e)[:300]
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"two_white_stork_cohorts.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if report["status"]!="SHARED_TAG_DEPLOYMENT_CHRONOLOGY_QC_COMPLETE":
        raise SystemExit("Original shared tag chronology not verified")

if __name__=="__main__":main()
