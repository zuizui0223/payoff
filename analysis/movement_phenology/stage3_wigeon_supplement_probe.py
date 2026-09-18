#!/usr/bin/env python3
"""Extract the HMM/staging contract from the published wigeon supplementary R code."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URL = (
    "https://media.springernature.com/original/springer-static/esm/"
    "art%3A10.1186%2Fs40462-021-00296-0/MediaObjects/"
    "40462_2021_296_MOESM2_ESM.html"
)
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

KEYWORDS = (
    "fitHMM",
    "prepData",
    "Par0",
    "stateNames",
    "viterbi",
    "momentuHMM",
    "step",
    "angle",
    "Weibull",
    "gamma",
    "solar",
    "migration",
    "migratory",
    "dt",
    "50.184",
    "staging",
    "regularise",
    "target.time",
    "sampling frequency",
    "3600",
)


def main():
    r = requests.get(URL, timeout=120)
    r.raise_for_status()
    text = r.text
    soup = BeautifulSoup(text, "html.parser")

    # RMarkdown HTML stores rendered code in <pre><code> blocks.
    blocks = []
    for node in soup.find_all(["pre", "code"]):
        s = node.get_text("\n", strip=False)
        if not s.strip():
            continue
        if any(k.lower() in s.lower() for k in KEYWORDS):
            blocks.append(s)

    # Deduplicate nested code/pre copies while preserving order.
    unique = []
    seen = set()
    for b in blocks:
        norm = "\n".join(line.rstrip() for line in b.splitlines()).strip()
        if norm and norm not in seen:
            seen.add(norm)
            unique.append(norm)

    joined = "\n\n--- BLOCK ---\n\n".join(unique)
    (OUT / "stage3_wigeon_supplement_hmm_blocks.txt").write_text(
        joined + "\n", encoding="utf-8"
    )

    # Also create a line-context audit from all visible text/code.
    raw_lines = soup.get_text("\n").splitlines()
    contexts = []
    for i, line in enumerate(raw_lines):
        if any(k.lower() in line.lower() for k in KEYWORDS):
            lo = max(0, i - 5)
            hi = min(len(raw_lines), i + 10)
            chunk = "\n".join(x for x in raw_lines[lo:hi] if x.strip())
            if chunk not in contexts:
                contexts.append(chunk)

    (OUT / "stage3_wigeon_supplement_hmm_contexts.txt").write_text(
        "\n\n=== CONTEXT ===\n\n".join(contexts) + "\n",
        encoding="utf-8",
    )

    # Compact machine-readable windows around the exact HMM contract tokens.
    contract_tokens = (
        "fitHMM",
        "Par0",
        "stateNames",
        "viterbi",
        "prepData",
        "dist=list",
        "formula",
        "50.184",
        "regularise",
        "target.time",
        "3600",
    )
    joined_lines = joined.splitlines()
    contract_windows = []
    seen_windows = set()
    for i, line in enumerate(joined_lines):
        if any(tok.lower() in line.lower() for tok in contract_tokens):
            lo = max(0, i - 8)
            hi = min(len(joined_lines), i + 24)
            window = "\n".join(joined_lines[lo:hi]).strip()
            if window and window not in seen_windows:
                seen_windows.add(window)
                contract_windows.append(
                    {
                        "trigger_line": line.strip()[:500],
                        "start_line": lo + 1,
                        "end_line": hi,
                        "context": window,
                    }
                )

    contract = {
        "tokens": list(contract_tokens),
        "n_windows": len(contract_windows),
        "windows": contract_windows,
    }
    (OUT / "stage3_wigeon_hmm_contract.json").write_text(
        json.dumps(contract, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    receipt = {
        "url": URL,
        "http_status": r.status_code,
        "content_bytes": len(r.content),
        "n_keyword_blocks": len(unique),
        "n_contexts": len(contexts),
        "n_contract_windows": len(contract_windows),
        "keywords": list(KEYWORDS),
        "claim_ceiling": (
            "Published supplementary-code extraction only; extracted snippets "
            "must be reviewed before porting the HMM contract."
        ),
    }
    (OUT / "stage3_wigeon_supplement_probe.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
