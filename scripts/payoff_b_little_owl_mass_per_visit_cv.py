"""Source-verified Little Owl visit -> estimated-delivered-mass conversion.

NOT prey-stock availability, consumed food, fitness or game-theoretic payoff.
Exploratory, prior-art bounded. Freeze:
docs/PAYOFF_B_LITTLE_OWL_MASS_PER_VISIT_PREDICTION_FREEZE_20261117.md

Each brood receives equal total training weight; heldout entire nest/brood.
All original data are retrieved from official Zenodo file links and checked
against pinned original SHA256 and manifest MD5, no locally inferred records.
"""
import argparse
import json
import math
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scripts.payoff_b_little_owl_broodday_source_admission import (
    download_original, parse_number
)

BAD_BROODS=frozenset(("KW0222012","OF0922012","PO0612012"))
REQUIRED=["temp","wind","age","number_juv.x","prov_rate2","BM2",
          "prop.day.monitored"]
FEATURE_M1=["age","temperature","wind","brood_size","hq_fraction"]
FEATURE_ORACLE=FEATURE_M1+["share_mammal","share_bird","share_insect",
                          "share_earthworms","share_other"]
MIN_ROWS=700
MIN_BROODS=45
MIN_NESTS=30
MIN_COUNTRIES=3
MIN_YEARS=10


def prepare(data):
    prey=data["Littleowl.dat.JAB.csv"]
    habitat=data["all_hab_vars.csv"]
    hq={}
    for x in habitat:
        nest=(x.get("nestID") or "").strip()
        if not nest or nest in hq:
            raise ValueError("Duplicate or blank habitat nest identifier")
        vals=[parse_number(x.get(k)) for k in (
            "Grassland area","Garden area","Hedges area","Orchard area")]
        if any(v is None or v<0 for v in vals):
            raise ValueError("Missing or negative habitat area")
        fraction=sum(vals)/151976
        if not 0<=fraction<=1:
            raise ValueError("Implausible source habitat fractional area")
        hq[nest]=fraction

    duplicate=Counter()
    keys=set()
    bad=Counter()
    for row in prey:
        k=((row.get("broodID") or "").strip(), (row.get("day") or "").strip())
        if not all(k):
            raise ValueError("No source brood day")
        if k in keys:
            duplicate[k[0]]+=1
        keys.add(k)
    if set(duplicate)!=BAD_BROODS:
        raise ValueError("Original German source inconsistent brood set drift")

    admitted=[]
    unique=set()
    for row in prey:
        brood=(row.get("broodID") or "").strip()
        nest=(row.get("nestID") or "").strip()
        day=(row.get("day") or "").strip()
        if brood in BAD_BROODS:
            bad["all_rows_in_three_conflicting_broods"]+=1
            continue
        key=(brood,day)
        if key in unique:
            raise ValueError("Unexpected duplicated source brood-day")
        unique.add(key)
        year=parse_number(row.get("Year"))
        age=parse_number(row.get("age"))
        visit=parse_number(row.get("prov_rate2"))
        mass=parse_number(row.get("BM2"))
        fraction=parse_number(row.get("prop.day.monitored"))
        chicks=parse_number(row.get("number_juv.x"))
        temp=parse_number(row.get("temp"))
        wind=parse_number(row.get("wind"))
        if year is None or age is None or not 1<=age<=30:
            bad["missing_or_outside_source_age_day_1_30"]+=1
            continue
        if any(z is None for z in (visit,mass,fraction,chicks,temp,wind)):
            bad["nonfinite_source_amount_or_context"]+=1
            continue
        if not (visit>0 and mass>0 and 0<fraction<=1 and chicks>0):
            bad["zero_or_invalid_delivery_or_chicks"]+=1
            continue
        if not nest or nest not in hq:
            bad["missing_exact_original_habitat_nest"]+=1
            continue
        country=(row.get("country") or "").strip()
        if not country:
            bad["country_unverified"]+=1
            continue
        comp=[parse_number(row.get(s)) for s in
              ("mammal","bird","insect","earthworms","other")]
        if any(s is None or s<0 for s in comp):
            bad["invalid_source_prey_composition"]+=1
            continue
        n=sum(comp)
        if n<=0:
            bad["no_source_prey_category_counts"]+=1
            continue
        # Published authors count provisioning items by category; this
        # denominator is source category TOTAL, not source visit count.
        shares=[v/n for v in comp]
        row_out={
          "broodID":brood,"nestID":nest,"year":int(year),
          "country":country,"day_id":day,"age":age,
          "temperature":temp,"wind":wind,
          "brood_size":chicks,"hq_fraction":hq[nest],
          "visits":visit,"biomass_g":mass,"mass_per_visit_g":mass/visit,
          "monitor_fraction":fraction,
          "n_category_items":n,
        }
        for col,val in zip(FEATURE_ORACLE[5:],shares):
            row_out[col]=val
        admitted.append(row_out)
    groups={key:len({r[key] for r in admitted}) for key in
            ("nestID","broodID","year","country")}
    qp=np.asarray([r["mass_per_visit_g"] for r in admitted],float)
    bybrood=Counter(r["broodID"] for r in admitted)
    source_qa={
      "source_rows":len(prey),"source_habitat_nests":len(habitat),
      "pre_source_discrepancy":{
          "ambiguous_broods":sorted(duplicate),
          "duplicate_key_counts":dict(duplicate),
          "source_quality_exclusion_whole_broods":sorted(BAD_BROODS),
      },
      "excluded_counts":dict(bad),
      "admitted_positive_delivery_brood_days":len(admitted),
      "unique_units":groups,
      "median_days_per_brood":float(np.median(list(bybrood.values()))) if bybrood else None,
      "mass_per_visit_source_estimated_g":{
          "min":float(np.min(qp)) if qp.size else None,
          "p05":float(np.percentile(qp,5)) if qp.size else None,
          "median":float(np.median(qp)) if qp.size else None,
          "p95":float(np.percentile(qp,95)) if qp.size else None,
          "max":float(np.max(qp)) if qp.size else None
      },
      "grams_not_ingested_energy":True,
      "prey_composition_is_post_delivery_oracle":True,
      "published_habitat_weather_finding_prior_art":True,
    }
    eligible=(len(admitted)>=MIN_ROWS and groups["broodID"]>=MIN_BROODS
              and groups["nestID"]>=MIN_NESTS
              and groups["country"]>=MIN_COUNTRIES
              and groups["year"]>=MIN_YEARS)
    return admitted,source_qa,eligible


