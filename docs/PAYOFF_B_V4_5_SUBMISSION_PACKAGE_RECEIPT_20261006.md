# PAYOFF-B V4.5 submission-package receipt — 2026-10-06

Status: **ANONYMOUS REVIEW PACKAGE + REPRODUCIBILITY PACKAGE PASS**

## Anonymous reviewer package

Workflow:
- run **37470823411**
- head **492432324d3bc4ef797a45ab896e16f7c445da68**

Artifact:
- id **11418146845**
- name **payoff-b-v45-amn-package**
- artifact digest
  **sha256:df1d8dfb35263d459d273a1674f268106ecc59a3438a5a3861deb1ffd0ea7940**

The final inner reviewer ZIP contains only:
- anonymous manuscript;
- Supporting Information;
- figure legends;
- figure 1;
- figure 2;
- figure 3;
- package manifest.

It contains no title page, author information or internal project/version label.

Local artifact inspection confirmed:
- no PAYOFF-B / V2–V8 / post-freeze / rollback strings;
- no submitter account name;
- no submitter personal name variants;
- figure legends are below the journal's 100-word guidance;
- figures use generic reviewer-facing filenames.

Package-manifest manuscript statistics:
- abstract: **165 words**
- main text before Literature Cited: **6385 words**
- title: **Seasonal tracking depends on information access and opportunities for correction**

## Anonymous reproducibility package

Workflow:
- run **37469126486**
- head **1f300e2736fb8622039db42e74fd4ac506402837**

Artifact:
- id **11416773256**
- name **payoff-b-v45-reproducibility**
- artifact digest
  **sha256:fe51583e370644fdd1bd067977fbf2e8e31b8125f180691151790474a75c37b2**

The archive contains manuscript-specific:
- bird primary and diagnostic R scripts;
- mule-deer reanalysis scripts;
- relevant contracts;
- frozen figure-data manifest;
- selected tests;
- anonymous review README.

Identity scan:
**PASS — no submitter-identifying strings detected in the final inner bundle.**

The bundle points reviewers to the two previously published public source
datasets and preserves the preregistered/posthoc/prior-art evidence classes.

## Main figures

Frozen separately in:
`docs/PAYOFF_B_V4_5_MAIN_FIGURE_RECEIPT_20261006.md`

Main-figure workflow:
- run **37407791647**
- artifact **11387890969**
- digest
  **sha256:499850ff5d865c50bb3e916f5ce17d90b69652ba17b012a16d1e201f67a038f2**

## DOCX

A prior review DOCX build passed, but visual QA found an incorrect title-page
word count caused by an escaped-whitespace regex in the DOCX builder.

That artifact is **superseded and must not be submitted**.

The builder was fixed in commit:
**ae94d01e488a9fafff14a964c342aece98cd5e93**

A new DOCX build is pending final CI/render/visual QA.

## Submission decision

Scientific analysis is frozen under the V4.5 stop rule.

The only open deliverable gate is:
**corrected anonymous review DOCX render-and-visual-QA.**
