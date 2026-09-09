import pytest

from src.evidence_lane_separation import (
    ArchitectureMappingReceipt,
    GenericGameReceipt,
    RawArchiveReceipt,
    adjudicate_evidence_lanes,
    validate_architecture_mapping_receipt,
    validate_generic_game_receipt,
)


def raw(**kw):
    base = dict(
        system_id="SYS",
        dataset_id="DATA",
        support_reference="RAW_REF",
        bytes_acquired=True,
        checksum_verified=True,
        manifest_reconstructed=True,
        schema_reconstructed=True,
        transformations_reconstructed=True,
        raw_analysis_reproduced=True,
    )
    base.update(kw)
    return RawArchiveReceipt(**base)


def game(**kw):
    base = dict(
        system_id="SYS",
        comparison_id="PAIR",
        strategy_unit_id="UNIT",
        dataset_id=None,
        support_reference="GAME_REF",
        evidence_source_mode="published_text",
        frequency_support_declared=True,
        common_outcome_scale_declared=True,
        generic_game_result_recovered=True,
        architecture_semantics_used_declared=False,
    )
    base.update(kw)
    return GenericGameReceipt(**base)


def arch(**kw):
    base = dict(
        system_id="SYS",
        comparison_id="PAIR",
        architecture_unit_id="UNIT",
        support_reference="ARCH_REF",
        integrated_shared_candidate_declared=True,
        differentiated_released_candidate_declared=True,
        matched_net_task_declared=True,
        heritable_or_stable_unit_declared=True,
        unit_consistency_declared=True,
        mapping_independent_of_game_result_declared=True,
    )
    base.update(kw)
    return ArchitectureMappingReceipt(**base)


def adjudicate(g=None, a=None, r=None, align=True):
    return adjudicate_evidence_lanes(
        g or game(),
        a or arch(),
        raw=r,
        pair_alignment_declared=align,
        pair_alignment_reference="ALIGN_REF",
    )


def test_raw_success_does_not_auto_promote_game_or_architecture():
    g = game(generic_game_result_recovered=False)
    a = arch(differentiated_released_candidate_declared=False)
    x = adjudicate(g, a, raw())
    assert x.raw_reconstruction_certified
    assert x.raw_analysis_reproduction_certified
    assert not x.generic_game_validation_certified
    assert not x.architecture_mapping_certified
    assert not x.architecture_specific_claim_licensed


def test_generic_game_success_does_not_imply_architecture_mapping():
    a = arch(integrated_shared_candidate_declared=False)
    x = adjudicate(game(), a)
    assert x.generic_game_validation_certified
    assert not x.architecture_mapping_certified
    assert x.generic_game_claim_allowed
    assert not x.architecture_specific_claim_licensed


def test_architecture_mapping_success_does_not_imply_generic_game_result():
    g = game(frequency_support_declared=False)
    x = adjudicate(g, arch())
    assert x.architecture_mapping_certified
    assert x.architecture_mapping_claim_allowed
    assert not x.generic_game_validation_certified
    assert not x.architecture_specific_claim_licensed


def test_raw_archive_game_requires_certified_matching_raw_receipt():
    g = game(
        evidence_source_mode="raw_archive",
        dataset_id="DATA",
    )
    x_missing = adjudicate(g, arch(), None)
    assert not x_missing.generic_game_validation_certified
    assert "RAW_RECEIPT_REQUIRED_FOR_RAW_ARCHIVE_GAME_EVIDENCE" in x_missing.blockers

    x_bad = adjudicate(
        g,
        arch(),
        raw(checksum_verified=False),
    )
    assert not x_bad.generic_game_validation_certified
    assert "RAW_RECONSTRUCTION_NOT_CERTIFIED" in x_bad.blockers

    x_ok = adjudicate(g, arch(), raw())
    assert x_ok.raw_reconstruction_certified
    assert x_ok.generic_game_validation_certified


def test_raw_reconstruction_does_not_require_analysis_reproduction():
    r = raw(raw_analysis_reproduced=False)
    assert r.reconstruction_certified
    assert not r.analysis_reproduction_certified


