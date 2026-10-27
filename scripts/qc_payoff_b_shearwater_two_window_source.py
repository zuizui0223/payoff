#!/usr/bin/env python3
"""Original experimental shearwater GPS early/late source-observation gate.

Not a new published navigation effect. Recheck GPS/reference original CC0
bitstream MD5/bytes. Compare **measurement coverage**, not flight course
or outcome, across experimental sensory treatment arms.

GPS-equipped denominator comes from original publication (9,9,9).
Anosmic 5 Argos by-design birds are NOT GPS failures. Individual GPS
locations, releases, dates, bird IDs, ring IDs, or tracks are never exported.
"""
from __future__ import annotations
import argparse, csv, json, math, statistics, tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_shearwater_cue_experiment_source import FILES, refs
from scripts.qc_payoff_b_shearwater_sensor_quality import reference_animal_tags
from scripts.audit_payoff_b_shearwater_device_allocation import (
    GROUPS, REFERENCE, GPS_EQUIPPED, ORIGINAL_GPS, ORIGINAL_ARGOS
)

WINDOW_HOURS = 12.0
MIN_UNIQUE_FIXES_PER_HALF = 6
MAX_INTERNAL_GAP_HOURS = 3.0
MAX_BOUNDARY_GAP_HOURS = 4.0
MIN_FIRST_HALF_END_HOURS = 10.0
MAX_FIRST_HALF_START_HOURS = 2.0
MAX_SECOND_HALF_START_HOURS = 14.0
MIN_SECOND_HALF_END_HOURS = 22.0
MIN_ELIGIBLE_PER_ARM = 5


def utc(stamp):
    d=datetime.fromisoformat(str(stamp or "").strip().replace("Z","+00:00"))
    if d.tzinfo is None:
        return d
    return d.astimezone(timezone.utc).replace(tzinfo=None)


def read_original_gps(path, arms, tag_to_animal):
    tracks=defaultdict(set)
    audit=Counter()
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        rdr=csv.DictReader(f)
        col=set(rdr.fieldnames or [])
        required={"timestamp","location-lat","location-long"}
        if not required.issubset(col):
            raise ValueError("Original source missing expected GPS time and coordinate fields")
        if "individual-local-identifier" not in col and "tag-local-identifier" not in col:
            raise ValueError("Original GPS has no subject key")
        for row in rdr:
            animal=str(row.get("individual-local-identifier") or "").strip()
            if animal not in arms:
                tag=str(row.get("tag-local-identifier") or "").strip()
                animal=tag_to_animal.get(tag,"")
            if animal not in arms:
                audit["unmapped_original_fix"]+=1
                continue
            try:
                timestamp=utc(row.get("timestamp"))
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not (math.isfinite(lat) and math.isfinite(lon)
                        and -90<=lat<=90 and -180<=lon<=180):
                    raise ValueError("Invalid position")
            except (TypeError,ValueError,OverflowError):
                audit["invalid_source_fix"]+=1
                continue
            tracks[animal].add(timestamp)
            audit["valid_original_fix_rows"]+=1
    return tracks,audit


def max_gap_hours(values):
    return max(((b-a).total_seconds()/3600.0
                for a,b in zip(values,values[1:])),default=None)


def two_window_quality(time_values):
    points=sorted(set(time_values))
    if not points:
        return {"status":"NO_GPS_SOURCE","first_half_fixes":0,
                "second_half_fixes":0}
    start=points[0]
    elapsed=[((t-start).total_seconds()/3600.0,t) for t in points]
    early=[(h,t) for h,t in elapsed if 0<=h<WINDOW_HOURS]
    later=[(h,t) for h,t in elapsed if WINDOW_HOURS<=h<=2*WINDOW_HOURS]
    out={
      "first_half_fixes":len(early),
      "second_half_fixes":len(later),
      "original_unique_fix_count":len(points),
      "max_gap_first_half_hours":max_gap_hours([t for _,t in early]),
      "max_gap_second_half_hours":max_gap_hours([t for _,t in later]),
      "cross_12h_boundary_gap_hours":
          (later[0][1]-early[-1][1]).total_seconds()/3600
          if early and later else None,
      "initial_fix_equals_release_instant_verified":False,
    }
    if len(early)<MIN_UNIQUE_FIXES_PER_HALF or len(later)<MIN_UNIQUE_FIXES_PER_HALF:
        out["status"]="INSUFFICIENT_FIXES_IN_EARLY_OR_LATE_WINDOW"
        return out
    if not (early[0][0]<=MAX_FIRST_HALF_START_HOURS
        and early[-1][0]>=MIN_FIRST_HALF_END_HOURS
        and later[0][0]<=MAX_SECOND_HALF_START_HOURS
        and later[-1][0]>=MIN_SECOND_HALF_END_HOURS):
        out["status"]="INCOMPLETE_24H_BOUNDARY_COVERAGE"
        return out
    if (out["max_gap_first_half_hours"]>MAX_INTERNAL_GAP_HOURS or
        out["max_gap_second_half_hours"]>MAX_INTERNAL_GAP_HOURS or
        out["cross_12h_boundary_gap_hours"]>MAX_BOUNDARY_GAP_HOURS):
        out["status"]="GPS_SAMPLING_GAP_TOO_LONG"
        return out
    out["status"]="BOTH_12H_WINDOWS_GPS_SOURCE_ADMITTED"
    return out


