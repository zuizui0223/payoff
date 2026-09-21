#!/usr/bin/env python3
"""Merge full multi-task AppEEARS MOD09Q1/MOD10A2 point-result CSVs."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.appeears_result_merge import (
    discover_product_csvs,
    merge_point_result_csvs,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("download_root", type=Path)
    parser.add_argument(
        "--mod09-output",
        type=Path,
        default=Path("outputs/aikens_full_mod09q1_v061.csv"),
    )
    parser.add_argument(
        "--mod10-output",
        type=Path,
        default=Path("outputs/aikens_full_mod10a2_v061.csv"),
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=Path("outputs/aikens_full_appeears_merge_receipt.json"),
    )
    args = parser.parse_args()

    mod09_files = discover_product_csvs(
        args.download_root,
        "MOD09Q1",
    )
    mod10_files = discover_product_csvs(
        args.download_root,
        "MOD10A2",
    )

    mod09 = merge_point_result_csvs(
        mod09_files,
        product="MOD09Q1.061",
        output_path=args.mod09_output,
    )
    mod10 = merge_point_result_csvs(
        mod10_files,
        product="MOD10A2.061",
        output_path=args.mod10_output,
    )

    receipt = {
        "status": "full_appeears_point_results_merged",
        "download_root": str(args.download_root),
        "MOD09Q1.061": asdict(mod09),
        "MOD10A2.061": asdict(mod10),
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "task-level point-result merge only; no IRG or lambda result"
        ),
    }
    args.receipt_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.receipt_output)
    print(
        "appeears_full_merge "
        f"mod09_files={len(mod09_files)} "
        f"mod09_rows={mod09.rows} "
        f"mod10_files={len(mod10_files)} "
        f"mod10_rows={mod10.rows}"
    )


if __name__ == "__main__":
    main()
