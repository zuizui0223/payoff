# PAYOFF-B integrated tracking ecology — PREOUTCOME readiness

Frozen readiness date: **2026-09-25**

Status: **PREOUTCOME_INTERNAL_READY**

Canonical manuscript:

`manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md`

Adopted publication architecture merge:

`572b3a63de54a6a9abf46739108ed57ee8a876f9`

## Machine validation

Validated source head:

`cc8674cefecf0a09b85ac25446275b5bdc44dc4b`

### Full repository CI

```text
workflow = test
run = 36106665350
status = PASS
```

The full pytest phase and all downstream repository smoke / reproducibility
steps completed successfully.

### Integrated manuscript audit

```text
workflow = Integrated PAYOFF-B manuscript audit
run = 36106665356
artifact = 10850919823
artifact_sha256 = 14a983f031287d344031b8a8636fc1b93b0889e76e8f78608c727407f994191d
status = PASS
```

Audited manuscript metrics:

```text
abstract_words = 231
main_text_words = 3458
keywords = 8
references = 21
uncited_references = 0
main_figures = 6
identity_leaks = 0
```

Every PREOUTCOME hard gate passed:

- theorem manuscript remains separate;
- broad 55-species falsification remains the primary cross-system result;
- broad result is bound to the frozen Stage-1 workflow artifact;
- all references are cited;
- exactly six main figures are declared;
- all four Aikens outcome-blind marker pairs occur exactly once;
- the Aikens lambda outcome remains unopened;
- anonymous text contains no author/repository/email leak;
- universal lambda / universal actuator claims remain prohibited.

### Integrated six-figure render

```text
workflow = Integrated PAYOFF-B six figures
run = 36106665345
artifact = 10851039331
artifact_sha256 = c6529f1f16b6df25dbff6fa7cf1c37bc11536b0b1792a5f65ddda93378bc62be
status = PASS
```

The figure manifest records:

```text
aikens_result_present = false
aikens_outcome_opened = false
figure_count = 6
```

## Outcome-blind completion path

The authenticated Aikens workflow is wired end to end:

```text
frozen GPS source
-> V061 environmental extraction
-> peak-IRG reconstruction
-> fixed 24 h phase pairs
-> preregistered lambda contrast
-> registered result JSON
-> outcome-rendered integrated manuscript
-> six-figure set with adjudicated Figure 6
-> post-outcome integrated manuscript audit
```

The same frozen renderer has test coverage for all four licensed result classes:

- `PASS`;
- `FAIL_WRONG_DIRECTION`;
- `FAIL_INSUFFICIENT_SUPPORT`;
- `NOT_ESTIMABLE`.

No outcome class is allowed to add Aikens as a fourth cross-taxon replication or
to retune the narrative after outcome inspection.

## Remaining blocker

There is no unresolved internal manuscript, citation, figure, provenance,
anonymity, or code blocker.

The remaining scientific dependency is execution of the registered authenticated
AppEEARS/Earthdata environmental extraction and consequent Aikens fixed-24 h
adjudication. The workflow requires either an AppEEARS token or the configured
Earthdata username/password pair; credential values are not stored in or exposed
by this repository receipt.

After that adjudication, the post-outcome audit determines whether the rendered
integrated manuscript is scientifically ready for final submission preparation.

## Rollback boundary

The former standalone sources remain preserved:

- `manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`;
- `manuscript/PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V3_PREOUTCOME.md`.

They are provenance / rollback sources, not simultaneous submission manuscripts
under the adopted two-paper architecture.
