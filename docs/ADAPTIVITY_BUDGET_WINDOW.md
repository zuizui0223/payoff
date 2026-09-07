# Intermediate budget window for adaptive PAYOFF phase resolution

Status: optional finite-panel diagnostic. All examples are synthetic; no continuous parameter region or natural population is certified here.

## Two minimum costs

The exact finite-panel solvers already return

```text
C_adapt = minimum worst-path cost of a resolving adaptive tree
C_fixed = minimum acquisition cost of a resolving fixed bundle.
```

For an integer acquisition budget `B`, adaptive routing has an exclusive resolution advantage exactly when

```text
C_adapt <= B < C_fixed.
```

Implementation: `src/adaptivity_budget_profile.py`.

## Registered routing witness

For the existing four-world quadratic/triangular witness,

```text
C_adapt = 2
C_fixed = 3.
```

Therefore the adaptive-only resolution window is

```text
B = 2.
```

The full budget profile is:

```text
B=0,1  -> neither class guarantees phase resolution
B=2    -> adaptive tree guarantees resolution; no fixed bundle can
B>=3   -> both classes can guarantee resolution.
```

The positive routing advantage is therefore neither a zero-budget phenomenon nor a permanent superiority at large budget. It appears when there is enough resource to route and execute one branch-specific continuation, but not enough to buy every contrast a fixed design would need.

## Direct-resolution control

A two-world control has one interaction contrast that directly separates the two phases. Then

```text
C_adapt=C_fixed=1
```

and the adaptive-only budget window is empty.

## Relation to measurement precision

This budget window is conditional on the declared query error bounds and candidate vocabulary. If precision degrades until opposite-phase response intervals overlap for every available contrast, both minimum costs become undefined because neither class can guarantee phase identification.

Thus

```text
more adaptive planning
cannot replace insufficient measurement resolution.
```

Conversely, improving precision can change both minimum costs and therefore the width of the adaptive-only budget window.

## Claim boundary

- Costs are abstract positive acquisition-resource units, not biological switching costs.
- The profile concerns the finite enumerated panel and frozen-resident phase target.
- A budget window is not a field sample-size recommendation.
- It does not imply adaptivity is common in randomly generated or empirical panels; the existing adverse benchmark found no strict saving in its independently seeded 500-case panel check.
- Continuous-region certification remains the responsibility of the bounded-error identification route after actual new response bands are obtained.

## Reproduce

```bash
python -m pytest -q tests/test_adaptivity_budget_profile.py
```

## Exact precision and unequal-cost continuation

The full-vocabulary error-scale ceiling is now available as an exact certificate,
including an opposite-phase pair and common response vector at a finite boundary.
For the registered witness the separate error thresholds are `9/80`, `1/225`,
and `1/300` (all strict), and unequal positive acquisition costs give
`C_adapt=c_B+max(c_20,c_10)` versus `C_fixed=c_B+c_20+c_10`.

See [`PRECISION_LIMIT_HANDOFF.md`](PRECISION_LIMIT_HANDOFF.md) and the proof in
[`../theory/FINITE_PANEL_PRECISION_LIMIT.md`](../theory/FINITE_PANEL_PRECISION_LIMIT.md).
