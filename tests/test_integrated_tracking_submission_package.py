from pathlib import Path
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "build_integrated_tracking_submission_package.py"

spec = importlib.util.spec_from_file_location("integrated_package", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_integrated_preoutcome_package_is_deterministic_and_blocked(
    tmp_path: Path,
) -> None:
    out = tmp_path / "package"
    zip_path = tmp_path / "package.zip"

    first = module.build_package(out, zip_path)
    first_hash = first["zip_sha256"]
    second = module.build_package(out, zip_path)

    assert second["zip_sha256"] == first_hash
    assert second["figure_count"] == 6
    assert second["final_submission_eligible"] is False
    assert second["aikens_outcome_opened"] is False

    manifest = json.loads(
        (
            out / "PAYOFF_B_INTEGRATED_PREOUTCOME_PACKAGE_MANIFEST.json"
        ).read_text(encoding="utf-8")
    )
    assert manifest["scientific_state"] == "PREOUTCOME_INTERNAL_READY"
    assert manifest["final_submission_eligible"] is False
    assert manifest["figure_count"] == 6

    anon = (
        out
        / "submission_ready"
        / "PAYOFF_B_INTEGRATED_ANON_MAIN_TEXT_PREOUTCOME.md"
    ).read_text(encoding="utf-8")
    assert "AIKENS LAMBDA RESULT PENDING" in anon
    assert "**Status:**" not in anon
    assert "**Publication architecture:**" not in anon
    assert "zuizui0223" not in anon
    assert "ZHANG" not in anon

    si = (
        out
        / "submission_ready"
        / "PAYOFF_B_INTEGRATED_SUPPORTING_INFORMATION_PREOUTCOME.md"
    ).read_text(encoding="utf-8")
    assert "## S9. Broad 55-species migration-speed falsification" in si
    assert "## S10. Direct phase-control systems and interval scale" in si
    assert "## S11. Environmental-reconstruction reliability" in si
    assert (
        "## S12. Industrial actuation perturbation and preregistered Aikens gate"
        in si
    )
    assert "PREOUTCOME STATE: the Aikens lambda outcome is unopened" in si


def test_integrated_package_contains_templates_and_six_figures(
    tmp_path: Path,
) -> None:
    out = tmp_path / "package"
    module.build_package(out, None)

    ready = out / "submission_ready"
    for name in (
        "PAYOFF_B_INTEGRATED_TITLE_PAGE_TEMPLATE.md",
        "PAYOFF_B_INTEGRATED_COVER_LETTER_TEMPLATE.md",
        "PAYOFF_B_INTEGRATED_DATA_CODE_TEMPLATE.md",
        "PAYOFF_B_INTEGRATED_FIGURE_CAPTIONS.md",
        "PAYOFF_B_INTEGRATED_PACKAGE_INDEX.md",
    ):
        assert (ready / name).exists()

    figures = sorted(
        (out / "figures").glob("PAYOFF_B_INTEGRATED_FIG*.svg")
    )
    assert len(figures) == 6
