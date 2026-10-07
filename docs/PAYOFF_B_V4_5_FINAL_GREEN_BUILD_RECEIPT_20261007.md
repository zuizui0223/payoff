# PAYOFF-B V4.5 final green-build receipt — 2026-10-07

Status: **SCIENCE + REVIEW PACKAGE GREEN**

Canonical science SHA:
**6d826796099941af65d16487b86511151005442d**

## Repository-wide validation

### Standard test suite

Workflow:
- name: `test`
- run: **37562979898**
- SHA: **6d826796099941af65d16487b86511151005442d**
- conclusion: **SUCCESS**

### Environment matrix

Workflow:
- name: `test-environments`
- run: **37562979982**
- SHA: **6d826796099941af65d16487b86511151005442d**
- conclusion: **SUCCESS**

Earlier failures on 2026-10-07 were build/test infrastructure issues introduced
by the new submission tests:
- dynamic import helpers were not registered in `sys.modules`;
- the empirical-extras environment did not install `python-docx`.

Both were repaired. No ecological or statistical result was changed to make the
repository-wide tests pass.

## Anonymous reviewer package

Workflow:
- run: **37562980001**
- SHA: **6d826796099941af65d16487b86511151005442d**
- conclusion: **SUCCESS**

Artifact:
- id: **11456869372**
- digest:
  **sha256:4e790b88d90955a6318f291e8b67c9a6fcb4ce15aaecbce876b4f4f6f356823e**

The package acceptance tests enforce:
- abstract <= 200 words;
- main text <= 7,500 words;
- 1–6 keywords;
- short title <= 40 characters;
- three figure callouts;
- three legends <= 100 words;
- absence of repository-internal version labels in the anonymous manuscript;
- deterministic package ZIP.

## Anonymous review DOCX

Workflow:
- run: **37562979913**
- SHA: **6d826796099941af65d16487b86511151005442d**
- conclusion: **SUCCESS**

Artifact:
- id: **11457418624**
- digest:
  **sha256:29d51b8a0d6038190de76603cf7ccf55261b23d19da3ebb6c74d4a49a4ae5f9a**

The DOCX was downloaded and rendered independently with LibreOffice after the
workflow completed.

Visual QA:
- rendered pages: **30**;
- title page present;
- Abstract begins on its own page;
- main text begins on its own page;
- continuous line numbering visible;
- page numbering visible;
- equations readable;
- no obvious page overflow or clipping;
- Literature Cited followed by Figure Legends;
- no orphan blank legend page;
- final one-word wording change (`rigid` -> `limited`) did not alter page
  count or visible layout.

## Anonymous reproducibility bundle

Workflow:
- run: **37562808347**
- SHA: **399f5b0729b1499650a36d5b1f8c50f918e8351e**
- conclusion: **SUCCESS**

Artifact:
- id: **11456844175**
- digest:
  **sha256:b190078595ee4ba4f026f600a1b8d26b068c7e21edb5a6f8f3924ee8e618975d**

The difference from the canonical science SHA consists only of subsequent test
helper / CI repairs and the final wording change. No reproducibility-bundle
analysis source or frozen figure data changed after this successful build.

## Main figures

Frozen figure receipt remains:
- workflow run: **37407791647**
- artifact: **11387890969**
- digest:
  **sha256:499850ff5d865c50bb3e916f5ce17d90b69652ba17b012a16d1e201f67a038f2**

No figure data changed after the frozen figure build.

## Current journal-facing scientific boundary

Central architecture:

```text
environmental forecastability
-> organismal information access
-> retained actionability
-> correction
```

Bird data estimate:
- environmental forecastability;
- population timing;
- a restricted population-level stage transformation.

Bird data do not directly estimate:
- cue perception;
- organismal information value;
- individual actionability;
- individual feedback gain.

Mule deer provide the independent individual-level correction anchor; the
compensation phenomenon remains explicitly attributed to prior work.

## Freeze rule

The current American Naturalist science package is frozen.

Do not reopen analysis unless a substantive validity error is identified.

Permitted changes:
- author metadata;
- affiliations;
- funding / COI / contributions;
- preprint declaration;
- typographic repair;
- journal-portal rendering repair.

Current state:
**GREEN_BUILD_READY_FOR_EDITORIAL_MANAGER**
