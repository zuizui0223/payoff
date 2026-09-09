import json
from pathlib import Path

from src.consortium_strategic_unit import (
    ConsortiumStrategicUnitReceipt,
    adjudicate_consortium_strategic_unit,
)


REGISTRY = Path("validation/consortium_strategic_unit_status_v1.json")


def test_registry_recomputes_all_expected_strategic_unit_statuses():
    data = json.loads(REGISTRY.read_text())
    assert data["registry_id"] == "PAYOFF_CONSORTIUM_STRATEGIC_UNIT_STATUS_V1"
    assert data["systems"]
    for row in data["systems"]:
        result = adjudicate_consortium_strategic_unit(
            ConsortiumStrategicUnitReceipt(**row["receipt"])
        )
        assert result.strategic_unit_certified == row["expected_strategic_unit_certified"]
        assert set(row["primary_blockers"]).issubset(set(result.blockers))


def test_stable_internal_composition_is_explicitly_not_sufficient():
    data = json.loads(REGISTRY.read_text())
    assert not data["stable_internal_composition_is_sufficient"]
    evolved = next(
        row for row in data["systems"]
        if row["receipt"]["system_id"] == "EVOLVED_ECOLI_CROSSFEEDING"
    )
    assert evolved["receipt"]["composition_state_reproducible_declared"]
    result = adjudicate_consortium_strategic_unit(
        ConsortiumStrategicUnitReceipt(**evolved["receipt"])
    )
    assert not result.strategic_unit_certified
    assert "INTERNAL_Q_NOT_SEPARATED_FROM_EXTERNAL_P" in result.blockers
    assert "WHOLE_UNIT_EXTERNAL_FREQUENCY_NOT_DEFINED" in result.blockers


def test_beck_r3_and_generic_multimetric_results_do_not_enter_a_subgate():
    data = json.loads(REGISTRY.read_text())
    assert not data["generic_game_evidence_used"]
    assert not data["raw_reconstruction_status_used"]
    beck = next(
        row for row in data["systems"]
        if row["receipt"]["system_id"] == "BECK_SYNTHETIC_ECOLI"
    )
    result = adjudicate_consortium_strategic_unit(
        ConsortiumStrategicUnitReceipt(**beck["receipt"])
    )
    assert not result.strategic_unit_certified
    assert not result.architecture_mapping_promoted
    assert not result.generic_game_promoted


def test_no_current_multigenotype_consortium_is_certified_as_payoff_strategy_unit():
    data = json.loads(REGISTRY.read_text())
    assert not data["any_strategic_unit_certified"]
    assert not any(
        adjudicate_consortium_strategic_unit(
            ConsortiumStrategicUnitReceipt(**row["receipt"])
        ).strategic_unit_certified
        for row in data["systems"]
    )
