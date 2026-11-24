#!/usr/bin/env python3
"""Read only 3 SHA-pinned original CC0 small deployment-reference CSV files.

All original tag/animal IDs, dates and raw CSV rows stay ephemeral in memory.
Output consists of cohort-level year/missingness counts and known-bounded
deployment overlaps only. Co-deployed tags are NOT co-present birds.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, date
from hashlib import md5, sha256
import csv
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from payoff_b_stork_dspace_file_metadata_20261124 import (
    get_metadata, bundle_entries, bitstream_entries, ROOT, UUID_RE
)

DEFAULT_CONTRACT = HERE.parent / "data/payoff_b_stork_deployment_time_contract_20261124.json"

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None

def parse_source_date(raw: str):
    s = str(raw or "").strip()
    if not s or s.upper() in {"NA", "N/A", "NULL", "NAN"}:
        return None
    if not re.match(r"^(?:19|20)\d{2}-\d{2}-\d{2}(?:$|[T ])",s):
        return None
    try:
        d=datetime.fromisoformat(s.replace("Z","+00:00")).date()
        return d
    except ValueError:
        return None

def bounded_cc0_csv(original, cohort, contract, opener=None):
    """Private byte read, restricted to SHA-pinned <=80KB public reference CSV."""
    ids = {c: info["item_uuid"] for c,info in contract["original_archives"].items()}
    uid=ids[cohort]
    item=get_metadata(f"/server/api/core/items/{uid}",set(ids.values()),set())
    if item["status"]!="PUBLIC_METADATA_OK" or (item["data"] or {}).get("handle")!=original["handle"]:
        raise ValueError("Original source item identity mismatch")
    bundles=get_metadata(f"/server/api/core/items/{uid}/bundles",set(ids.values()),set())
    if bundles["status"]!="PUBLIC_METADATA_OK":
        raise ValueError("Source bundle metadata not available")
    orig=[b for b in bundle_entries(bundles["data"] or {})
          if str(b.get("name",""))=="ORIGINAL" and UUID_RE.fullmatch(str(b.get("uuid") or ""))]
    if len(orig)!=1:
        raise ValueError("Original bundle not uniquely identified")
    bid=orig[0]["uuid"]
    files=get_metadata(f"/server/api/core/bundles/{bid}/bitstreams",set(ids.values()),{bid})
    if files["status"]!="PUBLIC_METADATA_OK":
        raise ValueError("Public original file metadata unavailable")
    options=[f for f in bitstream_entries(files["data"] or {})
             if Path(str(f.get("name",""))).suffix.lower()==".csv"]
    if len(options)!=1:
        raise ValueError("Expected one CC0 cohort reference CSV")
    f=options[0]
    size=f.get("sizeBytes")
    if not isinstance(size,int) or not 1<=size<=contract["source_admission"]["max_bytes_per_csv"]:
        raise ValueError("Reference CSV outside fixed byte cap")
    file_id=str(f.get("uuid") or f.get("id") or "")
    if not UUID_RE.fullmatch(file_id):
        raise ValueError("Public file identity missing")
    allowed=ROOT+f"/server/api/core/bitstreams/{file_id}/content"
    if (f.get("_links",{}).get("content",{}) or {}).get("href")!=allowed:
        raise ValueError("Unregistered content URL")
    checksum=f.get("checkSum") or {}
    if not isinstance(checksum,dict) or str(checksum.get("checkSumAlgorithm","")).upper()!="MD5":
        raise ValueError("Public MD5 source digest missing")
    expected_md5=str(checksum.get("value") or "").lower()
    if not re.fullmatch(r"[0-9a-f]{32}",expected_md5):
        raise ValueError("Public MD5 digest malformed")
    opener=opener or build_opener(NoRedirect())
    req=Request(allowed,headers={"User-Agent":"PAYOFF-deployment-metadata-only/1.0","Accept":"text/csv,text/plain"})
    with opener.open(req,timeout=25) as response:
        target=urlparse(response.geturl())
        if target.hostname!="datarepository.movebank.org" or target.path!=urlparse(allowed).path:
            raise ValueError("Source content redirected to unsupported endpoint")
        payload=response.read(contract["source_admission"]["max_bytes_per_csv"]+1)
    if len(payload)!=size:
        raise ValueError("Source actual size disagrees with metadata")
    if md5(payload).hexdigest()!=expected_md5:
        raise ValueError("Source original MD5 changed")
    if sha256(payload).hexdigest()!=original["sha256"]:
        raise ValueError("Pre-frozen source SHA-256 changed")
    return payload

def read_tag_intervals(raw:bytes,expected_n:int):
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    fields={"tag-id","animal-id","deploy-on-date","deploy-off-date","manipulation-type"}
    if not fields.issubset(set(rows[0]) if rows else set()):
        raise ValueError("Expected five original deployment field names not available")
    if len(rows)!=expected_n:
        raise ValueError("Original reference CSV row count drift")
    result=[]
    for row in rows:
        tag=str(row["tag-id"] or "").strip()
        if not tag:
            raise ValueError("Original tag-id is empty")
        start=parse_source_date(row["deploy-on-date"])
        end=parse_source_date(row["deploy-off-date"])
        result.append({"tag":tag,"start":start,"end":end})
    return result

def overlap_days(a,b):
    """Inclusive potential co-deployment days, NOT co-travel or social contact."""
    if None in (a["start"],a["end"],b["start"],b["end"]):
        return 0
    if a["end"]<a["start"] or b["end"]<b["start"]:
        raise ValueError("Source deploy-off earlier than deploy-on")
    left=max(a["start"],b["start"])
    right=min(a["end"],b["end"])
    return max(0,(right-left).days+1)

def classifiable_intervals(rows):
    good=[]
    malformed=0
    for item in rows:
        if item["start"] is None or item["end"] is None:
            continue
        if item["end"] < item["start"]:
            malformed+=1
            continue
        good.append(item)
    return good,malformed

def cohort_summary(rows,expected):
    good,malformed=classifiable_intervals(rows)
    starts=[r["start"] for r in rows if r["start"]]
    ends=[r["end"] for r in rows if r["end"]]
    unique_tags={r["tag"] for r in rows}
    start_years=Counter(x.year for x in starts)
    end_years=Counter(x.year for x in ends)
    return {
        "original_csv_rows":len(rows),
        "source_expected_rows":expected,
        "distinct_tag_ids":len(unique_tags),
        "n_on_dates_parseable":len(starts),
        "n_off_dates_parseable":len(ends),
        "n_bounded_valid_on_off_intervals":len(good),
        "n_missing_or_unparseable_on":len(rows)-len(starts),
        "n_missing_or_unparseable_off":len(rows)-len(ends),
        "n_off_before_on":malformed,
        "min_start_year":min(start_years) if starts else None,
        "max_start_year":max(start_years) if starts else None,
        "start_year_counts":[{"year":k,"n":start_years[k]} for k in sorted(start_years)],
        "end_year_counts":[{"year":k,"n":end_years[k]} for k in sorted(end_years)],
        "complete_bounded_source_not_bird_co_travel":True
    }

def pair_overlap(rows_a,rows_b,same_cohort=False):
    """Distinct pair of tag IDs with >=1 complete known shared calendar day."""
    a,_=classifiable_intervals(rows_a)
    b,_=classifiable_intervals(rows_b)
    seen=set()
    for i,one in enumerate(a):
        for j,two in enumerate(b):
            if same_cohort and j<=i:
                continue
            if one["tag"]==two["tag"]:
                continue
            if overlap_days(one,two)>0:
                key=tuple(sorted((one["tag"],two["tag"]))) if same_cohort else (one["tag"],two["tag"])
                seen.add(key)
    return len(seen)

def compute(rows,contract):
    if set(rows)!=set(contract["original_archives"]):
        raise ValueError("Unexpected cohort metadata")
    summary={k:cohort_summary(v,contract["original_archives"][k]["rows"]) for k,v in rows.items()}
    for s in summary.values():
        if s["original_csv_rows"]!=s["source_expected_rows"] or s["n_off_before_on"]>0:
            raise ValueError("Original source rows or temporal direction not admissible")
    # Cross-cohort reused tag ID is only an identifier collision audit:
    # it cannot establish same bird or shared social opportunity.
    reused=[]
    keys=sorted(rows)
    for i,a in enumerate(keys):
        for b in keys[i+1:]:
            reused.append({"cohort_a":a,"cohort_b":b,
                           "n_reused_tag_strings":len({r["tag"] for r in rows[a]}&{r["tag"] for r in rows[b]}),
                           "n_distinct_tag_pairs_with_known_bounded_deployment_overlap":pair_overlap(rows[a],rows[b])})
    within=[{"cohort":k,"n_distinct_tag_pairs_with_known_bounded_deployment_overlap":pair_overlap(v,v,same_cohort=True)}
            for k,v in rows.items()]
    eligible=all(s["n_bounded_valid_on_off_intervals"]>=5 for s in summary.values())
    return {
       "status":"TIME_METADATA_BOUNDED_SUPPORT_ONLY" if eligible else "TIME_WINDOW_ENDS_UNOBSERVED",
       "source_cohorts":summary,
       "within_cohort_known_bounded_tag_deployment_pair_counts":within,
       "cross_cohort_known_bounded_tag_deployment_pair_counts":reused,
       "n_groups_with_ge5_bounded_intervals":sum(s["n_bounded_valid_on_off_intervals"]>=5 for s in summary.values()),
       "group_count":len(summary),
       "no_animal_contact_or_encounter_measured":True,
       "no_actual_bird_colocation_or_social_information_identified":True,
       "no_environmental_predictive_reliability_estimated":True,
       "GPS_ZIPs_downloaded":False,
       "raw_tag_ids_or_source_rows_exported":False,
       "original_fitness_or_treatment_effect_refitted":False,
       "no_ebird":True,
       "interpretation":"Tag deployment date overlap is source coverage potential only; deployment dates are not actual individual location or behavior timestamps and missing off dates are not imputed."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    raw_contract=args.contract.read_bytes()
    contract=json.loads(raw_contract)
    datasets={}
    digests={}
    for cohort,info in contract["original_archives"].items():
        payload=bounded_cc0_csv(info,cohort,contract)
        datasets[cohort]=read_tag_intervals(payload,info["rows"])
        digests[cohort]={"sha256":sha256(payload).hexdigest(),"md5_source_verified":True}
    result=compute(datasets,contract)
    result.update({
        "source_file_checksums":digests,
        "contract_sha256":sha256(raw_contract).hexdigest(),
        "source_doi":"10.1098/rspb.2023.1268",
        "analysis_date":contract["date"],
        "data_class":contract["class"]
    })
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print("STORK_DEPLOYMENT_TIME_GATE="+json.dumps(result,separators=(",",":")))

if __name__=="__main__":
    main()
