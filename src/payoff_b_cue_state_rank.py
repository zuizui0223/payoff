"""Pre-outcome PAYOFF-B cue-versus-state experimental design identification gate.

Pure linear-algebra check only. Rank does not prove cue perception, causality,
fitness improvement, or sufficient statistical power. No natural data opened.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable


def factorial_design_row(state: int, signal: int, predecision: int) -> tuple[int, ...]:
    """Saturated 2x2x2 state x signal x decision-time design row.

    Each input must be independently randomized in a genuine future experiment.
    """
    if any(type(x) is not int or x not in (0, 1) for x in (state, signal, predecision)):
        raise ValueError("state, signal, and predecision must be 0/1 integers")
    h, s, t = state, signal, predecision
    return (1, h, s, t, h * s, h * t, s * t, h * s * t)


def exact_rank(rows: Iterable[Iterable[int]]) -> int:
    """Exact Gaussian-elimination rank. Rows must share a common dimension."""
    matrix = [[Fraction(z) for z in row] for row in rows]
    if not matrix:
        return 0
    n = len(matrix[0])
    if any(len(row) != n for row in matrix):
        raise ValueError("Unequal row lengths")
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        k = matrix[rank][col]
        matrix[rank] = [x / k for x in matrix[rank]]
        for r in range(len(matrix)):
            if r == rank:
                continue
            m = matrix[r][col]
            if m:
                matrix[r] = [
                    a - m * b for a, b in zip(matrix[r], matrix[rank])
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def audit() -> dict:
    full = [factorial_design_row(*c) for c in product((0, 1), repeat=3)]
    confounded = [
        factorial_design_row(state, state, predecision)
        for state, predecision in product((0, 1), repeat=2)
    ]
    never_predecision = [
        factorial_design_row(state, signal, 0)
        for state, signal in product((0, 1), repeat=2)
    ]
    return {
        "status": "DESIGN_IDENTIFIABILITY_ONLY",
        "saturated_terms": [
            "intercept", "true_state", "signal", "predecision",
            "state_x_signal", "state_x_predecision",
            "signal_x_predecision", "state_x_signal_x_predecision",
        ],
        "fully_crossed_2x2x2": {"rows": len(full), "rank": exact_rank(full)},
        "cue_equals_state": {
            "rows": len(confounded), "rank": exact_rank(confounded),
            "reason": "true state and signal effects cannot be separated",
        },
        "never_predecision_signal": {
            "rows": len(never_predecision), "rank": exact_rank(never_predecision),
            "reason": "decision-time availability effects cannot be estimated",
        },
        "not_inferred": [
            "causal cue use", "fitness benefit", "perception", "power",
            "physical recourse", "evolutionary novelty",
        ],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(audit(), indent=2))
