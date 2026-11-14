import pytest

from src.japan_phenology_biomass_bridge import (
    ResourceSourceNotAdmitted, biomass_source_gate, integrate_resource_biomass,
)


def example():
    return [
        {"site_id": "TEST", "resource_guild": "caterpillar", "date": d,
         "biomass_g_m2": b, "sample_area_m2": 1,
         "source_id": "SYNTHETIC_TEST_ONLY", "sampling_effort_verified": True,
         "mass_basis": "dry", "independent_from_bird_outcome": True}
        for d, b in [("2020-04-01", 1), ("2020-04-06", 3), ("2020-04-11", 1)]
    ]


def test_trapezoid_exact_for_synthetic_resource():
    result = integrate_resource_biomass(example(), window_start="2020-04-01", window_end="2020-04-11")
    assert result["resource_exposure_g_day_m2"] == pytest.approx(20)
    assert result["mean_resource_biomass_g_m2"] == pytest.approx(2)
    assert result["fitness_effect_estimated"] is False


@pytest.mark.parametrize("change", [
    lambda a: a[0].update(independent_from_bird_outcome=False),
    lambda a: a[0].update(sampling_effort_verified=False),
    lambda a: a[0].update(biomass_g_m2=-1),
    lambda a: a[0].update(mass_basis="fresh"),
    lambda a: a[0].update(resource_guild="vegetation"),
    lambda a: a[0].update(sample_area_m2=0),
    lambda a: a[0].update(source_id=""),
    lambda a: a[0].update(date="2020-04-06"),
])
def test_bad_biomass_source_fails(change):
    x = example()
    change(x)
    with pytest.raises(ResourceSourceNotAdmitted):
        integrate_resource_biomass(x, window_start="2020-04-01", window_end="2020-04-11")


def test_no_extrapolation_or_long_gaps():
    with pytest.raises(ResourceSourceNotAdmitted):
        integrate_resource_biomass(example(), window_start="2020-03-30", window_end="2020-04-11")
    x = example()
    x[1]["date"] = "2020-04-20"
    x[2]["date"] = "2020-04-30"
    with pytest.raises(ResourceSourceNotAdmitted):
        integrate_resource_biomass(x, window_start="2020-04-01", window_end="2020-04-30")


def test_proxy_not_promoted_to_biomass():
    assert biomass_source_gate({"quantity_kind": "NDVI"}) == "VEGETATION_GREENNESS_PROXY_NOT_BIOMASS"
    assert biomass_source_gate({"quantity_kind": "count"}) == "NON_MASS_OBSERVATION"
    assert biomass_source_gate({"quantity_kind": "peak_date"}) == "NON_MASS_OBSERVATION"
    assert biomass_source_gate({"quantity_kind": "mass_per_area", "units": "g/m2"}) == "MEASURED_BIOMASS_SOURCE_NOT_YET_VERIFIED"
