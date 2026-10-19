#!/usr/bin/env python3
"""Exploratory cross-taxon 20-to-80% northing timing handoff.

This does NOT identify information uptake, active correction or fitness.
The source samples and relative-latitude gate were fixed in prior source-QC
receipts. Results below are exploratory because taxa were selected after
source availability was known. No source outputs are selected by effect sign.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import tempfile
from collections import Counter,defaultdict
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import (
    SYSTEMS, origin_source, read_daily, analyze_one,
)
from scripts.run_payoff_b_stork_stage_handoff_pilot import (
    normalize_365, slope_group_fe, cluster_bootstrap, percentile,
)

EXPECTED_ADMITTED = {
    "stork":91,
    "woodcock_argos":37,
    "white_fronted_goose":23,
    "curlew":7,
    "dabbling_ducks":0,
}
MIN_SEASONS=20
MIN_ANIMALS=10
MIN_YEARS=3
BOOT=2000
SEED=20261019


def eligible_rows(groups):
    classes=defaultdict(list)
    status=defaultdict(Counter)
    for (tax, ident, year),data in groups.items():
        r=analyze_one(data)
        status[tax][r["status"]]+=1
        if r["status"]!="TWO_NORTHWARD_CHECKPOINTS":
            continue
        x=normalize_365(r["first20_doy"],year)
        y=normalize_365(r["first80_doy"],year)
        if y<x:
            raise ValueError("Reverse checkpoint time from a validated track")
        classes[tax].append(dict(animal=ident,year=year,x=float(x),y=float(y)))
    return classes,status


def evaluate(rows):
    yrs=sorted({r["year"] for r in rows})
    animals=sorted({r["animal"] for r in rows})
    r=dict(n_seasons=len(rows),n_animal_identity_labels=len(animals),
           n_calendar_years=len(yrs),calendar_years=yrs,
           stage_clock="Feb-May source-relative first 20% to first 80%",
           year_FE=True,animal_clustered_bootstrap_B=BOOT,
           bootstrap_seed=SEED,
           ecological_effect_confirmed=False)
    if len(rows)<MIN_SEASONS or len(animals)<MIN_ANIMALS or len(yrs)<MIN_YEARS:
        return {**r,"status":"NOT_ESTIMABLE_FROZEN_SAMPLE_GATE"}
    try:
        beta=slope_group_fe(rows)
        boots,bad=cluster_bootstrap(rows,seed=SEED,replicates=BOOT)
    except ValueError as exc:
        return {**r,"status":"NOT_ESTIMABLE_YEAR_FE_OR_BOOTSTRAP",
                "failure_reason":str(exc)[:160]}
    lo,hi=percentile(boots,.025),percentile(boots,.975)
    grouped=Counter(row["animal"] for row in rows)
    repeated={k for k,v in grouped.items() if v>=2}
    repeated_data=[row for row in rows if row["animal"] in repeated]
    if len(repeated)>=10:
        try:within=slope_group_fe(repeated_data,group="animal")
        except ValueError:within=None
    else:within=None
    return {
        **r,"status":"EXPLORATORY_ESTIMATE",
        "year_FE_beta_X20_to_Y80":beta,
        "interval_on_X20_slope":beta-1,
        "animal_cluster_95pct_CI":[lo,hi],
        "valid_bootstrap_samples":len(boots),
        "invalid_bootstrap_samples":bad,
        "observed_intercheckpoint_interval_median_days":
            statistics.median(row["y"]-row["x"] for row in rows),
        "within_animal_beta_repeated_only":within,
        "n_repeated_animals":len(repeated),
        "descriptive_below_one_ci":hi<1,
        "structural_window_bias_excluded":False,
        "observed_passive_retention_separated_from_feedback":False,
        "individual_stage_cue_availability_measured":False,
    }


def run_all(groups):
    by_tax,counts=eligible_rows(groups)
    results={tax:evaluate(rows) for tax,rows in sorted(by_tax.items())}
    return {
        "source_taxon_statuses":{
            tax:dict(sorted(v.items())) for tax,v in sorted(counts.items())
        },
        "taxa":results,
        "total_eligible_source_seasons":sum(len(s) for s in by_tax.values()),
        "total_exploratory_estimable_taxa":
            sum(v["status"]=="EXPLORATORY_ESTIMATE" for v in results.values()),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",required=True,choices=sorted(SYSTEMS))
    ap.add_argument("--out",type=Path,
                    default=Path("outputs/payoff_b_crossguild_timing_handoff"))
    args=ap.parse_args()
    output={"system":args.system,
            "schema":"payoff_b_crossguild_relative_northing_year_fe_v1",
            "classification":"POST_SOURCE_COVERAGE_EXPLORATORY_NO_CAUSAL_CUE",
            "prior_source_gate_expected_seasons":EXPECTED_ADMITTED[args.system],
            "status":"NOT_OPENED"}
    try:
        with tempfile.TemporaryDirectory() as temp:
            src=Path(temp)/"source.csv"
            doi,taxon,sensor,checksum=origin_source(args.system,src)
            groups,errors,taxa,idcol=read_daily(src,taxon)
            x=run_all(groups)
            if x["total_eligible_source_seasons"]!=EXPECTED_ADMITTED[args.system]:
                raise ValueError("Changed original source case definition")
            output.update(source_doi=doi,publisher_taxa=taxon,
                          source_sensor=sensor,source_integrity=checksum,
                          source_geometry_counts=x["source_taxon_statuses"],
                          taxon_estimands=x["taxa"],
                          source_identity_field=idcol,
                          status="EXPLORATORY_TIMING_HANDOFF_REPORTED")
    except (OSError,ValueError,TypeError) as e:
        output["status"]="SOURCE_OR_MODEL_GATE_FAILED"
        output["error"]=type(e).__name__+": "+str(e)[:250]
    output["no_raw_location_or_individual_ID_exported"]=True
    output["not_independent_confirmatory_causal_evidence"]=True
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))
    if output["status"]!="EXPLORATORY_TIMING_HANDOFF_REPORTED":
        raise SystemExit("exploratory source timing handoff failed")

if __name__=="__main__":
    main()
