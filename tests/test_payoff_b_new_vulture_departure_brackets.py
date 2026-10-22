from datetime import date,timedelta
from collections import Counter
import pytest
from scripts.qc_payoff_b_new_vulture_departure_brackets import (
    choose_first_per_animal_year,report_brackets,
    EXACT_PRIOR_DEDUP_CANDIDATES,EXACT_ANIMAL_YEARS_WITH_CASE,
)

def synthetic():
    day=date(2016,3,1)
    rows=[(day+timedelta(days=i),20.,10.) for i in range(14)]
    rows += [(day+timedelta(days=14),20.5,10.5),
             (day+timedelta(days=15),21.6,11.2)]
    return rows

def test_first_original_case_per_year_uses_only_source_geometry():
    selected,count=choose_first_per_animal_year({
        ("Neophron percnopterus","secret",2016):synthetic()})
    assert count==1
    assert len(selected)==1
    assert list(selected.values())[0][2:]==(None,None)

def test_bracket_counts_never_forge_gps_departure_or_relax_fixed_n():
    s=report_brackets(Counter({"BRACKET_WITHIN_24H":13,
                               "NO_OUTBOUND_NEXT_DAY_FIX":5}),
                      [1.5,2.0,2.5,3,4,5,6,7,8,9,10,11,12],18,30)
    assert s["fixed_future_hourly_meteorology_source_gate"]["passed"]
    assert not s["true_behavioral_commitment_instant_identified"]
    assert s["brackets_narrower_than_h"]["3"]==4
    with pytest.raises(ValueError,match="original"):
        report_brackets(Counter({"BRACKET_WITHIN_24H":13,
                                 "NO_OUTBOUND_NEXT_DAY_FIX":5}),
                        [1]*13,17,30)
    assert EXACT_PRIOR_DEDUP_CANDIDATES==30
    assert EXACT_ANIMAL_YEARS_WITH_CASE==18
