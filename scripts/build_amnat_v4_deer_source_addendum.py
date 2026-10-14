#!/usr/bin/env python3
"""Extend the tested anonymized V8 archive with Ortega deer source data/code.

Inputs are fixed archived review bytes and publisher-provided Source Data.
The analysis remains unaltered apart from filenames/imports/identifying
labels. The final ZIP is created only AFTER the independent deer replay passes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
V8_ARCHIVE_SHA="1f1e6036871a75c60ff9f9a21df401409ac3b3f6e69b3e91bc4d05859874ec53"
DEER_SHA="2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364"
ORIGINAL_CODE={
 "scripts/payoff_b_ortega_source_data_probe.py":"scripts/source_workbook_reader.py",
 "scripts/payoff_b_ortega_variance_funnel.py":"scripts/animal_phase_variance.py",
 "scripts/payoff_b_mule_deer_readiness_source_data.py":"scripts/animal_readiness.py",
 "scripts/payoff_b_mule_deer_two_clock_channel.py":"scripts/animal_phase_channels.py",
}
ORIGINAL_FROZEN={
 "data/payoff_b_ortega_variance_funnel_result_20261003.json":"data/frozen_deer/frozen_variance.json",
 "data/payoff_b_mule_deer_readiness_result_20261003.json":"data/frozen_deer/frozen_readiness.json",
 "data/payoff_b_mule_deer_two_clock_channel_result_20261003.json":"data/frozen_deer/frozen_channels.json",
}
FORBIDDEN=("zuizui0223","payoff_b","PAYOFF-B","ZHANG RUIQI","rachelzhang0223")
EMAIL=re.compile(r"(?i)[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}")


def sha(blob:bytes)->str:
    return hashlib.sha256(blob).hexdigest()


def neutralize(s:str)->str:
    for old,new in (
       ("payoff_b_ortega_source_data_probe","source_workbook_reader"),
       ("payoff_b_ortega_variance_funnel","animal_phase_variance"),
       ("payoff_b_mule_deer_readiness_source_data","animal_readiness"),
       ("payoff_b_mule_deer_two_clock_channel","animal_phase_channels"),
       ("PAYOFF-B","Seasonal tracking"),
       ("PAYOFF_B","SEASONAL_TRACKING"),
       ("payoff_b_","seasonal_"),
    ):
        s=s.replace(old,new)
    return s


def safe_text(txt:str,name:str):
    for item in FORBIDDEN:
        if item.casefold() in txt.casefold():
            raise ValueError("Identifying project/author content in "+name)
    if EMAIL.search(txt):
        raise ValueError("Possible direct email contact in "+name)


def save(root:Path,relative:str,content:bytes,scan:bool=True):
    if scan:safe_text(content.decode("utf-8"),relative)
    path=root/relative
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(content)


def addendum_readme():
    return """# Independent mule-deer source-data reproduction

Supplement to the anonymous Paper 2 seasonal tracking V8 archive.

Published original study: Ortega, A. C., Aikens, E. O., Merkle, J. A.,
Monteith, K. L. and Kauffman, M. J. (2023), Migrating mule deer
compensate en route for phenological mismatches, Nature Communications
14:2008, doi:10.1038/s41467-023-37750-z.

