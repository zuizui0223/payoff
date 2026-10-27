#!/usr/bin/env python3
"""Exploratory 0-12h versus 12-24h homing-progress proxy.

Original Pollonara 2015 source route effects are prior art, NOT a new PAYOFF
discovery. Source-only two-window GPS coverage was prechecked separately.
Publish only treatment-arm aggregates and no bird IDs/locations/timestamps.
"""
from __future__ import annotations
import argparse,csv,json,math,statistics,tempfile
from collections import Counter,defaultdict
from datetime import timezone
from pathlib import Path
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_shearwater_cue_experiment_source import FILES,refs
from scripts.qc_payoff_b_shearwater_sensor_quality import reference_animal_tags
from scripts.qc_payoff_b_shearwater_two_window_source import two_window_quality,utc
from scripts.audit_payoff_b_shearwater_device_allocation import (
 GROUPS,REFERENCE,GPS_EQUIPPED,ORIGINAL_GPS)

# Midpoint of 2 study colony coordinates published by Pollonara et al.
HOME=(42.576,10.0985)
MIN_PATH=20.
MIN_START_HOME_DISTANCE=100.
MIN_LATE_HOME_DISTANCE=20.
MAX_STEP_SPEED=100.
R=6371.0088

def km(a,b):
    la1,lo1=map(math.radians,a);la2,lo2=map(math.radians,b)
    dlat=la2-la1;dlon=(lo2-lo1+math.pi)%(2*math.pi)-math.pi
    h=math.sin(dlat/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(max(0.,min(1.,h))))

def tracks_from_cc0(source,arms,tags):
    values=defaultdict(dict);qc=Counter()
    with Path(source).open(encoding="utf-8-sig",errors="replace",newline="") as h:
        reader=csv.DictReader(h)
        if not {"timestamp","location-lat","location-long"}.issubset(reader.fieldnames or []):
            raise ValueError("Original GPS fields missing")
        for row in reader:
            bird=(row.get("individual-local-identifier") or "").strip()
            if bird not in arms:
                bird=tags.get((row.get("tag-local-identifier") or "").strip(),"")
            if bird not in arms:
                qc["unmatched_source_fix"]+=1;continue
            try:
                t=utc(row.get("timestamp"))
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not (math.isfinite(lat) and math.isfinite(lon) and -90<=lat<=90 and -180<=lon<=180):
                    raise ValueError("bad fix")
            except (ValueError,TypeError,OverflowError):
                qc["invalid_source_fix"]+=1;continue
            current=values[bird].get(t)
            if current is not None and current!=(lat,lon):
                raise ValueError("Same timestamp with contradictory GPS locations")
            if current is not None:
                qc["repeated_identical_time"]+=1
            values[bird][t]=(lat,lon)
            qc["valid_fix_row"]+=1
    return values,qc

def segment(points,origin,window):
    start,end=window
    chosen=[]
    for t,coord in points:
        hours=(t-origin).total_seconds()/3600.
        if start<=hours<end or (end==24 and hours==24):
            chosen.append((t,coord))
    if len(chosen)<6:return {"status":"INSUFFICIENT_FIXES"}
    path=0.
    for (t0,c0),(t1,c1) in zip(chosen,chosen[1:]):
        hours=(t1-t0).total_seconds()/3600.
        if hours<=0:return {"status":"INVALID_TIME_ORDER"}
        step=km(c0,c1)
        if step/hours>MAX_STEP_SPEED:return {"status":"OUTLIER_SPEED"}
        path+=step
    if path<MIN_PATH:return {"status":"INSUFFICIENT_TRAVEL_DISTANCE"}
    startdist=km(chosen[0][1],HOME)
    enddist=km(chosen[-1][1],HOME)
    progress=(startdist-enddist)/path
    if abs(progress)>1.00001:raise ValueError("Invalid geodesic progress index")
    return {"status":"PROGRESS_CALCULATED","start_colony_dist":startdist,
            "efficiency":max(-1.,min(1.,progress))}

def evaluate(events):
    times=sorted(events)
    q=two_window_quality(times)
    if q["status"]!="BOTH_12H_WINDOWS_GPS_SOURCE_ADMITTED":
        return {"status":"TWO_WINDOW_GPS_NOT_ADMITTED"}
    pts=[(t,events[t]) for t in times]
    early=segment(pts,times[0],(0.,12.))
    late=segment(pts,times[0],(12.,24.))
    if early["status"]!="PROGRESS_CALCULATED":
        return {"status":"EARLY_"+early["status"]}
    if late["status"]!="PROGRESS_CALCULATED":
        return {"status":"LATE_"+late["status"]}
    if early["start_colony_dist"]<MIN_START_HOME_DISTANCE:
        return {"status":"FIRST_GPS_FIX_TOO_NEAR_HOME"}
    if late["start_colony_dist"]<MIN_LATE_HOME_DISTANCE:
        return {"status":"SECOND_WINDOW_NEAR_COLONY"}
    delta=late["efficiency"]-early["efficiency"]
    return {"status":"BOTH_STAGE_PROGRESS_ESTIMABLE","early":early["efficiency"],
            "late":late["efficiency"],"change":delta,"improved":delta>0}

