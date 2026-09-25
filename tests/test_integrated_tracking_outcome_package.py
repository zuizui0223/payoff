import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

BASELINE = ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"
RENDER_MANUSCRIPT = SCRIPTS / "render_aikens_lambda_manuscript.py"

from render_integrated_tracking_figures import render_all as render_figures
from audit_rendered_integrated_tracking_manuscript import audit as audit_rendered
from build_integrated_tracking_outcome_supporting_information import (
    build_supporting_information as build_outcome_si,
)
from build_integrated_tracking_outcome_package import build_package


def contrast_payload(
    *,
    passed: bool,
    direction: bool = True,
    support: bool = True,
    a: float = 0.2,
    b: float = 0.5,
    p: float = 0.01,
) -> dict:
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
    "pass": contrast_payload(passed=True),
    "wrong_direction": contrast_payload(
        passed=False,
        direction=False,
        support=True,
        a=0.5,
        b=0.2,
    ),
    "insufficient_support": contrast_payload(
        passed=False,
        direction=True,
        support=False,
        p=0.2,
    ),
    "not_estimable": {
        "status": "phase_retention_contrast_not_estimable",
        "reasons": ["too few fixed-24h transitions"],
        "lambda_outcome_opened": False,
    },
}


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("pass", "REGISTERED OUTCOME: PASS"),
        ("wrong_direction", "REGISTERED OUTCOME: FAILED IN DIRECTION"),
        ("insufficient_support", "REGISTERED OUTCOME: INSUFFICIENT SUPPORT"),
        ("not_estimable", "REGISTERED OUTCOME: NOT ESTIMABLE"),
    ],
)
def test_outcome_supporting_information_covers_all_registered_classes(
    tmp_path: Path,
    name: str,
    expected: str,
) -> None:
    result_json = tmp_path / f"{name}.json"
    result_json.write_text(
        json.dumps(CASES[name], indent=2) + "\n",
        encoding="utf-8",
    )
    text = build_outcome_si(result_json)
    assert expected in text
    assert "PREOUTCOME STATE: the Aikens lambda outcome is unopened" not in text
    assert "narrative retuning after outcome inspection: false" in text
    assert "Aikens added to cross-taxon lambda synthesis: false" in text


def render_case(tmp_path: Path, name: str) -> dict:
    payload = CASES[name]
    result_json = tmp_path / f"{name}_result.json"
    rendered = tmp_path / f"{name}_rendered.md"
    claim = tmp_path / f"{name}_claim.json"
    figures = tmp_path / f"{name}_figures"
    audit_json = tmp_path / f"{name}_audit.json"

    result_json.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    run = subprocess.run(
        [
            sys.executable,
            str(RENDER_MANUSCRIPT),
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

    rendered_figures = render_figures(figures, result_json)
    audit = audit_rendered(
        rendered,
        result_json,
        claim,
        rendered_figures["manifest"],
    )
    assert audit["final_submission_science_ready"] is True
    audit_json.write_text(
        json.dumps(audit, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "result": result_json,
        "rendered": rendered,
        "claim": claim,
        "figures": figures,
        "audit": audit_json,
    }


@pytest.mark.parametrize(
    ("name", "expected_opened"),
    [("pass", True), ("not_estimable", False)],
)
def test_outcome_package_builds_for_positive_or_nonestimable_adjudication(
    tmp_path: Path,
    name: str,
    expected_opened: bool,
) -> None:
    case = render_case(tmp_path, name)
    output_dir = tmp_path / f"{name}_package"
    zip_path = tmp_path / f"{name}_package.zip"

    first = build_package(
        manuscript=case["rendered"],
        result_json=case["result"],
        claim_state_json=case["claim"],
        figure_dir=case["figures"],
        postoutcome_audit_json=case["audit"],
        output_dir=output_dir,
        zip_path=zip_path,
    )
    first_hash = first["zip_sha256"]

    second = build_package(
        manuscript=case["rendered"],
        result_json=case["result"],
        claim_state_json=case["claim"],
        figure_dir=case["figures"],
        postoutcome_audit_json=case["audit"],
        output_dir=output_dir,
        zip_path=zip_path,
    )

    assert second["zip_sha256"] == first_hash
    assert second["final_submission_science_ready"] is True
    assert second["portal_metadata_complete"] is False
    assert second["aikens_result_present"] is True
    assert second["aikens_outcome_opened"] is expected_opened
    assert second["figure_count"] == 6

    anon = (
        output_dir
        / "submission_ready"
        / "PAYOFF_B_INTEGRATED_ANON_MAIN_TEXT_OUTCOME_RENDERED.md"
    ).read_text(encoding="utf-8")
    assert "PENDING" not in anon
    assert "OUTCOME-RENDERED" not in anon
    assert "**Publication architecture:**" not in anon

    cover = (
        output_dir
        / "submission_ready"
        / "PAYOFF_B_INTEGRATED_COVER_LETTER_OUTCOME_WORKING.md"
    ).read_text(encoding="utf-8")
    assert "PREOUTCOME NOTE" not in cover
