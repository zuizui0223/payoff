#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path

import pandas as pd
import requests

FILES = [
    ("arrival_early_late.R", 34678, "code"),
    ("arrival.csv", 34672, "data"),
    ("arrorder.csv", 34677, "data"),
    ("population.csv", 34676, "data"),
    ("replicates.csv", 34675, "data"),
    ("swaps14.csv", 34673, "data"),
    ("swaps15.csv", 34674, "data"),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_file(session: requests.Session, file_id: int) -> tuple[bytes | None, dict]:
    urls = [
        f"https://datadryad.org/api/v2/files/{file_id}/download",
        f"https://datadryad.org/stash/downloads/file_stream/{file_id}",
    ]
    diag = {"attempts": []}
    for url in urls:
        try:
            r = session.get(url, timeout=120, allow_redirects=True)
            rec = {
                "url": url,
                "final_url": r.url,
                "status_code": r.status_code,
                "content_type": r.headers.get("content-type"),
                "bytes": len(r.content),
                "prefix": r.content[:80].decode("utf-8", errors="replace"),
            }
            diag["attempts"].append(rec)
            if r.status_code == 200 and r.content and b"<html" not in r.content[:500].lower():
                return r.content, diag
        except Exception as e:
            diag["attempts"].append({"url": url, "error": repr(e)})
    return None, diag


def inspect_csv(data: bytes) -> dict:
    last = None
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            df = pd.read_csv(io.BytesIO(data), encoding=enc)
            break
        except Exception as e:
            last = repr(e)
    else:
        return {"parse_error": last}
    low = {}
    for c in df.columns:
        n = int(df[c].nunique(dropna=True))
        if n <= 30:
            low[str(c)] = [str(x) for x in df[c].dropna().unique()[:40]]
    return {
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "dtypes": {str(c): str(df[c].dtype) for c in df.columns},
        "low_cardinality": low,
        "head": df.head(5).where(pd.notna(df), None).to_dict(orient="records"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 PAYOFF-B reproducibility probe",
        "Accept": "*/*",
    })
    result = {
        "result_id": "payoff_b_e2_decision_time_source_probe_20260929",
        "status": "SOURCE_PROBE",
        "files": {},
    }
    acquired = 0
    for name, file_id, typ in FILES:
        data, diag = get_file(session, file_id)
        row = {"file_id": file_id, "type": typ, "diagnostics": diag}
        if data is not None:
            acquired += 1
            row["status"] = "ACQUIRED"
            row["bytes"] = len(data)
            row["sha256"] = sha256_bytes(data)
            if typ == "data":
                row["inspection"] = inspect_csv(data)
            else:
                txt = data.decode("utf-8", errors="replace")
                row["inspection"] = {
                    "lines": len(txt.splitlines()),
                    "first_120_lines": "\n".join(txt.splitlines()[:120]),
                }
        else:
            row["status"] = "BLOCKED"
        result["files"][name] = row

    result["summary"] = {
        "required_files": len(FILES),
        "acquired": acquired,
        "blocked": len(FILES) - acquired,
        "all_acquired": acquired == len(FILES),
    }
    result["status"] = "SOURCE_BYTES_ACQUIRED" if acquired == len(FILES) else "SOURCE_ACCESS_BLOCKED"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
