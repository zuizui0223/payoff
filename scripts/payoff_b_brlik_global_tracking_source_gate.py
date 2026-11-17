"""Source-only check for Brlik et al. 2026 global migration timing data.

Zenodo paper-concept ID 18175801, candidate v3 record 19821864.
DO NOT fit an ecological outcome, use eBird, invent cues, or assume location
data from a migration schedule. Verify both authoritative record metadata and
every original downloaded source checksum. Bounded plain CSV scanning only.
"""
import argparse,csv,hashlib,io,json,re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
from scripts.payoff_b_scotland_resource_source_probe import open_url

RECORD_IDS=(18175801,19821864)
API="https://zenodo.org/api/records/{}"
LIMIT_META=1_800_000
LIMIT_ONE=5_000_000
LIMIT_TOTAL=12_000_000
MAX_FIELDS=220
MAX_ROWS=90_000
NA_SET={"","na","n/a","nan","null","none","-999"}


def check_hash(content,source):
    if not isinstance(source,str) or ":" not in source:
        return {"verified":False,"reason":"NO_CHECKSUM"}
    algo,original=source.split(":",1)
    if algo not in ("md5","sha256"):
        return {"verified":False,"reason":"UNSUPPORTED_HASH_ALGORITHM"}
    digest=hashlib.new(algo,content).hexdigest()
    return {"verified":digest.lower()==original.lower(),
            "algorithm":algo,"original":original.lower(),
            "calculated":digest.lower()}


def csv_schema(content,basename):
    try:
        s=content.decode("utf-8-sig")
        charset="utf-8-sig"
    except UnicodeDecodeError:
        s=content.decode("cp1252")
        charset="cp1252"
    first_line=s.splitlines()[0] if s.splitlines() else ""
    delim="\t" if basename.lower().endswith(".tsv") or first_line.count("\t")>first_line.count(",") else ","
    reader=csv.DictReader(io.StringIO(s,newline=""),delimiter=delim)
    cols=reader.fieldnames or []
    if len(cols)>MAX_FIELDS:
        return {"status":"NO_GO_TOO_MANY_COLUMNS","n_columns":len(cols)}
    missing=Counter()
    candidates={
        "individual":[c for c in cols if re.search(r"(individual|bird_?id|tracking|animal|tag|(^|_)id($|_))",c,re.I)],
        "species":[c for c in cols if re.search(r"speci|taxon",c,re.I)],
        "year":[c for c in cols if re.search(r"year|season",c,re.I)],
        "date_or_event":[c for c in cols if re.search(r"date|doy|time|start|end|depart|arriv|stage|spring|autumn|winter|breed|migrat|stopp",c,re.I)],
        "geography":[c for c in cols if re.search(r"(^lat|^lon|latitude|longitude|(^|_)site|location|region|colony|coordinate)",c,re.I)],
        "outcome":[c for c in cols if re.search(r"fitness|recruit|success|fledg|nest|surviv|brood",c,re.I)],
    }
    n=0
    previews=[]
    for row in reader:
        n+=1
        if n<=2:
            relevant=[c for cat in ("individual","species","year","date_or_event","geography","outcome") for c in candidates[cat]]
            relevant=list(dict.fromkeys(relevant))[:34]
            previews.append({col:str(row.get(col) or "")[:90] for col in relevant})
        for c in cols:
            if str(row.get(c) or "").strip().lower() in NA_SET:
                missing[c]+=1
        if n>=MAX_ROWS:
            break
    return {"status":"CSV_SOURCE_READ","delimiter":delim,"encoding":charset,
            "n_rows_scanned":n,"source_scan_row_limit":MAX_ROWS,
            "n_columns":len(cols),"columns":cols,
            "candidate_fields":candidates,
            "missing_count":dict(missing),
            "first_two_relevant_records":previews,
            "row_limit_not_reached":n<MAX_ROWS}


