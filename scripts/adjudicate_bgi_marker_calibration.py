from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.direct_mu_bgi_response_blind_calibration import (  # noqa: E402
    CalibrationPair,
    calibrate_bgi_marker_thresholds,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Adjudicate response-blind non-M5 BGI marker calibration")
    parser.add_argument("input_tsv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    with args.input_tsv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    pairs = [
        CalibrationPair(
            candidate_id=row["candidate_id"],
            marker=row["marker"],
            pacbio_marker_coverage_pct=float(row["pacbio_marker_coverage_pct"]),
            pacbio_core_coverage_pct=float(row["pacbio_core_coverage_pct"]),
            bgi_normalized_ratio=float(row["bgi_normalized_ratio"]),
        )
        for row in rows
    ]
    result = calibrate_bgi_marker_thresholds(pairs)
    payload = {
        "receipt_id": "STREPTOMYCES_M5_BGI_MARKER_CALIBRATION_RESULT_V1",
        "target_candidate_id": "M5_T0",
        "target_data_used": False,
        "calibration_qualified": result.calibration_qualified,
        "absence_max_ratio": result.absence_max_ratio,
        "presence_min_ratio": result.presence_min_ratio,
        "absent_pair_count": result.absent_pair_count,
        "present_pair_count": result.present_pair_count,
        "absent_candidate_count": result.absent_candidate_count,
        "present_candidate_count": result.present_candidate_count,
        "unresolved_pair_count": result.unresolved_pair_count,
        "blockers": list(result.blockers),
        "m5_bgi_marker_class_opened": False,
        "qualified_d_reference_count_increment": 0,
        "architecture_specific_inference_open": False,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
