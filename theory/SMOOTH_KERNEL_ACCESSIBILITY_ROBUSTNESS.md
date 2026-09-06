# Smooth-kernel robustness of finite-jump accessibility

`HARD_CUTOFF_ESCAPE_THEOREM.md` proves an exact interface barrier for a hard
interaction radius. This note asks the obvious adverse-control question:

> Does the finite-jump barrier survive when the hard cutoff is smoothed?

Implementation:

```text
src/interaction_kernel_robustness.py
tests/test_interaction_kernel_robustness.py
```

---

## 1. Kernel family

For architecture distance `d=|r-q|`, write

```text
H(r,q)=-gamma d^2 w(d).
```

The registered comparison uses:

```text
hard:
  w(d)=1{d<=epsilon}

triangular:
  w(d)=max(0,1-d/epsilon)

cosine:
  w(d)=0.5[1+cos(pi d/epsilon)]  for d<epsilon,
       =0                         otherwise

gaussian:
  w(d)=exp[-0.5(d/epsilon)^2]

global:
  w(d)=1.
```

Triangular and cosine remove the payoff discontinuity at `epsilon`. Gaussian
removes the finite support as well.

---

## 2. General resident payoff derivative

For a shared resident at `0`,

```text
p(r)
=b(r)-gamma r^2 w(r)
```

with

```text
b(r)=alpha r-(kappa/2)r^2.
```

Where the kernel is differentiable,

```text
p'(r)
=alpha-kappa r
 -gamma[2r w(r)+r^2 w'(r)].
```

Therefore a smooth finite-jump barrier does not require a discontinuity. It can
arise whenever the distance-weighted interaction reward/penalty creates a local
ridge followed by a lower-payoff interval before a better architecture region.

The hard-cutoff jump is one sufficient mechanism, not the only one.

---

## 3. Adverse control: one hard-cutoff barrier disappears under smoothing

For

```text
alpha=0.5,
kappa=1,
gamma=-1,
epsilon=0.1,
```

the hard kernel has the exact interface barrier derived in
`HARD_CUTOFF_ESCAPE_THEOREM.md`.

On a 161-bin grid:

```text
hard        -> critical jump > one bin
triangular  -> one-bin uphill accessibility
a cosine    -> one-bin uphill accessibility
gaussian    -> one-bin uphill accessibility.
```

(`a cosine` above means the registered cosine-taper kernel.)

This negative robustness result is retained. The particular
`gamma=-1, epsilon=0.1` barrier should **not** be advertised as kernel-shape
robust.

---

## 4. Positive robustness: smooth kernels can still create finite-jump barriers

The same accessibility audit finds finite barriers without a hard payoff jump
when interaction feedback is sufficiently strong or broad.

Registered finite-grid witnesses at 161 bins include:

```text
triangular:
  alpha=0.5, kappa=1, gamma=-2, epsilon=0.3
  critical jump distance > 0.05

cosine:
  alpha=0.5, kappa=1, gamma=-3, epsilon=0.3
  critical jump distance > 0.05

gaussian:
  alpha=0.5, kappa=1, gamma=-20, epsilon=0.05
  critical jump distance >= 0.05.
```

The compact smooth kernels therefore demonstrate that a finite-jump
accessibility bottleneck is not logically equivalent to a hard discontinuity.
The Gaussian witness shows that finite support itself is also not strictly
necessary, although the registered Gaussian example requires much stronger
feedback.

---

## 5. Interpretation

The bounded-interaction extension now has a useful hierarchy:

```text
hard cutoff
-> exact interface theorem available
-> barrier can occur at moderate feedback

smooth compact support
-> no interface discontinuity
-> barrier can still occur through a smooth local ridge

smooth infinite support (Gaussian)
-> locality decays continuously rather than terminating
-> barrier is possible in the tested family but required stronger feedback.
```

So the defensible statement is not

```text
finite interaction range always creates a jump barrier.
```

It is:

> Interaction locality can create architecture accessibility bottlenecks, but
> their existence and size depend on feedback strength, interaction range and
> kernel shape.

That is a more informative object because `kernel shape` becomes a biological
or empirical sensitivity dimension rather than an invisible modelling choice.

---

## 6. Next empirical/theoretical target

The next useful estimand is a kernel-robust accessibility envelope:

```text
delta_c(gamma,epsilon,w)
```

and, for a declared plausible kernel class `W`,

```text
[min_w delta_c, max_w delta_c].
```

A biological claim about local evolvability should be called kernel-robust only
when its qualitative accessibility class is invariant across the prospectively
declared kernel family.

---

## Claim boundary

The registered witnesses are deterministic finite-grid results. They do not
establish a universal ordering such as

```text
hard > triangular > cosine > gaussian
```

for every parameter set. Nor do they identify the interaction kernel of any
natural biological system. The adverse control is part of the result: one
apparently strong hard-cutoff barrier vanishes immediately when that particular
kernel is smoothed.
