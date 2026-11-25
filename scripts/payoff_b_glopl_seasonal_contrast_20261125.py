#!/usr/bin/env python3
"""GloPL source-context inventory and one author-confirmed secondary contrast.
No primary theta, no inferred pairing, no effects for other candidates.
"""
from __future__ import annotations
import csv, hashlib, io, json, math, re, sys
from collections import Counter,defaultdict
from pathlib import Path
from urllib.parse import unquote
import requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch, Hold
from payoff_b_gezon_glopl_source_screen_20261125 import GLOPL_URL, verify_git_blob

SHA="8c764ce03da86db0cb280e8f8f92cc0e62e2df6d85a2226e3246dc1afeb3f65f"
CER="10.1657/1523-0430(2003)035[0242:bsifva]2.0.co;2"
SP=("cerastium_alpinum","cerastium_cerastoides")
ENDPOINTS=("FS","SO","SPFR","SPFL","SPP")
NOTE="Additional_Treatment_Information"
FIELDS=("unique_number","unique_study_number","Species_Author","Species_accepted_names","Author","Year","DOI","year_of_study","population","Level_of_Supplementation","Emasculated_treatment",NOTE)
MATCH_FIELDS=("unique_study_number","Species_Author","Species_accepted_names","year_of_study","population","Level_of_Supplementation","Emasculated_treatment")
MISSING={"","na","n/a","nan","null"}
PHASE=re.compile(r"(?<![a-z])(?:early|late)(?![a-z])",re.I|re.ASCII)
def doi(x):return unquote(x.strip()).lower()
def clean(x):return " ".join(x.strip().lower().split())
def number(x):
    try:
        n=float(x)
        return n if math.isfinite(n) else None
    except (ValueError,TypeError):return None
def endpoint(r,e):
    out={}
    for arm in ("Natural","Sup"):
        v,n,sd=(number(r.get(f"{arm}_{c}_{e}")) for c in ("X","N","SD"))
        out[arm]={"mean":v,"n":n,"sd":sd}
    return out
def good_mean(v):return v is not None and v>0
def good_var(a):return a["n"] is not None and a["n"]>=2 and a["n"].is_integer() and a["sd"] is not None and a["sd"]>=0
def support(r,e):
    a=endpoint(r,e)
    return {"positive_means":all(good_mean(x["mean"]) for x in a.values()),
            "sd_n_available":all(good_var(x) for x in a.values())}
def phase(r):
    matches=list(PHASE.finditer(r[NOTE]))
    return matches[0].group(0).lower() if len(matches)==1 else None
def pairing_key(r):
    return (*[clean(r[k]) for k in MATCH_FIELDS],clean(PHASE.sub("<phase>",r[NOTE])))
def code_view(s):
    return "".join(c if ord(c)<128 else f"\\x{ord(c):02x}" for c in s)
def signed(e,l):
    if not all(0 < a["mean"] <= 1 for p in (e,l) for a in p.values() if a["mean"] is not None):
        raise Hold("SEED_OVULE_RATIO_OUT_OF_RANGE")
    if not all(good_mean(a["mean"]) for p in (e,l) for a in p.values()):
        raise Hold("MISSING_OR_ZERO_MEAN")
    def lr(p):return math.log(p["Sup"]["mean"]/p["Natural"]["mean"])
    le,ll=lr(e),lr(l)
    result={"early_lnRR":le,"late_lnRR":ll,"delta_late_minus_early":ll-le,
            "ratio_of_response_ratios":math.exp(ll-le),"early_arms":e,"late_arms":l,
            "covariance_known":False,"admitted_primary":False,
            "status":"SECONDARY_POINT_ONLY"}
    if all(good_var(a) for p in (e,l) for a in p.values()):
        def v(p):return sum(a["sd"]**2/(a["n"]*a["mean"]**2) for a in p.values())
        ve,vl=v(e),v(l); dv=ll-le
        va=ve+vl; vmax=(math.sqrt(ve)+math.sqrt(vl))**2
        result.update(status="SECONDARY_CONDITIONAL_VARIANCE_SENSITIVITY",
            early_variance_conditional=ve,late_variance_conditional=vl,
            variance_if_zero_between_period_covariance=va,
            maximum_variance_given_marginal_variances=vmax,
            normal95_if_zero_between_period_covariance=[dv-1.96*math.sqrt(va),dv+1.96*math.sqrt(va)],
            normal95_maximum_variance_sensitivity=[dv-1.96*math.sqrt(vmax),dv+1.96*math.sqrt(vmax)])
    return result
