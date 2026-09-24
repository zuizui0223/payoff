# PAYOFF-B migration–phenology synthetic results receipt

Frozen: 2026-09-20

This receipt records the first synthetic results from the migration–phenology
tracking extension. These are model results under declared synthetic designs,
not calibrated natural frequencies or ecological thresholds.

## 1. Core distinction

The model asks which adaptive axis tracks a moving environment:

    migration x phenology
    -> environmental tracking
    -> partner-axis mismatch
    -> growth
    -> population persistence.

This is separate from izu-core's starting-state x realized-community response
geometry.

## 2. Deterministic coordination barriers

The two-species rare-mutation model compares:

    locally accessible unilateral substitutions

against

    a coordinated matched-pair optimum.

A coordination barrier is present when the matched pair has higher joint payoff
but the alternating strictly improving unilateral walk stops below it.

In the first full ecological grid

    interaction strength: 5 levels
    cost bias:            5 levels
    climate velocity:     3 levels

44 of 75 ecological cells contained a positive coordination gap.

The same 44/75 ecological pattern reappeared when crossed with nine demographic
designs, producing 396 barrier cells out of 675 total cells.

The barrier therefore is not a rare corner of this declared synthetic design.
The numerical frequencies are design-volume frequencies only.

## 3. Demographic transport

Low-density tracking payoff g_t was transported into integer abundance through

    E[N_(t+1) | N_t]
    = N_t exp[g_t - d N_t/K],

followed by Poisson demographic sampling. Zero abundance is absorbing.

### Initial 32-replicate stress pilot

Workflow run: 35469501599

Across 675 cells:

    barriers:                         396
    barrier cells with gain >= 0.10: 9
    maximum persistence gain:        0.1875

The largest cell was

    interaction = 0.1
    cost bias   = -0.08
    velocity    = 0.04
    g0          = 0.04
    K           = 100

with local versus matched persistence

    0.59375 -> 0.78125.

This extreme cell-level effect was treated as a pilot result rather than a
promoted conclusion.

### Independent 128-replicate replication

Workflow run: 35469664405

The complete 675-cell design was rerun with an independent seed and four times
more demographic replicates.

Results:

    barriers:                         396
    barrier cells with gain >= 0.10: 0
    maximum persistence gain:        0.09375

Therefore the >=10 percentage-point cell effects from the 32-replicate pilot
did not replicate and are not retained as a headline result.

The aggregate structure did replicate.

For barrier cells, selected growth x K summaries were:

    g0=0.04, K=30:
        local persistence   0.01864
        matched persistence 0.02273
        mean gain           0.00408

    g0=0.04, K=100:
        local persistence   0.54936
        matched persistence 0.57049
        mean gain           0.02113

    g0=0.04, K=300:
        local persistence   0.98899
        matched persistence 0.99130
        mean gain           0.00231

    g0=0.12, K=30:
        local persistence   0.26012
        matched persistence 0.26953
        mean gain           0.00941

    g0=0.12, K=300:
        both local and matched persistence 1.0.

Across all 396 barrier cells in the independent replication, mean persistence
gain was approximately 0.00552.

When barrier cells were grouped by local joint persistence, cells with local
persistence in 0.3–0.7 had mean gain approximately 0.01974, whereas cells in
0.9–1 had mean gain approximately 0.00111.

The retained interpretation is therefore a **demographic visibility window**:

> Coordination barriers are often demographically cryptic when both strategies
> are nearly doomed or nearly certain to persist, and become most visible near
> the persistence transition.

This is an ensemble-level synthetic pattern. Individual cell rankings were not
stable enough to promote.

## 4. Finite-N weak-mutation tracking

For a resident and mutant with growth difference Delta g, the finite-N
frequency-independent Moran mapping uses

    r = exp(beta Delta g).

With symmetric strategy mutation, reciprocal fixation gives the exact
stationary law

    Pi_i proportional to exp[beta (N-1) g_i].

Thus larger N or stronger selection concentrates occupancy on high-payoff
migration–phenology strategies; small N retains broader strategy occupancy.

The exact law and explicit substitution simulations are implemented and covered
by CI.

## 5. Drift-assisted coordination escape

Workflow run: 35469853874

A representative verified barrier regime had

    accessibility gap = 0.0016
    deterministic local joint growth   = 0.340292788918
    coordinated matched joint growth   = 0.341892788918.

Finite-N stochastic substitutions were then started at the deterministic local
endpoint.

At beta=5:

    N=10:
        escape-replicate fraction      0.9375
        high-payoff occupancy          0.00494
        mean joint growth              0.31657

    N=30:
        escape-replicate fraction      0.96875
        high-payoff occupancy          0.04709
        mean joint growth              0.33416

    N=100:
        escape-replicate fraction      0
        local-endpoint occupancy       0.87089
        mean joint growth              0.33985

    N>=300:
        local-endpoint occupancy       1.0.

At beta=20:

    N=10:
        escape-replicate fraction      0.9375
        high-payoff occupancy          0.07006
        mean joint growth              0.33594

    N>=30:
        no high-payoff escape was retained in the sampled design.

The retained conclusion is deliberately asymmetric:

> Finite-population drift can cross a deterministic coordination barrier, but
> in the sampled regime the drift load from broader exploration outweighed the
> small coordinated payoff gain, so mean long-run joint growth did not exceed
> the deterministic local endpoint.

This is **drift-assisted barrier crossing**, not demonstrated drift rescue.

## 6. Current strongest synthetic story

The current hierarchy is:

    moving environment
        -> migration / phenology substitutability
        -> partner-axis matching
        -> coordination barrier
        -> local accessibility != coordinated value
        -> demographic effect depends on persistence regime
        -> finite-N drift can cross the barrier
        -> but excessive drift carries a payoff load.

In compact form:

> Interacting species can become evolutionarily locked into a jointly
> suboptimal way of tracking environmental change. The lock is often
> demographically invisible away from persistence boundaries. Finite-population
> drift can break the lock, but barrier crossing is not automatically
> beneficial because the same drift broadens occupancy into lower-payoff
> strategies.

## 7. Claim ceiling

These results do not establish:

- natural frequencies of migration, phenological change, or mixed tracking;
- a universal 58.7% prevalence of coordination barriers;
- a universal persistence gain from coordinated adaptation;
- a universal small-population benefit;
- that drift improves long-run fitness;
- that any named plant–pollinator system follows this parameterization.

The next strong tests are robustness to interaction form, mutation geometry,
bounded environmental forcing, explicit spatial landscapes, and empirical
parameterization.
