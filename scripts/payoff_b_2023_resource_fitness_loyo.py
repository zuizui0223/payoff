"""Exploratory grouped-year out-of-sample prediction of recruits per brood.

Not causal. No chick-demand timing model; laying-to-peak offset is a proxy.
Resource biomass is shared within site/year, so CV holds out whole years.
"""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_filtered_descriptive_join import number

def prepare(data):
    resource={(str(r["AreaName"]).strip(),int(r["Year"])):r
              for r in data["resource"] if r.get("AreaName") and r.get("Year")}
    by=defaultdict(list)
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):continue
        area=str(r.get("Area") or "").strip()
        yr=number(r.get("YearOfBreeding"))
        if yr is None or (area,int(yr)) not in resource:continue
        species=str(r.get("Species") or "")
        if species not in ("Great Tit","Blue Tit"):continue
        res=resource[(area,int(yr))]
        lay=number(r.get("LayDateApril"));peak=number(res.get("MidDate"))
        biom=number(res.get("MaxBiom"));rec=number(r.get("NumberRecruitsAllBroodsSummed"))
        if None in (lay,peak,biom,rec) or biom<0 or rec<0:continue
        by[(area,species,int(yr))].append((lay,peak,biom,rec))
    return by
def fit_predict(x,y,xt):
    # fixed mild ridge with unpenalized intercept, features standardized on train only
    mean=x.mean(axis=0);std=x.std(axis=0)
    std[std<1e-9]=1
    a=(x-mean)/std;b=(xt-mean)/std
    A=np.column_stack([np.ones(len(a)),a]);B=np.column_stack([np.ones(len(b)),b])
    penalty=np.eye(A.shape[1])*1.0;penalty[0,0]=0
    beta=np.linalg.solve(A.T@A+penalty,A.T@y)
    return B@beta
def cv(by):
    # population/species/year mean outcomes; no pseudo-replicated broods in fitting
    groups=defaultdict(list)
    for (area,species,year),rows in by.items():
        if len(rows)<5:continue
        lay=float(np.mean([r[0] for r in rows]))
        peak=rows[0][1];biom=rows[0][2]
        recruit=float(np.mean([r[3] for r in rows]))
        groups[(area,species)].append((year,lay,peak,biom,recruit,len(rows)))
    result={}
    for (area,species),rows in sorted(groups.items()):
        if len(rows)<12:continue
        rows.sort()
        yy=np.array([r[4] for r in rows])
        lag=np.array([abs(r[1]-r[2]) for r in rows])
        biomass=np.array([math.log1p(r[3]) for r in rows])
        # no invented optimal offset; raw absolute lay/peak offset exploratory only
        feature_sets={"intercept":np.empty((len(rows),0)),
                      "timing_proxy":lag[:,None],
                      "peak_biomass":biomass[:,None],
                      "timing_plus_biomass":np.column_stack([lag,biomass])}
        errors={}
        for name,X in feature_sets.items():
            preds=[]
            for i in range(len(rows)):
                train=np.arange(len(rows))!=i
                preds.append(float(fit_predict(X[train],yy[train],X[~train])[0]))
            errors[name]=float(np.mean((yy-np.array(preds))**2))
        result[area+"|"+species]={"site_years":len(rows),
            "broods":sum(r[5] for r in rows),
            "year_range":[rows[0][0],rows[-1][0]],
            "mean_recruits_per_brood":float(yy.mean()),
            "loyo_mse":{k:round(v,7) for k,v in errors.items()},
            "delta_mse_vs_intercept":{k:round(errors["intercept"]-v,7) for k,v in errors.items()},
            "units":"mean recruits per included brood, squared",
            "interpretation":"exploratory predictive LOYO only"}
    return {"status":"ORIGINAL_DRYAD_2023_EXPLORATORY_POPULATION_SPECIES_LOYO",
        "models":result,"same_year_site_species_mean_outcome":True,
        "leave_one_site_year_out":True,
        "timing_proxy_not_chick_food_mismatch":True,
        "peak_biomass_not_integrated_exposure":True,
        "causal_effect_identified":False,
        "uncertainty_intervals_estimated":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args();result=cv(prepare(load()))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
