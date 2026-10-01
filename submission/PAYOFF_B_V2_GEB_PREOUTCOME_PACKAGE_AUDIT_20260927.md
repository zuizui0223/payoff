# PAYOFF-B V2 GEB PREOUTCOME package audit

Audited: **2026-10-01**

Status: **PASS — canonical V2 PREOUTCOME working package ready**

## Canonical source

`manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md`

V1 status:

`FROZEN_PROVENANCE_ONLY`

The package is rebuilt from the information-coordination V2 source and does not
reuse the superseded temporal-buffering V1 GEB overlay.

## Verified GEB-facing metrics

```text
structured_abstract_words = 283
main_body_words = 4902
references = 25
display_pieces = 7
keywords = 8
running_title_chars = 38
internal_token_hits = 0
email_hits = 0
deinternalization_artifact_hits = 0
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
deinternalization prose audit = PASS
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

Figure panels in the V2 renderer use lower-case journal-style panel labels. The interaction-response bridge now uses two independent interaction contexts—Burgess bird–caterpillar trophic pairs and Samplonius resident–migrant cavity breeders—without changing the seven-figure set; D2-D1 and the q1<q<=q2 information-use window remain prospective. Figure 5 integrates the E6 migration-distance and local benchmark evidence. The manuscript explicitly retains photoperiodic/endogenous timing as a non-exclusive alternative and states that pairwise deadline differences remain untested in nature.

The structured abstract now foregrounds three empirical layers only: predictive
connectivity, migration-distance responsiveness and the 0.94 d/decade
resident–migrant laying-date divergence. The wigeon null remains in
Results/Figure 5 rather than competing in the abstract.

## Frozen build provenance

```text
workflow_run = 36807276298
workflow_run_attempt = 1
validated_head = fb03cec738558b2fd8800a60c5d80c3ae609c237
workflow_conclusion = success

artifact_id = 11138366353
artifact_name = payoff-b-v2-geb-preoutcome-package
artifact_sha256 =
5ad4ca0b5be5c9b888d71385d2a7e05f079a09026b45f50c55cfbf1fc5d4e3c3

inner_zip = PAYOFF_B_V2_GEB_PREOUTCOME_PACKAGE.zip
inner_zip_sha256 =
048e234b69363800d17de98401d288d78913bc994d130024ad9310d1db6557a1
```

Deterministic reproduction is checked inside the successful workflow by
`test_v2_geb_package_zip_is_deterministic`, which builds the package twice and
requires identical inner ZIP hashes.

```text
deterministic_inner_archive = PASS_IN_WORKFLOW_TEST
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

The current submission route is the frozen non-scientific source-access
limitation render; authenticated Aikens execution remains permitted later under
the original preregistration but is not a present submission blocker.

Remaining external inputs:

1. deliver the anonymous reviewer archive through the journal portal or a stable
   anonymous review link;
2. populate author-controlled title-page and declaration metadata;
3. upload the validated portal files and complete the journal form.

The package is therefore scientifically closed for the current submission
route, with only portal-facing inputs remaining.
