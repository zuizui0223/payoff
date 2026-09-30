#!/usr/bin/env python3
"""Build the blinded GEB-facing PREOUTCOME source from canonical PAYOFF-B V2."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"

RUNNING_TITLE = "Information deadlines and coordination"

STRUCTURED_ABSTRACT = """### Aim

To determine when improving environmental information can desynchronize
interacting seasonal organisms and why restored information may fail to restore
coordination.

### Location

General theory, with empirical modules from eastern North America and European
bird interaction systems.

### Time period

Dataset-specific; principal reconstructed phenology records span approximately
1980–2020.

### Major taxa studied

Migratory birds, with plants and insect pollinators as an independent benchmark.

### Methods

We combine exact Bayesian decision theory and finite coordination games with
preregistered comparative analyses, source-table reconstructions, published
experiments and interaction-level phenology studies.

### Results

Information becomes actionable only above an exact reliability threshold, but
waiting is governed by an effective deadline cost: direct waiting loss plus the
minimum cost of downstream compensation and residual delay. Raw waiting time
therefore does not generally rank effective deadlines and can even reverse the
predicted order of information-use thresholds. Heterogeneous effective
deadlines create a finite asynchronous-uptake window, so better information
increases mismatch during part of the uptake transition. Perfect information
can also support obsolete uninformed and better informed strict equilibria;
after cue degradation collapses coordinated information use, restoring perfect
cue accuracy does not recover the informed state. Natural evidence supports
successive links rather than the full hysteresis process: stronger predictive
connectivity is associated with smaller mismatch across 37 bird species, a
944-effect reconstruction shows weaker temperature responses in long- than
short-distance migrants, and differential climate sensitivity across 10
European nest-box schemes widened resident–migrant laying-date intervals by
0.94 d/decade.

### Main conclusions

Seasonal mismatch cannot be interpreted from cue quality or raw waiting time
alone. Effective deadline costs determine when information is worth using,
while strategic coordination can determine whether use recovers at all.
Theory predicts that environmental information can recover before ecological
coordination does.
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
