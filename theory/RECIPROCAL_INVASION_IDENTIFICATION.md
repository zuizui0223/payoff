# Reciprocal invasion identifies the PAYOFF phase directly

Status: exact algebra for the canonical deterministic two-architecture PAYOFF game.
This is an identification theorem and software adapter, not a new empirical result.

## 1. Two PAYOFF-owned observations

For differentiated frequency `p`,

```text
Delta(p)=pi_D-pi_S=phi+eta(2p-1).
```

Define the two oriented rare-invasion margins

```text
u = D advantage when rare in an S resident = Delta(0)  = phi-eta,
v = S advantage when rare in a D resident = -Delta(1) = -phi-eta.
```

Therefore, on one common positive payoff/growth scale,

```text
phi = (u-v)/2,
eta = -(u+v)/2.
```

The map is bijective. Unlike importing `eta` from SCH, BALANCE or BITA, both
observations belong to PAYOFF's population-frequency layer.

## 2. A stronger sign-only result

The strict deterministic phase needs only the signs:

| `u` | `v` | certified phase |
|---|---|---|
| `>0` | `>0` | stable architecture coexistence |
| `<0` | `<0` | coordination bistability |
| `>0` | `<0` | differentiated dominance |
| `<0` | `>0` | shared dominance |

Proof follows immediately from the two pure-boundary vector fields. In particular,
mutual invasion means both pure boundaries repel and hence the unique interior
zero is stable; mutual non-invasion means both pure boundaries attract and the
interior zero is unstable.

This sign theorem does **not** require the two assays to share a magnitude scale.
Unknown assay-specific positive multipliers preserve each sign. Numerical `phi`
and `eta`, equilibrium frequency, distance to a phase boundary, and cross-assay
magnitude comparisons do require one common positive scale.

## 3. Closed bounded-error certificate

Let

```text
u in [u_lo,u_hi],  v in [v_lo,v_hi]
```

be simultaneous closed bounds. A strict phase is certified only when each whole
band has a strict sign. If either interval touches or crosses zero, the software
refuses to promote a strict phase.

When a common scale is declared, the exact feasible set in `(phi,eta)` is the
parallelogram obtained by transforming the four rectangle corners. Its coordinate
projections are

```text
phi in [(u_lo-v_hi)/2, (u_hi-v_lo)/2],
eta in [-(u_hi+v_hi)/2, -(u_lo+v_lo)/2].
```

These marginal bands are reported together with all four exact transformed
vertices so they are not mistaken for an independent rectangular uncertainty set.
A nonzero `eta` is certified whenever its projected interval excludes zero.

## 4. What this closes, and what it does not

This closes a logical gap created by treating `eta` as PAYOFF-owned: there is now
an explicit route from two reciprocal population-level margins to the deterministic
phase, and conditionally to `(phi,eta)`, without using a sister-repository theorem
as evidence for frequency dependence.

It does not show that a particular natural system has performed these invasions.
It does not identify finite-population fixation, recurrent mutation, historical
causation, or mutation support. A positive sister result still cannot substitute
for these reciprocal PAYOFF observations, and reciprocal PAYOFF observations do
not validate SCH conflict, BALANCE middle-world occupancy, or BITA dimensional
release.

## Reproduce

```bash
python -m pytest -q tests/test_reciprocal_invasion_identification.py
```

Implementation: `src/reciprocal_invasion_identification.py`.
Existing forward adapter: `src.payoff_game.invasion_margins`.
