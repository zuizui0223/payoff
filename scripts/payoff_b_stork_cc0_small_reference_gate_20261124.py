#!/usr/bin/env python3
"""Small, CC0 README / reference-table source gate. NEVER fetch GPS/ACC ZIPs.

Reads only <=80KB .txt/.csv bitstreams in the ORIGINAL bundle of the three
pinned original DOI items, verifies source MD5, and emits only metadata
indicators (headers, counts, booleans). No raw animal identifiers or rows
leave the CI runner; no experimental outcomes or social effects are fitted.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import build_opener,Request,HTTPRedirectHandler
from urllib.error import HTTPError,URLError

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

from payoff_b_stork_dspace_file_metadata_20261124 import (
  get_metadata, bundle_entries, bitstream_entries,UUID_RE,ROOT
)

CONTRACT=Path(__file__).resolve().parents[1] / "data/payoff_b_stork_small_ref_files_contract_20261124.json"

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def content_meta_gate(file,contract):
    name=str(file.get("name") or "")
    ext=Path(name).suffix.lower()
    n=file.get("sizeBytes")
    if ext not in {".txt",".csv"}:
        raise ValueError("Binary tracking-file extension disallowed")
    if not isinstance(n,int) or n<1 or n>contract["file_access"]["max_file_bytes"]:
        raise ValueError("Reference file outside max-size cap")
    u=str(file.get("uuid") or file.get("id") or "")
    if not UUID_RE.fullmatch(u):
        raise ValueError("Original bitstream UUID missing")
    target=ROOT+f"/server/api/core/bitstreams/{u}/content"
    original=file.get("_links",{}).get("content",{}).get("href","")
    if original!=target:
        raise ValueError("Original content href not exact registered host and bitstream UUID")
    chk=file.get("checkSum") or {}
    if not isinstance(chk,dict) or str(chk.get("checkSumAlgorithm","")).upper()!="MD5":
        raise ValueError("Original public MD5 missing")
    md5=str(chk.get("value") or "").lower()
    if not re.fullmatch("[0-9a-f]{32}",md5):
        raise ValueError("Original public MD5 invalid")
    return ext,n,target,md5


def small_verified_file(file,contract,opener=None):
    ext,expected_bytes,url,expected_md5=content_meta_gate(file,contract)
    opener=opener or build_opener(NoRedirect())
    req=Request(url,headers={"Accept":"text/plain,text/csv,application/octet-stream,*/*",
                             "User-Agent":"PAYOFF-B-CC0-small-reference-only/1.0"})
    try:
        with opener.open(req,timeout=25) as resp:
            actual=urlparse(resp.geturl())
            if actual.hostname!="datarepository.movebank.org" or actual.path!=urlparse(url).path:
                raise ValueError("Unexpected file-content redirect")
            raw=resp.read(contract["file_access"]["max_file_bytes"]+1)
            if len(raw)>contract["file_access"]["max_file_bytes"]:
                raise ValueError("Source content over 80KiB cap")
        if len(raw)!=expected_bytes:
            raise ValueError("Declared source size mismatch")
        if hashlib.md5(raw).hexdigest()!=expected_md5:
            raise ValueError("Original public content MD5 mismatch")
    except (HTTPError,URLError,TimeoutError,OSError,ValueError) as exc:
        return {"status":"SOURCE_REFERENCE_CONTENT_NOT_VERIFIED",
                "extension":ext,
                "error_class":type(exc).__name__,
                "http_status":exc.code if isinstance(exc,HTTPError) else None,
                "raw_source_file_or_rows_committed":False}
    if ext==".csv":
        reader=csv.reader(io.StringIO(raw.decode("utf-8-sig",errors="replace")))
        try:
            head=next(reader)
        except StopIteration:
            head=[]
        count=0
        idx=next((j for j,t in enumerate(head) if re.sub("[^a-z0-9]","",t.lower()) in
                 ("taglocalidentifier","individuallocalidentifier","individualid","tagid")),None)
        ids=set()
        for row in reader:
            if not any(x.strip() for x in row):
                continue
            count+=1
            if idx is not None and idx<len(row) and row[idx]:
                ids.add(row[idx])
        details={"column_names":[str(h)[:100] for h in head[:80]],
                 "n_data_rows":count,
                 "unique_tag_or_individual_count":len(ids) if idx is not None else None,
                 "tag_identity_field_in_schema":bool(idx is not None)}
    else:
        txt=raw.decode("utf-8-sig",errors="replace").lower()
        details={"word_present":{
            "gps":bool(re.search(r"\bgps\b",txt)),
            "accelerometer":bool(re.search(r"\bacc\b|acceleromet",txt)),
            "timestamp":bool(re.search(r"timestamp|time.?stamp",txt)),
            "utc":bool(re.search(r"\butc\b",txt)),
            "frequency_or_interval":bool(re.search(r"frequency|interval|second|minute",txt)),
            "license":bool(re.search(r"\blicen[cs]e\b",txt)),
            "individual":bool(re.search(r"individual|animal",txt)),
        },"readme_n_characters":len(txt)}
    return {
        "status":"PUBLIC_CC0_SOURCE_METADATA_COMPANION_VERIFIED",
        "extension":ext,
        "size_bytes":len(raw),
        "sha256":hashlib.sha256(raw).hexdigest(),
        "md5_matches_public_DSpace_metadata":True,
        "content_metadata_only":details,
        "raw_source_file_or_rows_committed":False,
    }


def audit(contract):
    items=contract["item_uuid"]
    uuids=set(items.values())
    out={
      "date":contract["date"],
      "status":"CC0_REFERENCE_SOURCE_GATE_COMPLETE",
      "original_small_file_scope_only":True,
      "source_items":[],
      "GPS_or_ACC_ZIPs_downloaded":False,
      "source_rows_or_tag_ids_exported":False,
      "tracking_events_downloaded":False,
      "new_survival_or_migration_effect_estimated":False,
      "conspecific_social_cue_accuracy_q_estimated":False,
      "licence_terms_autoaccepted":False,
      "no_ebird":True
    }
    for cohort,uuid in items.items():
        item=get_metadata(f"/server/api/core/items/{uuid}",uuids,set())
        if item["status"]!="PUBLIC_METADATA_OK" or (item["data"] or {}).get("handle")!=contract["item_handle"][cohort]:
            out["source_items"].append({"cohort":cohort,"status":"PUBLIC_ITEM_IDENTITY_NOT_VERIFIED"})
            continue
        res=get_metadata(f"/server/api/core/items/{uuid}/bundles",uuids,set())
        if res["status"]!="PUBLIC_METADATA_OK":
            out["source_items"].append({"cohort":cohort,"status":"BUNDLE_METADATA_UNAVAILABLE"})
            continue
        orig=[b for b in bundle_entries(res["data"] or {}) if b.get("name")=="ORIGINAL" and UUID_RE.fullmatch(str(b.get("uuid") or ""))]
        if len(orig)!=1:
            out["source_items"].append({"cohort":cohort,"status":"ORIGINAL_BUNDLE_NOT_UNIQUE"})
            continue
        bid=orig[0]["uuid"]
        file_res=get_metadata(f"/server/api/core/bundles/{bid}/bitstreams",uuids,{bid})
        if file_res["status"]!="PUBLIC_METADATA_OK":
            out["source_items"].append({"cohort":cohort,"status":"PUBLIC_REFERENCE_FILE_METADATA_UNAVAILABLE"})
            continue
        entries=bitstream_entries(file_res["data"] or {})
        selected=[f for f in entries if Path(str(f.get("name") or "")).suffix.lower() in {".txt",".csv"}]
        if len(selected)!=contract["file_access"]["expected_file_count_per_cohort"]:
            out["source_items"].append({"cohort":cohort,"status":"PUBLIC_REFERENCE_FILES_COUNT_MISMATCH",
                                        "found_small_ref_files":len(selected)})
            continue
        files=[small_verified_file(f,contract) for f in selected]
        out["source_items"].append({"cohort":cohort,
           "status":"SMALL_REFERENCE_DOCUMENTS_VERIFIED" if all(x["status"]=="PUBLIC_CC0_SOURCE_METADATA_COMPANION_VERIFIED" for x in files) else "SMALL_REFERENCE_DOCUMENTS_ACCESS_INCOMPLETE",
           "files":files})
    out["all_three_cohorts_readme_csv_verified"]=len(out["source_items"])==3 and all(
      x["status"]=="SMALL_REFERENCE_DOCUMENTS_VERIFIED" for x in out["source_items"])
    out["claim_limit"]="The READMEs and study reference tables only support source identity/schema/time-context readiness, not individual route co-presence, recorded information transmission, cue reliability, compensation ability or causal inference."
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--contract",type=Path,default=CONTRACT)
    a=p.parse_args()
    result=audit(json.loads(a.contract.read_text()))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("PAYOFF_STORK_CC0_SMALL_SOURCE_GATE="+json.dumps(result,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
