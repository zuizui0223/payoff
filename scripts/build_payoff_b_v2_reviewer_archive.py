#!/usr/bin/env python3
"""Build deterministic anonymous reviewer archive for canonical PAYOFF-B V2."""

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
ZIP_TIMESTAMP = (2026, 9, 27, 0, 0, 0)

ENTRY_PY = (
    "scripts/build_information_theory_figure_data.py",
    "scripts/render_information_deadlines_figures.py",
    "scripts/payoff_b_bayesian_phase_diagram.py",
    "scripts/payoff_b_information_timing_sweep.py",
    "scripts/payoff_b_shared_cue_deadline_hysteresis.py",
    "scripts/audit_broad_predictive_connectivity_dependency.py",
    "scripts/payoff_b_wigeon_predictive_connectivity.py",
    "scripts/payoff_b_cv24c_cue_driver.py",
    "scripts/build_payoff_b_v2_geb_source.py",
    "scripts/audit_payoff_b_v2_geb_source.py",
    "scripts/build_payoff_b_v2_geb_supporting_information.py",
    "scripts/build_payoff_b_v2_geb_outcome_supporting_information.py",
)

DIRECT_FILES = (
    "pyproject.toml",
    "analysis/movement_phenology/payoff_b_predictive_connectivity_amaral.R",
    "analysis/movement_phenology/payoff_b_predictive_connectivity_amaral_sensitivity.R",
    "data/payoff_b_information_deadline_theorem_20260927.json",
    "data/payoff_b_endogenous_information_timing_result_20260926.json",
    "data/payoff_b_network_information_uptake_theorem_20260927.json",
    "data/payoff_b_perfect_information_coordination_trap_20260927.json",
    "data/payoff_b_information_rescue_coalition_theorem_20260927.json",
    "data/payoff_b_shared_cue_deadline_hysteresis_result_20260927.json",
    "data/payoff_b_bayesian_strict_phase_diagram_20260926.json",
    "data/payoff_b_predictive_connectivity_contract_20260926.json",
    "data/payoff_b_broad_predictive_connectivity_result_20260926.json",
    "data/payoff_b_flycatcher_social_information_anchor_20260926.json",
    "data/payoff_b_wigeon_predictive_connectivity_result_20260926.json",
    "data/payoff_b_cv24c_cue_driver_result_20260927.json",
    "data/payoff_b_tracking_synthetic_receipt_20260920.json",
    "data/payoff_b_moving_landscape_receipt_20260920.json",
    "data/payoff_b_2d_connectivity_receipt_20260920.json",
    "data/payoff_b_closed_loop_tracking_receipt_20260920.json",
    "data/payoff_b_movement_feedback_landscape_receipt_20260920.json",
    "data/aikens2022_lambda_perturbation_registration_20260921.json",
    "data/aikens2022_environment_product_amendment_20260922.json",
    "data/aikens2022_phase_reconstruction_execution_contract_v2_20260922.json",
    "theory/INFORMATION_DEADLINE_THEOREM.md",
    "theory/PERFECT_INFORMATION_COORDINATION_TRAP.md",
    "theory/INFORMATION_RESCUE_COALITION_THEOREM.md",
    "theory/NETWORK_INFORMATION_UPTAKE_THEOREM.md",
    "theory/PARTIAL_INFORMATION_COORDINATION.md",
)

