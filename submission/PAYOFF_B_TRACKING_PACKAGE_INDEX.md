# PAYOFF-B tracking theory — submission package index

Updated: **2026-09-25**

Status: **scientifically frozen for first-submission preparation**

Canonical branch:

`main`

## Core manuscript

- `manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`
  - standalone synthetic theory manuscript;
  - separate from the GEB empirical phase-retention programme;
  - current framing is governed by the 2026-09-25 amendment: endpoint
    environmental mismatch does not identify the tracking architecture that
    produces it; coordination barriers are retained as one buffering-failure
    mode rather than the sole headline.

## Claim and provenance boundary

- `data/payoff_b_tracking_theory_claim_freeze_20260924.json`
- `data/payoff_b_tracking_theory_framing_amendment_20260925.json`
- `docs/PAYOFF_B_TRACKING_THEORY_PRIOR_ART_20260924.md`
- five frozen 2026-09-20 synthetic receipt families in `data/` and `docs/`

Authority rule:

- the 2026-09-24 claim freeze governs the scientific evidence and numerical
  claim boundary;
- the 2026-09-25 framing amendment governs the current title, headline
  contribution, novelty hierarchy, and testability framing when wording differs;
- no post-2026-09-20 empirical phase-retention result licenses a new synthetic
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

Post-reframing audited figure artifact:

- audited main HEAD `a89deb56ae096bf2d3840b16cfed2a7cd7f1dc98`;
- workflow run `36089011639`;
- artifact `10845126875`;
- SHA256 `5249d69a52b0e95f958432d121910bc1b45a90f6074ac7f5961492b3f2453513`.

## Methods and result organization

Parameter/design map:

- `submission/PAYOFF_B_TRACKING_PARAMETER_TABLE.md`

Results-to-figure crosswalk:

- `submission/PAYOFF_B_TRACKING_RESULTS_FIGURE_CROSSWALK.md`

Supplement structure:

- `submission/PAYOFF_B_TRACKING_SUPPLEMENT_MAP.md`

Portal-ready Supporting Information:

- source generator: `scripts/build_tracking_theory_supporting_information.py`
- RTF renderer: `scripts/build_oikos_supporting_information.py`
- generated source file: `PAYOFF_B_TRACKING_SUPPORTING_INFORMATION_V1.md`
- upload file: `OIKOS_TRACKING_SUPPORTING_INFORMATION.rtf`

These files define what remains in the main paper versus what belongs in
robustness/supplementary material.

## References

BibTeX:

- `submission/PAYOFF_B_TRACKING_REFERENCES.bib`

Current manuscript reference count:

- **10** normalized references;
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
- `submission/OIKOS_INITIAL_SUBMISSION_PACKET.md`
- current machine audit: `submission/OIKOS_MACHINE_PREPARATION_AUDIT_20260925.md`
- historical pre-reframing audit: `submission/OIKOS_MACHINE_PREPARATION_AUDIT_20260924.md`

Tracking-specific administrative templates:

- `submission/PAYOFF_B_TRACKING_TITLE_PAGE_TEMPLATE.md`
- `submission/PAYOFF_B_TRACKING_COVER_LETTER_TEMPLATE.md`

Remaining tasks are human/portal-specific only:

- fill verified author/title-page metadata and ORCID;
- finalize funding, conflict, ethics, acknowledgment and CRediT declarations;
- complete ScholarOne entries and uploads;
- replace the post-acceptance repository placeholder when a public DOI exists.

No unresolved machine-generation or synthetic-analysis task remains.

## Reproducible working package

Builder:

- `scripts/build_tracking_theory_submission_package.py`

Canonical command:

```bash
python scripts/build_tracking_theory_submission_package.py \
  --output-dir outputs/tracking_theory_submission_package \
  --zip outputs/PAYOFF_B_TRACKING_SUBMISSION_PACKAGE.zip
```

The builder assembles the manuscript-facing files, a Supporting Information
document generated from the five frozen JSON receipts, internal claim/provenance
contracts, the five frozen synthetic receipt families, the two core theory
documents, and freshly rendered Figures 1–6. It writes per-file SHA256 values
to `PAYOFF_B_TRACKING_SUBMISSION_MANIFEST.json`. The ZIP uses a fixed frozen
timestamp so identical content produces an identical archive, and
`PAYOFF_B_TRACKING_SUBMISSION_ARCHIVE_RECEIPT.json` records the package-manifest
hash and final ZIP SHA256 without creating a circular self-hash.

CI artifact name:

`payoff-b-tracking-theory-submission-package`

The bundle contract explicitly excludes the later empirical phase-retention
programme (including Aikens/wigeon/barnacle observation products).


Anonymous review code/data bundle:

- builder: `scripts/build_tracking_theory_review_bundle.py`
- ZIP: `OIKOS_TRACKING_ANON_CODE_DATA.zip`
- CI artifact: `payoff-b-tracking-theory-anonymous-review-bundle`
- contents: frozen synthetic receipts/results, theory documents, declared sweep
  entry points, figure/SI builders, and recursively resolved `src/`
  dependencies only;
- anonymity gate: rejects author-identifying tokens, email addresses, and
  empirical-programme paths before archive creation.

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
- current framing-amendment authority and novelty boundary;
- visual-audit receipt;
- scientific-freeze declaration;
- Oikos abstract <=300-word/citation/acronym compliance;
- frozen Supporting Information generation;
- deterministic submission ZIP across output paths.

## Stop rule

Do not add another synthetic sweep merely to increase parameter volume.

A new simulation requires one of:

1. a specific reviewer-relevant robustness gap not already covered;
2. failure of an existing claim/figure contract;
3. a closer prior-art model that requires a matched contrast.

Otherwise the correct next action is journal-specific submission preparation,
not further model expansion.
