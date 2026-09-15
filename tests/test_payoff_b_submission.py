from scripts.build_payoff_b_figures_svg import fig1, fig2
from scripts.build_payoff_b_submission_source import build_submission_source
from scripts.check_payoff_b_submission import check
from scripts.verify_payoff_b_note import verify


def test_submission_source_claim_boundary_and_current_journal_requirements() -> None:
    result = check()
    assert result["status"] == "PASS"
    assert 150 <= result["abstract_words"] <= 250
    assert 4 <= result["keyword_count"] <= 6
    assert result["main_words_pre_references"] <= 4000
    assert result["references"] >= 6
    assert result["internal_target_line_removed"] == "true"
    assert result["declarations_present"] == "true"


def test_submission_overlay_preserves_science_and_adds_metadata_gates() -> None:
    text = build_submission_source()
    assert "**Target:**" not in text
    assert "exactly one stationary point" in text
    assert "Benaïm et al. (2023)" in text
    assert "## Statements and Declarations" in text
    assert "[AUTHOR CONFIRMATION REQUIRED" in text
    assert "[AUTHOR REVIEW REQUIRED BEFORE SUBMISSION.]" in text


def test_exact_note_numerical_receipt() -> None:
    receipt = verify()
    assert receipt["all_checks_pass"] is True
    assert receipt["floquet_formula_cases"] == 81
    assert receipt["numerical_receipt_is_not_proof"] is True
    assert len(receipt["optimum_grid"]) == 12


def test_publication_figures_are_bounded_and_use_correct_claims() -> None:
    one = fig1()
    two = fig2()
    assert 'viewBox="0 0 1200 760"' in one
    assert 'viewBox="0 0 1200 760"' in two
    assert "One finite optimum for every nonzero contrast" in one
    assert "weak-contrast limit 1.606115" in two
    assert "strong-contrast limit 1" in two