FORBIDDEN_TEXT = (
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


def local_module_path(module: str, importer: Path) -> Path | None:
    if module.startswith("src."):
        candidate = ROOT / (module.replace(".", "/") + ".py")
        return candidate if candidate.exists() else None

    same_dir = importer.parent / (module.replace(".", "/") + ".py")
    if same_dir.exists():
        return same_dir

    scripts_candidate = ROOT / "scripts" / (module.replace(".", "/") + ".py")
    if scripts_candidate.exists():
        return scripts_candidate

    return None


def imports_from(path: Path) -> tuple[set[Path], set[str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    local: set[Path] = set()
    external: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level > 0:
                base = path.parent
                for _ in range(node.level - 1):
                    base = base.parent
                names = [module] if module else [a.name for a in node.names]
                for name in names:
                    candidate = base / (name.replace(".", "/") + ".py")
                    if candidate.exists():
                        local.add(candidate)
                    else:
                        raise FileNotFoundError(
                            f"cannot resolve relative import {name!r} from {path}"
                        )
            elif module == "src":
                for alias in node.names:
                    candidate = local_module_path("src." + alias.name, path)
                    if candidate is None:
                        raise FileNotFoundError(
                            f"cannot resolve src.{alias.name} imported by {path}"
                        )
                    local.add(candidate)
            elif module:
                candidate = local_module_path(module, path)
                if candidate is not None:
                    local.add(candidate)
                else:
                    external.add(module.split(".")[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                candidate = local_module_path(alias.name, path)
                if candidate is not None:
                    local.add(candidate)
                elif alias.name != "src":
                    external.add(alias.name.split(".")[0])

    external -= set(sys.stdlib_module_names)
    return local, external


def resolve_python_closure() -> tuple[list[str], list[str]]:
    pending = [ROOT / rel for rel in ENTRY_PY]
    seen: set[Path] = set()
    external: set[str] = set()

    while pending:
        path = pending.pop()
        if path in seen:
            continue
        if not path.exists():
            raise FileNotFoundError(path)
        seen.add(path)

        local, third_party = imports_from(path)
        external.update(third_party)
        for dependency in local:
            if dependency not in seen:
                pending.append(dependency)

    return (
        sorted(str(path.relative_to(ROOT)) for path in seen),
        sorted(external),
    )


def assert_anonymous(path: Path) -> None:
    if path.suffix.lower() not in {
        ".py", ".r", ".md", ".json", ".txt", ".toml", ".csv", ".yml", ".yaml"
    }:
        return
    text = path.read_text(encoding="utf-8", errors="strict")
    lower = text.casefold()
    for token in FORBIDDEN_TEXT:
        if token.casefold() in lower:
            raise ValueError(
                f"identity token {token!r} found in reviewer file {path}"
            )
    hit = EMAIL_RE.search(text)
    if hit:
        raise ValueError(
            f"email-like identifier {hit.group(0)!r} found in reviewer file {path}"
        )


def copy_one(rel: str, output_dir: Path) -> dict:
    source = ROOT / rel
    if not source.exists():
        raise FileNotFoundError(source)
    target = output_dir / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert_anonymous(target)
    return {
        "bundle_path": rel,
        "source": rel,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def deterministic_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in sorted(p for p in source_dir.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(
                path.relative_to(source_dir).as_posix(),
                date_time=ZIP_TIMESTAMP,
            )
            info.create_system = 3
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def readme(*, outcome_rendered: bool, python_deps: list[str]) -> str:
    state = "outcome-rendered" if outcome_rendered else "PREOUTCOME"
    return f"""# Anonymous reviewer archive — seasonal information coordination

Archive state: **{state}**

This archive contains the code, frozen derived receipts, exact theory sources,
journal-facing blinded manuscript, Supporting Information and deterministic
figures needed to audit the manuscript's reported analyses.

It contains no author names, email addresses, repository-owner identifiers or
author-controlled title-page metadata.

## Core reproducibility entry points

- `scripts/build_information_theory_figure_data.py`
- `scripts/render_information_deadlines_figures.py`
- `scripts/payoff_b_bayesian_phase_diagram.py`
- `scripts/payoff_b_information_timing_sweep.py`
- `analysis/movement_phenology/payoff_b_predictive_connectivity_amaral.R`
- `scripts/payoff_b_wigeon_predictive_connectivity.py`
- `scripts/payoff_b_cv24c_cue_driver.py`

## Software

Python 3.12.

Detected non-standard Python import roots:

{chr(10).join("- " + dep for dep in python_deps) if python_deps else "- none"}

The declared empirical Python environment is also recorded in `pyproject.toml`.

R: the broad-bird scripts use base R plus `mgcv`.

## Source-data boundary

Raw source datasets are not silently redistributed in this archive.

- broad migratory birds: source DOI 10.5061/dryad.ttdz08m6w and frozen source
  commit are encoded in the analysis scripts/contract;
- pied-flycatcher manipulation: paper DOI 10.1111/1365-2656.12640 and Dryad DOI
  10.5061/dryad.bs427 are recorded in the frozen source-backed receipt;
- Eurasian wigeon: the analysis retains the published system and frozen derived
  transition/environment provenance;
- long-term flycatcher selection: the frozen analysis uses the published PLOS
  Supporting Data and public environmental reconstruction.

Where source repositories require their own access terms, reviewers should use
the cited source records; derived result receipts in this archive document the
exact retained analysis state.

## Claim boundary

Exact game-theoretic statements are restricted to the declared models.
Natural-data analyses support separate links of the mechanism. No natural
interaction network is claimed to demonstrate the complete information-loss →
coordination-shift → information-recovery → persistent-state hysteresis sequence.

The registered industrial-development result is {'included in Supporting Information' if outcome_rendered else 'not yet opened; the archive remains PREOUTCOME'}.
"""


def build(
    output_dir: Path,
    *,
    zip_path: Path | None = None,
    result_json: Path | None = None,
) -> dict:
    from build_payoff_b_v2_geb_source import build_source
    from build_payoff_b_v2_geb_supporting_information import (
        build_supporting_information as build_preoutcome_si,
    )
    from render_information_deadlines_figures import render_all

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    python_files, python_deps = resolve_python_closure()
    selected = sorted(set(python_files + list(DIRECT_FILES)))

    manifest = {
        "status": (
            "anonymous_v2_reviewer_archive_outcome"
            if result_json is not None
            else "anonymous_v2_reviewer_archive_preoutcome"
        ),
        "canonical_science": "PAYOFF_B_INFORMATION_COORDINATION_V2",
        "outcome_rendered": result_json is not None,
        "files": [],
    }

    for rel in selected:
        manifest["files"].append(copy_one(rel, output_dir))

    main = output_dir / "manuscript" / "GEB_V2_BLINDED_MAIN.md"
    main.parent.mkdir(parents=True, exist_ok=True)
    main.write_text(build_source(), encoding="utf-8")
    assert_anonymous(main)
    manifest["files"].append(
        {
            "bundle_path": str(main.relative_to(output_dir)),
            "source": "generated:blinded V2 main text",
            "bytes": main.stat().st_size,
            "sha256": sha256(main),
        }
    )

    if result_json is None:
        si_text = build_preoutcome_si()
        claim_state = None
    else:
        from build_payoff_b_v2_geb_outcome_supporting_information import (
            build_supporting_information as build_outcome_si,
        )
        si_text, claim_state = build_outcome_si(result_json)

    si = output_dir / "supporting_information" / "GEB_V2_SUPPORTING_INFORMATION.md"
    si.parent.mkdir(parents=True, exist_ok=True)
    si.write_text(si_text, encoding="utf-8")
    assert_anonymous(si)
    manifest["files"].append(
        {
            "bundle_path": str(si.relative_to(output_dir)),
            "source": "generated:V2 Supporting Information",
            "bytes": si.stat().st_size,
            "sha256": sha256(si),
        }
    )

    if result_json is not None:
        result_target = output_dir / "registered_result" / "registered_phase_retention_result.json"
        result_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(result_json, result_target)
        assert_anonymous(result_target)
        manifest["files"].append(
            {
                "bundle_path": str(result_target.relative_to(output_dir)),
                "source": "provided:frozen registered result",
                "bytes": result_target.stat().st_size,
                "sha256": sha256(result_target),
            }
        )
        claim_target = output_dir / "registered_result" / "claim_state.json"
        claim_target.write_text(
            json.dumps(claim_state, indent=2) + "\n",
            encoding="utf-8",
        )
        assert_anonymous(claim_target)
        manifest["files"].append(
            {
                "bundle_path": str(claim_target.relative_to(output_dir)),
                "source": "generated:registered result claim state",
                "bytes": claim_target.stat().st_size,
                "sha256": sha256(claim_target),
            }
        )

    figures_dir = output_dir / "figures"
    rendered = render_all(figures_dir)
    for index in range(1, 8):
        path = rendered[f"figure_{index}"]
        manifest["files"].append(
            {
                "bundle_path": str(path.relative_to(output_dir)),
                "source": f"generated:figure_{index}",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    fig_manifest = rendered["manifest"]
    manifest["files"].append(
        {
            "bundle_path": str(fig_manifest.relative_to(output_dir)),
            "source": "generated:figure manifest",
            "bytes": fig_manifest.stat().st_size,
            "sha256": sha256(fig_manifest),
        }
    )

    readme_path = output_dir / "README_REVIEW.md"
    readme_path.write_text(
        readme(
            outcome_rendered=result_json is not None,
            python_deps=python_deps,
        ),
        encoding="utf-8",
    )
    assert_anonymous(readme_path)
    manifest["files"].append(
        {
            "bundle_path": readme_path.name,
            "source": "generated:review README",
            "bytes": readme_path.stat().st_size,
            "sha256": sha256(readme_path),
        }
    )

    pyreq = output_dir / "requirements-review-python.txt"
    pyreq.write_text(
        "".join(dep + "\n" for dep in python_deps),
        encoding="utf-8",
    )
    manifest["files"].append(
        {
            "bundle_path": pyreq.name,
            "source": "generated:Python import roots",
            "bytes": pyreq.stat().st_size,
            "sha256": sha256(pyreq),
        }
    )
    rreq = output_dir / "requirements-review-r.txt"
    rreq.write_text("R >= 4\nmgcv\n", encoding="utf-8")
    manifest["files"].append(
        {
            "bundle_path": rreq.name,
            "source": "generated:R requirements",
            "bytes": rreq.stat().st_size,
            "sha256": sha256(rreq),
        }
    )

    manifest["file_count"] = len(manifest["files"])
    manifest["python_source_count"] = len(python_files)
    manifest["python_third_party_import_roots"] = python_deps
    manifest["identity_scan_passed"] = True
    manifest["raw_empirical_data_redistributed"] = False
    manifest["figure_count"] = 7

    manifest_path = output_dir / "PAYOFF_B_V2_ANON_REVIEW_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    assert_anonymous(manifest_path)

    if zip_path is not None:
        deterministic_zip(output_dir, zip_path)
        receipt = {
            "status": "anonymous_v2_reviewer_archive_receipt",
            "outcome_rendered": result_json is not None,
            "manifest_sha256": sha256(manifest_path),
            "zip_file": zip_path.name,
            "zip_bytes": zip_path.stat().st_size,
            "zip_sha256": sha256(zip_path),
            "zip_timestamp": "2026-09-27T00:00:00",
            "identity_scan_passed": True,
        }
        receipt_path = zip_path.parent / "PAYOFF_B_V2_ANON_REVIEW_ARCHIVE_RECEIPT.json"
        receipt_path.write_text(
            json.dumps(receipt, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest["zip_sha256"] = receipt["zip_sha256"]
        manifest["archive_receipt_path"] = str(receipt_path)

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_v2_anonymous_review"),
    )
    parser.add_argument(
        "--zip",
        type=Path,
        default=Path("outputs/PAYOFF_B_V2_ANON_REVIEW.zip"),
    )
    parser.add_argument("--result-json", type=Path)
    args = parser.parse_args()

    manifest = build(
        args.output_dir,
        zip_path=args.zip,
        result_json=args.result_json,
    )
    print(
        "PAYOFF_B_V2_ANON_REVIEW "
        f"files={manifest['file_count']} "
        f"python={manifest['python_source_count']} "
        f"figures={manifest['figure_count']} "
        f"outcome={manifest['outcome_rendered']} "
        f"zip_sha256={manifest.get('zip_sha256')}"
    )


if __name__ == "__main__":
    main()
