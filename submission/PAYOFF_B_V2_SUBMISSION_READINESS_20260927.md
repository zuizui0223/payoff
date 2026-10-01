# PAYOFF-B V2 submission readiness

Frozen: **2026-09-27**  
Updated: **2026-10-01**

## Current state

PAYOFF-B Paper 2 has one canonical source:

`manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md`

V1 is frozen provenance only.

The current first-shot route remains:

```text
Global Ecology and Biogeography
Research Article
```

## 1. PREOUTCOME science package — READY

The canonical V2 GEB package has passed all hard gates.

```text
structured abstract = 283 words
main body = 4,902 words
references = 25
display pieces = 7
keywords = 8
running title = 38 characters
identity leaks = 0
internal tokens = 0
package files = 17
```

Frozen package:

```text
workflow run = 36807276298 (attempt 1)
artifact = 11138366353
artifact digest =
5ad4ca0b5be5c9b888d71385d2a7e05f079a09026b45f50c55cfbf1fc5d4e3c3

validated head =
fb03cec738558b2fd8800a60c5d80c3ae609c237

inner deterministic ZIP SHA256 =
048e234b69363800d17de98401d288d78913bc994d130024ad9310d1db6557a1
```

Deterministic reproduction is enforced inside the successful workflow by
building the package twice and requiring identical inner ZIP hashes. The final
claim-ceiling package therefore passed the deterministic archive gate on the
same validated head.

## 2. Postoutcome V2 pipeline — ACCESS_BLOCKED submission state frozen

PR #178 routes the real registered Aikens result only into canonical V2.

The pipeline supports four scientific result classes:

- PASS;
- FAIL_WRONG_DIRECTION;
- FAIL_INSUFFICIENT_SUPPORT;
- NOT_ESTIMABLE.

It also supports a fifth **external-access render state**, `ACCESS_BLOCKED`.
This is not a scientific result class. It is now explicitly activated for the
current submission route after repeated credential-only preflight confirmed
that the frozen authenticated MODIS source route is unavailable. It cannot be
relabeled as NOT_ESTIMABLE, and future authenticated execution remains
permitted under the original preregistration.

For every class, automated tests require:

```text
blinded main text = unchanged
seven main figures = unchanged
registered result = Supporting Information only
retuning = forbidden
```

Validated CI:

```text
V2 package CI = 36312188417 — success
environment CI = 36312188377 — success
full repository CI = 36312188416 — success
```

Thus the postoutcome pipeline is **ACCESS_BLOCKED_STATE_FROZEN** for the
current submission route. The four scientific result classes remain available
for future authenticated execution without changing the registered contract.

## 2.5 Anonymous reviewer archive — READY, delivery pending

A deterministic PREOUTCOME reviewer archive has been built from the canonical
claim-ceiling V2 source.

```text
workflow run = 36807276290
artifact = 11137374088
artifact digest =
4b27f0502913bf3dd665303cc8b3b3821852912c15ffba09b5917f61b3af6c66

validated head =
fb03cec738558b2fd8800a60c5d80c3ae609c237

inner reviewer ZIP SHA256 =
95b815a62b024b3a0a3210552bc1e61f0eb3523dc6702bc567037553b797b294

files = 78
Python source closure = 28
figures = 7
identity scan = PASS
raw empirical data redistributed = false
deterministic reproduction = PASS_IN_WORKFLOW_TEST
```

The archive contains the blinded manuscript, Supporting Information, exact
theory sources, frozen derived receipts and the code closure needed to audit
the reported analyses. Raw source datasets with separate access terms are not
silently redistributed.

The archive builder also supports the frozen postoutcome result classes. The
current ACCESS_BLOCKED outcome archive was generated from the same frozen
submission-state receipt:

```text
source-access-limited reviewer ZIP SHA256 =
15678fd57b3865fb099e80c265e03ef67315afb7a12eea14018b9f76e157062c

workflow run = 36807276328
artifact = 11138336737
artifact digest =
ebefd85ebd8ef38288e3bad093f33d7235f9022ca1fbffdd8a468efdf9c174b4

deterministic reproduction = PASS
```

The remaining reviewer-archive task is therefore **delivery**, not construction:
upload the ACCESS_BLOCKED ZIP through the journal review portal or provide a
stable anonymous link.

## 3. Aikens execution state — ACCESS_BLOCKED frozen for submission

The scientific contract is frozen and the outcome is still unopened.

A fresh credential-only preflight was rerun on 2026-09-28:

```text
workflow run = 36372973062
artifact = 10950280495
status = NOT_CONFIGURED
credential route = none
credential values recorded = false
network submission performed = false
environmental values opened = false
lambda outcome opened = false
```

The current submission decision is now frozen as:

```text
Aikens execution state = ACCESS_BLOCKED
scientific result = unavailable
environmental values opened = false
lambda outcome opened = false
substitute analysis used = false
author decision = SUBMIT_WITH_ACCESS_BLOCKED
future authenticated execution = permitted
original preregistration = remains binding
```

