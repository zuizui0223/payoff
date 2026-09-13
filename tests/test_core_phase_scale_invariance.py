from __future__ import annotations

import math

import pytest

from src.game_potential import (
    coexistence_frequency,
    coordination_basin_sizes,
    risk_dominant_architecture,
)
from src.invasion import invasion_regime
from src.numerical_tolerance import DEFAULT_RELATIVE_TOL, relative_band
from src.payoff_game import classify_lke_phase, classify_phase, interior_equilibrium


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_core_phase_labels_are_invariant_to_common_payoff_rescaling():
    cases = [
        (-2.0, 0.5, "shared_dominance"),
        (2.0, 0.5, "differentiated_dominance"),
        (0.2, -1.0, "stable_architecture_coexistence"),
        (0.2, 1.0, "coordination_bistability"),
        (1.0, 1.0, "nonhyperbolic_phase_boundary"),
        (-1.0, 1.0, "nonhyperbolic_phase_boundary"),
        (0.0, 0.0, "neutral_architecture_boundary"),
    ]
    for phi, eta, expected in cases:
        for scale in SCALES:
            assert classify_phase(scale * phi, scale * eta) == expected


def test_eta_zero_dominance_does_not_collapse_to_neutral_at_small_units():
    for scale in SCALES:
        assert classify_phase(2.0 * scale, 0.0) == "differentiated_dominance"
        assert classify_phase(-2.0 * scale, 0.0) == "shared_dominance"


def test_reciprocal_invasion_regimes_are_scale_invariant():
    cases = [
        (0.2, -1.0, "mutual_invasion"),
        (0.2, 1.0, "mutual_noninvasion"),
        (2.0, 0.5, "differentiated_invasion_only"),
        (-2.0, 0.5, "shared_invasion_only"),
        (1.0, 1.0, "invasion_boundary"),
    ]
    for phi, eta, expected in cases:
        for scale in SCALES:
            assert invasion_regime(scale * phi, scale * eta) == expected


def test_interior_and_potential_game_geometry_are_scale_invariant():
    expected_coexistence = interior_equilibrium(0.2, -1.0)
    expected_coordination = interior_equilibrium(0.2, 1.0)
    expected_basins = coordination_basin_sizes(0.2, 1.0)
    assert expected_coexistence is not None
    assert expected_coordination is not None
    assert expected_basins is not None

    for scale in SCALES:
        coexist = interior_equilibrium(0.2 * scale, -1.0 * scale)
        coord = interior_equilibrium(0.2 * scale, 1.0 * scale)
        basins = coordination_basin_sizes(0.2 * scale, 1.0 * scale)
        stable = coexistence_frequency(0.2 * scale, -1.0 * scale)
        risk = risk_dominant_architecture(0.2 * scale, 1.0 * scale)

        assert coexist == pytest.approx(expected_coexistence, rel=2e-15, abs=2e-15)
        assert coord == pytest.approx(expected_coordination, rel=2e-15, abs=2e-15)
        assert stable == pytest.approx(expected_coexistence, rel=2e-15, abs=2e-15)
        assert basins == pytest.approx(expected_basins, rel=2e-15, abs=2e-15)
        assert risk == "D"


def test_l_s_k_eta_route_preserves_phase_under_common_fitness_rescaling():
    # R=sL=1 and K=0.8, hence phi=0.2.  Scaling L, K, and eta together is
    # only a change of payoff units and must not change the phase.
    for scale in SCALES:
        assert (
            classify_lke_phase(
                conflict_load=2.0 * scale,
                separation_fraction=0.5,
                architecture_cost=0.8 * scale,
                eta=-1.0 * scale,
            )
            == "stable_architecture_coexistence"
        )
        assert (
            classify_lke_phase(
                conflict_load=2.0 * scale,
                separation_fraction=0.5,
                architecture_cost=0.8 * scale,
                eta=1.0 * scale,
            )
            == "coordination_bistability"
        )


def test_exact_mode_with_zero_tolerance_retains_exact_boundaries():
    assert classify_phase(0.0, 0.0, tol=0.0) == "neutral_architecture_boundary"
    assert classify_phase(1.0, 1.0, tol=0.0) == "nonhyperbolic_phase_boundary"
    assert invasion_regime(1.0, 1.0, tol=0.0) == "invasion_boundary"


def test_relative_band_has_no_absolute_payoff_floor():
    assert DEFAULT_RELATIVE_TOL > 0.0
    assert relative_band((0.0, 0.0)) == 0.0
    for scale in SCALES:
        observed = relative_band((2.0 * scale, -3.0 * scale))
        assert observed == pytest.approx(
            DEFAULT_RELATIVE_TOL * 3.0 * scale,
            rel=2e-15,
            abs=0.0,
        )
    with pytest.raises(ValueError, match="tol must be finite"):
        relative_band((1.0,), math.inf)
    with pytest.raises(ValueError, match="values must be finite"):
        relative_band((math.nan,))
