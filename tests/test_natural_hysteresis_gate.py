from src.natural_hysteresis_gate import (
    NaturalHysteresisDataset,
    evaluate_natural_hysteresis_gate,
    rank_evidence_ladder,
)


def test_three_nonoverlapping_windows_define_duration_gate():
    short = NaturalHysteresisDataset(
        name="short",
        years=23,
        has_precommitment_cue=True,
        has_future_destination_state=True,
        has_focal_timing=True,
        has_partner_timing=True,
        has_interaction_outcome=True,
    )
    enough = NaturalHysteresisDataset(
        name="enough",
        years=24,
        has_precommitment_cue=True,
        has_future_destination_state=True,
        has_focal_timing=True,
        has_partner_timing=True,
        has_interaction_outcome=True,
    )

    assert not evaluate_natural_hysteresis_gate(short).direct_hysteresis_ready
    assert evaluate_natural_hysteresis_gate(enough).direct_hysteresis_ready


def test_long_phenology_series_is_not_direct_information_hysteresis_without_cue():
    sweden = NaturalHysteresisDataset(
        name="Kallander_1969_2012",
        years=44,
        has_precommitment_cue=False,
        has_future_destination_state=False,
        has_focal_timing=True,
        has_partner_timing=True,
        has_interaction_outcome=False,
    )

    gate = evaluate_natural_hysteresis_gate(sweden)

    assert gate.duration_passed
    assert not gate.information_pair_passed
    assert not gate.direct_hysteresis_ready
    assert gate.evidence_level == "LONG_TERM_PHENOLOGY_CONTRAST"


def test_two_year_manipulation_remains_information_timing_anchor():
    experiment = NaturalHysteresisDataset(
        name="Samplonius_Both_2017",
        years=2,
        has_precommitment_cue=False,
        has_future_destination_state=True,
        has_focal_timing=True,
        has_partner_timing=True,
        has_interaction_outcome=True,
        experimental_information_timing=True,
    )

    gate = evaluate_natural_hysteresis_gate(experiment)

    assert not gate.direct_hysteresis_ready
    assert gate.evidence_level == "DECISION_TIME_INFORMATION_ANCHOR"


def test_ten_year_competition_series_cannot_be_relabelled_hysteresis():
    competition = NaturalHysteresisDataset(
        name="Samplonius_Both_2019",
        years=10,
        has_precommitment_cue=False,
        has_future_destination_state=True,
        has_focal_timing=True,
        has_partner_timing=True,
        has_interaction_outcome=True,
    )

    gate = evaluate_natural_hysteresis_gate(competition)

    assert not gate.duration_passed
    assert not gate.direct_hysteresis_ready
    assert gate.evidence_level == "INTERACTION_TIMING_CONSEQUENCE"


def test_population_series_without_timing_is_not_direct_hysteresis():
    population = NaturalHysteresisDataset(
        name="Wittwer_1956_2012",
        years=57,
        has_precommitment_cue=False,
        has_future_destination_state=True,
        has_focal_timing=False,
        has_partner_timing=False,
        has_interaction_outcome=True,
    )

    gate = evaluate_natural_hysteresis_gate(population)

    assert gate.duration_passed
    assert gate.evidence_level == "INTERACTION_OUTCOME_ONLY"
    assert not gate.direct_hysteresis_ready


def test_ranking_is_evidence_class_not_numeric_quality_score():
    rows = rank_evidence_ladder(
        [
            NaturalHysteresisDataset(
                name="background",
                years=40,
                has_precommitment_cue=False,
                has_future_destination_state=False,
                has_focal_timing=False,
                has_partner_timing=False,
                has_interaction_outcome=False,
            ),
            NaturalHysteresisDataset(
                name="direct",
                years=30,
                has_precommitment_cue=True,
                has_future_destination_state=True,
                has_focal_timing=True,
                has_partner_timing=True,
                has_interaction_outcome=True,
            ),
        ]
    )

    assert rows[0].dataset.name == "direct"
    assert rows[0].evidence_level == "DIRECT_HYSTERESIS_READY"
