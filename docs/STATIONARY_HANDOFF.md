# Stationary PAYOFF empirical handoff

This document freezes the empirical interface for the recurrent-mutation layer.

The goal is not to fit `L,s,K,eta,u_SD,u_DS,beta,N` simultaneously from one stationary histogram. The quantities should be handed off from separate evidence layers wherever possible.

## 1. Required receipts

### SCH

```text
common reproductive fitness scale
conflict-active context
shared compromise geometry
conflict load L
```

### BALANCE / BITA

```text
dimensional recovery s or direct R
architecture cost K when identified
independent optimized gap phi_bridge=R-K=sL-K
```

### PAYOFF frequency game

```text
frequency-feedback eta
preferably from reciprocal endpoint contrasts or a registered p-gradient experiment
```

### finite population

```text
effective population size N
selection-intensity mapping beta
```

### recurrent mutation / conversion

```text
u_SD : S -> D transition probability per offspring/update
u_DS : D -> S transition probability per offspring/update
```

These transitions may represent literal mutation only if the biological implementation supports that interpretation. If the architecture can switch developmentally, epigenetically, or by state conversion, the rates should be named accordingly rather than automatically called genetic mutation.

---

## 2. Full stationary prediction

Given all receipts, PAYOFF predicts

```text
Pi_0,...,Pi_N
```

from the exact recurrent-mutation birth-death chain.

Primary registered summaries should include

```text
mean D frequency
boundary mass Pi_0+Pi_N
interior mass 1-Pi_0-Pi_N
mean two-type heterozygosity
stationary mode locations.
```

These are predictions, not fitting targets, when all input quantities are frozen upstream.

---

## 3. Neutral mutation control

Before interpreting a stationary polymorphism as evidence for frequency-dependent selection, compare with the exact neutral benchmark.

For `phi=eta=0` and `u_SD+u_DS<1`,

```text
alpha=N u_SD/(1-u_SD-u_DS)
beta_m=N u_DS/(1-u_SD-u_DS)
```

and the stationary count distribution is beta-binomial.

Its exact mean is

```text
E[D frequency]=u_SD/(u_SD+u_DS).
```

For symmetric mutation `u_SD=u_DS=mu`,

```text
mu_c=1/(N+2)
```

separates a mutation-only boundary-biased distribution from an interior-biased distribution.

Therefore

```text
observed interior polymorphism
!= automatically negative frequency dependence.
```

The neutral mutation benchmark is the negative control.

---

## 4. Rare-mutation stationary test

If mutation is independently demonstrated to be rare, monomorphic boundary odds obey

```text
Y=log(Pi_N/Pi_0)
 =m+beta(N-2)phi,
```

where

```text
m=log(u_SD/u_DS)
phi=sL-K.
```

A single `Y` cannot separate `m` from `phi`.

### Preferred two-size design

Hold context, `phi`, `beta`, and the mutation ratio fixed while using two effective population sizes:

```text
Y_1=m+beta(N_1-2)phi
Y_2=m+beta(N_2-2)phi.
```

Then

```text
phi_stationary
=(Y_2-Y_1)/[beta(N_2-N_1)]
```

and

```text
m
=Y_1-beta(N_1-2)phi_stationary.
```

The decisive independent comparison is

```text
phi_stationary ?= phi_bridge=sL-K.
```

This should be prospectively registered before observing the long-run occupancy data.

---

## 5. Multi-treatment regression

With more than two treatments define

```text
X_j=beta_j(N_j-2)
Y_j=log(Pi_N/Pi_0)_j.
```

Under a common `phi` and common mutation bias,

```text
Y_j=m+X_j phi.
```

Thus

```text
intercept -> mutation log-bias m
slope     -> stationary estimate of phi.
```

More than two distinct `X_j` values turn the model into an over-identified straight-line test rather than a two-point identity.

Model failure is informative: curvature or treatment-specific intercepts indicate that at least one supposedly held-fixed quantity is changing or that the rare-mutation approximation is inadequate.

---

## 6. Environmental crossing test

If upstream work predicts

```text
phi(e)=alpha(e-e0),
```

then rare-mutation equal occupancy occurs at

```text
e_occ
=e0-log(u_SD/u_DS)/[alpha beta(N-2)].
```

Therefore the observed occupancy crossing and static architecture crossing need not coincide under mutation bias.

Symmetric mutation predicts

```text
e_occ=e0.
```

This is a clean environmental validation target.

---

## 7. Claim ceiling

A stationary fit cannot by itself establish historical trait splitting, genetic mutation, or causal frequency dependence.

The strongest intended design is:

```text
upstream ecology fixes L,s,K
frequency experiment fixes eta
mutation/conversion assay fixes or constrains u_SD/u_DS
population design fixes N,beta
        |
        v
PAYOFF predicts the stationary distribution or occupancy slope
        |
        v
held-out long-run population data test the prediction.
```

This is the recurrent-mutation extension of the SCH -> BALANCE -> BITA -> PAYOFF bridge.
