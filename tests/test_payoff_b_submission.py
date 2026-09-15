from scripts.build_payoff_b_figures_svg import fig1, fig2
from scripts.check_payoff_b_submission import check
from scripts.verify_payoff_b_note import verify


def test_brief_manuscript_claim_boundary_and_length() -> None:
    result = check()
    assert result["status"] == "PASS"
    assert result["main_words_pre_references"] <= 4000
    assert result["references"] >= 6


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
    assert "Every nonzero contrast has one finite migration optimum" in one
    assert "weak-contrast limit 1.606115" in two
    assert "strong-contrast limit 1" in two
