import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_aikens_lambda_manuscript import (
    ABSTRACT_END,
    ABSTRACT_START,
    CONCLUSION_END,
    CONCLUSION_START,
    DISCUSSION_END,
    DISCUSSION_START,
    RESULTS_END,
    RESULTS_START,
    render_blocks,
    replace_between,
)

PACKAGE = ROOT / "scripts" / "build_geb_integrated_outcome_package.py"

spec = importlib.util.spec_from_file_location("geb_outcome_package", PACKAGE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def payload(*, passed=True, direction=True, support=True, a=0.2, b=0.5, p=0.01):
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
            "lambda_difference_b_minus_a": b - a,
            "observation": {
                "lambda_a": a,
                "lambda_b": b,
                "p_difference": p,
            },
        },
    }


CASES = {
    "PASS": payload(passed=True),
    "FAIL_WRONG_DIRECTION": payload(
        passed=False, direction=False, support=True, a=0.5, b=0.2, p=0.02
    ),
    "FAIL_INSUFFICIENT_SUPPORT": payload(
        passed=False, direction=True, support=False, a=0.2, b=0.35, p=0.2
    ),
    "NOT_ESTIMABLE": {
        "status": "phase_retention_contrast_not_estimable",
        "reasons": ["too few fixed-24h transitions"],
        "lambda_outcome_opened": False,
    },
}


def render_integrated(tmp_path: Path, name: str, data: dict):
    baseline = (
        ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"
    ).read_text(encoding="utf-8")
    results, discussion, abstract, conclusion, claim = render_blocks(data)
    text = replace_between(baseline, RESULTS_START, RESULTS_END, results)
    text = replace_between(text, DISCUSSION_START, DISCUSSION_END, discussion)
    text = replace_between(text, ABSTRACT_START, ABSTRACT_END, abstract)
    text = replace_between(text, CONCLUSION_START, CONCLUSION_END, conclusion)
    text = text.replace(
        "**Status:** integrated ecology manuscript v1, PREOUTCOME",
        "**Status:** integrated ecology manuscript v1, OUTCOME-RENDERED",
        1,
    )

    manuscript = tmp_path / f"{name}.md"
    result_json = tmp_path / f"{name}.json"
    claim_json = tmp_path / f"{name}_claim.json"
    manuscript.write_text(text, encoding="utf-8")
    result_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    claim.update(
        {
            "result_source": str(result_json),
            "baseline_manuscript": "test baseline",
            "retuning_permitted": False,
            "aikens_added_to_cross_taxon_lambda_synthesis": False,
        }
    )
    claim_json.write_text(json.dumps(claim, indent=2) + "\n", encoding="utf-8")
    return manuscript, result_json, claim_json


@pytest.mark.parametrize("name", tuple(CASES))
def test_all_registered_aikens_classes_build_science_ready_geb_source(
    tmp_path: Path, name: str
) -> None:
    manuscript, result_json, claim_json = render_integrated(
        tmp_path, name, CASES[name]
    )
    out = tmp_path / f"out_{name}"
    zip_path = tmp_path / f"{name}.zip"
    m = module.build(manuscript, result_json, claim_json, out, zip_path)
    assert m["scientific_state"] == "OUTCOME_RENDERED_SCIENCE_READY"
    assert m["scientific_result"] == name
    assert m["final_science_blocker"] is None
    assert m["final_submission_eligible"] is False
    assert m["figure_count"] == 6
    assert m["structured_abstract_words"] <= 300
    assert m["main_body_words"] <= 5000
    assert zip_path.exists()

    audit = json.loads(
        (out / "GEB_INTEGRATED_OUTCOME_AUDIT.json").read_text(encoding="utf-8")
    )
    assert audit["all_outcome_hard_gates_pass"] is True
    source = (out / "GEB_INTEGRATED_BLINDED_OUTCOME.md").read_text(encoding="utf-8")
    assert "PENDING" not in source


def test_geb_outcome_package_is_deterministic(tmp_path: Path) -> None:
    manuscript, result_json, claim_json = render_integrated(
        tmp_path, "pass_det", CASES["PASS"]
    )
    z1 = tmp_path / "one.zip"
    z2 = tmp_path / "two.zip"
    module.build(manuscript, result_json, claim_json, tmp_path / "one", z1)
    module.build(manuscript, result_json, claim_json, tmp_path / "two", z2)
    assert module.sha256(z1) == module.sha256(z2)
