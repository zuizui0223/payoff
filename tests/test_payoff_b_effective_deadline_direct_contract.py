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
    assert "D_eff" in contract["theoretical_input"]["exact_threshold"]
    assert "D_eff_revealed" in contract["inverse_validation"]["identity"]


def test_direct_test_document_defines_compensated_cost():
    text = DIRECT_DOC.read_text(encoding="utf-8")

    assert "## Compensated-deadline rule" in text
    assert "D_{eff}" in text
    assert "raw delay is not itself the empirical" in text
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
