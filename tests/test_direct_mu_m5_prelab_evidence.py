from src.direct_mu_m5_prelab_evidence import M5PrelabEvidence, blockers, next_action


def current(**overrides):
    values = dict(
        archived_material_existence_documented=True,
        physical_stock_access_confirmed=False,
        t0_whole_genome_sequenced=True,
        public_sequence_project_recovered=True,
        exact_t0_sequence_accession_resolved=False,
        chloramphenicol_marker_support=True,
        arginine_auxotrophy_marker_support=True,
        terminal_deletion_context_reported=True,
        direct_registered_marker_pattern_verified=False,
        core_reference_verified=False,
        gross_secondary_rearrangement_resolved=False,
        realization_band_available=False,
    )
    values.update(overrides)
    return M5PrelabEvidence(**values)


def test_primary_source_supports_deep_candidate_without_qualifying_class():
    e = current()
    assert e.deep_class_candidate_supported
    assert not e.deletion_class_qualified
    assert not e.prelab_material_ready
    assert not e.qualified_reference
    assert "REGISTERED_MARKER_PATTERN_NOT_DIRECTLY_VERIFIED" in blockers(e)


def test_archived_stock_existence_does_not_equal_physical_access():
    e = current()
    assert e.archived_material_existence_documented
    assert not e.physical_stock_access_confirmed
    assert next_action(e) == "CONFIRM_CURRENT_M5_T0_STOCK_ACCESS_OR_CUSTODIAN"


def test_sequence_project_does_not_equal_exact_m5_accession():
    e = current(physical_stock_access_confirmed=True)
    assert e.public_sequence_project_recovered
    assert not e.exact_t0_sequence_accession_resolved
    assert next_action(e) == "RESOLVE_EXACT_M5_T0_SEQUENCE_ACCESSION"


def test_direct_marker_check_is_required_even_with_argg_phenotype():
    e = current(
        physical_stock_access_confirmed=True,
        exact_t0_sequence_accession_resolved=True,
    )
    assert e.deep_class_candidate_supported
    assert not e.deletion_class_qualified
    assert next_action(e) == "DIRECTLY_SCORE_REGISTERED_DELETION_MARKERS"


def test_closed_prelab_packet_still_does_not_qualify_without_realization():
    e = current(
        physical_stock_access_confirmed=True,
        exact_t0_sequence_accession_resolved=True,
        direct_registered_marker_pattern_verified=True,
        core_reference_verified=True,
        gross_secondary_rearrangement_resolved=True,
    )
    assert e.deletion_class_qualified
    assert e.prelab_material_ready
    assert not e.qualified_reference
    assert next_action(e) == "RUN_MATCHED_72_120H_D_REALIZATION_ASSAY"


def test_reference_can_only_qualify_after_both_prelab_and_realization():
    e = current(
        physical_stock_access_confirmed=True,
        exact_t0_sequence_accession_resolved=True,
        direct_registered_marker_pattern_verified=True,
        core_reference_verified=True,
        gross_secondary_rearrangement_resolved=True,
        realization_band_available=True,
    )
    assert e.prelab_material_ready
    assert e.qualified_reference
    assert next_action(e) == "RUN_EXISTING_PER_REFERENCE_QUALIFICATION_GATE"
