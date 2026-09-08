# Pseudomonas stutzeri published reciprocal-invasion receipt v1

Status: **Lane A generic game-layer empirical receipt** from published directional tests. This is not Lane P architecture identification.

Primary source:

- Dolinšek, Ramoneda & Johnson (2022), *ISME Communications* 2:77
- DOI: `10.1038/s43705-022-00160-1`
- public-data archive declared by the paper: ERIC DOI `10.25678/0006RZ`

The public archive is reported to contain all experimental data and code. The raw archive bytes were **not** inspected for this receipt; all numerical/sign statements below are restricted to values and tests explicitly reported in the published article.

## 1. Algebraic mapping only

For the purpose of testing the PAYOFF reciprocal-sign logic, define purely algebraic labels

```text
S = complete-denitrification generalist
D = nitrite-only specialist
```

These labels do **not** mean that the generalist is a PAYOFF shared architecture or that the specialist is a PAYOFF differentiated architecture.

The oriented signs are

```text
u = rare D-in-S advantage  = rare specialist can increase in a generalist-rich resident
v = rare S-in-D advantage  = rare generalist can increase in a specialist-rich resident.
```

Only sign/phase logic is used. No common numerical payoff scale is reconstructed.

## 2. Why the first three transfers are the correct fixed-resident window

The authors explicitly used the first three serial transfers for reciprocal initial-ratio tests because this was the fewest number of transfers permitting their trend test while minimizing the probability that genetic or phenotypic changes emerged.

Each 1:100 transfer corresponds to approximately `6.644` generations, so the reciprocal-invasion window is about

```text
3 * 6.644 = 19.932 generations.
```

This is the appropriate published window for a frozen two-type sign receipt.

## 3. Published starting-frequency support

The article reports initial `log10(r_S/G)` values. Converting with

```text
p_D = r_S/G / (1 + r_S/G)
    = 10^log10(r_S/G) / (1 + 10^log10(r_S/G))
```

gives the following approximate specialist frequencies.

### pH 6.5 — strong nitrite toxicity

```text
generalist rare assays:
log10(r_S/G) =  3.23 -> p_D ~= 0.999412
log10(r_S/G) =  1.98 -> p_D ~= 0.989637

specialist rare assays:
log10(r_S/G) = -3.19 -> p_D ~= 0.000645
log10(r_S/G) = -2.65 -> p_D ~= 0.002234
```

### pH 7.5 — weak nitrite toxicity

```text
generalist rare assays:
log10(r_S/G) =  2.98 -> p_D ~= 0.998954
log10(r_S/G) =  2.12 -> p_D ~= 0.992471

specialist rare assays:
log10(r_S/G) = -3.33 -> p_D ~= 0.000468
log10(r_S/G) = -2.13 -> p_D ~= 0.007359
```

The authors kept total initial cell density constant across these composition treatments.

## 4. pH 6.5: both oriented invasion signs are positive

When the generalist was rare, `log(r_S/G)` decreased over the first three transfers:

```text
Mann-Kendall tau = -1
p = 0.042
```

so rare generalists increased relative to specialists:

```text
v > 0.
```

When the specialist was rare, `log(r_S/G)` increased over the first three transfers:

```text
Mann-Kendall tau = +1
p = 0.042
```

so rare specialists increased relative to generalists:

```text
u > 0.
```

Therefore the oriented-sign pair is

```text
(u,v) = (positive, positive).
```

Under the declared two-strategy PAYOFF phase map this certifies the strict sign phase

```text
stable_architecture_coexistence
```

with one important naming guardrail: here this means **generic two-type reciprocal invasion / protected coexistence**, not empirical coexistence of shared versus differentiated trait architectures.

Receipt label:

```text
PSTUTZERI_PH65_GENERIC_RECIPROCAL_INVASION_COEXISTENCE_RECOVERED
```

## 5. pH 7.5: one oriented sign is positive and the other is unresolved

When the generalist was rare, `log(r_S/G)` again decreased:

```text
Mann-Kendall tau = -1
p = 0.042
```

so

```text
v > 0.
```

When the specialist was rare, however, the article reports no significant trend:

```text
Mann-Kendall tau = 0.67
p = 0.31.
```

This is coded as

```text
u = unresolved
```

—not as `u<0` and not as `u=0`.

The new qualitative partial-identification map therefore leaves only

```text
stable_architecture_coexistence
shared_dominance
```

as compatible strict PAYOFF sign phases, with a reciprocal-invasion boundary also compatible.

It excludes

```text
coordination_bistability
differentiated_dominance.
```

Under the purely algebraic mapping used here, `shared_dominance` corresponds to generalist dominance. The word `shared` is not an empirical architecture claim.

Receipt label:

```text
PSTUTZERI_PH75_GENERIC_RECIPROCAL_PHASE_PARTIALLY_IDENTIFIED
```

## 6. Long-term pH 6.5 dynamics violate a frozen-game extrapolation

The short reciprocal-invasion window is not the whole story.

For the 12-transfer experiment at pH 6.5 (approximately 80 generations), co-cultures rapidly approached a similar ratio over the first few transfers, but treatments started with rare specialists later diverged as the generalist acquired altered nitrite-consumption phenotypes.

The clearest reported example starts at

```text
log10(r_S/G) = -3.19
specialist frequency ~= 6.4e-4.
```

The specialist rose to

```text
0.41
```

after the first three transfers, then declined to

```text
0.08
```

after the remaining nine transfers.

The authors isolated evolved generalist phenotypes and linked initial composition to later phenotypic diversification. Their model required introduction of an evolved generalist phenotype to recreate the long-term deviation.

For PAYOFF this is a useful empirical boundary result:

```text
short pre-evolution window:
    reciprocal sign phase is identifiable;

long evolutionary window:
    the resident/type payoff map itself changes,
    so a fixed (phi,eta) game should not be extrapolated unchanged.
```

Receipt label:

```text
PSTUTZERI_LONG_WINDOW_FIXED_GAME_ASSUMPTION_NOT_SUPPORTED
```

This is not a failure of the short-window reciprocal-invasion result. It is evidence that the estimand must include a declared evolutionary time horizon.

## 7. What has and has not been recovered

Recovered:

```text
real reciprocal initial-ratio design at near-endpoint frequencies
real bidirectional rare-type increase at pH 6.5
set-valued partial phase at pH 7.5
real context dependence of reciprocal invasion
real long-window breakdown of fixed-type extrapolation through generalist evolution
```

Not recovered:

```text
numerical phi
numerical eta
a no-refit affine Delta(p) validation
finite-population fixation
recurrent-mutation occupancy
PAYOFF S/D architecture mapping
historical SCH->BITA mechanism
```

Current programme labels:

```text
LANE_A_GENERIC_RECIPROCAL_INVASION_LOGIC_EMPIRICALLY_RECOVERED
PSTUTZERI_PH65_GENERIC_RECIPROCAL_INVASION_COEXISTENCE_RECOVERED
PSTUTZERI_PH75_GENERIC_RECIPROCAL_PHASE_PARTIALLY_IDENTIFIED
PSTUTZERI_LONG_WINDOW_FIXED_GAME_ASSUMPTION_NOT_SUPPORTED
PSTUTZERI_ERIC_RAW_ARCHIVE_NOT_YET_INSPECTED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```
