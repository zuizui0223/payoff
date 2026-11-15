"""One original-data Tokyo 2020 phenology × April daily-weather alignment.

The public JMA weather HTML has no verified quality/homogeneity flags.
This emits source-only overlap and timing; it NEVER admits weather effects.
"""
from __future__ import annotations
import argparse
import datetime as dt
import io
import json
from pathlib import Path
import sys
import urllib.request
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.payoff_b_jma_single_month_real_weather_probe import URL as WEATHER_URL, TableReader, probe
from scripts.payoff_b_japan_phenology_source_census import URL as PHENO_URL, INDEX_URL, parse_index_labels
from src.japan_phenology_panel import parse_wide_jma_csv

def align_original_sources(weather_html:bytes,phenology_zip:bytes,labels:dict):
    tables=TableReader();tables.feed(weather_html.decode("utf-8",errors="replace"))
    candidates=[t for t in tables.tables if sum(bool(r and r[0].isdigit() and 1<=int(r[0])<=30) for r in t)==30]
    if len(candidates)!=1:raise ValueError("Expected exactly one 30-day weather table")
    weather_days={}
    for row in candidates[0]:
        if not row or not row[0].isdigit() or not 1<=int(row[0])<=30:continue
        date=dt.date(2020,4,int(row[0]))
        # Numeric HTML display values only, not certified source-quality data.
        weather_days[date]={"tmean_c":float(row[6]),"tmax_c":float(row[7]),
                            "tmin_c":float(row[8]),"humidity_pct":float(row[9]),
                            "wind_mean_mps":float(row[11]),"sunshine_h":float(row[16])}
    events=[]
    with zipfile.ZipFile(io.BytesIO(phenology_zip)) as z:
        for name in z.namelist():
            if not name.endswith(".csv"):continue
            file=name.rsplit("/",1)[-1]
            panel,_=parse_wide_jma_csv(z.read(name),source_file=file,
                                       event_label=labels.get(file,file))
            events.extend(x for x in panel if x["year"]==2020 and x["station_name"]=="東京")
    if not events:raise ValueError("No Tokyo 2020 phenology events in original JMA archive")
    rows=[]
    for event in sorted(events,key=lambda x:x["event_date"]):
        d=dt.date.fromisoformat(event["event_date"])
        before=[v for date,v in weather_days.items() if date<d]
        after=[v for date,v in weather_days.items() if date>=d]
        rows.append({"source_file":event["source_file"],"label":event["event_label"],
                     "phenology_station_id":event["station_id"],
                     "phenology_station_name":event["station_name"],
                     "event_date":event["event_date"],
                     "rm_code_uninterpreted":event["rm_original_code"],
                     "april_weather_days_strictly_before_event":len(before),
                     "april_weather_days_on_or_after_event":len(after),
                     "april_tmean_pre_event_display_only_c":round(sum(v["tmean_c"] for v in before)/len(before),3) if before else None,
                     "full_30day_pre_event_window_covered_by_april_source":all(
                         d-dt.timedelta(days=offset) in weather_days for offset in range(1,31))})
    return {"status":"ORIGINAL_SOURCE_TEMPORAL_ALIGNMENT_NOT_QUALITY_ADMITTED",
            "weather_source":WEATHER_URL,
            "weather_source_receipt":{k:v for k,v in probe(weather_html).items() if k in ("source_sha256","source_daily_rows","daily_weather_unqualified_source_summary")},
            "phenology_station_name":"東京","phenology_event_year":2020,
            "original_phenology_event_count":len(rows),
            "events":rows,
            "weather_station_code_in_url":"47662",
            "weather_to_phenology_station_id_crosswalk_certified":False,
            "weather_quality_codes_certified":False,
            "weather_homogeneity_numbers_certified":False,
            "weather_phenology_effect_fitted":False}

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    def fetch(url,limit=8_000_000):
        req=urllib.request.Request(url,headers={"User-Agent":"PAYOFF-B-one-site-weather-phenology-audit/1.0"})
        with urllib.request.urlopen(req,timeout=60) as r:return r.read(limit+1)
    labels=parse_index_labels(fetch(INDEX_URL).decode("utf-8"))
    out=align_original_sources(fetch(WEATHER_URL),fetch(PHENO_URL),labels)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False))
if __name__=="__main__":main()
