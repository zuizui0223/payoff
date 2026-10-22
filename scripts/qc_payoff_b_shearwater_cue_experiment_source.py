#!/usr/bin/env python3
"""Original CC0 experimental olfactory/magnetic cue manipulation source audit.

Pollonara et al. (2015) shearwater displacements. The paper's published
olfactory-navigation effect is PRIOR ART, not a new PAYOFF-B discovery.
Stage checks whether sensory intervention labels and original GPS/Argos
telemetry are aligned enough for independent information×recourse modelling.

Preserve original publisher's 'asnomic' spelling as alias of anosmic.
No original animal identifiers, exact site coordinates, release times,
GPS tracks, or individual homing outcomes leave the CI runner.
"""
from __future__ import annotations
import argparse,csv,json,math,statistics,tempfile
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
from scripts.qc_public_movebank_crossguild import download_verified

DOI="10.5441/001/1.tc76g560"
PAPER="10.1038/srep16486"
TAXON="Calonectris diomedea"
FILES={
 "gps":dict(uuid="13197a6e-ae74-4e81-b209-93c60fb16fe1",
            size=4420051,md5="35679733d880e26a17ddd7c51b5637eb"),
 "argos":dict(uuid="8df7ca3a-c7c8-423f-ae7d-15a0b3718cd7",
              size=44019,md5="7826b6457846cc9d6a1bb81dee65ca1f"),
 "reference":dict(uuid="20e10e5f-c500-419b-b835-8e2bbd23e799",
                  size=9867,md5="20a038104c926229690a8bcd11c365db"),
 "readme":dict(uuid="b9eaa4bd-977a-4bfd-8875-f8dde7c9e274",
               size=16541,md5="d45da171ce1445cb9a80f984c0050073"),
}
EXPECTED_REFERENCE_GROUPS={"control":9,"magnetic_disruption":9,"olfactory_deprivation":14}
MIN_TRACKED_TREATMENT_GROUPS=3
MIN_TOTAL_TRACKED_ORIGINAL_ANIMALS=12
MIN_EVENTS_PER_TRACK_FOR_COVERAGE=10


def arm(comments):
    s=str(comments or "").casefold()
    if "control group" in s:return "control"
    if "magnet" in s:return "magnetic_disruption"
    if any(x in s for x in ("anosmi","asnomic","olfact","zinc","smell-deprived")):
        return "olfactory_deprivation"
    return "UNRESOLVED_TREATMENT"


def refs(path):
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        r=csv.DictReader(f)
        cols=r.fieldnames or []
        required={"animal-id","tag-id","manipulation-comments","manipulation-type"}
        if not required.issubset(cols):
            raise ValueError("Original treatment-reference mapping fields absent")
        rows=list(r)
    if len(rows)!=32:raise ValueError("Original treatment archive does not have 32 rows")
    assignments={}
    tag_arms=defaultdict(set)
    unresolved=Counter()
    for row in rows:
        a=(row.get("animal-id") or "").strip()
        t=(row.get("tag-id") or "").strip()
        category=arm(row.get("manipulation-comments"))
        if not a or not t:raise ValueError("Original published animal/tag identity missing")
        if a in assignments and assignments[a]!=category:
            raise ValueError("One animal has mutually incompatible experimental groups")
        assignments[a]=category
        tag_arms[t].add(category)
        if category=="UNRESOLVED_TREATMENT":unresolved["unresolved_reference_rows"]+=1
    totals=Counter(arm(x.get("manipulation-comments")) for x in rows)
    if dict(totals)!=EXPECTED_REFERENCE_GROUPS or len(assignments)!=32:
        raise ValueError("Predeclared experimental group census did not reproduce")
    tags={tag:next(iter(v)) for tag,v in tag_arms.items() if len(v)==1}
    return assignments,tags,{
      "source_reference_deployments":len(rows),
      "distinct_original_birds_in_reference":len(assignments),
      "published_treatment_groups":dict(sorted(totals.items())),
      "tags_mapped_unambiguously_to_treatment":len(tags),
      "tags_with_conflicting_treatment_group":sum(len(v)>1 for v in tag_arms.values()),
      "published_spelling_alias_asnomic_used":True,
      "original_group_assignment_is_blinded_randomized":False,
      "individual_ring_tag_or_deployment_values_exported":False,
    }


def event_time(s):
    try:return datetime.fromisoformat(str(s or "").strip().replace("Z","+00:00"))
    except (ValueError,TypeError):return None


