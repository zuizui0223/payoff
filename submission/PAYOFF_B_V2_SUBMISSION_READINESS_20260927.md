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
main body = 4,829 words
references = 20
display pieces = 7
keywords = 8
running title = 38 characters
identity leaks = 0
internal tokens = 0
package files = 17
```

Frozen package:

```text
workflow run = 36518027323 (attempt 1)
artifact = 11011469698
artifact digest =
51708a9befb1751cd60148bebe5f856190e9679245681208398d90b08e939b6c

inner deterministic ZIP SHA256 =
d7c8f3ab4f2c4d3c32da4655e069b9b35b66cb356a44643fa9018288e759ae1a
```

The declarations-inclusive package was rerun from the same frozen head in
workflow run 36518027323 (attempt 2; artifact 11012051730). The deterministic
inner ZIP remained byte-identical:

```text
d7c8f3ab4f2c4d3c32da4655e069b9b35b66cb356a44643fa9018288e759ae1a
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
workflow run = 36518027268
artifact = 11012081041
artifact digest =
0d238d11125a766f72529eb771e7839fb2b46002c8dbd553b646fdf5cb24b1c5

inner reviewer ZIP SHA256 =
b2de4fcfcdfff0236c5e18ee31073ca71b6bee635a54a1dd6276809fe2201339

files = 76
Python source closure = 27
figures = 7
identity scan = PASS
raw empirical data redistributed = false
reviewer archive reproduction run = 36518027268
reviewer archive reproduction artifact = 11012355384
reviewer archive deterministic inner SHA256 = b2de4fcfcdfff0236c5e18ee31073ca71b6bee635a54a1dd6276809fe2201339
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
8b5ba5d1a6d8c06f71bc6a8de9790ccbc1f702feb81a820790625d79d8c8ba51

workflow run = 36518314363
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
`36518314363` from head `7a4cee269f5dac9524e4517b034f3a0d967675c8`.

```text
attempt 1 artifact = 11011073915
attempt 1 artifact digest =
a74b6afccb735c8f2d39c6a1f14d88df1e277e46f9620b283ce4bccff4e66356

GEB inner ZIP SHA256 =
b74ae989a1048e0fcaa0577a2224b22fd2064ccc3b621fc8e7ce8058017a26a7

outcome reviewer ZIP SHA256 =
8b5ba5d1a6d8c06f71bc6a8de9790ccbc1f702feb81a820790625d79d8c8ba51

attempt 2 artifact = 11011782314
attempt 2 artifact digest =
0cb98c94ad2dc6581c21353ec4a529db5cb63c8ed5236ef6d5ffc1f3db5297c5

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
