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
main body = 4,242 words
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
workflow run = 36374436480 (attempt 1)
artifact = 10950726054
artifact digest =
81e9b9383895193073c701e2ca63678a830ff1a619911f0f30a80f4d26000cab

inner deterministic ZIP SHA256 =
07c6b9896d1536e5720770674ec02508bc8f302dd06ed25a248d91c82cf39e6c
```

The declarations-inclusive package was rerun from the same frozen head in
workflow run 36374436480 (attempt 2; artifact 10950107881). The deterministic
inner ZIP remained byte-identical:

```text
07c6b9896d1536e5720770674ec02508bc8f302dd06ed25a248d91c82cf39e6c
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
workflow run = 36374436474
artifact = 10949304838
artifact digest =
4caf4a1dc083d2f4ec0212730c0cb76ef22d7f6fa11f4f52731b796601f3aeda

inner reviewer ZIP SHA256 =
a933bc428ab9e6577536c381e493b565aadb88235b164713ce546509b698d960

files = 71
Python source closure = 26
figures = 7
identity scan = PASS
raw empirical data redistributed = false
reviewer archive reproduction run = 36374436474
reviewer archive reproduction artifact = 10950815667
reviewer archive deterministic inner SHA256 = a933bc428ab9e6577536c381e493b565aadb88235b164713ce546509b698d960
```

The archive contains the blinded manuscript, Supporting Information, exact
theory sources, frozen derived receipts and the code closure needed to audit
the reported analyses. Raw source datasets with separate access terms are not
silently redistributed.

The archive builder also supports the frozen postoutcome result classes. The
remaining reviewer-archive task is therefore **delivery**, not construction:
upload the ZIP through the journal review portal or provide a stable anonymous
link.

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
`36381284351` from head `ac63cac9fd2b76946628304f98f81763804c89b2`.

```text
attempt 1 artifact = 10952901983
attempt 1 artifact digest =
2344d57ba082510004c1c9b8251a5c704b8265209e22226eacaf9643b4703f59

GEB inner ZIP SHA256 =
c4d96db3bda99fb68b475504dcdf1e0072264e6e4e4cb7435d51979111c40e8b

outcome reviewer ZIP SHA256 =
d11c518c3eb5499f85e99f1cf7125e067745b211b5da764b8d961c930460151c

attempt 2 artifact = 10952483251
attempt 2 artifact digest =
fd49a351cc46d95fd275874425ac7acb6919f48d08d4d7995847ac922c33f4e4

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
