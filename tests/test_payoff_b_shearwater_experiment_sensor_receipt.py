"""Published-source telemetry QC receipt, no new behavioral-effect promotion."""
import json
from pathlib import Path

def test_shearwater_experiment_original_source_receipt():
    p=Path("data/payoff_b_shearwater_experiment_sensor_coverage_20261023.json")
    v=json.loads(p.read_text(encoding="utf-8"))
    assert v["public_reference_groups"]=={"control":9,"magnetic_disruption":9,"olfactory_deprivation":14}
    assert v["GPS_continuous_24h_by_arm"]=={"control":8,"magnetic_disruption":8,"olfactory_deprivation":6}
    assert v["subject_capture_by_sensor_and_group"]["olfactory_deprivation"]["Argos_subjects"]==5
    assert v["subject_capture_by_sensor_and_group"]["olfactory_deprivation"]["GPS_subjects"]==6
    assert v["GPS_source_gate_passed"] is True
    assert v["measured_actual_perceived_cue_or_stagewise_recourselike_action"] is False
    assert v["original_experiment_results_reanalysed_as_new_study"] is False
