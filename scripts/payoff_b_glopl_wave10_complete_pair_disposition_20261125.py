#!/usr/bin/env python3
"""Wave 10: audit all 28 candidate dispositions; no weighted meta-analysis."""
import csv,hashlib,io,json,math,sys
from pathlib import Path
from collections import Counter,defaultdict
import requests
import payoff_b_glopl_seasonal_contrast_20261125 as c
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

# Table 3, Stanton 1987: control and augmented, early and late; printed flower N.
# Rates are rounded source summaries, not reconstructed individual outcomes.
TABLE={
"120":("white",(.73,80),(.62,42),(.24,38),(.21,24)),
"122":("yellow",(.60,35),(.58,24),(.44,50),(.41,29)),
"124":("pink",(.80,64),(.72,32),(.49,45),(.70,23)),
"126":("bronze",(.75,48),(.81,26),(.40,45),(.44,103))}
PROVISIONAL={
"158":("FS","population_season"),"161":("FS","population_season"),
"19":("SO","population_season"),"25":("SO","population_season"),
"478":("FS","within_plant_sequence"),"479":("FS","within_plant_sequence"),"483":("FS","within_plant_sequence"),
"48":("SPFL","season_context_unverified"),
"414":("SPFR","within_plant_sequence"),"415":("SPFR","within_plant_sequence")}
PRIOR={"1073":"PRIOR_CONDITIONAL","1076":"PRIOR_CONDITIONAL",
"988":"PRIOR_POINT_ONLY","991":"PRIOR_POINT_ONLY","994":"PRIOR_POINT_ONLY","997":"PRIOR_POINT_ONLY","1000":"PRIOR_POINT_ONLY",
"1003":"QUARANTINE_CONFLICTING_O3",
"2192":"QUARANTINE_DUPLICATE_SPECIES","2194":"QUARANTINE_DUPLICATE_SPECIES"}
HOLDS={"1879":"HOLD_EARLY_VS_PEAK","706":"HOLD_OTC_DESIGN","708":"HOLD_OTC_DESIGN","90":"HOLD_DISEASE_AND_TREATMENT_CONTEXT"}

def contrast(a,b,d,e):
    # early natural, early supplied, late natural, late supplied
    if not all(math.isfinite(x) and x>0 for x in (a,b,d,e)):raise Hold("NONPOSITIVE_MEANS")
    early=math.log(b/a);late=math.log(e/d)
    A=math.log(e/b);B=math.log(d/a)
    if not math.isclose(late-early,A-B,abs_tol=1e-12):raise Hold("IDENTITY")
    return {"early_lnRR":early,"late_lnRR":late,"late_minus_early_lnRR":late-early,
            "supplemented_performance_log_change":A,"natural_performance_log_change":B,
            "supplemented_relative_change":math.expm1(A),"natural_relative_change":math.expm1(B),
            "supplemented_point_decline":A<0}

def extract(rows,inventory):
    by={r["unique_number"]:r for r in rows}
    if len(rows)!=2969 or len(by)!=2969:raise Hold("SOURCE_IDS")
    pairs=inventory["exact_label_pair_screen"]["pairs"]
    expected=set(TABLE)|set(PROVISIONAL)|set(PRIOR)|set(HOLDS)
    if len(pairs)!=28 or {x["early_row"] for x in pairs}!=expected or len(expected)!=28:raise Hold("PAIR_FRAME_CHANGED")
    out=[]
    for p in pairs:
        eid,lid=p["early_row"],p["late_row"];e,l=by[eid],by[lid]
        z={**p,"primary_theta_eligible":False,"variance_status":"HOLD_NOT_VERIFIED"}
        out.append(z)
        for r,note in ((e,p["early_note"]),(l,p["late_note"])):
            if (c.doi(r["DOI"]),r["Species_Author"],r["population"],r["year_of_study"],r[c.NOTE])!=(p["doi"],p["species"],p["population"],p["year"],note):raise Hold("PINNED_CONTEXT")
        if c.pairing_key(e)!=c.pairing_key(l):raise Hold("PAIR_CONTEXT")
        if eid in PRIOR:z["disposition"]=PRIOR[eid];continue
        if eid in HOLDS:z["disposition"]=HOLDS[eid];continue
        endpoint,stratum=("FS","population_season") if eid in TABLE else PROVISIONAL[eid]
        if endpoint not in p["common_positive_mean_endpoints"]:raise Hold("ENDPOINT_CONTEXT")
        ea,la=c.endpoint(e,endpoint),c.endpoint(l,endpoint)
        aa=[ea["Natural"],ea["Sup"],la["Natural"],la["Sup"]]
        means=[x["mean"] for x in aa]
        z.update(endpoint=endpoint,stratum=stratum,compiled_early=ea,compiled_late=la)
        if not all(x is not None and x>0 for x in means) or (endpoint in ("FS","SO") and any(x>1 for x in means)):
            z["disposition"]="HOLD_INVALID_MEANS";continue
        if eid in TABLE:
            morph,*printed=TABLE[eid]
            source_means=[x[0] for x in printed];source_n=[x[1] for x in printed]
            checks=[abs(a["mean"]-m)<=.0051 and a["n"]==n for a,m,n in zip(aa,source_means,source_n)]
            z.update(morph=morph,source_table3_rounded_means=source_means,source_table3_flower_n=source_n,
                     source_crosscheck_cells=checks,source_table3_contrast=contrast(*source_means))
            if not all(checks):
                z["disposition"]="HOLD_COMPILED_SOURCE_MISMATCH";continue
            z["disposition"]="TABLE_CROSSCHECKED_SECONDARY_POINT_ONLY"
            z["variance_status"]="HOLD_SHARED_PLANT_AND_REPEAT_FLOWER_UNITS"
        else:
            z["disposition"]="ABSTRACT_CONSISTENT_COMPILED_PROVISIONAL_POINT_ONLY"
        z["compiled_contrast"]=contrast(*means)
    return out

