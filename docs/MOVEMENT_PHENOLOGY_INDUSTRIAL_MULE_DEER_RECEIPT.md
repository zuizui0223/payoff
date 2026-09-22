# Industrial-development mule-deer perturbation receipt

Status: **quantitative actuation / control-permeability perturbation reconstructed from public archived GPS**.

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

The Aikens system asks a different question:

> Does industrial development attenuate the ability to express movement control along a migration route?

This is an **actuation** test, not a second estimate of phenological phase-retention lambda.

## Source reconstruction

The public Dryad archive contains spring-migration GPS points and two development footprints.

Registered analysis input:

~~~text
GPS points               = 64,539
valid movement steps     = 64,286
GPS animal-years         = 253
GPS animals              = 137
years                    = 2005, 2006, 2008, 2009, 2010, 2015, 2016, 2017, 2018

WHB / small-development points = 52,063
DCC / large-development points = 12,476
~~~

All shapefiles are transformed into the GPS coordinate reference system before distance calculations.

## Control-permeability quantity

For each animal-year, define

\[
G
=
\frac{\operatorname{median}(\text{movement speed near development boundary})}
{\operatorname{median}(\text{movement speed far from development boundary})}.
\]

Primary registered spatial contrast:

~~~text
near boundary <= 2 km
far from boundary >= 10 km
minimum 3 movement steps in each zone
~~~

Interpretation is relative rather than absolute:

~~~text
larger G
  stronger local movement response near the boundary relative to the animal's
  own far-route pace

smaller G
  attenuation of that local movement response
~~~

The quantity is not itself a phenological phase-retention coefficient.

## Primary result — large-development population has lower control permeability

Primary analyzable sample:

~~~text
188 animal-years
103 animals
9 study years
~~~

Median G:

~~~text
small-development WHB = 1.656
large-development DCC = 1.037
~~~

Clustered longitudinal model:

\[
\log G
\sim
\text{year}\times\text{large-development population}.
\]

At centered study year, the large-development population shift is

~~~text
beta = -0.4763
SE   =  0.1967
p    =  0.0172
~~~

On the multiplicative G scale,

\[
\exp(-0.4763)\approx0.621.
\]

Thus the fitted relative movement response is approximately **38% lower** in the large-development population at the centered study year.

This effect size is conceptually distinct from the published 38.65% reduction in route-scale green-wave surfing and should not be treated as a replication of that exact published percentage.

## Sensitivity to near/far distance definitions

The qualitative contrast is stable across all registered combinations:

~~~text
edge / far km      median G small      median G large

1 / 5                 2.137               1.123
1 / 10                2.157               0.966
1 / 20                2.340               0.841

2 / 5                 1.685               1.115
2 / 10                1.656               1.037
2 / 20                1.790               0.941

5 / 10                1.453               0.889
5 / 20                1.517               0.808
~~~

The large-development intercept shift is negative throughout the grid.

Therefore the primary inference does not depend on a single arbitrary spatial threshold.

## Step-level within-animal-year analysis

A second model uses all valid movement steps with individual-year fixed effects.

Registered terms:

~~~text
near-boundary edge effect:
  beta = +0.1963
  p = 4.59e-5

edge × large-development population:
  beta = -0.1518
  p = 0.0382

edge × year:
  beta = -0.0260
  p = 0.00106

edge × large-development × year:
  beta = +0.0146
  p = 0.226
~~~

The negative edge × large-development interaction means that the local edge-associated movement response is attenuated in the large-development population.

Because the response is \(\log(1+\text{speed})\), exponentiated coefficients should not be described as exact percentage changes in raw speed.

## Longitudinal prediction — not supported

The preregistered stronger prediction was:

> permeability should decline more strongly through time in the large-development population.

Observed interaction:

~~~text
year × large-development beta = +0.0405
SE = 0.0411
p = 0.327
~~~

There is therefore **no support** for a stronger temporal decline of G in the large-development population.

This is an important negative result.

The quantitative perturbation evidence supports a persistent cross-population attenuation of realized movement control, but not the stronger claim that this attenuation became progressively more severe through the sampled years.

## Relation to the published result

Aikens et al. report that industrial development caused mule deer to hold up and become decoupled from the green wave, with a 38.65% route-scale decline in surfing across the long-term study.

The PAYOFF-B reanalysis asks a different question at GPS-step scale:

> Is the local movement response near the development footprint attenuated relative to far-route movement?

The answer is yes in the registered comparison.

The archived GPS therefore supplies a quantitative **actuation-boundary** result consistent with the control-permeability interpretation, while the absence of a significant year × development interaction prevents claiming a newly demonstrated longitudinal erosion of G.

## Framework interpretation

The result supports separating environmental information from behavioral actuation.

A route can remain spatially passable while its effective control permeability is reduced.

In the controller notation,

\[
u_{\rm realized}(E,s)
=
G(s)\,u_{\rm desired}(E).
\]

The data do not identify \(u_{\rm desired}(E)\) directly in this population, so the observed G is a relative movement-permeability proxy rather than the literal latent multiplier in this equation.

## Gate consequence

~~~text
published perturbation / failure evidence:
  PASS

harmonized quantitative actuation test:
  PASS, with claim boundary

cross-sectional attenuation prediction:
  PASS

stronger longitudinal deterioration prediction:
  NOT SUPPORTED
~~~

This partial success is more informative than treating the perturbation system as a simple confirmatory example.

## Claim boundary

Licensed:

- public archived GPS and development footprints are directly reanalyzed;
- relative near-boundary movement response is lower in the large-development population;
- the contrast is qualitatively stable across the registered near/far sensitivity grid;
- step-level within-animal-year analysis also detects attenuation in the large-development population;
- the result is consistent with reduced movement control permeability.

Not licensed:

- a causal development effect, because the two populations differ in more than development footprint;
- a direct phenological phase-retention lambda from this dataset;
- a claim that G is below one in all developed animals;
- reproduction of the published 38.65% surfing decline from this new metric;
- a stronger longitudinal deterioration of G through time;
- universal treatment of all ecological barriers as the same actuation mechanism.
