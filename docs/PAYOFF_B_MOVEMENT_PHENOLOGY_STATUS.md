# PAYOFF-B movement–phenology status

Status date: 2026-09-18.

## Executive state

The macroecological extension has changed shape after empirical testing.

The original proposed claim

> natural migrants should show one universal order-one movement/environment speed optimum

is **not supported** by the first broad bird reanalysis.

The stronger emerging programme is instead

> **Migrants can preserve a species- or population-specific phenological phase by changing movement rate and stopover behavior in response to phase error; the strength and spatial scale of this feedback should vary predictably among migration systems.**

This is a more general and empirically defensible development of PAYOFF-B.

## PAYOFF-B1 remains unchanged

The active short theorem paper remains:

~~~text
symmetric two-patch
exact anti-phase seasonal switching
constant symmetric migration rate
unique positive migration optimum
dimensionless scaling u*=m*tau
~~~

Nothing in the macro programme changes that theorem or its submission claim boundary.

## Macro Stage 1 — 55 migratory bird species

Dataset: Amaral et al. (2025), eastern North America, 2002–2017.

Registered complete analysis:

~~~text
N = 5816 species × year × cell observations
55 species
15 years
median animal/environment front speed ratio = 1.263
median directional alignment = 0.948
~~~

### Raw mismatch

Absolute arrival–green-up lag does not show the predicted universal order-one optimum.

Flexible GAM minima:

~~~text
median directional alignment: u_macro ≈ 0.405
perfect alignment:             u_macro ≈ 0.365
~~~

### Local-phase-centered mismatch

After removing each species × cell's usual phase offset:

~~~text
median alignment: u_macro ≈ 1.043
perfect alignment: u_macro ≈ 1.397
~~~

These point minima are order-one but shallow and highly uncertain.

Species diagnostics:

~~~text
41 species could be fit
16/41 positive quadratic curvature
11/41 finite vertices within observed support
4/11 supported vertices inside 1 .. 1.606115
~~~

No convincing moderator emerged from HWI, body mass, overwinter latitude, mean phenological sensitivity, route-direction concentration, animal/environment directional alignment, or simple interannual timing variability.

Conclusion:

> Broad population-front data suggest that phase centering matters, but do not support a universal natural constant.

## Conceptual correction — phase locking

The correct empirical null is not zero arrival lag.

For route position \(s\),

\[
T_a(s)=a_0+s/c_a,
\qquad
T_e(s)=e_0+s/c_e.
\]

If \(c_a=c_e\),

\[
T_a(s)-T_e(s)=a_0-e_0,
\]

which is constant but need not equal zero.

Thus timescale matching predicts **preservation of a characteristic phase offset**.

## Macro Stage 3 — mule-deer independent validation

Official published source data from Ortega et al. (2023) provide 152 animal-years from 72 individuals across eight years.

Define

\[
u_{\rm macro}
=
\frac{\text{animal movement rate}}
{\text{green-wave propagation speed}}
\]

and let \(E_{\rm start}\) be days from the resource peak at migration start.

The fitted feedback is

\[
\log u
=
\alpha+\kappa E_{\rm start}.
\]

Result:

~~~text
kappa = 0.01830 per day
individual-clustered SE = 0.001223
cluster p = 1.21e-50
positive kappa in 8/8 years
~~~

Thus each additional day behind the resource wave is associated with approximately 1.85% higher relative movement speed.

Stopover is adjusted in the same compensatory direction:

~~~text
-0.492 stopover days per +1 day of phase error
individual-clustered p = 6.07e-37
~~~

Absolute phase error declines during migration:

~~~text
mean start error = 21.91 d
mean end error   = 11.12 d
clustered mean reduction = 10.79 ± 1.41 d
p = 2.28e-14
~~~

The fitted stable phase is nonzero:

~~~text
E* = 8.46 d
delta-method SE ≈ 2.30 d
~~~

and the estimated local correction scale is

~~~text
green-wave speed = 5.61 km/d
e-folding correction distance ≈ 307 km
half-error distance ≈ 213 km
~~~

Conclusion:

> The mule-deer data support an observational closed-loop phase-correction mechanism rather than a fixed universal optimum.

## New theoretical module

For any positive, continuous, strictly increasing speed response \(u(E)\) with one crossing \(u(E_*)=1\),

\[
\frac{dE}{ds}
=
\frac{1/u(E)-1}{c_e}
\]

points toward \(E_*\) on both sides.

Therefore \(E_*\) is globally asymptotically stable.

For exponential feedback

\[
u(E)=u_0e^{\kappa E},
\]

\[
E_*=-\frac{\log u_0}{\kappa},
\qquad
\ell=\frac{c_e}{\kappa}.
\]

This is now the mathematical bridge from fixed-rate PAYOFF-B to adaptive movement–phenology tracking.

## Cross-system macro target

The comparative quantities are now:

~~~text
controller gain        kappa
stable phase            E*
correction distance     ell
phase compression       beta_end,start
behavioral levers       speed / stopover / route / departure
environmental predictability
barrier structure
cue-resource coupling
~~~

The first quantitative meta-analysis is gated until at least three independent Tier A/B systems can estimate compatible controller parameters.

## Next systems

Priority:

1. barnacle geese, three flyways — environmental predictability / barriers;
2. Eurasian wigeon — migration-distance contrast;
3. red deer — jump versus surf strategies;
4. industrial-development mule deer — perturbation / mechanism break;
5. Yellowstone bison — endogenous resource-wave boundary case.

The barnacle-goose literature already establishes that three flyways differ in spring predictability and that arrival timing tracks local spring more closely where predictability is greater. The next task is to recover compatible individual/stopover-level data and translate that result into the controller coordinates.

## Publication logic

At present the cleanest structure is:

~~~text
PAYOFF-B1
exact fixed-rate theorem
-> Theoretical Ecology short paper

Movement–phenology macro paper
phase locking / feedback control
-> broad bird reanalysis
-> strong mule-deer mechanistic validation
-> independent avian replication
-> cross-system controller framework
~~~

Do not merge the macro extension into the frozen B1 manuscript.

The macro paper becomes publication-ready when at least one additional independent migration system reproduces a stabilizing phase-feedback or phase-predictability signature under a compatible measurement design.
