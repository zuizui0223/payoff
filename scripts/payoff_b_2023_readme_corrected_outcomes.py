"""README-corrected fitness endpoints, year-held-out exploratory validation.

Source: original Dryad 2023 README, SHA256 7aa6f4c1d0bb440a73b2c31c70ff5f50bc3f807fc211876a05f788fd77ee18e9
Fledgling estimate = NumberFledged + 0.5 * NumberFledgedDeviation.
Recruits are ALL broods in breeding year, not first-clutch-only.
No fixed chick-demand timing or causal inference.
"""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_filtered_descriptive_join import number
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict

def panel(data):
    resource={}
    for r in data["resource"]:
        if r.get("AreaName") is None or r.get("Year") is None:continue
        key=(str(r["AreaName"]).strip(),int(r["Year"]))
        if key in resource:raise ValueError("Duplicate site/year resource")
        resource[key]=r
    by=defaultdict(list)
    missing=defaultdict(int)
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):continue
        area=str(r.get("Area") or "").strip()
        year=number(r.get("YearOfBreeding"))
        if year is None or (area,int(year)) not in resource:continue
        species=str(r.get("Species") or "")
        if species not in ("Great Tit","Blue Tit"):continue
        res=resource[(area,int(year))]
        lay=number(r.get("LayDateApril"));peak=number(res.get("MidDate"))
        biomass=number(res.get("MaxBiom"))
        fledged=number(r.get("NumberFledged"))
        deviation=number(r.get("NumberFledgedDeviation"))
        recruits=number(r.get("NumberRecruitsAllBroodsSummed"))
        if None in (lay,peak,biomass) or biomass<0:continue
        corrected=None if fledged is None or deviation is None else fledged+0.5*deviation
        if corrected is None:missing["missing_corrected_fledged_components"]+=1
        if recruits is None:missing["missing_recruits"]+=1
        by[(area,species,int(year))].append((lay,peak,biomass,fledged,corrected,recruits))
    return by,dict(missing)

def loyo(by):
    outcomes={"fledged_raw":3,"fledged_readme_corrected":4,"recruits_all_broods":5}
    out={}
    for label,idx in outcomes.items():
        groups=defaultdict(list)
        for (area,species,year),records in by.items():
            rows=[r for r in records if r[idx] is not None and r[idx]>=0]
            if len(rows)<5:continue
            groups[(area,species)].append((year,len(rows),
                float(np.mean([r[0] for r in rows])),rows[0][1],rows[0][2],
                float(np.mean([r[idx] for r in rows]))))
        models={}
        for (area,species),rows in sorted(groups.items()):
            if len(rows)<12:continue
            rows.sort()
            y=np.array([r[5] for r in rows])
            lag=np.array([abs(r[2]-r[3]) for r in rows])
            biomass=np.log1p(np.array([r[4] for r in rows]))
            xs={"intercept":np.empty((len(rows),0)),
                "timing_proxy":lag[:,None],
                "peak_biomass":biomass[:,None],
                "timing_plus_biomass":np.column_stack((lag,biomass))}
            mse={}
            for name,X in xs.items():
                pred=[]
                for i in range(len(rows)):
                    train=np.arange(len(rows))!=i
                    pred.append(float(fit_predict(X[train],y[train],X[~train])[0]))
                mse[name]=float(np.mean((y-np.array(pred))**2))
            models[area+"|"+species]={"site_years":len(rows),
                "records":sum(r[1] for r in rows),
                "mean_outcome":round(float(y.mean()),6),
                "loyo_mse":{k:round(v,7) for k,v in mse.items()},
                "delta_mse_vs_intercept":{k:round(mse["intercept"]-v,7) for k,v in mse.items()}}
        out[label]=models
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    by,missing=panel(load())
    result={"status":"ORIGINAL_DRYAD_2023_README_CORRECTED_OUTCOMES_LOYO",
        "readme_sha256":"7aa6f4c1d0bb440a73b2c31c70ff5f50bc3f807fc211876a05f788fd77ee18e9",
        "lay_and_peak_both_april_days":True,
        "recruits_count_all_broods_not_first_only":True,
        "chick_demand_window_not_observed":True,
        "site_year_replication_not_individual_broods":True,
        "missing":missing,"outcomes":loyo(by),
        "causal_effect_identified":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
