# Continuous architecture ESS — from partial modularity to architecture branching

The binary shared-versus-differentiated PAYOFF game can be extended to a continuum of architectures without abandoning the upstream SCH/BALANCE/BITA bridge.

The key coordinate is not an arbitrary trait label. It is the **recovered shared-conflict loss**

```text
r in [0,L],
```

where `L` is the fully shared conflict load and `r` is the amount recovered by a candidate coupling architecture before architecture cost.

For the network model in `NETWORK_EXTENSION.md`,

```text
r=R(lambda)=L-D_lambda*.
```

For a connected coupling graph with non-identical function optima, `R(lambda)` is continuous and strictly decreasing from `L` to `0` as integration strength `lambda` increases from `0` to infinity. Therefore `r` is a valid one-to-one architecture coordinate along that release path.

This note asks:

> Which amount of dimensional release is evolutionarily stable when recovery itself is costly and ecological interactions depend on architectural similarity?

The adaptive-dynamics concepts used below are established prior theory; see Geritz, Kisdi, Meszena & Metz (1998), Evolutionary Ecology 12:35-57, DOI `10.1023/A:1006554906681`. PAYOFF's contribution is the architecture-specific substitution of recovery `r` generated from `L -> R(lambda)`.

---

## 1. Costed continuous architecture

Let architecture maintenance/development cost be

```text
C(r)=c1*r + (kappa/2)*r^2,
```

with

```text
kappa>0.
```

Relative to the fully shared architecture, pre-frequency intrinsic payoff is

```text
b(r)=r-C(r)
    =alpha*r-(kappa/2)*r^2,
```

where

```text
alpha=1-c1.
```

The linear term `alpha` is the net marginal value of the first unit of recovered conflict loss; `kappa` is the curvature of the architecture-cost schedule.

The trait domain is

```text
0 <= r <= L.
```

Interpretation:

```text
r=0   fully shared / fully integrated endpoint,
0<r<L partial dimensional release / partial modularity,
r=L   full recovery / fully differentiated endpoint.
```

---

## Theorem C1 — exact no-feedback architecture optimum

Without frequency-dependent architecture interactions, the unique payoff-maximizing recovery is

```text
r0=clip(alpha/kappa,0,L).
```

Hence:

```text
alpha <= 0
-> r0=0
-> shared architecture;

0 < alpha < kappa L
-> r0=alpha/kappa
-> partial modularity;

alpha >= kappa L
-> r0=L
-> full differentiation.
```

### Proof

`b(r)` is strictly concave because

```text
b''(r)=-kappa<0.
```

Its unconstrained stationary point solves

```text
b'(r)=alpha-kappa r=0,
```

so `r=alpha/kappa`. Projection onto `[0,L]` gives the unique constrained maximizer. QED.

### Interpretation

The binary BALANCE/BITA contrast becomes a continuous three-region result:

```text
marginal architecture cost too high
-> no release;

marginal benefit and rising cost cross inside the feasible interval
-> partial modularity;

benefit remains above marginal cost throughout the interval
-> full release.
```

---

## 2. Symmetric ecological feedback among architecture levels

Let two architecture recoveries `r` and `q` receive pairwise feedback

```text
H(r,q)=-gamma(r-q)^2.
```

Thus:

```text
gamma>0
-> architectural mismatch is penalized
-> similarity / coordination feedback;

gamma<0
-> architectural mismatch is rewarded
-> dissimilarity / negative-frequency feedback.
```

A symmetric continuous game kernel is

```text
A(r,q)=b(r)+b(q)+H(r,q).
```

The common partner term `b(q)` cancels from relative payoff comparisons, exactly as in the finite multi-architecture game.

For a mutant `y` invading a monomorphic resident `x`, invasion fitness relative to the resident is

```text
f(y,x)
=b(y)-b(x)-gamma(y-x)^2.
```

---

## Theorem C2 — the monomorphic selection gradient ignores symmetric mismatch feedback

The mutant selection gradient at a monomorphic resident is

```text
g(x)
= partial_y f(y,x) at y=x
= alpha-kappa x.
```

Therefore the interior singular architecture is

```text
x*=alpha/kappa
```

whenever

```text
0<alpha<kappa L.
```

It is convergence stable because

```text
g'(x*)=-kappa<0.
```

### Proof

Differentiate

```text
f(y,x)=b(y)-b(x)-gamma(y-x)^2
```

with respect to `y`. The derivative of the mismatch term vanishes at `y=x`, leaving `b'(x)=alpha-kappa x`. QED.

### Interpretation

Symmetric difference-dependent ecology does **not** move the gradual-evolution target of a monomorphic population. It changes whether that target remains evolutionarily stable once reached.

That first-order/second-order separation is central to the continuous PAYOFF extension.

---

