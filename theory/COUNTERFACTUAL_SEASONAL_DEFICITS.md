# PAYOFF-B: exact capacity × information × coordination deficit accounting

**Date:** 2026-11-14  
**Status:** source-free counterfactual mathematics; NOT a biological effect estimate, not a new theorem about generic value of information.  
**Scope:** two seasonal states, one binary cue, finite state-dependent timing actions and an explicit, *shared* joint-fitness loss scale.

## Why this is a necessary correction

The legacy partial-information toy model (theory/PARTIAL_INFORMATION_COORDINATION.md) can write
a clean additive information + coordination identity because it **holds capacity
adequate and fixed**. One cannot take that additive identity and infer three
separately observed natural causal effects called information, capacity and
coordination.

The Paper-2 mathematical correction (Supplementary Note S4.4 in the unmerged
Paper-2 draft) already warns that serial phase identities are not additive
fitness allocations. The new code makes this warning operational: it crosses
capacity and information interventions, identifies their mathematical
interaction, and **only then** defines an explicit three-part accounting rule.

## Five well-defined expected-loss counterfactuals

Let a latent future spring state be H in {late, early}, with prior
p=P(H=early). A predecision cue Z reports the state correctly with symmetric
accuracy q in [1/2,1]. A finite *limited* response set A_L is a subset of the
counterfactual *full* response set A_F. The same joint loss ell(a,H)
is used in every counterfactual.

Define R_{I,A}=sum_z min_{a in A} sum_h P(h,z) ell(a,h), the optimal
joint expected loss using the **available** cue. With perfect future
information before acting, define
R_{P,A}=sum_h P(h) min_{a in A} ell(a,h).

The four crossed regimes are:

| Symbol | Information available | Feasible action set | Objective |
| --- | --- | --- | --- |
| R_{P,F} | Perfect state | Full | Joint loss |
| R_{P,L} | Perfect state | Limited | Joint loss |
| R_{I,F} | Noisy cue | Full | Joint loss |
| R_{I,L} | Noisy cue | Limited | Joint loss |

For the fifth regime, the focal actor chooses a_L^private(z) in A_L to
minimize a separate **private** expected loss, but we then **score that action
using exactly the same joint loss**:

R_D = sum_{h,z} P(h,z) ell(a_L^private(z),h).

An observed animal is not assumed to implement this private optimum; it is a
declared game-theoretic benchmark.

Because A_L is contained in A_F and the perfect state Blackwell-dominates a
noisy cue for a centralized policy,

- R_{P,F} <= R_{P,L} <= R_{I,L};
- R_{P,F} <= R_{I,F} <= R_{I,L};
- R_{I,L} <= R_D.

## Both possible nested decompositions

Suppose information is improved first:

- information shortage at limited capacity = R_{I,L} - R_{P,L};
- capacity shortage with perfect information = R_{P,L} - R_{P,F}.

Suppose capacity is improved first:

- capacity shortage with the noisy cue = R_{I,L} - R_{I,F};
- information shortage at full capacity = R_{I,F} - R_{P,F}.

Both paths telescope to R_{I,L} - R_{P,F}, but they need **not assign the
same loss to each cause**.

Define the exact signed interaction:

    X = (R_{I,L} - R_{P,L}) - (R_{I,F} - R_{P,F})
      = (R_{I,L} - R_{I,F}) - (R_{P,L} - R_{P,F}).

X > 0 means information is more valuable with the *limited* response set
than with full capacity (e.g. a newly accessible robust/hedging action can
make the cue less valuable). X < 0 means limiting recourse destroys some
information value (e.g. only one committed action remains).

Therefore there is **no context-free natural information-deficit number**.
A decomposition must specify the counterfactual order or an allocation rule.

## Explicit symmetric two-order allocation (Shapley convention)

Average the two paths, treating the private-vs-joint coordination penalty as
the *last* layer at the available cue and limited feasible set:

    INFORMATION = 0.5 * [(R_{I,F}-R_{P,F}) + (R_{I,L}-R_{P,L})]
    CAPACITY    = 0.5 * [(R_{P,L}-R_{P,F}) + (R_{I,L}-R_{I,F})]
    COORDINATION = R_D - R_{I,L}
    TOTAL        = R_D - R_{P,F}

