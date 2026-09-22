# Ungulate reaction-norm evidence receipt

Status: independent literature-derived support for phenological plasticity; not a direct controller calibration.

Source: Laforge et al. (2025), *Ecology Letters* 28:e70101, DOI 10.1111/ele.70101.

## Design

The study used behavioral reaction norms for three North American ungulate species / five populations in Wyoming and evaluated migration timing and green-up selection across years.

The figure-level dataset includes 129 individuals across the five populations for repeatability analyses.

## Published result

The central result is asymmetric plasticity across the migration sequence:

~~~text
arrival timing on summer range:
  plastic to timing of spring green-up

departure timing from winter range:
  not detectably plastic to timing of spring green-up
~~~

Both departure and arrival timing also showed repeatable among-individual differences.

The authors interpret the arrival plasticity as evidence that herbivores can synchronize migration with interannual changes in green-up by adjusting migration pace.

## Controller interpretation

This result is consistent with a distributed controller rather than a departure-date-only controller.

If departure timing is comparatively fixed but arrival timing tracks green-up, phase correction must occur during the migration interval through some combination of:

~~~text
movement rate
stopover duration
route use
intermediate habitat selection
~~~

That is qualitatively aligned with the mule-deer phase-feedback result, where late animals move faster and reduce stopover time.

## Macro implication

Individual migration behavior contains at least two variance components:

~~~text
stable individual intercept:
  characteristic timing / phase target

plastic slope:
  response to environmental timing
~~~

These correspond naturally to different controller quantities.

A stable individual timing offset is not noise to be removed blindly; it can represent heterogeneity in target phase \(E_*\).

Environmental reaction-norm slope is related to behavioral responsiveness, but it is not identical to the controller gain \(\kappa=d\log u/dE\).

## Claim boundary

Licensed:

- migration arrival timing is plastic to spring green-up in the published study;
- migration departure timing is less plastic;
- individual timing differences are repeatable;
- the result motivates within-individual controller models.

Not licensed:

- numerical \(\kappa\), \(E_*\), or \(\ell\) from this study;
- equivalence between reaction-norm slope and the PAYOFF-B controller gain;
- a claim that all ungulate species share the same plasticity mechanism.

## Role in the programme

This is supporting prior art and design evidence rather than a new validation point in the quantitative controller registry.

It strengthens the case for estimating individual random intercepts and random controller slopes in future Tier-A trajectory analyses.
