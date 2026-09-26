# PAYOFF-B strict Bayesian timing phase diagram

Frozen: **2026-09-26**

## Why the strict rerun matters

The first phase diagram counted pure Bayesian Nash equilibria that could include
exact best-response ties. A direct audit found that the original illustrative
0.90 local-cue / 0.50 interaction cell sat exactly on such a recovery boundary.

The stronger analysis therefore requires every player in the recovered
historical state to have a **strictly positive** payoff margin over its best
unilateral alternative.

## Strict result

The full 451-cell grid was rerun for three interaction topologies.

| topology | eligible | resident cascade | any hysteresis | lower-payoff hysteresis | **strict lower-payoff hysteresis** |
|---|---:|---:|---:|---:|---:|
| complete | 391 | 221 | 201 | 121 | **118** |
| chain | 364 | 194 | 174 | 55 | **52** |
| migrant-star | 404 | 367 | 14 | 9 | **0** |

Only three complete-graph cells and three chain cells from the old
lower-payoff-hysteresis category were supported solely by exact ties.

By contrast, **all nine** lower-payoff migrant-star cases were tie-supported.
No migrant-star cell in the declared grid retained strict inefficient
hysteresis after information recovery.

## Main mechanistic result

This sharpens the topology result.

A migrant-star can readily transmit a temporary information shock: 367/404
eligible cells show a resident cascade. But after migrant information recovers,
353 of those cells are reversible and none remains in a strictly stable,
lower-joint-payoff timing regime.

The chain has the same number of undirected edges as the migrant-star, but
retains 52 strict lower-payoff hysteresis cells.

Therefore the relevant distinction is not interaction density alone.

> **Network topology determines whether an information shock is merely
> transmitted or is stored as ecological timing memory.**

In the declared three-player model, coupling among destination partners can
convert a transient migrant information loss into a strictly self-maintaining
historical timing state.

## Representative interior witness

The primary illustrative cell is now:

    local cue accuracy   = 0.875
    interaction strength = 0.50
    prior early spring   = 0.40.

Under both complete and chain topologies:

    high information  -> follow/follow/follow
    migrant q <= 0.72 -> late/late/late
    information back -> late/late/follow.

The recovered state has strictly positive unilateral best-response margins.
Under the migrant-star, the same perturbation returns to
follow/follow/follow.

The older 0.90/0.50 example remains documented as a useful boundary example,
but it is no longer the primary strict witness.

## Claim ceiling

The 118/391 and 52/364 quantities are frequencies in a declared synthetic grid,
not estimated natural frequencies.

The strict phase diagram supports a mechanistic prediction about topology and
history dependence. A natural time series showing degradation and recovery of
predictive connectivity is still required before PAYOFF-B can claim empirical
community-level hysteresis.

## Provenance

Workflow run: 36233538599

Artifacts:

- complete: 10903252871, SHA256
  441590e3dbda2404736677573987261c1b46419e1b1e33d7066f920f6ae5df0b
- chain: 10903890021, SHA256
  f569c3e6c0251e674b7df75a13453049686a253b3645967c3d05bd11cef311a0
- migrant-star: 10903113212, SHA256
  2494c55ad5d91e44f2f34dde8e76df47b80342a48f1caa5952670cc3502f13a2
