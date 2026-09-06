# PAYOFF theorems

This note gives the minimal analytic core connecting shared-trait compromise, persistence of an integrated architecture, evolutionary differentiation of trait dimensions, and population-level architecture games.

## Notation

Two functions have quadratic losses around preferred trait values `theta1` and `theta2` with positive weights `a,b>0`. Let

```text
d = theta1-theta2.
```

The shared architecture has one coordinate `z`. The differentiated architecture has two coordinates `x,y`, residual coupling `c>=0`, and additional architecture cost `K>=0`.

Fitness is a common baseline minus loss and architecture cost. Only payoff differences matter for the game.

---

## Theorem 1 — unique shared compromise

For

```text
LS(z) = a(z-theta1)^2 + b(z-theta2)^2,
```

the unique minimizer is

```text
zS* = (a theta1+b theta2)/(a+b),
```

and the minimized conflict load is

```text
L = LS(zS*) = [ab/(a+b)] d^2.
```

Therefore `L>0` iff `theta1 != theta2`.

### Proof

Differentiate:

```text
dLS/dz = 2a(z-theta1)+2b(z-theta2).
```

Setting the derivative to zero gives the stated weighted mean. Since

```text
d2LS/dz2 = 2(a+b) > 0,
```

the minimizer is unique. Substituting `zS*` gives

```text
zS*-theta1 = -[b/(a+b)]d,
zS*-theta2 =  [a/(a+b)]d,
```

hence

```text
L
= a[b^2/(a+b)^2]d^2 + b[a^2/(a+b)^2]d^2
= [ab/(a+b)]d^2.
```

QED.

---

## Theorem 2 — `n`-function conflict load is weighted disagreement

For `n` functions with positive weights `a_i` and preferred values `theta_i`, define

```text
LS(z) = sum_i a_i (z-theta_i)^2,
A     = sum_i a_i,
theta_bar = (sum_i a_i theta_i)/A.
```

Then

```text
zS* = theta_bar
```

and

```text
L_n
= sum_i a_i(theta_i-theta_bar)^2
= (1/A) sum_{i<j} a_i a_j (theta_i-theta_j)^2.
```

Thus shared-coordinate conflict is exactly the weighted pairwise dispersion among function-specific optima.

### Proof

The first identity follows from differentiating `LS`. For the second, expand

```text
sum_{i<j} a_i a_j(theta_i-theta_j)^2
```

and collect the `theta_i^2` and cross terms. Equivalently use the weighted-variance identity

```text
A sum_i a_i(theta_i-theta_bar)^2
= sum_{i<j} a_i a_j(theta_i-theta_j)^2.
```

Dividing by `A` yields the result.

QED.

### Consequence

The theory does not require exactly two biological functions. In one shared phenotypic dimension, the irreducible conflict budget is a weighted disagreement statistic over all functions using that dimension.

---

## Theorem 3 — exact partial dimensional release with residual coupling

For the differentiated architecture

```text
LD(x,y)
= a(x-theta1)^2
+ b(y-theta2)^2
+ c(x-y)^2,
```

define

```text
Q = ab+c(a+b).
```

The unique optimum for finite `c>=0` is

```text
x* = [a(b+c)theta1 + bc theta2]/Q,
y* = [ac theta1 + b(a+c)theta2]/Q.
```

The realized separation is

```text
x*-y* = [ab/Q] d.
```

Define

```text
s = |x*-y*|/|d|
  = ab/Q
```

when `d != 0`, and use the same algebraic value `ab/Q` when `d=0`.

The minimized differentiated loss is

```text
LD* = [abc/Q] d^2.
```

The recovered shared-compromise loss is exactly

```text
R = L-LD* = sL.
```

### Proof

The first-order conditions are

```text
(a+c)x - cy = a theta1,
-cx + (b+c)y = b theta2.
```

The determinant is

```text
Q=(a+c)(b+c)-c^2=ab+c(a+b)>0,
```

so the optimum is unique and solving the linear system gives `x*` and `y*`. Subtraction yields

```text
x*-y* = (ab/Q)d.
```

Direct substitution gives

```text
LD* = (abc/Q)d^2.
```

From Theorem 1,

```text
L = [ab/(a+b)]d^2.
```

Therefore

```text
R
= ab d^2/(a+b) - abc d^2/Q
= [a^2 b^2/((a+b)Q)]d^2
= (ab/Q)L
= sL.
```