def balanced_weights(rows):
    cs=Counter(r["broodID"] for r in rows)
    vals=np.asarray([1/cs[r["broodID"]] for r in rows],float)
    return vals/vals.sum()


def weighted_ridge(X,y,xt,weights,n_unique_broods):
    X=np.asarray(X,float);y=np.asarray(y,float);xt=np.asarray(xt,float)
    w=np.asarray(weights,float)
    w=w/w.sum()
    m=np.average(X,axis=0,weights=w)
    sd=np.sqrt(np.average((X-m)**2,axis=0,weights=w))
    sd[sd<1e-8]=1
    a=np.column_stack([np.ones(len(X)),(X-m)/sd])
    b=np.column_stack([np.ones(len(xt)),(xt-m)/sd])
    # Weight scales to number of unique broods, not raw day count.
    alpha=float(1.0)
    if n_unique_broods<2:
        raise ValueError("Training data have insufficient independent broods")
    ridge=np.eye(a.shape[1])*alpha
    ridge[0,0]=0
    theta=np.linalg.solve((a.T*(w*n_unique_broods))@a+ridge,
                           (a.T*(w*n_unique_broods))@y)
    return b@theta


def predict(rows_train, rows_test, name):
    w=balanced_weights(rows_train)
    y=np.asarray([r["mass_per_visit_g"] for r in rows_train],float)
    if name=="M0_constant_g_per_visit":
        q=np.full(len(rows_test),np.average(y,weights=w))
    else:
        cols=FEATURE_M1 if name=="M1_context_rate_conversion" else FEATURE_ORACLE
        x=np.asarray([[r[z] for z in cols] for r in rows_train],float)
        testx=np.asarray([[r[z] for z in cols] for r in rows_test],float)
        q=weighted_ridge(x,y,testx,w,len({r['broodID'] for r in rows_train}))
    q=np.maximum(0,q)
    v=np.asarray([r["visits"] for r in rows_test],float)
    return q*v


MODELS=["M0_constant_g_per_visit","M1_context_rate_conversion",
        "M2_post_delivery_oracle"]


