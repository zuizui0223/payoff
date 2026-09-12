"""Panel-level independent-origin gate for Streptomyces direct-mu references.

Individual named lineages are not automatically independent biological origins.
This module prevents multiple descendants of one founding mutant from being
counted as the minimum two independent D references required for a deletion class.
It does not qualify references, measure realization, or promote architecture claims.
"""
from __future__ import annotations

from dataclasses import dataclass

_ALLOWED_CLASSES = frozenset({"ENTRY_CLASS", "INTERMEDIATE_CLASS", "DEEP_CLASS"})


@dataclass(frozen=True)
class OriginTaggedReference:
    reference_id: str
    deletion_class: str
    origin_cluster_id: str
    reference_qualified: bool


@dataclass(frozen=True)
class OriginIndependenceReceipt:
    deletion_class: str
    qualified_reference_count: int
    independent_origin_count: int
    independent_origin_ids: tuple[str, ...]
    minimum_independent_origins: int
    origin_independence_pass: bool


def adjudicate_origin_independence(
    references: tuple[OriginTaggedReference, ...], *, minimum_independent_origins: int = 2
) -> tuple[OriginIndependenceReceipt, ...]:
    if minimum_independent_origins < 2:
        raise ValueError("minimum_independent_origins must be at least two")
    for r in references:
        if not r.reference_id.strip() or not r.origin_cluster_id.strip():
            raise ValueError("reference_id and origin_cluster_id are required")
        if r.deletion_class not in _ALLOWED_CLASSES:
            raise ValueError("deletion_class must be predeclared")

    receipts = []
    for class_id in sorted(_ALLOWED_CLASSES):
        class_refs = tuple(r for r in references if r.deletion_class == class_id and r.reference_qualified)
        origins = tuple(sorted({r.origin_cluster_id for r in class_refs}))
        receipts.append(
            OriginIndependenceReceipt(
                deletion_class=class_id,
                qualified_reference_count=len(class_refs),
                independent_origin_count=len(origins),
                independent_origin_ids=origins,
                minimum_independent_origins=minimum_independent_origins,
                origin_independence_pass=len(origins) >= minimum_independent_origins,
            )
        )
    return tuple(receipts)