QED.

### Boundary cases

- `c=0`: `s=1`, `x*=theta1`, `y*=theta2`, `LD*=0`; full release.
- `c -> infinity`: `s->0` and `LD*->L`; the differentiated coordinates become effectively shared.

---

## Corollary 3.1 — stronger residual coupling cannot improve recovery

For `a,b>0`,

```text
s(c)=ab/[ab+c(a+b)]
```

obeys

```text
ds/dc = -ab(a+b)/[ab+c(a+b)]^2 < 0.
```

Hence `R(c)=s(c)L` is nonincreasing in coupling, and strictly decreasing whenever `L>0`.

QED.

---

## Theorem 4 — optimized architecture payoff gap

Let `B` be any common baseline fitness. Define

```text
WS* = B-L,
WD* = B-LD*-K.
```

Then

```text
phi = WD*-WS* = sL-K.
```

### Proof

By Theorem 3, `L-LD*=sL`, so

```text
WD*-WS*
= (B-LD*-K)-(B-L)
= L-LD*-K
= sL-K.
```

QED.

---

## Corollary 4.1 — three-world partition

Under `L>=0`, `0<=s<=1`, `K>=0`:

```text
L = 0                 no shared-axis conflict,
L > 0 and phi < 0     conflict exists but shared architecture has higher payoff,
phi = 0               architecture critical surface,
phi > 0               differentiated architecture has higher payoff.
```

For `L>0`, the second line is the BALANCE region and the fourth is the BITA-favored region. SCH supplies the compromise geometry and `L`.

This partition is exhaustive apart from equality surfaces because `phi` is a scalar optimized payoff difference.

---

## Theorem 5 — minimal architecture game and replicator dynamics

Let `S` and `D` be the shared and differentiated architecture strategies. Let `p` be the population frequency of `D` and define

```text
Delta(p) = pi_D(p)-pi_S(p)
         = phi + eta(2p-1),
```

where `eta` is a frequency-feedback coefficient.

One genuinely symmetric two-strategy game representation is

```text
          opponent S    opponent D
S              0           phi-eta
D           phi-eta         2phi
```

because

```text
pi_S(p) = (phi-eta)p,
pi_D(p) = (phi-eta)(1-p)+2phi p,
pi_D-pi_S = phi+eta(2p-1).
```

Under replicator dynamics,

```text
dp/dt = p(1-p)Delta(p).
```

For `eta != 0`, an interior equilibrium exists iff

```text
|phi| < |eta|,
```

and is

```text
p* = (1-phi/eta)/2.
```

It is locally asymptotically stable iff `eta<0`, and unstable iff `eta>0`.

### Proof

Interior equilibria satisfy `Delta(p*)=0`, giving the stated `p*`. The condition `0<p*<1` is algebraically equivalent to `|phi|<|eta|`.

Let

```text
f(p)=p(1-p)Delta(p).
```

At an interior equilibrium `Delta(p*)=0`, hence

```text
f'(p*) = p*(1-p*) Delta'(p*)
       = 2 eta p*(1-p*).
```

Since `p*(1-p*)>0`, the sign of `f'(p*)` is the sign of `eta`. Negative derivative gives local asymptotic stability and positive derivative instability.

QED.

---

## Corollary 5.1 — complete phase classification

### Frequency-independent baseline: `eta=0`

```text
phi<0  -> S dominates,
phi>0  -> D dominates,
phi=0  -> every p is stationary under the baseline game.
```

### Negative frequency dependence: `eta<0`

Let `h=|eta|`.

```text
phi <= -h       -> S dominates,
-h < phi < h    -> unique stable mixed equilibrium,
phi >= h        -> D dominates.
```

### Positive frequency dependence: `eta>0`

```text
phi <= -eta       -> S dominates,
-eta < phi < eta  -> p=0 and p=1 are locally stable, p* is an unstable threshold,
phi >= eta        -> D dominates.
```

At equality boundaries one obtains non-hyperbolic limiting cases.

### Proof

At `p=0`, local stability requires

```text
Delta(0)=phi-eta<0.
```

At `p=1`, local stability requires

```text
Delta(1)=phi+eta>0.
```

Combine these boundary conditions with Theorem 5 and the monotonicity of `Delta(p)`.

QED.

---

## Corollary 5.2 — ESS interpretation

For the strict cases of the two-strategy symmetric game:

