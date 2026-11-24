#!/usr/bin/env python3
"""Verify only six tiny original Kölzsch barnacle tracking reference files.

Three public archived original dataset records carry distinct CC0/CC-BY-NC
licenses. Inspect ONLY a fixed <20KB .csv reference table and <20KB .txt
README in each original DSpace bundle. Never read or publish the 1.97-7.27MB
original tracking/event CSVs, bird fixes, tag identifiers, or any V7 q×U fit.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,sys
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.parse import urlparse
from urllib.request import Request,build_opener

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_v7_barnacle_archived_source_audit_20261124 import (
    ROOT,DATACITE,SEARCH,SEARCH_ALIAS,UUID_RE,NoRedirect,
    get_public_json,citation_record,dspace_discovery,find_item_for_doi,bundle_items
)

DEFAULT_CONTRACT=HERE.parent/"data/payoff_b_v7_barnacle_small_source_contract_20261124.json"
META_CONTRACT=HERE.parent/"data/payoff_b_v7_barnacle_archive_metadata_contract_20261124.json"
MAX_BYTES=20000

def source_file_gate(f,expected_size,expected_ext):
    name=str(f.get("name") or "")
    if not name.lower().endswith(expected_ext) or Path(name).suffix.lower()!=expected_ext:
        raise ValueError("Not exact predeclared small source extension")
    if re.search(r"gps|location|event|track|accel",name,re.I) and expected_ext==".csv":
        raise ValueError("Tracking/event source not admitted as tiny reference")
    size=f.get("sizeBytes")
    if not isinstance(size,int) or size!=expected_size or size>MAX_BYTES:
        raise ValueError("Original small reference file size changed")
    original=f.get("checkSum") or {}
    if not isinstance(original,dict) or str(original.get("checkSumAlgorithm","")).upper()!="MD5":
        raise ValueError("Original public DSpace reference MD5 missing")
    expected_md5=str(original.get("value") or "").lower()
    if not re.fullmatch(r"[0-9a-f]{32}",expected_md5):
        raise ValueError("Original MD5 malformed")
    uid=str(f.get("uuid") or f.get("id") or "")
    if not UUID_RE.fullmatch(uid):
        raise ValueError("Original bitstream UUID missing")
    url=ROOT+f"/core/bitstreams/{uid}/content"
    if (f.get("_links",{}).get("content") or {}).get("href")!=url:
        raise ValueError("Original DSpace reference content URI not exact")
    return url,size,expected_md5

def read_small_public_reference(f,expected_size,extension,opener=None):
    url,size,original_md5=source_file_gate(f,expected_size,extension)
    opener=opener or build_opener(NoRedirect())
    req=Request(url,headers={"Accept":"text/plain,text/csv,application/octet-stream,*/*",
                             "User-Agent":"PAYOFF-B-V7-small-original-source-only/1.0"})
    try:
        with opener.open(req,timeout=25) as rsp:
            if int(rsp.status)!=200 or urlparse(rsp.geturl()).hostname!="datarepository.movebank.org" or urlparse(rsp.geturl()).path!=urlparse(url).path:
                raise ValueError("Unexpected original source redirect or status")
            raw=rsp.read(MAX_BYTES+1)
        if len(raw)!=size or hashlib.md5(raw).hexdigest()!=original_md5:
            raise ValueError("Source original MD5/size mismatch")
    except (HTTPError,URLError,TimeoutError,OSError,ValueError) as e:
        return {"status":"SMALL_SOURCE_BYTES_NOT_VERIFIED","extension":extension,
                "error_class":type(e).__name__,
                "http_status":int(e.code) if isinstance(e,HTTPError) else None,
                "raw_source_rows_or_identifiers_exported":False}
    if extension==".csv":
        rr=csv.reader(io.StringIO(raw.decode("utf-8-sig","replace")))
        try: header=next(rr)
        except StopIteration:header=[]
        fields=[str(x)[:120] for x in header[:80]]
        normalized=[re.sub(r"[^a-z0-9]","",x.lower()) for x in fields]
        tag_field=next((i for i,n in enumerate(normalized) if n in ("tagid","taglocalidentifier")),None)
        animal_field=next((i for i,n in enumerate(normalized) if n in ("animalid","individuallocalidentifier")),None)
        unique_tags=set()
        unique_animals=set()
        n=0
        for row in rr:
            if not row or not any(x.strip() for x in row):continue
            n+=1
            if tag_field is not None and tag_field<len(row) and row[tag_field]:
                unique_tags.add(row[tag_field])
            if animal_field is not None and animal_field<len(row) and row[animal_field]:
                unique_animals.add(row[animal_field])
        detail={
          "column_names":fields,
          "n_data_rows":n,
          "n_distinct_tag_strings":len(unique_tags) if tag_field is not None else None,
          "n_distinct_animal_strings":len(unique_animals) if animal_field is not None else None,
          "original_1982_2011_environment_anomaly_pair_fields_present":all(
              k in normalized for k in (
                  "year","sourceonsetanomalydays","targetonsetanomalydays")
          ),
        }
    else:
        txt=raw.decode("utf-8-sig","replace").lower()
        detail={
          "keywords_present":{
            "GPS":bool(re.search(r"\bgps\b",txt)),
            "timestamp":bool(re.search(r"timestamp|time.?stamp",txt)),
            "UTC":bool(re.search(r"\butc\b",txt)),
            "GDD":bool(re.search(r"\bgdd\b",txt)),
            "historical_spring":bool(re.search(r"spring onset|onset of spring|spring phenology",txt)),
            "license":bool(re.search(r"licen[cs]e",txt))
          },
          "characters_read":len(txt)
        }
    return {
      "status":"ORIGINAL_TINY_SOURCE_MD5_VERIFIED",
      "extension":extension,
      "size_bytes":len(raw),
      "source_sha256":hashlib.sha256(raw).hexdigest(),
      "matches_original_DSpace_MD5":True,
      "summary_only":detail,
      "raw_source_rows_or_identifiers_exported":False
    }

def audit(c,meta):
    source_searches=[get_public_json(url,meta) for url in (SEARCH,SEARCH_ALIAS)]
    discovered=list({x["uuid"]:x for v in source_searches if v["data"]
                     for x in dspace_discovery(v["data"])}.values())
    receipt=[]
    for entry in meta["archive_DOIs"]:
        cohort=entry["flyway"]
        registration=c["source_flyways"][cohort]
        doi=entry["doi"]
        citation_res=get_public_json(DATACITE+doi,meta)
        if citation_res["status"]!="PUBLIC_METADATA_JSON_VERIFIED":
            receipt.append({"flyway":cohort,"status":"ORIGINAL_SOURCE_DOI_UNAVAILABLE"});continue
        citation=citation_record(citation_res["data"],doi,entry["expected_label"])
        matched=find_item_for_doi(citation,discovered)
        if not matched:
            receipt.append({"flyway":cohort,"status":"ORIGINAL_ITEM_NOT_FOUND"});continue
        # Svalbard copyright/language differs: never assume original CC0.
        ids={r["rightsIdentifier"].lower() for r in citation["rights"]}
        required="cc-by-nc-4.0" if cohort=="svalbard" else "cc0-1.0"
        if required not in ids and not (cohort=="barents" and citation["CC0_metadata_confirmed"]):
            receipt.append({"flyway":cohort,"status":"SOURCE_LICENSE_CONFLICT"});continue
        uid=matched["uuid"]
        item=get_public_json(ROOT+f"/core/items/{uid}",meta,items={uid})
        if item["status"]!="PUBLIC_METADATA_JSON_VERIFIED" or str((item["data"] or {}).get("handle"))!=matched["handle"]:
            receipt.append({"flyway":cohort,"status":"ORIGINAL_ITEM_IDENTITY_MISMATCH"});continue
        bundles=get_public_json(ROOT+f"/core/items/{uid}/bundles",meta,items={uid})
        if bundles["status"]!="PUBLIC_METADATA_JSON_VERIFIED":
            receipt.append({"flyway":cohort,"status":"PUBLIC_ORIGINAL_BUNDLE_NOT_ACCESSIBLE"});continue
        b=[x for x in bundle_items(bundles["data"],"bundles") if
           x.get("name")=="ORIGINAL" and UUID_RE.fullmatch(str(x.get("uuid") or ""))]
        if len(b)!=1:
            receipt.append({"flyway":cohort,"status":"ORIGINAL_BUNDLE_NOT_UNIQUE"});continue
        bid=b[0]["uuid"]
        files_res=get_public_json(ROOT+f"/core/bundles/{bid}/bitstreams",meta,bundles={bid})
        if files_res["status"]!="PUBLIC_METADATA_JSON_VERIFIED":
            receipt.append({"flyway":cohort,"status":"ORIGINAL_FILE_METADATA_NOT_ACCESSIBLE"});continue
        source=bundle_items(files_res["data"],"bitstreams")
        tiny_csv=[x for x in source if str(x.get("name") or "").lower().endswith(".csv") and x.get("sizeBytes")==registration["expected_small_original_csv"]]
        txt=[x for x in source if str(x.get("name") or "").lower().endswith(".txt") and x.get("sizeBytes")==registration["expected_readme_txt"]]
        if len(tiny_csv)!=1 or len(txt)!=1:
            receipt.append({"flyway":cohort,"status":"SMALL_SOURCE_SELECTION_NOT_UNIQUE"});continue
        a=read_small_public_reference(tiny_csv[0],registration["expected_small_original_csv"],".csv")
        b=read_small_public_reference(txt[0],registration["expected_readme_txt"],".txt")
        receipt.append({
          "flyway":cohort,
          "source_original_archive_doi":doi,
          "source_license":registration["license"],
          "status":"TWO_ORIGINAL_SMALL_SOURCES_VERIFIED" if a["status"]==b["status"]=="ORIGINAL_TINY_SOURCE_MD5_VERIFIED" else "SMALL_SOURCE_BYTES_UNVERIFIED",
          "reference_csv":a,
          "readme_txt":b,
          "large_GPS_event_CSV_bytes_downloaded":False
        })
    return {
      "date":c["date"],
      "status":"BARNACLE_ORIGINAL_TINY_REFERENCE_SOURCE_GATE_COMPLETED",
      "n_source_cohorts":len(receipt),
      "sources":receipt,
      "n_cohorts_with_two_md5_verified_reference_files":sum(x["status"]=="TWO_ORIGINAL_SMALL_SOURCES_VERIFIED" for x in receipt),
      "original_tracking_event_or_ZIP_bytes_read":False,
      "raw_tag_strings_or_animal_locations_exported":False,
      "focal_V7_q_U_test_opened":False,
      "source_is_supplemental_phenology_tables":False,
      "no_ebird":True,
      "claim_limit":"Original public reference table structural read only. Author supplementary Tables S2–S7 are separate from the Movebank original GPS dataset; q and bird response still unestimated."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--metadata-contract",type=Path,default=META_CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    obj=audit(json.loads(a.contract.read_text()),json.loads(a.metadata_contract.read_text()))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
    print("V7_BARNACLE_TINY_CC0_BYNC_SOURCE="+json.dumps(obj,separators=(",",":")))

if __name__=="__main__":
    main()
