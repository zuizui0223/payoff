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
    EMAIL_RE,
    FORBIDDEN_PATH_TERMS,
    FORBIDDEN_TEXT_TOKENS,
    build_review_bundle,
    imports_from,
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
        "data/payoff_b_tracking_theory_claim_freeze_20260924.json",
        "data/payoff_b_tracking_theory_framing_amendment_20260925.json",
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
            assert EMAIL_RE.search(text) is None


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


def test_review_bundle_resolves_relative_and_bare_local_imports():
    relative_local, relative_external = imports_from(
        ROOT / "src" / "invasion.py"
    )
    assert ROOT / "src" / "numerical_tolerance.py" in relative_local
    assert "numerical_tolerance" not in relative_external

    bare_local, bare_external = imports_from(
        ROOT / "scripts" / "render_tracking_theory_figures.py"
    )
    assert (
        ROOT / "scripts" / "build_tracking_theory_figure_data.py"
        in bare_local
    )
    assert "build_tracking_theory_figure_data" not in bare_external


def test_review_bundle_declares_current_framing_authority(tmp_path):
    out = tmp_path / "review"
    manifest = build_review_bundle(out, None)
    readme = (out / "README_REVIEW.md").read_text(encoding="utf-8")

    assert manifest["framing_amendment_date"] == "2026-09-25"
    assert (
        manifest["current_framing_authority"]
        == "data/payoff_b_tracking_theory_framing_amendment_20260925.json"
    )
    assert "Framing authority" in readme
    assert "2026-09-24 claim-freeze JSON is retained as provenance" in readme
    assert "2026-09-25 framing amendment is authoritative" in readme
