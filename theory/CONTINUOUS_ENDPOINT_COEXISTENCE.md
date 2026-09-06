# Continuous branching closes into the original PAYOFF coexistence wedge

The continuous architecture model has one especially useful self-consistency result: once the partial-modularity singular strategy crosses the branching threshold, the protected endpoint polymorphism is not a new unrelated game. It lies exactly inside the negative-frequency coexistence phase of the original two-strategy PAYOFF model.

Assume

```text
0<alpha<kappa L
```

so the intrinsic continuous optimum is interior,

```text
r0=alpha/kappa.
```

Assume strong dissimilarity-favoring feedback,

```text
gamma<-kappa/2.
```

The continuous game uses

```text
b(r)=alpha r-(kappa/2)r^2,
H(r,q)=-gamma(r-q)^2.
```

---

## Theorem E1 — branching automatically places the endpoint subgame inside stable coexistence

For endpoint architectures

```text
S: r=0,
D: r=L,
```

the canonical two-strategy parameters are

```text
phi_end
=alpha L-(kappa/2)L^2,

eta_end
=gamma L^2.
```

Under

```text
0<alpha<kappa L
```

one has

```text
|phi_end| < (kappa/2)L^2.
```

Under

```text
gamma<-kappa/2
```

one has

```text
|eta_end| > (kappa/2)L^2.
```

Therefore

```text
|phi_end|<|eta_end|
```

with

```text
eta_end<0.
```

So the endpoint game necessarily lies in PAYOFF's strict negative-frequency stable-coexistence wedge.

### Proof

Divide `phi_end` by `L^2`:

```text
phi_end/L^2
=alpha/L-kappa/2.
```

Since `0<alpha/L<kappa`, this lies strictly between `-kappa/2` and `+kappa/2`. Thus `|phi_end|<(kappa/2)L^2`.

The branching condition gives `|gamma|>kappa/2`, hence `|eta_end|=|gamma|L^2>(kappa/2)L^2`. QED.

---

## Theorem E2 — protected endpoint frequency is exactly the PAYOFF coexistence equilibrium

Let `p_D` be differentiated-endpoint frequency. The continuous potential theorem gives

```text
p_D*
=
[2alpha-(kappa+2gamma)L]
/[-4gamma L].
```

The original two-strategy PAYOFF equilibrium gives

```text
p_D*
=(1-phi_end/eta_end)/2.
```

These expressions are identical.

Thus the continuous architecture trajectory

```text
partial architecture
-> branching threshold
-> endpoint polymorphism
```

lands exactly on the original binary PAYOFF coexistence solution.

---

## Corollary E2.1 — the branching threshold preserves the old mean recovery

Approach the threshold from the branching side:

```text
gamma -> -kappa/2 from below.
```

Then

```text
p_D* -> alpha/(kappa L)=r0/L.
```

Therefore the endpoint mixture at the threshold has mean recovery

```text
p_D* L -> r0.
```

This matches the neutral-variance theorem: at `gamma=-kappa/2`, every architecture distribution with mean `r0` has the same potential.

---

## Corollary E2.2 — strong dissimilarity feedback drives endpoint frequencies toward one half

Write

```text
h=-gamma>kappa/2.
```

Then

```text
p_D*
=1/2 + phi_end/(2hL^2).
```

Hence

```text
h -> infinity
-> p_D* -> 1/2.
```

The sign of `phi_end` determines which endpoint remains more common at finite `h`, but stronger dissimilarity reward progressively erases that intrinsic abundance asymmetry.

---

## Interpretation

This closes a loop in PAYOFF:

```text
SCH / network conflict
        |
        v
continuous recovery coordinate r
        |
        v
partial architecture r0
        |
        | gamma crosses -kappa/2
        v
architecture branching
        |
        v
protected {shared, fully differentiated} polymorphism
        |
        v
original two-strategy PAYOFF stable coexistence.
```

So the binary game is not only a coarse approximation imposed at the beginning. In the declared continuous model it reappears endogenously as the post-branching endpoint phase.

## Claim boundary

This exact closure depends on the quadratic intrinsic payoff and squared architecture-distance interaction kernel. It should not be claimed for arbitrary continuous architecture games.
