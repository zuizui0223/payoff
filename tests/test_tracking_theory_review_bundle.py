import hashlib
import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_tracking_theory_review_bundle import (
    FORBIDDEN_PATH_TERMS,
    FORBIDDEN_TEXT_TOKENS,
    build_review_bundle,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_anonymous_review_bundle_contains_frozen_evidence_and_code(tmp_path):
    out = tmp_path / "review"
    archive = tmp_path / "review.zip"
    manifest = build_review_bundle(out, archive)
    names = {row["bundle_path"] for row in manifest["files"]}

    for required in [
        "data/payoff_b_tracking_synthetic_receipt_20260920.json",
        "data/payoff_b_moving_landscape_receipt_20260920.json",
        "data/payoff_b_2d_connectivity_receipt_20260920.json",
        "data/payoff_b_closed_loop_tracking_receipt_20260920.json",
        "data/payoff_b_movement_feedback_landscape_receipt_20260920.json",
        "theory/MIGRATION_PHENOLOGY_TRACKING.md",
        "theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md",
        "scripts/migration_phenology_2d_coevolution.py",
        "scripts/movement_feedback_landscape_sweep.py",
        "src/spatiotemporal_tracking.py",
        "src/moving_climate_landscape_2d.py",
        "README_REVIEW.md",
    ]:
        assert required in names

    assert manifest["code_file_count"] >= 20
    assert archive.exists()


def test_anonymous_review_bundle_excludes_empirical_programme_and_identity(tmp_path):
    out = tmp_path / "review"
    manifest = build_review_bundle(out, None)

    for row in manifest["files"]:
        lowered_path = row["bundle_path"].lower()
        for term in FORBIDDEN_PATH_TERMS:
            assert term not in lowered_path

        path = out / row["bundle_path"]
        if path.suffix.lower() in {".py", ".md", ".json", ".txt"}:
            text = path.read_text(encoding="utf-8").lower()
            for token in FORBIDDEN_TEXT_TOKENS:
                assert token.lower() not in text
            assert "@" not in text or "@" in "exp[beta (N-1) g_i]"


def test_anonymous_review_bundle_is_byte_stable_across_output_paths(tmp_path):
    first_dir = tmp_path / "one"
    second_dir = tmp_path / "elsewhere" / "two"
    first_zip = tmp_path / "one.zip"
    second_zip = tmp_path / "elsewhere" / "two.zip"

    first = build_review_bundle(first_dir, first_zip)["zip_sha256"]
    second = build_review_bundle(second_dir, second_zip)["zip_sha256"]

    assert first == second
    assert first == digest(first_zip)
    assert second == digest(second_zip)

    with zipfile.ZipFile(second_zip) as archive:
        timestamps = {info.date_time for info in archive.infolist()}
        manifest = json.loads(
            archive.read("OIKOS_TRACKING_ANON_CODE_DATA_MANIFEST.json")
        )
    assert timestamps == {(2026, 9, 24, 0, 0, 0)}
    assert manifest["synthetic_receipt_freeze_date"] == "2026-09-20"
