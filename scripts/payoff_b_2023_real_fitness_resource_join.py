"""Digest-verified Dryad 2023 source population-year join; no ecological effect fit."""
import argparse,hashlib,io,json,urllib.request
from collections import Counter,defaultdict
from pathlib import Path
from openpyxl import load_workbook
FILES={
"fitness":("Tbl_Fitness_GT_HVVLOHLBWH_FirstClutches.xlsx","53c5c4e0861759c2b33e5a95e1b734f83368875a67cff481353e22072fafb977"),
"resource":("tbl_PeakDate_Biomass_AllAreas_AllSpecies.xlsx","f6562a60c91b98b2c295afb1f07b1f9f8af5760a6e72c1375369a0daaedd0b28")}
def rows(raw):
    ws=load_workbook(io.BytesIO(raw),read_only=True,data_only=True).worksheets[0]
    it=ws.iter_rows(values_only=True)
    header=[str(x).strip() for x in next(it)]
    return [dict(zip(header,r)) for r in it]
def load():
    req=urllib.request.Request("https://zenodo.org/api/records/8377972",
        headers={"User-Agent":"PAYOFF-B-real-join-source/1.0"})
    with urllib.request.urlopen(req,timeout=40) as response:
        record=json.load(response)
    manifest={f["key"]:f["links"]["self"] for f in record["files"]}
    result={}
    for name,(filename,expected) in FILES.items():
        with urllib.request.urlopen(urllib.request.Request(manifest[filename],
                headers={"User-Agent":"PAYOFF-B-real-join-source/1.0"}),timeout=50) as response:
            raw=response.read(2_000_000)
        if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError("Dryad SHA mismatch")
        result[name]=rows(raw)
    return result
def join(data):
    fitness=data["fitness"];resource=data["resource"]
    counts=Counter()
    for r in fitness:
        if r.get("Area") is None or r.get("YearOfBreeding") is None:continue
        counts[(str(r["Area"]).strip(),int(r["YearOfBreeding"]))]+=1
    resources=defaultdict(list)
    for r in resource:
        if r.get("AreaName") is None or r.get("Year") is None:continue
        resources[(str(r["AreaName"]).strip(),int(r["Year"]))].append(r)
    shared=set(counts)&set(resources)
    areas=sorted({a for a,y in shared})
    byarea={}
    for area in areas:
        ys=sorted(y for a,y in shared if a==area)
        byarea[area]={"shared_years":len(ys),"first_year":ys[0],"last_year":ys[-1],
            "fitness_rows":sum(counts[(area,y)] for y in ys),
            "resource_rows":sum(len(resources[(area,y)]) for y in ys)}
    return {"status":"ORIGINAL_DRYAD_2023_FITNESS_RESOURCE_JOIN_COVERAGE_ONLY",
        "fitness_total_rows":len(fitness),"resource_total_rows":len(resource),
        "fitness_areas":sorted({a for a,y in counts}),
        "resource_areas":sorted({a for a,y in resources}),
        "shared_area_years":len(shared),"shared_areas":len(areas),
        "by_area":byarea,"same_year_population_join_only":True,
        "species_and_include_filter_not_yet_applied":True,
        "ecological_effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=join(load())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
