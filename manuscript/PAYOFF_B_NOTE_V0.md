# A unique finite migration optimum under exact anti-phase environmental switching

## Scope

This Note isolates one result from the broader PAYOFF programme: in the declared symmetric two-patch, two-season anti-phase model, the temporal premium has exactly one positive migration optimum for every nonzero seasonal contrast.

It does **not** present the full architecture-payoff hierarchy, continuous branching theory, topology theory, rare-mutation occupancy, or general spatial spectral transport.

## Model

Let the two patches alternate exactly out of phase across seasons of duration `tau`:

```text
season A: (r_bar+x, r_bar-x)
season B: (r_bar-x, r_bar+x)
```

with symmetric migration rate `m`.

The exact long-run growth exponent is

```text
Lambda_F
= r_bar-m
  +(1/tau) asinh[
      m/sqrt(m^2+x^2)
      *sinh(tau sqrt(m^2+x^2))
    ].
```

Relative to the static mean system, define the temporal premium

```text
P = Lambda_F-r_bar.
```

Using dimensionless variables

```text
u = m tau >= 0,
v = |x| tau > 0,
```

write

```text
F(u,v)=tau P
= -u
  +asinh[
      u/sqrt(u^2+v^2)
      *sinh(sqrt(u^2+v^2))
    ].
```

## Main theorem

For every fixed nonzero seasonal contrast `v>0`, `F(u,v)` has exactly one stationary point on `u>0`, and that point is the unique global maximum.

The derivative sign reduces to the comparison

```text
u^2/d^2 < R(d),
```

where

```text
d=sqrt(u^2+v^2)
```

and

```text
R(d)
= [sinh^2 d-d^2]
  /[d cosh d-sinh d]^2.
```

The left-hand side is strictly increasing in `d`, while `R(d)` is strictly decreasing and positive for `d>0`. They therefore cross exactly once. Hence the premium rises, reaches one interior maximum, and then declines.

## Scaling law

Let `u_star(v)` denote the unique maximizer. Then

```text
m_star
= u_star(|x|tau)/tau.
```

Thus all exact anti-phase optima collapse onto one dimensionless scaling curve.

## Weak-contrast limit

As

```text
v -> 0,
```

```text
u_star(v)
-> 1.60611529880277...
```

and the maximal temporal premium obeys

```text
P_max
~= 0.13248753945 x^2 tau.
```

## Strong-contrast limit

As

```text
v -> infinity,
```

```text
u_star(v)
= 1+1/v+O(v^-2),
```

so

```text
m_star tau -> 1.
```

At the optimum,

```text
max_u F(u,v)
= v-log v-1+O(v^-1).
```

## Biological interpretation

The result is sharper than the statement that intermediate migration can be favorable. In this exact anti-phase system, the best migration timescale is always of the same order as the environmental switching timescale:

```text
weak contrast:   m_star tau -> 1.6061153...
strong contrast: m_star tau -> 1
```

The optimum therefore remains finite and bounded as seasonal contrast changes.

## Novelty boundary

Intermediate-dispersal optima are already known in temporally varying source-sink systems. The contribution claimed here is narrower:

1. an exact closed-form anti-phase growth exponent for the declared symmetric model;
2. an exact uniqueness proof for the positive migration optimum;
3. the one-parameter scaling law `u_star(v)`;
4. weak- and strong-contrast asymptotic limits that bound the optimal migration timescale.

No universal claim is made for arbitrary periodic environments, asymmetric migration, more than two patches, stochastic forcing, or general noncommuting seasonal operators.

## Planned compact structure

```text
1. Motivation: why "intermediate migration" is not yet a sharp prediction
2. Exact anti-phase model and closed-form Floquet exponent
3. Uniqueness theorem
4. Weak- and strong-contrast asymptotics
5. Biological timescale interpretation
6. Discussion and claim boundary
```

## Canonical proof source

- `theory/EXACT_ANTI_PHASE_OPTIMUM.md`
- `theory/WEAK_CONTRAST_UNIVERSAL_MIGRATION_OPTIMUM.md`
- `docs/TEMPORAL_HANDOFF.md`

```text
STATUS = NOTE_V0_SCOPE_FROZEN
```
