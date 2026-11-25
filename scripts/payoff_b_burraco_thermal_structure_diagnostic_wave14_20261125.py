#!/usr/bin/env python3
"""Diagnose source columns and assigned-slot identities, without fitting."""
import hashlib,io,json,sys,itertools
from collections import Counter,defaultdict
from pathlib import Path
import openpyxl,requests
import payoff_b_burraco_thermal_family_fit_wave14_20261125 as core
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

def audit(b):
    if len(b)!=87598 or hashlib.md5(b).hexdigest()!=core.MD5 or hashlib.sha256(b).hexdigest()!=core.SHA:raise Hold("SOURCE_INTEGRITY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    try:r=[list(x) for x in w["Sheet1"].iter_rows(values_only=True) if any(v is not None for v in x)]
    finally:w.close()
    if r[2][:17]!=core.HEAD or len(r[3:])!=787:raise Hold("SOURCE_GRAIN")
    rr=[dict(zip(core.HEAD,a[:17])) for a in r[3:]]
    extra=[]
    for j in range(17,max(map(len,r))):
        vals=[a[j] for a in r[3:] if len(a)>j and a[j] is not None]
        txt=Counter(str(x).strip() for x in vals if isinstance(x,str))
        extra.append({"column_1based":j+1,"header":r[2][j],"nonempty":len(vals),"value_types":dict(Counter(type(x).__name__ for x in vals)),
                      "text_labels":dict(txt) if len(txt)<=15 else {"distinct_text":len(txt)},"numeric_count":sum(isinstance(x,(float,int)) for x in vals)})
    keys=Counter();vials=defaultdict(list);families=set();codes=defaultdict(lambda:defaultdict(set));exceptions=Counter()
    for x in rr:
        try:
            f=str(x["Family"]);d=core.PH[x["Phenology"]];t=core.ROOM[x["Temp"]];q=core.FOOD[x["Food"]];i=core.slot(x["LarvaeN"])
            k=(f,d,t,q,i)
        except (Hold,KeyError,ValueError,TypeError) as e:
            exceptions[type(e).__name__]+=1;continue
        for col,sem in (("FamN",f),("PCode",d),("PhenN",d),("TCode",t),("TempN",t),("FCode",q),("FoodN",q)):
            codes[col][str(x[col])].add(str(sem))
        keys[k]+=1;vials[str(x["Vial"])].append(k);families.add(f)
    expected={(f,*c,i) for f in families for c in core.CELLS for i in range(1,7)}
    dup={k:[list(a) for a in v] for k,v in vials.items() if len(v)>1}
    return {"status":"STRUCTURE_DIAGNOSTIC_ONLY","source_sha256":core.SHA,"n_rows":len(rr),"additional_columns":extra,
            "families":len(families),"unique_slot_keys":len(keys),"duplicate_slot_keys":[[list(k),n] for k,n in keys.items() if n>1],
            "missing_planned_slots":len(expected-set(keys)),"unexpected_keys":len(set(keys)-expected),"duplicate_vial_labels":dup,
            "unresolved_design_rows":dict(exceptions),"code_crosswalk":{k:{a:sorted(b) for a,b in v.items()} for k,v in codes.items()}}
if __name__=="__main__":
    with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/25051406",cap=100000)
    d=audit(b)
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
