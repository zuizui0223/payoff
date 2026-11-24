#!/usr/bin/env python3
"""Original CC0 Movebank study-relative tag/animal/deployment key audit.

Uses original three small SHA-pinned archived reference CSVs only. This
diagnostic opens no GPS/ACC files, returns no tag, animal, deployment IDs,
record rows or positions, and never asserts cross-study identity equivalence.
"""
from __future__ import annotations
import argparse,csv,io,json,sys
from collections import Counter,defaultdict
from pathlib import Path
from hashlib import sha256

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_stork_deployment_time_gate_20261124 import bounded_cc0_csv

DEFAULT_CONTRACT=HERE.parent/"data/payoff_b_stork_id_join_semantics_contract_20261124.json"
DEFAULT_INPUT=HERE.parent/"data/payoff_b_stork_deployment_time_contract_20261124.json"
FIELDS=["tag-id","animal-id","deployment-id"]

def read_reference_ids(raw,n):
    rdr=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if not set(FIELDS+["deploy-on-date","deploy-off-date"]).issubset(rdr.fieldnames or []):
        raise ValueError("Original Movebank identity fields are not all present")
    rows=list(rdr)
    if len(rows)!=n:
        raise ValueError("Source row identity grain changed")
    return [{f:str(row.get(f) or "").strip() for f in FIELDS} for row in rows]

def same_source_profile(rows):
    by={}
    for field in FIELDS:
        vals=[r[field] for r in rows if r[field]]
        cnt=Counter(vals)
        by[field]={
           "nonblank_rows":len(vals),
           "missing_rows":len(rows)-len(vals),
           "distinct_nonblank_values":len(cnt),
           "repeated_identifier_extra_rows":sum(k-1 for k in cnt.values() if k>1),
           "identifier_strings_used_multiple_times":sum(k>1 for k in cnt.values())
        }
    tag_to_deploy=defaultdict(set)
    dep_to_animals=defaultdict(set)
    for row in rows:
        if row["tag-id"] and row["deployment-id"]:
            tag_to_deploy[row["tag-id"]].add(row["deployment-id"])
        if row["deployment-id"] and row["animal-id"]:
            dep_to_animals[row["deployment-id"]].add(row["animal-id"])
    return {
      "original_reference_rows":len(rows),
      "source_id_fields":by,
      "n_tag_strings_linked_to_multiple_distinct_deployment_strings":sum(len(vals)>1 for vals in tag_to_deploy.values()),
      "n_deployment_strings_linked_to_multiple_animal_strings":sum(len(vals)>1 for vals in dep_to_animals.values()),
      "identity_strings_exported":False
    }

def audit(rows):
    expected={"control":19,"delayed":40,"naturally_timed":153}
    if set(rows)!=set(expected):
        raise ValueError("Unregistered cohort identity")
    profiles={cohort:same_source_profile(values) for cohort,values in rows.items()}
    if any(profiles[x]["original_reference_rows"]!=expected[x] for x in expected):
        raise ValueError("Original source row shape changed")
    pairwise=[]
    keys=sorted(expected)
    for i,a in enumerate(keys):
        for b in keys[i+1:]:
            reuses={f:len({r[f] for r in rows[a] if r[f]} &
                          {r[f] for r in rows[b] if r[f]})
                    for f in FIELDS}
            pairwise.append({
              "cohort_a":a,
              "cohort_b":b,
              "overlapping_identifier_strings":reuses,
              "same_animal_identity_inferred":False
            })
    # This source grain was independently read in the prior frozen time support
    # receipt. If the three prior tag overlap counts do not reproduce, fail
    # closed rather than silently allowing a new identity join.
    original_tags={
       ("control","delayed"):1,
       ("control","naturally_timed"):2,
       ("delayed","naturally_timed"):9
    }
    tag_ok=all(z["overlapping_identifier_strings"]["tag-id"]==
          original_tags[(z["cohort_a"],z["cohort_b"])] for z in pairwise)
    return {
       "status":"SOURCE_IDS_MATCH_PREVIOUS_TAG_GATE_NO_CROSS_COHORT_IDENTITY" if tag_ok
                 else "SOURCE_IDS_COLLISION_BENCHMARK_MISMATCH",
       "n_original_reference_rows":sum(len(x) for x in rows.values()),
       "n_studies":len(rows),
       "study_relative_id_profiles":profiles,
       "between_cohort_id_string_collisions":pairwise,
       "original_cross_cohort_tag_overlap_checkpoint_pass":tag_ok,
       "identity_join_authorized":False,
       "source_tag_can_be_redeployed":True,
       "same_tag_implies_same_bird":False,
       "gps_events_requested":False,
       "original_tag_animal_deployment_ids_exported":False,
       "source_animal_records_exported":False,
       "predeparture_information_q_or_recourse_r_estimated":False,
       "no_ebird":True,
       "claim_limit":"Only repeated string counts in study-relative original metadata, not actual bird identity, co-travel, or information receipt."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--source-contract",type=Path,default=DEFAULT_INPUT)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    contract_bytes=args.contract.read_bytes()
    c=json.loads(contract_bytes)
    source=json.loads(args.source_contract.read_text())
    tables={}
    for cohort,item in source["original_archives"].items():
        raw=bounded_cc0_csv(item,cohort,source)
        tables[cohort]=read_reference_ids(raw,item["rows"])
    result=audit(tables)
    result.update({
      "date":c["date"],
      "source_contract_sha256":sha256(args.source_contract.read_bytes()).hexdigest(),
      "identity_gate_contract_sha256":sha256(contract_bytes).hexdigest(),
      "original_paper_doi":"10.1098/rspb.2023.1268",
    })
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print("STORK_ID_GRAIN_SOURCE_RESULT="+json.dumps(result,separators=(",",":")))

if __name__=="__main__":
    main()
