# Budgeted observations to discriminate frozen-resident PAYOFF phases

Status: optional finite-panel design. All bundled examples are synthetic. This
does not modify existing population dynamics or turn a finite panel into the
continuous compatible set in `BOUNDED_ERROR_IDENTIFICATION.md`.

## Question and contract

After observations leave more than one phase possible, which affordable set of
additional matched payoff contrasts distinguishes the phases? The target is the
binary statement "a frozen-resident local ridge has a better outside optimum",
not the complete parameter vector or actual evolutionary trapping.

Supply a finite, explicitly enumerated panel of `ArchitectureWorld` objects,
panel provenance, feasible architecture length, and the matched-design declaration.
Every world must satisfy positive coefficients and `0 < epsilon < alpha/kappa <= L`.
Exact duplicate parameter vectors are rejected: duplicating rows would change the
secondary pair-count objective. Metadata does not verify biological calibration,
common scale, or completeness of the panel. `retain_worlds_in_bands` optionally
filters this panel using the earlier simultaneous response-band contract.

For candidate `ContrastQuery`, declare its kind, coordinate, response error bound,
and positive integer acquisition cost. Predictions are

    intrinsic:   B(r) = alpha*r - kappa*r^2/2
    interaction: A(d) = G*d^2*max(0,1-d/epsilon).

The observed response lies in `[prediction-error, prediction+error]`. Errors are
bounded-adversarial, not standard errors or Gaussian noise. Architecture-coordinate
error and cross-stage scale failure are not modelled. Candidate choices are fixed
before any future response is read.

## Exact finite-panel discrimination theorem

For opposite-phase worlds i,j, a query q separates the pair if and only if

    abs(prediction_i(q)-prediction_j(q)) > 2*error(q).

Equality is insufficient: closed response intervals touch at a common outcome.

Under the declared Cartesian bounded-error model, a fixed bundle identifies the
phase for every possible response if and only if it separates EVERY opposite-phase
pair on at least one coordinate. Proof: two Cartesian response boxes intersect
exactly when all their coordinate intervals intersect. An unseparated pair admits
a common observation vector and hence remains ambiguous; covering all pairs
prevents any observation vector from retaining two different phase labels.

This becomes an exact finite-budget pair-cover problem. The implementation
searches all affordable subsets of at most 16 declared queries on at most 128
worlds using bitsets. Its objective is first to minimize the number of uncovered
opposite-phase pairs, then minimize total acquisition cost. When full separation
is affordable, this gives the cheapest resolving bundle within the budget.
When not, pair count is only a finite-panel design heuristic; it is not a posterior
probability, continuum volume, or worst-case remaining entropy.

The solver returns ALL optimal bundles under those two criteria. For a selected
non-resolving optimum it also returns one opposite-phase world pair and an exact
rational observation vector compatible with both. This is a constructive ambiguity
witness, not a fabricated future observation.

## Same old response, different phase, different next distance

Two synthetic worlds share `alpha=0.5, kappa=1`:

    world 1: G=2,    epsilon=0.3 -> barrier phase
    world 2: G=16/9, epsilon=0.4 -> ridge not below outside optimum.

Both predict `A(0.1)=1/75`. Their intrinsic responses also agree at every r.
Thus repeated measurements at that old distance cannot distinguish them even
with exact response values. This is an observation-direction ambiguity, not a
problem solved by replicating the same contrast indefinitely.

At distance `d=0.3`, however,

    world 1 predicts 0
    world 2 predicts 0.04.

With bounded response error 0.005 and equal query costs, the one-unit plan chooses
`d=0.3`. The two response intervals are disjoint. At error 0.02 they merely touch;
the solver correctly refuses guaranteed discrimination. Under bounded-adversarial
errors, repeating an unchanged noisy contrast also cannot guarantee improvement:
an adversary can repeat the same response. A justified stochastic error model
could give replication a different value, but is not silently assumed here.

## Assimilation and claim boundaries

`condition_on_phase_bundle` accepts outcomes for exactly the actually selected
queries, retains every compatible panel world, and errors on an empty retained
panel. An empty panel means panel/data incompatibility, not proof that no
biological explanation exists. Phase labels are evaluated with the existing
rational discriminant, not rounded roots.

A finite resolving design is NOT a phase certificate for unenumerated parameter
worlds. The receipt always carries `continuous_region_certified=False`. Sampling
polygon vertices does not justify removing this warning. The continuous bounded-
error certificate must be rerun on actual new response bands for its own guarantee.
An adaptive design could outperform a precommitted bundle and is not optimized here.

Positive common payoff rescaling preserves phase and separability only when all
response-error bounds are rescaled too. None of these measurements identifies a
hard mutation-support bound, fixation probability, or evolving-resident barrier.

The pair-cover formulation is an elementary consequence of the declared response
sets. No general claim of inventing non-myopic experimental design is made.

## Reproduce

    python -m src.phase_observation_budget
    python -m pytest -q tests/test_phase_observation_budget.py

Optional API: `ArchitectureWorld`, `ContrastQuery`, `retain_worlds_in_bands`,
`plan_phase_observation_budget`, `condition_on_phase_bundle`.

See also `EMPIRICAL_IDENTIFICATION_CONTRACT.md` and
`BOUNDED_ERROR_IDENTIFICATION.md`. Calibration observations used to construct the
panel cannot also serve as independent validation of that fitted panel.
