# PAYOFF-B tracking theory — supplement map

Updated: **2026-09-24**

Canonical manuscript:

`manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`

This map defines the supplementary structure for the standalone synthetic
tracking-theory paper. It reorganizes existing frozen results only. It does not
license new simulations or new claims.

## Supplement S1 — Deterministic tracking benchmark and evolutionary estimands

**Purpose:** establish the distinction between optimization, local
accessibility, recurrent-mutation occupancy, and finite-N weak-mutation
occupancy before introducing explicit landscapes.

Primary sources:

- `theory/MIGRATION_PHENOLOGY_TRACKING.md`
- `docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md`
- `data/payoff_b_tracking_synthetic_receipt_20260920.json`

Include:

- deterministic migration–phenology payoff surface;
- equal-`m+h` abiotic substitution check;
- classification definitions and their reporting-only status;
- deterministic rare-substitution walk;
- recurrent mutation–selection occupancy;
- exact finite-N weak-mutation stationary law;
- ecological-grid coordination-barrier count as a model diagnostic.

Do **not** promote the early ecological-grid barrier fraction as natural
prevalence.

Recommended items:

- **Table S1:** estimands and their definitions;
- **Figure S1:** deterministic optimum versus locally accessible endpoint
  schematic;
- **Table S2:** finite-N occupancy conditions used in the synthetic benchmark.

## Supplement S2 — Moving landscape, connectivity and anisotropy robustness

**Purpose:** support Figure 2 without crowding the main paper with route and
resolution details.

Primary sources:

- `docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md`
- `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`
- `data/payoff_b_moving_landscape_receipt_20260920.json`
- `data/payoff_b_2d_connectivity_receipt_20260920.json`

Include:

- 7 x 7 versus 11 x 11 one-dimensional frontier resolution;
- all six `z_max` persistence brackets;
- terminal-capacity diagnostic and its explicit status as a diagnostic rather
  than a theorem;
- centered versus displaced corridor comparison;
- gap-width crossing fractions;
- open / straight / zigzag route comparisons;
- full anisotropic movement table for y/x ratios 1, 0.5, 0.25 and 0.1;
- boundary-leakage robustness;
- stochastic integer patch-demography validation.

Recommended items:

- **Figure S2:** full one-dimensional frontier and resolution overlay;
- **Table S3:** corridor geometry and crossing fractions;
- **Figure S3:** zigzag penalty versus movement anisotropy;
- **Table S4:** boundary-retention and stochastic patch-demography robustness.

Main-text handoff:

Figure 2 retains only the finite temporal-bypass / spatial-re-entry sequence and
the headline buffering magnitude.

## Supplement S3 — Coordination-gate robustness and interaction geometry

**Purpose:** demonstrate that Figure 3 is not an artifact of mutation
resolution, centroid compression, boundary rule, or one special geometry.

Primary sources:

- `docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md`
- `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`
- `data/payoff_b_2d_connectivity_receipt_20260920.json`

Include:

- coarse versus fine unilateral mutation steps;
- interaction-strength breakdown;
- open / straight / zigzag barrier and persistence-rescue counts;
- direct one-step gate;
- distribution-level Bhattacharyya-overlap sensitivity;
- one-dimensional boundary-retention robustness;
- integer stochastic patch-demography persistence of the canonical rescue.

Recommended items:

- **Table S5:** coarse/fine barrier counts by interaction and geometry;
- **Figure S4:** unilateral gain versus overlap-penalty scale;
- **Table S6:** boundary retention and stochastic-demography checks.

Claim discipline:

The supplement may show all sampled design counts, but captions must state that
these frequencies describe synthetic parameter grids rather than natural
prevalence.

## Supplement S4 — Partner asymmetry and forcing-dependent synchronization

**Purpose:** provide the full cells behind Figure 4.

Primary source:

- `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`, section 8
- `data/payoff_b_2d_connectivity_receipt_20260920.json::partner_asymmetry`

