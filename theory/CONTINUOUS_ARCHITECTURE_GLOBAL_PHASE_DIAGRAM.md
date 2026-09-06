# Global phase diagram of the continuous architecture game

The local branching theorem focuses on systems whose intrinsic architecture optimum is partial. The quadratic continuous game actually admits a complete global phase diagram over the net marginal recovery value `alpha` and architecture-distance feedback `gamma`.

Recall

```text
r in [0,L],
b(r)=alpha*r-(kappa/2)r^2,
H(r,q)=-gamma(r-q)^2,
kappa>0.
```

For a population distribution with mean `mu` and variance `sigma2`, the symmetric-game potential is

```text
V
=2alpha mu
-kappa mu^2
-(kappa+2gamma)sigma2.
```

Define

```text
c=kappa+2gamma.
```

---

## Region I — variance-penalizing ecology: c>0

When

```text
gamma>-kappa/2,
```

variance lowers potential. The global optimum is therefore monomorphic at

```text
r*=clip(alpha/kappa,0,L).
```

This gives the three intrinsic architecture phases:

```text
alpha<=0
-> shared endpoint r=0;

0<alpha<kappa L
-> one partial architecture r=alpha/kappa;

alpha>=kappa L
-> fully differentiated endpoint r=L.
```

---

## Region II — variance-neutral threshold: c=0

At

```text
gamma=-kappa/2,
```

potential is independent of architecture variance at fixed mean.

The optimal mean is still

```text
mu*=clip(alpha/kappa,0,L).
```

If the mean is interior, every distribution with that mean has equal maximal potential.

Thus the threshold segment

```text
0<alpha<kappa L
```

is an exact neutral-variance manifold between the monomorphic partial phase and the endpoint-polymorphism phase.

At `alpha<=0` or `alpha>=kappa L`, the optimal mean is already an endpoint, so the only feasible zero-variance optimum remains the corresponding pure endpoint.

---

## Region III — variance-rewarding ecology: c<0

When

```text
gamma<-kappa/2,
```

potential is maximized by the largest feasible variance at each mean. Hence every global optimum is supported on the endpoints

```text
{0,L}.
```

Let `p` be the frequency of `r=L`. Then

```text
mu=pL,
sigma2=p(1-p)L^2.
```

The endpoint-mixture potential is a strictly concave quadratic in `p`, and the unconstrained optimum is

```text
p_raw
=
[2alpha-(kappa+2gamma)L]
/[-4gamma L].
```

The constrained optimum is

```text
p*=clip(p_raw,0,1).
```

---

## Theorem GP1 — exact endpoint phase boundaries under strong dissimilarity feedback

For

```text
gamma<-kappa/2,
```

define

```text
alpha_S(gamma)
=[(kappa+2gamma)L]/2,

alpha_D(gamma)
=[(kappa-2gamma)L]/2.
```

Then:

```text
alpha <= alpha_S
-> p*=0
-> pure shared endpoint;

alpha_S < alpha < alpha_D
-> 0<p*<1
-> protected shared/differentiated endpoint polymorphism;

alpha >= alpha_D
-> p*=1
-> pure fully differentiated endpoint.
```

### Proof

The denominator of `p_raw` is positive because `gamma<0`. Therefore `p_raw>0` iff

```text
2alpha-(kappa+2gamma)L>0,
```

which is `alpha>alpha_S`.

Likewise `p_raw<1` iff

```text
2alpha-(kappa+2gamma)L<-4gamma L,
```

or

```text
alpha<[(kappa-2gamma)L]/2=alpha_D.
```

Outside those bounds the clipped optimum is the corresponding endpoint. QED.

---

## Corollary GP1.1 — the branching line joins continuously to the intrinsic phase boundaries

At

```text
gamma=-kappa/2,
```

the strong-feedback boundary formulas become

```text
alpha_S=0,
alpha_D=kappa L.
```

These are exactly the no-feedback shared/partial and partial/full boundaries.

Thus the phase diagram joins continuously at the branching threshold:

```text
weak dissimilarity / coordination side
    shared | partial | full

at gamma=-kappa/2
    shared | neutral-variance manifold | full

strong dissimilarity side
    shared | endpoint polymorphism | full.
```

---

## Corollary GP1.2 — strong negative frequency dependence expands the polymorphism domain beyond intrinsically partial systems

For

```text
gamma<-kappa/2,
```

one has

```text
alpha_S<0,
alpha_D>kappa L.
```

Therefore the protected endpoint-polymorphism region includes:

```text
some systems with alpha<0
that would intrinsically choose the shared architecture,

and

some systems with alpha>kappa L
that would intrinsically choose full differentiation.
```

Population feedback can therefore maintain both architecture extremes even when the frequency-independent cost-recovery curve alone prefers one endpoint.

---

## Corollary GP1.3 — the polymorphism wedge broadens linearly with dissimilarity reward

Its width on the `alpha` axis is

```text
alpha_D-alpha_S
=-2gamma L
=2|gamma|L.
```

As `gamma` becomes more negative, the interval of intrinsic architecture preferences that can be converted into protected endpoint coexistence broadens linearly.

Its midpoint is always

```text
(alpha_S+alpha_D)/2
=kappa L/2.
```

So negative-frequency architecture feedback widens the polymorphism region symmetrically around the intrinsic endpoint-indifference center.

---

## Corollary GP1.4 — very strong dissimilarity reward drives the interior mixture toward one half

Inside the polymorphism region,

```text
p*
=1/2
+ phi_endpoint/[2(-gamma)L^2],
```

where

```text
phi_endpoint
=alpha L-(kappa/2)L^2.
```

Hence for fixed intrinsic parameters,

```text
gamma->-infinity
-> p*->1/2.
```

---

# Compact phase map

For fixed `kappa,L`, the two-dimensional `(alpha,gamma)` diagram is:

```text
gamma > -kappa/2:
    alpha<=0             shared monomorph
    0<alpha<kappa L      partial monomorph
    alpha>=kappa L       full monomorph


gamma = -kappa/2:
    alpha<=0             shared endpoint
    0<alpha<kappa L      neutral variance at mean alpha/kappa
    alpha>=kappa L       full endpoint


gamma < -kappa/2:
    alpha<=alpha_S       shared endpoint
    alpha_S<alpha<alpha_D endpoint polymorphism
    alpha>=alpha_D       full endpoint.
```

The phase-boundary lines are

```text
gamma=-kappa/2,
alpha=0,
alpha=kappa L,
alpha=[(kappa+2gamma)L]/2,
alpha=[(kappa-2gamma)L]/2.
```

---

# PAYOFF interpretation

This creates a continuous architecture version of the SCH/BALANCE/BITA/PAYOFF programme:

```text
architecture cost-recovery geometry
        |
        v
shared / partial / full intrinsic optimum
        |
        | increase dissimilarity-favoring feedback
        v
variance threshold gamma=-kappa/2
        |
        v
protected endpoint coexistence wedge.
```

The key distinction remains:

```text
intrinsic architecture optimum
!=
population-level architecture distribution.
```

Strong frequency-dependent ecological complementarity can support both architecture extremes even when neither a binary static comparison nor the intrinsic continuous optimum would predict that final distribution.

# Claim boundary

This exact global phase diagram relies on the quadratic intrinsic payoff and squared architecture-distance feedback. The general convex-cost theorem supports the local branching threshold but not these global linear phase boundaries.
