# PAYOFF-B tracking theory — figure visual audit

Audited: **2026-09-25**

Scope: **post-reframing Oikos figure set**

Audited main HEAD:

`a89deb56ae096bf2d3840b16cfed2a7cd7f1dc98`

Green workflow run:

`36089011639`

Artifact:

`payoff-b-tracking-theory-figures`

Artifact ID:

`10845126875`

Artifact SHA256:

`5249d69a52b0e95f958432d121910bc1b45a90f6074ac7f5961492b3f2453513`

This supersedes the layout receipt from 2026-09-24 for the current
mismatch-buffering framing. The earlier audit remains in repository history but
does not govern the post-reframing Figure 1.

## Audit method

The successful main artifact was downloaded and all six SVG files were
rasterized at their native **1200 x 720** canvas. The complete six-figure set
was visually inspected for:

- text clipping;
- panel overlap;
- labels extending outside boxes or axes;
- titles colliding with neighboring panels;
- unreadable wrapping;
- annotations colliding with axes;
- accidental numeric changes during the framing revision.

This is a visual-layout audit only. Numeric content remains governed by the
frozen 2026-09-20 figure-data and scientific claim contracts.

## Result

| Figure | File | Visual status | Notes |
|---|---|---|---|
| 1 | `PAYOFF_B_TRACKING_FIG1_CONCEPT.svg` | PASS | new “buffered mismatch to tracking breakdown” headline and all seven conceptual boxes fit without clipping |
| 2 | `PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg` | PASS | A/B panels remain distinct; annotations remain inside the canvas |
| 3 | `PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg` | PASS | negative/positive bars, zero line and labels remain legible |
| 4 | `PAYOFF_B_TRACKING_FIG4_SYNCHRONIZATION.svg` | PASS | endpoint descriptions fit inside all six boxes |
| 5 | `PAYOFF_B_TRACKING_FIG5_DEMOGRAPHY_DRIFT.svg` | PASS | both panels and explanatory text fit without collision |
| 6 | `PAYOFF_B_TRACKING_FIG6_COMPLEMENTARITY.svg` | PASS | theorem, persistence contrast and fixed-gain boxes remain fully visible |

## Scientific-content check

The reframing changed **Figure 1 wording and hierarchy**, not the frozen
simulation evidence. Figures 2–6 retain the same quantitative results.

The current figure set still displays:

- Figure 2: finite temporal bypass and migration re-entry;
- Figure 3: coordinated gain approximately +1.095 versus unilateral gains
  approximately -5.946;
- Figure 4: 9/9 persistence at moderate forcing and 0/9 interacting persistence
  in the strong-forcing lock;
- Figure 5: the failed >=0.10 demographic replication and finite-N escape
  contrast;
- Figure 6: 0/7 persistence for `h=0` versus 7/7 for timing-enabled slices.

## Freeze rule

Future figure changes before submission are limited to typography, journal
formatting, accessibility, or correction of a documented layout defect. Any
change to a numeric value, evidence source, or scientific interpretation
requires a new figure-data/claim-contract review rather than being treated as
layout repair.