Include:

- 3 x 3 partner-specific cost-bias combinations;
- interaction strengths 0, 0.5 and 1;
- moderate forcing `v=0.04`;
- strong forcing `v=0.06`;
- endpoint migration and timing strategies;
- partner strategy distance;
- interaction mismatch;
- persistence status.

Recommended items:

- **Figure S5:** 3 x 3 endpoint strategy matrices at moderate forcing;
- **Figure S6:** 3 x 3 endpoint strategy matrices at strong forcing;
- **Table S7:** persistence and mismatch summaries.

Main-text handoff:

Figure 4 reports only the sign change in the ecological effect of
synchronization. The complete partner-bias matrix remains supplementary.

## Supplement S5 — Demographic visibility and finite-N barrier crossing

**Purpose:** preserve the negative replication and separate stochastic crossing
from stochastic rescue.

Primary sources:

- `docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md`
- `data/payoff_b_tracking_synthetic_receipt_20260920.json`

Include:

- 32-replicate pilot as explicitly superseded cell-level evidence;
- independent 128-replicate demographic rerun;
- all visibility examples by baseline growth and carrying-capacity scale;
- local-persistence-bin summaries;
- finite-N drift rows at beta 5 and beta 20;
- high-payoff occupancy, local-endpoint occupancy and mean joint growth.

Recommended items:

- **Table S8:** pilot versus replication demographic summary;
- **Figure S7:** persistence gain by local persistence regime;
- **Table S9:** finite-N drift outcomes;
- **Figure S8:** escape probability and mean growth across population sizes.

Mandatory interpretation:

```text
barrier existence
!= demographic visibility
!= stochastic crossing
!= long-run payoff improvement
```

The failed large-effect replication is retained, not hidden.

## Supplement S6 — Closed-loop controller and explicit feedback robustness

**Purpose:** support Figure 6 and distinguish the exact local theorem from the
explicit spatial controller experiment.

Primary sources:

- `theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md`
- `docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md`
- `docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md`
- `data/payoff_b_closed_loop_tracking_receipt_20260920.json`
- `data/payoff_b_movement_feedback_landscape_receipt_20260920.json`

Include:

- full local stability classes;
- equal-cost controller witness at all frozen forcing values;
- movement-expensive and phenology-expensive cost-asymmetry witnesses;
- distinction between baseline movement rate `m` and feedback gain `q_m`;
- complete 105-cell explicit feedback design;
- weak, intermediate and strong forcing summaries;
- ceiling-contact fractions;
- within-persistent-regime feedback benefits.

Recommended items:

- **Figure S9:** local controller phase classes versus total gain `K`;
- **Table S10:** exact allocation witnesses;
- **Figure S10:** explicit landscape growth/mismatch across feedback gains;
- **Table S11:** fixed-`k_m=1.6` movement unloading by timing response.

Claim discipline:

Synthetic controller gain is not an empirical Aikens estimate. The GEB
phase-retention paper remains outside this supplement.

## Supplement provenance table

A final supplement table should record, for every frozen numerical source:

- result/receipt file;
- workflow run ID;
- artifact ID when available;
- SHA256 digest;
- frozen date;
- whether the source is primary, robustness-only, or superseded.

Use the provenance already stored in the five canonical JSON receipts rather
than manually retyping hashes into multiple places.

## Main-paper / supplement boundary

The main paper carries only six conceptual/results figures:

1. hierarchy;
2. finite temporal bypass and spatial re-entry;
3. direct coordination gate;
4. forcing-dependent synchronization;
5. demographic visibility and drift crossing;
6. local substitutability versus explicit complementarity.

The supplement owns:

- resolution checks;
- individual route geometries;
- individual anisotropy levels;
- full interaction/cost-bias matrices;
- overlap-penalty details;
- boundary-condition robustness;
- complete drift grids;
- complete controller grids.

This boundary is intended to keep the main paper mechanism-first rather than
parameter-sweep-first.
