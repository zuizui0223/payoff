# PAYOFF-B V4.5 final review-DOCX receipt — 2026-10-07

Status: **PASS — REVIEW DOCX READY**

## Workflow provenance

Workflow:
- run **37559117694**
- head **2f2726a157c83eb0bfcf979bbfcdb6b149796989**

Artifact:
- id **11456151706**
- name **payoff-b-v45-amn-docx**
- digest **sha256:422a963907a36715536f170bcad647bce4b7546786dd2dfdf38920da4c4b0f21**

Canonical manuscript used by the build:
- scientific manuscript head **d92c6135f58c2330a6b3476600d57b7a8b515abe**
- title: **Seasonal tracking depends on information access and opportunities for correction**

## Automated acceptance

The DOCX workflow passed its structural tests.

Verified:
- anonymous manuscript contains no internal project/version labels;
- title present;
- short title present and <=40 characters;
- six keywords or fewer;
- title-page word count is within the Major Article limit;
- Abstract present;
- Methods precede Natural evidence;
- Figure 1–3 callouts present;
- Figure Legends present;
- continuous line-numbering XML present;
- page-number field present;
- Normal style double spaced;
- raw LaTeX control sequences do not leak into the review document.

## Visual QA

The final DOCX was rendered with the project DOCX renderer and inspected page
by page.

Rendered pages:
- **30**

Visual inspection:
- pages **1–30 all inspected individually**;
- title page readable;
- Abstract begins on its own page;
- main text begins on a new page;
- continuous line numbers visible;
- page numbers visible;
- no clipping;
- no overlapping text;
- no missing section headings;
- displayed equations are readable in reviewer-facing Unicode/plain-text form;
- Literature Cited is legible;
- Figure Legends follow Literature Cited;
- the previous orphan two-line page was eliminated;
- final Figure 3 legend fits cleanly on page 30.

## Review-document metadata

Current package-manifest statistics:
- Abstract: **167 words**
- main text before Literature Cited: **6385 words**
- main figures: **3**
- keywords: **6**
- short title: **Information access and correction**

These are inside the current American Naturalist initial-submission limits used
for the build.

## Claim boundary preserved

The review document retains the current V4.5 interpretation:

```text
environmental forecastability
-> organismal information access
-> retained actionability
-> downstream correction
-> realized seasonal timing
```

The bird analyses are not presented as direct evidence that birds perceived the
reconstructed source variable. Mule-deer compensation is labelled as a
published prior phenomenon and used only as an independent individual-level
correction anchor.

## Decision

**REVIEW_DOCX = PASS**

This closes the last machine/visual build gate for the current V4.5 American
Naturalist route.

Remaining actions are portal/human metadata only:
- author list and affiliations;
- corresponding-author details;
- funding / conflicts / author contributions;
- any preprint declaration;
- final reviewer suggestions if requested;
- upload to Editorial Manager.

Do not reopen the scientific analyses unless a substantive validity defect is
identified.
