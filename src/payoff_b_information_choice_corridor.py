"""PAYOFF-B: value-of-information versus cue-guided settlement choice.

Exact, finite-state Bayesian decision calculations. The model is a prospective
toy counterexample / identification aid, NOT a newly proven ecological law or
a biological estimate. Additional information is free, optional, and cannot
decrease optimal expected payoff when the focal feasible action set and other
actors' strategies are held fixed.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class CueCompetition:
    prior_good: float = 0.5
    accuracy: float = 0.8
    value_if_good: float = 4.0
    value_if_bad: float = -2.0
    competitor_density: float = 1.0
    cost_per_competitor: float = 1.0
    cue_before_choice: bool = True


def _finite(value: float) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value)


def evaluate(model: CueCompetition) -> dict:
    """Optimize settlement/avoidance, not ecological fitness from observations.

    Source state is good or bad. The accuracy q is the likelihood P(S=state)
    for either state; q>=0.5. Entering a plot gives V_state - c*d and avoiding
    gives zero. Cue may be discarded; decisions are rational. Competitor
    density is fixed, not an endogenous strategic response.
    """
    for name in ("prior_good", "accuracy", "value_if_good", "value_if_bad",
                 "competitor_density", "cost_per_competitor"):
        if not _finite(getattr(model, name)):
            raise ValueError(f"{name} must be a finite real number")
    if not (0 <= model.prior_good <= 1 and .5 <= model.accuracy <= 1):
        raise ValueError("prior_good in [0,1], accuracy in [0.5,1]")
    if not (model.value_if_good > model.value_if_bad
            and model.cost_per_competitor > 0
            and model.competitor_density >= 0):
        raise ValueError("Need V_good>V_bad, positive cost and nonnegative density")
    if type(model.cue_before_choice) is not bool:
        raise ValueError("cue_before_choice must be bool")

    p, q, vg, vb = (
        model.prior_good, model.accuracy,
        model.value_if_good, model.value_if_bad
    )
    hazard = model.competitor_density * model.cost_per_competitor
    gain_good = vg - hazard
    gain_bad = vb - hazard
    mean_gain = p * gain_good + (1-p) * gain_bad
    no_cue_payoff = max(0.0, mean_gain)

    # Joint masses P(H,S). With p=0 or p=1 some signals are impossible.
    mass_good_signal = p*q + (1-p)*(1-q)
    mass_bad_signal = p*(1-q) + (1-p)*q
    weighted_good_signal_gain = p*q*gain_good + (1-p)*(1-q)*gain_bad
    weighted_bad_signal_gain = p*(1-q)*gain_good + (1-p)*q*gain_bad

    posterior_good = (weighted_good_signal_gain / mass_good_signal
                      if mass_good_signal else None)
    posterior_bad = (weighted_bad_signal_gain / mass_bad_signal
                     if mass_bad_signal else None)

    if model.cue_before_choice:
        value = max(0.0, weighted_good_signal_gain) + max(0.0, weighted_bad_signal_gain)
        choose_good = weighted_good_signal_gain > 0
        choose_bad = weighted_bad_signal_gain > 0
        entry_rate = mass_good_signal*choose_good + mass_bad_signal*choose_bad
    else:
        # Information arriving after an irreversible settlement cannot
        # change *that* settlement decision; future actions are outside scope.
        value = no_cue_payoff
        choose_good = choose_bad = mean_gain > 0
        entry_rate = float(mean_gain > 0)

    voi = value - no_cue_payoff
    if voi < -1e-12:
        raise ArithmeticError("Blackwell/free-disposal nonnegativity violated")

    def threshold(mass: float, weighted: float) -> float | None:
        if mass == 0:
            return None
        return (weighted / mass + hazard) / model.cost_per_competitor

    return {
        "status": "TOY_DECISION_MODEL_NOT_NATURAL_EVIDENCE",
        "no_cue_optimal_expected_payoff": no_cue_payoff,
        "cue_optimal_expected_payoff": value,
        "incremental_information_value": max(0.0, voi),
        "optimal_entry_probability": entry_rate,
        "enter_after_good_signal": bool(choose_good),
        "enter_after_bad_signal": bool(choose_bad),
        "good_signal_probability": mass_good_signal,
        "bad_signal_probability": mass_bad_signal,
        "posterior_entry_gain_good_signal": posterior_good,
        "posterior_entry_gain_bad_signal": posterior_bad,
        "density_enter_boundary_good_signal": threshold(mass_good_signal, weighted_good_signal_gain),
        "density_enter_boundary_bad_signal": threshold(mass_bad_signal, weighted_bad_signal_gain),
        "density_without_cue_boundary": (
            p*vg + (1-p)*vb
        ) / model.cost_per_competitor,
        "entry_is_a_choice_not_value_of_information": True,
        "general_equilibrium_or_social_welfare": "NOT_IDENTIFIED",
        "future_actions_after_commitment": "NOT_MODELLED",
    }


def density_sweep(*, accuracy: float = 0.8) -> list[dict]:
    """Predeclared illustrative grid; NOT fitted to migrant/tit field data."""
    densities = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
    return [
        {"density": density, **evaluate(CueCompetition(
            accuracy=accuracy,
            competitor_density=density
        ))}
        for density in densities
    ]


def route_stage_sweep() -> list[dict]:
    """Constructive comparison: ecological crowding versus decision deadline.

    The focal settlement action remains reversible through stage 4 inclusive.
    Signal accuracy increases monotonically, while competitor density rises.
    Stage 5's signal arrives after commitment.
    Synthetic assumptions are illustrative, not empirical estimates.
    """
    stages = (
        (0, .60, 0.0, True),
        (1, .70, 0.5, True),
        (2, .80, 1.0, True),
        (3, .85, 2.0, True),
        (4, .90, 3.5, True),
        (5, .95, 4.0, False),
    )
    return [
        {
            "stage": stage, "accuracy": q, "density": d,
            "settlement_still_reversible": reversible,
            **evaluate(CueCompetition(
                accuracy=q, competitor_density=d, cue_before_choice=reversible
            )),
        }
        for stage, q, d, reversible in stages
    ]


if __name__ == "__main__":
    import json
    print(json.dumps({"sweep": density_sweep(), "stages": route_stage_sweep()}, indent=2))
