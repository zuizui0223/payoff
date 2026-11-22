#!/usr/bin/env python3
"""Bounded retrospective radar/greenup order with one unresolved source DOY.

This POST-FAILURE exploratory diagnostic does NOT replace the previous strict
chronology result. It reports exact logical bounds for 828 original complete
station-years while keeping one out-of-calendar 2012 greenup (DOY=-27)
unclassified. No bird cue, learning, predictor gain, or ecological effect fit.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_radar_greenup_heldout import source_rows, complete_rows
from payoff_b_radar_greenup_chronology_20261122 import chronological_categories, date_gap


def bound_source_rows(records, contract):
    expected=contract["known_counts"]
    complete=complete_rows(records)
    if (len(records),len(complete)) != (expected["source_rows"],expected["complete_case_station_years"]):
        raise ValueError("original complete-case grain changed")
    keys=[(r["site"],r["year"]) for r in records]
    if len(set(keys))!=len(keys):
        raise ValueError("duplicate original site-year")
    if (len({r["site"] for r in complete}),len({r["year"] for r in complete})) != (
        expected["stations"],expected["years"]
    ):
        raise ValueError("site-year group count differs from frozen source")
    years=sorted({r["year"] for r in complete})
    if years != list(range(2003,2019)):
        raise ValueError("original 2003-2018 years changed")
    valid=[]
    unknown=[]
    for r in complete:
        passage=r["spring_q50"]
        greenup=r["mean_greenup"]
        if not (1 <= passage <= 366 and 1 <= greenup <= 366):
            unknown.append(r)
        else:
            valid.append((r,date_gap(passage,greenup)))
    if len(unknown)!=expected["invalid_greenup_DOY_count"]:
        raise ValueError("unexpected out-of-range original source count")
    if any(
       u["year"]!=expected["invalid_greenup_year"]
       or u["mean_greenup"]!=expected["invalid_greenup_value"]
       or not 1<=u["spring_q50"]<=366 for u in unknown
    ):
        raise ValueError("original unusual value identity or type changed")
    if len(valid)!=expected["valid_comparable_station_years"]:
        raise ValueError("valid original source count changed")
    years_info={year:{"n":0,"valid":0,"unknown":0,"counts":Counter()} for year in years}
    summary=Counter()
    for r in complete:
        years_info[r["year"]]["n"]+=1
    for r in unknown:
        years_info[r["year"]]["unknown"]+=1
    for r,gap in valid:
        d=chronological_categories(gap)
        years_info[r["year"]]["valid"]+=1
        years_info[r["year"]]["counts"].update({k:int(v) for k,v in d.items()})
        summary.update({k:int(v) for k,v in d.items()})
    assert summary["greenup_strictly_before_q50"]+summary["q50_strictly_before_greenup"]+summary["same_day_or_equal_timing"]==len(valid)
    fields=tuple(chronological_categories(0).keys())
    def bounds(k, n, unknown):
        return {"valid_count":k,"lower":k/n,"upper":(k+unknown)/n}
    annual=[]
    for year in years:
        v=years_info[year]
        annual.append({
           "year":year,
           "original_complete_station_years":v["n"],
           "valid_station_years":v["valid"],
           "unknown_station_years":v["unknown"],
           "bounds":{f:bounds(v["counts"][f],v["n"],v["unknown"]) for f in fields},
        })
    n=len(complete)
    unknown_n=len(unknown)
    overall={f:bounds(summary[f],n,unknown_n) for f in fields}
    majority_lower=sum(x["bounds"]["q50_strictly_before_greenup"]["lower"]>0.5 for x in annual)
    majority_possible=sum(x["bounds"]["q50_strictly_before_greenup"]["upper"]>0.5 for x in annual)
    return {
       "status":"BOUNDED_SOURCE_CHRONOLOGY_POST_FAILURE_NOT_NEW_EFFECT",
       "original_strict_chronology_status":"HOLD_REQUIRES_SOURCE_SEMANTICS",
       "source_rows":len(records),
       "original_complete_station_years":n,
       "valid_classifiable_station_years":len(valid),
       "unresolved_original_station_years":unknown_n,
       "unresolved_source_year":expected["invalid_greenup_year"],
       "unresolved_source_mean_greenup_value":expected["invalid_greenup_value"],
       "n_sites":len({r["site"] for r in complete}),
       "n_years":len(years),
       "coverage_bounded_uncertainty_fraction":unknown_n/n,
       "gap_direction":"spring radar median DOY minus MODIS greenup DOY; positive = greenup before bird assemblage median",
       "pooled_exact_identification_bounds":overall,
       "n_years_majority_q50_prior_greenup_certain":majority_lower,
       "n_years_majority_q50_prior_greenup_possible":majority_possible,
       "yearly_aggregate_only":annual,
       "is_post_failure_exploratory_sensitivity":True,
       "sampling_confidence_interval_estimated":False,
       "animal_cue_availability_or_behavior_identified":False,
       "previous_heldout_greenup_effect_refitted":False,
       "original_source_rows_exported":False,
       "no_ebird":True,
       "claim_limit":"This bounds event chronology for a radar assemblage and MODIS retrospective marker; it is not actual knowledge or a causal decision-date forecast.",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--contract",type=Path,default=HERE.parent/"data/payoff_b_radar_greenup_chronology_bounds_contract_20261122.json")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    raw=a.contract.read_bytes()
    contract=json.loads(raw)
    if contract["no_ebird"] is not True:
        raise ValueError("source policy not satisfied")
    rows=source_rows(a.input)
    z=bound_source_rows(rows,contract)
    z.update({
        "contract_sha256":hashlib.sha256(raw).hexdigest(),
        "original_source_sha256":contract["original_source_sha256"],
        "source_doi":"10.6084/m9.figshare.26050390.v2",
    })
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(z,indent=2,allow_nan=False)+"\n")
    print("PAYOFF_RADAR_GREENUP_BOUNDS="+json.dumps(z,separators=(",",":"),allow_nan=False))


if __name__=="__main__":
    main()
