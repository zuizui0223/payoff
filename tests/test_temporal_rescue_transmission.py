import pytest

from src.temporal_rescue_transmission import (
    environmental_response_transmission,
    linear_state_debt_transmission,
    temporal_rescue_transmission,
)


@pytest.mark.parametrize(
    "beta,tau,regime",
    [
        (0.0, 1.0, "FULL_TRANSMISSION"),
        (-0.3, 0.7, "PARTIAL_TRANSMISSION"),
        (-1.0, 0.0, "FULL_DEBT_TRANSFER"),
        (-1.2, -0.2, "REVERSAL"),
        (0.2, 1.2, "AMPLIFIED_OR_CONFOUNDED"),
    ],
)
def test_temporal_rescue_regimes(beta, tau, regime):
    out = temporal_rescue_transmission(beta)
    assert out.transmission == pytest.approx(tau)
    assert out.regime == regime


def test_linear_state_debt_boundary():
    assert linear_state_debt_transmission(0.0, 2.0) == pytest.approx(1.0)
    assert linear_state_debt_transmission(1.0, 2.0) == pytest.approx(0.5)
    assert linear_state_debt_transmission(2.0, 2.0) == pytest.approx(0.0)
    assert linear_state_debt_transmission(3.0, 2.0) == pytest.approx(-0.5)


def test_published_lameris_descriptive_ratio():
    assert environmental_response_transmission(0.35, 0.51) == pytest.approx(
        0.6862745098
    )


def test_zero_upstream_response_fails_closed():
    with pytest.raises(ValueError, match="non-zero"):
        environmental_response_transmission(0.2, 0.0)
