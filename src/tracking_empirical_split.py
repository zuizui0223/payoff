"""Deterministic group splits for empirical tracking calibration."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class GroupSplit:
    training_groups: tuple[str, ...]
    held_out_groups: tuple[str, ...]
    holdout_fraction_requested: float

    @property
    def total_groups(self) -> int:
        return len(self.training_groups) + len(self.held_out_groups)

    @property
    def realized_holdout_fraction(self) -> float:
        if self.total_groups == 0:
            return 0.0
        return len(self.held_out_groups) / self.total_groups


def deterministic_group_split(
    groups: Iterable[str],
    *,
    holdout_fraction: float,
    seed: str = "PAYOFF-B",
) -> GroupSplit:
    """Split unique groups by a stable SHA256 rank.

    The result is invariant to row ordering. At least one group is assigned to
    each side, so two or more unique groups are required.
    """

    if not isfinite(holdout_fraction):
        raise ValueError("holdout_fraction must be finite")
    if not 0.0 < holdout_fraction < 1.0:
        raise ValueError("holdout_fraction must lie in (0,1)")

    unique = sorted(
        {
            str(group).strip()
            for group in groups
            if str(group).strip()
        }
    )
    if len(unique) < 2:
        raise ValueError(
            "at least two unique groups are required for holdout validation"
        )

    ranked = sorted(
        unique,
        key=lambda group: sha256(
            f"{seed}|{group}".encode("utf-8")
        ).hexdigest(),
    )
    n_holdout = int(round(holdout_fraction * len(ranked)))
    n_holdout = max(1, min(len(ranked) - 1, n_holdout))

    held_out = tuple(sorted(ranked[:n_holdout]))
    held_set = set(held_out)
    training = tuple(
        sorted(group for group in unique if group not in held_set)
    )
    return GroupSplit(
        training_groups=training,
        held_out_groups=held_out,
        holdout_fraction_requested=holdout_fraction,
    )
