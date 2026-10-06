# American Naturalist V4.5 submission readiness — 2026-10-06

Status: **FIGURE / PACKAGE BUILD IN PROGRESS**

## Canonical files

Manuscript:
`manuscript/PAYOFF_B_FORECAST_ACCESS_CORRECTION_V4_5_AMNAT.md`

Front matter:
`submission/AMNAT_V4_5_FRONTMATTER_20261006.md`

Supporting Information:
`submission/AMNAT_V4_5_SUPPORTING_INFORMATION_20261006.md`

Figure captions:
`submission/AMNAT_V4_5_FIGURE_CAPTIONS_20261006.md`

Frozen figure data:
`data/payoff_b_v45_figure_data_20261006.json`

Figure renderer:
`scripts/render_payoff_b_v45_main_figures.py`

Claim stack:
`docs/PAYOFF_B_V4_5_CLAIM_STACK_20261006.md`

Novelty audit:
`docs/PAYOFF_B_V4_5_NOVELTY_AUDIT_20261006.md`

Adversarial audit:
`docs/PAYOFF_B_V4_5_ADVERSARIAL_READINESS_20261006.md`

## Current manuscript state

Target:
**The American Naturalist — Major Article**

Title:
**Seasonal tracking depends on information access and opportunities for
correction**

Main-text word count:
approximately **6,252**.

Abstract:
**165 words**.

Main figures:
**3 planned**.

Internal repository labels in journal-facing manuscript:
**none detected**.

## Scientific readiness

### Complete

- one ecological question;
- forecastability/access/actionability/correction hierarchy;
- preregistered environmental contrast retained as preregistered;
- posthoc diagnostics explicitly separated;
- rho-to-day-scale correction completed;
- alternative baseline robustness completed;
- year-leverage audit completed;
- source-rank sensitivity completed;
- source-event observability boundary completed;
- signed arrival–green-up timing decomposition completed;
- forecast-value transfer structural nulls completed;
- same-system stagewise subset audited;
- stagewise measurement uncertainty audited;
- phase-retention non-identifiability explicitly quarantined;
- mule-deer prior-art boundary explicit;
- novelty boundary checked against closest conceptual and empirical prior work.

### Scientific blocker for current American Naturalist route

**None requiring another analysis of the current datasets.**

### Blocker for a materially higher journal ceiling

A natural system jointly measuring at multiple ordered stages:
- external forecastability;
- actual organismal information access;
- retained correction opportunity;
- behavioral response;
- phase outcome.

This is future work, not a blocker for the current route.

## Main claim boundary

The paper may claim:

> Environmental forecastability, organismal information access and downstream
> correction are distinct stages of seasonal tracking.

It may also claim:

> In the sampled bird system, regional environmental structure gained analyst
> forecast value while population arrival changed little relative to an
> advancing target.

It may not claim:

- birds used the reconstructed source predictor;
- G_CV is organismal information value;
- actionability loss caused the bird pattern;
- individual feedback correction was identified in birds;
- climate change caused the two-window contrasts;
- zero arrival-minus-mid-green-up is the fitness optimum.

## Figure readiness

Figure 1:
framework.

Figure 2:
bird forecastability / observability / signed timing.

Figure 3:
mule-deer individual correction.

Current build:
`.github/workflows/payoff-b-v45-main-figures.yml`

Acceptance criteria:
- all three SVGs parse;
- deterministic SHA256 across two renders;
- frozen headline values appear verbatim;
- no internal version labels appear in rendered figures;
- figure manifest records input-data SHA256.

## Supporting Information scope

Main text should not absorb additional audit detail.

Supporting Information carries:
- dependence corrections;
- metric-scale derivations;
- baseline sensitivity;
- source-rank sensitivity;
- temporal-order and observability tables;
- transfer structural nulls;
- stagewise subset selection;
- measurement-error propagation;
- retention non-identifiability;
- complete mule-deer reanalysis details.

## Remaining practical tasks

1. Pass the deterministic main-figure CI.
2. Inspect rendered SVGs visually for clipping and density.
3. Freeze figure SHA256 receipts.
4. Build final anonymous manuscript package.
5. Build title-page metadata file separately.
6. Verify references and DOI formatting.
7. Apply final journal style / line numbering.
8. Prepare cover letter and reviewer suggestions.
9. Final human read for claim-status language.
10. Upload to journal portal.

## Stop rule

Do not add another biological analysis to the current datasets unless it repairs:
- a direct validity problem in a main figure;
- a source-definition flaw;
- a measurement-error flaw;
- an explicit reviewer-critical gap.

Otherwise proceed to submission build.
