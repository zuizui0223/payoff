from math import isclose

from src.invasion import invasion_regime
from src.temporal_reciprocal_game import (
    classify_reciprocal_temporal_state,
    effective_coordination_strength,
    reciprocal_exponents,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)

LABELS = {
    "mutual_invasion": "reciprocal_invasion",
    "mutual_noninvasion": "mutual_noninvasion",
    "differentiated_invasion_only": "d_only_invasion",
    "shared_invasion_only": "s_only_invasion",
    "invasion_boundary": "boundary",
}


def _scaled(base, q):
    phi_bar, eta, contrast, migration, duration = base
    return (
        phi_bar * q,
        eta * q,
        contrast * q,
        migration * q,
        duration / q,
    )


def test_temporal_state_is_invariant_under_consistent_time_unit_conversion():
    # First case is analytically D-only even without temporal heterogeneity;
    # second exercises a nonzero anti-phase premium while staying far from a
    # reciprocal boundary.
    cases = (
        (0.4, 0.1, 0.0, 0.3, 1.0),
        (2.0, 0.2, 0.5, 0.3, 1.0),
    )
    for base in cases:
        baseline = classify_reciprocal_temporal_state(*base)
        assert baseline != "boundary"
        baseline_exponents = reciprocal_exponents(*base)

        for q in SCALES:
            args = _scaled(base, q)
            assert classify_reciprocal_temporal_state(*args) == baseline
            exponents = reciprocal_exponents(*args)
            assert isclose(exponents[0] / q, baseline_exponents[0], rel_tol=1e-11, abs_tol=1e-12)
            assert isclose(exponents[1] / q, baseline_exponents[1], rel_tol=1e-11, abs_tol=1e-12)


def test_temporal_wrapper_matches_canonical_effective_game_at_every_scale():
    base = (0.25, 0.4, 1.2, 0.6, 0.8)
    for q in SCALES:
        phi_bar, eta, contrast, migration, duration = _scaled(base, q)
        eta_effective = effective_coordination_strength(
            eta,
            contrast,
            migration,
            duration,
        )
        canonical = invasion_regime(phi_bar, eta_effective)
        observed = classify_reciprocal_temporal_state(
            phi_bar,
            eta,
            contrast,
            migration,
            duration,
        )
        assert observed == LABELS[canonical]


def test_tiny_strict_temporal_invasion_is_not_collapsed_to_boundary():
    q = 1e-16
    args = _scaled((0.4, 0.1, 0.0, 0.3, 1.0), q)
    lambda_d, lambda_s = reciprocal_exponents(*args)
    assert 0.0 < lambda_d < 1e-12
    assert lambda_s < 0.0
    assert classify_reciprocal_temporal_state(*args) == "d_only_invasion"
