# American Naturalist V4.5 portal handoff — 2026-10-07

Status: **PORTAL READY — AUTHOR METADATA / UPLOAD ONLY**

Final green-build receipt:
`docs/PAYOFF_B_V4_5_FINAL_GREEN_BUILD_RECEIPT_20261007.md`

Repository-wide `test` and `test-environments` both passed on the canonical
science SHA **6d826796099941af65d16487b86511151005442d**.

## Article

Journal:
**The American Naturalist**

Article type:
**Major Article**

Title:
**Seasonal tracking depends on information access and opportunities for correction**

Short title:
**Information access and correction**

Keywords:
1. environmental forecastability
2. information access
3. phenological mismatch
4. migration
5. actionability
6. feedback control

Current anonymous-manuscript statistics:
- Abstract: **167 words**
- main text before Literature Cited: **6385 words**
- main figures: **3**
- review DOCX pages after rendering: **30**

## Canonical reviewer files

### 1. Main anonymous manuscript

Use the final anonymous DOCX artifact:

- workflow run: **37562979913**
- artifact id: **11457418624**
- artifact digest:
  **sha256:29d51b8a0d6038190de76603cf7ccf55261b23d19da3ebb6c74d4a49a4ae5f9a**

Contents / formatting:
- no author names or affiliations;
- anonymous title page;
- title, short title, six keywords, word count, article type and manuscript
  elements on page 1;
- Abstract starts on a separate page;
- main text starts on a separate page;
- double-spaced;
- continuous line numbering;
- page numbering;
- Methods before Natural evidence;
- Literature Cited followed by Figure Legends.

Final visual-QA receipt:
`docs/PAYOFF_B_V4_5_FINAL_DOCX_RECEIPT_20261007.md`

### 2. Main figures

Use the three frozen reviewer-facing figures:

- Figure 1: forecastability / access / actionability / correction framework
- Figure 2: bird forecastability / observability / signed timing
- Figure 3: mule-deer individual correction anchor

Frozen figure workflow:
- run: **37407791647**
- artifact id: **11387890969**
- digest:
  **sha256:499850ff5d865c50bb3e916f5ce17d90b69652ba17b012a16d1e201f67a038f2**

Figure receipt:
`docs/PAYOFF_B_V4_5_MAIN_FIGURE_RECEIPT_20261006.md`

Figure legends:
`submission/AMNAT_V4_5_FIGURE_CAPTIONS_20261006.md`

All three legends are below 100 words.

### 3. Supporting Information

Use:
`submission/AMNAT_V4_5_SUPPORTING_INFORMATION_20261006.md`

Supporting Information contains the audit-heavy material intentionally removed
from the main-text narrative:
- dependence sensitivities;
- metric-scale forecast decomposition;
- G_CV robustness;
- alternative baseline;
- source-rank sensitivity;
- event-order / observability audit;
- signed timing;
- forecastability-to-timing structural null;
- restricted stagewise analyses;
- measurement-uncertainty audit;
- retention non-identifiability;
- mule-deer source-data reanalysis details;
- theoretical / claim boundaries.

### 4. Anonymous data/code package for review

Use the anonymous reproducibility artifact:

- workflow run: **37562808347**
- artifact id: **11456844175**
- digest:
  **sha256:b190078595ee4ba4f026f600a1b8d26b068c7e21edb5a6f8f3924ee8e618975d**

The archive contains manuscript-specific code/contracts/tests and an anonymous
README. Identity scan passed.

Data/code statement:
`submission/AMNAT_V4_5_DATA_CODE_REVIEW_STATEMENT_20261006.md`

## Anonymous reviewer package receipt

The current anonymous reviewer ZIP was rebuilt from the current science
manuscript:

- workflow run: **37562980001**
- manuscript head: **6d826796099941af65d16487b86511151005442d**
- artifact id: **11456869372**
- digest:
  **sha256:4e790b88d90955a6318f291e8b67c9a6fcb4ce15aaecbce876b4f4f6f356823e**

Manifest statistics:
- Abstract: **167 words**
- main text: **6385 words**

The reviewer ZIP contains only:
- anonymous manuscript source;
- Supporting Information;
- figure legends;
- Figure 1;
- Figure 2;
- Figure 3;
- manifest.

It contains no title page with author identity and no internal project/version
labels.

## Editorial Manager metadata — author must supply

Do not put these identifiers into the anonymous reviewer manuscript.

Fill in the portal:
- full author list;
- author order;
- affiliations;
- corresponding author;
- corresponding email;
- ORCID(s), if requested;
- funding;
- conflicts of interest;
- author contributions;
- acknowledgments;
- preprint status / URL, if applicable;
- any other required declarations.

Draft for the portal Comments field:
`submission/AMNAT_V4_5_AUTHOR_COMMENTS_DRAFT_20261006.md`

The journal does not require a conventional sales-oriented cover letter for
initial submission; keep portal comments factual.

## Generative-AI disclosure

The Methods section already states that ChatGPT (OpenAI) was used under author
supervision for:
- manuscript drafting/editing;
- code drafting/troubleshooting;
- deterministic figure-layout code.

The disclosure explicitly states that AI output was not treated as empirical
data or statistical results and that authors retain responsibility.

Do not remove this disclosure from the submission copy.

## Evidence-status rule during portal entry

If the portal asks for a short summary or significance statement, preserve this
boundary:

Preregistered:
- source-destination detrended-correlation contrast.

Posthoc:
- metric-scale decomposition;
- G_CV;
- baseline/source-rank sensitivities;
- observability;
- signed timing;
- transfer structural null;
- stagewise bird diagnostics.

Published prior phenomenon + reanalysis:
- mule-deer compensation/resynchronization.

Do not describe posthoc G_CV or bird-stage analyses as preregistered.

## Portal-safe one-sentence contribution

> Seasonal tracking depends not only on how forecastable future conditions are,
> but on whether organisms can access that information and still convert
> residual timing error into correction.

## Claims that must not appear in portal summaries

Do not write:
- birds received better information but failed to use it;
- G_CV is bird information value;
- birds observed source mid-green-up;
- birds were shown to use downstream feedback;
- climate change caused the two-window difference;
- zero arrival-minus-mid-green-up is the fitness optimum;
- mule-deer compensation was discovered here.

## Final human checks immediately before clicking Submit

1. Confirm author order.
2. Confirm affiliations and corresponding-author email.
3. Confirm funding / COI / contribution statements.
4. Confirm preprint declaration.
5. Confirm anonymous manuscript contains no author identity.
6. Confirm all three figures display correctly in the portal-generated PDF.
7. Confirm Supporting Information is attached.
8. Confirm anonymous data/code archive is accessible to reviewers/editors.
9. Confirm the portal PDF preserves line numbers and equations.
10. Read the generated PDF once from title through Figure Legends.
11. Submit only after the generated PDF matches the frozen V4.5 claim stack.

## Stop rule

Scientific analysis is frozen.

Do not reopen bird or mule-deer analyses for portal preparation.

Any remaining change should be limited to:
- author metadata;
- journal-format conversion;
- typographic correction;
- portal-generated rendering defects;
- a newly identified substantive validity error.

Current state:
**READY_FOR_AUTHOR_METADATA_AND_EDITORIAL_MANAGER_UPLOAD**
