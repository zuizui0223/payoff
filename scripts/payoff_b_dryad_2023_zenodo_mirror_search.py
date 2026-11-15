"""Public Zenodo metadata search for byte-identical Dryad 2023 file mirrors.

This is discovery, not a license to substitute a similarly named file.
"""
import argparse,hashlib,json,urllib.parse,urllib.request,urllib.error
from pathlib import Path
EXPECTED={
"Tbl_Fitness_GT_HVVLOHLBWH_FirstClutches.xlsx":"53c5c4e0861759c2b33e5a95e1b734f83368875a67cff481353e22072fafb977",
"tbl_PeakDate_Biomass_AllAreas_AllSpecies.xlsx":"f6562a60c91b98b2c295afb1f07b1f9f8af5760a6e72c1375369a0daaedd0b28",
"deBilt_1955_2022.xlsx":"0c10fe860fc80c6b77f4315514de5caac8ff19973d4b332a2d2cf368fec591c6"}
QUERIES=['"10.5061/dryad.1zcrjdfz0"','"Tbl_Fitness_GT_HVVLOHLBWH_FirstClutches"',
         '"Climate change does not equally affect temporal patterns"']
def fetch(url):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"PAYOFF-B-public-archive-discovery/1.0"})
    with urllib.request.urlopen(req,timeout=35) as response:
        raw=response.read(3_000_001)
        if len(raw)>3_000_000:raise ValueError("Source too large")
    return json.loads(raw),hashlib.sha256(raw).hexdigest()
def search():
    results=[]
    for query in QUERIES:
        url="https://zenodo.org/api/records?"+urllib.parse.urlencode({"q":query,"size":10})
        try:
            data,digest=fetch(url)
            hits=[]
            for item in data.get("hits",{}).get("hits",[]):
                files=item.get("files",[])
                hits.append({"record_id":item.get("id"),"doi":item.get("doi"),
                    "title":item.get("metadata",{}).get("title"),
                    "files":[{"key":f.get("key"),"checksum":f.get("checksum"),"size":f.get("size"),
                              "url":f.get("links",{}).get("self")} for f in files]})
            results.append({"query":query,"status":"PUBLIC_SEARCH_RESPONSE",
                "sha256":digest,"hits":hits})
        except (urllib.error.HTTPError,urllib.error.URLError,ValueError) as exc:
            results.append({"query":query,"status":"SEARCH_UNAVAILABLE",
                            "error_type":type(exc).__name__})
    return {"status":"PUBLIC_MIRROR_SEARCH_NO_RAW_FILE_SUBSTITUTION",
            "expected_original_sha256":EXPECTED,
            "searches":results,
            "digest_verified_mirror_files":[],
            "raw_original_workbooks_downloaded":False,
            "biological_effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=search()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
