# Stochastic architecture barrier and critical introduction size

This note extends the finite-population PAYOFF Moran model from a single mutant to an arbitrary initial number of differentiated (`D`) individuals.

It addresses a practical question that the deterministic replicator equation cannot answer:

> If positive frequency dependence creates an architecture coordination barrier, how many differentiated individuals must be introduced before fixation becomes likely?

The results are exact for the declared well-mixed, self-excluding, exponential-fitness Moran process.

---

## 1. Fixation from arbitrary initial count

Let population size be `N`, differentiated count be `i`, and

```text
Delta_N(j)
= [phi(N-2)+eta(2j-N)]/(N-1).
```

Define cumulative payoff differences

```text
C_0=0,
C_k=sum_{j=1}^k Delta_N(j)
   = k[phi(N-2)+eta(k+1-N)]/(N-1).
```

Under exponential fitness `f=exp(beta*pi)`, define positive weights

```text
w_k=exp(-beta C_k),
k=0,...,N-1.
```

The probability that `D` ultimately fixates starting from `i` copies is

```text
rho_i
= [sum_{k=0}^{i-1} w_k]
  /[sum_{k=0}^{N-1} w_k],
```

with `rho_0=0` and `rho_N=1`.

Because every `w_k>0`,

```text
rho_{i+1}-rho_i
= w_i / sum_k w_k
>0.
```

Therefore fixation probability is strictly increasing with initial differentiated count.

---

## 2. Stochastic critical mass

For any target fixation probability `q` with `0<q<=1`, define

```text
m_q
= min{i in {1,...,N}: rho_i>=q}.
```

Because `rho_i` is strictly increasing, `m_q` is unique.

Equivalently, `m_q` is the first weighted quantile satisfying

```text
sum_{k=0}^{m_q-1} w_k
>= q sum_{k=0}^{N-1} w_k.
```

This makes the architecture barrier directly measurable on an individual-count scale.

At neutrality (`beta=0`), all weights equal one, so

```text
rho_i=i/N
```

and

```text
m_q=ceil(qN).
```

Thus departures of `m_q` from `ceil(qN)` quantify selection plus frequency feedback, not drift alone.

---

## 3. Finite-population drift-zero count

The finite-population selection direction changes where

```text
Delta_N(i)=0.
```

For `eta!=0`, the continuous zero-gap count is

```text
i_0
= [N-phi(N-2)/eta]/2.
```

For positive frequency dependence (`eta>0`):

```text
i<i_0  -> Delta_N(i)<0 -> selection pushes D downward,
i>i_0  -> Delta_N(i)>0 -> selection pushes D upward.
```

As `N -> infinity`,

```text
i_0/N -> p*
```

where

```text
p*=(1-phi/eta)/2
```

is the deterministic coordination threshold.

The exact finite-size relation is

```text
i_0=N p* + phi/eta.
```

Thus self-exclusion shifts the zero-drift count by an `O(1)` number of individuals while preserving the same large-population threshold.

---

## 4. Strong-selection concentration

For `eta>0`, `C_k` is a convex quadratic function of `k` because its quadratic coefficient is positive.

The fixation weights are

```text
w_k=exp(-beta C_k).
```

As `beta` increases, these weights concentrate around the integer minimizer(s) of `C_k`, located where the increments

```text
C_k-C_{k-1}=Delta_N(k)
```

change sign.

Hence the stochastic fixation curve `rho_i` becomes increasingly step-like around the finite drift-zero region. In particular, the 50% critical mass

```text
m_0.5
```

approaches the median of the minimizing integer states when the minimizer is unique/tied only locally.

This is why the deterministic coordination threshold becomes a sharp release threshold under strong selection, while finite `beta` smooths it into a probability curve.

The repository treats `m_q` itself as the exact finite-population diagnostic; the strong-selection statement is used only as interpretation.

---

## 5. Three distinct D-side barriers under positive frequency dependence

