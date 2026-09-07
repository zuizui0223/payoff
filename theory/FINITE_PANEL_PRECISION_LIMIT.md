# Exact precision ceiling and weighted routing advantage

Status: proved for the declared finite-panel, Cartesian closed-error model.
The PAYOFF response adapter and regression tests use the existing quadratic /
triangular family and frozen-resident phase target. No natural population or
unenumerated continuous parameter region is certified.

## 1. The question left after the budget window

`docs/ADAPTIVITY_BUDGET_WINDOW.md` establishes the budget condition

```text
C_adapt <= B < C_fixed.
```

Those costs are conditional on measurement precision. We now separate two issues:

1. Does the entire measurement vocabulary contain enough resolving information?
2. If it does, how much acquisition resource does adaptive routing save?

No acquisition strategy can compensate for a vocabulary whose response bands
admit a shared outcome for two opposite-phase worlds.

## 2. Exact full-vocabulary precision theorem

Let W be a nonempty finite panel, with deterministic phase label h(w), and let
Q be a finite query vocabulary. Query q has a known response y_q(w) and a
nonnegative baseline error e_q. At a common error multiplier t >= 0 its possible
response is the CLOSED interval

```text
I_q(w;t) = [y_q(w)-t e_q, y_q(w)+t e_q].
```

The world stays fixed; acquisitions are noninvasive and order-invariant; the
joint admissible error set is Cartesian. No distribution over worlds or errors
is assumed. For an opposite-phase pair (i,j), define

```text
d_ij,q = |y_q(i)-y_q(j)| / (2 e_q)              when e_q > 0
         +infinity                             when e_q = 0 and responses differ
         0                                     when e_q = 0 and responses agree

t_ij = max_q d_ij,q

t_* = min_{h(i) != h(j)} t_ij.
```

Use max(empty)=0 and min(empty)=+infinity. Then:

> With unlimited acquisition budget, a fixed bundle or an adaptive policy
> guarantees phase identification on W exactly when 0 <= t < t_*.

A finite t_* is an EXCLUDED upper endpoint, not an achievable maximum.

### Proof: sufficiency

For t < t_* every opposite-phase pair has some query with disjoint intervals:
`|y_q(i)-y_q(j)| > 2 t e_q`, or a separating exact query. Acquire all queries.
If a full response vector retained opposite-phase worlds i and j, its component
at that separating query would have to belong to both disjoint intervals, a
contradiction. Thus every nonempty retained set has only one phase.

### Proof: necessity, including adaptive policies

For finite t >= t_* choose a minimizing opposite-phase pair. All its query
intervals intersect. Choose one response from each intersection. Cartesian
errors make this single complete response vector admissible under either fixed
world. Every adaptive policy follows the same observations and decisions in
those two worlds, so it cannot distinguish their phases. This construction does
not change the true world during acquisition and does not use future outcomes
in the planner. Closed-band contact is already enough for the obstruction.

For t_*=0 the panel is unidentifiable even at zero error; for t_*=+infinity it
is identifiable at every finite multiplier. A single-phase panel needs no query.

### Computable certificate

`src/phase_precision_certificate.py` computes all pair limits, a minimizing pair,
and a common response vector at the finite boundary, with exact rational
arithmetic. This vector remains admissible at every larger multiplier.
Complexity is O(|W|^2 |Q|); no decision-tree search is required for feasibility.
The public adapter obtains labels and responses from the existing PAYOFF model,
not user-assigned labels. Costs remain the job of the existing design solvers.

Increasing any baseline error cannot improve identifiability at a fixed scale;
adding a valid matched query cannot worsen it. Adaptivity changes acquisition
cost, not this full-vocabulary precision ceiling.

## 3. Exact heterogeneous thresholds in the registered PAYOFF witness

Use the four valid architecture worlds and three response formulas in
`docs/ADAPTIVE_PHASE_DESIGN.md`. In order (w0,w1,w2,w3), their phases are
`(no, yes, no, yes)` and the exact responses are:

