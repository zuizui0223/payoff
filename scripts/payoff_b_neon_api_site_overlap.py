"""NEON public product API: original server metadata and exact site/month overlap.

No raw ecological effect or population inference. No auth token required.
"""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

API="https://data.neonscience.org/api/v0/products/"
PRODUCTS={"plant_phenology":"DP1.10055.001","air_temperature":"DP1.00002.001",
          "precipitation":"DP1.00006.001","breeding_birds":"DP1.10003.001",
          "herbaceous_biomass":"DP1.10023.001"}
def fetch_product(product_id):
    url=API+product_id
    req=urllib.request.Request(url,headers={"User-Agent":"PAYOFF-B-source-metadata-audit/1.0",
                                            "Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=40) as resp:
        raw=resp.read(4_000_001)
        if len(raw)>4_000_000:raise ValueError("Unexpected metadata response size")
        if resp.status!=200:raise ValueError("NEON API returned non-200")
    payload=json.loads(raw)
    if "data" not in payload:raise ValueError("NEON API missing data")
    return payload["data"],hashlib.sha256(raw).hexdigest()
def availability_rows(data):
    result=set()
    for item in data.get("siteCodes",[]):
        site=item.get("siteCode")
        if not site:continue
        for month in item.get("availableMonths",[]):
            if isinstance(month,str) and len(month)>=7:
                result.add((site,month[:7]))
    return result
def summarize(sources):
    rows={name:availability_rows(data) for name,(data,_) in sources.items()}
    phen=rows["plant_phenology"]
    results={}
    for name,pairs in rows.items():
        shared=phen & pairs
        sites=sorted({s for s,_ in shared})
        years=sorted({m[:4] for _,m in shared})
        results[name]={"site_months":len(pairs),"sites":len({s for s,_ in pairs}),
            "phenology_shared_site_months":len(shared),
            "phenology_shared_sites":len(sites),
            "phenology_shared_years":years,
            "phenology_shared_site_codes":sites}
    return {"status":"ORIGINAL_NEON_API_PRODUCT_METADATA_ONLY",
        "site_months_not_raw_observation_days":True,
        "product_receipts":{name:{"product_id":PRODUCTS[name],"api_sha256":digest,
            "api_product_name":data.get("productName"),
            "site_codes_count":len(data.get("siteCodes",[]))}
            for name,(data,digest) in sources.items()},
        "availability":results,
        "raw_neon_observations_downloaded":False,
        "phenology_climate_effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    sources={name:fetch_product(pid) for name,pid in PRODUCTS.items()}
    result=summarize(sources)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
