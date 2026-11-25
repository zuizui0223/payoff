#!/usr/bin/env python3
"""Pardee et al. 2019 original public snowmelt × frost × pollen experiment.
Metadata and source-design inspection only. No outcome model or exported raw rows.
"""
import csv, hashlib, io, json, sys
from pathlib import Path
import requests, openpyxl
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch, Hold

BASE="https://zenodo.org/records/4970401/files/"
FILES={
"Claytonia_SeedSet.csv":"8ececdc7e4711c155d51d92733791ef3",
"Delphinium_SeedSet.csv":"ed31af34e704d15d23d6897001d999fd",
"Mertensia_SeedSet.csv":"c18f19a5c5ba7ee9b9ba942a278dfe04",
"Potentilla_SeedSet.csv":"046df7b111a30effc245c68889023073",
"MetaData.xlsx":"69f7e248e121931d62e8465dc46ef442"}
def source(s,name):
    b=fetch(s,BASE+name+"?download=1",cap=1_000_000)
    if hashlib.md5(b).hexdigest()!=FILES[name]:raise Hold("PROVIDER_MD5_MISMATCH")
    return b
def schema(b):
    r=csv.DictReader(io.StringIO(b.decode("utf-8-sig")))
    h=r.fieldnames
    if not h or len(h)!=len(set(h)):raise Hold("BAD_HEADER")
    rows=list(r)
    if not rows or any(None in x for x in rows):raise Hold("BAD_ROWS")
    # Only design levels for explicit treatment/year columns, never outcome values.
    design={}
    for c in h:
        low=c.lower()
        if any(k in low for k in ("treat","snow","frost","pollin","supplem","year")) and not any(k in low for k in ("date","damage","visit","seed","fruit","flower","number","count","abund","time","rate","mean","prop")):
            values=sorted({(x[c] or "").strip() for x in rows})
            if len(values)<=15:design[c]=values
    return {"headers":h,"rows":len(rows),"design_levels":design,
            "missing_counts":{c:sum((x[c] or "").strip().lower() in {"","na","nan","null"} for x in rows) for c in h}}
def run():
    d={"status":"ORIGINAL_SOURCE_ONLY","doi":"10.5061/dryad.kd1r166","files":{}}
    with requests.Session() as s:
        for name in FILES:
            x={"provider_md5":FILES[name]};d["files"][name]=x
            try:
                b=source(s,name)
                x.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status="MD5_VERIFIED")
                if name.endswith(".csv"):x["schema"]=schema(b)
                else:
                    wb=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
                    try:
                        # Provider-published data dictionary, not biological data.
                        x["dictionary"]=[{"sheet":w.title,"rows":w.max_row,"columns":w.max_column,
                            "text_rows":[[str(v)[:200] if isinstance(v,str) else None for v in row[:12]]
                                for row in w.iter_rows(min_row=1,max_row=min(w.max_row or 1,65),values_only=True)]
                            } for w in wb.worksheets if any(k in w.title.lower() for k in ("seed","meta","variable","readme","key"))]
                    finally:wb.close()
            except (Hold,ValueError,requests.RequestException,UnicodeError,KeyError) as e:
                x.update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
    print(json.dumps(d,indent=2),flush=True);return d
if __name__=="__main__":
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(run(),indent=2)+"\n")