| Query | w0 | w1 | w2 | w3 |
|---|---:|---:|---:|---:|
| B(1/2) | 1/8 | 1/8 | 7/20 | 7/20 |
| A(1/5) | 8/225 | 2/75 | 2/75 | 2/75 |
| A(1/10) | 1/75 | 1/75 | 1/75 | 1/50 |

Let the respective, independently declared error half-widths be e_B, e_20,
and e_10. The full vocabulary identifies the phase if and only if

```text
e_B  < 9/80,
e_20 < 1/225,
e_10 < 1/300.
```

Necessity follows from three unavoidable pairs: (w1,w2) differ only in B(1/2),
(w0,w1) only in A(1/5), and (w2,w3) only in A(1/10). Each half-width must be
strictly less than half its sole distinguishing gap. Under those inequalities,
B first separates the low/high-alpha groups; the appropriate interaction query
then separates each group's phases, proving sufficiency. If any one inequality
fails, that unavoidable pair defeats every fixed or adaptive policy.

With common error e, the exact ceiling is e < 1/300. With baseline errors
1/1000 the common multiplier ceiling is t < 10/3. At t=10/3 the certificate
returns w2 and w3 with the shared response vector

```text
B(1/2) = 7/20, A(1/5) = 2/75, A(1/10) = 1/60.
```

Consequently, improving the broad intrinsic contrast cannot compensate for an
unresolved narrow interaction contrast in this vocabulary. This is a conditional
measurement-identifiability statement, not a claim that those exact contrast
coordinates or thresholds apply universally in ecology.

## 4. Weighted acquisition-cost law

Assume the three strict precision conditions and arbitrary positive integer
acquisition costs c_B, c_20, c_10. Then the exact optimal costs are

```text
C_fixed = c_B + c_20 + c_10,
C_adapt = c_B + max(c_20,c_10),
C_fixed - C_adapt = min(c_20,c_10).
```

The adaptive-only integer budget window is therefore

```text
c_B + max(c_20,c_10) <= B < c_B + c_20 + c_10.
```

It contains exactly min(c_20,c_10) integer budgets.

### Proof

Each of the three unavoidable opposite-phase pairs requires its sole separating
query, so every resolving fixed bundle contains all three queries. The B-first
adaptive tree has the stated worst-path cost. If A(1/5) is queried first, a shared
response leaves {w1,w2,w3}; within that set B and A(1/10) are both unavoidable on
a worst-case path. Similarly, an A(1/10)-first tree can retain {w0,w1,w2}, forcing
both remaining queries on a worst-case path. Either interaction-first root
therefore incurs all three costs in the worst case. Positive costs make B the
unique optimal first query and prove the lower bound matching the construction.

This is a worst-case acquisition saving, with no assumed prevalence or expected
cost. It is not a payoff or an architectural switching cost.

## 5. Verification and claim ceiling

Tests include an independent endpoint/open-cell interval oracle on 120 seeded
response tables, the exact contact boundary, zero-error and zero-query cases,
40 seeded valid PAYOFF architecture panels against the existing adaptive and
fixed solvers, all 27 below/equal/above heterogeneous-error combinations, and
27 positive cost triples against the exact decision-tree optimizer.

The random checks validate the certificate, NOT the prevalence of adaptive
advantage. The previously reported 500-panel benchmark finding no strict saving
is unchanged. The weighted theorem concerns the registered four-world witness,
not arbitrary panels or its continuous neighbourhood under unequal costs.
The general precision theorem applies to any supplied finite panel under the
stated error contract. Its algebra is a finite discrimination consequence, not
a claim to invent a new general theory of experimental design.

PAYOFF remains a separate transport/population-game layer. This certificate does
not replace SCH conflict reconstruction, BALANCE architecture-cost comparisons,
BITA recovered-conflict mechanisms, meta-analytic pattern recovery, or actual
independent frequency-dependent evidence. It does not show fixation, evolving-
resident trapping, mutation support, or biological causal identification.

## Reproduce

```bash
python -m src.phase_precision_certificate
python -m pytest -q tests/test_phase_precision_certificate.py
```
