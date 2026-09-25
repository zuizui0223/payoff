from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SCRIPT = ROOT / "scripts" / "build_integrated_tracking_submission_package.py"

spec = importlib.util.spec_from_file_location("integrated_package", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_integrated_submission_package_builds_complete_preoutcome_bundle(tmp_path: Path) -> None:
    out = tmp_path / "package"
    zip_path = tmp_path / "package.zip"
    review_zip = tmp_path / "review.zip"
    manifest = module.build_submission_package(out, zip_path, review_zip)

    assert manifest["scientific_state"] == "PREOUTCOME_INTERNAL_READY"
    assert manifest["aikens_lambda_outcome_opened"] is False
    assert manifest["figure_count"] == 6
    assert manifest["final_science_blocker"] == "registered Aikens fixed-24h lambda adjudication"
    assert zip_path.exists()
    assert review_zip.exists()
    assert (out / "submission_ready" / "PAYOFF_B_INTEGRATED_TRACKING_SUPPORTING_INFORMATION_V1.md").exists()
    assert (out / "figures" / "PAYOFF_B_INTEGRATED_FIG6_INFORMATION_ACTUATION.svg").exists()


def test_integrated_anonymous_review_bundle_has_no_identity_leak(tmp_path: Path) -> None:
    out = tmp_path / "review"
    zip_path = tmp_path / "review.zip"
    manifest = module.build_anonymous_review_bundle(out, zip_path)
    assert zip_path.exists()
    assert manifest["figure_count"] == 6
    assert all(not rows for rows in manifest["identity_scan"].values())
    assert manifest["aikens_lambda_outcome_opened"] is False


def test_integrated_submission_zip_is_deterministic(tmp_path: Path) -> None:
    out1 = tmp_path / "one"
    out2 = tmp_path / "two"
    zip1 = tmp_path / "one.zip"
    zip2 = tmp_path / "two.zip"
    module.build_submission_package(out1, zip1)
    module.build_submission_package(out2, zip2)
    assert module.sha256(zip1) == module.sha256(zip2)
