"""Download and audit original Dryad 2023 XLSX schemas with declared SHA256.

Only source column names and date/site coverage; no outcome modeling.
"""
import argparse,hashlib,io,json,urllib.request,urllib.error
from collections import Counter
from pathlib import Path
from openpyxl import load_workbook

FILES={
 "fitness":(2611390,"53c5c4e0861759c2b33e5a95e1b734f83368875a67cff481353e22072fafb977",1_491_018),
 "caterpillar":(2611389,"f6562a60c91b98b2c295afb1f07b1f9f8af5760a6e72c1375369a0daaedd0b28",11_355),
 "temperature":(2611387,"0c10fe860fc80c6b77f4315514de5caac8ff19973d4b332a2d2cf368fec591c6",583_350),
}
def inspect(name,file_id,expected,size):
    url=f"https://datadryad.org/api/v2/files/{file_id}/download"
    req=urllib.request.Request(url,headers={"User-Agent":"PAYOFF-B-Dryad-original-file-audit/1.0"})
    with urllib.request.urlopen(req,timeout=60) as response:
        raw=response.read(size+1)
        if len(raw)!=size:raise ValueError(f"{name}: source size mismatch")
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=expected:raise ValueError(f"{name}: SHA256 mismatch")
    book=load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
    sheets=[]
    for ws in book.worksheets:
        iterator=ws.iter_rows(values_only=True)
        header=next(iterator,())
        sample=[]
        for i,row in enumerate(iterator):
            if i>=3:break
            sample.append([str(v)[:70] if v is not None else None for v in row[:12]])
        sheets.append({"sheet":ws.title,"rows":ws.max_row,"columns":ws.max_column,
            "header":[str(v) if v is not None else None for v in header[:80]],
            "first_three_rows":sample})
    return {"file_id":file_id,"size":len(raw),"sha256":digest,"sheets":sheets}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result={"status":"DRYAD_2023_ORIGINAL_XLSX_ACCESS_AUDIT_NO_FIT",
            "files":{},"ecological_effect_fitted":False}
    for name,(fid,digest,size) in FILES.items():
        try:
            result["files"][name]=inspect(name,fid,digest,size)
        except urllib.error.HTTPError as exc:
            result["files"][name]={"file_id":fid,"expected_sha256":digest,
                "status":"DRYAD_DIRECT_DOWNLOAD_ACCESS_BLOCKED","http_status":exc.code,
                "raw_source_downloaded":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
