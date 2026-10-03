#!/usr/bin/env python3
"""Schema-only probe for the Pederson et al. Eurasian curlew Dryad dataset.

This script deliberately does NOT compute biological outcomes.

It:
1. identifies the six Dryad files from known file_stream IDs using HTTP headers;
2. downloads only the smallest XLSX workbook;
3. reports workbook sheet names, dimensions, and header-like cells from the
   first few rows of each sheet.

Purpose: decide whether a migration-level summary table exists before freezing
any clock-portfolio empirical analysis.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET


FILE_IDS=(1522013,1522014,1522015,1522016,1522017,1522018)
BASE="https://datadryad.org/downloads/file_stream/{}"

NS={
    "main":"http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkg":"http://schemas.openxmlformats.org/package/2006/relationships",
}

CANDIDATE_TERMS=(
    "id","individual","bird","tag","year","season","spring","autumn",
    "departure","arrival","migration","duration","stopover","distance",
    "track","date","time",
)


def request(url:str,method:str="GET"):
    req=urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130 Safari/537.36",
            "Accept":"*/*",
        },
    )
    return urllib.request.urlopen(req,timeout=120)


def header_filename(headers)->str|None:
    cd=headers.get("Content-Disposition","")
    m=re.search(r"""filename\*?=(?:UTF-8''|")?([^";]+)""",cd,re.I)
    return m.group(1).strip('"') if m else None


def shared_strings(zf):
    p="xl/sharedStrings.xml"
    if p not in zf.namelist():
        return []
    root=ET.fromstring(zf.read(p))
    out=[]
    for si in root.findall("main:si",NS):
        out.append("".join(t.text or "" for t in si.findall(".//main:t",NS)))
    return out


def cell_value(cell,strings):
    kind=cell.attrib.get("t")
    if kind=="inlineStr":
        return "".join(t.text or "" for t in cell.findall(".//main:t",NS))
    v=cell.find("main:v",NS)
    raw="" if v is None or v.text is None else v.text
    if kind=="s" and raw:
        try:
            return strings[int(raw)]
        except Exception:
            return raw
    return raw


def col_index(ref):
    m=re.match(r"([A-Z]+)",ref or "")
    if not m:
        return 0
    n=0
    for ch in m.group(1):
        n=n*26+(ord(ch)-64)
    return n-1


def sheet_paths(zf):
    wb=ET.fromstring(zf.read("xl/workbook.xml"))
    rels=ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rmap={r.attrib["Id"]:r.attrib["Target"] for r in rels.findall("pkg:Relationship",NS)}
    out=[]
    for sh in wb.findall("main:sheets/main:sheet",NS):
        name=sh.attrib.get("name","")
        rid=sh.attrib.get(f"{{{NS['rel']}}}id")
        target=rmap.get(rid,"")
        if target.startswith("/"):
            path=target.lstrip("/")
        elif target.startswith("xl/"):
            path=target
        else:
            path="xl/"+target.lstrip("/")
        out.append((name,path))
    return out


def inspect_sheet(zf,path,strings,max_rows=8,max_cols=80):
    root=ET.fromstring(zf.read(path))
    dim=root.find("main:dimension",NS)
    rows=[]
    candidates=[]
    for row in root.findall("main:sheetData/main:row",NS)[:max_rows]:
        vals={}
        for cell in row.findall("main:c",NS):
            idx=col_index(cell.attrib.get("r",""))
            if idx>=max_cols:
                continue
            val=cell_value(cell,strings)
            if val!="":
                vals[idx]=val[:200]
                low=val.lower()
                if any(term in low for term in CANDIDATE_TERMS):
                    candidates.append({
                        "row":int(row.attrib.get("r","0")),
                        "cell":cell.attrib.get("r"),
                        "text":val[:200],
                    })
        if vals:
            width=min(max(vals)+1,max_cols)
            arr=[""]*width
            for i,v in vals.items():
                arr[i]=v
            rows.append({"row":int(row.attrib.get("r","0")),"values":arr})
    return {
        "dimension":None if dim is None else dim.attrib.get("ref"),
        "first_rows":rows,
        "candidate_header_cells":candidates,
    }


def main():
    receipt={
        "date":"2026-10-03",
        "status":"SCHEMA_ONLY",
        "dataset_doi":"10.5061/dryad.nk98sf7w6",
        "outcomes_opened":False,
        "files":[],
    }

    # HEAD only: identify file names/sizes without opening workbook outcomes.
    for fid in FILE_IDS:
        url=BASE.format(fid)
        meta={"file_id":fid,"url":url}
        try:
            with request(url,"HEAD") as res:
                meta.update({
                    "status":getattr(res,"status",None),
                    "content_length":int(res.headers.get("Content-Length","0") or 0),
                    "content_type":res.headers.get("Content-Type"),
                    "filename":header_filename(res.headers),
                    "resolved_url":res.geturl(),
                })
        except Exception as exc:
            # Some origins reject HEAD; do a ranged GET and do not retain body.
            try:
                req=urllib.request.Request(
                    url,
                    headers={
                        "User-Agent":"Mozilla/5.0",
                        "Range":"bytes=0-0",
                    },
                )
                with urllib.request.urlopen(req,timeout=120) as res:
                    res.read(1)
                    meta.update({
                        "status":getattr(res,"status",None),
                        "content_length":int(res.headers.get("Content-Length","0") or 0),
                        "content_range":res.headers.get("Content-Range"),
                        "content_type":res.headers.get("Content-Type"),
                        "filename":header_filename(res.headers),
                        "resolved_url":res.geturl(),
                    })
            except Exception as exc2:
                meta["error"]=f"{type(exc).__name__}: {exc}; fallback {type(exc2).__name__}: {exc2}"
        receipt["files"].append(meta)

    xlsx=[
        f for f in receipt["files"]
        if str(f.get("filename","")).lower().endswith(".xlsx")
    ]
    # Prefer named Poland workbook if metadata identifies it; otherwise smallest XLSX.
    selected=next((f for f in xlsx if "poland" in str(f.get("filename","")).lower()),None)
    if selected is None and xlsx:
        selected=min(xlsx,key=lambda f:f.get("content_length") or 10**18)

    if selected is None:
        receipt["status"]="NO_XLSX_IDENTIFIED"
    else:
        with request(selected["url"],"GET") as res:
            raw=res.read()
        selected["downloaded_bytes"]=len(raw)
        selected["sha256"]=hashlib.sha256(raw).hexdigest()
        if not raw.startswith(b"PK"):
            receipt["status"]="SELECTED_NOT_XLSX_ZIP"
        else:
            with zipfile.ZipFile(BytesIO(raw)) as zf:
                strings=shared_strings(zf)
                sheets=[]
                for name,path in sheet_paths(zf):
                    sheets.append({
                        "name":name,
                        "path":path,
                        **inspect_sheet(zf,path,strings),
                    })
                receipt["selected_workbook"]={
                    "file_id":selected["file_id"],
                    "filename":selected.get("filename"),
                    "sha256":selected["sha256"],
                    "sheet_count":len(sheets),
                    "sheets":sheets,
                }
                receipt["status"]="WORKBOOK_SCHEMA_PARSED"

    out=Path("outputs/payoff_b_curlew_schema_probe.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    main()
