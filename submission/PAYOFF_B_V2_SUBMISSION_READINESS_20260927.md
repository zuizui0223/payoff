# PAYOFF-B V2 submission readiness

Frozen: **2026-09-27**

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
main body = 4,167 words
references = 13
display pieces = 7
keywords = 8
running title = 38 characters
identity leaks = 0
internal tokens = 0
```

Frozen package:

```text
workflow run = 36313076476
artifact = 10930130067
artifact digest =
c47efff79a125945361d4a7f576141d70df6cbd30512556337be1c3f62c693c6

inner deterministic ZIP SHA256 =
cf1ada3fb67b603b972f6e3994f439292b3ed3b18f17d2f0c3407c0bc90288cd
```

The frozen package was reproduced after the claim-ceiling update in run
36315132279. The deterministic inner ZIP remained byte-identical:

```text
cf1ada3fb67b603b972f6e3994f439292b3ed3b18f17d2f0c3407c0bc90288cd
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
workflow run = 36315711405
artifact = 10930372460
artifact digest =
2b364730325982cfb12d7152d41810a58f52b24c662f4bca55b1d57bc81e7a4d

inner reviewer ZIP SHA256 =
857d6e22fe2b9bc4724c35659667fa9159d69a8c93f7789f68f496828df918a6

files = 64
Python source closure = 23
figures = 7
identity scan = PASS
raw empirical data redistributed = false
```

The archive contains the blinded manuscript, Supporting Information, exact
theory sources, frozen derived receipts and the code closure needed to audit
the reported analyses. Raw source datasets with separate access terms are not
silently redistributed.

The archive builder also supports the frozen postoutcome result classes. The
remaining reviewer-archive task is therefore **delivery**, not construction:
upload the ZIP through the journal review portal or provide a stable anonymous
link.

## 3. Real Aikens execution — credential recheck required

The scientific contract is frozen and the outcome is still unopened.

The last verified credential-only preflight was 2026-09-25:

```text
workflow run = 36113621057
artifact = 10853764396
status = NOT_CONFIGURED
credential route = none
environmental values opened = false
lambda outcome opened = false
```

This is a historical verified state, not a claim about the current GitHub
Secrets configuration. Secret values are not visible from repository audit.

The next execution step is therefore:

```text
rerun credential preflight
-> if credentials are configured:
   execute the already frozen full AppEEARS / V061 / fixed-24 h workflow
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
- a negative long-term cue-driver decline–recovery gate.

That boundary must remain explicit in the final abstract, cover letter and
Discussion.
