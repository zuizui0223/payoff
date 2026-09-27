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


package = load(
    "v2_postoutcome_package",
    SCRIPTS / "build_payoff_b_v2_geb_postoutcome_package.py",
)
supporting = load(
    "v2_postoutcome_si",
    SCRIPTS / "build_payoff_b_v2_geb_postoutcome_supporting_information.py",
)


def payload_pass():
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


def payload_wrong_direction():
    return {
        "status": "phase_retention_contrast_gate_fail",
        "gate": {
            "passed": False,
            "direction_passed": False,
            "support_passed": True,
            "lambda_difference_b_minus_a": -0.3,
            "observation": {
                "lambda_a": 0.5,
                "lambda_b": 0.2,
                "p_difference": 0.02,
            },
        },
    }


def payload_insufficient_support():
    return {
        "status": "phase_retention_contrast_gate_fail",
        "gate": {
            "passed": False,
            "direction_passed": True,
            "support_passed": False,
            "lambda_difference_b_minus_a": 0.12,
            "observation": {
                "lambda_a": 0.25,
                "lambda_b": 0.37,
                "p_difference": 0.20,
            },
        },
    }


def payload_not_estimable():
    return {
        "status": "phase_retention_contrast_not_estimable",
        "reasons": ["too few adjacent valid fixed-24h phase pairs"],
    }


PAYLOADS = {
    "PASS": payload_pass,
    "FAIL_WRONG_DIRECTION": payload_wrong_direction,
    "FAIL_INSUFFICIENT_SUPPORT": payload_insufficient_support,
    "NOT_ESTIMABLE": payload_not_estimable,
}


def write_payload(tmp_path: Path, name: str, payload: dict) -> Path:
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def test_postoutcome_si_renders_all_registered_classes_without_pending_text():
    for expected, factory in PAYLOADS.items():
        text, claim = supporting.render_supporting_information(factory())
        assert claim["scientific_result"] == expected
        assert claim["render_surface"] == "V2 Supporting Information only"
        assert claim["main_text_changed_by_result"] is False
        assert claim["figures_changed_by_result"] is False
        assert claim["retuning_permitted"] is False
        assert "Appendix S8. Registered industrial-development phase-retention result" in text
        assert "remains unopened" not in text
        assert "— pending" not in text


def test_main_and_figures_are_identical_across_all_aikens_outcomes(tmp_path: Path):
    main_hashes = set()
    figure_hashes = set()
    si_hashes = set()
    result_classes = set()

    for name, factory in PAYLOADS.items():
        result_path = write_payload(tmp_path, name, factory())
        out = tmp_path / f"out_{name}"
        zip_path = tmp_path / f"{name}.zip"
        manifest = package.build(
            out,
            result_json=result_path,
            zip_path=zip_path,
        )

        result_classes.add(manifest["aikens_result_class"])
        main_hashes.add(manifest["outcome_invariance"]["main_sha256"])
        figure_hashes.add(
            manifest["outcome_invariance"]["figure_manifest_sha256"]
        )
        si_hashes.add(
            package.sha256(
                out / "GEB_V2_SUPPORTING_INFORMATION_POSTOUTCOME.md"
            )
        )

        assert manifest["scientific_state"] == "POSTOUTCOME_INTERNAL_READY"
        assert manifest["aikens_outcome_opened"] is True
        assert manifest["aikens_result_surface"] == "Supporting Information only"
        assert manifest["retuning_permitted"] is False
        assert manifest["final_submission_eligible"] is False
        assert manifest["final_submission_blockers"] == [
            "anonymous stable reviewer archive link",
            "author-controlled title-page and declaration metadata",
        ]
        assert manifest["figure_count"] == 7
        assert zip_path.exists()

    assert result_classes == set(PAYLOADS)
    assert len(main_hashes) == 1
    assert len(figure_hashes) == 1
    assert len(si_hashes) == 4


def test_postoutcome_package_is_deterministic_within_result_class(tmp_path: Path):
    result = write_payload(tmp_path, "pass", payload_pass())

    z1 = tmp_path / "one.zip"
    z2 = tmp_path / "two.zip"
    package.build(
        tmp_path / "one",
        result_json=result,
        zip_path=z1,
    )
    package.build(
        tmp_path / "two",
        result_json=result,
        zip_path=z2,
    )

    assert package.sha256(z1) == package.sha256(z2)


def test_postoutcome_package_excludes_v1_and_preoutcome_pending_markers(tmp_path: Path):
    result = write_payload(tmp_path, "pass", payload_pass())
    out = tmp_path / "package"
    package.build(out, result_json=result)

    assert not any("V1" in path.name for path in out.iterdir())
    assert not (out / "REGISTERED_INDUSTRIAL_PHASE_RETENTION_PENDING.md").exists()

    main = (out / "GEB_V2_BLINDED_POSTOUTCOME.md").read_text(encoding="utf-8")
    assert "AIKENS_LAMBDA" not in main
    assert "PREOUTCOME" not in main
    assert "PAYOFF-B" not in main

    si = (out / "GEB_V2_SUPPORTING_INFORMATION_POSTOUTCOME.md").read_text(
        encoding="utf-8"
    )
    assert "Frozen outcome class: **PASS**" in si
