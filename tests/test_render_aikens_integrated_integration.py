import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"
RENDER = ROOT / "scripts" / "render_aikens_lambda_manuscript.py"
AUDIT_SCRIPT = ROOT / "scripts" / "audit_rendered_integrated_tracking_manuscript.py"

spec = importlib.util.spec_from_file_location("rendered_audit", AUDIT_SCRIPT)
audit_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit_module)


def contrast_payload(*, passed, direction=True, support=True, a=0.2, b=0.5, p=0.01):
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
    "pass": (contrast_payload(passed=True), True),
    "wrong_direction": (
        contrast_payload(passed=False, direction=False, support=True, a=0.5, b=0.2),
        True,
    ),
    "insufficient_support": (
        contrast_payload(passed=False, direction=True, support=False, p=0.2),
        True,
    ),
    "not_estimable": (
        {
            "status": "phase_retention_contrast_not_estimable",
            "reasons": ["too few fixed-24h transitions"],
            "lambda_outcome_opened": False,
        },
        False,
    ),
}


@pytest.mark.parametrize("name", tuple(CASES))
def test_all_registered_outcomes_render_final_integrated_science稿(
    tmp_path: Path,
    name: str,
) -> None:
    payload, expected_opened = CASES[name]
    result_json = tmp_path / f"{name}.json"
    rendered = tmp_path / f"{name}.md"
    claim = tmp_path / f"{name}_claim.json"
    figure_manifest = tmp_path / f"{name}_figures.json"
    result_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    run = subprocess.run(
        [
            sys.executable,
            str(RENDER),
            "--baseline",
            str(BASELINE),
            "--result-json",
            str(result_json),
            "--output",
            str(rendered),
            "--claim-state-output",
            str(claim),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr

    figure_manifest.write_text(
        json.dumps(
            {
                "aikens_result_present": True,
                "aikens_outcome_opened": expected_opened,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    audit = audit_module.audit(rendered, result_json, claim, figure_manifest)
    assert audit["all_postoutcome_hard_gates_pass"] is True
    assert audit["final_submission_science_ready"] is True
    assert audit["aikens_lambda_outcome_opened"] is expected_opened

    rendered_text = rendered.read_text(encoding="utf-8")
    assert "OUTCOME-RENDERED" in rendered_text
    assert "PENDING" not in rendered_text
