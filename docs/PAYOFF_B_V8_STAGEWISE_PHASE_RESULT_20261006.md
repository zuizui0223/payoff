# PAYOFF-B V8 stagewise population-phase transition result — 2026-10-06

Status: **POSTHOC POPULATION-FRONT PHASE DIAGNOSTIC; FROZEN V8 PRIMARY UNCHANGED**

## Question

In the restricted source-target subset where the same species has at least six
annual arrival estimates in both source and target cells in both periods, how
does population-front timing relative to local green-up transform between the
two stages?

Define local signed phase:

    e = bird arrival - local mid-green-up.

Negative values mean the estimated population front arrives before local
mid-green-up.

Define stage transformation:

    Delta_e_route = e_target - e_source

which is exactly

    (target arrival - source arrival)
      -
    (target green-up - source green-up).

Negative values mean the population front becomes earlier relative to local
mid-green-up between source and target.

This is population-level stage geometry, not individual feedback or a direct
estimate of correction gain.

## Sample

- **56 species-source-target units**;
- **31 unique source-target pairs**;
- **14 species**.

This is a restricted subset and should not be generalized mechanically to the
full 166-pair environmental network.

## Local phase shifted at both stages, but more strongly at the source

Pair means:

Source phase:
- early = **-4.56 d**;
- late = **-1.06 d**;
- shift = **+3.50 d**;
- 95% pair-bootstrap CI **+2.99 to +3.95 d**.

Target phase:
- early = **-8.14 d**;
- late = **-6.00 d**;
- shift = **+2.13 d**;
- 95% CI **+1.19 to +3.08 d**.

Thus the population front became less early relative to local mid-green-up at
both mapped stages, but the change was larger at the source.

Zero phase is not established as the fitness optimum; these are signed
relative-timing coordinates.

## Downstream phase transformation became more negative

Pair-mean stage transformation:

- early = **-3.57 d**;
- late = **-4.95 d**;
- late-minus-early change = **-1.37 d**;
- median change = **-1.64 d**;
- 95% pair-bootstrap CI = **-2.36 to -0.36 d**.

Direction:
- **23/31 pairs** became more negative;
- 8/31 more positive.

Equal-species:
- early = **-3.03 d**;
- late = **-4.96 d**;
- change = **-1.93 d**;
- 95% pair-incidence bootstrap CI = **-2.86 to -0.26 d**;
- **12/14 species** became more negative.

Therefore the larger late-period improvement in source local phase was not fully
retained at the target stage.

## Descriptive attenuation of the between-period source-stage shift

At the pair-mean level, the source-stage signed phase changed by **+3.50 d**
between periods, whereas the target-stage phase changed by **+2.13 d**.

Define the descriptive attenuation fraction:

    A
      =
    1 - delta_target_phase / delta_source_phase
      =
    - delta_phase_transform / delta_source_phase.

The estimate is:

- **A = 0.392**;
- pair-bootstrap 95% CI **0.101 to 0.656**.

Thus, on this aggregate scale, about 39% of the source-stage between-period
relative-timing shift was not retained at the target stage.

This is a descriptive stage-transformation fraction. It is **not**:
- an individual correction fraction;
- controller gain;
- evidence that zero phase is optimal;
- a fitness benefit estimate.

## Geometric decomposition

Population-front source-to-target interval:
- early = **7.20 d**;
- late = **5.69 d**;
- change = **-1.51 d**;
- 95% CI **-2.31 to -0.72 d**.

Green-up source-to-target interval:
- early = **10.78 d**;
- late = **10.64 d**;
- change = **-0.14 d**;
- 95% CI **-0.68 to +0.36 d**.

Thus the more negative downstream phase transformation is generated primarily
because the estimated migration front traversed the source-to-target interval
more quickly, while the green-up wave interval changed little.

This is consistent with the source paper's emphasis on migration-speed
adjustment, but it does not identify individual behavioral decisions.

## Descriptive stage-to-stage phase retention

Across the 31 pair-level stage summaries:

Early:
- source-to-target phase slope = **0.679**;
- correlation = **0.771**.

Late:
- slope = **0.558**;
- correlation = **0.732**.

These are descriptive cross-pair coordinates only. They are not controller-gain
estimates and are not used as a causal test.

## Arrival-estimate precision boundary

Mean posterior SD of arrival estimates decreased strongly:

Source:
- **3.22 d -> 0.87 d**.

Target:
- **2.84 d -> 1.01 d**.

This difference in posterior precision must be acknowledged in the manuscript.
The stagewise analysis uses posterior means and does not assume constant
measurement precision across periods.

## Ecological interpretation

In the subset where the same species' estimated migration front is observed at
both mapped stages:

1. the front generally reaches the source first;
2. local signed phase became less early at both stages;
3. the improvement was larger at the source than at the target;
4. the source-to-target population-front interval shortened while the
   source-to-target green-up interval changed little;
5. consequently, the downstream phase transformation became more negative.

A narrow licensed statement is:

> **Population-level relative timing changed across migration stages rather than
> being passively carried from the source to the target, and the late-period
> source-stage shift was not fully retained at the target stage.**

Do not state:
- individuals detected signed phase error and corrected it;
- the more negative transformation is necessarily maladaptive;
- zero phase is optimal;
- the result identifies actionability r(t) or controller gain;
- the restricted 31-pair subset represents all V8 routes.

## Role in V4.4

This result gives a same-system stagewise bridge between:
- environmental forecast opportunity; and
- realized population timing.

It complements, but does not replace, the mule-deer individual-level anchor.
Mule deer remain the stronger evidence that signed downstream behavioral
correction exists in nature.

## Provenance

Workflow:
- run: 37402488851
- artifact: 11385472835
- artifact SHA256:
  6bf859f01d2b3d0c0416693d87e685b4122e2b7c8b07d7a9cfa6e987de5f2dfe

Script:
analysis/movement_phenology/payoff_b_v8_stagewise_phase_transition.R
