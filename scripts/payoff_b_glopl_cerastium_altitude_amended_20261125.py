#!/usr/bin/env python3
"""Explicit altitude amendment, restricted to the four pinned source rows."""
import csv,hashlib,io,json,sys
from pathlib import Path
import requests
import payoff_b_glopl_seasonal_contrast_20261125 as c
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

PAIRS={"cerastium_alpinum":("1072","1073","1074"),"cerastium_cerastoides":("1075","1076","1077")}
def extract(b):
    c.verify_git_blob(b)
    if hashlib.sha256(b).hexdigest()!=c.SHA:raise Hold("SOURCE_SHA_MISMATCH")
    rows=list(csv.DictReader(io.StringIO(b.decode("latin-1"))))
    byid={r["unique_number"]:r for r in rows}
    if len(rows)!=2969 or len(byid)!=2969:raise Hold("SOURCE_ROW_ID_MISMATCH")
    out={"status":"SECONDARY_CERASTIUM_ONLY","source_sha256":c.SHA,"species":{},"primary_theta_added":0}
    for sp,(lowid,eid,lid) in PAIRS.items():
        z=out["species"][sp]={"status":"HOLD"}
        try:
            low,e,l=(byid[k] for k in (lowid,eid,lid))
            rset=[r for r in rows if c.doi(r["DOI"])==c.CER and c.clean(r["Species_Author"]).replace(" ","_")==sp]
            if {r["unique_number"] for r in rset}!={lowid,eid,lid}:raise Hold("SOURCE_SPECIES_CONTEXT_CHANGED")
            for r,pop,note in ((low,"1","low-early"),(e,"2","high-early"),(l,"2","high-late")):
                if r["population"]!=pop or c.clean(r[c.NOTE])!=note or r["Level_of_Supplementation"]!="flower" or r["Emasculated_treatment"]!="no":raise Hold("SOURCE_CONTEXT_CHANGED")
            if c.pairing_key(e)!=c.pairing_key(l):raise Hold("EARLY_LATE_CONTEXT_NOT_IDENTICAL")
            if any(r["year_of_study"].strip().lower() not in c.MISSING|{"2000"} for r in (e,l)):raise Hold("YEAR")
            z.update(c.signed(c.endpoint(e,"SO"),c.endpoint(l,"SO")),source_row_ids=[eid,lid],
                     excluded_low_altitude_row=lowid,period="high elevation 2000, early versus late",
                     independence_limit="separate plants within period per paper; repeated plants across periods not ruled out; conditional SD/N variance")
        except (Hold,KeyError,ValueError) as ex:z["error"]=str(ex)
    return out

if __name__=="__main__":
    c.self_test()
    with requests.Session() as s:out=extract(fetch(s,c.GLOPL_URL,cap=6_000_000))
    print(json.dumps(out,indent=2),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2)+"\n")
