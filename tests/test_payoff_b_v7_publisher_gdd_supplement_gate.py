"""Official-publisher supporting-info link security and fallback tests."""
from scripts.payoff_b_v7_publisher_gdd_supplement_gate import (
    FILE_NAME,DocumentLinks,source_href,sample_docx
)

def test_supplement_only_from_official_article_advertised_href():
    page="https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.12281"
    ok="/doi/suppl/10.1111/1365-2656.12281/other/"+FILE_NAME
    assert source_href(page,ok).startswith("https://besjournals.onlinelibrary.wiley.com/")
    assert source_href(page,"https://malicious.org/"+FILE_NAME) is None
    assert source_href(page,"file.zip") is None


def test_link_parser_accepts_real_html_only():
    p=DocumentLinks()
    p.feed('<html><a href="/other/'+FILE_NAME+'">Support</a></html>')
    assert FILE_NAME in p.links[0]


def test_non_docx_never_called_historical_table_source():
    assert sample_docx(b"This is not a docx")["verified"] is False
