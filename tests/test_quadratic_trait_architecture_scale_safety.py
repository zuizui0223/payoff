from math import isclose, isfinite

from src.payoff_game import QuadraticTraitArchitecture


BASE = QuadraticTraitArchitecture(
    a=2.0,
    b=3.0,
    theta1=-1.0,
    theta2=2.0,
    coupling=4.0,
    architecture_cost=0.5,
)


def _scaled(q: float) -> QuadraticTraitArchitecture:
    coefficient_scale = q * q
    return QuadraticTraitArchitecture(
        a=2.0 / coefficient_scale,
        b=3.0 / coefficient_scale,
        theta1=-1.0 * q,
        theta2=2.0 * q,
        coupling=4.0 / coefficient_scale,
        architecture_cost=0.5,
    )


def test_quadratic_architecture_outputs_are_coordinate_unit_covariant():
    base_shared = BASE.shared_optimum
    base_differentiated = BASE.differentiated_optima
    base_conflict = BASE.conflict_load
    base_separation = BASE.separation_fraction
    base_differentiated_loss = BASE.differentiated_loss
    base_recovered = BASE.recovered_loss
    base_phi = BASE.phi
    base_critical = BASE.critical_coupling()
    assert base_critical is not None

    for q in (1e-150, 1.0, 1e100, 1e150):
        observed = _scaled(q)
        assert isfinite(observed.shared_optimum)
        assert all(isfinite(value) for value in observed.differentiated_optima)
        assert isfinite(observed.conflict_load)
        assert isfinite(observed.differentiated_loss)
        assert isfinite(observed.recovered_loss)
        assert isfinite(observed.phi)

        assert isclose(observed.shared_optimum / q, base_shared, rel_tol=3e-12, abs_tol=0.0)
        for value, expected in zip(observed.differentiated_optima, base_differentiated):
            assert isclose(value / q, expected, rel_tol=3e-12, abs_tol=0.0)
        assert isclose(observed.conflict_load, base_conflict, rel_tol=3e-12, abs_tol=0.0)
        assert isclose(observed.separation_fraction, base_separation, rel_tol=3e-12, abs_tol=0.0)
        assert isclose(
            observed.differentiated_loss,
            base_differentiated_loss,
            rel_tol=3e-12,
            abs_tol=0.0,
        )
        assert isclose(observed.recovered_loss, base_recovered, rel_tol=3e-12, abs_tol=0.0)
        assert isclose(
            observed.recovered_loss_via_bridge,
            base_recovered,
            rel_tol=3e-12,
            abs_tol=0.0,
        )
        assert isclose(observed.phi, base_phi, rel_tol=3e-12, abs_tol=0.0)

        critical = observed.critical_coupling()
        assert critical is not None and isfinite(critical)
        assert isclose(critical * q * q, base_critical, rel_tol=3e-12, abs_tol=0.0)


def test_raw_q_underflow_does_not_break_derived_architecture_quantities():
    observed = _scaled(1e150)
    # The dimensional q=a*b+c(a+b) is far below the float range at this unit
    # choice. Derived quantities must not divide by that raw representation.
    assert observed.q == 0.0
    assert observed.separation_fraction > 0.0
    assert all(isfinite(value) for value in observed.differentiated_optima)
    assert isclose(observed.conflict_load, BASE.conflict_load, rel_tol=3e-12, abs_tol=0.0)
    assert isclose(observed.phi, BASE.phi, rel_tol=3e-12, abs_tol=0.0)


def test_zero_coupling_remains_exactly_fully_separated_across_units():
    for q in (1e-150, 1.0, 1e150):
        coefficient_scale = q * q
        model = QuadraticTraitArchitecture(
            a=2.0 / coefficient_scale,
            b=3.0 / coefficient_scale,
            theta1=-1.0 * q,
            theta2=2.0 * q,
            coupling=0.0,
            architecture_cost=0.0,
        )
        assert model.separation_fraction == 1.0
        assert model.differentiated_loss == 0.0
        x, y = model.differentiated_optima
        assert isclose(x / q, -1.0, rel_tol=0.0, abs_tol=0.0)
        assert isclose(y / q, 2.0, rel_tol=0.0, abs_tol=0.0)
