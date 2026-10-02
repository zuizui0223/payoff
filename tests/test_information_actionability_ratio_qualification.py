import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUAL = ROOT / "data" / "payoff_b_information_actionability_ratio_qualification_20261002.json"


def load():
    return json.loads(QUAL.read_text(encoding="utf-8"))


def test_no_current_natural_chi_estimate_is_promoted():
    payload = load()
    assert payload["status"] == "NO_CURRENT_NATURAL_CHI_ESTIMATE_QUALIFIED"
    assert all(
        row["chi_status"] == "NOT_QUALIFIED"
        for row in payload["candidates"]
    )


def test_snow_goose_static_q_sequence_is_not_forced_into_exponential_fit():
    payload = load()
    snow = next(
        row for row in payload["candidates"]
        if row["system"] == "greater snow goose"
    )
    q = snow["published_static_gaussian_q_bridge"]
    assert q["St_Lawrence_short"] == 0.580
    assert q["Nunavik"] == 0.535
    assert q["Baffin"] == 0.614
    assert q["St_Lawrence_short"] > q["Nunavik"]
    assert snow["monotone_exponential_q_licensed"] is False


def test_barnacle_lambda_is_not_relabelled_as_actionability():
    payload = load()
    barnacle = next(
        row for row in payload["candidates"]
        if row["system"] == "barnacle goose"
    )
    assert barnacle["r_status"] == "PHASE_CORRECTION_MEASURED_BUT_NOT_R"
    assert any("set r equal to 1-lambda" in row for row in payload["forbidden"])


def test_general_condition_is_retained_for_natural_systems():
    payload = load()
    assert any(
        "general q(t), r(t), D(t) first-order condition" in row
        for row in payload["valid_next_steps"]
    )
