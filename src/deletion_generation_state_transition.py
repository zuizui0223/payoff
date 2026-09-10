"""Realization-separated identification of deletion-generation fraction.

Lane A mechanism-measurement layer only.

For one registered deletion class, let G_t and D_t be intact and deleted
chromosome-equivalent lineage mass at the beginning of an interval.  The
registered two-state transition is

    G_{t+1} = (1-mu) g G_t
    D_{t+1} = d D_t + mu g G_t

where `mu` is the fraction of new generalist output entering the deletion class
and `r=d/g` is the independently measured relative realization of an already
deleted lineage over the same interval/context.

If f_t=D_t/(G_t+D_t), then

    mu = f_{t+1} - r*f_t*(1-f_{t+1})/(1-f_t).

Thus a final mutant fraction alone is not a generation-rate estimand, but two
state censuses plus an independently bounded realization ratio identify `mu`
under this declared transition model.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _q(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("use an exact rational-compatible value")


def _fraction(value: object, name: str, *, strict_upper: bool = True) -> Fraction:
    q = _q(value)
    upper_ok = q < 1 if strict_upper else q <= 1
    if q < 0 or not upper_ok:
        op = "[0,1)" if strict_upper else "[0,1]"
        raise ValueError(f"{name} must lie in {op}")
    return q


def _band(value: tuple[object, object], name: str, *, nonnegative: bool = False) -> tuple[Fraction, Fraction]:
    if not isinstance(value, tuple) or len(value) != 2:
        raise ValueError(f"{name} must be a two-element tuple")
    lo, hi = _q(value[0]), _q(value[1])
    if lo > hi:
        raise ValueError(f"{name} lower bound exceeds upper bound")
    if nonnegative and lo < 0:
        raise ValueError(f"{name} must be nonnegative")
    return lo, hi


def deletion_odds(deletion_fraction: object) -> Fraction:
    f = _fraction(deletion_fraction, "deletion_fraction")
    return f / (1 - f)


def generation_fraction_from_states(
    deletion_fraction_t: object,
    deletion_fraction_next: object,
    relative_deleted_realization: object,
) -> Fraction:
    """Return exact `mu` implied by two state fractions and r=d/g."""
    f0 = _fraction(deletion_fraction_t, "deletion_fraction_t")
    f1 = _fraction(deletion_fraction_next, "deletion_fraction_next")
    r = _q(relative_deleted_realization)
    if r < 0:
        raise ValueError("relative_deleted_realization must be nonnegative")
    return f1 - r * f0 * (1 - f1) / (1 - f0)


@dataclass(frozen=True)
class GenerationFractionBandReceipt:
    deletion_fraction_t_band: tuple[Fraction, Fraction]
    deletion_fraction_next_band: tuple[Fraction, Fraction]
    relative_deleted_realization_band: tuple[Fraction, Fraction]
    raw_mu_projection: tuple[Fraction, Fraction]
    biological_mu_band: tuple[Fraction, Fraction] | None
    transition_model_compatible: bool
    point_identified: bool
    scope: str = "two_state_deletion_generation_identification"


def generation_fraction_band_from_states(
    deletion_fraction_t_band: tuple[object, object],
    deletion_fraction_next_band: tuple[object, object],
    relative_deleted_realization_band: tuple[object, object],
) -> GenerationFractionBandReceipt:
    """Exact Cartesian-band projection for `mu`.

    `mu(f0,f1,r)` is decreasing in f0 and r and increasing in f1 for the
    admissible domain. Therefore the exact extrema over closed Cartesian bands
    occur at opposite corners, without numerical optimization.
    """
    f0_lo, f0_hi = _band(deletion_fraction_t_band, "deletion_fraction_t_band")
    f1_lo, f1_hi = _band(deletion_fraction_next_band, "deletion_fraction_next_band")
    for value, name in (
        (f0_lo, "f0 lower"), (f0_hi, "f0 upper"),
        (f1_lo, "f1 lower"), (f1_hi, "f1 upper"),
    ):
        _fraction(value, name)
    r_lo, r_hi = _band(relative_deleted_realization_band, "relative_deleted_realization_band", nonnegative=True)

    raw_lo = generation_fraction_from_states(f0_hi, f1_lo, r_hi)
    raw_hi = generation_fraction_from_states(f0_lo, f1_hi, r_lo)

    bio_lo = max(raw_lo, Fraction(0))
    bio_hi = min(raw_hi, Fraction(1))
    compatible = bio_lo <= bio_hi
    bio = (bio_lo, bio_hi) if compatible else None
    return GenerationFractionBandReceipt(
        deletion_fraction_t_band=(f0_lo, f0_hi),
        deletion_fraction_next_band=(f1_lo, f1_hi),
        relative_deleted_realization_band=(r_lo, r_hi),
        raw_mu_projection=(raw_lo, raw_hi),
        biological_mu_band=bio,
        transition_model_compatible=compatible,
        point_identified=bool(compatible and bio_lo == bio_hi),
    )


@dataclass(frozen=True)
class GenerationReductionReceipt:
    control_mu_band: tuple[Fraction, Fraction]
    probe_mu_band: tuple[Fraction, Fraction]
    material_reduction: Fraction
    guaranteed_reduction_lower_bound: Fraction
    possible_reduction_upper_bound: Fraction
    generation_result: str
    scope: str = "predeclared_material_generation_reduction_classification"


def classify_generation_reduction(
    control_mu_band: tuple[object, object],
    probe_mu_band: tuple[object, object],
    *,
    material_reduction: object,
) -> GenerationReductionReceipt:
    """Map mu bands to the preregistered RED-triangulation outcome categories.

    Closed bands are handled conservatively:
    - `reduced` only if every compatible pair exceeds the material threshold;
    - `material_reduction_excluded` only if every compatible pair is below it;
    - equality/contact remains `unresolved`.
    """
    c_lo, c_hi = _band(control_mu_band, "control_mu_band")
    p_lo, p_hi = _band(probe_mu_band, "probe_mu_band")
    for value, name in ((c_lo, "control lower"), (c_hi, "control upper"), (p_lo, "probe lower"), (p_hi, "probe upper")):
        if not (0 <= value <= 1):
            raise ValueError(f"{name} must lie in [0,1]")
    delta = _q(material_reduction)
    if delta < 0:
        raise ValueError("material_reduction must be nonnegative")

    guaranteed = c_lo - p_hi
    possible = c_hi - p_lo
    if guaranteed > delta:
        result = "reduced"
    elif possible < delta:
        result = "material_reduction_excluded"
    else:
        result = "unresolved"

    return GenerationReductionReceipt(
        control_mu_band=(c_lo, c_hi),
        probe_mu_band=(p_lo, p_hi),
        material_reduction=delta,
        guaranteed_reduction_lower_bound=guaranteed,
        possible_reduction_upper_bound=possible,
        generation_result=result,
    )
