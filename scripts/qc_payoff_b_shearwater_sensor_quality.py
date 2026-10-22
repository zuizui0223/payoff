#!/usr/bin/env python3
"""Shearwater experimental source quality: treatment-dependent GPS/Argos coverage.

CC0 original experiment was already published in Pollonara et al. 2015.
No treatment effect, route correction, behavioral decision or fitness inferred.
Original animal IDs, GPS, dates, nesting and release sites are kept private.
"""
from __future__ import annotations
import argparse,csv,json,tempfile
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_shearwater_cue_experiment_source import FILES,refs,arm,event_time,EXPECTED_REFERENCE_GROUPS

MAX_CONTIGUOUS_GAP_H=6.0
MIN_CONTIGUOUS_SEGMENT_H=24.0
MIN_FIXES_PER_ANIMAL=10
MIN_GPS_SUBJECTS_PER_GROUP=5


def reference_animal_tags(path):
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=32:raise ValueError("Original source reference cohort count changed")
    tag_to_animal={}
    for row in rows:
        tag=(row.get("tag-id") or "").strip()
        animal=(row.get("animal-id") or "").strip()
        if tag in tag_to_animal and tag_to_animal[tag]!=animal:
            raise ValueError("One original tag belongs to conflicting animals")
        tag_to_animal[tag]=animal
    return tag_to_animal


def stream_sensor(path,animal_arm,tag_to_animal):
    seen=defaultdict(list)
    errors=Counter()
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        rd=csv.DictReader(f)
        fields=rd.fieldnames or []
        if not {"timestamp","location-lat","location-long"}.issubset(fields):
            raise ValueError("Original sensor lacks timestamp and coordinates")
        for r in rd:
            ident=(r.get("individual-local-identifier") or "").strip()
            tag=(r.get("tag-local-identifier") or "").strip()
            animal=ident if ident in animal_arm else tag_to_animal.get(tag)
            if not animal:
                errors["unmapped_original_events"]+=1
                continue
            stamp=event_time(r.get("timestamp"))
            try:
                la=float(r.get("location-lat") or "")
                lo=float(r.get("location-long") or "")
                import math
                ok=math.isfinite(la) and math.isfinite(lo) and -90<=la<=90 and -180<=lo<=180
            except (ValueError,TypeError):
                ok=False
            if stamp is None or not ok:
                errors["invalid_source_event"]+=1
                continue
            seen[animal].append(stamp)
    return seen,errors


def maximal_contiguous_hours(times):
    """Continuous observed run: adjacent fixes no more than 6h apart."""
    ordered=sorted(set(times))
    if not ordered:return 0.
    start=last=ordered[0]
    longest=0.
    for t in ordered[1:]:
        gap=(t-last).total_seconds()/3600.
        if gap>MAX_CONTIGUOUS_GAP_H:
            longest=max(longest,(last-start).total_seconds()/3600.)
            start=t
        last=t
    return max(longest,(last-start).total_seconds()/3600.)


def sensor_qc(animals,arm_by_animal):
    groups=defaultdict(lambda:{"n_animals":0,"n_with_10plus_fixes":0,
                                "n_with_contiguous_24h":0,
                                "n_fixes":0,"n_with_24h_gap":0})
    for ident,times in animals.items():
        group=arm_by_animal.get(ident)
        if group is None:raise ValueError("Unknown reference treatment")
        s=groups[group]
        s["n_animals"]+=1
        s["n_fixes"]+=len(times)
        s["n_with_10plus_fixes"]+=len(times)>=MIN_FIXES_PER_ANIMAL
        s["n_with_contiguous_24h"]+=maximal_contiguous_hours(times)>=MIN_CONTIGUOUS_SEGMENT_H
        ordered=sorted(set(times))
        s["n_with_24h_gap"]+=any((v-u).total_seconds()>24*3600
                                   for u,v in zip(ordered,ordered[1:]))
    return {k:dict(v) for k,v in sorted(groups.items())}


