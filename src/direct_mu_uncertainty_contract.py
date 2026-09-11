"""Pre-outcome bounded uncertainty construction for Streptomyces direct-mu.

The contract is deterministic rather than distributional. A response-blind
validation panel fixes an assay-specific maximum absolute error before focal
candidate outcomes are opened. Focal measurements are then converted to closed
nonnegative bands, realization fold-change bands are propagated exactly, and
reference heterogeneity is retained by a closed envelope rather than pooled.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _f(value, name: str) -> Fraction:
    try:
        out = value if isinstance(value, Fraction) else Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be rational-compatible") from exc
    return out


def nonnegative_measurement_band(estimate, max_absolute_error) -> tuple[Fraction, Fraction]:
    """Closed nonnegative band from a frozen absolute-error bound."""
    x = _f(estimate, "estimate")
    e = _f(max_absolute_error, "max_absolute_error")
    if x < 0 or e < 0:
        raise ValueError("estimate and error bound must be nonnegative")
    return max(Fraction(0), x - e), x + e


def max_absolute_validation_error(estimates, truths) -> Fraction:
    """Freeze the worst absolute error on a predeclared response-blind panel."""
    est = tuple(_f(x, "validation estimate") for x in estimates)
    tru = tuple(_f(x, "validation truth") for x in truths)
    if not est or len(est) != len(tru):
        raise ValueError("nonempty validation estimates and truths must match")
    if any(x < 0 for x in est + tru):
        raise ValueError("validation quantities must be nonnegative")
    return max(abs(a - b) for a, b in zip(est, tru))


def positive_ratio_band(numerator_band, denominator_band) -> tuple[Fraction, Fraction]:
    """Exact Cartesian projection of a nonnegative numerator / positive denominator."""
    nL, nH = (_f(x, "numerator band") for x in numerator_band)
    dL, dH = (_f(x, "denominator band") for x in denominator_band)
    if nL < 0 or dL < 0 or nL > nH or dL > dH:
        raise ValueError("bands must be ordered and nonnegative")
    if dL <= 0:
        raise ValueError("denominator lower bound must be strictly positive")
    return nL / dH, nH / dL


def envelope_closed_bands(bands) -> tuple[Fraction, Fraction]:
    """Conservative closed envelope; never pool reference heterogeneity toward a mean."""
    checked = []
    for band in bands:
        if len(band) != 2:
            raise ValueError("each band needs lower and upper endpoints")
        lo, hi = (_f(x, "band endpoint") for x in band)
        if lo < 0 or lo > hi:
            raise ValueError("bands must be ordered and nonnegative")
        checked.append((lo, hi))
    if not checked:
        raise ValueError("at least one band is required")
    return min(lo for lo, _ in checked), max(hi for _, hi in checked)


@dataclass(frozen=True)
class DirectMuUncertaintyContract:
    response_blind_validation_panel_frozen: bool
    max_absolute_error_rule_frozen: bool
    candidate_outcomes_used_to_tune_error_bound: bool
    closed_nonnegative_bands_declared: bool
    exact_ratio_propagation_declared: bool
    d_reference_envelope_declared: bool
    parametric_distribution_assumed: bool
    favorable_reference_pooling_allowed: bool

    @property
    def frozen_preoutcome(self) -> bool:
        return bool(
            self.response_blind_validation_panel_frozen
            and self.max_absolute_error_rule_frozen
            and not self.candidate_outcomes_used_to_tune_error_bound
            and self.closed_nonnegative_bands_declared
            and self.exact_ratio_propagation_declared
            and self.d_reference_envelope_declared
            and not self.parametric_distribution_assumed
            and not self.favorable_reference_pooling_allowed
        )
