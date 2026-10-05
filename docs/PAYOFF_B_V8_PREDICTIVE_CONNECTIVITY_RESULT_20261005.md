# PAYOFF-B V8 primary result — predictive-connectivity degradation

Frozen: **2026-10-05**

Contract:
`docs/PAYOFF_B_V8_PREDICTIVE_CONNECTIVITY_DEGRADATION_CONTRACT_20261005.md`

Workflow run: **37254852212**  
Artifact: **11321853430**  
Artifact SHA256:
`31a496d0495180312b2521c4ef2315c86cb8922c817847a11103a8522dbcb42e`

## Admission gate

The frozen gate passed without changing thresholds.

```text
FROZEN_MAPPINGS = 842
ELIGIBLE_EARLY_LATE_PAIRS = 393
ELIGIBLE_SPECIES = 28
SPECIES_WITH_AT_LEAST_3_PAIRS = 26
ADMISSION = PASS
```

The primary environmental analysis therefore opened.

## Registered degradation hypothesis

The registered prediction was

[
E(Deltaho)<0,
qquad
Deltaho
=
ho_{2010-2017}
-
ho_{2002-2009}.
]

It is **not supported**.

Primary mixed estimate:

[
widehat{Deltaho}
=
+0.3506,
]

with species-cluster bootstrap 95% interval

[
[+0.2627,,+0.4241].
]

Species-level mean:

[
+0.3364
]

with species bootstrap 95% interval

[
[+0.2023,,+0.4472].
]

Of 28 species:
- 26 had positive species-mean change;
- 2 had negative species-mean change;
- one-sided sign-test p-value for the preregistered **negative-majority**
  prediction was (0.9999999).

Thus:

```text
V8_BROAD_DEGRADATION = NOT_SUPPORTED
```

## Direction of the observed result

The result is not merely a null around zero. The observed distribution is
strongly in the opposite direction.

Across eligible source-target pairs:

```text
MEAN_RHO_EARLY = 0.4277
MEAN_RHO_LATE = 0.7806
MEDIAN_RHO_EARLY = 0.5842
MEDIAN_RHO_LATE = 0.8840
PAIR_DELTA_POSITIVE = 350
PAIR_DELTA_NEGATIVE = 43
```

Positive-to-nonpositive sign reversals occurred in 8 pairs, but
nonpositive-to-positive changes occurred in 73 pairs.

The two species with negative mean change were:
- *Hirundo rustica* (1 eligible pair);
- *Vireo flavifrons* (13 eligible pairs).

## What this means

The original user-level hypothesis was biologically plausible and has a natural
route-level precedent: climate change can make one location a worse predictor
of a later spring state.

But in this broad 2002–2017 Amaral sample, the preregistered generalization is
wrong in direction.

The licensed conclusion is:

> **We found no broad degradation of signed detrended source-to-destination
> spring predictability. Instead, the sampled route pairs became substantially
> more positively connected between the two non-overlapping eight-year
> windows.**

This does **not** yet establish that migrants gained usable information.

A stronger positive correlation can arise from environmental covariance
structure without birds perceiving or exploiting it, and V8 does not establish
a climate-causal mechanism.

## Why the result is still ecologically interesting

The result separates two different global-change problems.

Published work shows that:
- mean spring timing can shift heterogeneously in space;
- migration can become mismatched with current green-up;
- particular route links can lose or reverse predictability.

V8 shows that these facts do not imply a general decline in the
**interannual signed covariance structure** linking earlier and later places.

In other words:

[
	ext{spatial phenological decoupling}

otRightarrow
	ext{broad loss of interannual predictive connectivity}.
]

That distinction was not guaranteed in advance.

## Next frozen step

The mandatory contract sensitivities are still unopened.

They must be run before any positive reinterpretation is promoted:
- Fisher-z change;
- complete 8/8-year pairs;
- species-balanced weighting;
- source-target distance moderator;
- raw undetrended negative control;
- non-overlapping 7-year windows;
- leave-one-species-out.

No new window or threshold may be introduced.

```text
V8_PRIMARY_RESULT = FROZEN
V8_SUPPORT_STATUS = NOT_SUPPORTED
V8_OBSERVED_DIRECTION = STRONG_INCREASE
V8_SENSITIVITIES = UNOPENED
```
