from src.payoff_b_monisen_source_inventory import source_inventory, candidate_hypotheses

def test_official_source_inventory_never_invents_download_or_join():
    receipt=source_inventory()
    assert receipt["status"]=="OFFICIAL_WEB_CATALOG_VERIFIED_RAW_RECORDS_NOT_ACQUIRED"
    assert receipt["actual_shared_site_year_count"] is None
    assert receipt["original_file_sha256"] is None
    assert receipt["biomass_overlap_confirmed"] is False
    assert len(receipt["source_types"])>=8
    assert all(s["raw_source_download_verified"] is False for s in receipt["source_types"])

def test_hypothesis_admission_explicitly_closed():
    rows=candidate_hypotheses()
    assert {r["hypothesis"] for r in rows}=={"H1","H2","H3","H4"}
    assert all(r["admission"].startswith("NOT_ADMITTED") for r in rows)
