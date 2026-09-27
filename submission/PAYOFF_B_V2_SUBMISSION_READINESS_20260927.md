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
structured abstract = 243 words
main body = 4,148 words
references = 13
display pieces = 7
keywords = 8
running title = 38 characters
identity leaks = 0
internal tokens = 0
```

Frozen package:

```text
workflow run = 36309072630
artifact = 10927484417
artifact digest =
7b1033684a17e8018ce12e8d9d1809583bffbf98eb9431c3aa9075e573e857f5

inner deterministic ZIP SHA256 =
d5b5652beb032ea8dfed90eab85527f20310c6b4e0a304e50f48755d233d653b
```

After the postoutcome pipeline was added, the package was rebuilt in run
36312188417. The deterministic inner ZIP remained byte-identical:

```text
d5b5652beb032ea8dfed90eab85527f20310c6b4e0a304e50f48755d233d653b
```

So postoutcome plumbing did not alter the frozen PREOUTCOME journal package.

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

1. anonymous stable reviewer archive link;
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