def cerastium(rows):
    out={}
    for sp in SP:
        rr=[r for r in rows if clean(r["Species_Author"]).replace(" ","_")==sp and doi(r["DOI"])==CER]
        s={"status":"HOLD","source_rows":len(rr)};out[sp]=s
        # Original paper has one low-altitude period and two high-altitude periods.
        ee=[r for r in rr if phase(r)=="early"];ll=[r for r in rr if phase(r)=="late"]
        if len(rr)!=3 or len(ee)!=1 or len(ll)!=1:
            s["error"]="SOURCE_PERIOD_STRUCTURE_NOT_UNIQUE";continue
        e,l=ee[0],ll[0]
        if pairing_key(e)!=pairing_key(l):
            s["error"]="EARLY_LATE_CONTEXT_NOT_IDENTICAL";continue
        if any(re.search(r"(?<![a-z])low(?![a-z])",r[NOTE]+" "+r["population"],re.I) for r in (e,l)):
            s["error"]="LOW_ALTITUDE_LABEL";continue
        if any(r["year_of_study"].strip().lower() not in MISSING|{"2000"} for r in (e,l)):
            s["error"]="SOURCE_FIELD_YEAR_MISMATCH";continue
        try:
            s.update(signed(endpoint(e,"SO"),endpoint(l,"SO")),
                     source_row_ids=[e["unique_number"],l["unique_number"]],
                     source_note_labels=[e[NOTE],l[NOTE]],
                     period_semantics="unique two high-elevation periods in original 2000 field design; third row outside pair",
                     covariance_limit="within-period separate plants per article; cross-period reuse unknown; compiled SD/N assumed correct; not exact CI")
        except Hold as exc:s["error"]=str(exc)
    return out
def run(b,frame):
    verify_git_blob(b)
    if hashlib.sha256(b).hexdigest()!=SHA:raise Hold("PINNED_SHA256_MISMATCH")
    t=b.decode("latin-1")
    r=csv.DictReader(io.StringIO(t),delimiter=",")
    if not set(FIELDS).issubset(r.fieldnames or []):raise Hold("SCHEMA")
    rows=list(r)
    if len(rows)!=2969 or len({x["unique_number"] for x in rows})!=len(rows) or any(None in x or any(v is None for v in x.values()) for x in rows):
        raise Hold("SOURCE_ROW_ID_OR_SHAPE")
    ds={doi(x["doi"]) for x in frame["context_only_publications"] if doi(x["doi"])!="10.1674/0003-0031-168.1.93"}
    if len(ds)!=16 or CER not in ds:raise Hold("SOURCE_FRAME_CHANGED")
    sel=[x for x in rows if doi(x["DOI"]) in ds]
    papers={}
    for k in sorted(ds):
        rr=[x for x in sel if doi(x["DOI"])==k]
        papers[k]={"n_rows":len(rr),"n_source_study_ids":len({x["unique_study_number"] for x in rr}),
            "n_early_late_notes":sum(phase(x) is not None for x in rr),
            "records":[{"metadata":{c:code_view(x[c]) for c in FIELDS},
                        "endpoint_support":{e:support(x,e) for e in ENDPOINTS}} for x in rr]}
    return {"status":"SOURCE_INVENTORY_AND_CONFIRMED_SECONDARY_ONLY","source_sha256":SHA,
            "source_rows":len(rows),"candidate_publications":len(papers),
            "all_candidate_publication_rows":len(sel),"candidate_inventory":papers,
            "cerastium":cerastium(sel),"primary_theta_added":0}
def self_test():
    e={"Natural":{"mean":.2,"n":12.,"sd":.1},"Sup":{"mean":.4,"n":12.,"sd":.1}}
    l={"Natural":{"mean":.4,"n":12.,"sd":.1},"Sup":{"mean":.4,"n":12.,"sd":.1}}
    x=signed(e,l)
    assert abs(x["delta_late_minus_early"]+math.log(2))<1e-12
    assert x["maximum_variance_given_marginal_variances"]>=x["variance_if_zero_between_period_covariance"]
    l["Natural"]["mean"]=0
    try:signed(e,l)
    except Hold:pass
    else:raise AssertionError("zero not rejected")
    print("SYNTHETIC_CONTRAST_CHECKS_PASS",flush=True)
if __name__=="__main__":
    self_test()
    f=json.loads(Path("data/payoff_b_glopl_source_frame_result_20261125.json").read_text())
    with requests.Session() as s:
        out=run(fetch(s,GLOPL_URL,cap=6_000_000),f)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2,ensure_ascii=True)+"\n")
    # Compact receipt: all exact source context rows (not outcome values) for review.
    summary={k:v for k,v in out.items() if k!="candidate_inventory"}
    summary["inventory_review"]={k:{"n_rows":v["n_rows"],"n_source_study_ids":v["n_source_study_ids"],
        "records":[{"id":x["metadata"]["unique_number"],"study":x["metadata"]["unique_study_number"],"species":x["metadata"]["Species_Author"],"year":x["metadata"]["year_of_study"],"pop":x["metadata"]["population"],"supp":x["metadata"]["Level_of_Supplementation"],"emasculated":x["metadata"]["Emasculated_treatment"],"note":x["metadata"][NOTE],"available":[e for e,y in x["endpoint_support"].items() if y["positive_means"]],"sd_n":[e for e,y in x["endpoint_support"].items() if y["sd_n_available"]]} for x in v["records"]]} for k,v in out["candidate_inventory"].items()}
    print(json.dumps(summary,ensure_ascii=True,separators=(",",":")),flush=True)
