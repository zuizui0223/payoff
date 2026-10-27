"""Frozen source early-vs-late shearwater calibration and sharp missingness."""
import json
from pathlib import Path
def test_stagewise_shearwater_source_receipt():
    j=json.loads(Path("data/payoff_b_shearwater_stagewise_progress_result_20261028.json").read_text("utf-8"))
    assert j["original_output"]["status"]=="STAGEWISE_SOURCE_DESCRIPTIVE_AND_BOUNDS_COMPLETE"
    assert j["outcome_interpretation"]["eligible_subjects"]==22
    assert j["outcome_interpretation"]["improvement_counts"]=={
        "control":3,"magnetic_disruption":1,"olfactory_deprivation":2}
    lo,hi=j["outcome_interpretation"]["olfactory_minus_control_binary_outcome_full_arm_sharp_bound"]
    assert lo<0<hi
    assert j["outcome_interpretation"]["coastal_information_rescue_tested"] is False
    assert j["outcome_interpretation"]["experimental_causal_effect_identified"] is False
