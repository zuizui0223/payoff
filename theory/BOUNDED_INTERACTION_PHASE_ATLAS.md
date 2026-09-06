# Bounded interaction, local branching, and mesoscopic phase fate

This note separates the **local adaptive-dynamics branching criterion** from the
**nonlocal population-distribution fate** once architecture interaction has a
finite range.

The finite-grid atlas is implemented in:

```text
src/architecture_phase_atlas.py
scripts/build_mesoscopic_phase_atlas.py
tests/test_architecture_phase_atlas.py
```

The atlas is a deterministic finite-grid experiment. It is not a new general
branching theorem.

---

## 1. Bounded architecture interaction

For recovery coordinate `r` and partner architecture `q`, use

```text
H_epsilon(r,q)
= -gamma (r-q)^2 1{|r-q| <= epsilon}.
```

The global PAYOFF kernel is recovered by `epsilon=None`.

For a monomorphic resident `x`, mutant relative payoff is locally

```text
f_epsilon(y,x)
= b(y)-b(x)-gamma(y-x)^2
```

whenever

```text
|y-x| < epsilon.
```

Therefore any strictly local derivative calculation at `y=x` is unchanged by
finite positive `epsilon`.

---

## Proposition BI1 — finite interaction range does not move the local branching boundary

For quadratic intrinsic payoff

```text
b(r)=alpha r-(kappa/2)r^2,
kappa>0,
```

and an interior singular architecture

```text
r0=alpha/kappa,
```

any `epsilon>0` gives the same local mutant curvature as the global kernel:

```text
partial_yy f_epsilon(y,r0)|_{y=r0}
= -kappa-2gamma.
```

Hence the local branching-compatible boundary remains

```text
gamma_branch=-kappa/2.
```

### Proof

There is an open neighbourhood of `y=r0` in which
`|y-r0|<epsilon`, so the indicator equals one identically there. The local
invasion function is therefore exactly the global-kernel quadratic on that
neighbourhood. Differentiating twice gives `-kappa-2gamma`. QED.

### Consequence

Finite interaction range can change what happens **after** local disruptive
selection begins without changing the infinitesimal branching threshold itself.

So these are different questions:

```text
local branching compatibility
!=
nonlocal branch separation / endpoint fate.
```

---

## Proposition BI2 — a hard interaction radius creates a payoff interface

For a monomorphic resident `x`, compare the one-sided mutant payoff at the
interaction boundary `|y-x|=epsilon`.

Inside the boundary the interaction term is

```text
-gamma epsilon^2.
```

Immediately outside it is zero. Therefore the one-sided interface jump is

```text
payoff_out - payoff_in = gamma epsilon^2.
```

Thus:

```text
gamma < 0
-> leaving the interaction neighbourhood produces a downward jump;

gamma > 0
-> leaving the interaction neighbourhood produces an upward jump.
```

This interface exists even when intrinsic architecture payoff `b(r)` is smooth.
It can therefore generate finite-jump accessibility structure that is absent
from the unbounded quadratic kernel.

This proposition is about the declared hard cutoff. Smooth compact-support
kernels need not have a discontinuous interface.

---

## 2. Why the population fate can differ from the local theorem

Under negative frequency feedback, nearby distinct architectures can initially
receive a mismatch reward when `gamma<-kappa/2`. With bounded interaction,
however, that reward disappears after their separation exceeds `epsilon`.

Therefore the global-kernel result

```text
local branching
-> continuing separation
-> endpoint coexistence
```

cannot be transported automatically to finite `epsilon`.

The bounded model can instead show:

```text
single persistent cluster,
interior multiple clusters,
or endpoint coexistence,
```

depending on interaction range, feedback strength, mutation scale and the
finite-grid update.

This is why the atlas reports the final distribution separately from the local
branching theorem.

---

## 3. Accessibility overlay

For a declared resident distribution, freeze its current architecture payoff
vector `pi_i`. A jump graph allows `i -> j` only when

```text
|i-j| <= delta_bins
and
pi_j > pi_i.
```

The atlas computes

