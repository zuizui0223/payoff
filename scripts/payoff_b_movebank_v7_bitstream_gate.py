"""Read public original GPS/reference bitstreams from verified Movebank DOIs.

This is source schema discovery, NOT a fitted migration route, arrival timing,
or q × urgency effect. DSpace REST returns HATEOAS links and repository
checksums. Copyright/CC BY-NC restrictions are preserved for the 2 flyways.
"""
import argparse,csv,hashlib,io,json,re,zipfile
from collections import Counter
from pathlib import Path
from scripts.payoff_b_scotland_resource_source_probe import open_url
from scripts.payoff_b_movebank_v7_published_source_gate import (
    ROOT,DOIS,controlled_link,source_json,discover
)

MAX_BITSTREAM=22_000_000
MAX_TOTAL=57_000_000
SCAN_ROWS=180_000


def checksum_compare(blob,source):
    if not isinstance(source,dict) or not source.get("value"):
        return {"source_verified":False,"reason":"NO_OFFICIAL_DSPACE_CHECKSUM"}
    alg=str(source.get("checkSumAlgorithm") or source.get("algorithm") or "").lower().replace("-","")
    if alg not in ("md5","sha256"):
        return {"source_verified":False,"reason":"UNRECOGNIZED_DSPACE_CHECKSUM","name":alg}
    calculated=hashlib.new(alg,blob).hexdigest()
    return {"source_verified":calculated.lower()==str(source["value"]).lower(),
            "algorithm":alg,
            "expected":str(source["value"]).lower(),
            "calculated":calculated.lower()}


def inspect_table(raw,name):
    try:s=raw.decode("utf-8-sig")
    except UnicodeDecodeError:s=raw.decode("cp1252")
    first=s.splitlines()[0] if s.splitlines() else ""
    delim="\t" if first.count("\t")>first.count(",") else ","
    reader=csv.DictReader(io.StringIO(s,newline=""),delimiter=delim)
    names=reader.fieldnames or []
    cnt=0
    missing=Counter()
    id_cols=[n for n in names if re.search(r"individual|(^id$)|tag|bird|animal",n,re.I)]
    date_cols=[n for n in names if re.search(r"time|date|timestamp|year",n,re.I)]
    coords=[n for n in names if re.search(r"longitude|latitude|location.lat|location.long",n,re.I)]
    uniq={n:set() for n in id_cols[:5]}
    for r in reader:
        cnt+=1
        for n in uniq:
            v=str(r.get(n) or "").strip()
            if v and len(uniq[n])<3000:uniq[n].add(v)
        for k in (id_cols+date_cols+coords):
            if str(r.get(k) or "").strip()=="":missing[k]+=1
        if cnt>=SCAN_ROWS:break
    return {"name":name,"n_rows_scanned":cnt,"n_fields":len(names),
            "headers":names[:140],"id_columns":id_cols,
            "date_columns":date_cols,"coordinate_columns":coords,
            "unique_id_values":{k:len(v) for k,v in uniq.items()},
            "missing_sources":dict(missing),
            "no_migration_stops_fitted":True}


def gate():
    ret={"status":"PAYOFF_B_V7_ORIGINAL_MOVEbank_GPS_BITSTREAM_GATE",
         "frozen_contract":"docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md",
         "no_focal_q_x_U_effect_fitted":True,
         "no_eBird":True,
         "source_flyways":{}}
    total=0
    for fly,doi in DOIS.items():
        item=discover(doi)
        result={"doi":doi,"license":item.get("doi_exact_matching_items",[{}])[0].get("license"),
                "doi_gate":item.get("gate")}
        if item.get("gate")!="ARCHIVE_ITEM_DOI_MATCH":
            result["gate"]="NO_GO_SOURCE_ARCHIVE"
            ret["source_flyways"][fly]=result
            continue
        orig=next((b for b in item.get("bundle_overview",[]) if b["name"]=="ORIGINAL"),None)
        if orig is None or not orig.get("bitstreams"):
            result["gate"]="NO_GO_ORIGINAL_BUNDLE"
            ret["source_flyways"][fly]=result
            continue
        rec,obj=source_json(orig["bitstreams"])
        result["bitstreams_listing_receipt"]=rec
        if obj is None:
            result["gate"]="NO_GO_BITSTREAM_MANIFEST"
            ret["source_flyways"][fly]=result
            continue
        bits=obj.get("_embedded",{}).get("bitstreams",[])
        result["original_file_count"]=len(bits)
        docs=[]
        for b in bits:
            name=b.get("name") or ""
            size=b.get("sizeBytes")
            checksum=b.get("checkSum")
            uri=controlled_link(b.get("_links",{}).get("content",{}).get("href"))
            f={"name":name,"size_bytes":size,"source_checksum":checksum,
               "official_bitstream_url":uri}
            if not uri or not isinstance(size,int) or size<=0 or size>MAX_BITSTREAM or total+size>MAX_TOTAL:
                f["status"]="NO_GO_ORIGINAL_LINK_OR_SIZE"
                docs.append(f);continue
            if not (name.lower().endswith((".csv",".txt",".md",".zip"))):
                f["status"]="NON_TABLE_SOURCE_SKIPPED"
                docs.append(f);continue
            res=open_url(uri,max_read=size,timeout=75)
            raw=res.get("body")
            f["http_status"]=res.get("http_status")
            if not raw or res.get("http_status")!=200:
                f["status"]="ORIGINAL_SOURCE_NOT_ACCESSIBLE"
            elif len(raw)!=size:
                f["status"]="SOURCE_SIZE_MISMATCH"
            else:
                f["sha256"]=hashlib.sha256(raw).hexdigest()
                f["checksum_validation"]=checksum_compare(raw,checksum)
                if not f["checksum_validation"]["source_verified"]:
                    f["status"]="SOURCE_DIGEST_NOT_VERIFIED"
                else:
                    f["status"]="OFFICIAL_GPS_SOURCE_VERIFIED"
                    if name.lower().endswith(".csv"):
                        f["source_csv"]=inspect_table(raw,name)
                    elif name.lower().endswith(".zip"):
                        with zipfile.ZipFile(io.BytesIO(raw)) as z:
                            f["zip_members"]=[{"name":m.filename,"size":m.file_size}
                                for m in z.infolist()[:100]]
                    else:
                        f["readme_first_3000"]=raw.decode("utf-8",errors="replace")[:3000]
                    total+=len(raw)
            docs.append(f)
        result["original_files"]=docs
        result["gate"]="VERIFIED_GPS_ORIGINAL_FILES" if any(
            f["status"]=="OFFICIAL_GPS_SOURCE_VERIFIED" and ("source_csv" in f or "zip_members" in f)
            for f in docs
        ) else "HOLD_NO_VERIFIED_LOCATION_BITSTREAM"
        ret["source_flyways"][fly]=result
    ret["source_original_bytes_downloaded"]=total
    ret["all_three_original_gps_admitted"]=all(
         f.get("gate")=="VERIFIED_GPS_ORIGINAL_FILES" for f in ret["source_flyways"].values()
    )
    ret["gate"]="GPS_PROVENANCE_VERIFIED_STOP_REGION_Q_NOT_YET_ADMITTED" if ret["all_three_original_gps_admitted"] else "PARTIAL_OR_BLOCKED_ORIGINAL_GPS"
    return ret


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=gate()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
