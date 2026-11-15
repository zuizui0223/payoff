"""Original Dryad 2023 version file inventory and bounded source CSV preview."""
import argparse,hashlib,json,urllib.request,urllib.parse
from pathlib import Path
VERSION_FILES="https://datadryad.org/api/v2/versions/257297/files"
def fetch(url,limit=2_000_000):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"PAYOFF-B-Dryad-source-inventory/1.0"})
    with urllib.request.urlopen(req,timeout=45) as resp:
        raw=resp.read(limit+1)
        if len(raw)>limit:raise ValueError("Response exceeds cap")
        if resp.status!=200:raise ValueError("HTTP error")
    return raw
def inventory():
    raw=fetch(VERSION_FILES)
    doc=json.loads(raw)
    items=doc.get("_embedded",{}).get("stash:files",[])
    files=[]
    for f in items:
        links=f.get("_links") or {}
        files.append({"id":f.get("id"),"path":f.get("path"),
            "size":f.get("size"),"digest":f.get("digest"),
            "download_href":(links.get("stash:download") or {}).get("href")})
    return {"status":"ORIGINAL_DRYAD_2023_FILE_METADATA_NOT_RAW_OBSERVATIONS",
        "doi":"10.5061/dryad.1zcrjdfz0",
        "version_files_url":VERSION_FILES,
        "api_sha256":hashlib.sha256(raw).hexdigest(),
        "api_file_count":len(files),"files":files,
        "raw_fitness_resource_rows_downloaded":False,
        "fitness_resource_effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=inventory()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
