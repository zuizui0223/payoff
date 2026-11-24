#!/usr/bin/env python3
"""Post-outcome descriptive radar passage-window vs greenup timing audit.

Independent scientific unit: weather-radar station x year, not an individual
migrating bird. Original Adams 2025 Figshare RDS is accessed only inside CI.
Never export raw site, location, site-year observations, or a causal cue result.
The same parent 828-row sample and strict q50 benchmark are immutable.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path

SOURCE_SHA256 = "1751ca4cd523d632368ba7fbb27987c2d6c1cc4c1a9c75b8c67255476d799900"
FIELDS = ("site","year","spring_q10","spring_q50","spring_q90","mean_greenup","spring_mean_temp")
DOY_EPS=1e-9
CLASSES = ("greenup_before_q10",
           "greenup_q10_to_before_q50",
           "greenup_q50_to_q90",
           "greenup_after_q90")
MEASURES=CLASSES + ("greenup_at_least_7d_before_q10",
                    "greenup_at_least_7d_before_q50",
                    "q10_strictly_before_greenup",
                    "greenup_strictly_before_q50")
DEFAULT_CONTRACT=Path(__file__).resolve().parents[1] / "data/payoff_b_radar_migration_window_contract_20261124.json"


def parse_number(raw: str):
    raw = str(raw or "").strip()
    if raw.upper() in {"","NA","NAN","NULL","N/A"}:
        return None
    val=float(raw)
    if not math.isfinite(val):
        raise ValueError("Nonfinite original numeric source field")
    return val


def source_rows(path: Path):
    rows=[]
    keys=set()
    with Path(path).open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        if not all(field in (reader.fieldnames or []) for field in FIELDS):
            raise ValueError("Missing required source field")
        for row in reader:
            site=str(row.get("site","")).strip()
            yr_txt=str(row.get("year","")).strip()
            if not site or not yr_txt.isdigit():
                raise ValueError("Original site/year identity invalid")
            year=int(yr_txt)
            if year<2003 or year>2018:
                raise ValueError("Original year outside fixed source period")
            key=(site,year)
            if key in keys:
                raise ValueError("Duplicate site-year")
            keys.add(key)
            rows.append({
                "site":site,"year":year,
                **{f:parse_number(row.get(f,"")) for f in FIELDS[2:]},
            })
    return rows


def q50_checkpoint(rows,expected):
    """Reproduce prior #416 median date chronology on its original 828 records."""
    counts=Counter()
    unknown=Counter()
    for row in rows:
        g=row["mean_greenup"]
        q50=row["spring_q50"]
        if g is None or q50 is None:
            raise ValueError("Unexpected source sample missing q50/greenup")
        if not 1<=g<=366:
            unknown[(row["year"],g)]+=1
            continue
        if not 1<=q50<=366:
            raise ValueError("Invalid source q50 day")
        if q50-g>DOY_EPS:
            counts["strict_greenup_before_q50"]+=1
        elif q50-g < -DOY_EPS:
            counts["q50_before_greenup"]+=1
        else:
            counts["tie"]+=1
    if (
        counts["strict_greenup_before_q50"] != expected["strict_greenup_before_q50"]
        or counts["q50_before_greenup"] != expected["q50_before_greenup"]
        or counts["tie"] != expected["tie"]
        or sum(unknown.values()) != expected["unclassifiable"]
        or unknown != Counter({(2012,-27.0):1})
    ):
        raise ValueError("Parent PR #416 q50 source checkpoint failed")
    return {
        "strict_greenup_before_q50":counts["strict_greenup_before_q50"],
        "q50_before_greenup":counts["q50_before_greenup"],
        "tie":counts["tie"],
        "unclassifiable":sum(unknown.values()),
    }


def exclusive_class(q10,q50,q90,g):
    """Ties: greenup at q10 enters q10–q50; at q50/q90 enters q50–q90."""
    if not (1<=q10<=366 and 1<=q50<=366 and 1<=q90<=366 and 1<=g<=366):
        raise ValueError("Classifier requires 4 valid original DOY values")
    if q10>q50+DOY_EPS or q50>q90+DOY_EPS:
        raise ValueError("Nonmonotonic radar quantile source chronology")
    if g < q10-DOY_EPS:
        return CLASSES[0]
    if g < q50-DOY_EPS:
        return CLASSES[1]
    if g <= q90+DOY_EPS:
        return CLASSES[2]
    return CLASSES[3]


def classification(row):
    g=row["mean_greenup"]
    q10=row["spring_q10"]
    q50=row["spring_q50"]
    q90=row["spring_q90"]
    if g is None or q10 is None or q50 is None or q90 is None:
        return None
    if not all(1<=v<=366 for v in (g,q10,q50,q90)):
        return None
    category=exclusive_class(q10,q50,q90,g)
    out={c:int(category==c) for c in CLASSES}
    out.update({
        "greenup_at_least_7d_before_q10":int(q10-g>=7-DOY_EPS),
        "greenup_at_least_7d_before_q50":int(q50-g>=7-DOY_EPS),
        "q10_strictly_before_greenup":int(g-q10>DOY_EPS),
        "greenup_strictly_before_q50":int(q50-g>DOY_EPS),
    })
    return out


def bounds(count,unknown,total):
    if count+unknown>total:
        raise ValueError("Incorrect denominator")
    return {
        "classifiable_positive_count":count,
        "possible_count_range":[count,count+unknown],
        "fraction_lower":count/total,
        "fraction_upper":(count+unknown)/total,
    }


