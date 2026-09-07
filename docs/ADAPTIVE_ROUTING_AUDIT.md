# Branch-dependent routing in adaptive PAYOFF phase design

Status: optional structural audit on the existing finite-panel adaptive phase design. It adds no probability model to PAYOFF and does not certify a continuous parameter region.

## Why a structural audit instead of information bits

The finite-panel PAYOFF design uses bounded-adversarial response intervals and does not assign probabilities to architecture worlds or response branches. Therefore this layer does **not** invent Shannon information.

It asks a simpler question:

> after the first measured contrast, do different possible response branches require different immediate next contrasts?

Implementation: `src/adaptive_routing_audit.py`.

## Registered witness

The existing four-world witness uses

```text
intrinsic_r_0.5
interaction_d_0.2
interaction_d_0.1
```

with the exact quadratic intrinsic payoff and triangular interaction response already registered in PAYOFF.

The minimum resolving fixed bundle costs 3 acquisition units. The adaptive optimum costs 2.

Its first query is

```text
intrinsic_r_0.5.
```

That first measurement does not itself resolve phase on every possible response branch. Instead it routes the continuation:

```text
low-alpha response branch  -> interaction_d_0.2
high-alpha response branch -> interaction_d_0.1.
```

Hence the audit reports

```text
branch_dependent_continuation = true
root_alone_resolves_phase_on_every_outcome = false
adaptive_worst_case_cost_saving = 1
routing_without_direct_phase_resolution = true.
```

This is the set-valued PAYOFF analogue of the MROD routing witness: the first observation is valuable because it selects the appropriate next measurement, not because it finishes the target decision immediately.

## Direct-resolution control

A two-world control has a single interaction-distance contrast whose response intervals already separate the two phases. The root therefore resolves the phase directly; all children stop and the minimum fixed and adaptive costs are both one.

The audit reports no routing-only value.

Thus

```text
branching in a decision tree
!=
routing value.
```

The continuation must actually differ across possible first outcomes, and the exact adaptive solver must realize a positive acquisition saving before this finite-panel audit calls it a routing-without-direct-resolution witness.

## Claim boundaries

- No world probabilities are introduced; no result is expressed in bits.
- Different branch actions do not by themselves prove a scientific advantage. The positive fixed-versus-adaptive cost difference is reported separately.
- The target remains the frozen-resident binary barrier phase on the explicitly enumerated panel.
- A finite-panel routing witness is not a continuous-region phase certificate.
- The architecture coordinate, common payoff scale, kernel family, matched context, noninvasive acquisition and bounded-error contract remain assumptions.
- Adaptivity can reduce the number of contrasts but cannot overcome an insufficient response-resolution vocabulary: the existing `e >= 1/300` adverse limit remains.

## Reproduce

```bash
python -m pytest -q tests/test_adaptive_routing_audit.py
```

Related files:

```text
src/adaptive_phase_design.py
src/phase_observation_budget.py
docs/ADAPTIVE_PHASE_DESIGN.md
```
