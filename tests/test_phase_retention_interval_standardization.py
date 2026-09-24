import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from standardize_phase_retention_intervals import (
    build_result,
    equivalent_interval_metrics,
)


CONTRACT = (
    ROOT
    / "data"
    / "payoff_b_phase_retention_interval_standardization_contract_20260925.json"
)
FROZEN_RESULT = (
    ROOT
    / "data"
    / "payoff_b_phase_retention_interval_standardization_result_20260925.json"
)


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def find_variant(result, system_id, variant_id):
    system = next(
        row for row in result["systems"] if row["system_id"] == system_id
    )
    return next(
        row for row in system["variants"] if row["variant_id"] == variant_id
    )


def test_equivalent_decay_definition():
    row = equivalent_interval_metrics(0.25, 2.0)
    assert math.isclose(
        row["equivalent_decay_constant_per_day"],
        -math.log(0.25) / 2.0,
    )
    assert math.isclose(row["equivalent_daily_retention"], 0.5)
    assert row["lambda_sign"] == 1


def test_negative_lambda_keeps_overshoot_sign():
    row = equivalent_interval_metrics(-0.25, 2.0)
    assert row["lambda_sign"] == -1
    assert math.isclose(row["retention_magnitude"], 0.25)
    assert math.isclose(row["equivalent_daily_retention"], 0.5)


def test_contract_is_frozen_before_aikens_outcome():
    contract = load_contract()
    assert contract["Aikens_lambda_outcome_opened"] is False
    assert contract["freeze_timing"] == "before_Aikens_lambda_outcome_opened"
    assert (
        contract["source_policy"]["Aikens_future_rule"]
        .startswith("if the preregistered fixed-24h")
    )


def test_wigeon_uses_animal_year_count_histogram_not_224_over_28():
    result = build_result(load_contract())
    power = find_variant(
        result, "eurasian_wigeon_staging_transition", "POWER"
    )
    path = power["path_memory"]
    assert path["animal_years"] == 32
    assert path["unique_individuals"] == 28
    assert path["transitions"] == 224
    assert path["transition_count_mean"] == 7.0
    assert path["transition_count_median"] == 7.0
    assert math.isclose(
        path["retention_at_median_transition_count"],
        0.7497680211367301 ** 7,
        rel_tol=1e-12,
    )


def test_wigeon_power_and_era5_typical_path_are_same_order_as_mule_deer():
    result = build_result(load_contract())
    mule = find_variant(result, "mule_deer_whole_migration", "source_naive")
    power = find_variant(
        result, "eurasian_wigeon_staging_transition", "POWER"
    )
    era5 = find_variant(
        result, "eurasian_wigeon_staging_transition", "ERA5"
    )

    mule_path = mule["path_memory"]["path_retention_magnitude"]
    power_path = power["path_memory"]["retention_at_median_transition_count"]
    era5_path = era5["path_memory"]["retention_at_median_transition_count"]

    assert 0.10 < mule_path < 0.11
    assert 0.13 < power_path < 0.14
    assert 0.23 < era5_path < 0.24


def test_simex_upper_sensitivity_blocks_universal_80_percent_correction_claim():
    result = build_result(load_contract())
    upper = find_variant(
        result,
        "eurasian_wigeon_staging_transition",
        "SIMEX_conservative_full_disagreement",
    )
    path = upper["path_memory"]
    assert 0.62 < path["retention_at_median_transition_count"] < 0.63
    assert path["correction_at_median_transition_count"] < 0.40


def test_goose_whole_route_cumulative_retention_is_not_licensed():
    result = build_result(load_contract())
    for system_id, variant_id in (
        ("barnacle_svalbard_R2_R4", "POWER"),
        ("barnacle_greenland_R2_R3", "POWER"),
        ("barnacle_barents_R1_R2", "POWER"),
    ):
        row = find_variant(result, system_id, variant_id)
        assert row["path_memory"]["licensed"] is False


def _assert_semantically_equal(frozen, expected):
    if isinstance(frozen, dict) and isinstance(expected, dict):
        assert set(frozen) == set(expected)
        for key in frozen:
            _assert_semantically_equal(frozen[key], expected[key])
        return

    if isinstance(frozen, list) and isinstance(expected, list):
        assert len(frozen) == len(expected)
        for left, right in zip(frozen, expected):
            _assert_semantically_equal(left, right)
        return

    if (
        isinstance(frozen, (int, float))
        and not isinstance(frozen, bool)
        and isinstance(expected, (int, float))
        and not isinstance(expected, bool)
    ):
        assert math.isclose(
            float(frozen),
            float(expected),
            rel_tol=1e-12,
            abs_tol=1e-15,
        )
        return

    assert frozen == expected


def test_frozen_result_semantically_matches_contract_recalculation():
    expected = build_result(load_contract())
    frozen = json.loads(FROZEN_RESULT.read_text(encoding="utf-8"))
    _assert_semantically_equal(frozen, expected)
