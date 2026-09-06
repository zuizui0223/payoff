# Common temporal environmental forcing: an exact null theorem

The spatial PAYOFF invasion operator for rare differentiated architecture at a reference environment is

```text
A_D0
= diag(phi_j0-eta_j)-mL_G.
```

Suppose environmental variation acts identically on every patch by adding a scalar time-dependent shift

```text
q(t)
```

to all static architecture gaps. Then

```text
A_D(t)=A_D0+q(t)I.
```

Rare shared architecture receives the opposite environmental shift:

```text
A_S(t)=A_S0-q(t)I.
```

This is the simplest temporal extension and should be used as a negative control before attributing effects to environmental fluctuations themselves.

---

## Theorem 1 — exact factorization of finite-time growth

Because

```text
q(t)I
```

commutes with every matrix, the fundamental solution for rare D factorizes exactly:

```text
X_D(t)
= exp[integral_0^t q(s) ds]
  exp[A_D0 t].
```

For rare S,

```text
X_S(t)
= exp[-integral_0^t q(s) ds]
  exp[A_S0 t].
```

### Proof

Define

```text
Q(t)=integral_0^t q(s)ds.
```

Set

```text
x(t)=exp[Q(t)]y(t).
```

Then

```text
x_dot
= q(t)exp[Q]y+exp[Q]y_dot.
```

Substituting into

```text
x_dot=[A_D0+q(t)I]x
```

cancels the scalar forcing term and leaves

```text
y_dot=A_D0y.
```

Hence

```text
y(t)=exp[A_D0t]y(0),
```

which gives the factorization. The rare-S case follows with `q -> -q`. QED.

---

## Theorem 2 — temporal invasion exponent depends only on the mean scalar shift

Let

```text
Lambda_D0=lambda_max(A_D0),
Lambda_S0=lambda_max(A_S0).
```

If the long-time temporal mean exists,

```text
q_bar
= lim_{T->infinity} (1/T) integral_0^T q(t)dt,
```

then the asymptotic reciprocal invasion exponents are exactly

```text
Lambda_D,temporal
= Lambda_D0+q_bar,

Lambda_S,temporal
= Lambda_S0-q_bar.
```

### Consequence

Two temporal sequences with the same time-average scalar shift have identical asymptotic rare-architecture invasion exponents, regardless of:

```text
amplitude,
variance,
period,
season ordering,
or temporal autocorrelation.
```

Those features can affect only transient multiplicative trajectories, not the long-run exponent, under this common additive forcing model.

---

## Corollary 2.1 — zero-mean fluctuations have exactly zero invasion effect

If

```text
q_bar=0,
```

then

```text
Lambda_D,temporal=Lambda_D0,
Lambda_S,temporal=Lambda_S0.
```

Thus arbitrary common temporal fluctuations around zero mean cannot rescue or suppress a rare architecture in this model.

This is an exact null result, not a weak-noise approximation.

It gives a sharp diagnostic:

> If zero-mean temporal variability changes long-run architecture invasion in data or simulation, at least one assumption of common additive forcing is false.

Possible failures include patch-specific environmental slopes, nonlinear environmental response, time-varying `eta`, time-varying movement, density dependence, or other noncommuting mechanisms.

---

## Corollary 2.2 — common linear environmental forcing obeys a mean-environment rule

Let

```text
q(t)=alpha[e(t)-e0].
```

Then

```text
q_bar
= alpha[e_bar-e0],
```

so

```text
Lambda_D,temporal
= Lambda_D0+alpha(e_bar-e0),

Lambda_S,temporal
= Lambda_S0-alpha(e_bar-e0).
```

Only the time-averaged environment enters.

The temporal rare-D neutral condition is

```text
e_bar
= e0-Lambda_D0/alpha,
```

which is exactly the static spatial critical environment derived in `SPATIAL_ENVIRONMENTAL_THRESHOLDS.md`.

Therefore, under common linear forcing,

```text
static environment threshold
=
time-average temporal threshold.
```

---

## Corollary 2.3 — the reciprocal threshold width is unchanged by zero-mean temporal variability

The reciprocal exponent sum is

```text
Lambda_D,temporal+Lambda_S,temporal
= Lambda_D0+Lambda_S0.
```

The scalar temporal shift cancels exactly.

Thus common temporal environmental forcing moves the D and S invasion exponents in opposite directions but does not change the signed reciprocal-invasion versus coordination width at fixed migration.

Environmental variance cannot widen or narrow that reciprocal window under the declared common additive model.

---

## 3. Seasonal piecewise-constant form

For seasons `l=1,...,M` with durations `tau_l` and common shifts `q_l`, total period

```text
T=sum_l tau_l.
```

The exact log growth multiplier along any eigenmode of the baseline operator with exponent `lambda` is

```text
log M
= lambda T + sum_l q_l tau_l.
```

Hence the per-time exponent is

```text
lambda + [sum_l q_l tau_l]/T.
```

Season order does not matter because all seasonal environmental corrections are scalar identity matrices and commute.

---

## 4. Why this null theorem matters

Temporal ecology often generates variance or ordering effects because nonlinear growth maps and noncommuting state transitions create geometric-mean or Floquet phenomena.

PAYOFF's common additive environmental forcing deliberately removes those mechanisms. It therefore supplies a registered negative control:

```text
common additive temporal shift
-> mean effect only;

observed variance/order effect
-> evidence for a richer temporal mechanism.
```

The next temporal model should only be introduced after this null baseline is rejected or biologically inappropriate.

---

## 5. What can generate a genuine temporal effect beyond the mean?

At least one of the following is sufficient to break the scalar-commuting structure:

```text
patch-specific slopes alpha_j,
time-varying migration graph or migration rate,
time-varying eta_j,
nonlinear phi_j(e),
season-dependent architecture costs K_j,
season-dependent recovery s_jL_j,
density-dependent demographic coupling.
```

Then the seasonal operators need not commute, and long-run growth is determined by products of matrix exponentials / a Floquet or Lyapunov exponent rather than by a simple time average.

---

## 6. Claim boundary

Commuting linear systems, Floquet theory, and the fact that a scalar identity shift adds its time average to a Lyapunov exponent are standard linear-systems mathematics.

PAYOFF's contribution is the architecture interpretation of the baseline operator

```text
A_D0
= diag(s_jL_j-K_j-eta_j)-mL_G
```

and the resulting falsifiable null prediction for temporal ecological variation.
