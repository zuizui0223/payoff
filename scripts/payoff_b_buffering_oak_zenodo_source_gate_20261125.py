#!/usr/bin/env python3
"""Public CC0 Zenodo oak source, and metadata-only Vazquez manifest diagnosis.
No protected-file retry, no biological fit, no raw data published.
"""
import csv, hashlib, io, json, sys
from pathlib import Path
import requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import manifest, fetch, Hold

OAK_URL="https://zenodo.org/records/5306693/files/pollen_addition_results.csv?download=1"
OAK_MD5="9bb924a2d0739e78e6823f1df6878e6a"
OAK_DOI="10.5061/dryad.sn02v6x2b"
V_DOI="10.5061/dryad.37pvmcvmp"

def oak_schema(b):
    if hashlib.md5(b).hexdigest()!=OAK_MD5:
        raise Hold("ZENODO_MD5_MISMATCH")
    text=b.decode("utf-8-sig")
    dialect=csv.Sniffer().sniff(text[:4096],delimiters=",;\t")
    reader=csv.DictReader(io.StringIO(text),dialect=dialect)
    cols=reader.fieldnames
    if not cols or len(set(cols))!=len(cols): raise Hold("CSV_HEADER_INVALID")
    rows=list(reader)
    if not rows or any(None in r for r in rows): raise Hold("CSV_ROWS_INVALID")
    return {"file_sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),
        "delimiter":dialect.delimiter,"headers":cols,"rows":len(rows),
        "missing_counts":{c:sum((r[c] or "").strip().lower() in {"","na","nan","null"} for r in rows) for c in cols},
        "status":"ORIGINAL_BYTES_VERIFIED_SCHEMA_ONLY"}

def run():
    result={"status":"SOURCE_ONLY_NO_NEW_FIT","oak":{"doi":OAK_DOI,"provider_md5":OAK_MD5,
        "url":OAK_URL},"vazquez":{"doi":V_DOI}}
    with requests.Session() as s:
        try:
            b=fetch(s,OAK_URL,cap=100_000)
            result["oak"].update(oak_schema(b))
        except (Hold,ValueError,requests.RequestException,csv.Error) as e:
            result["oak"].update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
        try:
            m=manifest(s,V_DOI)
            result["vazquez"].update(m,status="METADATA_ONLY_NO_DOWNLOAD")
        except (Hold,ValueError,requests.RequestException,KeyError) as e:
            result["vazquez"].update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
    # Only header/aggregate counts and public source metadata in log/artifact.
    print(json.dumps(result,indent=2,ensure_ascii=False),flush=True)
    return result

if __name__=="__main__":
    out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(run(),indent=2,ensure_ascii=False)+"\n")
