"""Exact direct-mu identification from absolute state masses and independent D realization.

Registered two-state model:
    G1 = (1-mu) * g * G0
    D1 = d * D0 + mu * g * G0

If G1, D0, D1 are measured as compatible chromosome-equivalent state masses
and d is independently measured for pre-existing D material, then
    N = D1 - d*D0 = mu*g*G0
    mu = N / (G1 + N)
without separately identifying g.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _fraction(value, name: str) -> Fraction:
    try:
        out = value if isinstance(value, Fraction) else Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be rational-compatible") from exc
    return out


def _nonnegative(value, name: str) -> Fraction:
    out = _fraction(value, name)
    if out < 0:
        raise ValueError(f"{name} must be nonnegative")
    return out


def direct_mu_from_absolute_masses(G0, D0, G1, D1, d) -> tuple[Fraction, Fraction]:
    """Return (mu, g) under the registered absolute-mass two-state model."""
    G0 = _nonnegative(G0, "G0")
    D0 = _nonnegative(D0, "D0")
    G1 = _nonnegative(G1, "G1")
    D1 = _nonnegative(D1, "D1")
    d = _nonnegative(d, "d")
    if G0 <= 0:
        raise ValueError("G0 must be positive")

    new_D = D1 - d * D0
    if new_D < 0:
        raise ValueError("observed D1 is smaller than independently realized pre-existing D mass")
    total_intact_output = G1 + new_D
    if total_intact_output <= 0:
        raise ValueError("G1 plus new D output must be positive")

    mu = new_D / total_intact_output
    g = total_intact_output / G0
    if not (Fraction(0) <= mu <= Fraction(1)):
        raise ValueError("identified mu lies outside [0,1]")
    return mu, g


@dataclass(frozen=True)
class AbsoluteMassMuProjection:
    mu_low: Fraction
    mu_high: Fraction
    new_D_low: Fraction
    new_D_high: Fraction
    physical_model_compatible: bool


def project_direct_mu_absolute_bands(
    *,
    G1_band,
    D0_band,
    D1_band,
    d_band,
) -> AbsoluteMassMuProjection:
    """Exact closed-band projection for mu over a Cartesian uncertainty box.

    All state masses and d are constrained nonnegative. The physical model adds
    N = D1 - d*D0 >= 0. mu=N/(G1+N) is increasing in N and decreasing in G1.
    """
    G1L, G1H = (_nonnegative(x, "G1 band") for x in G1_band)
    D0L, D0H = (_nonnegative(x, "D0 band") for x in D0_band)
    D1L, D1H = (_nonnegative(x, "D1 band") for x in D1_band)
    dL, dH = (_nonnegative(x, "d band") for x in d_band)
    if G1L > G1H or D0L > D0H or D1L > D1H or dL > dH:
        raise ValueError("bands must be ordered closed intervals")

    raw_N_low = D1L - dH * D0H
    raw_N_high = D1H - dL * D0L
    if raw_N_high < 0:
        return AbsoluteMassMuProjection(
            mu_low=Fraction(0),
            mu_high=Fraction(0),
            new_D_low=raw_N_low,
            new_D_high=raw_N_high,
            physical_model_compatible=False,
        )

    N_low = max(Fraction(0), raw_N_low)
    N_high = raw_N_high

    def mu_of(N: Fraction, G: Fraction) -> Fraction:
        denom = G + N
        if denom == 0:
            # Only possible at G=N=0, which carries no output and cannot identify mu.
            raise ValueError("zero total output leaves mu unidentified")
        return N / denom

    mu_low = mu_of(N_low, G1H) if (N_low + G1H) > 0 else Fraction(0)
    if N_high == 0 and G1L == 0:
        mu_high = Fraction(0)
    else:
        mu_high = mu_of(N_high, G1L)

    return AbsoluteMassMuProjection(
        mu_low=mu_low,
        mu_high=mu_high,
        new_D_low=N_low,
        new_D_high=N_high,
        physical_model_compatible=True,
    )
