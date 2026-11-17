"""PAYOFF-B V7 frozen Kölzsch Movebank GPS quality gate.

This script reports only SOURCE QUALITY of original published GPS records:
UTC timestamp parsing, valid coordinates, sensor type, duplicate person-time
keys and support across calendar years/months. It does not reconstruct stops,
arrival phase, historical q, urgency U or V7 q×U. No individual locations,
IDs, times or raw tracks are printed or archived; respect CC BY-NC flyways.
"""
import argparse,csv,hashlib,io,json,math
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
from scripts.payoff_b_scotland_resource_source_probe import open_url
from scripts.payoff_b_movebank_v7_published_source_gate import DOIS,discover,source_json
from scripts.payoff_b_movebank_v7_bitstream_gate import checksum_compare

FROZEN_GPS_SHA256={
 "Greenland":"6e01f16ddbc3638ae14dcce6c0883f26c61ce6abd81dc1629c37bea4db75b18d",
 "Svalbard":"e879874956afbb73a5e291d4ff87c17dafcc825dc2f04805a65690b21bdcd2e0",
 "Barents Sea":"9ce5865e8edf4b0546adf4e52f26d665510514219ea75e924fbb93cbeb6fb786",
}
MAX_GPS_BYTES=9_000_000
MIN_SPRING_FIXES=10
SPRING_MONTHS={3,4,5,6,7}


def date_utc(raw):
    if not raw:return None
    try:
        value=datetime.fromisoformat(str(raw).strip().replace("Z","+00:00"))
    except ValueError:
        return None
    if value.tzinfo is None:
        return None
    return value.astimezone(__import__("datetime").timezone.utc)


def parse_coord(raw,bound):
    try:v=float(raw)
    except (TypeError,ValueError):return None
    if not math.isfinite(v) or abs(v)>bound:return None
    return v


def audit_gps_rows(rows, expected_flyway):
    keys=set()
    bad=Counter()
    month=Counter()
    sensor=Counter()
    years=Counter()
    valid_by_indyear=Counter()
    by_individual=Counter()
    known_ids=set()
    row_count=0
    for r in rows:
        row_count+=1
        ident=str(r.get("individual-local-identifier") or "").strip()
        ts=date_utc(r.get("timestamp"))
        longitude=parse_coord(r.get("location-long"),180)
        latitude=parse_coord(r.get("location-lat"),90)
        if not ident:
            bad["missing_individual_id"]+=1
        else:
            known_ids.add(ident)
            by_individual[ident]+=1
        if ts is None:
            bad["invalid_or_missing_utc_timestamp"]+=1
        if longitude is None or latitude is None:
            bad["invalid_or_missing_lat_long"]+=1
        if ts is None or not ident or longitude is None or latitude is None:
            continue
        key=(ident,ts.isoformat())
        if key in keys:
            bad["duplicate_same_individual_utc_timestamp"]+=1
            continue
        keys.add(key)
        if latitude == 0.0 and longitude == 0.0:
            bad["null_island_zero_zero_position"]+=1
            continue
        years[ts.year]+=1
        month[ts.month]+=1
        sensor[(r.get("sensor-type") or "").strip()]+=1
        valid_by_indyear[(ident,ts.year)]+=1
    spring_iy=[k for k in valid_by_indyear
          if valid_by_indyear[k]>=MIN_SPRING_FIXES]
    byyr=defaultdict(int)
    for (ident,year),n in valid_by_indyear.items():
        byyr[year]+=1
    return {
        "flyway":expected_flyway,
        "source_all_rows":row_count,
        "individual_ids_unique_n":len(known_ids),
        "source_valid_unique_gps_fix_n":len(keys)-bad["null_island_zero_zero_position"],
        "bad_source_counts":dict(bad),
        "year_fix_counts":dict(sorted(years.items())),
        "month_fix_counts":dict(sorted(month.items())),
        "sensor_type_counts":dict(sensor),
        "individual_year_series_total":len(valid_by_indyear),
        "individual_year_series_with_at_least_10_valid_fixes":len(spring_iy),
        "individual_year_series_by_year":dict(sorted(byyr.items())),
        "individual_trace_fix_count_min":min(by_individual.values()) if by_individual else None,
        "individual_trace_fix_count_max":max(by_individual.values()) if by_individual else None,
        "cannot_infer_complete_migration_or_stopover_from_raw_fix_counts":True,
        "independent_30year_predictability_q_from_supplement":False,
        "individual_data_not_returned":True,
    }


