"""Anonymous Dryad API original multi-population dataset inventory, metadata only."""
import argparse,hashlib,json,urllib.request,urllib.parse
from pathlib import Path
DOIS={"hoge_veluwe_2021":"10.5061/dryad.f1vhhmgx6",
      "multisite_tit_2023":"10.5061/dryad.1zcrjdfz0",
      "wytham_2026":"10.5061/dryad.51c59zwjn"}
API="https://datadryad.org/api/v2/"
def fetch(url):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"PAYOFF-B-Dryad-metadata/1.0"})
    with urllib.request.urlopen(req,timeout=35) as response:
        raw=response.read(2_000_001)
        if len(raw)>2_000_000:raise ValueError("Metadata too large")
    return json.loads(raw),hashlib.sha256(raw).hexdigest()
def inventory():
    results={}
    for key,doi in DOIS.items():
        url=API+"datasets/"+urllib.parse.quote("doi:"+doi,safe="")
        try:
            metadata,digest=fetch(url)
            results[key]={"doi":doi,"metadata_sha256":digest,
                "title":metadata.get("title"),
                "version":metadata.get("versionNumber"),
                "publicationDate":metadata.get("publicationDate"),
                "source_url":url,
                "raw_files_downloaded":False}
            version=metadata.get("_links",{}).get("stash:version",{}).get("href")
            if version:
                details,vdigest=fetch(urllib.parse.urljoin("https://datadryad.org",version))
                results[key]["version_metadata_sha256"]=vdigest
                results[key]["version_files_url"]=details.get("_links",{}).get("stash:files",{}).get("href")
        except Exception as exc:
            results[key]={"doi":doi,"status":"SOURCE_METADATA_UNAVAILABLE",
                          "error_type":type(exc).__name__}
    return {"status":"DRYAD_ANONYMOUS_SOURCE_INVENTORY_NO_EFFECT_ESTIMATION",
            "datasets":results,"biological_outcome_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    receipt=inventory()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(receipt,ensure_ascii=False))
if __name__=="__main__":main()
