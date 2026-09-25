# GEB integrated tracking ecology — post-Aikens pipeline readiness

Audited: **2026-09-25**

Status: **PIPELINE_READY / REAL AIKENS OUTCOME STILL UNOPENED**

This receipt validates the journal-facing completion path after registered Aikens
adjudication. It does **not** report or infer the real Aikens result.

## Validated branch head

`160e183c8edbc238c64546e7de1a56421e65ff42`

Full repository CI:

```text
workflow = test
run = 36110717190
status = PASS
```

## End-to-end route

The authenticated Aikens workflow now continues through:

```text
registered Aikens result JSON
-> outcome-rendered integrated ecology manuscript
-> outcome-rendered integrated six-figure set
-> integrated post-outcome science audit
-> science-ready journal-neutral outcome package
-> GEB outcome-rendered blinded source
-> GEB outcome-rendered Supporting Information
-> GEB six-figure format overlay with adjudicated Figure 6
-> GEB post-outcome audit
-> deterministic GEB outcome package
```

The workflow artifact upload includes both the journal-neutral integrated outcome
package and `GEB_INTEGRATED_OUTCOME_PACKAGE.zip`.

## Licensed result classes

The post-outcome pipeline is tested for all four frozen result classes:

- `PASS`;
- `FAIL_WRONG_DIRECTION`;
- `FAIL_INSUFFICIENT_SUPPORT`;
- `NOT_ESTIMABLE`.

For every class, tests require:

- no `PENDING` placeholder remains;
- structured GEB abstract remains <=300 words;
- main body remains <=5,000 words;
- exactly six display pieces remain;
- all references remain cited;
- blinded-text identity scan passes;
- all four Aikens marker pairs are preserved;
- claim-state result class matches the registered result;
- retuning remains forbidden;
- Aikens is not added to the cross-taxon lambda synthesis;
- Figure 6 state matches the adjudicated result;
- deterministic GEB ZIP reproduction succeeds.

## Scientific / portal boundary

After a real registered adjudication and a passing GEB post-outcome audit:

```text
SCIENTIFIC_STATE = OUTCOME_RENDERED_SCIENCE_READY
FINAL_SCIENCE_BLOCKER = none
FINAL_SUBMISSION_ELIGIBLE = false
```

The remaining blockers are portal / author controlled only:

1. anonymous stable reviewer archive link;
2. author-controlled title-page and declaration metadata.

A negative, wrong-direction, insufficient-support or non-estimable registered
result is scientifically valid and does not trigger narrative retuning.

## Real-outcome boundary

At the time of this receipt:

```text
REAL_AIKENS_LAMBDA_OUTCOME = UNOPENED
APPEEARS_AUTHENTICATED_EXTRACTION = external dependency
```

No simulated test payload is a scientific result.
