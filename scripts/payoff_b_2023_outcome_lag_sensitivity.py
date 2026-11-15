"""Original Dryad 2023 sensitivity: fledglings vs recruits; signed vs absolute timing.

All features exploratory. Laying-to-peak offset is not the chick-demand mismatch.
Year is the replication unit, not the number of nests.
"""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_filtered_descriptive_join import number
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict

def prepare(data):
    resources={}
    for r in data["resource"]:
        if r.get("AreaName") and r.get("Year") is not None:
            key=(str(r["AreaName"]).strip(),int(r["Year"]))
            if key in resources:raise ValueError("Duplicate site-year resource")
            resources[key]=r
    groups=defaultdict(list)
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):continue
        area=str(r.get("Area") or "").strip()
        year=number(r.get("YearOfBreeding"))
        if year is None or (area,int(year)) not in resources:continue
        species=str(r.get("Species") or "")
        if species not in ("Great Tit","Blue Tit"):continue
        res=resources[(area,int(year))]
        lay=number(r.get("LayDateApril"))
        peak=number(res.get("MidDate"))
        biomass=number(res.get("MaxBiom"))
        fledged=number(r.get("NumberFledged"))
        recruits=number(r.get("NumberRecruitsAllBroodsSummed"))
        if None in (lay,peak,biomass) or biomass<0:continue
        groups[(area,species,int(year))].append(
            {"lay":lay,"peak":peak,"biomass":biomass,
             "fledged":fledged,"recruits":recruits})
    return groups

def audit(groups):
    result={}
    for outcome in ("fledged","recruits"):
        by=defaultdict(list)
        for (area,species,year),records in groups.items():
            valid=[r for r in records if r[outcome] is not None and r[outcome]>=0]
            if len(valid)<5:continue
            by[(area,species)].append({
                "year":year,"n":len(valid),
                "lay":float(np.mean([r["lay"] for r in valid])),
                "peak":valid[0]["peak"],"biomass":valid[0]["biomass"],
                "y":float(np.mean([r[outcome] for r in valid]))})
        models={}
        for (area,species),rows in sorted(by.items()):
            if len(rows)<12:continue
            rows.sort(key=lambda r:r["year"])
            yy=np.array([r["y"] for r in rows])
            signed=np.array([r["lay"]-r["peak"] for r in rows])
            absolute=np.abs(signed)
            biomass=np.log1p([r["biomass"] for r in rows])
            Xs={"intercept":np.empty((len(rows),0)),
                "signed_offset":signed[:,None],
                "absolute_offset":absolute[:,None],
                "peak_biomass":biomass[:,None],
                "signed_plus_biomass":np.column_stack([signed,biomass]),
                "absolute_plus_biomass":np.column_stack([absolute,biomass])}
            errors={}
            for name,X in Xs.items():
                predictions=[]
                for i in range(len(rows)):
                    train=np.arange(len(rows))!=i
                    predictions.append(float(fit_predict(X[train],yy[train],X[~train])[0]))
                errors[name]=float(np.mean((yy-np.array(predictions))**2))
            baseline=errors["intercept"]
            models[area+"|"+species]={
                "years":len(rows),"broods":sum(r["n"] for r in rows),
                "mse":{k:round(v,7) for k,v in errors.items()},
                "delta_vs_intercept":{k:round(baseline-v,7) for k,v in errors.items()},
                "best_exploratory_model":min(errors,key=errors.get)}
        result[outcome]=models
    return {"status":"ORIGINAL_DRYAD_2023_OUTCOME_LAG_SENSITIVITY_LOYO",
            "results":result,"source_original_sha256_checked":True,
            "site_year_as_replication_unit":True,
            "lay_date_peak_offset_not_chick_demand_mismatch":True,
            "lag_date_units_and_original_definition_require_readme_review":True,
            "posthoc_model_comparison_no_confirmatory_claim":True,
            "causal_effect_identified":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=audit(prepare(load()))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
