"""Read one official JMA daily observation page (Tokyo, April 2020).

Bounded, single public-page source probe. Does not assert JMA CSV quality
flags/homogeneity values exist in HTML. No automated bulk scraping.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.request

URL="https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2020&month=4&day=&view="

class TableReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables=[];self.table=None;self.row=None;self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=="table":self.table=[];self.tables.append(self.table)
        elif tag=="tr" and self.table is not None:self.row=[];self.table.append(self.row)
        elif tag in ("td","th") and self.row is not None:self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ("td","th") and self.cell is not None:
            self.row.append("".join(self.cell).strip());self.cell=None
        elif tag=="tr":self.row=None
        elif tag=="table":self.table=None

def probe(html:bytes):
    reader=TableReader()
    text=html.decode("utf-8",errors="replace")
    reader.feed(text)
    summaries=[]
    for i,table in enumerate(reader.tables):
        if not table:continue
        rows=[r for r in table if r]
        summaries.append({"table_index":i,"rows":len(rows),
                          "header_rows":rows[:5],
                          "first_data_rows":rows[5:8],
                          "rows_with_day_1_to_31":sum(bool(r and r[0].isdigit() and 1<=int(r[0])<=31) for r in rows)})
    return {"source_url":URL,"source_sha256":hashlib.sha256(html).hexdigest(),
            "bytes":len(html),"html_table_count":len(reader.tables),
            "table_summaries":summaries,
            "weather_csv_quality_codes_present_and_verified":False,
            "homogeneity_numbers_present_and_verified":False,
            "phenology_station_crosswalk_verified":False,
            "climate_effect_fitted":False}

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    req=urllib.request.Request(URL,headers={"User-Agent":"PAYOFF-B-JMA-one-page-source-probe/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        if r.status!=200:raise RuntimeError("Official JMA source returned non-200")
        data=r.read(2_000_001)
    if len(data)>2_000_000:raise ValueError("Unexpectedly large JMA page")
    receipt=probe(data)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False))
if __name__=="__main__":main()
