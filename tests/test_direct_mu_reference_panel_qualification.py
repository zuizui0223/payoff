import pytest

from src.direct_mu_reference_panel_qualification import (
    DReferenceCandidate,
    adjudicate_reference_panel,
    qualify_d_reference,
)


def candidate(reference_id="r1", deletion_class="ENTRY_CLASS", **updates):
    data = dict(
        reference_id=reference_id,
        deletion_class=deletion_class,
        marker_pattern_verified=True,
        core_reference_present=True,
        pre_existing_at_72h=True,
        same_medium_and_context=True,
        independently_derived=True,
        candidate_outcomes_used_for_selection=False,
        viable_at_72h=True,
        measurable_at_120h=True,
        gross_secondary_rearrangement_unresolved=False,
        realization_band_available=True,
    )
    data.update(updates)
    return DReferenceCandidate(**data)


def test_clean_reference_qualifies():
    q = qualify_d_reference(candidate())
    assert q.qualified
    assert q.blockers == ()


def test_candidate_outcome_selection_is_disqualifying():
    q = qualify_d_reference(candidate(candidate_outcomes_used_for_selection=True))
    assert not q.qualified
    assert "CANDIDATE_OUTCOME_USED_FOR_REFERENCE_SELECTION" in q.blockers


def test_unresolved_secondary_rearrangement_is_disqualifying():
    q = qualify_d_reference(candidate(gross_secondary_rearrangement_unresolved=True))
    assert not q.qualified
    assert "GROSS_SECONDARY_REARRANGEMENT_UNRESOLVED" in q.blockers


def test_missing_realization_band_is_disqualifying():
    q = qualify_d_reference(candidate(realization_band_available=False))
    assert not q.qualified
    assert "REALIZATION_BAND_NOT_AVAILABLE" in q.blockers


def test_panel_requires_two_qualified_independent_references_per_predeclared_class():
    rows = []
    for cls in ("ENTRY_CLASS", "INTERMEDIATE_CLASS", "DEEP_CLASS"):
        rows.extend((candidate(f"{cls}_1", cls), candidate(f"{cls}_2", cls)))
    ready, blockers, qualifications = adjudicate_reference_panel(tuple(rows))
    assert ready
    assert blockers == ()
    assert all(q.qualified for q in qualifications)


def test_one_reference_per_class_is_not_enough():
    rows = tuple(candidate(cls, cls) for cls in ("ENTRY_CLASS", "INTERMEDIATE_CLASS", "DEEP_CLASS"))
    ready, blockers, _ = adjudicate_reference_panel(rows)
    assert not ready
    assert len(blockers) == 3


def test_one_bad_reference_does_not_get_replaced_posthoc_by_lowering_minimum():
    rows = []
    for cls in ("ENTRY_CLASS", "INTERMEDIATE_CLASS", "DEEP_CLASS"):
        rows.extend((candidate(f"{cls}_1", cls), candidate(f"{cls}_2", cls)))
    rows[0] = candidate("ENTRY_bad", "ENTRY_CLASS", realization_band_available=False)
    ready, blockers, _ = adjudicate_reference_panel(tuple(rows))
    assert not ready
    assert any(b.startswith("ENTRY_CLASS_") for b in blockers)
    with pytest.raises(ValueError):
        adjudicate_reference_panel(tuple(rows), minimum_per_class=1)
