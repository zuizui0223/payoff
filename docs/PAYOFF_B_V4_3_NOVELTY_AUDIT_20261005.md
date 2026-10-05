# PAYOFF-B V4.3 novelty audit — 2026-10-05

Status: **POST-DIAGNOSTIC NOVELTY BOUNDARY**

## Bottom line

The metric-scale diagnostic improves the paper, but it changes what is novel.

Do not claim novelty for:
- using spatial phenology correlation as a migration-information coordinate;
- combining correlation with a slope/proportionality measure;
- relating route predictability to migration timing;
- recognizing environmental variability as distinct from predictability;
- generic feedforward versus feedback control;
- increasing spatial synchrony of spring phenology under warming;
- increasing spatial synchrony in North American environmental or population
  time series.

These all have clear prior art.

## Closest prior work

### Kölzsch et al. 2015

Barnacle-goose migration work already used:
- correlation of spring anomalies between successive stopovers;
- a proportionality/slope index;
- migration-arrival RMSD;
- long-term spring variability;
- tests relating environmental predictability to tracking.

Therefore V4.3 cannot claim that ecology previously treated predictability as
correlation alone.

### Bernhardt et al. 2020

The feedback/feedforward distinction in fluctuating environments is explicit
prior art. V4.3 cannot claim to introduce prediction versus correction as a
generic ecological distinction.

### Liu et al. 2019

Increasing spatial synchrony of spring vegetation phenology under climatic
warming is established prior art. A positive temporal change in V8 rho is not
the novelty by itself.

### Koenig & Liebhold 2016

Temporal increase in spatial synchrony of North American environmental and bird
time series is also established.

### Bauer et al. 2020

Sequential environmental information and the timing value of migration-stage
cues are established. V4.3 cannot claim to introduce stagewise information
acquisition.

## Candidate contribution that survives

The narrow empirical contribution is the joint temporal decomposition in the
same sampled source-destination network:

1. destination anomaly SD increased strongly;
2. standardized source-destination coupling increased strongly;
3. target-only out-of-sample forecast error increased strongly;
4. source-informed out-of-sample forecast error did not worsen detectably;
5. therefore the day-scale out-of-sample value of cross-site information
   increased strongly;
6. bird arrival-green-up mismatch showed no corresponding deterioration.

This is not equivalent to "spring became more predictable." It is a change in
the *value of nonlocal information under increasing local variability*.

The narrow theoretical contribution is to put that forecast-value object into
the existing seasonal actionability model:

    N(t) = r(t) G(t) - C(t),

where G(t) is decision-scale expected-loss reduction from information and r(t)
is retained biological actionability.

For Gaussian timing prediction under squared loss:

    G = sigma_Y^2 rho^2
    R_residual = sigma_Y^2 (1-rho^2).

This makes explicit that environmental information value and residual absolute
uncertainty can increase together.

The existing finite information-use window then becomes a special seasonal
case of a more general value-times-actionability geometry.

## What is still not identified

The bird analysis does not identify:
- which environmental cue individual birds perceive;
- whether birds used the fitted source green-up signal;
- whether increased source forecast value caused mismatch stability;
- whether downstream correction caused mismatch stability;
- climate-change causation of the two-window contrast.

The mule-deer system independently establishes signed downstream correction
and phase convergence, but does not identify the bird mechanism.

## Journal implication

American Naturalist remains a credible first target if the paper is written as:

> a theory-plus-natural-evidence paper about the ecological value and
> actionability of seasonal information,

not as:
- a discovery that spatial synchrony increased;
- a discovery that feedforward and feedback coexist;
- a claim that better predictability failed to improve tracking.

The empirical novelty is narrower than a top general-science discovery, but the
combination of:
- preregistered falsification transparency;
- posthoc scale diagnosis;
- decision-scale information-value theory;
- independent downstream-correction anchor

is well aligned with an American Naturalist Major Article.

Ecology Letters / PNAS / Nature Ecology & Evolution still require a more direct
natural test of the predicted information-value/actionability geometry.

## Strongest future decisive test

Measure at three or more ordered stages of the same seasonal decision:

1. the no-information prediction loss L0(t);
2. the information-informed prediction loss L1(t);
3. G(t)=L0(t)-L1(t);
4. independently measured remaining response opportunity r(t);
5. observed cue-linked behavior/correction.

Then test whether behavior follows r(t)G(t)-C(t) better than correlation,
forecast error, or G(t) alone.