def tracking_stream(path,animal_groups,tag_groups):
    valid=Counter();unknown=Counter()
    per_animal=Counter()
    timestamps=defaultdict(list)
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as h:
        r=csv.DictReader(h)
        fields=r.fieldnames or []
        if not {"timestamp","location-lat","location-long"}.issubset(fields):
            return {
                "status":"SOURCE_EVENT_SCHEMA_MISSING",
                "required_timestamp_and_latlong_present":False,
                "public_source_columns_not_subject_values":fields,
            }
        available=[k for k in ("individual-local-identifier",
                               "tag-local-identifier") if k in fields]
        if not available:
            raise ValueError("Original GPS source has no registered animal or tag label")
        for event in r:
            identity=(event.get("individual-local-identifier") or "").strip()
            tag=(event.get("tag-local-identifier") or "").strip()
            treatment=animal_groups.get(identity) or tag_groups.get(tag)
            if treatment is None:
                unknown["original_event_unmatched_to_reference"]+=1
                continue
            stamp=event_time(event.get("timestamp"))
            try:
                lat=float(event.get("location-lat") or "")
                lon=float(event.get("location-long") or "")
            except (ValueError,TypeError):
                lat=lon=float("nan")
            if stamp is None or not (math.isfinite(lat) and math.isfinite(lon) and
                                     -90<=lat<=90 and -180<=lon<=180):
                unknown["original_event_invalid_time_or_position"]+=1
                continue
            animal=identity if identity in animal_groups else "tag:"+tag
            valid[treatment]+=1
            per_animal[(treatment,animal)]+=1
            timestamps[(treatment,animal)].append(stamp)
    over10=Counter()
    intervals=Counter()
    for (t,animal),n in per_animal.items():
        if n>=MIN_EVENTS_PER_TRACK_FOR_COVERAGE:over10[t]+=1
        times=sorted(timestamps[(t,animal)])
        for x,y in zip(times,times[1:]):
            d=(y-x).total_seconds()/3600.
            if d<=0:intervals["duplicate_or_nonmonotonic"]+=1
            elif d<=1:intervals["within_1_hour"]+=1
            elif d<=6:intervals["within_6_hours"]+=1
            elif d<=24:intervals["within_24_hours"]+=1
            else:intervals["more_than_24_hours"]+=1
    return {
      "status":"SOURCE_EVENT_COLUMNS_AUDITED",
      "original_valid_events_by_manipulation_group":dict(sorted(valid.items())),
      "source_animal_or_tag_labels_with_events_by_group":
          dict(sorted(Counter(k[0] for k in per_animal).items())),
      "individual_tracks_with_at_least_10_events":dict(sorted(over10.items())),
      "original_gap_counts_hour_bands":dict(sorted(intervals.items())),
      "events_missing_or_invalid":dict(sorted(unknown.items())),
      "source_GPS_and_Argos_track_IDs_may_repeat_the_same_bird":True,
      "actual_release_site_and_sensory_cue_chronology_verified":False,
      "individual_positions_IDs_dates_or_release_locations_exported":False,
    }


def run():
    with tempfile.TemporaryDirectory() as d:
        paths={name:Path(d)/(name+(".txt" if name=="readme" else ".csv"))
               for name in FILES}
        checks={name:download_verified(FILES[name],path) for name,path in paths.items()}
        reference,taggroups,ref_summary=refs(paths["reference"])
        gps=tracking_stream(paths["gps"],reference,taggroups)
        argos=tracking_stream(paths["argos"],reference,taggroups)
        groups=set(gps.get("original_valid_events_by_manipulation_group",{}))
        tracked=sum(gps.get("source_animal_or_tag_labels_with_events_by_group",{}).values())
        admissible=(len(groups)>=MIN_TRACKED_TREATMENT_GROUPS and
                    tracked>=MIN_TOTAL_TRACKED_ORIGINAL_ANIMALS and
                    all(gps.get("individual_tracks_with_at_least_10_events",{}).get(k,0)>0
                        for k in EXPECTED_REFERENCE_GROUPS))
        return {
          "study_DOI":DOI,
          "published_paper_DOI":PAPER,
          "published_taxon":TAXON,
          "public_original_CC0_file_integrity":checks,
          "original_reference":ref_summary,
          "original_GPS_sensor":gps,
          "original_Argos_sensor":argos,
          "predeclared_source_gate":{
              "min_tracking_groups":MIN_TRACKED_TREATMENT_GROUPS,
              "min_original_GPS_animal_labels":MIN_TOTAL_TRACKED_ORIGINAL_ANIMALS,
              "at_least_one_track_of_10_events_per_group":True,
              "passed":admissible,
          },
          "experimental_treatment_mapping_is_complete":True,
          "original_sensor_manipulation_effects_already_prior_art":True,
          "source_treatment_randomization_verified":False,
          "route_correction_and_actionability_effect_fitted":False,
          "phenological_or_vital_rate_outcome_evaluated":False,
          "raw_sensitive_tracking_data_exported":False,
        }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_unopened_shearwater"))
    a=p.parse_args()
    rec={"schema":"payoff_b_manipulated_shearwater_source_only_admission_20261023",
         "scientific_class":"PRIOR_PAPER_EXPERIMENTAL_CUE_STUDY_SOURCE_QC_ONLY"}
    try:
        rec["result"]=run()
        rec["status"]="CC0_EXPERIMENTAL_REFERENCE_AND_TELEMETRY_QC_COMPLETE"
    except (ValueError,OSError,TypeError) as e:
        rec["status"]="EXPERIMENT_SOURCE_QC_FAILED"
        rec["error"]=type(e).__name__+": "+str(e)[:320]
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"shearwater.json").write_text(
        json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(rec,ensure_ascii=False,indent=2))
    if rec["status"]!="CC0_EXPERIMENTAL_REFERENCE_AND_TELEMETRY_QC_COMPLETE":
        raise SystemExit("Original shearwater source integrity / group mapping failed")

if __name__=="__main__":main()
