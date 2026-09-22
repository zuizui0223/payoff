# Barnacle-goose phase-uncertainty budget receipt

Status: exploratory route-stage synthesis using direct controller estimates and
independently reconstructed spring-onset anomalies.

## Model

For one migration step,

\[
V_{i+1}
=
\lambda_i^2V_i+\sigma_{\xi,i}^2,
\]

where:

~~~text
lambda
= fraction/sign of current phase error retained after behavioral correction

sigma_xi
= SD of destination spring-timing innovation after predicting it from the
  origin spring anomaly
~~~

For a repeated homogeneous stable step,

\[
\sigma_{E,\infty}
=
\frac{\sigma_\xi}{\sqrt{1-\lambda^2}}.
\]

This is a model-derived phase-noise floor, not an observed RMSD.

## Selected stable fixed transitions

Using the registered POWER anomaly reconstruction:

| Flyway | Transition | predictability r | innovation SD (d) | lambda | |lambda| | predicted stationary phase SD (d) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Greenland | R2 -> R3 | 0.169 | 5.278 | 0.131 | 0.131 | 5.324 |
| Barents | R1 -> R2 | 0.892 | 6.190 | 0.494 | 0.494 | 7.120 |
| Barents | R1 -> R5 | -0.002 | 6.084 | -0.009 | 0.009 | 6.085 |
| Barents | R2 -> R3 | 0.950 | 3.590 | 0.538 | 0.538 | 4.261 |
| Barents | R3 -> R5 | 0.283 | 5.836 | 0.225 | 0.225 | 5.989 |

Two registered transitions have \(|\lambda|>1\) and therefore do not have a
stationary phase-noise floor under the local repeated-map approximation:

~~~text
Greenland R1 -> R2:
  lambda ~ -1.080

Barents R4 -> R5:
  lambda ~ 1.249
~~~

They are retained as route-stage amplification / boundary cases.

## What the table shows

The table illustrates why environmental predictability and behavioral feedback
cannot be represented by one scalar "tracking ability."

### Barents R2 -> R3

~~~text
environmental innovation SD ~3.59 d
lambda ~0.54
predicted phase floor ~4.26 d
~~~

The route is highly predictable, so moderate behavioral retention still yields
a relatively low uncertainty floor.

### Greenland R2 -> R3

~~~text
environmental innovation SD ~5.28 d
lambda ~0.13
predicted phase floor ~5.32 d
~~~

The environment is less predictable, but feedback nearly resets incoming phase
error.

### Barents R1 -> R5

~~~text
environmental innovation SD ~6.08 d
lambda ~0
predicted phase floor ~6.08 d
~~~

Near-complete behavioral reset cannot remove newly introduced environmental
innovation.

This is the cleanest empirical interpretation of the two-channel framework:

> **Feedback can erase inherited mismatch, but it cannot erase uncertainty that
> has not yet entered the system.**

## Revised macro prediction

Phenological precision should be predicted from both:

\[
\sigma_\xi
\quad\text{and}\quad
|\lambda|,
\]

not from either environmental predictability or behavioral responsiveness alone.

For stable systems, a first-order cross-system index is

\[
U_\phi
=
\frac{\sigma_\xi}
{\sqrt{1-\lambda^2}}.
\]

This should be treated as a predicted uncertainty budget, not as a new fitness
metric.

## Claim boundary

Licensed:

- environmental innovation and feedback retention are empirically separable;
- the registered fixed transitions occupy different combinations of the two;
- the variance recursion gives a transparent model-derived uncertainty floor.

Not licensed:

- stationarity of real migration routes;
- independence of innovations from animal state in every system;
- comparison of the predicted floor with observed arrival RMSD as a validated
  goodness-of-fit test;
- independent-effect meta-analysis of the transition rows, which share species,
  routes and individuals.
