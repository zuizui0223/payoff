# PAYOFF-B tracking theory — submission package index

Updated: **2026-09-24**

Status: **scientifically frozen for first-submission preparation**

Branch:

`feature/payoff-b-migration-phenology-20260919`

## Core manuscript

- `manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`
  - standalone synthetic theory manuscript;
  - separate from the GEB empirical phase-retention programme;
  - final novelty sentence frozen around adaptive capacity versus unilateral
    accessibility.

## Claim and provenance boundary

- `data/payoff_b_tracking_theory_claim_freeze_20260924.json`
- `docs/PAYOFF_B_TRACKING_THEORY_PRIOR_ART_20260924.md`
- five frozen 2026-09-20 synthetic receipt families in `data/` and `docs/`

Rule:

No post-2026-09-20 empirical phase-retention result licenses a new synthetic
claim in this manuscript.

## Figures

Generator:

- `scripts/render_tracking_theory_figures.py`

Figure-data builder:

- `scripts/build_tracking_theory_figure_data.py`

Main figures:

1. `PAYOFF_B_TRACKING_FIG1_CONCEPT.svg`
2. `PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg`
3. `PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg`
4. `PAYOFF_B_TRACKING_FIG4_SYNCHRONIZATION.svg`
5. `PAYOFF_B_TRACKING_FIG5_DEMOGRAPHY_DRIFT.svg`
6. `PAYOFF_B_TRACKING_FIG6_COMPLEMENTARITY.svg`

Captions:

- `submission/PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md`

Visual audit:

- `submission/PAYOFF_B_TRACKING_FIGURE_VISUAL_AUDIT.md`

Audited green artifact:

- workflow run `35987790697`;
- artifact `10803495155`;
- SHA256 `0d61c3f691d3d37cdffcb3703ec0fd6dd43efdf1d3442cda1cd8ba379a01914e`.

## Methods and result organization

Parameter/design map:

- `submission/PAYOFF_B_TRACKING_PARAMETER_TABLE.md`

Results-to-figure crosswalk:

- `submission/PAYOFF_B_TRACKING_RESULTS_FIGURE_CROSSWALK.md`

Supplement structure:

- `submission/PAYOFF_B_TRACKING_SUPPLEMENT_MAP.md`

These three files define what remains in the main paper versus what belongs in
robustness/supplementary material.

## References

BibTeX:

- `submission/PAYOFF_B_TRACKING_REFERENCES.bib`

Current manuscript reference count:

- eight normalized references;
- DOI metadata checked and guarded by CI.

## Submission readiness

- `submission/PAYOFF_B_TRACKING_SUBMISSION_READINESS.md`

Scientific status:

- no unresolved synthetic result;
- no unresolved claim-boundary issue;
- no unresolved parameter-status issue;
- no unresolved main-figure mapping issue;
- no unresolved bibliography issue;
- no unresolved figure clipping/overlap issue.

Journal targeting:

- `submission/PAYOFF_B_TRACKING_JOURNAL_TARGETING_20260924.md`
- first shot: **Oikos**
- strong fallback: **Theoretical Ecology**
- stretch option: **Global Change Biology**

Oikos handoff:

- `submission/OIKOS_TRACKING_HANDOFF_V1.md`

Tracking-specific administrative templates:

- `submission/PAYOFF_B_TRACKING_TITLE_PAGE_TEMPLATE.md`
- `submission/PAYOFF_B_TRACKING_COVER_LETTER_TEMPLATE.md`

Remaining tasks are target-journal-specific only:

- fill verified author/title-page metadata;
- adapt references to the selected journal style;
- finalize declarations;
- replace repository placeholders with an archived DOI;
- perform portal-specific file conversion or upload steps.

## CI contracts

The tracking-theory package is guarded by tests covering:

- manuscript text integrity;
- frozen negative results;
- claim-freeze consistency;
- figure-data provenance;
- six SVG rendering contracts;
- parameter-map values;
- Results-to-Figure and supplement maps;
- bibliography normalization;
- final novelty sentence;
- visual-audit receipt;
- scientific-freeze declaration.

## Stop rule

Do not add another synthetic sweep merely to increase parameter volume.

A new simulation requires one of:

1. a specific reviewer-relevant robustness gap not already covered;
2. failure of an existing claim/figure contract;
3. a closer prior-art model that requires a matched contrast.

Otherwise the correct next action is journal-specific submission preparation,
not further model expansion.
