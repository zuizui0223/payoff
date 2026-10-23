#!/usr/bin/env python3
"""Full stationary-day risk set from original public MD5-pinned CC0 bird GPS.

Day-3 stationary eligibility depends only on previous source observations.
Next 2 days define outcome, with missing future explicitly right-censored.
No environment/outcome effect is fitted; no bird IDs, sites or dates exported.
"""
from __future__ import annotations
import argparse,json,math,statistics,tempfile
from collections import Counter,defaultdict
from datetime import timedelta
from pathlib import Path
from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import (
    SYSTEMS,daily_source_positions,detect_transfer_candidates,haversine,
    vector_mean_lon,STATIONARY_RADIUS_KM,FIRST_MOVE_DISTANCE_KM,
    TWO_DAY_MOVE_DISTANCE_KM,TWO_DAY_NORTHING_DEGREES,
)

EXPECTED={"stork":145,"white_fronted_goose":106,"curlew":59}
LABELS=("NORTHWARD_CANDIDATE","STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED")


def site_three(anchor):
    if len(anchor)!=3:raise ValueError("Expected 3 stationary days")
    return (statistics.median(v[1] for v in anchor),
            vector_mean_lon(sum(math.cos(math.radians(v[2])) for v in anchor),
                            sum(math.sin(math.radians(v[2])) for v in anchor)))


def label_future(center,followup):
    if not followup or not all(followup):return "CENSORED"
    a,b=followup
    d1=haversine(*center,a[1],a[2])
    d2=haversine(*center,b[1],b[2])
    if (d1>=FIRST_MOVE_DISTANCE_KM and d2>=TWO_DAY_MOVE_DISTANCE_KM
            and b[1]-center[0]>=TWO_DAY_NORTHING_DEGREES):
        return "NORTHWARD_CANDIDATE"
    if d1<=STATIONARY_RADIUS_KM and d2<=STATIONARY_RADIUS_KM:
        return "STAYED_TWO_DAYS"
    return "OTHER_MOVEMENT"


def risk_opportunities(daily):
    """Every 3-day stationary anchor, including animals that never depart."""
    p=sorted(daily)
    by_day={r[0]:r for r in p}
    for i in range(2,len(p)):
        anchor=p[i-2:i+1]
        if any((anchor[k+1][0]-anchor[k][0]).days!=1 for k in range(2)):
            continue
        center=site_three(anchor)
        if max(haversine(*center,r[1],r[2]) for r in anchor)>STATIONARY_RADIUS_KM:
            continue
        day=anchor[-1][0]
        next_two=[by_day.get(day+timedelta(days=j)) for j in (1,2)]
        yield day,center,label_future(center,next_two)


def collect(groups):
    counts=Counter()
    month=defaultdict(Counter)
    yearcounts=defaultdict(Counter)
    private=[]
    frozen_all=set()
    raw_all=set()
    for group,track in sorted(groups.items()):
        tax,ident,year=group
        _,frozen=detect_transfer_candidates(track)
        counts["deduplicated_frozen_cases"]+=len(frozen)
        for day in frozen:frozen_all.add((group,day))
        n=0
        case=False
        stayed=False
        for day,center,label in risk_opportunities(track):
            n+=1
            private.append((group,day,center,label))
            counts[label]+=1
            month[(tax,day.month)][label]+=1
            yearcounts[(tax,year)][label]+=1
            case=case or label=="NORTHWARD_CANDIDATE"
            stayed=stayed or label=="STAYED_TWO_DAYS"
            if label=="NORTHWARD_CANDIDATE":raw_all.add((group,day))
        counts["animal_years_with_risk_opportunities"]+=bool(n)
        counts["animal_years_with_any_departure_proxy"]+=case
        counts["animal_years_with_any_stay_proxy"]+=stayed
    if not frozen_all.issubset(raw_all):
        raise ValueError("Frozen earlier case detector omitted from risk-set labels")
    counts["all_at_risk_stationary_days"]=len(private)
    counts["raw_unthinned_departure_labels"]=len(raw_all)
    counts["frozen_cases_reconstructed"]=len(frozen_all)
    return private,counts,month,yearcounts


def receipt(groups,system):
    private,c,month,year=collect(groups)
    if c["deduplicated_frozen_cases"]!=EXPECTED[system]:
        raise ValueError("Original case count was not reproduced")
    denom=c["NORTHWARD_CANDIDATE"]+c["STAYED_TWO_DAYS"]
    return {
      "schema":"payoff_b_complete_source_risk_days_v1",
      "source_system":system,
      "eligibility":"all 3-day stationary original GPS windows before day4/5",
      "counts":dict(sorted(c.items())),
      "source_month_counts":{
          f"{tax}|{month:02d}":dict(sorted(x.items()))
          for (tax,month),x in sorted(month.items())
      },
      "source_year_counts":{
          f"{tax}|{year}":dict(sorted(x.items()))
          for (tax,year),x in sorted(year.items())
      },
      "candidate_fraction_among_resolved_move_or_stay":(
          c["NORTHWARD_CANDIDATE"]/denom if denom else None),
      "candidate_fraction_is_true_departure_hazard":False,
      "risk_entry_uses_future_information":False,
      "labels_only_use_observed_day4_and_day5":True,
      "censored_cases_labeled_stay":False,
      "other_movements_labeled_stay":False,
      "daily_risk_records_independent_samples":False,
      "weather_analyzed":False,"bird_cue_use_estimated":False,
      "physical_recourse_or_fitness_estimated":False,
      "original_IDs_event_dates_or_positions_exported":False
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--system",choices=SYSTEMS,required=True)
    parser.add_argument("--out",type=Path,default=Path("outputs/payoff_b_complete_riskset"))
    a=parser.parse_args()
    result={"source_system":a.system,"status":"NOT_OPENED",
            "analysis":"SOURCE_ONLY_COMPLETE_RISKSET"}
    try:
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"original.csv"
            doi,taxon,sensor,checksum=origin_source(a.system,path)
            groups,quality,identity=daily_source_positions(path,taxon)
            result.update(source_doi=doi,source_taxon=taxon,
                original_file_integrity=checksum,
                coverage=receipt(groups,a.system),
                status="COMPLETE_STATIONARY_RISKSET_VERIFIED")
    except (OSError,ValueError,TypeError) as e:
        result.update(status="SOURCE_RISKSET_FAILURE",
                      error=type(e).__name__+": "+str(e)[:350])
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if result["status"]!="COMPLETE_STATIONARY_RISKSET_VERIFIED":
        raise SystemExit("Original risk-set source audit failed")

if __name__=="__main__":main()
