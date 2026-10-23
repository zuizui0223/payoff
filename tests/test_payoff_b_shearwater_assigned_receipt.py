"""Archived shearwater GPS-allocation result must preserve source denominator."""
import json
from pathlib import Path

def test_original_assignments_not_conflated_with_tracking_loss():
    d=json.loads(Path(
      "data/payoff_b_shearwater_assigned_device_capture_result_20261023.json"
    ).read_text(encoding="utf-8"))
    assert d["original_reference_subjects"]==32
    assert d["GPS_equipped_by_original_publication"]=={
        "control":9,"magnetic_disruption":9,"olfactory_deprivation":9}
    assert d["GPS_valid_by_archived_source"]=={
        "control":8,"magnetic_disruption":9,"olfactory_deprivation":6}
    assert d["Argos_assigned_by_original_publication"]["olfactory_deprivation"]==5
    assert abs(d["GPS_equipped_only_three_arm_exact"]["two_sided_conditional_probability"]-0.28)<1e-12
    assert abs(d["all_treated_GPS_yes_no_three_arm_exact_but_design_confounding"]["two_sided_conditional_probability"]-0.004297937879695388)<1e-12
    assert d["experimental_effect_on_navigation_identified"] is False
    assert d["original_animal_identifiers_or_locations_exported"] is False
