# PAYOFF-B Paper 2 — GEB final upload map

Checked against the current **Global Ecology and Biogeography** Author Guidelines on **2026-10-01**.

Journal: **Global Ecology and Biogeography**  
Article type: **Research Article**  
Canonical title: **Information deadlines can desynchronize seasonal interactions under environmental change**  
Science state: **closed**  
Current submission route: **source-access limitation recorded in Supporting Information; no scientific result inferred from that limitation**

## 1. What GEB currently requires at initial submission

The journal uses free-format submission, but the current instructions still require:

- an **editable main manuscript**;
- figures embedded in the main text for review;
- Supporting Information as a **separate file**;
- a **separate title page** with identifying information;
- a **cover letter uploaded separately as PDF**;
- a cover-letter paragraph of **<250 words** explaining why the paper is of interest to GEB readers;
- a structured abstract of **<=300 words** with:
  Aim, Location, Time period, Major taxa studied, Methods, Results, Main conclusions;
- Research Articles typically around **5,000 words in the main body**, about 50 references and 6–8 display pieces.

Source:
https://onlinelibrary.wiley.com/page/journal/14668238/homepage/forauthors.html

## 2. Upload these files

### A. Main Document — upload

Use:

`GEB_MAIN_MANUSCRIPT.docx`

Role:

- blinded editable main document;
- title + running title;
- structured abstract + keywords;
- Introduction / Theory / Results / Discussion / Conclusion;
- References;
- Data and Code Availability Statement;
- seven figure legends;
- seven figures embedded at the end;
- continuous line numbers.

Validated QA:

```text
main_body_words = 4902
abstract_words = 283
references = 25
embedded_figures = 7
rendered_review_pages = 28
line_numbers = true
internal_editor_token_hits = 0
deinternalization_prose_artifacts = 0
```

File SHA256:

`84fe857e8f03d6306f3d6cc0292aa09c7effbc54621648e138e1d98e502a0fb5`

A rendered review-only check copy also exists:

`GEB_MAIN_MANUSCRIPT_REVIEW.pdf`

Do **not** substitute that PDF for the editable Main Document unless the portal specifically requests an additional review PDF.

### B. Supporting Information — upload

Use:

`GEB_SUPPORTING_INFORMATION.docx`

Role:

- outcome-rendered Supporting Information;
- records that the registered industrial-development analysis was not executed because authenticated source access was unavailable;
- does not classify that access limitation as a scientific null or NOT_ESTIMABLE result;
- retains the frozen claim boundary.

Rendered QA:

```text
pages = 4
PREOUTCOME leakage = 0
pending-language leakage = 0
```

File SHA256:

`b3648cfd8877501212cab7c10e68a505efc4932b7f78322b210051b709a8d97c`

### C. Title Page — upload after author completion

Use:

`GEB_TITLE_PAGE.docx`

Current state:

`READY_FOR_AUTHOR_METADATA`

Fill before upload:

- complete author list;
- affiliations where the work was carried out;
- exactly one corresponding author;
- ORCID information requested by the portal;
- acknowledgements;
- funding;
- competing interests;
- author contributions;
- any present-address footnote if applicable;
- journal-required generative-AI disclosure wording.

Current rendered QA:

```text
pages = 2
internal project labels = 0
```

File SHA256 before author metadata:

`0dde8cd6751f038095f93ab463ef61d16f3b004923d92f52d5a0c38dc7396a4b`

**The SHA will legitimately change after author metadata are entered.**

### D. Cover Letter — upload as separate PDF

Use:

`GEB_COVER_LETTER.pdf`

Validated state:

```text
pages = 1
GEB-interest paragraph ~= 202 words
internal project labels = 0
source-access machine label in cover = absent
```

File SHA256:

`0cfdb5d79a30b0c1ed90e1323db64b55b8c6fcf1b83454a4292ee35962d4b8da`

Before upload, replace the author-controlled placeholders:

