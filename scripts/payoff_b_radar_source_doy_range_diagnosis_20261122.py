#!/usr/bin/env python3
"""Original source-only DOY range diagnosis; no chronology or effect calculation.

Only aggregate n, min, max, source-year counts may leave the private CI runner.
This is a mandatory validity gate before radar passage vs MODIS greenup timing.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from payoff_b_radar_greenup_heldout import source_rows, complete_rows


def diagnose(rows):
    complete=complete_rows(rows)
    result={
        "status":"SOURCE_FIELD_RANGE_DIAGNOSIS_NO_CHRONOLOGY",
        "original_rows":len(rows),
        "complete_rows":len(complete),
        "distinct_site_count":len({r["site"] for r in complete}),
        "distinct_year_count":len({r["year"] for r in complete}),
        "source_fields":{},
        "no_effect_or_gap_calculated":True,
        "no_original_station_row_export":True,
    }
    has_any_invalid=False
    for field in ["spring_q50","mean_greenup"]:
        vals=[r[field] for r in complete]
        low=[v for v in vals if v<1]
        high=[v for v in vals if v>366]
        invalid_by_year=Counter(r["year"] for r in complete if r[field]<1 or r[field]>366)
        has_any_invalid|=bool(low or high)
        result["source_fields"][field]={
            "n_numeric":len(vals),
            "min_value":min(vals),
            "max_value":max(vals),
            "n_less_than_1":len(low),
            "n_greater_than_366":len(high),
            "invalid_min":min(low+high) if low or high else None,
            "invalid_max":max(low+high) if low or high else None,
            "invalid_count_by_year":[{"year":int(y),"n_invalid":invalid_by_year[y]} for y in sorted(invalid_by_year)],
        }
    result["date_range_gate"]="REQUIRES_SOURCE_SEMANTICS" if has_any_invalid else "PASS"
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    rows=source_rows(a.input)
    result=diagnose(rows)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print("PAYOFF_RADAR_SOURCE_RANGE_DIAGNOSIS="+json.dumps(result,separators=(",",":"),allow_nan=False))


if __name__=="__main__":
    main()
