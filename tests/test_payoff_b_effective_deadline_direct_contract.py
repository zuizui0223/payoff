import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "data"
    / "payoff_b_effective_deadline_threshold_contract_v2_20260929.json"
)
DIRECT_DOC = ROOT / "docs" / "PAYOFF_B_DIRECT_DEADLINE_THRESHOLD_TEST_20260929.md"
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"


def test_effective_deadline_contract_supersedes_raw_delay_contract():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert contract["supersedes"] == (
        "payoff_b_pairwise_deadline_threshold_direct_test_v1_20260929"
    )
    assert contract["forbidden_substitutions"]["raw_waiting_days_for_D_eff"]
    assert contract["forbidden_substitutions"]["departure_date_for_D_eff"]
    assert contract["forbidden_substitutions"][
        "multiply_sequential_timing_slopes_into_D_eff_without_causal_model"
    ]
    assert "J(delta)" in contract["theoretical_input"]["general_effective_cost"]
    assert "D_eff" in contract["theoretical_input"]["exact_threshold"]
    assert "total_effect_route" in contract["empirical_identification_routes"]
    assert "mechanistic_route" in contract["empirical_identification_routes"]
    assert contract["forbidden_substitutions"][
        "captivity_effect_for_natural_D_eff_without_treatment_fidelity"
    ]
    assert contract["forbidden_substitutions"][
        "full_timing_recovery_for_zero_D_eff_when_direct_J_may_remain"
    ]
    assert "D_eff_revealed" in contract["inverse_validation"]["identity"]


def test_direct_test_document_defines_direct_plus_compensated_cost():
    text = DIRECT_DOC.read_text(encoding="utf-8")

    assert "## Direct-plus-compensated deadline rule" in text
    assert "J(\\delta)" in text
    assert "D_{eff}" in text
    assert "total causal effect" in text
    assert "mechanistic decomposition" in text
    assert "complete timing recovery does not imply" in text
    assert "src/compensated_information_deadline.py" in text


def test_manuscript_natural_test_uses_effective_cost_gap():
    text = MANUSCRIPT.read_text(encoding="utf-8")

    assert (
        r"D_{eff,2}-D_{eff,1} \rightarrow q_2-q_1"
        in text
    )
    section = text.split(
        "### 4.6 Natural evidence currently supports the information axis",
        1,
    )[1].split(
        "### 4.7 Capacity, information and coordination",
        1,
    )[0]
    assert r"D_2-D_1 \rightarrow q_2-q_1" not in section
