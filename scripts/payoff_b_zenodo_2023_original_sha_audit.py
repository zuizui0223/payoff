"""Retrieve public Zenodo 8377972 workbooks, enforce Dryad SHA256 identity."""
import argparse,hashlib,io,json,urllib.request
from pathlib import Path
from openpyxl import load_workbook
EXPECTED={
"Tbl_Fitness_GT_HVVLOHLBWH_FirstClutches.xlsx":"53c5c4e0861759c2b33e5a95e1b734f83368875a67cff481353e22072fafb977",
"tbl_PeakDate_Biomass_AllAreas_AllSpecies.xlsx":"f6562a60c91b98b2c295afb1f07b1f9f8af5760a6e72c1375369a0daaedd0b28",
"deBilt_1955_2022.xlsx":"0c10fe860fc80c6b77f4315514de5caac8ff19973d4b332a2d2cf368fec591c6"}
def get(url,limit):
    req=urllib.request.Request(url,headers={"User-Agent":"PAYOFF-B-Zenodo-public-original-sha-audit/1.0"})
    with urllib.request.urlopen(req,timeout=50) as resp:
        raw=resp.read(limit+1)
        if len(raw)>limit:raise ValueError("Source exceeds bounded limit")
        if resp.status!=200:raise ValueError("Source not HTTP 200")
    return raw
def inspect():
    record=json.loads(get("https://zenodo.org/api/records/8377972",2_000_000))
    manifest={f["key"]:f for f in record.get("files",[])}
    result={"status":"ZENODO_ORIGINAL_SHA256_COMPARISON",
        "zenodo_record_id":8377972,"dryad_doi":"10.5061/dryad.1zcrjdfz0",
        "files":{},"ecological_effect_fitted":False}
    for name,digest in EXPECTED.items():
        file=manifest[name]
        out={"dryad_sha256":digest,"zenodo_checksum":file.get("checksum"),
             "size":file.get("size")}
        try:
            raw=get(file["links"]["self"],3_000_000)
            got=hashlib.sha256(raw).hexdigest()
            out["download_sha256"]=got
            out["source_identical_to_dryad"]=got==digest
            if got==digest:
                book=load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
                out["sheets"]=[]
                for ws in book.worksheets:
                    iterator=ws.iter_rows(values_only=True)
                    header=next(iterator,())
                    out["sheets"].append({"name":ws.title,"rows":ws.max_row,
                        "columns":ws.max_column,
                        "first_row":[str(x) if x is not None else None for x in header[:70]]})
        except Exception as exc:
            out["download_status"]="ERROR_"+type(exc).__name__
        result["files"][name]=out
    result["all_three_dryad_sha256_identical"]=all(
        f.get("source_identical_to_dryad") is True for f in result["files"].values())
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=inspect()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
