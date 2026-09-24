#!/usr/bin/env python3
"""Build an anonymous synthetic-theory code/data review bundle for Oikos."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 9, 24, 0, 0, 0)

ENTRY_SCRIPTS = [
    "scripts/migration_phenology_phase_sweep.py",
    "scripts/migration_phenology_coevolution_sweep.py",
    "scripts/migration_phenology_population_barrier_sweep.py",
    "scripts/migration_phenology_population_stress_sweep.py",
    "scripts/migration_phenology_finite_occupancy.py",
    "scripts/migration_phenology_drift_escape.py",
    "scripts/migration_phenology_moving_landscape.py",
    "scripts/migration_phenology_landscape_frontier.py",
    "scripts/migration_phenology_landscape_coevolution.py",
    "scripts/migration_phenology_landscape_gate_audit.py",
    "scripts/migration_phenology_boundary_robustness.py",
    "scripts/migration_phenology_stochastic_landscape_validation.py",
    "scripts/migration_phenology_2d_corridor.py",
    "scripts/migration_phenology_2d_zigzag.py",
    "scripts/migration_phenology_2d_bypass_capacity.py",
    "scripts/migration_phenology_2d_coevolution.py",
    "scripts/migration_phenology_2d_gate_audit.py",
    "scripts/migration_phenology_2d_overlap_sensitivity.py",
    "scripts/migration_phenology_2d_partner_asymmetry.py",
    "scripts/migration_phenology_2d_anisotropy.py",
    "scripts/closed_loop_tracking_phase_sweep.py",
    "scripts/movement_feedback_landscape_sweep.py",
]

UTILITY_SCRIPTS = [
    "scripts/build_tracking_theory_figure_data.py",
    "scripts/render_tracking_theory_figures.py",
    "scripts/build_tracking_theory_supporting_information.py",
]

FROZEN_FILES = [
    "data/payoff_b_tracking_theory_claim_freeze_20260924.json",
    "data/payoff_b_tracking_synthetic_receipt_20260920.json",
    "data/payoff_b_moving_landscape_receipt_20260920.json",
    "data/payoff_b_2d_connectivity_receipt_20260920.json",
    "data/payoff_b_closed_loop_tracking_receipt_20260920.json",
    "data/payoff_b_movement_feedback_landscape_receipt_20260920.json",
    "docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md",
    "docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md",
    "docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md",
    "docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md",
    "docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md",
    "theory/MIGRATION_PHENOLOGY_TRACKING.md",
    "theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md",
    "submission/PAYOFF_B_TRACKING_PARAMETER_TABLE.md",
    "submission/PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md",
]

FORBIDDEN_PATH_TERMS = (
    "aikens",
    "wigeon",
    "barnacle",
    "mule_deer",
    "tracking_empirical",
    "phase_retention_observation",
)

FORBIDDEN_TEXT_TOKENS = (
    "zuizui0223",
    "ZHANG RUIQI",
    "rachelzhang0223",
    "github.com/zuizui0223",
)

EMAIL_RE = re.compile(
    r"(?i)(?<![A-Z0-9._%+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def module_path(module: str) -> Path | None:
    if not module.startswith("src."):
        return None
    candidate = ROOT / (module.replace(".", "/") + ".py")
    return candidate if candidate.exists() else None


def imports_from(path: Path) -> tuple[set[str], set[str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    local: set[str] = set()
    external: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("src."):
                local.add(module)
            elif module == "src":
                for alias in node.names:
                    local.add("src." + alias.name)
            elif module and node.level == 0:
                external.add(module.split(".")[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("src."):
                    local.add(alias.name)
                elif alias.name != "src":
                    external.add(alias.name.split(".")[0])

    external -= set(sys.stdlib_module_names)
    return local, external


def resolve_source_closure(seed_paths: list[str]) -> tuple[list[str], list[str]]:
    pending = [ROOT / path for path in seed_paths]
    seen_paths: set[Path] = set()
    external: set[str] = set()

    while pending:
        path = pending.pop()
        if path in seen_paths:
            continue
        if not path.exists():
            raise FileNotFoundError(path)
        seen_paths.add(path)

        local_modules, third_party = imports_from(path)
        external.update(third_party)
        for module in sorted(local_modules):
            dependency = module_path(module)
            if dependency is None:
                raise FileNotFoundError(
                    f"cannot resolve local module {module!r} imported by {path}"
                )
            if dependency not in seen_paths:
                pending.append(dependency)

    relative = sorted(str(path.relative_to(ROOT)) for path in seen_paths)
    return relative, sorted(external)


def assert_review_safe_source_paths(paths: list[str]) -> None:
    for path in paths:
        lowered = path.lower()
        for term in FORBIDDEN_PATH_TERMS:
            if term in lowered:
                raise ValueError(
                    f"empirical/post-freeze path not allowed in anonymous review bundle: {path}"
                )


def assert_anonymous_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    for token in FORBIDDEN_TEXT_TOKENS:
        if token.lower() in lowered:
            raise ValueError(
                f"identity token {token!r} found in anonymous review file {path}"
            )
    email = EMAIL_RE.search(text)
    if email:
        raise ValueError(
            f"email-like identifier {email.group(0)!r} found in anonymous review file {path}"
        )


def copy_source(source_rel: str, output_dir: Path) -> dict:
    source = ROOT / source_rel
    if not source.exists():
        raise FileNotFoundError(source)
    target = output_dir / source_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert_anonymous_text(target)
    return {
        "bundle_path": source_rel,
        "source": source_rel,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def write_deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(source_dir).as_posix()
            info = zipfile.ZipInfo(relative, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def review_readme(entry_scripts: list[str], third_party: list[str]) -> str:
    dependency_note = (
        ", ".join(third_party)
        if third_party
        else "none; the included scientific code uses the Python standard library"
    )
    lines = [
        "# Anonymous review code and synthetic data",
        "",
        "This bundle contains the code and frozen synthetic outputs supporting the manuscript",
        "'Tracking together or failing apart: space-time substitution, finite temporal buffering, and coordination barriers under moving environments.'",
        "",
        "The bundle is restricted to the synthetic tracking-theory programme. It excludes the separate empirical phase-retention programme and contains no author names, email addresses, repository-owner identifiers, or private data.",
        "",
        "## Environment",
        "",
        "- Python 3.12",
        f"- third-party imports detected by static analysis: {dependency_note}",
        "",
        "## Frozen evidence",
        "",
        "All manuscript numerical claims are restricted to the five JSON result receipts dated 2026-09-20. Human-readable result summaries and the two core theory documents are included alongside them.",
        "",
        "## Reproduction entry points",
        "",
    ]
    lines.extend(f"- {path}" for path in entry_scripts)
    lines += [
        "",
        "Run any entry point with --help to inspect its declared design arguments. The frozen receipt files record the retained outputs and workflow/artifact provenance used by the manuscript. The figure-data and Supporting Information builders are also included.",
        "",
        "## Claim boundary",
        "",
        "The supplied parameter values and barrier frequencies are synthetic design quantities. They are not calibrated natural climate thresholds, natural prevalence estimates, or named-species parameter estimates.",
        "",
    ]
    return "\n".join(lines)


def build_review_bundle(output_dir: Path, zip_path: Path | None = None) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    code_paths, third_party = resolve_source_closure(
        ENTRY_SCRIPTS + UTILITY_SCRIPTS
    )
    all_source_paths = sorted(set(code_paths + FROZEN_FILES))
    assert_review_safe_source_paths(all_source_paths)

    manifest = {
        "status": "anonymous_synthetic_tracking_review_bundle",
        "synthetic_receipt_freeze_date": "2026-09-20",
        "scientific_freeze_date": "2026-09-24",
        "entry_scripts": ENTRY_SCRIPTS,
        "utility_scripts": UTILITY_SCRIPTS,
        "third_party_import_roots": third_party,
        "files": [],
    }

    for source_rel in all_source_paths:
        manifest["files"].append(copy_source(source_rel, output_dir))

    readme_path = output_dir / "README_REVIEW.md"
    readme_path.write_text(
        review_readme(ENTRY_SCRIPTS, third_party),
        encoding="utf-8",
    )
    assert_anonymous_text(readme_path)
    manifest["files"].append({
        "bundle_path": readme_path.name,
        "source": "generated:review_readme",
        "bytes": readme_path.stat().st_size,
        "sha256": sha256(readme_path),
    })

    requirements_path = output_dir / "requirements-review.txt"
    requirements_path.write_text(
        "".join(f"{name}\n" for name in third_party),
        encoding="utf-8",
    )
    manifest["files"].append({
        "bundle_path": requirements_path.name,
        "source": "generated:requirements",
        "bytes": requirements_path.stat().st_size,
        "sha256": sha256(requirements_path),
    })

    manifest["file_count"] = len(manifest["files"])
    manifest["code_file_count"] = len(
        [row for row in manifest["files"] if row["bundle_path"].endswith(".py")]
    )

    manifest_path = output_dir / "OIKOS_TRACKING_ANON_CODE_DATA_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    if zip_path is not None:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        if zip_path.exists():
            zip_path.unlink()
        write_deterministic_zip(output_dir, zip_path)
        receipt = {
            "status": "anonymous_synthetic_tracking_review_archive_receipt",
            "package_manifest": manifest_path.name,
            "package_manifest_sha256": sha256(manifest_path),
            "zip_file": zip_path.name,
            "zip_bytes": zip_path.stat().st_size,
            "zip_sha256": sha256(zip_path),
            "zip_timestamp": "2026-09-24T00:00:00",
        }
        receipt_path = (
            zip_path.parent
            / "OIKOS_TRACKING_ANON_CODE_DATA_ARCHIVE_RECEIPT.json"
        )
        receipt_path.write_text(
            json.dumps(receipt, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest["archive_receipt_path"] = str(receipt_path)
        manifest["zip_sha256"] = receipt["zip_sha256"]

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/oikos_tracking_anonymous_review_bundle"),
    )
    parser.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        default=Path("outputs/OIKOS_TRACKING_ANON_CODE_DATA.zip"),
    )
    args = parser.parse_args()
    manifest = build_review_bundle(args.output_dir, args.zip_path)
    print(args.output_dir / "OIKOS_TRACKING_ANON_CODE_DATA_MANIFEST.json")
    print(
        "anonymous_review_bundle "
        f"files={manifest['file_count']} "
        f"code_files={manifest['code_file_count']} "
        f"zip_sha256={manifest.get('zip_sha256', 'none')}"
    )


if __name__ == "__main__":
    main()