def compare_sensors(arm_by_animal,gps,argos):
    group=defaultdict(Counter)
    for animal,category in arm_by_animal.items():
        g=animal in gps
        a=animal in argos
        group[category]["original_reference_subjects"]+=1
        group[category]["GPS_subjects"]+=g
        group[category]["Argos_subjects"]+=a
        group[category]["both_sensors_same_subject"]+=g and a
        group[category]["subjects_without_either_tracked_stream"]+=not g and not a
    if {k:v["original_reference_subjects"] for k,v in group.items()}!=EXPECTED_REFERENCE_GROUPS:
        raise ValueError("Original experiment group count changed")
    result={}
    for category,c in sorted(group.items()):
        result[category]={
            **dict(c),
            "GPS_subject_fraction_of_reference":
                c["GPS_subjects"]/c["original_reference_subjects"],
            "any_telemetry_subject_count":
                c["GPS_subjects"]+c["Argos_subjects"]-c["both_sensors_same_subject"],
        }
    return result


def run():
    with tempfile.TemporaryDirectory() as td:
        paths={k:Path(td)/(k+".txt" if k=="readme" else k+".csv") for k in FILES}
        source={k:download_verified(FILES[k],paths[k]) for k in FILES}
        arm_by_animal,_,ref=refs(paths["reference"])
        tags=reference_animal_tags(paths["reference"])
        gps,errors_gps=stream_sensor(paths["gps"],arm_by_animal,tags)
        argos,errors_argos=stream_sensor(paths["argos"],arm_by_animal,tags)
        rates=compare_sensors(arm_by_animal,gps,argos)
        quality_gps=sensor_qc(gps,arm_by_animal)
        quality_argos=sensor_qc(argos,arm_by_animal)
        data_gate=all(
            quality_gps.get(group,{}).get("n_with_contiguous_24h",0)>=
            MIN_GPS_SUBJECTS_PER_GROUP for group in EXPECTED_REFERENCE_GROUPS
        )
        return {
            "published_source_doi":"10.5441/001/1.tc76g560",
            "original_pinned_files":source,
            "original_reference_group_counts":ref["published_treatment_groups"],
            "groupwise_original_sensor_capture":rates,
            "GPS_within_group_observation_resolution":quality_gps,
            "Argos_within_group_observation_resolution":quality_argos,
            "source_missing_or_invalid_by_sensor":{
                "GPS":dict(sorted(errors_gps.items())),
                "Argos":dict(sorted(errors_argos.items())),
            },
            "predeclared_continuous_GPS_source_admission":{
                "min_24h_contiguous_tracks_in_each_arm":MIN_GPS_SUBJECTS_PER_GROUP,
                "max_observed_adjacent_fix_gap_hours":MAX_CONTIGUOUS_GAP_H,
                "passed":data_gate,
            },
            "measurement_sensor_distribution_depends_on_manipulation_group":True,
            "GPS_and_Argos_equal_positional_uncertainty":False,
            "original_navigation_and_coastal_decision_effects_prior_art":True,
            "future_route_correction_information_effect_estimated":False,
            "individual_fitness_benefit_estimated":False,
            "original_animal_locations_IDs_exact_dates_exported":False,
        }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_shearwater_sensor_quality"))
    a=p.parse_args()
    result={"schema":"payoff_b_shearwater_manipulation_sensor_coverage_audit_20261023"}
    try:result["result"]=run();result["status"]="ORIGINAL_PUBLIC_SENSOR_SELECTION_QC_COMPLETE"
    except (OSError,ValueError,TypeError) as e:
        result["status"]="SOURCE_SENSOR_QC_FAILED"
        result["error"]=type(e).__name__+": "+str(e)[:260]
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"shearwater.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["status"]!="ORIGINAL_PUBLIC_SENSOR_SELECTION_QC_COMPLETE":
        raise SystemExit("Experimental source sensor quality failed")


if __name__=="__main__":main()
