"""Independent exact-state enumeration and regression for the new theory witness."""
from __future__ import annotations

from math import isclose
import pytest

from src.plastic_compromise_architecture import (
    PlasticCompromise,
    analytic_turnover_crossover,
)


def witness(rho: float, *, q: float = 0.9, k: float = 1.0, K: float = 3.8,
            baseline: float = 0.05) -> PlasticCompromise:
    return PlasticCompromise(
        a=3, b=1, delta=2,
        q=q, rho=rho,
        plastic_running_cost=baseline,
        plastic_switch_cost=k,
        module_cost=K,
    )


def brute_force_16_cases(m: PlasticCompromise, alpha: float) -> tuple[float, float]:
    """Independent joint distribution over (past state, now state, past cue, now cue).

    The previous environment is symmetric stationary; independent observation
    errors are conditional on each true state. This directly tests both
    ecological loss and the actual cue-response switching burden.
    """
    expected_loss = 0.0
    cue_switch_probability = 0.0
    for past_state in (0, 1):
        for now_state in (0, 1):
            state_prob = m.rho if past_state != now_state else 1.0 - m.rho
            w1, w2 = ((m.a, m.b) if now_state == 0 else (m.b, m.a))
            for past_cue in (0, 1):
                emit_past = m.q if past_cue == past_state else 1.0-m.q
                for now_cue in (0, 1):
                    emit_now = m.q if now_cue == now_state else 1.0-m.q
                    joint = .5 * state_prob * emit_past * emit_now
                    z = 1 if now_cue == 1 else -1
                    x = m.delta / 2 + alpha * m.trait_optimum_separation*z/2
                    mismatch = w1*x*x + w2*(x-m.delta)**2
                    change = (past_cue != now_cue)
                    expected_loss += joint * (
                        mismatch + m.plastic_running_cost
                        + m.plastic_switch_cost
                        * alpha * m.trait_optimum_separation * change
                    )
                    cue_switch_probability += joint * change
    return expected_loss, cue_switch_probability


@pytest.mark.parametrize("q,rho,alpha", [
    (0.5,0.0,0.0), (1.0,0.0,1.0), (1.0,1.0,0.3),
    (0.9,0.1,0.6), (0.9,0.9,0.42), (0.6,0.37,0.25),
])
def test_exact_stationary_enumeration(q,rho,alpha):
    m=witness(rho,q=q)
    loss, flips=brute_force_16_cases(m,alpha)
    assert isclose(m.plastic_loss(alpha), loss, abs_tol=1e-10)
    assert isclose(m.cue_flip_probability, flips, abs_tol=1e-10)


def test_concurrent_conflict_floor_separate_from_temporal_mismatch():
    m=witness(0.1)
    assert isclose(m.unavoidable_simultaneous_conflict, 3.0)
    assert isclose(m.between_environment_compromise_loss, 1.0)
    assert isclose(m.trait_optimum_separation, 1.0)
    assert isclose(m.shared_loss,4.0)
    assert isclose(m.cue_flip_probability,0.244)
    assert isclose(m.optimal_memoryless_amplitude,0.678)
    assert isclose(m.optimized_plastic_loss,3.590316,abs_tol=1e-8)
    assert m.result()["loss_minimizers"] == ["PLASTIC"]


def test_turnover_switches_best_architecture_despite_constant_conflict_and_cost():
    early=witness(0.1).result()
    late=witness(0.9).result()
    assert early["loss_minimizers"] == ["PLASTIC"]
    assert late["loss_minimizers"] == ["FIXED_MODULES"]
    assert isclose(early["same_time_conflict_floor_C"],late["same_time_conflict_floor_C"])
    assert isclose(early["losses"]["SHARED"],late["losses"]["SHARED"])
    assert isclose(early["losses"]["FIXED_MODULES"],late["losses"]["FIXED_MODULES"])
    assert isclose(late["observed_cue_flip_rate"],0.756)
    assert isclose(late["optimal_plastic_amplitude"],0.422)
    assert isclose(late["losses"]["PLASTIC"],3.871916,abs_tol=1e-8)


def test_interior_turnover_crossover_is_exact_and_reciprocal():
    m=witness(0.25)
    cutoff=analytic_turnover_crossover(m)
    assert cutoff["status"]=="STRICT_INTERIOR_PLASTIC_TO_MODULE_CROSSOVER"
    assert isclose(cutoff["rho_crossing"],.65625,abs_tol=1e-12)
    x=witness(cutoff["rho_crossing"]).result()
    assert isclose(x["losses"]["PLASTIC"], x["losses"]["FIXED_MODULES"],abs_tol=1e-10)
    assert "FIXED_MODULES" in x["loss_minimizers"]
    assert "PLASTIC" in x["loss_minimizers"]
    assert winner_at(.65) == "PLASTIC"
    assert winner_at(.66) == "FIXED_MODULES"


