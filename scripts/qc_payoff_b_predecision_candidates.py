#!/usr/bin/env python3
"""Source-only high-confidence stationary-to-northward GPS departures.

This is NOT true decision-time cue uptake or active timing correction.
Only aggregate counts leave the CI runner. Thresholds are frozen here before
the five-day source events are screened.
"""
from __future__ import annotations
import argparse,csv,json,math,statistics,tempfile
from collections import Counter,defaultdict
from datetime import datetime,timedelta
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source

SYSTEMS=("stork","curlew","white_fronted_goose")
MONTHS={2,3,4,5}
MIN_HOURLY_BINS_PER_DAY=2
STATIONARY_RADIUS_KM=30.0
FIRST_MOVE_DISTANCE_KM=30.0
TWO_DAY_MOVE_DISTANCE_KM=120.0
TWO_DAY_NORTHING_DEGREES=0.8
MIN_EVENT_SEPARATION_DAYS=7

def haversine(lat1,lon1,lat2,lon2):
    r=math.pi/180
    p1,p2=lat1*r,lat2*r
    dp=(lat2-lat1)*r
    dl=(lon2-lon1)*r
    a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 6371.0088*2*math.atan2(math.sqrt(max(0,a)),math.sqrt(max(0,1-a)))

def vector_mean_lon(cos_sum,sin_sum):
    if abs(cos_sum)+abs(sin_sum)<1e-12:
        raise ValueError("Longitude resultant undefined")
    return math.degrees(math.atan2(sin_sum,cos_sum))

def daily_source_positions(path,source_taxon):
    aggregate=defaultdict(lambda:[0.0,0.0,0.0,0])
    hour_bins=defaultdict(set)
    counters=Counter()
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        rd=csv.DictReader(f)
        fields=rd.fieldnames or []
        if not {"timestamp","location-lat","location-long"}.issubset(fields):
            raise ValueError("Required original GPS time/position columns missing")
        identity=next((v for v in ("individual-local-identifier",
                                  "deployment-id","tag-local-identifier")
                       if v in fields),None)
        if identity is None:
            raise ValueError("Original source lacks animal/deployment identity")
        for row in rd:
            try:
                stamp=datetime.fromisoformat((row.get("timestamp") or "").strip().replace("Z","+00:00"))
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not math.isfinite(lat) or not math.isfinite(lon) or not -90<=lat<=90 or not -180<=lon<=180:
                    raise ValueError("Out-of-range GPS")
            except (TypeError,ValueError):
                counters["invalid_timestamp_or_position"]+=1
                continue
            ident=(row.get(identity) or "").strip()
            if not ident:
                counters["empty_identity"]+=1
                continue
            if stamp.month not in MONTHS:
                counters["outside_original_spring_months"]+=1
                continue
            tax=(row.get("individual-taxon-canonical-name") or "").strip() or source_taxon
            k=(tax,ident,stamp.year,stamp.date())
            a=aggregate[k]
            a[0]+=lat
            a[1]+=math.cos(math.radians(lon))
            a[2]+=math.sin(math.radians(lon))
            a[3]+=1
            hour_bins[k].add(stamp.hour)
            counters["valid_spring_fixes"]+=1

    by_animal_year=defaultdict(list)
    excluded=0
    for (tax,ident,yr,day),sums in aggregate.items():
        if len(hour_bins[(tax,ident,yr,day)])<MIN_HOURLY_BINS_PER_DAY:
            excluded+=1
            continue
        try:
            lat=sums[0]/sums[3]
            lon=vector_mean_lon(sums[1],sums[2])
        except ValueError:
            excluded+=1
            continue
        by_animal_year[(tax,ident,yr)].append((day,lat,lon))
    counters["days_with_too_few_independent_hour_bins"]=excluded
    return by_animal_year,counters,identity


def detect_transfer_candidates(daily):
    """5 consecutive observed UTC days: 3 stationary, then 2 northward."""
    positions=sorted(daily)
    windows=0
    candidates=[]
    last=None
    for i in range(2,len(positions)-2):
        five=positions[i-2:i+3]
        if any((five[j+1][0]-five[j][0]).days!=1 for j in range(4)):
            continue
        windows+=1
        anchor=five[:3]
        lat=statistics.median(v[1] for v in anchor)
        lon=vector_mean_lon(
            sum(math.cos(math.radians(v[2])) for v in anchor),
            sum(math.sin(math.radians(v[2])) for v in anchor))
        if max(haversine(lat,lon,v[1],v[2]) for v in anchor)>STATIONARY_RADIUS_KM:
            continue
        first=five[3]
        second=five[4]
        if haversine(lat,lon,first[1],first[2])<FIRST_MOVE_DISTANCE_KM:
            continue
        if haversine(lat,lon,second[1],second[2])<TWO_DAY_MOVE_DISTANCE_KM:
            continue
        if second[1]-lat<TWO_DAY_NORTHING_DEGREES:
            continue
        candidate=five[2][0]
        if last is not None and (candidate-last).days<MIN_EVENT_SEPARATION_DAYS:
            continue
        candidates.append(candidate)
        last=candidate
    return windows,candidates


