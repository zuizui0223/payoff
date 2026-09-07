# Interior-frequency holdout theorem for canonical PAYOFF

Status: mathematical measurement-validation result for the declared deterministic
two-architecture PAYOFF model. No natural population is validated here.

## Endpoint identification does not validate the interior law

Reciprocal rare-invasion measurements give

```text
u = Delta(0)  = phi - eta
v = -Delta(1) = -phi - eta.
```

They identify the endpoint signs and, on a common positive scale, `(phi,eta)`.
But any nonlinear function can share the same two endpoints. Therefore the two
rare-invasion measurements alone do **not** validate the canonical frequency law

```text
Delta(p) = phi + eta(2p-1).
```

The missing falsification step is an independently predeclared measurement at
one or more strict interior frequencies `0<p<1`.

## No-refit theorem

For the canonical model,

```text
Delta(p) = (1-p)u - p v.
```

Hence exact endpoints make every interior prediction parameter-free. With closed,
simultaneous endpoint bands

```text
u in [uL,uH],  v in [vL,vH],
```

and Cartesian admissibility, the exact endpoint-derived prediction band is

```text
[(1-p)uL - p vH, (1-p)uH - p vL].
```

An interior observed closed band is compatible exactly when it intersects this
prediction band. Equality/contact counts as compatibility. Holdout observations
must never be used to tighten endpoint bands or refit `(phi,eta)`; otherwise the
check ceases to be an out-of-endpoint test.

If one registered holdout band is disjoint, the declared canonical linear
frequency response is rejected for that matched context. Passing all registered
holdouts establishes compatibility with this line, not uniqueness among all
possible nonlinear models.

## Why the scale requirement is stronger than phase identification

The reciprocal-invasion phase needs only the two oriented endpoint signs. Thus
separate unknown positive multipliers in the two assays leave strict phase labels
unchanged. Interior interpolation is different: a numerical line between endpoints
is meaningless unless endpoint and interior `D-minus-S` gaps share one positive
payoff/growth scale and orientation. This module therefore refuses holdout
validation without that declaration.

## Minimal interpretation

A single strict interior holdout can falsify the canonical line. More interior
frequencies improve coverage but do not by themselves identify an arbitrary
nonlinear frequency-response family. A successful receipt says only:

> the endpoint-derived canonical PAYOFF line survived the predeclared interior
> frequency checks under the stated closed-band contract.

It does not prove fixation, mutation support, historical causation, ecological
mechanism, SCH/BALANCE/BITA claims, or that `eta` has a particular biological
source.

Implementation: `src/frequency_response_holdout.py`.
Tests: `tests/test_frequency_response_holdout.py`.
