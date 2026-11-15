"""Original Dryad 2023: bird vs caterpillar temperature slopes in days/degree C.

Same site-year and same KNMI proxy for both phenologies. Non-causal.
Annual site/species mean laying dates, caterpillar peak; no pseudo-replicated nests.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
import numpy as np
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_knmi_temperature_phenology import weather
from scripts.payoff_b_2023_filtered_descriptive_join import number

def panel(data,temperatures):
    resource={}
    for r in data["resource"]:
        if r.get("AreaName") is None or r.get("Year") is None:continue
        key=(str(r["AreaName"]).strip(),int(r["Year"]))
        if key in resource:raise ValueError("Duplicate area-year resource")
        resource[key]=r
    grouped=defaultdict(list)
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):continue
        area=str(r.get("Area") or "").strip()
        year=number(r.get("YearOfBreeding"))
        if year is None or (area,int(year)) not in resource:continue
        species=str(r.get("Species") or "")
        if species not in ("Great Tit","Blue Tit"):continue
        lay=number(r.get("LayDateApril"))
        if lay is not None:grouped[(area,species,int(year))].append(lay)
    by=defaultdict(list)
    for (area,species,year),laydates in grouped.items():
        if len(laydates)<5:continue
        station="deKooy" if area=="Vlieland" else "deBilt"
        t=temperatures[station].get(year)
        peak=number(resource[(area,year)].get("MidDate"))
        if t is None or peak is None:continue
        lay=float(np.mean(laydates))
        by[(area,species)].append((year,t,lay,peak,peak-lay,len(laydates)))
    return by

def slope(x,y):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    denom=float(np.sum((x-x.mean())**2))
    if denom<1e-9:return None
    return float(np.sum((x-x.mean())*(y-y.mean()))/denom)

def audit(by,boot=1000,seed=20261115):
    result={}
    for (area,species),rows in sorted(by.items()):
        if len(rows)<12:continue
        rows.sort()
        a=np.asarray(rows,dtype=float)
        x=a[:,1]
        metrics={"laying_date":a[:,2],"caterpillar_peak":a[:,3],
                 "peak_minus_laying":a[:,4]}
        rng=np.random.default_rng(seed)
        inds=rng.integers(0,len(rows),size=(boot,len(rows)))
        output={}
        for label,y in metrics.items():
            point=slope(x,y)
            bootvals=[slope(x[idx],y[idx]) for idx in inds]
            valid=np.asarray([v for v in bootvals if v is not None])
            output[label]={"slope_days_per_c":round(point,5),
                "year_resample_95pct_interval_days_per_c":
                    [round(float(v),5) for v in np.percentile(valid,[2.5,97.5])],
                "bootstrap_replicates":len(valid)}
        result[area+"|"+species]={"years":len(rows),
            "year_range":[int(a[0,0]),int(a[-1,0])],
            "included_broods":int(a[:,5].sum()),
            "weather_proxy":"deKooy" if area=="Vlieland" else "deBilt",
            "slopes":output}
    return {"status":"ORIGINAL_DRYAD_2023_TEMPERATURE_SLOPE_GAP_EXPLORATORY",
        "temperature_window":"March-April average (TN+TX)/2 Celsius",
        "phenology_units":"April days (April 1 = day 1) for both laying and peak",
        "gap_definition":"caterpillar peak date minus first egg laying date, NOT chick-demand mismatch",
        "site_station_crosswalk_verified":False,
        "resampling_unit":"site-species-year; separate within each population and species",
        "uncertainty_method":"1000 year-level nonparametric bootstrap resamples, descriptive",
        "shared_caterpillar_peak_across_species":True,
        "causal_effect_identified":False,"results":result}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=audit(panel(load(),weather()))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
