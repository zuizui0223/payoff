# Industrial-development mule-deer perturbation receipt

Status: independent published perturbation evidence. Raw Dryad reanalysis is deferred because the current Dryad file-stream endpoint requires an authenticated session.

Source: Aikens et al. (2022), *Nature Ecology & Evolution* 6:1733–1741, DOI 10.1038/s41559-022-01887-9.

Dataset: Dryad DOI 10.5061/dryad.7d7wm37z5.

## Why this system matters

The Ortega mule-deer system supplies a positive controller signature:

~~~text
late relative to resource wave
-> faster movement
-> less stopover
-> reduced phase error
~~~

The Aikens long-term gas-field system is a natural perturbation of that mechanism.

It asks whether a migration corridor can remain geometrically connected while industrial disturbance prevents animals from expressing the movement response needed to stay coupled to phenology.

## Published result

Across a 14-year period of coalbed natural-gas development, migrating mule deer initially synchronized movement with peak spring green-up.

As development expanded, deer increasingly held up at the edge of the developed gas field and allowed the green wave to pass.

The published study reports:

~~~text
route-scale green-wave surfing reduction = 38.65%
study duration = 14 years
~~~

The behavioral disruption propagated beyond the physically developed section of the migration corridor.

The study found no evidence that animals acclimatized sufficiently to recover the earlier surfing behavior as development increased.

## Controller interpretation

In the phase-feedback framework, development can be represented as a constraint on the behavioral response:

\[
u_{\rm realized}(E,s)
=
G(s)\,u_{\rm desired}(E),
\]

where \(G(s)\) is a route-specific movement-permeability or behavioral-gating term.

For an undisturbed route,

\[
G(s)\approx1.
\]

At a strongly disruptive segment,

\[
0<G(s)<1,
\]

so an animal that is late may be unable to realize the speed/stopover response implied by its phase error.

Then

\[
\frac{dE}{ds}
=
\frac{1/u_{\rm realized}(E,s)-1}{c_e}
\]

can remain positive even when the unconstrained controller would have produced phase correction.

This provides a mechanistic interpretation of corridor degradation:

> A corridor can remain physically traversable yet lose its **phenological control bandwidth**.

## New macro quantity — control permeability

Define

\[
G
=
\frac{u_{\rm realized}}
{u_{\rm expected}(E)}
\]

relative to a reference controller calibrated in undisturbed conditions.

~~~text
G ~ 1
behavioral control is fully expressed

G < 1
movement response is attenuated

G -> 0
effective controller failure / hold-up
~~~

In a before–after or developed–undeveloped design, \(G\) can be estimated from deviations in realized relative movement speed after conditioning on phase error.

## Macro prediction

Infrastructure should not merely increase raw travel time.

It should specifically:

1. lower effective control permeability \(G\);
2. lengthen phase-correction distance;
3. increase the probability that a green wave overtakes the animal;
4. reduce route-scale surfing even when only a small route fraction is directly disturbed.

This is stronger than a generic "barriers slow migration" hypothesis because it predicts failure relative to the animal's current phase error.

## Relation to barnacle geese

The goose evidence and this perturbation system separate two different roles of barriers:

~~~text
barnacle geese:
barriers can reduce environmental predictability,
but binary barrier presence is not itself the strongest phase predictor.

gas-field mule deer:
disturbance changes realized movement behavior,
directly attenuating the tracking response.
~~~

Thus barrier effects should be decomposed into:

~~~text
information effect:
does the route make future phenology less predictable?

control effect:
does the route prevent the animal from expressing corrective behavior?
~~~

A single binary barrier variable conflates those processes.

## Claim boundary

Licensed:

- published industrial development caused mule deer to hold up and become decoupled from green-up;
- route-scale surfing declined 38.65% over 14 years;
- the finding is consistent with attenuation of a phase-correction controller;
- the system is a strong perturbation test for the proposed framework.

Not licensed:

- a numerical estimate of \(G\) from the current branch;
- direct comparison of \(\kappa\) between the Ortega and Aikens herds;
- proof that development changes fitness specifically through the controller mechanism;
- treatment of all ecological barriers as equivalent to industrial disturbance.

## Promotion rule

Upgrade this system to a quantitative Tier A/B perturbation test when the Dryad source tables are retrieved and the published days-from-peak / route-progress metrics can be harmonized with the controller model.
