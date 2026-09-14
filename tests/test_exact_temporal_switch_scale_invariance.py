from math import isclose

from src.anti_phase_temporal import anti_phase_temporal_premium
from src.temporal_reciprocal_game import exact_reciprocal_switch_migrations


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_exact_switch_roots_covary_under_time_unit_conversion():
    eta = 0.15
    phi_bar = 0.0
    contrast = 1.5
    tau = 1.0

    reference = exact_reciprocal_switch_migrations(
        eta, phi_bar, contrast, tau
    )
    assert reference is not None
    reference_lower, reference_upper = reference

    for q in SCALES:
        scaled_tau = tau / q
        roots = exact_reciprocal_switch_migrations(
            eta * q,
            phi_bar * q,
            contrast * q,
            scaled_tau,
        )
        assert roots is not None
        lower, upper = roots

        # Migration is a rate, so both roots must transform as m -> q*m.
        assert isclose(lower / q, reference_lower, rel_tol=1e-10, abs_tol=0.0)
        assert isclose(upper / q, reference_upper, rel_tol=1e-10, abs_tol=0.0)

        # Equivalently, the dimensionless roots u=m*tau are invariant.
        assert isclose(
            lower * scaled_tau,
            reference_lower * tau,
            rel_tol=1e-10,
            abs_tol=0.0,
        )
        assert isclose(
            upper * scaled_tau,
            reference_upper * tau,
            rel_tol=1e-10,
            abs_tol=0.0,
        )


def test_returned_roots_hit_the_scaled_exact_premium_target():
    eta = 0.15
    phi_bar = 0.04
    contrast = 1.5
    tau = 1.0
    target = eta + abs(phi_bar)

    for q in SCALES:
        scaled_tau = tau / q
        roots = exact_reciprocal_switch_migrations(
            eta * q,
            phi_bar * q,
            contrast * q,
            scaled_tau,
        )
        assert roots is not None
        for migration in roots:
            premium = anti_phase_temporal_premium(
                contrast * q,
                migration,
                scaled_tau,
            )
            # Divide out the rate-unit conversion before comparing accuracy.
            assert isclose(
                premium / q,
                target,
                rel_tol=1e-9,
                abs_tol=0.0,
            )


def test_large_rate_unit_no_longer_hits_dimensional_bracketing_cutoff():
    q = 1e16
    roots = exact_reciprocal_switch_migrations(
        0.15 * q,
        0.0,
        1.5 * q,
        1.0 / q,
    )
    assert roots is not None
    lower, upper = roots
    assert 0.0 < lower < upper
    # The upper root is deliberately above the old absolute 1e15 cutoff.
    assert upper > 1e15