def summarize(original,contract):
    if len(original)!=contract["expected_source_rows"]:
        raise ValueError("Original source row count drift")
    bases=[
        r for r in original
        if all(r.get(col) is not None for col in ("spring_q50","mean_greenup","spring_mean_temp"))
    ]
    if len(bases)!=contract["expected_base_complete_rows"]:
        raise ValueError("Parent PR #415 row count drift")
    if len({r["site"] for r in bases})!=contract["expected_sites"]:
        raise ValueError("Parent source site count drift")
    years=sorted({r["year"] for r in bases})
    if years!=list(range(contract["source_years"][0],contract["source_years"][1]+1)):
        raise ValueError("Year support changed")
    checkpoint=q50_checkpoint(bases,contract["source_structure_gates"]["validate_original_q50_counts"])
    year_stats={year:{"n_original":0,"classifiable":0,"unknown":0,"tallies":Counter()} for year in years}
    pooled=Counter()
    unknown_reasons=Counter()
    nonmonotonic=0
    for row in bases:
        z=year_stats[row["year"]]
        z["n_original"]+=1
        q10,q50,q90,g=(row["spring_q10"],row["spring_q50"],row["spring_q90"],row["mean_greenup"])
        if q10 is not None and q90 is not None and q50 is not None and (
            q10>q50+DOY_EPS or q50>q90+DOY_EPS
        ):
            nonmonotonic+=1
        d=classification(row) if not nonmonotonic else None
        if d is None:
            z["unknown"]+=1
            unknown_reasons["missing_q10_or_q90"]+=int(q10 is None or q90 is None)
            unknown_reasons["out_of_range_original_calendar_field"]+=int(
                any(v is not None and not 1<=v<=366 for v in (q10,q50,q90,g)))
        else:
            z["classifiable"]+=1
            z["tallies"].update(d)
            pooled.update(d)
    n=len(bases)
    unknown_total=sum(z["unknown"] for z in year_stats.values())
    checks={
        "fixed_parent_source_rows":len(original)==contract["expected_source_rows"],
        "fixed_parent_complete_cases":n==contract["expected_base_complete_rows"],
        "parent_q50_checkpoint":checkpoint==contract["source_structure_gates"]["validate_original_q50_counts"],
        "quantiles_ordered":nonmonotonic==0,
        "unknown_fraction_within_cap":unknown_total/n<=contract["source_structure_gates"]["max_total_unclassifiable_fraction"],
        "all_rows_partition":sum(pooled[c] for c in CLASSES)+unknown_total==n,
    }
    gate="PASS" if all(checks.values()) else "SOURCE_SUPPORT_FAILED"
    metadata={
        "status":gate,
        "source_counts":{"original_rows":len(original),"original_base_complete":n,
                         "n_sites":len({r["site"] for r in bases}),"n_years":len(years),
                         "classifiable":n-unknown_total,"unclassifiable":unknown_total,
                         "unclassifiable_reasons":dict(unknown_reasons),
                         "nonmonotonic_q10_q50_q90":nonmonotonic},
        "source_checks":checks,
        "parent_q50_checkpoint":checkpoint,
        "original_q50_negative_unknown_retained":True,
        "no_individual_bird_information_use_estimated":True,
        "ecological_effects_refitted":False,
        "original_station_rows_exported":False,
        "class_definitions":contract["primary_exclusive_classes"],
        "no_ebird":True,
    }
    if gate!="PASS":
        metadata["pooled_logical_bounds"]=None
        metadata["annual_aggregate"]=None
        return metadata
    annual=[]
    for year in years:
        y=year_stats[year]
        if y["n_original"] != y["classifiable"]+y["unknown"]:
            raise ValueError("Annual partition failed")
        annual.append({
            "year":year,"original_complete_station_years":y["n_original"],
            "classifiable":y["classifiable"],"unknown":y["unknown"],
            "logical_bounds":{
                f:bounds(y["tallies"][f],y["unknown"],y["n_original"])
                for f in MEASURES
            },
        })
    metadata.update({
        "status":"WINDOW_CHRONOLOGY_COMPLETED_BOUNDING_NOT_CUE_USE",
        "pooled_logical_bounds":{
            f:bounds(pooled[f],unknown_total,n) for f in MEASURES
        },
        "annual_aggregate":annual,
        "classifiable_exclusive_counts":{f:pooled[f] for f in CLASSES},
        "evidence_limit":"Logical event ordering of radar migratory assemblage q10/q50/q90 and a retrospective MODIS greenup marker; not any bird's available forecast, cue, decision, reward or information threshold.",
    })
    return metadata


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    contract_bytes=args.contract.read_bytes()
    contract=json.loads(contract_bytes)
    if contract["no_ebird"] is not True:
        raise ValueError("Source restriction mismatch")
    data=source_rows(args.input)
    result=summarize(data,contract)
    result.update({
        "date":contract["date"],
        "analysis_class":contract["status"],
        "source_sha256":SOURCE_SHA256,
        "contract_sha256":hashlib.sha256(contract_bytes).hexdigest(),
    })
    args.output.parent.mkdir(exist_ok=True,parents=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print("PAYOFF_B_RADAR_WINDOW_RESULT="+json.dumps(result,separators=(",",":"),allow_nan=False))


if __name__=="__main__":
    main()
