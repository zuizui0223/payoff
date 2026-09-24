from pathlib import Path

import pytest

from src.appeears_result_merge import (
    discover_product_csvs,
    merge_point_result_csvs,
)


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_discover_and_merge_multiple_product_csvs(tmp_path):
    write(
        tmp_path / "task1" / "A_MOD09Q1_result.csv",
        "ID,Date,value\ncell1,2020-01-01,1\n",
    )
    write(
        tmp_path / "task2" / "B_MOD09Q1_result.csv",
        "ID,Date,value\ncell2,2020-01-01,2\n",
    )
    files = discover_product_csvs(tmp_path, "MOD09Q1")
    assert len(files) == 2

    output = tmp_path / "merged.csv"
    result = merge_point_result_csvs(
        files,
        product="MOD09Q1.061",
        output_path=output,
    )

    assert result.rows == 2
    assert output.read_text().splitlines() == [
        "ID,Date,value",
        "cell1,2020-01-01,1",
        "cell2,2020-01-01,2",
    ]


def test_merge_rejects_header_drift(tmp_path):
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    write(a, "ID,Date,value\ncell1,2020-01-01,1\n")
    write(b, "ID,Date,other\ncell2,2020-01-01,2\n")

    with pytest.raises(ValueError, match="header drift"):
        merge_point_result_csvs(
            (a, b),
            product="MOD09Q1.061",
            output_path=tmp_path / "merged.csv",
        )


def test_merge_rejects_duplicate_rows_across_tasks(tmp_path):
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    row = "cell1,2020-01-01,1"
    write(a, "ID,Date,value\n" + row + "\n")
    write(b, "ID,Date,value\n" + row + "\n")

    with pytest.raises(ValueError, match="duplicate"):
        merge_point_result_csvs(
            (a, b),
            product="MOD09Q1.061",
            output_path=tmp_path / "merged.csv",
        )


def test_discovery_rejects_missing_product(tmp_path):
    with pytest.raises(ValueError, match="no AppEEARS CSV"):
        discover_product_csvs(tmp_path, "MOD10A2")
