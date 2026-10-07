# PAYOFF-B temporal rescue transmission

Date: **2026-10-07**  
Status: **prospective re-analysis framework; generic algebra is not claimed as a new theorem**

## 1. Biological problem

A migrant can shorten migration and arrive earlier, yet fail to advance
reproduction by the same amount if rapid migration creates a state deficit that
must be repaid after arrival.

The biological object is therefore not only:

    did arrival timing recover?

but:

    how much of the timing gain survived into the next fitness-relevant stage?

## 2. Exact stage identity

For one individual, measured from a common departure checkpoint,

\[
T_{\rm lay}
=
T_{\rm migration}
+
T_{\rm prebreed},
\]

where

- \(T_{\rm migration}\) is time from the checkpoint to breeding-site arrival;
- \(T_{\rm prebreed}\) is time from arrival to laying.

This is bookkeeping, not a new mathematical result.

## 3. Empirical transmission coefficient

Within a comparable environmental stratum, let

\[
\beta
=
\frac{dT_{\rm prebreed}}
     {dT_{\rm migration}}.
\]

Then

\[
\frac{dT_{\rm lay}}
     {dT_{\rm migration}}
=
1+\beta.
\]

Define

\[
\boxed{
\tau
=
1+\beta
}
\]

as **temporal rescue transmission**.

Interpretation:

- \(\tau=1\): variation in faster/slower migration transmits one-for-one to
  laying time;
- \(0<\tau<1\): only part of the migration timing gain survives because
  post-arrival recovery offsets the gain;
- \(\tau=0\): migration timing gain is fully absorbed by post-arrival delay;
- \(\tau<0\): faster migration is associated with more than one-for-one
  post-arrival delay;
- \(\tau>1\): migration and post-arrival timing covary in the same direction,
  potentially reflecting individual quality or another shared driver.

A causal interpretation requires stronger assumptions than this identity.

## 4. Simple state-debt model

Let a correction action \(u\ge0\) advance arrival by \(u\) days relative to a
baseline.

Suppose that correction creates physiological/resource debt

\[
D(u),
\]

and post-arrival recovery clears that debt at effective rate \(\rho>0\).

Then the induced recovery delay is

\[
P(u)=D(u)/\rho,
\]

and the change in laying time is

\[
\Delta T_{\rm lay}(u)
=
-u + \frac{D(u)}{\rho}.
\]

The marginal transmission of arrival correction to laying is

\[
\boxed{
\tau(u)
=
1-\frac{D'(u)}{\rho}.
}
\]

Thus:

- \(D'(u)<\rho\): timing rescue survives downstream;
- \(D'(u)=\rho\): marginal timing gain is fully spent repaying state debt;
- \(D'(u)>\rho\): stronger arrival correction worsens downstream reproductive
  timing.

This is a declared mechanistic witness, not a universal physiological law.

## 5. Lameris et al. 2018 anchor

The barnacle-goose system provides a direct biological motivation:

- geese did not advance temperate departure with earlier Arctic snowmelt;
- after the Baltic, they accelerated migration and skipped/shortened Arctic
  stopovers;
- breeding-site arrival advanced strongly;
- laying advanced less strongly;
- accelerated migration reduced Arctic resource acquisition;
- earlier-arriving birds in 2015 spent longer pre-breeding;
- longer pre-breeding was associated with greater use of local resources for
  egg production;
- larger reproductive mismatch was associated with lower gosling survival.

Published snowmelt slopes were approximately:

\[
b_{\rm arrival}=0.51,
\qquad
b_{\rm lay}=0.35.
\]

A descriptive environmental-response transmission is therefore

\[
\tau_{\rm snow}
=
\frac{b_{\rm lay}}{b_{\rm arrival}}
\approx
0.686.
\]

This ratio is only a published-effect summary because covariance between the
two slope estimates is not available from the reported coefficients alone.

## 6. Relationship to existing PAYOFF-B theory

This module is downstream of:

    information
      ->
    commitment
      ->
    correction.

It adds a second state dimension:

    phase correction
      ->
    state debt
      ->
    downstream recovery delay.

It therefore complements, rather than replaces:

- prediction-correction substitution;
- route-wise phase control;
- full-annual-cycle fitness closure.

The main conceptual warning is:

> phase rescue at one checkpoint can be converted into state debt that delays
> the next life-history event.

## 7. Claim boundary

Safe:

> Temporal rescue transmission quantifies how much timing variation at one
> stage is retained at the next stage after post-arrival delay.

Safe:

> In a simple state-debt witness, downstream timing rescue depends on the
> marginal debt created by correction relative to the rate at which debt can be
> repaid.

Not licensed:

> The algebra is a new general theorem of migration ecology.

Not licensed:

> A negative empirical migration-duration/pre-breeding slope is causal without
> accounting for shared environmental and individual-quality effects.

Not licensed:

> Earlier arrival necessarily improves net fitness.
