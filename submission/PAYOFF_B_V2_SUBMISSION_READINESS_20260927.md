# PAYOFF-B V2 submission readiness

Frozen: **2026-09-27**  
Updated: **2026-09-28**

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
structured abstract = 246 words
main body = 4,298 words
references = 14
display pieces = 7
keywords = 8
running title = 38 characters
identity leaks = 0
internal tokens = 0
package files = 17
```

Frozen package:

```text
workflow run = 36370295430 (attempt 1)
artifact = 10949330110
artifact digest =
0146afe2d091f951c7d5b9dd6b0afab853c70f977fce51729faf4fbd768127fb

inner deterministic ZIP SHA256 =
262c6f1d5fdee798db5c2a8bc60b81ef05f480da70eb9de3d93de67de49c585f
```

The declarations-inclusive package was rerun from the same frozen head in
workflow run 36370295430 (attempt 2; artifact 10949105921). The deterministic
inner ZIP remained byte-identical:

```text
262c6f1d5fdee798db5c2a8bc60b81ef05f480da70eb9de3d93de67de49c585f
```

The inner archive remained byte-identical, confirming deterministic reproduction of the claim-ceiling package.

## 2. Postoutcome V2 pipeline — READY, outcome unopened

PR #178 routes the real registered Aikens result only into canonical V2.

The pipeline supports all four registered outcomes:

- PASS;
- FAIL_WRONG_DIRECTION;
- FAIL_INSUFFICIENT_SUPPORT;
- NOT_ESTIMABLE.

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

Thus the postoutcome pipeline is **READY_UNOPENED**, not
`REBUILD_REQUIRED`.

## 2.5 Anonymous reviewer archive — READY, delivery pending

A deterministic PREOUTCOME reviewer archive has been built from the canonical
claim-ceiling V2 source.

```text
workflow run = 36370295435
artifact = 10948908201
artifact digest =
cb1a090d6d2ace3ec54f72aba0a58e4dbd3a7e1348907214879529909e66fd4e

inner reviewer ZIP SHA256 =
6e7dd4d6ac3ad953eb2368743434d3bce10f52aceeb29cb0e66bcdf4c940babf

files = 70
Python source closure = 26
figures = 7
identity scan = PASS
raw empirical data redistributed = false
reviewer archive reproduction run = 36370295435
reviewer archive reproduction artifact = 10948993094
reviewer archive deterministic inner SHA256 = 6e7dd4d6ac3ad953eb2368743434d3bce10f52aceeb29cb0e66bcdf4c940babf
```

The archive contains the blinded manuscript, Supporting Information, exact
theory sources, frozen derived receipts and the code closure needed to audit
the reported analyses. Raw source datasets with separate access terms are not
silently redistributed.

The archive builder also supports the frozen postoutcome result classes. The
remaining reviewer-archive task is therefore **delivery**, not construction:
upload the ZIP through the journal review portal or provide a stable anonymous
link.

## 3. Real Aikens execution — credentials not configured

The scientific contract is frozen and the outcome is still unopened.

A fresh credential-only preflight was run on 2026-09-27:

```text
workflow run = 36318036795
artifact = 10931233185
status = NOT_CONFIGURED
credential route = none
credential values recorded = false
network submission performed = false
environmental values opened = false
lambda outcome opened = false
```

The next execution step therefore requires external credential configuration:

```text
configure APPEEARS_TOKEN
or configure EARTHDATA_USERNAME + EARTHDATA_PASSWORD
-> rerun credential preflight
-> execute the already frozen full AppEEARS / V061 / fixed-24 h workflow
-> classify result
-> render Supporting Information only
-> generate final V2 outcome package
```

No scientific tuning is permitted at any stage.

## 4. Final journal upload — NOT YET ELIGIBLE

Even after the science result is frozen, portal upload still requires:

1. delivery of the already-built anonymous reviewer archive through the journal portal or a stable anonymous link;
2. author list, affiliations, ORCID and corresponding-author metadata;
3. funding, conflict-of-interest, acknowledgements and contribution
   declarations;
4. final human review of the generated outcome package.

## Scientific ceiling

Current natural evidence does **not** demonstrate the full
information-loss → coordination-collapse → information-recovery → persistent
network-state sequence.

The recovery-failure and rescue-leverage conclusions are theoretical
predictions of the declared games.

Natural evidence currently provides:

- pooled, dependence-sensitive support for predictive connectivity across
  migratory birds;
- a decision-time cue-availability anchor from the pied-flycatcher experiment;
- a registered wigeon predictive-connectivity controller null;
- a negative long-term cue-driver decline–recovery gate;
- a second preregistered same-system cue–resource gate that returned
  NO_CUE_RESOURCE_REVERSAL before resident–migrant history was opened.

That boundary must remain explicit in the final abstract, cover letter and
Discussion.
