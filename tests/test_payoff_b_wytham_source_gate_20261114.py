import copy
import json

import pytest

from scripts.audit_payoff_b_wytham_source_gate_20261114 import SOURCE, audit


def source():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def test_public_metadata_admission_is_no_go():
    out = audit(source())
    assert out["public_source_records_screened"] == 5
    assert out["public_dois"] == 4
    assert out["status"] == "NO_GO_DIRECT_RESOURCE_BIOMASS_FIT"
    assert not out["direct_prey_biomass_time_series_admitted"]
    assert not out["migrant_information_recourse_identified"]


@pytest.mark.parametrize("edit", [
    lambda s: s.update(schema="other"),
    lambda s: s.update(no_resource_biomass_source_admitted=False),
    lambda s: s.update(no_new_biomass_fitness_effect_fitted=False),
    lambda s: s.update(no_migrant_mechanism_inference=False),
    lambda s: s["sources"][0].update(raw_schema_verified=True),
    lambda s: s["sources"][1].update(raw_file_checksum_verified=True),
    lambda s: s["sources"][2].update(resource_biomass_magnitude_measured=True),
    lambda s: s["sources"][0].update(source_years=[2023]),
    lambda s: s["sources"].append(copy.deepcopy(s["sources"][0])),
    lambda s: s["predeclared_primary_model_requires"].pop(),
])
def test_source_promotion_requires_new_verified_evidence(edit):
    payload = copy.deepcopy(source())
    edit(payload)
    with pytest.raises(ValueError):
        audit(payload)
