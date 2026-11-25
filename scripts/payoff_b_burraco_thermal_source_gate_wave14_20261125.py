#!/usr/bin/env python3
"""Source-only admission: Burraco et al. Oikos 2021, 3x2x2 experiment."""
import json,sys,hashlib,io,csv,re
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
                if not r:
                    out.append({"sheet":s.title,"rows":0,"status":"EMPTY_SHEET"});continue
                info=s.title.lower()
                if any(k in info for k in ("info","variable","readme","metadata","key","legend","description")):
                    out.append({"sheet":s.title,"rows":len(r),"dictionary":[[str(x)[:500] if x is not None else None for x in v] for v in r[:60]]})
                    continue
                # Choose header from structural design/endpoint names, not outcomes.
                pats=(r"family|sibship|clutch",r"phenol|hatch|delay",r"temp",r"food|feed",r"surv|alive",r"larval|develop|duration|days",r"mass|weight")
                previews=[]
                scores=[]
                for i,row in enumerate(r[:20]):
                    strings=[str(v).strip() if isinstance(v,str) else None for v in row]
                    joined=" ".join(v for v in strings if v)
                    score=sum(bool(re.search(p,joined,re.I)) for p in pats)
                    scores.append(score)
                    previews.append({"nonempty_row":i+1,"text_cells":strings,"score":score})
                hi=max(range(len(scores)),key=lambda j:scores[j])
                if scores[hi]<4:
                    out.append({"sheet":s.title,"status":"HEADER_UNRESOLVED","text_preamble":previews});continue
                h=[str(x).strip() if x is not None else None for x in r[hi]]
                d={}
                for i,x in enumerate(h):
                    if x is None:continue
                    c=Counter(str(v[i]) for v in r[hi+1:] if i<len(v) and v[i] is not None)
                    d[x]={"nonmissing":sum(c.values()),"distinct":len(c)}
                    # Known source design terms only; no durations/masses or outcome values.
                    if re.search(r"family|sibship|clutch|phenol|hatch|delay|temp|food|feed|surv|alive|treat|block",x,re.I) and not re.search(r"length|mass|weight|duration|days|period|time|date|rate|growth",x,re.I) and len(c)<=30:
                        d[x]["levels"]=dict(c)
                out.append({"sheet":s.title,"rows":len(r)-hi-1,"header_nonempty_row":hi+1,"headers":h,"column_support":d,"preamble_text":[v for v in previews if v["nonempty_row"]<=hi+1]})
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
            q.update(status="PROVIDER_MD5_VERIFIED",sha256=hashlib.sha256(b).hexdigest())
            print("VERIFIED_SOURCE "+json.dumps(q,ensure_ascii=True),flush=True)
            q["schema"]=inspect(b,name)
    return o
if __name__=="__main__":
    try:d=run()
    except (Hold,ValueError,KeyError,requests.RequestException) as e:d={"status":"HOLD","error":str(e) if isinstance(e,Hold) else type(e).__name__}
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
