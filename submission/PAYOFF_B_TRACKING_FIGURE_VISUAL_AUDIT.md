# PAYOFF-B tracking theory — figure visual audit

Audited: **2026-09-24**

Branch:

`feature/payoff-b-migration-phenology-20260919`

Audited HEAD:

`3cb931230b6ddc294d7ef6615f44de89a3bda7ce`

Green workflow run:

`35987790697`

Artifact:

`payoff-b-tracking-theory-figures`

Artifact ID:

`10803495155`

Artifact SHA256:

`0d61c3f691d3d37cdffcb3703ec0fd6dd43efdf1d3442cda1cd8ba379a01914e`

## Audit method

The CI artifact was downloaded from the successful workflow run, the six SVG
files were rasterized at their native 1200 x 720 canvas, and each figure was
inspected for:

- text clipping;
- panel overlap;
- labels extending outside boxes or axes;
- titles colliding with neighboring panels;
- unreadable wrapping;
- annotations colliding with axes;
- scientific values changing during layout repair.

This is a visual-layout audit only. Numeric content remains governed by the
frozen figure-data and claim contracts.

## Result

| Figure | File | Visual status | Notes |
|---|---|---|---|
| 1 | `PAYOFF_B_TRACKING_FIG1_CONCEPT.svg` | PASS | all seven conceptual boxes fit; wrapped titles/subtitles remain inside boxes |
| 2 | `PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg` | PASS | A/B panels remain distinct; lower annotations fit inside canvas |
| 3 | `PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg` | PASS | negative and positive bars, zero line and labels are all legible |
| 4 | `PAYOFF_B_TRACKING_FIG4_SYNCHRONIZATION.svg` | PASS | strong-forcing endpoint descriptions wrap inside all three boxes |
| 5 | `PAYOFF_B_TRACKING_FIG5_DEMOGRAPHY_DRIFT.svg` | PASS | both panels and explanatory text fit without collision |
| 6 | `PAYOFF_B_TRACKING_FIG6_COMPLEMENTARITY.svg` | PASS | theorem, persistence contrast and fixed-gain boxes remain fully visible |

## Scientific-content check

The visual repairs do not change the frozen scientific values. In particular,
the audited figures still display:

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
formatting, or accessibility improvements. Any change to a numeric value,
scientific interpretation, panel membership, or evidence source requires a new
figure-data/claim-contract review rather than being treated as layout repair.
