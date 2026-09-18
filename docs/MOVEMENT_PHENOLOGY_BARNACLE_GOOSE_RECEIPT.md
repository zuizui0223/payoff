# Barnacle-goose predictability evidence receipt

Status: **independent literature-derived Tier-C evidence**. This receipt does not estimate controller gain \(\kappa\) because a compatible continuous relative-speed response has not yet been reconstructed from the raw tracks.

Source: Kölzsch et al. (2015), *Journal of Animal Ecology* 84:272–283, DOI 10.1111/1365-2656.12281.

Published Movebank datasets:

~~~text
Greenland: 10.5441/001/1.5d3f0664
Svalbard:  10.5441/001/1.5k6b1364
Barents:   10.5441/001/1.ps244r11
~~~

## Design

The study tracked 40 barnacle geese across three flyways:

~~~text
Greenland N = 7
Svalbard N = 21
Barents Sea N = 12
~~~

Stopover sites were grouped into 16 general regions.

Environmental predictability between successive stopover regions was represented by:

~~~text
r = correlation of onset-of-spring anomalies between regions
s = proportionality index (SMA slope) of those anomalies
~~~

Goose phase error was arrival date relative to local onset of spring.

## Evidence 1 — environmental predictability varies across route structure

The paper reports that phenology correlation and proportionality differed strongly across ecological barriers:

~~~text
phenology correlation r:
  barrier single-term deletion P = 0.006

proportionality index s:
  barrier single-term deletion P < 0.001
~~~

Examples:

~~~text
Greenland land-connected segments:
  southern -> northern Iceland r = 0.85
  southern -> northern Greenland r = 0.50

Greenland sea crossings:
  Ireland -> southern Iceland r = -0.10
  northern Iceland -> southern Greenland r = -0.33

Svalbard consecutive regions:
  0.45 < r < 0.81

Barents Sea:
  Central Europe / Sweden / Baltics 0.78 < r < 0.97
  Baltics -> White Sea r = 0.39, s = 0.48
~~~

Thus the route provides a natural environmental-predictability contrast.

## Evidence 2 — more predictable routes have smaller phase mismatch

At the stopover-region level, better arrival/onset-of-spring fit was associated with higher phenology correlation:

~~~text
RMSD model:
  drop r -> P = 0.03
~~~

The paper reports a negative relationship between phenology correlation and individual arrival deviation:

~~~text
P < 0.001
R^2 approximately 0.07
~~~

Predictability expressed as the proportionality index showed a clearer nonlinear relationship with arrival timing; arrival was closest to local onset of spring when predictability was high, around 0.8–1.

In the integrated mixed model with individual and year as random effects:

~~~text
proportionality index s:
  LR = 8.41
  P = 0.004

width of onset-of-spring peak:
  LR = 14.49
  P < 0.001

flyway:
  LR = 15.65
  P < 0.001

breeding status:
  LR = 7.22
  P = 0.007
~~~

This supplies independent support for the macro hypothesis that predictable environmental progression permits tighter phenological phase control.

## Evidence 3 — barrier presence is not the direct performance predictor

Although ecological barriers reduce environmental predictability, barrier presence itself is not retained as an important predictor of goose arrival mismatch once the environmental variables are modeled.

For stopover-region RMSD:

~~~text
barrier P = 0.19
~~~

In the integrated individual mixed model:

~~~text
barrier P = 0.20
distance between sites P = 0.51
distance to breeding site P = 0.22
phenology correlation r P = 0.64
proportionality index s P = 0.004
~~~

This refines the macro hypothesis:

> Barriers matter primarily insofar as they alter the predictability or usable propagation of environmental information; a binary barrier label is not itself the controller variable.

## Evidence 4 — stable phase is route-position dependent

The geese do not maintain zero lag throughout migration.

Published examples include:

~~~text
southern Iceland:
  RMSD = 21.2 d
  birds generally after spring onset

northern Iceland:
  RMSD = 11.3 d

Greenland sites:
  RMSD = 25.6 and 24.9 d
  birds generally before spring onset

White Sea:
  RMSD = 5.9 d
  close tracking of spring onset

Barents Arctic sites:
  RMSD roughly 7.9–16.0 d
~~~

Across flyways, birds tended to arrive after spring onset at early migration stages and before spring onset near breeding sites.

This is consistent with the phase-locking framework in one important respect: **the biologically relevant phase offset is not universally zero and can change systematically with migration stage and life-history objective.**

It also shows the limit of the simplest single-\(E_*\) controller model: capital breeders can deliberately overtake the green wave near breeding grounds.

## Cross-system interpretation

Together with the mule-deer result:

~~~text
mule deer:
  strong behavioral phase-error feedback
  -> speed up + reduce stopover when late

barnacle geese:
  phase precision improves when downstream spring is predictable
  -> environmental information controls how tightly phase can be maintained
~~~

These are complementary pieces of the proposed controller framework:

\[
\text{phase error}
\rightarrow
\text{behavioral correction}
\]

requires usable information about the future resource wave.

## Claim boundary

Licensed:

- environmental predictability differs strongly among route segments and flyways;
- published goose arrival mismatch is lower under higher spring predictability;
- the proportionality/predictability index remains significant in the integrated individual/year mixed model;
- a simple ecological-barrier indicator is not itself a strong arrival-mismatch predictor;
- phase offsets change along the route, so universal zero lag is inappropriate.

Not licensed:

- a new reanalysis of raw GPS tracks;
- a direct estimate of \(\kappa\), \(E_*\), or \(\ell\);
- causal proof that predictability is used as a cue;
- a claim that barnacle geese obey the same controller law as mule deer.

## Promotion rule

This system moves from Tier C to Tier A when the published Movebank tracks and environmental timing surfaces are reconstructed on a common route coordinate so that segment-level relative speed and signed phase error can be estimated directly.
