#!/usr/bin/env python3
"""Inspect raw source-design labels without assuming regex; no response values."""
import hashlib,io,json,sys,re
from pathlib import Path
from collections import Counter,defaultdict
import requests,openpyxl
from payoff_b_priority_compensation_tank_fit_20261125 import MD5,SHA,HEAD,PH,GROUPS
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
def run(b):
    if len(b)!=81042 or hashlib.md5(b).hexdigest()!=MD5 or hashlib.sha256(b).hexdigest()!=SHA:raise Hold("SOURCE_INTEGRITY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    try:
        it=w["Data"].iter_rows(values_only=True)
        if list(next(it))!=HEAD:raise Hold("HEADER")
        rr=[dict(zip(HEAD,r)) for r in it if any(v is not None for v in r)]
    finally:w.close()
    tanks=defaultdict(list)
    for r in rr:tanks[r["ContainerID"]].append(r)
    if len(rr)!=828 or len(tanks)!=69 or any(len(rs)!=12 for rs in tanks.values()):raise Hold("GRAIN")
    receipts=[]
    for rs in tanks.values():
        x=rs[0];p=Counter(PH.get(r["Phenology"],"?") for r in rs)
        pn=Counter(str(r["PhenN"]) for r in rs)
        pairs=Counter((str(r["Phenology"]),str(r["PhenN"])) for r in rs)
        receipts.append({"container_code":str(x["Container"]),"block":str(x["Block"]),"mix":str(x["Mix"]),"food":str(x["Food"]),
            "phenology_labels":dict(p),"phenology_numeric":dict(pn),"joint_label_codes":[{"string":k[0],"numeric":k[1],"n":v} for k,v in pairs.items()],
            "unique_larvae_slots":len({r["LarvaeN"] for r in rs}),
            "constant_assignments":all(len({r[k] for r in rs})==1 for k in ("Container","ContainerID","Block","Food","FoodN","Mix"))})
    return {"status":"SOURCE_DESIGN_LABEL_RECEIPT_ONLY","source_sha256":SHA,"rows":len(rr),"tanks":len(tanks),"records":receipts,
            "source_composition_compatible":sum(any(Counter(x["phenology_labels"])==v for v in GROUPS.values()) for x in receipts)}
if __name__=="__main__":
    with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/6328354",cap=100000)
    d=run(b);print(json.dumps(d,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