def source_audit(groups,counters,source_id):
    by_tax=defaultdict(Counter)
    candidates_by_year=Counter()
    first_years=Counter()
    animals_with_candidates=defaultdict(set)
    total_windows=0
    total_candidates=0
    repeat_event_identity_years=0
    for (tax,ident,year),daily in groups.items():
        windows,dates=detect_transfer_candidates(daily)
        by_tax[tax]["animal_years_with_geovalid_days"]+=1
        by_tax[tax]["calendar_consecutive_five_day_windows"]+=windows
        by_tax[tax]["candidate_stationary_to_northward_events"]+=len(dates)
        by_tax[tax]["animal_years_with_one_or_more_candidates"]+=int(bool(dates))
        candidates_by_year[str(year)]+=len(dates)
        animals_with_candidates[tax].update([ident] if dates else [])
        total_windows+=windows
        total_candidates+=len(dates)
        repeat_event_identity_years+=int(len(dates)>1)
    for tax,animals in animals_with_candidates.items():
        by_tax[tax]["distinct_animal_IDs_with_candidate_events"]=len(animals)
    return {
        "schema":"payoff_b_stationary_to_northward_candidate_source_qc_v1",
        "source_identity_field":source_id,
        "classified_source_taxa":{k:dict(sorted(v.items()))
                                  for k,v in sorted(by_tax.items())},
        "candidate_events_by_calendar_year":dict(sorted(candidates_by_year.items())),
        "total_candidate_events":total_candidates,
        "total_consecutive_five_day_windows":total_windows,
        "animal_years_with_multiple_candidate_events":repeat_event_identity_years,
        "original_source_quality":dict(sorted(counters.items())),
        "time_standard":"UTC calendar-day aggregate; no inferred precise departure instant",
        "frozen_gate":{
            "calendar_months":"February-May",
            "independent_hour_bins_per_day_min":MIN_HOURLY_BINS_PER_DAY,
            "consecutive_preposition_days":3,
            "observed_followup_days":2,
            "stationary_radius_max_km":STATIONARY_RADIUS_KM,
            "first_outbound_day_min_distance_km":FIRST_MOVE_DISTANCE_KM,
            "two_day_outbound_min_distance_km":TWO_DAY_MOVE_DISTANCE_KM,
            "two_day_northward_latitude_min_degrees":TWO_DAY_NORTHING_DEGREES,
            "candidate_min_separation_days":MIN_EVENT_SEPARATION_DAYS,
        },
        "published_source_stopovers_validated":False,
        "actual_decision_timestamp_known":False,
        "predecision_weather_joined":False,
        "cue_information_causally_used":False,
        "remaining_feasible_recourse_measured":False,
        "bird_response_or_fitness_effect_tested":False,
        "individual_identifiers_or_track_points_exported":False,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SYSTEMS,required=True)
    ap.add_argument("--out",type=Path,
                    default=Path("outputs/payoff_b_departure_source_qc"))
    args=ap.parse_args()
    out={"system":args.system,"status":"NOT_OPENED","analysis":"SOURCE_ONLY_BEHAVIORAL_EVENT_ELIGIBILITY"}
    try:
        with tempfile.TemporaryDirectory() as d:
            raw=Path(d)/"original.csv"
            doi,taxon,sensor,integrity=origin_source(args.system,raw)
            groups,counters,idcol=daily_source_positions(raw,taxon)
            out.update(source_doi=doi,publisher_taxa=taxon,source_sensor=sensor,
                       original_file_integrity=integrity,
                       result=source_audit(groups,counters,idcol),
                       status="CANDIDATE_SOURCE_SCREEN_COMPLETE")
    except (OSError,ValueError,TypeError) as e:
        out["status"]="SOURCE_OR_EVENT_PROCESS_FAILED"
        out["error"]=type(e).__name__+": "+str(e)[:400]
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    if out["status"]!="CANDIDATE_SOURCE_SCREEN_COMPLETE":
        raise SystemExit("Predecision checkpoint source screen failed")

if __name__=="__main__":main()
