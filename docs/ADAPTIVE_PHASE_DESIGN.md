# Adaptive phase measurements on an explicit finite PAYOFF panel

Status: optional finite-panel extension; synthetic examples only. The quadratic /
triangular payoff family and frozen-resident target are unchanged. This extends
`PHASE_OBSERVATION_BUDGET.md`, retaining its fixed-bundle comparator and its warning
that finite-panel discrimination is not continuous-region certification.

## What changes

A fixed bundle commits to all contrasts before acquisition. An adaptive policy
chooses the next contrast using only already measured responses. The optimizer now
returns the smallest WORST-PATH acquisition cost needed to identify the binary
phase on every possible response path, within the declared finite candidate set.
Each candidate can be used once per path. The acquisition is assumed noninvasive,
order-invariant and matched on the same context and payoff scale. Bounded errors
are Cartesian across queries, and the parameter world remains fixed throughout.
No posterior weights or hidden actual-world outcomes are supplied to the planner.

## Exact decision recursion

For retained world set S and available query set R, let C(S,R) be the minimum
worst-path cost of resolving the phase. Then

    C(S,R)=0                           if the phase is constant on S;
    C(S,R)=min_q [cost(q)+max_y C(S_y,R minus q)] otherwise,

where S_y contains worlds whose closed prediction/error intervals include y.
An infeasible continuation has infinite cost. The minimum is exact because a
policy must choose a first query, pay its cost, and supply a valid continuation for
EVERY possible outcome; the minimizing choice and optimal children attain this
lower bound. The nested nonempty retained sets on a finite history contain a fixed
world, so adversarial response selection does not require the true world to change.

Continuous responses do not require a numerical grid. Sort all exact interval
endpoints. Every endpoint is a singleton cell, and every open gap between adjacent
endpoints is another cell; the compatible-world set is constant on each such cell.
Discard empty cells. Rational endpoints and exact midpoints enumerate ALL distinct
response cases. Keeping singleton endpoints is essential: touching closed intervals
remain ambiguous even if their interiors do not overlap.

A resource cap raises `PhaseSearchLimitError`. Reaching that cap is not evidence
that no identifying tree exists. A completed computation returns separately:

- the minimum worst-case cost;
- the minimum resolving fixed-bundle cost;
- whether the given budget funds the adaptive tree;
- a concrete inseparable-pair witness when the entire query vocabulary is insufficient.

At most eight queries and 64 worlds are accepted. The receipt uses exact rational
arithmetic for geometry and integer costs. It never certifies an unenumerated
continuous parameter region or identifies mutation support.

## Why some ambiguities cannot be removed even adaptively

If two opposite-phase worlds have intersecting response intervals for EVERY
available query, choose one response in each intersection. This single common
response vector is compatible with both worlds. Any adaptive policy sees the same
history in the two worlds and cannot resolve them. Conversely, if every opposite-
phase pair is separated by some query, the full fixed bundle resolves the phase.
Thus adaptivity can reduce the worst acquisition cost but cannot make an intrinsically
insufficient query vocabulary sufficient under this Cartesian bounded-error model.

## Witness from the actual quadratic / triangular formulas

These are four valid parameter vectors, not arbitrary assigned phase labels.
All have kappa=1 and feasible length L=1:

| World | alpha | G | epsilon | Barrier phase? |
|---|---:|---:|---:|---|
| low_alpha_wide | 0.5 | 16/9 | 0.4 | no |
| low_alpha_middle | 0.5 | 2 | 0.3 | yes |
| high_alpha_middle | 0.95 | 2 | 0.3 | no |
| high_alpha_narrow | 0.95 | 10/3 | 0.25 | yes |

Three matched response queries are available, each costing one acquisition unit
and each with error bounded by +/-0.001:

| World | B(0.5) | A(0.2) | A(0.1) |
|---|---:|---:|---:|
| low_alpha_wide | 1/8 | 8/225 | 1/75 |
| low_alpha_middle | 1/8 | 2/75 | 1/75 |
| high_alpha_middle | 7/20 | 2/75 | 1/75 |
| high_alpha_narrow | 7/20 | 2/75 | 1/50 |

No fixed pair suffices. B(0.5)+A(0.1) cannot distinguish the low-alpha pair;
B(0.5)+A(0.2) cannot distinguish the high-alpha pair; A(0.1)+A(0.2) cannot distinguish
the two middle-kernel worlds, whose intrinsic payoffs and phases differ. The full
three-query bundle resolves all pairs.

The adaptive tree first measures B(0.5). The two group response bands are disjoint.
Near 1/8, it measures A(0.2); near 7/20, it measures A(0.1). Each remaining pair is
then separated by more than twice the error bound. The phase is identified in at
most TWO measurements, and one measurement cannot suffice. The exact optimal costs
are therefore 2 adaptive versus 3 fixed: one fewer acquisition, not better instrument
precision or an empirical sample-size guarantee.

The distinction has an exact precision limit as well. If every query has common
error e, the high-alpha pair differs only by 1/150 at A(0.1). At e=1/300 their bands
touch. No fixed or adaptive plan using these three contrasts can then guarantee
identification. For 0<=e<1/300 the stated adaptive tree works. Adaptivity saves
queries here but does not remove this response-resolution requirement.

## Execute without future-outcome leakage

    python -m src.adaptive_phase_design
    python -m pytest -q tests/test_adaptive_phase_design.py

API: `plan_adaptive_phase_budget`, `execute_phase_policy`. The executor asks a
caller-supplied callback for the selected query only, follows its exact response
cell, and stops at a same-phase leaf. Responses inconsistent with every remaining
world abort. No fabricated response is used during planning. Execution examples
use synthetic responses and do not represent actual acquired data.

Real application still requires a calibrated architecture coordinate, common payoff
scale, supported kernel family and explicit conditioning data. Feed actual new
response bands back into `certify_bounded_triangular` for its separate continuous-
set certificate. A phase label in this file concerns a frozen-resident payoff ridge,
not an evolving resident's trapping, fixation probability, or mutation jump bound.

The decision-tree recurrence is a standard finite sequential-design construction;
its contribution here is the verified adapter to PAYOFF's actual response formula,
exact bounded-error cells and constructive identifiability/cost comparisons.

## Robustness and an adverse benchmark

The routing witness does not require exact equality of nominal coefficients.
A separate sufficient certificate in the regression test allows every alpha,
kappa, G and epsilon in each of the four nominal worlds to vary independently by
+/-0.0001. Rational phase-box inequalities certify the same phase in each local
box. Monotonic response bounds, with the additional +/-0.001 observation error,
certify that the first query still separates the two groups and each second query
still separates the corresponding target phases. The nominal inseparable pairs
remain contained in the local boxes, so their fixed-bundle lower bound also remains.
This certifies the example's declared four-box neighbourhood, NOT an arbitrary
continuous feasible set returned by a real-data calibration.

An independently seeded 500-case panel check verified the optimizer but found no
strict adaptive cost saving among those randomly generated panels. The deliberately
constructed routing witness demonstrates a possibility and a robust local example;
it does not estimate how often the advantage occurs in biological applications.