The deterministic source-access-limited submission package was built in
workflow `36807276328` from head
`fb03cec738558b2fd8800a60c5d80c3ae609c237`.

```text
artifact = 11138336737
artifact digest =
ebefd85ebd8ef38288e3bad093f33d7235f9022ca1fbffdd8a468efdf9c174b4

GEB inner ZIP SHA256 =
3b0690ea7e2b914454f1aca132835bdb800c659b2e12918ec1c5faee4ca560f0

outcome reviewer ZIP SHA256 =
15678fd57b3865fb099e80c265e03ef67315afb7a12eea14018b9f76e157062c

deterministic inner archives = PASS
```

If authenticated access later becomes available, the already-frozen AppEEARS /
V061 / fixed-24 h workflow may still be executed and classified into one of the
four scientific result classes. That future execution is no longer required
for the present submission route.

## 3.5 Journal portal files — READY FOR AUTHOR METADATA

The journal-facing editable files were rendered and QA-checked from the same
frozen science state.

```text
workflow run = 36807276327
artifact = 11138137692
artifact digest =
b76da056019b77827722f5cd0295cfced7cb711837f16364a72442ef62bce428

validated head =
fb03cec738558b2fd8800a60c5d80c3ae609c237

main manuscript DOCX SHA256 =
84fe857e8f03d6306f3d6cc0292aa09c7effbc54621648e138e1d98e502a0fb5

main review PDF SHA256 =
b461d5cd4df7e9be76af75e15dc363b2d13a8eb5925d0da02820f42b216204c6

Supporting Information DOCX SHA256 =
b3648cfd8877501212cab7c10e68a505efc4932b7f78322b210051b709a8d97c

title-page DOCX SHA256 =
0dde8cd6751f038095f93ab463ef61d16f3b004923d92f52d5a0c38dc7396a4b

cover-letter PDF SHA256 =
0cfdb5d79a30b0c1ed90e1323db64b55b8c6fcf1b83454a4292ee35962d4b8da

main manuscript pages = 28
cover letter pages = 1
title page pages = 2
Supporting Information pages = 4
embedded main figures = 7
line numbers = true
internal editor-token scan = PASS
rendered visual QA = PASS
```

The portal artifact contains the editable blinded main manuscript, editable
Supporting Information, editable title page, one-page cover-letter PDF and
seven separate vector figure PDFs. Author-controlled metadata remain
placeholders by design.

## 4. Final journal upload — SCIENCE-CLOSED, PORTAL INPUTS REMAIN

The current science state is closed for submission and the generated portal
files have passed machine and visual QA. External submission still requires:

1. delivery of the anonymous reviewer archive through the journal portal or a
   stable anonymous link;
2. author list, affiliations, ORCID and corresponding-author metadata;
3. funding, conflict-of-interest, acknowledgements, contribution and required
   AI-use declarations;
4. upload of the validated files and completion of the journal form.

The current manuscript now explicitly states that photoperiodic/endogenous migration programmes are a non-exclusive alternative explanation for the E6 migration-distance gradient, and that the pairwise deadline-difference mechanism has not yet been directly tested in a natural interacting pair.

The interaction-response bridge now has two independent published contexts. Burgess et al. show consumer–resource response asymmetry generating mismatch, while Samplonius et al. (2018) show stronger resident-tit temperature sensitivity than migratory flycatchers and a 0.94 d/decade widening of their laying-date interval. Neither measures D2-D1 or the q1<q<=q2 information-use window.

The structured abstract is now intentionally limited to three empirical layers:
predictive connectivity, migration-distance responsiveness, and the
Samplonius et al. 0.94 d/decade resident–migrant laying-date divergence. The
wigeon null remains an important boundary test in Results/Figure 5 but is not
listed in the abstract.

## Scientific ceiling

Current natural evidence does **not** demonstrate the full
information-loss → coordination-collapse → information-recovery → persistent
network-state sequence.

The recovery-failure and rescue-leverage conclusions are theoretical
predictions of the declared games.

Natural evidence currently provides:

- pooled, dependence-sensitive support for predictive connectivity across
  migratory birds;
- E6 cross-system information-distance triangulation: the 944-effect
  migration meta-regression gives an adjusted long-minus-short response of
  +0.421 d/°C (95% CI +0.121 to +0.722, p=0.0077; 28/28 leave-one-study-out
  fits positive), while the independent 1,763-species plant–pollinator
  benchmark reproduces all five published group means. This is not a causal
  taxon ranking or a new two-source cross-taxon meta-analysis;
- a decision-time cue-availability anchor from the pied-flycatcher experiment;
- a registered wigeon predictive-connectivity controller null;
- a negative long-term cue-driver decline–recovery gate;
- a second preregistered same-system cue–resource gate that returned
  NO_CUE_RESOURCE_REVERSAL before resident–migrant history was opened.

That boundary must remain explicit in the final abstract, cover letter and
Discussion.
