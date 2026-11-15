"""Source-verified exploratory phenology/resource/fitness joins and descriptive summaries.

Do not interpret laying date minus caterpillar peak as chick food-demand mismatch.
No causal, selective, or individual fitness coefficient is estimated here.
"""
import argparse,json,math
from collections import Counter,defaultdict
from pathlib import Path
from scripts.payoff_b_2023_real_fitness_resource_join import load

def number(x):
    if isinstance(x,bool):return None
    try:
        n=float(x)
        return n if math.isfinite(n) else None
    except (TypeError,ValueError):return None
def audit(data):
    resource={}
    for r in data["resource"]:
        a=str(r.get("AreaName") or "").strip()
        y=number(r.get("Year"))
        if not a or y is None:continue
        key=(a,int(y))
        if key in resource:raise ValueError("Duplicate resource area/year")
        resource[key]=r
    by=defaultdict(list)
    rejection=Counter()
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):
            rejection["include_not_1"]+=1;continue
        area=str(r.get("Area") or "").strip()
        year=number(r.get("YearOfBreeding"))
        if year is None or (area,int(year)) not in resource:
            rejection["no_exact_resource_area_year"]+=1;continue
        lay=number(r.get("LayDateApril"))
        peak=number(resource[(area,int(year))].get("MidDate"))
        biomass=number(resource[(area,int(year))].get("MaxBiom"))
        if None in (lay,peak,biomass):
            rejection["missing_timing_or_biomass"]+=1;continue
        species=str(r.get("Species") or "")
        if species not in ("Great Tit","Blue Tit"):
            rejection["unverified_species"]+=1;continue
        fledged=number(r.get("NumberFledged"))
        recruits=number(r.get("NumberRecruitsAllBroodsSummed"))
        by[(area,int(year),species)].append((lay,peak,biomass,fledged,recruits))
    summary={}
    for (area,year,species),rows in sorted(by.items()):
        k=area+"|"+species
        obj=summary.setdefault(k,{"years":set(),"rows":0,"fledged_observed":0,
                                  "recruits_observed":0,"timing_rows":0})
        obj["years"].add(year);obj["rows"]+=len(rows);obj["timing_rows"]+=len(rows)
        obj["fledged_observed"]+=sum(v[3] is not None for v in rows)
        obj["recruits_observed"]+=sum(v[4] is not None for v in rows)
    for obj in summary.values():
        obj["year_range"]=[min(obj["years"]),max(obj["years"])]
        obj["shared_years"]=len(obj["years"]);del obj["years"]
    return {"status":"ORIGINAL_DRYAD_2023_FILTERED_DESCRIPTIVE_JOIN_NO_FIT",
        "include_filter_applied":True,"site_alias_mapping_applied":False,
        "lay_date_minus_resource_peak_is_not_chick_demand_mismatch":True,
        "resource_peak_biomass_not_integrated_food_exposure":True,
        "by_area_species":summary,"excluded_rows":dict(rejection),
        "admitted_rows":sum(x["rows"] for x in summary.values()),
        "effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=audit(load())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
