#!/usr/bin/env python3
"""Reproduce the post-outcome V7R phase-slope identity from frozen Stage-3 ZIPs.

The output is a descriptive covariance/kinematic audit, not a new hypothesis
test or evidence that individual stopover duration changes were causal actions.

Use:
  python scripts/audit_v7r_phase_identity.py \
    --multiflyway-zip barnacle_multiflyway_stage3.zip \
    --svalbard-zip svalbard_stage3.zip \
    --output-csv phase_components.csv --output-json phase_identity.json
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from src.v7r_phase_identity import PhaseTransition, decompose_phase_transfer

MULTI_SHA="8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f"
SVAL_SHA="29558f9b8b43a7375b3922118a77b74464558f4869a7722472570a32745f2856"

PRIMARY_KEYS={
    ("greenland","R1","R2"),
    ("greenland","R2","R3"),
    ("svalbard","R1","R2"),
    ("svalbard","R2","R4"),
    ("barents","R1","R2"),
    ("barents","R1","R5"),
    ("barents","R2","R3"),
    ("barents","R3","R5"),
    ("barents","R4","R5"),
    ("barents","R5","R7"),
}

def _csv(z,name):
    reader=csv.DictReader(io.StringIO(z.read(name).decode("utf-8-sig")))
    return [dict(x) for x in reader]

def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _load_rows(multi,sval):
    out=defaultdict(list)
    ids=defaultdict(set)
    for flyway in ("greenland","barents","svalbard"):
        if flyway=="svalbard":
            data=_csv(sval,"stage3_svalbard_goose_transitions.csv")
            source_cols=("origin_arrival_phase_days","destination_arrival_phase_days")
        else:
            data=_csv(multi,f"stage3_{flyway}_goose_anomaly_phase_transitions.csv")
            source_cols=("origin_arrival_phase_anom","destination_arrival_phase_anom")
        for row in data:
            key=(flyway,str(row["origin_region"]),str(row["destination_region"]))
            origin=float(row["origin_arrival_doy"])
            destination=float(row["destination_arrival_doy"])
            stop=float(row["origin_stopover_days"])
            transit=(float(row["transit_days"]) if flyway=="svalbard"
                     else destination-origin-stop)
            out[key].append(PhaseTransition(
                origin_arrival_doy=origin,
                destination_arrival_doy=destination,
                origin_phase=float(row[source_cols[0]]),
                destination_phase=float(row[source_cols[1]]),
                origin_stopover_days=stop,
                transit_days=transit,
            ))
            ids[key].add(str(row["individual_id"]))
    return out,ids

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--multiflyway-zip",type=Path,required=True)
    parser.add_argument("--svalbard-zip",type=Path,required=True)
    parser.add_argument("--output-csv",type=Path,required=True)
    parser.add_argument("--output-json",type=Path,required=True)
    args=parser.parse_args()

    actual_multi=_sha(args.multiflyway_zip)
    actual_sval=_sha(args.svalbard_zip)
    if actual_multi!=MULTI_SHA or actual_sval!=SVAL_SHA:
        raise ValueError("Stage-3 source checksum mismatch")

    with zipfile.ZipFile(args.multiflyway_zip) as multi, zipfile.ZipFile(args.svalbard_zip) as sval:
        groups,individuals=_load_rows(multi,sval)

    focal={key for key,rows in groups.items() if len(rows)>=5}
    if focal!=PRIMARY_KEYS:
        raise ValueError("source no longer matches frozen ten transitions")

    table=[]
    for key in sorted(PRIMARY_KEYS):
        out=decompose_phase_transfer(groups[key])
        table.append({
            "flyway":key[0],"origin":key[1],"destination":key[2],
            "n":out.n,"n_individuals":len(individuals[key]),
            "lambda_observed":out.lambda_observed,
            "b_stopover":out.b_stopover,
            "b_transit":out.b_transit,
            "b_interregional_season":out.b_interregional_season,
            "lambda_reconstructed":out.lambda_reconstructed,
            "row_identity_error":out.maximum_row_identity_error,
            "slope_identity_error":out.slope_identity_error,
        })

    args.output_csv.parent.mkdir(parents=True,exist_ok=True)
    with args.output_csv.open("w",newline="",encoding="utf-8") as fh:
        writer=csv.DictWriter(fh,fieldnames=list(table[0]))
        writer.writeheader();writer.writerows(table)

    summary={
        "schema":"payoff_b_v7r_phase_identity_postoutcome_v1",
        "status":"POST_OUTCOME_DIAGNOSTIC_NOT_CONFIRMATORY",
        "flyways":3,"focal_transitions":10,
        "maximum_row_identity_error":max(x["row_identity_error"] for x in table),
        "maximum_slope_identity_error":max(x["slope_identity_error"] for x in table),
        "negative_stopover_slopes":sum(x["b_stopover"]<0 for x in table),
        "negative_interregional_season_slopes":sum(x["b_interregional_season"]<0 for x in table),
        "source_sha256":{"multiflyway_stage3":actual_multi,"svalbard_stage3":actual_sval},
        "identity":"lambda=1+b_stopover+b_transit+b_interregional_season",
        "claim_ceiling":"All components are observational OLS slopes, not causal actor response gains. Frozen V7R null unchanged.",
    }
    args.output_json.parent.mkdir(parents=True,exist_ok=True)
    args.output_json.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
