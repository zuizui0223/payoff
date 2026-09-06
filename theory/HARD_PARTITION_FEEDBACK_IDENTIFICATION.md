# Hard-partition feedback identification — estimate `gamma` from reciprocal architecture invasions

The hard-partition population game uses

```text
H(P,Q)=-gamma q(P,Q),
```

where `q(P,Q)` is known once the two module partitions and pair weights are fixed.

This makes the frequency-feedback scale `gamma` empirically identifiable from endpoint population contrasts rather than a free tuning parameter.

---

## 1. Pairwise canonical game

For partitions `P` and `Q`, let

```text
phi_PQ=b(Q)-b(P),
eta_PQ=gamma q(P,Q).
```

If `p` is frequency of `Q`, the pairwise payoff gap is

```text
Delta_PQ(p)
=phi_PQ+eta_PQ(2p-1).
```

Measure or estimate the endpoint gaps

```text
Delta_0=Delta_PQ(0)
```

and

```text
Delta_1=Delta_PQ(1).
```

Then

```text
Delta_0=phi-eta,
Delta_1=phi+eta.
```

---

## Theorem HPFI1 — endpoint inversion identifies `phi`, `eta`, and `gamma`

The pairwise parameters are

```text
phi_obs
=(Delta_0+Delta_1)/2,
```

```text
eta_obs
=(Delta_1-Delta_0)/2.
```

For distinct partitions with

```text
q(P,Q)>0,
```

the distance-feedback coefficient is

```text
gamma_obs
=eta_obs/q(P,Q).
```

### Architecture bridge check

The independently generated hard-partition landscape predicts

```text
phi_arch
=b(Q)-b(P).
```

Therefore

```text
delta_phi
=phi_obs-phi_arch
```

is a population-to-architecture bridge residual.

The same endpoint experiment can thus test two things separately:

```text
frequency-independent pair difference
phi_obs ?= phi_arch;

frequency-feedback scale
gamma_obs.
```

---

## 2. Reciprocal invasion-margin form

Instead of `Delta_1`, one may record the reciprocal rare-architecture invasion margins

```text
I_Q
= Q invading P
=Delta_0,
```

```text
I_P
= P invading Q
=-Delta_1.
```

Then

```text
phi_obs
=(I_Q-I_P)/2,
```

```text
eta_obs
=-(I_Q+I_P)/2,
```

and

```text
gamma_obs
=-(I_Q+I_P)/(2q).
```

This is often the more natural biological design because both quantities are measured as rare-type growth in reciprocal resident backgrounds.

---

## Theorem HPFI2 — multiple partition pairs overidentify a common distance-feedback scale

For pair `j`, let

```text
q_j>0
```

and endpoint-derived

```text
eta_j.
```

The common-kernel model predicts

```text
eta_j=gamma q_j.
```

Thus every pair yields

```text
gamma_j=eta_j/q_j.
```

If one common `gamma` is assumed across partition pairs, multiple reciprocal experiments overidentify that assumption.

With positive analysis weights `w_j`, the zero-intercept weighted least-squares estimate is

```text
gamma_hat
=
[sum_j w_j q_j eta_j]
/
[sum_j w_j q_j^2].
```

The pair residual is

```text
r_j
=eta_j-gamma_hat q_j.
```

A systematic residual pattern means partition distance alone is insufficient to explain the observed frequency feedback.

---

## 3. Registered three-function example

At hard-module cost

```text
kappa=1,
```

the `M-F` pair has

```text
b_M=19/6,
b_F=8/3,
q(M,F)=1.
```

Take registered population coefficient

```text
gamma=-1.
```

Then

```text
phi=-1/2,
eta=-1.
```

so endpoint payoff gaps are

```text
Delta_0
=phi-eta
=1/2,
```

```text
Delta_1
=phi+eta
=-3/2.
```

Inverting them gives

```text
phi_obs=-1/2,
eta_obs=-1,
gamma_obs=-1.
```

The frequency-independent result exactly matches the architecture-predicted

```text
b_F-b_M=-1/2.
```

For the `S-M` pair under the same `gamma`,

```text
q(S,M)=2,
eta=-2.
```

so both pairs return the same

```text
gamma=-1.
```

This is a software/theory fixture, not empirical evidence for one common biological feedback coefficient.

---

## 4. Cross-repository identification chain

A strong design can now freeze both architecture and population parameters independently:

```text
SCH
-> theta_i,a_i
-> hard partition recoveries

BALANCE direct worldlines
-> identify kappa
-> freeze intrinsic b(P)

PAYOFF reciprocal population experiment
-> Delta_0,Delta_1 for selected partition pairs
-> identify gamma

held-out pair
-> predict phi from b differences
-> predict eta=gamma q
-> predict invasion / coexistence / coordination
-> test without refitting.
```

---

## 5. Claim boundary

The endpoint inversion is algebra for a linear two-strategy frequency game. The substantive biological assumption is that one common distance kernel

```text
eta_PQ=gamma q(P,Q)
```

applies across the compared partitions.

Appropriate interpretation:

> Given a declared partition-distance kernel, reciprocal invasion contrasts identify its frequency-feedback coefficient and allow an independent check of the architecture-predicted intrinsic payoff difference.

Do not assume one common `gamma` across unrelated biological contexts without testing it.
