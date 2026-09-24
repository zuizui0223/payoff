# Oikos handoff — PAYOFF-B tracking theory v1

Prepared: **2026-09-24**

Target journal: **Oikos**

Scientific package status: frozen. This handoff changes framing and submission
packaging only.

## Why Oikos is the first shot

Oikos explicitly publishes innovative theoretical ecology and emphasizes
ecological mechanisms, processes and patterns that can shape broader ecological
thinking.

Official journal page:

https://onlinelibrary.wiley.com/journal/16000706

The manuscript's strongest transferable mechanism is:

```text
multiple adaptive axes
do not imply
evolutionary access to their best combination
```

The climate-tracking model is the vehicle for that mechanism.

## Submission-facing one-sentence contribution

> Interacting populations can possess enough combined spatial and temporal
> adaptive capacity to persist, yet fail because the jointly viable tracking
> architecture is inaccessible through unilateral improving changes.

This sentence is a submission framing, not an additional scientific claim.

## Abstract emphasis for Oikos

Retain the frozen quantitative content, but order the logic as:

1. adaptive capacity and adaptive accessibility are different;
2. local movement/timing substitution supplies the null;
3. finite timing creates temporal bypass and spatial re-entry;
4. interaction matching creates the direct one-step coordination gate;
5. demographic visibility and finite-N crossing are separate downstream
   consequences.

Avoid opening with a catalogue of climate-response modes. The paper should read
as a general mechanism paper that happens to use moving environments as the
ecological setting.

## Introduction emphasis

First paragraph:

- multiple response axes can close the same environmental mismatch;
- this says nothing about whether interacting populations can evolve from one
  allocation to another.

Core question:

> When partners must remain matched, can a jointly valuable reallocation
> between spatial and temporal tracking be reached by unilateral selection?

Keep existing prior-art boundary:

- combined range + phenology response is already known;
- moving-habitat models are already known;
- dispersal/timing evolution is already known;
- climate-driven mismatch is already known.

Do not convert those established ideas into novelty claims.

## Main figures for the editorial read

If editors inspect only three figures, the conceptual sequence should still be
clear from:

- Figure 1 — capacity versus accessibility hierarchy;
- Figure 3 — direct one-step coordination gate;
- Figure 4 — synchronization changes ecological sign.

Figures 2, 5 and 6 provide the spatial, demographic and analytic depth.

## Discussion emphasis

Use this hierarchy:

```text
capacity
-> architecture
-> coordinated value
-> unilateral accessibility
-> persistence
```

Then add:

```text
barrier crossing
!=
long-run payoff improvement
```

The broad ecological message is not that phenology or movement is superior. It
is that substitutable ecological functions can become non-substitutable once
their evolutionary path is constrained by partner matching and landscape
mechanics.

## Cover-letter pitch

Use:

`submission/PAYOFF_B_TRACKING_COVER_LETTER_TEMPLATE.md`

For Oikos, the first paragraph after the manuscript title should emphasize the
general ecological mechanism, not the climate-change application.

Suggested editorial hook:

> The paper asks why interacting populations can fail to use an adaptive
> solution that already exists one mutation step away.

## Data/code packaging

Before actual submission:

- archive the scientific-freeze code/results to a persistent repository such as
  Zenodo or another journal-acceptable archive;
- replace the temporary repository statement in the title-page template with
  the archived DOI;
- preserve the five frozen 2026-09-20 result families and claim contracts in
  that archive.

Recent Oikos papers routinely include explicit data-availability statements and
repository records; the tracking paper should do the same for code and
synthetic outputs.

## Files to submit or derive

Core:

- `manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`
- `submission/PAYOFF_B_TRACKING_REFERENCES.bib`
- six main SVG figures
- `submission/PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md`

Supplement:

- material organized by
  `submission/PAYOFF_B_TRACKING_SUPPLEMENT_MAP.md`

Administrative:

- `submission/PAYOFF_B_TRACKING_TITLE_PAGE_TEMPLATE.md`
- `submission/PAYOFF_B_TRACKING_COVER_LETTER_TEMPLATE.md`

Internal, not normally uploaded as manuscript files:

- claim freeze;
- prior-art audit;
- parameter map;
- Results-to-Figure crosswalk;
- figure visual audit;
- package index.

## Fallback rule

If Oikos declines on breadth/fit rather than on a scientific flaw, do **not**
retune the simulations.

Move the same scientific freeze to **Theoretical Ecology**, where the
combination of exact local theory, computational landscape models and
evolutionary accessibility is directly within scope.

A rejection on journal breadth is not evidence that more parameter sweeps are
needed.