def winner_at(rho):
    return witness(rho).result()["loss_minimizers"][0]


def test_perfect_cue_can_not_remove_simultaneous_shared_coordinate_conflict():
    m=witness(.4,q=1.,k=0.,K=10.,baseline=0.)
    assert m.optimal_memoryless_amplitude == 1.
    assert isclose(m.optimized_plastic_loss,m.unavoidable_simultaneous_conflict)
    assert m.unavoidable_simultaneous_conflict > 0
    assert m.result()["loss_minimizers"] == ["PLASTIC"]


def test_no_state_contrast_or_no_conflict_never_necessitates_new_module():
    equal=PlasticCompromise(
        a=2.,b=2.,delta=2.,q=1.,rho=.7,
        plastic_running_cost=.1,plastic_switch_cost=1.,module_cost=5.,
    )
    assert equal.between_environment_compromise_loss == 0
    assert equal.optimal_memoryless_amplitude == 0
    assert equal.result()["loss_minimizers"] == ["SHARED"]
    neutral=PlasticCompromise(
        a=3.,b=1.,delta=0.,q=1.,rho=.7,
        plastic_running_cost=.1,plastic_switch_cost=1.,module_cost=.3,
    )
    assert neutral.unavoidable_simultaneous_conflict == 0
    assert neutral.shared_loss == 0
    assert neutral.result()["loss_minimizers"] == ["SHARED"]


def test_unreliable_cue_and_high_plastic_cost_make_shared_compromise_win():
    m=witness(.5,q=.5,K=6.,baseline=.1)
    assert m.optimal_memoryless_amplitude==0
    assert m.result()["loss_minimizers"]==["SHARED"]
    assert analytic_turnover_crossover(m)["rho_crossing"] is None


def test_cue_is_not_env_flip_rate_when_observations_noisy():
    m=witness(0.,q=.9)
    assert isclose(m.cue_flip_probability,.18)
    m=witness(1.,q=.9)
    assert isclose(m.cue_flip_probability,.82)
    assert m.cue_flip_probability != m.rho


def test_separate_frequency_dependence_can_prevent_rare_module_invasion():
    x=witness(.9).result(coordination_penalty=.08)
    assert x["loss_minimizers"]==["FIXED_MODULES"]
    assert x["intrinsic_module_vs_best_nonmodule_margin"] > 0
    assert x["hypothetical_rare_module_invasion_margin_given_eta"] < 0
    assert x["not_a_genotype_invasion_without_fitness_frequency_measurement"]


def test_analytic_cutoff_is_hold_outside_identifiable_interior_regime():
    assert analytic_turnover_crossover(witness(.5,k=0))["rho_crossing"] is None
    assert analytic_turnover_crossover(witness(.5,K=4.1))["rho_crossing"] is None
    assert analytic_turnover_crossover(witness(.5,q=.5))["rho_crossing"] is None
    assert analytic_turnover_crossover(witness(.5,K=3.2))["rho_crossing"] is None


@pytest.mark.parametrize("kwargs", [
    {"a":0}, {"b":0}, {"a":.5,"b":1}, {"delta":-1},
    {"q":.49}, {"q":1.1}, {"rho":-.1}, {"rho":1.1},
    {"module_cost":-1}, {"plastic_running_cost":-1},
    {"plastic_switch_cost":-1}, {"q":float("nan")},
    {"plastic_switch_cost":float("inf")},
])
def test_invalid_or_numerically_unsafe_model_rejected(kwargs):
    baseline={
        "a":3,"b":1,"delta":2,"q":.9,"rho":.5,
        "plastic_running_cost":.05,"plastic_switch_cost":1,
        "module_cost":3.8,
    }
    baseline.update(kwargs)
    with pytest.raises(ValueError):
        PlasticCompromise(**baseline)


def test_response_amplitude_and_coordination_are_finite_nonnegative():
    m=witness(.25)
    with pytest.raises(ValueError):
        m.plastic_loss(-.2)
    with pytest.raises(ValueError):
        m.plastic_loss(1.2)
    with pytest.raises(ValueError):
        m.result(coordination_penalty=-1)
