"""Identification for developmental-readiness and decision-control clocks.

Post-freeze PAYOFF-B extension.

The two-clock architecture separates:
- G in [0,1]: physiological/developmental readiness or actuator availability;
- K in [0,1]: effective information weight for signed phase;
- g >= 0: decision/controller gain once the action is available.

Observed correction is governed by the product

    h = G g,

so the mean phase-retention coefficient is

    lambda = phi (1 - h K)

and the innovation-free variance-retention ratio is

    rho = phi^2 [1 - K h(2-h)].

Mean + variance moments can identify K and h when passive retention phi and
process innovation Q are independently known. They cannot, by themselves,
separate G from g.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


_TOL = 1e-12


@dataclass(frozen=True)
class TwoClockForward:
    passive_retention: float
    readiness_gate: float
    decision_gain: float
    information_weight: float
    effective_gain: float
    mean_phase_retention: float
    innovation_free_variance_retention: float


@dataclass(frozen=True)
class TwoClockInverse:
    prior_variance: float
    next_variance: float
    process_variance: float
    passive_retention: float
    mean_phase_retention: float
    normalized_variance_retention: float
    inferred_information_weight: float
    inferred_effective_gain: float


@dataclass(frozen=True)
class ClockSeparation:
    effective_gain: float
    readiness_gate: float
    decision_gain: float
    identified_from: str



@dataclass(frozen=True)
class TwoClockSensitivity:
    """Local sensitivities of mean phase retention."""

    passive_retention: float
    readiness_gate: float
    decision_gain: float
    information_weight: float
    mean_phase_retention: float
    d_lambda_d_phi: float
    d_lambda_d_G: float
    d_lambda_d_g: float
    d_lambda_d_K: float

def _finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _unit(name: str, value: float) -> float:
    x = _finite(name, value)
    if x < 0.0 or x > 1.0:
        raise ValueError(f"{name} must lie in [0,1]")
    return x


def _nonnegative(name: str, value: float) -> float:
    x = _finite(name, value)
    if x < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return x


def two_clock_forward(
    *,
    passive_retention: float,
    readiness_gate: float,
    decision_gain: float,
    information_weight: float,
) -> TwoClockForward:
    """Return mean and variance retention for the two-clock controller."""

    phi = _finite("passive_retention", passive_retention)
    G = _unit("readiness_gate", readiness_gate)
    g = _nonnegative("decision_gain", decision_gain)
    K = _unit("information_weight", information_weight)

    h = G * g
    lam = phi * (1.0 - h * K)
    rho = phi**2 * (1.0 - K * h * (2.0 - h))

    return TwoClockForward(
        passive_retention=phi,
        readiness_gate=G,
        decision_gain=g,
        information_weight=K,
        effective_gain=h,
        mean_phase_retention=lam,
        innovation_free_variance_retention=rho,
    )


def infer_information_and_effective_gain(
    prior_variance: float,
    next_variance: float,
    *,
    process_variance: float,
    passive_retention: float,
    mean_phase_retention: float,
    tolerance: float = 1e-10,
) -> TwoClockInverse:
    """Infer K and h=Gg from mean and variance phase moments.

    Let

        d = 1 - lambda/phi = hK

    and

        v = (P_next-Q)/(phi^2 P)
          = 1 - Kh(2-h).

    Then

        v = 1 - 2d + d^2/K,

    giving

        K = d^2 / (v - 1 + 2d),
        h = d / K.

    G and g are not separately identified without another constraint.
    """

    P = _nonnegative("prior_variance", prior_variance)
    Pn = _nonnegative("next_variance", next_variance)
    Q = _nonnegative("process_variance", process_variance)
    phi = _finite("passive_retention", passive_retention)
    lam = _finite("mean_phase_retention", mean_phase_retention)
    tol = _nonnegative("tolerance", tolerance)

    if P <= _TOL:
        raise ValueError("prior_variance must be positive")
    if abs(phi) <= tol:
        raise ValueError("passive_retention must be nonzero")

    d = 1.0 - lam / phi
    if abs(d) <= tol:
        raise ValueError(
            "K and effective gain are not separately identified when "
            "mean retention equals passive retention"
        )

    v = (Pn - Q) / (phi**2 * P)
    denom = v - 1.0 + 2.0 * d
    if denom <= tol:
        raise ValueError(
            "moments are incompatible with positive information weight "
            "under the declared two-clock Gaussian controller"
        )

    K = d * d / denom
    if K < -tol or K > 1.0 + tol:
        raise ValueError("inferred information weight lies outside [0,1]")
    K = min(max(K, 0.0), 1.0)
    if K <= tol:
        raise ValueError("effective gain is not identified at K=0")

    h = d / K
    if h < -tol:
        raise ValueError("inferred effective gain is negative")
    h = max(h, 0.0)

    return TwoClockInverse(
        prior_variance=P,
        next_variance=Pn,
        process_variance=Q,
        passive_retention=phi,
        mean_phase_retention=lam,
        normalized_variance_retention=v,
        inferred_information_weight=K,
        inferred_effective_gain=h,
    )


def separate_readiness_and_decision_gain(
    effective_gain: float,
    *,
    readiness_gate: float | None = None,
    decision_gain: float | None = None,
    tolerance: float = 1e-10,
) -> ClockSeparation:
    """Separate h=Gg only when G or g is independently known.

    Exactly one of readiness_gate or decision_gain should normally be supplied.
    If both are supplied, the function only verifies their product.
    """

    h = _nonnegative("effective_gain", effective_gain)
    tol = _nonnegative("tolerance", tolerance)

    if readiness_gate is None and decision_gain is None:
        raise ValueError(
            "G and g are not separately identified from effective_gain alone"
        )

    if readiness_gate is not None:
        G = _unit("readiness_gate", readiness_gate)
    else:
        G = None

    if decision_gain is not None:
        g = _nonnegative("decision_gain", decision_gain)
    else:
        g = None

    if G is not None and g is not None:
        if abs(G * g - h) > tol:
            raise ValueError("supplied readiness_gate and decision_gain do not match h")
        return ClockSeparation(
            effective_gain=h,
            readiness_gate=G,
            decision_gain=g,
            identified_from="both_supplied_verified",
        )

    if G is not None:
        if G <= tol:
            if h > tol:
                raise ValueError("positive effective_gain is impossible at G=0")
            raise ValueError("decision_gain is not identified when G=0 and h=0")
        g = h / G
        return ClockSeparation(
            effective_gain=h,
            readiness_gate=G,
            decision_gain=g,
            identified_from="independent_readiness_gate",
        )

    assert g is not None
    if g <= tol:
        if h > tol:
            raise ValueError("positive effective_gain is impossible at g=0")
        raise ValueError("readiness_gate is not identified when g=0 and h=0")
    G = h / g
    if G > 1.0 + tol:
        raise ValueError("inferred readiness_gate exceeds 1")
    G = min(max(G, 0.0), 1.0)
    return ClockSeparation(
        effective_gain=h,
        readiness_gate=G,
        decision_gain=g,
        identified_from="independent_decision_gain",
    )


def reduced_actionability_from_gates(
    readiness_gates: Sequence[float],
    *,
    weights: Sequence[float] | None = None,
) -> float:
    """Return a declared weighted reduced actionability summary.

    This is a convenient reduction,

        r = sum_a omega_a G_a / sum_a omega_a,

    not a universal definition of Paper-2 actionability.
    """

    gates = tuple(_unit("readiness_gate", x) for x in readiness_gates)
    if not gates:
        raise ValueError("at least one readiness gate is required")

    if weights is None:
        ws = (1.0,) * len(gates)
    else:
        ws = tuple(_nonnegative("weight", x) for x in weights)
        if len(ws) != len(gates):
            raise ValueError("weights and readiness_gates must have equal length")

    total = sum(ws)
    if total <= _TOL:
        raise ValueError("positive total weight is required")
    return sum(w * g for w, g in zip(ws, gates)) / total


def two_clock_retention_sensitivity(
    *,
    passive_retention: float,
    readiness_gate: float,
    decision_gain: float,
    information_weight: float,
) -> TwoClockSensitivity:
    """Return exact local derivatives of lambda=phi(1-GgK).

    The active-correction layers are multiplicative complements:

        d lambda / dG = -phi g K
        d lambda / dg = -phi G K
        d lambda / dK = -phi G g.

    Therefore the marginal effect of improving any one layer vanishes when a
    required partner layer is zero.
    """

    phi = _finite("passive_retention", passive_retention)
    G = _unit("readiness_gate", readiness_gate)
    g = _nonnegative("decision_gain", decision_gain)
    K = _unit("information_weight", information_weight)

    lam = phi * (1.0 - G * g * K)
    return TwoClockSensitivity(
        passive_retention=phi,
        readiness_gate=G,
        decision_gain=g,
        information_weight=K,
        mean_phase_retention=lam,
        d_lambda_d_phi=1.0 - G * g * K,
        d_lambda_d_G=-phi * g * K,
        d_lambda_d_g=-phi * G * K,
        d_lambda_d_K=-phi * G * g,
    )


def first_order_controller_difference(
    *,
    passive_retention: float,
    readiness_gate: float,
    decision_gain: float,
    information_weight: float,
    delta_phi: float = 0.0,
    delta_G: float = 0.0,
    delta_g: float = 0.0,
    delta_K: float = 0.0,
) -> float:
    """First-order attribution of actor-to-actor retention difference.

    Around a declared baseline,

        delta_lambda ≈
            (1-GgK) delta_phi
          - phi gK delta_G
          - phi GK delta_g
          - phi Gg delta_K.

    This is a local attribution device, not an exact finite-change
    decomposition for large differences.
    """

    s = two_clock_retention_sensitivity(
        passive_retention=passive_retention,
        readiness_gate=readiness_gate,
        decision_gain=decision_gain,
        information_weight=information_weight,
    )
    return (
        s.d_lambda_d_phi * _finite("delta_phi", delta_phi)
        + s.d_lambda_d_G * _finite("delta_G", delta_G)
        + s.d_lambda_d_g * _finite("delta_g", delta_g)
        + s.d_lambda_d_K * _finite("delta_K", delta_K)
    )
