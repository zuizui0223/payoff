import csv
import io
import zipfile

import pytest

from scripts.payoff_b_japan_phenology_source_census import classify, summarize_zip, parse_index_labels


def fixture_zip():
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("bird.csv", "地点,年,日付\n東京,2000,20000405\n".encode("cp932"))
        z.writestr("frog.csv", "地点,年,日付\n京都,2001,20010312\n".encode("cp932"))
        z.writestr("notes.txt", "not a CSV")
    return out.getvalue()


def test_census_is_schema_only():
    x = summarize_zip(fixture_zip())
    assert x["csv_file_count"] == 2
    assert len(x["archive_sha256"]) == 64
    assert all(y["header_only_no_biological_fit"] for y in x["files"])
    assert all(y["row_count_including_headers"] == 2 for y in x["files"])
    assert x["files"][0]["first_three_rows_first_12_cells"][0] == ["地点", "年", "日付"]


@pytest.mark.parametrize("filename,expected", [
    ("にほんあまがえる初鳴.csv", "amphibian"),
    ("とのさまがえる初見.csv", "amphibian"),
    ("うぐいす初鳴.csv", "bird"),
    ("つばめ初見.csv", "bird"),
    ("あぶらぜみ初鳴.csv", "insect"),
    ("さくら開花.csv", "plant_or_unclassified"),
])
def test_filename_classification_is_explicitly_provisional(filename, expected):
    assert classify(filename) == expected


def test_reject_invalid_archive():
    with pytest.raises(zipfile.BadZipFile):
        summarize_zip(b"not-a-zip")


def test_reject_archive_over_limit():
    with pytest.raises(ValueError):
        summarize_zip(b"x" * 8_000_001)


def test_official_html_labels_recover_numeric_csv_taxa():
    html = '<a href="ruinenchi/114.csv">にほんあまがえる初鳴</a><a href="ruinenchi/201.csv">★さくら開花</a>'
    labels = parse_index_labels(html)
    assert labels["114.csv"] == "にほんあまがえる初鳴"
    assert labels["201.csv"] == "さくら開花"
    with_labels = summarize_zip(fixture_zip(), labels={"bird.csv": "うぐいす初鳴", "frog.csv": "にほんあまがえる初鳴"})
    assert with_labels["files_with_official_event_labels"] == 2
    assert with_labels["source_taxon_filename_class_counts"] == {"bird": 1, "amphibian": 1}
