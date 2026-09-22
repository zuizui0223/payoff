# Movement–phenology phase locking

## Why zero phenological lag is the wrong null

A migrant does not have to arrive on the day of vegetation mid-green-up to be well matched. Different species may systematically lead or lag the vegetation wave because the relevant resource, territory establishment, breeding preparation, or trophic response occurs before or after the remotely sensed green-up metric.

Let route position be s and suppose local animal and environmental timing are approximately planar along the route:

~~~text
T_animal(s)      = a0 + s / c_a
T_environment(s) = e0 + s / c_e
~~~

where c_a and c_e are the animal and environmental front speeds.

The phenological lag is

~~~text
L(s)
= T_animal(s) - T_environment(s)
= (a0-e0) + s * (1/c_a - 1/c_e).
~~~

Therefore

~~~text
c_a = c_e
=> L(s) = constant,
~~~

not necessarily zero.

The intercept a0-e0 is a species-specific or route-specific phase offset. Movement–phenology timescale matching predicts **phase preservation**, not universal zero lag.

## Phase drift

The spatial drift in phase is

~~~text
dL/ds = 1/c_a - 1/c_e.
~~~

With

~~~text
u_macro = c_a / c_e,
~~~

the drift is

~~~text
dL/ds = (1/u_macro - 1) / c_e.
~~~

Thus parallel fronts have zero phase drift exactly at

~~~text
u_macro = 1.
~~~

In two spatial dimensions,

~~~text
gradient(L)
= gradient(T_animal) - gradient(T_environment).
~~~

A dimensionless phase-drift diagnostic is

~~~text
D_phase
= ||gradient(T_animal)-gradient(T_environment)||
  / ||gradient(T_environment)||.
~~~

Writing u for the speed ratio and A for directional alignment,

~~~text
D_phase
= sqrt(1 + 1/u^2 - 2*A/u).
~~~

This is distinct from the normalized velocity-vector mismatch

~~~text
D_velocity
= sqrt(1 + u^2 - 2*u*A).
~~~

Both vanish at equal speed and direction, but D_phase is the more direct measure of whether a species-specific phenological offset remains spatially stable.

## Connection to Stage 1

The Amaral reanalysis shows exactly why this distinction matters.

Raw absolute arrival/green-up lag has its flexible minimum well below the PAYOFF-B order-one reference. After subtracting each species × cell's usual lag, however, the flexible point minimum returns to order-one values.

That pattern is consistent with a system in which species have nonzero local phase offsets but can still track changes in the moving phenology wave.

The Stage-1 centered response

~~~text
current lag - mean species × cell lag
~~~

is therefore an interannual analogue of spatial phase drift: it removes the local phase intercept and asks how strongly the phase relationship is displaced.

## Empirical prediction

The macro programme should no longer ask

~~~text
Do animals arrive exactly at green-up when u_macro is near one?
~~~

It should ask

~~~text
Do animals preserve their characteristic phenological phase most effectively
when movement and environmental fronts have matching timescales?
~~~

This distinction is central to Stage 2.

## Claim boundary

This phase-locking identity is kinematic. It does not by itself show that natural selection optimized a migration strategy, that a stable phase offset maximizes fitness, or that the exact PAYOFF-B anti-phase optimum transfers unchanged to continuous landscapes.

Its role is to define the correct empirical observable before demographic or evolutionary interpretation.