```text
delta_critical
= minimum jump radius for which at least one strictly-uphill path reaches a
global payoff state.
```

Then

```text
delta_bins < delta_critical
-> small_jump_trapped = True.
```

This is deliberately an **all-uphill accessibility** statement. Recurrent
mutation can leak probability across a payoff valley over sufficiently long
time; the flag does not claim literal stochastic impossibility.

---

## 4. Canonical development sweep

The reproducible builder defaults to:

```text
alpha=0.5
kappa=1.0
L=1.0
bins=41
beta=1.5
mutation_rate=0.03
steps=800

gamma in {-2,-1,-0.75,-0.5,-0.25,0,0.5}
epsilon in {0.05,0.10,0.20,0.40,global}
jump_radius_bins in {1,2,4}.
```

This is 105 finite-grid cells.

The development sweep produced:

```text
single_cluster          85
interior_multicluster   11
endpoint_coexistence     9

small_jump_trapped      12 / 105 cells.
```

These counts are parameter-grid results, not prevalence claims.

### Global interaction recovers the analytic local boundary qualitatively

For `epsilon=global`:

```text
gamma = -2,-1,-0.75
-> endpoint coexistence for all three tested jump radii;

gamma = -0.5,-0.25,0,0.5
-> single cluster for all three tested jump radii.
```

Thus the sampled finite-grid transition falls on the expected strict side of

```text
gamma_branch=-kappa/2=-0.5.
```

This is a regression-style consistency check, not a numerical proof of the
analytic theorem.

### Finite interaction range changes branch maturation

At `epsilon=0.40`:

```text
gamma = -2,-1,-0.75
-> interior multicluster rather than endpoint coexistence.
```

At `epsilon=0.05` every sampled cell remained a single cluster, including the
strongly branch-compatible `gamma=-2` cells.

The safe interpretation is:

> local disruptive curvature can exist while finite interaction range prevents
> the same nonlocal endpoint fate seen under global interaction.

Do not reinterpret this finite sweep as an epsilon-dependent replacement for
the local theorem in Proposition BI1.

### Jump scale has two distinct roles

At `epsilon=0.20, gamma=-2`:

```text
jump radius 1 -> interior multicluster
jump radius 2 -> interior multicluster
jump radius 4 -> single cluster.
```

So larger jumps can increase accessibility while also smoothing or reconnecting
a population distribution strongly enough to erase a separated-cluster phase.

Therefore

```text
more accessible
!=
more differentiated.
```

This is one of the main reasons to keep the accessibility and population-phase
columns separate.

### Accessibility and clustering are orthogonal in the tested grid

Examples include:

```text
epsilon=0.10, gamma=-1:
critical uphill jump radius = 2 bins;
radius 1 is accessibility-trapped while the population phase remains one cluster.


epsilon=0.40, gamma=+0.5:
critical uphill jump radius = 5 bins;
small tested jump radii remain trapped despite coordination rather than disruptive feedback.
```

Thus a finite-jump barrier is not synonymous with branching or coexistence.

---

## 5. Reproduce

```bash
python scripts/build_mesoscopic_phase_atlas.py
```

Default outputs:

```text
outputs/mesoscopic_phase_atlas.csv
outputs/mesoscopic_phase_atlas_summary.json
```

The CSV reports both:

```text
dynamical_regime
small_jump_trapped
```

for every cell.

---

## 6. Claim boundary

This extension does **not** claim:

- that biological architecture interactions literally follow Hegselmann--Krause opinion dynamics;
- that a hard confidence radius is universal biology;
- that the finite-grid phase labels are continuum PDE theorems;
- that `small_jump_trapped=True` means valley crossing is impossible under recurrent stochastic mutation;
- that the 105-cell counts are biological frequencies;
- that finite `epsilon` changes the infinitesimal branching threshold for any `epsilon>0`.

The current positive result is narrower:

> PAYOFF's architecture branching criterion can be embedded in a bounded-
> interaction mesoscopic model in which the local branching threshold is
> retained but nonlocal branch fate and all-uphill accessibility become separate,
> measurable objects controlled by interaction range and jump scale.
