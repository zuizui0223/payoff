#!/usr/bin/env python3
"""Read only the pinned original Pardikes factorial CSVs and dictionaries.
No outcomes fitted, no authorization bypass, no raw records exported.
"""
import csv,io,json,hashlib,re,sys
from collections import Counter
from pathlib import Path
import requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import verified_bytes,fetch,Hold
RECEIPT="data/payoff_b_pardikes2022_exact_source_gate_wave17_result_20261125.json"
NAMES=("all.dat.nsbNov24.csv","all.dat.sbNov24.csv","README-all.dat.nsbNov24.csv","README-all.dat.sbNov24.csv")
CODE=("PublicationPsitRateFactorMay112021.R","PublicationPropSurv3FactorMay112021.R","CompetitionNSBControlOct31-2021.R")
def inspect(b,name):
    t=b.decode("utf-8-sig")
    d=csv.Sniffer().sniff(t[:12000],delimiters=",\t;")
    rr=list(csv.reader(io.StringIO(t),dialect=d))
    if not rr:raise Hold("EMPTY_CSV")
    h=rr[0]
    if name.startswith("README"):
        # dictionary only, never assume interpretation from outcome signs
        return {"status":"ORIGINAL_DICTIONARY","rows":len(rr),"dictionary":rr[:100],"truncated":len(rr)>100}
    if len(set(h))!=len(h) or any(len(x)!=len(h) for x in rr[1:]):raise Hold("CSV_SHAPE")
    out={"status":"RAW_SCHEMA_ONLY","rows":len(rr)-1,"header":h,"columns":{}}
    for j,k in enumerate(h):
        c=Counter(r[j] for r in rr[1:]);missing=sum(c.get(x,0) for x in ("","NA","NaN"))
        q={"distinct":len(c),"missing":missing}
        # Design labels only; exclude abundance, performance and response-like columns.
        if len(c)<=30 and re.search(r"^(temp(erature)?|species|waspspecies|treatment|hostspecies|host|wasp|block|rep(licate)?|delay|shift|psit(time)?|community|food|competition|group|diet|control|time)$",k,re.I):
            q["levels"]=dict(c)
        out["columns"][k]=q
    return out
def run():
    src=json.loads(Path(RECEIPT).read_text());o={"status":"SOURCE_BYTES_GATE_NO_FIT","article_doi":"10.1111/gcb.16195","dryad_doi":"10.5061/dryad.02v6wwq5k","files":{},"author_code":{}}
    if src["dryad_manifest"]["version"]!=175194:raise Hold("MANIFEST_VERSION")
    with requests.Session() as s:
        for n in NAMES:
            f=src["dryad_manifest"]["files"][n]
            a=o["files"][n]={"file_id":f["file_id"],"expected_bytes":f["bytes"],"expected_digest":f["digest"]}
            try:
                b=verified_bytes(s,f)
                a.update(status="PROVIDER_DIGEST_VERIFIED",sha256=hashlib.sha256(b).hexdigest(),schema=inspect(b,n))
            except (Hold,requests.RequestException,ValueError,UnicodeError,KeyError,csv.Error) as e:
                a.update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
        # Public, linked MIT-licensed author analysis files only.
        try:
            m=json.loads(fetch(s,"https://zenodo.org/api/records/6425791",cap=1500000))
            fm={x["key"]:x for x in m.get("files",[])}
            pinned={x["name"]:x for x in src["zenodo"]["6425791"]["files"]}
            for n in CODE:
                q=o["author_code"][n]={"status":"HOLD"}
                try:
                    f=fm[n];p=pinned[n];u=f["links"]["self"]
                    if not u.startswith("https://zenodo.org/"):raise Hold("SOURCE_LINK")
                    b=fetch(s,u,cap=150000)
                    if len(b)!=p["bytes"] or hashlib.sha256(b).hexdigest()!=p["sha256"]:raise Hold("CODE_HASH")
                    lines=b.decode("utf-8",errors="replace").splitlines()
                    # Limited structural excerpts of original analysis code; no numeric response data.
                    sel=[]
                    for i,line in enumerate(lines,1):
                        if re.search(r"read\.(csv|table)|\b(glmmTMB|glmer|lmer|glm|aggregate|summarise|summarize|group_by|factor)\s*\(|\b(nsb|sb)Nov24",line,re.I):
                            sel.append({"line":i,"code":line[:400]})
                    q.update(status="PINNED_CODE_VERIFIED",sha256=p["sha256"],structural_lines=sel[:55],matched_lines=len(sel))
                except (Hold,ValueError,KeyError,requests.RequestException) as e:
                    q.update(error=str(e) if isinstance(e,Hold) else type(e).__name__)
        except (Hold,requests.RequestException,ValueError,KeyError) as e:o["code_gate_error"]=str(e) if isinstance(e,Hold) else type(e).__name__
    return o
if __name__=="__main__":
    d=run()
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=True)+"\n")
