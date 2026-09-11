from src.direct_mu_candidate_pool_audit import LiteratureCandidate, audit_literature_candidate


def make_candidate(**updates):
    data = dict(
        candidate_id="M1_T0",
        source_family="ZHANG_2022",
        named_or_traceable=True,
        archived_or_recoverable_material_declared=True,
        genome_or_marker_characterization_declared=True,
        fitness_or_realization_related_measurement_declared=True,
        exact_registered_marker_class_verified=False,
        same_72_120_context_realization_available=False,
        gross_secondary_rearrangement_resolved=False,
        independent_realization_band_available=False,
    )
    data.update(updates)
    return LiteratureCandidate(**data)


def test_strong_named_literature_candidate_is_carried_forward_but_not_qualified():
    audit = audit_literature_candidate(make_candidate())
    assert audit.carry_forward_candidate
    assert not audit.qualified_reference_now
    assert "REGISTERED_72_120_CONTEXT_REALIZATION_NOT_AVAILABLE" in audit.blockers
    assert "INDEPENDENT_REALIZATION_BAND_NOT_AVAILABLE" in audit.blockers


def test_complete_hypothetical_reference_would_qualify():
    audit = audit_literature_candidate(make_candidate(
        exact_registered_marker_class_verified=True,
        same_72_120_context_realization_available=True,
        gross_secondary_rearrangement_resolved=True,
        independent_realization_band_available=True,
    ))
    assert audit.carry_forward_candidate
    assert audit.qualified_reference_now
    assert audit.blockers == ()


def test_unnamed_pool_is_not_promoted_to_reference_candidate():
    audit = audit_literature_candidate(make_candidate(
        candidate_id="WL11_PANEL",
        named_or_traceable=False,
        archived_or_recoverable_material_declared=False,
        fitness_or_realization_related_measurement_declared=False,
    ))
    assert not audit.carry_forward_candidate
    assert not audit.qualified_reference_now
    assert "REFERENCE_NOT_INDIVIDUALLY_TRACEABLE" in audit.blockers


def test_missing_genomic_characterization_blocks_carry_forward():
    audit = audit_literature_candidate(make_candidate(genome_or_marker_characterization_declared=False))
    assert not audit.carry_forward_candidate
    assert not audit.qualified_reference_now
