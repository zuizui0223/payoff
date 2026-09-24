import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = (
    ROOT
    / "data"
    / "payoff_b_lambda_classical_error_stress_20260924.json"
)


def test_classical_error_stress_receipt_matches_closed_form_thresholds():
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    rows = {row["system_id"]: row for row in payload["systems"]}

    for system_id in (
        "mule_deer_whole_migration",
        "barnacle_greenland_R2_R3",
        "barnacle_barents_R1_R2",
        "eurasian_wigeon_staging_transition",
    ):
        row = rows[system_id]
        expected_ratio = (1.0 - row["observed_lambda_hat"]) ** 0.5
        expected_days = (
            row["observed_predictor_sd_days"] * expected_ratio
        )
        assert row["finite_solution"]
        assert row[
            "required_error_sd_over_observed_predictor_sd"
        ] == pytest.approx(expected_ratio)
        assert row["required_error_sd_days"] == pytest.approx(
            expected_days
        )

    svalbard = rows[
        "barnacle_svalbard_southern_norway_to_svalbard"
    ]
    assert not svalbard["finite_solution"]
    assert svalbard["observed_lambda_hat"] < 0
    assert svalbard["required_error_sd_days"] is None


def test_stress_receipt_does_not_promote_thresholds_to_empirical_error():
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    boundary = " ".join(payload["claim_boundary"]).lower()
    assert "not measured error" in boundary
    assert payload["interpretation"][
        "no_cross_taxon_corrected_ranking_licensed"
    ]
