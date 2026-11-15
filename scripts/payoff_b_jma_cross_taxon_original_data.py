"""Run source-verified JMA event-day exploratory cross-taxon associations."""
from __future__ import annotations
import argparse
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.payoff_b_japan_phenology_source_census import URL, INDEX_URL, parse_index_labels, classify
from src.japan_phenology_panel import parse_wide_jma_csv
from src.japan_phenology_cross_taxon import paired_station_year_anomaly_correlation
from src.japan_phenology_coupling_robustness import station_balanced_coupling
from src.japan_phenology_rm_sensitivity import rm_sensitivity
from src.japan_phenology_event_definition_audit import source_event_inventory

def compute(raw: bytes, labels: dict) -> dict:
    events = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for path in z.namelist():
            if not path.lower().endswith(".csv"):
                continue
            filename = path.rsplit("/",1)[-1]
            label = labels.get(filename, filename)
            group = classify(label)
            rows, _ = parse_wide_jma_csv(z.read(path), source_file=filename, event_label=label)
            for r in rows:
                r["source_taxon_guess"] = group
            events.extend(rows)
    pairs = []
    balanced = []
    for a,b in (("amphibian","plant_or_unclassified"),
                ("bird","plant_or_unclassified"),
                ("insect","plant_or_unclassified"),
                ("amphibian","bird"),
                ("bird","insect"),
                ("amphibian","insect")):
        pairs.append(paired_station_year_anomaly_correlation(events, group_a=a,group_b=b))
        balanced.append(station_balanced_coupling(events,a,b))
    return {"source":"JMA official cumulative biological season archive",
            "source_event_date_cells":len(events),
            "analysis":"exploratory cross-taxon within-station event-year anomaly correlation",
            "provisional_taxon_classification":True,
            "rm_code_quality_screened":False,
            "weather_ndvi_biomass_fitted":False,
            "pair_results":pairs,"station_balanced_robustness":balanced,
            "rm_and_leap_sensitivity":rm_sensitivity(events),
            "source_event_definition_inventory":source_event_inventory(events)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    def fetch(url):
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"PAYOFF-B-cross-taxon-original-data/1.0"}),timeout=60) as r:
            return r.read(30_000_000)
    labels=parse_index_labels(fetch(INDEX_URL).decode("utf-8"))
    out=compute(fetch(URL),labels)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False))

if __name__=="__main__":
    main()
