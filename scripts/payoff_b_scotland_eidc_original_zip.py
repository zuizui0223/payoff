"""PAYOFF-B: original EIDC 44-site tritrophic ZIP and exact source join audit.

Source URL is the explicit official download href on the EIDC dataset
landing page. This is an openly offered data ZIP under OGL, not guessed
private URL scraping. Source SHA256 and RO-Crate member sizes are preserved.
No ecological effects, no cross-dataset harmonization, no synthetic values.
"""
import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from scripts.payoff_b_scotland_eidc_original_csv_gate import get_support
from scripts.payoff_b_scotland_resource_source_probe import EIDC_ID, open_url

OFFICIAL_ZIP = f"https://data-package.ceh.ac.uk/data/{EIDC_ID}.zip"
MAX_SOURCE_ZIP = 28_000_000
SENTINELS = {"-999", "-999.0", "", "NA", "N/A", "NaN", "NULL", "null"}


def csv_file(b):
    rows = csv.DictReader(io.StringIO(b.decode("utf-8-sig", errors="replace"), newline=""))
    return rows.fieldnames or [], list(rows)


def audit():
    registered, doc = get_support()
    lookup={x["path"]:x for x in registered}
    received=open_url(OFFICIAL_ZIP,timeout=90,max_read=MAX_SOURCE_ZIP)
    raw=received.get("body")
    base={"status":"PAYOFF_B_EIDC_ORIGINAL_PUBLIC_ZIP_AUDIT",
          "source_doi":"10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3",
          "official_zip_url":OFFICIAL_ZIP,
          "head_source":"official_eidc_download_landing_page_href",
          "http_status":received.get("http_status"),
          "source_size":len(raw) if raw else None,
          "no_auth_bypass":True,
          "fitness_model_fitted":False}
    if not raw or received.get("http_status")!=200:
        return {**base,"status":"NO_GO_SOURCE_ZIP"}
    base["download_sha256"]=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        base["archive_member_count"]=len(names)
        base["archive_member_names"]=names[:45]
        schemas={}
        for name, src in lookup.items():
            paths=[x for x in names if x==name or x.endswith("/"+name)]
            if len(paths)!=1:
                schemas[name]={"admission":"MISSING_OR_DUPLICATED_MEMBER",
                               "matching_paths":paths}
                continue
            b=z.read(paths[0])
            if len(b)!=src["bytes"]:
                schemas[name]={"admission":"ROCRATE_SIZE_MISMATCH",
                               "bytes":len(b),"rocrate_bytes":src["bytes"]}
                continue
            col,rows=csv_file(b)
            site_col=next((x for x in col if x.lower()=="site"),None)
            year_col=next((x for x in col if x.lower()=="year"),None)
            station_year=Counter()
            for row in rows:
                if site_col and year_col:
                    k=(str(row.get(site_col)).strip(),str(row.get(year_col)).strip())
                    if k[0] and k[1] and k[0] not in SENTINELS and k[1] not in SENTINELS:
                        station_year[k]+=1
            schemas[name]={
                "admission":"SOURCE_BYTES_ROCRATE_MATCH",
                "file_sha256":hashlib.sha256(b).hexdigest(),
                "bytes":len(b),
                "rocrate_bytes":src["bytes"],
                "n_rows":len(rows),
                "columns":col,
                "sites":len({x[0] for x in station_year}),
                "years":sorted({x[1] for x in station_year}),
                "site_years":len(station_year),
                "site_year_keys":sorted(f"{s}|{y}" for s,y in station_year),
                "missing_values":{
                    x:sum(str(r.get(x,"")).strip() in SENTINELS for r in rows)
                    for x in col if any(k in x.lower() for k in
                        ("date","hatch","fledg","mass","nest","caterpillar"))
                },
            }
        base["schemas"]=schemas
        needed=("data/bird_phenology.csv","data/branch_beating.csv","data/nestlings.csv")
        compatible=all(schemas.get(x,{}).get("admission")=="SOURCE_BYTES_ROCRATE_MATCH"
                       for x in needed)
        if compatible:
            keys=[]
            for n in needed:
                keys.append(set(schemas[n]["site_year_keys"]))
            base["core_site_year_overlap"]={
                "bird_and_prey":len(keys[0]&keys[1]),
                "bird_and_nestlings":len(keys[0]&keys[2]),
                "all_three":len(keys[0]&keys[1]&keys[2]),
                "all_three_years":sorted({k.split("|")[1] for k in keys[0]&keys[1]&keys[2]}),
                "all_three_sites":len({k.split("|")[0] for k in keys[0]&keys[1]&keys[2]})}
        base["core_triplet_admitted"]=compatible
        base["biomass_mass_censoring_resolved"]=False
        base["manipulated_nests_excluded"]=False
    return base


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    x=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(x,separators=(",",":"),ensure_ascii=False))


if __name__ == "__main__":
    main()