def source():
    outcomes={}
    for fly,doi in DOIS.items():
        src=discover(doi)
        info={"source_doi":doi,"source_archive_gate":src.get("gate"),
              "source_license":src.get("doi_exact_matching_items",[{}])[0].get("license")}
        if src.get("gate")!="ARCHIVE_ITEM_DOI_MATCH":
            info["gate"]="NO_GO_PUBLISHED_ARCHIVE"
            outcomes[fly]=info;continue
        original=next((b for b in src.get("bundle_overview",[]) if b.get("name")=="ORIGINAL"),None)
        if original is None:
            info["gate"]="NO_GO_ORIGINAL_ARCHIVE"
            outcomes[fly]=info;continue
        brec,bsource=source_json(original.get("bitstreams"))
        if bsource is None:
            info["gate"]="NO_GO_ORIGINAL_BITSTREAM_LIST"
            outcomes[fly]=info;continue
        candidates=[b for b in bsource.get("_embedded",{}).get("bitstreams",[])
           if str(b.get("name") or "").lower().endswith(".csv")
              and "-reference-data" not in str(b.get("name") or "").lower()]
        if len(candidates)!=1:
            info["gate"]="NO_GO_UNIQUE_GPS_FILE"
            info["candidate_file_count"]=len(candidates)
            outcomes[fly]=info;continue
        file=candidates[0]
        url=file.get("_links",{}).get("content",{}).get("href")
        size=file.get("sizeBytes")
        if not isinstance(size,int) or size<=0 or size>MAX_GPS_BYTES:
            info["gate"]="NO_GO_UNEXPECTED_SOURCE_SIZE"
            outcomes[fly]=info;continue
        res=open_url(url,timeout=90,max_read=size)
        raw=res.get("body")
        if res.get("http_status")!=200 or not raw or len(raw)!=size:
            info["gate"]="NO_GO_SOURCE_BYTES_UNAVAILABLE"
            info["http_status"]=res.get("http_status")
            outcomes[fly]=info;continue
        digest=hashlib.sha256(raw).hexdigest()
        if digest!=FROZEN_GPS_SHA256[fly] or not checksum_compare(
            raw,file.get("checkSum")
        )["source_verified"]:
            info["gate"]="NO_GO_ORIGINAL_SHA256_OR_MD5_DRIFT"
            outcomes[fly]=info;continue
        try:
            source_text=raw.decode("utf-8-sig",errors="strict")
            source_charset="utf-8"
        except UnicodeDecodeError:
            # Older Movebank source text can contain CP1252 characters in
            # metadata/person names; preserve numerical GPS columns exactly.
            source_text=raw.decode("cp1252",errors="strict")
            source_charset="cp1252"
        rows=csv.DictReader(io.StringIO(source_text,newline=""))
        headers=rows.fieldnames or []
        for col in ("individual-local-identifier","timestamp",
                    "location-lat","location-long"):
            if col not in headers:
                raise ValueError("Missing source GPS field: "+col)
        info["source_sha256"]=digest
        info["source_original_bytes"]=size
        info["source_encoding"]=source_charset
        info["qa"]=audit_gps_rows(rows,fly)
        info["gate"]="SOURCE_GPS_FIXES_QUALITY_AUDITED"
        outcomes[fly]=info
    eligible=all(x.get("gate")=="SOURCE_GPS_FIXES_QUALITY_AUDITED"
                 for x in outcomes.values())
    return {
       "status":"PAYOFF_B_V7_ORIGINAL_GOOSE_GPS_FIX_QUALITY_AUDIT",
       "flyways":outcomes,
       "all_three_gps_checked":eligible,
       "total_original_fixes":sum(x.get("qa",{}).get("source_all_rows",0) for x in outcomes.values()),
       "source_distinct_individuals_sum_by_flyway":sum(x.get("qa",{}).get("individual_ids_unique_n",0) for x in outcomes.values()),
       "does_not_claim_independent_migrations_equal_individuals":True,
       "actual_historical_q_frozen_from_source_not_identified":True,
       "v7_q_U_outcome_not_run":True,
       "no_eBird":True,
       "no_raw_tracks_shared":True,
       "gate":"GPS_FIXES_SOURCE_AUDITED_ONLY" if eligible else "NO_GO_ORIGINAL_GPS_QUALITY"
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=source()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
