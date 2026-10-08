#!/usr/bin/env python3
"""Run an exploratory V7R calendar-anchoring audit on frozen Stage-3 ZIPs.

This does not rerun, alter, or replace the registered V7R Q×R analysis.
Example:
 python scripts/audit_v7r_calendar_anchor.py \
   --multiflyway-zip barnacle_multiflyway_stage3.zip \
   --svalbard-zip svalbard_stage3.zip \
   --output v7r_calendar_diagnostic.json
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from src.v7r_calendar_anchor_diagnostic import summarize_edge

SOURCES = {
    "greenland": (
        "multiflyway",
        "stage3_greenland_goose_anomaly_phase_transitions.csv",
        "origin_arrival_phase_anom",
        "destination_arrival_phase_anom",
    ),
    "barents": (
        "multiflyway",
        "stage3_barents_goose_anomaly_phase_transitions.csv",
        "origin_arrival_phase_anom",
        "destination_arrival_phase_anom",
    ),
    "svalbard": (
        "svalbard",
        "stage3_svalbard_goose_transitions.csv",
        "origin_arrival_phase_days",
        "destination_arrival_phase_days",
    ),
}
EXPECTED_SHA256 = {
    "multiflyway": "8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f",
    "svalbard": "29558f9b8b43a7375b3922118a77b74464558f4869a7722472570a32745f2856",
}

def read_csv(z, filename):
    return list(csv.DictReader(io.StringIO(z.read(filename).decode("utf-8-sig"))))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--multiflyway-zip",required=True)
    parser.add_argument("--svalbard-zip",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--bootstrap-draws",type=int,default=4000)
    args=parser.parse_args()
    paths={
        "multiflyway":Path(args.multiflyway_zip),
        "svalbard":Path(args.svalbard_zip),
    }
    for kind,path in paths.items():
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=EXPECTED_SHA256[kind]:
            raise SystemExit(f"Source SHA mismatch for {kind}: {actual}")
    with zipfile.ZipFile(paths["multiflyway"]) as multiflyway,zipfile.ZipFile(paths["svalbard"]) as svalbard:
        zips={"multiflyway":multiflyway,"svalbard":svalbard}
        edge_results=[]
        barents_r1_r5_rows=[]
        for flyway,(source,member,first_phase,next_phase) in SOURCES.items():
            grouped={}
            for r in read_csv(zips[source],member):
                key=(r["origin_region"],r["destination_region"])
                grouped.setdefault(key,[]).append({
                    "e0":float(r[first_phase]),
                    "e1":float(r[next_phase]),
                    "a0":float(r["origin_arrival_doy"]),
                    "a1":float(r["destination_arrival_doy"]),
                    "stop_days":float(r["origin_stopover_days"]),
                    "year":int(r["year"]),
                    "individual_id":str(r["individual_id"]),
                })
            if flyway=="barents":
                barents_r1_r5_rows=grouped.get(("R1","R5"),[])
            for (origin,destination),observations in sorted(grouped.items()):
                if len(observations)<5:
                    continue
                out=summarize_edge(observations,draws=args.bootstrap_draws)
                edge_results.append({
                    "flyway":flyway,"origin":origin,"destination":destination,**out
                })

        raw=read_csv(multiflyway,"stage3_barents_goose_transitions_raw.csv")
        stops=read_csv(multiflyway,"stage3_barents_goose_stopovers.csv")
        focus=[r for r in raw if r["origin_region"]=="R1" and r["destination_region"]=="R5"]
        r1stops=[r for r in stops if r.get("region_id")=="R1"]
        first_r1={}
        for r in r1stops:
            key=(r["individual_id"],r["year"])
            first_r1[key]=min(first_r1.get(key,r["start"]),r["start"])
        origin_stop_indices=[]
        non_first=0
        for row in focus:
            matches=[
                s for s in r1stops
                if (s["individual_id"],s["year"],s["start"])
                == (row["individual_id"],row["year"],row["origin_arrival"])
            ]
            if len(matches)!=1:
                raise ValueError("R1->R5 origin provenance join failed")
            origin_stop_indices.append(int(matches[0]["stop_index"]))
            non_first+=int(
                row["origin_arrival"]>first_r1[(row["individual_id"],row["year"])]
            )
        onset={
            int(r["year"]):float(r["onset_doy_raw"])
            for r in read_csv(multiflyway,"stage3_barents_goose_power_gdd_anomalies.csv")
            if r["region_id"]=="R1"
        }
        for edge in edge_results:
            if (edge["flyway"],edge["origin"],edge["destination"])==("barents","R1","R5"):
                for year in edge["annual_arrival_departure"]:
                    year["origin_spring_onset_doy_power"]=onset[year["year"]]

        year_scope_checks=[]
        for admitted_years in ((2008,2009),(2009,),(2008,2009,2010)):
            subset=[
                row for row in barents_r1_r5_rows
                if int(row["year"]) in admitted_years
            ]
            check=summarize_edge(subset,draws=min(args.bootstrap_draws,400))
            year_scope_checks.append({
                "included_years":list(admitted_years),
                "n":check["n"],
                "lambda":check["lambda"],
                "beta_stopover":check["beta_stopover"],
                "beta_spring_shift":check["beta_spring_shift"],
                "departure_on_arrival_calendar_slope":(
                    check["departure_on_arrival_calendar_slope"]
                ),
            })

        receipt={
            "schema":"payoff_b_v7r_calendar_anchor_postoutcome_v1",
            "status":"POST_OUTCOME_EXPLORATORY_ACCOUNTING_NOT_CONFIRMATION",
            "source_sha256":EXPECTED_SHA256,
            "identity":"lambda = 1 + slope(stopover_days on origin phase) + slope(transit_days on origin phase) + slope(origin-minus-destination spring on origin phase)",
            "edge_results":edge_results,
            "barents_R1_R5_year_scope_exploration":year_scope_checks,
            "barents_R1_R5_origin_definition":{
                "focal_rows":len(focus),
                "final_local_stop_index_counts":{
                    str(i):origin_stop_indices.count(i)
                    for i in sorted(set(origin_stop_indices))
                },
                "focal_origin_is_not_first_observed_R1_stop_count":non_first,
                "caution":"R1 is the Netherlands wintering/staging region. Origin arrival is arrival at the selected last local R1 stop, not arrival to the wintering region.",
            },
            "claim_boundary":[
                "Arithmetic decomposition is not causal identification.",
                "Arrival/stay coupling can reflect a fixed departure calendar.",
                "Some origin timing depends on last-local-stop selection and tagging.",
                "Near-zero between-site historical predictability is not absence of local cues.",
                "Frozen V7R primary and its null result are unchanged.",
            ],
        }
        output=Path(args.output)
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print(f"EDGES {len(edge_results)}")
        print(f"MAX_IDENTITY_ERROR {max(abs(x['identity_residual']) for x in edge_results):.3g}")
        print(f"R1R5_ORIGIN_NON_FIRST {non_first}/{len(focus)}")
        print(f"OUTPUT {output}")

if __name__=="__main__":
    main()
