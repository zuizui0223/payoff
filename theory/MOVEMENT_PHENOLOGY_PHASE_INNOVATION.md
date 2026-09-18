# Phase innovation and controller memory

Status: mathematical synthesis for the movement–phenology macro programme. The variance recursion is elementary AR(1)/control algebra and is **not** claimed as a novel theorem by itself.

## Why predictability and feedback must be separated

The initial macro hypothesis treated environmental predictability as though it should directly increase behavioral feedback gain.

The multi-flyway barnacle-goose screen does not support that simple monotonic coupling.

This suggests two distinct channels:

~~~text
feed-forward / information channel
  how well can the timing of the next environment be predicted?

feedback / actuation channel
  how much of current phase error remains after one opportunity to correct it?
~~~

A route can therefore have:

~~~text
high predictability + weak behavioral correction
low predictability  + strong behavioral correction
high predictability + strong correction
low predictability  + weak correction
~~~

and these should not be collapsed into one parameter.

## Linearized phase map with environmental innovation

Let

\[
E_i=A_i-T_i
\]

be animal arrival time minus environmental onset at stage \(i\).

Let \(E_i^*\) be the route-stage-specific target phase and define centered phase error

\[
e_i=E_i-E_i^*.
\]

After one behavioral correction opportunity, linearize the animal-side controller as

\[
e_i^{\rm beh}=\lambda_i e_i,
\]

where

\[
\lambda_i
=
\frac{dE_{i+1}}{dE_i}
\]

is the net phase-retention coefficient.

Now let

\[
\xi_i
\]

be the unpredictable component of destination environmental timing after conditioning on the environmental information available at stage \(i\).

Because a later-than-predicted destination spring shifts \(E=A-T\) downward, the coupled map is

\[
e_{i+1}
=
\lambda_i e_i-\xi_i.
\tag{I1}
\]

The sign of \(\xi_i\) does not affect the variance results below.

## Mean dynamics

If

\[
\mathbb E[\xi_i]=0,
\]

then

\[
\mathbb E[e_{i+1}]
=
\lambda_i\mathbb E[e_i].
\]

Thus behavioral phase retention controls persistence of systematic error.

Environmental predictability controls the stochastic disturbance entering the next stage.

These are logically separate effects.

## Phase-uncertainty budget

Assume \(\xi_i\) is independent of \(e_i\) with variance

\[
\sigma_{\xi,i}^2.
\]

Then

\[
V_{i+1}
=
\lambda_i^2 V_i+\sigma_{\xi,i}^2,
\tag{I2}
\]

where

\[
V_i=\operatorname{Var}(e_i).
\]

Equation (I2) is the route-level phase-uncertainty budget.

It cleanly decomposes next-stage phase variance into:

~~~text
retained previous phase uncertainty:
  lambda_i^2 * V_i

new environmental innovation:
  sigma_xi,i^2
~~~

## Constant-route special case

For constant \(\lambda\) and innovation variance \(\sigma_\xi^2\),

\[
V_n
=
\lambda^{2n}V_0
+
\sigma_\xi^2
\frac{1-\lambda^{2n}}{1-\lambda^2},
\qquad |\lambda|<1.
\tag{I3}
\]

The stationary phase variance is

\[
V_\infty
=
\frac{\sigma_\xi^2}{1-\lambda^2}.
\tag{I4}
\]

Therefore the stationary phase standard deviation is

\[
\sigma_{E,\infty}
=
\frac{\sigma_\xi}{\sqrt{1-\lambda^2}}.
\tag{I5}
\]

This quantity is a useful **phase-noise floor**.

## Interpretation

Equation (I5) resolves an apparent contradiction.

A highly predictable route can show precise phenological arrival even if its behavioral feedback gain is not unusually strong, because \(\sigma_\xi\) is small.

Conversely, strong behavioral correction can coexist with substantial residual mismatch if environmental innovation is large.

Hence:

> **Environmental predictability need not increase controller gain to improve phenological precision.**

It can act by reducing disturbance variance.

## Environmental innovation from paired phenology anomalies

For two successive regions, let

\[
X_i
\]

be the origin-year spring anomaly and

\[
Y_i
\]

the destination-year spring anomaly.

Fit

\[
Y_i=a+bX_i+\xi_i.
\]

Then

\[
\sigma_\xi
=
\operatorname{SD}(\xi_i)
\]

is a direct environmental innovation scale in days.

Correlation \(r\) or \(R^2\) remains useful descriptively, but \(\sigma_\xi\) is preferable for the uncertainty budget because it retains units of phenological days.

## Route-level propagation

For a sequence of stages with different controller strengths and innovation scales,

\[
V_{i+1}
=
\lambda_i^2V_i+\sigma_{\xi,i}^2
\]

can be iterated exactly.

This gives a route-specific prediction for where phase uncertainty should:

~~~text
contract
remain stable
or inflate
~~~

without assuming one global controller gain.

## Relation to empirical systems

### Svalbard barnacle geese

Direct reconstruction estimates a strong STEP controller in southern Norway, while the original study and the modern POWER reconstruction characterize environmental timing relationships among regions.

The two quantities should be entered separately into Eq. (I2).

### Mule deer

The mule-deer analysis estimates behavioral feedback directly. A comparable environmental innovation term can be constructed from interannual green-wave propagation variability.

### Broad bird front data

The weak universal signal in the 55-species analysis is compatible with large heterogeneity in both \(\lambda\) and \(\sigma_\xi\).

Pooling species without separating these channels can erase strong within-system control.

## Revised macro hypotheses

### I1 — environmental information

Higher environmental predictability reduces

\[
\sigma_\xi,
\]

not necessarily \(|\lambda|\).

### I2 — behavioral correction

Stronger phase correction reduces

\[
|\lambda|.
\]

### I3 — phase precision

Observed phenological precision depends jointly on both:

\[
\sigma_E
\sim
f(\sigma_\xi,|\lambda|).
\]

### I4 — perturbation

Barriers or disturbance that attenuate behavioral actuation should increase \(|\lambda|\) even if \(\sigma_\xi\) is unchanged.

### I5 — environmental change

Climate change can degrade tracking either by:

~~~text
increasing environmental innovation sigma_xi
or
shifting the target phase / controller architecture
~~~

without requiring a decline in the animal's intrinsic movement capacity.

## Claim boundary

Licensed:

- information and feedback are mathematically distinct channels;
- Eq. (I2) gives their exact variance decomposition under the stated linearization and independence assumptions;
- a simple positive correlation between predictability and behavioral feedback gain is not required for predictable routes to show better phase precision.

Not licensed:

- independence of environmental innovations from animal phase error in every natural system;
- Gaussian phase errors;
- universal stationarity;
- a claim that the AR(1) variance formula itself is mathematically novel.

The scientific contribution would be empirical demonstration that this decomposition organizes heterogeneous migration systems better than a single mismatch or speed-ratio metric.
