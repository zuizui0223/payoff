# PAYOFF-B Bayesian hysteresis — strictness amendment

Date: **2026-09-26**

## Why this amendment is necessary

The first three-player example used:

- local cue accuracy = 0.90;
- interaction strength = 0.50;
- prior early spring = 0.40.

It correctly produces a degradation cascade and historical non-return under the
declared tie-preserving best-response rule. However, a direct best-response
margin audit shows that after information recovery the two resident players are
exactly indifferent between remaining late and returning to cue-following.

So the old example is a **boundary witness**, not the right representative
example for strict hysteresis.

It is retained for provenance and is not deleted.

## Interior strict witness

Move only the local cue accuracy from 0.90 to **0.875**, leaving interaction
strength at 0.50 and the early-spring prior at 0.40.

Under the complete interaction graph:

- all players initially follow cues;
- migrant cue degradation causes collapse at q = 0.72;
- the low-information state is late/late/late;
- after migrant information returns to q = 1, the system remains
  late/late/follow;
- the alternative follow/follow/follow equilibrium has higher joint payoff.

Most importantly, the recovered late/late/follow state is **strictly** locally
stable. The chosen-policy payoff minus the best unilateral alternative is:

- flower: +0.025;
- local pollinator: +0.025;
- migrant: +0.200.

The history-locked joint-payoff loss relative to the better recovered
equilibrium is about **0.191**.

## Topology contrast at the same interior point

For the chain

    flower -- local pollinator -- migrant

the same cascade occurs at q = 0.72 and recovery again ends at
late/late/follow. The best-response margins are +0.200, +0.025 and +0.200, so
this is also a strict equilibrium. The joint-payoff history-lock loss is about
0.067.

For the two-edge migrant-star

    flower -- migrant -- local pollinator

the same temporary information degradation can collapse all three players, but
restoring migrant information returns the system to follow/follow/follow.

Thus the topology-dependent memory result survives removal of the tie artifact.

## Updated interpretation

The robust candidate statement is:

> A temporary loss of predictive information in a migratory partner can push an
> interaction network into a strictly self-maintaining timing regime that
> persists after information recovery, and whether that historical state is
> retained depends on who is coupled to whom.

The dedicated phase-diagram workflow now counts only recovered states with
strictly positive unilateral best-response margins as the strongest hysteresis
class.
