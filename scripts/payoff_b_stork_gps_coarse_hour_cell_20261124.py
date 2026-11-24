#!/usr/bin/env python3
"""Three-cohort CC0 GPS source support by UTC hour and coarse geographic cell.

This is NOT a bird contact, flocking, information, cognition, q/r, or payoff
analysis. No original GPS coordinates, cell IDs, individual/tag strings,
event rows, or raw ZIP files are written to repo/logs/artifacts.

Source: exact same 3 selected Bontekoe et al 2023 CC0 Movebank original GPS
ZIPs authenticated in PR421. All original member rows are scanned again and
source counts must exactly reproduce that complete MD5/CRC GPS date receipt.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime,date,timezone
from itertools import combinations
import io
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import zipfile
from hashlib import sha256

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_stork_original_gps_date_coverage_20261124 import (
    get_original_zip_entry,download_original_zip,choose_main_member,
    expected_columns,parse_coord
)

CONTRACT=HERE.parent/"data/payoff_b_stork_original_gps_hour_cell_contract_20261124.json"
SOURCE=HERE.parent/"data/payoff_b_stork_original_gps_date_coverage_contract_20261124.json"
HEADERS=HERE.parent/"data/payoff_b_stork_gps_csv_header_result_20261124.json"
ORIGINAL_RECEIPTS={
  "control":HERE.parent/"data/payoff_b_stork_original_gps_date_control_result_20261124.json",
  "delayed":HERE.parent/"data/payoff_b_stork_original_gps_date_delayed_result_20261124.json",
  "naturally_timed":HERE.parent/"data/payoff_b_stork_original_gps_date_naturally_timed_result_20261124.json"
}

def parse_UTC_dt(raw,asof):
    text=str(raw or "").strip()
    if not re.match(r"^(?:19|20)\d{2}-\d{2}-\d{2}[ T]",text):
        return None
    try:
        dt=datetime.fromisoformat(text.replace("Z","+00:00"))
        if dt.tzinfo is None:
            dt=dt.replace(tzinfo=timezone.utc)
        dt=dt.astimezone(timezone.utc)
    except ValueError:
        return None
    return dt if dt.date()<=asof else None


def cell_hour_key(hour,lat,lon,units_per_degree):
    """Only internal integer occupancy; never output this key or its hash."""
    if not 0<=lat+90<=180 or not 0<=lon+180<=360:
        raise ValueError("Source latitude/longitude not in validated range")
    latbin=int(math.floor((lat+90)*units_per_degree))
    lonbin=int(math.floor((lon+180)*units_per_degree))
    if latbin>=4096 or lonbin>=4096:
        raise ValueError("Too many grid bins for 12-bit internal source packing")
    return (hour<<24)|(latbin<<12)|lonbin


def year_from_hour(hour):
    return date.fromordinal(hour//24).year


def source_scan_main_csv(stream,expected_columns_26,asof):
    import csv
    reader=csv.DictReader(stream)
    if (reader.fieldnames or [])!=expected_columns_26:
        raise ValueError("Source schema no longer matches original 26-column GPS header")
    n_rows=0
    n_valid=0
    n_bad_timestamp=0
    n_bad_position=0
    n_missing_tag=0
    day_keys=set()
    hour_keys=set()
    first_tag_by_key={10:{},5:{}}
    multiple_tag_keys={10:set(),5:set()}
    for row in reader:
        n_rows+=1
        dt=parse_UTC_dt(row.get("timestamp"),asof)
        if dt is None:
            n_bad_timestamp+=1
            continue
        tag=str(row.get("tag-local-identifier") or "").strip()
        if not tag:
            n_missing_tag+=1
            continue
        a,why_a=parse_coord(row.get("location-lat"),-90,90)
        b,why_b=parse_coord(row.get("location-long"),-180,180)
        if not a or not b:
            n_bad_position+=1
            continue
        lat=float(row["location-lat"])
        lon=float(row["location-long"])
        n_valid+=1
        d=dt.date().toordinal()
        hour=d*24+dt.hour
        day_keys.add(d)
        hour_keys.add(hour)
        for resolution in (10,5): # 0.1 and 0.2 degree fixed at source contract
            key=cell_hour_key(hour,lat,lon,resolution)
            first=first_tag_by_key[resolution]
            if key not in first:
                first[key]=tag
            elif first[key]!=tag:
                multiple_tag_keys[resolution].add(key)
    coarse_keys={i:set(v.keys()) for i,v in first_tag_by_key.items()}
    first_tag_by_key.clear() # original tag strings intentionally discarded
    return {
      "n_raw_rows":n_rows,
      "n_valid_georeferenced_rows":n_valid,
      "n_unusable_time":n_bad_timestamp,
      "n_unusable_coordinate":n_bad_position,
      "n_missing_tag":n_missing_tag,
      "day_ordinals":day_keys,
      "hour_ordinals":hour_keys,
      "cell_hour_keys":coarse_keys,
      "cell_hour_two_distinct_tag_keys":multiple_tag_keys,
    }


def verify_against_first_pass(scan,receipt):
    checks=[
        (scan["n_raw_rows"],receipt["n_original_main_member_GPS_CSV_rows"]),
        (scan["n_valid_georeferenced_rows"],receipt["n_valid_georeferenced_event_rows"]),
        (scan["n_unusable_time"],receipt["n_unusable_timestamp_rows"]),
        (scan["n_unusable_coordinate"],receipt["n_unusable_coordinate_rows"]),
        (scan["n_missing_tag"],receipt["n_unusable_tag_rows"]),
        (len(scan["day_ordinals"]),receipt["n_distinct_UTC_dates_with_valid_events"]),
    ]
    if any(a!=b for a,b in checks):
        raise ValueError("Original GPS support rows differ from previously authenticated PR421 census")
    if receipt["full_original_zip_md5_source_verified"] is not True or receipt["not_full_study_coverage"] is not True:
        raise ValueError("Original full ZIP provenance was not admitted")


def count_years(keys,kind):
    if kind=="days":
        get_year=lambda x:date.fromordinal(x).year
    elif kind=="hours":
        get_year=year_from_hour
    else:
        get_year=lambda x:year_from_hour(x>>24)
    counts=Counter(get_year(x) for x in keys)
    return [{"year":year,"n_bins":counts[year]} for year in sorted(counts)]


def one_cohort(scan,cohort):
    return {
      "cohort":cohort,
      "n_original_GPS_rows_checked":scan["n_raw_rows"],
      "n_original_valid_GPS_rows_checked":scan["n_valid_georeferenced_rows"],
      "n_UTC_days_with_valid_GPS":len(scan["day_ordinals"]),
      "n_UTC_hours_with_valid_GPS":len(scan["hour_ordinals"]),
      "n_UTC_hour_0p1_degree_cells":len(scan["cell_hour_keys"][10]),
      "n_UTC_hour_0p2_degree_cells":len(scan["cell_hour_keys"][5]),
      "n_UTC_hour_0p1_cells_with_at_least_two_tag_strings":len(scan["cell_hour_two_distinct_tag_keys"][10]),
      "n_UTC_hour_0p2_cells_with_at_least_two_tag_strings":len(scan["cell_hour_two_distinct_tag_keys"][5]),
      "yearly_0p1_degree_cell_count":count_years(scan["cell_hour_keys"][10],"cells"),
      "yearly_0p2_degree_cell_count":count_years(scan["cell_hour_keys"][5],"cells"),
      "no_original_tag_or_coordinate_exported":True
    }


def cross_cohort_support(scans):
    if set(scans)!={"control","delayed","naturally_timed"}:
        raise ValueError("Exactly three pinned original cohorts required")
    pairs=[]
    for a,b in combinations(["control","delayed","naturally_timed"],2):
        x,y=scans[a],scans[b]
        common_hours=x["hour_ordinals"]&y["hour_ordinals"]
        pair={"cohort_a":a,"cohort_b":b,
              "n_common_UTC_hours":len(common_hours),
              "common_hour_counts_by_year":count_years(common_hours,"hours")}
        for grid,label in [(10,"0p1"),(5,"0p2")]:
            same=x["cell_hour_keys"][grid]&y["cell_hour_keys"][grid]
            pair[f"n_same_UTC_hour_and_{label}_degree_cell_keys"]=len(same)
            pair[f"yearly_{label}_cell_hour_common_keys"]=count_years(same,"cells")
        pairs.append(pair)
    triple_hours=set.intersection(*(scans[k]["hour_ordinals"] for k in scans))
    triple={
      "n_common_UTC_hours":len(triple_hours),
      "common_hour_counts_by_year":count_years(triple_hours,"hours")
    }
    for grid,label in [(10,"0p1"),(5,"0p2")]:
        same=set.intersection(*(scans[k]["cell_hour_keys"][grid] for k in scans))
        triple[f"n_same_UTC_hour_and_{label}_degree_cell_keys"]=len(same)
        triple[f"yearly_{label}_cell_hour_common_keys"]=count_years(same,"cells")
    return {"pairwise_aggregate":pairs,"three_cohort_aggregate":triple}


def process_all(c,original,headers,receipts):
    asof=date.fromisoformat(original["reference_day"])
    scans={}
    md5_count=0
    for cohort in ["control","delayed","naturally_timed"]:
        src=receipts[cohort]
        url,expected_size,expected_md5=get_original_zip_entry(cohort,original)
        with tempfile.TemporaryDirectory(prefix="payoff_stork_gps_source_private_") as temporary:
            path=Path(temporary)/"source_original_cc0.zip"
            verified=download_original_zip(url,expected_size,expected_md5,path)
            if verified["full_original_zip_md5_source_verified"] is not True:
                raise ValueError("Original public ZIP MD5 not verified")
            with zipfile.ZipFile(path,"r") as archive:
                info=choose_main_member(archive,cohort,original)
                with archive.open(info,"r") as body:
                    with io.TextIOWrapper(body,encoding="utf-8-sig",newline="") as textstream:
                        scan=source_scan_main_csv(textstream,expected_columns(cohort,headers),asof)
            # The original main ZIP member reached EOF; its CRC was checked
            # by ZipExtFile; no GPS values or ZIP files persist past this scope.
            verify_against_first_pass(scan,src)
            scans[cohort]=scan
            md5_count+=1
    original_aggregate={cohort:one_cohort(scans[cohort],cohort) for cohort in scans}
    pair=cross_cohort_support(scans)
    return {
       "date":c["date"],
       "status":"SOURCE_ORIGINAL_GPS_COARSE_HOUR_CELL_SUPPORT_COMPUTED_NOT_SOCIAL_CUE",
       "n_original_source_ZIPs_reverified_MD5_and_CRC":md5_count,
       "three_cohort_source":original_aggregate,
       **pair,
       "spatial_primary":"Same 0.1 degree lat/lon bin anchored at -90,-180, NOT fixed-distance or direct visibility",
       "spatial_sensitivity":"Same 0.2 degree lat/lon bin, no source retuning",
       "hour_definition":"Same UTC clock hour, not exactly simultaneous GPS event",
       "file_selection":"One previously frozen smallest public GPS ZIP per 2023 cohort",
       "not_complete_original_study_GPS_population":True,
       "original_GPS_ZIPs_or_event_rows_exported":False,
       "tag_or_animal_identifiers_or_cell_keys_exported":False,
       "focal_same_bird_cross_cohort_join_performed":False,
       "actual_bird_social_interaction_or_cue_receipt_identified":False,
       "predictive_reliability_q_or_remaining_recourse_r_estimated":False,
       "biological_fitness_or_behavior_model_fitted":False,
       "no_ebird":True,
       "claim_limit":"UTC-hour×degree-grid occupancy of tagged source instruments only. Even matching hour and grid bin is not direct flock contact, individual information, cue reliability, or payoff."
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--source-contract",type=Path,default=SOURCE)
    p.add_argument("--header-receipt",type=Path,default=HEADERS)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    c=json.loads(a.contract.read_text())
    original=json.loads(a.source_contract.read_text())
    headers=json.loads(a.header_receipt.read_text())
    receipts={key:json.loads(path.read_text()) for key,path in ORIGINAL_RECEIPTS.items()}
    result=process_all(c,original,headers,receipts)
    result.update({
       "source_contract_sha256":sha256(a.source_contract.read_bytes()).hexdigest(),
       "new_frozen_contract_sha256":sha256(a.contract.read_bytes()).hexdigest(),
       "original_paper_doi":"10.1098/rspb.2023.1268"
    })
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print("STORK_GPS_COARSE_HOUR_CELL_RESULT="+json.dumps(result,separators=(",",":")))

if __name__=="__main__":
    main()
