"""PAYOFF-B V7: fail-closed readiness for registered q × geometry-only urgency.

Source: docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md.
This script never fits the target outcome. It only checks required source
grains and tells what is still unverified after uploaded 2015 supplement.
"""
import argparse,csv,json,math
from collections import Counter
from pathlib import Path
from scripts.payoff_b_v7_suppinfo_aggregate_gate import (
    ROOT,QP,REGIONS,readrows,audit_pairs
)

REQUIRED_ANNUAL={"flyway","region_code","year","gdd_jerk_onset_julian",
                 "original_source_identifier"}
REQUIRED_STOPS={"flyway","individual_id","year","source_region_code",
                "target_region_code","arrival_julian","breeding_attempt",
                "stopover_membership_source"}
REQUIRED_GEOMETRY={"flyway","region_code","centroid_lat","centroid_long",
                   "frozen_region_geometry_source"}
CONTRACT="docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md"

def inspect_optional(path,needed):
    if path is None:
        return {"status":"NOT_PROVIDED","required_columns":sorted(needed)}
    if not Path(path).is_file():
        return {"status":"FILE_NOT_FOUND","path":str(path)}
    entries=readrows(Path(path))
    if not entries:
        return {"status":"EMPTY_TABLE"}
    missing=needed-set(entries[0])
    if missing:
        return {"status":"MISSING_SOURCE_COLUMNS",
                "missing_columns":sorted(missing),
                "supplied_row_count":len(entries)}
    return {"status":"SCHEMA_COLUMNS_PRESENT_NOT_YET_ADMITTED",
            "supplied_row_count":len(entries),
            "source_columns":sorted(entries[0])}

def gate(annual=None,stops=None,geometry=None):
    q=readrows(QP)
    r=readrows(REGIONS)
    base=audit_pairs(q,r)
    consecutive=[x for x in q if x["consecutive"]=="1"]
    clean=[x for x in consecutive if x["source_alias_status"]=="exact"
           and x["target_alias_status"]=="exact"]
    annual_r=inspect_optional(annual,REQUIRED_ANNUAL)
    stop_r=inspect_optional(stops,REQUIRED_STOPS)
    geom_r=inspect_optional(geometry,REQUIRED_GEOMETRY)
    out={
      "status":"PAYOFF_B_V7_2015_UPLOADED_AGGREGATE_SOURCE_READINESS",
      "contract":CONTRACT,
      "user_uploaded_original_docx_sha256":base["uploaded_original_docx_sha256"],
      "source_30year_q_pairs":len(q),
      "consecutive_candidate_q_pairs":len(consecutive),
      "consecutive_q_without_unresolved_alias":len(clean),
      "meets_at_least_10_independent_q_transition_minimum_if_GPS_regions_confirm":len(clean)>=10,
      "annual_GDD_jerk_region_year_data":annual_r,
      "original_GPS_stopover_visits":stop_r,
      "original_independent_region_geometry":geom_r,
      "focal_bird_phenology_coefficient_fitted":False,
      "source_S1_30year_mean_does_not_replace_year_S_jy":True,
      "source_averaged_goose_stopover_duration_prohibited_as_geometry_U":True,
      "q_from_1982_2011_is_retrospective_and_not_actual_bird_knowledge":True,
      "source_gates_frozen_20161005":True
    }
    if annual_r["status"]!="SCHEMA_COLUMNS_PRESENT_NOT_YET_ADMITTED":
        out["stop_reason"]="MISSING_FOCAL_YEAR_REGION_SPECIFIC_GDD_ONSETS"
    elif stop_r["status"]!="SCHEMA_COLUMNS_PRESENT_NOT_YET_ADMITTED":
        out["stop_reason"]="MISSING_GPS_STOPOVER_MEMBERSHIP_AND_ACTUAL_ARRIVAL_DOY"
    elif geom_r["status"]!="SCHEMA_COLUMNS_PRESENT_NOT_YET_ADMITTED":
        out["stop_reason"]="MISSING_INDEPENDENT_REGIONAL_GEOMETRY_FOR_U"
    else:
        # Presence of a schema alone does not certify original region matches,
        # exact 40 complete migrations, ≥30 genuine stops, ≥2 flyways or q-U
        # non-collinearity. Real original values must be independently audited.
        out["stop_reason"]="ORIGINAL_ROW_AND_Q_U_ADMISSION_UNVERIFIED"
    out["V7_REGISTERED_PRIMARY_GATE"]="HOLD_NOT_ESTIMABLE"
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--annual-region-years",type=Path)
    p.add_argument("--gps-stopovers",type=Path)
    p.add_argument("--region-geometry",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    info=gate(a.annual_region_years,a.gps_stopovers,a.region_geometry)
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(info,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(info,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
