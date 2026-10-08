"""Guard against silently malformed historical V7R artifact digests.

A single missing hex digit caused the V7R source-download workflow to fail
before statistical execution. This test is intentionally source-free and
checks the immutable digest declarations in the committed workflow.
"""

from pathlib import Path
import re


WORKFLOW = Path(".github/workflows/payoff-b-v7r-direct-recourse.yml")

EXPECTED = {
    "multi.zip": "8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f",
    "sval.zip": "29558f9b8b43a7375b3922118a77b74464558f4869a7722472570a32745f2856",
    "era5_multi.zip": "c37502b116f4170760e0fbf5029fe1804999def4de3f702cdb5bf61e61b8606f",
    "era5_sval.zip": "6155a9efe854167883190db7410ce60c151721e4569d564f23bc01a555013825",
}


def test_v7r_artifact_sha256_values_are_full_length_and_match_frozen_archives():
    source = WORKFLOW.read_text(encoding="utf-8")
    found = re.findall(
        r'echo "([0-9a-f]+)  outputs/([a-z0-9_]+[.]zip)" *[|] *sha256sum -c -',
        source,
    )
    assert len(found) == len(EXPECTED), found
    by_file = {filename: digest for digest, filename in found}
    assert set(by_file) == set(EXPECTED)
    for filename, digest in by_file.items():
        assert len(digest) == 64, (filename, digest)
        assert digest == EXPECTED[filename]
