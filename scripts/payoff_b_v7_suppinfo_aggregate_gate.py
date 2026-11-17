"""PAYOFF-B V7 user-uploaded Kölzsch 2015 source aggregate admission.

Stand-alone validation of derived public source aggregate tables. The original
copyrighted DOCX need not be republished: if --source-docx is supplied, verify
its exact SHA256, seven tables / four embedded figures and independently
re-extract EVERY r, SMATR value and original S1 onset mean against the CSVs.

This never fits goose q×U, invents S_jy or a GPS region crosswalk.
"""
import argparse,csv,hashlib,json,math,re
from collections import Counter
from pathlib import Path

SOURCE_SHA="925e1e5921a4f005b55c5ffb60fa2958bcb29be8c56f4252cd00f66effe91e19"
ROOT=Path(__file__).resolve().parents[1]
QP=ROOT/"data/payoff_b_v7_kolzsch_2015_suppinfo_q_20261117.csv"
REGIONS=ROOT/"data/payoff_b_v7_kolzsch_2015_suppinfo_S1_20261117.csv"
ROUTES={
 "Greenland":["IRE","SIC","NIC","SGR","NGR"],
 "Svalbard":["SCO","SNO","NNO","SVA"],
 "Barents Sea":["NLDK","SWE","BALT","WS","KAN","PEKO","NSE"],
}
CORR_TABLE={"Greenland":1,"Svalbard":3,"Barents Sea":5}
SMATR_TABLE={"Greenland":2,"Svalbard":4,"Barents Sea":6}
CORR_RX=re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)(\*{1,3}|[’'])?\s*$")
SLOPE_RX=re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)(\*{1,3}|[’'])?\s*\(\s*([+-]?\d+(?:\.\d+)?)\s*,\s*([+-]?\d+(?:\.\d+)?)\s*\)\s*$")
MEAN_RX=re.compile(r"\(\s*(\d+)\s*±\s*([\d.]+)\s*\)")

def readrows(path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def audit_pairs(rows,regions):
    if len(rows)!=23 or len(regions)!=16:
        raise ValueError("Expected 23 source q rows and 16 regional means")
    names={z["code"]:z for z in regions}
    if len(names)!=16 or any(z["source_docx_sha256"]!=SOURCE_SHA for z in rows+regions):
        raise ValueError("Original hash/region key drift")
    observed=Counter()
    adjacent=Counter()
    ids=set()
    doubtful=set()
    reverse_slope=[]
    for x in rows:
        f=x["flyway"];src=x["source_code"];tgt=x["target_code"]
        if f not in ROUTES or src not in ROUTES[f] or tgt not in ROUTES[f]:
            raise ValueError("Unknown original route or region code")
        if (f,src,tgt) in ids:
            raise ValueError("Repeated source transition in source q")
        ids.add((f,src,tgt))
        step=ROUTES[f].index(tgt)-ROUTES[f].index(src)
        if step<=0 or step!=int(x["route_step"]) or (step==1)!=bool(int(x["consecutive"])):
            raise ValueError("Route order/adjacency differs from original")
        r=float(x["q_30year_correlation"])
        lo=float(x["smatr_ci_low_source"]);hi=float(x["smatr_ci_high_source"])
        smatr=float(x["smatr_slope_source"])
        if not math.isfinite(r) or abs(r)>1 or not(lo<=smatr<=hi) or x["q_significance"] not in ("","*","**","***","'"):
            raise ValueError("Original published correlation or SMATR bounds invalid")
        for code,col in ((src,"source"),(tgt,"target")):
            if (x[col+"_S1_candidate"]!=names[code]["region_S1_name"]
                 or x[col+"_alias_status"]!=names[code]["source_alias_status"]):
                raise ValueError("Candidate original regional alias differs from S1")
            if x[col+"_alias_status"]!="exact":
                doubtful.add(code)
        if smatr*r<0:reverse_slope.append((f,src,tgt))
        observed[f]+=1
        if step==1:adjacent[f]+=1
    if observed!={"Greenland":7,"Svalbard":5,"Barents Sea":11}:
        raise ValueError("Original published 30-year q tables differ")
    if adjacent!={"Greenland":4,"Svalbard":3,"Barents Sea":6}:
        raise ValueError("Original 13 consecutive route transitions differ")
    if doubtful!={"NLDK","NSE"}:
        raise ValueError("Unexpected unresolved published region aliases")
    exact_adj=sum(x["consecutive"]=="1" and
        x["source_alias_status"]=="exact" and x["target_alias_status"]=="exact"
        for x in rows)
    if exact_adj!=11:
        raise ValueError("Source exact adjacent transition count changed")
    for z in regions:
        if int(z["mean_onset_julian_day"])<1 or int(z["mean_onset_julian_day"])>366 or float(z["onset_sd_days"])<=0:
            raise ValueError("Source Julian onset values impossible")
    # POST-OPEN document integrity screen, NOT biological inference.
    # For a standard magnitude SMA, s is related to SD(target)/SD(source).
    # Different source year/pair inclusion could affect this diagnostic.
    sd_by_code={x["code"]:float(x["onset_sd_days"]) for x in regions}
    ratio_screen={}
    for flyway in ROUTES:
        sub=[x for x in rows if x["flyway"]==flyway]
        abs_diff=[
            abs(float(x["smatr_slope_source"]) -
                sd_by_code[x["target_code"]]/sd_by_code[x["source_code"]])
            for x in sub
        ]
        ratio_screen[flyway]={
            "n_published_smatr":len(sub),
            "n_within_0_025_of_candidate_S1_sd_ratio":sum(z<0.025 for z in abs_diff),
            "mean_absolute_smatr_minus_S1_ratio":sum(abs_diff)/len(abs_diff),
            "screen_tolerance_selected_post_inspection_not_inference":0.025,
        }
    return {
      "status":"PUBLISHED_ORIGINAL_30YEAR_Q_AGGREGATES_ADMITTED",
      "uploaded_original_docx_sha256":SOURCE_SHA,
      "original_table_S1_regions":len(regions),
      "original_30year_pairwise_q":len(rows),
      "pairwise_q_by_flyway":dict(observed),
      "consecutive_route_pairs":sum(adjacent.values()),
      "consecutive_by_flyway":dict(adjacent),
      "consecutive_unambiguous_S1_candidate_names":exact_adj,
      "unverified_source_region_alias_codes":sorted(doubtful),
      "published_q_30y_range":[min(float(x["q_30year_correlation"]) for x in rows),
                               max(float(x["q_30year_correlation"]) for x in rows)],
      "negative_correlation_with_positive_published_smatr_slope":len(reverse_slope),
      "negative_r_positive_smatr_pairs":reverse_slope,
      "post_open_smatr_vs_S1_sd_ratio_screen":ratio_screen,
      "smatr_alternative_s_sensitivity_status":"HOLD_AUTHOR_OR_ORIGINAL_PAIRYEAR_CALCULATION_CHECK",
      "original_annual_1982_2011_regional_onsets_as_tabular_rows":False,
      "Figure_S1_annual_traces_are_not_tabular_source":True,
      "original_region_geometry_or_polygons_attached":False,
      "frozen_V7_q_transition_count_admission":"PASS_Q_COUNTS_ONLY",
      "frozen_V7_primary_q_x_U":"NOT_ESTIMABLE_MISSING_YEAR_SPECIFIC_S_JY_AND_GPS_REGION_GEOMETRY",
      "frozen_V7_bird_arrival_response_y_opened":False,
      "original_DOCX_redistributed":False,
    }

def compare_original_document(q,region,source):
    from docx import Document
    if hashlib.sha256(source.read_bytes()).hexdigest()!=SOURCE_SHA:
        raise ValueError("Uploaded original DOCX SHA256 mismatch")
    d=Document(source)
    if len(d.tables)!=7 or len(d.inline_shapes)!=4:
        raise ValueError("Original DOCX table/image count mismatch")
    qkey={(x["flyway"],x["source_code"],x["target_code"]):x for x in q}
    regkey={x["region_S1_name"]:x for x in region}
    for row in d.tables[0].rows[1:]:
        orig=row.cells[0].text.strip()
        matched=MEAN_RX.search(row.cells[1].text)
        if orig not in regkey or not matched:
            raise ValueError("Original regional table missing")
        expected=regkey[orig]
        if int(matched.group(1))!=int(expected["mean_onset_julian_day"]) or abs(float(matched.group(2))-float(expected["onset_sd_days"]))>1e-8:
            raise ValueError("Original S1 source values disagree with CSV")
    for flyway in ROUTES:
        correlation=d.tables[CORR_TABLE[flyway]]
        slope=d.tables[SMATR_TABLE[flyway]]
        columns=[c.text.strip() for c in correlation.rows[0].cells]
        for k in range(2,len(correlation.rows)):
            sr=correlation.rows[k].cells[0].text.strip()
            for col in range(1,len(columns)):
                raw=correlation.rows[k].cells[col].text.strip()
                raw_s=slope.rows[k].cells[col].text.strip()
                if not raw and not raw_s:continue
                x=qkey.get((flyway,sr,columns[col]))
                mr=CORR_RX.fullmatch(raw)
                ms=SLOPE_RX.fullmatch(raw_s)
                if x is None or mr is None or ms is None:
                    raise ValueError("Published original pair not reproduced")
                if (abs(float(mr.group(1))-float(x["q_30year_correlation"]))>1e-12
                    or abs(float(ms.group(1))-float(x["smatr_slope_source"]))>1e-12
                    or abs(float(ms.group(3))-float(x["smatr_ci_low_source"]))>1e-12
                    or abs(float(ms.group(4))-float(x["smatr_ci_high_source"]))>1e-12):
                    raise ValueError("Original published q or SMATR row mismatch")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--q",type=Path,default=QP)
    p.add_argument("--regions",type=Path,default=REGIONS)
    p.add_argument("--source-docx",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    q=readrows(args.q)
    reg=readrows(args.regions)
    report=audit_pairs(q,reg)
    if args.source_docx:
        compare_original_document(q,reg,args.source_docx)
        report["exact_original_DOCX_reextracted"]=True
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
