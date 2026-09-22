#!/usr/bin/env python3
"""Build an identity-scrubbed reviewer snapshot for the GEB manuscript.

The archive contains only the movement-phenology submission lane. It excludes
Git history, unrelated PAYOFF modules, raw tracking data, title-page metadata,
and author-owned repository links. Public data are reacquired from source
repositories by the included scripts when a full reconstruction is needed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "outputs/movement_phenology/reviewer_snapshot"
ARCHIVE = ROOT / "outputs/movement_phenology/GEB_REVIEWER_SNAPSHOT.zip"
READINESS = ROOT / "docs/MOVEMENT_PHENOLOGY_GEB_READINESS.md"

FILES = [
    "manuscript/PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V2.md",
    "scripts/build_movement_phenology_macro_figures.py",
    "scripts/audit_movement_phenology_figures.py",
    "data/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_REGISTRY.csv",
    "data/MOVEMENT_PHENOLOGY_PHASE_UNCERTAINTY_REGISTRY.csv",
    "data/MOVEMENT_PHENOLOGY_INDUSTRIAL_PERMEABILITY_REGISTRY.csv",
    "docs/MOVEMENT_PHENOLOGY_STAGE1_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_MULE_DEER_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_SVALBARD_DIRECT_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_BARNACLE_MULTIFLYWAY_DIRECT_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_WIGEON_DIRECT_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_PHASE_CONTRACTION_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_PHASE_UNCERTAINTY_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_INDUSTRIAL_MULE_DEER_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_BISON_ENDOGENEITY_RECEIPT.md",
    "docs/MOVEMENT_PHENOLOGY_SYSTEMATIC_NOVELTY_SEARCH_20260920.md",
    "docs/MOVEMENT_PHENOLOGY_FLAGSHIP_NOVELTY_AUDIT.md",
    "theory/MOVEMENT_PHENOLOGY_PHASE_FEEDBACK.md",
    "theory/MOVEMENT_PHENOLOGY_STEP_CONTROLLER.md",
    "theory/MOVEMENT_PHENOLOGY_PHASE_INNOVATION.md",
    "theory/MOVEMENT_PHENOLOGY_FEEDFORWARD_FEEDBACK.md",
]

DIRECTORIES = ["analysis/movement_phenology"]
TEST_GLOB = "tests/test_movement_phenology_*.py"
EXCLUDE_BASENAMES = {"__pycache__", ".DS_Store"}

IDENTITY_PATTERNS = {
    "author_name": re.compile(r"\bZHANG\s+RUIQI\b|\bRuiqi\s+Zhang\b|張瑞琪", re.I),
    "author_repo": re.compile(r"github\.com/zuizui0223|\bzuizui0223\b", re.I),
    "author_email": re.compile(r"rachelzhang0223|@(?:gmail|outlook|qq)\.com", re.I),
    "absolute_home": re.compile(r"(?:/home/[^/\s]+|[A-Za-z]:\\Users\\[^\\\s]+)"),
}
SECRET_PATTERNS = {
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "openai_key": re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "generic_secret": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[=:]\s*['\"][^'\"]{12,}['\"]"
    ),
}

README = """# Anonymous reviewer reproduction snapshot

This snapshot accompanies the blinded movement-phenology manuscript.

It intentionally contains no Git history, title page, author metadata, raw GPS
data, private credentials, or author-owned repository link.

Included:
- blinded manuscript source;
- movement-phenology analysis and reconstruction scripts;
- promoted derived registries used by the synthesis figures;
- source/claim receipts for promoted results;
- theory notes defining phase-retention coordinates;
- movement-phenology tests;
- figure audit and reproducibility scripts.

Original GPS, environmental and source-data archives remain at their cited
public repositories/DOIs. Acquisition scripts document and reconstruct promoted
analyses where source licences and endpoints permit.

Minimal figure reproduction:
1. install packages from requirements-reviewer.txt;
2. run scripts/build_movement_phenology_macro_figures.py;
3. run scripts/audit_movement_phenology_figures.py;
4. verify the blinded manuscript against the supplied claim receipts.

Figure 4 and Figure 5 use only included derived registries.

