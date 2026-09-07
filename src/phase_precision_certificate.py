"""Exact precision limits for PAYOFF's declared finite architecture panel.

This does not calibrate a biological model or certify an unenumerated continuous
parameter region. Each query's Cartesian closed error band is multiplied by a
common nonnegative scale. Zero-error queries remain exact at every finite scale.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
import json
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from .phase_observation_budget import ArchitectureWorld, ContrastQuery


def _rational(value: object) -> F:
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric bound")
    try:
        return F(value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("bounds must be finite rational-compatible numbers") from exc


@dataclass(frozen=True)
class PairPrecisionLimit:
    world_names: tuple[str, str]
    # None means +infinity, not an unknown or failed calculation.
    critical_error_scale_exact: str | None
    maximizing_queries: tuple[str, ...]


@dataclass(frozen=True)
class PhasePrecisionReceipt:
    support_reference: str
    phase_by_world: dict[str, bool]
    cross_phase_pair_count: int
    critical_error_scale_exact: str | None
    identifiable_at_declared_errors: bool
    pair_limits: tuple[PairPrecisionLimit, ...]
    blocking_pair: tuple[str, str] | None
    common_response_at_critical: dict[str, str] | None
    status: str
    scope: str = "finite_panel_cartesian_bounded_errors_common_error_scaling_frozen_resident"
    continuous_region_certified: bool = False
    mutation_radius_identified: bool = False

    def identifiable_at_error_scale(self, scale: object) -> bool:
        """Unlimited acquisition budget; equality at a finite limit FAILS.

        This is a property of the full declared vocabulary, not affordability.
        Decimal strings and Fraction values preserve intended exact boundaries.
        """
        value = _rational(scale)
        if value < 0:
            raise ValueError("error scale must be nonnegative")
        return (self.critical_error_scale_exact is None
                or value < F(self.critical_error_scale_exact))


def _certificate_from_responses(
    world_names: Sequence[str], phases: Sequence[bool],
    query_names: Sequence[str], response_rows: Sequence[Sequence[object]],
    error_bounds: Sequence[object], *, support_reference: str,
) -> PhasePrecisionReceipt:
    """Algebraic core; rows index queries, columns index finite worlds.

    Public callers should use certify_phase_precision so phase labels and
    responses are computed from the actual PAYOFF architecture formulas.
    """
    names, labels, qs = tuple(world_names), tuple(phases), tuple(query_names)
    rows = tuple(tuple(_rational(y) for y in row) for row in response_rows)
    errors = tuple(_rational(e) for e in error_bounds)
    if not isinstance(support_reference, str) or not support_reference.strip():
        raise ValueError("declare panel provenance")
    if (not names or len(labels) != len(names)
            or any(type(label) is not bool for label in labels)):
        raise ValueError("nonempty worlds and one boolean phase per world required")
    for values in (names, qs):
        if (any(not isinstance(v, str) or not v.strip() for v in values)
                or len(set(values)) != len(values)):
            raise ValueError("world and query names must each be unique nonempty strings")
    if (len(rows) != len(qs) or len(errors) != len(qs)
            or any(len(row) != len(names) for row in rows)
            or any(e < 0 for e in errors)):
        raise ValueError("response dimensions must match and errors must be nonnegative")

    limits: list[PairPrecisionLimit] = []
    critical: F | None = None
    blocking: tuple[int, int] | None = None
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if labels[i] == labels[j]:
                continue
            exact_separators = tuple(q for q, row, e in zip(qs, rows, errors)
                                     if e == 0 and row[i] != row[j])
            if exact_separators:
                limits.append(PairPrecisionLimit((names[i], names[j]), None,
                                                 exact_separators))
                continue
            # Identical exact predictions contribute zero, not 0/0.
            ratios = tuple(abs(row[i] - row[j]) / (2 * e) if e else F(0)
                           for row, e in zip(rows, errors))
            limit = max(ratios, default=F(0))
            winners = tuple(q for q, ratio in zip(qs, ratios) if ratio == limit)
            limits.append(PairPrecisionLimit((names[i], names[j]), str(limit), winners))
            if critical is None or limit < critical:
                critical, blocking = limit, (i, j)

    common = None
    pair = None
    if blocking is not None:
        i, j = blocking
        pair = names[i], names[j]
        common = {}
        for q, row, e in zip(qs, rows, errors):
            lo = max(row[i], row[j]) - critical * e
            hi = min(row[i], row[j]) + critical * e
            if lo > hi:
                raise ArithmeticError("blocking-pair certificate lost interval intersection")
            common[q] = str((lo + hi) / 2)
    status = ("panel_phase_already_identified" if not limits else
              "unbounded_finite_error_scale_tolerance" if critical is None else
              "not_identifiable_even_at_zero_error" if critical == 0 else
              "finite_precision_limit")
    return PhasePrecisionReceipt(
        support_reference, dict(zip(names, labels)), len(limits),
        None if critical is None else str(critical),
        critical is None or F(1) < critical, tuple(limits), pair, common, status,
    )


def certify_phase_precision(
    worlds: Sequence[ArchitectureWorld], queries: Sequence[ContrastQuery], *,
    support_reference: str, matched_contrasts_declared: bool, length: object = 1,
) -> PhasePrecisionReceipt:
    """Exact full-vocabulary precision threshold, independent of design budget.

    At scale t query q permits y_q(w) +/- t*error_bound_q. Let
        t_ij = max_q |y_q(i)-y_q(j)|/(2*error_bound_q)
    for every opposite-phase pair, treating a separating zero-error query as
    +infinity and an identical exact query as zero. Then t_* = min_ij t_ij.
    The finite panel is identifiable iff 0 <= t < t_*. At a finite t_* the
    returned pair and common response vector defeat EVERY adaptive policy.
    With one phase only, all finite scales are identifiable with no acquisition.

    Query costs are validated by the existing adapter but do not enter this
    unlimited-budget feasibility certificate. Use the existing adaptive/fixed
    solvers separately for acquisition costs. Work is O(worlds**2 * queries).
    """
    from .phase_observation_budget import _panel, _queries, _response

    if matched_contrasts_declared is not True:
        raise ValueError("declare matched contrasts")
    panel, parameters, phases, L = _panel(worlds, length)
    qs = _queries(queries, L)
    rows = tuple(tuple(_response(p, q.kind, q.coordinate) for p in parameters)
                 for q in qs)
    return _certificate_from_responses(
        tuple(w.name for w in panel), phases, tuple(q.name for q in qs), rows,
        tuple(q.error_bound for q in qs), support_reference=support_reference,
    )


def main() -> None:
    """Emit a reproducible synthetic receipt, never an empirical conclusion."""
    from .phase_observation_budget import ArchitectureWorld, ContrastQuery

    worlds = (
        ArchitectureWorld("low_alpha_wide", "1/2", 1, "16/9", "2/5"),
        ArchitectureWorld("low_alpha_middle", "1/2", 1, 2, "3/10"),
        ArchitectureWorld("high_alpha_middle", "19/20", 1, 2, "3/10"),
        ArchitectureWorld("high_alpha_narrow", "19/20", 1, "10/3", "1/4"),
    )
    queries = (
        ContrastQuery("B_half", "intrinsic", "1/2", "1/1000"),
        ContrastQuery("A_fifth", "interaction", "1/5", "1/1000"),
        ContrastQuery("A_tenth", "interaction", "1/10", "1/1000"),
    )
    receipt = certify_phase_precision(
        worlds, queries, support_reference="synthetic_registered_four_world_routing_witness",
        matched_contrasts_declared=True,
    )
    print(json.dumps(asdict(receipt), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
