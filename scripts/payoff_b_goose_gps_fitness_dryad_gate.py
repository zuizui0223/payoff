"""PAYOFF-B: official Dryad barnacle goose original GPS + breeding source check.

Published DOI 10.5061/dryad.m63xsj47x (Boom et al. 2023).
No downloaded bird outcome coefficients, regressions or proxy cue invention.
Use official public Dryad API's *documented full-dataset* download URL.
Fail-close if the public endpoint blocks or raw files mismatch source manifest.
"""
import argparse,csv,hashlib,io,json,re,zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote
from scripts.payoff_b_scotland_resource_source_probe import open_url
from scripts.payoff_b_dryad_food_supplement_provisioning_probe import (
    json_source,version_ids_from_listing,file_rows_from_listing,
    validate_manifest_digest
)

DOI="10.5061/dryad.m63xsj47x"
ROOT="https://datadryad.org/api/v2/datasets/"+quote("doi:"+DOI,safe="")
REQUIRED_FILES=("1.NestLocationData.csv","2.RawTrackingData_GPSACC.csv",
                "3.RawTrackingData_GPSonly.csv","4.ID_list.csv","README.md")
MAX_RAW_PACKAGE=18_000_000
MAX_SOURCE_CSV=12_000_000
MAX_CSV_ROWS=280_000


def columns_and_counts(data,name):
    try:
        source=data.decode("utf-8-sig")
    except UnicodeDecodeError:
        source=data.decode("cp1252")
    reader=csv.DictReader(io.StringIO(source,newline=""))
    header=reader.fieldnames or []
    if len(header)>220:
        return {"status":"TOO_MANY_ORIGINAL_SOURCE_COLUMNS","n_columns":len(header)}
    relevant={
        "identity":[c for c in header if re.search(r"(^id|bird|individual|tag|track|animal|name|ring)",c,re.I)],
        "temporal":[c for c in header if re.search(r"date|time|timestamp|year|doy|arrival|depart|start|stop|spring",c,re.I)],
        "spatial":[c for c in header if re.search(r"(^lat|^lon|latitude|longitude|position|coordinate|nest_loc|site)",c,re.I)],
        "breeding":[c for c in header if re.search(r"nest|breed|success|hatch|propens|offspring",c,re.I)],
        "environment":[c for c in header if re.search(r"gdd|temp|greenup|spring|weather|resource",c,re.I)]
    }
    n=0
    miss=Counter()
    unique={}
    for k in ("identity","temporal","spatial","breeding","environment"):
        for col in relevant[k]:
            if col not in unique and len(unique)<55:
                unique[col]=set()
    for row in reader:
        n+=1
        for col in unique:
            raw=str(row.get(col) or "").strip()
            if raw=="" or raw.lower() in ("na","nan","null","n/a","-999"):
                miss[col]+=1
            elif len(unique[col])<15000:
                unique[col].add(raw)
        if n>=MAX_CSV_ROWS:break
    return {
        "status":"SOURCE_CSV_SCHEMA_INSPECTED",
        "n_source_rows":n,
        "row_limit":MAX_CSV_ROWS,
        "n_columns":len(header),
        "header":header,
        "field_groups":relevant,
        "field_missing_n":dict(miss),
        "field_unique_count":{k:len(v) for k,v in unique.items()},
        "no_spatial_coordinates_inferred":True,
    }


def source_package():
    dataset,m0=json_source(ROOT)
    summary={
        "status":"PAYOFF_B_GOOSE_GPS_FITNESS_DRYAD_SOURCE_GATE",
        "source_doi":DOI,
        "paper_doi":"10.1111/1365-2656.14020",
        "dataset_metadata":m0,
        "only_public_documented_Dryad_API_endpoints":True,
        "uses_eBird":False,
        "bird_fitness_effect_fitted":False,
        "no_proxy_cue_inferred":True,
    }
    if dataset is None:
        summary["gate"]="NO_GO_PUBLIC_DATASET_METADATA"
        return summary
    versions,vr=json_source(ROOT+"/versions")
    summary["versions_metadata"]=vr
    ids=version_ids_from_listing(versions)
    summary["versions"]=[{"id":x,"versionNumber":v} for x,v,obj in ids]
    if not ids:
        summary["gate"]="NO_GO_PUBLIC_VERSION_MANIFEST"
        return summary
    vid=ids[-1][0]
    fl,fr=json_source(f"https://datadryad.org/api/v2/versions/{vid}/files")
    summary["source_file_list_receipt"]=fr
    if fl is None:
        summary["gate"]="NO_GO_FILE_MANIFEST"
        return summary
    manifest=file_rows_from_listing(fl)
    summary["source_files"]=manifest
    byname={r["path"]:r for r in manifest}
    summary["required_files_in_metadata"]=list(
        sorted(set(REQUIRED_FILES)&set(byname))
    )
    missing=set(REQUIRED_FILES)-set(byname)
    if missing:
        summary["gate"]="NO_GO_REQUIRED_FILE_NOT_LISTED"
        summary["missing_files"]=sorted(missing)
        return summary
    # Official Dryad published API says the following download URL retrieves
    # a complete version. This is not a private/bypass endpoint.
    documented_url=ROOT+"/download"
    response=open_url(documented_url,max_read=MAX_RAW_PACKAGE,timeout=90)
    blob=response.get("body")
    summary["official_documented_dataset_download"]={
        "url":documented_url,
        "status":response.get("http_status"),
        "content_type":response.get("content_type"),
        "final_url":response.get("final_url"),
    }
    if response.get("http_status")!=200 or not blob:
        summary["gate"]="HOLD_OFFICIAL_ARCHIVE_DOWNLOAD_UNAVAILABLE"
        return summary
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        summary["gate"]="HOLD_OFFICIAL_ARCHIVE_NOT_A_ZIP"
        return summary
    summary["full_package_sha256"]=hashlib.sha256(blob).hexdigest()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names=z.namelist()
        summary["zip_names"]=names[:80]
        verified={}
        for basename in REQUIRED_FILES:
            matches=[n for n in names if n==basename or n.endswith("/"+basename)]
            if len(matches)!=1:
                summary["gate"]="NO_GO_DUPLICATE_OR_MISSING_SOURCE_MEMBER"
                summary["file_name_disambiguation"]={basename:matches}
                return summary
            zip_info=z.getinfo(matches[0])
            metadata=byname[basename]
            if zip_info.file_size!=metadata["size"] or zip_info.file_size>MAX_SOURCE_CSV:
                summary["gate"]="NO_GO_SOURCE_MEMBER_LENGTH"
                summary["bad_member"]=basename
                return summary
            raw=z.read(matches[0])
            digest=validate_manifest_digest(raw,metadata)
            if not digest["verified"]:
                summary["gate"]="NO_GO_SOURCE_CHECKSUM"
                summary["bad_member"]=basename
                summary["digest"]=digest
                return summary
            verified[basename]={
                "length":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
                "source_checksum":metadata.get("digest"),
                "source_checksum_verified":True,
            }
            if basename.lower().endswith(".csv"):
                verified[basename]["schema"]=columns_and_counts(raw,basename)
            else:
                verified[basename]["readme_first_3000"]=raw.decode(
                    "utf-8",errors="replace")[:3000]
    summary["verified_original"]=verified
    summary["gate"]="ORIGINAL_GPS_NEST_SOURCE_SCHEMA_ADMITTED"
    summary["breeding_effect_fitted"]=False
    summary["information_recourse_effect_fitted"]=False
    return summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    x=source_package()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(x,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