## Theorem C3 — exact architecture branching threshold

Assume the intrinsic optimum is interior:

```text
0<alpha<kappa L,
```

so

```text
r0=alpha/kappa.
```

Then mutant invasion fitness against the singular resident simplifies exactly to

```text
f(y,r0)
=-(kappa/2+gamma)(y-r0)^2.
```

Therefore:

```text
gamma > -kappa/2
-> r0 is a strict global ESS;

gamma = -kappa/2
-> every recovery level is neutral against resident r0;

gamma < -kappa/2
-> every distinct nearby mutant can invade r0.
```

Under the standard small-mutation adaptive-dynamics interpretation, the last case makes the convergence-stable singular architecture branching-compatible.

### Proof

Because `r0=alpha/kappa`, completing the square gives

```text
b(y)-b(r0)
=-(kappa/2)(y-r0)^2.
```

Adding pairwise mismatch feedback gives the stated identity. The sign classification is immediate. QED.

### Important prior-art boundary

Convergence-stable but evolutionarily unstable singular strategies and evolutionary branching are established adaptive-dynamics concepts. PAYOFF does **not** claim to invent branching theory.

The architecture-specific result is the exact curvature receipt

```text
intrinsic architecture-cost curvature kappa
versus
mismatch-feedback curvature -2 gamma,
```

with threshold

```text
gamma_branch=-kappa/2.
```

---

## 3. Population potential in the continuous architecture game

Let a population distribution over recovery levels have

```text
mu = E[r],
sigma2 = Var(r).
```

For two independently sampled individuals,

```text
E[(r-r')^2]=2 sigma2.
```

The mean symmetric-game payoff is therefore

```text
V
= E[A(r,r')]
= 2 alpha mu
  - kappa mu^2
  - (kappa+2 gamma) sigma2.
```

This is the continuous analogue of the Lyapunov potential in `MULTI_ARCHITECTURE_GAME.md`.

---

## Theorem C4 — one curvature coefficient decides whether architecture variance is penalized or rewarded

At fixed mean recovery `mu`, the coefficient on architecture variance is

```text
-(kappa+2 gamma).
```

Hence:

```text
kappa+2 gamma > 0
-> architecture variance lowers potential;

kappa+2 gamma = 0
-> potential is independent of architecture variance at fixed mean;

kappa+2 gamma < 0
-> architecture variance raises potential.
```

The variance threshold is exactly the same as the mutant branching threshold in Theorem C3.

### Proof

Substitute

```text
E[r^2]=mu^2+sigma2
```

and

```text
E[(r-r')^2]=2sigma2
```

into the expected game payoff. QED.

---

## Theorem C5 — weak dissimilarity feedback gives one monomorphic partial architecture

Assume

```text
0<alpha<kappa L
```

and

```text
gamma>-kappa/2.
```

Then the unique global potential maximizer is the monomorphic architecture

```text
r=r0=alpha/kappa.
```

### Proof

Since `kappa+2gamma>0`, variance is strictly penalized, so for every fixed mean the best distribution has

```text
sigma2=0.
```

The remaining potential is

```text
2alpha mu-kappa mu^2,
```

strictly maximized at `mu=alpha/kappa`. QED.

---

## Theorem C6 — at the branching threshold an entire variance manifold is neutral

Assume

```text
gamma=-kappa/2
```

and the intrinsic optimum is interior.

Then every population distribution on `[0,L]` with mean

```text
E[r]=r0=alpha/kappa
```

has the same maximal potential.

### Proof

At the threshold,

```text
kappa+2gamma=0,
```

so variance drops out of `V`. The remaining strictly concave mean term is maximized at `mu=r0`. QED.

### Interpretation

The threshold is not merely where one second derivative changes sign. It is an exact flattening of the population potential with respect to architecture variance at the optimal mean.

---

## Theorem C7 — strong dissimilarity feedback produces an extreme-architecture polymorphism

Assume

```text
0<alpha<kappa L
```

and

```text
gamma<-kappa/2.
```

Then the global potential-maximizing distribution is supported on the two endpoint architectures

```text
r=0
and
r=L.
```

Let `p` be the frequency of the fully differentiated endpoint `r=L`. The unique maximizing frequency is

```text
p*
=
[2alpha-(kappa+2gamma)L]
/[-4 gamma L].
```

Under the stated conditions,

```text
0<p*<1.
```

The mean recovery and variance are

```text
mu*=p*L,
sigma2*=p*(1-p*)L^2.
```

### Proof

When `kappa+2gamma<0`, potential increases with variance at fixed mean. For any random variable on `[0,L]`,

```text
Var(r)<=mu(L-mu),
```

with equality exactly for a distribution supported on `{0,L}` with `P(r=L)=mu/L`.

Therefore the global optimization reduces to endpoint mixtures. Substituting

