import json
import math
from pathlib import Path

from src.reciprocal_sign_partial_identification import (
    identify_phase_from_sign_evidence,
)


RECEIPT = Path("validation/pstutzeri_published_reciprocal_sign_v1.json")


def load_receipt():
    return json.loads(RECEIPT.read_text())


def test_ph65_published_oriented_signs_recover_strict_reciprocal_invasion_phase():
    data = load_receipt()
    c = data["contexts"]["pH_6_5"]
    r = identify_phase_from_sign_evidence(
        c["specialist_rare"]["oriented_sign"],
        c["generalist_rare"]["oriented_sign"],
        support_reference=data["receipt_id"],
    )
    assert r.strict_phase_certified
    assert r.certified_strict_phase == "stable_architecture_coexistence"
    assert c["generic_payoff_sign_phase"] == r.certified_strict_phase


def test_ph75_published_evidence_is_partial_not_negative_by_nonsignificance():
    data = load_receipt()
    c = data["contexts"]["pH_7_5"]
    assert c["specialist_rare"]["reported_p"] == 0.31
    assert c["specialist_rare"]["oriented_sign"] == "unresolved"

    r = identify_phase_from_sign_evidence(
        c["specialist_rare"]["oriented_sign"],
        c["generalist_rare"]["oriented_sign"],
        support_reference=data["receipt_id"],
    )
    assert not r.strict_phase_certified
    assert r.boundary_compatible
    assert set(r.compatible_strict_phases) == set(c["compatible_strict_phases"])
    assert set(r.excluded_strict_phases) == set(c["excluded_strict_phases"])


def test_reported_log10_ratio_to_frequency_conversions_are_reproducible():
    data = load_receipt()
    for context in data["contexts"].values():
        for assay in ("generalist_rare", "specialist_rare"):
            logs = context[assay]["initial_log10_specialist_to_generalist"]
            recorded = context[assay]["initial_specialist_frequency_approx"]
            recomputed = [10.0**x / (1.0 + 10.0**x) for x in logs]
            for got, want in zip(recomputed, recorded):
                assert math.isclose(got, want, rel_tol=0, abs_tol=1e-7)


def test_short_and_long_windows_are_kept_separate():
    data = load_receipt()
    assert data["short_window"]["transfers"] == 3
    assert math.isclose(data["short_window"]["generations_approx"], 19.932)
    assert data["long_window_pH_6_5"]["transfers"] == 12
    assert data["long_window_pH_6_5"]["generations_approx"] == 80
    assert (
        data["long_window_pH_6_5"]["interpretation"]
        == "fixed_type_fixed_payoff_extrapolation_not_supported_because_generalist_phenotypic_and_genetic_change_accumulates"
    )


def test_claim_ceiling_is_preserved():
    flags = load_receipt()["claim_flags"]
    assert flags["generic_lane_A_reciprocal_invasion_logic_recovered"]
    assert not flags["numerical_phi_identified"]
    assert not flags["numerical_eta_identified"]
    assert not flags["affine_frequency_response_validated"]
    assert not flags["payoff_architecture_mapping_established"]
    assert not flags["historical_causation_identified"]
