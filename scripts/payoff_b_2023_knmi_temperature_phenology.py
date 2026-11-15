"""Source-certified KNMI daily temperature and 2023 Dryad bird/resource timing.

Exploratory temperature covariate and phenology associations, not causality.
Do not assume de Bilt/de Kooy stations represent individual breeding plots.
"""
import argparse,hashlib,io,json,datetime,urllib.request
from collections import defaultdict
from pathlib import Path
import numpy as np
from openpyxl import load_workbook
from scripts.payoff_b_2023_real_fitness_resource_join import load
from scripts.payoff_b_2023_filtered_descriptive_join import number
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict

SOURCES={
 "deBilt":("deBilt_1955_2022.xlsx","0c10fe860fc80c6b77f4315514de5caac8ff19973d4b332a2d2cf368fec591c6"),
 "deKooy":("temp_deKooy_1955_2022.xlsx","169bdf477ffe77e3179d059394b5ce20c5b7c7c96dbbbf889ebfa89f0295b98e")}
def weather():
    req=urllib.request.Request("https://zenodo.org/api/records/8377972",
        headers={"User-Agent":"PAYOFF-B-KNMI-temperature-proxy/1.0"})
    with urllib.request.urlopen(req,timeout=45) as response:manifest=json.load(response)
    urls={f["key"]:f["links"]["self"] for f in manifest["files"]}
    output={}
    for station,(filename,digest) in SOURCES.items():
        req=urllib.request.Request(urls[filename],
            headers={"User-Agent":"PAYOFF-B-KNMI-temperature-proxy/1.0"})
        with urllib.request.urlopen(req,timeout=60) as response:raw=response.read(1_000_000)
        if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError("KNMI source SHA mismatch")
        ws=load_workbook(io.BytesIO(raw),read_only=True,data_only=True).worksheets[0]
        it=ws.iter_rows(values_only=True)
        header=[str(x).strip() for x in next(it)]
        if not {"YYYYMMDD","TN","TX"}.issubset(header):raise ValueError("Missing KNMI columns")
        byyear=defaultdict(list)
        for cells in it:
            row=dict(zip(header,cells))
            date=str(row.get("YYYYMMDD") or "").strip()
            if date.endswith(".0"):date=date[:-2]
            if len(date)!=8 or not date.isdigit():continue
            try:d=datetime.date(int(date[:4]),int(date[4:6]),int(date[6:8]))
            except ValueError:continue
            tn=number(row.get("TN"));tx=number(row.get("TX"))
            if tn is None or tx is None:continue
            # Fixed calendar window March 1–April 30, chosen before reading results.
            if (d.month==3 or d.month==4):
                byyear[d.year].append((tn+tx)/20.0)
        output[station]={year:sum(v)/len(v) for year,v in byyear.items()
                         if len(v)>=50}
    return output
def audit(data,temperatures):
    resource={(str(r["AreaName"]).strip(),int(r["Year"])):r
              for r in data["resource"] if r.get("AreaName") and r.get("Year")}
    by=defaultdict(list)
    for r in data["fitness"]:
        if str(r.get("Include")).strip() not in ("1","1.0"):continue
        area=str(r.get("Area") or "").strip();year=number(r.get("YearOfBreeding"))
        if year is None or (area,int(year)) not in resource:continue
        species=str(r.get("Species") or "")
        if species not in ("Great Tit","Blue Tit"):continue
        lay=number(r.get("LayDateApril"))
        peak=number(resource[(area,int(year))].get("MidDate"))
        if lay is None or peak is None:continue
        by[(area,species,int(year))].append((lay,peak))
    result={}
    for (area,species,year),rows in by.items():
        if len(rows)<5:continue
        # Station assignment is only an exploratory geographic proxy.
        station="deKooy" if area=="Vlieland" else "deBilt"
        t=temperatures[station].get(year)
        if t is None:continue
        result.setdefault((area,species),[]).append((year,t,
            float(np.mean([r[0] for r in rows])),rows[0][1],len(rows)))
    outputs={}
    for (area,species),rows in sorted(result.items()):
        if len(rows)<12:continue
        rows.sort()
        X=np.array([[r[1]] for r in rows])
        predictions={}
        for outcome,idx in (("mean_laying_date",2),("caterpillar_peak_date",3)):
            y=np.array([r[idx] for r in rows])
            errs={}
            for name,feature in (("intercept",np.empty((len(rows),0))),
                                 ("march_april_temp",X)):
                pred=[]
                for i in range(len(rows)):
                    train=np.arange(len(rows))!=i
                    pred.append(float(fit_predict(feature[train],y[train],feature[~train])[0]))
                errs[name]=float(np.mean((y-np.array(pred))**2))
            predictions[outcome]={"mse":{k:round(v,5) for k,v in errs.items()},
                "delta_mse":round(errs["intercept"]-errs["march_april_temp"],5)}
        outputs[area+"|"+species]={"years":len(rows),"broods":sum(r[4] for r in rows),
            "station_proxy":"deKooy" if area=="Vlieland" else "deBilt",
            "temperature_range_c":[round(min(r[1] for r in rows),3),
                                    round(max(r[1] for r in rows),3)],
            "loyo":predictions}
    return {"status":"ORIGINAL_DRYAD_2023_KNMI_TEMPERATURE_PHENOLOGY_LOYO",
        "temperature_window":"March 1–April 30 calendar mean of (TN+TX)/2 in deg C",
        "temperature_original_units":"KNMI TN TX in 0.1 deg C",
        "site_station_crosswalk_verified":False,
        "station_assignment":"Vlieland: deKooy; other sites: deBilt; exploratory proxy only",
        "weather_original_sha256_verified":True,
        "year_level_cv":True,
        "results":outputs,"causal_effect_identified":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args();result=audit(load(),weather())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
