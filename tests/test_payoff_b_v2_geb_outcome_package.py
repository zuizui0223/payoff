from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


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


outcome = load(
    "v2_geb_outcome_package",
    SCRIPTS / "build_payoff_b_v2_geb_outcome_package.py",
)


def payload(result_class: str) -> dict:
    if result_class == "NOT_ESTIMABLE":
        return {
            "status": "phase_retention_contrast_not_estimable",
            "reasons": ["too few fixed-24h transitions"],
        }
    if result_class == "ACCESS_BLOCKED":
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

    if result_class == "PASS":
        passed = True
        direction = True
        support = True
        a, b, p = 0.2, 0.5, 0.01
    elif result_class == "FAIL_WRONG_DIRECTION":
        passed = False
        direction = False
        support = True
        a, b, p = 0.5, 0.2, 0.01
    elif result_class == "FAIL_INSUFFICIENT_SUPPORT":
        passed = False
        direction = True
        support = False
        a, b, p = 0.2, 0.5, 0.20
    else:
        raise ValueError(result_class)

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


def write_payload(tmp_path: Path, result_class: str) -> Path:
    path = tmp_path / f"{result_class}.json"
    path.write_text(
        json.dumps(payload(result_class), indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def file_hash_map(manifest: dict) -> dict[str, str]:
    return {
        row["path"]: row["sha256"]
        for row in manifest["files"]
    }


def test_four_scientific_results_plus_access_blocked_build_v2_packages(tmp_path: Path):
    for result_class in (
        "PASS",
        "FAIL_WRONG_DIRECTION",
        "FAIL_INSUFFICIENT_SUPPORT",
        "NOT_ESTIMABLE",
        "ACCESS_BLOCKED",
    ):
        result_json = write_payload(tmp_path, result_class)
        out = tmp_path / result_class
        zip_path = tmp_path / f"{result_class}.zip"

        manifest = outcome.build(result_json, out, zip_path)

        assert manifest["scientific_result"] == result_class
        expected_state = (
            "OUTCOME_RENDERED_ACCESS_BLOCKED"
            if result_class == "ACCESS_BLOCKED"
            else "OUTCOME_RENDERED_SCIENCE_READY"
        )
        assert manifest["scientific_state"] == expected_state
        if result_class == "ACCESS_BLOCKED":
            assert manifest["final_science_blocker"] is not None
            assert "author decision" in manifest["final_science_blocker"]
        else:
            assert manifest["final_science_blocker"] is None
        assert manifest["final_submission_eligible"] is False
        assert manifest["registered_execution_state_frozen"] is True
        expected_result_frozen = result_class != "ACCESS_BLOCKED"
        assert manifest["registered_result_frozen"] is expected_result_frozen
        assert (
            manifest["registered_scientific_result_available"]
            is expected_result_frozen
        )
        expected_estimable = result_class not in {
            "NOT_ESTIMABLE",
            "ACCESS_BLOCKED",
        }
        assert manifest["phase_retention_estimate_available"] is expected_estimable
        assert manifest["aikens_outcome_opened"] is expected_estimable
        assert manifest["main_text_retuned"] is False
        assert manifest["main_figures_retuned"] is False
        assert manifest["aikens_result_location"] == "Supporting Information only"
        assert manifest["figure_count"] == 7
        assert (out / "GEB_V2_DECLARATIONS_TEMPLATE.md").exists()
        assert "anonymous reviewer archive delivery channel" in manifest["remaining_portal_blockers"]
        cover = (out / "GEB_V2_COVER_LETTER_OUTCOME.md").read_text(encoding="utf-8")
        assert "The theory predicts that **environmental information can recover before" in cover
        assert zip_path.exists()

        main = (out / "GEB_V2_BLINDED_OUTCOME.md").read_text(encoding="utf-8")
        si = (out / "GEB_V2_SUPPORTING_INFORMATION_OUTCOME.md").read_text(
            encoding="utf-8"
        )
        claim = json.loads(
            (out / "GEB_V2_AIKENS_CLAIM_STATE.json").read_text(
                encoding="utf-8"
            )
        )
        audit = json.loads(
            (out / "GEB_V2_OUTCOME_AUDIT.json").read_text(
                encoding="utf-8"
            )
        )

        assert result_class not in main
        normalized_main = " ".join(main.split())
        assert normalized_main.startswith(
            "# Information deadlines can desynchronize seasonal interactions "
            "under environmental change"
        )
        assert "Dossman et al., 2023" in normalized_main
        assert "Raw waiting time therefore does not generally rank effective deadlines" in normalized_main
        assert "Theory predicts that environmental information can recover before ecological coordination does." in normalized_main

        normalized_cover = " ".join(cover.split())
        assert "effective waiting cost" in normalized_cover
        assert "raw waiting duration" in normalized_cover
        assert result_class in si
        assert claim["scientific_result"] == result_class
        assert claim["retuning_permitted"] is False
        if result_class == "ACCESS_BLOCKED":
            assert claim["access_blocked"] is True
            assert claim["executed"] is False
            assert claim["estimable"] is False
            assert "not executed" in si
        else:
            assert claim.get("access_blocked", False) is False
        assert audit["all_outcome_hard_gates_pass"]
        assert "PREOUTCOME" not in si
        assert "remains unopened" not in si


def test_main_text_and_seven_figures_are_identical_across_result_classes(
    tmp_path: Path,
):
    hashes = {}
    for result_class in (
        "PASS",
        "FAIL_WRONG_DIRECTION",
        "FAIL_INSUFFICIENT_SUPPORT",
        "NOT_ESTIMABLE",
        "ACCESS_BLOCKED",
    ):
        result_json = write_payload(tmp_path, result_class)
        manifest = outcome.build(
            result_json,
            tmp_path / f"out_{result_class}",
            tmp_path / f"out_{result_class}.zip",
        )
        mapping = file_hash_map(manifest)
        invariant = {
            path: digest
            for path, digest in mapping.items()
            if path == "GEB_V2_BLINDED_OUTCOME.md"
            or (
                path.startswith("figures/")
                and path.endswith(".svg")
            )
        }
        assert len(invariant) == 8
        hashes[result_class] = invariant

    first = hashes["PASS"]
    for result_class, mapping in hashes.items():
        assert mapping == first, result_class


def test_supporting_information_changes_with_registered_result(tmp_path: Path):
    hashes = {}
    for result_class in (
        "PASS",
        "FAIL_WRONG_DIRECTION",
        "FAIL_INSUFFICIENT_SUPPORT",
        "NOT_ESTIMABLE",
        "ACCESS_BLOCKED",
    ):
        result_json = write_payload(tmp_path, result_class)
        manifest = outcome.build(
            result_json,
            tmp_path / f"si_{result_class}",
            None,
        )
        mapping = file_hash_map(manifest)
        hashes[result_class] = mapping[
            "GEB_V2_SUPPORTING_INFORMATION_OUTCOME.md"
        ]

    assert len(set(hashes.values())) == 5


def test_outcome_zip_is_deterministic_for_same_registered_result(tmp_path: Path):
    result_json = write_payload(tmp_path, "PASS")
    z1 = tmp_path / "one.zip"
    z2 = tmp_path / "two.zip"

    outcome.build(result_json, tmp_path / "one", z1)
    outcome.build(result_json, tmp_path / "two", z2)

    assert outcome.sha256(z1) == outcome.sha256(z2)

def test_activated_access_blocked_clears_author_decision_science_blocker(tmp_path: Path):
    state = ROOT / "data" / "aikens2022_access_blocked_submission_state_20260928.json"
    payload_data = json.loads(state.read_text(encoding="utf-8"))
    assert payload_data["author_decision"]["decision"] == "SUBMIT_WITH_ACCESS_BLOCKED"
    assert payload_data["author_decision"]["scientific_result_claimed"] is False
    assert payload_data["author_decision"]["future_authenticated_execution_permitted"] is True

    out = tmp_path / "activated_access_blocked"
    zip_path = tmp_path / "activated_access_blocked.zip"
    manifest = outcome.build(state, out, zip_path)

    assert manifest["scientific_result"] == "ACCESS_BLOCKED"
    assert manifest["scientific_state"] == "OUTCOME_RENDERED_ACCESS_BLOCKED"
    assert manifest["access_blocked_author_decision_frozen"] is True
    assert manifest["final_science_blocker"] is None
    assert "author decision on registered Aikens ACCESS_BLOCKED state" not in manifest["remaining_portal_blockers"]
    assert manifest["registered_result_frozen"] is False
    assert manifest["registered_scientific_result_available"] is False
    assert manifest["aikens_outcome_opened"] is False
    assert (out / "GEB_V2_TITLE_PAGE_ACCESS_BLOCKED_TEMPLATE.md").exists()
    assert (out / "GEB_V2_DATA_CODE_ACCESS_BLOCKED.md").exists()
    assert (out / "GEB_V2_PORTAL_HANDOFF_ACCESS_BLOCKED.md").exists()
    assert not (out / "GEB_V2_TITLE_PAGE_OUTCOME_TEMPLATE.md").exists()

    access_data = (out / "GEB_V2_DATA_CODE_ACCESS_BLOCKED.md").read_text(
        encoding="utf-8"
    )
    normalized_access_data = " ".join(access_data.split())
    assert "was not executed" in normalized_access_data
    assert "not evidence for or against" in normalized_access_data
    assert "future authenticated execution remains permissible" in normalized_access_data

    claim = json.loads(
        (out / "GEB_V2_AIKENS_CLAIM_STATE.json").read_text(encoding="utf-8")
    )
    assert claim["scientific_result"] == "ACCESS_BLOCKED"
    assert claim["author_decision_frozen"] is True
    assert claim["author_decision"] == "SUBMIT_WITH_ACCESS_BLOCKED"
    assert claim["future_authenticated_execution_permitted"] is True
    assert claim["original_registration_remains_binding"] is True

