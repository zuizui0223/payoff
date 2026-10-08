#!/usr/bin/env python3
"""Original houbara workbook: schema, timing chronology and actionability ONLY.

Pinned Zenodo Burnside 2021, verified MD5 via the adjacent source-gate
script. No new migration-cue coefficient or natural fitness model is fitted.
No individual coordinates or timestamps are exported.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import io
import json
import math
import posixpath
import re
import statistics
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import payoff_b_houbara_zenodo_metadata_gate as gate

N = {"m":gate.MAIN_XML_NS}
P = gate.PKG_REL_NS
R = gate.DOC_REL_NS


def workbook_sections(raw):
    z = zipfile.ZipFile(io.BytesIO(raw))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    relations = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    paths = {}
    for rel in relations.findall(f"{{{P}}}Relationship"):
        url = rel.attrib.get("Target","")
        paths[rel.attrib.get("Id")] = (
            url.lstrip("/") if url.startswith("/") else
            posixpath.normpath(posixpath.join("xl",url))
        )
    strings=[]
    if "xl/sharedStrings.xml" in z.namelist():
        with z.open("xl/sharedStrings.xml") as fh:
            for event, el in ET.iterparse(fh,events=("end",)):
                if el.tag == f"{{{gate.MAIN_XML_NS}}}si":
                    strings.append("".join(el.itertext()))
                    el.clear()
    out={}
    names={}
    for sh in wb.findall(".//m:sheets/m:sheet",N):
        name=sh.attrib["name"]
        rid=sh.attrib.get(f"{{{R}}}id")
        target=paths.get(rid)
        if not target or target not in z.namelist():
            raise ValueError("missing worksheet target")
        names[name]=target
    for name,target in names.items():
        if name == "null_spring_dataset":
            out[name]={"metadata_only":True}
            continue
        root=ET.fromstring(z.read(target))
        rows=[]
        for rr in root.findall(".//m:sheetData/m:row",N):
            arr={}
            for cell in rr.findall("m:c",N):
                cellref=cell.attrib.get("r","")
                col=re.match(r"[A-Z]+",cellref)
                if col is None:continue
                t=cell.attrib.get("t","")
                v=cell.find("m:v",N)
                inline=cell.find("m:is",N)
                if t=="s" and v is not None and v.text is not None:
                    val=strings[int(v.text)]
                elif t=="inlineStr" and inline is not None:
                    val="".join(inline.itertext())
                elif v is not None:
                    try: val=float(v.text)
                    except (ValueError,TypeError):val=v.text
                else:
                    val=None
                arr[col.group(0)]=val
            if arr:rows.append(arr)
        out[name]={"rows":rows,"row_nodes_with_values":len(rows)}
    z.close()
    return out


def column_number(key):
    v=0
    for ch in key:
        v=v*26+ord(ch)-64
    return v


def safe_normalize(x):
    if x is None:return None
    if isinstance(x,str):return x.strip()
    if isinstance(x,float):
        if not math.isfinite(x):return None
        if x==int(x):return str(int(x))
        return str(x)
    return str(x)


def to_serial(x):
    if x is None:return None
    if isinstance(x,(int,float)):
        return float(x) if math.isfinite(x) else None
    x=str(x).strip()
    if not x:return None
    try:return float(x)
    except ValueError:pass
    try:
        date=dt.datetime.fromisoformat(x.replace("Z","+00:00"))
        return (date-dt.datetime(1899,12,30,tzinfo=date.tzinfo)).total_seconds()/86400
    except ValueError:return None


def inspect_event_sheet(sheet, name):
    rows=sheet["rows"]
    if not rows:return {"status":"EMPTY"}
    headers={k:safe_normalize(v) for k,v in rows[0].items()}
    byname={v:k for k,v in headers.items() if v}
    essentials=["id","Year","departure.date","arrival.date",
                 "departure.temperature.C","arrival.temperature.C"]
    if name=="autumn_migration_data":
        essentials.remove("arrival.temperature.C")
    miss_columns=[x for x in essentials if x not in byname]
    if miss_columns:
        raise ValueError(f"{name} missing essential fields {miss_columns}")
    row_data=rows[1:]
    missing={}
    for col in essentials:
        key=byname[col]
        missing[col]=sum(safe_normalize(r.get(key)) in (None,"","NA","NaN")
                         for r in row_data)
    identity_year=collections.Counter()
    years=collections.Counter()
    ids=set()
    duration=[]
    bad_chronology=0
    for row in row_data:
        bird=safe_normalize(row.get(byname["id"]))
        year=safe_normalize(row.get(byname["Year"]))
        if bird is not None:ids.add(bird)
        if year is not None:years[year]+=1
        if bird and year:identity_year[(bird,year)]+=1
        a=to_serial(row.get(byname["departure.date"]))
        b=to_serial(row.get(byname["arrival.date"]))
        if a is not None and b is not None:
            if b<a:bad_chronology+=1
            duration.append(b-a)
    key_dups={str(v):sum(1 for count in identity_year.values() if count==v)
              for v in sorted(set(identity_year.values()))}
    output={
        "sheet":name,
        "populated_rows_including_header":len(rows),
        "data_records":len(row_data),
        "declared_columns":list(byname),
        "distinct_source_id":len(ids),
        "year_distribution":dict(sorted(years.items())),
        "duplicate_or_repeat_id_year_codes":key_dups,
        "missingness_in_time_and_cue_columns":missing,
        "departure_after_arrival_count":bad_chronology,
        "paired_departure_arrival_count":len(duration),
        "duration_days_min":min(duration) if duration else None,
        "duration_days_median":statistics.median(duration) if duration else None,
        "duration_days_max":max(duration) if duration else None,
    }
    return output


def script_keyword_audit(raw):
    s=raw.decode("utf-8-sig")
    lines=s.splitlines()
    expression=re.compile(r"stopover|staging|waypoint|tracking|risk.set|hazard|survival|fitness|route|migration.duration|trip.duration|arrival.temperature|departure.temperature|null_spring_dataset|spring_migration_data|weather",re.I)
    terms=["stopover","staging","waypoint","risk.set","hazard","fitness",
           "survival","migration.duration","route"]
    counts={t:len(re.findall(re.escape(t),s,flags=re.I)) for t in terms}
    found=[(i,line.strip()[:180]) for i,line in enumerate(lines,1) if expression.search(line)]
    return {
        "script_lines":len(lines),
        "presence_of_explicit_checkpoints_or_fitness_words":counts,
        "bounded_relevant_source_code_context":[
            {"line":i,"text":t} for i,t in found[:24]
        ],
        "search_is_not_proof_of_no_function":True,
    }



# Field meanings are checked against the original author's Explanations
# sheet. These patterns are narrow provenance assertions, not inferences.
FIELD_DESCRIPTION_PATTERNS = {
    "departure.date": ("last fix", "departure site"),
    "arrival.date": ("first fix", "arrival site"),
    "departure.temperature.C": ("modis", "8 days prior"),
    "arrival.temperature.C": ("modis", "8 days after"),
    "annual.ref.temperature.breeding": ("breeding site", "mean population departure date"),
    "departure.date.shuffled": ("shuffled",),
    "temperature.rand": ("shuffled",),
}


def check_author_temporal_semantics(explanation_rows):
    definitions = {}
    for r in explanation_rows:
        name = safe_normalize(r.get("A"))
        desc = safe_normalize(r.get("B"))
        if name in FIELD_DESCRIPTION_PATTERNS and isinstance(desc, str):
            if name in definitions:
                raise ValueError("duplicated author field definition: " + name)
            definitions[name] = desc
    missing = sorted(set(FIELD_DESCRIPTION_PATTERNS) - definitions.keys())
    if missing:
        raise ValueError("source author field explanations absent: " + repr(missing))
    for col, fragments in FIELD_DESCRIPTION_PATTERNS.items():
        val = definitions[col].lower()
        for fragment in fragments:
            if fragment not in val:
                raise ValueError("source author semantics changed at " + col)
    return {
        "status": "PUBLISHER_EXPLANATIONS_SOURCE_TEXT_VERIFIED",
        "field_definitions": definitions,
        "temporal_admission": {
            "departure.date": "LAST_FIX_AT_DEPARTURE_SITE_NOT_INSTANTANEOUS_DECISION",
            "arrival.date": "FIRST_FIX_AT_ARRIVAL_SITE_POST_MIGRATION",
            "departure.temperature.C": "MODIS_8DAY_PRIOR_TO_LAST_DEPARTURE_FIX_PROXY_NOT_DIRECT_BIRD_BELIEF",
            "arrival.temperature.C": "MODIS_8DAY_AFTER_ARRIVAL_POST_OUTCOME_NEVER_PREDEPARTURE_CUE",
            "annual.ref.temperature.breeding": "REMOTE_BREEDING_SITE_REFERENCE_AT_POPULATION_MEAN_DEPARTURE_DATE_NOT_INDIVIDUAL_KNOWLEDGE",
            "departure.date.shuffled": "AUTHOR_SHUFFLED_DEPARTURE_DATE_NOT_OBSERVED_NONDEPARTURE_RISK_SET",
            "temperature.rand": "AUTHOR_SHUFFLED_NULL_TEMPERATURE_NOT_OBSERVED_CUE_CHRONOLOGY",
        },
        "invalid_predeparture_model_features": [
            "arrival.date", "arrival.temperature.C",
            "annual.ref.temperature.breeding",
        ],
        "fit_interpretation_ceiling": (
            "Event-indexed prior temperature associations may be replicated, "
            "but direct perception, route-stage updating and causal "
            "departure hazard require independent data."
        ),
    }


def source_audit():
    raw,meta=gate._download_verified("MigrationData.xlsx")
    code,code_meta=gate._download_verified("PNAS_code.R")
    info={"source_archive_file":meta,"source_code_file":code_meta}
    if raw is None:
        info["status"]="ACCESS_OR_CHECKSUM_HOLD"
        return info
    tabs=workbook_sections(raw)
    for name in ("spring_migration_data","autumn_migration_data"):
        info[name]=inspect_event_sheet(tabs[name],name)
    known=tabs.get("Explanations",{}).get("rows",[])
    info["explanations"]={
        "rows":len(known),
        "author_field_definition_summaries":[
            " | ".join(safe_normalize(v)[:120] for v in row.values()
                       if v is not None and safe_normalize(v))
            for row in known[:36]
        ]
    }
    info["author_temporal_semantics"] = check_author_temporal_semantics(known)
    info["null_spring_dataset"]={
        "xlsx_declared_dimension":"A1:N132001",
        "year_shuffled_rows_not_used":True,
        "this_does_not_supply_real_non_departure_risk_sets":True
    }
    if code is not None:
        info["original_script_keyword_audit"]=script_keyword_audit(code)
    spring=info["spring_migration_data"]
    info["source_vs_published_Fig2_spring_departure_count"]={
        "fig2_publication_departures":133,
        "source_workbook_populated_departure_rows":spring["data_records"],
        "one_record_difference_if_132":spring["data_records"]==132,
        "reason": "NOT_IDENTIFIED",
        "do_not_repair_or_discard_rows":True,
    }
    names=set(spring["declared_columns"])
    info["has_observed_midroute_checkpoint_columns"]=any(
        "stopover" in col.lower() or "waypoint" in col.lower()
        for col in names
    )
    info["has_individual_fitness_outcome_columns"]=any(
        t in col.lower() for col in names for t in
        ("breeding_success","survival","offspring","reproduction")
    )
    info["has_daily_no_departure_decision_risk_sets"]=False
    info["decision_time_source_cue_note"]=(
        "The original paper uses prior-eight-day local temperature summarized "
        "relative to observed departure. The released spring sheet has event "
        "summaries, not full potential non-departure day risk sets."
    )
    info["source_status"]="VERIFIED_EVENT_LEVEL_PREDEPARTURE_CUE_ONLY"
    info["stagewise_recourse_status"]="NOT_OBSERVED_IN_WORKBOOK"
    info["fitness_status"]="NOT_OBSERVED_IN_WORKBOOK"
    info["causal_claim_status"]="HOLD; original authors already discovered temperature threshold repeatability"
    return info


def self_test():
    assert to_serial(12.5)==12.5
    assert to_serial("2021-01-01") is not None
    assert to_serial(None) is None
    assert column_number("AA")==27
    fake={"rows":[
        {"A":"id","B":"Year","C":"departure.date","D":"arrival.date",
         "E":"departure.temperature.C","F":"arrival.temperature.C"},
        {"A":1,"B":2018,"C":43000,"D":43010,"E":11,"F":14},
        {"A":2,"B":2018,"C":43000,"D":43015,"E":9,"F":17},
    ]}
    semantic_rows = [
        {"A": k, "B": " | ".join(v)} for k, v in
        FIELD_DESCRIPTION_PATTERNS.items()
    ]
    x = check_author_temporal_semantics(semantic_rows)
    assert x["status"] == "PUBLISHER_EXPLANATIONS_SOURCE_TEXT_VERIFIED"
    assert "arrival.temperature.C" in x["invalid_predeparture_model_features"]
    assert "departure.temperature.C" not in x["invalid_predeparture_model_features"]
    bad = [dict(z) for z in semantic_rows]
    for z in bad:
        if z["A"] == "arrival.temperature.C":
            z["B"] = "MODIS surface temperature 8 days prior"
    try:
        check_author_temporal_semantics(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("future arrival temperature relabel failed closed")
    result=inspect_event_sheet(fake,"spring_migration_data")
    assert result["data_records"]==2
    assert result["paired_departure_arrival_count"]==2
    assert result["duration_days_median"]==12.5
    assert result["departure_after_arrival_count"]==0
    print("PAYOFF_B_HOUBARA_FULL_SOURCE_SCHEMA_SYNTHETIC_PASS")


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--output",default="outputs/payoff_b_houbara_event_time_recourse_gate_20261008.json")
    args=ap.parse_args()
    if args.self_test:
        self_test()
    else:
        report=source_audit()
        path=Path(args.output)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
        print("PAYOFF_B_HOUBARA_FULL_SOURCE_ADMISSION")
        out={k:v for k,v in report.items() if k not in ("explanations","original_script_keyword_audit")}
        print(json.dumps(out,ensure_ascii=False))
        print("NO NEW CLIMATE CUE EFFECT, ACTIVE CONTROL OR FITNESS ESTIMATED")
        if report.get("source_status") != "VERIFIED_EVENT_LEVEL_PREDEPARTURE_CUE_ONLY":
            raise SystemExit(
                "SOURCE_GATE_FAILURE: event-level source was not actually "
                "read and verified in this execution. Receipt saved; "
                "archive timeouts cannot count as a green source audit."
            )
        if (report.get("author_temporal_semantics", {}).get("status") !=
                "PUBLISHER_EXPLANATIONS_SOURCE_TEXT_VERIFIED"):
            raise SystemExit(
                "SOURCE_GATE_FAILURE: author timestamp/cue definitions "
                "were not verified on this execution."
            )
