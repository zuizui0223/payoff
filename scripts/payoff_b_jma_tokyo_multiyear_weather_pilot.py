"""Bounded real JMA weather year-to-year pilot: Tokyo March–April 2019–2021.

Original public daily HTML only. Does not certify original downloadable CSV
quality or homogeneity codes and cannot be admitted to a causal model.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.request
from scripts.payoff_b_jma_single_month_real_weather_probe import TableReader

URL="https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year={year}&month={month}&day=&view="
YEARS=(2019,2020,2021)
MONTHS=(3,4)
COLUMNS={"tmean_c":6,"tmax_c":7,"tmin_c":8,"humidity_pct":9,
         "wind_mean_mps":11,"sunshine_hours":16}
def parse_month(html,year,month):
    p=TableReader();p.feed(html.decode("utf-8",errors="replace"))
    days=dt.date(year,month+1,1).toordinal()-dt.date(year,month,1).toordinal() if month<12 else 31
    candidates=[table for table in p.tables
        if sum(bool(row and row[0].isdigit() and 1<=int(row[0])<=days)
               for row in table)==days]
    if len(candidates)!=1:raise ValueError(f"Ambiguous official daily table {year}-{month}")
    values={}
    for row in candidates[0]:
        if not row or not row[0].isdigit() or not 1<=int(row[0])<=days:continue
        date=dt.date(year,month,int(row[0]))
        if date in values:raise ValueError("Duplicate source daily row")
        vals={}
        for variable,index in COLUMNS.items():
            token=row[index].strip() if len(row)>index else ""
            try:vals[variable]=float(token)
            except ValueError:vals[variable]=None
        values[date]=vals
    if len(values)!=days:raise ValueError("Incomplete original daily month")
    return values

def summarize_sources(sources):
    by_year={}
    for year in YEARS:
        daily={}
        for month in MONTHS:
            html=sources[(year,month)]
            daily.update(parse_month(html,year,month))
        march=[v for d,v in daily.items() if d.month==3]
        april=[v for d,v in daily.items() if d.month==4]
        def summary(rows,variable):
            valid=[r[variable] for r in rows if r[variable] is not None]
            return {"days_numeric":len(valid),"days_total":len(rows),
                    "mean":round(sum(valid)/len(valid),4) if valid else None,
                    "sum":round(sum(valid),4) if valid else None}
        by_year[str(year)]={
            "march_tmean":summary(march,"tmean_c"),
            "april_tmean":summary(april,"tmean_c"),
            "march_april_tmean":summary(march+april,"tmean_c"),
            "march_april_sunshine":summary(march+april,"sunshine_hours"),
            "march_april_humidity":summary(march+april,"humidity_pct"),
            "source_month_sha256":{str(month):hashlib.sha256(sources[(year,month)]).hexdigest()
                                   for month in MONTHS},
            "source_weather_days":len(daily)}
    return {"status":"ORIGINAL_JMA_HTML_YEARLY_WEATHER_DESCRIPTIVE_NOT_QUALITY_ADMITTED",
        "weather_station_source_code":"47662",
        "weather_to_phenology_station_crosswalk_verified":False,
        "weather_csv_quality_codes_verified":False,
        "weather_homogeneity_numbers_verified":False,
        "year_range":[2019,2021],"months":[3,4],
        "years":by_year,"phenology_effect_fitted":False}

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    sources={}
    for year in YEARS:
        for month in MONTHS:
            url=URL.format(year=year,month=month)
            req=urllib.request.Request(url,headers={"User-Agent":"PAYOFF-B-bounded-six-month-JMA-source-audit/1.0"})
            with urllib.request.urlopen(req,timeout=40) as response:
                if response.status!=200:raise RuntimeError("Official JMA HTTP failure")
                body=response.read(500_001)
                if len(body)>500_000:raise ValueError("Unexpectedly large source page")
                sources[(year,month)]=body
    result=summarize_sources(sources)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
