"""PAYOFF-B: test incremental out-of-year fitness prediction by timing gap.

Exploratory only: gap is caterpillar peak minus first egg, not chick food demand.
KNMI station is a proxy; temperature is not site-measured. Site/year is unit.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import numpy as np
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_knmi_temperature_phenology import weather
from scripts.payoff_b_2023_filtered_descriptive_join import number
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict

def build(data,temps):
    resource={}
    for r in data["resource"]:
        if r.get("AreaName") is None or r.get("Year") is None:continue
        k=(str(r["AreaName"]).strip(),int(r["Year"]))
        if k in resource:raise ValueError("duplicate resource site/year")
        resource[k]=r
    rows=defaultdict(list)
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):continue
        site=str(r.get("Area") or "").strip()
        yr=number(r.get("YearOfBreeding"))
        if yr is None or (site,int(yr)) not in resource:continue
        species=str(r.get("Species") or "")
        if species not in ("Great Tit","Blue Tit"):continue
        station="deKooy" if site=="Vlieland" else "deBilt"
        temp=temps[station].get(int(yr))
        res=resource[(site,int(yr))]
        lay=number(r.get("LayDateApril"))
        peak=number(res.get("MidDate"))
        biom=number(res.get("MaxBiom"))
        fledged=number(r.get("NumberFledged"))
        deviation=number(r.get("NumberFledgedDeviation"))
        recruits=number(r.get("NumberRecruitsAllBroodsSummed"))
        if None in (temp,lay,peak,biom) or biom<0:continue
        corrected=None if fledged is None or deviation is None else fledged+0.5*deviation
        rows[(site,species,int(yr))].append((temp,lay,peak,biom,corrected,recruits))
    return rows

def evaluate(by):
    results={}
    for endpoint,idx in (("corrected_fledged_first_brood",4),
                         ("recruits_all_broods",5)):
        groups=defaultdict(list)
        for (site,species,year),records in by.items():
            valid=[r for r in records if r[idx] is not None and r[idx]>=0]
            if len(valid)<5:continue
            groups[(site,species)].append((year,len(valid),
                valid[0][0],float(np.mean([r[1] for r in valid])),
                valid[0][2],valid[0][3],float(np.mean([r[idx] for r in valid]))))
        output={}
        for (site,species),rs in sorted(groups.items()):
            if len(rs)<12:continue
            rs.sort()
            y=np.asarray([r[6] for r in rs])
            temp=np.asarray([r[2] for r in rs])
            gap=np.asarray([r[4]-r[3] for r in rs])
            biomass=np.log1p(np.asarray([r[5] for r in rs]))
            Xs={"intercept":np.empty((len(rs),0)),
                "temperature":temp[:,None],
                "temperature_plus_gap":np.column_stack((temp,gap)),
                "temperature_plus_biomass":np.column_stack((temp,biomass)),
                "temperature_plus_gap_plus_biomass":np.column_stack((temp,gap,biomass))}
            errors={}
            for name,X in Xs.items():
                pred=[]
                for i in range(len(rs)):
                    train=np.arange(len(rs))!=i
                    pred.append(float(fit_predict(X[train],y[train],X[~train])[0]))
                errors[name]=float(np.mean((y-np.array(pred))**2))
            base=errors["temperature"]
            output[site+"|"+species]={"years":len(rs),"records":sum(r[1] for r in rs),
                "loyo_mse":{k:round(v,7) for k,v in errors.items()},
                "delta_mse_vs_temperature":{k:round(base-v,7) for k,v in errors.items()},
                "gap_improves_temperature":errors["temperature_plus_gap"]<base}
        results[endpoint]=output
    return {"status":"ORIGINAL_DRYAD_2023_CLIMATE_GAP_FITNESS_INCREMENT_LOYO",
        "results":results,"year_level_prediction_unit":True,
        "gap":"caterpillar peak April day minus mean first egg April day",
        "gap_is_not_chick_demand_mismatch":True,
        "corrected_fledged":"NumberFledged + 0.5 * NumberFledgedDeviation",
        "recruits_all_broods":True,
        "weather_station_crosswalk_verified":False,
        "posthoc_exploratory_no_confirmatory_p_values":True,
        "causal_effect_identified":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=evaluate(build(load(),weather()))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
