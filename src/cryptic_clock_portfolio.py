"""Cryptic clock-portfolio divergence under opportunity loss.

Post-freeze PAYOFF-B theory.

A historical timing strategy allocates required log-precision P between:
- entry-clock precision x;
- downstream feedback precision f = 2 n y.

Define feedback share

    s = f / P,

so x = (1-s)P and f=sP.

If a fraction omega of historically usable downstream correction opportunity
remains after environmental change, while the historical allocation is retained,
then

    V_disrupted / V_target = exp[(1-omega) s P].

Two species can therefore have identical historical final precision but diverge
after the same opportunity loss if their hidden feedback shares differ.

This module also gives pairwise mismatch-variance inflation for two zero-mean
timing errors under a retained correlation witness.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, sqrt


_TOL=1e-12


@dataclass(frozen=True)
class PortfolioDisruption:
    historical_target_variance: float
    precision_budget: float
    feedback_share: float
    opportunity_retained: float
    inflation_factor: float
    disrupted_variance: float


@dataclass(frozen=True)
class PortfolioPairDivergence:
    species_1: PortfolioDisruption
    species_2: PortfolioDisruption
    log_variance_ratio_after: float
    variance_ratio_after: float


@dataclass(frozen=True)
class PairMismatchInflation:
    historical_variance_each: float
    historical_correlation: float
    inflation_factor_1: float
    inflation_factor_2: float
    historical_mismatch_variance: float
    disrupted_mismatch_variance: float
    mismatch_inflation_ratio: float
    mean_inflation_component: float
    asymmetry_penalty: float


def _finite(name: str, value: float) -> float:
    x=float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _positive(name: str, value: float) -> float:
    x=_finite(name,value)
    if x<=0.0:
        raise ValueError(f"{name} must be positive")
    return x


def _unit(name: str, value: float) -> float:
    x=_finite(name,value)
    if x<0.0 or x>1.0:
        raise ValueError(f"{name} must lie in [0,1]")
    return x


def disrupted_portfolio_variance(
    *,
    historical_target_variance: float,
    precision_budget: float,
    feedback_share: float,
    opportunity_retained: float,
) -> PortfolioDisruption:
    """Return immediate variance inflation after opportunity loss.

    If the historical strategy hits target V* using feedback share s, and only
    fraction omega of downstream opportunity remains,

        F = V_disrupted / V*
          = exp[(1-omega) s P].
    """

    vstar=_positive("historical_target_variance",historical_target_variance)
    P=_finite("precision_budget",precision_budget)
    if P<0.0:
        raise ValueError("precision_budget must be non-negative")
    s=_unit("feedback_share",feedback_share)
    omega=_unit("opportunity_retained",opportunity_retained)

    F=exp((1.0-omega)*s*P)
    return PortfolioDisruption(
        historical_target_variance=vstar,
        precision_budget=P,
        feedback_share=s,
        opportunity_retained=omega,
        inflation_factor=F,
        disrupted_variance=vstar*F,
    )


def cryptic_portfolio_pair_divergence(
    *,
    historical_target_variance_1: float,
    precision_budget_1: float,
    feedback_share_1: float,
    opportunity_retained_1: float,
    historical_target_variance_2: float,
    precision_budget_2: float,
    feedback_share_2: float,
    opportunity_retained_2: float,
) -> PortfolioPairDivergence:
    """Return post-disruption variance divergence for two hidden portfolios.

    In general,

        log(V1'/V2')
          = log(V1*/V2*)
            + (1-omega1)s1 P1
            - (1-omega2)s2 P2.

    If historical targets, P and omega are equal, this reduces to

        log(V1'/V2')
          = (1-omega)P(s1-s2).

    Thus historically indistinguishable final precision can conceal different
    fragility.
    """

    a=disrupted_portfolio_variance(
        historical_target_variance=historical_target_variance_1,
        precision_budget=precision_budget_1,
        feedback_share=feedback_share_1,
        opportunity_retained=opportunity_retained_1,
    )
    b=disrupted_portfolio_variance(
        historical_target_variance=historical_target_variance_2,
        precision_budget=precision_budget_2,
        feedback_share=feedback_share_2,
        opportunity_retained=opportunity_retained_2,
    )
    lr=log(a.disrupted_variance/b.disrupted_variance)
    return PortfolioPairDivergence(
        species_1=a,
        species_2=b,
        log_variance_ratio_after=lr,
        variance_ratio_after=exp(lr),
    )


def critical_opportunity_retention(
    *,
    precision_budget: float,
    feedback_share: float,
    tolerated_variance_inflation: float,
) -> float | None:
    """Return omega threshold below which tolerated inflation is exceeded.

    Solve

        exp[(1-omega)sP] = T

    for omega:

        omega_crit = 1 - log(T)/(sP).

    If sP=0, opportunity loss has no effect and no finite threshold exists.
    The returned threshold is clipped to [0,1] only when the tolerance is
    reachable inside that range. If the threshold is <=0, even total loss does
    not exceed the declared tolerance, so None is returned.
    """

    P=_finite("precision_budget",precision_budget)
    if P<0.0:
        raise ValueError("precision_budget must be non-negative")
    s=_unit("feedback_share",feedback_share)
    T=_positive("tolerated_variance_inflation",tolerated_variance_inflation)
    if T<1.0:
        raise ValueError("tolerated_variance_inflation must be at least 1")

    denom=s*P
    if denom<=_TOL:
        return None
    crit=1.0-log(T)/denom
    if crit<=0.0:
        return None
    if crit>=1.0:
        return 1.0
    return crit


def pairwise_mismatch_variance_inflation(
    *,
    historical_variance_each: float,
    historical_correlation: float,
    inflation_factor_1: float,
    inflation_factor_2: float,
) -> PairMismatchInflation:
    """Return pairwise timing-mismatch variance after unequal fragility.

    Witness assumptions:
    - both actors historically have zero-mean timing errors with equal variance V*;
    - their historical error correlation is r in [-1,1);
    - environmental change inflates their variances by F1 and F2;
    - the correlation coefficient remains r.

    Historical mismatch variance:

        M* = 2 V* (1-r).

    Disrupted mismatch variance:

        M' = V* [F1 + F2 - 2 r sqrt(F1 F2)].

    Therefore

        M'/M*
          = (F1+F2)/2
            + r/[2(1-r)] (sqrt(F1)-sqrt(F2))^2.

    The second term is an asymmetry penalty: correlated partners suffer extra
    mismatch when hidden clock portfolios inflate differently.
    """

    v=_positive("historical_variance_each",historical_variance_each)
    r=_finite("historical_correlation",historical_correlation)
    if r < -1.0 or r >= 1.0:
        raise ValueError("historical_correlation must lie in [-1,1)")
    f1=_positive("inflation_factor_1",inflation_factor_1)
    f2=_positive("inflation_factor_2",inflation_factor_2)

    m0=2.0*v*(1.0-r)
    m1=v*(f1+f2-2.0*r*sqrt(f1*f2))
    ratio=m1/m0
    mean_component=0.5*(f1+f2)
    asymmetry=r/(2.0*(1.0-r))*(sqrt(f1)-sqrt(f2))**2

    if abs(ratio-(mean_component+asymmetry))>1e-10:
        raise AssertionError("mismatch inflation identity failed")

    return PairMismatchInflation(
        historical_variance_each=v,
        historical_correlation=r,
        inflation_factor_1=f1,
        inflation_factor_2=f2,
        historical_mismatch_variance=m0,
        disrupted_mismatch_variance=m1,
        mismatch_inflation_ratio=ratio,
        mean_inflation_component=mean_component,
        asymmetry_penalty=asymmetry,
    )
