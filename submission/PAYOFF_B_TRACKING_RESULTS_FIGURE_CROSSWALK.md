# PAYOFF-B tracking theory — results-to-figure crosswalk

Updated: **2026-09-24**

Canonical manuscript:

`manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`

Canonical figure captions:

`submission/PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md`

Canonical parameter map:

`submission/PAYOFF_B_TRACKING_PARAMETER_TABLE.md`

Purpose:

Every principal Results claim in the standalone tracking-theory manuscript is
assigned to a main figure or to an explicitly named frozen supplementary
receipt. Main figures summarize the claim; frozen receipts remain the numeric
source of truth.

## Crosswalk

| Results section | Principal claim | Main figure | Frozen source / supplement | Main-text status |
|---|---|---|---|---|
| 3.1 Phenological capacity extends tracking | Increasing `z_max` expands the sampled persistence frontier, but frontier strategies remain migration-dominant | Figure 2A | `docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md`; `data/payoff_b_moving_landscape_receipt_20260920.json` | primary result |
| 3.2 Temporal bypass and spatial re-entry | At high timing capacity, phenology-only tracking at `v=0.04–0.05` becomes mixed by `v=0.06`; corridor crossing reappears | Figure 2B | `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`; `data/payoff_b_2d_connectivity_receipt_20260920.json` | primary result |
| 3.3 Route-cost buffering under anisotropy | Timing reduces zigzag growth-cost magnitude by ~83% in the canonical route comparison and ~75–76% across sampled anisotropy levels | Figure 2 annotation; Supplement S2 | `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`, sections 3 and 9 | primary mechanism + robustness |
| 3.4 Interaction matching creates coordination barriers | Positive interaction produces widespread barriers in the declared 2D design; fine grid retains 22/24 barriers and 21/24 persistence rescues | Figure 3 summary | `data/payoff_b_2d_connectivity_receipt_20260920.json` | primary result |
| 3.5 Direct one-step coordination gate | Joint adjacent timing shift is beneficial while either unilateral shift is strongly deleterious | Figure 3 | `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`, section 6 | central mechanism |
| 3.6 Distribution-level overlap sensitivity | Adding an explicit Bhattacharyya-overlap penalty preserves the barrier and makes unilateral escape more costly | Supplement S3 | `data/payoff_b_2d_connectivity_receipt_20260920.json::distribution_overlap_sensitivity` | robustness, not main novelty |
| 3.7 Synchronization changes sign with forcing | Interaction aligns partner strategies at moderate forcing but locks them onto an extinct local attractor under stronger forcing | Figure 4 | `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`, section 8 | primary ecological consequence |
| 3.8 Demographic visibility window | Higher-replication demographic effects are largest near persistence transitions; pilot large cell effects do not replicate | Figure 5A | `docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md`; `data/payoff_b_tracking_synthetic_receipt_20260920.json` | primary negative/positive synthesis |
| 3.9 Drift crossing is not rescue | Small `N` crosses the deterministic barrier more often, but mean long-run joint growth is not improved | Figure 5B | `data/payoff_b_tracking_synthetic_receipt_20260920.json::drift_escape` | primary negative result |
| 3.10 Local substitution -> landscape complementarity | Local `K=q_m+q_h` equivalence breaks under finite movement/timing capacities; timing crosses the sampled persistence boundary and unloads movement demand | Figure 6 | `docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md`; `docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md` | primary cross-scale synthesis |

## Main-figure numeric contract

### Figure 2

Licensed main-text numbers:

- one-dimensional frontier brackets for `z_max=0,...,5`;
- 2D `z_max=4` strategy sequence at `v=0.04,0.05,0.06,0.07`;
- second-wall crossing approximately 0, 0, 0.1318, 0.3144;
- canonical zigzag penalty reduction approximately 83%.

Anisotropy-specific penalty values stay supplementary. The main text may report
the approximately 75–76% range but should not add the four individual
anisotropy penalties unless Supplement S2 is cited.

### Figure 3

Licensed main-text numbers:

- fine positive-interaction design: 22/24 barriers;
- 21/24 persistence rescues;
- resident `(m,h)=(0.2,0)`;
- coordinated adjacent strategy `(0.2,0.2)`;
- resident joint growth approximately -0.840;
- coordinated joint growth approximately +0.255;
- coordinated gain approximately +1.095;
- unilateral gains approximately -5.946;
- unilateral interaction mismatch approximately 3.747.

Distribution-overlap scale-specific gains stay supplementary.

### Figure 4

Licensed main-text comparisons:

- moderate forcing `v=0.04`: all 9 pairs persist under `I=0,0.5,1`;
- interaction `I=0.5` or `1` collapses mean strategy distance to zero;
- strong forcing `v=0.06`: no-interaction pairs persist at matched mixed
  tracking, while interacting pairs synchronize to the migration-only lock and
  0/9 persist.

The full 3 x 3 partner cost-bias matrix stays supplementary.

### Figure 5

Licensed main-text numbers:

- independent demographic replication: 396 barrier cells;
- mean persistence gain approximately 0.0055;
- maximum replicated gain 0.09375;
- pilot cells with gain >=0.10: 9;
- replicated cells with gain >=0.10: 0;
- mean gain near local persistence 0.3–0.7: approximately 0.0197;
- mean gain at local persistence 0.9–1: approximately 0.0011;
- at `beta=5`, escape fractions 0.9375 at `N=10`, 0.96875 at `N=30`,
  and 0 at `N=100`.

The manuscript must preserve the interpretation that barrier crossing is not
equivalent to evolutionary rescue.

### Figure 6

Licensed main-text numbers and exact statements:

- exact local recurrence `e_(t+1)=(1-q_m-q_h)e_t+r`;
- `K=q_m+q_h`;
- exact stability `0<K<2`;
- at `v=0.05` and `0.06`, `h=0` has 0/7 persistent controller gains;
- `h=0.25` and `h=0.5` have 7/7;
- at `v=0.06, k_m=1.6`, mean effective movement is 0.947854, 0.325324,
  and 0.231577 for `h=0,0.25,0.5`, respectively.

Other closed-loop witness values belong in Supplement S5 unless specifically
needed to explain the stability theorem.

## Numbers deliberately excluded from headline figures

These values remain valid frozen results but should not be promoted as
additional headline evidence:

- descriptive linear frontier slope and R-squared;
- terminal-capacity diagnostic fit statistics;
- coarse 1D barrier counts once the fine-resolution comparison is available;
- individual distribution-overlap sensitivity gains;
- full anisotropy penalty table;
- the initial 32-replicate demographic maximum 0.1875 except when explicitly
  contrasted with its failed replication;
- beta=20 drift rows;
- exact synthetic controller-optimum values for all forcing levels.

They belong in the supplement or robustness text.

## No-orphan-number rule

Before manuscript freeze:

1. every numerical statement in Results 3.1–3.10 must appear in this crosswalk;
2. every main-text number must trace to one of the five frozen 2026-09-20
   synthetic receipts;
3. a number absent from this crosswalk is either moved to the supplement or
   removed from the main Results;
4. GEB phase-retention numbers never enter this crosswalk.

This rule keeps the standalone theory paper independent of later empirical
programme growth.
