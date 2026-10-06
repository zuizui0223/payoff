# PAYOFF-B V4.5 main-figure receipt — 2026-10-06

Status: **MAIN FIGURES RENDERED, TESTED AND VISUALLY REVIEWED**

## Workflow

GitHub Actions run:
- **37407791647**

Artifact:
- **11387890969**

Artifact digest:
- **sha256:499850ff5d865c50bb3e916f5ce17d90b69652ba17b012a16d1e201f67a038f2**

Renderer commit:
- **b76ce35d3a74df7463552bda21902d9bdf65a84b**

Frozen figure-data manifest:
- `data/payoff_b_v45_figure_data_20261006.json`

Renderer:
- `scripts/render_payoff_b_v45_main_figures.py`

Tests:
- `tests/test_payoff_b_v45_main_figures.py`

## Generated figures

1. `PAYOFF_B_V45_FIG1_FRAMEWORK.svg`
2. `PAYOFF_B_V45_FIG2_BIRDS.svg`
3. `PAYOFF_B_V45_FIG3_MULE_DEER.svg`

The CI verifies:
- deterministic figure-data SHA;
- deterministic SVG SHA across repeated renders;
- valid SVG parsing;
- presence of frozen headline values;
- absence of internal project/version labels in rendered figure text.

## Visual review

SVGs were rendered to PNG at 1400 px width for manual inspection.

### Figure 1

Status: **PASS**

- four-panel hierarchy is legible;
- forecastability/access/actionability/correction sequence is visually clear;
- no clipping detected;
- conceptual status is obvious;
- no empirical overclaim added by the graphic.

### Figure 2

Status: **PASS AFTER LAYOUT REVISION**

Initial visual review found:
- top-panel heading collisions;
- truncation of the panel-C heading;
- overlap between early/late arrival numeric labels.

The renderer was revised before this receipt.

Final review:
- panel headings no longer collide;
- observability percentages retain one decimal place and match frozen values;
- arrival labels are separated vertically;
- preregistered versus posthoc evidence is visibly labelled;
- the observability panel does not imply that the reconstructed predictor was an observed cue.

### Figure 3

Status: **PASS AFTER LAYOUT REVISION**

Initial visual review found top-panel heading crowding.

Final review:
- headings are compact and separated;
- phase-variance, phase-error and actuator panels are legible;
- the serial correction schematic is clear;
- the caption-level warning that the mule-deer mechanism does not identify the bird mechanism is preserved in the graphic.

## Claim boundary

Figure 2 represents:
- analyst/environmental forecastability;
- source-event observability boundary;
- population timing.

It does **not** represent:
- bird cue perception;
- organismal information value;
- bird actionability.

Figure 3 is an independent natural correction anchor and does not identify the bird mechanism.

## Decision

Main figures are frozen for the current American Naturalist V4.5 route unless:
- a journal-format conversion introduces clipping;
- a factual value changes because a validated source receipt was wrong;
- a reviewer-critical validity issue is found.

Cosmetic redesign alone is not a reason to reopen the scientific figure set.