The included Source Data XLSX is republished with that open-access
article and credited under its Creative Commons Attribution 4.0
license (https://creativecommons.org/licenses/by/4.0/). The workbook
SHA256 is 2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364.
No individual deer tracks beyond what the authors released are
generated or fabricated.

From the extracted archive root, run:
    bash scripts/reproduce_mule_deer.sh

This independently regenerates descriptive (NOT causal) source-data
analyses: 152 animal-years/72 animals, the variance contraction and
signed movement/stopover association, and the conservative March
IFBFat subset (62 animal-years/40 deer). It checks exactly
the frozen numeric estimands and confidence intervals, retaining
the earlier original study's priority.

The source-data analysis files have only owner/project-identifying
comments, paths and import names changed. Original scripts belong to
this manuscript's author(s) and no general software reuse license
is asserted by this archive.

The published source already demonstrated phase convergence and
compensatory movement. A pattern of source-data functional
dissociation here is not evidence of separately identified latent
information or route-control gains, molecular clocks, fitness
benefits, or demographic effects.

This archive remains an internal anonymous candidate, not a deposited
reviewer link or an approved journal submission. Human review of
all pages and source-data conditions remains required.
"""


def reproduction_script():
    return """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p outputs/deer
SOURCE_URL="$(python3 -c "from pathlib import Path; print(Path('data/mule_deer_source_data.xlsx').resolve().as_uri())")"
python3 scripts/animal_phase_variance.py --url "$SOURCE_URL" --seed 20261003 --bootstrap-replicates 10000 --output outputs/deer/reproduced_variance.json
python3 scripts/animal_readiness.py --url "$SOURCE_URL" --seed 20261003 --bootstrap-replicates 10000 --output outputs/deer/reproduced_readiness.json
python3 scripts/animal_phase_channels.py --url "$SOURCE_URL" --seed 20261003 --bootstrap-replicates 10000 --output outputs/deer/reproduced_channels.json
python3 scripts/verify_animal.py --source data/mule_deer_source_data.xlsx --frozen data/frozen_deer --replayed outputs/deer --receipt outputs/deer/verified_deer.json
"""


def fixed_zip(root:Path,dest:Path):
    if dest.exists():
        raise ValueError("Refuse to overwrite frozen reviewer ZIP")
    dest.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(dest,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(p for p in root.rglob("*") if p.is_file()):
            zi=zipfile.ZipInfo(f.relative_to(root).as_posix(),date_time=(2026,10,14,0,0,0))
            zi.create_system=3
            zi.external_attr=(0o644&0xffff)<<16
            zi.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(zi,f.read_bytes())


def prepare(source_zip:Path,deer_xlsx:Path,pdf_qc:Path,dest:Path)->dict:
    if dest.exists() and any(dest.iterdir()):
        raise ValueError("Nonempty archive destination")
    raw=source_zip.read_bytes()
    if sha(raw)!=V8_ARCHIVE_SHA:
        raise ValueError("Original verified V8 anonymous archive digest changed")
    if sha(deer_xlsx.read_bytes())!=DEER_SHA:
        raise ValueError("Nature Communications deer Source Data SHA256 drift")
    with zipfile.ZipFile(source_zip) as z:
        names=z.namelist()
        if len(names)<25 or any(x.startswith("/") or ".." in Path(x).parts for x in names):
            raise ValueError("Bad base ZIP file membership/path")
        z.extractall(dest)
    qc=json.loads(pdf_qc.read_text(encoding="utf-8"))
    if (qc.get("status")!="PDF_ALL_PAGE_MECHANICAL_PASS_HUMAN_VISUAL_HOLD"
        or qc.get("pages")!=39
        or qc.get("human_visual_approval") is not False):
        raise ValueError("All-pages PDF QC receipt not admitted")
    save(dest,"data/mule_deer_source_data.xlsx",deer_xlsx.read_bytes(),scan=False)
    for original,new in ORIGINAL_CODE.items():
        text=neutralize((ROOT/original).read_text(encoding="utf-8"))
        save(dest,new,text.encode("utf-8"))
    for original,new in ORIGINAL_FROZEN.items():
        src=(ROOT/original).read_text(encoding="utf-8")
        src=neutralize(src)
        save(dest,new,src.encode("utf-8"))
    verify=neutralize((ROOT/"scripts/verify_amnat_v4_muledeer_replay.py").read_text(encoding="utf-8"))
    save(dest,"scripts/verify_animal.py",verify.encode("utf-8"))
    save(dest,"scripts/reproduce_mule_deer.sh",reproduction_script().encode("utf-8"))
    save(dest,"DEER_SOURCE_DATA_README.md",addendum_readme().encode("utf-8"))
    page_report={
        k:qc[k] for k in ("status","pdf_sha256","pages","embedded_image_xrefs","checks")
    }
    page_report["human_visual_approval"]=False
    save(dest,"qc/PDF_39_PAGE_MECHANICAL_QC.json",
         (json.dumps(page_report,indent=2)+"\n").encode("utf-8"))
    manifest=json.loads((dest/"MANIFEST.json").read_text(encoding="utf-8"))
    manifest.update({
       "status":"V8_AND_DEER_SOURCE_INCLUDED_MULE_DEER_REPLAY_PENDING",
       "mule_deer_published_workbook_sha256":DEER_SHA,
       "mule_deer_source_doi":"10.1038/s41467-023-37750-z",
       "mule_deer_source_license":"CC BY 4.0 with published-source attribution",
       "mule_deer_replay_verified":False,
       "pdf_39_pages_mechanically_passed":True,
       "pdf_39_pages_human_visual_approved":False,
       "anonymous_delivery_link_exists":False,
       "journal_submission_ready":False,
    })
    (dest/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return {
        "status":"DEER_SOURCE_ADDED_REPLAY_PENDING",
        "source_input_sha256":DEER_SHA,
        "original_anonymous_zip_sha256":V8_ARCHIVE_SHA,
        "registered_source_scripts":len(ORIGINAL_CODE),
        "frozen_deer_outcomes":len(ORIGINAL_FROZEN),
        "paper_full_page_human_approved":False,
    }


def finish(dest:Path,output_zip:Path)->dict:
    result_file=dest/"outputs/deer/verified_deer.json"
    result=json.loads(result_file.read_text(encoding="utf-8"))
    if result.get("status")!="MULE_DEER_PUBLISHED_SOURCE_REPRODUCTION_PASS":
        raise ValueError("Mule-deer independent source reproduction not supported")
    manifest=json.loads((dest/"MANIFEST.json").read_text(encoding="utf-8"))
    manifest["status"]="V8_AND_MULE_DEER_SCIENTIFIC_REPLAY_VERIFIED_EDITORIAL_HOLD"
    manifest["mule_deer_replay_verified"]=True
    manifest["anonymous_delivery_link_exists"]=False
    manifest["journal_submission_ready"]=False
    (dest/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    safe_text((dest/"MANIFEST.json").read_text(),"MANIFEST.json")
    save(dest,"qc/MULE_DEER_SOURCE_REPRODUCTION.json",
         (json.dumps(result,indent=2)+"\n").encode("utf-8"))
    # The existing full-source bird replay was proved independently by the
    # earlier immutable candidate; no retrospective biological refitting.
    for f in dest.rglob("*"):
        if f.is_file():
            name=f.relative_to(dest).as_posix()
            if any(bad.casefold() in name.casefold() for bad in FORBIDDEN):
                raise ValueError("Owner identity in reviewer archive filename")
            if f.suffix.lower() in (".md",".json",".py",".sh",".csv",".r",".svg",".txt"):
                safe_text(f.read_text(encoding="utf-8"),name)
    fixed_zip(dest,output_zip)
    return {
      "status":"SOURCE_VERIFIED_V8_AND_DEER_ANONYMOUS_CANDIDATE_EDITORIAL_HOLD",
      "zip_sha256":sha(output_zip.read_bytes()),
      "zip_bytes":output_zip.stat().st_size,
      "zip_files":len([p for p in dest.rglob("*") if p.is_file()]),
      "v8_original_source_analysis_unchanged":True,
      "mule_deer_original_source_analysis_reproduced":True,
      "final_human_visual_approval":False,
      "reviewer_delivery_link_exists":False,
      "journal_submission_ready":False,
    }


def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="stage",required=True)
    first=sub.add_parser("prepare")
    for k in ("base-zip","source-xlsx","pdf-qc","output"):
        first.add_argument("--"+k,type=Path,required=True)
    last=sub.add_parser("finish")
    last.add_argument("--input",type=Path,required=True)
    last.add_argument("--zip",type=Path,required=True)
    last.add_argument("--receipt",type=Path,required=True)
    a=p.parse_args()
    if a.stage=="prepare":
        result=prepare(a.base_zip,a.source_xlsx,a.pdf_qc,a.output)
    else:
        result=finish(a.input,a.zip)
        a.receipt.parent.mkdir(parents=True,exist_ok=True)
        a.receipt.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result))


if __name__=="__main__":
    main()
