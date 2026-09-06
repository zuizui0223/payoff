# Neutral recurrent-mutation benchmark

This note gives an exact negative-control benchmark for the recurrent-mutation PAYOFF model.

Set game selection to neutral:

```text
phi=0,
eta=0.
```

Fitness is then equal for the two architectures, so the stationary distribution is driven only by drift and offspring mutation.

Let

```text
u = u_SD
v = u_DS
q = 1-u-v.
```

Assume

```text
u>0,
v>0,
u+v<1.
```

---

## Theorem 1 — exact neutral beta-binomial stationary law

With `i` differentiated individuals in a population of size `N`, neutral parent sampling gives

```text
P(parent D)=i/N.
```

After mutation, the offspring is `D` with probability

```text
b_D(i)
= (i/N)(1-v)+(1-i/N)u
= [uN+qi]/N.
```

Similarly,

```text
b_S(i)
= [vN+q(N-i)]/N.
```

Therefore

```text
T_i^+
= [uN+qi](N-i)/N^2,

T_i^-
= [vN+q(N-i)]i/N^2.
```

Define

```text
alpha = Nu/q,
beta_m = Nv/q.
```

Detailed balance gives

```text
Pi_i/Pi_{i-1}
= [(N-i+1)/i]
  [(alpha+i-1)/(beta_m+N-i)].
```

This is exactly the adjacent-ratio formula of a beta-binomial distribution:

```text
Pi_i
propto C(N,i)
        (alpha)_i
        (beta_m)_(N-i),
```

where `(x)_k` is the rising factorial, with the usual normalization by `(alpha+beta_m)_N`.

Hence the neutral recurrent-mutation PAYOFF stationary distribution is exactly beta-binomial.

### Proof

Substitute the neutral transition probabilities into

```text
Pi_i/Pi_{i-1}=T_{i-1}^+/T_i^-.
```

The result is

```text
Pi_i/Pi_{i-1}
= [(N-i+1)/i]
  [uN+q(i-1)]/[vN+q(N-i)].
```

Factor `q` from numerator and denominator and use the definitions of `alpha` and `beta_m`. The resulting recurrence is the beta-binomial recurrence, which uniquely determines the normalized distribution. QED.

---

## Corollary 1.1 — exact neutral mean architecture frequency

For a beta-binomial distribution,

```text
E[i/N]
= alpha/(alpha+beta_m).
```

Therefore

```text
E[i/N]
= u/(u+v).
```

So under neutral selection the long-run mean differentiated frequency is determined exactly by mutation bias, independent of population size `N` and independent of the total mutation rate except through the ratio `u:v`.

In particular,

```text
u=v
-> E[i/N]=1/2.
```

This provides a direct neutral control for interpreting stationary architecture asymmetry.

---

## Theorem 2 — exact symmetric mutation shape threshold

Set

```text
u=v=mu,
0<mu<1/2.
```

Then

```text
alpha=beta_m=theta
```

with

```text
theta
= mu N/(1-2mu).
```

The stationary adjacent ratio is

```text
Pi_i/Pi_{i-1}
= [(N-i+1)/i]
  [(theta+i-1)/(theta+N-i)].
```

The distribution has three regimes:

```text
theta<1  -> boundary-biased / U-shaped,
theta=1  -> exactly uniform over i=0,...,N,
theta>1  -> interior-biased with central mode(s).
```

The exact mutation threshold is obtained from `theta=1`:

```text
mu N/(1-2mu)=1
```

so

```text
mu_c = 1/(N+2).
```

Therefore

```text
mu < 1/(N+2)
-> neutral stationary mass is biased toward homogeneous architecture states,

mu = 1/(N+2)
-> Pi_i=1/(N+1) for every architecture count,

mu > 1/(N+2), mu<1/2
-> neutral stationary mass is biased toward mixed architecture states.
```

### Proof

At `theta=1`,

```text
Pi_i/Pi_{i-1}
= [(N-i+1)/i]
  [i/(N-i+1)]
=1
```

for all `i`, so the stationary distribution is uniform.

For `theta<1`, the first ratio is

```text
Pi_1/Pi_0
= N theta/(N-1+theta)<1,
```

and by symmetry the distribution decreases from both boundaries toward the center, producing a U shape.

For `theta>1`, the inequality reverses at the boundary and symmetry places the maximum at the center (one central state for even `N`, two adjacent central states for odd `N`). Solving `theta=1` gives `mu_c=1/(N+2)`. QED.

---

## Interpretation for PAYOFF

This result is not a new general mutation theorem. Neutral mutation-drift stationary distributions and mutation thresholds in finite Moran systems are established theory.

Its value here is as a **registered negative control**:

```text
neutral baseline:
    stationary shape explained by N and mutation alone

PAYOFF game:
    deviations from that baseline attributed to phi and eta only
    after mutation mechanism and rates are held fixed.
```

The threshold

```text
mu_c=1/(N+2)
```

therefore marks the mutation-only point at which a finite population changes from spending more long-run time near homogeneous architecture states to spending more time at mixed architecture counts.

Any claimed selection-driven coordination or coexistence signature should be compared against this neutral mutation benchmark rather than against a mutation-free model.

---

## Empirical use

A stationary architecture-frequency experiment should report at minimum

```text
N,
u_SD,
u_DS,
observed stationary count distribution.
```

The neutral prediction is then fixed before fitting `phi` or `eta`:

```text
alpha=Nu_SD/(1-u_SD-u_DS)
beta_m=Nu_DS/(1-u_SD-u_DS).
```

Only residual departures from that beta-binomial benchmark should be used as evidence for architecture selection or frequency-dependent ecological feedback.
