"""Read original Zenodo/Dryad 2023 README and identify phenology date definitions."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
EXPECTED="7aa6f4c1d0bb440a73b2c31c70ff5f50bc3f807fc211876a05f788fd77ee18e9"
def run():
    req=urllib.request.Request("https://zenodo.org/api/records/8377972",
        headers={"User-Agent":"PAYOFF-B-original-readme-date-definition/1.0"})
    with urllib.request.urlopen(req,timeout=35) as response:
        record=json.load(response)
    f=next(x for x in record["files"] if x["key"]=="README.md")
    with urllib.request.urlopen(urllib.request.Request(f["links"]["self"],
          headers={"User-Agent":"PAYOFF-B-original-readme-date-definition/1.0"}),timeout=35) as response:
        raw=response.read(10_000)
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=EXPECTED:raise ValueError("README original Dryad SHA256 mismatch")
    text=raw.decode("utf-8")
    lines=text.splitlines()
    keywords=("LayDateApril","MidDate","MaxBiom","hatch","incubat","recruit","April","caterpillar","day of year")
    matches=[]
    for i,line in enumerate(lines):
        if any(k.lower() in line.lower() for k in keywords):
            matches.append({"line":i+1,"context":" ".join(lines[max(0,i-1):min(len(lines),i+2)])[:1000]})
    return {"status":"ORIGINAL_DRYAD_README_SHA_VERIFIED",
            "readme_sha256":digest,"readme_lines":len(lines),
            "timing_definition_matches":matches,
            "full_readme_text":text,
            "lay_date_and_peak_same_origin_certified":False,
            "mismatch_effect_fitted":False}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
