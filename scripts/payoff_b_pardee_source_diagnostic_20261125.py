#!/usr/bin/env python3
"""Diagnose frozen admission failures without opening any held model coefficient."""
import csv,io,json,sys,math
from collections import defaultdict,Counter
from pathlib import Path
import requests
from payoff_b_pardee_snow_pollen_contrast_20261125 import verified,N,MISSING

def diagnostics(b,sp):
    reader=csv.DictReader(io.StringIO(b.decode("utf-8-sig")))
    rows=list(reader);keys=defaultdict(list);invalid=Counter();mis=0;noncanonical=0
    for row in rows:
        k=(row["Plot"].strip(),row["Plant_num"].strip())
        keys[k].append(row)
        code=row["Pollen_supplemented"].strip();pid=k[1]
        if pid not in [str(i) for i in range(1,9)]:noncanonical+=1
        elif code in ("NP","AP") and code != ("NP" if int(pid)<=4 else "AP"):mis+=1
        token=row["Total_seeds"].strip()
        if token.lower() in MISSING:continue
        try:
            v=float(token)
            if not math.isfinite(v) or v<0 or v!=int(v):invalid["nonfinite_negative_or_noninteger"]+=1
        except ValueError:
            # No raw numeric outcome or IDs. Describe unparseable token categories.
            if all(not c.isdigit() for c in token):
                invalid["nonnumeric_token:"+token[:40]]+=1
            elif "," in token:
                invalid["numeric_token_with_comma"]+=1
            else:invalid["other_unparseable_numeric_token"]+=1
    dup=[r for r in keys.values() if len(r)>1]
    diffs=Counter()
    for rr in dup:
        for col in reader.fieldnames:
            if len({r[col] for r in rr})>1:diffs[col]+=1
    return {"rows":len(rows),"unique_plot_plant_keys":len(keys),"duplicate_key_groups":len(dup),
        "duplicate_rows_above_unique_key":sum(len(rr)-1 for rr in dup),
        "identical_duplicate_groups":sum(len({tuple(r.items()) for r in rr})==1 for rr in dup),
        "differing_fields_in_duplicate_groups":dict(diffs),"invalid_seed_token_categories":dict(invalid),
        "noncanonical_plant_number_rows":noncanonical,"pollen_assignment_mismatch_rows":mis}
def run():
    out={"status":"DIAGNOSTIC_ONLY_NO_MODEL","source_doi":"10.5061/dryad.kd1r166","species":{}}
    with requests.Session() as s:
        for sp in N:
            try:out["species"][sp]=diagnostics(verified(s,sp+"_SeedSet.csv"),sp)
            except Exception as e:out["species"][sp]={"status":"HOLD","error":type(e).__name__}
    print(json.dumps(out,indent=2),flush=True);return out
if __name__=="__main__":
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(run(),indent=2)+"\n")
