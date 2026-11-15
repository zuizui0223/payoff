"""Fail-closed site/year overlap preflight for actual Monitoring Sites 1000 tables.

No column names or site IDs are guessed. User-provided explicit mappings are
required, and source-file metadata cannot masquerade as observations.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import json

class OverlapNotAdmitted(ValueError):
    pass

def read_channel_csv(path, *, site_column, year_column, source_id, max_bytes=30_000_000):
    path=Path(path)
    raw=path.read_bytes()
    if not raw or len(raw)>max_bytes:raise OverlapNotAdmitted("Invalid source size")
    try:
        text=raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise OverlapNotAdmitted("Source encoding not UTF-8; explicitly convert and record provenance") from exc
    rows=list(csv.DictReader(text.splitlines()))
    if not rows:raise OverlapNotAdmitted("No original observation rows")
    if site_column not in rows[0] or year_column not in rows[0]:
        raise OverlapNotAdmitted("Source site/year columns not verified")
    if not source_id:raise OverlapNotAdmitted("Missing source identifier")
    pairs=set()
    missing=0
    for r in rows:
        site=(r[site_column] or "").strip()
        year=(r[year_column] or "").strip()
        if not site or not year.isdigit() or not 1900<=int(year)<=2100:
            missing+=1
            continue
        pairs.add((site,int(year)))
    if not pairs:raise OverlapNotAdmitted("No valid site/year records")
    return {"source_id":source_id,"sha256":hashlib.sha256(raw).hexdigest(),
            "rows":len(rows),"missing_site_year_rows":missing,
            "unique_site_years":len(pairs),"sites":len({s for s,_ in pairs}),
            "years":[min(y for _,y in pairs),max(y for _,y in pairs)],
            "site_year_pairs":pairs}

def overlap_preflight(channels, *, minimum_years=3):
    if not channels:raise OverlapNotAdmitted("No source channels")
    if len(set(channels))!=len(channels):raise OverlapNotAdmitted("Duplicate channel")
    if any(not v.get("sha256") or not v.get("source_id") for v in channels.values()):
        raise OverlapNotAdmitted("Source receipts not verified")
    common=set.intersection(*(v["site_year_pairs"] for v in channels.values()))
    per_site=defaultdict(set)
    for site,year in common:per_site[site].add(year)
    eligible={site:sorted(years) for site,years in per_site.items() if len(years)>=minimum_years}
    return {"status":"ORIGINAL_SOURCE_SITE_YEAR_OVERLAP_PREFLIGHT_ONLY",
            "channels":{name:{k:v for k,v in receipt.items() if k!="site_year_pairs"}
                        for name,receipt in channels.items()},
            "matched_site_years":len(common),
            "matched_sites":len(per_site),
            "sites_with_minimum_years":len(eligible),
            "minimum_years":minimum_years,
            "eligible_site_years":eligible,
            "site_id_crosswalk_verified":False,
            "sampling_protocol_equivalence_verified":False,
            "weather_biomass_effect_fitted":False}

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--mapping",type=Path,required=True,
                        help="Explicit JSON: channel -> {path,site_column,year_column,source_id}")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    mapping=json.loads(args.mapping.read_text(encoding="utf-8"))
    receipts={name:read_channel_csv(**cfg) for name,cfg in mapping.items()}
    result=overlap_preflight(receipts)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
