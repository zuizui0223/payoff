"""Stagewise information and signed recourse for seasonal tracking.

This module is a prospective PAYOFF-B extension. It does not alter the frozen
Paper 2 submission model.

Two gaps are addressed explicitly:

1. The existing compensated-deadline model only corrects positive raw delay.
   Here phase error is signed. Positive error means late and can be corrected
   by speeding up / compressing stopovers; negative error means early and can
   be corrected by slowing down / extending stopovers.

2. The existing hidden-state deadline functions compare no state information
   with perfect state revelation before compensation. Here a noisy en-route
   signal interpolates between those endpoints.

The finite-signal result is standard Bayesian value-of-information / recourse
mathematics. PAYOFF-B should not claim generic novelty for that theorem. Its
role is to make the ecological "Schroedinger's spring" analogy precise:
the future seasonal state can remain latent while the feasible recourse set
shrinks as commitment proceeds.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Sequence


_TOL = 1e-12


@dataclass(frozen=True)
class SignedRecourseResult:
    """Optimal one-stage timing correction for a signed phase error."""

    phase_error: float
    advance_capacity: float
    delay_capacity: float
    correction_cost_per_unit: float
    residual_loss_per_unit: float
    direct_commit_cost: float
    optimal_correction: float
    residual_phase_error: float
    effective_cost: float
    mode: str


@dataclass(frozen=True)
class FiniteSignalRecourse:
    """Bayes risks before and after a noisy en-route signal."""

    no_signal_risk: float
    post_signal_risk: float
    perfect_information_risk: float
    signal_value: float
    perfect_information_value: float
    signal_action_indices: tuple[int, ...]
    no_signal_action_index: int
    allowed_actions: tuple[int, ...]


def _finite_nonnegative(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return x


def signed_linear_phase_recourse(
    phase_error: float,
    *,
    advance_capacity: float,
    delay_capacity: float,
    correction_cost_per_unit: float,
    residual_loss_per_unit: float,
    direct_commit_cost: float = 0.0,
) -> SignedRecourseResult:
    """Return the optimal signed temporal correction.

    Sign convention
    ---------------
    phase_error > 0
        The actor is late. Positive correction advances progress, e.g. faster
        migration or shorter stopovers.

    phase_error < 0
        The actor is early. Negative correction delays progress, e.g. slower
        migration or longer stopovers.

    The feasible correction interval is
        [-delay_capacity, +advance_capacity].

    Loss is
        direct_commit_cost
        + kappa * |correction|
        + mu * |phase_error - correction|.

    With kappa < mu, correction is the projection of the phase error onto the
    feasible interval. With kappa >= mu, correction is not worth buying and
    the deterministic tie rule chooses zero.
    """

    error = float(phase_error)
    if not isfinite(error):
        raise ValueError("phase_error must be finite")

    advance = _finite_nonnegative("advance_capacity", advance_capacity)
    delay = _finite_nonnegative("delay_capacity", delay_capacity)
    kappa = _finite_nonnegative(
        "correction_cost_per_unit", correction_cost_per_unit
    )
    mu = _finite_nonnegative("residual_loss_per_unit", residual_loss_per_unit)
    direct = _finite_nonnegative("direct_commit_cost", direct_commit_cost)

    if kappa < mu:
        correction = min(max(error, -delay), advance)
    else:
        correction = 0.0

    residual = error - correction
    effective = direct + kappa * abs(correction) + mu * abs(residual)

    if correction > _TOL:
        mode = "speed_up_or_compress"
    elif correction < -_TOL:
        mode = "slow_or_wait"
    else:
        mode = "none"

    return SignedRecourseResult(
        phase_error=error,
        advance_capacity=advance,
        delay_capacity=delay,
        correction_cost_per_unit=kappa,
        residual_loss_per_unit=mu,
        direct_commit_cost=direct,
        optimal_correction=correction,
        residual_phase_error=residual,
        effective_cost=effective,
        mode=mode,
    )


def _validate_prior(prior: Sequence[float]) -> tuple[float, ...]:
    probs = tuple(float(x) for x in prior)
    if not probs:
        raise ValueError("prior must be non-empty")
    if any((not isfinite(x)) or x < 0.0 for x in probs):
        raise ValueError("prior probabilities must be finite and non-negative")
    if abs(sum(probs) - 1.0) > 1e-10:
        raise ValueError("prior probabilities must sum to one")
    return probs


def _validate_signal(
    signal_likelihoods: Sequence[Sequence[float]],
    n_states: int,
) -> tuple[tuple[float, ...], ...]:
    rows = tuple(tuple(float(x) for x in row) for row in signal_likelihoods)
    if len(rows) != n_states:
        raise ValueError("signal_likelihoods must have one row per state")
    if not rows or not rows[0]:
        raise ValueError("signal_likelihoods must be non-empty")
    n_signals = len(rows[0])
    if any(len(row) != n_signals for row in rows):
        raise ValueError("signal_likelihood rows must have equal length")
    for row in rows:
        if any((not isfinite(x)) or x < 0.0 for x in row):
            raise ValueError("signal probabilities must be finite and non-negative")
        if abs(sum(row) - 1.0) > 1e-10:
            raise ValueError("each state-specific signal row must sum to one")
    return rows


def _validate_losses(
    loss_matrix: Sequence[Sequence[float]],
    n_states: int,
) -> tuple[tuple[float, ...], ...]:
    losses = tuple(tuple(float(x) for x in row) for row in loss_matrix)
    if not losses:
        raise ValueError("loss_matrix must contain at least one action")
    if any(len(row) != n_states for row in losses):
        raise ValueError("each action loss row must have one value per state")
    if any((not isfinite(x)) for row in losses for x in row):
        raise ValueError("loss values must be finite")
    return losses


def finite_signal_recourse(
    prior: Sequence[float],
    signal_likelihoods: Sequence[Sequence[float]],
    loss_matrix: Sequence[Sequence[float]],
    *,
    allowed_actions: Iterable[int] | None = None,
) -> FiniteSignalRecourse:
    """Compute exact Bayes risk with noisy en-route information.

    Parameters
    ----------
    prior
        P(H=h) over latent seasonal states.
    signal_likelihoods
        Matrix P(Z=z | H=h), indexed [state][signal].
    loss_matrix
        Loss L(a,h), indexed [action][state].
    allowed_actions
        Recourse actions still feasible after the signal. Restricting this set
        represents increasing irreversibility.

    Returns
    -------
    The no-signal Bayes risk, post-signal Bayes risk, perfect-information risk,
    and the corresponding values of information.

    Notes
    -----
    post_signal_risk is evaluated as
        sum_z min_a sum_h P(h)P(z|h)L(a,h),
    so posterior normalization is unnecessary.

    With a singleton allowed action set, signal_value is exactly zero: learning
    the state cannot improve behavior after all recourse has been lost.
    """

    probs = _validate_prior(prior)
    signal = _validate_signal(signal_likelihoods, len(probs))
    losses = _validate_losses(loss_matrix, len(probs))

    if allowed_actions is None:
        actions = tuple(range(len(losses)))
    else:
        actions = tuple(sorted(set(int(i) for i in allowed_actions)))
        if not actions:
            raise ValueError("allowed_actions must be non-empty")
        if any(i < 0 or i >= len(losses) for i in actions):
            raise ValueError("allowed action index out of bounds")

    action_prior_risks = tuple(
        sum(p * losses[a][h] for h, p in enumerate(probs))
        for a in actions
    )
    no_pos = min(range(len(actions)), key=lambda i: action_prior_risks[i])
    no_action = actions[no_pos]
    no_signal = action_prior_risks[no_pos]

    n_signals = len(signal[0])
    chosen = []
    post_signal = 0.0
    for z in range(n_signals):
        risks = tuple(
            sum(
                probs[h] * signal[h][z] * losses[a][h]
                for h in range(len(probs))
            )
            for a in actions
        )
        pos = min(range(len(actions)), key=lambda i: risks[i])
        chosen.append(actions[pos])
        post_signal += risks[pos]

    perfect = sum(
        probs[h] * min(losses[a][h] for a in actions)
        for h in range(len(probs))
    )

    signal_value = no_signal - post_signal
    perfect_value = no_signal - perfect
    if signal_value < -1e-10:
        raise AssertionError("post-signal optimization increased Bayes risk")
    if perfect_value < -1e-10:
        raise AssertionError("perfect information increased Bayes risk")

    return FiniteSignalRecourse(
        no_signal_risk=no_signal,
        post_signal_risk=post_signal,
        perfect_information_risk=perfect,
        signal_value=max(0.0, signal_value),
        perfect_information_value=max(0.0, perfect_value),
        signal_action_indices=tuple(chosen),
        no_signal_action_index=no_action,
        allowed_actions=actions,
    )



@dataclass(frozen=True)
class BinaryActionability:
    """Information value when only a fraction of full recourse remains."""

    cue_accuracy: float
    recourse_fraction: float
    wrong_state_loss: float
    no_signal_risk: float
    post_signal_risk: float
    information_value: float


def binary_actionability_value(
    cue_accuracy: float,
    recourse_fraction: float,
    *,
    wrong_state_loss: float = 1.0,
) -> BinaryActionability:
    """Exact binary information value with partial retained optionality.

    Consider the canonical symmetric two-state problem with prior 1/2.

    With probability/weight r, the actor can still implement the cue-matched
    action. With the remaining 1-r, the earlier commitment is effectively
    irreversible and the cue cannot alter behavior.

    Mixing those two regimes gives

        R0 = W/2
        R(q,r) = (1-r) W/2 + r W(1-q)
        V(q,r) = r W (q - 1/2).

    Thus information quality and retained actionability enter multiplicatively
    in this declared reduced model. Better information can have declining
    behavioral value if optionality disappears faster than q improves.
    """

    q = float(cue_accuracy)
    r = float(recourse_fraction)
    if not isfinite(q) or q < 0.5 or q > 1.0:
        raise ValueError("cue_accuracy must lie in [0.5, 1]")
    if not isfinite(r) or r < 0.0 or r > 1.0:
        raise ValueError("recourse_fraction must lie in [0, 1]")
    wrong = _finite_nonnegative("wrong_state_loss", wrong_state_loss)

    no_signal = 0.5 * wrong
    post = (1.0 - r) * no_signal + r * wrong * (1.0 - q)
    value = no_signal - post
    return BinaryActionability(
        cue_accuracy=q,
        recourse_fraction=r,
        wrong_state_loss=wrong,
        no_signal_risk=no_signal,
        post_signal_risk=post,
        information_value=max(0.0, value),
    )


def actionability_profile(
    cue_accuracies: Sequence[float],
    recourse_fractions: Sequence[float],
    *,
    wrong_state_loss: float = 1.0,
) -> tuple[BinaryActionability, ...]:
    """Evaluate a route/stage profile of improving information and shrinking recourse."""

    if len(cue_accuracies) != len(recourse_fractions) or not cue_accuracies:
        raise ValueError("cue_accuracies and recourse_fractions must align and be non-empty")
    return tuple(
        binary_actionability_value(
            q,
            r,
            wrong_state_loss=wrong_state_loss,
        )
        for q, r in zip(cue_accuracies, recourse_fractions)
    )

def binary_schrodinger_spring(
    cue_accuracy: float,
    *,
    wrong_state_loss: float = 1.0,
    allowed_actions: Iterable[int] | None = None,
) -> FiniteSignalRecourse:
    """Canonical two-state 'Schroedinger's spring' signal problem.

    States are EARLY and LATE spring with prior 1/2. Signals report EARLY or
    LATE with symmetric accuracy q >= 1/2. Two actions are matched responses to
    the two states.

    With both actions feasible:
        no-signal risk = W/2
        post-signal risk = W(1-q)
        signal value = W(q-1/2).

    With only one action feasible, the signal value is zero regardless of q.
    """

    q = float(cue_accuracy)
    if not isfinite(q) or q < 0.5 or q > 1.0:
        raise ValueError("cue_accuracy must lie in [0.5, 1]")
    wrong = _finite_nonnegative("wrong_state_loss", wrong_state_loss)

    return finite_signal_recourse(
        [0.5, 0.5],
        [
            [q, 1.0 - q],
            [1.0 - q, q],
        ],
        [
            [0.0, wrong],
            [wrong, 0.0],
        ],
        allowed_actions=allowed_actions,
    )
