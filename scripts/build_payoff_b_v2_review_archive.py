#!/usr/bin/env python3
"""Build an anonymous PAYOFF-B V2 reviewer code/data archive.

The archive is deliberately narrower than the repository. It contains only the
code, frozen registrations/receipts, theory notes and deterministic figure
builders needed to audit the information-coordination manuscript. It excludes
author metadata, publication-state bookkeeping, GitHub workflows and private
credentials.

An optional frozen Aikens result may be supplied after adjudication. Before
that, the archive is PREOUTCOME and carries the preregistration only.
"""

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

ENTRY_SCRIPTS = [
    "scripts/build_information_theory_figure_data.py",
    "scripts/render_information_deadlines_figures.py",
    "scripts/payoff_b_information_timing_sweep.py",
    "scripts/payoff_b_bayesian_phase_diagram.py",
    "scripts/audit_broad_predictive_connectivity_dependency.py",
    "scripts/payoff_b_wigeon_predictive_connectivity.py",
    "scripts/payoff_b_cv24c_cue_driver.py",
]

FROZEN_FILES = [
    "data/payoff_b_information_deadline_theorem_20260927.json",
    "data/payoff_b_perfect_information_coordination_trap_20260927.json",
    "data/payoff_b_information_rescue_coalition_theorem_20260927.json",
    "data/payoff_b_bayesian_strict_phase_diagram_20260926.json",
    "data/payoff_b_broad_predictive_connectivity_result_20260926.json",
    "data/payoff_b_wigeon_predictive_connectivity_result_20260926.json",
    "data/payoff_b_flycatcher_social_information_anchor_20260926.json",
    "data/payoff_b_cv24c_cue_driver_result_20260927.json",
    "data/payoff_b_predictive_connectivity_contract_20260926.json",
    "data/aikens2022_lambda_perturbation_registration_20260921.json",
    "data/aikens2022_lambda_outcome_interpretation_contract_20260922.json",
    "theory/INFORMATION_DEADLINE_THEOREM.md",
    "theory/PERFECT_INFORMATION_COORDINATION_TRAP.md",
    "theory/INFORMATION_RESCUE_COALITION_THEOREM.md",
    "docs/PAYOFF_B_CANONICAL_CLAIM_STACK_20260927.md",
]

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
                if module:
                    dependency = base / (module.replace(".", "/") + ".py")
                    if dependency.exists():
                        local.add(dependency)
                else:
                    for alias in node.names:
                        dependency = base / (alias.name.replace(".", "/") + ".py")
                        if dependency.exists():
                            local.add(dependency)
            elif module == "src":
                for alias in node.names:
                    dependency = local_module_path("src." + alias.name, path)
                    if dependency is not None:
                        local.add(dependency)
            elif module:
                dependency = local_module_path(module, path)
                if dependency is not None:
                    local.add(dependency)
                else:
                    external.add(module.split(".")[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                dependency = local_module_path(alias.name, path)
                if dependency is not None:
                    local.add(dependency)
                elif alias.name != "src":
                    external.add(alias.name.split(".")[0])

    external -= set(sys.stdlib_module_names)
    return local, external


def resolve_source_closure(seed_paths: list[str]) -> tuple[list[str], list[str]]:
    pending = [ROOT / path for path in seed_paths]
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
        pending.extend(dep for dep in local if dep not in seen)

    return (
        sorted(str(path.relative_to(ROOT)) for path in seen),
        sorted(external),
    )


def assert_anonymous_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    for token in FORBIDDEN_TEXT_TOKENS:
        if token.lower() in lowered:
            raise ValueError(
                f"identity token {token!r} found in reviewer archive file {path}"
            )
    hit = EMAIL_RE.search(text)
    if hit:
        raise ValueError(
            f"email-like identifier {hit.group(0)!r} found in reviewer archive file {path}"
        )


def copy_file(rel: str, output_dir: Path) -> dict:
    source = ROOT / rel
    if not source.exists():
        raise FileNotFoundError(source)
    target = output_dir / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert_anonymous_text(target)
    return {
        "path": rel,
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


def readme(*, third_party: list[str], aikens_status: str) -> str:
    dependencies = ", ".join(third_party) if third_party else "none"
    return f"""# Anonymous review code and derived evidence

This archive supports the manuscript on information deadlines and seasonal
coordination.

It contains only non-identifying analysis code, exact/synthetic theory,
registered analysis contracts, frozen derived result receipts and deterministic
figure builders. Author names, email addresses, repository-owner identifiers,
publication-state bookkeeping and credentials are excluded.

## Environment

- Python 3.12
- third-party import roots detected from the included entry scripts:
  {dependencies}

## Evidence organization

The archive separates:

1. exact information-deadline and coordination results;
2. strict synthetic network-memory and rescue results;
3. registered broad-bird predictive-connectivity results;
4. the source-backed flycatcher timing-information anchor;
5. the registered wigeon null;
6. the preregistered long-term cue-driver negative gate;
7. the preregistered industrial-development phase-retention test.

Aikens adjudication state in this archive: **{aikens_status}**.

## Reproduction

The included scripts are the manuscript-facing entry points. Frozen JSON files
contain the reported derived values and claim boundaries. Original empirical
source data remain governed by the repositories and publications named in the
manuscript and registrations.

No synthetic parameter value should be interpreted as a natural threshold or
prevalence estimate.

## Double-anonymous boundary

This archive intentionally omits author-controlled title-page material,
acknowledgements, funding, ORCID, correspondence details, repository-owner
identifiers and GitHub Actions metadata.
"""


def build(
    output_dir: Path,
    *,
    zip_path: Path | None = None,
    aikens_result_json: Path | None = None,
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    code_paths, third_party = resolve_source_closure(ENTRY_SCRIPTS)
    source_paths = sorted(set(code_paths + FROZEN_FILES))

    manifest = {
        "status": "payoff_b_v2_anonymous_reviewer_archive",
        "canonical_science_generation": "information_coordination_v2",
        "aikens_gate_resolved": aikens_result_json is not None,
        "aikens_result_included": aikens_result_json is not None,
        "third_party_import_roots": third_party,
        "entry_scripts": ENTRY_SCRIPTS,
        "files": [],
    }

    for rel in source_paths:
        manifest["files"].append(copy_file(rel, output_dir))

    if aikens_result_json is not None:
        payload = json.loads(aikens_result_json.read_text(encoding="utf-8"))
        target = output_dir / "data" / "registered_aikens_phase_retention_result.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
        assert_anonymous_text(target)
        manifest["files"].append(
            {
                "path": str(target.relative_to(output_dir)),
                "source": "provided:frozen registered Aikens result",
                "bytes": target.stat().st_size,
                "sha256": sha256(target),
            }
        )
        aikens_status = str(payload.get("status", "resolved"))
    else:
        aikens_status = "PREOUTCOME — registered result not included"

    readme_path = output_dir / "README_REVIEW.md"
    readme_path.write_text(
        readme(third_party=third_party, aikens_status=aikens_status),
        encoding="utf-8",
    )
    assert_anonymous_text(readme_path)
    manifest["files"].append(
        {
            "path": readme_path.name,
            "source": "generated:anonymous reviewer README",
            "bytes": readme_path.stat().st_size,
            "sha256": sha256(readme_path),
        }
    )

    requirements = output_dir / "requirements-review.txt"
    requirements.write_text(
        "".join(f"{name}\n" for name in third_party),
        encoding="utf-8",
    )
    manifest["files"].append(
        {
            "path": requirements.name,
            "source": "generated:detected import roots",
            "bytes": requirements.stat().st_size,
            "sha256": sha256(requirements),
        }
    )

    manifest["file_count"] = len(manifest["files"])
    manifest["code_file_count"] = sum(
        row["path"].endswith(".py") for row in manifest["files"]
    )

    mp = output_dir / "REVIEW_ARCHIVE_MANIFEST.json"
    mp.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    if zip_path is not None:
        deterministic_zip(output_dir, zip_path)
        manifest["zip_path"] = str(zip_path)
        manifest["zip_bytes"] = zip_path.stat().st_size
        manifest["zip_sha256"] = sha256(zip_path)

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_v2_anonymous_review_archive"),
    )
    parser.add_argument(
        "--zip",
        type=Path,
        default=Path("outputs/PAYOFF_B_V2_ANON_REVIEW_CODE_DATA.zip"),
    )
    parser.add_argument("--aikens-result-json", type=Path)
    args = parser.parse_args()

    manifest = build(
        args.output_dir,
        zip_path=args.zip,
        aikens_result_json=args.aikens_result_json,
    )
    print(
        "PAYOFF_B_V2_REVIEW_ARCHIVE "
        f"files={manifest['file_count']} "
        f"code={manifest['code_file_count']} "
        f"aikens_resolved={manifest['aikens_gate_resolved']} "
        f"zip_sha256={manifest.get('zip_sha256')}"
    )


if __name__ == "__main__":
    main()