- `S` is a pure ESS when `Delta(0)<0`;
- `D` is a pure ESS when `Delta(1)>0`;
- when `eta<0` and `|phi|<|eta|`, the stable interior equilibrium is the mixed ESS;
- when `eta>0` and `|phi|<eta`, the interior equilibrium is not an ESS and instead separates the basins of the two pure ESSs.

This is the point where PAYOFF becomes genuine evolutionary game theory rather than a metaphorical game among biological functions.

---

## Theorem 6 — switching-cost hysteresis

Suppose a population currently in `S` must pay transition cost `C_SD>=0` to adopt `D`, and a population currently in `D` must pay `C_DS>=0` to return to `S`. Let these costs be amortized over a persistence horizon `T>0`.

At a given ecological state and population frequency, switching rules are

```text
S -> D iff Delta(p) > C_SD/T,
D -> S iff Delta(p) < -C_DS/T.
```

Therefore both inherited states can persist without switching whenever

```text
-C_DS/T <= Delta(p) <= C_SD/T.
```

The width of this hysteresis band on the payoff-gap scale is

```text
Delta_hyst = (C_SD+C_DS)/T.
```

### Proof

An `S` state persists if the gain from switching fails to exceed its amortized switching cost:

```text
Delta(p) <= C_SD/T.
```

A `D` state persists if the gain from switching back to `S`, equal to `-Delta(p)`, fails to exceed `C_DS/T`:

```text
-Delta(p) <= C_DS/T,
```

or equivalently `Delta(p)>=-C_DS/T`. Their intersection is the stated interval. Its width is upper minus lower bound.

QED.

### Frequency-dependent consequence

When `eta != 0`, the hysteresis inequalities can be mapped to frequency thresholds by solving

```text
phi+eta(2p-1)=C_SD/T
```

and

```text
phi+eta(2p-1)=-C_DS/T.
```

Thus ecological frequency feedback and architectural switching costs produce distinct but composable sources of history dependence.

---

## Theorem 7 — positive affine payoff invariance

Apply the same positive affine transformation to all game payoffs:

```text
pi'_i = alpha pi_i + beta,
alpha>0.
```

Then

```text
Delta'(p)=alpha Delta(p)
```

and the replicator equation becomes

```text
dp/dt = alpha p(1-p)Delta(p).
```

Hence phase portraits and equilibria are unchanged; only time is rescaled by `tau=alpha t`.

### Proof

The common shift `beta` cancels from payoff differences. Positive multiplication by `alpha` preserves all signs and zeros of `Delta`. Replicator trajectories in state space are therefore identical under a positive rescaling of time.

QED.

### Caveat

If explicit switching costs are included, those costs must be transformed on the same payoff scale for the full switching model to retain affine invariance.

---

## Theorem 8 — the static architecture crossing splits into two invasion surfaces

Let

```text
R=sL,
phi=R-K.
```

The invasion advantage of rare `D` in an `S` resident population is

```text
I_D = Delta(0)=phi-eta=R-K-eta.
```

The invasion advantage of rare `S` in a `D` resident population is

```text
I_S = -Delta(1)=-phi-eta=K-R-eta.
```

Therefore the reciprocal neutral-invasion surfaces are

```text
Sigma_D: K=R-eta,
Sigma_S: K=R+eta.
```

For fixed `s`, these are planes in `(L,K,eta)` space:

```text
Sigma_D: K=sL-eta,
Sigma_S: K=sL+eta.
```

They intersect exactly along the frequency-independent architecture crossing

```text
eta=0,
K=sL.
```

Away from equality surfaces, the complete phase partition is

```text
K > R+|eta|                -> shared dominance,
K < R-|eta|                -> differentiated dominance,
|K-R|<|eta| and eta<0      -> stable architecture coexistence,
|K-R|<|eta| and eta>0      -> coordination bistability.
```

The middle game's width on the `K` axis is exactly

```text
W_K=2|eta|.
```

### Proof

The neutral surfaces follow by setting `I_D=0` and `I_S=0`. By Corollary 5.1, shared dominance is equivalent to

```text
phi < -|eta|,
```

which becomes `K>R+|eta|`. Differentiated dominance is equivalent to `phi>|eta|`, which becomes `K<R-|eta|`. The remaining strict region is `|phi|<|eta|`, equivalent to `|K-R|<|eta|`; Corollary 5.1 assigns coexistence for `eta<0` and coordination bistability for `eta>0`. Its `K` interval is `(R-|eta|,R+|eta|)`, whose width is `2|eta|`.

