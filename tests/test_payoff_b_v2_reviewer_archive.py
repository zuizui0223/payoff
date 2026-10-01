from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_payoff_b_v2_reviewer_archive.py"


def load_module():
    spec = importlib.util.spec_from_file_location("v2_review_archive", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def pass_payload() -> dict:
    return {
        "status": "phase_retention_contrast_gate_pass",
        "gate": {
            "passed": True,
            "direction_passed": True,
            "support_passed": True,
            "lambda_difference_b_minus_a": 0.3,
            "observation": {
                "lambda_a": 0.2,
                "lambda_b": 0.5,
                "p_difference": 0.01,
            },
        },
    }


def access_blocked_payload() -> dict:
    return {
        "status": "phase_retention_contrast_access_blocked",
        "reason_code": "CREDENTIALS_NOT_CONFIGURED",
        "credential_preflight": {
            "date": "2026-09-28",
            "workflow_run": 36372973062,
            "artifact_id": 10950280495,
            "configured": False,
            "credential_route": "none",
            "environmental_values_opened": False,
            "lambda_outcome_opened": False,
        },
    }


def test_preoutcome_reviewer_archive_is_anonymous_and_complete(tmp_path: Path):
    module = load_module()
    out = tmp_path / "review"
    zip_path = tmp_path / "review.zip"

    manifest = module.build(out, zip_path=zip_path)

    assert manifest["outcome_rendered"] is False
    assert manifest["identity_scan_passed"] is True
    assert manifest["raw_empirical_data_redistributed"] is False
    assert manifest["figure_count"] == 7
    assert manifest["python_source_count"] > 10
    assert zip_path.exists()

    main = (out / "manuscript" / "GEB_V2_BLINDED_MAIN.md").read_text(
        encoding="utf-8"
    )
    assert main.startswith(
        "# Information deadlines can desynchronize seasonal interactions "
        "under environmental change"
    )
    assert "Dossman et al., 2023" in main

    required = {
        "manuscript/GEB_V2_BLINDED_MAIN.md",
        "supporting_information/GEB_V2_SUPPORTING_INFORMATION.md",
        "README_REVIEW.md",
        "data/payoff_b_information_deadline_theorem_20260927.json",
        "data/payoff_b_broad_predictive_connectivity_result_20260926.json",
        "data/payoff_b_wigeon_predictive_connectivity_result_20260926.json",
        "data/payoff_b_cross_system_empirical_contract_20260928.json",
        "data/payoff_b_cross_system_information_result_20260928.json",
        "data/payoff_b_pairwise_tracking_bridge_20260929.json",
        "docs/PAYOFF_B_PAIRWISE_TRACKING_BRIDGE_20260929.md",
        "docs/PAYOFF_B_REDSTART_EFFECTIVE_DEADLINE_BRIDGE_20261001.md",
        "scripts/payoff_b_cross_system_information.py",
        "analysis/movement_phenology/payoff_b_predictive_connectivity_amaral.R",
    }
    paths = {row["bundle_path"] for row in manifest["files"]}
    assert required.issubset(paths)

    readme = (out / "README_REVIEW.md").read_text(encoding="utf-8")
    assert "10.5061/dryad.mb4nd" in readme
    assert "10.5061/dryad.v41ns1rxv" in readme
    assert "10.7488/ds/2215" in readme
    assert "10.1038/s41559-018-0543-1" in readme
    assert "10.1111/gcb.14160" in readme
    assert "10.1002/ecy.3938" in readme
    assert "natural D_eff or q_wait" in readme
    assert 'python -m pip install -e ".[test,empirical]"' in readme
    assert "statsmodels>=0.14" in readme
    assert "fails if any are skipped" in readme

    for path in out.rglob("*"):
        if path.is_file():
            module.assert_anonymous(path)


def test_reviewer_archive_is_deterministic(tmp_path: Path):
    module = load_module()
    z1 = tmp_path / "one.zip"
    z2 = tmp_path / "two.zip"

    module.build(tmp_path / "one", zip_path=z1)
    module.build(tmp_path / "two", zip_path=z2)

    assert module.sha256(z1) == module.sha256(z2)


def test_outcome_reviewer_archive_includes_registered_result_only_when_supplied(
    tmp_path: Path,
):
    module = load_module()
    result = tmp_path / "result.json"
    result.write_text(
        json.dumps(pass_payload(), indent=2) + "\n",
        encoding="utf-8",
    )

    out = tmp_path / "outcome"
    manifest = module.build(
        out,
        zip_path=tmp_path / "outcome.zip",
        result_json=result,
    )

    assert manifest["outcome_rendered"] is True
    assert (out / "registered_result" / "registered_phase_retention_result.json").exists()
    assert (out / "registered_result" / "claim_state.json").exists()

    si = (
        out
        / "supporting_information"
        / "GEB_V2_SUPPORTING_INFORMATION.md"
    ).read_text(encoding="utf-8")
    assert "Registered result class: PASS" in si
    assert "PREOUTCOME" not in si


def test_archive_excludes_internal_publication_state_and_author_metadata(tmp_path: Path):
    module = load_module()
    out = tmp_path / "review"
    manifest = module.build(out)

    paths = {row["bundle_path"] for row in manifest["files"]}
    forbidden_paths = {
        "docs/PUBLICATION_STATUS.md",
        "docs/PAYOFF_B_V1_V2_PUBLICATION_RELATION_20260927.md",
        "submission/GEB_V2_TITLE_PAGE_TEMPLATE.md",
        "submission/GEB_V2_COVER_LETTER_PREOUTCOME.md",
    }
    assert paths.isdisjoint(forbidden_paths)

def test_access_blocked_reviewer_archive_is_explicit_and_noninferential(
    tmp_path: Path,
):
    module = load_module()
    result = tmp_path / "access_blocked.json"
    result.write_text(
        json.dumps(access_blocked_payload(), indent=2) + "\n",
        encoding="utf-8",
    )

    out = tmp_path / "blocked"
    manifest = module.build(
        out,
        zip_path=tmp_path / "blocked.zip",
        result_json=result,
    )

    assert manifest["outcome_rendered"] is True
    si = (
        out
        / "supporting_information"
        / "GEB_V2_SUPPORTING_INFORMATION.md"
    ).read_text(encoding="utf-8")
    claim = json.loads(
        (out / "registered_result" / "claim_state.json").read_text(
            encoding="utf-8"
        )
    )
    assert "Registered analysis status: not executed because authenticated source access was unavailable." in si
    assert "Registered result class: ACCESS_BLOCKED" not in si
    assert "not executed" in si
    assert claim["scientific_result"] == "ACCESS_BLOCKED"
    assert claim["executed"] is False
    assert claim["estimable"] is False
    assert claim["access_blocked"] is True
    assert claim["retuning_permitted"] is False

