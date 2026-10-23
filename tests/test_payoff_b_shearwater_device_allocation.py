"""Confirm original source-device denominators before interpreting attrition."""
import json
from pathlib import Path
import pytest
from scripts.audit_payoff_b_shearwater_device_allocation import run

def original():
    return json.loads(Path(
        "data/payoff_b_shearwater_experiment_sensor_coverage_20261023.json"
    ).read_text(encoding="utf-8"))

def test_olfactory_arm_was_not_all_equipped_with_GPS():
    x=run(original())
    assert x["GPS_equipped_by_original_publication"]=={
        "control":9,"magnetic_disruption":9,"olfactory_deprivation":9}
    assert x["GPS_valid_by_archived_source"]=={
        "control":8,"magnetic_disruption":9,"olfactory_deprivation":6}
    assert x["Argos_assigned_by_original_publication"]["olfactory_deprivation"]==5
    assert x["GPS_capture_fraction_among_GPS_equipped"]["olfactory_deprivation"]==pytest.approx(6/9)

def test_exact_diagnostics_show_design_vs_capture_distinction():
    x=run(original())
    assert x["GPS_equipped_only_three_arm_exact"]["two_sided_conditional_probability"]==pytest.approx(.28,abs=1e-13)
    assert x["olfactory_vs_other_GPS_equipped_Fisher_two_sided"]==pytest.approx(0.09333333333333332,abs=1e-13)
    assert x["all_treated_GPS_yes_no_three_arm_exact_but_design_confounding"]["two_sided_conditional_probability"]==pytest.approx(.004297937879695388,abs=1e-13)

def test_missing_binary_outcome_identification_not_effect():
    x=run(original())
    assert x["olfactory_minus_control_GPS_outcome_difference_bound_width"]==pytest.approx(8/14+1/9)
    assert not x["experimental_effect_on_navigation_identified"]
    assert not x["assignment_randomization_verified_here"]
    assert not x["original_animal_identifiers_or_locations_exported"]

def test_source_divergence_fails_closed():
    x=original()
    x["subject_capture_by_sensor_and_group"]["olfactory_deprivation"]["GPS_subjects"]=7
    with pytest.raises(ValueError,match="capture changed"):
        run(x)
