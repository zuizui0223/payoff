"""Closed-form, excluded-invader, degeneracy, and numerical-scale regressions."""
import json
import math
import random
import subprocess
import sys

import pytest

from src.concave_partition_equilibrium import audit_partition_mixture, stable_negative_feedback_mixture
from src.full_partition_audit import enumerate_all_partitions, exact_five_partition_frequencies, registered_five_partition_problem, restricted_three_partition_frequencies


def problem():
    data = registered_five_partition_problem()
    data.pop("names")
    return data


def direct_kernel(data, h, weights=(1, 1, 1)):
    # Independent set-membership construction, not the solver's feature routine.
    def feature(partition):
        return [any(i in block and j in block for block in partition) for i, j in ((0, 1), (0, 2), (1, 2))]
    f = [feature(partition) for partition in data["partitions"]]
    b = data["intrinsic_payoffs"]
    return [[b[i] + b[j] + h * sum(w * (x != y) for w, x, y in zip(weights, f[i], f[j])) for j in range(len(b))] for i in range(len(b))]


def potential(matrix, p):
    return sum(pi * pj * matrix[i][j] for i, pi in enumerate(p) for j, pj in enumerate(p))


@pytest.mark.parametrize("h", [1e-6, .1, .25, .5, .50001, .75, 1, 1.00001, 1.5, 2, 13/6, 2.2, 3, 10, 1000])
def test_complete_five_partition_closed_form(h):
    data = problem()
    solution = stable_negative_feedback_mixture(**data, gamma=-h)
    assert solution["frequencies"] == pytest.approx(exact_five_partition_frequencies(h), abs=2e-10)
    assert solution["numerically_unique"]
    assert solution["normalized_kkt_residual"] < 1e-10
    assert solution["support_size_bound"] == 4
    assert len(solution["support"]) <= 4
    assert solution["scope"] == "DECLARED_CANDIDATE_SET_ONLY"
    matrix = direct_kernel(data, h)
    p = solution["frequencies"]
    assert solution["potential"] == pytest.approx(potential(matrix, p))
    u = [sum(a * pi for a, pi in zip(row, p)) for row in matrix]
    assert max(u) <= potential(matrix, p) + 2e-10


@pytest.mark.parametrize("h", [.1, .5, .8, 1])
def test_old_restricted_solution_survives_only_before_new_invader_boundary(h):
    audit = audit_partition_mixture(**problem(), frequencies=restricted_three_partition_frequencies(h), gamma=-h)
    assert audit["kkt_within_tolerance"]


@pytest.mark.parametrize("h", [1.01, 1.2, 19/12, 2, 10])
def test_excluded_partition_invades_old_three_strategy_solution(h):
    audit = audit_partition_mixture(**problem(), frequencies=restricted_three_partition_frequencies(h), gamma=-h)
    expected = h - 1 if h <= 19/12 else 7/12
    assert audit["invasion_margins"][3] == pytest.approx(expected)
    assert 3 in audit["invadable_candidate_indices"]
    assert not audit["kkt_within_tolerance"]


def test_h_two_changes_biological_composition_not_just_a_threshold():
    p = stable_negative_feedback_mixture(**problem(), gamma=-2)["frequencies"]
    assert p == pytest.approx((0, 5/8, 0, 1/4, 1/8))
    assert restricted_three_partition_frequencies(2)[0] == pytest.approx(5/48)


@pytest.mark.parametrize("h", [3, 5, 100])
def test_four_way_phase_excludes_fifth_with_constant_margin(h):
    solved = stable_negative_feedback_mixture(**problem(), gamma=-h)
    assert solved["support"] == (0, 1, 3, 4)
    assert solved["invasion_margins"][2] == pytest.approx(-4/3, abs=2e-10)


def test_degenerate_global_face_has_unique_marginals_not_unique_mixture():
    data = problem()
    data["intrinsic_payoffs"] = (0,) * 5
    solved = stable_negative_feedback_mixture(**data, gamma=-1)
    assert not solved["numerically_unique"]
    assert solved["tied_global_kkt_count"] == 2
    assert solved["comembership_marginals"] == pytest.approx((.5, .5, .5))
    assert solved["max_equilibrium_marginal_disagreement"] < 1e-10
    expected = ((.25, .5), (0, .25), (0, .25), (0, .25), (0, .5))
    for observed, bound in zip(solved["equilibrium_frequency_bounds"], expected):
        assert observed == pytest.approx(bound)
    for t in [.25, .3, .4, .5]:
        p = (t, .5-t, .5-t, .5-t, 2*t-.5)
        receipt = audit_partition_mixture(**data, frequencies=p, gamma=-1)
        assert receipt["kkt_within_tolerance"]
        assert receipt["potential"] == pytest.approx(1.5)


@pytest.mark.parametrize("scale", [1e-100, 1e-20, 1e-6, 1, 1e6, 1e20, 1e100])
def test_common_payoff_unit_change_preserves_frequencies(scale):
    data = problem()
    data["intrinsic_payoffs"] = tuple(scale * x for x in data["intrinsic_payoffs"])
    result = stable_negative_feedback_mixture(**data, gamma=-2 * scale)
    assert result["frequencies"] == pytest.approx(exact_five_partition_frequencies(2), abs=1e-10)