- originality / author-approval / not-under-consideration statement;
- suggested reviewers and/or handling editors, if supplied;
- brief reason for each suggestion;
- no-conflict-of-interest statement for each suggested reviewer/editor;
- corresponding-author sign-off.

GEB currently encourages reviewer / handling-editor suggestions but warns that suggestions with clear conflicts of interest may be rejected.

### E. Anonymous code/data reviewer archive — deliver

Current reviewer artifact:

```text
workflow_run = 36807276290
artifact_id = 11137374088
artifact_sha256 =
4b27f0502913bf3dd665303cc8b3b3821852912c15ffba09b5917f61b3af6c66

inner_archive_sha256 =
95b815a62b024b3a0a3210552bc1e61f0eb3523dc6702bc567037553b797b294

files = 78
python_source_files = 28
figures = 7
identity_scan = PASS
raw_empirical_data_redistributed = false
```

Delivery options:

1. upload through the journal review portal if an appropriate anonymous
   supplementary/reviewer-file designation is available; or
2. provide a stable anonymous review link.

Do not use a normal identity-bearing GitHub repository URL as the sole blinded
review route.

## 3. Seven vector figure PDFs

The portal artifact also contains:

```text
FIGURE_1.pdf
FIGURE_2.pdf
FIGURE_3.pdf
FIGURE_4.pdf
FIGURE_5.pdf
FIGURE_6.pdf
FIGURE_7.pdf
```

For **initial review**, the current GEB instructions say figures should be
embedded in the main text. Therefore these separate vector PDFs are normally
**backup / later-production files**, not required initial uploads unless the
live portal explicitly requests separate figure files.

If separate files are requested, use the vector PDFs.

## 4. Current machine-validated package provenance

```text
science_commit =
d3b58c3d1fa036a59d4abe6b7d167d3f4a31f15d

final_package_content_head =
fb03cec738558b2fd8800a60c5d80c3ae609c237

PREOUTCOME_package_run =
36807276298

PREOUTCOME_artifact =
11138366353

PREOUTCOME_inner_zip_sha256 =
048e234b69363800d17de98401d288d78913bc994d130024ad9310d1db6557a1

science_closed_package_run =
36807276328

science_closed_package_artifact =
11138336737

reviewer_archive_run =
36807276290

reviewer_archive_artifact =
11137374088

portal_files_run =
36807276327

portal_files_artifact =
11138137692

portal_files_artifact_sha256 =
b76da056019b77827722f5cd0295cfced7cb711837f16364a72442ef62bce428
```

The current main branch includes the final CI-regression alignment after package generation.
That later change affects only a regression assertion and does not alter any
submission artifact bytes.

## 5. Final human-controlled checklist

Do not reopen the science or figures for these tasks.

```text
[ ] author names finalized
[ ] affiliations finalized
[ ] exactly one corresponding author selected
[ ] ORCID values entered
[ ] acknowledgements finalized
[ ] funding statement finalized
[ ] competing-interests statement finalized
[ ] author contributions finalized
[ ] AI-use disclosure wording approved
[ ] title-page placeholders removed
[ ] cover-letter author placeholders removed
[ ] reviewer/editor suggestions conflict-checked, if supplied
[ ] anonymous reviewer archive uploaded or anonymous link supplied
[ ] title in portal matches manuscript exactly
[ ] article type = Research Article
[ ] main DOCX uploaded as Main Document
[ ] Supporting Information uploaded separately
[ ] title page uploaded separately
[ ] cover letter uploaded separately as PDF
[ ] generated portal proof checked before pressing Submit
```

## 6. Stop rule

If a live-portal field conflicts with this handoff, resolve the **portal field**
without changing scientific claims unless the journal explicitly requests a
scientific revision.

At this stage, author metadata, declarations, anonymous archive delivery and
portal entry are **external submission tasks**, not reasons to retune the
manuscript.
