# PAYOFF-B Aikens IID target-coverage support robustness receipt

Frozen: 2026-09-22

Status: **outcome-blind support robustness quantified before environmental extraction**.

This receipt uses only the frozen fixed 24 h GPS targets selected before any
environmental availability is observed.

It does not use MODIS values, reconstructed peak IRG, phase values, or lambda
outcomes.

## 1. Frozen source

Pre-environment fixed-target artifact:

    workflow:
        payoff-b Aikens pre-environment support ceiling

    run:
        35687039708

    artifact:
        10676913354

    artifact sha256:
        ab88ade2ec53c8f91b1a2099d58ad210ad57ab80d826375938c94bfe8689efa2

Frozen target table:

    aikens_primary_fixed_gps_targets.csv

Target count:

    5,710

Group target counts:

    large-development:
        1,114

    small-development:
        4,596

Maximum frozen adjacent-pair support:

    large-development:
        1,022 pairs
        48 animals

    small-development:
        4,434 pairs
        89 animals.

Registered final support threshold per group:

    >=10 animals
    >=100 adjacent valid phase pairs.

## 2. Declared robustness model

Let each already selected target independently have valid environmental phase
with probability

    p.

A frozen adjacent target pair contributes only when both targets are valid.

The exact dynamic programme computes

    P(
        adjacent valid pairs >= 100
        AND
        animals with >=1 valid adjacent pair >= 10
      )

for each development group and jointly across groups.

This is exact under the declared IID target-validity model.

It is **not** an empirical model of MODIS / IRG missingness. Real failures can
be correlated by pixel-year, geography, date, snow, quality flags, or
development population.

## 3. Exact support curve

### p = 0.25

Large-development support probability:

    0.000146

Small-development support probability:

    approximately 1.

Joint support probability:

    0.000146.

### p = 0.30

Large-development support probability:

    0.24148

Small-development support probability:

    approximately 1.

Joint support probability:

    0.24148.

### p = 0.35

Large-development support probability:

    0.98149

Small-development support probability:

    approximately 1.

Joint support probability:

    0.98149.

### p = 0.40

Joint support probability:

    >0.999999.

Thus the support transition is dominated by the large-development group.

## 4. 95% joint-support threshold

The exact bisection search, tolerance 1e-4, gives

    minimum IID target-validity probability:
        0.341979980469.

At this point:

    joint support probability:
        0.950017321171.

Large-development group:

    support probability:
        0.950017321171

    expected valid adjacent pairs:
        119.5232

    expected animals with >=1 valid adjacent pair:
        34.1933.

Small-development group:

    support probability:
        1.0 within numerical precision

    expected valid adjacent pairs:
        518.5577

    expected animals with >=1 valid adjacent pair:
        71.3082.

Therefore, under IID target-level environmental validity, roughly **34.2%**
validity is sufficient for a 95% probability that both frozen support gates
are met.

## 5. Interpretation

This materially narrows the current operational uncertainty.

The pre-environment support ceiling already showed that the final test is
possible.

The present result shows that, under a simple independent-validity envelope,
the final registered support gate does not require near-complete environmental
coverage.

The bottleneck is specifically the large-development group.

This is useful operationally because AppEEARS / IRG extraction can now be
assessed against a predeclared support-risk scale rather than judged after the
lambda fit.

## 6. Pixel-year clustering boundary

The frozen targets are not all independent environmental units.

Descriptive source geometry shows:

    large-development:
        1,114 targets
        910 unique pixel-years
        about 30.8% of targets belong to pixel-years used more than once

    small-development:
        4,596 targets
        3,400 unique pixel-years
        about 41.8% of targets belong to pixel-years used more than once.

Therefore the IID target-level model is a reference envelope, not a final
missingness model.

A pixel-year-clustered sensitivity can be added separately, but it must remain
a robustness analysis and must not be used to retune the registered support
threshold.

## 7. Provenance

Canonical optimized run:

    workflow:
        payoff-b Aikens IID target coverage support

    run:
        35689293494

    head:
        be5182bb6c2d2703c7c54f78581734e06e9a997a

    artifact:
        10677867402

    artifact sha256:
        dc377ddaaf56b7c641a9b9b666fbcbfee677edac1010b1cd564558447fbcd37c.

The original unoptimized implementation produced the same threshold in run

    35689048123

which provides an independent code-path consistency check before the dynamic
programme was optimized.

## 8. Claim ceiling

Licensed now:

- exact support probability under IID target-level validity;
- the 95% joint-support threshold p ~= 0.342 under that model;
- large-development is the support-limiting group;
- final support need not require near-complete target validity under the IID
  envelope.

Not licensed:

- a claim that real environmental validity is IID;
- a guarantee that 34.2% observed MODIS / IRG coverage will pass the final gate;
- changing the registered >=10 animal / >=100 pair thresholds;
- changing fixed target geometry after environmental missingness is observed;
- opening lambda from this robustness analysis.

The lambda outcome remains unopened.
