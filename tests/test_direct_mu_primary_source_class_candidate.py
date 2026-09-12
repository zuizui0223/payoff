from src.direct_mu_primary_source_class_candidate import SourceMarkerEvidence, adjudicate_source_class


def test_deep_source_markers_support_candidate_but_not_registered_class_without_exact_panel():
    result = adjudicate_source_class(
        SourceMarkerEvidence(
            entry_marker_loss_supported=True,
            deep_marker_loss_supported=True,
            terminal_deletion_context_supported=True,
            exact_registered_marker_pattern_verified=False,
        )
    )
    assert result.candidate_class == "DEEP_CLASS"
    assert result.candidate_supported
    assert not result.registered_class_qualified
    assert "EXACT_REGISTERED_MARKER_PATTERN_NOT_VERIFIED" in result.blockers


def test_exact_pattern_can_promote_class_only_after_source_candidate_is_supported():
    result = adjudicate_source_class(
        SourceMarkerEvidence(
            entry_marker_loss_supported=True,
            deep_marker_loss_supported=True,
            terminal_deletion_context_supported=True,
            exact_registered_marker_pattern_verified=True,
        )
    )
    assert result.candidate_class == "DEEP_CLASS"
    assert result.registered_class_qualified


def test_deep_marker_alone_without_terminal_deletion_context_is_not_enough():
    result = adjudicate_source_class(
        SourceMarkerEvidence(
            entry_marker_loss_supported=True,
            deep_marker_loss_supported=True,
            terminal_deletion_context_supported=False,
            exact_registered_marker_pattern_verified=False,
        )
    )
    assert result.candidate_class is None
    assert not result.candidate_supported
    assert not result.registered_class_qualified
