from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PAYOFF_B_TEMPORAL_BUFFERING_CLAIM_HIERARCHY_20260925.md"
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"


def test_temporal_buffering_is_primary_and_identification_is_secondary() -> None:
    text = DOC.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Temporal buffering delays but does not permanently replace spatial tracking" in text
    assert "Low current mismatch can conceal latent spatial tracking demand" in text
    assert "The inference statement is not the headline result." in text
    assert manuscript.startswith(
        "# Temporal buffering delays but does not replace spatial tracking under environmental change"
    )


def test_latent_spatial_demand_is_descriptive_not_empirically_estimated() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "a descriptive phrase" in text
    assert "not" in text.lower()
    assert "a newly fitted state variable" in text
    assert "an empirically estimated quantity in the 55-species bird analysis" in text
    assert "all natural phenological adjustment creates hidden movement" in text


def test_aikens_cannot_retune_primary_conclusion() -> None:
    text = DOC.read_text(encoding="utf-8")
    for cls in ("PASS", "wrong-direction", "insufficient-support", "NOT_ESTIMABLE"):
        assert cls in text
    assert "leave the primary temporal-buffering conclusion unchanged" in text


def test_claim_hierarchy_records_registered_natural_substitution_failure() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "FAIL_WRONG_DIRECTION" in text
    assert "+0.0351 ± 0.0289" in text
    assert "Timing responsiveness can improve average alignment without making" in text
    assert "movement-speed matching dispensable" in text
    assert "secondary timing main effect" in text


def test_claim_hierarchy_distinguishes_gain_capacity_and_transport() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Gain–capacity–propagation decomposition" in text
    assert "timing gain" in text
    assert "timing capacity / temporal budget" in text
    assert "movement speed / route progression" in text
    assert "high gain" in text
    assert "remaining capacity" in text