Let

```text
R=sL
phi=R-K
eta>0.
```

There are three distinct thresholds for differentiated architecture `D`.

### Barrier A — reciprocal fixation ordering

From the exact exponential-Moran ratio,

```text
rho_D/rho_S=exp[beta phi(N-2)].
```

Thus

```text
rho_D=rho_S
iff
phi=0
iff
K=R.
```

Below this cost, `D` is more likely to fix than the reciprocal `S` mutant, even if both fixation probabilities remain below neutral drift.

### Barrier B — fixation above neutral drift

Under weak selection,

```text
rho_D>1/N
iff
3phi>eta
iff
K<R-eta/3.
```

### Barrier C — positive local growth when rare

For a single `D` individual,

```text
Delta_N(1)
= [(N-2)/(N-1)](phi-eta).
```

For `N>2`, its sign is exactly the deterministic rare-invasion sign:

```text
Delta_N(1)>0
iff
phi>eta
iff
K<R-eta.
```

Since `eta>0`,

```text
R-eta < R-eta/3 < R.
```

So as architecture cost `K` falls, the transitions occur in the order

```text
K=R
  D becomes more likely to fix than reciprocal S
        |
        v
K=R-eta/3
  one D mutant becomes favored above neutral drift
        |
        v
K=R-eta
  one D mutant has positive local selection when rare.
```

This yields an important interval:

```text
R-eta < K < R-eta/3.
```

There, a lone `D` mutant is initially selected downward (`Delta_N(1)<0`) but nevertheless has fixation probability above the neutral value under weak selection.

This is the architecture-specific expression of the established one-third-law phenomenon: later frequency-dependent gains can outweigh the initial disadvantage.

Another interval is

```text
R-eta/3 < K < R.
```

where `D` has the larger reciprocal fixation probability (`rho_D>rho_S`) but its absolute single-mutant fixation probability is still below `1/N` under weak selection.

Thus

```text
relative fixation preference
!= fixation above neutrality
!= local invasion when rare.
```

---

## 6. Mirror hierarchy for shared architecture

The `S` side is obtained by `phi -> -phi`.

For `eta>0`, as `K` rises above `R`, the mirror thresholds are

```text
K=R
K=R+eta/3
K=R+eta.
```

They respectively mark

```text
rho_S>rho_D,
rho_S>1/N under weak selection,
positive local selection for rare S.
```

The full coordination region therefore contains a nested sequence of stochastic and deterministic barriers around the static architecture crossing.

---

## 7. Negative frequency dependence reverses the nesting

For `eta<0`, rare-type advantage is promoted rather than suppressed.

The D thresholds become

```text
K=R
K=R+|eta|/3
K=R+|eta|.
```

so local rare-D invasion can remain possible even when `K>R` and the static architecture gap favors `S`.

Likewise, sufficiently strong negative feedback can make both reciprocal single mutants more likely than neutral to fix:

```text
eta<-3|phi|.
```

This is the stochastic counterpart of stable deterministic coexistence.

---

## 8. Empirical use

Given estimated or manipulated values of

```text
N, beta, L, s, K, eta,
```

PAYOFF can now predict:

```text
rho_1        fixation probability from one D mutant
rho_i        fixation probability from any initial D count
m_0.5        minimum D introduction size for >=50% fixation
m_0.9        minimum D introduction size for >=90% fixation
i_0          finite-population zero-drift count.
```

The useful empirical object is therefore not just a binary statement that `D` can or cannot invade. It is a full **architecture release curve**

```text
i -> rho_i.
```

This turns the coordination barrier into a quantitative, finite-population prediction that can be tested by replicate introductions, microcosms, experimental populations, or simulation-calibrated field systems when an architecture analogue can be manipulated.

The exact fixation machinery is standard birth-death theory. PAYOFF's contribution remains the bridge from ecological compromise quantities `L,s,K` and feedback `eta` to that release curve.
