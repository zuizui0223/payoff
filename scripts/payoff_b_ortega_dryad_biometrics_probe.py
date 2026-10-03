#!/usr/bin/env python3
"""Probe Ortega et al. 2023 public Dryad CSV for readiness variables.

Transport/schema audit only.  No inferential model is fitted here.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import urllib.request
from pathlib import Path


DEFAULT_URL = "https://datadryad.org/downloads/file_stream/2189257"
EXPECTED_SHA256 = "9c6bf95c11ed9e09c2a26be3cb6d47d93d79569101ad91de7ba748c79aaebf4c"

CANDIDATES = (
    "id",
    "year",
    "body",
    "mass",
    "fat",
    "rump",
    "ifb",
    "condition",
    "preg",
    "fetal",
    "age",
    "start",
    "depart",
    "migration",
    "dfp",
    "timing",
)


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default=DEFAULT_URL)
    ap.add_argument("--output",type=Path,default=Path("outputs/payoff_b_ortega_dryad_biometrics_probe.json"))
    args=ap.parse_args()

    req=urllib.request.Request(
        args.url,
        headers={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130 Safari/537.36",
            "Accept":"text/csv,text/plain,*/*",
            "Referer":"https://datadryad.org/dataset/doi:10.5061/dryad.8kprr4xsj",
        },
    )
    receipt={
        "date":"2026-10-03",
        "status":"UNOPENED",
        "url":args.url,
        "expected_sha256":EXPECTED_SHA256,
        "frozen_submission_affected":False,
    }
    try:
        with urllib.request.urlopen(req,timeout=60) as res:
            raw=res.read()
            receipt["http_status"]=getattr(res,"status",None)
            receipt["resolved_url"]=res.geturl()
            receipt["content_type"]=res.headers.get("Content-Type")
    except Exception as exc:
        receipt["status"]="DOWNLOAD_FAILED"
        receipt["error"]=f"{type(exc).__name__}: {exc}"
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(receipt,indent=2))
        return

    receipt["bytes"]=len(raw)
    sha=hashlib.sha256(raw).hexdigest()
    receipt["sha256"]=sha
    if sha != EXPECTED_SHA256:
        receipt["status"]="SHA_MISMATCH_OR_NONCSV"
        receipt["preview"]=raw[:500].decode("utf-8",errors="replace")
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(receipt,indent=2))
        return

    text=raw.decode("utf-8-sig")
    rows=list(csv.DictReader(io.StringIO(text)))
    headers=list(rows[0].keys()) if rows else []
    candidate_headers=[
        h for h in headers
        if any(term in h.lower() for term in CANDIDATES)
    ]
    preview=[]
    for row in rows[:8]:
        preview.append({h:row.get(h) for h in candidate_headers})

    nonmissing={}
    for h in candidate_headers:
        vals=[row.get(h,"").strip() for row in rows]
        nonmissing[h]=sum(v not in {"","NA","NaN","nan"} for v in vals)

    receipt.update({
        "status":"DOWNLOADED_AND_PARSED",
        "row_count":len(rows),
        "headers":headers,
        "candidate_headers":candidate_headers,
        "candidate_nonmissing_counts":nonmissing,
        "candidate_preview":preview,
    })
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    main()
