from src.goose_archive_eligibility import audit_reference_eligibility


def test_svalbard_explicit_not_used_flag_recovers_21_from_22():
    rows = [
        {
            "animal-id": f"id{i}",
            "deployment-id": f"id{i}-07",
            "deploy-on-date": "2007-02-01 07:00:00.000",
        }
        for i in range(21)
    ]
    rows.append(
        {
            "animal-id": "70568",
            "deployment-id": "70568-not used",
            "deploy-on-date": "2007-02-01 07:00:00.000",
        }
    )
    out = audit_reference_eligibility(rows)
    assert out.archived_rows == 22
    assert out.eligible_rows == 21
    assert out.excluded_rows == 1
    assert out.excluded_animal_ids == ("70568",)


def test_barents_explicit_not_used_flags_recover_12_from_15():
    rows = [
        {
            "animal-id": f"used{i}",
            "deployment-id": f"used{i}-09",
            "deploy-on-date": "2009-02-01 08:00:00.000",
        }
        for i in range(12)
    ] + [
        {
            "animal-id": "78040",
            "deployment-id": "78040-not used",
            "deploy-on-date": "2008-02-01 08:00:00.000",
        },
        {
            "animal-id": "78042a",
            "deployment-id": "78042a-not used",
            "deploy-on-date": "2008-02-01 08:00:00.000",
        },
        {
            "animal-id": "78042b",
            "deployment-id": "78042b-not used",
            "deploy-on-date": "2009-02-01 08:00:00.000",
        },
    ]
    out = audit_reference_eligibility(rows)
    assert out.archived_rows == 15
    assert out.eligible_rows == 12
    assert out.excluded_animal_ids == ("78040", "78042a", "78042b")


def test_eligibility_does_not_drop_tracks_for_other_comments():
    rows = [
        {
            "animal-id": "A",
            "deployment-id": "A-09",
            "deploy-on-date": "2009-02-01 08:00:00.000",
            "deployment-comments": "tag failed after summer",
        },
        {
            "animal-id": "B",
            "deployment-id": "B-09",
            "deploy-on-date": "2009-02-01 08:00:00.000",
            "animal-comments": "exclude? free text is not a declared rule",
        },
    ]
    out = audit_reference_eligibility(rows)
    assert out.eligible_rows == 2
    assert out.excluded_rows == 0



def test_deployment_year_is_explicitly_frozen_for_each_used_animal():
    rows = [
        {
            "animal-id": "A",
            "deployment-id": "A-08",
            "deploy-on-date": "2008-03-10 12:00:00.000",
        },
        {
            "animal-id": "B",
            "deployment-id": "B-09",
            "deploy-on-date": "2009-02-01 08:00:00.000",
        },
    ]
    out = audit_reference_eligibility(rows)
    assert out.eligible_deployment_years == (("A", 2008), ("B", 2009))
