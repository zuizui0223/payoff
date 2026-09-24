import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "manuscript" / "PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V3_PREOUTCOME.md"
RENDER = ROOT / "scripts" / "render_aikens_lambda_manuscript.py"
AUDIT = ROOT / "scripts" / "audit_movement_phenology_geb.py"


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
            "magnitude_passed": True,
            "support_passed": support,
            "lambda_difference_b_minus_a": b - a,
            "registration": {},
            "observation": {
                "lambda_a": a,
                "lambda_b": b,
                "p_difference": p,
            },
            "reasons": [],
        },
    }


CASES = {
    "pass": contrast_payload(passed=True),
    "fail_wrong_direction": contrast_payload(
        passed=False,
        direction=False,
        support=True,
        a=0.5,
        b=0.2,
        p=0.02,
    ),
    "fail_insufficient_support": contrast_payload(
        passed=False,
        direction=True,
        support=False,
        a=0.2,
        b=0.35,
        p=0.20,
    ),
    "not_estimable": {
        "status": "phase_retention_contrast_not_estimable",
        "reasons": ["too few fixed-24h transitions"],
    },
}


@pytest.mark.parametrize("name", tuple(CASES))
def test_every_registered_aikens_outcome_renders_auditable_geb_manuscript(
    tmp_path: Path,
    name: str,
):
    result_path = tmp_path / f"{name}.json"
    rendered = tmp_path / f"{name}.md"
    claim = tmp_path / f"{name}_claim.json"
    audit = tmp_path / f"{name}_audit.json"
    result_path.write_text(
        json.dumps(CASES[name], indent=2) + "\n",
        encoding="utf-8",
    )

    render_run = subprocess.run(
        [
            sys.executable,
            str(RENDER),
            "--baseline",
            str(BASELINE),
            "--result-json",
            str(result_path),
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
    assert render_run.returncode == 0, render_run.stderr

    rendered_text = rendered.read_text(encoding="utf-8")
    assert "AIKENS LAMBDA RESULT PENDING" not in rendered_text
    assert "AIKENS LAMBDA DISCUSSION PENDING" not in rendered_text
    assert "AIKENS LAMBDA ABSTRACT PENDING" not in rendered_text
    assert "AIKENS LAMBDA CONCLUSION PENDING" not in rendered_text

    audit_run = subprocess.run(
        [
            sys.executable,
            str(AUDIT),
            "--manuscript",
            str(rendered),
            "--output",
            str(audit),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert audit_run.returncode == 0, (
        name + "\nSTDOUT:\n" + audit_run.stdout + "\nSTDERR:\n" + audit_run.stderr
    )

    audit_payload = json.loads(audit.read_text(encoding="utf-8"))
    assert audit_payload["all_hard_gates_pass"]
    assert audit_payload["hard_gates"]["aikens_lambda_result_resolved"]
    assert audit_payload["abstract_words"] <= 300
