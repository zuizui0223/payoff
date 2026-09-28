# PAYOFF-B V2 GEB PREOUTCOME package audit

Audited: **2026-09-28**

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
main_body_words = 4298
references = 14
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
- V2 declarations template;
- seven deterministic SVG figures;
- figure manifest.

Internal V1/V2 provenance documents are deliberately excluded from the journal-facing ZIP so package hashes do not depend on publication-state bookkeeping.

Figure panels in the V2 renderer use lower-case journal-style panel labels.

## Frozen build provenance

```text
workflow_run = 36370295430
workflow_run_attempt = 1
validated_head = a518a4a4ca6bab3b05b3c1f87d2055a332c5ed08
workflow_conclusion = success

artifact_id = 10949330110
artifact_name = payoff-b-v2-geb-preoutcome-package
artifact_sha256 =
0146afe2d091f951c7d5b9dd6b0afab853c70f977fce51729faf4fbd768127fb

inner_zip = PAYOFF_B_V2_GEB_PREOUTCOME_PACKAGE.zip
inner_zip_sha256 =
262c6f1d5fdee798db5c2a8bc60b81ef05f480da70eb9de3d93de67de49c585f
```

Deterministic reproduction check:

```text
reproduction_workflow_run = 36370295430
reproduction_run_attempt = 2
reproduction_head = a518a4a4ca6bab3b05b3c1f87d2055a332c5ed08
reproduction_artifact_id = 10949105921
reproduction_artifact_sha256 =
94527f1d47d6ad544e6c79ade914960922e198262dbdf2bf70a4fd09b3d72ca3
reproduction_inner_zip_sha256 =
262c6f1d5fdee798db5c2a8bc60b81ef05f480da70eb9de3d93de67de49c585f
deterministic_inner_archive = PASS
package_file_count = 17
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
species is claimed to have been identified. The preregistered Hoge Veluwe
cue–resource recovery gate returned `NO_CUE_RESOURCE_REVERSAL`, so its
resident–migrant history gate remained unopened.

## Final-submission state

```text
CURRENT_V2_PREOUTCOME_PACKAGE = READY
FINAL_SUBMISSION_ELIGIBLE = false
```

Remaining blockers:

1. configure AppEEARS/Earthdata credentials and freeze the registered
   industrial-development phase-retention result;
2. deliver the already-built anonymous reviewer archive through the journal
   portal or a stable anonymous review link;
3. populate author-controlled title-page and declaration metadata;
4. perform final human review of the outcome-rendered package and portal metadata.

The package is therefore ready for internal scientific review and for immediate
post-result regeneration, but not for journal upload yet.