QED.

### Consequence 8.1 — static BALANCE can admit invasion

If `phi<0` but `eta<0` and `|phi|<|eta|`, then

```text
I_D=phi-eta>0.
```

Thus a rare differentiated architecture can invade from the static BALANCE side of the frequency-independent crossing. The deterministic outcome is coexistence, not differentiated dominance.

### Consequence 8.2 — static BITA advantage can face a coordination barrier

If `phi>0` but `eta>0` and `phi<eta`, then

```text
I_D=phi-eta<0.
```

Thus a differentiated architecture with positive frequency-independent advantage can nevertheless fail to invade when rare.

Therefore

```text
static architecture advantage != invasion success.
```

---

## Theorem 9 — reciprocal threshold inversion identifies recovery and frequency feedback

Hold `R` and `eta` fixed while varying architecture cost. Let

```text
K_D=R-eta
```

be the cost at which rare `D` is neutral in an `S` population, and let

```text
K_S=R+eta
```

be the cost at which rare `S` is neutral in a `D` population. Then

```text
R   = (K_D+K_S)/2,
eta = (K_S-K_D)/2.
```

The signed threshold split is

```text
K_S-K_D=2eta.
```

### Proof

Add and subtract the defining equations for `K_D` and `K_S`.

QED.

### Interpretation

Threshold ordering diagnoses feedback topology:

```text
K_S<K_D  -> eta<0 -> reciprocal-invasion / coexistence geometry,
K_S>K_D  -> eta>0 -> reciprocal-exclusion / coordination geometry.
```

The mathematical thresholds may lie outside the biologically feasible range `K>=0`; empirical identification requires both relevant thresholds to be experimentally reachable.

---

## Theorem 10 — monotone environmental paths generically have two game transitions

Let environment `e` change the frequency-independent architecture gap continuously and strictly monotonically while `eta` is constant:

```text
phi=phi(e).
```

If `phi(e)` is strictly increasing, each of the two game boundaries

```text
phi=-|eta|,
phi=+|eta|
```

can be crossed at most once. If the environmental range spans both values, the ordered phase sequence is exactly

```text
shared dominance
-> middle game region
-> differentiated dominance,
```

where the middle region is stable coexistence for `eta<0` and coordination bistability for `eta>0`.

### Proof

A continuous strictly increasing function takes each value at most once. Corollary 5.1 fixes the phase on the three intervals separated by `-|eta|` and `+|eta|`.

QED.

### Corollary 10.1 — exact splitting along a linear environmental gradient

If

```text
phi(e)=alpha(e-e0),
alpha != 0,
```

then `e0` is the static `phi=0` crossing and the two game boundaries solve `phi=+-|eta|`. Their ordered separation is

```text
W_e=2|eta|/|alpha|.
```

Thus stronger frequency feedback broadens the environmental transition zone, whereas a steeper environmental change in static architecture payoff compresses it.

### Corollary 10.2 — variable feedback requires margin-level topology

If both `phi(e)` and `eta(e)` vary, define

```text
I_D(e)=phi(e)-eta(e),
I_S(e)=-phi(e)-eta(e).
```

Every change in reciprocal-invasion status requires a zero crossing of at least one of these margins. Re-entry into a previously occupied invasion-status region therefore requires at least one margin to cross zero more than once or to lose monotonicity.

---

# Main synthesis

The analytic chain is now

```text
functional disagreement
    -> shared conflict load L
    -> partial dimensional release s
    -> recovered loss R=sL
    -> architecture payoff gap phi=sL-K
    -> frequency-dependent game Delta(p)
    -> two reciprocal invasion surfaces
    -> dominance / coexistence / coordination threshold
    -> environmental threshold splitting
    -> optional switching-cost hysteresis.
```

The model therefore distinguishes four questions that should not be collapsed:

1. **Is there functional conflict?** `L>0`.
2. **Which optimized architecture has the higher frequency-independent payoff?** `phi=sL-K`.
3. **Can a rare alternative architecture invade a resident population?** determined separately by `I_D=phi-eta` and `I_S=-phi-eta`.
4. **What architecture state is evolutionarily stable in a population?** determined by the full `Delta(p)`, frequency feedback, and transition costs.

That separation is the theoretical bridge from SCH to BALANCE to BITA and then beyond them into evolutionary game dynamics.