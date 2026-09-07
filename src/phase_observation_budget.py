"""Budgeted phase discrimination on a declared FINITE architecture-world panel.

An exact finite-panel result is not a certificate for the continuous compatible
polygons of bounded_error_identification. Responses are bounded-adversarial,
not Gaussian, and bundles are chosen before any outcome is read. The resident
background and the quadratic/triangular family remain fixed assumptions.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import combinations
import json
from typing import Mapping, Sequence

from .bounded_error_identification import _bands, _discriminant, _q


@dataclass(frozen=True)
class ArchitectureWorld:
    name: str
    alpha: object
    kappa: object
    feedback_strength: object
    epsilon: object


@dataclass(frozen=True)
class ContrastQuery:
    name: str
    kind: str  # intrinsic or interaction
    coordinate: object
    error_bound: object
    cost: int = 1


@dataclass(frozen=True)
class PhaseBundle:
    query_names: tuple[str, ...]
    cost: int
    unresolved_cross_phase_pairs: int
    guarantees_panel_phase: bool


@dataclass(frozen=True)
class PhaseBudgetReceipt:
    support_reference: str
    budget: int
    phase_by_world: dict[str, bool]
    cross_phase_pair_count: int
    separating_pairs_by_query: dict[str, tuple[tuple[str, str], ...]]
    optimal_bundles: tuple[PhaseBundle, ...]
    ambiguity_witness: dict | None
    status: str
    objective: str = "min_unseparated_cross_phase_pairs_then_min_cost"
    scope: str = "finite_panel_fixed_bundles_cartesian_bounded_errors_frozen_resident"
    continuous_region_certified: bool = False


def _integer(value: int, name: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _panel(worlds: Sequence[ArchitectureWorld], length: object):
    panel, L = tuple(worlds), _q(length)
    if not panel or L <= 0:
        raise ValueError("nonempty world panel and positive length required")
    if len(panel) > 128:
        raise ValueError("finite-panel exact solver permits at most 128 worlds")
    if any(not isinstance(w.name, str) or not w.name.strip() for w in panel):
        raise ValueError("world names must be nonempty strings")
    if len({w.name for w in panel}) != len(panel):
        raise ValueError("world names must be unique")
    pars = []
    for w in panel:
        a, k, G, e = map(_q, (w.alpha, w.kappa, w.feedback_strength, w.epsilon))
        if min(a, k, G, e) <= 0 or not e < a/k <= L:
            raise ValueError("each world requires positive coefficients and epsilon < rstar <= length")
        pars.append((a, k, G, e))
    if len(set(pars)) != len(pars):
        raise ValueError("duplicate parameter worlds would reweight the pair-count objective")
    phases = tuple(G/k > a/(k*e)-1 and _discriminant(k*e/a, G/k) < 0
                   for a, k, G, e in pars)
    return panel, tuple(pars), phases, L


def _queries(queries: Sequence[ContrastQuery], length: F):
    qs = tuple(queries)
    if len(qs) > 16:
        raise ValueError("exact bundle enumeration permits at most 16 queries")
    if any(not isinstance(q.name, str) or not q.name.strip() for q in qs):
        raise ValueError("query names must be nonempty strings")
    if len({q.name for q in qs}) != len(qs):
        raise ValueError("query names must be unique")
    for q in qs:
        _integer(q.cost, "query cost", 1)
        if q.kind not in ("intrinsic", "interaction"):
            raise ValueError("query kind must be intrinsic or interaction")
        if not 0 < _q(q.coordinate) <= length or _q(q.error_bound) < 0:
            raise ValueError("query coordinate outside domain or negative error bound")
    return qs


def _response(parameters, kind: str, coordinate: object) -> F:
    a, k, G, e = parameters
    x = _q(coordinate)
    return a*x-k*x*x/2 if kind == "intrinsic" else G*x*x*max(F(0), 1-x/e)


def retain_worlds_in_bands(
    worlds: Sequence[ArchitectureWorld], *, intrinsic_bands=(), interaction_bands=(),
    length: object = 1,
) -> tuple[ArchitectureWorld, ...]:
    """Filter a finite panel using the existing simultaneous response-band contract.

    This does not enumerate the whole continuous feasible region. Empty results
    are panel incompatibility, not proof that the biological model is impossible.
    """
    panel, pars, _, L = _panel(worlds, length)
    bb, ab = _bands(intrinsic_bands, L), _bands(interaction_bands, L)
    retained = tuple(w for w, p in zip(panel, pars)
                     if all(lo <= _response(p, kind, x) <= hi
                            for kind, bands in (("intrinsic", bb), ("interaction", ab))
                            for x, lo, hi in bands))
    if not retained:
        raise ValueError("no supplied panel world is compatible with the response bands")
    return retained


def plan_phase_observation_budget(
    worlds: Sequence[ArchitectureWorld], queries: Sequence[ContrastQuery], *,
    budget: int, support_reference: str, matched_contrasts_declared: bool,
    length: object = 1,
) -> PhaseBudgetReceipt:
    """Exact fixed-bundle optimum for an explicit finite panel and integer budget.

    A query separates two worlds iff |prediction_i-prediction_j| > 2*error.
    Equality is NOT separation: their closed response intervals still touch.
    A bundle resolves the binary phase for every possible response iff every
    opposite-phase pair is separated by at least one query in that bundle.
    Unknown cross-query error constraints are not invented; Cartesian intervals
    are the declared adversarial error model. Repeating an unchanged query adds
    no guaranteed separation. No realized outcomes are supplied to this planner.
    """
    B = _integer(budget, "budget")
    if (not isinstance(support_reference, str) or not support_reference.strip()
            or matched_contrasts_declared is not True):
        raise ValueError("declare panel provenance and matched contrasts")
    panel, pars, phases, L = _panel(worlds, length)
    qs = _queries(queries, L)
    pairs = tuple((i, j) for i, j in combinations(range(len(panel)), 2)
                  if phases[i] != phases[j])
    masks, predictions, separated = [], [], {}
    for q in qs:
        ys = tuple(_response(p, q.kind, q.coordinate) for p in pars)
        predictions.append(ys)
        bits = sum(1 << h for h, (i, j) in enumerate(pairs)
                   if abs(ys[i]-ys[j]) > 2*_q(q.error_bound))
        masks.append(bits)
        separated[q.name] = tuple((panel[i].name, panel[j].name)
                                  for h, (i, j) in enumerate(pairs) if bits & (1 << h))
    # Dynamic union of bitsets, but a NON-adaptive exhaustive bundle search.
    costs, covers = [0]*(1 << len(qs)), [0]*(1 << len(qs))
    best_key, choices = None, []
    for subset in range(1 << len(qs)):
        if subset:
            bit = subset & -subset
            j = bit.bit_length()-1
            previous = subset ^ bit
            costs[subset] = costs[previous]+qs[j].cost
            covers[subset] = covers[previous] | masks[j]
        if costs[subset] > B:
            continue
        key = len(pairs)-covers[subset].bit_count(), costs[subset]
        if best_key is None or key < best_key:
            best_key, choices = key, [subset]
        elif key == best_key:
            choices.append(subset)
    bundles = tuple(PhaseBundle(tuple(q.name for j, q in enumerate(qs) if s & (1 << j)),
                               costs[s], len(pairs)-covers[s].bit_count(),
                               covers[s].bit_count() == len(pairs)) for s in choices)
    witness = None
    if best_key[0]:
        subset = choices[0]
        h = next(h for h in range(len(pairs)) if not covers[subset] & (1 << h))
        i, j = pairs[h]
        vector = {}
        for k, q in enumerate(qs):
            if subset & (1 << k):
                e = _q(q.error_bound)
                lo = max(predictions[k][i]-e, predictions[k][j]-e)
                hi = min(predictions[k][i]+e, predictions[k][j]+e)
                assert lo <= hi
                vector[q.name] = str((lo+hi)/2)
        witness = {"world_names": (panel[i].name, panel[j].name),
                   "for_bundle": bundles[0].query_names,
                   "shared_possible_observation_vector": vector}
    status = ("panel_phase_already_identified" if not pairs else
              "guaranteed_panel_phase_resolution" if best_key[0] == 0 else
              "no_guaranteed_resolution_within_declared_budget_and_queries")
    return PhaseBudgetReceipt(support_reference, B,
                              dict(zip((w.name for w in panel), phases)), len(pairs),
                              separated, bundles, witness, status)


def condition_on_phase_bundle(
    worlds: Sequence[ArchitectureWorld], selected_queries: Sequence[ContrastQuery],
    observed_responses: Mapping[str, object], *, length: object = 1,
) -> dict:
    """Use only the actually selected contrasts; never discard incompatible data silently."""
    panel, pars, phases, L = _panel(worlds, length)
    qs = _queries(selected_queries, L)
    if not qs:
        raise ValueError("conditioning requires a nonempty selected bundle")
    if set(observed_responses) != {q.name for q in qs}:
        raise ValueError("responses must cover exactly the selected query names")
    ys = {q.name: _q(observed_responses[q.name]) for q in qs}
    keep = tuple(i for i, p in enumerate(pars)
                 if all(abs(_response(p, q.kind, q.coordinate)-ys[q.name]) <= _q(q.error_bound)
                        for q in qs))
    if not keep:
        raise ValueError("observed bundle contradicts every supplied panel world")
    targets = {phases[i] for i in keep}
    return {"remaining_world_names": tuple(panel[i].name for i in keep),
            "panel_phase_identified": len(targets) == 1,
            "frozen_resident_barrier": next(iter(targets)) if len(targets) == 1 else None,
            "continuous_region_certified": False}


def synthetic_example() -> dict:
    worlds = (ArchitectureWorld("barrier", "0.5", 1, 2, "0.3"),
              ArchitectureWorld("ridge_superior", "0.5", 1, F(16, 9), "0.4"))
    queries = (ContrastQuery("repeat_d_0.1", "interaction", "0.1", "0.005"),
               ContrastQuery("new_d_0.3", "interaction", "0.3", "0.005"))
    receipt = plan_phase_observation_budget(worlds, queries, budget=1,
        support_reference="synthetic two-world witness, NOT a continuous feasible set",
        matched_contrasts_declared=True)
    return {"data_kind": "synthetic_finite_panel", "receipt": asdict(receipt)}


if __name__ == "__main__":
    print(json.dumps(synthetic_example(), indent=2, allow_nan=False))
