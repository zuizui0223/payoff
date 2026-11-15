"""Bounded original NEON data manifest and CSV sample, no ecological inference."""
import argparse,csv,hashlib,io,json,urllib.request
from pathlib import Path
PRODUCTS={"phenology":"DP1.10055.001","temperature":"DP1.00002.001"}
API="https://data.neonscience.org/api/v0/data/"
def get(url,limit=2_000_000):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"PAYOFF-B-original-source-audit/1.0"})
    with urllib.request.urlopen(req,timeout=45) as response:
        if response.status!=200:raise ValueError("HTTP non-200")
        raw=response.read(limit+1)
        if len(raw)>limit:raise ValueError("Source exceeds bounded download")
        return raw
def manifest(product,site,month):
    raw=get(API+product+"/"+site+"/"+month,2_000_000)
    data=json.loads(raw)["data"]
    files=data.get("files") or []
    return {"sha256":hashlib.sha256(raw).hexdigest(),
            "files":[{"name":f.get("name"),"url":f.get("url"),"size":f.get("size")}
                     for f in files]}
def select_csv(files,product):
    # NEON publishes basic/expanded and sensor files; never guess a
    # biological measurement table from a metadata/validation file.
    candidates=[f for f in files if f["name"] and f["name"].lower().endswith(".csv")
                and "readme" not in f["name"].lower()
                and "variables" not in f["name"].lower()
                and "validation" not in f["name"].lower()
                and f["url"] and (f["size"] is None or f["size"]<=1_000_000)]
    if product=="phenology":
        candidates=[f for f in candidates if "statusintensity" in f["name"].lower()]
    else:
        candidates=[f for f in candidates if "basic" in f["name"].lower() and "30min" in f["name"].lower()]
    return sorted(candidates,key=lambda f:f["name"])[:1]
def inspect_csv(raw):
    decoded=raw.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(decoded))
    if not reader.fieldnames:raise ValueError("No original CSV header")
    count=sum(1 for _ in reader)
    return {"header":reader.fieldnames,"rows":count,"sha256":hashlib.sha256(raw).hexdigest()}
def run(site="ABBY",month="2020-05"):
    result={"status":"ORIGINAL_NEON_MANIFEST_PROBE_NOT_EFFECT_FIT","site":site,"month":month,
            "site_plot_crosswalk_verified":False,"measurement_quality_verified":False,
            "phenology_weather_effect_fitted":False,"products":{}}
    for name,product in PRODUCTS.items():
        m=manifest(product,site,month)
        chosen=select_csv(m["files"],name)
        out={"product_id":product,"manifest_sha256":m["sha256"],
             "manifest_files":len(m["files"]),"csv_candidates":len(chosen),
             "first_file_names":[f["name"] for f in m["files"][:12]]}
        if chosen:
            f=chosen[0]
            try:
                raw=get(f["url"],1_000_000)
                out["sample"]={"name":f["name"],**inspect_csv(raw)}
            except (ValueError,UnicodeError,TimeoutError) as exc:
                out["sample_error"]=type(exc).__name__+":"+str(exc)[:120]
        result["products"][name]=out
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
