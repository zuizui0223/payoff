# PAYOFF-B V2 GEB PREOUTCOME package audit

Audited: **2026-09-27**

Status: **PASS — canonical V2 PREOUTCOME working package ready**

## Canonical source

`manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md`

V1 status:

`FROZEN_PROVENANCE_ONLY`

The package is rebuilt from the information-coordination V2 source and does not
reuse the superseded temporal-buffering V1 GEB overlay.

## Verified GEB-facing metrics

```text
structured_abstract_words = 246
main_body_words = 4167
references = 13
display_pieces = 7
keywords = 8
running_title_chars = 38
internal_token_hits = 0
email_hits = 0
expected_citations_present = PASS
```

Hard gates:

```text
structured_abstract = PASS
abstract <= 300 = PASS
keywords 6..10 = PASS
keywords alphabetical = PASS
running title < 40 chars = PASS
main body <= 5000 = PASS
references 1..50 = PASS
display pieces = 7 = PASS
anonymous/internal-token scan = PASS
citation/reference presence = PASS
Aikens placeholder absent from blinded main text = PASS
```

The blinded overlay uses the current GEB Research Article structure: Aim,
Location, Time period, Major taxa studied, Methods, Results and Main
conclusions.

## Package contents

The deterministic package contains:

- blinded V2 main manuscript;
- package audit JSON;
- PREOUTCOME Supporting Information;
- registered industrial-development Supplement pending marker;
- separate V2 title-page template;
- V2 cover-letter template;
- V2 data/code statement;
- V2 portal handoff;
- seven deterministic SVG figures;
- figure manifest.

Internal V1/V2 provenance documents are deliberately excluded from the journal-facing ZIP so package hashes do not depend on publication-state bookkeeping.

Figure panels in the V2 renderer use lower-case journal-style panel labels.

## Frozen build provenance

```text
workflow_run = 36313076476
validated_head = 3524f28d00299c5fc5990c8b64154c9057954e2d
workflow_conclusion = success

artifact_id = 10930130067
artifact_name = payoff-b-v2-geb-preoutcome-package
artifact_sha256 =
c47efff79a125945361d4a7f576141d70df6cbd30512556337be1c3f62c693c6

inner_zip = PAYOFF_B_V2_GEB_PREOUTCOME_PACKAGE.zip
inner_zip_sha256 =
cf1ada3fb67b603b972f6e3994f439292b3ed3b18f17d2f0c3407c0bc90288cd
```

## Scientific boundary

The package does not open or infer the registered industrial-development
phase-retention result.

That result is removed from the blinded main text and reserved as a pending
Supporting Information gate. Its eventual sign is not permitted to change:

- the title;
- the structured abstract spine;
- the information-deadline theorem;
- the perfect-information recovery-failure result;
- the broad-bird/flycatcher/wigeon claim boundaries.

No natural interaction network is claimed to have demonstrated the full
degradation–recovery hysteresis sequence, and no natural singleton rescue
species is claimed to have been identified.

## Final-submission state

```text
CURRENT_V2_PREOUTCOME_PACKAGE = READY
FINAL_SUBMISSION_ELIGIBLE = false
```

Remaining blockers:

1. freeze the registered industrial-development phase-retention result;
2. supply an anonymous stable reviewer archive link;
3. populate author-controlled title-page and declaration metadata;
4. regenerate and re-audit the final V2 package.

The package is therefore ready for internal scientific review and for immediate
post-result regeneration, but not for journal upload yet.