```text
sigma2=mu(L-mu)
```

into `V` gives

```text
V_extreme(mu)
=[2alpha-(kappa+2gamma)L]mu
+2gamma mu^2.
```

Because `gamma<0`, this is strictly concave. Its unique maximizer is

```text
mu*
=[2alpha-(kappa+2gamma)L]/[-4gamma],
```

which yields the stated `p*=mu*/L`.

The interior condition follows from `0<alpha<kappa L` together with `gamma<-kappa/2`. QED.

---

## Theorem C8 — the endpoint polymorphism is globally uninvadable by intermediate architectures

Write

```text
h=-gamma>kappa/2.
```

At the endpoint mixture `p*`, shared and fully differentiated endpoints have equal payoff.

For any candidate recovery `y in [0,L]`, its frequency-dependent payoff against the endpoint mixture is a strictly convex quadratic in `y`:

```text
pi(y)
=b(y)
+h[(1-p*)y^2+p*(y-L)^2]
+ common partner term.
```

Because the quadratic coefficient is

```text
h-kappa/2>0,
```

its maximum on `[0,L]` occurs at an endpoint. Since the two endpoints have equal payoff at `p*`, every strict interior recovery has lower payoff.

Therefore the endpoint mixture is globally protected against invasion by every intermediate architecture.

### Interpretation

Strong enough negative frequency dependence does not merely broaden a partial architecture distribution. In this exact quadratic model it drives the potential optimum all the way to a protected polymorphism of the two architectural extremes.

---

## Corollary C8.1 — exact reduction to the original two-strategy PAYOFF game

Restrict the continuous game to the endpoints

```text
S: r=0,
D: r=L.
```

The differentiated endpoint has intrinsic gap

```text
phi_endpoint
=b(L)-b(0)
=alpha L-(kappa/2)L^2.
```

The mismatch kernel gives unlike-architecture feedback

```text
H(0,L)=-gamma L^2.
```

Comparing with the canonical PAYOFF matrix

```text
          S             D
S         0         phi-eta
D      phi-eta        2phi
```

identifies

```text
eta_endpoint=gamma L^2.
```

Hence the endpoint coexistence frequency from the original two-strategy game,

```text
p_D*
=(1-phi_endpoint/eta_endpoint)/2,
```

is exactly the same as the continuous-game `p*` in Theorem C7.

Thus the original binary PAYOFF game reappears as the endpoint phase of the continuous architecture model.

---

## 4. Mapping the optimal recovery back to residual coupling

Along any connected network release path, strict monotonicity of `R(lambda)` gives a unique coupling strength corresponding to every interior recovery.

For the original two-function quadratic residual-coupling model,

```text
R(lambda)
=
L * ab/[ab+lambda(a+b)].
```

Therefore for any

```text
0<r<L
```

the exact residual coupling that realizes recovery `r` is

```text
lambda(r)
=
ab(L-r)/[r(a+b)].
```

At the endpoints:

```text
r=L -> lambda=0,
r=0 -> lambda->infinity.
```

So the no-feedback partial optimum `r0=alpha/kappa` has exact two-function coupling

```text
lambda*
=
ab(L-alpha/kappa)
/
[(alpha/kappa)(a+b)]
```

whenever `0<alpha/kappa<L`.

This supplies a direct bridge from continuous architecture ESS back to a measurable residual-integration parameter.

---

# Compact phase diagram

For an interior intrinsic optimum `0<alpha<kappa L`:

```text
gamma > -kappa/2
    |
    v
one monomorphic partial architecture
r*=alpha/kappa


gamma = -kappa/2
    |
    v
neutral variance manifold
E[r]=alpha/kappa


gamma < -kappa/2
    |
    v
branching-compatible singular point
    |
    v
protected endpoint polymorphism
{r=0,r=L}
with frequency p*.
```

The key threshold is

```text
gamma_branch=-kappa/2.
```

It appears independently from:

```text
mutant invasion curvature,
population-potential variance curvature,
and endpoint-polymorphism stability.
```

That coincidence is the main theorem-level result of the continuous architecture extension.

---

# Biological claim ceiling

Do not interpret the endpoint polymorphism as proof that real organisms must split into fully integrated and fully modular morphs. The result depends on the declared quadratic recovery-cost schedule and quadratic symmetric architecture-mismatch kernel.

Appropriate language:

> Under a continuous recovery coordinate, convex architecture costs generate a unique partial-modularity optimum; sufficiently strong dissimilarity-favoring ecological feedback destabilizes that monomorphic optimum at `gamma=-kappa/2` and, in the declared quadratic potential game, produces a protected mixture of the shared and fully differentiated endpoints.

Avoid:

> Negative frequency dependence universally causes modular architectures to branch into two extreme morphs.
