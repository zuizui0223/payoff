from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path
from statistics import median


TARGETS = ("SCO7662", "SCO7350", "SCO7036", "SCO3879")
CORE = ("SCO3000", "SCO3300", "SCO3600", "SCO3900", "SCO4200", "SCO4500", "SCO4800", "SCO5100", "SCO5400")


def coverage(bam: Path, ref_name: str, start: str, end: str) -> tuple[float, float]:
    region = f"{ref_name}:{start}-{end}"
    text = subprocess.check_output(["samtools", "coverage", "-r", region, str(bam)], text=True)
    rows = [line for line in text.splitlines() if line and not line.startswith("#")]
    if len(rows) != 1:
        raise ValueError(f"unexpected samtools coverage output for {region}: {text!r}")
    cols = rows[0].split("\t")
    return float(cols[5]), float(cols[6])


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--loci", type=Path, required=True)
    p.add_argument("--controls", type=Path, required=True)
    p.add_argument("--bam-dir", type=Path, required=True)
    p.add_argument("--reference-name", default="NC_003888.3")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    with args.loci.open(encoding="utf-8", newline="") as h:
        loci = {row["legacy_locus"]: row for row in csv.DictReader(h, delimiter="\t")}
    expected = set(TARGETS) | set(CORE)
    if set(loci) != expected:
        raise ValueError(f"locus panel mismatch; missing={sorted(expected-set(loci))}, extra={sorted(set(loci)-expected)}")

    with args.controls.open(encoding="utf-8", newline="") as h:
        controls = list(csv.DictReader(h, delimiter="\t"))
    if not controls:
        raise ValueError("no calibration controls")
    if any(row["candidate_id"] == "M5_T0" for row in controls):
        raise ValueError("M5_T0 is forbidden in calibration controls")

    out = []
    for row in controls:
        cid = row["candidate_id"]
        pac = args.bam_dir / f"{cid}.pacbio.bam"
        bgi = args.bam_dir / f"{cid}.bgi.bam"
        if not pac.exists() or not bgi.exists():
            raise FileNotFoundError(f"missing mapped control BAM for {cid}")

        pac_cov = {}
        for locus in TARGETS:
            x = loci[locus]
            pac_cov[locus] = coverage(pac, args.reference_name, x["start"], x["end"])[0]
        pac_core_cov = pac_cov["SCO3879"]

        core_depths = []
        for locus in CORE:
            x = loci[locus]
            _, depth = coverage(bgi, args.reference_name, x["start"], x["end"])
            core_depths.append(depth)
        baseline = median(core_depths)
        if baseline <= 0:
            raise ValueError(f"non-positive BGI central-core baseline for {cid}")

        for locus in TARGETS:
            x = loci[locus]
            _, depth = coverage(bgi, args.reference_name, x["start"], x["end"])
            out.append({
                "candidate_id": cid,
                "marker": locus,
                "pacbio_marker_coverage_pct": f"{pac_cov[locus]:.12g}",
                "pacbio_core_coverage_pct": f"{pac_core_cov:.12g}",
                "bgi_mean_depth": f"{depth:.12g}",
                "bgi_core_panel_median_depth": f"{baseline:.12g}",
                "bgi_normalized_ratio": f"{depth / baseline:.12g}",
            })

    fields = [
        "candidate_id", "marker", "pacbio_marker_coverage_pct", "pacbio_core_coverage_pct",
        "bgi_mean_depth", "bgi_core_panel_median_depth", "bgi_normalized_ratio",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
