#!/usr/bin/env python3
"""Build an anonymous reproducibility bundle for PAYOFF-B V4.5 review.

The bundle contains only analysis scripts, contracts, frozen figure data,
selected tests, and an anonymized README that map directly to the manuscript.
It excludes author metadata, repository URLs that identify the submitting
authors, unrelated project history, and internal publication-status ledgers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    # Bird primary and diagnostics
    "analysis/movement_phenology/payoff_b_v8_admission_gate.R",
    "analysis/movement_phenology/payoff_b_v8_primary.R",
    "analysis/movement_phenology/payoff_b_v8_metric_scale_diagnostic.R",
    "analysis/movement_phenology/payoff_b_v8_information_value_baseline_sensitivity.R",
    "analysis/movement_phenology/payoff_b_v8_information_value_transfer_diagnostic.R",
    "analysis/movement_phenology/payoff_b_v8_signal_arrival_window_diagnostic.R",
    "analysis/movement_phenology/payoff_b_v8_signed_mismatch_diagnostic.R",
    "analysis/movement_phenology/payoff_b_v8_source_stage_access_diagnostic.R",
    "analysis/movement_phenology/payoff_b_v8_stagewise_phase_transition.R",
    "analysis/movement_phenology/payoff_b_v8_stagewise_measurement_uncertainty.R",
    "analysis/movement_phenology/payoff_b_v8_stagewise_retention_identifiability.R",
    "analysis/movement_phenology/payoff_b_v8_stagewise_subset_representativeness.R",
    "analysis/movement_phenology/payoff_b_v8_source_rank_sensitivity.R",
    "analysis/movement_phenology/payoff_b_v8_source_event_observability_audit.R",

    # Mule-deer source-data reanalysis
    "scripts/payoff_b_ortega_variance_funnel.py",
    "scripts/payoff_b_mule_deer_two_clock_channel.py",
    "scripts/payoff_b_mule_deer_readiness_source_data.py",

    # Contracts / frozen figure data
    "data/payoff_b_ortega_variance_funnel_contract_20261003.json",
    "data/payoff_b_mule_deer_two_clock_channel_contract_20261003.json",
    "data/payoff_b_v45_figure_data_20261006.json",

    # Renderer / audit tests used for manuscript figures
    "scripts/render_payoff_b_v45_main_figures.py",
    "tests/test_payoff_b_v45_main_figures.py",
    "tests/test_ortega_variance_funnel_result.py",
    "tests/test_mule_deer_two_clock_channel.py",
]

FORBIDDEN_IDENTIFIERS = (
    "zuizui0223",
    "ZHANG Ruiqi",
    "張瑞琪",
    "れいちぇる",
)

FIXED_ZIP_TIME = (2026, 10, 6, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_checked(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8")
    bad = [x for x in FORBIDDEN_IDENTIFIERS if x.lower() in text.lower()]
    if bad:
        raise ValueError(f"identity-bearing text in {src}: {bad}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    entries = sorted(p for p in source_dir.rglob("*") if p.is_file())
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in entries:
            info = zipfile.ZipInfo(p.relative_to(source_dir).as_posix(), FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())


def build(output_dir: Path, zip_path: Path) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    missing = [rel for rel in FILES if not (ROOT / rel).exists()]
    if missing:
        raise FileNotFoundError(f"missing required files: {missing}")

    copied = []
    for rel in FILES:
        src = ROOT / rel
        dst = output_dir / rel
        copy_checked(src, dst)
        copied.append(dst)

    readme = output_dir / "README_REVIEW.txt"
    readme.write_text(
        """Anonymous reproducibility bundle for the manuscript
"Seasonal tracking depends on information access and opportunities for correction"

EVIDENCE CLASSES
1. The source-destination correlation contrast was prospectively specified.
2. Metric-scale, forecast-value, observability, signed-timing, transfer and
   stagewise bird analyses were designed after the primary correlation outcome
   was known and must be treated as posthoc diagnostics.
3. The mule-deer compensation phenomenon was published previously; bundled
   scripts re-express the public source data on the signed phase scale used in
   the manuscript.

EXTERNAL SOURCE DATA
A. Migratory birds
   Amaral BR, Youngflesh C, Tingley MW, Miller DAW (2025),
   Diversity and Distributions 31:e70033, doi:10.1111/ddi.70033.
   The analyses use the public final.rds source dataset fixed to source-project
   commit 62c58d77c2028bd863dfe3697b0d9cf29ceaeab0.

B. Mule deer
   Ortega AC et al. (2023), Nature Communications 14:2008,
   doi:10.1038/s41467-023-37750-z.
   The bundled source-data scripts use the public supplementary source workbook
   associated with that article.

MAIN BIRD ANALYSIS ORDER
1. payoff_b_v8_admission_gate.R
2. payoff_b_v8_primary.R
3. payoff_b_v8_metric_scale_diagnostic.R
4. baseline / source-rank / observability / signed-timing diagnostics
5. transfer and stagewise sensitivity scripts

IMPORTANT INTERPRETATION
The empirical G_CV quantity is a finite-sample, restricted-model
cross-validation contrast. It is an operational analyst forecast-value proxy,
not organismal value of information. The source-event observability audit shows
that reconstructed source mid-green-up was not consistently an online event
before the population front reached the mapped source stage.

SOFTWARE
Bird analyses are written in base R.
Mule-deer reanalyses are Python scripts using the dependencies declared by the
project environment and/or standard scientific Python stack.

FIGURES
data/payoff_b_v45_figure_data_20261006.json freezes the numeric values used by
scripts/render_payoff_b_v45_main_figures.py.
""",
        encoding="utf-8",
    )
    copied.append(readme)

    manifest = {
        "status": "anonymous_review_reproducibility_bundle",
        "date": "2026-10-06",
        "file_count": len(copied),
        "files": {
            p.relative_to(output_dir).as_posix(): {
                "sha256": sha256(p),
                "bytes": p.stat().st_size,
            }
            for p in sorted(copied)
        },
    }
    mp = output_dir / "MANIFEST.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    deterministic_zip(output_dir, zip_path)
    return {"manifest": mp, "zip": zip_path, "file_count": len(copied)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_v45_reproducibility"),
    )
    ap.add_argument(
        "--zip",
        type=Path,
        default=Path("outputs/payoff_b_v45_reproducibility.zip"),
    )
    args = ap.parse_args()
    result = build(args.output_dir, args.zip)
    print(result["manifest"])
    print(result["zip"])
    print(f"files={result['file_count']}")


if __name__ == "__main__":
    main()
