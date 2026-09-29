# PAYOFF-B greater snow goose GPS cue-uptake registration

Date: **2026-09-29**  
Status: **PREOUTCOME — registered, not executed**

## Aim

The public Movebank study `Greater snow goose migration` (study
**1442516400**) covers 75 GPS-tracked birds in 2019-2023. This creates a
prospective opportunity to test a narrower link than the full information-
deadline theorem:

> Does a bird's departure decision become more contingent on a local
> temperature cue when that cue has historically been more informative about
> later Bylot conditions?

This is a **behavioral cue-uptake proxy**. It is not a direct estimate of
(q_{wait}(D)).

## Frozen information coordinate

For each focal migration year and route context, predictive connectivity must
be estimated using climate years strictly before the focal year.

- historical window: 20 years;
- minimum paired years: 15;
- origin and Bylot series detrended separately;
- primary coordinate: signed Pearson (ho);
- target: Bylot 30 May-15 June temperature;
- secondary mapping only:
  [
  q=0.5+\arcsin(\rho)/\pi.
  ]

The 1979-2018 values published by Resendiz-Infante & Gauthier (2024) are a
sanity check, not outcome-dependent tuning.

## Frozen behavioral response

The risk set is individual × staging-context × day.

[
Y=1
]

when the bird leaves the staging context within the next 24 h and does not
return for at least 48 h; otherwise (Y=0).

The focal local cue is the 3-day mean local 2-m temperature anomaly ending on
the decision day.

The primary model is

[
\text{logit},P(Y=1)
=
\alpha
+\beta_T T
+\beta_q q
+\beta_{Tq}Tq
+\text{controls}.
]

Controls are day within the seasonal route context, wind support,
precipitation, context and year.

Primary prediction:

[
\boxed{\beta_{Tq}>0}
]

because a warm local signal should influence onward departure more strongly
when that signal has historically predicted warm/early conditions farther
north.

## Estimability gate

The primary analysis is opened only with:

- at least 30 individuals;
- at least 4 years;
- at least 3 staging contexts;
- at least 100 departure events;
- non-zero within-context variation in pre-outcome predictive connectivity;
- SD of the predictive-connectivity coordinate at least 0.03.

Failure of any gate returns `NOT_ESTIMABLE`.

## Secondary threshold-like analysis

Only after the primary model is estimable, a prespecified grid

[
q_c\in\{0.50,0.525,\ldots,0.70\}
]

may be used to ask whether temperature contingency appears only above a
particular information level.

Selection uses leave-one-individual-out predictive log loss. A threshold is
reported only if an interior candidate improves on the no-threshold model and
is separated from its adjacent grid points by the declared one-standard-error
rule. Otherwise the result is

`THRESHOLD_NOT_IDENTIFIED`.

Even a supported threshold is **not** the theorem's (q_{wait}(D)), because
the current snow-goose sources do not identify a clean opportunity cost (D).

## Why this analysis is worth doing

The published temperature analysis already shows that southern conditions are
weak predictors of later Bylot conditions, while Baffin-to-Bylot predictability
is stronger. The GPS dataset can therefore test whether behavior changes with
that information structure rather than merely documenting that the information
structure exists.

The useful evidence ladder is:

[
\text{route predictability}
\rightarrow
\text{temperature-contingent departure}
\rightarrow
\text{threshold-like uptake (if estimable)}.
]

The direct theoretical ladder remains separate:

[
D
\rightarrow
q_{wait}
\rightarrow
\text{asynchronous information use}.
]

No result from the GPS analysis may collapse these two ladders into one.
