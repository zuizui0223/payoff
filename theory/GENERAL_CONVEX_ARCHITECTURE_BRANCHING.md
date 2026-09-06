# General convex architecture branching theorem

The quadratic continuous architecture model has an exact branching threshold

```text
gamma=-kappa/2.
```

That threshold is not fundamentally about quadratic costs. Its local form extends to any smooth convex architecture-cost curve once the architecture coordinate is recovered conflict loss itself.

Let

```text
r in [0,L]
```

be recovered shared-conflict loss and let architecture cost be a twice continuously differentiable function

```text
C(r).
```

Intrinsic relative payoff is

```text
b(r)=r-C(r).
```

Assume local strict convexity at the singular architecture:

```text
C''(r)>0.
```

Use the same symmetric architecture-distance feedback

```text
H(r,q)=-gamma(r-q)^2.
```

Mutant invasion fitness in a monomorphic resident `x` is

```text
f(y,x)
=
[y-C(y)]-[x-C(x)]
-gamma(y-x)^2.
```

---

## Theorem G1 — symmetric mismatch feedback does not move the monomorphic selection gradient

The selection gradient is

```text
g(x)
= partial_y f(y,x)|y=x
=1-C'(x).
```

Therefore every interior singular architecture satisfies

```text
C'(r*)=1.
```

The parameter `gamma` does not appear.

### Proof

The derivative of `-gamma(y-x)^2` with respect to mutant recovery is zero at `y=x`. QED.

### Interpretation

The singular architecture is the ordinary marginal-value condition

```text
marginal recovered conflict fitness
=
marginal architecture cost.
```

Symmetric frequency-dependent feedback changes second-order evolutionary stability, not the first-order location of this balance point.

---

## Theorem G2 — convergence stability follows from local cost convexity

At an interior singular architecture,

```text
g'(r*)=-C''(r*).
```

Hence if

```text
C''(r*)>0,
```

the singular architecture is locally convergence stable under the standard one-dimensional adaptive-dynamics criterion.

---

## Theorem G3 — general local architecture branching threshold

The mutant-fitness curvature at the singular resident is

```text
partial_y^2 f(y,r*)|y=r*
=
-C''(r*)-2gamma.
```

Therefore:

```text
gamma > -C''(r*)/2
-> locally evolutionarily stable singular architecture;

gamma = -C''(r*)/2
-> second-order neutral threshold;

gamma < -C''(r*)/2
-> locally disruptive / branching-compatible singular architecture.
```

Thus the general local threshold is

```text
gamma_branch
=-C''(r*)/2.
```

### Proof

Differentiate invasion fitness twice with respect to mutant recovery. The intrinsic term contributes `-C''(r*)`; the squared mismatch term contributes `-2gamma`. QED.

---

## Corollary G3.1 — quadratic cost is the constant-curvature special case

For

```text
C(r)=c1*r+(kappa/2)r^2,
```

one has

```text
C''(r)=kappa
```

for every architecture. Hence

```text
gamma_branch=-kappa/2,
```

recovering `CONTINUOUS_ARCHITECTURE_ESS.md`.

---

## Corollary G3.2 — locally flatter cost curves branch more easily

Holding the architecture-distance feedback `gamma<0` fixed, smaller

```text
C''(r*)
```

requires a weaker dissimilarity reward to violate ESS stability.

Conversely, strongly convex architecture costs stabilize a monomorphic partial architecture against disruptive frequency-dependent feedback.

This yields a direct measurable prediction:

```text
branching susceptibility
is controlled by
local cost curvature at the marginal recovery optimum.
```

---

## What remains quadratic-specific?

The local singular and branching results above are general.

The stronger global conclusions in `CONTINUOUS_ARCHITECTURE_ESS.md`—especially

```text
an exactly flat variance manifold at threshold,
protected support exactly on {0,L},
and the closed-form endpoint frequency p*
```

use the quadratic intrinsic payoff together with the squared mismatch kernel.

For nonquadratic `C(r)`, the post-branching architecture distribution must be solved from the full game; it need not consist only of the two endpoints.

---

## Prior-art boundary

The logic

```text
convergence-stable singular point
+
disruptive mutant curvature
-> evolutionary branching
```

is established adaptive-dynamics theory (e.g. Geritz et al. 1998, DOI `10.1023/A:1006554906681`).

PAYOFF's architecture-specific statement is the substitution

```text
r = recovered compromise loss
```

which makes the singular condition

```text
C'(r*)=1
```

and the local branching threshold

```text
gamma=-C''(r*)/2
```

direct receipts of measurable architecture-cost geometry.