def crossvalidate(rows,groupkey):
    labels=sorted({r[groupkey] for r in rows})
    model_sq={name:[] for name in MODELS}
    fold={}
    for label in labels:
        held=[r for r in rows if r[groupkey]==label]
        train=[r for r in rows if r[groupkey]!=label]
        if len({r["broodID"] for r in train})<8:
            return {"status":"NO_GO_TRAIN_BROODS_TOO_FEW",
                    "failed_fold":str(label),"n_folds":len(labels)}
        actual=np.asarray([r["biomass_g"] for r in held])
        fold[str(label)]={"n_brood_days":len(held),
                          "n_broods":len({r["broodID"] for r in held}),
                          "n_nests":len({r["nestID"] for r in held})}
        for name in MODELS:
            pred=predict(train,held,name)
            err=(actual-pred)**2
            fold[str(label)][name+"_mse"]=float(err.mean())
            model_sq[name].extend(err.tolist())
    mse={name:float(np.mean([v[name+"_mse"] for v in fold.values()]))
         for name in MODELS}
    n_improved=sum(v["M0_constant_g_per_visit_mse"]>
                   v["M1_context_rate_conversion_mse"] for v in fold.values())
    return {
        "status":"GROUPED_CV_COMPLETE","n_source_folds":len(labels),
        "n_admitted_days":len(rows),
        "equal_group_mse_g2":mse,
        "pooled_day_mse_g2":{k:float(np.mean(v)) for k,v in model_sq.items()},
        "heldout_fold_metrics":fold,
        "fraction_folds_context_improves":n_improved/len(fold),
    }


def report(rows,qa,eligible):
    out={
        "status":"PAYOFF_B_LITTLE_OWL_ORIGINAL_DELIVERED_MASS_PER_VISIT",
        "source_doi":"10.5281/zenodo.17521558",
        "paper_doi":"10.1002/ece3.72969",
        "analysis_freeze":"docs/PAYOFF_B_LITTLE_OWL_MASS_PER_VISIT_PREDICTION_FREEZE_20261117.md",
        "source_qa":qa,
        "admitted":eligible,
        "not_independent_published_biomass_habitat_finding":True,
        "no_fitness_or_information_payoff_estimated":True,
        "not_causal":True,
    }
    if not eligible:
        out["gate"]="NO_GO_SOURCE_BROODDAY_SUPPORT"
        return out
    nest=cv_nest=crossvalidate(rows,"nestID")
    brood=crossvalidate(rows,"broodID")
    country=crossvalidate(rows,"country")
    out["cv"]={"leave_one_nest_out":nest,
               "leave_one_brood_out":brood,
               "leave_one_country_out_descriptive":country}
    if nest.get("status")!="GROUPED_CV_COMPLETE" or brood.get("status")!="GROUPED_CV_COMPLETE":
        out["gate"]="HOLD_GROUPED_CV_UNAVAILABLE"
        return out
    delta_nest=nest["equal_group_mse_g2"][MODELS[0]]-nest["equal_group_mse_g2"][MODELS[1]]
    delta_brood=brood["equal_group_mse_g2"][MODELS[0]]-brood["equal_group_mse_g2"][MODELS[1]]
    fraction=nest["fraction_folds_context_improves"]
    other=[r for r in rows if r["country"]!="Germany"]
    other_nests=len({r["nestID"] for r in other})
    other_countries=len({r["country"] for r in other})
    if other_nests>=20 and other_countries>=2 and len({r["broodID"] for r in other})>=12:
        no_de=crossvalidate(other,"nestID")
        out["non_german_sensitivity"]=no_de
        de_ok=(no_de.get("status")=="GROUPED_CV_COMPLETE"
             and no_de["equal_group_mse_g2"][MODELS[0]]>
                 no_de["equal_group_mse_g2"][MODELS[1]])
    else:
        out["non_german_sensitivity"]={
          "status":"NO_GO_PRELISTED_SOURCE_PANEL_TOO_SMALL",
          "n_nests":other_nests,"n_countries":other_countries
        }
        de_ok=True # Not mandatory when admission threshold fails, documented.
    out["m0_minus_m1_nest_mse_g2"]=delta_nest
    out["m0_minus_m1_brood_mse_g2"]=delta_brood
    out["context_better_in_nest_fraction"]=fraction
    out["gate"]=("EXPLORATORY_CONTEXT_CONVERSION_INCREMENT" if
                delta_nest>0 and delta_brood>0 and fraction>=0.60 and de_ok
                else "HOLD_CONTEXT_NOT_GENERALIZABLE")
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    rows,qa,eligible=prepare(download_original())
    out=report(rows,qa,eligible)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(out,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
