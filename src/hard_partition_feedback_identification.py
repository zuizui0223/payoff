"""Identify hard-partition distance feedback from endpoint population contrasts."""

from __future__ import annotations

from typing import Dict, Sequence, Tuple


def endpoint_gap_inversion(delta0: float, delta1: float) -> Dict[str, float]:
    """Return phi=(d0+d1)/2 and eta=(d1-d0)/2."""

    return {
        "phi": 0.5 * (delta0 + delta1),
        "eta": 0.5 * (delta1 - delta0),
    }


def reciprocal_invasion_inversion(
    invading_second_into_first: float,
    invading_first_into_second: float,
) -> Dict[str, float]:
    """Invert reciprocal rare-invasion margins into canonical phi,eta.

    I_second = Delta(0)=phi-eta
    I_first  =-Delta(1)=-phi-eta
    """

    i_second = invading_second_into_first
    i_first = invading_first_into_second
    return {
        "phi": 0.5 * (i_second - i_first),
        "eta": -0.5 * (i_second + i_first),
    }


def gamma_from_endpoint_gaps(
    delta0: float,
    delta1: float,
    partition_distance: float,
) -> Dict[str, float]:
    """Return phi,eta,gamma from endpoint gaps and q>0."""

    if partition_distance <= 0.0:
        raise ValueError("partition_distance must be positive")
    result = endpoint_gap_inversion(delta0, delta1)
    return {
        **result,
        "partition_distance": partition_distance,
        "gamma": result["eta"] / partition_distance,
    }


def gamma_from_reciprocal_invasions(
    invading_second_into_first: float,
    invading_first_into_second: float,
    partition_distance: float,
) -> Dict[str, float]:
    """Return phi,eta,gamma from reciprocal invasion margins and q>0."""

    if partition_distance <= 0.0:
        raise ValueError("partition_distance must be positive")
    result = reciprocal_invasion_inversion(
        invading_second_into_first,
        invading_first_into_second,
    )
    return {
        **result,
        "partition_distance": partition_distance,
        "gamma": result["eta"] / partition_distance,
    }


def weighted_common_gamma_fit(
    etas: Sequence[float],
    partition_distances: Sequence[float],
    analysis_weights: Sequence[float] | None = None,
) -> Dict[str, object]:
    """Fit eta_j=gamma*q_j by zero-intercept weighted least squares."""

    n = len(etas)
    if n == 0 or len(partition_distances) != n:
        raise ValueError("etas and partition_distances must have same non-zero length")
    if any(float(q) <= 0.0 for q in partition_distances):
        raise ValueError("partition_distances must be positive")
    if analysis_weights is None:
        weights = [1.0] * n
    else:
        if len(analysis_weights) != n:
            raise ValueError("analysis_weights must match input length")
        if any(float(weight) <= 0.0 for weight in analysis_weights):
            raise ValueError("analysis_weights must be positive")
        weights = [float(weight) for weight in analysis_weights]

    q = [float(value) for value in partition_distances]
    eta = [float(value) for value in etas]
    numerator = sum(w * qi * ei for w, qi, ei in zip(weights, q, eta))
    denominator = sum(w * qi * qi for w, qi in zip(weights, q))
    gamma = numerator / denominator
    predicted = tuple(gamma * qi for qi in q)
    residuals = tuple(observed - fitted for observed, fitted in zip(eta, predicted))
    implied = tuple(observed / qi for observed, qi in zip(eta, q))
    weighted_sse = sum(w * r * r for w, r in zip(weights, residuals))
    return {
        "gamma_hat": gamma,
        "implied_gammas": implied,
        "predicted_etas": predicted,
        "residuals": residuals,
        "weighted_sse": weighted_sse,
    }


def architecture_phi_residual(observed_phi: float, intrinsic_first: float, intrinsic_second: float) -> float:
    """Return phi_obs-(b_second-b_first)."""

    return observed_phi - (intrinsic_second - intrinsic_first)
