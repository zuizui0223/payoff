# GEB integrated tracking ecology — PREOUTCOME package audit

Audited: **2026-09-25**

Status: **PASS — GEB Research Article overlay is internally ready in PREOUTCOME state**

## Journal routing

```text
FIRST_SHOT = Global Ecology and Biogeography
ARTICLE_TYPE = Research Article
SCIENCE_SOURCE = manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md
SCIENCE_RETUNING = forbidden
```

The GEB overlay is a journal-facing structural transformation only. It does not
recalculate any scientific result.

## Machine validation

### GEB overlay audit

```text
workflow = GEB integrated PREOUTCOME overlay
run = 36109434346
head = d532366aea1dc112dbb876713ea56e0870db4186
status = PASS
```

Audited GEB-facing metrics:

```text
structured_abstract_words = 222
main_body_words = 3690
references = 21
uncited_references = 0
display_pieces = 6
keywords = 8
running_title_chars = 28
identity_leaks = 0
internal_submission_tokens = 0
aikens_marker_pairs = 4 / 4
```

All GEB PREOUTCOME hard gates pass:

- seven required structured-abstract headings are present;
- abstract <=300 words;
- main body <=5,000 words;
- references <=50 and all cited;
- exactly six display pieces;
- 6–10 alphabetized keywords;
- running title <40 characters;
- blinded manuscript contains no author/repository/email leak;
- internal Status / Figure architecture / Claim ceiling tokens are absent;
- the prior-art boundary is moved into Discussion as
  “Relationship to existing literature”;
- the stable anonymous reviewer-link placeholder is present;
- Aikens remains outcome-blind with exactly one marker pair in Abstract,
  Results, Discussion and Conclusion.

### Deterministic GEB working package

```text
workflow = GEB integrated PREOUTCOME package
run = 36109813368
head = bd4467fec7a5f70f13005cf6446a8e65f9f49d6f
status = PASS
artifact = payoff-b-geb-integrated-preoutcome-package
artifact_id = 10852587229
artifact_sha256 = d5ac9123d9d90b4216d37b02b42db543f4d93443f254cc7fb3c035653d51580d
```

Inner deterministic archive:

```text
file = GEB_INTEGRATED_PREOUTCOME_PACKAGE.zip
bytes = 39566
sha256 = 5a7743af95734532b6f3515c09ea3493584b9f9617dda3b949962c078e8469cf
package_manifest_sha256 = ec136c5c9cb34f4effd3ea44743a0433817019aeec7bf02756609ec34b2e092e
geb_audit_sha256 = 84942f8354530cbfd57c07f37eec941d9148ab6d61b0748db9ec4cbaf3bbbc37
blinded_main_sha256 = 42d1b08a44034c05f843cc42ac1ac5e40cde2ff99199416b9688ce37ff0bd1a9
supporting_information_sha256 = 7f6f0a0dfd1d8f115d12707b738e0570a8e8a7129f2e15038fdb56945f9dc3ed
files = 15
figures = 6
```

Full repository CI on the deterministic-package head:

```text
workflow = test
run = 36109813351
status = PASS
```

The determinism test rebuilds the package twice under different temporary
directories and requires identical ZIP SHA256 values.

## GEB figure overlay

The six GEB figures are format overlays of the canonical integrated figures.
Only journal-facing panel labels are changed to lower-case parenthetical form.

The GEB figure manifest records:

```text
scientific_result_changed = false
format_change_only = true for Figures 1–6
```

Canonical-to-GEB source hashes remain explicitly paired in
`GEB_INTEGRATED_FIGURE_MANIFEST.json`.

## Package contents

The deterministic GEB package contains:

- blinded GEB PREOUTCOME manuscript;
- machine GEB audit;
- integrated Supporting Information;
- GEB title-page template;
- GEB cover-letter overlay;
- GEB data/code template;
- GEB portal handoff;
- journal-targeting memo;
- six GEB-formatted SVG figures;
- GEB figure manifest.

## Remaining blockers

This audit does **not** declare the paper final-submission eligible.

Remaining blockers are exactly:

1. registered Aikens fixed-24 h lambda adjudication;
2. anonymous stable reviewer archive link;
3. author-controlled title-page and declaration metadata.

After Aikens adjudication, the existing outcome-blind renderer must rebuild the
manuscript and Figure 6 before final GEB portal preparation. No post-outcome
retuning of the broad-bird result, direct-system synthesis, or headline is
licensed.
