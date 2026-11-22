#!/usr/bin/env python3
"""Retrospective chronological feasibility, not bird cue-use identification.

The source records are from Adams et al. (2025), Figshare article 26050390.v2.
Only the original exact 828 complete station-years from PAYOFF-B PR #415 are
admitted. No station names, GPS coordinates, original rows, or individual
observations appear in this output. The original radar-data outcomes and
prior ecological model estimates are already published/open; this is a new
post-open descriptive chronology, NOT a prospectively registered effect.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import statistics
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from payoff_b_radar_greenup_heldout import source_rows, complete_rows
DEFAULT_CONTRACT = HERE.parent / "data/payoff_b_radar_greenup_chronology_contract_20261122.json"


def interp_quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("no values")
    if not (0 <= q <= 1):
        raise ValueError("quantile outside 0..1")
    x = sorted(values)
    if len(x) == 1:
        return float(x[0])
    pos = (len(x)-1)*q
    lo = int(pos)
    hi = min(lo+1, len(x)-1)
    return float(x[lo]*(1-(pos-lo)) + x[hi]*(pos-lo))


def date_gap(passage: float, greenup: float) -> float:
    if not (1 <= passage <= 366 and 1 <= greenup <= 366):
        raise ValueError("calendar day is outside annual DOY 1..366")
    return float(passage - greenup)


def chronological_categories(gap: float) -> dict:
    # Absolute numerical tolerance protects 7.000000000 - 1e-14 day artifacts
    # from subtracting fractional source DOYs. The 1e-9-day tolerance is
    # effectively zero (~86 microseconds), not a biological latency change.
    # Values are NOT probabilities that individual birds observed a cue.
    eps = 1e-9
    return {
        "greenup_strictly_before_q50": gap > eps,
        "q50_strictly_before_greenup": gap < -eps,
        "same_day_or_equal_timing": abs(gap) <= eps,
        "optimistic_same_day_or_prior": gap >= -eps,
        "at_least_one_day_prior": gap >= 1 - eps,
        "at_least_seven_days_prior": gap >= 7 - eps,
    }


def calc(records: list[dict], contract: dict) -> dict:
    # Guard against post-open accidental sample switching.
    complete = complete_rows(records)
    if len(records) != contract["parent_source_grain_numeric"]["expected_original_rows"]:
        raise ValueError("source original n changed")
    if len(complete) != contract["expected_rows"]:
        raise ValueError("complete-case sample differs from frozen PR #415")
    original_keys = [(r["site"],r["year"]) for r in records]
    if len(set(original_keys)) != len(original_keys):
        raise ValueError("duplicate site-year")
    sites = {r["site"] for r in complete}
    years = sorted({r["year"] for r in complete})
    if len(sites)!=contract["expected_sites"] or len(years)!=contract["expected_years"]:
        raise ValueError("site/year support deviates from parent analysis")
    if years != list(range(2003, 2019)):
        raise ValueError("site-year source period not 2003-2018")
    diffs_by_year=defaultdict(list)
    keys=tuple(chronological_categories(0).keys())
    event_counts=Counter()
    year_rows=[]
    all_diffs=[]
    for r in complete:
        d=date_gap(r["spring_q50"], r["mean_greenup"])
        all_diffs.append(d)
        diffs_by_year[r["year"]].append(d)
        event_counts.update({k:int(v) for k,v in chronological_categories(d).items()})
    for year in years:
        ds=diffs_by_year[year]
        ct=Counter()
        for d in ds:
            ct.update({k:int(v) for k,v in chronological_categories(d).items()})
        annual={
           "year":year,
           "n_station_years":len(ds),
           "median_delta_q50_minus_greenup_days":interp_quantile(ds,0.5),
           "fraction_greenup_strictly_before_q50":ct["greenup_strictly_before_q50"]/len(ds),
           "fraction_q50_strictly_before_greenup":ct["q50_strictly_before_greenup"]/len(ds),
           "fraction_at_least_one_day_prior":ct["at_least_one_day_prior"]/len(ds),
           "fraction_at_least_seven_days_prior":ct["at_least_seven_days_prior"]/len(ds),
        }
        year_rows.append(annual)
    fractions={k:event_counts[k]/len(complete) for k in keys}
    equal_year_fields={
       "greenup_before":"fraction_greenup_strictly_before_q50",
       "q50_before":"fraction_q50_strictly_before_greenup",
       "one_day_prior":"fraction_at_least_one_day_prior",
       "seven_days_prior":"fraction_at_least_seven_days_prior",
    }
    rng=random.Random(contract["uncertainty"]["seed"])
    reps=contract["uncertainty"]["bootstrap_replicates"]
    draws={k:[] for k in equal_year_fields}
    for _ in range(reps):
        picked=[year_rows[rng.randrange(len(years))] for _ in years]
        for field, col in equal_year_fields.items():
            draws[field].append(statistics.fmean(x[col] for x in picked))
    ci={
       k:[interp_quantile(v,contract["uncertainty"]["quantiles"][0]),
          interp_quantile(v,contract["uncertainty"]["quantiles"][1])]
       for k,v in draws.items()
    }
    equal_means={
       k:statistics.fmean(r[col] for r in year_rows)
       for k,col in equal_year_fields.items()
    }
    return {
      "status":"SOURCE_CHRONOLOGY_COMPLETED_NOT_ANIMAL_INFORMATION",
      "n_original_station_years":len(records),
      "n_complete_station_years":len(complete),
      "excluded_incomplete_station_years":len(records)-len(complete),
      "n_stations":len(sites),
      "n_years":len(years),
      "year_start":years[0],
      "year_end":years[-1],
      "gap_definition":"spring_q50 DOY minus mean_greenup DOY; positive means greenup occurred before radar assemblage median",
      "gap_days":{
        "p25":interp_quantile(all_diffs,0.25),
        "median":interp_quantile(all_diffs,0.5),
        "p75":interp_quantile(all_diffs,0.75),
        "mean":statistics.fmean(all_diffs),
      },
      "pooled_station_year_counts":{k:event_counts[k] for k in keys},
      "pooled_station_year_fractions":fractions,
      "equal_year_mean_fractions":equal_means,
      "equal_year_bootstrap_ci95":ci,
      "bootstrap":{"unit":"calendar_year","replicates":reps,
                   "seed":contract["uncertainty"]["seed"],
                   "not_causal_inference":True},
      "n_years_majority_q50_before_greenup":sum(
          r["fraction_q50_strictly_before_greenup"]>0.5 for r in year_rows
      ),
      "annual_aggregate_only":year_rows,
      "individual_bird_information_or_causal_cue_use_estimated":False,
      "original_location_rows_exported":False,
      "prior_greenup_predictive_effect_reopened":False,
      "interpretation_note":(
          "MODIS mean greenup is a retrospective site-season landmark and can "
          "be sensed gradually; even greenup prior to radar median is only "
          "an optimistic timing proxy, not measured bird knowledge. The "
          "assemblage q50 is not an individual choice timestamp."
      ),
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    raw=a.contract.read_bytes()
    contract=json.loads(raw)
    if contract["no_ebird"] is not True:
        raise ValueError("eBird source policy")
    rows=source_rows(a.input)
    result=calc(rows,contract)
    result.update({
        "source_doi":"10.6084/m9.figshare.26050390.v2",
        "original_source_sha256":contract["source_sha256"],
        "contract_sha256":hashlib.sha256(raw).hexdigest(),
        "analysis_class":contract["status"],
        "no_ebird":True,
        "derived_only":True,
    })
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print("PAYOFF_RADAR_GREENUP_CHRONOLOGY="+json.dumps(result,separators=(",",":"),allow_nan=False))


if __name__=="__main__":
    main()
