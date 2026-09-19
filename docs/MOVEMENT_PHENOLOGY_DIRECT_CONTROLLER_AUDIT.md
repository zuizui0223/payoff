# Direct-controller registry audit

Status: descriptive synthesis of registered direct movement–phenology controller
estimates.

## Common cross-system quantity

Actuator coefficients are not directly interchangeable:

~~~text
mule deer:
  speed gain + stopover response

barnacle geese:
  discrete stopover response
~~~

The common response is instead the fraction of phase error retained after one
ecologically meaningful correction opportunity:

\[
R_\phi=|\lambda|.
\]

Define

\[
C_\phi=1-|\lambda|
\]

as phase-correction strength.

This gives a common scale without pretending that speed gain and stopover gain
are the same behavioral parameter.

## Registered primary direct rows

~~~text
mule deer, full spring migration:
  lambda =  0.107
  |lambda| = 0.107

Svalbard barnacle goose, southern Norway -> Svalbard:
  lambda = -0.106
  |lambda| = 0.106

Greenland barnacle goose, R2 -> R3:
  lambda =  0.131
  |lambda| = 0.131

Barents barnacle goose, R1 -> R2:
  lambda =  0.494
  |lambda| = 0.494
~~~

All four highlighted maps are in the stable contraction regime

\[
|\lambda|<1.
\]

The biological actuator differs, but each system/route transmits substantially
less than the full incoming phase error.

## Gate interpretation

Current direct evidence is:

~~~text
direct population/route rows = 4
taxa represented             = 2
stable primary maps          = 4/4
~~~

Therefore:

~~~text
population/route replication gate = PASS
three-taxon generality gate       = OPEN
~~~

The next direct taxon is Eurasian wigeon.

## Why not meta-analyze these four rows yet

The three goose rows are not three independent taxa and the underlying route
transitions arise from related analyses of the same species and source paper.

The current registry is appropriate for:

- mechanism comparison;
- controller architecture comparison;
- descriptive phase-retention ranges;
- designing a third-taxon analysis.

It is not yet appropriate for a conventional cross-study random-effects
meta-analysis.

## Claim boundary

The registered values support a common phase-retention coordinate across
continuous and discrete controllers.

They do not establish a universal \(\lambda\), a universal correction fraction,
or independence of the four direct rows.
