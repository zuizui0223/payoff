import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "payoff_b_prediction_correction_substitution_motivation_20261002.json"


def load():
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_motivation_receipt_is_explicitly_posthoc():
    payload = load()
    assert payload["status"] == "POSTHOC_MOTIVATION_ONLY_NOT_CONFIRMATORY"
    assert payload["frozen_submission_affected"] is False
    assert "after these barnacle and wigeon outcomes" in payload["theory_timing"]


def test_five_stable_rows_have_descriptive_opposite_rank_for_correction():
    payload = load()
    rows = sorted(
        payload["stable_barnacle_registry_subset"],
        key=lambda row: row["predictability_r"],
    )
    lambdas = [row["abs_lambda"] for row in rows]
    correction = [row["correction_fraction"] for row in rows]
    assert lambdas == sorted(lambdas)
    assert correction == sorted(correction, reverse=True)
    assert payload["subset_description"]["inferential_p_value_reported"] is False


def test_broader_screen_is_retained_not_replaced():
    payload = load()
    screen = payload["broader_existing_screen"]
    assert screen["matched_pairs"] == 7
    assert screen["spearman_rho"] == -0.464
    assert screen["p"] == 0.294
    assert screen["status"] == "NOT_SUPPORTED"
    assert any(
        "drop the broader seven-pair screen" in row
        for row in payload["forbidden_use"]
    )


def test_wigeon_registered_null_is_not_relabelled_as_support():
    payload = load()
    wigeon = payload["wigeon_registered_result"]
    assert wigeon["estimate"] == 0.0202
    assert wigeon["p"] == 0.756
    assert wigeon["status"] == "NOT_SUPPORTED"
    assert any(
        "wigeon registered null" in row
        for row in payload["forbidden_use"]
    )
