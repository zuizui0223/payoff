import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_aikens_lambda_manuscript.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_aikens", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def payload(*, passed, direction=True, support=True, a=0.2, b=0.5, p=0.01):
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


def test_pass_wording_is_forcing_association_not_cross_taxon_replication():
    m = load_module()
    results, discussion, abstract, conclusion, claim = m.render_blocks(payload(passed=True))
    assert claim["scientific_result"] == "PASS"
    assert claim["lambda_shift_supported"]
    assert not claim["cross_taxon_lambda_synthesis_changed"]
    assert "within-taxon" in results
    assert "not counted as an additional cross-taxon" in results
    assert "does not identify a causal equality" in discussion
    assert "supported greater" in abstract
    assert "actuation attenuation" in conclusion


def test_wrong_direction_is_scientific_fail_not_common_coordinate_failure():
    m = load_module()
    results, discussion, abstract, conclusion, claim = m.render_blocks(
        payload(passed=False, direction=False, support=True, a=0.5, b=0.2)
    )
    assert claim["scientific_result"] == "FAIL_WRONG_DIRECTION"
    assert claim["wrong_direction"]
    assert "failed in direction" in results
    assert "does not invalidate the shared within-system phase-retention estimator form" in discussion
    assert "failed" in abstract
    assert "distinct empirical levels" in conclusion


def test_positive_direction_without_support_does_not_license_shift():
    m = load_module()
    results, discussion, abstract, conclusion, claim = m.render_blocks(
        payload(passed=False, direction=True, support=False, p=0.2)
    )
    assert claim["scientific_result"] == "FAIL_INSUFFICIENT_SUPPORT"
    assert not claim["lambda_shift_supported"]
    assert "do not claim" in results
    assert "without a supported shift in lambda" in discussion
    assert "did not pass" in abstract
    assert "not accompanied by a supported shift" in conclusion


def test_not_estimable_forbids_retuning_language():
    m = load_module()
    results, discussion, abstract, conclusion, claim = m.render_blocks(
        {
            "status": "phase_retention_contrast_not_estimable",
            "reasons": ["too few fixed-24h transitions"],
        }
    )
    assert claim["scientific_result"] == "NOT_ESTIMABLE"
    assert not claim["estimable"]
    assert "not estimable" in results
    assert "did not change the 24 h interval" in results
    assert "rather than being rescued by retuning" in discussion
    assert "not estimable" in abstract
    assert "remained unresolved" in conclusion


def test_marker_replacement_preserves_markers_and_removes_pending_text():
    m = load_module()
    text = (
        "A\n"
        + m.RESULTS_START
        + "\n[AIKENS LAMBDA RESULT PENDING — x]\n"
        + m.RESULTS_END
        + "\nB"
    )
    rendered = m.replace_between(
        text, m.RESULTS_START, m.RESULTS_END, "resolved"
    )
    assert "resolved" in rendered
    assert "PENDING" not in rendered
    assert m.RESULTS_START in rendered
    assert m.RESULTS_END in rendered
