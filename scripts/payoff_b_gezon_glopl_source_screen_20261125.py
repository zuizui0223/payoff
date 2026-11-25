#!/usr/bin/env python3
"""Source-frame screen only; no pollen-limitation or primary effect fitted."""
import csv, hashlib, io, json, re, sys, zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
import requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch, Hold

GLOPL_URL="https://raw.githubusercontent.com/idiv-biodiversity/pollen-limitation-data-descriptor/master/Data/GloPL_with_id.csv"
GLOPL_BLOB="d22fe333b19489c473e076dd173ed7a67b1afbf0"
DOI="10.1111/gcb.13209"
SUPPS={"S10":"gcb13209-sup-0010-AppendixS10.docx","S13":"gcb13209-sup-0013-AppendixS13.docx"}
PATTERN=re.compile(r"phenolog\w*|\btiming\b|flower\w*\s+(?:time|date)|\bearly\b|\blate\b|season\w*|snow\w*|frost|warming|mismatch|temporal|anthesis|delayed|compensat\w*|\bwindow\b",re.I)
MISSING={"","na","n/a","nan","null"}
def verify_git_blob(b):
    h=hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()
    if h!=GLOPL_BLOB:raise Hold("PUBLIC_GIT_BLOB_MISMATCH")
def context_column(c):
    # No outcomes or taxon names searched as generic context text.
    low=re.sub(r"[^a-z0-9]","",c.lower())
    if any(k in low for k in ("mean","variance","stderr","response","effectsize","latitude","longitude","species","family","genus","order","fruitset","seedset")):
        return False
    return any(k in low for k in ("author","ref","citation","title","publication","study","comment","note","remark","design","treatment","context","season","phenolog","timing","date","method","doi","year","experiment","condition"))
def identity_columns(h):
    return [c for c in h if re.search(r"author|reference|citation|doi|publication|year|study.?id",c,re.I) and not re.search(r"study.?duration|year.?start|year.?end",c,re.I)]
def screen(b):
    verify_git_blob(b)
    # GloPL includes Unicode author names; don't silently replace bytes.
    t=b.decode("utf-8-sig")
    d=csv.Sniffer().sniff(t[:16000],delimiters=",;\t")
    r=csv.DictReader(io.StringIO(t),dialect=d)
    h=r.fieldnames
    if not h or len(set(h))!=len(h):raise Hold("CSV_HEADER")
    rows=list(r)
    if not rows or any(None in v or any(z is None for z in v.values()) for v in rows):raise Hold("CSV_ROW_SHAPE")
    context=[c for c in h if context_column(c)]
    identity=identity_columns(h)
    taxa=[c for c in h if re.search(r"species|taxon|genus|binomial",c,re.I)]
    hits=Counter()
    coverage={c:sum(v[c].strip().lower() not in MISSING for v in rows) for c in context}
    cand={}
    ge=0;cl=0
    for v in rows:
        ge+=any(re.search(r"\bgezon\b",v[c],re.I) for c in identity)
        cl+=any(re.search(r"\bclaytonia\b",v[c],re.I) for c in taxa)
        cc=[c for c in context if PATTERN.search(v[c])]
        for c in cc:hits[c]+=1
        if not cc:continue
        key=tuple(v[c].strip() for c in identity)
        x=cand.setdefault(key,{"rows":0,"fields":set(),"terms":set()})
        x["rows"]+=1;x["fields"].update(cc)
        for c in cc:x["terms"].update(m.group(0).lower() for m in PATTERN.finditer(v[c]))
    return {"status":"AUTHENTICATED_AUTHOR_SOURCE_FRAME_ONLY","rows":len(rows),"columns":h,"delimiter":d.delimiter,
        "sha256":hashlib.sha256(b).hexdigest(),"git_blob_sha":GLOPL_BLOB,"bytes":len(b),
        "context_columns":context,"identity_columns":identity,"taxon_columns":taxa,"context_nonmissing":coverage,"field_hit_counts":dict(hits),
        "matching_rows":sum(x["rows"] for x in cand.values()),"candidate_identity_groups":len(cand),
        "gezon_identity_matching_rows":ge,"claytonia_taxon_matching_rows":cl,
        "candidate_identities":[{"identity":dict(zip(identity,k)),"rows":v["rows"],"matched_fields":sorted(v["fields"]),"matched_terms":sorted(v["terms"])} for k,v in sorted(cand.items())],
        "note":"Lexical leads only; author source preceding final curation; no extracted numeric biological effects."}

def docx_screen(b):
    if not zipfile.is_zipfile(io.BytesIO(b)):raise Hold("NOT_DOCX")
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        if sum(x.file_size for x in z.infolist())>8_000_000:raise Hold("EXPANSION_LIMIT")
        if "word/document.xml" not in z.namelist():raise Hold("NO_DOCUMENT_XML")
        root=ET.fromstring(z.read("word/document.xml"))
    ns={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    def cell(t):return " ".join(x.text or "" for x in t.findall(".//w:t",ns))
    tables=[]
    for t in root.findall(".//w:tbl",ns):
        rows=[[cell(c) for c in r.findall("w:tc",ns)] for r in t.findall("w:tr",ns)]
        # Short structural preview, not full copyrighted table or biological fit.
        tables.append({"n_rows":len(rows),"row_widths":dict(Counter(map(len,rows))),"first_row":rows[0][:12] if rows else []})
    return {"status":"ORIGINAL_SUPPLEMENT_BYTES_READ_STRUCTURE_ONLY","sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"table_count":len(tables),"tables":tables}
def run():
    out={"status":"SOURCE_FRAME_ONLY_NO_NEW_EFFECT","gezon":{"doi":DOI,"supplements":{}},"glopl":{"url":GLOPL_URL}}
    with requests.Session() as s:
        for name,file in SUPPS.items():
            u=f"https://onlinelibrary.wiley.com/doi/suppl/{DOI}/supinfo/{file}"
            a={"url":u};out["gezon"]["supplements"][name]=a
            try:a.update(docx_screen(fetch(s,u,cap=300_000)))
            except (Hold,ValueError,requests.RequestException,zipfile.BadZipFile,ET.ParseError) as e:a.update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
        try:out["glopl"].update(screen(fetch(s,GLOPL_URL,cap=6_000_000)))
        except (Hold,ValueError,requests.RequestException,csv.Error,UnicodeError) as e:out["glopl"].update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
    print(json.dumps(out,indent=2,ensure_ascii=False),flush=True)
    return out
if __name__=="__main__":
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(run(),indent=2,ensure_ascii=False)+"\n")
