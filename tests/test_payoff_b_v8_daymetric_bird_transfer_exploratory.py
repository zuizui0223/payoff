"""Immutable post-outcome scope and output guards for direct day-metric transfer."""
from pathlib import Path

S=Path(__file__).resolve().parents[1]/"analysis/movement_phenology/payoff_b_v8_daymetric_bird_transfer_exploratory.R"
C=Path(__file__).resolve().parents[1]/"docs/PAYOFF_B_V8_DAYMETRIC_BIRD_TRANSFER_EXPLORATORY_LOCK_20261015.md"


def test_exploratory_definition_does_not_change_frozen_primary():
    script=S.read_text(encoding="utf-8")
    contract=C.read_text(encoding="utf-8")
    for x in ("delta_loo_rmse","delta_loo_value_mse",
              "delta_log","delta_pseudo_mismatch","bird_increment"):
        assert x in script and x in contract
    assert "POST_OUTCOME_EXPLORATORY_SIX_SLOPES_COMPLETE" in script
    assert "B <- 10000L" in script
    assert "seed <- 20261015L" in script
    assert 'length(unique(birds$pair_key))!=72L' in script
    assert "nrow(birds)!=150L" in script
    assert "nrow(pairs)!=166L" in script
    assert "nrow(structural)!=150L" in script
    assert "max(abs(joined$delta_log-joined$delta_mismatch)) > 1e-8" in script
    assert "POST-OUTCOME" in contract
    assert "Six fixed descriptive slopes" in contract


def test_all_scientifically_separate_rival_outcomes_preserved():
    script=S.read_text(encoding="utf-8")
    assert 'responses <- c("observed"="delta_log","fixed_arrival"="delta_pseudo_mismatch",' in script
    assert '"bird_increment"="bird_increment"' in script or '"bird_increment"' in script
    assert "beta_per_original_eligible_pair_SD" in script
    assert "ci_excludes_zero" in script
    assert "preregistered=FALSE" in script
    assert "original_registered_transfer_modified=FALSE" in script
    assert "demographic_fitness_effect_identified=FALSE" in script
    assert "all(complete.cases" not in script
    assert "sample(ids,length(ids),replace=TRUE)" in script
