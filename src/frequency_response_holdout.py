"""Out-of-endpoint validation for the canonical linear PAYOFF frequency response.

The reciprocal invasion endpoints determine
    Delta(0)=u=phi-eta,
    Delta(1)=-v=phi+eta,
so the canonical model predicts the whole interior line
    Delta(p)=(1-p)u-pv = phi+eta(2p-1).

This module treats interior-frequency observations as genuine holdouts. It never
refits phi/eta to those holdouts. Closed prediction and observation bands must
intersect at every registered p; otherwise the canonical linear response is
rejected for the declared context.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Iterable, Sequence

from .reciprocal_invasion_identification import _band, _q


def _frequency(value: object) -> F:
    p = _q(value)
    if not F(0) < p < F(1):
        raise ValueError("holdout frequencies must be strictly interior")
    return p


@dataclass(frozen=True)
class FrequencyHoldout:
    frequency_exact: str
    observed_gap_band_exact: tuple[str, str]
    predicted_gap_band_exact: tuple[str, str]
    compatible: bool
    overlap_band_exact: tuple[str, str] | None


@dataclass(frozen=True)
class FrequencyResponseHoldoutReceipt:
    support_reference: str
    differentiated_into_shared_band_exact: tuple[str, str]
    shared_into_differentiated_band_exact: tuple[str, str]
    holdouts: tuple[FrequencyHoldout, ...]
    all_holdouts_compatible: bool
    canonical_linear_frequency_response_supported: bool
    status: str
    max_registered_frequency_gap_exact: str | None
    scope: str = "predeclared_interior_frequency_holdout_no_refit_closed_bands_two_architecture_PAYOFF"
    endpoints_refit_with_holdouts: bool = False
    nonlinear_frequency_response_identified: bool = False
    finite_population_fixation_identified: bool = False
    historical_causation_identified: bool = False


def validate_frequency_response_holdouts(
    differentiated_into_shared_band: Sequence[object],
    shared_into_differentiated_band: Sequence[object],
    holdouts: Iterable[tuple[object, Sequence[object]]],
    *, support_reference: str,
    resident_contexts_matched_declared: bool,
    common_oriented_gap_scale_declared: bool,
) -> FrequencyResponseHoldoutReceipt:
    """Validate interior Delta(p) bands against endpoint-derived predictions only.

    `differentiated_into_shared_band` is u=Delta(0). `shared_into_differentiated`
    is the rare-S advantage v=-Delta(1), hence Delta(1)=-v. Interior observations
    must be oriented as Delta=payoff(D)-payoff(S) on the SAME positive scale as
    the endpoints. Unknown separate positive scales preserve endpoint signs but
    cannot validate an interior line, so a common oriented-gap scale is required.

    Under independent closed endpoint bands u in [ul,uh], v in [vl,vh],
        Delta(p)=(1-p)u-pv,
    giving the exact prediction interval
        [(1-p)ul-p*vh, (1-p)uh-p*vl].
    Holdouts are never used to tighten endpoints or re-estimate the line.
    """
    if not isinstance(support_reference, str) or not support_reference.strip():
        raise ValueError("declare support provenance")
    if resident_contexts_matched_declared is not True:
        raise ValueError("declare matched resident/context conditions")
    if common_oriented_gap_scale_declared is not True:
        raise ValueError("interior validation requires one common oriented payoff/growth-gap scale")

    ul, uh = _band(differentiated_into_shared_band, "D-in-S endpoint band")
    vl, vh = _band(shared_into_differentiated_band, "S-in-D endpoint band")
    raw = tuple(holdouts)
    if not raw:
        raise ValueError("at least one predeclared interior holdout is required")

    seen: set[F] = set()
    rows: list[FrequencyHoldout] = []
    worst_gap: F | None = None
    for p_raw, obs_raw in raw:
        p = _frequency(p_raw)
        if p in seen:
            raise ValueError("holdout frequencies must be unique")
        seen.add(p)
        ol, oh = _band(obs_raw, "observed interior gap band")
        pl = (1-p)*ul - p*vh
        ph = (1-p)*uh - p*vl
        lo, hi = max(pl, ol), min(ph, oh)
        compatible = lo <= hi
        overlap = (str(lo), str(hi)) if compatible else None
        if compatible:
            gap = F(0)
        elif oh < pl:
            gap = pl-oh
        else:
            gap = ol-ph
        worst_gap = gap if worst_gap is None or gap > worst_gap else worst_gap
        rows.append(FrequencyHoldout(
            str(p), (str(ol), str(oh)), (str(pl), str(ph)), compatible, overlap,
        ))

    ok = all(row.compatible for row in rows)
    return FrequencyResponseHoldoutReceipt(
        support_reference, (str(ul), str(uh)), (str(vl), str(vh)), tuple(rows), ok, ok,
        "canonical_linear_frequency_response_holdout_supported" if ok else
        "canonical_linear_frequency_response_rejected_by_holdout",
        str(worst_gap) if worst_gap is not None else None,
    )
