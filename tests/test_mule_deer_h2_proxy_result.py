import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
H2 = ROOT / "data" / "payoff_b_mule_deer_h2_proxy_result_20261003.json"
CLASS = ROOT / "data" / "payoff_b_two_clock_classification_20261003.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_mule_deer_h2_proxy_is_fail_closed():
    r = load(H2)
    assert r["decision_rule"]["outcome"] == "NO_PROXY_SUPPORT"
    assert r["decision_rule"]["rate_pass"] is False
    assert r["decision_rule"]["stopover_pass"] is False


def test_h2_proxy_intervals_cross_zero():
    r = load(H2)
    rate = r["movement_rate"]["ci95"]
    stop = r["stopover"]["ci95"]
    assert rate[0] < 0 < rate[1]
    assert stop[0] < 0 < stop[1]


def test_mule_deer_remains_h1_not_h2():
    p = load(CLASS)
    deer = next(x for x in p["systems"] if x["system"] == "Ortega mule deer")
    assert deer["hybrid"] == "H1_CANDIDATE"
    assert deer["h2_proxy"] == "NO_PROXY_SUPPORT"
    assert "not supported" in deer["boundary"].lower()


def test_no_natural_system_promoted_to_h2():
    p = load(CLASS)
    assert all(x["hybrid"] != "H2" for x in p["systems"])
    assert "did not support H2" in p["global_boundary"]
