"""Audit species/Include distributions before pre-registering resource-fitness fit."""
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path
from scripts.payoff_b_2023_real_fitness_resource_join import load
def audit(data):
    fitness=data["fitness"];resource=data["resource"]
    species=Counter(str(r.get("Species")) for r in fitness)
    includes=Counter(str(r.get("Include")) for r in fitness)
    groups=defaultdict(Counter)
    for r in fitness:
        groups[str(r.get("Area"))][(str(r.get("Species")),str(r.get("Include")))]+=1
    peak=defaultdict(list)
    for r in resource:
        peak[str(r.get("AreaName"))].append(r)
    return {"status":"ORIGINAL_2023_SPECIES_INCLUDE_AND_RESOURCE_SCHEMA_AUDIT",
        "fitness_species_counts":dict(species),"fitness_include_counts":dict(includes),
        "fitness_area_species_include":{a:{"|".join(k):v for k,v in counts.items()}
                                       for a,counts in groups.items()},
        "resource_by_area":{a:{"rows":len(rows),
             "nonmissing_peak_day":sum(r.get("MidDate") is not None for r in rows),
             "nonmissing_max_biomass":sum(r.get("MaxBiom") is not None for r in rows)}
             for a,rows in peak.items()},
        "site_name_alias_unverified":["Liesbosch Breda","Liesbos"],
        "ecological_effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args();result=audit(load())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
