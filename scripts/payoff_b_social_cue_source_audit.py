"""PAYOFF-B 2017 Dryad competitor-phenology source-only admission.

No biological response, treatment contrast, density effect, model coefficient,
phenological slope, or fitness endpoint can be read from this program.
Run in an environment with authorised HTTPS access to the public Dryad files.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MANIFEST = Path("data/payoff_b_social_cue_source_manifest_20261011.json")
BASE_HOST = "https://datadryad.org"
USER_AGENT = "PAYOFF-B-source-only-audit/20261011 (+https://github.com/zuizui0223/payoff)"


def validate_manifest(manifest: dict) -> list[dict]:
    if manifest.get("status") != "SOURCE_ONLY_PREOUTCOME":
        raise ValueError("Gate status must remain SOURCE_ONLY_PREOUTCOME")
    if manifest.get("outcome_status") != "UNOPENED":
        raise ValueError("Refusing to reopen outcome")
    names = [
        "arrival_early_late.R", "arrival.csv", "arrorder.csv",
        "population.csv", "replicates.csv", "swaps14.csv", "swaps15.csv"
    ]
    files = manifest["files"]
    if [f["name"] for f in files] != names:
        raise ValueError("Unexpected file names or file order")
    if len({f["file_id"] for f in files}) != len(files):
        raise ValueError("Duplicate registered file ID")
    if any(not (isinstance(f["size"], int) and f["size"] > 0)
           for f in files):
        raise ValueError("Invalid registered byte size")
    return files


def _csv_shape(blob: bytes) -> dict:
    """Structural metadata only: headers + count. Do not expose row values."""
    txt = blob.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    # Published original R code explicitly reads all six data files with
    # read.table(..., sep=";", dec=","). A comma CSV parser would collapse
    # entire original records to a single field and falsely reject the data.
    reader = csv.reader(io.StringIO(txt), delimiter=";", quotechar='"')
    try:
        header = next(reader)
    except StopIteration as exc:
        raise ValueError("CSV empty") from exc
    if len(header) < 2 or not all(h.strip() for h in header):
        raise ValueError("Unusable column header")
    if len(set(header)) != len(header):
        raise ValueError("Duplicate column headers")
    n = 0
    for row in reader:
        if not row:
            continue
        if len(row) != len(header):
            raise ValueError("CSV row/column mismatch")
        n += 1
    if n == 0:
        raise ValueError("CSV has no observations")
    return {"n_rows": n, "n_columns": len(header), "columns": header,
            "delimiter": ";", "decimal_mark": ",",
            "published_reader": "read.table(sep=\";\", dec=\",\")"}


def source_receipt(metadata: dict, blob: bytes, transport_url: str) -> dict:
    name = metadata["name"]
    size = len(blob)
    if size != metadata["size"]:
        raise ValueError(
            f"File-size mismatch for {name}: got {size}, expected {metadata['size']}"
        )
    result = {
        "name": name,
        "id": metadata["file_id"],
        "role": metadata["role"],
        "size": size,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "transport_url": transport_url,
        "metadata_only": True,
    }
    if name.endswith(".csv"):
        result["schema"] = _csv_shape(blob)
    elif name.endswith(".R"):
        # Do not execute downloaded source code or search it for outcomes.
        if not blob.strip():
            raise ValueError("Empty published analysis script")
        result["schema"] = {"extension": ".R", "source_code_executed": False}
    else:
        raise ValueError("Unexpected file type")
    return result


def download(metadata: dict, timeout: int = 30) -> tuple[bytes, str]:
    """Try public Dryad routes only; no credentials or outside substitutes."""
    fid = metadata["file_id"]
    urls = [
        f"{BASE_HOST}/api/v2/files/{fid}/download",
        f"{BASE_HOST}/downloads/file_stream/{fid}",
    ]
    problems = []
    for url in urls:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read(metadata["size"] + 1)
                used = response.geturl()
            if len(data) != metadata["size"]:
                problems.append(f"{url}: wrong byte count {len(data)}")
                continue
            return data, used
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            problems.append(f"{url}: {type(exc).__name__}: {str(exc)[:160]}")
    raise RuntimeError(
        f"SOURCE_ACCESS_BLOCKED: cannot retrieve registered {metadata['name']}: "
        + "; ".join(problems)
    )


def run(manifest: dict, timeout: int = 30) -> dict:
    files = validate_manifest(manifest)
    receipt = {
        "gate_id": manifest["gate_id"],
        "dataset_doi": manifest["dataset_doi"],
        "status": "SOURCE_ONLY_IN_PROGRESS",
        "outcome_opened": False,
        "analysis_outcome_computed": False,
        "files": [],
        "limitations": [
            "Metadata/source access is not proof of a cue independently manipulated from real competition",
            "2019 mortality and 2020 playback datasets are not linked to these records",
            "No fitness or behavioural inference authorised by this source gate",
        ],
    }
    for f in files:
        try:
            blob, url = download(f, timeout=timeout)
            receipt["files"].append(source_receipt(f, blob, url))
        except (RuntimeError, ValueError, UnicodeDecodeError) as exc:
            receipt["files"].append({
                "name": f["name"],
                "id": f["file_id"],
                "status": "SOURCE_ACCESS_BLOCKED" if isinstance(exc, RuntimeError)
                          else "SOURCE_SCHEMA_REVIEW_REQUIRED",
                "reason": str(exc)[:900],
            })
    success = len([f for f in receipt["files"] if f.get("metadata_only")])
    receipt["file_success_n"] = success
    receipt["file_expected_n"] = len(files)
    receipt["status"] = (
        "SOURCE_SCHEMA_PASS_MECHANISM_NOT_IDENTIFIED"
        if success == len(files)
        else "SOURCE_ACCESS_OR_SCHEMA_BLOCKED"
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = run(manifest, timeout=args.timeout)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": result["status"],
        "files": result["file_success_n"],
        "expected": result["file_expected_n"],
        "outcomes_opened": result["outcome_opened"],
        "diagnostics": [
            {"name": item["name"], "status": item["status"],
             "reason": item.get("reason", "")[:220]}
            for item in result["files"] if not item.get("metadata_only")
        ],
    }))
    # Fail-closed: partial files are audit artifacts but not admitted inputs.
    if result["status"] != "SOURCE_SCHEMA_PASS_MECHANISM_NOT_IDENTIFIED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
