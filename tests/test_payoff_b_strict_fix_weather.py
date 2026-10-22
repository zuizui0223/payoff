"""Regression guards for strict source QC and no cue claim."""
from scripts.run_payoff_b_strict_fix_weather import (
    SOURCE_LIST,ORIGINAL_CLEAN_COUNT,BOOT_DRAWS,COMPLETE_THRESHOLD,
    CASE,STAY
)
def test_fixed_prior_source_population():
    assert set(SOURCE_LIST)=={"stork","white_fronted_goose",
                             "curlew","egyptian_vulture"}
    assert ORIGINAL_CLEAN_COUNT["stork"]==(1110,85,716)
    assert ORIGINAL_CLEAN_COUNT["egyptian_vulture"]==(1257,13,1029)
    assert CASE=="NORTHWARD_CANDIDATE"
    assert STAY=="STAYED_TWO_DAYS"
    assert BOOT_DRAWS==3000
    assert COMPLETE_THRESHOLD==.95
