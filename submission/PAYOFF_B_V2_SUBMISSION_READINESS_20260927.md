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
structured abstract = 244 words
main body = 4,761 words
references = 18
display pieces = 7
keywords = 8
running title = 38 characters
identity leaks = 0
internal tokens = 0
package files = 17
```

Frozen package:

```text
workflow run = 36405110540 (attempt 1)
artifact = 10962346030
artifact digest =
66919dc4bb327c601e48c0545f240789f56b9f03dcfe2ff947753d4cc24642aa

inner deterministic ZIP SHA256 =
6d9e2aa0a1e9628d56d5a08fa23bd50999c7f8e059488b525585a4c2631cf1d1
```

The declarations-inclusive package was rerun from the same frozen head in
workflow run 36405110540 (attempt 2; artifact 10956526561). The deterministic
inner ZIP remained byte-identical:

```text
6d9e2aa0a1e9628d56d5a08fa23bd50999c7f8e059488b525585a4c2631cf1d1
```

The inner archive remained byte-identical, confirming deterministic reproduction of the claim-ceiling package.

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
workflow run = 36405110527
artifact = 10962266489
artifact digest =
3945c71f7c8e00521cb8a7d9a5793a8b0b688d3d27d58914a9d3decd72d1acba

inner reviewer ZIP SHA256 =
6e4ef8542ba7f02737d77328b72217ff766ed1c7b4d1362d35cf7f3b77ce1275

files = 74
Python source closure = 27
figures = 7
identity scan = PASS
raw empirical data redistributed = false
reviewer archive reproduction run = 36405110527
reviewer archive reproduction artifact = 10956531442
reviewer archive deterministic inner SHA256 = 6e4ef8542ba7f02737d77328b72217ff766ed1c7b4d1362d35cf7f3b77ce1275
```

The archive contains the blinded manuscript, Supporting Information, exact
theory sources, frozen derived receipts and the code closure needed to audit
the reported analyses. Raw source datasets with separate access terms are not
silently redistributed.

The archive builder also supports the frozen postoutcome result classes. The
current ACCESS_BLOCKED outcome archive was generated from the same frozen
submission-state receipt:

```text
ACCESS_BLOCKED reviewer ZIP SHA256 =
071de59f078a57ea900da56e9e0aa3fc0f0d4b411b3324288f9409919b0b50eb

workflow run = 36405529626
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

The deterministic ACCESS_BLOCKED submission package was built in workflow
`36405529626` from head `7bcaaef50407f06a0624ec7e6931decffbfc664d`.

```text
attempt 1 artifact = 10962600581
attempt 1 artifact digest =
1c6041c9c26d849eb3d2b856fe50875acb2ee13dff0feca5e719d096463fb5ff

GEB inner ZIP SHA256 =
f84157091ebc07a8dc17a86b6da21fcc97698d81d806a14bc6558904fc95a69e

outcome reviewer ZIP SHA256 =
071de59f078a57ea900da56e9e0aa3fc0f0d4b411b3324288f9409919b0b50eb

attempt 2 artifact = 10962317280
attempt 2 artifact digest =
9e6194e02484bc95d651ff7b01a34b6dd11d3e12e143c852ad7490c588808a67

deterministic inner archives = PASS
```

If authenticated access later becomes available, the already-frozen AppEEARS /
V061 / fixed-24 h workflow may still be executed and classified into one of the
four scientific result classes. That future execution is no longer required
for the present submission route.

## 4. Final journal upload — SCIENCE-CLOSED, PORTAL INPUTS REMAIN

The current ACCESS_BLOCKED science state is closed for submission. Portal
upload still requires:

1. delivery of the already-built anonymous reviewer archive through the journal portal or a stable anonymous link;
2. author list, affiliations, ORCID and corresponding-author metadata;
3. funding, conflict-of-interest, acknowledgements and contribution
   declarations;
4. final human review of the generated outcome package.

The current manuscript now explicitly states that photoperiodic/endogenous migration programmes are a non-exclusive alternative explanation for the E6 migration-distance gradient, and that the pairwise deadline-difference mechanism has not yet been directly tested in a natural interacting pair.

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
