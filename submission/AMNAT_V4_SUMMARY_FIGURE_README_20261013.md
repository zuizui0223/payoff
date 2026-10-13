# The American Naturalist Paper 2: four frozen-summary figure previews

Date: 2026-10-13
Status: **summary-figure renderer complete only if dedicated CI passes; this is NOT an anonymous reviewer archive or full biological reproduction.**
Base paper: PR #326; implementation branch: analysis/payoff-b-amnat-v4-four-figure-preview-20261013.

## Generate the preliminary SVGs

From the repository root:

    python -m pytest -q tests/test_payoff_b_amnat_v4_summary_figures.py
    python scripts/build_payoff_b_amnat_v4_summary_figures.py \
      --out outputs/amnat_v4_summary_preview \
      --zip outputs/amnat_v4_summary_preview.zip

No external dependencies are needed for figure rendering. Each output is deterministic SVG. The package contains:
- figure1_summary.svg — **theory schematic**, not inferred animal belief or fitness
- figure2_summary.svg — **2 environment-correlation summary estimates and pair-bootstrap intervals**, NOT 166 plotted observed pairs
- figure3_summary.svg — **registered transfer, fixed-arrival structural null, bird-increment summary estimates, confidence intervals and permutation-interval label**; no pair-level scatter
- figure4_summary.svg — **means of absolute phase and variance-ratio summaries** in Ortega mule deer; no reconstructed individual tracks
- LEGENDS.md — figure captions
- figure_manifest.json — exact SHA256 of every used repository receipt and generated SVG, as well as negative flags for raw-data inclusion and submission readiness.

These source-bounded views make the paper's numerical logic inspectable without inventing any raw observations.

## Frozen inputs and provenance

The renderer consumes exactly these repository files, without overwriting or recomputing their results:

1. docs/PAYOFF_B_V8_PRIMARY_AND_SENSITIVITY_RESULT_20261005.md (n=166 unique pairs; 28 species; mean change +0.3690; mean difference CI +0.2984 to +0.4365).
2. docs/PAYOFF_B_V8_DOWNSTREAM_TRANSFER_PRIMARY_RESULT_20261005.md (registered slope +0.06243969, 95% unique-pair CI -0.01411178 to +0.1363489; 150 exposure rows / 72 unique pairs / 22 species).
3. docs/PAYOFF_B_V8_TRANSFER_STRUCTURAL_NULL_RESULT_20261005.md (fixed-arrival beta +0.04742, paired observed-minus-fixed-arrival effect +0.01502; null permutation median +0.04677).
4. data/payoff_b_ortega_variance_funnel_result_20261003.json (152 animal-years, 72 individuals, end/start variance ratio 0.248875 and clustered 95% interval).
5. data/payoff_b_mule_deer_two_clock_channel_result_20261003.json (March condition subset 62 animal-years from 40 individuals; downstream gating not proven).

The renderer fails if primary environmental degradation or matching-transfer frozen status is changed. These values are summary-level estimates from source-data calculations; running this program DOES NOT independently verify the original Amaral and Ortega microdata or bootstrap code.

## Essential missing steps (explicit submission HOLD)

- **Pair-level green-up and species-target matched arrival records** from the original V8 climate and bird data, with precise source-mapping, joined years, bootstrap resamples and source SHA/DOI. No observed pair-level scatter may be generated until these are independently recoverable and a full data/figure audit passes.
- **Animal-year phase and actuator records** from the exact Ortega workbook, using its recorded SHA256, and complete individual-cluster bootstrap reproduction. No observed animal paths have been fabricated.
- Reviewer-compatible **anonymized**, line-numbered and double-spaced manuscript PDF; final citations and Literature Cited; figure legends with final visual inspection; full named outputs and verified archive of analysis scripts/input dependencies; author-approved declarations.
- Existing CI artifact is an internal figure preview (non-anonymous); it is NOT compliant with the journal's data/code archival and reviewer access requirements.
- Published controls and unrelated examples (pink-footed goose, redstart, social-cue studies) are **not** promoted to a new joint fitness result. They remain prior art or descriptive anchors.

## Interpretation ceiling

**F2** rejects an across-sample broad weakening of *spatial environmental correlations*, not of bird-perceived forecast information. **F3** does not show that increased information worsened timing: the primary slope's predicted direction was not supported and a fixed-arrival null reproduces the positive point direction. **F4** reproduces known phase convergence and actuator associations but does not identify the animal's internal feedback parameter, available information or survival consequences. **F1** is theory, not empirical verification.

Do not rename the machine status VERIFIED_SUMMARY_FIGURE_PREVIEW_SUBMISSION_HOLD to SUBMISSION_READY, or imply that the SVG preview ZIP contains complete underlying data.