def summarize(records):
    counts=Counter(x["disposition"] for x in records)
    groups=defaultdict(list)
    for r in records:
        if "compiled_contrast" in r:groups[r["doi"]].append(r)
    papers={}
    for doi,g in groups.items():
        v=[x["compiled_contrast"] for x in g]
        papers[doi]={"pairs":len(g),"status":sorted(set(x["disposition"] for x in g)),
            "stratum":sorted(set(x["stratum"] for x in g)),
            "supplemented_declines":sum(x["supplemented_point_decline"] for x in v),
            "delta_positive":sum(x["late_minus_early_lnRR"]>0 for x in v),
            "delta_negative":sum(x["late_minus_early_lnRR"]<0 for x in v),
            "delta_range":[min(x["late_minus_early_lnRR"] for x in v),max(x["late_minus_early_lnRR"] for x in v)]}
    return {"disposition_counts":dict(counts),"source_table_crosschecked_new_pairs":counts["TABLE_CROSSCHECKED_SECONDARY_POINT_ONLY"],
        "provisional_new_pairs":counts["ABSTRACT_CONSISTENT_COMPILED_PROVISIONAL_POINT_ONLY"],"paper_level_descriptive":papers}

def self_test():
    a=contrast(.2,.4,.4,.4)
    assert math.isclose(a["late_minus_early_lnRR"],-math.log(2))
    assert a["supplemented_relative_change"]==0
    assert math.isclose(a["natural_relative_change"],1)
    try:contrast(0,1,1,1)
    except Hold:pass
    else:raise AssertionError("zero accepted")
    print("SYNTHETIC_CONTRAST_IDENTITY_CHECKS_PASS",flush=True)

if __name__=="__main__":
    self_test()
    inv=json.loads(Path("data/payoff_b_glopl_seasonal_inventory_initial_20261125.json").read_text())
    with requests.Session() as s:b=fetch(s,c.GLOPL_URL,cap=6_000_000)
    c.verify_git_blob(b)
    if hashlib.sha256(b).hexdigest()!=c.SHA:raise Hold("PINNED_SHA256")
    rows=list(csv.DictReader(io.StringIO(b.decode("latin-1"))))
    records=extract(rows,inv)
    d={"status":"COMPLETE_CANDIDATE_DISPOSITION_SECONDARY_ONLY","source_sha256":c.SHA,
       "source_rows":len(rows),"candidate_pairs":len(records),"records":records,"summary":summarize(records),
       "stanton_published_tests":{"table":3,"time_chi2":44.79,"time_df":1,"time_p":.0001,
            "treatment_chi2":.01,"treatment_df":1,"treatment_p":.9271,
            "time_treatment_chi2":.92,"time_treatment_df":1,"time_treatment_p":.3387,
            "color_time_treatment_chi2":2.37,"color_time_treatment_df":3,"color_time_treatment_p":.4992,
            "note":"As printed original contingency analysis; repeated plants and branch allocation preclude naive independent-flower reanalysis."},
       "primary_theta_added":0,"meta_pooled":False}
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