The manuscript does not claim a universal migration speed, universal
phase-retention coefficient, common reactive actuator across taxa, or novelty
for generic AR/control mathematics. Negative prospective results are retained.
"""

REQUIREMENTS = """numpy>=1.26
pandas>=2.1
scipy>=1.11
matplotlib>=3.8
requests>=2.31
statsmodels>=0.14
scikit-learn>=1.3
beautifulsoup4>=4.12
pyproj>=3.6
pytest>=8.0
"""


def all_source_paths() -> list[Path]:
    paths: list[Path] = []
    for rel in FILES:
        p = ROOT / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        paths.append(p)
    for rel in DIRECTORIES:
        base = ROOT / rel
        for p in sorted(base.rglob("*")):
            if p.is_file() and not any(x in p.parts for x in EXCLUDE_BASENAMES):
                paths.append(p)
    paths.extend(sorted(ROOT.glob(TEST_GLOB)))
    unique: dict[str, Path] = {}
    for p in paths:
        unique[p.relative_to(ROOT).as_posix()] = p
    return [unique[k] for k in sorted(unique)]


def scan_text(rel: str, text: str) -> list[dict]:
    hits = []
    for kind, pattern in {**IDENTITY_PATTERNS, **SECRET_PATTERNS}.items():
        for match in pattern.finditer(text):
            hits.append(
                {"file": rel, "kind": kind, "match": match.group(0)[:120]}
            )
    return hits


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def deterministic_zip(source_dir: Path, target: Path) -> None:
    if target.exists():
        target.unlink()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(source_dir.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(source_dir).as_posix()
            info = zipfile.ZipInfo(rel)
            info.date_time = (2026, 9, 21, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())


def refresh_manifest() -> None:
    rows = []
    for p in sorted(BUILD.rglob("*")):
        if p.is_file() and p.name != "MANIFEST_SHA256.txt":
            rows.append(f"{sha256(p)}  {p.relative_to(BUILD).as_posix()}")
    (BUILD / "MANIFEST_SHA256.txt").write_text(
        "\n".join(rows) + "\n", encoding="utf-8"
    )


def main() -> None:
    readiness = READINESS.read_text(encoding="utf-8")
    science_hold = (
        "SCIENCE HOLD" in readiness
        or "SCIENCE / CLAIM CEILING:\n  HOLD" in readiness
    )
    if science_hold:
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        if ARCHIVE.exists():
            ARCHIVE.unlink()
        receipt = {
            "status": "BLOCKED_SCIENCE_HOLD",
            "archive_created": False,
            "readiness_source": str(READINESS.relative_to(ROOT)),
            "reason": (
                "GEB science gate is on hold pending source-backed lambda "
                "measurement-error calibration"
            ),
        }
        receipt_path = (
            ROOT
            / "outputs/movement_phenology/reviewer_snapshot_receipt.json"
        )
        receipt_path.write_text(
            json.dumps(receipt, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(receipt, indent=2))
        return

    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    identity_hits = []
    copied = []
    for src in all_source_paths():
        rel = src.relative_to(ROOT)
        target = BUILD / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        copied.append(rel.as_posix())

        if src.suffix.lower() in {
            ".py", ".r", ".md", ".txt", ".csv", ".json", ".yml", ".yaml"
        }:
            text = src.read_text(encoding="utf-8", errors="replace")
            identity_hits.extend(scan_text(rel.as_posix(), text))

    (BUILD / "README_REVIEWER.md").write_text(README, encoding="utf-8")
    (BUILD / "requirements-reviewer.txt").write_text(
        REQUIREMENTS, encoding="utf-8"
    )
    identity_hits.extend(scan_text("README_REVIEWER.md", README))
    identity_hits.extend(scan_text("requirements-reviewer.txt", REQUIREMENTS))

    if identity_hits:
        (BUILD / "SNAPSHOT_AUDIT.json").write_text(
            json.dumps(
                {"status": "FAIL", "identity_or_secret_hits": identity_hits},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        raise SystemExit(
            "Reviewer snapshot identity/secret audit failed:\n"
            + json.dumps(identity_hits[:20], indent=2)
        )

    audit = {
        "status": "PASS",
        "source_files_copied": len(copied),
        "identity_or_secret_hits": [],
        "raw_tracking_data_included": False,
        "git_history_included": False,
        "title_page_included": False,
        "public_author_repo_link_included": False,
    }
    (BUILD / "SNAPSHOT_AUDIT.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8"
    )
    refresh_manifest()

    deterministic_zip(BUILD, ARCHIVE)
    archive_sha = sha256(ARCHIVE)
    receipt = {
        **audit,
        "n_files": len([p for p in BUILD.rglob("*") if p.is_file()]),
        "archive": str(ARCHIVE.relative_to(ROOT)),
        "archive_sha256": archive_sha,
        "manifest": str((BUILD / "MANIFEST_SHA256.txt").relative_to(ROOT)),
    }
    receipt_path = ROOT / "outputs/movement_phenology/reviewer_snapshot_receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