def bound(success,observed,denom):
    if not 0<=success<=observed<=denom:raise ValueError("invalid bounds")
    return [success/denom,(success+denom-observed)/denom]

def summarise(arms,tracks):
    outcomes=defaultdict(list);reasons=defaultdict(Counter)
    for animal,group in arms.items():
        val=evaluate(tracks.get(animal,{}))
        reasons[group][val["status"]]+=1
        if val["status"]=="BOTH_STAGE_PROGRESS_ESTIMABLE":
            outcomes[group].append(val)
    result={}
    for i,group in enumerate(GROUPS):
        n=REFERENCE[i];equipped=GPS_EQUIPPED[i]
        observed=sum(bool(tracks.get(a)) and g==group for a,g in arms.items())
        if observed!=ORIGINAL_GPS[i] or sum(reasons[group].values())!=n:
            raise ValueError("Publisher treatment/device denominator changed")
        good=outcomes[group];k=len(good);wins=sum(x["improved"] for x in good)
        result[group]={
            "original_treated_subjects":n,"GPS_equipped_subjects":equipped,
            "GPS_observed_subjects":observed,"two_window_progress_eligible":k,
            "observed_progress_improvement_binary":wins,
            "source_status_counts":dict(sorted(reasons[group].items())),
            "median_early_progress":statistics.median(x["early"] for x in good) if k else None,
            "median_late_progress":statistics.median(x["late"] for x in good) if k else None,
            "median_late_minus_early_progress":statistics.median(x["change"] for x in good) if k else None,
            "sharp_outcome_rate_bound_among_all_assigned":bound(wins,k,n),
            "sharp_outcome_rate_bound_among_GPS_equipped":bound(wins,k,equipped),
        }
    def diff(a,b):
        return [a[0]-b[1],a[1]-b[0]]
    olf=result["olfactory_deprivation"]["sharp_outcome_rate_bound_among_all_assigned"]
    mag=result["magnetic_disruption"]["sharp_outcome_rate_bound_among_all_assigned"]
    ctl=result["control"]["sharp_outcome_rate_bound_among_all_assigned"]
    return {
        "source":"10.5441/001/1.tc76g560",
        "classification":"EXPLORATORY_PRIOR_ART_SECONDARY_BEHAVIOR_PROXY",
        "source_reference_subjects":sum(REFERENCE),
        "source_GPS_equipped":sum(GPS_EQUIPPED),
        "source_GPS_observed":sum(ORIGINAL_GPS),
        "original_arm_results":result,
        "overall_progress_eligible":sum(v["two_window_progress_eligible"] for v in result.values()),
        "olfactory_vs_control_sharp_full_arm_improvement_difference_bound":diff(olf,ctl),
        "magnetic_vs_control_sharp_full_arm_improvement_difference_bound":diff(mag,ctl),
        "true_signal_access_measured":False,
        "coast_encounter_measured":False,
        "phenological_recourse_or_fitness_measured":False,
        "causal_treatment_effect_identified":False,
        "first_original_GPS_fix_is_release_time":False,
        "GPS_coordinates_IDs_dates_exported":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_shearwater_stage_proxy.json"))
    a=p.parse_args()
    out={"schema":"payoff_b_shearwater_two_stage_source_proxy_20261028"}
    try:
        with tempfile.TemporaryDirectory() as d:
            gps=Path(d)/"gps.csv";ref=Path(d)/"reference.csv"
            originals={"gps":download_verified(FILES["gps"],gps),
                       "reference":download_verified(FILES["reference"],ref)}
            arms,_,_=refs(ref)
            tags=reference_animal_tags(ref)
            tracks,qc=tracks_from_cc0(gps,arms,tags)
            data=summarise(arms,tracks)
            data["source_pinned_MD5_and_bytes"]=originals
            data["GPS_fix_integrity_counts"]=dict(sorted(qc.items()))
            out["result"]=data
            out["status"]="STAGEWISE_SOURCE_DESCRIPTIVE_AND_BOUNDS_COMPLETE"
    except (OSError,ValueError,TypeError) as err:
        out["status"]="SOURCE_GEOMETRY_OR_IDENTITY_FAILURE"
        out["error"]=type(err).__name__+": "+str(err)[:300]
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    if out["status"]!="STAGEWISE_SOURCE_DESCRIPTIVE_AND_BOUNDS_COMPLETE":
        raise SystemExit("Source-stagewise calibration failed")

if __name__=="__main__":main()
