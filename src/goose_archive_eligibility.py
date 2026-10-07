"""Source-faithful eligibility helpers for archived barnacle-goose tracks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class GooseEligibilityAudit:
    archived_rows: int
    eligible_rows: int
    excluded_rows: int
    eligible_animal_ids: tuple[str, ...]
    excluded_animal_ids: tuple[str, ...]
    exclusion_reasons: tuple[str, ...]


def audit_reference_eligibility(
    reference_rows: Sequence[Mapping[str, object]],
) -> GooseEligibilityAudit:
    """Apply only explicit archive-level exclusion flags.

    The public Movebank reference data associated with Kölzsch et al. contain
    deployment IDs such as

        70568-not used
        78040-not used
        78042a-not used
        78042b-not used.

    This helper excludes a deployment only when its deployment-id explicitly
    contains "not used" (case-insensitive). It does not infer exclusion from
    track length, timing, movement outcome, or any PAYOFF response.

    Additional paper-specific eligibility rules, if discovered, must be added
    explicitly rather than silently inferred from the data.
    """

    if not reference_rows:
        raise ValueError("reference_rows must be non-empty")

    eligible = []
    excluded = []
    reasons = []

    seen = set()
    for row in reference_rows:
        if "animal-id" not in row or "deployment-id" not in row:
            raise ValueError("reference rows require animal-id and deployment-id")
        animal = str(row["animal-id"]).strip()
        deployment = str(row["deployment-id"]).strip()
        if not animal:
            raise ValueError("animal-id must be non-empty")
        if animal in seen:
            raise ValueError(f"duplicate animal-id in reference data: {animal}")
        seen.add(animal)

        if "not used" in deployment.lower():
            excluded.append(animal)
            reasons.append(f"{animal}: deployment-id={deployment}")
        else:
            eligible.append(animal)

    return GooseEligibilityAudit(
        archived_rows=len(reference_rows),
        eligible_rows=len(eligible),
        excluded_rows=len(excluded),
        eligible_animal_ids=tuple(sorted(eligible)),
        excluded_animal_ids=tuple(sorted(excluded)),
        exclusion_reasons=tuple(sorted(reasons)),
    )