Thus, by algebra,

    TOTAL = INFORMATION + CAPACITY + COORDINATION.

All three allocated quantities are nonnegative under the declared common
objective, nested action sets, perfect-state benchmark, and centralized
joint optimum. The result is **an accounting identity**, not independent
additive causal mechanisms. Capacity/information shares are conventional
Shapley averages for those two factors; coordination is deliberately evaluated
last. Changing the baseline or the intervention order changes attribution.

## Two independently enumerable, opposing witnesses

### W1 — adding a robust action makes information less valuable

Use prior p=0.55 and q=0.55. The limited set is {late,early}; the full set
also offers a robust buffer strategy. Each loss vector is ordered
(normal spring, early spring):

| Action | Joint loss | Private loss |
| --- | --- | --- |
| late | (0, 3.5) | (0, 1.5) |
| early | (4.5, 0) | (2.5, 0) |
| buffer | (1, 1) | (1, 1) |

The *private* policy uses late after either cue. The *joint* limited policy
follows early only after the early cue. The extra full-capacity buffer action
becomes optimal after either noisy cue.

Exact risks:

    R_{P,F}=0; R_{P,L}=0;
    R_{I,F}=1.0000; R_{I,L}=1.7775; R_D=1.9250.

Allocation:

    information=1.38875
    capacity=0.38875
    coordination=0.14750
    total=1.92500
    X=+0.77750.

This case demonstrates both information × capacity interaction and a
private-versus-joint uptake wedge, in one explicit finite toy system.

### W2 — irreversibility eliminates the behavioral value of a cue

Use prior p=0.40, q=0.80, joint/private losses
late=(0,1), early=(2,0), limited actions={late}, full={late,early}.

    R_{P,F}=0; R_{P,L}=0.40;
    R_{I,F}=0.32; R_{I,L}=0.40; R_D=0.40.

Then:

    information=0.16
    capacity=0.24
    coordination=0
    total=0.40
    X=-0.32.

With only one feasible action, perfect information cannot change the
actor's response. This is the mathematical core of the irreversible
seasonal-commitment analogy, not a quantum phenomenon.

## Relationship to the empirical evidence

The V8 migratory-bird test found a **positive** early/late change in
source-target green-up correlation (+0.369 across 166 unique pairs),
contrary to the prespecified degradation prediction, while enhanced
connectivity did not license a bird-mismatch causal improvement. The
2026-10-19 to 2026-10-28 independent CC0 tracking audits are
descriptive/exploratory: some physical prior-weather signals associate
with subsequent GPS movements, but causal cue perception, remaining
actionability, partner timing and fitness were **not** jointly identified.
The new W1/W2 cases are **not fits to those observations**.

A biological test would need, independently and before outcome fitting:
(1) timestamped cue access and predictive quality q;
(2) intervention- or design-based feasible alternative actions/recourse;
(3) consequences measured on a common final reproductive/survival
fitness scale for each state/action;
(4) private and partner fitness payoffs under comparable conditions.

The four joint-risk surfaces are counterfactuals, not automatically
identified by movement correlations or observational phase-retention slopes.
One cannot estimate the three components by plugging observed q and a
post-treatment movement decision into this formula.

## Reproduction and scientific hold

- Engine: `src/seasonal_deficit_decomposition.py`
- Exhaustive independent cue-policy enumeration tests:
  `tests/test_seasonal_deficit_decomposition.py`
- Source-free witness runner:
  `scripts/run_seasonal_deficit_decomposition.py`
- Output status:
  `SYNTHETIC_COUNTERFACTUAL_IDENTITY_NOT_EMPIRICAL_MECHANISM`

This branch does not change the frozen V7R/V8 outcomes, old manuscripts,
the existing Bayesian game, other open Draft PRs or any submitted claim.
Avoid treating a Shapley accounting convention as a new ecological law.
