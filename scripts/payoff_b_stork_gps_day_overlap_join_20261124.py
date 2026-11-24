#!/usr/bin/env python3
"""Derived-only cohort GPS UTC-date overlap from three verified source receipts.

Inputs contain no raw GPS events, original tag/animal IDs or coordinates.
Same-day overlap ≠ same-time or same-place GPS; not information usage, q or r.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import hashlib
from itertools import combinations

CONTRACT=Path(__file__).resolve().parents[1]/"data/payoff_b_stork_gps_day_overlap_contract_20261124.json"

def source_date_set(receipt,source_gate):
    for key,expected in source_gate.items():
        if key=="n_valid_georeferenced_event_rows_min":
            if int(receipt.get("n_valid_georeferenced_event_rows") or 0)<expected:
                raise ValueError("No verified georeferenced records in frozen cohort source")
        elif receipt.get(key)!=expected:
            raise ValueError("Source cohort gate mismatch: "+key)
    if receipt.get("status")!="ORIGINAL_CC0_GPS_SINGLE_ARCHIVE_UTC_DATE_SUPPORT_VERIFIED":
        raise ValueError("Original full GPS source was not authenticated")
    day_rows=receipt.get("daily_aggregate_only")
    if not isinstance(day_rows,list) or len(day_rows)!=receipt.get("n_distinct_UTC_dates_with_valid_events"):
        raise ValueError("Original UTC-date support differs from frozen receipt")
    days=set()
    yearly_events=Counter()
    yearly_days=Counter()
    multi_tag_days=Counter()
    for obj in day_rows:
        value=obj.get("UTC_date")
        if not isinstance(value,str) or len(value)!=10:
            raise ValueError("Invalid source UTC date")
        try:
            d=date.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid source UTC date") from None
        if value!=d.isoformat() or value in days:
            raise ValueError("Noncanonical or repeated source UTC day")
        count=obj.get("n_valid_georeferenced_event_rows")
        tags=obj.get("n_distinct_observed_tag_strings")
        if not isinstance(count,int) or not isinstance(tags,int) or count<1 or tags<1 or tags>count:
            raise ValueError("Invalid source day count/tag bound")
        days.add(value)
        yearly_days[d.year]+=1
        yearly_events[d.year]+=count
        multi_tag_days[d.year]+=int(tags>=2)
    if sum(yearly_events.values())!=receipt["n_valid_georeferenced_event_rows"]:
        raise ValueError("Original source-event sum disagrees with daily output")
    original_years=receipt.get("yearly_aggregate") or []
    if len(original_years)!=len(yearly_days):
        raise ValueError("Year aggregate number differs from source")
    for source in original_years:
        y=source["year"]
        if (source["n_valid_georeferenced_events"]!=yearly_events[y]
            or source["n_UTC_dates_with_georeferenced_events"]!=yearly_days[y]
            or source["n_UTC_dates_with_at_least_two_tag_strings"]!=multi_tag_days[y]):
            raise ValueError("Original year and day support do not reconcile")
    return days,{int(y):{"n_valid_events":yearly_events[y],
                          "n_observed_UTC_days":yearly_days[y],
                          "n_days_2plus_tags":multi_tag_days[y]} for y in sorted(yearly_days)}


def derived_overlap(cohort_receipts,contract):
    if set(cohort_receipts)!=set(contract["expected_cohorts"]):
        raise ValueError("Three exact original cohorts required")
    source_contract_sha_set={cohort_receipts[k].get("source_contract_sha256")
                             for k in contract["expected_cohorts"]}
    header_sha_set={cohort_receipts[k].get("header_source_receipt_sha256")
                    for k in contract["expected_cohorts"]}
    if (len(source_contract_sha_set)!=1 or None in source_contract_sha_set or
        len(header_sha_set)!=1 or None in header_sha_set):
        raise ValueError("Original cohort source contract or header provenance mismatched")
    sets={}
    years={}
    for key in contract["expected_cohorts"]:
        receipt=cohort_receipts[key]
        if receipt.get("cohort")!=key:
            raise ValueError("Swapped cohort source receipt")
        sets[key],years[key]=source_date_set(
            receipt,contract["verified_source_required"])
    pairs=[]
    for a,b in combinations(contract["expected_cohorts"],2):
        ds=sets[a]&sets[b]
        byyear=Counter(int(d[:4]) for d in ds)
        pairs.append({"cohort_a":a,"cohort_b":b,
                      "n_exact_UTC_days_with_observations_in_both_selected_archives":len(ds),
                      "yearly_common_day_counts":[
                         {"year":y,"n_days":byyear[y]} for y in sorted(byyear)]
                     })
    common=set.intersection(*(sets[x] for x in contract["expected_cohorts"]))
    years_triple=Counter(int(x[:4]) for x in common)
    union=set.union(*(sets[x] for x in contract["expected_cohorts"]))
    # String comparison of exact YYYY-MM-DD is safe for this ISO-only input.
    # No raw event locations or individual tags exist in these inputs.
    return {
       "status":"DERIVED_COHORT_UTC_DAY_SOURCE_OVERLAP_NOT_COLOCATION",
       "n_source_cohorts":3,
       "source_cohort_yearly_counts":years,
       "pairwise_same_day_observation_support":pairs,
       "n_UTC_days_in_all_three_selected_ZIPs":len(common),
       "triple_same_day_year_counts":[
            {"year":y,"n_days":years_triple[y]} for y in sorted(years_triple)
       ],
       "n_UTC_days_with_any_selected_ZIP_data":len(union),
       "within_group_same_day_two_tag_support":{
          k:sum(v["n_days_2plus_tags"] for v in years[k].values())
          for k in contract["expected_cohorts"]
       },
       "original_scope":"one frozen smallest original GPS ZIP per cohort, not all published tracking data",
       "UTC_day_only_no_hour_or_spatial_colocation":True,
       "social_contact_information_q_or_recourse_r_estimated":False,
       "animal_id_or_original_event_location_exported":False,
       "outcome_or_fitness_model_fitted":False,
       "no_ebird":True,
       "claim_limit":"Common GPS observation dates are temporal data overlap only; distinct tagged birds need not be co-located, see each other or obtain useful predictive information."
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--control",type=Path,required=True)
    p.add_argument("--delayed",type=Path,required=True)
    p.add_argument("--naturally-timed",type=Path,required=True)
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    contract_bytes=args.contract.read_bytes()
    contract=json.loads(contract_bytes)
    r={
       "control":json.loads(args.control.read_text()),
       "delayed":json.loads(args.delayed.read_text()),
       "naturally_timed":json.loads(args.naturally_timed.read_text()),
    }
    output=derived_overlap(r,contract)
    output.update({
      "contract_sha256":hashlib.sha256(contract_bytes).hexdigest(),
      "source_receipt_sha256":{
         k:hashlib.sha256(path.read_bytes()).hexdigest()
         for k,path in [("control",args.control),("delayed",args.delayed),
                        ("naturally_timed",args.naturally_timed)]
      }
    })
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2)+"\n")
    print("STORK_GPS_COHORT_DAY_OVERLAP="+json.dumps(output,separators=(",",":")))


if __name__=="__main__":
    main()
