import pytest

from src.japan_phenology_panel import parse_wide_jma_csv


def test_wide_jma_panel_preserves_rm_and_calendar_dates():
    payload = (
        "1,うめの開花,,,,\n"
        "番号,地点名,1953,rm,1954,rm,統計,2032\n"
        "401,稚内,405,6,0,0,その他,2024\n"
        "402,札幌,229,8,305,7,その他,2023\n"
    ).encode("cp932")
    panel, receipt = parse_wide_jma_csv(payload, source_file="001.csv", event_label="うめ開花")
    assert len(panel) == 2
    assert [x["event_date"] for x in panel] == ["1953-04-05", "1954-03-05"]
    assert [x["rm_original_code"] for x in panel] == ["6", "7"]
    assert all(x["rm_quality_interpretation"] == "UNVERIFIED" for x in panel)
    assert receipt["last_year_column"] == 1954
    assert receipt["valid_event_rm_codes"] == {"6": 1, "7": 1}


def test_leap_year_and_doy():
    payload = (
        "1,うめの開花\n番号,地点名,2000,rm,2001,rm\n"
        "401,稚内,229,6,229,6\n"
    ).encode("cp932")
    panel, receipt = parse_wide_jma_csv(payload, source_file="001.csv", event_label="うめ開花")
    assert len(panel) == 1
    assert panel[0]["day_of_year"] == 60
    assert receipt["invalid_or_missing_date_cells"]["INVALID_CALENDAR_DATE"] == 1


def test_duplicate_station_year_fails():
    payload = (
        "1,うめの開花\n番号,地点名,2000,rm\n"
        "401,稚内,405,6\n401,稚内,406,6\n"
    ).encode("cp932")
    with pytest.raises(ValueError, match="Duplicate"):
        parse_wide_jma_csv(payload, source_file="001.csv", event_label="うめ開花")


def test_unrecognized_header_fails():
    with pytest.raises(ValueError, match="Not a recognized"):
        parse_wide_jma_csv("event,year\nうめ,2000".encode("cp932"), source_file="x.csv", event_label="うめ")
