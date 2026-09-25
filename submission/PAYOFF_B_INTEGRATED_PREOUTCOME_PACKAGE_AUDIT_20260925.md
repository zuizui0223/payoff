# PAYOFF-B integrated PREOUTCOME package audit — 2026-09-25

Status: **PASS — deterministic PREOUTCOME working package built and inspected**

## Source state

Validated package source head:

`7ed53264c8c2bb6dbd8c9d077d43b394a6892a06`

Scientific state:

```text
PREOUTCOME_INTERNAL_READY
final_submission_eligible = false
final_submission_blocker = registered Aikens fixed-24h lambda adjudication
```

## Package workflow

```text
workflow = Integrated PAYOFF-B PREOUTCOME package
run = 36108335115
status = PASS
artifact = payoff-b-integrated-tracking-preoutcome-package
artifact_id = 10851908495
artifact_sha256 = 44141280ac1c86b86671d52e02abb85e11985615903f84be351416b57f7bfeca
```

Full repository CI on the same head:

```text
workflow = test
run = 36108335117
status = PASS
```

## Inner deterministic archive

The workflow artifact contains the deterministic submission-working ZIP:

```text
file = PAYOFF_B_INTEGRATED_TRACKING_PREOUTCOME_PACKAGE.zip
bytes = 83719
sha256 = 09e6a822ed32301ce360ae78ac39ab64484c36f030c00f677022c0bb4455e47a
fixed_zip_timestamp = 2026-09-25T00:00:00
```

Package manifest:

```text
file = PAYOFF_B_INTEGRATED_PREOUTCOME_PACKAGE_MANIFEST.json
sha256 = 06febc1219c89d07be8823d8ceafca5d3b08addeae8b2d387c8553a3f470dc4e
file_count = 33
figure_count = 6
aikens_result_present = false
aikens_outcome_opened = false
```

## Submission-ready working layer

The package contains:

- anonymized PREOUTCOME main text;
- integrated Supporting Information;
- title-page template;
- cover-letter template;
- data/code statement template;
- integrated figure captions;
- package index;
- six deterministic SVG main figures.

The anonymous main text was inspected for the following identity leaks:

```text
ZHANG = false
Ruiqi = false
zuizui0223 = false
email_pattern = false
internal_status_line = absent
```

The main text deliberately retains the registered Aikens placeholder:

```text
AIKENS LAMBDA RESULT PENDING = present
```

so the PREOUTCOME working package cannot be mistaken for a final-submission manuscript.

## Supporting Information

The generated Supporting Information contains:

- S1–S8: frozen synthetic mechanism evidence;
- S9: broad 55-species macroecological test;
- S10: direct phase-control systems and interval scale;
- S11: environmental-reconstruction reliability;
- S12: industrial actuation perturbation and preregistered Aikens gate;
- S13: integrated claim boundary.

The Supporting Information explicitly retains:

```text
PREOUTCOME STATE: the Aikens lambda outcome is unopened
```

## Figure integrity

The package contains exactly six SVG main figures. Their hashes are identical to
the canonical pre-Aikens integrated render:

| Figure | SHA256 |
|---|---|
| 1 | `34fc00c0b117bf8e7d6e1cb39cebde860f92afc01eea70bb127386a7ebcce0b6` |
| 2 | `166202cb17e74cca857afcb383038a8e082d5337a78a35dd7fab3bbda50375dc` |
| 3 | `f34f60a63590b7c7ea101b9c55c680f30786aee6a1a3f1ec7f9c654d819c4591` |
| 4 | `1f0aa3de78be965d14162cf22d7081a56750a3447ab5516c53f9061828538a6e` |
| 5 | `b5c0230ee5edb19ee9452d69b2a2c38ce34995dd40245a15d549cdeeb5b66295` |
| 6 | `e83e38f6f47c62b92f5628612d3411dfb7e7061e1a3dc935ab1cf14425c3001b` |

## Publication implication

The integrated paper now has a reproducible, anonymous, journal-neutral
PREOUTCOME working package. No internal manuscript, citation, figure,
Supporting Information, packaging, provenance or anonymity task remains open.

This audit does **not** promote the package to final-submission eligibility.

Final scientific progression remains:

```text
authenticated Aikens environmental extraction
-> registered fixed-24h adjudication
-> outcome-rendered manuscript
-> outcome-rendered Figure 6 / six-figure set
-> post-outcome manuscript audit
-> journal-specific finalization
```

No post-outcome narrative retuning is licensed.
