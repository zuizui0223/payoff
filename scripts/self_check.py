#!/usr/bin/env python3
"""Dependency-free numerical audits for PAYOFF's core analytic identities."""

from __future__ import annotations

import random
import sys
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.payoff_game import (
    QuadraticTraitArchitecture,
    architecture_payoffs,
    architecture_phi,
    classify_lke_phase,
    classify_phase,
    game_matrix,
    infer_recovery_feedback_from_cost_thresholds,
    interior_equilibrium,
    invasion_cost_surfaces,
    invasion_margins,
    middle_cost_interval,
    n_function_conflict,
    payoff_gap,
    replicator_rhs,
)


def check_quadratic_bridge() -> None:
    rng = random.Random(20260906)
    for _ in range(2000):
        a = 10 ** rng.uniform(-2, 2)
        b = 10 ** rng.uniform(-2, 2)
        theta1 = rng.uniform(-5, 5)
        theta2 = rng.uniform(-5, 5)
        coupling = 10 ** rng.uniform(-3, 3)
        cost = rng.uniform(0, 10)
        model = QuadraticTraitArchitecture(
            a=a,
            b=b,
            theta1=theta1,
            theta2=theta2,
            coupling=coupling,
            architecture_cost=cost,
        )
        x, y = model.differentiated_optima
        assert isclose(
            model.recovered_loss,
            model.separation_fraction * model.conflict_load,
            rel_tol=1e-10,
            abs_tol=1e-10,
        )
        assert isclose(
            x - y,
            model.separation_fraction * (theta1 - theta2),
            rel_tol=1e-10,
            abs_tol=1e-10,
        )
        assert isclose(
            model.phi,
            model.separation_fraction * model.conflict_load - cost,
            rel_tol=1e-10,
            abs_tol=1e-10,
        )


def check_n_function_identity() -> None:
    rng = random.Random(17)
    for n in range(2, 11):
        for _ in range(100):
            weights = [10 ** rng.uniform(-1, 1) for _ in range(n)]
            optima = [rng.uniform(-4, 4) for _ in range(n)]
            _, variance_load, pairwise_load = n_function_conflict(weights, optima)
            assert isclose(variance_load, pairwise_load, rel_tol=1e-10, abs_tol=1e-10)


def check_game_representation() -> None:
    for phi in [-1.2, -0.3, 0.0, 0.4, 1.7]:
        for eta in [-1.0, -0.2, 0.0, 0.5, 1.3]:
            matrix = game_matrix(phi, eta)
            assert matrix[0][1] == matrix[1][0]
            for p in [0.0, 0.1, 0.37, 0.5, 0.81, 1.0]:
                pi_s, pi_d = architecture_payoffs(p, phi, eta)
                assert isclose(pi_d - pi_s, payoff_gap(p, phi, eta), abs_tol=1e-12)


def check_phase_directions() -> None:
    phi, eta = 0.2, -1.0
    p_star = interior_equilibrium(phi, eta)
    assert p_star is not None
    assert classify_phase(phi, eta) == "stable_architecture_coexistence"
    assert replicator_rhs(p_star - 0.05, phi, eta) > 0
    assert replicator_rhs(p_star + 0.05, phi, eta) < 0

    phi, eta = 0.2, 1.0
    p_star = interior_equilibrium(phi, eta)
    assert p_star is not None
    assert classify_phase(phi, eta) == "coordination_bistability"
    assert replicator_rhs(p_star - 0.05, phi, eta) < 0
    assert replicator_rhs(p_star + 0.05, phi, eta) > 0


def check_invasion_surface_identities() -> None:
    rng = random.Random(19051988)
    for _ in range(3000):
        conflict_load = rng.uniform(0.0, 10.0)
        separation_fraction = rng.random()
        architecture_cost = rng.uniform(0.0, 10.0)
        eta = rng.uniform(-3.0, 3.0)

        recovery = separation_fraction * conflict_load
        phi = architecture_phi(conflict_load, separation_fraction, architecture_cost)
        i_d, i_s = invasion_margins(
            conflict_load, separation_fraction, architecture_cost, eta
        )
        assert isclose(i_d, phi - eta, abs_tol=1e-12)
        assert isclose(i_s, -phi - eta, abs_tol=1e-12)

        k_d, k_s = invasion_cost_surfaces(conflict_load, separation_fraction, eta)
        recovered, inferred_eta = infer_recovery_feedback_from_cost_thresholds(k_d, k_s)
        assert isclose(recovered, recovery, abs_tol=1e-12)
        assert isclose(inferred_eta, eta, abs_tol=1e-12)
        assert isclose(k_s - k_d, 2.0 * eta, abs_tol=1e-12)

        lower, upper = middle_cost_interval(conflict_load, separation_fraction, eta)
        assert isclose(upper - lower, 2.0 * abs(eta), abs_tol=1e-12)

        phase_direct = classify_lke_phase(
            conflict_load, separation_fraction, architecture_cost, eta
        )
        phase_phi = classify_phase(phi, eta)
        assert phase_direct == phase_phi


def main() -> None:
    check_quadratic_bridge()
    check_n_function_identity()
    check_game_representation()
    check_phase_directions()
    check_invasion_surface_identities()
    print("PAYOFF_SELF_CHECK_OK")


if __name__ == "__main__":
    main()
