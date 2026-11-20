"""Prospective binary information × correction: SYNTHETIC ONLY.

These tests reject any change that would silently replace the fixed PAYOFF-B
theorem witness, treat trials as independent colonies, or present a simulated
effect as observed biological evidence.
"""
import copy
import statistics

import pytest

from scripts.payoff_b_joint_cue_recourse_design_sim import (
    ARMS, load_contract, model_geometry,
    simulated_colony_mean_loss, estimate_interaction, simulate,
)


def test_exact_paper2_threshold_and_only_highq_highr_window():
    config = load_contract()
    theory = model_geometry(config)
    assert theory["cue_actionability_threshold_q0"] == pytest.approx(0.75)
    assert theory["total_asymmetric_loss_scale"] == pytest.approx(1.6)
    assert theory["baseline_normal_action_expected_loss"] == pytest.approx(.4)
    assert theory["perfect_policy_expected_causal_interaction"] == pytest.approx(.192)
    arms = theory["intervention_arms"]
    assert set(arms) == set(ARMS)
    assert arms["highq_highr"]["gross_information_value"] == pytest.approx(.272)
    assert arms["highq_highr"]["net_information_value_minus_waiting_cost"] == pytest.approx(.192)
    assert arms["highq_lowr"]["net_information_value_minus_waiting_cost"] == pytest.approx(-.016)
    assert arms["lowq_highr"]["gross_information_value"] == pytest.approx(0.0)
    assert sum(v["optimal_wait_for_cue_in_reduced_model"] for v in arms.values()) == 1
    assert not arms["highq_lowr"]["optimal_wait_for_cue_in_reduced_model"]


def test_factorial_direction_is_colony_level_not_trial_pseudoreplication():
    means = {
        "lowq_lowr": [.4,.42,.38,.43],
        "highq_lowr": [.41,.40,.39,.39],
        "lowq_highr": [.39,.41,.44,.38],
        "highq_highr": [.21,.23,.25,.20]
    }
    result = estimate_interaction(means)
    expected = ((.39+.41+.44+.38)/4 - (.21+.23+.25+.20)/4) - (
        (.4+.42+.38+.43)/4 - (.41+.40+.39+.39)/4
    )
    assert result["ITT_loss_difference_in_differences"] == pytest.approx(expected)
    assert result["positive_interaction_lower_bound_above_zero"] is True
    assert result["inference_is_a_synthetic_large_sample_approximation"] is True


def test_missing_randomized_arm_and_one_colony_are_not_fitted():
    valid={a: [.4,.6] for a in ARMS}
    broken=copy.deepcopy(valid)
    del broken["highq_highr"]
    with pytest.raises(ValueError,match="Four original"):
        estimate_interaction(broken)
    broken=copy.deepcopy(valid)
    broken["highq_highr"]=[.4]
    with pytest.raises(ValueError,match="two independent colonies"):
        estimate_interaction(broken)


def test_frozen_contract_cannot_be_changed_to_select_power():
    cfg=load_contract()
    altered=copy.deepcopy(cfg)
    altered["synthetic_power_plan"]["seed"]=20261121
    import json
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as root:
        p=Path(root)/"contract.json"
        p.write_text(json.dumps(altered))
        with pytest.raises(ValueError,match="Synthetic design power contract changed"):
            load_contract(p)
    altered=copy.deepcopy(cfg)
    altered["design"]["randomized_factors"]["corrective_switch_opportunity_r"]=[.35,.8]
    with tempfile.TemporaryDirectory() as root:
        p=Path(root)/"contract.json"
        p.write_text(json.dumps(altered))
        with pytest.raises(ValueError,match="original synthetic numerical witness changed"):
            load_contract(p)


def test_short_seeded_simulation_is_repeatable_and_never_claims_organisms():
    cfg=load_contract()
    first=simulate(cfg,colony_numbers=[8],repetitions=14)
    second=simulate(cfg,colony_numbers=[8],repetitions=14)
    assert first == second
    assert len(first["synthetic_simulation"]) == 3
    assert first["simulation_status"].startswith("SYNTHETIC_DESIGN")
    assert first["frozen_main_Payoff_B_papers_unchanged"] is True
    assert first["does_not_create_an_independent_positive_ecological_record"] is True
    for row in first["synthetic_simulation"]:
        assert row["synthetic_total_colonies"]==32
        assert row["synthetic_trials_per_colony"]==48
        assert row["simulations"]==14
        assert row["calibration_does_not_observe_organism_choices"] is True
    assert first["synthetic_simulation"][0]["theoretical_interaction_given_compliance"]==0
    assert first["synthetic_simulation"][1]["theoretical_interaction_given_compliance"]==pytest.approx(.096)
    assert first["synthetic_simulation"][2]["theoretical_interaction_given_compliance"]==pytest.approx(.144)


def test_colony_level_synthetic_did_approaches_theory_without_fabricated_biology():
    cfg=load_contract()
    result=simulate(cfg,colony_numbers=[16],repetitions=100)
    data={row["synthetic_compliance"]:row for row in result["synthetic_simulation"]}
    assert abs(data[0]["synthetic_mean_estimated_interaction"]) < .055
    assert data[0.75]["synthetic_mean_estimated_interaction"]==pytest.approx(.144, abs=.045)
    assert data[0.50]["synthetic_mean_estimated_interaction"]==pytest.approx(.096, abs=.045)
    # Not a statistical theorem or a promise of biological power; this is
    # a broad controlled check of source code's simulated effect direction.
    assert data[0.75]["synthetic_mean_estimated_interaction"] > data[0.50]["synthetic_mean_estimated_interaction"]


def test_invalid_synthetic_parameters_fail_closed():
    import random
    rng=random.Random(10)
    from scripts.payoff_b_joint_cue_recourse_design_sim import simulated_colony_mean_loss
    with pytest.raises(ValueError,match="Invalid frozen"):
        simulated_colony_mean_loss(
            rng,q=.9,r=1.2,compliance=.8,trials=5,pi=.4,
            cf=2,cm=1,delay=.08,baseline_cluster_noise=0.0
        )


def test_true_zero_compliance_sharp_null_never_acts_on_any_cue():
    import random
    seed=235
    common=dict(compliance=0.0,trials=1500,pi=.4,cf=2,cm=1,
                delay=.08,baseline_cluster_noise=0.0)
    ref=simulated_colony_mean_loss(random.Random(seed),q=.65,r=.20,**common)
    for q,r in ((.65,.85),(.95,.20),(.95,.85)):
        observed=simulated_colony_mean_loss(
            random.Random(seed),q=q,r=r,**common
        )
        # Exactly the same latent states and no waiting, despite different
        # randomized predictive cue and physical re-routing gate.
        assert observed == ref


def test_synthetic_null_power_result_is_not_passing_due_to_truncated_gaussian():
    cfg=load_contract()
    result=simulate(cfg,colony_numbers=[16],repetitions=160)
    d={x["synthetic_compliance"]:x for x in result["synthetic_simulation"]}
    assert abs(d[0]["synthetic_mean_estimated_interaction"]) < 0.045
    assert d[0]["theoretical_interaction_given_compliance"] == 0
    assert d[0]["synthetic_two_sided_rejection_frequency"] < 0.13
    assert d[0]["synthetic_directional_positive_CI_frequency"] < 0.09
    assert d[.75]["synthetic_mean_estimated_interaction"] > .08
