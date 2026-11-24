#!/usr/bin/env python3
"""Post-open source-only fine GPS triplet test in previously fixed coarse keys.

This analyses only the 11/16 *previously observed* three-cohort overlapping
hour-cells. It never claims to enumerate contacts outside coarse-bin gating,
and does not infer information use, q, recourse, adaptation or fitness.

Exact Bontekoe 2023 CC0 archive subset (one smallest original ZIP/cohort),
full original DSpace MD5 authentication, CRC to EOF, parent count gates.
Private raw GPS event values are held only in memory during GitHub CI.
Output contains ONLY totals and full-source provenance, never matching times,
positions, event IDs, tag IDs, grid keys, days or within-key source rows.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import date
import io
import json
import math
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import zipfile
from hashlib import sha256

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

from payoff_b_stork_original_gps_date_coverage_20261124 import (
    get_original_zip_entry, download_original_zip, choose_main_member,
    expected_columns, parse_coord
)
from payoff_b_stork_gps_coarse_hour_cell_20261124 import (
    source_scan_main_csv, verify_against_first_pass,
    cell_hour_key, parse_UTC_dt, count_years, cross_cohort_support
)

CONTRACT=HERE.parent/"data/payoff_b_stork_triple_proximity_contract_20261124.json"
ORIGINAL=HERE.parent/"data/payoff_b_stork_original_gps_date_coverage_contract_20261124.json"
HEADERS=HERE.parent/"data/payoff_b_stork_gps_csv_header_result_20261124.json"
COARSE=HERE.parent/"data/payoff_b_stork_original_gps_coarse_hour_cell_result_20261124.json"
PR421_RECEIPTS={
    key:HERE.parent/f"data/payoff_b_stork_original_gps_date_{key}_result_20261124.json"
    for key in ("control","delayed","naturally_timed")
}
COHORTS=("control","delayed","naturally_timed")
EARTH_METERS=6371008.8

def haversine_meters(x,y):
    """True spherical point-to-point distance; not a cell width proxy."""
    _,lat1,lon1=x
    _,lat2,lon2=y
    phi1=math.radians(lat1)
    phi2=math.radians(lat2)
    dphi=math.radians(lat2-lat1)
    dlam=math.radians(lon2-lon1)
    a=math.sin(dphi/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return EARTH_METERS*2*math.asin(math.sqrt(min(1.0,max(0.0,a))))

def exactly_one_triplet(grouped,max_span_s,max_distance_m):
    """Exists a cohort triplet with maximum time span/radius pairwise bound.

    Each list contains (epoch seconds, lat, lon). All 3 pairwise distances
    and global max-minus-min UTC timestamp must satisfy inclusive bounds.
    """
    if len(grouped)!=3 or any(not v for v in grouped):
        return False
    a,b,c=[sorted(v) for v in grouped]
    bt=[x[0] for x in b]
    ct=[x[0] for x in c]
    for x in a:
        # A-B time span cannot exceed allowed whole-triplet span.
        ilo=bisect_left(bt,x[0]-max_span_s)
        ihi=bisect_right(bt,x[0]+max_span_s)
        for y in b[ilo:ihi]:
            if haversine_meters(x,y)>max_distance_m:
                continue
            # A-C and B-C time tests imply max-min <= limit.
            start=max(x[0],y[0])-max_span_s
            end=min(x[0],y[0])+max_span_s
            jlo=bisect_left(ct,start)
            jhi=bisect_right(ct,end)
            for z in c[jlo:jhi]:
                if (
                    max(x[0],y[0],z[0])-min(x[0],y[0],z[0])<=max_span_s
                    and haversine_meters(x,z)<=max_distance_m
                    and haversine_meters(y,z)<=max_distance_m
                ):
                    return True
    return False

def collect_fixes(source,header,asof,candidates,contract):
    """Only candidate-key source fixes; ephemeral and never exported."""
    groups={10:defaultdict(list),5:defaultdict(list)}
    count=0
    max_total=int(contract["privacy"]["max_stored_candidate_event_fixes_per_cohort"])
    max_per=int(contract["privacy"]["max_fixes_per_candidate_key_per_cohort"])
    import csv
    reader=csv.DictReader(source)
    if (reader.fieldnames or [])!=header:
        raise ValueError("Original GPS member column names drifted")
    for row in reader:
        dt=parse_UTC_dt(row.get("timestamp"),asof)
        if dt is None:
            continue
        tag=str(row.get("tag-local-identifier") or "").strip()
        if not tag:
            continue
        ok_lat,_=parse_coord(row.get("location-lat"),-90,90)
        ok_lon,_=parse_coord(row.get("location-long"),-180,180)
        if not ok_lat or not ok_lon:
            continue
        lat=float(row["location-lat"])
        lon=float(row["location-long"])
        hour=dt.date().toordinal()*24+dt.hour
        fix=(dt.timestamp(),lat,lon)
        for units in (10,5):
            key=cell_hour_key(hour,lat,lon,units)
            if key not in candidates[units]:
                continue
            values=groups[units][key]
            values.append(fix)
            count+=1
            if count>max_total or len(values)>max_per:
                raise ValueError("Original coarse-candidate fix source exceeded frozen privacy cap")
    return groups

def compute(contract,original,headers,coarse,receipts):
    asof=date.fromisoformat(original["reference_day"])
    scans={}
    with TemporaryDirectory(prefix="payoff_b_stork_private_CC0_gps_") as private:
        zip_paths={}
        for cohort in COHORTS:
            archive_info=original["source_origins"][cohort]
            url,size,md5=get_original_zip_entry(cohort,original)
            path=Path(private)/f"private_source_{cohort}.zip"
            auth=download_original_zip(url,size,md5,path)
            if auth["full_original_zip_md5_source_verified"] is not True:
                raise ValueError("Original ZIP MD5 did not verify")
            zip_paths[cohort]=path
            with zipfile.ZipFile(path,"r") as archive:
                member=choose_main_member(archive,cohort,original)
                with archive.open(member,"r") as binary:
                    with io.TextIOWrapper(binary,encoding="utf-8-sig",newline="") as stream:
                        scan=source_scan_main_csv(stream,expected_columns(cohort,headers),asof)
            verify_against_first_pass(scan,receipts[cohort])
            original_aggregate=coarse["three_cohort_source"][cohort]
            checks=[
              (scan["n_raw_rows"],original_aggregate["n_original_GPS_rows_checked"]),
              (scan["n_valid_georeferenced_rows"],original_aggregate["n_original_valid_GPS_rows_checked"]),
              (len(scan["day_ordinals"]),original_aggregate["n_UTC_days_with_valid_GPS"]),
              (len(scan["hour_ordinals"]),original_aggregate["n_UTC_hours_with_valid_GPS"]),
              (len(scan["cell_hour_keys"][10]),original_aggregate["n_UTC_hour_0p1_degree_cells"]),
              (len(scan["cell_hour_keys"][5]),original_aggregate["n_UTC_hour_0p2_degree_cells"]),
            ]
            if any(a!=b for a,b in checks):
                raise ValueError("Original PR422 source cohort count drift")
            scans[cohort]=scan
        derived=cross_cohort_support(scans)
        if derived["three_cohort_aggregate"]!=coarse["three_cohort_aggregate"]:
            raise ValueError("PR422 original-source three-cohort aggregate changed")
        candidates={
            10:set.intersection(*(scans[k]["cell_hour_keys"][10] for k in COHORTS)),
            5:set.intersection(*(scans[k]["cell_hour_keys"][5] for k in COHORTS))
        }
        if len(candidates[10])!=contract["candidate_expected_counts"]["0p1_degree"] or len(candidates[5])!=contract["candidate_expected_counts"]["0p2_degree"]:
            raise ValueError("Originally frozen coarse candidate counts changed")
        if (count_years(candidates[10],"cells")!=[{"year":2020,"n_bins":11}]
            or count_years(candidates[5],"cells")!=[{"year":2020,"n_bins":16}]):
            raise ValueError("Source candidate year support changed")
        # Releases only raw tag strings stored by original first pass; original
        # independent GPS fixes are re-opened from private authenticated ZIPs.
        scans.clear()
        fixes={}
        for cohort in COHORTS:
            with zipfile.ZipFile(zip_paths[cohort],"r") as archive:
                member=choose_main_member(archive,cohort,original)
                with archive.open(member,"r") as binary:
                    with io.TextIOWrapper(binary,encoding="utf-8-sig",newline="") as stream:
                        fixes[cohort]=collect_fixes(
                            stream,expected_columns(cohort,headers),asof,
                            candidates,contract
                        )
    # Temporary private full-source ZIPs have now been removed. Internal GPS
    # points remain only in process memory until analysis result is returned.
    results=[]
    for variant in contract["estimands"]:
        label=variant["id"]
        units=10 if variant["coarse_cell_width_degrees"]==0.1 else 5
        all_keys=candidates[units]
        passed=0
        missing=0
        for key in all_keys:
            cohort_data=[fixes[g][units].get(key,[]) for g in COHORTS]
            if any(not rows for rows in cohort_data):
                missing+=1
                continue
            if exactly_one_triplet(
                cohort_data,
                variant["max_three_fix_time_span_seconds"],
                variant["max_three_pairwise_haversine_metres"]
            ):
                passed+=1
        if missing:
            raise ValueError("Original coarse source candidate did not reappear on event re-read")
        results.append({
          "id":label,
          "original_coarse_candidate_source_keys":len(all_keys),
          "n_keys_with_at_least_one_three_cohort_fix_triplet":passed,
          "n_candidate_keys_without_qualifying_three_cohort_fix_triplet":len(all_keys)-passed,
          "maximum_three_fix_span_seconds":variant["max_three_fix_time_span_seconds"],
          "maximum_each_pair_distance_metres":variant["max_three_pairwise_haversine_metres"],
          "same_coarse_cell_width_degrees":variant["coarse_cell_width_degrees"],
          "n_original_source_archive_MD5_and_CRC_reverified":3,
          "individual_animal_identity_verified":False,
          "GPS_records_or_source_coordinates_exported":False,
        })
    return {
      "date":contract["date"],
      "status":"POSTOPEN_COARSE_CONDITIONED_THREE_SOURCE_FIX_PROXIMITY_DIAGNOSTIC",
      "n_original_source_ZIPs_validated":3,
      "candidate_coarse_hour_cell_sources":{"0p1_degree":len(candidates[10]),"0p2_degree":len(candidates[5])},
      "all_candidate_keys_previously_observed_in_year":2020,
      "fixed_exploratory_time_distance_gates":results,
      "reanalysed_original_event_records_across_three_cohorts":sum(x["n_original_main_member_GPS_CSV_rows"] for x in receipts.values()),
      "all_original_GPS_files_removed_after_ephemeral_processing":True,
      "source_bird_tags_event_times_grid_keys_or_coordinates_exported":False,
      "no_fitness_or_migration_outcome_model_fitted":True,
      "no_actual_social_encounter_or_information_use_identified":True,
      "q_r_or_q_times_r_estimated":False,
      "not_all_original_stork_GPS_ZIPs_inspected":True,
      "no_ebird":True,
      "claim_limit":"Post-open conditional source diagnostic only. Triplets within a 1-hour/degree-cell prefilter are not all encounters, independent birds, sensory contact, predictive cue reliability or evidence for information×recourse."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    contract_bytes=a.contract.read_bytes()
    contract=json.loads(contract_bytes)
    source=json.loads(ORIGINAL.read_text())
    headers=json.loads(HEADERS.read_text())
    coarse=json.loads(COARSE.read_text())
    receipts={k:json.loads(p.read_text()) for k,p in PR421_RECEIPTS.items()}
    result=compute(contract,source,headers,coarse,receipts)
    result.update({
      "postopen_diagnostic_contract_sha256":sha256(contract_bytes).hexdigest(),
      "preexisting_coarse_result_sha256":sha256(COARSE.read_bytes()).hexdigest(),
      "original_paper_doi":"10.1098/rspb.2023.1268",
    })
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print("STORK_ORIGINAL_TRIPLE_PROXIMITY_SOURCE="+json.dumps(result,separators=(",",":")))

if __name__=="__main__":
    main()