def source_summary(arms,tracks,errors):
    by_arm=defaultdict(Counter)
    firstwindow={}
    for bird,times in tracks.items():
        group=arms[bird]
        result=two_window_quality(times)
        by_arm[group][result["status"]]+=1
        firstwindow[bird]=result
    for group in GROUPS:
        by_arm[group]["original_reference_subjects"]=REFERENCE[GROUPS.index(group)]
        by_arm[group]["GPS_originally_equipped"]=GPS_EQUIPPED[GROUPS.index(group)]
        observed=sum(v for k,v in by_arm[group].items()
                     if k not in ("original_reference_subjects","GPS_originally_equipped"))
        if observed!=ORIGINAL_GPS[GROUPS.index(group)]:
            raise ValueError("Original published GPS capture count changed")
        by_arm[group]["observed_GPS_subjects"]=observed
        by_arm[group]["GPS_equipped_but_no_original_fixes"]=(
            GPS_EQUIPPED[GROUPS.index(group)]-observed
        )
        by_arm[group]["Argos_assigned_by_design"]=ORIGINAL_ARGOS[GROUPS.index(group)]
    passed=all(by_arm[x]["BOTH_12H_WINDOWS_GPS_SOURCE_ADMITTED"]>=MIN_ELIGIBLE_PER_ARM
               for x in GROUPS)
    eligible_total=sum(by_arm[x]["BOTH_12H_WINDOWS_GPS_SOURCE_ADMITTED"] for x in GROUPS)
    result={
       "schema":"payoff_b_shearwater_first_vs_second_12h_source_observation_v1",
       "source_doi":"10.5441/001/1.tc76g560",
       "original_subjects":sum(REFERENCE),
       "original_GPS_equipped":sum(GPS_EQUIPPED),
       "valid_GPS_animals":sum(ORIGINAL_GPS),
       "original_Argos_assigned_separately":sum(ORIGINAL_ARGOS),
       "by_sensory_intervention":{
           group:dict(sorted(by_arm[group].items())) for group in GROUPS
       },
       "two_observed_windows_total_valid_GPS_subjects":eligible_total,
       "source_gate":{
          "minimum_GPS_animals_with_two_12h_windows_per_treatment":MIN_ELIGIBLE_PER_ARM,
          "passed":passed,
       },
       "source_invalid_or_unmapped_fix_counts":dict(sorted(errors.items())),
       "source_sampling_window_origin":"first valid published GPS fix, not certified release time",
       "source_cue_information_effect_estimated":False,
       "source_coastal_information_encounter_verified":False,
       "source_route_correction_or_fitness_effect_fitted":False,
       "sensitive_individual_observations_exported":False,
    }
    return result


def run():
    with tempfile.TemporaryDirectory() as td:
        paths={name:Path(td)/(name+".csv") for name in ("gps","reference")}
        hashes={name:download_verified(FILES[name],paths[name])
                for name in paths}
        arms,_,mapping=refs(paths["reference"])
        tags=reference_animal_tags(paths["reference"])
        tracks,errors=read_original_gps(paths["gps"],arms,tags)
        result=source_summary(arms,tracks,errors)
        result["original_CC0_file_checksums"]=hashes
        return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,
                        default=Path("outputs/payoff_b_shearwater_two_window_source.json"))
    args=parser.parse_args()
    report={
      "scientific_scope":"SOURCE_OBSERVATION_ELIGIBILITY_NOT_BEHAVIORAL_EFFECT",
      "method_predeclared_after_original_prior_art_review":True,
    }
    try:
        report["result"]=run()
        report["status"]="ORIGINAL_SHEARWATER_TWO_WINDOW_SOURCE_QC_COMPLETE"
    except (OSError,TypeError,ValueError) as exc:
        report["status"]="SOURCE_OR_OBSERVATION_GATE_FAILED"
        report["error"]=type(exc).__name__+": "+str(exc)[:260]
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if report["status"]!="ORIGINAL_SHEARWATER_TWO_WINDOW_SOURCE_QC_COMPLETE":
        raise SystemExit("Original high-frequency observation-gate failed")

if __name__=="__main__":
    main()
