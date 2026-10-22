#!/usr/bin/env python3
"""Original fix-level validation of 'stationary' daily-centroid risk windows.

Post-outcome, methodology-only audit on four published CC0 bird species.
All frozen GPS source/MD5 and source geometry labels are unchanged. For
every previously admitted 3-day stationary risk opportunity, check whether
ANY original GPS fix during those three days was already >30km outside
the source site's daily-centroid anchor. Distinguish later northward,
stationary continuation, other movement, and right-censored outcomes.
No source weather or fitness effect is opened. No GPS, IDs, timestamps,
grid coordinates, nest or other sensitive bird locations are exported.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import tempfile
from collections import Counter,defaultdict
from datetime import datetime,timedelta,timezone
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_unopened_gps_source import SOURCES as NEW_SOURCES
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_predecision_candidates import (
    daily_source_positions,haversine,
)
from scripts.qc_payoff_b_complete_stationary_riskset import collect

CASES="NORTHWARD_CANDIDATE"
STAYS="STAYED_TWO_DAYS"
SOURCE_NAMES=("stork","white_fronted_goose","curlew","egyptian_vulture")
EXPECTED={
    "stork":(1633,156,941,352,184),
    "white_fronted_goose":(2008,111,1456,285,156),
    "curlew":(1868,66,1632,90,80),
    "egyptian_vulture":(1859,33,1454,232,140),
}
THRESHOLD_KM=30.0
SEVERE_DEPARTURE_DISTANCE_KM=120.0


def date_utc(value):
    stamp=datetime.fromisoformat((value or "").strip().replace("Z","+00:00"))
    return stamp.astimezone(timezone.utc).replace(tzinfo=None) if stamp.tzinfo else stamp


def assemble_private_anchor_index(risk):
    """A single event fix may legitimately enter several overlapping windows."""
    idx=defaultdict(list)
    windows=[]
    for key,day,center,label in risk:
        tax,animal,year=key
        record={
            "center":center,
            "label":label,
            "counts":[0,0,0],
            "outside":[0,0,0],
            "far":[0,0,0],
            "last_time":[None,None,None],
            "last_outside":[False,False,False],
        }
        n=len(windows)
        windows.append(record)
        for offset in (-2,-1,0):
            d=day+timedelta(days=offset)
            idx[(tax,animal,d.year,d)].append((n,offset+2))
    return idx,windows


def audit_fixes(gps,risk,source_taxon):
    index,windows=assemble_private_anchor_index(risk)
    parse=Counter()
    with Path(gps).open(newline="",encoding="utf-8-sig",errors="replace") as h:
        rd=csv.DictReader(h)
        fields=rd.fieldnames or []
        essential={"timestamp","location-lat","location-long"}
        if not essential.issubset(fields):
            raise ValueError("Original GPS lacks time and position")
        identity=next((x for x in ("individual-local-identifier","deployment-id",
                                  "tag-local-identifier") if x in fields),None)
        if identity is None:
            raise ValueError("Source identity column missing")
        for row in rd:
            ident=(row.get(identity) or "").strip()
            if not ident:
                continue
            try:
                t=date_utc(row.get("timestamp") or "")
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not (math.isfinite(lat) and math.isfinite(lon)
                        and -90<=lat<=90 and -180<=lon<=180):
                    raise ValueError("Invalid physical source coordinate")
            except (ValueError,TypeError,OverflowError):
                parse["source_invalid_fix"]+=1
                continue
            tax=(row.get("individual-taxon-canonical-name") or "").strip() or source_taxon
            hits=index.get((tax,ident,t.year,t.date()),())
            if not hits:
                continue
            for n,k in hits:
                r=windows[n]
                distance=haversine(*r["center"],lat,lon)
                r["counts"][k]+=1
                if distance>THRESHOLD_KM:r["outside"][k]+=1
                if distance>SEVERE_DEPARTURE_DISTANCE_KM:r["far"][k]+=1
                if r["last_time"][k] is None or t>r["last_time"][k]:
                    r["last_time"][k]=t
                    r["last_outside"][k]=distance>THRESHOLD_KM
                parse["fixes_used_across_overlapping_anchors"]+=1
    statuses=defaultdict(Counter)
    overall=Counter()
    for r in windows:
        label=r["label"]
        counts=r["counts"]
        outside=r["outside"]
        if any(n==0 for n in counts):
            raise ValueError("Original three-day risk window lacks source fixes")
        stats=statuses[label]
        stats["original_admitted_3day_windows"]+=1
        overall["all_admitted_windows"]+=1
        stats["all_3days_every_fix_inside_30km"]+=int(not any(outside))
        stats["any_fix_outside_in_3day_anchor"]+=int(any(outside))
        stats["prior_first_or_second_day_any_fix_outside"]+=int(any(outside[:2]))
        stats["final_anchor_day_any_fix_outside"]+=int(outside[2]>0)
        stats["final_anchor_day_last_fix_outside"]+=int(r["last_outside"][2])
        stats["final_anchor_day_more_than_half_fixes_outside"]+=int(
            2*outside[2]>counts[2]
        )
        stats["any_anchor_day_fix_farther_than_120km"]+=int(any(r["far"]))
        overall["original_fix_assignments_across_riskdays"]+=sum(counts)
    return {
        "per_prior_riskday_outcome_fix_level_integrity":{
            k:dict(sorted(v.items())) for k,v in sorted(statuses.items())
        },
        "all_outcomes_including_censoring_preserved":True,
        "all_source_riskdays":len(windows),
        "source_original_parse_errors":dict(sorted(parse.items())),
        "absolute_30km_day_centroid_stationarity_can_hide_excursions":True,
        "anchor_fix_level_stable_is_verified_true_stopover":False,
        "study_wide_animal_independence_proven":False,
        "GPS_identity_time_and_coordinate_exported":False,
    }


def read_source(system):
    with tempfile.TemporaryDirectory() as td:
        file=Path(td)/"original_published_CC0_source.csv"
        if system=="egyptian_vulture":
            source=NEW_SOURCES[system]
            checksum=download_verified(source,file)
            doi,taxon=source["doi"],source["taxon"]
        else:
            doi,taxon,sensor,checksum=origin_source(system,file)
        groups,quality,idcol=daily_source_positions(file,taxon)
        risk,original,by_month,by_year=collect(groups)
        labels=("NORTHWARD_CANDIDATE","STAYED_TWO_DAYS",
                "OTHER_MOVEMENT","CENSORED")
        observed=(len(risk),)+(tuple(original[x] for x in labels))
        if observed!=EXPECTED[system]:
            raise ValueError("Original CC0 source riskday counts changed")
        audit=audit_fixes(file,risk,taxon)
        if audit["all_source_riskdays"]!=EXPECTED[system][0]:
            raise ValueError("Source fix-level opportunities mismatched")
        for label in labels:
            count=audit["per_prior_riskday_outcome_fix_level_integrity"].get(label,{})
            if count.get("original_admitted_3day_windows",0)!=original[label]:
                raise ValueError("Daily fix audit lost outcome source events")
        return {
            "status":"ORIGINAL_STATIONARY_SOURCE_FIX_LEVEL_INTEGRITY_COMPLETE",
            "source_system":system,
            "source_doi":doi,
            "original_CC0_checksum":checksum,
            "source_label_counts":dict(sorted(original.items())),
            "source_fix_level_integrity":audit,
            "original_physical_cue_effect_reestimated":False,
            "source_stage_decision_independently_validated":False,
            "sensitive_animal_location_or_event_date_exported":False,
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SOURCE_NAMES,required=True)
    ap.add_argument("--out",type=Path,default=Path("outputs/payoff_b_fix_level_stationarity"))
    q=ap.parse_args()
    result={
        "schema":"payoff_b_original_4guild_source_daily_centroid_fix_integrity_20261022",
        "system":q.system,
        "status":"NOT_RUN",
        "purpose":"POST_OUTCOME_MEASUREMENT_BIAS_SENSITIVITY",
    }
    try:
        result["result"]=read_source(q.system)
        result["status"]="SOURCE_DAILY_FIX_INTEGRITY_AUDITED"
    except (ValueError,OSError,OverflowError,TypeError) as e:
        result["status"]="SOURCE_FIX_LEVEL_QC_FAILED"
        result["error"]=type(e).__name__+": "+str(e)[:250]
    q.out.mkdir(parents=True,exist_ok=True)
    (q.out/(q.system+".json")).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if result["status"]!="SOURCE_DAILY_FIX_INTEGRITY_AUDITED":
        raise SystemExit("Published source daily risk-day fix integrity failed")


if __name__=="__main__":main()
