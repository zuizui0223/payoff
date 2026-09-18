# Feed-forward prediction and feedback correction are distinct phase-control channels

Status: revised synthesis after the multi-flyway barnacle-goose direct analysis.

## Motivation

The initial macro hypothesis treated environmental predictability as if it
should directly increase behavioral feedback gain.

That implication is not necessary.

A migrant can control phenological phase through two different channels:

1. **feed-forward prediction** — anticipate downstream environmental timing;
2. **feedback correction** — react to phase error after it is realized.

High predictability can improve phase precision without requiring stronger
feedback. Conversely, a poorly predictable transition can evoke strong
compensatory correction after mismatch becomes observable.

## Environmental transition

Let

\[
X_i
\]

be the environmental timing anomaly at the current stopover and

\[
Y_{i+1}
\]

the anomaly at the next one.

Write the best linear environmental forecast as

\[
Y_{i+1}
=
a_P+b_P X_i+\zeta_i,
\]

where

\[
\zeta_i
\]

is the unpredictable environmental innovation.

Useful feed-forward quantities are

\[
R_P^2
=
1-\frac{\operatorname{Var}(\zeta)}
{\operatorname{Var}(Y)}
\]

and

\[
\sigma_P
=
{\rm SD}(\zeta).
\]

Higher predictability means larger \(R_P^2\) or smaller \(\sigma_P\).

## Animal phase transition

Let \(E_i\) be animal phase error at the current decision point.

After one ecologically meaningful opportunity to correct it,

\[
E_{i+1}
=
a_C+\lambda E_i+\zeta_i+\eta_i.
\tag{FF1}
\]

Here

- \(\lambda\) is net feedback retention;
- \(\zeta_i\) is environmental forecast error;
- \(\eta_i\) represents behavioral/measurement noise not captured by the simple controller.

Interpretation:

~~~text
|lambda| ~ 1
little net feedback correction

|lambda| << 1
strong phase reset / feedback correction

lambda < 0
overshoot after correction

|lambda| > 1
local phase amplification / unstable retention
~~~

Thus environmental predictability and behavioral correction enter Eq. (FF1)
through different terms.

## Stationary variance benchmark

For a homogeneous repeated STEP process with

\[
|\lambda|<1
\]

and independent zero-mean innovations with total variance

\[
\sigma^2=\sigma_P^2+\sigma_\eta^2,
\]

the stationary phase variance is

\[
\operatorname{Var}(E)
=
\frac{\sigma^2}{1-\lambda^2}.
\tag{FF2}
\]

Therefore phase precision can improve in either of two ways:

\[
\sigma_P^2\downarrow
\quad\text{or}\quad
|\lambda|\downarrow.
\]

One does not imply the other.

## Continuous analogue

For continuous tracking near a stable phase,

\[
dE
=
-k(E-E_*)\,ds
+\sigma\,dW_s,
\]

where \(k\) is local feedback strength per unit distance.

The Ornstein–Uhlenbeck benchmark gives

\[
\operatorname{Var}(E)
\propto
\frac{\sigma^2}{2k}.
\]

Again, forcing noise and feedback strength are separate axes.

## Multi-flyway barnacle-goose result

The direct Greenland/Barents transition screen currently contains seven
fixed-transition controller estimates.

The preregistered directional hypothesis was

~~~text
higher spring predictability
-> stronger phase correction
-> smaller |lambda|
~~~

The observed exploratory association is instead

~~~text
Spearman(predictability r, 1-|lambda|)
= -0.464
p = 0.294
N transition pairs = 7
~~~

and the sign remains non-positive in every leave-one-transition-out screen.

This small, non-independent sample does not establish a negative biological
relationship.

It **does** reject using the direct-transition data as evidence that higher
predictability mechanically creates stronger feedback gain.

## Revised interpretation

The Kölzsch et al. literature result still supports:

> more predictable environmental progression is associated with more precise
> phenological arrival.

The direct-controller reconstruction now suggests that this need not occur
because the behavioral feedback slope is larger.

A more coherent interpretation is:

~~~text
predictable route:
  lower environmental innovation
  + possible anticipatory scheduling
  -> less residual error needing correction

unpredictable route:
  larger innovation
  -> feedback correction may become more important after mismatch is observed
~~~

This is an information-versus-control decomposition, not a reversal of the
published predictability result.

## Updated macro hypotheses

### H-INFO

Higher environmental predictability reduces the variance of downstream timing
innovation.

### H-FEEDBACK

Conditional on realized phase error, animals may use speed, stopover, departure
or route changes to contract error.

### H-COMPLEMENT

Feed-forward predictability and feedback correction are partially substitutable
routes to phase precision. No universal positive correlation between
predictability and feedback gain is expected.

### H-FAIL

Poor information plus weak actuation produces the largest phase mismatch.

## Comparative quantities

Each fixed transition should therefore report both:

~~~text
environment channel:
  predictability r / R2
  environmental innovation SD

controller channel:
  lambda
  |lambda|
  stopover/speed actuator gains

outcome:
  observed phase-error variance
~~~

The final comparative model should explain phase precision from both the
environmental innovation and controller retention terms rather than regressing
one against the other as if they were the same mechanism.

## Claim boundary

Eq. (FF1) and (FF2) are standard linear-control / AR(1) organization, not
claimed as new mathematics.

The candidate ecological contribution is applying the decomposition to
phenological migration across empirically different actuator architectures.