def record_metadata(record_id):
    u=API.format(record_id)
    resp=open_url(u,timeout=45,max_read=LIMIT_META)
    raw=resp.get("body")
    out={"record_id":record_id,"url":u,"status_code":resp.get("http_status")}
    if not raw or resp.get("http_status")!=200:
        out["gate"]="NO_METADATA"
        return out,None
    info=json.loads(raw)
    out.update({
        "gate":"SOURCE_ZENODO_METADATA_READ",
        "source_metadata_sha256":hashlib.sha256(raw).hexdigest(),
        "doi":info.get("doi"),
        "conceptdoi":info.get("conceptdoi"),
        "conceptrecid":info.get("conceptrecid"),
        "record_id_fetched":info.get("id"),
        "record_version":info.get("metadata",{}).get("version"),
        "published":info.get("metadata",{}).get("publication_date"),
        "license":info.get("metadata",{}).get("license"),
        "record_title":info.get("metadata",{}).get("title"),
        "file_manifest":[{
            "key":f.get("key"),
            "bytes":f.get("size"),
            "source_checksum":f.get("checksum"),
            "source_url":f.get("links",{}).get("self")
        } for f in info.get("files",[])]
    })
    return out,info


def audit():
    entries=[]
    chosen=None
    for identifier in RECORD_IDS:
        receipt,data=record_metadata(identifier)
        entries.append(receipt)
        if data is not None and (chosen is None or identifier==19821864):
            chosen=(receipt,data)
    out={
      "status":"PAYOFF_B_BRLIK_GLOBAL_TRACKING_SCHEMA_PREFLIGHT",
      "paper_doi":"10.1038/s41559-026-03208-w",
      "paper_data_statement_doi":"10.5281/zenodo.18175801",
      "candidate_published_v3_doi":"10.5281/zenodo.19821864",
      "zenodo_records":entries,
      "source_eBird_not_used":True,
      "paper_prior_art_already_shows_partial_compensation_and_nonbreeding_reset":True,
      "analysis_of_information_x_recourse_fitted":False,
      "actual_reproductive_success_available_unverified":True
    }
    if chosen is None:
        out["gate"]="NO_GO_ZENODO_VERSION_METADATA"
        return out
    receipt,record=chosen
    if (receipt.get("conceptdoi") not in (
           "10.5281/zenodo.18175801","10.5281/zenodo.19821864")
        and receipt.get("conceptrecid") not in ("18175801",18175801)):
        out["gate"]="NO_GO_VERSION_RELATIONSHIP_UNCONFIRMED"
        out["version_warning"]="Official conceptDOI did not match paper statement"
        return out
    total=0
    files=[]
    for f in record.get("files",[]):
        name=f.get("key") or ""
        size=f.get("size")
        uri=f.get("links",{}).get("self")
        row={"name":name,"source_size":size,"source_checksum":f.get("checksum"),
             "official_url":uri}
        if not name.lower().endswith((".csv",".tsv",".md",".txt",".html")):
            row["status"]="NOT_TARGET_FORMAT"
            files.append(row);continue
        if not uri or not uri.startswith("https://") or urlparse(uri).hostname not in ("zenodo.org","www.zenodo.org"):
            row["status"]="UNVERIFIED_OR_UNAUTHORIZED_FILE_URL"
            files.append(row);continue
        if not isinstance(size,int) or size<=0 or size>LIMIT_ONE or total+size>LIMIT_TOTAL:
            row["status"]="BOUNDED_SIZE_SKIP"
            files.append(row);continue
        r=open_url(uri,timeout=70,max_read=size)
        raw=r.get("body")
        row["http_status"]=r.get("http_status")
        if not raw or r.get("http_status")!=200:
            row["status"]="ORIGINAL_FILE_NOT_PUBLICLY_AVAILABLE"
        elif len(raw)!=size:
            row["status"]="SOURCE_MANIFEST_SIZE_MISMATCH"
        else:
            verify=check_hash(raw,f.get("checksum"))
            row["original_sha256"]=hashlib.sha256(raw).hexdigest()
            row["verification"]=verify
            if not verify["verified"]:
                row["status"]="SOURCE_CHECKSUM_FAILURE"
            elif name.lower().endswith((".csv",".tsv")):
                row["status"]="ORIGINAL_CSV_VERIFIED"
                row["original_table_schema"]=csv_schema(raw,name)
            else:
                row["status"]="VERIFIED_SUPPORTING_TEXT"
                row["supporting_preview_first_800"]=raw.decode("utf-8",errors="replace")[:800]
            total+=len(raw)
        files.append(row)
    out["inspected_v3_files"]=files
    out["verified_downloaded_bytes"]=total
    out["verified_tabular_files"]=sum(x.get("status")=="ORIGINAL_CSV_VERIFIED" for x in files)
    out["gate"]="SOURCE_COLUMNS_ADMITTED_PENDING_CUE_GEOGRAPHY" if out["verified_tabular_files"]>=1 \
        else "NO_GO_NO_SOURCE_CSV"
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    outcome=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(outcome,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
