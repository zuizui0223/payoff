#!/usr/bin/env python3
"""Exact target source acquisition; metadata and design schema only, no outcomes fitted."""
import json,sys,hashlib,io,csv,zipfile,re
from pathlib import Path,PurePosixPath
from urllib.parse import quote,urlparse
from collections import Counter
import requests,openpyxl
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold,manifest
DOI="10.5061/dryad.02v6wwq5k"
RID=(6425791,6425793)
TITLE="effects of phenological mismatch under warming are modified by community context"
CAP=6_000_000
def norm(t):return " ".join(re.sub(r"[^a-z0-9]+"," ",str(t).lower()).split())
def schema(b,name):
    ext=Path(name).suffix.lower()
    if ext in (".csv",".tsv",".txt"):
        try:t=b.decode("utf-8-sig")
        except UnicodeError:return {"status":"NON_UTF8_TEXT"}
        try:
            d=csv.Sniffer().sniff(t[:8000],delimiters=",;\t")
            r=csv.DictReader(io.StringIO(t),dialect=d)
            rows=list(r);h=r.fieldnames or []
            if not h or len(h)<2 or len(set(h))!=len(h) or any(None in x or any(v is None for v in x.values()) for x in rows):
                return {"status":"TEXT_NOT_RECTANGULAR","bytes":len(b)}
            # Report only exact column names and nonmissing/distinct counts for design-like fields;
            # no biological outcome values and no guessed cohort mapping.
            fields={}
            for k in h:
                if re.search(r"vial|block|treat|rep|temp|delay|time|species|host|paras|food|density|community|egg|control|stage",k,re.I):
                    z=Counter(x[k] for x in rows if x[k].strip())
                    fields[k]={"nonmissing":sum(z.values()),"distinct":len(z)}
                    if len(z)<=15 and not re.search(r"count|number|surv|emerg|hatched|dead|adult|egg|time|weight|mass|success|rate",k,re.I):
                        fields[k]["levels"]=dict(z)
            return {"status":"TABLE_SCHEMA_ONLY","rows":len(rows),"header":h,"design_column_support":fields}
        except (csv.Error,UnicodeError,ValueError):return {"status":"NON_TABULAR_TEXT","bytes":len(b)}
    if ext==".xlsx":
        w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
        out=[]
        try:
            for s in w.worksheets:
                rows=[x for x in s.iter_rows(values_only=True) if any(v is not None for v in x)]
                if not rows:out.append({"sheet":s.title,"status":"EMPTY_SHEET"});continue
                h=[str(x) if x is not None else None for x in rows[0]]
                out.append({"sheet":s.title,"nonempty_rows":len(rows),"first_row_fields":h})
        finally:w.close()
        return {"status":"WORKBOOK_SCHEMA_ONLY","sheets":out}
    if ext==".zip":
        out=[]
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            infos=z.infolist()
            if len(infos)>300 or sum(v.file_size for v in infos)>30_000_000:raise Hold("ZIP_LIMIT")
            for x in infos:
                if x.is_dir():continue
                if PurePosixPath(x.filename).is_absolute() or ".." in PurePosixPath(x.filename).parts:raise Hold("ZIP_PATH")
                rec={"path":x.filename,"bytes":x.file_size}
                if Path(x.filename).suffix.lower() in (".csv",".tsv",".xlsx",".txt") and x.file_size<=CAP:
                    bb=z.read(x);rec.update(sha256=hashlib.sha256(bb).hexdigest(),schema=schema(bb,x.filename))
                out.append(rec)
        return {"status":"ZIP_MANIFEST_AND_TABLE_SCHEMA_ONLY","members":out}
    return {"status":"FILE_IDENTIFIED_NOT_PARSED"}
def run():
    o={"status":"EXACT_TARGET_SOURCE_GATE_NO_FIT","article_doi":"10.1111/gcb.16195","dryad_doi":DOI,"zenodo":{}}
    with requests.Session() as s:
        try:
            o["dryad_manifest"]={"status":"METADATA_RETRIEVED",**manifest(s,DOI)}
        except (Hold,ValueError,KeyError,requests.RequestException) as e:o["dryad_manifest"]={"status":"HOLD","error":str(e) if isinstance(e,Hold) else type(e).__name__}
        for rid in RID:
            z=o["zenodo"][str(rid)]={"status":"HOLD","record_id":rid,"files":[]}
            try:
                m=json.loads(fetch(s,f"https://zenodo.org/api/records/{rid}",cap=1_500_000))
                md=m.get("metadata",{})
                if str(m.get("id"))!=str(rid) or TITLE not in norm(md.get("title","")):raise Hold("RECORD_IDENTITY")
                if DOI not in json.dumps(md.get("related_identifiers",[])).lower():raise Hold("RELATED_DRYAD_DOI")
                z.update(status="EXACT_LINKED_RECORD",title=md.get("title"),doi=m.get("doi"),license=md.get("license"),access_right=md.get("access_right"),related_identifiers=md.get("related_identifiers"))
                if md.get("access_right") not in ("open",None):raise Hold("NOT_OPEN")
                for f in m.get("files",[]):
                    key=f.get("key","");size=f.get("size");checksum=f.get("checksum","")
                    q={"name":key,"bytes":size,"checksum":checksum,"status":"METADATA_ONLY"};z["files"].append(q)
                    if not isinstance(size,int) or not 0<size<=CAP or not re.fullmatch(r"md5:[0-9a-f]{32}",checksum):q["status"]="HOLD_UNVERIFIABLE";continue
                    u=f.get("links",{}).get("self")
                    if not u or urlparse(u).scheme!="https" or urlparse(u).hostname!="zenodo.org":q["status"]="HOLD_SOURCE_LINK";continue
                    try:
                        b=fetch(s,u,cap=CAP)
                        if len(b)!=size or hashlib.md5(b).hexdigest()!=checksum[4:]:raise Hold("SOURCE_MD5")
                        q.update(status="PROVIDER_MD5_VERIFIED",sha256=hashlib.sha256(b).hexdigest(),schema=schema(b,key))
                    except (Hold,ValueError,KeyError,requests.RequestException,zipfile.BadZipFile) as e:q.update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
            except (Hold,ValueError,KeyError,requests.RequestException) as e:z["error"]=str(e) if isinstance(e,Hold) else type(e).__name__
    return o
if __name__=="__main__":
    d=run();print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=True)+"\n")
