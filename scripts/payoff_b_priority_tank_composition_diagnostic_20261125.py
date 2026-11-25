#!/usr/bin/env python3
"""Design-only diagnosis: no outcome fits or repaired individual labels."""
import hashlib,io,json,sys,re
from pathlib import Path
from collections import Counter,defaultdict
import requests,openpyxl
from payoff_b_priority_compensation_tank_fit_20261125 import MD5,SHA,HEAD,PH,GROUPS
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
def audit(b):
    if len(b)!=81042 or hashlib.md5(b).hexdigest()!=MD5 or hashlib.sha256(b).hexdigest()!=SHA:raise Hold("SOURCE_INTEGRITY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    it=w["Data"].iter_rows(values_only=True)
    if list(next(it))!=HEAD:raise Hold("HEADER")
    rr=[dict(zip(HEAD,r)) for r in it if any(v is not None for v in r)]
    w.close()
    tanks=defaultdict(list)
    for r in rr:tanks[r["ContainerID"]].append(r)
    if len(rr)!=828 or len(tanks)!=69 or any(len(rs)!=12 for rs in tanks.values()):raise Hold("GRAIN")
    out={"status":"DESIGN_DIAGNOSTIC_ONLY","source_sha256":SHA,"rows":len(rr),"tanks":len(tanks),"groups":{}}
    bad=[]
    for rs in tanks.values():
        x=rs[0]
        if any(len({r[k] for r in rs})!=1 for k in ("Container","ContainerID","Block","Mix","Food","FoodN")):raise Hold("TANK_CONSTANTS")
        m=re.match(r"^(NN|DD|EE|ND|NE)(H|L)",str(x["Container"]).strip(),re.I)
        if not m:raise Hold("UNRESOLVED_TANK_CODE")
        raw,food=m.group(1).upper(),m.group(2).upper()
        g=raw[0] if raw[0]==raw[1] else raw
        p=Counter(PH.get(r["Phenology"],"?") for r in rs)
        pn=Counter(str(r["PhenN"]) for r in rs)
        # Numerical source codes are a distinct recorded field, not imputed from strings.
        nomatch=sum(1 for r in rs if PH.get(r["Phenology"])!={"1":"N","2":"D","3":"E"}.get(str(r["PhenN"])))
        assignment_ok=(str(x["Mix"])==("2" if len(g)>1 else "1") and x["Food"]==("High" if food=="H" else "Low"))
        good=p==GROUPS[g] and assignment_ok and nomatch==0
        k=food+"_"+g
        z=out["groups"].setdefault(k,{"all_tanks":0,"compatible_tanks":0,"incompatible_tanks":0,"compatible_blocks":{},"compositions":{},"missing_duration":0,"missing_mass":0})
        z["all_tanks"]+=1
        z["compatible_tanks" if good else "incompatible_tanks"]+=1
        if good:z["compatible_blocks"][str(x["Block"])]=z["compatible_blocks"].get(str(x["Block"]),0)+1
        pk=json.dumps(dict(sorted(p.items())),sort_keys=True);z["compositions"][pk]=z["compositions"].get(pk,0)+1
        z["missing_duration"]+=sum(r["LarvalPeriod"] is None for r in rs)
        z["missing_mass"]+=sum(r["Mass"] is None for r in rs)
        if not good:bad.append({"group":k,"block":str(x["Block"]),"string_counts":dict(p),"numeric_counts":dict(pn),"phenology_code_disagreements":nomatch,"assignment_ok":assignment_ok})
    out["incompatible_tanks"]=bad
    out["compatible_total"]=sum(v["compatible_tanks"] for v in out["groups"].values())
    out["preliminary_support_all_cells_ge4"]=len(out["groups"])==10 and min(v["compatible_tanks"] for v in out["groups"].values())>=4
    return out
if __name__=="__main__":
    with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/6328354",cap=100000)
    try:d=audit(b)
    except (Hold,ValueError,KeyError) as e:d={"status":"HOLD","reason":str(e)}
    print(json.dumps(d,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
