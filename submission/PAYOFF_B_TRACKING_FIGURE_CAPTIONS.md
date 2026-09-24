# PAYOFF-B tracking theory — figure captions

Manuscript: `manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`

Rendering command:

```bash
python scripts/render_tracking_theory_figures.py \
  --output-dir submission/tracking_theory_figures
```

CI artifact name:

```text
payoff-b-tracking-theory-figures
```

All quantitative panels are rendered from the five frozen synthetic receipts dated
2026-09-20 through `scripts/build_tracking_theory_figure_data.py`. Post-2026-09-20
empirical phase-retention results are excluded.

## Figure 1. From buffered mismatch to tracking breakdown

**File:** `PAYOFF_B_TRACKING_FIG1_CONCEPT.svg`

Conceptual hierarchy showing why endpoint environmental mismatch does not
identify the tracking architecture that produces it. In the exact local null,
movement and timing share one restoring budget, so similar mismatch can be
maintained by different allocations between axes. Finite phenological capacity
then imposes a temporal-buffer ceiling, after which spatial tracking re-enters
under stronger forcing. Partner matching adds a second limit: reallocation can
be jointly favourable yet deleterious to either partner moving first. Population
consequences are most visible near persistence boundaries. This panel is a
synthesis diagram and contains no additional simulation result.

## Figure 2. Finite temporal bypass and spatial re-entry

**File:** `PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg`

(A) One-dimensional moving-landscape persistence brackets across increasing
phenological capacity. The solid series gives the maximum sampled climate
velocity that persisted; the dashed series gives the first sampled velocity that
failed. The frontier moves from 0.030/0.035 at phenology limit 0 to 0.065/0.070
at phenology limit 5, while frontier strategies remain migration dominant.
(B) Canonical two-dimensional zigzag sequence at phenology limit 4. The optimum
is phenology-only at climate velocities 0.04 and 0.05, becomes mixed at 0.06,
and increases its migration component at 0.07. The second-wall crossing fraction
rises from approximately zero to 0.132 and 0.314 at 0.06 and 0.07,
respectively. Across the frozen open-versus-zigzag comparison, phenology limit 4
reduces the magnitude of the sampled route growth penalty by approximately 83%.
These values are synthetic design results, not empirical climate thresholds.

## Figure 3. Coordinated value is not unilateral accessibility

**File:** `PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg`

Direct one-step audit of the canonical two-dimensional coordination barrier.
The matched resident strategy `(m,h)=(0.2,0)` has joint low-density growth
approximately -0.840. Shifting both partners to the adjacent matched strategy
`(0.2,0.2)` raises joint growth to approximately +0.255, a coordinated gain
of +1.095. The same timing change by either partner alone has payoff gain
approximately -5.946 because it creates strong transient partner mismatch.
Across the fine positive-interaction two-dimensional grid, 22 of 24 cells retain
a coordination barrier and 21 of 24 convert local extinction into coordinated
persistence. These frequencies describe the declared synthetic grid and are not
natural prevalence estimates.

## Figure 4. Interaction-mediated synchronization changes ecological sign

**File:** `PAYOFF_B_TRACKING_FIG4_SYNCHRONIZATION.svg`

Partner-asymmetry experiment showing forcing-dependent effects of the same
interaction-matching mechanism. Under moderate forcing (`v=0.04`), intrinsic
tracking preferences differ without interaction, whereas interaction strengths
0.5 and 1 collapse mean partner strategy distance to zero and all sampled pairs
persist. Under stronger forcing (`v=0.06`), the no-interaction pairs converge
to matched mixed tracking and all persist, while the interacting pairs
synchronize onto a migration-only local attractor and all fail. Interaction
therefore acts as beneficial alignment or maladaptive lock depending on whether
the synchronized attractor lies within the persistence envelope.

## Figure 5. Barrier visibility and finite-population crossing

**File:** `PAYOFF_B_TRACKING_FIG5_DEMOGRAPHY_DRIFT.svg`

(A) Population-level consequences of coordination barriers are concentrated
near persistence transitions. In the independent 128-replicate demographic
rerun, mean persistence gain is approximately 0.0197 for cells with local
persistence between 0.3 and 0.7 but only approximately 0.0011 for cells already
in the 0.9–1 range. The pilot contained nine barrier cells with persistence gain
at least 0.10; the higher-replication rerun contained none, and its maximum gain
was 0.09375. (B) Finite-population substitution dynamics at `beta=5`. Barrier
crossing is frequent at `N=10` and `N=30` but absent in the retained
high-payoff sense at `N=100` and above. Small-population exploration does not
raise mean long-run joint growth above the deterministic local endpoint in the
sampled regime. The retained conclusion is drift-assisted crossing, not drift
rescue.

## Figure 6. From local substitutability to explicit-landscape complementarity

**File:** `PAYOFF_B_TRACKING_FIG6_COMPLEMENTARITY.svg`

(A) Exact local controller null. Movement-mediated feedback `q_m` and
timing-mediated feedback `q_h` enter mismatch dynamics only through total
restoring gain `K=q_m+q_h`, with stability for `0<K<2`; at fixed `K`,
quadratic costs determine allocation between channels. (B) The explicit spatial
landscape breaks that equivalence under strong forcing. At climate velocity
0.06, none of seven sampled movement-feedback gains persist when the independent
timing rate is zero, whereas all seven persist at timing rates 0.25 and 0.5.
(C) At fixed movement-feedback gain 1.6 and velocity 0.06, increasing timing
response from zero to 0.25 or 0.5 reduces mean effective movement from 0.948 to
0.325 or 0.232, respectively, while moving the system into the persistent
regime. The comparison illustrates forcing-dependent complementarity rather than
a universal empirical rescue threshold.
