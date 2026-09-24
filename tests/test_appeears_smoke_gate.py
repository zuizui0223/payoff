from src.appeears_smoke_gate import evaluate_appeears_smoke_gate


def good_receipt():
    return {
        "status": "appeears_v061_irg_input_ready",
        "conversion": {
            "matched_rows": 100,
            "output_rows": 90,
            "unknown_snow_rows": 5,
            "invalid_reflectance_rows": 5,
        },
        "pixel_years": 10,
        "quality_good_rows": 70,
        "snow_free_rows": 60,
    }


def test_live_smoke_gate_passes_structurally_usable_receipt():
    gate = evaluate_appeears_smoke_gate(good_receipt())
    assert gate.passed
    assert gate.reasons == ()
    assert gate.output_rows == 90


def test_live_smoke_gate_rejects_no_quality_good_rows():
    receipt = good_receipt()
    receipt["quality_good_rows"] = 0
    gate = evaluate_appeears_smoke_gate(receipt)
    assert not gate.passed
    assert "NO_QUALITY_GOOD_ROWS" in gate.reasons


def test_live_smoke_gate_rejects_no_snow_free_rows():
    receipt = good_receipt()
    receipt["snow_free_rows"] = 0
    gate = evaluate_appeears_smoke_gate(receipt)
    assert not gate.passed
    assert "NO_SNOW_FREE_ROWS" in gate.reasons


def test_live_smoke_gate_rejects_unready_receipt():
    gate = evaluate_appeears_smoke_gate(
        {"status": "some_other_status"}
    )
    assert not gate.passed
    assert gate.reasons == ("IRG_INPUT_RECEIPT_NOT_READY",)
