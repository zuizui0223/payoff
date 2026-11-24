#!/usr/bin/env python3
"""Read six exact published author code notebooks from original GitHub.

Pin each author's Git blob SHA, inspect ONLY code cells (never execute them,
download GPS events, open stork data or examine individual tracks), and emit
aggregate coded-variable evidence. This checks author *code representation*,
not biological absence of social learning or the existence of other data.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.request

SOURCE_REPO="IrisDB/Delayed_migration_white_stork"
PINNED_NOTEBOOKS={
    "1_PrepareData_Python.ipynb":"164ce5602add5c4292214d1ca541b38b234bc87e",
    "2_Analyses_R.ipynb":"ccd38350b918b4e21de0a4b8c2935771ee006779",
    "3a_Figures_Python.ipynb":"5ed2d98c6ed18e8befc4b11deb822b363a15e8b2",
    "3b_Figures_R.ipynb":"79b723bfe7f18630b878444c70f30650ed351541",
    "4a_SupplementaryMaterial_R.ipynb":"35341d4c575da4b48d0c02a6c4bb9d8e853a580f",
    "4b_SupplementaryMaterial_Python.ipynb":"c7cdb90ccc46a6166b8f0bd9cc1c30d4a34c3610",
}
MAX_SIZE=600000
# 'group' is deliberately EXCLUDED from social exposure: Aviary is the
# experimental cohort, not a measured social cue or conspecific encounter.
CUE_PATTERNS={
    "flock":r"\bflock\b|\bflocking\b",
    "social_information":r"social[\s_]*inform(?:ation)?",
    "conspecific":r"\bconspecific",
    "neighbor_proximity":r"neighbou?r|proximity|interindividual|nearest[\s_]*(bird|individual)",
    "social_group_size":r"group[\s_]*size|flock[\s_]*size",
}
PRIOR_ART_VARIABLE_PATTERNS={
    "cohort":r"\bAviary\b",
    "wind":r"WindSupport|WindSpeed|wind[_ -]?support",
    "movement_speed":r"GlidingSpeed|AirSpeed|CrossCountrySpeed|ground.speed",
    "survival_or_death":r"Survival|Death|death",
    "stopover":r"Stopover",
    "temperature":r"Temperature|Temp",
    "date_time":r"Release|timestamp|DOY",
}

def git_blob_sha1(raw:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def audit_notebook(raw:bytes,expected_sha:str):
    got=git_blob_sha1(raw)
    if got != expected_sha:
        raise ValueError("Published author code changed since pinned blob SHA")
    notebook=json.loads(raw)
    if notebook.get("nbformat") not in (3,4):
        raise ValueError("Original code is not a supported notebook")
    cells=[c for c in notebook.get("cells",[]) if c.get("cell_type")=="code"]
    text=["".join(c.get("source",[])) if isinstance(c.get("source"),list) else str(c.get("source",""))
          for c in cells]
    counts=lambda patterns:{key:sum(bool(re.search(pattern,cell,re.IGNORECASE)) for cell in text)
                         for key,pattern in patterns.items()}
    return {
       "git_blob_sha1":got,
       "notebook_code_cell_count":len(cells),
       "explicit_social_cue_terms_in_code_cells":counts(CUE_PATTERNS),
       "already_published_behavioral_variables":counts(PRIOR_ART_VARIABLE_PATTERNS),
       "original_source_code_executed":False,
       "original_data_files_opened":False,
    }

def get_raw_notebook(name,sha):
    if name not in PINNED_NOTEBOOKS or PINNED_NOTEBOOKS[name] != sha:
        raise ValueError("Not one of six fixed original author notebooks")
    url=f"https://raw.githubusercontent.com/{SOURCE_REPO}/main/{name}"
    req=urllib.request.Request(url,headers={
        "Accept":"application/json",
        "User-Agent":"PAYOFF-B-public-archival-author-code-audit/1.0"
    })
    with urllib.request.urlopen(req,timeout=35) as resp:
        data=resp.read(MAX_SIZE+1)
    if len(data)>MAX_SIZE:
        raise ValueError("Original code notebook exceeds source-size bound")
    return data

def audit():
    notebooks={}
    for name,sha in PINNED_NOTEBOOKS.items():
        notebooks[name]=audit_notebook(get_raw_notebook(name,sha),sha)
    cue_counts={key:sum(x["explicit_social_cue_terms_in_code_cells"][key]
                        for x in notebooks.values())
                for key in CUE_PATTERNS}
    original={key:sum(x["already_published_behavioral_variables"][key]
                      for x in notebooks.values())
              for key in PRIOR_ART_VARIABLE_PATTERNS}
    social_code_found=any(cue_counts.values())
    return {
      "status":"AUTHOR_CODE_DIRECT_SOCIAL_CUE_EXPOSURE_NOT_FOUND" if not social_code_found
             else "AUTHOR_CODE_DIRECT_SOCIAL_CUE_TERMS_PRESENT_REQUIRE_MANUAL_VALIDATION",
      "date":"2026-11-24",
      "original_author_repo":SOURCE_REPO,
      "original_article_doi":"10.1098/rspb.2023.1268",
      "exact_file_count":len(notebooks),
      "n_original_code_cells":sum(x["notebook_code_cell_count"] for x in notebooks.values()),
      "files":notebooks,
      "explicit_social_cue_term_code_cell_counts":cue_counts,
      "already_published_variable_code_cell_counts":original,
      "source_code_measured_actual_flock_size_or_information_exposure":False if not social_code_found else None,
      "does_not_rule_out_unpublished_social_data_or_unmeasured_actual_exposure":True,
      "evidence_boundary":"Absence of a coded variable in these six original notebooks does not prove birds lacked social information, only that direct quantified cue exposure is not evidenced by these source analyses.",
      "source_code_executed":False,"tracking_or_individual_data_accessed":False,
      "no_ebird":True,"experimental_fitness_result_reestimated":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    obj=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
    print("PAYOFF_B_STORK_AUTHOR_CODE_AUDIT="+json.dumps(obj,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
