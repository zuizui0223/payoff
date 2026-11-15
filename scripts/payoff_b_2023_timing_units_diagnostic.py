"""Audit original laying-date and caterpillar-peak units before biological interpretation."""
import argparse,json
from collections import defaultdict
from pathlib import Path
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_filtered_descriptive_join import number
def audit(data):
    res={(str(r["AreaName"]).strip(),int(r["Year"])):r for r in data["resource"]
         if r.get("AreaName") and r.get("Year") is not None}
    values=defaultdict(list)
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):continue
        area=str(r.get("Area") or "").strip();year=number(r.get("YearOfBreeding"))
        if year is None or (area,int(year)) not in res:continue
        lay=number(r.get("LayDateApril"));peak=number(res[(area,int(year))].get("MidDate"))
        if lay is None or peak is None:continue
        values[(area,str(r.get("Species")))].append((lay,peak,lay-peak))
    result={}
    for (area,species),rows in sorted(values.items()):
        lay=[r[0] for r in rows];peak=[r[1] for r in rows];delta=[r[2] for r in rows]
        result[area+"|"+species]={"rows":len(rows),
            "lay_min_max":[min(lay),max(lay)],"peak_min_max":[min(peak),max(peak)],
            "offset_min_max":[min(delta),max(delta)],
            "negative_offsets":sum(v<0 for v in delta),
            "positive_offsets":sum(v>0 for v in delta),
            "zero_offsets":sum(v==0 for v in delta)}
    return {"status":"ORIGINAL_DRYAD_2023_DATE_UNITS_DIAGNOSTIC",
        "by_area_species":result,
        "source_readme_units_not_yet_certified":True,
        "signed_vs_absolute_identical_can_be_sign_degeneracy":True,
        "fitness_effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args();result=audit(load())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
