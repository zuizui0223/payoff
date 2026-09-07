"""Complete small partition sets and an independent exact five-strategy fixture."""
from __future__ import annotations

from math import isfinite
from numbers import Integral


def enumerate_all_partitions(n: int, max_partitions: int = 12):
    """Enumerate Bell(n) partitions; reject excessive size before enumeration."""
    for value, name in ((n, "n"), (max_partitions, "max_partitions")):
        if isinstance(value, bool) or not isinstance(value, Integral) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    # Saturated Stirling recurrence avoids building an enormous Bell integer.
    counts = [1]
    for size in range(1, n + 1):
        counts = [0] + [min(max_partitions + 1, (counts[k - 1] if k - 1 < len(counts) else 0) + (k * counts[k] if k < len(counts) else 0)) for k in range(1, size + 1)]
        if sum(counts) > max_partitions:
            raise ValueError("full partition set exceeds max_partitions")
    result = []
    def visit(i, blocks):
        if i == n:
            result.append(tuple(tuple(block) for block in blocks))
            return
        for j in range(len(blocks)):
            blocks[j].append(i)
            visit(i + 1, blocks)
            blocks[j].pop()
        blocks.append([i])
        visit(i + 1, blocks)
        blocks.pop()
    visit(0, [])
    return tuple(result)


def registered_five_partition_problem():
    """Synthetic theta=(0,1,3), a=(1,1,1), extra-module cost=1."""
    return {
        "names": ("S", "M01", "M02", "M12", "F"),
        "partitions": enumerate_all_partitions(3),
        "intrinsic_payoffs": (0.0, 19 / 6, -5 / 6, 5 / 3, 8 / 3),
        "n": 3,
    }


def exact_five_partition_frequencies(h: float):
    """Closed form in order S,M01,M02,M12,F; valid for h=-gamma>=0."""
    h = float(h)
    if not isfinite(h) or h < 0:
        raise ValueError("h must be finite and non-negative")
    if h <= 0.5:
        return (0.0, 1.0, 0.0, 0.0, 0.0)
    if h <= 1.0:
        return (0.0, 0.5 + 1 / (4 * h), 0.0, 0.0, 0.5 - 1 / (4 * h))
    if h <= 13 / 6:
        return (0.0, 0.5 + 1 / (4 * h), 0.0, 0.5 - 1 / (2 * h), 1 / (4 * h))
    return (0.5 - 13 / (12 * h), 4 / (3 * h), 0.0, 7 / (12 * h), 0.5 - 5 / (6 * h))


def restricted_three_partition_frequencies(h: float):
    """Previous S,M01,F solution, embedded in the complete five-strategy set."""
    h = float(h)
    if not isfinite(h) or h < 0:
        raise ValueError("h must be finite and non-negative")
    if h <= 0.5:
        return (0.0, 1.0, 0.0, 0.0, 0.0)
    p_f = 0.5 - 1 / (4 * h)
    if h <= 19 / 12:
        return (0.0, 1 - p_f, 0.0, 0.0, p_f)
    return (0.5 - 19 / (24 * h), 25 / (24 * h), 0.0, 0.0, p_f)
