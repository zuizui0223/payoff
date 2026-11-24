#!/usr/bin/env python3
"""Source-only full-archive GPS UTC *day coverage*, NOT spatial co-presence.

Bontekoe et al 2023 CC0 public Movebank archives. Each selected original GPS
ZIP is downloaded to a temporary private Actions directory, authenticated
using the full DSpace public MD5 and exact pinned original size, read as a
stream, and deleted. Only cohort/year/day counts are exported. No GPS rows,
original coordinate, event time, tag/animal identifier, or original ZIP is
committed or uploaded. No q, recourse, exposure or fitness model is fitted.

One smallest GPS ZIP per cohort; does NOT claim total coverage of the source
study, whose additional GPS ZIPs are deliberately not fetched in this stage.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import csv
from datetime import datetime,date,timezone
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys
import tempfile
from urllib.error import HTTPError,URLError
from urllib.parse import urlparse
from urllib.request import Request,build_opener
import zipfile

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_stork_dspace_file_metadata_20261124 import (
  get_metadata, bundle_entries, bitstream_entries, UUID_RE
)
from payoff_b_stork_gps_zip_range_gate_20261124 import NoRedirect

DEFAULT_CONTRACT=HERE.parent/"data/payoff_b_stork_original_gps_date_coverage_contract_20261124.json"
DEFAULT_26COL=HERE.parent/"data/payoff_b_stork_gps_csv_header_result_20261124.json"
DOWNLOAD_CHUNK=1024*1024
STAMP_FORMAT="Movebank raw UTC timestamp (naive source time interpreted as UTC by declaration)"


def parse_event_date(value,asof):
    """Never use GPS timestamp details in output; return UTC calendar DATE."""
    text=str(value or "").strip()
    if not text or text.upper() in {"NA","N/A","NULL","NAN"}:
        return None,"MISSING_TIME"
    if not re.match(r"^(?:19|20)\d{2}-\d{2}-\d{2}[ T]",text):
        return None,"UNPARSEABLE_TIME"
    try:
        dt=datetime.fromisoformat(text.replace("Z","+00:00"))
        if dt.tzinfo is None:
            dt=dt.replace(tzinfo=timezone.utc)
        d=dt.astimezone(timezone.utc).date()
    except ValueError:
        return None,"UNPARSEABLE_TIME"
    if d>asof:
        return None,"FUTURE_TIME"
    return d,"OK"


def parse_coord(value,lo,hi):
    v=str(value or "").strip()
    if not v or v.upper() in {"NA","N/A","NULL","NAN"}:
        return False,"MISSING_COORD"
    try:
        f=float(v)
    except ValueError:
        return False,"NONNUMERIC_COORD"
    if not math.isfinite(f) or f<lo or f>hi:
        return False,"INVALID_COORD_RANGE"
    return True,"OK"


def get_original_zip_entry(cohort,contract):
    data=contract["source_origins"]
    if cohort not in data:
        raise ValueError("Source cohort not registered")
    uid=data[cohort]["original_item_uuid"]
    allowed={i["original_item_uuid"] for i in data.values()}
    item=get_metadata(f"/server/api/core/items/{uid}",allowed,set())
    if item["status"]!="PUBLIC_METADATA_OK":
        raise ValueError("Cannot authenticate source item")
    raw=item["data"] or {}
    if (raw.get("handle")!=data[cohort]["original_handle"]
        or str(raw.get("uuid") or raw.get("id") or "")!=uid):
        raise ValueError("Original source item identity changed")
    bundles=get_metadata(f"/server/api/core/items/{uid}/bundles",allowed,set())
    if bundles["status"]!="PUBLIC_METADATA_OK":
        raise ValueError("Cannot authenticate original source bundle")
    original=[b for b in bundle_entries(bundles["data"] or {})
              if b.get("name")=="ORIGINAL" and UUID_RE.fullmatch(str(b.get("uuid") or ""))]
    if len(original)!=1:
        raise ValueError("Original bundle not unique")
    buuid=original[0]["uuid"]
    files=get_metadata(f"/server/api/core/bundles/{buuid}/bitstreams",allowed,{buuid})
    if files["status"]!="PUBLIC_METADATA_OK":
        raise ValueError("Cannot authenticate original source bitstream metadata")
    expected=data[cohort]["size_bytes"]
    options=[f for f in bitstream_entries(files["data"] or {})
       if str(f.get("name") or "").lower().endswith(".zip")
       and re.search(r"gps|location",str(f.get("name") or ""),re.I)]
    if not options:
        raise ValueError("No original GPS ZIP admitted")
    selected=min(options,key=lambda f:int(f.get("sizeBytes") or 0))
    if selected.get("sizeBytes")!=expected:
        raise ValueError("Registered smallest CC0 GPS ZIP size changed")
    uid=str(selected.get("uuid") or selected.get("id") or "")
    if not UUID_RE.fullmatch(uid):
        raise ValueError("Original GPS ZIP file identity invalid")
    expected_url=f"https://datarepository.movebank.org/server/api/core/bitstreams/{uid}/content"
    if (selected.get("_links",{}).get("content",{}) or {}).get("href")!=expected_url:
        raise ValueError("Original source GPS bitstream content endpoint changed")
    checksum=selected.get("checkSum") or {}
    if not isinstance(checksum,dict) or str(checksum.get("checkSumAlgorithm","")).upper()!="MD5":
        raise ValueError("Original full ZIP MD5 metadata missing")
    expected_md5=str(checksum.get("value") or "").lower()
    if not re.fullmatch(r"[a-f0-9]{32}",expected_md5):
        raise ValueError("Original full ZIP public MD5 malformed")
    return expected_url,expected,expected_md5


def download_original_zip(url,size,checksum_md5,target,opener=None):
    """Exact HTTP 200 full public CC0 selected ZIP, independent full-byte MD5."""
    opener=opener or build_opener(NoRedirect())
    req=Request(url,headers={
        "Accept":"application/zip,application/octet-stream,*/*",
        "User-Agent":"PAYOFF-B-original-CC0-source-md5-temporal-gate/1.0"
    })
    digest=hashlib.md5()
    read_total=0
    with opener.open(req,timeout=70) as resp:
        if int(resp.status)!=200:
            raise ValueError("Original selected ZIP did not return complete HTTP 200")
        resolved=urlparse(resp.geturl())
        if resolved.hostname!="datarepository.movebank.org" or resolved.path!=urlparse(url).path:
            raise ValueError("Original ZIP downloaded from unregistered redirect")
        announced=resp.headers.get("Content-Length")
        if announced is not None and announced.isdigit() and int(announced)!=size:
            raise ValueError("Declared original ZIP Content-Length drift")
        if "html" in str(resp.headers.get("Content-Type","")).lower():
            raise ValueError("Refusing HTML instead of original ZIP")
        with target.open("wb") as out:
            while True:
                chunk=resp.read(DOWNLOAD_CHUNK)
                if not chunk:
                    break
                read_total+=len(chunk)
                if read_total>size:
                    raise ValueError("Original file exceeds pinned source archive size")
                digest.update(chunk)
                out.write(chunk)
    if read_total!=size:
        raise ValueError("Original ZIP incomplete")
    if digest.hexdigest()!=checksum_md5:
        raise ValueError("Original ZIP MD5 differs from public DSpace metadata")
    return {"full_original_zip_md5_source_verified":True,
            "original_archive_byte_count":read_total,
            "md5_is_source_original":True}


def choose_main_member(zip_file,cohort,contract):
    expected=int(contract["source_origins"][cohort]["main_member_uncompressed_bytes"])
    infos=zip_file.infolist()
    selected=[m for m in infos if m.filename.lower().endswith(".csv")
              and m.file_size==expected and not m.is_dir()]
    if len(selected)!=1:
        raise ValueError("Expected exactly one pinned original main GPS CSV")
    if selected[0].flag_bits & 1:
        raise ValueError("Original ZIP main member encrypted")
    return selected[0]


def expected_columns(cohort,header_receipt):
    matching=[e for e in header_receipt["cohort_schemas"] if e.get("cohort")==cohort]
    if len(matching)!=1:
        raise ValueError("Expected unique previous source header cohort")
    rec=matching[0]["member_schemas_no_filename"]
    good=[x for x in rec if x.get("status")=="FIRST_LINE_PUBLIC_CSV_SCHEMA_RECOVERED"
          and x.get("n_csv_columns")==26]
    if len(good)!=1:
        raise ValueError("Original 26-column main header is not uniquely frozen")
    return good[0]["source_column_names"]


def classify_visible(raw):
    t=str(raw or "").strip().lower()
    if t in {"true","t","1","yes"}:return "visible_true"
    if t in {"false","f","0","no"}:return "visible_false"
    if t in {"","na","nan","n/a"}:return "visible_missing"
    return "visible_other"


def stream_csv_support(source_file,expected_header,asof,cohort):
    """Complete event scan; raw tags/animal IDs never leave source runtime."""
    counters=Counter()
    day_tags=defaultdict(set)
    day_events=Counter()
    year_tags=defaultdict(set)
    year_animals=defaultdict(set)
    year_events=Counter()
    year_visible=defaultdict(Counter)

    reader=csv.DictReader(source_file)
    observed=reader.fieldnames or []
    if observed!=expected_header:
        raise ValueError("Original GPS CSV header differs from previous exact source schema")
    required={"timestamp","location-lat","location-long",
              "tag-local-identifier","individual-local-identifier","visible"}
    if not required.issubset(set(observed)):
        raise ValueError("Original GPS source necessary fields absent")
    for row in reader:
        counters["n_original_CSV_event_rows"]+=1
        d,why=parse_event_date(row.get("timestamp"),asof)
        if d is None:
            counters["invalid_"+why.lower()]+=1
            continue
        tag=str(row.get("tag-local-identifier") or "").strip()
        if not tag:
            counters["missing_tag"]+=1
            continue
        latitude,ly=parse_coord(row.get("location-lat"),-90,90)
        longitude,lx=parse_coord(row.get("location-long"),-180,180)
        if not latitude or not longitude:
            counters["invalid_geocoord"]+=1
            counters["invalid_geocoord_"+ly.lower()]+=int(not latitude)
            counters["invalid_geocoord_"+lx.lower()]+=int(not longitude)
            continue
        # No raw coordinates are retained, reused, printed or uploaded.
        animal=str(row.get("individual-local-identifier") or "").strip()
        if not animal:
            counters["n_georeferenced_missing_individual_id"]+=1
        yr=d.year
        date_str=d.isoformat()
        v=classify_visible(row.get("visible"))
        year_visible[yr][v]+=1
        year_events[yr]+=1
        counters["n_valid_georeferenced_event_rows"]+=1
        year_tags[yr].add(tag)
        if animal:
            year_animals[yr].add(animal)
        day_tags[date_str].add(tag)
        day_events[date_str]+=1
    if not counters["n_valid_georeferenced_event_rows"]:
        raise ValueError("No original valid georeferenced source event")
    years=[]
    for yr in sorted(year_events):
        days=[d for d in day_events if int(d[:4])==yr]
        years.append({
          "year":yr,
          "n_valid_georeferenced_events":year_events[yr],
          "n_distinct_observed_tag_strings":len(year_tags[yr]),
          "n_distinct_observed_animal_strings":len(year_animals[yr]),
          "n_UTC_dates_with_georeferenced_events":len(days),
          "n_UTC_dates_with_at_least_two_tag_strings":sum(len(day_tags[d])>=2 for d in days),
          "observed_visible_source_counts":dict(year_visible[yr])
        })
    daily=[{"UTC_date":day,
            "n_valid_georeferenced_event_rows":day_events[day],
            "n_distinct_observed_tag_strings":len(day_tags[day])}
           for day in sorted(day_events)]
    return {
      "cohort":cohort,
      "n_original_main_member_GPS_CSV_rows":counters["n_original_CSV_event_rows"],
      "n_valid_georeferenced_event_rows":counters["n_valid_georeferenced_event_rows"],
      "n_unusable_timestamp_rows":sum(v for k,v in counters.items() if k.startswith("invalid_") and "time" in k),
      "n_unusable_tag_rows":counters["missing_tag"],
      "n_unusable_coordinate_rows":counters["invalid_geocoord"],
      "n_valid_coordinate_rows_without_animal_id":counters["n_georeferenced_missing_individual_id"],
      "n_distinct_UTC_dates_with_valid_events":len(daily),
      "n_UTC_dates_with_at_least_two_distinct_tag_strings":sum(x["n_distinct_observed_tag_strings"]>=2 for x in daily),
      "yearly_aggregate":years,
      "daily_aggregate_only":daily,
      "raw_identifiers_geolocation_or_event_timestamps_exported":False,
      "no_actual_same_place_same_time_evidence_claimed":True,
      "not_full_study_coverage":True,
    }


def process_cohort(cohort,contract,header_receipt):
    url,size,expected_md5=get_original_zip_entry(cohort,contract)
    with tempfile.TemporaryDirectory(prefix="payoff_b_stork_original_private_") as tmp:
        location=Path(tmp)/"original_cc0_gps.zip"
        source_checksum=download_original_zip(url,size,expected_md5,location)
        with zipfile.ZipFile(location,"r") as archive:
            zinfo=choose_main_member(archive,cohort,contract)
            with archive.open(zinfo,"r") as binstream:
                with io.TextIOWrapper(binstream,encoding="utf-8-sig",newline="") as stream:
                    # Reading to EOF also checks ZIP member CRC in Python's
                    # ZipExtFile. A truncated/corrupt source fails closed.
                    measured=stream_csv_support(
                      stream,expected_columns(cohort,header_receipt),
                      date.fromisoformat(contract["reference_day"]),cohort
                    )
        measured.update(source_checksum)
        measured.update({
          "status":"ORIGINAL_CC0_GPS_SINGLE_ARCHIVE_UTC_DATE_SUPPORT_VERIFIED",
          "original_main_zip_member_CRC_read_through_EOF":True,
          "original_selected_zip_size_bytes":size,
          "source_paper_doi":"10.1098/rspb.2023.1268",
          "source_archive_doi":contract["source_origins"][cohort]["doi"],
          "original_member_uncompressed_bytes":contract["source_origins"][cohort]["main_member_uncompressed_bytes"],
          "source_GPS_raw_file_committed":False,
          "source_event_values_exported":False,
          "same_time_geo_colocation_assessed":False,
          "no_ebird":True,
        })
        return measured


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cohort",choices=["control","delayed","naturally_timed"],required=True)
    p.add_argument("--contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--header-receipt",type=Path,default=DEFAULT_26COL)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    c=json.loads(a.contract.read_text())
    h=json.loads(a.header_receipt.read_text())
    if c["source_fidelity"]["no_ebird"] is not True:
        raise ValueError("Source policy forbids eBird")
    result=process_cohort(a.cohort,c,h)
    result.update({
        "date":c["date"],
        "source_contract_sha256":hashlib.sha256(a.contract.read_bytes()).hexdigest(),
        "header_source_receipt_sha256":hashlib.sha256(a.header_receipt.read_bytes()).hexdigest(),
        "source_gps_time_interpretation":STAMP_FORMAT,
        "no_biological_payoff_or_learning_effect_calculated":True,
    })
    a.output.parent.mkdir(exist_ok=True,parents=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("STORK_GPS_UTC_DATE_RESULT="+json.dumps(result,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
