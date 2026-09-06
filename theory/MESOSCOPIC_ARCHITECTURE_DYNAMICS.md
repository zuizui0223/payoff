# Mesoscopic architecture dynamics — bounded interaction, small jumps, and accessibility

This note adds a population-distribution layer to PAYOFF without changing the existing SCH → BALANCE → BITA handoff or the established continuous-architecture results.

The new object is a probability density (implemented on a finite grid)

```text
f(r,t),  r in [0,L],
```

where `r` is recovered shared-conflict loss, exactly as in `CONTINUOUS_ARCHITECTURE_ESS.md`.

## 1. Architecture payoff against a distribution

Retain the intrinsic architecture payoff

```text
b(r)=alpha*r-(kappa/2)*r^2.
```

Replace globally coupled pairwise feedback by the bounded kernel

```text
H_epsilon(r,q)
=-gamma (r-q)^2 1{|r-q| <= epsilon}.
```

The distribution-level payoff is

```text
pi(r;f)
=b(r)+integral H_epsilon(r,q) f(q) dq.
```

`epsilon -> infinity` recovers the globally interacting quadratic kernel already used by PAYOFF. Small `epsilon` means that only sufficiently similar architectures contribute to the frequency-dependent interaction term.

This is structurally analogous to bounded-confidence interaction models such as Hegselmann–Krause, but the biological objects here are heritable architectures, not opinions. PAYOFF therefore uses the descriptive term **bounded architecture interaction** rather than relabelling the model as an opinion-dynamics model.

## 2. Finite-grid mesoscopic update

`src/mesoscopic_architecture.py` implements a dependency-free finite-grid approximation.

Selection uses exponential payoff reweighting:

```text
f_i^sel
propto
f_i exp(beta*pi_i).
```

Mutation then redistributes a fraction `mu` of each source-bin mass only to bins within a declared jump radius `J`:

```text
M_ij = 0  when |i-j| > J.
```

Boundary rows are renormalised, so probability mass is conserved.

The implementation is deliberately a finite-grid replicator-mutator approximation. It does **not** claim to numerically solve a continuous Fokker–Planck equation.

## 3. Small-jump scaling limit

A natural continuous scaling is

```text
jump size delta -> 0,
mutation probability -> 0,
time step -> 0,
mutation variance / time -> finite.
```

Under the usual regularity conditions this motivates a replicator/advection/diffusion description of schematic form

```text
partial_t f
= f (pi(r;f)-mean_f pi)
  - partial_r[v(r,f) f]
  + D partial_rr f.
```

The exact limiting PDE depends on the declared mutation kernel and time scaling and is not asserted by the finite-grid code alone.

## 4. Local accessibility versus global payoff

PAYOFF already separates global architecture value from local evolutionary accessibility. The small-jump layer makes the mutation neighbourhood explicit.

For grid payoff values `pi_i`, define

```text
J_better(i)
=min |j-i| over j with pi_j > pi_i.
```

`minimum_jump_to_better_state()` computes this diagnostic. Therefore a state may satisfy

```text
global better architecture exists
and
J_available < J_better
```

at the same time.

This is the finite-grid analogue of the existing discontinuous modularization barrier and hard-module accessibility results: a global optimum and a locally accessible path are different objects.

## 5. Relation to existing PAYOFF limits

The new implementation nests several existing cases:

```text
gamma=0
-> intrinsic continuous-architecture payoff only

epsilon=None
-> global quadratic architecture interaction

mutation_rate=0
-> selection without architecture mutation

jump_radius_bins=0
-> mutation operator is the identity

narrow concentrated f
-> monomorphic/local adaptive-dynamics regime

mass near endpoints r=0,L
-> connection to the original two-architecture PAYOFF game.
```

No claim is made that these finite-grid limits are exact identities with every previously registered stochastic process. They are bridge cases that keep the estimands separate.

## 6. New testable questions

The implementation now makes three previously implicit quantities explicit:

```text
interaction radius epsilon,
mutation/jump radius J,
population architecture distribution f.
```

This permits prospective tests of:

1. whether the existing branching boundary is robust to bounded rather than global architecture interaction;
2. whether endpoint coexistence is reached under local mutation or remains separated by an accessibility barrier;
3. whether shrinking interaction radius produces persistent multiple architecture clusters;
4. whether the same intrinsic landscape gives different long-run states under different mutation radii.

These are extension questions, not results already established by the current repository.

## 7. Reproduce the implementation checks

```bash
pytest -q tests/test_mesoscopic_architecture.py
```

The tests verify mass conservation, locality of the mutation operator, bounded-kernel exclusion of distant architectures, intrinsic-selection direction, and the minimum-jump accessibility diagnostic.
