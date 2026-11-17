"""Check public *website* Dryad file_stream links grounded in exact API manifest IDs.

Official website file links (not API /files/{id}/download) may differ from
the public API's 401 response. This is a bounded, anonymous, GET-only probe.
Never request credentials, bypass site controls or claim source rows when the
original bytes/checksum are not verified.
"""
import argparse,csv,hashlib,io,json
from pathlib import Path
from urllib.parse import quote
from scripts.payoff_b_scotland_resource_source_probe import open_url
from scripts.payoff_b_dryad_food_supplement_provisioning_probe import (
    json_source,version_ids_from_listing,file_rows_from_listing,
    validate_manifest_digest,workbook_schema
)

PUBLIC_WEBSITE_PREFIX="https://datadryad.org/downloads/file_stream/"
DATASETS={
  "boom_goose_nest":{
    "doi":"10.5061/dryad.m63xsj47x",
    "file":"1.NestLocationData.csv",
    "expected_sha256":"385fec7dd65de996a54374296b4bb41bc28a1ba3a0a85b770e39ba369c3c8cef",
  },
  "boom_goose_readme":{
    "doi":"10.5061/dryad.m63xsj47x",
    "file":"README.md",
    "expected_sha256":"883e1c8cb894d65cf48cc835cf04ba4d317c908b1fa720b27a1c57e25de529fc",
  },
  "seress_great_tit_nests":{
    "doi":"10.5061/dryad.qbzkh18dj",
    "file":"Seress_JAE_food_exp_nestdata_2020.2.20.xlsx",
    "expected_sha256":"cbfdc03cae11e27060d229c57c08438fff2803e7713caaee70eca62e5e7a7dc8",
  },
}
MAX_BYTES=250000
def csv_report(raw):
    try:s=raw.decode("utf-8-sig")
    except UnicodeDecodeError:s=raw.decode("cp1252")
    rd=csv.DictReader(io.StringIO(s,newline=""))
    heads=rd.fieldnames or []
    n=0
    for _ in rd:n+=1
    return {"format":"csv","n_rows":n,"n_cols":len(heads),
            "columns":heads,"individual_row_values_not_exposed":True}

def source_result():
    # Retrieve source info once per DOI, then only the declared small files.
    out={
       "status":"PAYOFF_B_OFFICIAL_DRYAD_PUBLIC_WEBSITE_FILE_SOURCE_GATE",
       "anonymous_public_GET_only":True,
       "website_file_stream_is_documented_public_download_route":True,
       "not_private_API_or_credential_bypass":True,
       "published_food_treatment_and_spring_fitness_results_are_prior_art":True,
       "fitted_biological_outcome":False,
       "fitted_frozen_V7_interaction":False,
       "results":{}
    }
    info={}
    for key,row in DATASETS.items():
        doi=row["doi"]
        if doi not in info:
            api="https://datadryad.org/api/v2/datasets/"+quote("doi:"+doi,safe="")
            dataset,meta=json_source(api)
            detail={"dataset_manifest_status":meta}
            if dataset is None:
                info[doi]=(None,detail)
            else:
                versions,vmeta=json_source(api+"/versions")
                ids=version_ids_from_listing(versions)
                detail["version_ids"]=[i for i,v,obj in ids]
                detail["source_versions_status"]=vmeta
                if not ids:
                    info[doi]=(None,detail)
                else:
                    latest=ids[-1][0]
                    file_manifest,fmeta=json_source(
                        f"https://datadryad.org/api/v2/versions/{latest}/files")
                    detail["source_manifest_status"]=fmeta
                    info[doi]=(file_rows_from_listing(file_manifest),detail)
        manifest,detail=info[doi]
        res={"doi":doi,"expected_name":row["file"],
             "expected_sha256":row["expected_sha256"],
             "api_provenance":detail,"role":"SOURCE_ONLY"}
        if manifest is None:
            res["gate"]="HOLD_OFFICIAL_API_MANIFEST"
            out["results"][key]=res
            continue
        files=[f for f in manifest if f.get("path")==row["file"]]
        if len(files)!=1:
            res["gate"]="HOLD_SOURCE_NAME_AMBIGUOUS"
            res["matches"]=len(files)
            out["results"][key]=res
            continue
        f=files[0]
        res["manifest_file"]=f
        size=f.get("size")
        fid=f.get("id")
        if not isinstance(fid,int) or not isinstance(size,int) or not (0<size<=MAX_BYTES):
            res["gate"]="HOLD_FILE_ID_OR_SIZE_OUTSIDE_BOUND"
            out["results"][key]=res
            continue
        public_link=PUBLIC_WEBSITE_PREFIX+str(fid)
        # File ID from official manifest, route from documented public website.
        res["official_public_website_link"]=public_link
        downloaded=open_url(public_link,max_read=size,timeout=60)
        raw=downloaded.get("body")
        res["response"]={k:v for k,v in downloaded.items() if k!="body"}
        if downloaded.get("http_status")!=200 or not raw:
            res["gate"]="HOLD_PUBLIC_WEBSITE_SOURCE_UNAVAILABLE"
        elif len(raw)!=size:
            res["gate"]="HOLD_PUBLIC_WEBSITE_SOURCE_SIZE_MISMATCH"
            res["received_bytes"]=len(raw)
        else:
            original_sha256=hashlib.sha256(raw).hexdigest()
            verified=validate_manifest_digest(raw,f)
            res["file_sha256"]=original_sha256
            res["source_manifest_digest_verification"]=verified
            if (original_sha256!=row["expected_sha256"]
                or not verified["verified"]):
                res["gate"]="HOLD_ORIGINAL_SOURCE_SHA_MISMATCH"
            elif row["file"].endswith(".csv"):
                res["original_table_schema"]=csv_report(raw)
                res["gate"]="ORIGINAL_SOURCE_CSV_VERIFIED"
            elif row["file"].endswith(".xlsx"):
                res["original_table_schema"]={"format":"xlsx",
                    "sheets":workbook_schema(raw)}
                res["gate"]="ORIGINAL_SOURCE_XLSX_VERIFIED"
            else:
                res["original_text_first_1800"]=raw.decode("utf-8",errors="replace")[:1800]
                res["gate"]="ORIGINAL_SOURCE_TEXT_VERIFIED"
        out["results"][key]=res
    out["all_originals_verified"]=all(x["gate"].endswith("_VERIFIED")
                                for x in out["results"].values())
    out["boom_original_nesting_rows_available"]=(
      out["results"]["boom_goose_nest"]["gate"]=="ORIGINAL_SOURCE_CSV_VERIFIED")
    out["seress_original_nesting_sheets_available"]=(
      out["results"]["seress_great_tit_nests"]["gate"]=="ORIGINAL_SOURCE_XLSX_VERIFIED")
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    ans=source_result()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(ans,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(ans,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
