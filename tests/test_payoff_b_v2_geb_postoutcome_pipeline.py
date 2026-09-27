import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


supporting = load(
    "v2_postoutcome_supporting",
    SCRIPTS / "build_payoff_b_v2_geb_postoutcome_supporting_information.py",
)
package = load(
    "v2_postoutcome_package",
    SCRIPTS / "build_payoff_b_v2_geb_postoutcome_package.py",
)


def contrast_payload(
    *,
    passed: bool,
    direction: bool = True,
    support: bool = True,
    lambda_a: float = 0.25,
    lambda_b: float = 0.50,
    p_difference: float = 0.01,
):
    return {
        "status": (
            "phase_retention_contrast_gate_pass"
            if passed
            else "phase_retention_contrast_gate_fail"
        ),
        "gate": {
            "passed": passed,
            "direction_passed": direction,
            "support_passed": support,
            "lambda_difference_b_minus_a": lambda_b - lambda_a,
            "observation": {
                "lambda_a": lambda_a,
                "lambda_b": lambda_b,
                "p_difference": p_difference,
            },
        },
    }


CASES = {
    "pass": contrast_payload(passed=True),
    "wrong_direction": contrast_payload(
        passed=False,
        direction=False,
        support=True,
        lambda_a=0.50,
        lambda_b=0.25,
        p_difference=0.02,
    ),
    "insufficient_support": contrast_payload(
        passed=False,
        direction=True,
        support=False,
        lambda_a=0.25,
        lambda_b=0.40,
        p_difference=0.20,
    ),
    "not_estimable": {
        "status": "phase_retention_contrast_not_estimable",
        "reasons": ["registered reconstruction or sample-support gate failed"],
        "lambda_outcome_opened": False,
    },
}

EXPECTED_CLASSES = {
    "pass": "PASS",
    "wrong_direction": "FAIL_WRONG_DIRECTION",
    "insufficient_support": "FAIL_INSUFFICIENT_SUPPORT",
    "not_estimable": "NOT_ESTIMABLE",
}


@pytest.mark.parametrize("name", tuple(CASES))
def test_v2_postoutcome_supporting_information_renders_registered_class(name):
    text, claim = supporting.render_supporting_information(CASES[name])

    assert claim["scientific_result"] == EXPECTED_CLASSES[name]
    assert claim["render_surface"] == "V2 Supporting Information only"
    assert claim["main_text_changed_by_result"] is False
    assert claim["figures_changed_by_result"] is False
    assert claim["title_changed_by_result"] is False
    assert claim["structured_abstract_changed_by_result"] is False
    assert claim["retuning_permitted"] is False

    assert "Registered industrial-development supplement — pending" not in text
    assert "remains unopened at this PREOUTCOME stage" not in text
    assert f"Frozen outcome class: **{EXPECTED_CLASSES[name]}**" in text
    assert "The Aikens result does not enter the cross-taxon lambda synthesis" in text


def build_case(tmp_path: Path, name: str):
    result = tmp_path / f"{name}.json"
    result.write_text(
        json.dumps(CASES[name], indent=2) + "\n",
        encoding="utf-8",
    )
    out = tmp_path / f"{name}_package"
    zip_path = tmp_path / f"{name}.zip"
    manifest = package.build(
        out,
        result_json=result,
        zip_path=zip_path,
    )
    return manifest, out, zip_path


def test_all_outcome_classes_leave_main_and_figures_identical(tmp_path):
    manifests = {}
    supporting_hashes = {}

    for name in CASES:
        manifest, out, zip_path = build_case(tmp_path, name)
        manifests[name] = manifest
        supporting_hashes[name] = package.sha256(
            out / "GEB_V2_SUPPORTING_INFORMATION_POSTOUTCOME.md"
        )

        assert zip_path.exists()
        assert manifest["aikens_result_class"] == EXPECTED_CLASSES[name]
        assert manifest["aikens_result_surface"] == "Supporting Information only"
        assert manifest["retuning_permitted"] is False
        assert manifest["outcome_invariance"]["title_changed"] is False
        assert manifest["outcome_invariance"]["structured_abstract_changed"] is False
        assert manifest["outcome_invariance"]["main_text_changed"] is False
        assert manifest["outcome_invariance"]["figures_changed"] is False
        assert manifest["figure_count"] == 7
        assert manifest["final_submission_eligible"] is False
        assert manifest["final_submission_blockers"] == [
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
        ]

    main_hashes = {
        m["outcome_invariance"]["main_sha256"]
        for m in manifests.values()
    }
    figure_hashes = {
        m["outcome_invariance"]["figure_manifest_sha256"]
        for m in manifests.values()
    }

    assert len(main_hashes) == 1
    assert len(figure_hashes) == 1
    assert len(set(supporting_hashes.values())) == len(CASES)


@pytest.mark.parametrize("name", tuple(CASES))
def test_v2_postoutcome_zip_is_deterministic(tmp_path, name):
    result = tmp_path / f"{name}.json"
    result.write_text(
        json.dumps(CASES[name], indent=2) + "\n",
        encoding="utf-8",
    )

    z1 = tmp_path / f"{name}_one.zip"
    z2 = tmp_path / f"{name}_two.zip"
    package.build(
        tmp_path / f"{name}_one",
        result_json=result,
        zip_path=z1,
    )
    package.build(
        tmp_path / f"{name}_two",
        result_json=result,
        zip_path=z2,
    )

    assert package.sha256(z1) == package.sha256(z2)


def test_postoutcome_package_contains_no_preoutcome_pending_marker(tmp_path):
    manifest, out, _ = build_case(tmp_path, "pass")

    assert manifest["scientific_state"] == "POSTOUTCOME_INTERNAL_READY"
    assert manifest["aikens_outcome_opened"] is True

    main = (out / "GEB_V2_BLINDED_POSTOUTCOME.md").read_text(
        encoding="utf-8"
    )
    supporting_text = (
        out / "GEB_V2_SUPPORTING_INFORMATION_POSTOUTCOME.md"
    ).read_text(encoding="utf-8")

    assert "AIKENS LAMBDA RESULT PENDING" not in main
    assert "Registered industrial-development supplement — pending" not in supporting_text
    assert "UNOPENED" not in supporting_text
