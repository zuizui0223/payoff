#!/usr/bin/env python3
"""Source-only admission: Burraco et al. Oikos 2021, 3x2x2 experiment."""
import json,sys,hashlib,io,csv
from pathlib import Path
from collections import Counter
import requests,openpyxl
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
AID=13089020
CAP=6_000_000
def inspect(b,name):
    if name.lower().endswith(".xlsx"):
        w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
        out=[]
        try:
            for s in w.worksheets:
                r=[r for r in s.iter_rows(values_only=True) if any(v is not None for v in r)]
                info=s.title.lower()
                if any(k in info for k in ("info","variable","readme","metadata","key","legend","description")):
                    out.append({"sheet":s.title,"rows":len(r),"dictionary":[[str(x)[:500] if x is not None else None for x in v] for v in r[:60]]})
                    continue
                h=[str(x) if x is not None else None for x in r[0]]
                d={}
                for i,x in enumerate(h):
                    if x is None:continue
                    c=Counter(str(v[i]) for v in r[1:] if i<len(v) and v[i] is not None)
                    d[x]={"nonmissing":sum(c.values()),"distinct":len(c)}
                    # Known source design terms only; no durations/masses or outcome values.
                    if x.lower() in {"family","phenology","phenn","food","foodn","temperature","temp","tempn","survival","surv","survn","treatment","block","delay","phen","hatching","hatch","feeding"} and len(c)<=15:
                        d[x]["levels"]=dict(c)
                out.append({"sheet":s.title,"rows":len(r)-1,"headers":h,"column_support":d})
        finally:w.close()
        return {"sheets":out}
    if name.lower().endswith(".csv"):
        t=b.decode("utf-8-sig");dialect=csv.Sniffer().sniff(t[:4096],delimiters=",;\t")
        r=csv.DictReader(io.StringIO(t),dialect=dialect);rr=list(r)
        return {"headers":r.fieldnames,"rows":len(rr),"nonmissing":{k:sum(x[k] is not None and x[k]!="" for x in rr) for k in r.fieldnames}}
    return {"status":"FORMAT_HOLD"}
def run():
    o={"status":"SOURCE_ONLY_NO_FIT","article_id":AID,"article_doi":"10.1111/oik.07919","files":[]}
    with requests.Session() as s:
        m=json.loads(fetch(s,f"https://api.figshare.com/v2/articles/{AID}",cap=800000))
        if m.get("id")!=AID or m.get("is_public") is False:raise Hold("SOURCE_ID")
        o.update(title=m.get("title"),dataset_doi=m.get("doi"),license=m.get("license"),version=m.get("version"))
        for f in m.get("files",[]):
            name=f.get("name","");n=f.get("size");md5=f.get("computed_md5") or f.get("supplied_md5");fid=f.get("id")
            q={"name":name,"file_id":fid,"bytes":n,"provider_md5":md5,"status":"METADATA_ONLY"};o["files"].append(q)
            if not name.lower().endswith((".xlsx",".csv")):continue
            if not isinstance(n,int) or not 0<n<=CAP or not md5 or not isinstance(fid,int):
                q["status"]="HOLD_METADATA";continue
            b=fetch(s,f"https://api.figshare.com/v2/file/download/{fid}",cap=CAP)
            if len(b)!=n or hashlib.md5(b).hexdigest()!=md5:raise Hold("SOURCE_MD5_MISMATCH")
            q.update(status="PROVIDER_MD5_VERIFIED",sha256=hashlib.sha256(b).hexdigest(),schema=inspect(b,name))
    return o
if __name__=="__main__":
    try:d=run()
    except (Hold,ValueError,KeyError,requests.RequestException) as e:d={"status":"HOLD","error":str(e) if isinstance(e,Hold) else type(e).__name__}
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