def test_game_lane_rejects_architecture_semantics_leakage():
    with pytest.raises(ValueError):
        validate_generic_game_receipt(
            game(architecture_semantics_used_declared=True)
        )


def test_architecture_lane_rejects_mapping_derived_from_game_outcome():
    with pytest.raises(ValueError):
        validate_architecture_mapping_receipt(
            arch(mapping_independent_of_game_result_declared=False)
        )


def test_same_system_comparison_and_unit_plus_two_certified_lanes_license_claim():
    x = adjudicate(game(), arch(), align=True)
    assert x.generic_game_validation_certified
    assert x.architecture_mapping_certified
    assert x.pair_alignment_certified
    assert x.architecture_specific_claim_licensed


@pytest.mark.parametrize(
    "g,a,blocker",
    [
        (game(system_id="SYS_G"), arch(system_id="SYS_A"), "GAME_ARCHITECTURE_SYSTEM_MISMATCH"),
        (game(comparison_id="PAIR_G"), arch(comparison_id="PAIR_A"), "GAME_ARCHITECTURE_COMPARISON_MISMATCH"),
        (game(strategy_unit_id="CELL"), arch(architecture_unit_id="COLONY"), "GAME_ARCHITECTURE_STRATEGIC_UNIT_MISMATCH"),
    ],
)
def test_mismatched_pair_cannot_promote_even_when_each_lane_passes(g, a, blocker):
    x = adjudicate(g, a)
    assert x.generic_game_validation_certified
    assert x.architecture_mapping_certified
    assert not x.pair_alignment_certified
    assert not x.architecture_specific_claim_licensed
    assert blocker in x.blockers


def test_explicit_alignment_declaration_is_required():
    x = adjudicate(game(), arch(), align=False)
    assert not x.pair_alignment_certified
    assert not x.architecture_specific_claim_licensed
    assert "PAIR_ALIGNMENT_NOT_DECLARED" in x.blockers


def test_pstutzeri_pattern_generic_game_pass_architecture_fail():
    g = game(
        system_id="PSTUTZERI_2022",
        comparison_id="GENERALIST_VS_NITRITE_SPECIALIST",
        strategy_unit_id="CELL_TYPE",
        support_reference="PUBLISHED_RECIPROCAL_SIGN_V1",
    )
    a = arch(
        system_id="PSTUTZERI_2022",
        comparison_id="GENERALIST_VS_NITRITE_SPECIALIST",
        architecture_unit_id="CELL_TYPE",
        differentiated_released_candidate_declared=False,
    )
    x = adjudicate(g, a)
    assert x.generic_game_validation_certified
    assert not x.architecture_mapping_certified
    assert not x.architecture_specific_claim_licensed


def test_streptomyces_pattern_architecture_signal_but_wrong_frequency_unit():
    g = game(
        system_id="STREPTOMYCES",
        comparison_id="WT_VS_SPECIALIST_CELL",
        strategy_unit_id="CELL",
    )
    a = arch(
        system_id="STREPTOMYCES",
        comparison_id="DOL_ARCH_VS_GENERALIST_ARCH",
        architecture_unit_id="COLONY_ARCHITECTURE",
    )
    x = adjudicate(g, a)
    assert x.generic_game_validation_certified
    assert x.architecture_mapping_certified
    assert not x.architecture_specific_claim_licensed
    assert "GAME_ARCHITECTURE_COMPARISON_MISMATCH" in x.blockers
    assert "GAME_ARCHITECTURE_STRATEGIC_UNIT_MISMATCH" in x.blockers


def test_raw_provenance_mismatch_is_explicit():
    g = game(
        evidence_source_mode="raw_archive",
        dataset_id="DATA_A",
    )
    x = adjudicate(g, arch(), raw(dataset_id="DATA_B"))
    assert not x.generic_game_validation_certified
    assert "RAW_GAME_PROVENANCE_MISMATCH" in x.blockers
