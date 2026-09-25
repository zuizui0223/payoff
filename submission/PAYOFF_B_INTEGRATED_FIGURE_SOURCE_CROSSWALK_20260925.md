# PAYOFF-B integrated tracking ecology — six-figure source crosswalk

Updated: **2026-09-25**

Canonical experimental manuscript:

\`manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md\`

Purpose: prevent the integrated paper from becoming a concatenation of two
existing figure sets. Each main figure must answer one step in the single
argument

\`\`\`text
non-identifiability
-> ecological breakdown
-> broad falsification
-> mechanistic decomposition
-> information / actuation test
\`\`\`

and every quantitative panel must trace to a frozen source.

## Figure 1 — One mismatch, multiple tracking architectures

**Role:** conceptual bridge only.

Required content:

- separate PAYOFF-B1 anti-phase seasonal-timescale benchmark as a small
  contextual box, not a new theorem panel;
- local movement + timing restoring-budget null;
- empirical phase-retention coordinate;
- explicit statement that equal endpoint mismatch does not identify allocation
  among movement, timing, information and actuation.

Reusable source:

- \`PAYOFF_B_TRACKING_FIG1_CONCEPT.svg\`
- \`scripts/render_tracking_theory_figures.py::figure1\`
- \`submission/PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md::Figure 1\`

Build decision:

**RENDER NEW INTEGRATED VERSION.** The current tracking-theory Figure 1 already
contains most of the conceptual hierarchy, but the integrated paper needs one
additional empirical phase-retention branch and a visually subordinate PAYOFF-B1
benchmark box.

No new quantitative result is licensed.

## Figure 2 — Finite temporal buffering and spatial re-entry

**Role:** show why one-dimensional mismatch can hide a changing allocation of
tracking effort.

Reusable source:

- \`PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg\`
- \`scripts/render_tracking_theory_figures.py::figure2\`
- \`data/payoff_b_moving_landscape_receipt_20260920.json\`
- \`data/payoff_b_2d_connectivity_receipt_20260920.json\`
- \`docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md\`
- \`docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md\`

Licensed main numbers:

- 1D persistence bracket moves from 0.030/0.035 at \(z_{\max}=0\) to
  0.065/0.070 at \(z_{\max}=5\);
- zigzag \(z_{\max}=4\) is phenology-only at 0.04–0.05 and mixed from 0.06;
- second-wall crossing approximately 0, 0, 0.132, 0.314;
- canonical zigzag route-penalty magnitude reduction approximately 83%.

Build decision:

**REUSE / LIGHT REFRAME.** The current Figure 2 already carries the exact
mechanistic content needed by the integrated paper.

## Figure 3 — Partner dependence blocks coordinated reallocation

**Role:** show a second reason low mismatch / local adaptation can be fragile:
the next better tracking architecture may be jointly beneficial but individually
inaccessible.

Reusable source:

- \`PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg\`
- \`scripts/render_tracking_theory_figures.py::figure3\`
- \`data/payoff_b_2d_connectivity_receipt_20260920.json\`
- \`docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md\`

Licensed main numbers:

- 22/24 coordination barriers in the declared positive-interaction 2D grid;
- 21/24 local-extinction to coordinated-persistence conversions;
- resident \((m,h)=(0.2,0)\);
- adjacent coordinated strategy \((0.2,0.2)\);
- resident joint growth approximately -0.840;
- coordinated joint growth approximately +0.255;
- coordinated gain approximately +1.095;
- unilateral gain approximately -5.946.

Build decision:

**REUSE / COMPRESS.** Distribution-overlap, synchronization, demographic
visibility and drift panels move to integrated Supporting Information unless a
reviewer requires them in main text.

This is the largest compression relative to the standalone Oikos manuscript.

## Figure 4 — Broad natural test rejects one universal speed rule

**Role:** primary empirical generality test.

Required content:

- registered 5,816-observation / 55-species sample;
- raw absolute arrival–green-up mismatch versus speed ratio;
- local species-by-cell phase-centered mismatch versus speed ratio;
- species-level curvature / vertex heterogeneity summary;
- moderator null summary only if visually compact.

Current frozen headline values:

- median observed animal/environment front-speed ratio: 1.263;
- median directional alignment: 0.948;
- raw-mismatch flexible minimum at median alignment:
  \(u_{\rm macro}\approx0.405\);
- phase-centered flexible minimum at median alignment:
  \(u_{\rm macro}\approx1.043\);
- phase-centered flexible minimum under perfect alignment:
  approximately 1.397;
- minima remain shallow / heterogeneous and no registered moderator recovers one
  convincing universal rule.

Current provenance:

- \`manuscript/PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V3_PREOUTCOME.md\`,
  section “Broad bird data reject a universal natural speed-ratio optimum”;
- \`data/payoff_b_empirical_phase_panel_status_20260921.json::broad_bird_falsification\`;
- \`docs/PAYOFF_B_EMPIRICAL_PHASE_PANEL_STATUS_20260921.md\`.

Build decision:

**NEW INTEGRATED EMPIRICAL RENDERER REQUIRED.**

Before this PR can merge, the exact machine result / derived table supplying the
0.405 / 1.043 / 1.397 curves must be named explicitly in this crosswalk. The
manuscript is an acceptable prose source for the experimental draft but is not
a sufficient final figure-data provenance layer.

## Figure 5 — Real systems transform phase error through different architectures

**Role:** explain what replaces the failed universal speed rule.

Required panels:

A. direct segment-scale phase-retention estimates for mule deer, highlighted
barnacle-goose transitions and wigeon POWER/ERA5;

B. interval-scale / retained-memory comparison that explicitly prevents direct
biological ranking of raw lambda;

C. actuator architecture annotations: mule deer speed + stopover; barnacle
route-stage stopover/overtake; wigeon actuator reconstruction sensitivity.

Primary sources:

- \`data/payoff_b_empirical_phase_panel_status_20260921.json\`;
- \`data/payoff_b_phase_retention_interval_standardization_result_20260925.json\`;
- \`data/payoff_b_three_taxon_phase_retention_receipt_20260922.json\`;
- \`data/wigeon_era5_sourcefaithful_calibration_result_20260924.json\`;
- \`data/barnacle_era5_reliability_result_20260924.json\`;
- \`data/svalbard_barnacle_era5_reliability_result_20260924.json\`;
- \`docs/MOVEMENT_PHENOLOGY_MULE_DEER_RECEIPT.md\`;
- \`docs/PAYOFF_B_WIGEON_ERA5_SOURCEFAITHFUL_CALIBRATION_20260924.md\`;
- \`docs/PAYOFF_B_BARNACLE_ERA5_RELIABILITY_20260924.md\`.

Key main values:

- mule deer whole-migration lambda approximately 0.107;
- wigeon POWER lambda 0.749768 on 224 transitions / 28 individuals;
- wigeon ERA5 lambda 0.811312 on the same complete 224 transitions;
- highlighted goose POWER/ERA5 values retained with overshoot sign;
- wigeon typical seven-transition retained memory approximately 0.133 POWER and
  0.231 ERA5;
- conservative SIMEX path-memory sensitivity approximately 0.627.

Build decision:

**NEW INTEGRATED EMPIRICAL RENDERER REQUIRED**, but all major panel values have
machine-readable frozen sources.

## Figure 6 — Information, retention and actuation are distinct

**Role:** final mechanistic synthesis and within-taxon perturbation.

Pre-outcome panels:

A. environmental innovation \(\sigma_\xi\) versus raw segment-scale
\(|\lambda|\) for the stable barnacle-goose transitions;

B. industrial-development movement-control permeability contrast and the
falsified stronger longitudinal trend;

C. reserved Aikens fixed-24h phase-retention contrast, populated only by the
registered outcome-blind renderer if estimable. If the Aikens contrast is
non-estimable, panel C must show the registered support failure rather than be
silently dropped.

Sources:

- \`docs/PAYOFF_B_INDUSTRIAL_MULE_DEER_ACTUATOR_RECEIPT_20260921.md\`;
- \`data/payoff_b_empirical_phase_panel_status_20260921.json\`;
- barnacle environmental-innovation source used by the frozen GEB manuscript;
- \`data/aikens2022_lambda_outcome_interpretation_contract_20260922.json\`;
- future registered \`aikens_primary_lambda_result.json\` only after the frozen
  extraction workflow runs.

Build decision:

**NEW INTEGRATED EMPIRICAL RENDERER REQUIRED.**

## Material intentionally removed from integrated main figures

The following remain valid evidence but move to Supporting Information:

- current tracking Figure 4 synchronization sign-change grid;
- current tracking Figure 5 demographic visibility + drift;
- current tracking Figure 6 detailed closed-loop feedback sweep;
- full anisotropy sensitivity;
- full distribution-overlap sensitivity;
- full 1D / 2D coordination parameter grids;
- wigeon SIMEX scenario-by-scenario curves;
- all barnacle route rows beyond highlighted reliability / mechanism examples;
- all eight industrial near/far definitions beyond the compact robustness
  summary.

The integrated manuscript should not exceed six main figures by promoting these
back into the main sequence.

## Merge gate

This crosswalk is considered complete only when:

1. Figures 1–3 can be rendered from the existing frozen synthetic builder or a
   deterministic wrapper;
2. the exact Figure 4 broad-bird machine result path is identified;
3. Figures 5–6 consume machine-readable empirical receipts rather than values
   copied from manuscript prose;
4. all Aikens-dependent material is outcome-blind;
5. no integrated figure implies a pooled universal lambda or a prevalence
   estimate from a synthetic parameter grid.
