#!/usr/bin/env python3
"""Build the blinded GEB-facing PREOUTCOME source from canonical PAYOFF-B V2."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"

RUNNING_TITLE = "Information deadlines and coordination"

STRUCTURED_ABSTRACT = """### Aim

To determine whether seasonal coordination can fail even when organisms have
adequate response capacity and environmental information improves, because
interacting organisms begin using that information at different decision
thresholds.

### Location

The theory is general. Empirical evidence comes from migratory-bird systems
across multiple continents.

### Time period

The broad comparative bird analysis spans 2002–2017, and the wigeon outcome
data span 2018–2020.

### Major taxa studied

Migratory birds.

### Methods

We derive exact information-deadline and coordination conditions, analyse
shared-cue interaction networks, and compare these predictions with a
preregistered predictive-connectivity analysis, a dependence-aware migration
meta-regression and a registered phase-correction test.

### Results

Cue reliability and cue use are distinct state variables. Different waiting
costs create an exact interval in which improving the same cue causes
asynchronous information use and increased mismatch. Under perfect information,
an obsolete uninformed state and a better informed state can both be strict
equilibria, so temporary information degradation can produce persistent
coordination failure after cue quality recovers. Predictive connectivity is
associated with smaller mismatch, long-distance migrants show weaker
temperature responsiveness than short-distance migrants, and the registered
wigeon controller does not support stronger post-error correction. Natural
evidence therefore supports separate parts of the mechanism rather than the
full hysteresis sequence.

### Main conclusions

Theory predicts that environmental information can recover before ecological coordination does.
Seasonal mismatch therefore depends not only on response capacity and
information quality, but also on when interacting organisms can afford to use
that information and on the strategic accessibility of coordinated change.
"""

KEYWORDS = (
    "Bayesian games; climate change; ecological hysteresis; information ecology; "
    "migration; phenological mismatch; predictive connectivity; seasonal timing"
)

DATA_CODE = """## Data and Code Availability Statement

The study reanalyses previously published datasets and uses exact and synthetic
model analyses. Source datasets remain available from their cited publications
and repository records. Analysis code, frozen derived receipts, deterministic
figure builders and non-sensitive derived outputs will be supplied to editors
and reviewers through an anonymized stable repository link. A public persistent
archive will replace the blinded reviewer link at publication.

The preregistered industrial-development phase-retention analysis remains
unopened in this working package and is not used by the main-text theory,
empirical results or figures.
"""

FIGURE_LEGENDS = """## Figure legends

**Figure 1. Useful information can arrive after the decision deadline.**
Exact value-of-waiting model paired with the pied-flycatcher/resident-tit
experimental anchor showing that heterospecific phenology was unavailable to an
earlier settlement decision but relevant to a later one.

**Figure 2. Improving information can transiently worsen coordination.**
Expected timing mismatch under one monotonically improving shared cue when two
actors face different costs of waiting. The exact uptake thresholds delimit the
asynchronous information-use interval.

**Figure 3. Interaction topology determines whether information shocks are
stored.** Strict synthetic phase-diagram results separate temporary shock
transmission from lower-payoff historical memory across complete, chain and
migrant-star networks.

**Figure 4. Pre-outcome predictive connectivity is associated with lower
mismatch.** Broad migratory-bird analysis showing the preregistered pooled
coefficient, window/definition sensitivities and dependence-aware uncertainty.

**Figure 5. Information distance, local response and correction are distinct
axes.** The Usui migration-distance reconstruction shows weaker temperature
responsiveness in long- than short-distance migrants; the independent Freimuth
plant–pollinator benchmark shows strong but unequal local temperature
responses; flycatcher and wigeon results separate decision-time cue availability
from post-error correction. Panels from the bird and plant–pollinator datasets
are not interpreted as a causal taxon contrast.

**Figure 6. Capacity is a separate barrier: temporal bypass and spatial
re-entry.** Frozen moving-landscape results showing finite timing capacity as a
buffer rather than a permanent replacement for spatial tracking.

**Figure 7. Network position determines minimum rescue intervention.** Exact
perfect-information rescue result showing that trap stability and rescue
leverage are different network properties; in the canonical chain the central
local pollinator is the only singleton rescue seed.
"""


def _strip_internal_header(text: str) -> str:
    lines = text.splitlines()
    kept = []
    for line in lines:
        if line.startswith("**Status:**"):
            continue
        if line.startswith("**Lineage:**"):
            continue
        if line.startswith("**Evidence boundary:**"):
            continue
        kept.append(line)
    return "\n".join(kept)


def _replace_abstract(text: str) -> str:
    start = text.index("## Abstract")
    key = text.index("**Keywords:**", start)
    endline = text.index("\n", key)
    replacement = (
        "## Abstract\n\n"
        + STRUCTURED_ABSTRACT.strip()
        + "\n\n**Keywords:** "
        + KEYWORDS
    )
    return text[:start] + replacement + text[endline:]


def _remove_pending_aikens_section(text: str) -> str:
    start = text.find("## 5. Registered perturbation still unopened")
    if start < 0:
        return text
    end = text.find("## 6. Conclusion", start)
    if end < 0:
        raise ValueError("could not locate Conclusion after pending Aikens section")
    return text[:start] + text[end:].replace("## 6. Conclusion", "## 5. Conclusion", 1)


def _deinternalize(text: str) -> str:
    replacements = {
        "PAYOFF-B therefore": "We therefore",
        "PAYOFF-B distinguishes": "We distinguish",
        "PAYOFF-B does not claim": "We do not claim",
        "PAYOFF-B does not infer": "We do not infer",
        "A central result of PAYOFF-B": "A central result of this study",
        "The earlier PAYOFF-B temporal-buffering result": "The earlier temporal-buffering result",
        "The current PAYOFF-B story": "The current framework",
        "PAYOFF-B's": "the framework's",
        "PAYOFF-B": "this framework",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def build_source() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    text = _strip_internal_header(text)
    text = _replace_abstract(text)
    text = _remove_pending_aikens_section(text)
    text = _deinternalize(text)

    title_end = text.index("\n")
    text = (
        text[: title_end + 1]
        + "\n**Running title:** "
        + RUNNING_TITLE
        + "\n"
        + text[title_end + 1 :]
    )

    if "## References" not in text:
        raise ValueError("canonical V2 manuscript has no References section")

    if "## Data and Code Availability Statement" not in text:
        text = text.rstrip() + "\n\n---\n\n" + DATA_CODE.strip()

    text = text.rstrip() + "\n\n---\n\n" + FIGURE_LEGENDS.strip() + "\n"
    return text


if __name__ == "__main__":
    print(build_source())
