from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

# Allow direct execution as `python scripts/...py` from the repository root.
# This is a transport/import repair only; it does not alter the frozen gate.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.direct_mu_gross_rearrangement_audit import (
    GrossAuditEvidence,
    GrossEvent,
    adjudicate_gross_rearrangement_audit,
)


def load_bins(path: Path):
    with path.open(newline="") as h:
        rows = list(csv.DictReader(h, delimiter="\t"))
    if not rows:
        raise ValueError("empty coverage-bin table")
    return rows


def terminal_boundaries(rows, *, retained_depth: float = 10.0, confirmation_bins: int = 5):
    depths = [float(r["m5_mean_depth"]) for r in rows]
    starts = [int(r["start"]) for r in rows]
    ends = [int(r["end"]) for r in rows]

    def left():
        for i in range(len(depths)):
            if depths[i] >= retained_depth:
                prior = depths[:i]
                confirm = depths[i : i + confirmation_bins]
                if all(x == 0.0 for x in prior) and len(confirm) == confirmation_bins and all(x >= retained_depth for x in confirm):
                    return True, starts[i], i
                return False, None, None
        return False, None, None

    def right():
        for i in range(len(depths) - 1, -1, -1):
            if depths[i] >= retained_depth:
                after = depths[i + 1 :]
                lo = max(0, i - confirmation_bins + 1)
                confirm = depths[lo : i + 1]
                if all(x == 0.0 for x in after) and len(confirm) == confirmation_bins and all(x >= retained_depth for x in confirm):
                    return True, ends[i], i
                return False, None, None
        return False, None, None

    return left(), right()


def internal_zero_tracts(rows, left_i: int, right_i: int, min_bins: int = 5):
    events = []
    run_start = None
    for i in range(left_i, right_i + 2):
        is_zero = i <= right_i and float(rows[i]["m5_mean_depth"]) == 0.0
        if is_zero and run_start is None:
            run_start = i
        if not is_zero and run_start is not None:
            n = i - run_start
            if n >= min_bins:
                start = int(rows[run_start]["start"])
                end = int(rows[i - 1]["end"])
                events.append((start, end))
            run_start = None
    return events


def parse_vcf(path: Path, *, source: str):
    events = []
    if not path.exists():
        raise FileNotFoundError(path)
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) < 8:
            raise ValueError(f"malformed VCF row in {path}: {line!r}")
        pos = int(cols[1])
        info = {}
        for item in cols[7].split(";"):
            if "=" in item:
                k, v = item.split("=", 1)
                info[k] = v
        svtype = info.get("SVTYPE", "SV")
        end = int(info.get("END", pos))
        try:
            svlen = abs(int(float(info.get("SVLEN", end - pos))))
        except ValueError:
            svlen = abs(end - pos)
        if svlen < 50_000:
            continue
        eid = cols[2] if cols[2] != "." else f"{source}_{svtype}_{pos}_{end}"
        events.append(GrossEvent(eid, svtype, svlen, source, True))
    return events


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bins", type=Path, required=True)
    p.add_argument("--m5-vcf", type=Path, required=True)
    p.add_argument("--wt-vcf", type=Path, required=True)
    p.add_argument("--m5-central-depth", type=float, required=True)
    p.add_argument("--wt-central-depth", type=float, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    rows = load_bins(args.bins)
    left, right = terminal_boundaries(rows)
    events = []
    if left[0] and left[1] and left[1] >= 50_000:
        events.append(GrossEvent("LEFT_TERMINAL", "LEFT_TERMINAL_LOSS", left[1], "DEPTH", True))
    chrom_end = int(rows[-1]["end"])
    if right[0] and right[1] is not None and chrom_end - right[1] >= 50_000:
        events.append(GrossEvent("RIGHT_TERMINAL", "RIGHT_TERMINAL_LOSS", chrom_end - right[1], "DEPTH", True))

    if left[0] and right[0]:
        for j, (start, end) in enumerate(internal_zero_tracts(rows, left[2], right[2]), start=1):
            events.append(GrossEvent(f"INTERNAL_ZERO_{j}", "INTERNAL_COPY_LOSS", end - start, "DEPTH", True))

    m5_calls = parse_vcf(args.m5_vcf, source="SNIFFLES_M5")
    wt_calls = parse_vcf(args.wt_vcf, source="SNIFFLES_WT_CONTROL")
    events.extend(m5_calls)

    evidence = GrossAuditEvidence(
        candidate_id="M5_T0",
        target_pacbio_run="SRR16954720",
        wt_control_run="SRR16954715",
        reference_accession="NC_003888.3",
        coverage_bin_bp=10_000,
        gross_event_min_bp=50_000,
        m5_central_depth=args.m5_central_depth,
        wt_central_depth=args.wt_central_depth,
        coverage_segmentation_completed=True,
        left_terminal_boundary_resolved=left[0],
        right_terminal_boundary_resolved=right[0],
        long_read_sv_calling_completed=True,
        wt_control_processed_same_pipeline=True,
        all_detected_gross_events_catalogued=True,
        events=tuple(events),
    )
    result = adjudicate_gross_rearrangement_audit(evidence)
    payload = {
        "receipt_id": "STREPTOMYCES_M5_GROSS_REARRANGEMENT_AUDIT_RESULT_V1",
        "candidate_id": "M5_T0",
        "left_terminal": {"resolved": left[0], "first_retained_coordinate": left[1]},
        "right_terminal": {"resolved": right[0], "last_retained_coordinate": right[1]},
        "m5_central_depth": args.m5_central_depth,
        "wt_central_depth": args.wt_central_depth,
        "m5_gross_sv_call_count": len(m5_calls),
        "wt_gross_sv_call_count": len(wt_calls),
        "event_catalog": [event.__dict__ for event in events],
        "audit_completed": result.audit_completed,
        "gross_secondary_rearrangement_unresolved": result.gross_secondary_rearrangement_unresolved,
        "blockers": list(result.blockers),
        "qualified_d_reference": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(args.output.read_text())


if __name__ == "__main__":
    main()