def test_common_intrinsic_offset_preserves_frequencies():
    data = problem()
    original = stable_negative_feedback_mixture(**data, gamma=-2)
    data["intrinsic_payoffs"] = tuple(123 + x for x in data["intrinsic_payoffs"])
    shifted = stable_negative_feedback_mixture(**data, gamma=-2)
    assert shifted["frequencies"] == pytest.approx(original["frequencies"])
    assert shifted["potential"] - original["potential"] == pytest.approx(246)


def test_weighted_concavity_and_global_upper_bound_random_mixtures():
    data = problem()
    h = 1.7
    weights = (1, .7, 2)
    solved = stable_negative_feedback_mixture(**data, gamma=-h, pair_weights=weights)
    matrix = direct_kernel(data, h, weights)
    rng = random.Random(260907)
    for _ in range(80):
        raw = [rng.random() for _ in range(5)]
        p = [x/sum(raw) for x in raw]
        audit = audit_partition_mixture(**data, frequencies=p, gamma=-h, pair_weights=weights)
        distance = sum(w * (a-b)**2 for w, a, b in zip(weights, audit["comembership_marginals"], solved["comembership_marginals"]))
        gap = solved["potential"] - potential(matrix, p)
        assert gap >= 2*h*distance - 2e-10


def test_candidate_order_invariance():
    data = problem()
    permutation = (3, 0, 4, 2, 1)
    permuted = {**data, "partitions": tuple(data["partitions"][i] for i in permutation), "intrinsic_payoffs": tuple(data["intrinsic_payoffs"][i] for i in permutation)}
    p = stable_negative_feedback_mixture(**permuted, gamma=-3)["frequencies"]
    expected = exact_five_partition_frequencies(3)
    assert p == pytest.approx(tuple(expected[i] for i in permutation))


def test_bell_counts_and_explicit_enumeration_guard():
    for n, count in ((1, 1), (2, 2), (3, 5), (4, 15)):
        states = enumerate_all_partitions(n, max_partitions=15)
        assert len(states) == count
        assert len(set(states)) == count
    with pytest.raises(ValueError, match="exceeds"):
        enumerate_all_partitions(4)
    with pytest.raises(ValueError, match="exceeds"):
        enumerate_all_partitions(100)


def test_one_candidate_is_not_an_error():
    one = stable_negative_feedback_mixture((2,), (((0,),),), n=1, gamma=-1)
    assert one["frequencies"] == (1,)
    assert one["numerically_unique"]
    assert one["potential"] == 4
    assert one["comembership_marginals"] == ()


@pytest.mark.parametrize("change", [
    {"gamma": 0}, {"gamma": .1}, {"gamma": math.nan}, {"gamma": -math.inf},
    {"tol": 0}, {"tol": math.nan}, {"n": 2.5}, {"n": True},
    {"intrinsic_payoffs": (0, 1, 2, 3, math.inf)},
    {"pair_weights": (1, 0, 1)}, {"pair_weights": (1, math.nan, 1)},
    {"pair_weights": (1, 2)}, {"max_strategies": 4},
    {"partitions": (((0, 1, 2),),) * 5},
    {"partitions": (((0.5, 1, 2),),) * 5},
])
def test_invalid_inputs_do_not_receive_a_certificate(change):
    kwargs = {**problem(), "gamma": -1, **change}
    with pytest.raises(ValueError):
        stable_negative_feedback_mixture(**kwargs)


def test_script_reproduces_complete_candidate_audit(tmp_path):
    out = tmp_path / "audit"
    subprocess.run([sys.executable, "scripts/audit_partition_equilibrium.py", "--output-dir", str(out)], check=True, capture_output=True, text=True)
    summary = json.loads((out / "summary.json").read_text())
    assert summary["status"] == "SYNTHETIC_MODEL_AUDIT_NOT_EMPIRICAL"
    assert summary["candidate_count"] == 5
    assert summary["includes_all_partitions"]
    assert summary["exact_h_boundaries"] == pytest.approx([.5, 1, 13/6])
    assert all(row["numerically_unique"] for row in summary["certificates"])
    assert all(row["max_formula_error"] < 1e-8 for row in summary["certificates"])
    assert (out / "five_partition_equilibria.csv").exists()


def test_all_fifteen_four_function_partitions_and_degenerate_optimal_vertices():
    states = enumerate_all_partitions(4, max_partitions=16)
    solved = stable_negative_feedback_mixture((0.0,) * 15, states, 4, -1, max_strategies=16)
    assert solved["support_size_bound"] == 7
    assert solved["potential"] == pytest.approx(3)
    assert solved["comembership_marginals"] == pytest.approx((.5,) * 6)
    assert solved["tied_global_kkt_count"] == 48
    assert not solved["numerically_unique"]
    assert solved["max_equilibrium_marginal_disagreement"] < 1e-10
