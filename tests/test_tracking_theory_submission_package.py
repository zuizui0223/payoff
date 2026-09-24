import hashlib
import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_tracking_theory_submission_package import build_package


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_tracking_submission_package_builds_with_manifest(tmp_path):
    output_dir = tmp_path / "package"
    zip_path = tmp_path / "tracking.zip"
    manifest = build_package(output_dir, zip_path)

    assert manifest["scientific_freeze_date"] == "2026-09-24"
    assert manifest["synthetic_receipt_freeze_date"] == "2026-09-20"
    assert manifest["figure_count"] == 6
    assert manifest["file_count"] == 34
    assert zip_path.exists()
    assert manifest["zip_sha256"] == digest(zip_path)

    receipt_path = Path(manifest["archive_receipt_path"])
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    package_manifest = output_dir / "PAYOFF_B_TRACKING_SUBMISSION_MANIFEST.json"
    assert receipt["zip_sha256"] == digest(zip_path)
    assert receipt["package_manifest_sha256"] == digest(package_manifest)
    assert receipt["zip_timestamp"] == "2026-09-24T00:00:00"

    for row in manifest["files"]:
        path = output_dir / row["bundle_path"]
        assert path.exists(), row
        assert path.stat().st_size == row["bytes"]
        assert digest(path) == row["sha256"]


def test_tracking_submission_package_contains_core_files(tmp_path):
    output_dir = tmp_path / "package"
    zip_path = tmp_path / "tracking.zip"
    build_package(output_dir, zip_path)

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())

    assert "submission_ready/PAYOFF_B_TRACKING_THEORY_V1.md" in names
    assert "submission_ready/PAYOFF_B_TRACKING_REFERENCES.bib" in names
    assert "submission_ready/OIKOS_TRACKING_HANDOFF_V1.md" in names
    assert "internal_contracts/payoff_b_tracking_theory_claim_freeze_20260924.json" in names
    assert "theory/MIGRATION_PHENOLOGY_TRACKING.md" in names
    assert len([name for name in names if name.startswith("figures/") and name.endswith(".svg")]) == 6


def test_tracking_submission_package_excludes_later_empirical_programme(tmp_path):
    output_dir = tmp_path / "package"
    manifest = build_package(output_dir, None)
    sources = "\n".join(row["source"].lower() for row in manifest["files"])

    assert "aikens" not in sources
    assert "wigeon" not in sources
    assert "barnacle" not in sources
    assert "phase_retention_observation" not in sources


def test_tracking_submission_zip_is_byte_stable(tmp_path):
    output_dir = tmp_path / "package"
    zip_path = tmp_path / "tracking.zip"

    first = build_package(output_dir, zip_path)["zip_sha256"]
    second = build_package(output_dir, zip_path)["zip_sha256"]

    assert first == second
    assert first == digest(zip_path)

    with zipfile.ZipFile(zip_path) as archive:
        timestamps = {info.date_time for info in archive.infolist()}
    assert timestamps == {(2026, 9, 24, 0, 0, 0)}
