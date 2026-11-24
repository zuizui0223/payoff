"""No event bytes or identifiers in first-8KiB metadata-only page probe."""
import pytest

from scripts import payoff_b_stork_archival_landing_html_probe_20261124 as s


def test_classify_landing_anchor_extensions_without_emitting_links():
    html=(b'<html><a href="/bitstream/handle/10255/move.1627/package.csv">tracking</a>'
          b'<a href="/download/table.zip">download</a>'
          b'<a href="/terms">license</a></html>')
    r=s.summarize_html(html,"text/html; charset=utf-8")
    assert r["linked_file_extension_counts"]=={".csv":1,".zip":1}
    assert r["static_script_filenames"]==[]
    assert r["custom_markup_tags"]==[]
    assert r["contains_literal_bitstream_href"] is True
    assert r["contains_literal_file_download_href"] is True
    assert r["html_has_word_license"] is True
    assert "/bitstream/handle/" not in str(r)
    assert r["actual_linked_files_accessed"] is False


def test_reject_binary_even_if_appears_like_html():
    with pytest.raises(ValueError,match="HTML"):
        s.summarize_html(b"PK\x03\x04...","application/zip")


def test_reject_unregistered_direct_event_links():
    fixed="https://datarepository.movebank.org/handle/10255/move.1627"
    with pytest.raises(ValueError,match="unregistered"):
        s.read_landing("https://datarepository.movebank.org/bitstream/data.csv",{fixed})
    assert s.HTML_CAP==8192


def test_zero_link_html_is_unknown_not_evidence_of_no_files():
    r=s.summarize_html(b"<html><script>bootstrap()</script></html>","text/html")
    assert r["parsed_anchor_count"]==0
    assert r["source_html_sample_only"] is True
    assert r["actual_linked_files_accessed"] is False
