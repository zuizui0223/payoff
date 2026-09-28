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
structured_abstract_words = 244
main_body_words = 4761
references = 18
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

Figure panels in the V2 renderer use lower-case journal-style panel labels. Figure 5 integrates the E6 migration-distance and local benchmark evidence. The manuscript explicitly retains photoperiodic/endogenous timing as a non-exclusive alternative and states that pairwise deadline differences remain untested in nature.

## Frozen build provenance

```text
workflow_run = 36405110540
workflow_run_attempt = 1
validated_head = 7bcaaef50407f06a0624ec7e6931decffbfc664d
workflow_conclusion = success

artifact_id = 10962346030
artifact_name = payoff-b-v2-geb-preoutcome-package
artifact_sha256 =
66919dc4bb327c601e48c0545f240789f56b9f03dcfe2ff947753d4cc24642aa

inner_zip = PAYOFF_B_V2_GEB_PREOUTCOME_PACKAGE.zip
inner_zip_sha256 =
6d9e2aa0a1e9628d56d5a08fa23bd50999c7f8e059488b525585a4c2631cf1d1
```

Deterministic reproduction check:

```text
reproduction_workflow_run = 36405110540
reproduction_run_attempt = 2
reproduction_head = 7bcaaef50407f06a0624ec7e6931decffbfc664d
reproduction_artifact_id = 10956526561
reproduction_artifact_sha256 =
2c3b34d786bf702447285378653fcaaf3975cbff37bccfd80c2b5f8032a3ba35
reproduction_inner_zip_sha256 =
6d9e2aa0a1e9628d56d5a08fa23bd50999c7f8e059488b525585a4c2631cf1d1
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
- the broad-bird/flycatcher/wigeon claim boundaries;
- the E6 information-distance claim boundary: no causal bird-versus-pollinator
  ranking and no new two-source cross-taxon meta-analysis.

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

The current submission route is the frozen non-scientific `ACCESS_BLOCKED`
render; authenticated Aikens execution remains permitted later under the
original preregistration but is not a present submission blocker.

Remaining blockers:

1. deliver the already-built anonymous reviewer archive through the journal
   portal or a stable anonymous review link;
2. populate author-controlled title-page and declaration metadata;
3. perform final human review of the outcome-rendered package and portal metadata.

The package is therefore scientifically closed for the current submission
route, with only portal-facing inputs remaining.
