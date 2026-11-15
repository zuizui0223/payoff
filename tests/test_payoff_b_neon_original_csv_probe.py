from scripts.payoff_b_neon_original_csv_probe import select_csv,inspect_csv

def test_source_table_selection_and_actual_csv_schema():
    files=[{"name":"NEON.D01.ABBY.DP1.10055.001.statusIntensity.2020-05.basic.csv","url":"https://example.org/a","size":200},
           {"name":"NEON.D01.ABBY.DP1.10055.001.variables.csv","url":"https://example.org/b","size":200}]
    assert len(select_csv(files,"phenology"))==1
    result=inspect_csv(b"siteID,individualID,date\nABBY,A,2020-05-01\n")
    assert result["rows"]==1
    assert result["header"]==["siteID","individualID","date"]
