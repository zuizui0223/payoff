import pytest

from scripts.run_appeears_manifest import select_tasks


def manifest():
    return {
        "tasks": [
            {
                "year": 2020,
                "part": 1,
                "cell_count": 10,
                "task": {
                    "task_name": "task_2020_p001",
                },
            },
            {
                "year": 2021,
                "part": 1,
                "cell_count": 20,
                "task": {
                    "task_name": "task_2021_p001",
                },
            },
        ]
    }


def test_select_specific_task_indices():
    rows = select_tasks(
        manifest(),
        task_indices=(1,),
        submit_all=False,
    )

    assert len(rows) == 1
    assert rows[0]["year"] == 2021


def test_submit_all_selects_every_task():
    rows = select_tasks(
        manifest(),
        task_indices=(),
        submit_all=True,
    )
    assert len(rows) == 2


def test_submit_all_and_indices_are_mutually_exclusive():
    with pytest.raises(SystemExit):
        select_tasks(
            manifest(),
            task_indices=(0,),
            submit_all=True,
        )


def test_selection_requires_explicit_task_choice():
    with pytest.raises(SystemExit, match="choose at least one"):
        select_tasks(
            manifest(),
            task_indices=(),
            submit_all=False,
        )


def test_out_of_range_task_index_is_rejected():
    with pytest.raises(SystemExit, match="outside"):
        select_tasks(
            manifest(),
            task_indices=(2,),
            submit_all=False,
        )


def test_manifest_without_tasks_is_rejected():
    with pytest.raises(SystemExit, match="no tasks"):
        select_tasks(
            {"tasks": []},
            task_indices=(),
            submit_all=True,
        )
