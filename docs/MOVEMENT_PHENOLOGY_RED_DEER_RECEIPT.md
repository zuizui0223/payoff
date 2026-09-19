# Norwegian red-deer jump-versus-surf evidence receipt

Status: independent strategy-boundary evidence; raw GPS reanalysis pending.

Source: Bischof et al. (2012), *The American Naturalist* 180:407–424, DOI 10.1086/667590.

Dryad dataset: DOI 10.5061/dryad.3hr2c.

## Dataset

The archived dataset contains GPS data for 294 red deer monitored in Norway between 2002 and 2010.

The published analysis linked MODIS NDVI phenology with space use and distinguished:

~~~text
167 migratory deer
78 resident deer
~~~

within the analysis subset reported in the paper.

## Main result

Migrants obtained greater access to early plant phenology than residents, but did **not** generally surf the green wave continuously during migration.

Instead:

> migratory red deer moved rapidly from winter to summer range, effectively "jumping" the green wave.

After the migration jump, migrants — and to a lesser degree residents — tracked phenological green-up through smaller-scale habitat-use adjustments.

## Importance for PAYOFF-B

This is a critical boundary case.

The simplest phase-locking controller imagines continuous correction:

~~~text
phase error
-> change movement speed
-> stay locked to moving resource front
~~~

Red deer demonstrate a different viable architecture:

~~~text
winter range
-> rapid relocation / jump
-> reconnect with phenological spring at summer range
-> fine-scale local tracking
~~~

Thus successful phenological migration does not require continuous \(u_{\rm macro}\approx1\).

## Macro hypothesis generated

The controller framework needs a discrete strategy layer:

~~~text
SURF
continuous phase correction along route

JUMP
rapid transition between seasonal ranges,
then phase reacquisition at destination

STEP
stopover-to-stopover phase control

OVERTAKE
deliberately change target phase along route
~~~

Route-scale resource geometry should determine which strategy is favorable.

A likely predictor is whether useful phenological states form a continuous moving corridor or spatially separated seasonal patches.

## Relation to PAYOFF-B theory

The red-deer result is conceptually close to the distinction between:

~~~text
continuous tracking
versus
switching between favorable patches.
~~~

It therefore reconnects the movement–phenology macro programme to the original two-patch anti-phase PAYOFF-B benchmark more naturally than forcing all movement into a continuous wave model.

## Claim boundary

Licensed:

- the published system is dominated by jumping rather than continuous green-wave surfing during migration;
- smaller-scale phenological tracking occurs outside the main migration jump;
- a universal continuous phase-locking model is therefore insufficient across taxa.

Not licensed:

- a controller-gain estimate from the archived raw GPS data;
- proof that jumping is optimal in a game-theoretic or fitness sense;
- a quantitative threshold separating surf and jump strategies.

## Promotion rule

Raw reanalysis becomes useful when environmental phenology can be reconstructed along each route. The key target is not a single \(\kappa\), but a strategy classifier and a test of whether landscape phenology continuity predicts surf versus jump behavior.
